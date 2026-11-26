# `modem-config` — five rows, two unrelated artifacts, and a bucket name that describes neither (5 rows, 4 devices)

Analysis date: 2026-11-26. Analyst: OC-1 (`100milionseek`), issue
[#2051](https://github.com/adineo-cmd/open-device/issues/2051).

Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data
rows) for the census; three payload files fetched 2026-11-26 —
`modnet_c12v2_in_h416_w544.bin` (324,144 B), its co-shipped sibling
`modnet_c12v2_in_h416_w544.mnn` (7,867,488 B), and `MCD_NACHO_slog.bin`
(4,194,304 B). Also read 2026-11-26: `gitlab.com/kernel-firmware/linux-firmware`
`WHENCE` (11,958 lines / 542,574 B); `alibaba/MNN` `schema/default/MNN.fbs`
(12,531 B) for the `Net` table; and a public Exynos ABOX kernel driver,
`exynos8895/android_kernel_samsung_universal8895` branch `lineage-19.1`
`sound/soc/samsung/abox/abox.c` (5,674 lines / 161,783 B).

Every number below is command output. No payload is committed; samples are
≤16 bytes of hex.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** Five rows, four devices, 9,361,040 B — **#14 of 18** named
subfamilies by rows and **#12 of 18** by bytes. That is the whole of the
census-level interest, because **the bucket contains two artifacts that share
nothing but a mislabel.** `blob_family=modem` on all five rows is wrong on all
five: neither artifact contains a single modem token, and one of them is a
portrait-matting neural network filed under `vendor/etc/camera`.

Three findings carry the note.

First, **`modem-config` is a misnomer on both halves, and the `vendor/etc/camera`
path is the honest one.** The three Fairphone rows are `modnet_c12v2_in_h416_w544.bin`,
a **compiled MNN inference model** in FlatBuffer form — 30 embedded Mali OpenCL
kernel blobs, 19 `-cl-std=CL1.2` build option strings, and an output tensor
literally named `pred_matte`. It is a camera matting model, not configuration.
The two Samsung rows are `MCD_NACHO_slog.bin`, which is **not a log** either:
it is a 41-entry **printf descriptor table** compiled from
`../../../Exynos850_Abox/BSP/DM/Src/DM_printf.c` — format strings and line
numbers, zero captured messages, 99.82 % of the file empty.

Second, **all 22 modem tokens are zero in all three payloads.** `modem`, `qmi`,
`rmnet`, `baseband`, `LTE`, `NR5G`, `gsm`, `wcdma`, `sim`, `nas`, `mbn` and their
case variants: 0 occurrences across 12,385,936 bytes (324,144 + 7,867,488 +
4,194,304). The `blob_family=modem`
label on these rows is inherited from the directory, not measured from the bytes.

Third, **the `modnet` `.bin` is not a self-consistent FlatBuffer.** Its vtable and
root table are byte-identical to the sibling `.mnn`'s — which is expected, since
both are emitted by the same MNN schema — but its `bizCode` uoffset field holds
**7,867,444**, a value that resolves to 7,867,480 and is therefore **7,543,336
bytes past the `.bin`'s own EOF**. That target is, exactly, the offset at which
the *sibling* `.mnn` stores the 3-byte string `biz`. A second field overruns
independently: the `oplists` vector declares 226,304 entries needing 905,220 B in
a 324,144-byte file. Two independent overruns in one header is not a truncation
signature — a truncated file keeps valid counts and loses tail data. It is the
signature of an **offset table serialised against a larger buffer than the file
that shipped**.

---

## 0. Headline numbers

| quantity | value |
|---|---:|
| rows | **5** |
| devices | **4** (`FP4`, `FP5`, `FP6`, `Galaxy_A21S`) |
| basenames | **2** |
| distinct `md5_db` | **2** |
| distinct sizes | **2** (324,144 and 4,194,304) |
| total bytes | **9,361,040** |
| bytes after de-duplicating the exact-duplicate row | **5,166,736** |
| share of corpus rows | 0.0147 % |
| share of corpus bytes | 0.0134 % |
| share of `modem` rows | 0.197 % |
| share of `modem` bytes | 0.0361 % |
| rank among 18 named subfamilies, by rows | **#14** |
| rank among 18 named subfamilies, by bytes | **#12** |
| `isa_identified` populated | **0 of 5** |
| `sha256_if_listed` populated | **0 of 5** |

Corpus: 33,917 rows / 69,797,539,502 B. `modem` family: 2,539 rows /
25,939,141,330 B. `modem-config` is 0.20 % of its own family's rows but only
0.036 % of its bytes — the family's mass is in `modem.mdt`-class images, not here.

---

## 1. The census rows `[F]`

All five rows, verbatim from the matrix, in file order:

