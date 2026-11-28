"""Byte-level parser for the four container grammars filed under blob_family=boot.

======================================================================
CLEAN-ROOM STATEMENT
Written from published specifications only:

  * AOSP platform/system/tools/mkbootimg, include/bootimg/bootimg.h
    (Apache-2.0), fetched 2026-11-26, 433 lines. Normative for the
    Android boot image v0-v4 and vendor_boot v3-v4 layouts, the
    BOOT_MAGIC / VENDOR_BOOT_MAGIC strings, and the field sizes.
  * AOSP platform/external/avb, avbtool.py (Apache-2.0), fetched
    2026-11-26, 207,502 B. Normative for the AVB0 header, the AVBf
    footer, the descriptor tags and the two verification laws.
  * AOSP platform/system/tools/mkdtimg, libufdt, and the repo's own
    research/fleet/boot-dtb.md (751 lines) for the dt_table layout.
  * The repo's own research/qualcomm/docs/bootchain-census.md for the
    Qualcomm ELF/multi-ELF observations.

No proprietary code, header, string or payload was read. No payload is
committed. Every byte offset below is either quoted from the documents
above or verified against a public payload in test_bootimg_parser.py.
======================================================================

Four grammars, not one. The corpus files 26 distinct filenames into
blob_family=boot, but they are four unrelated containers:

  ANDROID!  Android boot image v0-v4     boot.img recovery.img init_boot.img
  VNDRBOOT  Android vendor_boot v3-v4    vendor_boot.img
  AVB0/AVBf Android Verified Boot        vbmeta.img, appended to dtbo/boot
  dt_table  device-tree table            dtbo.img dtb.img
  ELF       ELF32/ELF64, incl. multi-ELF xbl.img abl.img tzsw.img shrm.img ...

This module detects which one a buffer is and parses it. It never
decompresses and never verifies a signature it cannot verify without a
trust root: it reports what is present.
"""

import hashlib
import struct
import sys

BOOT_MAGIC = b"ANDROID!"
VENDOR_BOOT_MAGIC = b"VNDRBOOT"
AVB_MAGIC = b"AVB0"
AVB_FOOTER_MAGIC = b"AVBf"
DT_TABLE_MAGIC = 0xD7B7AB1E
ELF_MAGIC = b"\x7fELF"
FDT_MAGIC = b"\xd0\x0d\xfe\xed"

BOOT_IMAGE_HEADER_V3_SIZE = 1580
BOOT_IMAGE_HEADER_V4_SIZE = 1584
VENDOR_BOOT_IMAGE_HEADER_V3_SIZE = 2112
VENDOR_BOOT_IMAGE_HEADER_V4_SIZE = 2128
VENDOR_RAMDISK_TABLE_ENTRY_V4_SIZE = 108
AVB_VBMETA_HEADER_SIZE = 256
AVB_FOOTER_SIZE = 64
AVB_DESCRIPTOR_HEADER_SIZE = 16
AVB_DESCRIPTOR_RESERVED = 60
AVB_HASH_FIXED = 56
AVB_HASHTREE_FIXED = 120
AVB_DESCRIPTOR_FIXED = AVB_HASH_FIXED
DT_TABLE_HEADER_SIZE = 32
DT_TABLE_ENTRY_SIZE = 32

AVB_ALGORITHM_NAMES = {
    0: "NONE",
    1: "SHA256_RSA2048",
    2: "SHA256_RSA4096",
    3: "SHA256_RSA8192",
    4: "SHA512_RSA2048",
    5: "SHA512_RSA4096",
    6: "SHA512_RSA8192",
}

AVB_DESCRIPTOR_TAGS = {
    0: "PROPERTY",
    1: "HASHTREE",
    2: "HASH",
    3: "KERNEL_CMDLINE",
    4: "CHAIN_PARTITION",
}

DT_TABLE_ENTRY_NAMES = ("dtb_size", "dtb_offset", "id", "rev")


class ParseError(ValueError):
    pass


def _need(data, n, what):
    if len(data) < n:
        raise ParseError("%s needs %d bytes, buffer is %d" % (what, n, len(data)))


