# `tinysys` — MediaTek `scp.img` / `sspm.img`, one container, two chip generations (4 rows, 2 devices)

Analysis date: 2026-11-26. Analyst: OC-1 (`100milionseek`), issue
[#2063](https://github.com/adineo-cmd/open-device/issues/2063).

Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data
rows) for the census, cross-read against `research/mediatek/rosemary-census.md`
(rows at lines 145–148) and `docs/devices/xiaomi/Poco_12C/boot.md` §1.
**Twelve payload files** were fetched 2026-11-26, covering **six build sources**
on two devices: the on-disk `mediatek/extract/parts/scp.img` + `sspm.img` pair
(rosemary); `MySelly/vendor_xiaomi_rosemary` and
`android-tweak/android_vendor_xiaomi_rosemary` branch `14.0` (rosemary); and the
earth dump in three independent mirrors — `matu6968`, `ac973k`, and
`MinamiQuartet`. Also read 2026-11-26: `torvalds/linux`
`drivers/remoteproc/mtk_scp.c` (1,651 lines / 44,748 B) and
`include/linux/remoteproc/mtk_scp.h` (69 lines / 1,742 B); MTK LK's
`platform/mediatek/common/sspm/sspm_loader.c` (382 lines / 11,922 B) from
`Gigaset-dev/lk2`; `gitlab.com/kernel-firmware/linux-firmware` `WHENCE`
(11,954 lines / 542,288 B, 271 `Driver:` stanzas); four upstream `scp.img`
builds (mt8183 / mt8186 / mt8192 / mt8195); and LineageOS
`android_device_xiaomi_rosemary` `rootdir/etc/init.mt6785.rc` (1,231 lines,
`lineage-22.2`).

Every number below is command output. No payload is committed; samples are
≤16 bytes of hex.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** Four rows, two basenames, two devices — and the smallest
byte total in the `other` family. But the size is the least interesting thing
about it: **each row is a container, not a file.** `scp.img` and `sspm.img` are
neither ELF nor raw firmware. Both are `mtk_hdr` record chains (magic
`0x58881688`) of `image + cert1 + cert2` triples, and the record names and
sizes inside them are already recorded in this repo as the four
`rosemary-census.md` rows at lines 145–148. This note cites those, does not
re-derive them, and instead supplies the container law that explains them — then
goes one level deeper into the only record that has a **second** container
inside it.

Two findings carry the note.

First, **`sspm.img`'s payload is itself a 3-segment chain under a second magic,
`0x58901690`**, walked by MediaTek's own LK loader as `PT_MAGIC` with segment ids
`0 = DM`, `1 = PM`, `99 = XFILE`. The prior census called the `tinysys-sspm`
body "encrypted/packed" on the strength of body entropy ≥7.95 "from 0x20000".
That is true of exactly one segment: **segment 99, which is 79.4% of the inner
image.** Segment 0 is a plaintext string table at 0.94 bits/byte and segment 1
is a 6.95-bit/byte encoded table. The high-entropy boundary is not `0x20000` —
it is `0x2114c`, the first byte of segment 99's payload.

Second, **file size does not identify a build here, and in three cases it does
not even identify a firmware.** `sspm.img` ships at 663,552 B in two builds with
two md5; earth `sspm.img` ships at 506,000 B in three mirrors with three md5; and
earth `scp.img` ships at 627,968 B in three mirrors with three md5. Worse,
`MySelly` and `android-tweak` publish **the same rosemary `scp.img` firmware** at
2,327,424 B and 2,330,624 B: identical record sizes, byte-identical payloads for
5 of 9 records, and a whole-file diff of exactly **807 bytes** — 10 bytes of
build-date string and three RSA signatures. The 3,200-byte file-size difference
is pure trailing zero padding. Underneath all of it, the census's four
`size_bytes` values are not file sizes at all: each is `ALIGN4K(chain_end)`,
verified 4 of 4. That is why no public copy reproduces a census md5.

---

## 0. Headline

1. **`[F]` The bucket is 4 rows / 2 devices / 2 basenames / 4 sizes / 4 md5 /
   4,132,864 B.** 0.0118% of corpus rows and 0.0059% of corpus bytes; **#12 of
   13** `other` subfamilies by rows and **#11 of 13** by bytes.

2. **`[F]` Both files are `mtk_hdr` chains, not firmware.** `scp.img` is
   **9** headers in **3** `image + cert1 + cert2` groups at 0x0, 0x640, 0xef0,
   0x14b0, 0x1bee00, 0x1bf6b0, 0x1bfc70, 0x2197e0, 0x21a090; `sspm.img` is **3**
   headers at 0x0, 0xa0b30, 0xa13e0. Payloads are 99.68% / 99.52% of the file.

3. **`[F]` The chain law is one rule.** `next = ALIGN16(off + 512 + size)`, with
   `512` the u32 at header `+0x34` on every header of all 12 files. It holds on
   **60 of 60** inter-record links (48 across six `scp.img` files, 12 across six
   `sspm.img` files). Padding is whatever makes the end 16-aligned — observed
   `{3, 4, 5, 8, 10, 12, 13}`, not a constant.

4. **`[F]` A 515/520-byte "gap" is `512 + 3` or `512 + 8`, not an irregularity.**
   Measuring `next_header − (header + size)` folds in the 512-byte header block.
   Both numbers are the same ALIGN16 rule and there is nothing else to explain.

5. **`[F]` `sspm.img`'s payload is a 3-segment `ptimg_hdr_t` chain under
   `0x58901690`**, matching MTK LK's `PT_MAGIC` / `PT_ID_SSPM_DM` / `PM` /
   `XFILE` walk exactly: 71,344 + 64,084 + 522,144 B with `hdr_size = 24`,
   `align = 4`, and the first segment's three fields equal to the prior census's
   `(0x18, 0x116b0, 4)`.

6. **`[F]` The "encrypted body" is 79.4% of the inner image, not all of it.**
   Segment 0 (DM) is 0.9434 bits/byte and 97.5% printable-or-zero; segment 1 (PM)
   is 6.9475 bits/byte and decodes as no ISA; segment 99 (XFILE) is 7.9996
   bits/byte, 100.0% incompressible, and has **0** repeated 16-byte blocks in
   32,634 — so it is not ECB-shaped either.

7. **`[F]` The high-entropy boundary is `0x2114c`, not `0x20000`.** The first
   4 KiB window reaching 7.90 bits/byte is at `0x20e00` (7.9006); no 256-byte
   window anywhere in the body reaches 7.95 — the exhaustive byte-stride maximum
   is **7.4169** at `0x7c323` (7.3299 is the stride-256 grid max). The prior
   census figure reproduces only as a *cumulative-from-offset* statistic
   (`H(body[0x20000:]) = 7.9995`).

8. **`[F]` The ISA is proven on two records and inherited on the rest.**
   `tinysys-scp-CM4_A_dram` decodes 254/256 and 256/256 bytes of its first window
   as Thumb-2, and **0 of 1,433 (rosemary) / 0 of 58 (earth)** windows reach
   256/256 byte coverage under arm32, arm64, mips32 or riscv32 with ≥70
   instructions. `sspm` gets **no** ISA claim: 12 of 250 windows at best.

9. **`[F]` `sspm.img` is size-stable, content-varying — and the mechanism is
   page rounding.** Two rosemary builds sit at 663,552 B with md5 `527ada19…`
   and `c02f4dd9…`; their inner images differ (657,704 vs 657,606 B) but both
   chain ends round up to the same 4 KiB page.

10. **`[F]` Two published `scp.img` sizes are one firmware.** `MySelly`
    (2,327,424 B) and `android-tweak` (2,330,624 B) have identical chain ends
    (2,327,421), identical record sizes on all 9, and differ in 807 bytes total.

---

## 1. The bucket in numbers `[F]`

| quantity | value |
|---|---|
| rows | **4** |
| devices | **2** |
| distinct basenames | **2** (`scp.img`, `sspm.img`) |
| distinct sizes | **4** |
| distinct md5 | **4** |
| total bytes | **4,132,864** |
| % of corpus rows | 0.0118% |
| % of corpus bytes | 0.0059% |
| % of `other` rows | 0.0267% |
| % of `other` bytes | 0.0292% |
| `db_type` | `UNKNOWN` on 4/4 |
| `priority` | `P3` on 4/4 |
| `vendor` | `xiaomi` on 4/4 |
| `soc` | blank on 4/4 |
| `isa_identified` | populated on **2/4** |
| `interface_documented` | `n` on 4/4 |
| `sha256_if_listed` | blank on 4/4 |

`python3` assertion passed:
`630784 + 507904 + 2330624 + 663552 = 4132864`.

All four sizes are exact multiples of 4096 — **569 / 162 / 154 / 124 pages**,
1,009 pages total. That is not a coincidence; §3.3 shows it is the container rule.

### 1.1 Rank inside `other` `[F]`

`other` is 14,987 rows / 14,152,121,440 B across 13 subfamilies. `tinysys` is
second-to-last on rows and third-from-last on bytes.

| rank | by rows | rows | by bytes | bytes |
|---:|---|---:|---:|---:|
| 1 | `misc` | 10,720 | `misc` | 8,498,193,635 |
| 2 | `camera` | 1,611 | `camera` | 4,563,019,282 |
| 3 | `touch` | 880 | `touch` | 516,418,690 |
| 4 | `media` | 470 | `fingerprint` | 387,540,764 |
| 5 | `audio` | 422 | `sensors` | 86,541,968 |
| 6 | `fastchg` | 315 | `fastchg` | 36,989,007 |
| 7 | `fingerprint` | 284 | `media` | 29,190,348 |
| 8 | `oled` | 157 | `nfc` | 9,677,922 |
| 9 | `nfc` | 75 | `esim` | 8,407,085 |
| 10 | `esim` | 41 | `audio` | 5,418,315 |
| 11 | `sensors` | 5 | **`tinysys`** | **4,132,864** |
| 12 | **`tinysys`** | **4** | `oled` | 4,068,320 |
| 13 | `gpu-compute` | 3 | `gpu-compute` | 2,523,240 |

`tinysys` is **one of two** (family, subfamily) buckets in the whole corpus with
exactly 2 devices — the other is `wifi/wifi-bt-combo` (4 rows, 1,671,348 B). The
corpus has **18** named subfamilies across 9 families, or **26** buckets once the
8 blank-subfamily strata are counted; the count is the same either way, and only
these two have exactly 2 devices (next smallest is 3). What is unique to
`tinysys` is that its rows are not leaf files.

