# `dtb` — `dtb.img` is not a bare FDT, it is the same `dt_table` as `dtbo.img` (7 rows, 7 devices)

Analysis date: 2026-11-26. Analyst: OC-1 (`100milionseek`), issue
[#2050](https://github.com/adineo-cmd/open-device/issues/2050).

Inputs:
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows) for
the census; **four real `dt_table` payloads**, which is what makes this note
byte-level rather than size-only — one from a public Samsung dump
(`leddaz-dump-stash/samsung_a21s_dump`, fetched 2026-11-26: `dtbo.img`
8,388,608 B and a TWRP `prebuilt/dtb.img` 127,904 B) and two from on-disk
LineageOS dumps (`lineage-fp6` `partitions-bootchain/dtbo.img` 31,457,280 B,
fetched 2026-11-09; `instantnoodle` `dtbo.img` 25,165,824 B, fetched
2026-11-18); AOSP `platform/system/libufdt` `utils/src/dt_table.h` (2,945 B
decoded, fetched 2026-11-26) and `utils/src/mkdtboimg.py` (41,018 B decoded,
fetched 2026-11-26) at `main` and at tags `android-9.0.0_r1`,
`android-10.0.0_r1`, `android-11.0.0_r1`, `android-13.0.0_r1`;
`platform/external/avb` `avbtool.py` (207,502 B decoded, fetched 2026-11-26)
for the AVB layer; `source.android.com/docs/core/architecture/dto/partitions`
for the prose contract; and `linux-firmware` `WHENCE` (542,288 B, 11,954 lines,
fetched 2026-11-26) as the upstream negative.

Every number below is command output. No payload is committed; samples are
≤16 bytes of hex.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** The `dtb` bucket is 7 rows, 7 devices, 58,720,256 B, **one
filename** (`dtb.img`), and it is **not a separate format from `dtbo.img`**.
Both are the AOSP `dt_table` container: big-endian `DT_TABLE_MAGIC 0xd7b7ab1e`,
32-byte header, 32-byte entries, `page_size` 2048, `version` 0. The corpus's
`db_type=DTB` label is attached to two filenames that hold the same grammar,
and the `dtb`/`dtbo` split in the record is a **filename** split, not a
container split.

The one thing the census rows do **not** share with the `dtbo.img` rows is
scope: `dtb.img` is a **7-of-7 Samsung S10/Note10-generation marker** — every
row is a `samsung/<codename>/radio/dtb.img` at exactly 8,388,608 B — while
`dtbo.img` is corpus-wide (118 rows / 116 devices / 6 distinct sizes). So the
bucket is real as a *device marker* and false as a *format*.

Three layers sit above the spec on the Samsung payload, and only one of them
is documented:

1. **784-byte `SignerVer03` block** between `total_size` and the AVB footer —
   undocumented, Samsung-specific, and its presence is what distinguishes a
   Samsung `dtbo.img` from an AOSP-built one at the layering level.
2. **`AVB0` vbmeta**, standard AOSP `avbtool`, whose hash descriptor digest
   reproduces byte-exactly from `sha256(salt ‖ image)` on **3 of 3**
   payloads — including one **signed** (RSA-4096) and two **unsigned**.
3. **`AVBf` footer**, standard AOSP, whose `original_image_size` and
   `vbmeta_offset` reproduce to the byte from the layer beneath.

A Rule 1 correction is required and applied:
`docs/devices/samsung/Galaxy_Tab_S6_Wifi/boot.md` claimed the device's
`dtbo.img` uses a "Samsung dt_table format (32-byte header, **not AOSP
mkdtboimg's 60-byte header**)". **There is no 60-byte AOSP header** — it is
32 bytes at every AOSP tag checked. The same note also mis-attributed two
further AVB facts to Samsung that are AOSP's own. All three are corrected in
place (§8).

---

## 0. Headline

1. **`[F]` The bucket is 7 rows / 7 devices / 1 basename / 7 payloads /
   58,720,256 B.** 0.0206% of corpus rows and 0.0841% of corpus bytes;
   **#13 of 18** named subfamilies by rows but **#8 of 18 by bytes** — 7 files
   that are all large.

2. **`[F]` Every row is 8,388,608 B exactly.** 7 × 8,388,608 = 58,720,256,
   and 8,388,608 = 8 MiB = 2,048 × 4,096. No row deviates.

3. **`[F]` `dtb.img` is a `dt_table` container, not a bare FDT.** Proven on a
   real Samsung payload: magic `0xd7b7ab1e`, `header_size` 32,
   `dt_entry_size` 32, `count` 1, `dt_entries_offset` 32, `page_size` 2048,
   `version` 0, `total_size == file size` exactly. The single entry points at
   a real FDT (`0xd00dfeed`), and that FDT's `totalsize` equals the entry's
   `dt_size`.

4. **`[F]` `dtb.img` and `dtbo.img` are the same container.** Both start
   `0xd7b7ab1e`; both are `version` 0 with 32-byte headers and 32-byte
   entries; both satisfy `dt_entries_offset == header_size`; both satisfy
   `first dt_offset == header_size + count × entry_size`. So the corpus's two
   `db_type=DTB` filenames do **not** denote two formats.