def _round_up(value, page):
    if page <= 0:
        raise ParseError("page size must be positive, got %d" % page)
    return (value + page - 1) // page * page


def detect_format(data):
    """Return the grammar name for a buffer, or None if unrecognised.

    Order matters: a boot image with an AVB footer appended still starts
    with ANDROID!, so magic-at-zero is tested before the trailing footer.
    """
    if len(data) >= 8 and data[0:8] == BOOT_MAGIC:
        return "boot_image"
    if len(data) >= 8 and data[0:8] == VENDOR_BOOT_MAGIC:
        return "vendor_boot_image"
    if len(data) >= 4 and data[0:4] == ELF_MAGIC:
        return "elf"
    if len(data) >= 4 and data[0:4] == AVB_MAGIC:
        return "avb_vbmeta"
    if len(data) >= 4:
        (word,) = struct.unpack_from(">I", data, 0)
        if word == DT_TABLE_MAGIC:
            return "dt_table"
    if len(data) >= AVB_FOOTER_SIZE and data[-AVB_FOOTER_SIZE:-AVB_FOOTER_SIZE + 4] == AVB_FOOTER_MAGIC:
        return "avb_footer_only"
    return None


def parse_boot_image(data):
    """Parse an Android boot image, header v0 through v4.

    v0/v1/v2 carry the page size in the header and put the kernel one page
    in. v3/v4 have a fixed 4096-byte page and a 1580/1584-byte header, and
    v4 appends a boot signature after the ramdisk.
    """
    _need(data, 8, "boot image magic")
    if data[0:8] != BOOT_MAGIC:
        raise ParseError("not a boot image: magic %r" % data[0:8])

    page_size_field, = struct.unpack_from("<I", data, 36)
    header_version_field, = struct.unpack_from("<I", data, 40)

    if page_size_field == 0 or page_size_field > 65536:
        header_version = header_version_field if header_version_field in (3, 4) else 0
        page_size = 4096
    else:
        header_version = header_version_field
        page_size = page_size_field

    if header_version >= 3:
        return _parse_boot_image_v3_v4(data, header_version, page_size)
    return _parse_boot_image_v0_v2(data, header_version, page_size)


def _parse_boot_image_v0_v2(data, header_version, page_size):
    _need(data, 1632, "boot_img_hdr_v0")
    (kernel_size, kernel_addr, ramdisk_size, ramdisk_addr,
     second_size, second_addr, tags_addr, page_size,
     hdr_version, os_version) = struct.unpack_from("<10I", data, 8)
    name = data[48:64].split(b"\x00")[0].decode("ascii", "replace")
    cmdline = data[64:576].split(b"\x00")[0].decode("ascii", "replace")
    image_id = data[576:608]
    extra_cmdline = data[608:1632].split(b"\x00")[0].decode("ascii", "replace")

    result = {
        "format": "boot_image",
        "header_version": hdr_version,
        "header_size": 1632 if hdr_version == 0 else (1648 if hdr_version == 1 else 1660),
        "page_size": page_size,
        "kernel_size": kernel_size,
        "kernel_addr": kernel_addr,
        "ramdisk_size": ramdisk_size,
        "ramdisk_addr": ramdisk_addr,
        "second_size": second_size,
        "second_addr": second_addr,
        "tags_addr": tags_addr,
        "os_version_raw": os_version,
        "os_version": decode_os_version(os_version),
        "name": name,
        "cmdline": cmdline,
        "extra_cmdline": extra_cmdline,
        "id": image_id.hex(),
        "sections": [],
    }

    offset = page_size
    result["sections"].append(("kernel", offset, kernel_size))
    offset += _round_up(kernel_size, page_size)
    result["sections"].append(("ramdisk", offset, ramdisk_size))
    offset += _round_up(ramdisk_size, page_size)
    if second_size:
        result["sections"].append(("second", offset, second_size))
        offset += _round_up(second_size, page_size)

    if hdr_version >= 1:
        _need(data, 1648, "boot_img_hdr_v1")
        recovery_dtbo_size, = struct.unpack_from("<I", data, 1632)
        recovery_dtbo_offset, = struct.unpack_from("<Q", data, 1636)
        result["recovery_dtbo_size"] = recovery_dtbo_size
        result["recovery_dtbo_offset"] = recovery_dtbo_offset
        if recovery_dtbo_size:
            result["sections"].append(("recovery_dtbo", offset, recovery_dtbo_size))
            offset += _round_up(recovery_dtbo_size, page_size)

    if hdr_version >= 2:
        _need(data, 1660, "boot_img_hdr_v2")
        dtb_size, = struct.unpack_from("<I", data, 1648)
        dtb_addr, = struct.unpack_from("<Q", data, 1652)
        result["dtb_size"] = dtb_size
        result["dtb_addr"] = dtb_addr
        if dtb_size:
            result["sections"].append(("dtb", offset, dtb_size))
            offset += _round_up(dtb_size, page_size)

    result["computed_end"] = offset
    result["trailing_bytes"] = len(data) - offset
    result["trailing"] = _describe_trailing(data, offset)
    return result


