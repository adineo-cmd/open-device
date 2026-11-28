# `boot` — four container grammars under one label, and 73 rows filed under the wrong one

Analysis date: 2026-11-28 (census and Gate 0 re-verified today; first pass
2026-11-26). Analyst: OC-1 (`100milionseek`), issue
[#829](https://github.com/adineo-cmd/open-device/issues/829).

Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data
rows) for the census; the normative public specs — AOSP
`platform/system/tools/mkbootimg` `include/bootimg/bootimg.h` (433 lines) and
`platform/external/avb` `avbtool.py` (207,502 B), both fetched 2026-11-26; the
repo's own `research/qualcomm/docs/bootchain-census.md` (237 lines) and
`research/fleet/boot-dtb.md` (751 lines); and three real payloads held in scratch
space for byte-level verification (an 11,744,486 B `ANDROID!` v0 image, an
8,388,608 B `dtbo.img` carrying AVB, and a 127,904 B `dtb.img` without it).

Every number below is command output. No payload is committed; samples are ≤16
bytes of hex.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** The `boot` family is **1,038 rows / 23,864,283,348 B** — **34.19 %
of all corpus bytes**, which makes it the second-largest family by size, while
being only **3.06 % of rows**. That asymmetry is the whole story: the family is
enormous because `boot.img` partitions are padded to exact powers of two, not
because there is a lot of distinct firmware.

Under the one label sit **four unrelated container grammars**, plus a fifth
bucket of things that are neither:

| grammar | magic | rows | bytes | share of family bytes | basis |
|---|---|---:|---:|---:|---|
| Android boot image v0–v4 | `ANDROID!` | 258 | 20,877,809,664 | **87.49 %** | FP6 census + one real payload |
| `dt_table` | `0xd7b7ab1e` (BE) | 125 | 2,470,445,056 | 10.35 % | two real payloads |
| ELF32/ELF64, incl. multi-ELF | `\x7fELF` | 437 | 384,356,352 | 1.61 % | FP6 census |
| AVB (`vbmeta`) | `AVB0` | 115 | 946,176 | **0.004 %** | one real payload |
| **unverified remainder** (see §6) | — | 103 | 130,726,100 | 0.55 % | filename only |

The rows are grouped by **what has been byte-verified**, not by filename, and the
two differ. `pvmfw.img` is a boot image v3, so it belongs in the first row and
not in the remainder. `aop.img`/`cpucp.img` are ELF, so they belong in the
third. `tzsw`, `rpm`, `bl1`, `bl31`, `lk`, `preloader_raw`, `xbl_cfg.elf` and
`unsparse_super_empty` have **no** in-repo byte-level evidence for their
container, so they are the remainder rather than being assigned a grammar on the
strength of their name. The five groups sum to 1,038 rows and 26 basenames.

Two findings carry the note, and both are defects in the corpus rather than
discoveries about firmware.

First, **73 rows are tagged `db_type=BOOT` but are not Android boot images at
all.** They are `tzsw.img` (16, 113,909,760 B), `bl31.img` (16, 1,667,072 B),
`bl1.img` (16, 249,856 B) and `unsparse_super_empty.img` (25, 116,572 B).
`tzsw` alone is **98.25 %** of the 73 rows' 115,943,260 B, so this defect is
almost entirely a `tzsw` story.

The `unsparse_super_empty.img` case is `[F]` on size alone: all 25 rows are
4,592–4,772 B, and 4,772 < 8,192, so none can hold a 4 KiB boot page plus a
kernel. What it *is* (a sparse-image stub) is inferred from the name `[I]`.

The `bl1`/`bl31`/`tzsw` case is weaker evidence than it looks. All three exist
on **exactly the same 16 devices, all Google Tensor** (Pixel 6 through Pixel 9
Pro XL, Fold, Tablet), and the in-repo `docs/devices/google/Pixel_7_Pro/boot.md`
classifies them `[I]` — "an Arm trusted-boot grammar" — not `[F]`. This note
**does not** byte-verify them, so their identity as ATF BL1/BL31 and a TrustZone
image is prior-art inference, not a result here `[I]`.

A size argument does **not** settle it, and it is worth saying so because it is
tempting: all three are exact 4 KiB multiples (`bl1` 12,288/16,384/20,480;
`bl31` 90,112–114,688; `tzsw` 5,857,280–7,864,320), so the "not page-aligned"
test that works on `unsparse_super_empty` gives nothing here `[F]`. What is
`[F]` is narrower: `bl1` and `bl31` are **two to three orders of magnitude
below the smallest genuine boot image in the corpus** (8,388,608 B, the
`init_boot.img` size on all 29 rows), and `tzsw` is also below it. That is
consistent with them not being boot images; it is not proof `[F]`/`[I]`.

