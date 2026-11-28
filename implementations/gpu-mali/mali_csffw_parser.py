#!/usr/bin/env python3
"""Byte-level parser for the ARM Mali CSF firmware container.

======================================================================
CLEAN-ROOM STATEMENT
Written from published specifications only:

  * Linux kernel drivers/gpu/drm/panthor/panthor_fw.c (GPL-2.0), read
    2026-11-28, 45,236 B. Normative for CSF_FW_BINARY_HEADER_MAGIC
    (0xc3f13a6e), struct panthor_fw_binary_hdr, the CSF_FW_BINARY_ENTRY_*
    bit macros, enum panthor_fw_binary_entry_type, struct
    panthor_fw_binary_section_entry_hdr, and the panthor_fw_load_entry()
    walk terminated at hdr.size.
  * leegao/panthor2kbase, src/emulator/lifted_csffw.c and .h, read
    2026-11-28. Cited for the observation that the section table, not a
    hardcoded offset, locates the vector table. Its hardcoded constants
    are deliberately NOT used here: see research/fleet/gpu-mali-csffw.md
    section 4, where they are measured to fail on 5 of 5 payloads.

No proprietary code, header, string or payload was read. No payload is
committed. Every byte offset below is quoted from those sources or verified
against a public payload in test_mali_csffw_parser.py.

Three layers, and the corpus files only the outermost:

  header   20 B: u32 magic | u8 minor | u8 major | u16 pad1
            u32 version_hash | u32 pad2 | u32 hdr_size
  entry    u32 ehdr: bits[7:0] type, bits[15:8] size,
            bit30 UPDATE, bit31 OPTIONAL. Walked while offset < hdr_size.
  section  type 0 body: u32 flags | u32 va_start | u32 va_end
            | u32 data_start | u32 data_end

The critical reading, and the one a naive parser gets wrong, is that
hdr_size is the DESCRIPTOR TABLE length and not the file length. On every
payload measured, hdr_size is under 900 B while the file is a quarter of a
megabyte.

The module reports structure. It does not decode the CSF instruction set,
does not decompress, and does not interpret entry types 5, 7, 8 and 9,
whose meaning is not established by any source read here.
"""

import struct
import sys

CSF_FW_MAGIC = 0xC3F13A6E
HEADER_SIZE = 20

ENTRY_TYPE_IFACE = 0
ENTRY_TYPE_CONFIG = 1
ENTRY_TYPE_FUTF_TEST = 2
ENTRY_TYPE_TRACE_BUFFER = 3
ENTRY_TYPE_TIMELINE_METADATA = 4
ENTRY_TYPE_BUILD_INFO_METADATA = 6

TYPE_NAMES = {
    ENTRY_TYPE_IFACE: "IFACE",
    ENTRY_TYPE_CONFIG: "CONFIG",
    ENTRY_TYPE_FUTF_TEST: "FUTF_TEST",
    ENTRY_TYPE_TRACE_BUFFER: "TRACE_BUFFER",
    ENTRY_TYPE_TIMELINE_METADATA: "TIMELINE_METADATA",
    ENTRY_TYPE_BUILD_INFO_METADATA: "BUILD_INFO_METADATA",
}

ENTRY_UPDATE_BIT = 30
ENTRY_OPTIONAL_BIT = 31

SECTION_HEADER_SIZE = 20
BUILD_INFO_HEADER_SIZE = 8
TRACE_HEADER_SIZE = 28


def entry_type(ehdr):
    """Return the entry type from bits [7:0] of the entry header word."""
    return ehdr & 0xFF


def entry_size(ehdr):
    """Return the entry size in bytes from bits [15:8] of the header word."""
    return (ehdr >> 8) & 0xFF


def entry_update(ehdr):
    """Return True when bit 30 (UPDATE) is set on the entry header."""
    return bool(ehdr & (1 << ENTRY_UPDATE_BIT))


def entry_optional(ehdr):
    """Return True when bit 31 (OPTIONAL) is set on the entry header."""
    return bool(ehdr & (1 << ENTRY_OPTIONAL_BIT))


def type_name(value):
    """Return the documented name of an entry type, or None if unknown."""
    return TYPE_NAMES.get(value)