def _parse_boot_image_v3_v4(data, header_version, page_size):
    need = BOOT_IMAGE_HEADER_V4_SIZE if header_version >= 4 else BOOT_IMAGE_HEADER_V3_SIZE
    _need(data, need, "boot_img_hdr_v%d" % header_version)
    kernel_size, ramdisk_size, os_version, header_size = struct.unpack_from("<4I", data, 8)
    reserved = struct.unpack_from("<4I", data, 24)
    hdr_version, = struct.unpack_from("<I", data, 40)
    cmdline = data[44:44 + 1536].split(b"\x00")[0].decode("ascii", "replace")

    result = {
        "format": "boot_image",
        "header_version": hdr_version,
        "header_size": header_size,
        "page_size": page_size,
        "kernel_size": kernel_size,
        "ramdisk_size": ramdisk_size,
        "os_version_raw": os_version,
        "os_version": decode_os_version(os_version),
        "reserved": reserved,
        "cmdline": cmdline,
        "sections": [],
    }

    offset = page_size
    result["sections"].append(("kernel", offset, kernel_size))
    offset += _round_up(kernel_size, page_size)
    result["sections"].append(("ramdisk", offset, ramdisk_size))
    offset += _round_up(ramdisk_size, page_size)

    if header_version >= 4:
        signature_size, = struct.unpack_from("<I", data, 1580)
        result["signature_size"] = signature_size
        if signature_size:
            result["sections"].append(("boot_signature", offset, signature_size))
            offset += signature_size

    result["computed_end"] = offset
    result["trailing_bytes"] = len(data) - offset
    result["trailing"] = _describe_trailing(data, offset)
    return result


def _describe_trailing(data, offset):
    """Classify bytes past the computed end. Reported, never guessed away."""
    if offset >= len(data):
        return None
    tail = data[offset:]
    if len(tail) >= 4 and tail[0] == 0x30 and tail[1] == 0x82:
        total = 4 + int.from_bytes(tail[2:4], "big")
        return {
            "kind": "der_sequence",
            "bytes": len(tail),
            "der_total": total,
            "der_covers_tail": total == len(tail),
        }
    if len(tail) >= AVB_FOOTER_SIZE and tail[-AVB_FOOTER_SIZE:-AVB_FOOTER_SIZE + 4] == AVB_FOOTER_MAGIC:
        return {"kind": "avb_footer", "bytes": len(tail)}
    return {"kind": "unknown", "bytes": len(tail), "first16": tail[:16].hex()}


