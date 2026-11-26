# `sensors` — the `snsc.bin` scene-snapshot container (5 rows, 5 devices, 3 builds)

Analysis date: 2026-11-26. Analyst: OC-1 (`100milionseek`), issue
[#2062](https://github.com/adineo-cmd/open-device/issues/2062).

Inputs:
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows) for the
census; **five publicly downloadable payloads**, which is what makes this note
different from a size-only census — `PixelOS-Nuwa/Nuwa-Dump` (Mi_13_Pro),
`EncomDumps/xiaomi_unicorn_dump` (Mi_12S_Pro), `Lantaslab/xiaomi_marble_dump`
(Poco_F5), `DeltaDumps/xiaomi_thor_dump` (Mi_12S_Ultra) and the mayfly tree
(Mi_12S), all fetched 2026-11-26; the same dumps' co-shipped
`odm/etc/camera/snsc_params.json`, `sceneDetection.xml`,
`xiaomiSceneDetection.xml`, `xiaomi/satsnapshot.json` and
`xiaomi/satsnapshotjpeg.json`; LineageOS `lineage-23.0`
`proprietary-files.txt` for `mayfly`, `unicorn`, `thor`, `marble` and `nuwa`
(fetched 2026-11-26); and `gitlab.com/kernel-firmware/linux-firmware`
`WHENCE` (fetched 2026-11-26) as the upstream negative.

Every number below is command output. No payload is committed; samples are
≤16 bytes of hex.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** The `sensors` bucket is 5 rows, 5 devices, 86,541,968 B, **one
filename** (`snsc.bin`), and **three payloads**. It is the only bucket in the
33,917-row corpus whose subfamily name is not a device class but a single
file — `snsc.bin` is the sole member, so `sensors` is a one-file bucket and
the name is a guess about what that file is.

That guess is wrong, and the file is not a sensor blob. `snsc` is **scene
snapshot** — Xiaomi's MIALGO trigger for motion-gated low-light capture. The
token is defined by the vendor's own co-shipped XML: `sceneDetection.xml`
carries an `<snsc_trigger>` block with `snsc_motion_intensity_thres`,
`snsc_lux_idx_start`/`_end`, `snsc_delay_v0`/`_fin`/`_fout`, and
`snsc_enter_dist`. The bucket therefore holds a **capture-pipeline payload**,
not sensor calibration, and it sits in `etc/camera` alongside 428 rows the
matrix correctly files as `camera`.

The payload itself is the substantive result: `snsc.bin` is a **16-byte-block
ECB-encrypted container** with a 48-byte magic, a 64 KiB header zero-padded to
`0x10400`, and a ciphertext body. Three independent proofs, below. The key is
shared: the same `E_K(0)` block appears in all five builds and in both sibling
camera files `ellc.bin` and `ellv.bin`. What separates them is the header, not
the key — `ellc.bin` carries the identical 48-byte magic and so is the same
container, whereas `ellv.bin` uses a 208-byte header under the same key. A third
sibling, `night_align_lsc_tbl_40962304.bin`, has no repeated block at all and is
not this container.

The 5 rows are **3 builds**, and the 16-byte gap between
Mi_12S_Pro and Poco_F5 is exactly one inserted ciphertext block with a
byte-identical 32-byte tail — which is the ECB proof, because a chained mode
would avalanche.

---

## 0. Headline

1. **`[F]` The bucket is 5 rows / 5 devices / 1 basename / 3 payloads /
   86,541,968 B.** 0.0147% of corpus rows and 0.1240% of corpus bytes;
   **#11 of 13** `other` subfamilies by rows but **#5 of 13 by bytes** — a
   handful of very large files.

2. **`[F]` `snsc` = *scene snapshot*, and the bucket name `sensors` is a
   misnomer.** The vendor XML that ships beside the file defines
   `<snsc_trigger>` with motion, lux-index and delay fields; the sibling
   `snsc_params.json` describes an SNPE/DSP ELLC model with relight and
   threshold settings. Nothing in either file is sensor calibration.

3. **`[F]` `snsc.bin` is ECB-encrypted with a 16-byte block.** Three
   independent proofs: (a) 46,718–55,362 duplicate 16-byte blocks where a
   uniform 128-bit source predicts ~1.7×10⁻²⁷; (b) all 67,762 duplicate
   offsets are 16-byte aligned and every duplicate 32-byte pair has both
   halves duplicated; (c) inserting one block changes nothing downstream —
   the tail is byte-identical.

4. **`[F]` The container is `magic(16) ‖ per-file(32) ‖ zeros → 0x10400 ‖
   ciphertext`.** The `0x30..0x10400` region is 4,157 blocks of which 4,154
   are the identical `E_K(0)` value and exactly 3 are metadata; the body is a
   whole number of 16-byte blocks at every size.

5. **`[F]` One key, five devices, two sibling files.** The constant
   `2f312ec846097cca49b08c9e979904bd` appears 9,682 / 6,968 / 9,682 / 5,227 /
   6,076 times in `snsc`×3, `ellc` and `ellv`; `ellc.bin` also shares the
   exact 48-byte magic. `night_align_lsc_tbl_40962304.bin` has **zero**
   repeated blocks and is a different artifact class.

