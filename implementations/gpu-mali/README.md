# `gpu-mali` — the Mali CSF firmware container, byte level

**Clean-room statement.** This directory contains no proprietary code, headers,
strings or payload. Its only source is the public GPL-2.0 Linux kernel
`drivers/gpu/drm/panthor/panthor_fw.c`, read 2026-11-28. No vendor binary was
disassembled to produce it. The third-party project `leegao/panthor2kbase` is
cited in the research note as prior art and corrected there; none of its code
is copied here.

Issue #832. Evidence classed `[F]` fact / `[I]` inference / `[H]` hypothesis /
`[N]` negative / `[U]` unknown. All remote references verified **2026-11-28**.

The specification, the Gate 0 record, the census and the honest negatives are in
`research/fleet/gpu-mali-csffw.md`. This README covers only what the code here
does.

## What is here

| file | purpose |
|---|---|
| `mali_csffw_parser.py` | stdlib-only parser for the header, the entry walk, the IFACE section table, the trace-buffer bodies, the build-info string and the vector table |
| `make_fixture.py` | deterministic synthetic fixtures, written from the documented layouts |
| `test_mali_csffw_parser.py` | 71 tests |

No payload is committed. `.bin` is gitignored, so the suite calls
`make_fixture.write_all()` in `setUpModule` and a clean checkout regenerates the
fixtures on the fly.

## Run it

```
python3 -I implementations/gpu-mali/test_mali_csffw_parser.py
python3 -I implementations/gpu-mali/mali_csffw_parser.py FILE
```

## The three layers

```
header   20 B: u32 magic 0xc3f13a6e | u8 minor | u8 major | u16 pad1
          u32 version_hash | u32 pad2 | u32 hdr_size
entry    u32 ehdr: bits[7:0] type, bits[15:8] size,
          bit30 UPDATE, bit31 OPTIONAL.
          walked from offset 20 while offset < hdr_size, advancing by size
section  type 0 body: u32 flags | u32 va_start | u32 va_end
          | u32 data_start | u32 data_end
          then a name buffer of (entry_size - 24) bytes
```

## The five traps this parser encodes as tests

1. **`hdr_size` is the descriptor table length, not the file length.** Measured
   792–856 B on files of 282,624–344,064 B. A parser that compares `hdr_size`
   to the file size rejects every valid payload.
2. **Advance by `size`, not by an alignment.** The walk lands exactly on
   `hdr_size` on all five payloads, with no slack.
3. **A zero-length section is legitimate.** `data_start == data_end == 0` with
   flags `0x0000002b` is a BSS reservation, present in every generation.
   `arch14.8` additionally carries a degenerate `va_start == va_end` section at
   `0x00420000`. Rejecting either is wrong.
4. **Sections alias.** Two virtual ranges can point at one file range, so
   summing per-section lengths over-counts — 452,576 "covered" bytes in a
   282,624 B file. `union_coverage()` merges distinct ranges instead.
5. **The vector table is found by `va_start == 0`, not by a fixed offset.**
   The correct section is at file offset 4,892–5,060 depending on generation;
   the prior art's hardcoded `0x001124` is unmapped and reads ASCII.

## What this parser deliberately does not do

- It does **not** decode the CSF instruction set. That is the prior art's
  contribution and is not attempted here.
- It does **not** assign meaning to entry types 5, 7, 8 and 9. They appear once
  each, at 8–20 B, with `OPTIONAL` set, and are absent from the driver's enum.
  `parse()` reports their type numbers and `format_report()` prints them as
  `type-5` etc. rather than inventing names.
- It does **not** verify a signature. The container has no signature field;
  integrity is structural, and `integrity_ok()` implements the one real check:
  `max(data_end) == len(file)`.
- It does **not** interpret the cache-mode bits of the IFACE `flags` word. The
  bit positions come from the driver's macros; the semantics of the value do
  not.

## Evidence for the format

`research/fleet/gpu-mali-csffw.md` §2–§5 carries the measurements this code
implements, all against five real `linux-firmware` payloads fetched 2026-11-28.
The corpus connection is by name and size class only, and the corpus sizes
(278,528 / 294,912 B) do not overlap the upstream ones — that limit is stated
in §6.3 and is not papered over here.