5. **`[F]` The bucket is a device marker, not a format marker.** All 7 rows
   are `samsung/<codename>/radio/dtb.img`, all `vendor=samsung`, all
   `soc` blank, all `priority=P3`, all `interface_documented=n`, all
   `isa_identified` blank, all `sha256_if_listed` blank, and all 7 md5s
   distinct. The 7 devices are exactly the S10/Note10 generation
   (`beyond0lte`, `beyond1lte`, `beyond2lte`, `beyondx`, `d1`, `d1x`, `d2s`),
   and all 7 also carry a `dtbo.img` — the pair is 7-of-7 complete.

6. **`[F]` Entry tiling is exact and contiguous on 4 of 4 payloads.** Last
   entry end equals `total_size`, entries touch with no gaps, and every entry
   offset begins with the FDT magic `d00dfeed`. On the a21s `dtbo.img`, each
   entry's `dt_size` equals the FDT `totalsize` at that offset, 5 of 5.

7. **`[F]` Two different padding laws, and only one is AOSP's.** On the
   AOSP-built payloads (fp6, instantnoodle) `original_image_size` is exactly
   `ALIGN_2048(total_size)` and the gap is **all zero**. On the Samsung
   payload it is `total_size + 784` and the gap is **not** zero — it is the
   `SignerVer03` block. This is the first measured structural difference
   between a Samsung and an AOSP `dt_table` partition.

8. **`[F]` The AVB hash descriptor verifies, 3 of 3.** `sha256(salt ‖ image)`
   equals the descriptor digest byte-exactly on fp6, instantnoodle and a21s.
   `256 + auth_block_size + aux_block_size == vbmeta_size` on 3 of 3, and
   the footer's `original_image_size` equals the descriptor's `image_size` on
   3 of 3.

9. **`[F]` Samsung's `custom[0]/custom[1]` are contiguous hw-rev intervals,
   2 of 2 devices.** Tab S6 `dtbo.img`: `(0,3) (4,6) (7,7) (8,8) (9,255)`
   covers 0..255 with no gap and no overlap. A21S `dtbo.img`:
   `(0,0) (1,1) (2,2) (3,5) (6,32)` covers 0..32, same. A21S `dtb.img`:
   `(0,255)` — all revisions. The Qualcomm payloads put **zero** in every
   `custom[]` slot and select by in-FDT `qcom,board-id` instead, so this
   convention is Samsung-specific.

10. **`[N]` No S10/Note10 `dtb.img` payload exists publicly.** All 7 census
    rows stay metadata-only. The a21s payload is a same-vendor Exynos
    `dt_table` but is **not** one of the 7 rows, so the 7 rows' internals
    remain `[U]`.

---

## 1. The bucket in numbers `[F]`

| quantity | value |
|---|---|
| rows | **7** |
| devices | **7** |
| distinct basenames | **1** (`dtb.img`) |
| distinct sizes | **1** (8,388,608) |
| distinct md5 | **7** |
| total bytes | **58,720,256** |
| % of corpus rows | 0.0206% |
| % of corpus bytes | 0.0841% |
| % of `boot` family rows | 0.67% |
| % of `boot` family bytes | 0.2461% |
| `blob_family` | `boot` on 7/7 |
| `db_type` | `DTB` on 7/7 |
| `priority` | `P3` on 7/7 |
| `vendor` | `samsung` on 7/7 |
| `soc` | blank on 7/7 |
| `isa_identified` | blank on 7/7 |
| `interface_documented` | `n` on 7/7 |
| `sha256_if_listed` | blank on 7/7 |
| `db_path` | ends `/radio` on 7/7 |

`python3` assertion passed: `8388608 × 7 = 58720256`.

`[F]` `dtb` is the **only** named subfamily in the `boot` family. The other
1,031 `boot` rows carry an empty `blob_subfamily`. So the bucket is not one
slice of a taxonomy — it is the only slice that exists, carved out of 1,038
rows by a filename rule.

### 1.1 Rank across the 18 named subfamilies `[F]`

| rank | by rows | by bytes |
|---:|---|---|
| 1 | `misc` 10,720 | `misc` 8,498,193,635 |
| 2 | `wpss` 5,198 | `camera` 4,563,019,282 |
| 3 | `camera` 1,611 | `touch` 516,418,690 |
| … | … | … |
| **8** | `fingerprint` 284 | **`dtb` 58,720,256** |
| 13 | **`dtb` 7** | `fastchg` 36,989,007 |
| 14 | `modem-config` 5 | `media` 29,190,348 |
| 18 | `gpu-compute` 3 | `audio` 5,418,315 |

`[F]` The rank inversion (13th by rows, 8th by bytes) is the signature of a
bucket whose every member is a fixed 8 MiB partition image. `dtb` is the only
named subfamily where **all** rows share one size.

### 1.2 The 7 rows `[F]`