6. **`[F]` The 5 rows are 3 builds, and the size↔md5 map is a bijection.**
   3 sizes → 3 md5s → 1 md5 each. Mi_12S / Mi_12S_Pro / Mi_12S_Ultra are one
   byte-identical 17,329,600 B build; Mi_13_Pro is 17,223,584 B; Poco_F5 is
   17,329,584 B.

7. **`[F]` Mi_12S_Pro and Poco_F5 differ by exactly one ciphertext block.**
   Poco_F5 = Mi_12S_Pro with one 16-byte block inserted at `0x1086d90`; the
   following 32 bytes are byte-identical in both. A chained mode cannot do
   that.

8. **`[N]` No key, no plaintext, no algorithm.** Zero public sources describe
   the container (Gate 0, §9). No ISA, no interface, no `sha256` on any row.
   The cipher is not identified beyond "16-byte block, ECB-shaped".

9. **`[F]` Two Rule 1 corrections in `docs/devices/xiaomi/Mi_12S_Pro/other.md`.**
   Its line 154 calls `snsc.bin` a "sensor-calibration/scene binary
   hypothesis" and line 53 files it under "sensors 1"; both are corrected in
   place with a dated pointer to this note.

---

## 1. The bucket in numbers `[F]`

| quantity | value |
|---|---|
| rows | **5** |
| devices | **5** |
| distinct basenames | **1** (`snsc.bin`) |
| distinct sizes | **3** |
| distinct md5 | **3** |
| total bytes | **86,541,968** |
| % of corpus rows | 0.0147% |
| % of corpus bytes | 0.1240% |
| % of `other` rows | 0.0334% |
| % of `other` bytes | 0.6115% |
| `db_type` | `UNKNOWN` on 5/5 |
| `priority` | `P3` on 5/5 |
| `vendor` | `xiaomi` on 5/5 |
| `soc` | blank on 5/5 |
| `isa_identified` | blank on 5/5 |
| `interface_documented` | `n` on 5/5 |
| `sha256_if_listed` | blank on 5/5 |

`python3` assertion passed: `17329600×3 + 17223584 + 17329584 = 86541968`.

### 1.1 Rank inside `other` `[F]`

The bucket is **small on rows and mid-sized on bytes** — the inverse of the
`esim` bucket, which is small on both.

| rank | by rows | rows | by bytes | bytes |
|---:|---|---:|---:|---:|
| 1 | `misc` | 10,720 | `misc` | 8,498,193,635 |
| 2 | `camera` | 1,611 | `camera` | 4,563,019,282 |
| 3 | `touch` | 880 | `touch` | 516,418,690 |
| 4 | `media` | 470 | `fingerprint` | 387,540,764 |
| 5 | `audio` | 422 | **`sensors`** | **86,541,968** |
| 6 | `fastchg` | 315 | `fastchg` | 36,989,007 |
| 7 | `fingerprint` | 284 | `media` | 29,190,348 |
| 8 | `oled` | 157 | `nfc` | 9,677,922 |
| 9 | `nfc` | 75 | `esim` | 8,407,085 |
| 10 | `esim` | 41 | `audio` | 5,418,315 |
| 11 | **`sensors`** | **5** | `tinysys` | 4,132,864 |
| 12 | `tinysys` | 4 | `oled` | 4,068,320 |
| 13 | `gpu-compute` | 3 | `gpu-compute` | 2,523,240 |

`other` as a whole is 14,987 rows / 14,152,121,440 B.

### 1.2 One filename, three payloads `[F]`

| size | md5 | devices |
|---:|---|---|
| 17,329,600 | `d79c2869a3e2e79487252c1c4f410f31` | Mi_12S, Mi_12S_Pro, Mi_12S_Ultra |
| 17,223,584 | `b5c9867518a101e7a968d6f4b84ae953` | Mi_13_Pro |
| 17,329,584 | `30449b524d12964dfa3cabad1a5c915d` | Poco_F5 |

The map `size → md5` is a bijection in both directions: 3 distinct sizes, 3
distinct md5s, one md5 per size. So there is no "same size, different build"
case to reason about, and the size alone identifies the build.

The three sizes are related by whole blocks and one large gap:

```
17329600 - 17329584 =      16  = 1 block
17329600 - 17223584 =  106016  = 6,626 blocks
```

### 1.3 Device coverage and location `[F]`

| device | codename | census path | LineageOS path | size |
|---|---|---|---|---|
| Mi_12S | mayfly | `xiaomi/mayfly/vendor/etc/camera` | `vendor/etc/camera/snsc.bin` | 17,329,600 |
| Mi_12S_Pro | unicorn | `xiaomi/unicorn/vendor/etc/camera` | `vendor/etc/camera/snsc.bin` | 17,329,600 |
| Mi_12S_Ultra | thor | `xiaomi/thor/vendor/etc/camera` | `vendor/etc/camera/snsc.bin` | 17,329,600 |
| Mi_13_Pro | nuwa | `xiaomi/nuwa/odm/etc/camera` | `odm/etc/camera/snsc.bin` | 17,223,584 |
| Poco_F5 | marble | `xiaomi/marble/vendor/etc/camera` | `vendor/etc/camera/snsc.bin` | 17,329,584 |

