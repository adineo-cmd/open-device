# `wifi` — one family label, three container grammars, and a checksum that verifies 170/170

Analysis date: 2026-11-28. Analyst: OC-1 (`100milionseek`), issue
[#836](https://github.com/adineo-cmd/open-device/issues/836).

Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data
rows) for the census; three real upstream `board-2.bin` payloads from
`linux-firmware` for byte-level verification; the in-tree normative kernel
source `drivers/net/wireless/ath/{ath10k,ath11k}`; and this repository's own
`research/fleet/bdwlan-format.md` (271 lines) and `research/fleet/wifi-wpss.md`
(1,817 lines).

Every number below is command output. No payload is committed; samples are ≤16
bytes. Evidence classes: `[F]` fact measured by command, `[I]` inference from
measurements, `[H]` hypothesis, `[N]` honest negative, `[U]` unknown.

**Scope warning, stated first `[F]`.** The `wifi` family is **5,642 rows / 418
basenames / 107 devices**. This note does not spec all of it. It specs the
**`bdwlan` board-data container** — 5,120 rows / 370 basenames / 73 devices,
90.75 % of the family's rows — because that is the one sub-family with a
public normative grammar and real payloads available to test against. The
remaining 522 rows are named in §7 as an honest remainder.

---

## 0. Headline numbers

| quantity | value |
|---|---:|
| `wifi` rows | **5,642** |
| `wifi` bytes | **714,009,036** |
| `wifi` devices | 107 |
| `wifi` distinct basenames | 418 |
| rank among 9 families, by rows | **#2** |
| rank among 9 families, by bytes | #5 |
| share of corpus rows | 16.6347 % |
| share of corpus bytes | 1.0230 % |
| `bdwlan*` rows | **5,120** (90.75 % of family rows) |
| `bdwlan*` bytes | 270,399,184 (37.87 % of family bytes) |
| `bdwlan*` devices | 73 |
| `bdwlan*` distinct sizes | 32 |
| board bodies verified byte-level | **170** (three chipsets) |
| checksum law verified | **170 / 170** |

Corpus: 33,917 rows / 69,797,539,502 B.

---

## 1. The three verified payloads `[F]`

Nothing in this note is measured on a device from this repo's corpus. The
byte-level sections are measured on three files fetched from
`git.kernel.org/.../firmware/linux-firmware.git` on **2026-11-28**:

| path in `linux-firmware` | bytes | md5 |
|---|---:|---|
| `ath10k/WCN3990/hw1.0/board-2.bin` | 893,528 | `420356ebbf84fe34149ba470932fccaa` |
| `ath11k/WCN6750/hw1.0/board-2.bin` | 927,980 | `da585cfa4402ce063e02472c5d3ce653` |
| `ath11k/WCN6855/hw2.0/board-2.bin` | 7,479,440 | `2ac84328cf0b69f373817a6faf2a24e4` |

These are the **upstream** containers that this repo's on-device `bdwlan.*`
files are the unwrapped bodies of. `research/fleet/wifi-wpss.md` §3.3 already
establishes the `b`↔`e` wrapper relation and the 26,328 / 58,180 body sizes
from these same three upstream trees; this note extends that to the tag layer
and does not re-derive it.

**What this does and does not prove `[N]`.** It proves the *grammar* against
real vendor bytes. It does **not** prove that any of the 5,120 corpus rows has
the internal layout shown here — only that its size and its naming place it in
the same generation. A corpus payload would be needed for that, and none is
held in this workspace (§8.2).

---

## 2. Container grammar — PRIOR ART, restated only to anchor the rest `[F]`

The grammar below is **not new**. It is read directly from the in-tree kernel
source, which is the normative statement:

```c
#define ATH11K_BOARD_MAGIC  "QCA-ATH11K-BOARD"
#define ATH10K_BOARD_MAGIC  "QCA-ATH10K-BOARD"

struct ath11k_fw_ie {
        __le32 id;
        __le32 len;
        u8 data[];
};
```

with the walk in `ath11k_core_fetch_board_data_api_n()`:

```
magic_len = ALIGN(strlen(MAGIC) + 1, 4);     /* 17 -> 20 */
while (len > sizeof(struct ath11k_fw_ie)) {
        id  = le32(hdr->id);
        len = le32(hdr->len);
        ...
        ie_len = ALIGN(ie_len, 4);           /* the skip is 4-byte aligned */
}
```