Meanwhile the 240 rows that *are* Android boot images are all tagged `BOOT`, so
the error is one-directional: 73 false positives, 0 false negatives `[F]`.

Second, **the `boot.img` sizes are partition sizes, not image sizes, on 94.40 %
of rows.** 118 of 125 `boot.img` rows are exact MiB multiples — 96 MiB appears
53 times, 64 MiB 25 times, 192 MiB 21 times. A real boot image ends where its
last section ends; a number that is exactly 192.00 MiB is a partition table
entry. The 7 rows that are *not* MiB-aligned (all Sony Xperia and Xiaomi
`Redmi_4A`/`Poco_3S`) are the ones that recorded a real image length.

A third, smaller finding: **`dt_table`'s header field order is not what a naive
`>7I` read produces.** The eight big-endian u32 are `magic, total_size,
header_size, entry_size, entry_count, entries_offset, page_size, version` — and
reading `>7I` from offset 4 silently swaps `entry_size` (32) with `entry_count`,
so a 5-entry table reports `entry_size=5`. That is not hypothetical: it is what
this note's own first parse did before the field order was checked against
payload.

---

## 0. Headline numbers

| quantity | value |
|---|---:|
| rows | **1,038** |
| bytes | **23,864,283,348** |
| share of corpus rows | 3.0604 % |
| share of corpus bytes | **34.1907 %** |
| rank among 9 families, by bytes | **#2** |
| rank among 9 families, by rows | #6 |
| devices | 123 |
| distinct basenames | 26 |
| distinct md5 | 947 |
| distinct sizes | 156 |
| duplicate-md5 groups | 79 (170 rows) |
| largest single row | `Nord_CE4` `boot.img`, 201,326,592 B = exactly 192 MiB |
| rows tagged `db_type=BOOT` | 313 |
| …of which are real Android boot images | 240 |
| …of which are **not** | **73** |
| `boot.img` rows that are exact MiB multiples | **118 of 125 (94.40 %)** |

Corpus: 33,917 rows / 69,797,539,502 B.

---

## 1. The 26 basenames and what each actually is `[F]`

| basename | rows | devices | bytes | `db_type` | real grammar |
|---|---:|---:|---:|---|---|
| `boot.img` | 125 | 123 | 13,075,777,536 | `BOOT` | Android boot image v0–v4 |
| `dtbo.img` | 118 | 116 | 2,411,724,800 | `DTB` | `dt_table` |
| `vbmeta.img` | 115 | 113 | 946,176 | `AVB` | AVB `AVB0` |
| `recovery.img` | 86 | 65 | 7,540,133,888 | `BOOT` | Android boot image v0–v4 |
| `abl.img` | 79 | 79 | 60,735,488 | `UEFIBOOT` | ELF32 (Qualcomm LK-derived) |
| `xbl.img` | 63 | 63 | 206,077,952 | `UEFIBOOT` | **multi-ELF** (`xbl_s.melf`) |
| `qupfw.img` | 63 | 63 | 4,141,056 | `ELF64` | ELF32 `EM_QDSP6` |
| `xbl_config.img` | 63 | 63 | 11,091,968 | `ELF64` | ELF64 (junk machine, F-7) |
| `aop.img` | 40 | 40 | 11,132,928 | `UNKNOWN` | ELF32 RV32 |
| `cpucp.img` | 30 | 30 | 9,023,488 | `UNKNOWN` | ELF32 RV32 |
| `shrm.img` | 30 | 30 | 2,539,520 | `ELF64` | ELF32 RV32 |
| `init_boot.img` | 29 | 29 | 243,269,632 | `BOOT` | Android boot image v4 |
| `unsparse_super_empty.img` | 25 | 23 | 116,572 | **`BOOT`** | **sparse stub, not a boot image** |
| `rpm.img` | 24 | 24 | 10,567,680 | `ELF64` | **unverified** — not in the FP6 census |
| `aop_config.img` | 21 | 21 | 413,696 | `ELF64` | ELF32 |
| `uefi.img` | 21 | 21 | 60,907,520 | `ELF64` | ELF64 + EFI FV inside |
| `xbl_ramdump.img` | 21 | 21 | 18,198,528 | `ELF64` | ELF64 AArch64 |
| `pvmfw.img` | 18 | 18 | 18,628,608 | `SECURITY` | boot image v3, raw AArch64 payload |
| `bl1.img` | 16 | 16 | 249,856 | **`BOOT`** | not a boot image; ATF BL1 `[I]` |
| `bl31.img` | 16 | 16 | 1,667,072 | **`BOOT`** | not a boot image; ATF BL31 `[I]` |
| `tzsw.img` | 16 | 16 | 113,909,760 | **`BOOT`** | not a boot image; TZ software `[I]` |
| `dtb.img` | 7 | 7 | 58,720,256 | `DTB` | `dt_table` (not a bare FDT) |
| `cpucp_dtb.img` | 6 | 6 | 94,208 | `ELF64` | ELF64 wrapper + FDT |
| `xbl_cfg.elf` | 2 | 2 | 131,448 | `ELF64` | unverified (name only) |
| `lk.img` | 2 | 2 | 3,424,256 | `UNKNOWN` | unverified (name only) |
| `preloader_raw.img` | 2 | 2 | 659,456 | `UNKNOWN` | unverified (name only) |