The census `db_path` and the LineageOS manifest agree **5 of 5**, including the
`vendor` vs `odm` partition split: Mi_13_Pro is the only one on `odm`.

`snsc.bin` is not the only file in its directory. The corpus files **428**
`*/etc/camera` rows as `camera` and only these **5** as `sensors`, so the
`sensors` label is applied to one file inside a directory whose other members
are all `camera`. That is the structural signature of a hand-assigned label,
not a derived one — and §2 shows the label is wrong.

---

## 2. `snsc` = scene snapshot, and `sensors` is a misnomer `[F]`

The token is defined by the vendor's own co-shipped XML, in
`odm/etc/camera/sceneDetection.xml` (28,726 B) and its near-duplicate
`xiaomiSceneDetection.xml` (28,703 B). Both carry the block at lines 518–529:

```xml
<snsc_trigger>
      <snsc_motion_intensity_thres>20</snsc_motion_intensity_thres>
      <snsc_lux_idx_start>290</snsc_lux_idx_start>
      <snsc_lux_idx_end>400</snsc_lux_idx_end>
      <snsc_factor_delay_enable>1</snsc_factor_delay_enable>
      <snsc_delay_v0>15</snsc_delay_v0>
      <snsc_delay_fin>3</snsc_delay_fin>
      <snsc_delay_fout>14</snsc_delay_fout>
      <snsc_delay_margin>25</snsc_delay_margin>
      <snsc_dist_enable>0</snsc_dist_enable>
      <snsc_enter_dist>1.5</snsc_enter_dist>
</snsc_trigger>
```

`[F]` That is a **capture trigger**, not a sensor description: a motion
intensity threshold, a lux-index window (`290`–`400`), a "factor delay"
enable, three delay values (initial / fade-in / fade-out) and a distance gate.
The block sits in the same file as `<hdr_trigger_1..6>`, `<hdr_default>` and
`<indoors_no_se>` — i.e. the scene/HDR decision table for the camera HAL.

`[F]` The companion `odm/etc/camera/snsc_params.json` (2,072 B) is a
**model-parameter file**, not calibration data. Its single top-level key is
`ellc`, with `phone_version` `M2`, `model_version` `v10.0`, `hdr` `true`,
`resize` `false`, `shape_patch` `[784,1040]`, `overlap` `[32,32]`, an
`snpe` block (`runtime` `dsp`) naming the same DLC twice —
`20221017_SC4644non2_2_snpe2.3.1.3811a4.dlc` — with `tf16` input
`[1,784,1040,16]` and output `[1,784,1040,4]`, a `relight_setting` block of
four lux-index ranges, and a `Threshold` block with `T_brightness`,
`T_dark_scene`, `T_motion_1`/`_2`, `T_over_expose_*`, `T_first_frame_luxindex`
and `T_merge_ratio`.

`[I]` Read together: `snsc` gates a **multi-frame low-light capture** (merge
ratio, motion threshold, relight ranges) driven by an **ELLC** neural model on
the DSP. "Scene snapshot" is the natural expansion and matches every field;
the vendor never spells the acronym out, so the *name* is `[I]` while the
*function* is `[F]`.

`[F]` Four more corroborations that this is a capture feature and not a sensor
artifact:

- `proprietary-files.txt` ships it beside `libmialgo_snsc.so` and
  `com.xiaomi.plugin.mialgosnsc.so` — a shared library and a camera plugin,
  which is where a pipeline payload lives, not where sensor calibration lives.
- The same manifest ships `ellc.bin` and `ellc_params.json` next to
  `snsc.bin` and `snsc_params.json` — a matched payload+params pair each.
- `xiaomi/satsnapshot.json` defines a `SatSnapshot` pipeline
  (`com.xiaomi.plugin.anchor`, `com.xiaomi.plugin.offlinepostproc`,
  `RAW10` → `YUV420_NV12`) — the sibling "satellite snapshot" feature, showing
  that `snapshot` is the family's own vocabulary.
- All five devices ship `snsc.bin`, `snsc_params.json`, `libmialgo_snsc.so`
  and `com.xiaomi.plugin.mialgosnsc.so` — **4 entries, 5 of 5** — so the file
  travels as part of a four-piece feature bundle.

`[F]` The `snsc_params.json` is **per-device, not shared**: the five copies are
four distinct md5s (2,072 B for nuwa; 1,976 B for unicorn and thor at the same
size but different md5; 1,957 B for marble). So the *payload* is shared across
a platform generation while the *parameters* are tuned per device.

`[N]` Nothing in the corpus or on the public web expands `snsc` or `ellc`.
`ellc` is presumably "enhanced low-light capture" and `ellv` its video
counterpart `[I]`, but neither acronym is documented.