### 1.2 Four rows, four payloads `[F]`

| device | codename | filename | size (B) | md5 | `db_path` |
|---|---|---|---:|---|---|
| `Redmi_10S` | `rosemary` | `scp.img` | 2,330,624 | `981608d9eef7b04a5d93fad65293b0b8` | `xiaomi/rosemary/radio` |
| `Redmi_10S` | `rosemary` | `sspm.img` | 663,552 | `cc1936008c5ccdfbb99f3b83d2c093d4` | `xiaomi/rosemary/radio` |
| `Poco_12C` | `earth` | `scp.img` | 630,784 | `8cf28e290098f7328bc2d6b2ba189312` | `xiaomi/earth/radio` |
| `Poco_12C` | `earth` | `sspm.img` | 507,904 | `be3e30ee64e62b5b5632fd4c82f4447f` | `xiaomi/earth/radio` |

Unlike the `sensors` and `esim` buckets, **`size → md5` is a bijection here**:
4 sizes, 4 md5, one each. So within the census there is no "same size, different
build" case — which is exactly why the size-stability of §6.3 was invisible from
the matrix and only appears once public builds are compared.

The two devices are a generation apart: `Poco_12C` = `earth`, MT6768-class (the
vendor tree is `android_vendor_xiaomi_earth`, the dump is `matu6968`); `Redmi_10S`
= `rosemary`, MT6785 Helio G95.

### 1.3 Where the rows sit `[F]`

All four rows are `xiaomi/<codename>/radio`, and `radio` is a 1,850-row /
123-device directory that is overwhelmingly not `tinysys`: 1,511 rows have a
blank subfamily, 261 `misc`, 63 `hyp`, 7 `dtb`, 4 `tinysys`, 3 `camera`, 1
`audio`. Only 21 of the 123 `radio` devices are `xiaomi`, and those 21 carry 360
rows.

Sibling MTK firmware in the same directory is filed differently: `gz.img` and
`tee.img` are `misc`, `spmfw.img` is `misc`, while `lk.img` / `md1img.img` /
`preloader_raw.img` have a blank subfamily. The census records all of them as
`UNKNOWN` containers (§8.4). `tinysys` is a *newer* label than its siblings, not
a mislabel.

`scp.img` and `sspm.img` each appear on exactly these two devices and nowhere
else in the 33,917-row corpus.

---

## 2. The container: an `mtk_hdr` chain, and the ALIGN16 law `[F]`

### 2.1 The 512-byte header block

Field map verified on all 12 headers of the two on-disk files, and on all 72
headers across the 12 files:

| offset | width | meaning | observed |
|---:|---:|---|---|
| `+0x00` | 4 | magic | `0x58881688` on 72/72 |
| `+0x04` | 4 | payload size, u32 | 957 … 1,905,524 |
| `+0x08` | 32 | **name**, NUL-padded ASCII (`0x08..0x28`) | `tinysys-loader-CM4_A`, `cert1`, … |
| `+0x28` | 4 | class sentinel | `0x12345678` on cert, `0xffffffff` on image |
| `+0x2c` | 4 | fill | `0xffffffff` on 72/72 |
| `+0x30` | 4 | **second magic** | `0x58891689` on 72/72 |
| `+0x34` | 4 | **payload offset** — the field the chain law uses | `0x200` = 512 on 72/72 |
| `+0x38` | 4 | version | `1` on 72/72 |
| `+0x3c` | 4 | record subtype | `0` image, `0x02000000` cert1, `0x02000002` cert2 |
| `+0x40` | 4 | terminal flag | `0` on 60/72, `1` on the **last** `cert2` of each file (12/12) |
| `+0x44` | 4 | payload alignment | `0x10` = 16 on 72/72 |
| `+0x48` | 4 | zero | `0` on 72/72 |
| `+0x4c` | 4 | class sentinel | `0x22345678` on cert, `0` on image |
| `+0x50` | 432 | fill | **all `0xff`** on 72/72 |

Two decodes worth recording, because both look like errors at first glance:

- `+0x08` is the **name**, not a type tag followed by a name. The field is
  32 bytes wide and the 20-byte name `tinysys-loader-CM4_A` fills it. Reading
  `+0x08` as a 4-byte type gives `'tiny'` = `0x796e6974` and `'cert'` =
  `0x74726563` — ASCII-in-u32, a real property but a **derived** one; there is
  no separate type field.
- `+0x34 = 512` is **load-bearing**. It is not "header size" decoration: it is
  the value the chain law adds. The payload of record *n* begins at
  `off + 0x34`, and the 432-byte `0xff` fill is what pads the block out to it.

### 2.2 The law

```
next_header = ALIGN16( off + 512 + size )
publish_16  = ALIGN16( last_off + 512 + size )
publish_4k  = ALIGN4K( last_off + 512 + size )
```

Verified in full on all 12 payload files:

| build source | file | bytes | headers | links | law holds | pad values | `+0x34` |
|---|---|---:|---:|---:|---|---|---:|
| rosemary on-disk | `scp` | 2,207,744 | 9 | 8 | **8/8** | `{3, 8}` | 512 |
| rosemary on-disk | `sspm` | 663,552 | 3 | 2 | **2/2** | `{3, 8}` | 512 |
| rosemary `MySelly` | `scp` | 2,327,424 | 9 | 8 | **8/8** | `{3,4,8,12}` | 512 |
| rosemary `MySelly` | `sspm` | 661,824 | 3 | 2 | **2/2** | `{3, 10}` | 512 |
| rosemary `android-tweak` | `scp` | 2,330,624 | 9 | 8 | **8/8** | `{3,4,8,12}` | 512 |
| rosemary `android-tweak` | `sspm` | 663,552 | 3 | 2 | **2/2** | `{3, 10}` | 512 |
| earth `matu6968` | `scp` | 627,968 | 9 | 8 | **8/8** | `{3,4,5,8}` | 512 |
| earth `matu6968` | `sspm` | 506,000 | 3 | 2 | **2/2** | `{3, 13}` | 512 |
| earth `ac973k` | `scp` | 627,968 | 9 | 8 | **8/8** | `{3,4,5,8}` | 512 |
| earth `ac973k` | `sspm` | 506,000 | 3 | 2 | **2/2** | `{3, 13}` | 512 |
| earth `MinamiQuartet` | `scp` | 627,968 | 9 | 8 | **8/8** | `{3,4,5,8}` | 512 |
| earth `MinamiQuartet` | `sspm` | 506,000 | 3 | 2 | **2/2** | `{3, 13}` | 512 |

60 of 60 links. Header offsets are free-running, not on a grid: the 16-byte
alignment of *ends* plus a variable payload size puts headers at 0x0, 0x640,
0xef0, 0x14b0, 0x1bee00, … — none of which are multiples of 512.

### 2.3 The 515/520 trap `[F]`

Measuring the gap as `next_header − (header_offset + size)` yields, for the
on-disk `scp.img`, `8, 3, 3, 8, 3, 3, 8, 3, 3` — and if you instead measure
`next − (off + size)` you are folding in the 512-byte header block, producing
520 and 515:

```
512 + 3 = 515
512 + 8 = 520
```

There is no irregular cluster to explain. **A gap of 515 or 520 in this
container is `payload_offset(512) + ALIGN16 padding(3 or 8)`.** The "cluster"
is an artifact of subtracting the wrong baseline. The correct statement is
§2.2, and it holds on all 60 links.

The full pad set across the 12 files is `{3, 4, 5, 8, 10, 12, 13}` — the
residue needed to reach a 16-byte boundary from `(end mod 16) ∈ {13, 12, 11, 8,
6, 4, 3}`. Nothing here is vendor-specific padding.

### 2.4 The second magic `0x58891689` `[F]`

It appears **exactly once per header block** at `header + 0x30`: 9 occurrences in
each `scp.img` (0x30, 0x670, 0xf20, 0x14e0, …) and 3 in each `sspm.img` (0x30,
0xa0b60, 0xa1410) — 9/9 and 3/3, one per header, no extras and no omissions. It
is related to the primary magic by a single XOR constant:

```
0x58881688 ^ 0x58891689 = 0x00010001
```

but the two are distinct constants and not interchangeable: `0x58881688`
delimits a record, `0x58891689` delimits the parameter area inside that record's
header. The three fields that follow it are invariant across all 12 files:

```
0x58891689  0x00000200  0x00000001  ...  0x00000010
            ^ 512       ^ 1            ^ 16
```

`[I]` Because `0x34` (immediately after it) is the `payload_offset` the chain law
uses, this sub-record looks like the header's "parameter block" opening — not a
separate container object. I have not proven that, so it stays `[I]`. It is
**not** called a container here.

### 2.5 Header facts by record class `[F]`

| class | name | `0x28` | `0x2c` | `0x3c` | `0x4c` |
|---|---|---|---|---|---|
| image | `tinysys-*` | `ffffffff` | `ffffffff` | `00000000` | `00000000` |
| cert#1 | `cert1` | `12345678` | `ffffffff` | `02000000` | `22345678` |
| cert#2 | `cert2` | `12345678` | `ffffffff` | `02000002` | `22345678` |

Those four sentinels are stable on **72/72** headers across all 12 files, with
zero exceptions. `0x12345678` / `0x22345678` are placeholder-style magic
constants, not per-build values — which is why they are the strongest single
test that two files came from the same tool.

---

## 3. What is inside: 9 records and 3 records `[F]`

### 3.1 `scp.img` — three `image + cert1 + cert2` groups

On-disk build, 2,207,744 B:

| # | offset | name | size (B) | payload md5 (first 10) | class |
|---:|---:|---|---:|---|---|
| 0 | `0x0` | `tinysys-loader-CM4_A` | 1,080 | `a6d868f78f` | image |
| 1 | `0x640` | `cert1` | 1,709 | `753a5ded98` | cert |
| 2 | `0xef0` | `cert2` | 957 | `f5677a8652` | cert |
| 3 | `0x14b0` | `tinysys-scp-CM4_A` | 1,824,584 | `9dc88ff4f4` | image |
| 4 | `0x1bee00` | `cert1` | 1,709 | `2cbb6100d2` | cert |
| 5 | `0x1bf6b0` | `cert2` | 957 | `86c1afe7aa` | cert |
| 6 | `0x1bfc70` | `tinysys-scp-CM4_A_dram` | 366,952 | `1844dfd535` | image |
| 7 | `0x2197e0` | `cert1` | 1,709 | `090dc28362` | cert |
| 8 | `0x21a090` | `cert2` | 957 | `b9157dc45b` | cert |

