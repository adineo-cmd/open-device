"""Byte-level parser for the Qualcomm wifi board-data container.

======================================================================
CLEAN-ROOM STATEMENT
Written from published specifications only:

  * Linux kernel drivers/net/wireless/ath/ath11k/core.c and hw.h
    (GPL-2.0), read 2026-11-28. Normative for ATH11K_BOARD_MAGIC,
    struct ath11k_fw_ie {__le32 id; __le32 len; u8 data[];}, the
    ALIGN(ie_len, 4) skip, and the board/regdb element ids.
  * Linux kernel drivers/net/wireless/ath/ath10k/core.c and hw.h
    (GPL-2.0), read 2026-11-28. Normative for ATH10K_BOARD_MAGIC and
    the identical TLV walk.
  * ddimension/ath11k-board-bin-tool FORMAT.md (7,669 B), read
    2026-11-28, for the 0x0a XOR checksum law and the 0x6d pad fill.
  * The repo's own research/fleet/bdwlan-format.md (271 lines) and
    research/fleet/wifi-wpss.md (1,817 lines) for the raw-body TLV
    grammar and the b<->e wrapper relation.

No proprietary code, header, string or payload was read. No payload is
committed. Every byte offset below is quoted from those sources or
verified against a public payload in test_bdwlan_parser.py.

Three layers, and the corpus files only the bottom one:

  container  "QCA-ATH11K-BOARD" / "QCA-ATH10K-BOARD", 20-byte field,
             then {le32 id, le32 len} elements, 4-byte aligned
  element    id 0 = board, id 1 = regdb; each holds
             {le32 id, le32 len} sub-elements, id 0 = ASCII name,
             id 1 = the payload
  body       either a raw TLV chain (the bdwlan.b<NN> files) or an
             ELF32 wrapper whose PT_LOAD segment holds that chain

The module reports structure. It does not decode tag semantics, does not
decompress, and does not claim the checksum is a signature: it is an XOR
integrity word, and this parser only recomputes it.
"""

import hashlib
import struct
import sys

ATH11K_MAGIC = b"QCA-ATH11K-BOARD"
ATH10K_MAGIC = b"QCA-ATH10K-BOARD"
MAGICS = (ATH11K_MAGIC, ATH10K_MAGIC)

TOP_BOARD = 0
TOP_REGDB = 1
SUB_NAME = 0
SUB_DATA = 1

PAD_BYTE = 0x6D
CHECKSUM_OFFSET = 0x0A
ELF_MAGIC = b"\x7fELF"
PT_LOAD = 1

TAG_HEADER = 4


def align4(value):
    """Round a byte count up to the next multiple of four."""
    return (value + 3) & ~3


def magic_field_size(magic):
    """Return the container's magic field width for a magic string.

    The driver computes ``ALIGN(strlen(MAGIC) + 1, 4)``: the string, its
    terminating NUL, then padding to a 4-byte boundary. For both known
    magics (16 characters) that is 20 bytes.
    """
    return align4(len(magic) + 1)


def sniff(data):
    """Return the container magic found at offset 0, or None."""
    for magic in MAGICS:
        if data.startswith(magic):
            return magic
    return None


def xor_checksum(body):
    """Compute the container's whole-body XOR integrity word.

    The word at CHECKSUM_OFFSET is read as zero so the stored value does
    not affect its own recomputation. Trailing bytes, if the body length
    is odd, are not covered: the law is defined over le16 words.
    """
    total = 0
    words = len(body) // 2
    skip = CHECKSUM_OFFSET // 2
    for index in range(words):
        if index == skip:
            continue
        total ^= struct.unpack_from("<H", body, index * 2)[0]
    return (~total) & 0xFFFF


def stored_checksum(body):
    """Return the checksum word stored at offset 0x0a, or None if absent."""
    if len(body) < CHECKSUM_OFFSET + 2:
        return None
    return struct.unpack_from("<H", body, CHECKSUM_OFFSET)[0]


def checksum_verifies(body):
    """Return True when the stored checksum equals the recomputed one."""
    stored = stored_checksum(body)
    if stored is None:
        return False
    return stored == xor_checksum(body)