def parse_vendor_boot_image(data):
    """Parse an Android vendor_boot image, header v3 or v4."""
    _need(data, VENDOR_BOOT_IMAGE_HEADER_V3_SIZE, "vendor_boot_img_hdr_v3")
    if data[0:8] != VENDOR_BOOT_MAGIC:
        raise ParseError("not a vendor_boot image: magic %r" % data[0:8])
    header_version, page_size, kernel_addr, ramdisk_addr, vendor_ramdisk_size = \
        struct.unpack_from("<5I", data, 8)
    cmdline = data[28:28 + 2048].split(b"\x00")[0].decode("ascii", "replace")
    tags_addr, = struct.unpack_from("<I", data, 2076)
    name = data[2080:2096].split(b"\x00")[0].decode("ascii", "replace")
    header_size, dtb_size = struct.unpack_from("<2I", data, 2096)
    dtb_addr, = struct.unpack_from("<Q", data, 2104)

    result = {
        "format": "vendor_boot_image",
        "header_version": header_version,
        "page_size": page_size,
        "header_size": header_size,
        "kernel_addr": kernel_addr,
        "ramdisk_addr": ramdisk_addr,
        "vendor_ramdisk_size": vendor_ramdisk_size,
        "cmdline": cmdline,
        "tags_addr": tags_addr,
        "name": name,
        "dtb_size": dtb_size,
        "dtb_addr": dtb_addr,
        "vendor_ramdisk_table": [],
        "sections": [],
    }

    offset = page_size
    result["sections"].append(("vendor_ramdisk", offset, vendor_ramdisk_size))
    offset += _round_up(vendor_ramdisk_size, page_size)
    result["sections"].append(("dtb", offset, dtb_size))
    offset += _round_up(dtb_size, page_size)

    if header_version >= 4:
        _need(data, VENDOR_BOOT_IMAGE_HEADER_V4_SIZE, "vendor_boot_img_hdr_v4")
        table_size, entry_num, entry_size, bootconfig_size = struct.unpack_from("<4I", data, 2112)
        result["vendor_ramdisk_table_size"] = table_size
        result["vendor_ramdisk_table_entry_num"] = entry_num
        result["vendor_ramdisk_table_entry_size"] = entry_size
        result["bootconfig_size"] = bootconfig_size
        if entry_num and entry_size >= VENDOR_RAMDISK_TABLE_ENTRY_V4_SIZE:
            for i in range(entry_num):
                base = offset + i * entry_size
                if base + VENDOR_RAMDISK_TABLE_ENTRY_V4_SIZE > len(data):
                    break
                rsize, roff, rtype = struct.unpack_from("<3I", data, base)
                rname = data[base + 12:base + 44].split(b"\x00")[0].decode("ascii", "replace")
                board_id = struct.unpack_from("<16I", data, base + 44)
                result["vendor_ramdisk_table"].append({
                    "ramdisk_size": rsize,
                    "ramdisk_offset": roff,
                    "ramdisk_type": rtype,
                    "ramdisk_name": rname,
                    "board_id": board_id,
                })
        offset += _round_up(table_size, page_size)
        result["sections"].append(("bootconfig", offset, bootconfig_size))
        offset += bootconfig_size

    result["computed_end"] = offset
    result["trailing_bytes"] = len(data) - offset
    result["trailing"] = _describe_trailing(data, offset)
    return result


def decode_os_version(raw):
    """Decode the packed os_version word documented in boot_img_hdr_v3.

    Bits 31:25 major, 24:18 minor, 17:11 patch, 10:4 (year-2000), 3:0 month.
    Returns None when the field is zero, which is what a v0 header carries.
    """
    if raw == 0:
        return None
    return {
        "major": (raw >> 25) & 0x7F,
        "minor": (raw >> 18) & 0x7F,
        "patch": (raw >> 11) & 0x7F,
        "year": 2000 + ((raw >> 4) & 0x7F),
        "month": raw & 0xF,
    }