| # | device | vendor | filename | size | md5 |
|---:|---|---|---|---:|---|
| 1 | `FP6` | fairphone | `modnet_c12v2_in_h416_w544.bin` | 324,144 | `a189829fd86b30c34b4ed1044534027e` |
| 2 | `FP4` | fairphone | `modnet_c12v2_in_h416_w544.bin` | 324,144 | `a189829fd86b30c34b4ed1044534027e` |
| 3 | `FP5` | fairphone | `modnet_c12v2_in_h416_w544.bin` | 324,144 | `a189829fd86b30c34b4ed1044534027e` |
| 4 | `Galaxy_A21S` | samsung | `MCD_NACHO_slog.bin` | 4,194,304 | `802ac22cb0d090f5501b86aa12173ee1` |
| 5 | `Galaxy_A21S` | samsung | `MCD_NACHO_slog.bin` | 4,194,304 | `802ac22cb0d090f5501b86aa12173ee1` |

Rows 4 and 5 are an **exact duplicate** — same device, same `db_path`, same
filename, same size, same md5. The corpus contains **46** such exact-duplicate
groups covering **92** rows; this bucket owns one of them. So:

- the census's `size<->md5` map is a bijection (2 sizes / 2 md5 / 1 each) `[F]`
- but **`sum(size_bytes)` over 5 rows double-counts 4,194,304 B** `[F]`
- de-duplicated real payload mass is **5,166,736 B** = `324,144 × 3 + 4,194,304` `[F]`

Paths: `fairphone/FP{4,5,6}/vendor/etc/camera` and
`samsung/a21s/vendor/firmware`. Note the Fairphone path — **`vendor/etc/camera`**,
not `firmware`. The matrix's own path agrees with the payload (§2) and disagrees
with the `modem` family label.

### 1.1 Metadata is not uniform — and the DELTA comment was wrong about it `[F]`

Per-row field values:

| # | device | `soc` | `priority` | `interface_documented` |
|---:|---|---|---|---|
| 1 | `FP6` | *(blank)* | **P1** | **`y (qualcomm-fp6/docs/interface-cellular.md)`** |
| 2 | `FP4` | `Qualcomm SM7225 Snapdragon 750G` | P2 | `n` |
| 3 | `FP5` | `Qualcomm QCM6490` | P2 | `n` |
| 4 | `Galaxy_A21S` | *(blank)* | P3 | `n` |
| 5 | `Galaxy_A21S` | *(blank)* | P3 | `n` |

The `DELTA` comment posted on this issue on 2026-11-26 stated "all `priority=P3`,
all `interface_documented=n`". **Both halves of that are false**, and this note
corrects them: the bucket spans **three** priorities (P1, P2, P3), and **one row
claims a documented interface**.

That one claim is itself **dangling**. The referenced file is
`qualcomm-fp6/docs/interface-cellular.md`, which does not exist at that path.
The repo's actual file is `research/qualcomm/docs/interface-cellular.md`
(4,567 B), and it is a **one-page note about the FP6 `modem.mdt`/`b00–b30` PIL
image** — Hexagon, `e_machine` 164, `modem/image/milos/qdsp6m.qdb`. It never
mentions `modnet`, `c12v2`, a camera path, or anything in this bucket: `modnet`
→ 0, `c12v2` → 0, `modem-config` → 0, `MCD_NACHO` → 0 in that file `[F]`.

So the row's `y` is a **cross-reference to the wrong artifact** — the pointer
resolves (to a relocated copy) but the subject does not match. `FP6`'s P1
priority is likewise unjustified by anything in this bucket.

Also blank on all five rows: `isa_identified`, `sha256_if_listed`. `db_type` is
`UNKNOWN` on all five.

### 1.2 Rank inside the 18 named subfamilies `[F]`

`blob_subfamily` is populated on 18 distinct values (all other rows carry a blank
subfamily). `modem-config` sits at **#14 of 18 by rows** and **#12 of 18 by
bytes** — it rises two places on bytes because its 4 MiB `nacho` row is large
relative to its row count.

| rank | subfamily | rows | bytes |
|---:|---|---:|---:|
| 11 | `hyp` | 63 | 153,300,992 |
| 12 | `esim` | 41 | 8,407,085 |
| 13 | `dtb` | 7 | 58,720,256 |
| **14** | **`modem-config`** | **5** | **9,361,040** |
| 15 | `sensors` | 5 | 86,541,968 |
| 16 | `tinysys` | 4 | 4,132,864 |
| 17 | `wifi-bt-combo` | 4 | 1,671,348 |
| 18 | `gpu-compute` | 3 | 2,523,240 |