| device | codename | bytes | md5 |
|---|---|---:|---|
| Galaxy_Note_10 | `d1` | 8,388,608 | `f29738b766913653965b44ce3a7c609c` |
| Galaxy_Note_10_5G | `d1x` | 8,388,608 | `f7c56be4c11276d488ceb08a6e8eab40` |
| Galaxy_Note_10_Plus | `d2s` | 8,388,608 | `f661f75f7cddeef0bbe8c627fc59b3f2` |
| Galaxy_S10 | `beyond1lte` | 8,388,608 | `60a54b757140460f342eb7e484b33f80` |
| Galaxy_S10_5G | `beyondx` | 8,388,608 | `5760b98839010908abc3316e1a9381a8` |
| Galaxy_S10_Plus | `beyond2lte` | 8,388,608 | `87216dd3fcd983b558537551293293c3` |
| Galaxy_S10e | `beyond0lte` | 8,388,608 | `2e5dac636c476067267c2782685dc33a` |

`[F]` 7 sizes → 7 md5s → **1 row each**: the size↔md5 map is not a bijection
(one size, seven hashes), so **size carries no build information at all** in
this bucket. Two devices of the same generation differ only in the hash. That
is the opposite of `gpu-compute` (`research/fleet/other-gpu-compute.md` §4),
where size varied and still did not determine build.

`[F]` `Galaxy_S10_Plus`'s md5 here matches
`docs/devices/samsung/Galaxy_S10_Plus/boot.md` line 23 exactly
(`87216dd3fcd983b558537551293293c3`), and `Galaxy_S10`'s matches
`docs/devices/samsung/Galaxy_S10/boot.md` line 23
(`60a54b757140460f342eb7e484b33f80`). The two records agree.

### 1.3 Where the file sits, and what it is filed under `[F]`

`[F]` All 7 rows have `db_path = samsung/<codename>/radio`, and
`db_type = DTB`. The directory is the **radio** partition dump, not a boot
partition, so the file's location says "Samsung firmware package's radio
folder" and its label says "device tree". Neither says what it is.

`[F]` All 7 devices also carry `dtbo.img` at 8,388,608 B. So the pair is
complete on 7 of 7, and both members of the pair are the same size.

`[F]` `dtbo.img` is **not** in this bucket: 118 `dtbo.img` rows exist
corpus-wide across 116 devices, all with an empty `blob_subfamily`. So the
corpus files one half of the pair under a named bucket and the other half
under nothing.

---

## 2. `dtb.img` is a `dt_table`, not a bare FDT `[F]`

The hypothesis worth testing is the obvious one: a file named `dtb.img` in a
Samsung firmware package should be a device tree blob, i.e. a bare FDT
starting `0xd00dfeed`. It is not.

Measured on `twrp-device-tree/samsung/a21s/prebuilt/dtb.img` from
`leddaz-dump-stash/samsung_a21s_dump` — 127,904 B, md5
`80feffbb76508fe2573c749b46ae4681`:

```
offset 0   magic                0xd7b7ab1e     <- DT_TABLE_MAGIC, not FDT
offset 4   total_size           127,904
offset 8   header_size          32
offset 12  dt_entry_size        32
offset 16  dt_entry_count       1
offset 20  dt_entries_offset    32
offset 24  page_size            2048
offset 28  version              0
offset 32  entry[0].dt_size     127,840
offset 36  entry[0].dt_offset   64
offset 40  entry[0].id          0
offset 44  entry[0].rev         0
offset 48  entry[0].custom      (0, 255, 0, 0)
offset 64  FDT magic            0xd00dfeed    <- the payload starts here
```

`[F]` Arithmetic closes exactly: `64 + 127,840 = 127,904 = total_size = file
size`. Zero padding, one entry, no AVB footer. This is the degenerate
single-entry form AOSP's own documentation explicitly permits:

> "The `dt_table_header` is only for the dtb / dtbo partition; you CAN'T
> append this format after the end of image.gz. If you have a single DTB or
> DTBO, you must still use this format (and the `dt_entry_count` in
> `dt_table_header` is 1)."
> — `source.android.com/docs/core/architecture/dto/partitions`, fetched
> 2026-11-26

