#!/usr/bin/env python3
"""make_fixture.py — deterministic synthetic fixtures for the boot-family parser.

Every byte written here is SELF-MADE from the documented field layouts in
AOSP platform/system/tools/mkbootimg include/bootimg/bootimg.h (Apache-2.0,
fetched 2026-11-26) and AOSP platform/external/avb avbtool.py (Apache-2.0,
fetched 2026-11-26). No proprietary payload is copied into this repository
and none is needed: the parser under test reads field layouts, and the field
layouts are public.

Fixtures written:

  boot_v0.img            v0 header, page 2048, kernel+ramdisk+second, no
                         recovery dtbo, no dtb          (the pre-2018 shape)
  boot_v2.img            v2 header, page 4096, kernel+ramdisk+dtb
  boot_v3.img            v3 header, 1580-byte header, fixed 4096 page
  boot_v4.img            v4 header, 1584-byte header, + boot signature
  boot_v4_der_tail.img   v4 header with a DER SEQUENCE appended after the
                         signature (the shape a real AOSP test fixture has)
  vendor_boot_v3.img     vendor_boot v3, 2112-byte header, dtb section
  vendor_boot_v4.img     vendor_boot v4, 2128-byte header, 2 ramdisk table
                         entries + bootconfig
  vbmeta_rsa4096.img     AVB0 vbmeta, SHA256_RSA4096, one HASH descriptor
                         whose digest is real over the payload it names
  dt_table_multi.img     dt_table, 3 entries, FDT magic at each dtb_offset
  dt_table_single.img    dt_table, 1 entry, total_size == file size
  dtbo_with_avb.img      dt_table + AVB footer + AVB0 vbmeta + real digests
  elf32_multi.bin        two concatenated ELF32 headers (the xbl_s.melf shape)
  elf64.bin              one ELF64 header with one PT_LOAD covering e_entry
  garbage.bin            an unrecognised buffer (detection negative path)
  truncated_boot.img     a v0 header cut short (error path)

Regeneration is byte-exact: bodies are deterministic counter streams seeded
per fixture, so re-running reproduces every file bit-for-bit.
"""

import hashlib
import os
import struct

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")

BOOT_MAGIC = b"ANDROID!"
VENDOR_BOOT_MAGIC = b"VNDRBOOT"
AVB_MAGIC = b"AVB0"
AVB_FOOTER_MAGIC = b"AVBf"
DT_TABLE_MAGIC = 0xD7B7AB1E
FDT_MAGIC = b"\xd0\x0d\xfe\xed"
ELF_MAGIC = b"\x7fELF"


def stream(seed, length):
    out = bytearray()
    counter = 0
    while len(out) < length:
        out += hashlib.sha256(seed + counter.to_bytes(8, "little")).digest()
        counter += 1
    return bytes(out[:length])


def round_up(value, page):
    return (value + page - 1) // page * page


def build_boot_v0(kernel_size=5000, ramdisk_size=3000, second_size=1000,
                  page_size=2048, name=b"synth", cmdline=b"console=ttyS0"):
    header = bytearray(1632)
    header[0:8] = BOOT_MAGIC
    struct.pack_into("<10I", header, 8,
                     kernel_size, 0x00008000, ramdisk_size, 0x01000000,
                     second_size, 0x00f00000, 0x00000100, page_size,
                     0, 0)
    header[48:48 + len(name)] = name
    header[64:64 + len(cmdline)] = cmdline
    header[576:608] = stream(b"id-v0", 32)
    kernel = stream(b"k-v0", kernel_size)
    ramdisk = stream(b"r-v0", ramdisk_size)
    second = stream(b"s-v0", second_size)
    out = bytes(header).ljust(page_size, b"\x00")
    out += kernel.ljust(round_up(kernel_size, page_size), b"\x00")
    out += ramdisk.ljust(round_up(ramdisk_size, page_size), b"\x00")
    out += second.ljust(round_up(second_size, page_size), b"\x00")
    return out