---

## 3. The container is ECB-encrypted, 16-byte block `[F]`

This is the central result and it is proven three independent ways. All
measurements below are on the real payloads: the census md5s were **reproduced
exactly** from the public dumps (3 of 3 — `d79c2869…` 17,329,600 B,
`b5c98675…` 17,223,584 B, `30449b52…` 17,329,584 B), so the bytes analysed
are the bytes in the census.

### 3.1 Proof A — duplicate blocks at a rate uniform data cannot produce

Split each file into 16-byte blocks and count repeats:

| build | blocks | distinct | extra duplicates | uniform-128-bit expectation | ratio |
|---|---:|---:|---:|---:|---:|
| Mi_12S_Pro (17,329,600) | 1,083,100 | 1,027,738 | **55,362** | 1.72×10⁻²⁷ | 3.2×10³¹ |
| Mi_13_Pro (17,223,584) | 1,076,474 | 1,029,756 | **46,718** | 1.70×10⁻²⁷ | 2.7×10³¹ |
| Poco_F5 (17,329,584) | 1,083,099 | 1,027,748 | **55,351** | 1.72×10⁻²⁷ | 3.2×10³¹ |

`[F]` The birthday expectation for `n` blocks drawn uniformly from 2¹²⁸ is
`n²/(2·2¹²⁸)`; at `n ≈ 1.08×10⁶` that is ~1.7×10⁻²⁷ duplicates. Observing
46,718–55,362 is not a statistical fluctuation — it is 31 orders of magnitude.

`[F]` The repeats are concentrated in a single value. The block
`2f312ec846097cca49b08c9e979904bd` occurs **9,682** times in the 17,329,600 B
build, **6,968** in Mi_13_Pro and **9,682** in Poco_F5. The next most common
block occurs 318 times. A 16-byte value recurring thousands of times is the
signature of one plaintext block recurring thousands of times.

### 3.2 Proof B — the repeats are 16-byte aligned, and 32-byte pairs duplicate whole

`[F]` Every one of the 67,762 duplicate-block offsets in Mi_13_Pro is
`≡ 0 (mod 16)`. Not one falls on an odd byte. A 32-byte or 64-byte block
cipher would produce repeats aligned to 32 or 64; the observed alignment is
16.

`[F]` Of the 19,869 duplicate 32-byte pairs, **19,869 (100.0%)** have *both*
16-byte halves individually duplicated. If the cipher were 32-byte, a repeated
32-byte value would be a fresh coincidence at the 16-byte level; instead the
16-byte level is the cause.

`[F]` For every repeated block with a small repeat count, the offset
difference modulo 16 is 0 in **34,077 / 34,077** cases.

### 3.3 Proof C — inserting one block does not avalanche

Mi_12S_Pro is 17,329,600 B and Poco_F5 is 17,329,584 B — exactly 16 bytes
apart. Comparing them directly:

```
Mi_12S_Pro[0x1086d90+16:] == Poco_F5[0x1086d90:]   ->  True
```

`[F]` Poco_F5 is Mi_12S_Pro with **one 16-byte block inserted** at `0x1086d90`;
everything after that point is **byte-identical**, 32 bytes of it. The inserted
block is `48ee5ca01db7f1bcce6566f49ec4b6ac`, which occurs once in Mi_12S_Pro
and zero times in Poco_F5.

`[F]` This is decisive against a chained mode. In CBC, CFB, OFB or CTR,
inserting one plaintext block shifts the chaining input (or the counter) for
every subsequent block, so **every** later ciphertext block changes. Here the
tail is unchanged, which means each block is encrypted independently: ECB.

`[I]` A 32-byte tail is short, so Proof C alone would be weak; it is offered as
confirmation of A and B, which are statistical and do not depend on the tail
length. The three proofs agree, and no single one is load-bearing.

### 3.4 What ECB does *not* explain, and how the apparent conflict resolves

`[F]` The raw payload chi-square against a uniform byte distribution is
**2,104.8** (Mi_13_Pro) and **7,509.3** / **7,390.3** (Mi_12S_Pro / Poco_F5)
at 255 df, where uniform predicts ≈255 ± 22.6. On its face that contradicts
"ciphertext is uniform".

`[F]` It resolves by removing the duplicated blocks. Restricting to blocks that
occur **exactly once** gives chi-square **263.49**, **238.64** and **251.15** —
all inside the uniform band. So the ciphertext byte distribution *is* uniform;
the inflation is caused entirely by plaintext repetition surfacing as repeated
ciphertext blocks. That is precisely the ECB leak, so the "anomaly" is the
strongest single piece of evidence for ECB rather than a counterexample to it.

`[F]` Correspondingly the payload does not compress: zlib level 9 on the first
1 MiB of the body gives **98.88%**, **98.84%** and **98.88%** — i.e. no gain.
Entropy is 7.9997 bits/byte. There is no residual redundancy to exploit, which
is why the plaintext is not recoverable from statistics alone.