def parse_avb_vbmeta(data, base=0):
    """Parse an AVB0 vbmeta header and its descriptors.

    The two verification laws are exposed as functions rather than applied
    here, because applying them requires the caller to supply the blob the
    hash covers.
    """
    _need(data, base + AVB_VBMETA_HEADER_SIZE, "AvbVBMetaImageHeader")
    fields = struct.unpack_from("!4s2L2QL2Q2Q2Q2Q2QQLL47s", data, base)
    (magic, ver_major, ver_minor, auth_size, aux_size, algorithm_type,
     hash_offset, hash_size, sig_offset, sig_size, key_offset, key_size,
     meta_offset, meta_size, desc_offset, desc_size, rollback_index,
     flags, rollback_index_location, release) = fields

    if magic != AVB_MAGIC:
        raise ParseError("not a vbmeta header: magic %r" % magic)

    auth_base = base + AVB_VBMETA_HEADER_SIZE
    aux_base = auth_base + auth_size
    result = {
        "format": "avb_vbmeta",
        "version_major": ver_major,
        "version_minor": ver_minor,
        "authentication_data_block_size": auth_size,
        "auxiliary_data_block_size": aux_size,
        "algorithm_type": algorithm_type,
        "algorithm_name": AVB_ALGORITHM_NAMES.get(algorithm_type, "UNKNOWN"),
        "hash_offset": hash_offset,
        "hash_size": hash_size,
        "signature_offset": sig_offset,
        "signature_size": sig_size,
        "public_key_offset": key_offset,
        "public_key_size": key_size,
        "public_key_metadata_offset": meta_offset,
        "public_key_metadata_size": meta_size,
        "descriptors_offset": desc_offset,
        "descriptors_size": desc_size,
        "rollback_index": rollback_index,
        "flags": flags,
        "rollback_index_location": rollback_index_location,
        "release_string": release.split(b"\x00")[0].decode("ascii", "replace"),
        "total_size": AVB_VBMETA_HEADER_SIZE + auth_size + aux_size,
        "descriptors": [],
    }
    result["digest"] = data[auth_base + hash_offset:auth_base + hash_offset + hash_size]
    result["signature"] = data[auth_base + sig_offset:auth_base + sig_offset + sig_size]
    result["public_key"] = data[aux_base + key_offset:aux_base + key_offset + key_size]

    desc = data[aux_base + desc_offset:aux_base + desc_offset + desc_size]
    offset = 0
    while offset + 16 <= len(desc):
        tag, num_bytes = struct.unpack_from("!QQ", desc, offset)
        if num_bytes == 0 or offset + 16 + num_bytes > len(desc):
            break
        entry = {
            "tag": tag,
            "tag_name": AVB_DESCRIPTOR_TAGS.get(tag, "UNKNOWN"),
            "num_bytes_following": num_bytes,
        }
        if tag == 2:
            entry.update(_parse_avb_hash_descriptor(desc, offset, num_bytes))
        elif tag == 1:
            entry.update(_parse_avb_hashtree_descriptor(desc, offset, num_bytes))
        elif tag == 3:
            body = desc[offset + 16:offset + 16 + num_bytes]
            entry["kernel_cmdline"] = body.split(b"\x00")[0].decode("ascii", "replace")
        elif tag == 4:
            body = desc[offset + 16:offset + 16 + num_bytes]
            entry["chain_partition_name"] = body[0:32].split(b"\x00")[0].decode("ascii", "replace")
            entry["chain_public_key"] = body[32:]
        result["descriptors"].append(entry)
        offset += 16 + num_bytes
    return result


def _parse_avb_hash_descriptor(desc, offset, num_bytes):
    """tag 2: image_size, hash_algorithm[32], name_len, salt_len, digest_len, flags."""
    base = offset + 16
    image_size, = struct.unpack_from("!Q", desc, base)
    algorithm = desc[base + 8:base + 40].split(b"\x00")[0].decode("ascii", "replace")
    name_len, salt_len, digest_len, flags = struct.unpack_from("!4L", desc, base + 40)
    cursor = base + AVB_DESCRIPTOR_FIXED + 60
    name = desc[cursor:cursor + name_len].split(b"\x00")[0].decode("ascii", "replace")
    cursor += name_len
    salt = desc[cursor:cursor + salt_len]
    cursor += salt_len
    digest = desc[cursor:cursor + digest_len]
    return {
        "image_size": image_size,
        "hash_algorithm": algorithm,
        "partition_name": name,
        "salt": salt,
        "digest": digest,
        "flags": flags,
        "descriptor_payload": AVB_DESCRIPTOR_FIXED + 60 + name_len + salt_len + digest_len,
    }


