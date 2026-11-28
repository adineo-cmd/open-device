# `wifi` — the board-data container, byte level

**Clean-room statement.** This directory contains no proprietary code, headers,
strings or payload. Its sources are the public GPL-2.0 Linux kernel
`drivers/net/wireless/ath/{ath10k,ath11k}`, the public
`ddimension/ath11k-board-bin-tool` `FORMAT.md`, and this repository's own
committed research. No vendor binary was disassembled to produce it.

Issue #836. Evidence classed `[F]` fact / `[I]` inference / `[H]` hypothesis /
`[N]` negative / `[U]` unknown. All remote references verified **2026-11-28**.

The specification, the census and the honest remainder are in
`research/fleet/wifi-family-spec.md`. This README covers only what the code
here does.

## What is here

| file | purpose |
|---|---|
| `bdwlan_parser.py` | stdlib-only parser for the container, the board/regdb element layer, the ELF32 wrapper and the raw TLV tag chain |
| `make_fixture.py` | deterministic synthetic fixtures, written from the documented layouts |
| `test_bdwlan_parser.py` | 49 tests, 3 of which run against real payloads when `BDWLAN_FIXTURE_REAL` is set |

No payload is committed. Every fixture extension (`.bin`) is gitignored, so the
suite calls `make_fixture.write_all()` in `setUpModule` and a clean checkout
regenerates the fixtures on the fly.

## Run it

```
python3 -I implementations/wifi/test_bdwlan_parser.py
BDWLAN_FIXTURE_REAL=/path/to/board-2.bin/dir python3 -I implementations/wifi/test_bdwlan_parser.py
python3 -I implementations/wifi/bdwlan_parser.py FILE
```

## The three layers

```
container  "QCA-ATH11K-BOARD" / "QCA-ATH10K-BOARD", 20-byte field
           then { le32 id , le32 len , data , pad-to-4 }
             id 0 = board element, id 1 = regdb element
element    inside, { le32 id , le32 len } again
             id 0 = ASCII name, id 1 = payload
body       a raw TLV chain { le16 tag , le16 len , payload } repeated,
           or an ELF32 wrapper whose single PT_LOAD holds that chain
```

The parser reports structure and never guesses meaning: it does not say what
tag 8 *is*, only that it is 11,580 bytes at a known offset and that its length
is identical on both ath11k generations.

## The four traps the tests encode

1. **The `(0,0)` sentinel.** Zero-filled payloads parse as an unbounded
   `(0,0)` chain. A walker that does not stop at `(0,0)` reports 71 and 79
   "tags" for bodies that have 33 to 36. `test_sentinel_prevents_phantom_tags`
   asserts the difference explicitly.
2. **The ELF32 `e_phnum` index.** In the 13-field format string
   `"<16sHHIIIIIHHHHHH"`, `e_phentsize` is index 9 and `e_phnum` is index 10.
   Reading index 9 as the count walks 32 headers instead of 1 and yields a
   nonsense `p_filesz`.
3. **The 4-byte alignment.** The driver skips `ALIGN(len, 4)`, not `len`. On
   the three payloads measured, top-level lengths are already multiples of 4,
   so the align never fires there — the fill byte `0x6d` is observed only at
   the board sub-level. A test that asserted `0x6d` at top level would pass
   vacuously.
4. **The `0x0a` checksum.** It is `~(XOR of every le16 word)` with the word at
   `0x0a` itself read as zero. Including it makes the law fail on every file.

## What this parser does not do

- It does not verify a signature. The container carries none; integrity is the
  XOR word only, and that is not a signature.
- It does not decode tag semantics, decompress, or interpret the body beyond
  its TLV framing.
- It does not claim the corpus rows have this internal layout. The byte-level
  verification is on three upstream `linux-firmware` `board-2.bin` files; the
  corpus connection is by size and name, and `research/fleet/wifi-family-spec.md`
  §8.1 says so.