By bytes the order around it is `dtb` (#8, 58,720,256) … `nfc` (#11, 9,677,922),
**`modem-config` (#12, 9,361,040)**, `esim` (#13, 8,407,085). It is **tied at 5
rows with `sensors`** but carries **9.24× fewer bytes** — `sensors` is 86.5 MB of
`snsc.bin` across 5 devices, this bucket is 9.4 MB across 4.

---

## 2. Artifact A — `modnet_c12v2_in_h416_w544.bin` is a compiled MNN model `[F]`

324,144 B, md5 `a189829fd86b30c34b4ed1044534027e`, one payload on three devices
(FP4, FP5, FP6 — a single md5 across a Snapdragon 750G, a QCM6490 and an
unspecified FP6 SoC, so the artifact is **platform-independent** `[F]`).

### 2.1 Not ELF, not an archive `[F]`

`b[0:4] == 1c 00 00 00`, i.e. `u32le@0 = 28`. `\x7fELF`, `\x1f\x8b`, `PK\x03\x04`
all absent. Entropy **6.8090** bits/byte, 17.89 % zero bytes, 36.48 % printable.

### 2.2 It is a FlatBuffer, and the schema is MNN's `Net` `[F]`

Root table at 28, vtable at 4: `vtable_size = 24`, `object_size = 28`,
**10 fields** at offsets `(8, 0, 0, 12, 16, 5, 6, 20, 24, 7)`, so fields 0, 3, 4,
5, 6, 7, 8, 9 are present and 1, 2 are absent.

`alibaba/MNN` `schema/default/MNN.fbs` declares

```
table Net {
    bizCode: string;
    extraTensorDescribe: [TensorDescribe];
    extraInfo: ExtraInfo;
    oplists: [Op];
    outputName: [string];
    preferForwardType: ForwardType = CPU;
    sourceType: NetSource = CAFFE;
    tensorName: [string];
    tensorNumber: int = 0;
    usage:Usage = INFERENCE;
    subgraphs: [SubGraphProto];
    mnn_uuid: string;
}
```

Field 0 = `bizCode`, 3 = `oplists`, 4 = `outputName`, 5 = `preferForwardType`,
6 = `sourceType`, 7 = `tensorName`, 8 = `tensorNumber`, 9 = `usage`. The absent
fields 1/2 are `extraTensorDescribe`/`extraInfo`. The 10-field vtable is exactly
this schema truncated after field 9 — i.e. the writer's `Net` had no `subgraphs`
or `mnn_uuid`. Scalar decode: `preferForwardType = 0` (CPU),
`sourceType = 3`, `tensorNumber = 0`, `usage = 0` (INFERENCE) `[F]`.

### 2.3 The body carries 30 compiled Mali OpenCL kernels `[F]`

The decisive content is not the header but the body. Token counts in the `.bin`:

| token | count | reading |
|---|---:|---|
| `MBSX` | **30** | Mali binary shader executable block |
| `MBS2` | 30 | paired secondary block, each `MBSX` followed by `MBS2` |
| `EBIN` | 30 | Mali ELF-binary block marker |
| `OBJC` | 30 | per-kernel object block |
| `CCOM` / `CMMN` / `VEHW` / `VELA` | 30 each | Mali compiler/commander metadata |
| `CLCC` | **19** | OpenCL compile-config block |
| `-cl-std=CL1.2` | **19** | the OpenCL build option string |
| `-DMNN_SUPPORT_FP16` | **19** | MNN's FP16 build define |
| `MNN` | 19 | inside `-DMNN_SUPPORT_FP16` |

`MBSX` is a **Mali (Arm) binary shader** container tag; `EBIN`, `OBJC`, `CLCC`,
`CCOM`, `CMMN`, `VEHW`, `VELA` are the block tags of Arm's offline compiler
output. Each `MBSX` is followed by its length and then an `MBS2` block —
e.g. the first is at `0x1950` with length 5,108, immediately followed by
`MBS2` of length 5,096. First `MBSX` at `0x1950`, first `EBIN` at `0x1f3c`.

The kernel name table is present as 925 `STRI` length-prefixed records; the
kernel-argument names are `kernel_param_0` … `kernel_param_11` and
`__bifl_global_offset_plus_hds_offset`. The compute-kernel names are the
`winogradTransformSource` / `winogradTransformDest` / `depthwise_conv2d` /
`imageCopy` / `rasterImage` family — 1,079 printable runs of ≥8 chars.

This is a **weight-light, kernel-heavy** build: 30 compiled GPU kernels and 529
distinct identifiers of ≥4 chars in 324 KB — it carries compiled GPU kernels, not
the model's weights.

### 2.4 The `.bin`'s offset table is foreign to the `.bin` `[F]`

Four uoffset fields, resolved as `target = field_pos + u32`:

| field | field pos | uoffset | target | verdict |
|---|---:|---:|---:|---|
| `bizCode` | 36 | 7,867,444 | 7,867,480 | **past EOF by 7,543,336** |
| `oplists` | 40 | 2,060 | 2,100 | in range |
| `outputName` | 44 | 2,032 | 2,076 | in range |
| `tensorName` | 48 | 8 | 56 | in range |

Two independent inconsistencies:

1. **`bizCode` points 7.5 MB past the end of a 324,144-byte file.** The target
   7,867,480 is not arbitrary: `7,867,488 − 7,867,480 = 8`, and the sibling
   `.mnn` (length 7,867,488) stores the 3-byte string `biz` at exactly
   `0x780c5c = 7,867,484` with its length prefix at 7,867,480. **The `.bin`'s
   `bizCode` uoffset is the `.mnn`'s value.** `[F]`
2. **`oplists` declares 226,304 entries.** A vector of 226,304 uoffsets needs
   `4 + 226304 × 4 = 905,220` bytes; the file has 322,044 from that point.
   Only 80,510 four-byte slots exist. `[F]`

A truncated FlatBuffer fails the opposite way: it keeps **valid** counts and
loses tail bytes, so a reader hits EOF while walking a vector it can size
correctly. Here the **count itself** is impossible and a **second, unrelated
field** is out of range. One cause explains both: the header was serialised
against a larger buffer than the file that shipped `[I]`.

I cannot distinguish "fragment of a same-schema larger build" from "serialiser
emitted a stale offset table" from these bytes alone `[U]`. What is measured is
that **a strict MNN reader would reject or misparse this `.bin`** `[F]`.

### 2.5 The `.bin` and `.mnn` share a schema header, not a build `[F]`

The tempting reading is "the `.bin` is a truncated `.mnn`". It is not:

| test | result |
|---|---|
| common prefix | **exactly 128 B** |
| `b[0:4]` vs `m[0:4]` | both `1c 00 00 00` (root 28) |
| vtable `b[4:28] == m[4:28]` | **identical** |
| root table `b[28:56] == m[28:56]` | **identical** |
| same-offset identical bytes over `len(bin)` | **2,844 of 324,144 = 0.88 %** |
| `b'biz'` in `.bin` | **0** |
| `b'pred_matte'` in `.bin` | **0** (3 in `.mnn`) |
| `b'winogradTransformSource'` in `.bin` | 9 (0 in `.mnn`) |
| `b'MBSX'` in `.bin` | 30 (0 in `.mnn`) |
| `b'MNN'` in `.mnn` | 0 (19 in `.bin`) |

The 128-byte identity is **schema, not identity**: two FlatBuffers written from
the same `Net` schema emit the same root offset and the same vtable bytes. Past
byte 128 the two files diverge and only 0.88 % of positions agree. The `.bin`
carries 30 Mali kernels and no `pred_matte`; the `.mnn` carries 145 op entries,
no Mali kernels, and ends with `biz`.

So these are **two different serialisations of the same schema** `[F]`, and the
`.bin` is **not** a truncated `.mnn` `[F]`. What the `.bin` *is* in MNN's terms is
narrower than "the GPU plan", and the header argues against the obvious reading:
**both files declare `preferForwardType = 0`, which the `ForwardType` enum defines
as `CPU`**, and both declare `sourceType = 3`, `tensorNumber = 0`, `usage = 0`
(INFERENCE) — i.e. **the four scalar fields are identical in both files and
distinguish nothing.** What differs is the body: the `.bin` embeds **30** compiled
Mali OpenCL kernel blobs (`MBSX`/`MBS2`/`EBIN`) and **0** ops named `pred_matte`,
while the `.mnn` embeds **0** Mali kernels and 145 ops. So the `.bin` is a build
that **carries** compiled GPU kernels while its header still **prefers** CPU — a
combination the header alone cannot explain, so the mechanism is `[U]`. The
filename's `in_h416_w544` is the input tensor shape 416 × 544 — the portrait
aspect MODNet targets — and neither file contains the literal strings `416`,
`544`, `c12`, `c12v2`, `modnet` or `MODNet` `[F]`, so the shape is carried in the
filename only, not in the artifact.

### 2.6 The sibling `.mnn` is fully self-consistent `[F]`

For contrast, the same decode on `modnet_c12v2_in_h416_w544.mnn`
(7,867,488 B, md5 `cc28c50974d93d083803383673248a50`):

| field | target | count | bytes needed | verdict |
|---|---:|---:|---:|---|
| `bizCode` | 7,867,480 | 3 | 7 | fits, reads `biz` |
| `oplists` | 2,100 | 145 | 584 | fits |
| `outputName` | 2,076 | 1 | 8 | fits, reads `pred_matte` |
| `tensorName` | 56 | 145 | 584 | fits, **145/145 resolve** |

`tensorName` resolves to `input`, `463`, `468`, `822`, `475`, `480`, … — the
graph's tensor names. Entropy 7.5212, 0.49 % zero, 40.00 % printable, 3,839
printable runs of ≥8, 3,267 identifiers of ≥4 chars. **24.27×** the `.bin`'s size.

This matters for the verdict: the `.mnn` proves the decoder is correct. The
`.bin`'s two overruns are therefore **in the file**, not in the reading `[F]`.

---

## 3. Artifact B — `MCD_NACHO_slog.bin` is a printf descriptor table, not a log `[F]`

4,194,304 B, md5 `802ac22cb0d090f5501b86aa12173ee1`, `samsung/a21s/vendor/firmware`,
on the `Galaxy_A21S` (Exynos 850). The filename's `slog` suggests a captured log.
It is not one.

### 3.1 The file is 99.82 % empty `[F]`

| measurement | value |
|---|---:|
| size | 4,194,304 |
| non-zero bytes | **7,712** (0.1839 %) |
| entropy | **0.0298** bits/byte |
| zero bytes | 4,186,592 (99.82 %) |
| printable bytes | 6,852 (0.16 %) |
| non-empty 4 KiB blocks | **4 of 1,024** |
| those blocks | `0x0`, `0x1000`, `0x200000`, `0x201000` |

Only **8,848 bytes** of the 4 MiB carry content — 0.2110 %, split
**0x1168** in the first 2 MiB and **0x1128** in the second. Every byte after those
two extents is zero `[F]`.

### 3.2 Two 2 MiB banks, and the second is the first shifted by 0x40 `[F]`

The file is two 2 MiB halves. Bank 0's content occupies `0x40..0x1168`; bank 1's
occupies `0x0..0x1128`. Both extents are **exactly 4,392 bytes**, and
`0x1168 − 0x40 = 0x1128`, so the two banks are the *same size* — but they are
**not** the same bytes: comparing the two 4,392-byte regions offset-for-offset
gives **182 differing bytes**. The equal length is a consequence of bank 1
carrying 40 more string bytes and 40 fewer padding bytes (§3.4), not of one
being a slice of the other.

Bank 0's 0x40-byte prefix is **53 zero bytes**, then the 7-byte run
`PAM\x00\x00\x000` at `0x35..0x3c`, then 4 more zero bytes. `4,194,304 = 0x400000`,
so `PAM` is a plausible in-house magic, but the surrounding bytes are not a
documented header and nothing else in the file references it `[U]`.
Bank 1 has no such prefix — its content starts at `0x0` with the banner.

### 3.3 The record table: 41 entries per bank, 20-byte fields `[F]`

Each bank carries **41** `DBT:` markers (the DSP's printf tag). Inter-record
spacing is only **104 or 108 bytes** (27 × 108, 13 × 104 in each bank), and the
20 bytes after each `DBT:` decode as **five u32**:

| field | meaning | observed values |
|---|---|---|
| 0 | level | **3** on 41/41 |
| 1 | flags | `0` (1 record) or `8` (40 records) |
| 2 | mask | `0` (1 record) or `0xfecdba98` (40 records) |
| 3 | `0x3` in the top nibble, low 28 bits = **absolute file offset of the format string** | 41/41 resolve to a printable string (bank 0 from `0x40`, bank 1 from `0x200000`) |
| 4 | **source line number** in `DM_printf.c` | 293 … 445, **strictly increasing**, steps of 3 and 35 |
| 5 | `0x3` in the top nibble, low 28 bits = **absolute file offset of the source-path string** | 41/41 resolve to a printable string |

The layout law is exact: **`field5 == field3 + strlen(field3-string) + 1`** on
**41 of 41** records — field 5 is the byte immediately after the format string's
NUL. So each record is a pointer pair (format, path) plus a line number.

Field 3 on record 1 points at `0x40`, the banner
`=========== ABOX_flush_pending_logQ ============`; every other record points at
one of the 40 `[ABOX <tag>] CNT(%d) S(%d)` strings. Field 4 running 293→445
monotonically is the giveaway that these are **source line numbers** `[I]` — 41
`printf` call sites in one 4-line-span file region.

The `0x3` in the top nibble of fields 3 and 5 is an address-space tag (DSP window
3), not part of the offset `[I]`; masking it is what makes 41/41 resolve.

### 3.4 40 channel tags, twice, with one byte of drift `[F]`

The format strings are the whole content:

- **80** occurrences of `[ABOX …] CNT(%d) S(%d)` file-wide, **40 distinct**
  — 40 per bank, identical tag sets
- **80** occurrences of `[ABOX <tag>]` file-wide, **40 distinct tags**
- one and only one source path, repeated **41** times per bank:
  `../../../Exynos850_Abox/BSP/DM/Src/DM_printf.c`
- **83 distinct printable strings of ≥4 chars** in the whole file: the 40 bank-0
  format strings, the 40 bank-1 format strings (one leading byte different, §3.4),
  the banner, the single source path, and the literal `DBT:` — that is
  `40 + 40 + 1 + 1 + 1 = 83` `[F]`

The 40 tags are the Exynos ABOX audio-DSP channel map:

| group | tags | count |
|---|---|---:|
| PCM in | `VPCMIN0` … `VPCMIN15` | **16** |
| PCM out | `VPCMOUT0` … `VPCMOUT9` | **10** |
| serial audio in | `Tx SE In0`, `Tx SE In1`, `Tx SE MID`, `Rx SE In` | 4 |
| serial audio out | `Tx SE Out`, `Rx SE Out` | 2 |
| path-level | `Playback`, `Capture`, `ECHO REF`, `DEC PKT`, `ENC PKT` | 5 |
| reserved | `RESERVE1`, `RESERVE2`, `RESERVE3` | 3 |
| | **total** | **40** |

The **only** systematic difference between the banks' strings is a leading space:
every one of bank 1's 40 format strings begins with a space where bank 0's begins
with `0` directly. Multiset comparison of the 82 printable strings in each region
finds **42 distinct in each, 40 exclusive to bank 0, 40 exclusive to bank 1** —
and each exclusive pair differs by exactly that one leading byte, e.g.
`0[ABOX Playback] CNT(%d) S(%d)` vs ` 0[ABOX Playback] CNT(%d) S(%d)`. Only 2
strings are byte-identical across the banks (the banner and the source path).

So bank 1's strings are 40 bytes longer in total (**3,453** vs **3,413**
printable-string bytes including NUL terminators), and its non-string region is
correspondingly 40 bytes shorter (**939** vs **979**) — the two regions are
therefore the same 4,392-byte length despite carrying different content. This is
a **width-1 field alignment** in the DSP's printf (a `%1d`-style slot rendering
`0` in one bank and a space in the other) `[I]`; it is not different content.

The remaining differences are inside the record field blocks: **91 of the 182
differing bytes** fall inside the 41 × 24-byte record blocks, and the rest are
the string-prefix and padding bytes above. The two banks are therefore two dumps
of the same 41-call-site table from two builds (or two cores) that differ in
one alignment decision — not two halves of one stream, and not a ring buffer.

### 3.5 Zero modem content, and the ABOX driver does not name this table `[F]`/`[N]`

`MCD_NACHO` is not in `WHENCE` (0), and `MCD_NACHO` / `MCD_NACHO_slog.bin` return
no description anywhere (§5). The one public ABOX driver read,
`sound/soc/samsung/abox/abox.c` (5,674 lines), contains **`ABOX` ×527**,
`abox_flush` ×18 (all `abox_flush_mixp` / `_sifm` / `_sifs1` / `_sifs2` /
`_recp` / `_sifm0..2` — register flushes, unrelated), and **`VPCMIN` ×0**,
`DBT:` ×0, `flush_pending_logQ` ×0. So the channel *names* are a real Exynos ABOX
family (prior art confirms `VPCMIN` as a live ABOX PCM channel token: 556 GitHub
hits, and `silkyland/rabbiz-os-project` documents `VPCMIN` on the **same a21s**
device), but **no public source describes this descriptor table or its
`MCD_NACHO` name** `[N]`.

`flush_pending_logQ` — the banner — has **0** hits in GitHub code search across
all of GitHub. The string is unique to this file `[F]`.

---

## 4. Both artifacts fail the family label `[F]`

All 22 modem tokens measured in all three payloads:

| token | `.bin` | `.mnn` | `nacho.bin` |
|---|---:|---:|---:|
| `modem` | 0 | 0 | 0 |
| `MDM` | 0 | 0 | 0 |
| `qmi` / `QMI` | 0 | 0 | 0 |
| `rmnet` / `RMNET` | 0 | 0 | 0 |
| `AT+` / `AT ` | 0 | 0 | 0 |
| `baseband` / `Baseband` | 0 | 0 | 0 |
| `LTE` | 0 | 0 | 0 |
| `NR5G` | 0 | 0 | 0 |
| `gsm` / `GSM` | 0 | 0 | 0 |
| `wcdma` / `WCDMA` | 0 | 0 | 0 |
| `sim` / `SIM` | 0 | 0 | 0 |
| `nas` / `NAS` | 0 | 0 | 0 |
| `mbn` / `MBN` | 0 | 0 | 0 |

**0 of 22 tokens, in 0 of 3 files.** `blob_family=modem` is therefore a
**path-derived** label, and even the path disagrees on the Fairphone side
(`vendor/etc/camera`). The correct labels, from the bytes:

- `modnet_c12v2_in_h416_w544.bin` → a **camera** artifact (portrait matting),
  an MNN model build carrying 30 compiled Mali OpenCL kernels
- `MCD_NACHO_slog.bin` → an **audio** artifact, Exynos ABOX printf descriptor table

Neither is configuration. `modem-config` is wrong on `modem`, wrong on `config`,
and wrong for both rows.

---

## 5. Gate 0 — prior art `[F]`/`[N]`

Access date **2026-11-26** for every query below. Queries are exact strings.

### 5.1 GitHub code search (REST `/search/code`)

| query | hits | what they are |
|---|---:|---|
| `modnet_c12v2_in_h416_w544.bin` | **24** | **all** vendor blob manifests — `proprietary-files.txt` / `*-vendor.mk` in Fairphone device trees (`LineageOS/android_device_fairphone_FP4/FP5/FP6`, `ArianK16a/android_device_fairphone_FP6`, `WeAreFairphone/android_device_fairphone_FP5`, `CalyxOS/device_fairphone_FP4/FP5/FP6`, `LMODroid-Devices/device_fairphone_FP4/FP5`, `TheMuppets/proprietary_vendor_fairphone_FP4/FP5/FP6`, `fp6-aosp/…`, `Jiovanni-dump/fairphone_fp5_dump`) **plus one non-Fairphone tree**: `9cb14c1ec0/android_vendor_tcl_selene_vzw` (`selene_vzw-vendor.mk`, branch `master`, 3,583 lines / 304,487 B). **No repo describes the format.** |
| `modnet_c12v2` | **24** | same set |
| `filename:modnet_c12v2_in_h416_w544.bin` | 0 | — |
| `MCD_NACHO` | **31** | `proprietary-files.txt` in `LineageOS/android_device_samsung_a21s-common`, `crdroidandroid/android_device_samsung_a21s-common`, `TheMuppets/proprietary_vendor_samsung_a21s-common` (`a21s-common-vendor.mk`), plus sibling-Exynos850 trees (`a04s`, `a12s`, `a13xxv`, `m12`, `a14`, `exynos850-common` ×4) and two full-dump file lists (`leddaz-dump-stash/samsung_a21s_dump`, `redznn-dumps/samsung_m12_dump`). **Listings only.** |
| `filename:MCD_NACHO_slog.bin` | **0** | — |
| `MCD_NACHO_slog` | **31** | same set |
| `flush_pending_logQ` | **0** | — |
| `ABOX_flush_pending_logQ` | **0** | — |
| `abox_flush` | **313** | Exynos ABOX kernel drivers (`sound/soc/samsung/abox/abox.c`, `include/sound/samsung/abox_ipc.h`) across ~15 device kernels — **register-flush functions, not this table** |
| `VPCMIN` | **556** | Exynos ABOX channel tokens; includes `silkyland/rabbiz-os-project` a21s findings |
| `filename:modnet.mnn` | **0** | — |
| `filename:abox_tplg.bin` | **0** | — |
| `repo:alibaba/MNN "bizCode"` | **65** | MNN converter/tooling — confirms `bizCode` is a real `Net` field |

### 5.2 Web search (searxng, aggregating Google/Bing/Brave/DDG)

| query | result |
|---|---|
| `MCD_NACHO_slog.bin Samsung ABOX` | 0 hits |
| `Exynos ABOX audio DSP firmware` | 0 hits |
| `Samsung Exynos850 ABOX flush_pending_logQ` | 0 hits |
| `MODNet real-time portrait matting` | arXiv `2011.11961`, `github.com/ZHKKKe/MODNet`, OpenVINO model zoo `modnet-photographic-portrait-matting` |
| `Alibaba MNN .mnn model file format FlatBuffer biz` | `github.com/alibaba/MNN`, DeepWiki `MNNConvert Tool`, DeepWiki `Model Conversion and Optimization` |

### 5.3 Upstream trees

`linux-firmware` `WHENCE` (11,958 lines / 542,574 B, fetched 2026-11-26):
`modnet` **0**, `MCD_NACHO` **0**, `nacho` **0**, `NACHO` **0**, `abox` **0**,
`ABOX` **0**, `tflite` **0**, `snpe` **0**, `mnn` **0**, `.mnn` **0**.

### 5.4 Decision

**`DELTA`, not `PRIOR-ART`.** What exists is:

1. **File listings** — 24 repos list the `.bin`, 31 list `MCD_NACHO_slog.bin`,
   every one a vendor-blob manifest. No format documentation.
2. **The model family** — MODNet (arXiv `2011.11961`, AAAI 2022) is a published
   real-time portrait-matting network, and MNN (`alibaba/MNN`) is a published
   inference framework with a published `Net` FlatBuffer schema. That is genuine
   prior art for **what the artifact is for** and **how its container is shaped**,
   and this note relies on both — the schema citation is what makes §2.2
   decodable at all.
3. **The ABOX channel vocabulary** — `VPCMIN`/`VPCMOUT` and `abox_flush_*` are in
   public Exynos kernel drivers, which is what makes §3.4's tag list identifiable.
4. **A third-party tree ships the `.bin` and `.mnn` as a pair.**
   `9cb14c1ec0/android_vendor_tcl_selene_vzw` `selene_vzw-vendor.mk` (branch
   `master`, 3,583 lines / 304,487 B) installs **both**
   `vendor/etc/camera/modnet_c12v2_in_h416_w544.bin` **and**
   `vendor/etc/camera/modnet_c12v2_in_h416_w544.mnn` from the same directory, and
   also a third sibling `DS2_Dir/modnet_C8_without_IN_h512_.mimage_cache` — a
   **`.mimage_cache`**, i.e. a *pre-converted kernel cache*. That is direct
   external evidence that this model family ships a compiled-kernel companion
   beside the `.mnn` under `vendor/etc/camera` — the same directory layout and
   the same filename stem as the three Fairphone rows. It is a **manifest, not
   documentation**: it names the files and their install location, nothing about
   their bytes, and it does **not** explain why this `.bin`'s header says
   `preferForwardType = CPU` while its body carries 30 OpenCL kernels `[F]`.

What does **not** exist anywhere: any description of the `.bin`'s 30-kernel OpenCL
structure, its foreign offset table, its relationship to the `.mnn`; any
description of `MCD_NACHO_slog.bin`, its 41-record descriptor table, or the
`MCD_NACHO` name. Those are this note's delta.

### 5.5 Corrections to my own earlier DELTA comment `[F]`

The `DELTA` comment posted on this issue at 2026-11-26T11:38:35Z contains four
numbers that today's commands contradict. Corrected here rather than silently
superseded:

| DELTA said | measured 2026-11-26 | note |
|---|---|---|
| `modnet_c12v2_in_h416_w544.bin` → GitHub **0** | **24** | 24 vendor-tree listings; DELTA's 0 was wrong |
| `MCD_NACHO` → **0** everywhere | **31** | 31 listings; DELTA's 0 was wrong |
| `WHENCE` **542,288 B / 11,954 lines** | **542,574 B / 11,958 lines** | DELTA under-reported by 286 B / 4 lines |
| `nacho.bin`: **80 distinct format strings** | **80 occurrences, 40 distinct** | conflation of occurrences with distinct |
| `nacho.bin` is a "**log buffer**" / "ring" | a **printf descriptor table** | no messages are captured; only format strings and line numbers |
| "all `priority=P3`, all `interface_documented=n`" | P1/P2/P3; one `y` | see §1.1 |

The DELTA's substantive conclusions stand (FlatBuffer, MNN identifiers, 30
kernel-adjacent tokens, `.bin` not a prefix of `.mnn`, 99.8 % empty `nacho`,
40 ABOX tags, zero modem tokens). Its counts of prior art and its
"log buffer" reading do not.