def build_boot_v2(kernel_size=6000, ramdisk_size=4000, dtb_size=2048, page_size=4096):
    header = bytearray(1660)
    header[0:8] = BOOT_MAGIC
    struct.pack_into("<10I", header, 8,
                     kernel_size, 0x00008000, ramdisk_size, 0x01000000,
                     0, 0x00f00000, 0x00000100, page_size, 2, 0)
    header[48:53] = b"synth"
    header[64:76] = b"console=ttyS0"
    struct.pack_into("<I", header, 1632, 0)
    struct.pack_into("<Q", header, 1636, 0)
    struct.pack_into("<I", header, 1648, dtb_size)
    struct.pack_into("<Q", header, 1652, 0x01f00000)
    out = bytes(header).ljust(page_size, b"\x00")
    out += stream(b"k-v2", kernel_size).ljust(round_up(kernel_size, page_size), b"\x00")
    out += stream(b"r-v2", ramdisk_size).ljust(round_up(ramdisk_size, page_size), b"\x00")
    out += stream(b"d-v2", dtb_size).ljust(round_up(dtb_size, page_size), b"\x00")
    return out


def pack_os_version(major, minor, patch, year, month):
    return (((major & 0x7F) << 25) | ((minor & 0x7F) << 18)
            | ((patch & 0x7F) << 11) | (((year - 2000) & 0x7F) << 4)
            | (month & 0xF))


def build_boot_v3(kernel_size=5000, ramdisk_size=2500, page_size=4096,
                  os_version=None):
    if os_version is None:
        os_version = pack_os_version(14, 0, 0, 2024, 3)
    header = bytearray(1580)
    header[0:8] = BOOT_MAGIC
    struct.pack_into("<4I", header, 8, kernel_size, ramdisk_size, os_version, 1580)
    struct.pack_into("<I", header, 40, 3)
    header[44:44 + 11] = b"console=tty"
    out = bytes(header).ljust(page_size, b"\x00")
    out += stream(b"k-v3", kernel_size).ljust(round_up(kernel_size, page_size), b"\x00")
    out += stream(b"r-v3", ramdisk_size).ljust(round_up(ramdisk_size, page_size), b"\x00")
    return out


def build_boot_v4(kernel_size=4096, ramdisk_size=2048, signature_size=4096,
                  page_size=4096, der_tail=False):
    header = bytearray(1584)
    header[0:8] = BOOT_MAGIC
    struct.pack_into("<4I", header, 8, kernel_size, ramdisk_size, 0, 1584)
    struct.pack_into("<I", header, 40, 4)
    header[44:54] = b"console=tt"
    struct.pack_into("<I", header, 1580, signature_size)
    out = bytes(header).ljust(page_size, b"\x00")
    out += stream(b"k-v4", kernel_size).ljust(round_up(kernel_size, page_size), b"\x00")
    out += stream(b"r-v4", ramdisk_size).ljust(round_up(ramdisk_size, page_size), b"\x00")
    out += stream(b"sig-v4", signature_size)
    if der_tail:
        body = stream(b"der", 250)
        out += b"\x30\x82" + len(body).to_bytes(2, "big") + body
    return out


def build_vendor_boot_v3(vendor_ramdisk_size=3000, dtb_size=1024, page_size=4096):
    header = bytearray(2112)
    header[0:8] = VENDOR_BOOT_MAGIC
    struct.pack_into("<5I", header, 8, 3, page_size, 0x00008000, 0x01000000,
                     vendor_ramdisk_size)
    header[28:39] = b"console=tty"
    struct.pack_into("<I", header, 2076, 0x00000100)
    header[2080:2085] = b"synth"
    struct.pack_into("<2I", header, 2096, 2112, dtb_size)
    struct.pack_into("<Q", header, 2104, 0x01f00000)
    out = bytes(header).ljust(page_size, b"\x00")
    out += stream(b"vr-v3", vendor_ramdisk_size).ljust(round_up(vendor_ramdisk_size, page_size), b"\x00")
    out += stream(b"vd-v3", dtb_size).ljust(round_up(dtb_size, page_size), b"\x00")
    return out