def _parse_avb_hashtree_descriptor(desc, offset, num_bytes):
    """tag 1: dm-verity parameters. Offsets per avbtool's FORMAT_STRING."""
    base = offset + 16
    (dm_verity_version, image_size, tree_offset, tree_size,
     data_block_size, hash_block_size, fec_num_roots, fec_offset,
     fec_size) = struct.unpack_from("!LQQQLLLLQQ", desc, base)
    algorithm = desc[base + 52:base + 84].split(b"\x00")[0].decode("ascii", "replace")
    name_len, salt_len, digest_len, flags = struct.unpack_from("!4L", desc, base + 84)
    cursor = base + AVB_HASHTREE_FIXED + 60
    name = desc[cursor:cursor + name_len].split(b"\x00")[0].decode("ascii", "replace")
    cursor += name_len
    salt = desc[cursor:cursor + salt_len]
    cursor += salt_len
    digest = desc[cursor:cursor + digest_len]
    return {
        "dm_verity_version": dm_verity_version,
        "image_size": image_size,
        "tree_offset": tree_offset,
        "tree_size": tree_size,
        "data_block_size": data_block_size,
        "hash_block_size": hash_block_size,
        "fec_num_roots": fec_num_roots,
        "fec_offset": fec_offset,
        "fec_size": fec_size,
        "hash_algorithm": algorithm,
        "partition_name": name,
        "salt": salt,
        "root_digest": digest,
        "flags": flags,
    }


def parse_avb_footer(data, base=None):
    """Parse the 64-byte AVBf footer at the end of a partition."""
    if base is None:
        base = len(data) - AVB_FOOTER_SIZE
    _need(data, base + AVB_FOOTER_SIZE, "AvbFooter")
    magic, ver_major, ver_minor, original_image_size, vbmeta_offset, vbmeta_size = \
        struct.unpack_from("!4s2LQQQ", data, base)
    if magic != AVB_FOOTER_MAGIC:
        raise ParseError("not an AVB footer: magic %r" % magic)
    return {
        "format": "avb_footer",
        "footer_offset": base,
        "version_major": ver_major,
        "version_minor": ver_minor,
        "original_image_size": original_image_size,
        "vbmeta_offset": vbmeta_offset,
        "vbmeta_size": vbmeta_size,
    }


def avb_verify_vbmeta_digest(data, parsed):
    """Law 1: digest == hash(header[0:256] || aux_block).

    Quoted from avbtool.py verify_vbmeta_blob: the header is hashed as-is,
    because the stored digest lives in the authentication block, not the
    header. Returns (ok, computed_hex, stored_hex).
    """
    auth_base = AVB_VBMETA_HEADER_SIZE
    aux_base = auth_base + parsed["authentication_data_block_size"]
    aux_end = aux_base + parsed["auxiliary_data_block_size"]
    header_blob = data[0:AVB_VBMETA_HEADER_SIZE]
    aux_blob = data[aux_base:aux_end]
    computed = hashlib.sha256(header_blob + aux_blob).hexdigest()
    stored = parsed["digest"].hex()
    return computed == stored, computed, stored


def avb_verify_hash_descriptor(image, descriptor):
    """Law 2: digest == hash(salt || image[0:image_size]).

    This is the rule avbtool's HashDescriptor.check_digest applies when it
    hashes a partition's first image_size bytes with the descriptor salt.
    Returns (ok, computed_hex, stored_hex).
    """
    size = descriptor["image_size"]
    if size > len(image):
        raise ParseError("descriptor claims %d bytes, image has %d" % (size, len(image)))
    computed = hashlib.sha256(descriptor["salt"] + image[0:size]).hexdigest()
    stored = descriptor["digest"].hex()
    return computed == stored, computed, stored