**26 basenames, 5 grammars.** The `db_type` column names 7 distinct values
(`BOOT`, `DTB`, `AVB`, `UEFIBOOT`, `ELF64`, `SECURITY`, `UNKNOWN`) but only
`DTB` and `AVB` are consistently correct.

---

## 2. Grammar A — Android boot image v0–v4 `[F]`

Normative: AOSP `bootimg.h`, fetched 2026-11-26. Header sizes, field by field:

| version | header size | page size source | extra fields |
|---|---:|---|---|
| v0 | **1,632** | header field at offset 36 | — |
| v1 | 1,648 | header field | `recovery_dtbo_size`, `recovery_dtbo_offset`, `header_size` |
| v2 | 1,660 | header field | + `dtb_size`, `dtb_addr` |
| v3 | **1,580** | fixed 4,096 | `kernel_size`, `ramdisk_size`, `os_version`, `reserved[4]`, `cmdline[1536]` |
| v4 | **1,584** | fixed 4,096 | + `signature_size` |

`1,632 = 8 + 4×10 + 16 + 512 + 32 + 1,024` and `1,580 = 8 + 4×4 + 16 + 4 + 1,536`,
both confirmed by `struct.calcsize` on the documented layouts `[F]`.

### 2.1 The page arithmetic is the whole format `[F]`

```
offset = page_size                      # header occupies exactly one page
kernel  at offset;  offset += round_up(kernel_size,  page_size)
ramdisk at offset;  offset += round_up(ramdisk_size, page_size)
second  at offset;  offset += round_up(second_size,  page_size)   # v0-v2 only
recovery_dtbo at offset; ...                                       # v1+ only
dtb     at offset;  ...                                            # v2 only
boot_signature at offset; offset += signature_size                 # v4 only
```

Verified on a real 11,744,486 B image (Nexus 5X "bullhead", header v0) `[F]`:

| field | value |
|---|---|
| `kernel_size` | 10,456,559 |
| `ramdisk_size` | 1,280,946 |
| `second_size` | 0 |
| `page_size` | 4,096 |
| `header_version` | 0 |
| `name` | `""` |
| `cmdline` | `console=ttyHSL0,115200,n8 androidboot.hardware=bullhead boot_cpus=0-5 …` |

Page arithmetic: header 1 page (4,096) + ⌈10,456,559/4,096⌉ = **2,553 pages**
(10,457,088) + ⌈1,280,946/4,096⌉ = **313 pages** (1,282,048) = **11,743,232**.

### 2.2 A real tail case the format does not describe `[F]`

The file is **11,744,486 B**, which is **1,254 B past** the computed end. Those
bytes are not padding and not AVB:

```
offset 11,743,232: 30 82 04 e2 …
```

`0x30 0x82` is a DER `SEQUENCE` with a two-byte length, `0x04e2 = 1,250`, and
`4 + 1,250 = 1,254` — the tail is exactly one DER-encoded certificate. There is
no `AVB0` and no `AVBf` anywhere in the file (`count == 0` for both) `[F]`.

So a boot image may carry a **trailing DER certificate** that no AOSP header
field accounts for. A parser that trusts the arithmetic will report 1,254
unexplained bytes; the honest answer is to classify them, which the parser in
`implementations/boot/` does (`trailing.kind == "der_sequence"`).

### 2.3 The 94.40 % partition-size defect `[F]`

| size | count | as MiB |
|---:|---:|---:|
| 100,663,296 | 53 | 96.00 |
| 67,108,864 | 25 | 64.00 |
| 201,326,592 | 21 | 192.00 |
| 57,671,680 | 7 | 55.00 |
| 167,772,160 | 4 | 160.00 |
| 61,865,984 | 3 | 59.00 |