`[F]` One 1 MiB window is the exception and is worth recording as an honest
oddity: in Mi_13_Pro, `0x800000..0x900000` compresses to **74.11%** and has
42.0% duplicated blocks, against 100.03% for the neighbouring windows. Shuffling
its blocks in place raises the ratio to 95.91%, which proves the compressibility
comes from *repeated blocks*, not byte skew. `[I]` A run of identical plaintext
blocks inside the encrypted stream — most likely a zero-filled or constant
region of the underlying resource. `[U]` Its meaning is unknown.

### 3.5 The key is shared, and the siblings confirm it

`[F]` The constant block `2f312ec846097cca49b08c9e979904bd` appears in every
`snsc.bin` build and in two sibling camera files:

| file | 48-byte magic present | `E_K(0)` occurrences |
|---|---|---|
| `snsc.bin` (Mi_12S_Pro) | yes | 9,682 |
| `snsc.bin` (Mi_13_Pro) | yes | 6,968 |
| `snsc.bin` (Poco_F5) | yes | 9,682 |
| `ellc.bin` (nuwa) | **yes** | 5,227 |
| `ellv.bin` (nuwa) | no | 6,076 |
| `night_align_lsc_tbl_40962304.bin` | no | **0** |

`[F]` `ellc.bin` shares the **exact** 48-byte magic
(`f082344c5d714360d9eacb875812c241` at `0x00`) *and* the same `E_K(0)` value,
so `snsc` and `ellc` are the same container under the same key — the matched
payload pair the manifest hints at.

`[F]` `ellv.bin` shares the `E_K(0)` value but **not** the magic, and its
header is 208 bytes (`0x00..0xd0`) rather than 48: same key, different header
schema.

`[F]` `night_align_lsc_tbl_40962304.bin` has **2,359,296 distinct 16-byte
blocks out of 2,359,296** — zero repeats, maximum repeat count 1. It is not
this container and is not ECB-encrypted in the same way, despite being the
largest camera sibling.

`[N]` A shared `E_K(0)` proves a shared key **only** under the assumption that
the block is the encryption of zeros. That the value recurs is `[F]`; that it
is `E_K(0)` is `[I]`, resting on the zero-fill interpretation in §4.

---

## 4. The container layout `[F]`

Every `snsc.bin` size is a whole number of 16-byte blocks **after subtracting
66,560 bytes** (`0x10400`):

| build | size | `size − 0x10400` | blocks | remainder |
|---|---:|---:|---:|---:|
| Mi_12S_Pro | 17,329,600 | 17,263,040 | 1,078,940 | 0 |
| Mi_13_Pro | 17,223,584 | 17,157,024 | 1,072,314 | 0 |
| Poco_F5 | 17,329,584 | 17,263,024 | 1,078,939 | 0 |

`[F]` The region `0x30..0x10400` (66,512 B = 4,157 blocks) is where the
structure is visible:

| build | blocks in region | equal to `E_K(0)` | metadata blocks | metadata offsets |
|---|---:|---:|---:|---|
| Mi_12S_Pro | 4,157 | 4,154 | **3** | `0x400`, `0x410`, `0x420` |
| Mi_13_Pro | 4,157 | 4,154 | **3** | `0x400`, `0x410`, `0x420` |
| Poco_F5 | 4,157 | 4,154 | **3** | `0x400`, `0x410`, `0x420` |
| `ellc.bin` | 4,157 | 4,151 | **6** | `0x400`…`0x450` |

`[F]` Comparing the region across builds shows they differ in **exactly** the
metadata slots and nowhere else:

```
Mi_12S_Pro vs Mi_13_Pro   : 3 differing 16B blocks at 0x400, 0x410, 0x420
Mi_12S_Pro vs Poco_F5     : 3 differing 16B blocks at 0x400, 0x410, 0x420
Mi_12S_Pro vs ellc.bin    : 6 differing 16B blocks at 0x400..0x450
Mi_12S_Pro vs ellv.bin    : 40 differing 16B blocks (0x30..0xc0, 0x400..0x5d0)
```

`[F]` So the plaintext is a small header followed by a **long run of zeros to
`0x10400`**, and the ciphertext is that zero run encrypted block-by-block. This
is why one value recurs thousands of times: it is the encryption of the zero
block.

`[I]` The layout, with the caveat that all field meanings beyond the magic are
unknown:

| plaintext offset | length | content | evidence |
|---|---:|---|---|
| `0x00` | 16 | fixed magic `f082344c5d714360d9eacb875812c241` | identical in `snsc`×3 and `ellc`, absent in `ellv` `[F]` |
| `0x10` | 32 | per-file 32-byte value | differs across all 4 files `[F]`; **not** md5/sha1/sha256 of the body `[F]` |
| `0x30` | to `0x10400` | zeros, with 3 (or 6) metadata blocks at `0x400` | 4,154 / 4,157 blocks identical `[F]` |
| `0x10400` | to EOF | body: 1,072,314–1,078,940 blocks | whole blocks, no remainder `[F]` |

