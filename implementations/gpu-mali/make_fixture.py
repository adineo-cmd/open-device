#!/usr/bin/env python3
"""make_fixture.py — deterministic synthetic fixtures for the Mali CSF parser.

CLEAN-ROOM STATEMENT
Every byte written here is SELF-MADE from the documented field layouts in the
Linux kernel panthor driver drivers/gpu/drm/panthor/panthor_fw.c (GPL-2.0, read
2026-11-28). No proprietary payload is copied into this repository and none is
needed: the parser under test reads field layouts, and the layouts are public.

Fixtures written:

  csffw_basic.bin        one of each entry type, two IFACE sections, correct
                         hdr_size, data_end_max equal to the file size
  csffw_trace.bin        two TRACE_BUFFER entries with ASCII names, to exercise
                         the NUL-terminated name grammar
  csffw_zero_section.bin an IFACE section with data_start == data_end == 0, the
                         BSS-style reservation that a naive validator rejects
  csffw_alias.bin        two IFACE sections pointing at the SAME file range, so
                         a naive per-section sum over-counts
  csffw_bad_magic.bin    wrong magic word (detection negative path)
  csffw_short.bin        a valid magic followed by a cut-off entry table
  csffw_zero_entry.bin   an entry declaring size 0, which is malformed in this
                         format because there is no sentinel
  csffw_no_build.bin     a container with no BUILD_INFO entry

The build-info text is a fabricated 40-hex placeholder, not any real commit id.
"""

import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")

MAGIC = 0xC3F13A6E
HEADER_SIZE = 20
PAGE = 4096

FAKE_SHA = "0" * 40