16 distinct sizes for 125 rows, **118 of them exact MiB multiples**. The 7 that
are not are all Sony Xperia (`Xperia_XA2` 35,913,728; `Xperia_XA2_Plus`
35,905,536; `Xperia_XA2_Ultra` 35,917,824; `Xperia_10` 35,610,624;
`Xperia_10_Plus` 35,954,688) plus `Redmi_4A` (21,241,856) and `Poco_3S`
(21,788,672) `[F]`.

A boot image's length is determined by its contents, and none of these lengths
is content-derived: 201,326,592 B is exactly 192 MiB, which is what `fastboot
flash boot` pads to and what a partition table records `[I]`. So the most likely
reading is that for 118 rows the corpus recorded the **partition capacity**, and
for the 7 non-aligned rows it recorded the image `[I]`. Any byte-total statistic
over this family is therefore dominated by padding, which is why the family is
34.19 % of corpus bytes while being only 3.06 % of rows `[F]`.

This is `[I]`, not `[F]`: the matrix records one `size_bytes` per row and carries
no column that distinguishes an image length from a partition length, so the
mechanism cannot be confirmed from the corpus alone. What is `[F]` is the
quantization itself.

---

## 3. Grammar B — `dt_table` `[F]`

Normative: AOSP `mkdtimg`; in-repo `research/fleet/boot-dtb.md` already covers
the padding and AVB layers, so this section adds only the field order and the
verification.

### 3.1 The header, and the read that gets it wrong `[F]`

Eight big-endian u32, **not** the seven a `>7I` read from offset 4 yields:

| word | field | `a21s_dtbo.img` | `a21s_twrp_dtb.img` |
|---:|---|---:|---:|
| 0 | `magic` | `0xd7b7ab1e` | `0xd7b7ab1e` |
| 1 | `total_size` | 747,696 | 127,904 |
| 2 | `header_size` | 32 | 32 |
| 3 | `entry_size` | **32** | **32** |
| 4 | `entry_count` | **5** | **1** |
| 5 | `entries_offset` | 32 | 32 |
| 6 | `page_size` | 2,048 | 2,048 |
| 7 | `version` | 0 | 0 |

A `>7I` read starting at offset 4 returns `(747696, 32, 32, 5, 32, 2048, 0)` —
so `entry_size` appears to be **5**, which is the entry count. This note's own
first parse made exactly that error and produced garbage entries until the field
order was checked against the payload `[F]`.

### 3.2 Entry layout, and FDT magic as the check `[F]`

32 bytes: `dtb_size`, `dtb_offset`, `id`, `rev` (all `>I`), then `custom[4]`
(`>I` each). Verified on 6 entries across the two payloads:

| file | entry | `dtb_size` | `dtb_offset` | `id` | `custom[0..1]` | FDT at offset |
|---|---:|---:|---:|---:|---|---|
| `a21s_dtbo.img` | 0 | 138,788 | 192 | 0 | 0, 0 | ✓ |
| | 1 | 152,428 | 138,980 | 0 | 1, 1 | ✓ |
| | 2 | 152,020 | 291,408 | 0 | 2, 2 | ✓ |
| | 3 | 152,220 | 443,428 | 0 | 3, 5 | ✓ |
| | 4 | 152,048 | 595,648 | 0 | 6, 0x20 | ✓ |
| `a21s_twrp_dtb.img` | 0 | 127,840 | 64 | 0 | 0, 0xff | ✓ |

**6 of 6** have `\xd0\x0d\xfe\xed` (FDT magic) at `dtb_offset` `[F]`. That is the
cheapest structural check available and it is what the parser asserts.

### 3.3 `total_size` is not the file size `[F]`

`a21s_dtbo.img` declares `total_size = 747,696` but is **8,388,608 B** — exactly
8 MiB, so a partition-padded image. `a21s_twrp_dtb.img` declares 127,904 and *is*
127,904. So `total_size == file_size` is **not** an invariant; it holds when the
image was not padded and fails when it was. Both cases occur in the corpus `[F]`.

---

## 4. Grammar C — AVB `AVB0` / `AVBf` `[F]`

Normative: AOSP `avbtool.py` (207,502 B), fetched 2026-11-26.

### 4.1 The two structures `[F]`

`AvbVBMetaHeader` is **256 B**: magic 4, version 2×4, auth-block size 8,
aux-block size 8, algorithm 4, then five `(offset, size)` u64 pairs (hash,
signature, public key, public-key metadata, descriptors), rollback index 8,
flags 4, rollback-index location 4, release string 48, reserved 80.
`256 = 4+4+4+8+8+4+80+8+4+4+48+80` `[F]`.

`AvbFooter` is **64 B**: magic `AVBf` 4, version 2×4, `original_image_size` 8,
`vbmeta_offset` 8, `vbmeta_size` 8, reserved 28 `[F]`.