def walk_container(data):
    """Walk the top-level {le32 id, le32 len} chain of a board-2.bin buffer.

    Returns (magic, field_size, elements) where elements is a list of
    (id, payload_offset, length). Raises ValueError when the magic is
    absent or the chain overruns the buffer, because either means the
    buffer is not this container and a silent partial walk would be a
    lie about what was parsed.
    """
    magic = sniff(data)
    if magic is None:
        raise ValueError("not a wifi board-data container: no known magic")
    field = magic_field_size(magic)
    if len(data) < field:
        raise ValueError("buffer shorter than the magic field")
    offset = field
    elements = []
    while offset + 8 <= len(data):
        element_id, length = struct.unpack_from("<2I", data, offset)
        body = offset + 8
        if body + length > len(data):
            raise ValueError(
                "top-level element at %d declares %d bytes, %d remain"
                % (offset, length, len(data) - body)
            )
        elements.append((element_id, body, length))
        offset = body + align4(length)
    return magic, field, elements


def walk_element(data, payload_offset, length):
    """Walk the {le32 id, le32 len} sub-chain inside one top-level element.

    Returns a list of (id, payload_offset, length). The sub-chain is not
    required to fill its parent exactly: a short tail that cannot hold a
    header is tolerated, because real containers carry 4-byte padding
    there. A sub-element that overruns its parent raises ValueError.
    """
    end = payload_offset + length
    offset = payload_offset
    subs = []
    while offset + 8 <= end:
        sub_id, sub_len = struct.unpack_from("<2I", data, offset)
        sub_body = offset + 8
        if sub_body + sub_len > end:
            raise ValueError(
                "sub-element at %d declares %d bytes, %d remain in parent"
                % (offset, sub_len, end - sub_body)
            )
        subs.append((sub_id, sub_body, sub_len))
        offset = sub_body + align4(sub_len)
    return subs


def pair_board_entries(data, subs):
    """Pair each name sub-element with the data sub-element that follows it.

    Returns a list of (name_bytes, data_offset, data_length). A data
    element with no preceding name is reported with name None rather than
    dropped, so the caller can see the malformation.
    """
    pairs = []
    pending = None
    for sub_id, body, length in subs:
        if sub_id == SUB_NAME:
            pending = data[body:body + length]
        elif sub_id == SUB_DATA:
            pairs.append((pending, body, length))
            pending = None
    return pairs


def elf_load_segment(data, offset, length):
    """Return (file_offset, file_size) of the first PT_LOAD in an ELF32 blob.

    Returns None when the payload is not ELF or has no PT_LOAD. The header
    is unpacked as the full 13-field ELF32 Ehdr, so e_phentsize is index 9
    and e_phnum is index 10: reading index 9 as the count walks 32 headers
    instead of 1 and yields a nonsense p_filesz.
    """
    blob = data[offset:offset + length]
    if not blob.startswith(ELF_MAGIC):
        return None
    header = struct.unpack_from("<16sHHIIIIIHHHHHH", blob, 0)
    phoff = header[5]
    phentsize = header[9]
    phnum = header[10]
    for index in range(phnum):
        base = phoff + index * phentsize
        if base + 32 > len(blob):
            break
        p_type, p_offset, _vaddr, _paddr, p_filesz, _memsz, _flags, _align = (
            struct.unpack_from("<8I", blob, base)
        )
        if p_type == PT_LOAD:
            return (offset + p_offset, p_filesz)
    return None


def walk_tags(body):
    """Walk the raw TLV tag chain that fills a board body.

    Returns (tags, stop_reason) where tags is a list of (tag, length,
    offset) and stop_reason is one of:

      "sentinel"  a (0, 0) header was reached: the chain ends here
      "overrun"   a header declared more bytes than remain
      "eof"       the chain filled the buffer exactly

    The (0, 0) stop is not optional. Zero-filled payloads parse as an
    unbounded (0, 0) chain, so a walker that does not stop there reports
    hundreds of phantom tags for a body that has tens.
    """
    offset = 0
    tags = []
    while offset + TAG_HEADER <= len(body):
        tag, length = struct.unpack_from("<2H", body, offset)
        if tag == 0 and length == 0:
            return tags, "sentinel"
        if offset + TAG_HEADER + length > len(body):
            return tags, "overrun"
        tags.append((tag, length, offset))
        offset += TAG_HEADER + length
    return tags, "eof"


