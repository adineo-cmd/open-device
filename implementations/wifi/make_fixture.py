#!/usr/bin/env python3
"""make_fixture.py — deterministic synthetic fixtures for the wifi parser.

CLEAN-ROOM STATEMENT
Every byte written here is SELF-MADE from the documented field layouts in the
Linux kernel ath10k/ath11k board-data walk (GPL-2.0, read 2026-11-28) and
ddimension/ath11k-board-bin-tool FORMAT.md (read 2026-11-28). No proprietary
payload is copied into this repository and none is needed: the parser under
test reads field layouts, and the layouts are public.

Fixtures written:

  board2_ath11k.bin      two board elements + one regdb element, raw
                         bodies, checksums correct
  board2_ath11k_elf.bin  one board element whose body is an ELF32 wrapper
                         with a single PT_LOAD around the TLV chain
  board2_ath10k.bin      the ath10k magic, one board element, raw body
  board2_bad_checksum.bin one board whose 0x0a word is deliberately wrong
  body_sentinel.bin      a raw body that ends in a (0,0) sentinel followed
                         by zero padding (the trap that yields phantom tags)
  body_overrun.bin       a raw body whose last tag overruns the buffer
  no_magic.bin           an unrecognised buffer (detection negative path)
  truncated.bin          a valid magic followed by a cut-off element

The checksum is computed by the same law the parser checks, so a fixture
that passes proves the two agree, not that the law is right. The law is
proven against real payloads in the spec document, not here.
"""

import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")

PAD = 0x6D


def align4(value):
    """Round a byte count up to the next multiple of four."""
    return (value + 3) & ~3


def xor_checksum(body):
    """Compute the whole-body XOR integrity word with 0x0a read as zero."""
    total = 0
    words = len(body) // 2
    skip = 0x0A // 2
    for index in range(words):
        if index == skip:
            continue
        total ^= struct.unpack_from("<H", body, index * 2)[0]
    return (~total) & 0xFFFF


def tlv(tag, payload):
    """Encode one raw-body TLV: le16 tag, le16 len, payload."""
    return struct.pack("<2H", tag, len(payload)) + payload


def body_with_checksum(tags):
    """Build a raw body from (tag, payload) pairs and fix its checksum."""
    body = bytearray()
    for tag, payload in tags:
        body += tlv(tag, payload)
    if len(body) < 0x0C:
        body += bytes(0x0C - len(body))
    word = xor_checksum(bytes(body))
    struct.pack_into("<H", body, 0x0A, word)
    return bytes(body)


def sub_element(sub_id, payload):
    """Encode one {le32 id, le32 len} sub-element with 4-byte alignment."""
    out = struct.pack("<2I", sub_id, len(payload)) + payload
    out += bytes(align4(len(payload)) - len(payload))
    return out


def element(element_id, payload):
    """Encode one top-level {le32 id, le32 len} element, 4-byte aligned."""
    out = struct.pack("<2I", element_id, len(payload)) + payload
    out += bytes(align4(len(payload)) - len(payload))
    return out


def container(magic, elements):
    """Wrap elements in the magic field and return the file bytes."""
    field = align4(len(magic) + 1)
    head = magic + b"\x00"
    head += bytes(field - len(head) - 1)
    head += bytes([PAD]) * (field - len(head))
    return head + b"".join(elements)


def board_element(name, body):
    """Encode a board element: one name sub-element then one data sub-element."""
    return element(0, sub_element(0, name) + sub_element(1, body))


def regdb_element(name, data):
    """Encode a regdb element: one name sub-element then one data sub-element."""
    return element(1, sub_element(0, name) + sub_element(1, data))


def simple_body(seed, tag_count=6):
    """Build a small raw body whose payloads are derived from a seed byte."""
    tags = []
    for index in range(1, tag_count + 1):
        payload = bytes(((seed + index * 7 + k) & 0xFF) for k in range(16))
        tags.append((index, payload))
    return body_with_checksum(tags)