def build_vendor_boot_v4(vendor_ramdisk_size=2000, dtb_size=512,
                         bootconfig_size=300, page_size=4096):
    header = bytearray(2128)
    header[0:8] = VENDOR_BOOT_MAGIC
    struct.pack_into("<5I", header, 8, 4, page_size, 0x00008000, 0x01000000,
                     vendor_ramdisk_size)
    header[28:39] = b"console=tty"
    struct.pack_into("<I", header, 2076, 0x00000100)
    header[2080:2085] = b"synth"
    entry_size = 108
    entry_num = 2
    table_size = entry_size * entry_num
    struct.pack_into("<2I", header, 2096, 2128, dtb_size)
    struct.pack_into("<Q", header, 2104, 0x01f00000)
    struct.pack_into("<4I", header, 2112, table_size, entry_num, entry_size,
                     bootconfig_size)

    table = bytearray(table_size)
    struct.pack_into("<3I", table, 0, 1000, 0, 1)
    table[12:12 + 8] = b"platform"
    struct.pack_into("<3I", table, entry_size, 1000, 1000, 3)
    table[entry_size + 12:entry_size + 12 + 5] = b"dlkm"

    out = bytes(header).ljust(page_size, b"\x00")
    out += stream(b"vr-v4", vendor_ramdisk_size).ljust(round_up(vendor_ramdisk_size, page_size), b"\x00")
    out += stream(b"vd-v4", dtb_size).ljust(round_up(dtb_size, page_size), b"\x00")
    out += bytes(table).ljust(round_up(table_size, page_size), b"\x00")
    out += stream(b"bc-v4", bootconfig_size)
    return out


def build_dt_table(entry_sizes, page_size=2048, pad_to=None):
    entry_size = 32
    count = len(entry_sizes)
    entries_offset = 32
    blob_offset = entries_offset + count * entry_size
    entries = bytearray()
    blobs = bytearray()
    cursor = blob_offset
    for index, size in enumerate(entry_sizes):
        dtb = FDT_MAGIC + stream(b"fdt%d" % index, size - 4)
        entries += struct.pack(">4I", size, cursor, index, 0)
        entries += struct.pack(">4I", 0, 0, 0, 0)
        blobs += dtb
        cursor += size
    total = blob_offset + len(blobs)
    header = struct.pack(">8I", DT_TABLE_MAGIC, total, 32, entry_size, count,
                         entries_offset, page_size, 0)
    out = header + bytes(entries) + bytes(blobs)
    if pad_to:
        out = out.ljust(pad_to, b"\x00")
    return out


def build_vbmeta(payload, partition_name=b"boot", algorithm_type=2):
    salts = {"name": partition_name}
    salt = hashlib.sha256(b"avb-salt-" + partition_name).digest()
    digest = hashlib.sha256(salt + payload).digest()
    signature = stream(b"avb-sig", 512)
    public_key = stream(b"avb-key", 1032)

    name_len = len(partition_name)
    hash_payload = 116 + name_len + 32 + 32
    hash_desc = struct.pack("!QQ", 2, hash_payload)
    hash_desc += struct.pack("!Q", len(payload))
    hash_desc += b"sha256".ljust(32, b"\x00")
    hash_desc += struct.pack("!4L", name_len, 32, 32, 0)
    hash_desc += bytes(60)
    hash_desc += partition_name
    hash_desc += salt
    hash_desc += digest
    if len(hash_desc) != 16 + hash_payload:
        raise ValueError("descriptor length %d != declared %d"
                         % (len(hash_desc), 16 + hash_payload))

    aux_header_size = 48
    key_offset = aux_header_size
    meta_offset = key_offset + len(public_key)
    desc_offset = meta_offset + 64
    aux = struct.pack("!6Q", key_offset, len(public_key), meta_offset, 64,
                      desc_offset, len(hash_desc))
    aux += public_key
    aux += bytes(64)
    aux += hash_desc
    aux_size = len(aux)
    if aux_size != desc_offset + len(hash_desc):
        raise ValueError("aux size %d != %d" % (aux_size, desc_offset + len(hash_desc)))

    auth = digest
    auth += signature
    auth += bytes(576 - len(auth))
    if len(auth) != 576:
        raise ValueError("auth size %d != 576" % len(auth))

    header = bytearray(256)
    header[0:4] = AVB_MAGIC
    struct.pack_into("!2L", header, 4, 1, 0)
    struct.pack_into("!2Q", header, 12, len(auth), aux_size)
    struct.pack_into("!L", header, 28, algorithm_type)
    struct.pack_into("!2Q", header, 32, 0, 32)
    struct.pack_into("!2Q", header, 48, 32, 512)
    struct.pack_into("!2Q", header, 64, key_offset, len(public_key))
    struct.pack_into("!2Q", header, 80, meta_offset, 64)
    struct.pack_into("!2Q", header, 96, desc_offset, len(hash_desc))
    struct.pack_into("!Q", header, 112, 0)
    struct.pack_into("!2L", header, 120, 0, 0)
    header[128:128 + 13] = b"avbtool 1.2.0"
    if len(header) != 256:
        raise ValueError("header size %d != 256" % len(header))
    header = bytes(header)

    stored = hashlib.sha256(header + aux).digest()
    auth = stored + auth[32:]
    return header + auth + aux