def parse_header(data):
    """Parse the 20-byte firmware binary header.

    Returns a dict with magic, minor, major, pad1, version_hash, pad2 and
    hdr_size. Raises ValueError when the magic is absent or the buffer is
    too short, because either means the buffer is not this container and a
    silent partial parse would be a lie about what was read.
    """
    if len(data) < HEADER_SIZE:
        raise ValueError(
            "buffer is %d bytes, shorter than the %d-byte header"
            % (len(data), HEADER_SIZE)
        )
    magic, minor, major, pad1, version_hash, pad2, hdr_size = struct.unpack_from(
        "<IBBHIII", data, 0
    )
    if magic != CSF_FW_MAGIC:
        raise ValueError(
            "bad magic 0x%08x, expected 0x%08x" % (magic, CSF_FW_MAGIC)
        )
    return {
        "magic": magic,
        "minor": minor,
        "major": major,
        "pad1": pad1,
        "version_hash": version_hash,
        "pad2": pad2,
        "hdr_size": hdr_size,
    }


def walk_entries(data):
    """Walk the descriptor table and return (entries, stop_reason).

    entries is a list of dicts carrying the offset, the header word, the
    type, the size, the two flag bits and the body slice bounds. The walk
    stops when the offset reaches hdr_size, which is the table length and
    not the file length.

    stop_reason is one of:

      "table"    the walk consumed exactly hdr_size bytes
      "short"    hdr_size exceeds the buffer
      "overrun"  an entry declared more bytes than the table has left
      "zero"     an entry declared a size below the 4-byte header

    A zero size is a real failure mode, not a terminator: unlike the wifi
    board-data container there is no (0, 0) sentinel in this format, so a
    zero-length entry means the table is malformed rather than finished.
    """
    header = parse_header(data)
    hdr_size = header["hdr_size"]
    if hdr_size > len(data):
        return [], "short", header
    offset = HEADER_SIZE
    entries = []
    while offset < hdr_size:
        if offset + 4 > hdr_size:
            return entries, "overrun", header
        ehdr = struct.unpack_from("<I", data, offset)[0]
        size = entry_size(ehdr)
        if size < 4:
            return entries, "zero", header
        if offset + size > hdr_size:
            return entries, "overrun", header
        entries.append({
            "offset": offset,
            "ehdr": ehdr,
            "type": entry_type(ehdr),
            "size": size,
            "update": entry_update(ehdr),
            "optional": entry_optional(ehdr),
            "body_start": offset + 4,
            "body_end": offset + size,
        })
        offset += size
    reason = "table" if offset == hdr_size else "overrun"
    return entries, reason, header


def parse_section(data, entry):
    """Parse a type-0 IFACE section body into its five u32 fields.

    Returns a dict with flags, va_start, va_end, data_start and data_end.
    """
    if entry["size"] < 4 + SECTION_HEADER_SIZE:
        raise ValueError(
            "IFACE entry at %d is %d bytes, needs at least %d"
            % (entry["offset"], entry["size"], 4 + SECTION_HEADER_SIZE)
        )
    flags, va_start, va_end, data_start, data_end = struct.unpack_from(
        "<5I", data, entry["body_start"]
    )
    return {
        "flags": flags,
        "va_start": va_start,
        "va_end": va_end,
        "data_start": data_start,
        "data_end": data_end,
    }


def section_name(data, entry):
    """Return the section name, or "" when the entry carries none.

    The 20-byte struct is followed by a name buffer whose length is the rest
    of the entry (the driver computes name_len = entry_size - 24). On every
    real payload measured the first byte of that buffer is 0x00, so the name
    is empty; the remaining bytes hold build-dependent stale data. This
    function therefore returns the text up to the first NUL and never
    interprets the tail as a second address range.
    """
    start = entry["body_start"] + SECTION_HEADER_SIZE
    raw = data[start:entry["body_end"]]
    nul = raw.find(b"\x00")
    name_bytes = raw[:nul] if nul >= 0 else raw
    return name_bytes.decode("ascii", "replace")