---

## 6. Honest negatives `[N]`

- **No payload for `FP4` or `FP5` specifically.** One md5 covers all three
  Fairphone rows, so the FP6 copy is taken as representative. Whether the FP4
  (Snapdragon 750G) and FP5 (QCM6490) ship the *same* file is asserted by the
  matrix, not verified against three separate downloads.
- **No `MCD_NACHO_slog.bin` in `WHENCE`** (0 hits), and `MCD_NACHO` /
  `MCD_NACHO_slog` return **no descriptive page** anywhere — only manifests.
- **No public description of `MCD_NACHO`.** What the letters stand for is `[U]`.
  `NACHO` appears 0 times in `WHENCE` and 0 times in the ABOX driver read.
- **No public description of the `PAM` header tag** at `0x35` in bank 0.
- **No disassembly.** No ARM/Thumb decode was attempted on either artifact; the
  `.bin` carries compiled Mali GPU binaries for which no stdlib disassembler
  exists on this box, and `nacho.bin` carries no code at all (0.0298 bits/byte).
  So **no ISA claim is made for this bucket** — which matches the matrix's
  `isa_identified` being blank on 5 of 5 rows `[F]`.
- **The `bizCode` anomaly is unexplained in mechanism** (§2.4): the observation is
  measured, the cause is `[U]`.