### 4.2 Both verification laws reproduce on real bytes `[F]`

The `a21s_dtbo.img` payload carries an AVB footer at `8,388,544`:

| footer field | value |
|---|---|
| version | 1.0 |
| `original_image_size` | 748,480 |
| `vbmeta_offset` | 749,568 |
| `vbmeta_size` | 2,112 |

and at `749,568` an `AVB0` header with `authentication_data_block_size = 576`,
`auxiliary_data_block_size = 1,280`, `algorithm_type = 2` (`SHA256_RSA4096`),
`release_string = "avbtool 1.2.0"` `[F]`.

**Law 1 — the vbmeta digest.** `avbtool.py` hashes the 256-byte header *as-is*
together with the aux block; the stored digest lives in the auth block, not the
header. Measured:

```
sha256(header[0:256] ‖ aux_block) = 8b35b3478f3537c3dbc9ebdb69382c6cb729dbe886922d0221b30f3df65b752c
stored digest in auth[0:32]       = 8b35b3478f3537c3dbc9ebdb69382c6cb729dbe886922d0221b30f3df65b752c
```

**Law 2 — the hash descriptor.** The one descriptor is `tag=2` (`HASH`),
`partition_name = "dtbo"`, `image_size = 748,480`, `sha256`, 32-byte salt,
32-byte digest. Measured:

```
sha256(salt ‖ image[0:748480]) = 68fc8ad8982c180de7b6e0f4c6c08df4d45ec97701cef30867284380008dcb3c
stored digest                  = 68fc8ad8982c180de7b6e0f4c6c08df4d45ec97701cef30867284380008dcb3c
```

Both match byte-exactly `[F]`. This is the strongest single result in the note:
the spec, the payload and the implementation agree.

### 4.3 `image_size` is not `total_size` `[F]`

The dt_table header says `total_size = 747,696`; the AVB descriptor says
`image_size = 748,480`, which is **784 B larger**. And `748,480 mod 2048 = 960`,
so it is not page-aligned either. The digest therefore covers `747,696` real
table bytes plus 784 padding bytes — and hashing `d[0:747696]` instead gives
`a82d1289…` which does **not** match `[F]`. The AVB layer and the dt_table layer
disagree about how long the image is, and only the AVB number verifies.

### 4.4 Descriptor internals: the 60-byte reserved field `[F]`

`HashDescriptor` is `16 (header) + 56 (fixed) + 60 (reserved) + name + salt +
digest`. The variable-length fields start at **`offset + 132`**, not
`offset + 72`. Reading from 72 — which is where the fixed fields end — returns
the reserved zeros as if they were the partition name. This note's first parse
did that and produced `partition_name = b'\x00\x00\x00\x00'`; after correcting
to `+132` it reads `b"dtbo"` and the descriptor length is self-consistent:
`132 + 4 + 32 + 32 = 200`, matching `num_bytes_following = 184` plus the 16-byte
header `[F]`.

---

## 5. Grammar D — ELF, including the multi-ELF `xbl` `[F]`

437 rows across 11 basenames, 384,356,352 B — the count that is *verified* as
ELF, not every row whose name suggests it. `rpm.img` (24 rows) and `xbl_cfg.elf`
(2) are excluded because no in-repo source establishes their container (§6). The
repo's `research/qualcomm/docs/bootchain-census.md` already establishes the
per-image detail for FP6, so this section records only the two format-level
facts a cross-device parser needs.

- **`xbl.img` is several ELFs concatenated.** FP6's is three: an outer ELF32
  with junk machine (F-7), an inner ELF32 RISC-V, and an inner ELF64 AArch64,
  matching the stock name `xbl_s.melf` `[F]`. A parser that reads only the
  first header reports `e_machine = 1`, which is meaningless; it must walk every
  `\x7fELF` occurrence. The parser does this and reports `elf_count`.
- **`e_machine` alone is not an ISA claim.** `qupfw.img` is tagged `ELF64` on 63
  rows but FP6's is **ELF32 `EM_QDSP6` (164)** `[F]` — the `db_type` is wrong.
  Per the F-7 rule the machine value is a *claim*; `entry_in_load` is the
  cheapest corroboration and the parser reports both.

The 13-field ELF header is required reading. The last six halfwords are
`e_ehsize, e_phentsize, e_phnum, e_shentsize, e_shnum, e_shstrndx`, and the
header is **48 B (ELF64) / 52 B (ELF32)** — not the 42/46 B a ten-field struct
occupies `[F]`.