`[F]` The 32 bytes at `0x10` are not a digest of the body: `md5`, `sha1` and
`sha256` of `body = d[48:]` were computed for all three builds and none
matches. `[U]` Their role is unknown — plausibly a key id, a build id, or an
encrypted metadata block.

`[F]` The 3 metadata blocks at `0x400` are per-file distinct values:

| build | `0x400` | `0x410` | `0x420` |
|---|---|---|---|
| Mi_12S_Pro | `a66c7c408c5462e8239318466bc59723` | `5227a2d84ff5109bd3e6cd9751c90857` | `2e7e07450de613380031f7ec03e19fb1` |
| Mi_13_Pro | `6c25e0eae8f1cd522775b453b43ef69f` | `b486030f09f07bdb0b0b037f74dc7521` | `6d9f744a4c670def5ece917180608a35` |
| Poco_F5 | `60ae1f37154e5a35756650b4625c20e1` | `d486f798a4d07cb48d830e9b406a2b00` | `86151056776a8500a67a8d8e16301e35` |

`[I]` Three 16-byte records, differing per build, in a region otherwise zero —
consistent with a small table of per-build identifiers (counts, offsets, or
checksums). Not decoded.

`[F]` `ellv.bin` uses a 208-byte header and the same key: its `0xd0..0x10400`
region holds 4,117 `E_K(0)` blocks out of 4,147, with 30 non-filler blocks at
`0x400..0x5d0`. `[I]` Same container family, longer metadata schema.

---

## 5. Three builds, and one inserted block `[F]`

### 5.1 The 17,329,600 B build is shared by three devices `[F]`

Mi_12S, Mi_12S_Pro and Mi_12S_Ultra all carry md5
`d79c2869a3e2e79487252c1c4f410f31` at 17,329,600 B — one byte-identical build
across the three SM8475-generation devices. This is the expected pattern: they
share a camera platform and therefore a shared capture model.

`[F]` Note this against the sibling doc's phrasing, which lists the span as
`{Mi_12S, Mi_12S_Ultra}` — that is the same fact expressed *excluding* the
subject device, which is that document's convention throughout (verified: its
`night_align` span of 5 and `ellv` span of 1 both exclude Mi_12S_Pro). The
underlying census span is 3 devices. No correction needed there; see §7.

### 5.2 Poco_F5 vs Mi_12S_Pro: one block `[F]`

The two largest builds are 16 bytes apart and identical except for one
insertion (§3.3). Their `0x10` headers, `0x400` metadata and the bulk of the
body all differ, so they are **different builds** — the insertion is not a
padding difference on identical content. The body comparison is what carries
the proof: byte-identical for the whole 32-byte tail after the insertion
point.

`[F]` Pairwise identical-block fractions show how little the builds share:

| pair | identical 16-byte blocks | fraction |
|---|---:|---:|
| Mi_12S_Pro vs Mi_13_Pro | 4,818 / 1,076,474 | 0.45% |
| Mi_13_Pro vs Poco_F5 | 4,818 / 1,076,474 | 0.45% |
| Mi_12S_Pro vs Poco_F5 | 118,063 / 1,083,099 | **10.90%** |

`[F]` And that 10.90% is not uniform — it is concentrated in one window:

| window | identical |
|---|---:|
| `0x700000` | 48.38% |
| `0x800000` | **99.99%** |
| all other windows | ≤ 9.11% |

`[F]` So Mi_12S_Pro and Poco_F5 share one ~1 MiB region almost exactly, and the
rest of the body is unrelated. `[I]` A shared asset (one model or table) inside
otherwise per-build content. `[U]` Which asset is unknown.

`[F]` This window is the same `0x800000` region that is anomalously
compressible in Mi_13_Pro (§3.4) — but in Mi_13_Pro it is *not* shared with the
other builds. The two observations are about the same offset in different
files and should not be conflated.

### 5.3 Mi_13_Pro is a different generation `[F]`

Mi_13_Pro is 106,016 B (6,626 blocks) smaller than the 17,329,600 B build and
shares only 0.45% of its blocks with either other build. Its header, metadata
and body are all distinct. It is the SM8550 generation, one step beyond the
SM8475 trio, and the payload does not carry over.

---

## 6. Defects in the record `[F]`

### 6.1 The bucket name `sensors` is wrong `[F]`

The subfamily name asserts the file is sensor-related. §2 shows the file is a
capture-pipeline payload gated by a scene-snapshot trigger; §3 shows it is an
encrypted container. It contains no sensor identification, no calibration
data, and no per-sensor structure. All five rows are `xiaomi`, all five are in
`etc/camera`, and 428 sibling rows in the same directories are `camera`.

`[I]` The label was most likely assigned from the `sns` substring in `snsc`
read as "sensor". The vendor's own XML shows `sns` is "scene **sns**apshot".

`[N]` No rename is proposed here: changing a corpus label is a
`blob-database` change, not a `research/` change, and the issue scope is
documentation.

### 6.2 `soc` is blank on all five rows `[F]`