So the container is:

```
0x00  "QCA-ATH11K-BOARD" or "QCA-ATH10K-BOARD"   16 bytes
0x10  00 6d 6d 6d                                 4 bytes pad, total field 20
0x14  { le32 id , le32 len , u8 data[len] , pad-to-4 }   repeated
```

`id` enumerates the top-level element type; `id 0` = board data, `id 1` =
regulatory database. Inside a board element the same `{le32,le32}` shape
reappears with `id 0` = ASCII name and `id 1` = the body. This is prior art
(§9.1) and is reproduced here only so §3–§6 have a reference.

### 2.1 Verified against all three payloads `[F]`

| payload | magic | field | top IEs | walk ends at | == file size |
|---|---|---:|---:|---:|---|
| WCN3990 | `QCA-ATH10K-BOARD` | 20 | 36 | 893,528 | **yes** |
| WCN6750 | `QCA-ATH11K-BOARD` | 20 | 22 | 927,980 | **yes** |
| WCN6855 | `QCA-ATH11K-BOARD` | 20 | 126 | 7,479,440 | **yes** |

Three files, three exact walks to EOF, zero slack. Top-level `id` counts:
WCN3990 `{0: 36}` (board only, no regdb); WCN6750 `{0: 11, 1: 11}`;
WCN6855 `{0: 123, 1: 3}`.

### 2.2 The pad fill is `0x6d`, and only at the sub-level `[F]`

The 4-byte pad after the magic is `00 6d 6d 6d` in all three files. The
prior art states the TLV pad is filled with `0x6d`; I measured where that
actually happens:

| level | padded TLVs | pad byte content |
|---|---:|---|
| top-level (all 3 files) | **0** | — |
| board sub-level (WCN6750) | 17 | `6d6d` ×15, `6d6d6d` ×2 |

**Top-level `len` values are all already 4-byte multiples on these three
files**, so the `ALIGN` in the driver never fires there and the fill byte is
never observed. It is observed only inside board elements, where the ASCII
names are not multiple-of-4. A parser must still apply the align — the driver
does — but a test that asserts `0x6d` at top level would pass vacuously here
`[N]`.

---

## 3. The tag table — the gap `docs/REPO-STATE-MAP.md` names `[F]`

The state map says: *"`bdwlan-format.md` resolves tags 1..17 on the 19 KiB
generation only, tags 18..33 of the 58 KiB generation remain open"*. Measured
now on 170 bodies:

| generation | bodies | tag count | max tag |
|---|---:|---|---:|
| WCN3990 `hw1.0` | 36 | 17 / 18 / 19 | **19** |
| WCN6750 `hw1.0` | 11 | 33 / 34 | **34** |
| WCN6855 `hw2.0` | 123 | 34 / 35 / 36 | **36** |

**Tags 1..31 carry a byte-identical length on both ath11k generations**, with
zero exceptions across 134 bodies. The full measured table:

| tag | WCN3990 | WCN6750 | WCN6855 | stable across ath11k |
|---|---:|---:|---:|:--:|
| 1 | 1028 | 1028 | 1028 | ✓ |
| 2 | 292 | 292 | 292 | ✓ |
| 3 | 484 | 480 | 480 | ✗ |
| 4 | 1028 | 1128 | 1128 | ✗ |
| 5 | 656 | 620 | 620 | ✗ |
| 6 | 636 | 636 | 636 | ✓ |
| 7 | 280 | 280 | 280 | ✓ |
| 8 | 4932 | 11580 | 11580 | ✗ |
| 9 | 920 | 1356 | 1356 | ✗ |
| 10 | 928 | 952 | 952 | ✗ |
| 11 | 1028 | 3604 | 3604 | ✗ |
| 12 | 3432 | 9612 | 9612 | ✗ |
| 13 | 44 | 6956 | 6956 | ✗ |
| 14 | 260 | 1020 | 1020 | ✗ |
| 15 | 1016 | 2296 | 2296 | ✗ |
| 16 | 516 / 2052 | 2052 | 2052 | — |
| 17 | 68 / 1532 | 108 | 108 | — |
| 18 | 68 | 172 | 172 | ✓ |
| 19 | 7172 | 188 | 188 | — |
| 20 | — | 188 | 188 | ✓ |
| 21 | — | 7172 | 7172 | ✓ |
| 22 | — | 252 | 252 | ✓ |
| 23 | — | 252 | 252 | ✓ |
| 24 | — | 60 | 60 | ✓ |
| 25 | — | 92 | 92 | ✓ |
| 26 | — | 60 | 60 | ✓ |
| 27 | — | 60 | 60 | ✓ |
| 28 | — | 36 | 36 | ✓ |
| 29 | — | 1536 | 1536 | ✓ |
| 30 | — | 396 | 396 | ✓ |
| 31 | — | 2896 | 2896 | ✓ |
| 32 | — | 92 | 396 | ✗ |
| 33 | — | 10 / 596 | 16 | ✗ |
| 34 | — | 582 | 92 | ✗ |
| 35 | — | — | 148 / 176 | — |
| 36 | — | — | 24 | — |