def parse_dt_table(data):
    """Parse a dt_table (mkdtimg) container.

    The header is eight big-endian u32:
      magic, total_size, header_size, entry_size, entry_count,
      entries_offset, page_size, version.
    A naive >7I read silently swaps entry_size with entry_count; the field
    order here is the one mkdtimg writes and the one verified on payload.
    """
    _need(data, DT_TABLE_HEADER_SIZE, "dt_table header")
    (magic, total_size, header_size, entry_size, entry_count,
     entries_offset, page_size, version) = struct.unpack_from(">8I", data, 0)
    if magic != DT_TABLE_MAGIC:
        raise ParseError("not a dt_table: magic 0x%08x" % magic)

    result = {
        "format": "dt_table",
        "total_size": total_size,
        "header_size": header_size,
        "entry_size": entry_size,
        "entry_count": entry_count,
        "entries_offset": entries_offset,
        "page_size": page_size,
        "version": version,
        "file_size": len(data),
        "total_size_matches_file": total_size == len(data),
        "entries": [],
    }
    if entry_size < DT_TABLE_ENTRY_SIZE:
        raise ParseError("entry_size %d < %d" % (entry_size, DT_TABLE_ENTRY_SIZE))
    for i in range(entry_count):
        base = entries_offset + i * entry_size
        if base + DT_TABLE_ENTRY_SIZE > len(data):
            break
        dtb_size, dtb_offset, hw_id, hw_rev = struct.unpack_from(">4I", data, base)
        custom = struct.unpack_from(">4I", data, base + 16)
        fdt_ok = (dtb_offset + 4 <= len(data)
                  and data[dtb_offset:dtb_offset + 4] == FDT_MAGIC)
        result["entries"].append({
            "dtb_size": dtb_size,
            "dtb_offset": dtb_offset,
            "id": hw_id,
            "rev": hw_rev,
            "custom": custom,
            "fdt_magic_ok": fdt_ok,
            "bounds_ok": dtb_offset + dtb_size <= len(data),
        })
    return result


def parse_elf_headers(data):
    """Parse ELF32/ELF64 file and program headers, and count concatenated ELFs.

    A Qualcomm xbl.img is several ELFs concatenated (xbl_s.melf); the outer
    one carries a junk machine value, so callers need every inner offset,
    not just the first header.
    """
    _need(data, 16, "ELF ident")
    if data[0:4] != ELF_MAGIC:
        raise ParseError("not ELF: magic %r" % data[0:4])
    ei_class = data[4]
    ei_data = data[5]
    if ei_class not in (1, 2):
        raise ParseError("bad EI_CLASS %d" % ei_class)
    if ei_data not in (1, 2):
        raise ParseError("bad EI_DATA %d" % ei_data)
    is64 = ei_class == 2
    endian = "<" if ei_data == 1 else ">"

    if is64:
        (e_type, e_machine, e_version, e_entry, e_phoff, e_shoff, e_flags,
         e_ehsize, e_phentsize, e_phnum, e_shentsize, e_shnum,
         e_shstrndx) = struct.unpack_from(endian + "HHIQQQIHHHHHH", data, 16)
    else:
        (e_type, e_machine, e_version, e_entry, e_phoff, e_shoff, e_flags,
         e_ehsize, e_phentsize, e_phnum, e_shentsize, e_shnum,
         e_shstrndx) = struct.unpack_from(endian + "HHIIIIIHHHHHH", data, 16)

    program_headers = []
    for i in range(e_phnum):
        base = e_phoff + i * e_phentsize
        if base + e_phentsize > len(data):
            break
        if is64:
            p_type, p_flags, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align = \
                struct.unpack_from(endian + "IIQQQQQQ", data, base)
        else:
            p_type, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_flags, p_align = \
                struct.unpack_from(endian + "IIIIIIII", data, base)
        program_headers.append({
            "p_type": p_type,
            "p_offset": p_offset,
            "p_vaddr": p_vaddr,
            "p_paddr": p_paddr,
            "p_filesz": p_filesz,
            "p_memsz": p_memsz,
            "p_flags": p_flags,
        })

    inner = []
    cursor = 0
    while True:
        found = data.find(ELF_MAGIC, cursor)
        if found < 0:
            break
        inner.append(found)
        cursor = found + 1

    return {
        "format": "elf",
        "class": 64 if is64 else 32,
        "endian": "little" if ei_data == 1 else "big",
        "e_type": e_type,
        "e_machine": e_machine,
        "e_version": e_version,
        "e_entry": e_entry,
        "e_flags": e_flags,
        "e_ehsize": e_ehsize,
        "e_phoff": e_phoff,
        "e_phnum": e_phnum,
        "program_headers": program_headers,
        "elf_magic_offsets": inner,
        "elf_count": len(inner),
        "entry_in_load": any(
            ph["p_type"] == 1 and ph["p_vaddr"] <= e_entry < ph["p_vaddr"] + ph["p_memsz"]
            for ph in program_headers
        ),
    }