Budget: 9 × 512 = 4,608 B of headers + 2,200,614 B of payloads + 39 B of
inter-record pad = 2,205,261 B = `0x21a64d`, exactly the last declared end.
Payloads are **99.68%** of the file; the 1,080-byte loader is **0.05%**; the six
certificate records are **0.36%** (7,998 B); the multibin image alone is
**82.6%**.

The prior census rows at `research/mediatek/rosemary-census.md:145-148` list
`tinysys-loader-CM4_A` at 1,080 B, `tinysys-scp-CM4_A` at 1,824,584 B and
`tinysys-scp-CM4_A_dram` at 366,952 B — all **exactly reproduced** here, from the
same file. So the census did split this chain correctly; the delta is that they
are records in one file, in three cert-paired groups, and the group structure is
what the loader consumes.

The earth build has the same 9 names in the same order at different offsets:

| earth record | offset | size (B) |
|---|---:|---:|
| `tinysys-loader-CM4_A` | `0x0` | 1,080 |
| `cert1` / `cert2` | `0x640` / `0xef0` | 1,709 / 957 |
| `tinysys-scp-CM4_A` | `0x14b0` | 599,291 |
| `cert1` / `cert2` | `0x93bb0` / `0x94460` | 1,709 / 957 |
| `tinysys-scp-CM4_A_dram` | `0x94a20` | 14,956 |
| `cert1` / `cert2` | `0x98690` / `0x98f40` | 1,709 / 957 |

Earth budget: 4,608 + 623,325 + 32 = 627,965 = `0x994fd`. Payloads **99.26%**.

Note the shape difference: the earth SCP image is **599,291 B** against
rosemary's 1,824,584 B, and its DRAM image is **14,956 B** against 366,952 B — a
factor of 3 and a factor of 25. That is not a build variant of one chip; it is
two different SCP firmware generations, and it is why the two `scp.img` sizes are
630,784 and 2,330,624 and not near each other.

### 3.2 `sspm.img` — one image, one cert pair

On-disk build, 663,552 B:

| # | offset | name | size (B) | declared end | ALIGN16 |
|---:|---:|---|---:|---:|---:|
| 0 | `0x0` | `tinysys-sspm` | 657,704 | `0xa0b28` | `0xa0b30` |
| 1 | `0xa0b30` | `cert1` | 1,709 | `0xa13dd` | `0xa13e0` |
| 2 | `0xa13e0` | `cert2` | 957 | `0xa199d` | `0xa19a0` |

Budget: 1,536 + 660,370 + 11 = 661,917 = `0xa199d`. Payloads **99.52%**; the
inner image is **99.1%** of the file. Then `ALIGN4K(0xa199d) = 0xa2000 =
663,552` — which **is the file size and the census size**.

The 657,704 B figure is the prior census's `sspm` payload size
(`rosemary-census.md:148`), reproduced exactly. So the two numbers that look
contradictory — "663,552" and "657,704" — are the **outer file** and the **inner
declared image** of the same record. There is no conflict.

Earth `sspm.img` (506,000 B) is the same 3-record shape: `tinysys-sspm` 501,779 B
at `0x0`, then `cert1` 1,709 and `cert2` 957, with headers at `0x0`, `0x7aa20`,
`0x7b2d0` and chain end 505,997 = `0x7b88d`. Budget 1,536 + 504,445 + 16 =
505,997. Same law, same record names.

### 3.3 Where the size arithmetic shows up `[F]`

| build | file | chain end | `ALIGN16` | `ALIGN4K` | as published | convention | trailing zeros |
|---|---|---:|---:|---:|---:|---|---:|
| rosemary on-disk | `scp` | 2,205,261 | 2,205,264 | 2,207,744 | 2,207,744 | **ALIGN4K** | 2,483 |
| rosemary on-disk | `sspm` | 661,917 | 661,920 | 663,552 | 663,552 | **ALIGN4K** | 1,635 |
| rosemary `MySelly` | `scp` | 2,327,421 | 2,327,424 | 2,330,624 | 2,327,424 | **ALIGN16** | 3 |
| rosemary `MySelly` | `sspm` | 661,821 | 661,824 | 663,552 | 661,824 | **ALIGN16** | 3 |
| rosemary `android-tweak` | `scp` | 2,327,421 | 2,327,424 | 2,330,624 | 2,330,624 | **ALIGN4K** | 3,203 |
| rosemary `android-tweak` | `sspm` | 661,821 | 661,824 | 663,552 | 663,552 | **ALIGN4K** | 1,731 |
| earth (all 3 mirrors) | `scp` | 627,965 | 627,968 | 630,784 | 627,968 | **ALIGN16** | 3 |
| earth (all 3 mirrors) | `sspm` | 505,997 | 506,000 | 507,904 | 506,000 | **ALIGN16** | 3 |

Both conventions ship. A build is published at `ALIGN16` or `ALIGN4K`
independently of its content, and the trailing-zero column is exactly the
difference. **No file has zero trailing padding**: even the `ALIGN16` builds
carry 3 bytes, because `ALIGN16(chain_end)` is 3 bytes past the last declared
end in every case here.

**The census used the ALIGN4K convention.** All four census `size_bytes` values
are `ALIGN4K(chain_end)` of a build whose record layout we can match:

| census row | `ALIGN4K(chain_end)` | census size | match |
|---|---:|---:|---|
| `Redmi_10S` `scp` | `ALIGN4K(2,327,421)` = 2,330,624 | 2,330,624 | **yes** |
| `Redmi_10S` `sspm` | `ALIGN4K(661,821)` = 663,552 | 663,552 | **yes** |
| `Poco_12C` `scp` | `ALIGN4K(627,965)` = 630,784 | 630,784 | **yes** |
| `Poco_12C` `sspm` | `ALIGN4K(505,997)` = 507,904 | 507,904 | **yes** |

4 of 4. So a census `size_bytes` for this subfamily is **a page-rounded chain
end, not a byte count of any file** — which is why no published copy reproduces
it byte-for-byte, and why padding our files out to the census size still does not
match md5 (§10).

---

## 4. The inner container: `0x58901690` is `PT_MAGIC` `[F]`

### 4.1 The upstream definition

MediaTek's LK `sspm_loader.c` — `Gigaset-dev/lk2`,
`platform/mediatek/common/sspm/sspm_loader.c`, 382 lines / 11,922 B — defines
the struct and the walk:

```c
struct ptimg_hdr_t {
    unsigned int magic;     /* magic */
    unsigned int hdr_size;  /* data size */
    unsigned int img_size;  /* img size */
    unsigned int align;     /* align */
    unsigned int id;        /* image id */
    unsigned int addr;      /* memory addr */
};
...
hdr = (struct ptimg_hdr_t *) load_addr;
while (hdr->magic == PT_MAGIC) {
    img = ((char *) hdr) + hdr->hdr_size;
    switch (hdr->id) {
    case PT_ID_SSPM_PM:    pmimg  = img; pmsize  = hdr->img_size; break;
    case PT_ID_SSPM_DM:    dmimg  = img; dmsize  = hdr->img_size; break;
    case PT_ID_SSPM_CPM:   cpmimg = img; cpmsize = hdr->img_size; break;
    case PT_ID_SSPM_XFILE: ximg   = img; xsize   = hdr->img_size; break;
    default: dprintf(CRITICAL, "sspm warning: Ignore unknown sspm image_%d\n", hdr->id);
    }
    img += ROUNDUP(hdr->img_size, hdr->align);
    hdr = (struct ptimg_hdr_t *) img;
}
```

The loader also documents the trailer:
`info->xfile_sz = sizeof(struct ptimg_hdr_t) + xsize + sizeof(unsigned int);`
with the comment `/* with postfix 'END'*/`.

`[N]` The four `PT_ID_SSPM_*` numeric values live in a per-SoC `sspm_plat.h`
which we did **not** fetch; only the four names are in the `.c`. The id→name map
below is therefore `[I]` from the walk order and the segment contents, not from a
header file. `PT_MAGIC` itself is also not defined in the `.c` — the value
`0x58901690` comes from the bytes, matched to the struct layout.

### 4.2 The walk, reproduced on both builds `[F]`

`0x58901690` occurs **3 times** in each `sspm.img` and **0 times** in every
`scp.img`. On-disk rosemary, at file offsets `0x200`, `0x118c8`, `0x21334` —
i.e. body-relative `0x0`, `0x116c8`, `0x21134`, where the body begins at `0x200`
(the first byte after the 512-byte `mtk_hdr` block).

| build | body off | `hdr_size` | `img_size` | `align` | `id` | `addr` |
|---|---:|---:|---:|---:|---:|---:|
| rosemary | `0x0` | 24 | 71,344 | 4 | **0** (DM) | 0 |
| rosemary | `0x116c8` | 24 | 64,084 | 4 | **1** (PM) | 0 |
| rosemary | `0x21134` | 24 | 522,144 | 4 | **99** (XFILE) | 0 |
| earth | `0x0` | 24 | 8,852 | 4 | **0** (DM) | 0 |
| earth | `0x22ac` | 24 | 55,608 | 4 | **1** (PM) | 0 |
| earth | `0xfbfc` | 24 | 437,184 | 4 | **99** (XFILE) | 0 |

Walk check, rosemary: `24 + 71,344 = 71,368 = 0x116c8` → next header; `24 +
64,084 = 64,108`; `0x116c8 + 64,108 = 0x21134` → next header; `24 + 522,144 =
522,168`; `0x21134 + 522,168 = 0xa08ec`. The body ends at 657,704 = `0xa0928`,
so **60 bytes remain** — the `END` trailer. Earth: walk reaches `0x7a7d4` of
`0x7a813`, **63 bytes** remaining.

The first segment's fields at body `0x04 / 0x08 / 0x0c` are `24 / 71,344 / 4` —
**exactly** the `(0x18, 0x116b0, 4)` triple recorded in
`rosemary-census.md:148`. So the prior census's inner-`sspm` header claim is
**verified correct**, and cited here as corroborated rather than re-derived.

Earth's DM segment is **8,852 B** against rosemary's 71,344 B — a factor of 8 —
which is the same generation gap seen in `scp.img`'s record sizes.

### 4.3 Three segments, three different things `[F]`

Rosemary, measured segment by segment:

| segment | id | size (B) | share of inner | entropy (bits/byte) | zlib -9 ratio |
|---|---:|---:|---:|---:|---:|
| DM | 0 | 71,344 | 10.8% | **0.9434** | 6.4% |
| PM | 1 | 64,084 | 9.7% | 6.9475 | 72.6% |
| XFILE | 99 | 522,144 | **79.4%** | **7.9996** | **100.0%** |

Earth: DM 8,852 B at 4.5298, PM 55,608 at 6.9287, XFILE 437,184 at 7.9996. The
structural proportions are the same on both chips; only the sizes move.

**Segment 0 (DM) is a plaintext string/data table.** 97.5% of its bytes are
printable-ASCII-or-NUL, and it contains 155 printable runs of ≥6 characters on
rosemary. The first dozen, with offsets:

```
0x00008  vproc2                     0x00054  CEN_EMI_DEBUG_0
0x00010  vsram_proc2                0x00064  CEN_EMI_DEBUG_1
0x0001c  vproc1                     0x00074  CEN_EMI_DEBUG_2
0x00024  vsram_proc1                0x00084  CEN_EMI_DEBUG_3
0x00030  [EMI] %s: 0x%x             0x00094  CEN_EMI_DEBUG_4
0x00041  ----------------           0x000a4  CEN_EMI_DEBUG_5
0x000e4  CEN_EMI_DEBUG_9            ...
0x00114  EMI_IOCL                    0x002fc  [FH] DDS stable timeout ...
0x00130  EMI_IOCM                    0x0037c  mcdi Pre-pllbuck_req ...
                                     0x003ec  vgpu11
                                     0x00410  [PMU]vp
```

plus `[SWPM]` ×2, `thermal` ×18, `DDFS`, `DVFS`, `picachu` ×3, `mcdi` ×2,
`Tmr Svc`, `sspm doesn't leave SLP`, and a build stamp at `0x0dbc`:
`Build time: %s %s` / `Aug 11 2023` / `19:13:50`. The earth DM is the same
species — `cm_mgr_sysreg_read 0x%x fail!`, `vproc12`, `vsram_proc12`, the same
`CEN_EMI_DEBUG_*` block — 142 runs.

So DM is the SSPM's **debug/diagnostic name table**, and it is the reason
`sspm.img` has readable strings at all. The prior census records `vproc1/vproc2`
and `[EMI] %s` against this record and calls the body "encrypted"; DM is not
encrypted, and the build stamp lives here rather than in the code segment.

**Segment 1 (PM) is an encoded table, and no ISA is claimed.** Evidence against
every reading of it as code:

| test | result |
|---|---|
| Thumb-2, 256-B windows fully byte-decoded | **12 of 250** (4.8%) |
| Thumb-2, best 256-instruction window | 256 insns covering **42 bytes** |
| arm32, same | **0 of 250** |
| byte-swap-16 variant | 19 / 250 |
| byte-swap-32 variant | 17 / 250 |
| XOR 0xff variant | **0 / 250** |
| `push`-prologue halfwords (`b510`, `2de9`, `f0b5`, `30b5`) | **0** |
| printable-ASCII share | **20.4%** |
| distinct u32 at 4-byte stride | 13,071 of 16,021 |

It opens with 32 four-byte records sharing a `0x001e` prefix over `0x00..0x80`,
then dense 4-byte values — the shape of a register/parameter table, not a
function. Both chips do it (`earth` PM opens `1e0000401e005731…`, same tag). It
is **not** decodable as ARM, ARM64, MIPS or RISC-V, and I make no ISA claim for
it. The lopestom gist describes `sspm.img` as "partially encrypted", which is
consistent: DM plaintext, PM encoded, XFILE incompressible.

**Segment 99 (XFILE) is uniform-incompressible and not ECB.** 7.9996 bits/byte
over 522,144 B; zlib -9 produces a **larger** output than input (100.0%). Zero
repeated 16-byte blocks in 32,634 — a uniform 128-bit source predicts ~1.6×10⁻³⁰
duplicates, and a real ECB-mode ciphertext of this size would show dozens. Zero
printable runs of ≥16 characters. First 16 bytes:
`8a69e0b09cd6422443d0cbe5a0db6969`. So it is **not** a block cipher in ECB, and
not a lookup table; it is high-entropy data whose encoding is `[U]`.

### 4.4 The entropy claim, scoped `[F]`

`rosemary-census.md:148` says `body entropy 7.95+ from 0x20000`. Measured on the
actual body:

| body offset | 4 KiB window | 256 B window | `H(body[o:])` cumulative |
|---:|---:|---:|---:|
| `0x1f000` | 6.731 | — | — |
| `0x20000` | 6.786 | — | **7.9995** |
| `0x20e00` | **7.901** | — | — |
| `0x21000` | 7.937 | 6.018 | — |
| `0x21100` | 7.950 | 6.858 | — |
| `0x2114c` | 7.955 | 7.151 | 7.9996 |
| `0x22000` | 7.955 | 7.190 | 7.9996 |

The maximum 4 KiB entropy before `0x20e00` is 7.859, so `0x20e00` really is the
first crossing of 7.90. Three corrections fall out:

1. **`0x20000` is not a boundary.** The cumulative entropy *from* `0x20000` is
   7.9995, which is where the census number comes from — but as a *sliding
   baseline*, not a window. A 4 KiB window at `0x20000` is 6.786.
2. **The first 4 KiB window ≥7.90 is `0x20e00`; the exact structural boundary is
   `0x2114c`**, the first byte of segment 99's payload (segment header at
   `0x21134`, `hdr_size` 24). The 0x20e00 crossing is leakage: segment 99's
   header and a few of its first bytes are inside that window.
3. **No 256-byte window anywhere in the 657,704-byte body reaches 7.95.** The
   maximum depends on the stride: 7.3299 at stride 256 (`0x7c300`), 7.3377 at
   128, 7.3939 at 64, 7.4110 at 16, **7.4169 at stride 1** (`0x7c323`). A 4 KiB
   figure of 7.95 is reachable; a 256 B figure of 7.95 is not, at any stride.

So the correct statement is: **79.4% of the inner image, exactly segment 99, is
incompressible; the other 20.6% is plaintext or a table.** "The sspm body is
encrypted" overstates it by a factor of five.

### 4.5 The `END` trailer `[F]`

```
rosemary: "END" + "alps-mp-s0.mp1.tc8sp-cs2-V1.31_xiaomi.s0mp1.k85v1.64.k419"   (60 B)
earth:    "END" + "alps-mp-s0.mp1.tc8sp2-cs1-V1.3_huaqin.xm.s0mp1.k69v1.64.k419" (63 B)
```

`END` is 3 bytes ASCII at the exact end of the walked segments, followed by a
platform build string with no NUL terminator. This is the postfix the LK loader
comment names, and the only place in either file where the SoC's platform branch
(`s0.mp1`) and vendor (`xiaomi` vs `huaqin`) are written in cleartext.

`sspm.img` carries **no** codename marker: `rosemary` and `earth` both return 0
occurrences in both files. The only device-identity signal in the whole bucket is
in `scp.img` (§5.4).

---

## 5. ISA: what is proven, and what is inherited `[F]`

### 5.1 The loader's vector table — both chips

`tinysys-loader-CM4_A`, 1,080 B = 270 u32, opens with a textbook Cortex-M vector
table:

| field | rosemary | earth |
|---|---:|---:|
| word 0 (initial SP) | `0x538` | `0x538` |
| word 1 (reset) | `0x1e1` | `0x1e1` |
| reset odd → Thumb bit | **1** | **1** |
| word 2 (default handler) | `0x26d` | `0x261` |
| consecutive entries equal to word 2 | **78** | **78** |
| covering | `0x08..0x13c` | `0x08..0x13c` |
| nonzero words in 270 | 158 | 155 |
| last nonzero word index | 267 (`0x42c`) | 267 |

Then code. Disassembling the targets confirms all three:

```
reset 0x1e1 -> 0x1e0:  cpsid i ; bl #0x140 ; bl #0x1ae ; ldr r2,[pc,#0x6c]
handler 0x26d -> 0x26c: b.w #0x1b2
0x140:                  ldr r1,[pc,#0x70] ; bic r1,r1,#0xf ; ldr r0,[pc,#0x70] ...
```

`[F]` **The census's "6× handler 0x26d" (`rosemary-census.md:145`) is wrong by a
factor of 13.** It is 78 consecutive identical entries, not 6. The vector table
runs 0x08..0x13c (312 bytes of handlers, 80 words total including SP and reset)
and then the first real code word `0xf021491c` at `0x140` sustains a clean
Thumb-2 decode.

The two chips' loaders are **not the same bytes**: 129 differing bytes, of which
78 are the single low byte of every handler word (`0x26d` → `0x261`) and 51 lie
beyond `0x140`. So the loader differs by one address and one small code block —
consistent with a stub whose only job is to jump into the multibin.

### 5.2 The DRAM record decodes as Thumb-2, and nothing else does

`tinysys-scp-CM4_A_dram`, first 256-byte window:

| build | instructions | bytes covered | first instructions |
|---|---:|---:|---|
| rosemary | 93 | **254 / 256** | `push {r4,lr}` ; `mov r4,r0` ; `mov r0,r1` ; `movs r1,#0` ; `mov r3,r2` ; `mov r2,r1` ; `blx r4` |
| earth | 106 | **256 / 256** | `bx lr` ; `movs r0,r0` ; `push.w {r4,r5,r6,r7,r8,lr}` ; `ldr r2,[pc,#0x9c]` ; `ldr r3,[r2]` ; `tst.w r3,#8` |

Rosemary's opening 7-instruction sequence is byte-identical to what
`rosemary-census.md:147` records, so the prior decode is **reproduced**; the
`254/256` (not `256/256`) byte count is the one refinement, below.

The decisive test is not a single window but an impossibility argument. A
fixed-width 4-byte ISA can place at most **64** instructions in 256 bytes. So a
window that decodes 256/256 bytes *and* contains ≥70 instructions can only be a
2-or-4-byte variable-length encoding — Thumb-2. Counting such windows:

| blob | bytes | thumb-2 | arm32 | arm64 | mips32 | riscv32 |
|---|---:|---:|---:|---:|---:|---:|
| rosemary `dram` | 366,952 | **695 / 1,433** | 0 | 0 | 0 | 0 |
| earth `dram` | 14,956 | **41 / 58** | 0 | 0 | 0 | 0 |
| rosemary multibin (content) | 388,085 | **979 / 1,515** | 0 | 0 | 0 | 0 |
| earth multibin (content) | 188,329 | **436 / 735** | 0 | 0 | 0 | 0 |