def resolve_body(data, offset, length):
    """Return (body_offset, body_length) for a board payload, unwrapping ELF.

    A raw body is returned unchanged. An ELF32 wrapper is reduced to its
    PT_LOAD segment, which is the container this module then walks.
    """
    segment = elf_load_segment(data, offset, length)
    if segment is None:
        return (offset, length)
    return segment


def parse(data):
    """Parse a wifi board-data container into a plain dict.

    The returned dict carries the magic, the element counts, and per board
    entry: the ASCII name, the raw body size, whether the body is ELF
    wrapped, the tag chain and the checksum result. It never contains
    payload bytes, only lengths, offsets and booleans.
    """
    magic, field, elements = walk_container(data)
    board_count = 0
    regdb_count = 0
    boards = []
    regdbs = []
    for element_id, payload_offset, length in elements:
        subs = walk_element(data, payload_offset, length)
        if element_id == TOP_BOARD:
            for name, body_off, body_len in pair_board_entries(data, subs):
                board_count += 1
                raw = data[body_off:body_off + body_len]
                wrapped = raw.startswith(ELF_MAGIC)
                body_off2, body_len2 = resolve_body(data, body_off, body_len)
                body = data[body_off2:body_off2 + body_len2]
                tags, stop = walk_tags(body)
                boards.append({
                    "name": name.decode("ascii", "replace") if name else None,
                    "wrapper_bytes": body_len,
                    "elf_wrapped": wrapped,
                    "body_bytes": len(body),
                    "tag_count": len(tags),
                    "max_tag": max((t for t, _l, _o in tags), default=0),
                    "stop": stop,
                    "checksum_ok": checksum_verifies(body),
                })
        elif element_id == TOP_REGDB:
            for name, body_off, body_len in pair_board_entries(data, subs):
                regdb_count += 1
                regdbs.append({
                    "name": name.decode("ascii", "replace") if name else None,
                    "bytes": body_len,
                    "md5": hashlib.md5(data[body_off:body_off + body_len]).hexdigest(),
                })
    return {
        "magic": magic.decode("ascii", "replace"),
        "magic_field": field,
        "bytes": len(data),
        "top_elements": len(elements),
        "boards": board_count,
        "regdbs": regdb_count,
        "board_entries": boards,
        "regdb_entries": regdbs,
    }


def format_report(result):
    """Render a parse result as a short human-readable text block."""
    lines = []
    lines.append("magic        %s" % result["magic"])
    lines.append("magic field  %d bytes" % result["magic_field"])
    lines.append("file         %d bytes" % result["bytes"])
    lines.append("top elements %d" % result["top_elements"])
    lines.append("boards       %d" % result["boards"])
    lines.append("regdbs       %d" % result["regdbs"])
    for entry in result["board_entries"]:
        lines.append(
            "  board %-56s wrap %6d body %6d tags %2d max %2d %-8s csum %s"
            % (
                (entry["name"] or "<no name>")[:56],
                entry["wrapper_bytes"],
                entry["body_bytes"],
                entry["tag_count"],
                entry["max_tag"],
                entry["stop"],
                "ok" if entry["checksum_ok"] else "BAD",
            )
        )
    for entry in result["regdb_entries"]:
        lines.append(
            "  regdb %-56s %6d bytes md5 %s"
            % ((entry["name"] or "<no name>")[:56], entry["bytes"], entry["md5"][:12])
        )
    return "\n".join(lines)


def main(argv):
    """Command-line entry point: parse each path and print a report."""
    if len(argv) < 2:
        sys.stderr.write("usage: bdwlan_parser.py FILE [FILE ...]\n")
        return 2
    status = 0
    for path in argv[1:]:
        with open(path, "rb") as handle:
            data = handle.read()
        try:
            result = parse(data)
        except ValueError as exc:
            sys.stderr.write("%s: %s\n" % (path, exc))
            status = 1
            continue
        sys.stdout.write("%s\n" % path)
        sys.stdout.write(format_report(result))
        sys.stdout.write("\n")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