def build_avb_footer(original_image_size, vbmeta_offset, vbmeta_size):
    return struct.pack("!4s2LQQQ", AVB_FOOTER_MAGIC, 1, 0, original_image_size,
                       vbmeta_offset, vbmeta_size) + bytes(28)


def build_dtbo_with_avb(entry_sizes=(1024, 2048), pad_to=65536):
    table = build_dt_table(entry_sizes)
    footer_offset = pad_to - 64
    probe = build_vbmeta(b"\x00" * 1024, partition_name=b"dtbo")
    vbmeta_size = len(probe)
    vbmeta_offset = footer_offset - vbmeta_size
    image_size = vbmeta_offset
    body = table.ljust(image_size, b"\x00")
    vbmeta = build_vbmeta(body, partition_name=b"dtbo")
    if len(vbmeta) != vbmeta_size:
        raise ValueError("vbmeta size depends on payload length")
    out = body + vbmeta + build_avb_footer(image_size, vbmeta_offset, vbmeta_size)
    return out.ljust(pad_to, b"\x00")


def build_elf32_multi():
    def one(machine, entry, base_seed):
        ident = bytearray(16)
        ident[0:4] = ELF_MAGIC
        ident[4] = 1
        ident[5] = 1
        ident[6] = 1
        header = bytes(ident)
        header += struct.pack("<HHIIIIIHHHHHH", 2, machine, 1, entry,
                              52, 0, 0, 52, 32, 1, 40, 0, 0)
        phdr = struct.pack("<IIIIIIII", 1, 0x100, 0x10000, 0x10000,
                           0x200, 0x200, 5, 4)
        body = stream(base_seed, 0x200)
        return header + phdr + body

    outer = one(1, 0x10010, b"elf-outer")
    inner = one(243, 0x10020, b"elf-inner")
    return outer + inner


def build_elf64():
    ident = bytearray(16)
    ident[0:4] = ELF_MAGIC
    ident[4] = 2
    ident[5] = 1
    ident[6] = 1
    header = bytes(ident)
    header += struct.pack("<HHIQQQIHHHHHH", 2, 183, 1, 0x400000,
                          64, 0, 0, 64, 56, 1, 64, 0, 0)
    phdr = struct.pack("<IIQQQQQQ", 1, 5, 0, 0x400000, 0x400000,
                       0x300, 0x300, 0x1000)
    body = stream(b"elf64-body", 0x300)
    return header + phdr + body


def write_all():
    os.makedirs(FIXTURE_DIR, exist_ok=True)
    files = {
        "boot_v0.img": build_boot_v0(),
        "boot_v2.img": build_boot_v2(),
        "boot_v3.img": build_boot_v3(),
        "boot_v4.img": build_boot_v4(),
        "boot_v4_der_tail.img": build_boot_v4(der_tail=True),
        "vendor_boot_v3.img": build_vendor_boot_v3(),
        "vendor_boot_v4.img": build_vendor_boot_v4(),
        "dt_table_multi.img": build_dt_table((1024, 2048, 512)),
        "dt_table_single.img": build_dt_table((4096,)),
        "dtbo_with_avb.img": build_dtbo_with_avb(),
        "elf32_multi.bin": build_elf32_multi(),
        "elf64.bin": build_elf64(),
        "garbage.bin": stream(b"garbage", 4096),
        "truncated_boot.img": build_boot_v0()[:100],
    }
    payload = stream(b"vbmeta-payload", 8192)
    files["vbmeta_rsa4096.img"] = build_vbmeta(payload)
    written = []
    for name, data in sorted(files.items()):
        path = os.path.join(FIXTURE_DIR, name)
        with open(path, "wb") as handle:
            handle.write(data)
        written.append((name, len(data), hashlib.sha256(data).hexdigest()))
    return written


if __name__ == "__main__":
    for name, size, digest in write_all():
        print("%-24s %8d  %s" % (name, size, digest))