Zero for every 4-byte ISA on every blob. Full-record byte coverage under Thumb-2
(any instruction count) is 49.1% of windows for rosemary `dram` (avg 152.7/256)
and 70.7% for earth (avg 231.6/256) — the rest of the record is data and literal
pools, which is exactly what a `.dram` section should be.

### 5.3 The `256/256` metric needs one qualification `[F]`

`rosemary-census.md:147` and the `Redmi_10S` `scp.img` `isa_identified` field
both say `256/256 decode`. That is **reproducible only as an instruction count**:
requesting 256 instructions from a 4 KiB window returns 256 instructions, but
they cover **648 bytes** of the window (rosemary) / **632** (earth). As *byte*
coverage of a single 256-byte window it is 254/256 (rosemary) and 256/256
(earth) — the rosemary record has one 2-byte halfword in its first window that
capstone does not consume.

So the claim is true and the metric is defensible, but the number means
"256 instructions returned", not "256 of 256 bytes decoded". The full-record
figures (49.1% / 70.7% of windows fully covered) are the honest scale. This does
not weaken the ISA conclusion at all — §5.2's impossibility argument is much
stronger evidence than any single window.

### 5.4 The FreeRTOS evidence is in the multibin, not the DRAM record `[F]`

This is a correction to prior art. `rosemary-census.md:147` attributes
`kernel/FreeRTOS/Source/portable/GCC/ARM_CM4F/port.c`, `.../tasks.c` and
`FreeRTOS %s(build:%s %s)` to `tinysys-scp-CM4_A_dram`. They are not there:

| pattern | `tinysys-scp-CM4_A` (multibin) | `tinysys-scp-CM4_A_dram` |
|---|---:|---:|
| `FreeRTOS` | **7** | **0** |
| `kernel/` | 7 | **0** |
| `ARM_CM4F` | 1 | **0** |
| `port.c` | 2 | **0** |
| `tasks.c` | 1 | **0** |

All 7 source paths are in the multibin, at `0x4f768..0x4f947` (rosemary):

```
0x04f768  kernel/FreeRTOS/Source/list.c
0x04f786  kernel/FreeRTOS/Source/portable/GCC/ARM_CM4F/port.c
0x04f7d3  kernel/FreeRTOS/Source/portable/MemMang/heap_4.c
0x04f804  kernel/FreeRTOS/Source/queue.c
0x04f856  kernel/FreeRTOS/Source/tasks.c
0x04f896  kernel/FreeRTOS/Source/timers.c
0x04f947  kernel/service/common/src/wakelock.c
```

Same seven on earth, at `0x27ace..0x27cf8`. The DRAM record carries no strings of
interest — its 1,208 printable runs of ≥5 characters are all code-adjacent byte
sequences (`AEKFL`, `` `FHFK ``, `"Yh@H1`). So the DRAM record supplies the
**decode** and the multibin supplies the **runtime identity**. Both are in
`scp.img`; only one of them is a `.dram` section.

The multibin also carries the FreeRTOS banner, which turns out to be the only
per-build discriminator in the file:

| build | banner | date | time |
|---|---|---|---|
| rosemary on-disk | `FreeRTOS %s(build:%s %s)` / `V10.0.1` | `Dec 17 2024` | `06:24:17` |
| rosemary `MySelly` | same | `May 19 2023` | `03:58:51` |
| rosemary `android-tweak` | same | `Nov 22 2023` | `11:59:04` |
| earth `matu6968` | same | `Feb  2 2024` | `12:25:30` |

FreeRTOS **V10.0.1** on both chips, three different build dates on rosemary
alone. Rosemary also carries `2.4.4-9d0f65f` at `0x44184`,
`STAMP_K_VER_18041204` at `0x477f8`, `SCP_VOW_TASK_VER` at `0x4a07b`,
`[July 05, 2017]` and `[Jan 10, 2018]`; earth has `STAMP_K_VER_18041204` and
none of the others (`2.4.4`, `SCP_VOW_TASK_VER`, `ICM4`, `BMI` all return 0).

And there is a device-provenance marker the census did not record: the 4-byte
constant **`0x55aaaa55`** at multibin-relative `0x140` (file `0x17f0`, the same
offset on all four `scp.img` builds), followed by the NUL-padded codename:

```
55aaaa55 "rosemary" 00 00 00 00    (rosemary, all 3 builds)
55aaaa55 "earth"    00 00 00 00    (earth)
```

`0x55aaaa55` occurs **once** in each `scp.img` and **zero** times in each
`sspm.img`. It is the cleanest single check of which device a `scp.img` belongs
to — one 16-byte window, no heuristics.

Structure of the multibin record, for completeness: rosemary 1,824,584 B of which
**1,392,371 B (76.3%) is one contiguous zero run at `0x5ebf5`**, with 388,085 B
of live content before it and 44,128 B after. Earth is the same shape, 60.7%
zero (363,843 B at `0x2dfa9`). The trailing region holds the sensor-driver strings
(`ICM4X6XX*` ×40, `INIT_BMI2xy`, `lsm6dsm: spiIsrCallBack err`) — so the post-gap
block is a separate sensor-hub task image appended to the same record.

The multibin's first 16 u32 are **not** a clean section table:

```
rosemary: b8180 387d9 392f9 3937d 3948d 393f5 3881d 0 0 0 0 2e739 3881d 0 2e7e1 2e841
earth:    40d78 1f97d 20941 20a19 20b71 20abd 1f9c1 0 0 0 0 12759 1f9c1 0 12801 12861
```

11 of 16 values are in range, `0x387d9 → 0x392f9 → 0x3937d → 0x3948d` is
monotonic but the sequence then decreases twice, and the record starts with
`80810b00d9870300…` = a length-prefixed blob (`0x0b8180`) — so the table is
*offset-like* but the layout is `[U]`. The census calls it a "section table";
it is not one in any strict sense.

### 5.5 `sspm.img` gets no ISA claim `[F]`

| segment | Thumb-2 windows fully byte-decoded | 256 insns from segment start cover | printable | printable-or-zero |
|---|---:|---:|---:|---:|
| DM | 270 / 278 (data, coincidental) | 512 B | 5.5% | **97.5%** |
| PM | **12 / 250** | 42 B | 20.4% | 28.4% |
| XFILE | 5 / 2,039 | 40 B | 37.2% | 37.5% |

The DM row's high "printable-or-zero" is the whole explanation for its 270/278:
it is a string table padded with zeros, and Thumb-2 decodes arbitrary ASCII as
2-byte halfwords trivially (`7670` = `strb r6,[r6,#1]` at the first byte of
`vproc2`). Its bare printable share is 5.5%, *below* the 37.1% a uniform-random
byte stream produces.

XFILE's 37.2% printable is **exactly** the uniform-random expectation (95 of 256
byte values are printable) — i.e. it carries no text at all, the same fact its
7.9996 bits/byte states, arrived at independently. PM's 20.4% is below random.
So **neither `sspm.img` row has a byte-level ISA**, and the file contains no
`CM4` / `Cortex` / `Thumb` token at all (§8.6).

### 5.6 Upstream is not ISA-uniform `[F]`

This is the single most important scoping fact for the family. Upstream
linux-firmware ships `scp.img` as a **bare ELF32**, and the two SoC generations
use **different instruction sets**:

| upstream file | bytes | ELF32 at 0 | `e_type` | `e_machine` |
|---|---:|---|---:|---:|
| `mediatek/mt8183/scp.img` | 1,030,776 | **yes** | 2 (EXEC) | **40** (`EM_ARM`) |
| `mediatek/mt8186/scp.img` | 419,348 | **yes** | 2 (EXEC) | **40** (`EM_ARM`) |
| `mediatek/mt8192/scp.img` | 309,164 | **yes** | 2 (EXEC) | **243** (`EM_RISCV`) |
| `mediatek/mt8195/scp.img` | 635,532 | **yes** | 2 (EXEC) | **243** (`EM_RISCV`) |

`drivers/remoteproc/mtk_scp.c` (1,651 lines / 44,748 B) loads them as ELF32:

```c
struct elf32_hdr *ehdr;
struct elf32_phdr *phdr;
ehdr = (struct elf32_hdr *)elf_data;
phdr = (struct elf32_phdr *)(elf_data + ehdr->e_phoff);
...
scp_memcpy_aligned(ptr, elf_data + phdr->p_offset, filesz);
```

and builds the path as `mediatek/(soc_model)/scp.img`. So **"the ISA of
`scp.img`" has no single answer even upstream** — mt8183 is ARM32, mt8195 is
RISC-V.

The device files are a **different format entirely**: `\x7fELF` occurs **0
times** in all 12 files, while `0x58881688` occurs 9 or 3 times. So there is no
header-level ISA statement available from the device file, and the Cortex-M4 claim
is inherited from the Thumb-2 decode of the inner `tinysys-scp-CM4_A_dram`
record (§5.2) — nothing more.

`mtk_scp.c` **never names the ISA**, confirmed with word boundaries:
`grep -inE "\bcortex\b|\bthumb\b|\briscv\b|\barm64\b|\bARM\b"` → **0** matches.
A naive `grep -i isa` returns 13 hits, all of them `clk_disable` — a false
positive worth recording so it is not repeated.

The IPI surface the driver publishes is the interface an OS would use, in
`include/linux/remoteproc/mtk_scp.h`: a 17-value enum (`SCP_IPI_INIT`,
`VDEC_H264/VP8/VP9`, `VENC_H264/VP8`, `MDP_INIT/DEINIT/FRAME`, `DIP`,
`ISP_CMD/FRAME`, `FD_CMD`, `CROS_HOST_CMD`, `VDEC_LAT`, `VDEC_CORE`,
`IMGSYS_CMD`) plus `SCP_IPI_NS_SERVICE = 0xFF` and `SCP_IPI_MAX = 0x100`.

---

## 6. Size is not identity `[F]`

### 6.1 Twelve files, six build sources