Three readings a parser must take from this table:

1. **The tag number is not a global section ID.** Tag 19 is 7,172 B on
   WCN3990 and 188 B on the ath11k generation. The same number means a
   different thing across the ath10k→ath11k boundary `[F]`.
2. **Even within ath11k the last few tags drift.** Tags 32–34 differ between
   WCN6750 and WCN6855, so "tags 1..31 are stable" is the strongest claim the
   data supports `[F]`.
3. **The `—` cells are real absences, not parse failures.** WCN3990 bodies
   terminate at tag 19; there is no tag 20 to read `[F]`.

---

## 4. Chain termination: `eof` or a `(0,0)` sentinel, never a length field `[F]`

Walking a body to `len(seg)` produces one of two outcomes:

| generation | bodies | ends at EOF | stops at `(0,0)` |
|---|---:|---:|---:|
| WCN3990 | 36 | 33 | 3 |
| WCN6750 | 11 | 10 | 1 |
| WCN6855 | 123 | 90 | 33 |

Both outcomes are valid. A `(0,0)` pair is **not** a corrupt record: the walk
must stop there, because a zero tag with zero length is indistinguishable from
unwritten space and the driver has no terminator check at all. Where the
sentinel appears, the bytes after it are zero to end-of-body in 36 of 37
cases; the single exception is a 586-byte tail in one WCN6750 variant body
whose only non-zero content is 3 bytes, none of which parse as a TLV `[F]`.

**The all-zero payload trap `[N]`.** Zero-filled payloads parse as an
unbounded `(0,0)` chain. `research/fleet/bdwlan-format.md` §2 already records
this for the 19 KiB generation and it holds here: a parser that does not stop
at `(0,0)` will read tag 6 (636 B of pure zero, all 11 WCN6750 bodies) as 159
phantom IEs. My first walk in this session made exactly that error and
reported 71 and 79 "tags" for bodies that have 33–36.

---

## 5. The checksum at `0x0a` verifies 170/170 `[F]`

The prior art gives the law; I tested it. For a body `seg`:

```
csum = ~( XOR of every le16 word of seg )   with le16 at 0x0a treated as 0
```

| generation | bodies | match |
|---|---:|---:|
| WCN3990 | 36 | **36 / 36** |
| WCN6750 | 11 | **11 / 11** |
| WCN6855 | 123 | **123 / 123** |
| **total** | **170** | **170 / 170** |

Zero violations. The field at `0x0a` is therefore a **whole-body XOR
checksum**, and it is the field whose value varies most between bodies —
which is why it is also the field that breaks a naive "which u16 differs?"
analysis.

This is the strongest result in this note: a public claim, an independent
implementation, and 170 vendor bodies agree exactly, across two different
container magics and a 3-order-of-magnitude range in file size.

**What is not proven `[N]`.** XOR-8 parity over 170 samples is not evidence
about the *purpose* of the field beyond "it is a checksum the firmware can
validate". The prior art reports the firmware rejecting a board file with a
bad checksum (`-110`); I have not reproduced that on hardware and do not
claim it.

---

## 6. A committed claim corrected: `u16@8` is the declared chain length `[F]`

`research/fleet/bdwlan-format.md` §2 states, and its §2 IE map repeats:

> Inside the first IE payload, a u16 LE at absolute offset [8,10) equals
> **19152** — the total file size self-reference, present in all 35 files `[F]`.

That is **true on the files it was measured on and false as a general law**.
Measured on 170 bodies:

| generation | `u16@8 == len(seg)` | actual field value |
|---|---:|---|
| WCN3990 | **29 / 36** | 26,328 ×21, 19,152 ×15 |
| WCN6750 | **0 / 11** | 28,216 ×11 |
| WCN6855 | **0 / 123** | 28,216 ×123 |

The mechanism, resolved on WCN3990 where both values occur in one file:

| file length | `u16@8` | chain walks exactly to `u16@8` | bytes past declared |
|---:|---:|:--:|---:|
| 19,152 | 19,152 | yes | 0 |
| 26,328 | 19,152 | **yes** | 7,176 |
| 26,328 | 26,328 | yes | 0 |

So the field is the **declared TLV chain length**, not the file length. On the
19 KiB generation the two coincide because those bodies carry no trailing
padding — which is exactly why the original claim looked right on 35 of 35
files of that one size. On a body that is zero-extended past its chain, the
field keeps the *shorter* value and the two numbers separate.

**This is a Rule-1 correction, and it is a correction of a `[F]` label, not of
a measurement.** The 19,152 value on those 35 files was correctly measured;
what was wrong was promoting "equals 19152" to "the total file size
self-reference". §10 applies the correction in place in the source document.

**28,216 is `[U]`.** It is constant on all 134 ath11k bodies, is not the file
size (58,180), is not the chain end (58,180), and is not any cumulative tag
boundary — I checked all 33 boundaries and 28,216 falls inside tag 12's span
(`22000..31616`), 6,216 bytes in. I will not guess what it means.

---

## 7. Census reconciliation — and the 522 rows this note does not cover `[F]`

The matrix carries **0** `board-2.bin` rows. The `bdwlan*` rows are the
unwrapped bodies, which is consistent with §2's wrapper relation:

| size | rows | devices | reading |
|---|---:|---:|---|
| 26,328 | **1,676** | 37 | WCN3990-generation body |
| 58,180 | **116** | 6 | WCN6750/WCN6855-generation body |
| 19,152 | 7 | 5 | WCN3990 short body |
| 59,932 | 1,502 | 18 | ELF wrapper (`b`↔`e` delta 1,752) |
| 59,868 | 762 | 7 | ELF wrapper (delta 1,688) |
| 88,792 | 330 | 6 | larger wrapper, unexplained |
| 60,000 | 219 | 8 | ELF wrapper (delta 1,820) |
| others | 508 | — | 32 distinct sizes total |

The 58,180 B rows land on exactly **6 devices** — `Edge_30`, `FP5`, `FP6`,
`Nord_4`, `Nord_CE4`, `Phone_1` — all of which are the modern-generation
Qualcomm handsets, consistent with `[I]`.

### 7.1 Honest remainder `[N]`

**522 rows / 48 basenames are not covered by this note.** They are the
non-`bdwlan` wifi rows, and their grammars are different things:

| basename | rows | bytes | why out of scope |
|---|---:|---:|---|
| `amss20.bin` | 50 | 276,853,024 | modem-adjacent firmware, not board data |
| `fw_bcmdhd.bin` | 12 | 22,524,617 | Broadcom full-MAC firmware |
| `aoa_cldb_swl14.bin` / `_falcon.bin` | 34 | 28,555,104 | Broadcom AOA co-processor |
| `FW_NF_ILI7807S_*` | 115 | 43,319,571 | Novatek **display** firmware filed under wifi |
| `setfile_3m3.bin`, `m3.bin` | 34 | 19,435,608 | MediaTek / Broadcom M3 |
| `regdb.bin` | 92 | 2,090,606 | wireless-regdb, a different container |

`amss20.bin` alone is **276,853,024 B = 38.77 % of the family's bytes**, which
is **102.4 % of the entire `bdwlan` sub-family's 270,399,184 B** — a single
basename outweighs the 5,120-row sub-family this note specs. It is out of
scope here and deserves its own issue.
The `FW_NF_ILI7807S_*` rows are the most suspicious: `ILI7807S` is a Novatek
display driver IC, and 115 rows / 43,319,571 B of display firmware are filed
under `blob_family=wifi` — a corpus defect of the same shape as the
`db_type=BOOT` mislabel in the `boot` family `[I]`, flagged here and not
silently fixed.