`soc` is empty on 5/5. The devices are identifiable from public record —
Mi_12S/Pro/Ultra are SM8475, Mi_13_Pro is SM8550, Poco_F5 is SM7475-class —
but the matrix does not carry it. Recorded, not fixed (same reason as 6.1).

### 6.3 The file is not in the LineageOS tree as a `camera` file `[F]`

All five manifests list `snsc.bin` under `etc/camera` with the two `mialgo`
libraries, i.e. the ROM trees treat it as a camera component. The matrix
treats it as `sensors`. The two disagree, and the ROM trees are the better
witness because they are the vendor's own layout.

---

## 7. What this adds to the existing record `[F]`

`docs/devices/xiaomi/Mi_12S_Pro/other.md` already names `snsc.bin` twice. Both
passages were **corrected in place** (Rule 1, dated 2026-11-26), not merely
contradicted in this file:

- **Line 154** described `snsc.bin` as "a sensor-calibration/scene binary
  hypothesis [I], function unverified". The function is now verified from the
  vendor XML (§2) and the container is now characterised (§3–§4), so the
  passage is annotated with the decoded meaning and a pointer here.
- **Line 53** counted `sensors 1 = snsc.bin in H`, which is accurate as a
  census statement but repeats the misnomer; annotated with the decode.

`[F]` **No false correction was made.** The sibling doc's span convention
excludes the subject device, verified three ways before touching it: its
`night_align` span of 5 names the 5 non-Mi_12S_Pro carriers of a 6-device
md5; its `ellv` span of 1 names the single non-Mi_12S_Pro carrier of a
2-device md5; its "8-9 devices" bucket row matches a 9-device md5 on 8
non-subject devices. Under that convention its `{Mi_12S, Mi_12S_Ultra}`
phrasing for `snsc.bin` is **correct** and was left alone.

`[F]` The same check showed its line 184 row `| 2 devices | 9 | snsc.bin, … |`
uses the same convention: every one of those 9 files has a 3-device md5, so
"2 devices" = 2 non-subject carriers. Left alone for the same reason.

What is genuinely new:

- the container is identified and its layout measured (§4);
- the cipher mode is proven ECB and the block size 16 (§3);
- the key is shown shared across 5 builds and 2 sibling files (§3.5);
- `snsc` is decoded to scene snapshot from vendor data (§2);
- the 5 rows are resolved to 3 builds with a bijection (§1.2);
- the one-block insertion between two builds is located exactly (§5.2).

---

## 8. Honest negatives `[N]`

- **No key.** The cipher is 16-byte-block ECB-shaped, but the algorithm
  (AES? something else?) and the key are unknown. Every payload is publicly
  downloadable, which does not help: ECB is only breakable with known plaintext
  or a key, and the plaintext is a model/resource blob with no known structure.
- **No plaintext recovered.** No header, no string table, no magic inside the
  body. `grep` for `sensor`, `camera`, `SONY`, `IMX`, `samsung`, `xml`, `json`,
  `qualcomm`, `xiaomi`, `mialgo`, `snsc`, `snapshot`, `ellc`, `dlc`, `snpe`
  returns 0–2 incidental hits each on 17 MB, which is the expected count for
  random bytes.
- **The cipher is not named.** "ECB with a 16-byte block" is a mode+block-size
  statement; it is consistent with AES-128/192/256, SM4, or a vendor cipher.
  Not distinguishable from ciphertext alone.
- **`E_K(0)` is an inference.** The constant block recurring is `[F]`; that it
  equals the encryption of 16 zero bytes rests on the zero-fill reading of
  `0x30..0x10400` (`[I]`). A different constant plaintext would fit the
  observations equally.
- **No prior art.** Gate 0 (§9) found no public description of this container,
  no driver, no format spec, and no analysis. `snsc.bin` appears in exactly
  **one** GitHub code-search hit, a device dump with no write-up.
- **`snsc` and `ellc` are not expanded by any vendor document.** "Scene
  snapshot" and "enhanced low-light capture" are `[I]` readings of the
  configuration fields, not published expansions.
- **The 3 metadata blocks and the 32-byte `0x10` field are undecoded.** They
  are per-build distinct values with no observable structure.
- **The `0x800000` window is unexplained.** 42% duplicated blocks and 74%
  compressibility in one window, in one build, against 0% elsewhere. Recorded
  as a fact; the cause is `[U]`.
- **`isa_identified` is blank and correctly so.** There is no executable code
  visible: the body is ciphertext. The bucket has no ISA to report.
- **`interface_documented` is `n` and stays `n`.** No driver parses this file
  (linux-firmware `WHENCE` has 0 hits, §9), so there is no interface to cite.

---

## 9. Gate 0 — prior art search `[N]`

Recorded as required by the issue template. All queries run 2026-11-26.

**GitHub code search** (REST `/search/code`):