| build source | file | bytes | records | chain end | md5 |
|---|---|---:|---:|---:|---|
| rosemary on-disk | `scp` | 2,207,744 | 9 | 2,205,261 | `8d87c83dfa506d5923d67d71421c1b40` |
| rosemary `MySelly` | `scp` | 2,327,424 | 9 | 2,327,421 | `d7463b27d5d75889f101b12f656752d1` |
| rosemary `android-tweak` 14.0 | `scp` | 2,330,624 | 9 | 2,327,421 | `4cc6575fff74c87ba589d69c5688679f` |
| earth `matu6968` | `scp` | 627,968 | 9 | 627,965 | `d001ea92a6c1421803caa4499575f4c3` |
| earth `ac973k` | `scp` | 627,968 | 9 | 627,965 | `52961cc19915de3f131d0b92910ddcf8` |
| earth `MinamiQuartet` | `scp` | 627,968 | 9 | 627,965 | `e839cc03f10c2d36e123e9af6cb3f187` |
| rosemary on-disk | `sspm` | 663,552 | 3 | 661,917 | `527ada19b8f1cfb8afa973cc48e7f12c` |
| rosemary `MySelly` | `sspm` | 661,824 | 3 | 661,821 | `70699ed24073ebea63212318465a8bb3` |
| rosemary `android-tweak` 14.0 | `sspm` | 663,552 | 3 | 661,821 | `c02f4dd929e4ec7173404116035bac89` |
| earth `matu6968` | `sspm` | 506,000 | 3 | 505,997 | `0dbd383d8b5ce0d0f0ad8fc8043598e6` |
| earth `ac973k` | `sspm` | 506,000 | 3 | 505,997 | `ce75b63ca88b90a80a63d8c3822f6cf6` |
| earth `MinamiQuartet` | `sspm` | 506,000 | 3 | 505,997 | `47bc2170d005e7bfd16257ed9efe30fd` |

Observed: **4** distinct `scp` sizes across 6 files; **3** distinct `sspm` sizes
across 6 files; and **12 distinct md5 across all 12 files** — every single file is
unique. The three earth mirrors agree on size to the byte and disagree on md5
every time, for both files, at both 627,968 and 506,000.

**No public copy's md5 matches any census md5**, with or without page padding to
the census size. All 12 files were checked; 0 of 4 census md5 reproduced.

### 6.2 Two published sizes, one firmware

`rosemary/MySelly` vs `rosemary/android-tweak` — same device, same chip, two
commits apart in time:

| quantity | `MySelly` | `android-tweak` | equal |
|---|---:|---:|---|
| file size | 2,327,424 | 2,330,624 | no (Δ 3,200) |
| chain end | 2,327,421 | 2,327,421 | **yes** |
| record count | 9 | 9 | yes |
| all 9 record sizes | identical | identical | **yes** |
| records byte-identical | 5 of 9 | — | — |
| **whole-file differing bytes** | — | — | **807** |

The 807 differing bytes decompose exactly:

| record | differing bytes | span | what |
|---|---:|---|---|
| `tinysys-loader-CM4_A` | 0 | — | — |
| `cert1` ×3 | 0 | — | — |
| `tinysys-scp-CM4_A` | **10** | `0x5213c..0x5214f` | the banner date/time: `May 19 2023 03:58:51` → `Nov 22 2023 11:59:04` |
| `tinysys-scp-CM4_A_dram` | **0** | — | — |
| `cert2` #1 | **256** | `0x2bd..0x3bc` | the RSA signature |
| `cert2` #2 | **287** | `0x1f3..0x3bc` | 31 bytes of the PSS salt field + the 256-byte signature |
| `cert2` #3 | **254** | `0x2bd..0x3bc` | 254 of 256 signature bytes |
| total | **807** | | |

Note the shape: the three `cert2` diffs all end at the same offset (`0x3bc`,
the last signature byte) because they are the same field. Two of them are 256
bytes — the full RSA signature — and #3 differs in only 254 because two
signature bytes happen to coincide.

The 3,200-byte file-size difference is **entirely** trailing zeros: 3 bytes after
chain end in `MySelly`, 3,203 in `android-tweak`. Ten bytes of build stamp and
three signatures — that is the whole delta between two "different builds" whose
sizes differ by 3.2 KB. Nothing about the file size tells you that.

The `sspm` pair is the same story with an even cleaner shape: `MySelly` 661,824
and `android-tweak` 663,552, inner payload md5 **identical in both**
(`59bf67a1…`, size 657,606), differing bytes in the common prefix = **256**, all
contiguous, at `0xa183d..0xa193c` — i.e. the `cert2` signature — plus 1,728
trailing zeros in the larger file.

### 6.3 Why `sspm.img` is size-stable across content changes `[F]`

Two rosemary builds, 663,552 B each, md5 `527ada19…` and `c02f4dd9…`. Their inner
images are **657,704** and **657,606** B — 98 B apart — yet both chain ends
(661,917 and 661,821) round up to the **same 4 KiB page**:

```
ALIGN4K(661,917) = 663,552
ALIGN4K(661,821) = 663,552
```

That is the mechanism: the outer container pads to a page boundary, and a
sub-page change in the inner image is invisible to the outer size. So **file size
does not identify a build for `sspm.img`** — content does. This is the same shape
recorded elsewhere in this repo for `fastrpc_shell_0` (841,072 B on two devices
with two md5s, `research/fleet/other-gpu-compute.md`) and for the `wpss`
`bdwlan` family (5,120 rows, 73 devices, 1,895 distinct md5,
`research/fleet/wifi-wpss.md`). Three buckets, one lesson: size is a container
property, not a payload property.

Whether the same size-stability holds across the **four** census rows cannot be
tested — 3 of 4 census payloads were not obtained (§10).

---

## 7. The signature records `[F]`

Every image record in both files is followed by `cert1` (1,709 B) and `cert2`
(957 B), six cert records in `scp.img` and two in `sspm.img` — so each *pair*
of certs belongs to one image, which is why the chain is read in triples. The
prior census notes the DER shape (`30 82 …`) at `rosemary-census.md:205-212`; what is new here
is the internal structure and the invariance.

Both are plain X.509 `Certificate` SEQUENCEs, and both parse cleanly with a
hand-rolled DER TLV walk:

| property | `cert1` | `cert2` |
|---|---|---|
| size | 1,709 B | 957 B |
| outer SEQUENCE | `30 82 06 a9`, content 1,705 | `30 82 03 b9`, content 953 |
| TBS SEQUENCE | `30 82 05 58`, content **1,368** | `30 82 02 68`, content **616** |
| TBS offset | `8..1376` | `8..624` |
| subject | `Some-State1` / `Mediatek0` | same |
| validity | `150604031444Z` → `350604031444Z` (2015-06-04 → 2035-06-04) | same |
| signature algorithm | `sha256WithRSAEncryption` (`1.2.840.113549.1.1.11`) @`0x1a` | same @`0x1a` |
| PSS parameters | `RSASSA-PSS` (`1.2.840.113549.1.1.10`) @`0x562` | same @`0x272` |
| RSA modulus | 2 × 257-byte INTEGER (2,048-bit) | 1 × 257-byte INTEGER |
| signature BIT STRING | `03 82 01 01` content 257 (1 unused-bits byte + 256) | same |

Two structural observations that matter:

- **`cert1`'s TBS is byte-identical across all four builds and all three
  slots** — **1** distinct value out of 12. Only the 256-byte signature varies,
  and the three signature values are **shared across the three rosemary builds**
  and different on earth. So `cert1` is a single embedded vendor certificate
  being re-signed per image; it carries no version information at all.
- **`cert2` is the per-image record**: 9 distinct TBS values across the 12 `scp`
  slots (of 12 possible), and 12 distinct signature values out of 12.

Inside `cert2`'s TBS, at payload offset `0x1f3`, sits a **32-byte value** in a
private-OID TLV (`06 07 60 86 76 93 16 02` = OID `2.16.886.…`, then
`01 03 21 00 <32 B>`), followed by the RSA-PSS salt. Across builds and images
the map is a clean bijection:

| test (`scp`, 4 builds × 3 images) | result |
|---|---|
| distinct image payloads | **9** |
| distinct 32-byte values | **9** |
| payload → value is a function (1 each) | **yes** |
| value → payload is a function (1 each) | **yes** |
| `sspm`: shared payload (`59bf67a1…`) → shared value | **yes** |

So the field is a genuine per-image commitment, and it is the *independent*
confirmation of §6.2's "same firmware" claim: `MySelly` and `android-tweak` carry
the same 32-byte value on every record whose payload matches.

`[N]` It is **not** a hash of the payload that any stdlib function reproduces.
md5, SHA-1, SHA-256, SHA-384, SHA-512, SHA3-256, BLAKE2s and SM3 were all tried
against the payload, the whole record, the byte-reversed digest, and as an
embedded substring of the TBS — zero matches on all three image records. So the
pre-image is either the payload plus unknown context, or a non-standard
construction; that stays `[U]`.

---

## 8. Defects and disagreements in the record `[F]`

### 8.1 `size_bytes` is not a file size `[F]`

All four census sizes are `ALIGN4K(chain_end)`, verified 4 of 4 (§3.3). No
published tree ships these numbers. For earth `scp`, three independent mirrors all
ship 627,968 B while the census says 630,784 — a 2,816-byte gap that is pure page
padding, and the reason no mirror's md5 can equal the census md5.

### 8.2 The on-disk `scp.img` is not the census row `[F]`

| quantity | on-disk `scp.img` | `Redmi_10S` census row | match |
|---|---:|---:|---|
| size | 2,207,744 | 2,330,624 | no — 122,880 B (30 pages) apart |
| md5 | `8d87c83d…` | `981608d9…` | no |
| `tinysys-scp-CM4_A` | 1,824,584 | (build not held) | — |
| `tinysys-scp-CM4_A_dram` | 366,952 | (build not held) | — |

The 122,880-byte file delta decomposes exactly: the `scp` image is 80,940 B
larger and the `dram` image 41,220 B larger in the census-era build (122,160 B of
payload), plus 720 B of extra page slack (2,483 → 3,203). So this is **a
different firmware build of the same chip**, not a different chip.

**All structural claims in §2–§7 are measured on builds we hold** — the on-disk
pair, three rosemary public builds, three earth mirrors. Whether the exact census
build has the same 9-header chain is `[U]`; it almost certainly does, because
`MySelly` and `android-tweak` are also 9-header chains at the same chain end
across a 81 KB range of `scp` record sizes.

### 8.3 The prior-art doc and the census CSV disagree `[F]`

`research/mediatek/rosemary-census.md:127` states `scp` (2,207,744), `sspm`
(663,552). The census CSV states `scp` 2,330,624, `sspm` 663,552. So `scp`
disagrees by 122,880 B and `sspm` agrees. Two internal sources describe
**different builds of the same device** — one is the on-disk file, the other the
page-rounded census figure.

This is not a bug to fix in either artefact — both are internally consistent —
but it must be stated, because a reader who compares the two will otherwise
conclude one is wrong.