---

## 8. Honest negatives `[N]`

### 8.1 What is not measured

- **No corpus payload was opened.** Every byte-level claim in §2–§6 is on
  three upstream `linux-firmware` files, not on any of the 5,120 corpus rows.
  The corpus connection is by **size and name only**.
- **The semantic meaning of every tag is unknown.** I measure lengths,
  offsets, entropy and stability. I do not know what tag 8 or tag 21 *is*.
  `research/fleet/bdwlan-format.md` §4 offers record-stride evidence for tags
  8/12/13 on the 19 KiB generation; that is not extended here.
- **`u16@8 = 28,216` is unexplained** (§6).
- **The 88,792 / 125,288 B wrapper sizes are unexplained.** The `b`↔`e` delta
  table in `wifi-wpss.md` §3.3 covers 1,656–1,820 B deltas; 88,792 is 30,612 B
  above the 58,180 body and does not fit that decomposition. These may not be
  the same wrapper at all `[U]`.
- **No signature verification was attempted.** The container carries no
  signature field; integrity is the XOR checksum only. I did not test whether
  a modified body with a corrected checksum is accepted, and the prior art's
  `-110` observation is cited, not reproduced.

### 8.2 Why no corpus payload

`find` over the workspace for `bdwlan*` and `board-2.bin` returned nothing.
The `.gitignore` blocks `*.bin`, `*.elf`, `*.img`, so a corpus payload cannot
be committed even if obtained. This is a structural limit on this issue, not
an omission: the acceptance criteria forbid committing payloads, and the
byte-level work therefore has to run against upstream files fetched on the
day.

### 8.3 The prior-art field map does not transfer `[N]`

`ath11k-board-bin-tool`'s `FORMAT.md` gives a field map measured on **IPQ8074
access-point** boards: byte `0x40` = radio topology, `0x44` = common board
flags, `0x0e–0x31` = six default MACs. On the three payloads measured here:

| field | prior art (IPQ8074) | WCN3990 | WCN6750 | WCN6855 |
|---|---|---|---|---|
| `0x40` | radio topology, bit 4 = 160 MHz | 0 ×36 | 0 ×11 | 0 ×123 |
| `0x44` | common board flags | 0 ×36 | 0 ×11 | 0 ×123 |

Both fields are **zero on all 170 bodies**. The prior-art map is real but is
scoped to a different product line (AP vs client), and a reader who applies it
to a phone's `bdwlan.b0a` will read zeros and conclude the file is empty. The
one field that *does* transfer is the checksum at `0x0a` (§5), which is
generation-independent.

---

## 9. Gate 0 — prior art `[F]` / `[N]`

Access date **2026-11-28** for every query in this section. Queries are exact
strings.

### 9.1 GitHub code search (REST `/search/code`)

| query | hits | what they are |
|---|---:|---|
| `QCA-ATH11K-BOARD board-2.bin` | **363** | container magic across device trees and tools |
| `ath11k_core_parse_bd_ie_board` | **453** | the driver function that walks the sub-IEs |
| `bdwlan 58 KiB board data tags` | **36** | size-specific discussion |
| `ath11k board-2.bin regdb parse python` | **27** | reimplementations, incl. the tool below |
| `QCA-ATH10K-BOARD bdwlan` | **19** | the ath10k magic |
| `bdwlan.b0a TLV tag parser` | **4** | the narrowest query; almost no one parses per-tag |

Counts are a live index and drift between runs; the order of magnitude is the
finding, not the digit.

### 9.2 Normative source (in-tree)

- `drivers/net/wireless/ath/ath11k/core.c` — `ath11k_core_fetch_board_data_api_n()`,
  `ath11k_core_parse_bd_ie_board()`. Read 2026-11-28, 70,403 B.
- `drivers/net/wireless/ath/ath11k/hw.h` — `ATH11K_BOARD_MAGIC`,
  `struct ath11k_fw_ie`, the `ath11k_bd_ie_*` enums. 12,630 B.
- `drivers/net/wireless/ath/ath10k/core.c` (101,342 B) and `hw.h` —
  `ATH10K_BOARD_MAGIC`, same `ALIGN(ie_len, 4)` walk.