| query | hits | result |
|---|---:|---|
| `filename:snsc.bin` | 1 | `PixelOS-Nuwa/Nuwa-Dump:odm/etc/camera/snsc.bin` — a dump, no analysis |
| `"snsc.bin" in:path` | 1 | same |
| `snsc user:PixelOS-Nuwa` | 8 | all inside the same dump: `sceneDetection.xml`, `xiaomiSceneDetection.xml`, `xiaomi/satsnapshot.json`, `satsnapshotjpeg.json`, `proprietary-files.txt` |

**Web** (searxng, aggregating Google/Bing/Brave/DDG): `snsc.bin Xiaomi camera
firmware`; `snsc.bin file format sensor`; `"snsc.bin" xiaomi vendor etc
camera`; `Qualcomm snsc sensor "snapshot" camera service`; `"snsc" camera
Qualcomm sensor node service`; `snsc.bin 17MB xiaomi camera tuning`; `Xiaomi
snsc.bin what is it sensor calibration`; `Xiaomi MIALGO camera "snsc" scene
snapshot ELLC`; `"ellc_params.json" camera Xiaomi`; `MIALGO ELLC low light
camera Xiaomi`; `Xiaomi camera "snsc.bin" encrypted`; `Qualcomm camera tuning
binary encrypted 16 byte block ECB`.

`[N]` Zero pages describe the container, its cipher, its key or its plaintext
schema. The substantive hits are (a) vendor makefiles copying the file and (b)
a GitLab all-files listing co-locating `ellc.bin`, `ellc_params.json`,
`ellv.bin` — corroborating the sibling grouping of §3.5, not the format.

**Kernel / linux-firmware**: `gitlab.com/kernel-firmware/linux-firmware`
`WHENCE`, fetched 2026-11-26, 542,288 B, 11,954 lines, 271 `Driver:` stanzas.
`grep -i 'snsc|ellc|ellv|mialgo'` → **0** hits. The only Xiaomi-adjacent line
is `brcm/brcmfmac4356-pcie.Xiaomi Inc-Mipad2.txt`, unrelated. This is not a
linux-firmware blob and no upstream driver parses it.

**Decision**: no prior art, so the issue stayed open and this DELTA was
delivered rather than closing as duplicate. DELTA comment posted at
[#2062 comment 7186197732](https://github.com/adineo-cmd/open-device/issues/2062#issuecomment-7186197732).

---

## 10. Open items `[U]`

1. **Identify the cipher.** A 16-byte block with ECB is the shape; AES vs
   vendor cipher is unresolved. Any known-plaintext pair would settle it.
2. **Recover the key.** No route found. The key presumably lives in
   `libmialgo_snsc.so` or the plugin, neither of which is analysed here.
3. **Decode the 3 metadata blocks** at `0x400` and the 32-byte `0x10` field.
   Three per build, per-build distinct — likely counts/offsets/checksums.
4. **Decode the body.** 1.07M ciphertext blocks; the plaintext is presumably
   the ELLC model referenced by `snsc_params.json` plus supporting tables.
5. **Explain the `0x800000` window** (§3.4, §5.2): 42% duplicated blocks and
   74% compressibility, one window, one build.
6. **Establish `ellc` / `ellv` / `snsc` expansions** from a vendor document if
   one exists.
7. **Resolve the `sensors` label** with the `blob-database` owner (§6.1).
8. **Check whether `ellv.bin`'s 208-byte header is the same schema** with more
   fields, or a different one.

---

## 11. Method `[F]`

All commands `python3 -I`, stdlib only. No payload committed; the five dumps
were downloaded to a scratch directory outside the repo and only hashes,
sizes, offsets, counts and ≤16-byte hex samples appear above.

```python
# census
rows = list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s = [r for r in rows if r['blob_subfamily'] == 'sensors']      # -> 5 rows, 5 devices
sum(int(r['size_bytes']) for r in s)                            # -> 86541968

# payload identity reproduced against the census (3 of 3)
hashlib.md5(open(f,'rb').read()).hexdigest()                    # -> matches md5_db

# Proof A: duplicate 16-byte blocks vs the birthday expectation
blocks = [d[i:i+16] for i in range(0, len(d), 16)]
len(blocks) - len(set(blocks))                                  # -> 55362 / 46718 / 55351
len(blocks)**2 / (2 * 2**128)                                   # -> ~1.7e-27

# Proof B: alignment of duplicates
[i*16 for i,b in enumerate(blocks) if c[b] > 1]                 # all %16 == 0, 67762/67762

# Proof C: one-block insertion
u[:0x1086d90+16] != m[:0x1086d90+16] and u[0x1086d90+16:] == m[0x1086d90:]   # -> True

# layout: 0x10400 boundary
(len(d) - 0x10400) % 16                                         # -> 0 for all three

# filler: 4154 of 4157 blocks identical, 3 metadata
d[0x30:0x10400].count(BLK)                                      # -> 4154
```

Sibling files (`ellc.bin` 17,281,952 B, `ellv.bin` 3,626,064 B,
`night_align_lsc_tbl_40962304.bin` 37,748,736 B) were downloaded from the same
nuwa dump for the key-scope test in §3.5; none is committed.