### 8.4 `db_type = UNKNOWN` is a corpus-wide vocabulary gap `[F]`

All four rows are `UNKNOWN`, and so are `lk.img`, `gz.img`, `tee.img`,
`spmfw.img`, `md1img.img` and `preloader_raw.img` on both devices — every MTK
firmware in the set. `db_type` has **42** distinct values and **none** of them
names a container: no `MTK`, `MTK_HDR`, `GFH`, `HDR` or `CONTAINER` string
exists. `UNKNOWN` covers 12,756 rows, 544 of them `.img`, out of 2,914 total
`.img` rows.

### 8.5 `isa_identified` is blank on both `Poco_12C` rows `[F]`

The earth `scp.img` has the same 9-record chain, the same 1,080 B loader with
`SP=0x538` / `reset=0x1e1` / 78 handlers, and a `dram` record that decodes **41
of 58** windows fully as Thumb-2. The evidence that fills the `Redmi_10S` field
is present verbatim in the `Poco_12C` file. The blank is under-population, not
absence of evidence — and `db_type=UNKNOWN` on the same row suggests the label
was never attempted.

### 8.6 The `Redmi_10S` `sspm.img` ISA claim cites a token that is not in the file `[F]`

The field reads `ARM Cortex-M4 per tinysys family record names (tinysys-*-CM4_A)`.
`sspm.img` contains no such name and no such token:

| file | record names | `CM4` | `CM4_A` | `Cortex` |
|---|---|---:|---:|---:|
| `scp.img` | `tinysys-loader-CM4_A`, `cert1`, `cert2`, `tinysys-scp-CM4_A`, … | 52 | 11 | 0 |
| `sspm.img` | `tinysys-sspm`, `cert1`, `cert2` | **0** | **0** | **0** |

So the claim is a **family inheritance** that cannot be sourced to `sspm.img`
itself, and the evidence string it names belongs to `scp.img`. (The 7 `M4` byte
pairs in `sspm.img` are 2-byte subsequences inside the XFILE segment's random
bytes — e.g. at `0x455ec` in the middle of `…81 4d 34 b3 dd…` — not tokens.)

### 8.7 The census mis-states three measurements `[F]`

| claim | source | measured |
|---|---|---|
| `tinysys-loader-CM4_A`: "6× handler 0x26d" | `rosemary-census.md:145` | **78** consecutive entries, `0x08..0x13c` |
| `tinysys-scp-CM4_A_dram`: FreeRTOS / `ARM_CM4F/port.c` / `tasks.c` strings | `rosemary-census.md:147` | **0** in `dram`; **7** in the multibin |
| `tinysys-sspm`: "body entropy 7.95+ from 0x20000" | `rosemary-census.md:148` | cumulative-from-`0x20000` = 7.9995; 4 KiB window at `0x20000` = 6.786; boundary at `0x2114c` |
| `tinysys-scp-CM4_A`: header u32 table is a "section table" | `rosemary-census.md:146` | 11 of 16 in range, not monotonic; layout `[U]` |

In every case the *conclusion* survives and the *measurement* needs tightening.
That is the pattern for prior art in a first-pass census, and it is worth saying
plainly so the next analyst does not inherit the numbers.

### 8.8 `soc` blank and `interface_documented = n` `[F]`

`soc` is blank on all four rows, though `Poco_12C` is MT6768-class and
`Redmi_10S` is MT6785 — both documented elsewhere in this repo
(`docs/devices/xiaomi/Poco_12C/boot.md` §1 covers the pair).

`interface_documented = n` is defensible as "no interface is documented **in the
database**", but it is not true of the device. LineageOS
`android_device_xiaomi_rosemary/rootdir/etc/init.mt6785.rc` (1,231 lines,
`lineage-22.2`) has 14 `scp`/`sspm` lines and names the whole surface:

```
/dev/scp                                  /dev/sspm
/sys/class/misc/scp/scp_mobile_log        /sys/class/misc/sspm/sspm_mobile_log
/sys/class/misc/scp/scp_log_flush         /dev/audio_scp
/sys/class/misc/scp/scp_ee_force_ke
```

So the artifacts **do** have a runtime interface — a misc device plus per-role
sysfs log nodes — and `n` records a DB gap rather than a device fact. The same
directory ships `/dev/audio_scp`, which is the SCP↔audio-DSP path.

---

## 9. What this adds to the existing record `[F]`

1. **The container law.** `next = ALIGN16(off + 512 + size)`, 60 of 60 links
   across 12 files, with `+0x34 = 512` identified as the load-bearing field. The
   prior census had the empirical model at `rosemary-census.md:202-212` (and
   credits zrax / wairz); this note supplies the arithmetic, the pad set, and the
   515/520 trap.
2. **The group structure.** `scp.img` is 3 `image + cert1 + cert2` groups, and
   the census's four record names/sizes fall out of it. That is the delta over
   `rosemary-census.md:145-148`, which lists them as a flat set of partitions.
3. **The second container.** `sspm`'s payload is a 3-segment `ptimg_hdr_t` chain
   under `PT_MAGIC 0x58901690`, with the LK loader's own walk order. The prior
   census recorded the magic and the first segment's three fields; this note
   walks all three segments and maps them to `PT_ID_SSPM_DM/PM/XFILE`.
4. **The entropy scope.** One segment, 79.4% of the image, is incompressible;
   the other 20.6% is plaintext or table. Boundary `0x2114c`, not `0x20000`.
5. **The size-arithmetic result.** Census `size_bytes` = `ALIGN4K(chain_end)`,
   4 of 4. Two published `scp.img` sizes are one firmware, differing in 807
   bytes. `sspm.img` is size-stable because 98 B of inner change cannot move a
   page boundary.
6. **The build-provenance marker.** `0x55aaaa55` + codename at multibin `0x140`,
   once per `scp.img`, zero per `sspm.img`.
7. **The signature structure.** `cert1` = one embedded 2,048-bit certificate
   with an invariant TBS and a per-image signature; `cert2` = a per-image record
   with a 32-byte private-OID commitment that is a verified bijection with the
   payload.
8. **The upstream non-uniformity.** `scp.img` is ELF32 upstream with `e_machine`
   40 on mt8183/8186 and **243 (RISC-V)** on mt8192/8195, so the family has no
   single ISA. The device files have no ELF at all.

---

## 10. Honest negatives `[N]`

- **No census payload was reproduced.** 0 of 4 census md5 matched any public
  copy, including after padding the shorter files to the census size with `0x00`
  and with `0xff`. All 12 fetched files were checked against all four census md5
  values. The census build's signature bytes are simply not in any tree we could
  reach. Consequently the census rows' *structure* is inferred from builds that
  share their record layout and their `ALIGN4K` size, not from the rows
  themselves.

- **No documentation of the magics.** `mtk_hdr 0x58881688` → searxng **"No
  results found"**; `"0x58901690" MediaTek sspm` → **"No results found"**. The
  primary magic appears in 1,422 GitHub code hits and the sspm magic in 235, but
  the only real sources are `Gigaset-dev/lk2`'s `sspm_loader.c` / `sspm_plat.h`,
  Motorola's `kernel-mtk` apusys_rv, and coreboot's mt8196 `gpueb_priv.h` (the
  same magic family in a GPU execute-buffer context). No format specification, no
  vendor document, no write-up.

- **The `PT_ID_SSPM_*` numeric values were not read from a header.** `sspm_plat.h`
  was not fetched; only the four enum names appear in `sspm_loader.c`. The
  id→name mapping is `[I]` from walk order and segment contents.

- **`sspm`'s PM segment is undecoded.** Not ARM, ARM64, MIPS or RISC-V, in
  identity, byte-swap-16, byte-swap-32 or XOR-0xff forms; 0 `push` prologues;
  12 of 250 windows at best. **No ISA claim is made for it**, and none should be
  inherited from the family name.

- **`sspm`'s XFILE segment is undecoded.** 7.9996 bits/byte, 0 repeated 16-byte
  blocks in 32,634, no printable run ≥16. Not ECB, not a table, not compressed
  (zlib -9 expands it). The encoding is `[U]`, and no decrypt-first tooling was
  attempted.

- **The 32-byte `cert2` commitment is un-reproduced.** It is a verified bijection
  with the payload and differs whenever the payload differs — but it matches none
  of md5, SHA-1, SHA-256, SHA-384, SHA-512, SHA3-256, BLAKE2s or SM3 over the
  payload, the record, or the reversed forms. The pre-image is unknown.

- **The multibin's header table is not a section table.** 11 of 16 u32 in range,
  monotonic for 4 entries then decreasing twice; the record begins with a
  length-prefixed blob (`0x0b8180`). The layout is `[U]`.

- **The 1,392,371-byte zero gap in the multibin is unexplained.** It is 76.3% of
  the record on rosemary and 60.7% on earth, with live content on both sides
  (388,085 B before, 44,128 B after). Why a declared image size covers a mostly-
  zero span is `[U]`; the trailing block is a sensor-driver task image (§5.4),
  which is consistent with a multi-task-link layout but does not prove one.

- **`0x58891689` is not called a container.** It is once per header at `+0x30`
  with `{0x200, 1, 0x10}` following, which is suggestive of a parameter block
  inside the 512-byte header. Evidence is circumstantial; recorded `[I]`.

- **`db_type` has no container vocabulary.** 42 distinct values, none MTK/HDR/
  GFH/CONTAINER. So `UNKNOWN` on these rows is a schema gap, not a finding.

- **No `sspm` and no `tinysys` in linux-firmware.** `WHENCE` (11,954 lines,
  542,288 B, 271 `Driver:` stanzas): `scp.img` appears **7** times under
  `Driver: mtk_scp` (line 6565) for mt8183/8186/8192/8195/8188/8189; `sspm` →
  **0** hits; `tinysys` → **0** hits. So `sspm.img` is device-only, and no
  upstream driver parses it.

- **`mtk_scp.c` never names the ISA**, and the naive `grep -i isa` that suggests
  otherwise is 13 × `disable`.

- **Two prior-art measurements needed tightening** (§8.7): the handler count
  (6 → 78) and the FreeRTOS-string record (`dram` → multibin). Both conclusions
  survive.

- **No `docs/devices/xiaomi/Redmi_10S/` directory exists**, so the rosemary side
  of this device pair has no per-device doc in this repo to cite beyond the
  census and `Poco_12C/boot.md` §1's comparison table.

---

## 11. Gate 0 — prior art search `[N]`