The failure a truncated read causes is **not** what it looks like. `e_ehsize`,
`e_phentsize` and `e_phnum` sit at tuple indices 7, 8, 9 in *both* the 10-field
and the 13-field layout, so a ten-field read returns them **correctly** `[F]`.
What breaks is that the struct is 6 B short, so a builder that appends the
program header immediately after it writes the phdr at offset 58 while
`e_phoff = 64` — and the parser then reads 6 B late, giving `p_type = 0` and a
garbage `p_vaddr` (`0x4000000000` where `0x400000` was written) `[F]`.

That distinction matters for a reader: the symptom is "every program header is
type 0", and the instinct is to blame `e_phnum`. The actual defect is the
**header length**, and the fix is the six missing halfwords, not the count
field. This note's first diagnosis blamed `e_phnum` and was wrong `[F]`.

---

## 6. What is not any of the four `[F]`/`[N]`

103 rows / 130,726,100 B remain **unverified**: no in-repo byte-level evidence
establishes their container, so this note declines to assign one.

| basename | rows | bytes | devices | what the corpus claims | status |
|---|---:|---:|---:|---|---|
| `tzsw.img` | 16 | 113,909,760 | 16 | `BOOT` | not a boot image by size; TZ software `[I]` |
| `bl31.img` | 16 | 1,667,072 | 16 | `BOOT` | not a boot image by size; ATF BL31 `[I]` |
| `bl1.img` | 16 | 249,856 | 16 | `BOOT` | not a boot image by size; ATF BL1 `[I]` |
| `unsparse_super_empty.img` | 25 | 116,572 | 23 | `BOOT` | **`[F]` not a boot image** (all < 8,192 B) |
| `rpm.img` | 24 | 10,567,680 | 24 | `ELF64` | container unverified |
| `lk.img` | 2 | 3,424,256 | 2 | `UNKNOWN` | container unverified |
| `preloader_raw.img` | 2 | 659,456 | 2 | `UNKNOWN` | container unverified |
| `xbl_cfg.elf` | 2 | 131,448 | 2 | `ELF64` | container unverified |

Only `unsparse_super_empty.img` is settled here, and only by size. The other
seven are the honest gap: 103 rows whose grammar this note cannot state.

Two basenames that a filename-based grouping would put here do **not** belong:

- `pvmfw.img` (18 rows) is a boot image **v3** per the FP6 census — it is in the
  `ANDROID!` row of the verdict table, and its payload being raw AArch64 is a
  property of the payload, not of the container `[F]`.
- `aop.img` and `cpucp.img` (70 rows) are ELF32 per the FP6 census — they are in
  the ELF row. Their `db_type=UNKNOWN` is a corpus gap, not a grammar fact `[F]`.

That is the reason the verdict table is grouped by verification status rather
than by name: a name-based grouping puts `pvmfw` in the wrong bucket and
`aop`/`cpucp` in the wrong bucket, in opposite directions.

---

## 7. The `db_type` defect, quantified `[F]`

| `db_type` | rows | basenames | correct? |
|---|---:|---|---|
| `BOOT` | 313 | `boot`, `recovery`, `init_boot`, `unsparse_super_empty`, `bl1`, `bl31`, `tzsw` | **240 of 313** |
| `UEFIBOOT` | 142 | `abl`, `xbl` | **no** — both are ELF, no `_FVH` at offset 0 |
| `ELF64` | 251 | 9 basenames | **partly** — `qupfw`, `shrm`, `aop_config` are ELF32 per FP6 |
| `DTB` | 125 | `dtbo`, `dtb` | **yes** |
| `AVB` | 115 | `vbmeta` | **yes** |
| `UNKNOWN` | 74 | `aop`, `cpucp`, `lk`, `preloader_raw` | 70 are ELF |
| `SECURITY` | 18 | `pvmfw` | it is a boot image v3 |

**73 `BOOT` false positives + 142 `UEFIBOOT` + 74 `UNKNOWN`** = 289 of 1,038
rows (27.8 %) carry a `db_type` that is not the container they are `[F]`/`[I]`.

The `UEFIBOOT` label is the most misleading: `abl.img` and `xbl.img` are both
ELF (`abl` ELF32 `EM_ARM`, `xbl` multi-ELF), and neither has a UEFI firmware
volume header (`_FVH`) at offset 0. The label appears to be inferred from the
partition name rather than the bytes `[I]`.

---

## 8. Gate 0 — prior art `[F]`/`[N]`

Access date **2026-11-28** for every query in this section. Queries are exact
strings. Counts were re-run today and **drifted** from the 2026-11-26 values
taken earlier in the same session (467→475, 292→297, 674→666, 8→9; the other
three unchanged). GitHub code search is a live index, so the numbers below are a
snapshot and the drift is the honest reading: the **order of magnitude** is the
finding, not the digit `[F]`.