def elf_wrap(body):
    """Wrap a raw body in a minimal ELF32 with one PT_LOAD at offset 1024."""
    ehsize = 52
    phentsize = 32
    phnum = 1
    phoff = ehsize
    data_off = 1024
    ident = b"\x7fELF" + bytes([1, 1, 1]) + bytes(9)
    header = struct.pack(
        "<16sHHIIIIIHHHHHH",
        ident, 2, 40, 1, 0x8000, phoff, 0, 0,
        ehsize, phentsize, phnum, 40, 0, 0,
    )
    phdr = struct.pack(
        "<8I", 1, data_off, 0x1000, 0x1000, len(body), len(body), 6, 1024
    )
    out = bytearray(header + phdr)
    out += bytes(data_off - len(out))
    out += body
    return bytes(out)


def body_sentinel():
    """Build a body whose chain ends at a (0,0) sentinel then zero padding."""
    tags = [(1, bytes(16)), (2, bytes(16)), (3, bytes(16))]
    body = bytearray()
    for tag, payload in tags:
        body += tlv(tag, payload)
    struct.pack_into("<H", body, 0x0A, xor_checksum(bytes(body)))
    body += bytes(64)
    return bytes(body)


def body_overrun():
    """Build a body whose final tag declares more bytes than remain."""
    body = bytearray()
    body += tlv(1, bytes(16))
    body += tlv(2, bytes(16))
    body += struct.pack("<2H", 3, 4000)
    body += bytes(16)
    struct.pack_into("<H", body, 0x0A, xor_checksum(bytes(body)))
    return bytes(body)


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

    body_a = simple_body(0x10, 6)
    body_b = simple_body(0x40, 6)
    regdb = bytes(range(32))
    data = container(
        b"QCA-ATH11K-BOARD",
        [
            board_element(b"bus=ahb,qmi-chip-id=1,qmi-board-id=1", body_a),
            board_element(b"bus=ahb,qmi-chip-id=1,qmi-board-id=2", body_b),
            regdb_element(b"bus=ahb,qmi-chip-id=1,qmi-board-id=1", regdb),
        ],
    )
    paths.append(write("board2_ath11k.bin", data))

    body_elf = simple_body(0x22, 4)
    data = container(
        b"QCA-ATH11K-BOARD",
        [board_element(b"bus=ahb,qmi-chip-id=1,qmi-board-id=9", elf_wrap(body_elf))],
    )
    paths.append(write("board2_ath11k_elf.bin", data))

    body_c = simple_body(0x77, 5)
    data = container(
        b"QCA-ATH10K-BOARD",
        [board_element(b"bus=snoc,qmi-board-id=1,qmi-chip-id=1", body_c)],
    )
    paths.append(write("board2_ath10k.bin", data))

    bad = bytearray(simple_body(0x33, 6))
    struct.pack_into("<H", bad, 0x0A, (struct.unpack_from("<H", bad, 0x0A)[0] + 3) & 0xFFFF)
    data = container(
        b"QCA-ATH11K-BOARD",
        [board_element(b"bus=ahb,qmi-chip-id=1,qmi-board-id=7", bytes(bad))],
    )
    paths.append(write("board2_bad_checksum.bin", data))

    paths.append(write("body_sentinel.bin", body_sentinel()))
    paths.append(write("body_overrun.bin", body_overrun()))
    paths.append(write("no_magic.bin", b"NOT-A-BOARD-CONTAINER" + bytes(64)))

    good = container(
        b"QCA-ATH11K-BOARD",
        [board_element(b"bus=ahb,qmi-chip-id=1,qmi-board-id=1", simple_body(0x55, 4))],
    )
    paths.append(write("truncated.bin", good[:-12]))
    return paths


def main():
    """Write every fixture and print the paths."""
    for path in write_all():
        sys.stdout.write("%s\n" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