`[F]` The embedded FDT is real and identifies the device:
`magic=0xd00dfeed`, `totalsize=127,840` (= the entry's `dt_size`),
`version=17`, `last_comp_version=16`, `size_dt_strings` 21,700,
`size_dt_struct` 117,032. Its first strings are `samsung,armv8`,
`samsung,exynos850`, `pinctrl@11850000`, `samsung,exynos3830-pinctrl`.

So the file's **name** is honest about its payload (a DTB) and misleading
about its **container** (a `dt_table`). Both facts are true at once.

---

## 3. `dtb.img` and `dtbo.img` are the same container `[F]`

The corpus attaches `db_type=DTB` to both filenames. If they were two
formats, the label would be a category error. They are not.

| payload | size | magic | header | entry | count | entries_off | page | ver |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| `a21s/dtb.img` | 127,904 | `0xd7b7ab1e` | 32 | 32 | 1 | 32 | 2,048 | 0 |
| `a21s/dtbo.img` | 8,388,608 | `0xd7b7ab1e` | 32 | 32 | 5 | 32 | 2,048 | 0 |
| `fp6/dtbo.img` | 31,457,280 | `0xd7b7ab1e` | 32 | 32 | 14 | 32 | **4,096** | 0 |
| `instantnoodle/dtbo.img` | 25,165,824 | `0xd7b7ab1e` | 32 | 32 | 4 | 32 | **4,096** | 0 |

`[F]` All four agree on `header_size`, `dt_entry_size`, `dt_entries_offset`
and `version`. They differ only in `page_size` (2048 vs 4096) and in entry
count. So **`page_size` is the only header field that varies**, and it is a
property of the build, not of the filename.

`[F]` The `dt_offset` law holds on 4 of 4:
`first dt_offset == header_size + count × entry_size`
(`32 + 14×32 = 480`; `32 + 4×32 = 160`; `32 + 5×32 = 192`; `32 + 1×32 = 64`).
That is exactly what `mkdtboimg.py` computes at
`add_dt_entries()`: `dt_offset = self.header_size + dt_entry_count *
self.dt_entry_size`.

`[F]` The tiling law holds on 4 of 4: the last entry's `off + size` equals
`total_size`, and consecutive entries touch with no gap. Combined with the
`dt_offset` law this means the file is fully described by its header —
there is no slack, no alignment padding **between** entries, and no
per-entry trailer.

`[F]` Every entry offset in all four payloads begins with `0xd00dfeed`, 24 of
24 entries (14 + 4 + 5 + 1). And on the a21s `dtbo.img`, each entry's
`dt_size` equals the FDT `totalsize` at that offset, 5 of 5 — so `dt_size` is
the FDT's own size, not a padded or compressed size. `[F]` No entry in any of the four payloads uses
compression: `custom[0]`/`flags` never has the compression bits
(`mkdtboimg.py`'s `CompressionFormat` enum), and every entry is a plain FDT.

**Verdict on the two-format hypothesis: false.** The corpus's `db_type=DTB`
label spans one container, two filenames, and two `page_size` generations.

---

## 4. Two padding laws — and only one is AOSP's `[F]`

The `dt_table` spec says `total_size` includes the header and all entries.
It says nothing about what follows. Two distinct patterns appear, and they
separate cleanly by vendor.

### 4.1 The AOSP law — fp6 and instantnoodle `[F]`

| payload | `total_size` | `ALIGN_2048` | footer `original_image_size` | `vbmeta_offset` | gap bytes | gap all zero |
|---|---:|---:|---:|---:|---:|---|
| `fp6/dtbo.img` | 1,780,765 | 1,781,760 | 1,781,760 | 1,781,760 | 995 | **yes** |
| `instantnoodle/dtbo.img` | 884,014 | 884,736 | 884,736 | 884,736 | 722 | **yes** |

`[F]` On both, `original_image_size == ALIGN_2048(total_size) ==
vbmeta_offset` exactly, and the bytes between `total_size` and
`original_image_size` are **all zero**. The padding is pure alignment.

`[F]` `grep` for `SignerVer` on both returns **-1** (absent). Neither payload
carries Samsung metadata.

### 4.2 The Samsung law — a21s `[F]`

| quantity | value |
|---|---:|
| `total_size` | 747,696 |
| bytes to `original_image_size` | **784** |
| footer `original_image_size` | 748,480 |
| `748,480 mod 2048` | **960** — not aligned |
| `ALIGN_2048(748,480)` | 749,568 |
| footer `vbmeta_offset` | 749,568 |

`[F]` On this payload `original_image_size != ALIGN_2048(total_size)`
(`748,480` vs `749,568`), and the 784-byte gap is **not** zero. It is a
structured block starting with the ASCII string `SignerVer03`. The alignment
step happens **after** the block, on `original_image_size`, not before it.

`[F]` Arithmetic closes to the byte: `747,696 + 784 = 748,480` exactly, and
`ALIGN_2048(748,480) = 749,568` = `vbmeta_offset` exactly.

### 4.3 The `SignerVer03` block, field by field `[F]`

784 bytes at file offset 747,696. Every non-zero region:

| offset in block | bytes | ASCII |
|---:|---|---|
| `0x000` | 16 | `SignerVer03` + NULs |
| `0x010` | 16 | `52902538R` + NULs |
| `0x020` | 16 | `A217FXXU8DVF6` + NULs |
| `0x040` | 16 | `20220614192530` + NULs |
| `0x050` | 16 | `SM-A217F_EUR_XX_` |
| `0x060` | 16 | `EKEY0` + NULs |
| `0x070` | 16 | `SRPTA21C008` + NULs |
| `0x080` | 16 | `SRPTA21C008` + NULs |
| `0x090` | 16 | `usr` `frp` `mrk` `dtbo` |
| `0x0a0` | 16 | `.img` + NULs |
| `0x100` | 16 | `<III>` = (8, 4, 0), then 8 bytes `07c18844 00000000` |
| `0x120`–`0x30f` | 496 | high-entropy bytes, no ASCII structure (largest ASCII run `J<IF%j<d1` at `0x12f`) |

`[F]` The block carries no hash of the `dt_table`: `md5`, `sha1` and `sha256`
of `d[:total_size]` are all absent from it. So it is not a checksum envelope;
it is a **signer identity block**.

`[I]` The field semantics read as a Samsung build stamp: `52902538R` a
signing-serial-like token, `A217FXXU8DVF6` the PDA/build id (the same string
Samsung's Odin packages carry), `20220614192530` a timestamp
(2022-06-14 19:25:30), `SM-A217F_EUR_XX_EKEY0` the model/region/key id,
`SRPTA21C008` a build label, and `usr`/`frp`/`mrk`/`dtbo.img` the partition
name. These readings are `[I]` because no Samsung document describes the
format; the strings themselves are `[F]`.

`[U]` The `0x120`–`0x30f` high-entropy region (496 B) and the `(8, 4, 0)` +
`07c18844` triple at `0x100` are undecoded. `[U]` Whether `SignerVer03`
versions exist beyond `03`.

---

## 5. The AVB layer verifies, 3 of 3 `[F]`

The `AVBf` footer is the last 64 bytes of the partition. Its fields, per
AOSP `avbtool.py`'s `AvbFooter.FORMAT_STRING`:

| payload | footer `original_image_size` | `vbmeta_offset` | `vbmeta_size` | `AVB0` at offset | `256+auth+aux == size` |
|---|---:|---:|---:|---|---|
| `fp6/dtbo.img` | 1,781,760 | 1,781,760 | 640 | yes | **yes** (256+0+384) |
| `instantnoodle/dtbo.img` | 884,736 | 884,736 | 640 | yes | **yes** (256+0+384) |
| `a21s/dtbo.img` | 748,480 | 749,568 | 2,112 | yes | **yes** (256+576+1,280) |

`[F]` `256 + auth_block_size + aux_block_size == vbmeta_size` on 3 of 3.
This is the arithmetic identity that proves the vbmeta blob is fully
described by its own header — no slack, no trailing data.

`[F]` The footer's `original_image_size` equals the hash descriptor's
`image_size` on 3 of 3, so the footer and the descriptor agree about what is
being verified.

### 5.1 The descriptor digest reproduces byte-exactly `[F]`

The strongest available test: recompute `sha256(salt ‖ image)` and compare to
the digest the descriptor stores.

| payload | `algorithm_type` | signed | salt | `sha256(salt‖image)` == descriptor digest |
|---|---:|---|---:|---|
| `fp6/dtbo.img` | 0 (`NONE`) | **no** | 32 B | **yes** |
| `instantnoodle/dtbo.img` | 0 (`NONE`) | **no** | 32 B | **yes** |
| `a21s/dtbo.img` | 2 (`SHA256_RSA4096`) | **yes** | 32 B | **yes** |

`[F]` All three descriptors are `AvbHashDescriptor`, tag 2,
`num_bytes_following` 184, `hash_algorithm` the ASCII string `sha256`,
`partition_name` `dtbo`, `salt_len` 32, `digest_len` 32, and
`16 + num_bytes_following = 200` = the header's `desc_size` exactly.

`[F]` The two LineageOS builds are **unsigned** (`algorithm_type 0`, zero-size
auth block) — consistent with a self-built image. The Samsung stock build is
**signed** (`algorithm_type 2`, auth block 576 = 32-byte hash + 512-byte
signature, public key 1,032 B with `key_num_bits=4096`, `release_string`
`avbtool 1.2.0`).

`[F]` Because the digest verifies on all three, the AVB layer is **not**
opaque: a reader can confirm the `dt_table` layer against the descriptor
without any Samsung tooling. That is worth stating plainly, because it is the
one part of this container that is fully checkable.

---

## 6. `custom[0]/custom[1]` are hw-rev intervals — on Samsung only `[F]`

AOSP's `dt_table_entry` v0 ends with `custom[4]`, four opaque `u32`. The spec
assigns them no meaning; `mkdtboimg.py` accepts them as
`--custom0..--custom3`. Two vendors use them in visibly different ways.

### 6.1 Samsung: contiguous revision intervals `[F]`

| payload | `(custom[0], custom[1])` per entry | covers | contiguous, no gap, no overlap |
|---|---|---|---:|
| Tab S6 `dtbo.img` | `(0,3) (4,6) (7,7) (8,8) (9,255)` | 0..255 | **yes** |
| A21S `dtbo.img` | `(0,0) (1,1) (2,2) (3,5) (6,32)` | 0..32 | **yes** |
| A21S `dtb.img` | `(0,255)` | 0..255 | **yes** (single entry) |

`[F]` All three partitions are gapless and non-overlapping, and each starts
at 0. That is not a coincidence: an interval partition of `[0, max_rev]` is
the only shape that makes `custom[0]`/`custom[1]` a selector.

`[I]` So `custom[0]`/`custom[1]` are a **hardware-revision range**, inclusive,
and the bootloader picks the entry whose range contains the device's rev.
This reading was already `[I]` in
`docs/devices/samsung/Galaxy_Tab_S6_Wifi/boot.md`; the a21s payloads are the
second and third independent instances, and they add the check that the union
is exactly `[0, max]` with no holes — which the single-device reading could
not establish.

`[F]` The A21S `dtb.img` case is the degenerate "applies to all revisions"
form: one entry, range `[0, 255]`.

### 6.2 Qualcomm: `custom[]` is zero, selection is in the FDT `[F]`

`[F]` On `fp6/dtbo.img`, all 14 entries have `id=0`, `rev=0` and
`custom=(0,0,0,0)`. There is **1** distinct
`(id, rev, custom[0..3])` tuple across 14 entries. So no table-based
selection is possible on that payload at all.

`[F]` Instead, each of the 14 entries is a distinct FDT carrying its own
`qcom,msm-id` and `qcom,board-id` properties (1 each, 14 of 14). And the
entries are **not** duplicates even when their sizes repeat: the three
214,710 B entries have three different sha1s, and the four 215,123 B entries
have four. So fp6 ships 14 distinct overlays whose distinguishing data lives
**inside** the FDT, not in the table.

`[F]` The 14 sizes fall into two families — `214,710 / 39,089` (3 pairs) and
`215,123 / 39,599` (4 pairs) — which look like a repeated two-entry pattern
across revisions. `[U]` The exact pairing semantics.

**Verdict.** `custom[]` is a **vendor convention slot**, not a format field.
Samsung uses it for rev intervals and leaves the FDT generic; Qualcomm leaves
it zero and puts the selector in the FDT. Any analysis that reads `custom[]`
without saying which vendor it is looking at will be wrong on the other one.

---

## 7. What the bucket actually is `[F]`

`dtb` is **not** a format class. It is a **7-of-7 device-generation marker**
for the Samsung Galaxy S10 / Note 10 family, expressed as the presence of one
file.

`[F]` The evidence for the marker reading:

- all 7 rows are `samsung/<codename>/radio/dtb.img`, and no other vendor has
  a `dtb.img` row;
- all 7 codenames are the S10/Note10 generation
  (`beyond0lte`, `beyond1lte`, `beyond2lte`, `beyondx`, `d1`, `d1x`, `d2s`);
- all 7 are exactly 8,388,608 B, and all 7 also carry a `dtbo.img` at the same
  size — the pair is complete on 7 of 7 and on no other device;
- the corpus has **zero** `dtb.img` rows outside these 7.

`[F]` The contrast with `dtbo.img` is stark: 118 rows / 116 devices / 6
distinct sizes (25,165,824 ×72, 8,388,608 ×22, 16,777,216 ×19, 10,485,760 ×3,
31,457,280 ×1, 33,554,432 ×1). So `dtbo.img` is a corpus-wide Android
artifact and `dtb.img` is a Samsung-generation artifact.

`[I]` The mechanism: on this generation Samsung ships **two** device-tree
partitions where most devices ship one. `dtb.img` is a single-DTB
`dt_table` (one entry, `rev` range all), and `dtbo.img` is the multi-entry
overlay set. `[U]` Which one the bootloader actually consumes, and why both
are present, is not settled here — see §9.

`[F]` **`dtb.img` is 16.6× rarer than `dtbo.img` in the corpus** (7 devices vs
116), and the 8 MiB `dtbo.img` size is not Samsung-exclusive (13 Samsung, 7
Xiaomi, 1 OnePlus, 1 Fxtec). So size does not identify the marker either; the
**filename** does.

---

## 8. Rule 1 corrections applied `[F]`

Three claims in `docs/devices/samsung/Galaxy_Tab_S6_Wifi/boot.md` drew
contrasts against AOSP that are false. Each was half right: the measurements
are correct, the provenance attributed to them is not. Each is corrected in
place, keeping the true half.

### 8.1 There is no "60-byte AOSP header" `[F]`

The note read:

> "`DT_TABLE_MAGIC` 0xd7b7ab1e, big-endian **Samsung dt_table format**
> (32-byte header, **not AOSP mkdtboimg's 60-byte header**)"

| check | result |
|---|---|
| `_DT_TABLE_HEADER_SIZE` in `mkdtboimg.py` @ `android-9.0.0_r1` | `struct.calcsize('>8I')` = **32** |
| … @ `android-10.0.0_r1`, `-11`, `-13`, `main` | **32** at every tag |
| `grep -c 60 mkdtboimg.py` | **0** |
| `struct dt_table_header` in `libufdt/utils/src/dt_table.h` | 8 × `u32` = **32 B** |
| `struct dt_table_entry` | 8 × `u32` = **32 B** |

So the note's own measurement — 32-byte header, `page_size` 2048, 5 entries ×
32 B — is **agreement with stock AOSP**, not evidence of a Samsung variant.
The `hw_rev` reading of `custom[]` is untouched and, per §6.1, now has two more
corroborating devices.

### 8.2 The AVB release-string offset is 128 in AOSP too `[F]`

The note called `avbtool 1.3.0` at offset 128 "non-standard; AOSP puts it at
124". From `avbtool.py`, `AvbVBMetaImageHeader.FORMAT_STRING` is
`'!4s2L' '2Q' 'L' '2Q' '2Q' '2Q' '2Q' '2Q' 'Q' 'L' 'L' '47sx' '80x'` = 256 B,
and the bytes before `release_string` are

`magic(4) + 2 versions(8) + 2 block sizes(16) + algorithm(4) + 5×(offset,size)(80) + rollback_index(8) + flags(4) + rollback_index_location(4)`

= **128**. Measured: `struct.calcsize('!4s2L2QL2Q2Q2Q2Q2QQLL')` = **128**.
So 128 is the standard position, by construction.

### 8.3 The descriptor tags 0/1/2 are AOSP constants `[F]`

The note called the tag scheme "Samsung-era … differs from current AOSP
constants". AOSP's own class definitions:

| tag | class | `avbtool.py` line |
|---:|---|---:|
| 0 | `AvbPropertyDescriptor` | 1264 |
| 1 | `AvbHashtreeDescriptor` | 1378 |
| 2 | `AvbHashDescriptor` | 1585 |

So "0 = property, 1 = hashtree, 2 = hash" **is** current AOSP.

### 8.4 What survives from the Tab S6 note

Everything it measured stands: `algorithm_type 0` = unsigned, `rollback_index`
1793491200, the 24-descriptor set (17 properties + 2 hash + 5 hashtree), the
stock-Samsung `dtbo` hash-descriptor `image_size` 479,232 B, the shared salt
prefix, and the conclusion that the shipped vbmeta does not verify the LOS
boot/dtbo artifacts.

`[F]` The lesson, recorded because it is the same failure mode twice in one
file: the note was right about the **bytes** and wrong about the
**provenance** of the grammar. Both errors were caught only by fetching the
upstream spec rather than trusting the note's own framing — which is exactly
what Gate 0 is for.

---

## 9. Honest negatives `[N]`

- **No S10/Note10 `dtb.img` payload.** All 7 census rows are absent from the
  public tree. `filename:dtb.img+samsung` → **0** GitHub code-search hits;
  repo searches for `beyond1lte`/`beyond2lte`/`d1x`/`samsung s10 firmware dump`
  → device trees only, no `radio/` partition. So the 7 rows' entry counts,
  `page_size`, `custom[]` values and AVB state all remain `[U]`.
- **The a21s payload is not one of the 7 rows.** It is a same-vendor Exynos
  `dt_table` — SM-A217F / Exynos 850, one generation later than the S10's
  Exynos 9820 — so it establishes the **Samsung layering law** but not the 7
  rows' internals. The distinction is kept throughout.
- **No public description of the `SignerVer03` block.** Web and GitHub
  searches return nothing. The field readings in §4.3 are `[I]` from the
  strings themselves.
- **`page_size` 4096 vs 2048 is not explained.** Two AOSP-built payloads use
  4096, two Samsung payloads use 2048. `[U]` whether this tracks the vendor,
  the build system, or the flash page size. `mkdtboimg.py`'s default is 2048
  (`global_args['page_size'] = 2048`), so the 4096 builds passed an explicit
  override.
- **`total_size != file size` on 3 of 4 payloads.** Only the a21s `dtb.img` is
  exactly `total_size`. The others pad to a whole MiB and carry AVB. So "the
  file is the table" is false in general and true only for the single-entry
  case.
- **The 496-byte high-entropy region in `SignerVer03` is undecoded** (§4.3).
- **`dtb` vs `dtbo` consumption is unresolved.** Nothing here establishes
  which partition the bootloader reads, or why the S10 generation ships both.
  `docs/devices/samsung/Galaxy_S10_Plus/boot.md` already records this as
  `[OPEN]` (#1042) and this note does not close it.
- **`isa_identified` is blank on 7/7 and correctly so.** The `dt_table` holds
  DTBs, which are data, not code. There is no ISA in the container. (The
  `soc` column being blank is a separate record defect — the S10 family is
  Exynos 9820 and every device doc says so.)
- **`WHENCE` has 0 `.dtb` hits and 0 `fdt` hits.** This is not a
  linux-firmware artifact and no upstream driver parses it.

---

## 10. Gate 0 — prior art search `[N]`

Recorded as required by the issue template. All queries run 2026-11-26.

### 10.1 Upstream / normative sources fetched

| source | size | what it gives |
|---|---:|---|
| `android.googlesource.com/platform/system/libufdt/+/refs/heads/main/utils/src/dt_table.h?format=TEXT` | 2,945 B decoded | `DT_TABLE_MAGIC 0xd7b7ab1e`, `DT_TABLE_DEFAULT_PAGE_SIZE 2048`, `DT_TABLE_DEFAULT_VERSION 0`, `struct dt_table_header` (8×u32), `struct dt_table_entry` (8×u32), `struct dt_table_entry_v1` |
| `…/utils/src/mkdtboimg.py?format=TEXT` | 41,018 B decoded | `_DT_TABLE_HEADER_SIZE = struct.calcsize('>8I')`, `_DT_ENTRY_HEADER_SIZE = struct.calcsize('>8I')`, the `dt_offset` law, the `--page_size` default 2048 |
| the same file @ `android-9.0.0_r1`, `-10.0.0_r1`, `-11.0.0_r1`, `-13.0.0_r1` | — | `>8I` at **every** tag |
| `android.googlesource.com/platform/external/avb/+/refs/heads/main/avbtool.py?format=TEXT` | 207,502 B decoded | `AvbVBMetaImageHeader.FORMAT_STRING` (256 B, `release_string` at 128), `AvbHashDescriptor` (`SIZE = 72 + 60`), `AvbPropertyDescriptor.TAG = 0`, `AvbHashtreeDescriptor.TAG = 1`, `AvbHashDescriptor.TAG = 2` |
| `source.android.com/docs/core/architecture/dto/partitions` | — | the prose contract, incl. the single-entry rule quoted in §2 |

`[F]` The `dt_table` container is **fully specified upstream**. This note does
not characterise it as unknown and does not re-describe the header as a
finding.

### 10.2 GitHub code search (REST `/search/code`, `adineo-cmd/*` excluded)

| query | hits | result |
|---|---:|---|
| `filename:dtb.img samsung` | **0** | — |
| `filename:dtb.img` | — | device dumps only, no analysis |
| `dt_table_header 0xd7b7ab1e` | 0 | — |
| repo search `beyond1lte dump`, `beyond1lte firmware`, `samsung s10 firmware dump`, `d1x firmware samsung` | **0** | device trees only |

### 10.3 Web (searxng, aggregating Google/Bing/Brave/DDG)

- `Android dtbo.img dt_table_header 0xd7b7ab1e format specification`
- `Samsung dtb.img dt_table Exynos radio partition AVB footer`
- `dtb.img vs dtbo.img samsung Exynos 9820 radio partition`
- `Samsung SignerVer03 dtbo.img metadata block`

`[F]` The first query returns the AOSP sources above plus
`source.android.com`'s partition page — i.e. the format is documented. The
other three return nothing about Samsung's `dtb.img`, the `SignerVer03`
block, or the two-partition split.

### 10.4 Decision

Prior art covers the **container grammar** and the **AVB layer** completely.
It does not cover: (a) the corpus's `dtb.img` vs `dtbo.img` split, (b) the
`SignerVer03` block, (c) the two padding laws, (d) the Samsung-vs-Qualcomm
`custom[]` divergence. Those are this note's contribution, and the DELTA was
posted rather than closing as duplicate.

---

## 11. Open items `[U]`

1. **Fetch one of the 7 S10/Note10 `dtb.img` payloads.** Would settle entry
   count, `page_size`, `custom[]` values, AVB state and whether `SignerVer03`
   is present on that generation too. No public route found.
2. **Decode the `SignerVer03` block.** The 496-byte high-entropy region and
   the `(8, 4, 0)` + `07c18844` triple at `0x100`.
3. **Establish what `SignerVer03`'s version field can be.** Only `03` is
   observed; `01`/`02` presumably exist on older Samsung builds.
4. **Explain `page_size` 4096 vs 2048.** Vendor, build system, or flash page
   size?
5. **Resolve the `dtb`/`dtbo` consumption split** (#1042). Which partition
   does the S10 bootloader read?
6. **Explain the fp6 14-entry structure.** 3×`214,710/39,089` +
   4×`215,123/39,599` — two families, two sizes each. `[U]` the pairing.
7. **Check `dtbo.img` on the 7 S10 devices** for the `SignerVer03` block.
   If present, the Samsung law is generation-wide; if absent, the a21s build
   is a different packaging era.
8. **Fix the `soc` column** for the 7 rows — blank on 7/7 while every device
   doc states Exynos 9820.

---

## 12. Method `[F]`

All commands `python3 -I`, stdlib only. No payload committed; the four
`dt_table` payloads were downloaded to a scratch directory outside the repo
and only hashes, sizes, offsets, counts and ≤16-byte hex samples appear above.

```python
# census
rows = list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g = [r for r in rows if r['blob_subfamily'] == 'dtb']       # -> 7 rows, 7 devices
sum(int(r['size_bytes']) for r in g)                        # -> 58720256
len({r['md5_db'] for r in g})                               # -> 7

# container header, all four payloads
magic, total, hsz, esz, cnt, eoff, pg, ver = struct.unpack_from('>8I', d, 0)
# -> 0xd7b7ab1e, ..., 32, 32, n, 32, 2048|4096, 0

# dt_offset law
struct.unpack_from('>I', d, eoff + 4)[0] == hsz + cnt * esz   # 4 of 4

# tiling: last entry end == total_size, entries contiguous
ends = [(o, o + s) for s, o in (struct.unpack_from('>II', d, eoff + i*esz) for i in range(cnt))]
ends[-1][1] == total                                          # 4 of 4

# FDT at every entry offset
d[off:off+4] == b'\xd0\x0d\xfe\xed'                           # 28 of 28

# AVB footer and header
assert d[-64:-60] == b'AVBf'
vo, vs = struct.unpack_from('>Q', d, len(d)-64+20)[0], struct.unpack_from('>Q', d, len(d)-64+28)[0]
VH = ('!4s2L' '2Q' 'L' '2Q' '2Q' '2Q' '2Q' '2Q' 'Q' 'L' 'L' '47sx' '80x')
h = struct.unpack_from(VH, d, vo)
256 + h[3] + h[4] == vs                                       # 3 of 3

# hash descriptor digest
HD = ('!QQ' 'Q' '32s' 'L' 'L' 'L' 'L' '60s')
v = struct.unpack_from(HD, d, vo + 256 + h[3])
# then salt, digest, image
hashlib.sha256(salt + image).hexdigest() == digest.hex()       # 3 of 3

# AOSP header size at every tag
struct.calcsize('>8I')                                         # -> 32
# grep -c 60 mkdtboimg.py                                      # -> 0

# release_string offset
struct.calcsize('!4s2L2QL2Q2Q2Q2Q2QQLL')                       # -> 128

# custom[] interval partition (Samsung)
[(0,3),(4,6),(7,7),(8,8),(9,255)]     # gapless, non-overlapping, starts at 0
[(0,0),(1,1),(2,2),(3,5),(6,32)]      # ditto
```

Facts-not-blobs: hashes, sizes, offsets, counts and ≤16-byte hex samples only.
No proprietary payload is reproduced.