### 8.1 GitHub code search (REST `/search/code`)

| query | hits (2026-11-28) | hits (2026-11-26) | what they are |
|---|---:|---:|---|
| `ANDROID! boot image header v4 vendor_ramdisk_size` | **475** | 467 | `bootimg_info.py`, U-Boot `android_image.h`, `unpack-bootimg.py` — the format is widely implemented |
| `struct boot_img_hdr_v4` | **297** | 292 | `topjohnwu/Magisk` `bootimg.hpp`, `svoboda18/magiskboot`, `coreboot/vboot` `vb2_android_bootimg.h` |
| `BOOT_MAGIC ANDROID! mkbootimg header_version` | **666** | 674 | `cfig/Android_boot_image_editor` vendors AOSP `mkbootimg.py`; `Project-Aloha/mu_aloha_platforms` |
| `boot image v4 signature vbmeta boot_signature_size` | **174** | 174 | repack scripts across several device trees |
| `AVB0 AvbFooter avbtool vbmeta descriptor` | **232** | 232 | `badabing2005/PixelFlasher` `avbtool.py`, `JingMatrix/TEESimulator` `VbMeta.kt` |
| `Qualcomm MBN v7 struct mbn_header ELF image` | **9** | 8 | `libimobiledevice/idevicerestore` `src/mbn.c` |
| `xbl_s.melf multi-ELF container` | **0** | 0 | — |

### 8.2 Normative specifications

| source | establishes |
|---|---|
| AOSP `bootimg.h` (433 lines, fetched 2026-11-26) | every boot/vendor_boot header layout, `BOOT_MAGIC`, all field sizes |
| AOSP `avbtool.py` (207,502 B, fetched 2026-11-26) | `AVB0`/`AVBf`, descriptor tags, both verification laws |
| AOSP `mkdtimg` / `libufdt` | `dt_table` header and entry |
| repo `research/fleet/boot-dtb.md` (751 lines) | dt_table padding laws, the AOSP-vs-Samsung split, AVB descriptor digests |
| repo `research/qualcomm/docs/bootchain-census.md` (237 lines) | FP6 inventory, `xbl_s.melf` multi-ELF, RISC-V housekeeping cores |

### 8.3 Decision — **PRIOR-ART**, and this note is the synthesis, not a discovery

This is **not** a `DELTA` in the sense of new format knowledge. Every grammar in
this family is publicly specified, and two of them are among the most
re-implemented formats in Android tooling (475 and 666 hits). Anyone
implementing a boot-image parser should read AOSP `bootimg.h` and `avbtool.py`
first, and this note does not improve on either.

What was genuinely **missing** and is delivered here:

1. **A single document stating that the `boot` family is four grammars plus an
   unverified remainder, and which basename is which.** No public source does
   this, because public sources are per-format; the corpus is per-family. The
   mapping table in §1 is the contribution `[F]`.
2. **The 73-row `db_type=BOOT` false-positive count, and the 94.40 % MiB-quantization
   of `boot.img` sizes.** These are corpus defects, not format facts, and no
   external source can see them `[F]`.
3. **The `dt_table` `>7I` field-order trap** stated as a trap, with the wrong
   and right parses shown side by side `[F]`.
4. **The DER-certificate tail** on a real boot image, which no header field
   accounts for `[F]`.