All queries run **2026-11-26**.

**GitHub code search** (REST `/search/code`, authenticated):

| query | hits | result |
|---|---:|---|
| `tinysys` | 33,792 | overwhelmingly AOSP `system/chre` `platform/tinysys` and device trees |
| `filename:scp.img` | 31 | vendor trees and dumps; no analysis |
| `filename:sspm.img` | 23 | `TheMuppets/proprietary_vendor_xiaomi_{rosemary,earth,merlinx,lancelot}`, `rousseauuv/Dump`, … |
| `0x58901690` | 235 | `Gigaset-dev/lk2` `sspm_plat.h`/`sspm_loader.c`; `MotorolaMobilityLLC/kernel-mtk` apusys_rv; coreboot mt8196 `gpueb_priv.h` |
| `0x58881688` | 1,422 | MTK trees + dump manifests; no format spec |
| `tinysys-sspm` | 106 | device trees and dumps |
| `sspm_loader` | 1 | `Gigaset-dev/lk2` |
| `PT_MAGIC` | 49,728 | generic token; `PT_MAGIC sspm` → 52, all `Gigaset-dev/lk2` |
| `filename:scp.img tinysys` | **0** | no file co-indexed with the term |
| `tinysys-sspm sspm_loader` | **0** | — |

**Web** (searxng, aggregating Google/Bing/Brave/DDG):

| query | result |
|---|---|
| `MediaTek SCP tinysys firmware` | Patchew "[PATCH v1 0/2] firmware: Add MediaTek TinySYS SCMI Protocol" — Dimensity 9200/9300/9400 and MT8196, "used to communicate with the CM_MGR and other MCUs for power management" |
| `sspm.img MediaTek what is it` | lopestom gist; MediaTek Genio docs; an XDA fastboot thread — nothing on the container |
| `mtk_hdr 0x58881688` | **"No results found"** |
| `MediaTek SCP Cortex-M4 FreeRTOS` | lopestom gist only |
| `"0x58901690" MediaTek sspm` | **"No results found"** |
| `MediaTek tinysys RISC-V scp mt8195` | LWN 896815 / patchwork: "The MT8195 SCP is a dual-core RISC-V MCU" — corroborates §5.6 |

The one substantive web source is the lopestom gist
(`gist.github.com/lopestom/ce250f5de64a2764ee85092a2c01939e`, "Android Firmware
File Partition Description"). It says:

- `scp.img` — "Sensor Hub main firmware (tinysys, FreeRTOS) runs on Cortex M4"
- `sspm.img` — "Sensor Hub firmware Power management (tinysys), partially
  encrypted"
- `spmfw.img` — "SoC Power Management suspend state firmware"
- "mtk does not even have an elf bootloader in LK, and the sections are divided
  into code/data, this is especially visible on tinysys sections"

Every one of those is consistent with what §3–§5 measures: M4 + FreeRTOS in
`scp`, **partially** encrypted `sspm` (DM plaintext / PM encoded / XFILE
incompressible — exactly "partially"), no ELF, code/data split. It is a
description, not a specification: it gives no magic, no offsets, no chain law.

**Decision**: prior art exists for the *purpose* of both files and for the LK
`ptimg` grammar, but **none for the container layout of the device files**. The
issue stays open and this DELTA is delivered rather than closed as duplicate.

---

## 12. Open items `[U]`

1. **Obtain the exact census payloads.** 0 of 4 md5 reproduced. Routes tried:
   `raw.githubusercontent.com` on 6 vendor trees, GitHub LFS API (`403 Resource
   not accessible by personal access token`), `media.githubusercontent.com`
   (0 bytes for LFS pointers; some earth forks serve 131-byte LFS pointer files).
   A `git lfs` clone of `TheMuppets/proprietary_vendor_xiaomi_rosemary` at a
   matching revision is the obvious next step.
2. **Decode the XFILE segment.** 522,144 B at 7.9996 bits/byte with no block
   structure. Needs the SSPM's own loader/decryptor, or a known-plaintext pair.
3. **Decode the PM segment.** 64,084 B of 6.95-bit/byte `0x001e`-tagged records.
   A register-table schema from an MTK clock/power driver would crack it.
4. **Identify the `cert2` 32-byte commitment.** A bijection with the payload but
   not any stdlib hash. Likely a hash over a decorated pre-image.
5. **Decode the multibin header table** (§5.4) and the 76.3% zero gap.
6. **Fetch `sspm_plat.h`** to convert the `PT_ID_SSPM_*` mapping from `[I]` to
   `[F]`, and to check whether any SoC defines a `CPM` (id 3) segment. Neither
   build has one.
7. **Establish whether the census `scp.img` build has the same 9-record chain.**
   Its `ALIGN4K` size matches our chains, but the inner record sizes are a
   different generation (80,940 B larger `scp`, 41,220 B larger `dram`).
8. **Resolve the `db_type` vocabulary gap** with the `blob-database` owner — MTK
   firmware containers currently have no value to be filed under.
9. **Populate `isa_identified` on the two `Poco_12C` rows**; §8.5 shows the
   evidence is present in the file.

---

## 13. Method `[F]`

All commands `python3 -I`, stdlib only, except capstone 5.0.7 which lives outside
the isolated path (`ModuleNotFoundError` under `-I`) and was loaded via
`sys.path.insert(0, '/home/aditya/.local/lib/python3.12/site-packages')` inside
the heredoc. No payload is committed; the twelve binaries were fetched to a
scratch directory outside the repo and only hashes, sizes, offsets, counts and
≤16-byte hex samples appear above.

```python
import struct, csv, hashlib, math, collections

# census
rows = list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
t = [r for r in rows if r['blob_subfamily'] == 'tinysys']
len(t)                                                  # -> 4
len({r['device'] for r in t})                           # -> 2
sum(int(r['size_bytes']) for r in t)                    # -> 4132864
sorted({int(r['size_bytes']) for r in t})               # -> 4 sizes, all % 4096 == 0

# the chain law
def walk(d):
    L = len(d); o = 0; out = []
    while o + 0x200 <= L and struct.unpack_from('<I', d, o)[0] == 0x58881688:
        size = struct.unpack_from('<I', d, o + 4)[0]
        poff = struct.unpack_from('<I', d, o + 0x34)[0]      # 512 on every header
        out.append((o, d[o + 8:o + 0x28].split(b'\0')[0].decode(), size, poff))
        o = (o + poff + size + 0xF) & ~0xF
    return out

w = walk(open('scp.img', 'rb').read())                  # -> 9 records
all(poff == 512 for _, _, _, poff in w)                 # -> True
last = w[-1][0] + 512 + w[-1][2]                        # -> 2205261

# the two published conventions
((last + 0xF) & ~0xF, (last + 0xFFF) & ~0xFFF)          # -> (2205264, 2207744)

# the inner sspm chain
d = open('sspm.img', 'rb').read(); body = d[0x200:0x200 + 657704]
M = struct.pack('<I', 0x58901690); loc = []; i = 0
while (j := d.find(M, i)) >= 0:
    loc.append(j); i = j + 1
loc                                                     # -> [0x200, 0x118c8, 0x21334]
[struct.unpack_from('<6I', d, o) for o in loc]          # -> (magic, 24, 71344|64084|522144, 4, 0|1|99, 0)
d.count(M), d.count(b'\x7fELF')                         # -> 3, 0

# segment entropy
H = lambda x: -sum((v / len(x)) * math.log2(v / len(x)) for v in collections.Counter(x).values())
H(body[0x18:0x18 + 71344])                              # -> 0.9434   DM  (plaintext table)
H(body[0x116e0:0x116e0 + 64084])                        # -> 6.9475   PM  (encoded)
H(body[0x2114c:0x2114c + 522144])                       # -> 7.9996   XFILE (incompressible)

# the entropy boundary
next(o for o in range(0, len(body) - 4096, 256) if H(body[o:o + 4096]) >= 7.90)   # -> 0x20e00
max(H(body[o:o + 256]) for o in range(0, len(body) - 256, 256))                   # -> 7.3299 (stride 256)
max(H(body[o:o + 256]) for o in range(0, len(body) - 256))                         # -> 7.4169 (stride 1, exhaustive)

# ISA: only a 2/4-byte variable-length encoding can fit >64 insns in 256 B
def hits(bl, arch=capstone.CS_ARCH_ARM, mode=capstone.CS_MODE_THUMB):
    md = capstone.Cs(arch, mode); md.skipdata = False
    n = h = 0
    for o in range(0, len(bl) - 256, 256):
        ins = list(md.disasm(bl[o:o + 256], o)); n += 1
        h += (sum(len(i.bytes) for i in ins) == 256 and len(ins) >= 70)
    return h, n

hits(dram)                                              # -> (695, 1433) rosemary / (41, 58) earth
hits(dram, capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)  # -> (0, 1433)  arm32
hits(dram, capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)  # -> (0, 1433)
hits(dram, capstone.CS_ARCH_MIPS, capstone.CS_MODE_MIPS32)  # -> (0, 1433)
hits(dram, capstone.CS_ARCH_RISCV, capstone.CS_MODE_RISCV32)  # -> (0, 1433)

# the two sizes that are one firmware
sum(a[i] != b[i] for i in range(len(a)))                # -> 807 across 2,327,424
[sum(x != y for x, y in zip(p, q)) for p, q in zip(walk(A), walk(B))]  # -> [0,0,256,10,0,287,0,0,254]

# the DER walk behind §7
def tlv(b, o):
    tag = b[o]; ln = b[o + 1]; h = 2
    if ln & 0x80:
        n = ln & 0x7f; ln = int.from_bytes(b[o + 2:o + 2 + n], 'big'); h = 2 + n
    return tag, ln, o + h, o + h + ln

tlv(cert1, 0)                                           # -> (0x30, 1705, 4, 1709)
tlv(cert1, 4)                                           # -> (0x30, 1368, 8, 1376)   TBS
tlv(cert2, 0)                                           # -> (0x30,  953, 4,  957)
tlv(cert2, 4)                                           # -> (0x30,  616, 8,  624)   TBS
```

Upstream and prior art were read, not re-derived: `mtk_scp.c` (1,651 lines),
`mtk_scp.h` (69 lines), `sspm_loader.c` (382 lines), `WHENCE` (11,954 lines,
271 stanzas), four linux-firmware `scp.img` builds, the lopestom gist,
`init.mt6785.rc` (1,231 lines), and `research/mediatek/rosemary-census.md` lines
145–148 with §"Container formats" 202–221.