def parse_trace_buffer(data, entry):
    """Parse a type-3 TRACE_BUFFER body.

    The grammar, verified on 40 of 40 entries across five payloads, is:

        u32 flags | u32 va[5] | u32 value | ASCII name, NUL-terminated

    The name runs from offset 28 to the end of the entry and is zero-padded,
    so it is cut at the first NUL. Returns a dict with flags, the five
    virtual addresses, value and the decoded name.
    """
    if entry["size"] < 4 + TRACE_HEADER_SIZE:
        raise ValueError(
            "TRACE_BUFFER entry at %d is %d bytes, needs at least %d"
            % (entry["offset"], entry["size"], 4 + TRACE_HEADER_SIZE)
        )
    flags = struct.unpack_from("<I", data, entry["body_start"])[0]
    addresses = list(struct.unpack_from("<5I", data, entry["body_start"] + 4))
    value = struct.unpack_from("<I", data, entry["body_start"] + 24)[0]
    raw = data[entry["body_start"] + TRACE_HEADER_SIZE:entry["body_end"]]
    nul = raw.find(b"\x00")
    name_bytes = raw[:nul] if nul >= 0 else raw
    return {
        "flags": flags,
        "addresses": addresses,
        "value": value,
        "name": name_bytes.decode("ascii", "replace"),
        "name_printable": all(32 <= byte < 127 for byte in name_bytes) and bool(name_bytes),
    }


def parse_build_info(data, entry):
    """Parse a type-6 BUILD_INFO_METADATA body into (meta_start, meta_size)."""
    if entry["size"] < 4 + BUILD_INFO_HEADER_SIZE:
        raise ValueError(
            "BUILD_INFO entry at %d is %d bytes, needs at least %d"
            % (entry["offset"], entry["size"], 4 + BUILD_INFO_HEADER_SIZE)
        )
    meta_start, meta_size = struct.unpack_from("<2I", data, entry["body_start"])
    return {"meta_start": meta_start, "meta_size": meta_size}


def build_info_text(data):
    """Return the ASCII build-info string, or None when absent.

    The metadata is plain text of the form ``git_sha: <40 hex chars> \\0``
    at offset hdr_size. It is public provenance metadata about the build,
    not payload content.
    """
    header = parse_header(data)
    entries, _reason, _header = walk_entries(data)
    for entry in entries:
        if entry["type"] == ENTRY_TYPE_BUILD_INFO_METADATA:
            info = parse_build_info(data, entry)
            start = info["meta_start"]
            end = start + info["meta_size"]
            if end > len(data):
                return None
            raw = data[start:end]
            nul = raw.find(b"\x00")
            return (raw[:nul] if nul >= 0 else raw).decode("ascii", "replace")
    return None


def vector_table(data):
    """Return (initial_sp, reset_handler) from the section with va_start 0.

    The vector table is located structurally: it is the type-0 section whose
    virtual range begins at address zero. This is the correction to the
    prior art, which hardcodes file offset 0x001124; that offset is unmapped
    by the section table on all five payloads measured, and reading it yields
    ASCII text in the reset-handler field.

    Returns None when no section claims address zero.
    """
    entries, _reason, _header = walk_entries(data)
    for entry in entries:
        if entry["type"] != ENTRY_TYPE_IFACE:
            continue
        section = parse_section(data, entry)
        if section["va_start"] != 0:
            continue
        start = section["data_start"]
        end = section["data_end"]
        if end <= start or end > len(data):
            continue
        initial_sp = struct.unpack_from("<I", data, start)[0]
        reset = struct.unpack_from("<I", data, start + 4)[0]
        return (initial_sp, reset)
    return None


def sections(data):
    """Return the list of parsed type-0 sections, in table order."""
    entries, _reason, _header = walk_entries(data)
    result = []
    for entry in entries:
        if entry["type"] == ENTRY_TYPE_IFACE:
            parsed = parse_section(data, entry)
            parsed["entry_offset"] = entry["offset"]
            result.append(parsed)
    return result


def data_end_max(data):
    """Return the largest data_end across type-0 sections, or 0.

    This is the format's real integrity field. On every payload measured,
    max(data_end) equals the file size exactly, while hdr_size does not.
    """
    highest = 0
    for section in sections(data):
        if section["data_end"] > highest:
            highest = section["data_end"]
    return highest