def align_page(value):
    """Round a byte count up to the next 4096-byte boundary."""
    if value == 0:
        return 0
    return ((value + PAGE - 1) // PAGE) * PAGE


def entry(entry_type, body, update=False, optional=False):
    """Encode one entry: header word plus body, total size 4 + len(body).

    The size field is bits [15:8] of the header word, so the whole entry must
    fit in 255 bytes. The fixtures are built to respect that.
    """
    size = 4 + len(body)
    if size > 255:
        raise ValueError("entry size %d exceeds the 8-bit size field" % size)
    ehdr = (entry_type & 0xFF) | ((size & 0xFF) << 8)
    if update:
        ehdr |= 1 << 30
    if optional:
        ehdr |= 1 << 31
    return struct.pack("<I", ehdr) + body


def section_body(flags, va_start, va_end, data_start, data_end, name=b""):
    """Encode a type-0 IFACE section body.

    The body is the 20-byte documented struct (five u32 fields) followed by a
    name buffer. The driver reads name_len = entry_size - 24 bytes there and
    NUL-terminates it; on every real payload measured the first byte is 0x00,
    so the name is empty and the buffer is 8 bytes. This encoder reproduces
    that: five fields plus an 8-byte zero name buffer, giving entry size 32.
    """
    tail = name + bytes(8 - len(name)) if len(name) <= 8 else name
    return struct.pack(
        "<5I", flags, va_start, va_end, data_start, data_end
    ) + tail


def trace_body(flags, addresses, value, name):
    """Encode a type-3 TRACE_BUFFER body: flags, five VAs, value, ASCII name."""
    if len(addresses) != 5:
        raise ValueError("TRACE_BUFFER needs exactly five addresses")
    text = name.encode("ascii")
    out = struct.pack("<I", flags)
    out += struct.pack("<5I", *addresses)
    out += struct.pack("<I", value)
    out += text + b"\x00"
    pad = (-len(out)) % 4
    out += bytes(pad)
    return out


def build_info_body(meta_start, meta_size):
    """Encode a type-6 BUILD_INFO_METADATA body: two u32 fields."""
    return struct.pack("<2I", meta_start, meta_size)


def container(entries, build_text=None, magic=MAGIC, major=0, minor=3,
              version_hash=0x01050000):
    """Assemble a container from encoded entries and return its bytes.

    ``entries`` is either a sequence of encoded entries or one concatenated
    bytes object; both are accepted because the fixtures build them both
    ways. hdr_size is computed as 20 plus the entries, so the descriptor
    table is exactly as long as the walk expects. Section data ranges in the
    caller must be chosen so that max(data_end) equals the final file length.
    """
    if isinstance(entries, (bytes, bytearray)):
        table = bytes(entries)
    else:
        table = b"".join(entries)
    hdr_size = HEADER_SIZE + len(table)
    text = b""
    if build_text is not None:
        text = build_text.encode("ascii") + b"\x00"
    head = struct.pack(
        "<IBBHIII", magic, minor, major, 0, version_hash, 0, hdr_size
    )
    out = bytearray(head + table + text)
    return bytes(out)


def pad_to(data, total):
    """Right-pad a buffer with zeros to a target length."""
    if len(data) > total:
        raise ValueError("buffer already %d bytes, target %d" % (len(data), total))
    return data + bytes(total - len(data))


def write(name, data):
    """Write one fixture and return its path."""
    os.makedirs(FIX, exist_ok=True)
    path = os.path.join(FIX, name)
    with open(path, "wb") as handle:
        handle.write(data)
    return path


def write_all():
    """Regenerate every fixture and return the list of paths written."""
    paths = []

    hdr_size = HEADER_SIZE
    body_a = section_body(0x09, 0x00400000, 0x00410000, 0, 0)
    body_b = section_body(0x09, 0x00410000, 0x00420000, 0, 0)
    text = "git_sha: %s" % FAKE_SHA
    build_body_len = 4 + 8

    def build_parts(data_start_a, data_end_a, data_end_b, vector_start, vector_end, build_at):
        body_a = section_body(0x09, 0x00400000, 0x00410000, data_start_a, data_end_a)
        body_b = section_body(0x09, 0x00410000, 0x00420000, data_end_a, data_end_b)
        body_v = section_body(0x09, 0x00000000, 0x00010000, vector_start, vector_end)
        return [
            entry(0, body_a),
            entry(0, body_b),
            entry(0, body_v),
            entry(1, struct.pack("<I", 0) + b"Log verbosity\x00"),
            entry(3, trace_body(0, [0x00410004, 0x00410008, 0x0041000C,
                                    0x00410010, 0x00410014], 0, "fwutf")),
            entry(4, struct.pack("<I", 0) + b"timeline_header\x00"),
            entry(5, struct.pack("<3I", 1, 2, 3)),
            entry(6, build_info_body(build_at, len(text) + 1)),
            entry(7, struct.pack("<2I", 0x00410000, 0x00411000)),
            entry(8, struct.pack("<I", 0x00410408)),
            entry(9, struct.pack("<I", 1) + struct.pack("<I", 0x0202DE58)),
        ]

    table_len = sum(len(p) for p in build_parts(0, 0, 0, 0, 0, 0))
    build_at = HEADER_SIZE + table_len
    data_start_a = align_page(build_at + len(text) + 1)
    data_end_a = data_start_a + 128
    data_end_b = data_end_a + 256
    vector_start = data_end_b
    vector_end = vector_start + 32
    parts = build_parts(data_start_a, data_end_a, data_end_b, vector_start, vector_end, build_at)
    data = container(parts, build_text=text)
    data = pad_to(data, vector_end)
    data = bytearray(data)
    struct.pack_into("<2I", data, vector_start, 0x02030000, 0x00801FBD)
    paths.append(write("csffw_basic.bin", bytes(data)))

    hdr = HEADER_SIZE
    trace_one = trace_body(0x00000001, [0x00410014, 0x00410018, 0x0041001C,
                                        0x00410020, 0x00410024], 4, "firmware trace")
    trace_two = trace_body(0x00000000, [0x00410050, 0x00410054, 0x00410058,
                                        0x0041005C, 0x004112D4], 1, "timeline")
    sec_off = hdr
    sec_len = 4 + 28
    data_start = align_page(hdr + sec_len + 4 + len(trace_one) + 4 + len(trace_two))
    body = section_body(0x09, 0x00400000, 0x00410000, data_start, data_start + 64)
    entries = entry(0, body) + entry(3, trace_one) + entry(3, trace_two)
    data = container(entries, build_text=None)
    data = pad_to(data, data_start + 64)
    paths.append(write("csffw_trace.bin", data))

    body_zero = section_body(0x2B, 0x03000000, 0x03040000, 0, 0)
    data_start = align_page(hdr + 4 + 28 + 4 + 28)
    body_real = section_body(0x09, 0x00400000, 0x00410000, data_start, data_start + 128)
    entries = entry(0, body_real) + entry(0, body_zero)
    data = container(entries, build_text=None)
    data = pad_to(data, data_start + 128)
    paths.append(write("csffw_zero_section.bin", data))

    shared_start = align_page(hdr + 4 + 28 + 4 + 28)
    shared_end = shared_start + 256
    body_alias_one = section_body(0x09, 0x01000000, 0x01040000, shared_start, shared_end)
    body_alias_two = section_body(0x09, 0x02000000, 0x02040000, shared_start, shared_end)
    entries = entry(0, body_alias_one) + entry(0, body_alias_two)
    data = container(entries, build_text=None)
    data = pad_to(data, shared_end)
    paths.append(write("csffw_alias.bin", data))

    paths.append(write(
        "csffw_bad_magic.bin",
        container([entry(0, section_body(0x09, 0, 0x10000, 0, 0))],
                  build_text=None, magic=0xDEADBEEF),
    ))

    good = container(
        [entry(0, section_body(0x09, 0x00400000, 0x00410000, 0, 0))],
        build_text=None,
    )
    paths.append(write("csffw_short.bin", good[:24]))

    bad = bytearray(container(
        [entry(0, section_body(0x09, 0x00400000, 0x00410000, 0, 0))],
        build_text=None,
    ))
    struct.pack_into("<I", bad, HEADER_SIZE, 0)
    paths.append(write("csffw_zero_entry.bin", bytes(bad)))

    data_start = align_page(hdr + 4 + 28)
    body = section_body(0x09, 0x00400000, 0x00410000, data_start, data_start + 128)
    data = container([entry(0, body)], build_text=None)
    data = pad_to(data, data_start + 128)
    paths.append(write("csffw_no_build.bin", data))

    return paths


def main():
    """Write every fixture and print the paths."""
    for path in write_all():
        sys.stdout.write("%s\n" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