- **`0xfecdba98` in record field 2 is undecoded.** 40 of 41 records carry it,
  the banner record carries 0. It is not a length, not a pointer (it does not
  resolve as one), and not a flag with an obvious meaning `[U]`.
- **Fields 1 and 2 of the record** (`0`/`8`, `0`/`0xfecdba98`) co-vary perfectly
  with the banner-vs-format-string split, so they may be a single 64-bit value or
  two flags; not resolved `[U]`.
- **No `.mnn` row exists in the corpus** (0 rows end in `.mnn`), so the sibling
  file is not part of this bucket's census — it was fetched only to decode the
  `.bin`.
- **`interface_documented=y` on FP6 is dangling** (§1.1): the named path does not
  exist, and the repo's actual file documents `modem.mdt`, not this bucket.

---

## 7. Open items `[U]`

1. What serialiser produced the `.bin`'s offset table, and why it carries the
   `.mnn`'s `bizCode` offset. A real MNN reader run against the `.bin` would
   settle whether it loads, rejects, or silently misparses.
2. Whether `MCD_NACHO_slog.bin` is shipped as a *debug* build artifact only
   (a descriptor table with no messages is consistent with either a template
   never populated or a dump of the table alone).
3. Whether the two 2 MiB banks are a double buffer, two DSP cores, or two
   firmware images. They are near-identical, so the distinction is in the 0x40
   prefix, not the content.