This is GPL-2.0 source and is cited, not copied. No code from it appears in
`implementations/wifi/`; the parser there is written from the *format*, with a
clean-room header naming these files as the specification.

### 9.3 Third-party prior art

| item | what it covers | what it does not |
|---|---|---|
| `ddimension/ath11k-board-bin-tool` (`FORMAT.md`, 7,669 B) | container, TLV, ids, `0x6d` pad, **`0x0a` checksum**, IPQ8074 field map | no per-tag table; AP-line field map only |
| `qualcomm/qca-swiss-army-knife` `ath{10,11}k-bdencoder` | normative encoder for the container | nothing about tag semantics |
| `wireless.docs.kernel.org` ath10k calibration | user-facing overview | no byte layout |

### 9.4 Verdict

**PRIOR-ART for the container; the delta is the tag table, the checksum
cross-check and the correction.**

The container grammar is fully public and I claim nothing new in §2. What is
new in this note, and what no external source states:

1. **The tag table on 170 real bodies** with lengths, per-generation
   stability and the 1..31 invariance result (§3). The state map explicitly
   names tags 18..33 as open; they are now measured.
2. **The checksum law tested at 170/170** across two magics and three
   generations (§5) — the prior art states the formula but reports 68 files of
   a different product line.
3. **A correction to this repo's own `[F]` claim** about `u16@8` (§6).
4. **A stdlib parser** with the four documented traps encoded as tests (§10).

---

## 10. Method `[F]`

- Census: `csv.DictReader` over `upstream-contribution/blob-database/coverage-matrix.csv`,
  grouped on `blob_family`; every total, share and rank printed by the command
  that computed it.
- Container: `struct.unpack_from("<2I", d, off)` per TLV; skip is
  `off + 8 + ALIGN(len, 4)`; magic length is `ALIGN(strlen+1, 4) = 20`.
- Body: if the payload starts `\x7fELF`, the ELF32 header is read with
  `"<16sHHIIIIIHHHHHH"` and the `PT_LOAD` (`p_type == 1`) segment is taken as
  the chain. **Index care:** in that format string `e_phentsize` is index 9 and
  `e_phnum` is index 10 — reading `e[9]` as the count walks 32 phdrs instead of
  1 and yields garbage `p_filesz`. I made that error in this session and it is
  the reason §8.3's numbers were re-run.
- Chain: `struct.unpack_from("<2H", seg, o)`; **stop at `(0,0)`**, stop at
  `o + 4 + len > len(seg)`, else continue. Both stop conditions are needed
  (§4).
- Checksum: XOR of every `le16` word with the word at `0x0a` zeroed, then
  complement, masked to 16 bits.
- Payloads opened read-only from scratch space; nothing committed; the only hex
  in this note is ≤16 bytes per sample.
- Implementation: `implementations/wifi/bdwlan_parser.py`, self-tests in
  `test_bdwlan_parser.py`, fixtures generated deterministically by
  `make_fixture.py` because every fixture extension is gitignored, so the
  suite calls `make_fixture.write_all()` in `setUpModule`.

### 10.1 Rule-1 correction applied in place

`research/fleet/bdwlan-format.md` §2 and its IE-map row for tag 1 both assert
that `u16@8` is "the total file size self-reference". Both are now corrected
in the source document to state the declared-chain-length reading, with a
pointer to §6 here for the measurement. The original 19,152 observation is
preserved in the corrected text, because it was a correct measurement of a
field that is not the file size.

---

## 11. Open items `[U]`

1. What is `u16@8 = 28,216` on the ath11k generation? Constant across 134
   bodies, inside tag 12's span, not any boundary.
2. What are tags 1..36 *semantically*? Lengths and stability are known;
   meaning is not. The stride evidence in `bdwlan-format.md` §4 is the only
   in-repo lead and covers tags 8/12/13 only.
3. What are the 88,792 / 125,288 B wrappers? They exceed the §3.3 `b`↔`e`
   delta decomposition.
4. Is the 522-row non-`bdwlan` remainder one family or six? `amss20.bin`
   (276,853,024 B) alone deserves its own issue.
5. Are the 92 `FW_NF_ILI7807S_*` rows really `blob_family=wifi`? They look
   like Novatek display firmware.