def parse(data):
    """Detect the grammar and parse. Returns a dict with a 'format' key.

    An AVB footer is followed when present, because vbmeta is what a caller
    looking at a boot-family partition almost always wants next.
    """
    kind = detect_format(data)
    if kind is None:
        raise ParseError("unrecognised container in %d bytes: first4=%s"
                         % (len(data), data[:4].hex()))
    if kind == "boot_image":
        result = parse_boot_image(data)
    elif kind == "vendor_boot_image":
        result = parse_vendor_boot_image(data)
    elif kind == "elf":
        result = parse_elf_headers(data)
    elif kind == "avb_vbmeta":
        result = parse_avb_vbmeta(data)
    elif kind == "dt_table":
        result = parse_dt_table(data)
    else:
        result = {"format": "avb_footer_only", "footer": parse_avb_footer(data)}

    footer_offset = len(data) - AVB_FOOTER_SIZE
    if footer_offset > 0 and data[footer_offset:footer_offset + 4] == AVB_FOOTER_MAGIC:
        try:
            footer = parse_avb_footer(data)
        except ParseError:
            footer = None
        if footer is not None:
            result["avb_footer"] = footer
            start = footer["vbmeta_offset"]
            end = start + footer["vbmeta_size"]
            if 0 <= start < end <= len(data) and data[start:start + 4] == AVB_MAGIC:
                result["avb_vbmeta"] = parse_avb_vbmeta(data, base=start)
    return result


def _jsonable(value):
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, dict):
        return dict((k, _jsonable(v)) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    return value


def summarise(result):
    """Flatten a parse result into the one line a human wants to read."""
    kind = result.get("format")
    if kind == "boot_image":
        return ("boot_image v%d page=%d kernel=%d ramdisk=%d end=%d trailing=%d"
                % (result["header_version"], result["page_size"],
                   result["kernel_size"], result["ramdisk_size"],
                   result["computed_end"], result["trailing_bytes"]))
    if kind == "vendor_boot_image":
        return ("vendor_boot_image v%d page=%d vendor_ramdisk=%d dtb=%d end=%d"
                % (result["header_version"], result["page_size"],
                   result["vendor_ramdisk_size"], result["dtb_size"],
                   result["computed_end"]))
    if kind == "dt_table":
        good = sum(1 for e in result["entries"] if e["fdt_magic_ok"])
        return ("dt_table entries=%d entry_size=%d fdt_ok=%d/%d total_matches_file=%s"
                % (result["entry_count"], result["entry_size"], good,
                   len(result["entries"]), result["total_size_matches_file"]))
    if kind == "avb_vbmeta":
        return ("avb_vbmeta %s release=%r descriptors=%d"
                % (result["algorithm_name"], result["release_string"],
                   len(result["descriptors"])))
    if kind == "elf":
        return ("elf%d %s machine=%d phdrs=%d elf_count=%d entry_in_load=%s"
                % (result["class"], result["endian"], result["e_machine"],
                   len(result["program_headers"]), result["elf_count"],
                   result["entry_in_load"]))
    return str(kind)


def main(argv):
    """Parse files named on the command line, as text or JSON."""
    import argparse
    import json

    ap = argparse.ArgumentParser(
        description="Parse a boot-family container and report its layout.")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true", help="emit full JSON")
    args = ap.parse_args(argv)

    status = 0
    for path in args.files:
        try:
            with open(path, "rb") as handle:
                data = handle.read()
            result = parse(data)
        except (ParseError, OSError) as exc:
            print("%s: %s" % (path, exc), file=sys.stderr)
            status = 1
            continue
        if args.json:
            print(json.dumps({"path": path, "size": len(data),
                              "parsed": _jsonable(result)}, indent=2))
        else:
            print("%s (%d B): %s" % (path, len(data), summarise(result)))
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