4. `PAM` at `0x35`, and whether it is a magic or a coincidental byte run.

---

## 8. Method `[F]`

- Census: `csv.DictReader` over `upstream-contribution/blob-database/coverage-matrix.csv`,
  grouped on `blob_subfamily`; ranks computed by sorting the 18 populated
  subfamily aggregates, not in-head.
- FlatBuffer: root = `u32le@0`; vtable = `root − s32le@root`; `vtable_size` /
  `object_size` as `u16` pair; field offsets as `u16` array; each present field
  resolved as `field_pos + u32le` and bounds-checked against `len(file)`.
  Schema cross-read from `alibaba/MNN` `schema/default/MNN.fbs`.
- Vectors: length = `u32le` at the resolved target; element `i`'s string/table at
  `target + 4 + 4i + u32le(target + 4 + 4i)`; each element bounds-checked
  individually, which is what exposed the 29/145 vs 145/145 difference.
- `nacho.bin`: `re.finditer(rb"DBT:")` per 2 MiB bank; 20 bytes after each marker
  read as `struct.unpack("<6I")`; offsets masked with `& 0x0fffffff`; each masked
  offset tested for a printable run and for a NUL terminator.
- Entropy: Shannon over the byte histogram, base 2.
- All arithmetic (rank positions, percentages, byte sums, the 24.27× ratio, the
  7,543,336 shortfall) printed by the command that computed it, never carried in
  head.
- Every file opened read-only. No payload committed; the only hex in this note is
  ≤16 bytes per sample.