def integrity_ok(data):
    """Return True when max(data_end) equals the buffer length."""
    return data_end_max(data) == len(data)


def union_coverage(data):
    """Return (union_bytes, unclaimed_bytes) for the section data ranges.

    Sections alias: two virtual ranges can point at one file range, so the
    sum of per-section lengths over-counts. The union of distinct ranges is
    the honest figure, and the difference from the file size is the header,
    the descriptor table and page padding.
    """
    ranges = sorted({
        (section["data_start"], section["data_end"])
        for section in sections(data)
        if section["data_end"] > section["data_start"]
    })
    covered = 0
    position = 0
    for start, end in ranges:
        if start > position:
            covered += end - start
            position = end
        elif end > position:
            covered += end - position
            position = end
    return covered, len(data) - covered


def parse(data):
    """Parse a Mali CSF firmware container into a plain dict.

    The returned dict carries the header fields, the entry counts by type,
    the section table, the build-info string and the integrity result. It
    never contains payload bytes, only lengths, offsets and booleans.
    """
    entries, stop, header = walk_entries(data)
    counts = {}
    for entry in entries:
        counts[entry["type"]] = counts.get(entry["type"], 0) + 1
    parsed_sections = []
    for entry in entries:
        if entry["type"] == ENTRY_TYPE_IFACE:
            section = parse_section(data, entry)
            section["entry_offset"] = entry["offset"]
            parsed_sections.append(section)
    traces = []
    for entry in entries:
        if entry["type"] == ENTRY_TYPE_TRACE_BUFFER:
            traces.append(parse_trace_buffer(data, entry))
    covered, unclaimed = union_coverage(data)
    return {
        "bytes": len(data),
        "magic": header["magic"],
        "major": header["major"],
        "minor": header["minor"],
        "version_hash": header["version_hash"],
        "hdr_size": header["hdr_size"],
        "entries": len(entries),
        "stop": stop,
        "type_counts": counts,
        "sections": parsed_sections,
        "traces": traces,
        "build_info": build_info_text(data),
        "data_end_max": data_end_max(data),
        "integrity_ok": integrity_ok(data),
        "covered": covered,
        "unclaimed": unclaimed,
        "vector": vector_table(data),
    }


def format_report(result):
    """Render a parse result as a short human-readable text block."""
    lines = []
    lines.append("magic        0x%08x" % result["magic"])
    lines.append("version      %d.%d  hash 0x%08x"
                 % (result["major"], result["minor"], result["version_hash"]))
    lines.append("file         %d bytes" % result["bytes"])
    lines.append("hdr_size     %d bytes (descriptor table)" % result["hdr_size"])
    lines.append("entries      %d  stop %s" % (result["entries"], result["stop"]))
    lines.append("sections     %d" % len(result["sections"]))
    lines.append("data_end max %d  integrity %s"
                 % (result["data_end_max"], "ok" if result["integrity_ok"] else "BAD"))
    lines.append("covered      %d  unclaimed %d" % (result["covered"], result["unclaimed"]))
    if result["vector"] is not None:
        lines.append("vector       sp 0x%08x reset 0x%08x" % result["vector"])
    if result["build_info"]:
        lines.append("build info   %s" % result["build_info"])
    for entry_type in sorted(result["type_counts"]):
        name = type_name(entry_type) or "type-%d" % entry_type
        lines.append("  %-20s %d" % (name, result["type_counts"][entry_type]))
    for section in result["sections"]:
        lines.append(
            "  section off %4d flags 0x%08x va[0x%08x,0x%08x) data[%d,%d)"
            % (
                section["entry_offset"],
                section["flags"],
                section["va_start"],
                section["va_end"],
                section["data_start"],
                section["data_end"],
            )
        )
    for trace in result["traces"]:
        lines.append(
            "  trace %-20s flags 0x%08x value %3d"
            % (trace["name"][:20], trace["flags"], trace["value"])
        )
    return "\n".join(lines)


def main(argv):
    """Command-line entry point: parse each path and print a report."""
    if len(argv) < 2:
        sys.stderr.write("usage: mali_csffw_parser.py FILE [FILE ...]\n")
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