5. **An implementation** — `implementations/boot/bootimg_parser.py` — covering
   all four grammars with both AVB laws executable, which `implementations/boot/`
   did not have (it held only the `README.md` from issue #2042) `[F]`.

---

## 9. Honest negatives `[N]`

- **`xbl_s.melf` has zero external corroboration.** `xbl_s.melf` → **0** GitHub
  hits. The multi-ELF claim rests entirely on the repo's own FP6 census, which
  is a single-device observation. It may not generalize `[N]`/`[I]`.
- **No v3/v4 boot image was byte-verified.** The one real boot image obtained is
  **v0** (`header_version = 0`, Nexus 5X). v1–v4 were verified only against
  synthetic fixtures built from the documented layout, so their page arithmetic
  is spec-derived, not payload-derived `[N]`.
- **No `vendor_boot.img` payload was obtained at all.** That grammar is verified
  on fixtures only `[N]`.
- **No signature was cryptographically verified.** Both AVB laws check a
  **hash**; verifying the RSA signature would need the trust root, which is out
  of scope and out of policy. The note says "the digest matches", never "the
  image is authentic" `[N]`.
- **`pvmfw` is classified but not decoded.** It is a boot image v3 whose payload
  is raw AArch64 per the FP6 census; no disassembly was run here `[N]`.
- **Eight basenames are left unassigned.** `tzsw`, `bl31`, `bl1`, `rpm`, `lk`,
  `preloader_raw`, `xbl_cfg.elf` and `unsparse_super_empty` — 103 rows — have no
  in-repo byte-level evidence for their container. `tzsw`/`bl31`/`bl1` are
  called "not a boot image" on a **size** argument only, and their identity as
  TZ/ATF stages is prior-art inference, not a measurement here `[N]`/`[I]`.
- **`pvmfw`'s FP6 evidence is one device.** The boot-image-v3 classification
  rests on `research/qualcomm/docs/bootchain-census.md`, i.e. FP6 alone, applied
  to 18 rows spanning 18 devices including Pixel and OnePlus `[N]`/`[I]`.
- **The `boot.img` MiB-quantization cause is not established.** That 118 of 125
  rows are exact MiB multiples is `[F]`; that the corpus recorded partition
  sizes rather than image sizes is `[I]`, and nothing in the matrix distinguishes
  the two `[N]`.
- **No ISA claim** for `bl1`/`bl31`/`tzsw`/`aop`/`cpucp`. The `e_machine` values
  are recorded, not interpreted, per the F-7 rule `[N]`.
- **`unsparse_super_empty.img` is classified only by size.** At 4,592–4,772 B it
  cannot hold a 4 KiB boot page plus a kernel, so it is not a boot image; what
  it *is* (a sparse-image stub) is inferred from the name, not decoded `[N]`/`[I]`.

---

## 10. Open items `[U]`

1. Why `boot.img` sizes are MiB-quantized on 118 of 125 rows — is the upstream
   collector reading a partition table, or `fastboot`-padded images? The 7
   non-aligned rows suggest the method is not uniform `[U]`.
2. Whether the DER tail in §2.2 is a signing certificate for the boot image or
   an artefact of the test fixture it came from. One sample, so undecided `[U]`.
3. Whether `db_type=UEFIBOOT` on `abl`/`xbl` reflects an older UEFI-based
   bootloader generation that this corpus no longer contains `[U]`.
4. Whether `dt_table`'s `page_size` field (2,048 on both payloads) affects
   anything, given that entries are 4-byte aligned in practice `[U]`.

---

## 11. Method `[F]`

- Census: `csv.DictReader` over `upstream-contribution/blob-database/coverage-matrix.csv`,
  grouped on `blob_family`; every total, share, rank and percentage printed by
  the command that computed it, never carried in head.
- Boot image: `struct.unpack_from("<10I", d, 8)` for v0–v2 and
  `struct.unpack_from("<4I", d, 8)` for v3–v4, with `page_size` read from offset
  36 and `header_version` from offset 40; when `page_size` is 0 or absurd the
  version is taken from offset 40 and the page fixed at 4,096.
- `dt_table`: `struct.unpack_from(">8I", d, 0)` — all eight words, never `>7I`
  from offset 4.
- AVB: header at `struct.unpack_from("!4s2L2QL2Q2Q2Q2Q2QQLL47s")`, 256 B;
  footer at `len-64` as `!4s2LQQQ`; descriptors walked by
  `16 + num_bytes_following`.
- ELF: 13-field header (`HHIQQQIHHHHHH` for 64-bit, `HHIIIIIHHHHHH` for 32-bit);
  every `\x7fELF` offset collected to count concatenated images.
- Payloads opened read-only from scratch space; nothing committed; the only hex
  in this note is ≤16 bytes per sample.
- Grouping is by **verification status**, not filename: a basename enters a
  grammar row only if an in-repo source or a payload read establishes its
  container. This is why the verdict table sums to 1,038 rows while §6 still
  lists eight unassigned basenames — a filename-based grouping produced three
  misplacements (`pvmfw` into the remainder, `aop`/`cpucp` into it as well) that
  the verification-based one does not `[F]`.
- Implementation: `implementations/boot/bootimg_parser.py`, self-tests in
  `test_bootimg_parser.py` (67 tests, 3 skipped without `BOOT_FIXTURE_REAL`),
  fixtures generated by `make_fixture.py` from the documented layouts only. The
  suite calls `make_fixture.write_all()` in `setUpModule` because every fixture
  extension (`.img`, `.bin`) is gitignored, so a clean checkout regenerates them
  on the fly rather than depending on committed binaries `[F]`.
- Corrections made to this note during its own review are recorded in place
  rather than silently: the ELF failure mode (§5), the `bl1`/`bl31`/`tzsw`
  evidence class (verdict), the `rpm` container claim (§1), and the
  MiB-quantization inference (§2.3). Each was a value that had been *believed*
  rather than read off a command, and each now cites the command `[F]`.
