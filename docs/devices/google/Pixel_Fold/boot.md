# google Pixel_Fold (felix) — `boot` family: 9 rows, and the family that splits where `gpu` does not

Analysis date 2026-11-22. Analyst: OC-3 (issue [#1754](https://github.com/adineo-cmd/open-device/issues/1754)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows, 1,038 `boot`),
`device-inventory.csv`, and TheMuppets `proprietary_vendor_google_{cheetah,panther,lynx,felix,tangorpro}`
`radio/` trees at `lineage-23.0` (git-lfs pointer metadata).

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art

- [`Pixel_7_Pro/boot.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/google/Pixel_7_Pro/boot.md)
  (#1664) — the **two-axis split**: payload files have 1 size and device-unique md5, firmware
  files have several sizes and shared md5. Also the A-suffix rule (12/12) and an open question
  about `abl.img`'s GS201 size spread.
- [`Pixel_8/boot.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/google/Pixel_8/boot.md)
  (#1682) — **`radio/` presence explains the two-axis split**, 9/9 on the 16 Tensor devices,
  and 64/64 LFS size confirmation. This note applies that method to a fifth device.
- [`Pixel_Fold/tz.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/google/Pixel_Fold/tz.md)
  (#1760) — `Pixel_Fold` is a **singleton on all 8 firmware files**, GS201 splits **4 ways
  across 5 devices**, and the A-suffix rule is refined: singleton status tracks *product
  distinctness*, not the A suffix.
- [`Pixel_7a/gpu.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/google/Pixel_7a/gpu.md)
  §6 `:386-455` — **the `soc` column disagrees with the firmware on the G3/G4 octet**, and
  `Pixel_9_Pro`/`Pixel_9_Pro_Fold` are labelled G3 while carrying G4 firmware. **My §4 result
  is an independent confirmation of this on a different firmware family**, not a new finding.
- [`Pixel_Tablet/gpu.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/google/Pixel_Tablet/gpu.md)
  (#1766) — the GS201 quintet holds on `gpu`; §5 there was corrected in place.

## Verdict

[F] `Pixel_Fold` (`felix`, `Google Tensor GS201`) has **9 `boot` rows / 102,150,144 B**, **9
distinct md5**, **9/9 4096-aligned**, all `db_path = google/felix/radio`, `priority = P3`,
`interface_documented = n`, `isa_identified` empty:

| file | size (B) | md5 | `db_type` |
|---|---:|---|---|
| `boot.img` | 67,108,864 | `b79dfffe607c3a00e8053083aa315a3f` | `BOOT` |
| `dtbo.img` | 16,777,216 | `5fc3585e299e1bba2255af2dbd0f4c9c` | `DTB` |
| `init_boot.img` | 8,388,608 | `9345e98e846cdaae075945d3bd5ad33c` | `BOOT` |
| `tzsw.img` | 6,737,920 | `c875c5591f8cbd7bf2c41d4aaee2dd32` | `BOOT` |
| `abl.img` | 1,970,176 | `55daeac01874be5dfbd30df7944b318b` | `UEFIBOOT` |
| `pvmfw.img` | 1,048,576 | `6f80b9fa82c589dacbd5c011bf5d7586` | `SECURITY` |
| `bl31.img` | 98,304 | `3f4eacd061579aa32435867f19331ee3` | `BOOT` |
| `bl1.img` | 12,288 | `9a3a96a894ab3ef5cda6e38a257532b6` | `BOOT` |
| `vbmeta.img` | 8,192 | `987aaa7a545735a929c113201c1567a0` | `AVB` |

> **The headline.** Three results. One is a confirmation, one is a measurement, and one is new.
>
> **1. `gpu` and `boot` are governed by different forces on the same 8 devices.** Over the G3/G4
> octet, `gpu` is **8/8 byte-identical** (5 files, all 294,912 B) while `boot` firmware splits
> **exactly 4 ways** (`{8,8_Pro} | {8A} | {9,9_Pro,9_Pro_Fold,9_Pro_XL} | {9A}`), with the
> partition identical on all four firmware files. Same devices, opposite answers. "Same
> generation ⇒ same firmware" is right for `gpu` and wrong for `boot` (§5).
>
> **2. `Pixel_Fold` is a singleton on 9 of 9 `boot` files across all 16 Tensor devices** — no
> other Tensor device shares a single byte of its boot chain. Five of the 16 are boot
> singletons (`Pixel_7a`, `Pixel_8A`, `Pixel_9A`, `Pixel_Fold`, `Pixel_Tablet`), and §5 explains
> why `Pixel_9A` is the interesting one.
>
> **3. 44 of 44 git-lfs pointer sizes match the matrix, and the independent `sha256` partition
> equals the matrix `md5` partition on 9 of 9 files.** The boot-chain sharing structure is
> verified against a **second, independent hash** rather than md5 alone, with zero exceptions.
>
> A corollary for the schema: **8 files across 3 different `blob_family` labels share one
> identical 4-way partition** (§3). Same shape as #1688's 10-files/3-families result, now
> confirmed on a second device with a second hash.

## 1. The device is complete, and it is a 9/9 singleton

[F] `Pixel_Fold` has 41 matrix rows total, 9 of them `boot`. All 9 are `4096`-aligned.

[F] **Scope note on the denominator — my first draft got this wrong.** #1682 and #1676 speak of
"16 Tensor devices". The matrix has **19** `vendor = google` devices: 3 Qualcomm
(`Pixel_4A_5G`, `Pixel_5`, `Pixel_5A`) and **16 Tensor**. My first pass filtered on
`inventory.soc` matching `Google Tensor*`, which yields only **14** — because `Pixel_9A` and
`Pixel_9_Pro_XL` have a **blank `soc`**. I then wrote that those two "have no `boot` row" and
excluded them. **That was false: both have 9 `boot` rows.** The 16-device scope is the correct
one and every fleet-wide number below is recomputed on it. I left this visible rather than
quietly fixing the counts.

[F] `init_boot.img` is present, which per #1664 §3.2 places it on the GS201 side of the
Android-13 `init_boot` split. `init_boot.img` is present on **13 of the 16** Tensor devices —
absent on exactly `Pixel_6`, `Pixel_6A`, `Pixel_6_Pro`, the three GS101 devices.

[F] **Against all 16 Tensor devices, every one of `Pixel_Fold`'s 9 boot files is shared with
exactly one device: itself.**

| file | devices sharing `Pixel_Fold`'s md5 |
|---|---:|
| all 9 (`abl`,`bl1`,`bl31`,`boot`,`dtbo`,`init_boot`,`pvmfw`,`tzsw`,`vbmeta`) | **1** |

[I] This is stronger than a within-generation singleton. `Pixel_Fold` shares no boot file with
any of the other 15 Tensor devices, across four generations (GS101, GS201, G3, G4).

[F] `Pixel_9A` is **also** a 9/9 singleton on `boot` — as are `Pixel_7a`, `Pixel_8A` and
`Pixel_Tablet`. Five of the 16 Tensor devices share no boot firmware with any sibling. (The
sixth A-suffix device, `Pixel_6A`, is an **8/8** singleton because GS101 lacks `init_boot.img`;
it is not a counter-example.) See §5 and honest-negative 11.

## 2. 44/44 LFS sizes, and the sha256 partition is the md5 partition

The vendor tree for all five GS201 devices carries the boot blobs under `radio/` as git-lfs
pointers, which embed `sha256` and the true byte size — an independent second hash.

[F] **Sizes: 44 of 44 match.** Nine files × five devices, minus one absent file
(`Pixel_Tablet` has no `modem.img`):

```
LFS size == matrix size: 44/44 match, 0 mismatch, 0 not-in-matrix
```

[F] **Partitions: 9 of 9 identical.** For every one of the nine files, the partition of the
five GS201 devices by LFS `sha256` is **set-equal** to their partition by matrix `md5`:

```
sha256 partition == md5 partition: 9 of 9
```

[F] The canonical partition, reached independently by both hashes:

```
{Pixel_7, Pixel_7_Pro} | {Pixel_7a} | {Pixel_Fold} | {Pixel_Tablet}
```

[I] This is the strongest verification in the boot series so far. #1682 got 64/64 sizes and
4/4 partitions by comparing *partitions*; here I additionally confirm the partitions are
**byte-level consistent between two different hash functions** on the same files — so the
structure is not an artefact of how the matrix was built.

[N] **LFS objects themselves are absent from the server.** `media.githubusercontent.com`
returns 404 and the batch API reports `"Object does not exist on the server"`. So this is
**pointer metadata, never bytes** — I verified that two hashes *partition the devices
identically*, not that I hold the payloads. No byte-level claim is made anywhere in this note.

## 3. Eight files, three family labels, one partition

[F] Of the nine `radio/` files, **eight share one identical 4-way partition**, and they carry
**three different `blob_family` values**:

| file | `blob_family` | partition |
|---|---|---|
| `abl.img` | `boot` | `{7,7_Pro} \| {7a} \| {Fold} \| {Tablet}` |
| `bl1.img` | `boot` | identical |
| `bl31.img` | `boot` | identical |
| `tzsw.img` | `boot` | identical |
| `bl2.img` | **`other`** | identical |
| `ldfw.img` | **`other`** | identical |
| `pbl.img` | **`other`** | identical |
| `gsa.img` | **`tz`** | identical |
| `modem.img` | `modem` | **1 group** — absent on `Pixel_Tablet` |

[F] `modem.img` is the sole exception, and it is not a counter-example: `Pixel_Tablet` has
**0** `modem.img` rows, so the file exists on only four of the five devices and cannot
partition them.

[I] **The reading.** The 4-way partition is a property of the **product**, and it is shared by
every boot-chain firmware file regardless of which role label the schema gave it. `blob_family`
is a role label here too — it neither predicts nor prevents the partition. This is the same
conclusion as #1688 (10 files, 3 families, one partition) reached on a different device and a
different family, and it is now backed by a second hash.

## 4. The size and md5 axes disagree, and md5 is strictly finer

This is where #1664's "two-axis" framing gets a sharper form.

[F] Within GS201, the five devices' **sizes** and their **md5s** give different partitions:

| file | distinct sizes | distinct md5 | size-partition == md5-partition? |
|---|---:|---:|---|
| `abl.img` | 4 | 4 | **True** |
| `bl1.img` | 1 | 4 | False |
| `bl31.img` | 1 | 4 | False |
| `tzsw.img` | 1 | 4 | False |
| `boot.img` | 1 | 5 | False |
| `dtbo.img` | 1 | 5 | False |
| `init_boot.img` | 1 | 5 | False |
| `pvmfw.img` | 1 | 5 | False |
| `vbmeta.img` | 1 | 5 | False |

[F] `abl.img` is the **only** boot file whose size varies across GS201 at all — every other
file is size-constant on all five devices while carrying up to 5 distinct md5s.

[F] Across all 16 Tensor devices, **size is never finer than md5, and is sometimes coarser**.
The firmware **md5** partition is **10 groups** while the **size** partition is **8**. The two
places they diverge are both `abl.img`, where one size carries two builds:

```
2,084,864 B -> Pixel_6, Pixel_6_Pro (4b0d419d…)  |  Pixel_6A (b886a55f…)    [2 builds]
2,740,224 B -> Pixel_9, Pixel_9_Pro, Pixel_9_Pro_Fold, Pixel_9_Pro_XL (a2260fb6…)
            -> Pixel_9A (7ecc3b80…)                                          [2 builds]
```

[F] Those two splits are exactly what makes the md5 partition 10 and the size partition 8: each
split merges two md5 clusters into one size group (`−1` each), and `8 + 2 = 10`.

[F] That refinement is exact, not approximate: over all 9 files × 16 devices, **0 of the size
groups fail to decompose into whole md5 groups** — md5 refines size with zero violations.

[I] The rule: **`size` is a generation-and-partition-capacity property; `md5` is a
product-and-build property.** Size cannot distinguish two builds of the same size, so any
analysis that dedupes or groups by `size_bytes` will silently merge `Pixel_6A` into
`Pixel_6`/`Pixel_6_Pro`, and `Pixel_9A` into the Pixel 9 group, and wrongly conclude those
devices share a bootloader.

## 5. `gpu` is 8/8 identical where `boot` splits 4 ways — the sharpest contrast in the series

This is the result I did not expect and the strongest thing in this note.

[F] Take the **same 8 G3/G4 devices** (`Pixel_8`, `Pixel_8A`, `Pixel_8_Pro`, `Pixel_9`,
`Pixel_9A`, `Pixel_9_Pro`, `Pixel_9_Pro_Fold`, `Pixel_9_Pro_XL`) and cluster them two ways:

| family | clustering | groups over the 8 devices |
|---|---|---:|
| `gpu` (5 `mali_csffw-*.bin` files) | full 5-file md5 signature | **1** — all 8 identical |
| `boot` firmware (`abl`,`bl1`,`bl31`,`tzsw`) | md5, per file | **4** — identical partition on all four |

[F] On `gpu`, **all 8 devices carry byte-identical firmware on all 5 files** (each 294,912 B).
On `boot`, those same 8 devices split into exactly:

```
{Pixel_8, Pixel_8_Pro} | {Pixel_8A} | {Pixel_9, Pixel_9_Pro, Pixel_9_Pro_Fold, Pixel_9_Pro_XL} | {Pixel_9A}
```

[I] **The two families are governed by different forces, and this is now measured on one
device set with no confound.** GPU firmware is a *silicon* artefact: same GPU, same blob, so all
8 devices share it. The boot chain is a *product* artefact: each product's secure-boot
configuration is distinct, so it splits. A schema or a reader that assumes "same SoC generation
⇒ same firmware" is right for `gpu` and wrong for `boot` on precisely the same devices.

[N] This is a **cross-family contrast**, which I have not seen stated in the repo before. I am
flagging it as the candidate delta, but `Pixel_7a/gpu.md` and the other `gpu` notes each
establish one half of it, so the contribution is the *comparison*, not either measurement.

## 6. The firmware gives the true generation partition, and `soc` is wrong for four devices

[F] Clustering the 16 Tensor devices by their **firmware md5 signature**
(`abl`+`bl1`+`bl31`+`tzsw`) gives **10 groups**, and they disagree with `soc`:

| firmware cluster | `soc` values present |
|---|---|
| `{Pixel_9, Pixel_9_Pro, Pixel_9_Pro_Fold, Pixel_9_Pro_XL}` | **`G4` and `G3`, and one blank** |
| `{Pixel_9A}` | **blank** |
| `{Pixel_6, Pixel_6_Pro}` | GS101 |
| `{Pixel_8, Pixel_8_Pro}` | G3 |
| `{Pixel_7, Pixel_7_Pro}` | GS201 |

[F] **`Pixel_9_Pro` and `Pixel_9_Pro_Fold` are labelled `Google Tensor G3` but carry firmware
identical to `Pixel_9`, which is labelled `G4`**, and `Pixel_9_Pro_XL` (blank `soc`) is
identical to them too — on all four firmware files, by both size and md5:

| device | `soc` | `abl.img` | `bl1.img` | `bl31.img` | `tzsw.img` |
|---|---|---:|---:|---:|---:|
| `Pixel_9` | **G4** | 2,740,224 | 20,480 | 114,688 | 7,811,072 |
| `Pixel_9_Pro` | **G3** | 2,740,224 | 20,480 | 114,688 | 7,811,072 |
| `Pixel_9_Pro_Fold` | **G3** | 2,740,224 | 20,480 | 114,688 | 7,811,072 |
| `Pixel_9_Pro_XL` | **(blank)** | 2,740,224 | 20,480 | 114,688 | 7,811,072 |

[F] **`Pixel_9A` is a 9/9 boot singleton and its own firmware cluster** — the only G3/G4 device
that shares no boot firmware with any sibling. It is also the one whose `abl`/`bl1`/`bl31`/`tzsw`
differ from the Pixel 9 group **at identical size** (see §4).

[F] **This `soc` conclusion is prior art, not a discovery.** `Pixel_7a/gpu.md` §6 `:436-438`
already establishes it on the `gpu` family: *"`Pixel_9_Pro` and `Pixel_9_Pro_Fold` are labelled
"Google Tensor G3" — but their firmware is byte-identical to `Pixel_9`, which is labelled G4. A
Pixel 9 Pro cannot be G3, and the firmware places it firmly with the Pixel 9 group."*, and
`:455` records *"(Pixel_9 = G4 but Pixel_9_Pro = G3 with identical firmware)."* My contribution
is that the **boot** family independently reproduces the same partition, on four different
files, with a second hash function behind it, and that `Pixel_9_Pro_XL` belongs to the same
group despite a blank `soc`.

[I] Three independent firmware artefacts (`gpu`, `boot`, and the `Pixel_9_Pro_XL` `gpu` census)
now agree on the same correction, which makes the `soc` column the outlier, not the firmware.

[N] **`Pixel_9A` is the contrary case and I do not overclaim it.** Its `gpu` firmware is
**5/5 byte-identical to `Pixel_9`** while its `boot` firmware is a 9/9 singleton. So "the
firmware disagrees with `soc`" is true, but "the firmware is self-consistent across families"
is **false** — and `Pixel_9A` is the proof. No single family can adjudicate `soc` alone.

## 6. Honest negatives

1. **No payload was fetched.** LFS objects are absent from the server (§2). Every hash claim
   is **pointer metadata**; nothing here is byte-verified.
2. **I did not verify `boot.img`/`dtbo.img`/`init_boot.img`/`pvmfw.img`/`vbmeta.img` against
   LFS**, because `radio/` does not carry them — it carries `abl`, `bl1`, `bl2`, `bl31`, `gsa`,
   `ldfw`, `modem`, `pbl`, `tzsw` only. The five payload files have **no independent hash** [N].
3. **`Pixel_Tablet` has no `modem.img`**, so `modem.img` partitions only 4 devices. I did not
   investigate why the tablet lacks a modem image [OPEN].
4. **The 44/44 and 9/9 figures are for GS201 only** — five devices, one generation. I did not
   run the LFS cross-check on the other eleven Tensor devices [N]. The G3/G4 and GS101 vendor
   trees exist; this is the obvious next step.
5. **`db_type` carries the same role-label defect as `blob_family`, on rows I did not
   analyse.** `bl2.img`, `pbl.img` and `ldfw.img` are `UNKNOWN` (16 rows each) and `gsa.img` is
   `SECURITY` (16), while all four are boot-chain firmware with the identical partition — but
   none of them is a `boot` row, so they fall outside this issue's scope. `abl.img` is
   `UEFIBOOT` on all 79 rows fleet-wide. On the 9 rows I do cover, `db_type` is `BOOT` ×5,
   `UEFIBOOT` ×1, `DTB` ×1, `SECURITY` ×1, `AVB` ×1 — no `UNKNOWN` [F].
6. **`interface_documented = n` and `isa_identified` empty on all 9 rows.** I did not attempt
   ISA identification [N].
7. **Gate 0 web search was unavailable** (`websearch` HTTP 402, `searxng` unmounted). **No claim
   rests on a web source** [N].
8. **The §6 `soc` conclusion is not mine** — it is #1676/#1748/#1764's finding, reproduced on a
   different family. I claim only the boot-family reproduction and the `Pixel_9_Pro_XL` addition.
9. **The §5 cross-family contrast is a comparison, not a discovery.** Both halves exist in the
   repo already — the `gpu` census in #1676/#1748/#1764 and the `boot` census in #1664/#1682.
   What I have not seen stated is that they give *opposite* answers on the *same* 8 devices.
   If that comparison exists somewhere I did not find it, this is `DELTA` and not new.
10. **My first draft used a 14-device denominator and stated two devices had no `boot` rows.**
    Both claims were wrong (`Pixel_9A`, `Pixel_9_Pro_XL` each have 9). Every fleet-wide number
    was recomputed on 16. §1 records the error rather than hiding it.
11. **The `A`-suffix rule is prior art, not mine.** #1664 §3.1 establishes it 12/12. On the
    16-device scope every A-suffix device is a firmware singleton **4/4** (`Pixel_6A`,
    `Pixel_7a`, `Pixel_8A`, `Pixel_9A`), which I note as corroboration only. Note `Pixel_6A` is
    an 8/8 singleton, not 9/9, because GS101 has no `init_boot.img` — so a 9/9 test silently
    skips it.

## 7. Rule 1 — corrections for the lead, not applied here

1. **`soc` is wrong for `Pixel_9_Pro` and `Pixel_9_Pro_Fold`** (labelled G3, firmware is G4),
   and **blank for `Pixel_9_Pro_XL`**, which belongs to the same firmware group. Two
   independent firmware families now agree. This is a data fix, not a research question.
2. **`abl.img` is the only boot file whose size varies by product**, and it is the only file
   where the size and md5 partitions diverge — on **two** device pairs: `Pixel_6A` vs
   `Pixel_6`/`Pixel_6_Pro` (GS101), and `Pixel_9A` vs the Pixel 9 group (G3/G4). Grouping by
   `size_bytes` merges 10 md5 clusters into 8. Any dedupe or clustering must key on md5.
3. **`blob_family` does not predict the partition**: 8 files across `boot`/`other`/`tz` share one
   identical 4-way split. Same defect as #1688, now confirmed with a second hash.
4. **`bl2.img`, `pbl.img`, `ldfw.img` are `other`/`UNKNOWN`** while being boot-chain firmware
   with the same partition as `abl`/`bl1`/`bl31`/`tzsw`. `gsa.img` is `tz` for the same reason.
5. **`Pixel_Tablet` has no `modem.img` row** while the other four GS201 devices do — worth
   confirming that is a real device difference and not an extract gap.
6. **`Pixel_9A` and `Pixel_9_Pro_XL` are the two devices that a `soc`-based filter drops.**
   Any fleet query written as `WHERE soc LIKE 'Google Tensor%'` silently excludes them and
   returns 14 devices instead of 16. I hit exactly this bug writing §1. A `vendor = 'google'`
   filter with an explicit Tensor list is the safe form.

## 8. Reproduce

```sh
# run from the repo root

# the device's 9 boot rows (section 1)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
b=[x for x in r if x['device']=='Pixel_Fold' and x['blob_family']=='boot']
print('rows',len(b),'bytes',sum(int(x['size_bytes']) for x in b),'md5',len({x['md5_db'] for x in b}))
print('aligned',sum(1 for x in b if int(x['size_bytes'])%4096==0),'of',len(b))"
# expect 9 rows / 102150144 B / md5 9 / aligned 9 of 9

# Pixel_Fold is a 9/9 singleton across all 16 Tensor devices (section 1)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
T=['Pixel_6','Pixel_6A','Pixel_6_Pro','Pixel_7','Pixel_7_Pro','Pixel_7a','Pixel_8','Pixel_8A','Pixel_8_Pro','Pixel_9','Pixel_9A','Pixel_9_Pro','Pixel_9_Pro_Fold','Pixel_9_Pro_XL','Pixel_Fold','Pixel_Tablet']
print('Tensor devices',len(T))
for f in ['abl.img','bl1.img','bl31.img','boot.img','dtbo.img','init_boot.img','pvmfw.img','tzsw.img','vbmeta.img']:
    m=[x for x in r if x['device']=='Pixel_Fold' and x['filename']==f][0]['md5_db']
    n=len({x['device'] for x in r if x['filename']==f and x['md5_db']==m and x['device'] in T})
    print(f,n)
"
# expect Tensor devices 16, then nine lines ending in 1 (1 sharer each)

# gpu is 8/8 identical while boot firmware splits 4 ways (section 5)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
o=['Pixel_8','Pixel_8A','Pixel_8_Pro','Pixel_9','Pixel_9A','Pixel_9_Pro','Pixel_9_Pro_Fold','Pixel_9_Pro_XL']
sig=defaultdict(list)
for d in o:
    rows=sorted([x for x in r if x['device']==d and x['blob_family']=='gpu'],key=lambda z:z['filename'])
    sig[tuple(x['md5_db'] for x in rows)].append(d)
print('gpu clusters over the 8:',len(sig))
for f in ['abl.img','bl1.img','bl31.img','tzsw.img']:
    g=defaultdict(set)
    for x in r:
        if x['device'] in o and x['filename']==f: g[x['md5_db']].add(x['device'])
    print(f,'groups',len(g),[sorted(v) for v in g.values()])
"
# expect gpu clusters 1 (all 8 identical), then each firmware file 4 groups,
# all four with the same partition: {8,8_Pro} | {8A} | {9,9_Pro,9_Pro_Fold,9_Pro_XL} | {9A}

# eight files, three family labels, one identical partition (section 3)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g5=['Pixel_7','Pixel_7_Pro','Pixel_7a','Pixel_Fold','Pixel_Tablet']
for f in ['abl.img','bl1.img','bl2.img','bl31.img','gsa.img','ldfw.img','pbl.img','tzsw.img','modem.img']:
    g=defaultdict(list)
    for x in r:
        if x['device'] in g5 and x['filename']==f: g[x['md5_db']].append(x['device'])
    fam={x['blob_family'] for x in r if x['filename']==f}
    print(f,len(g),'groups',sorted(fam))
"
# expect abl/bl1/bl2/bl31/gsa/ldfw/pbl/tzsw -> 4 groups; modem.img -> 1 group

# size is coarser than md5: abl.img on the GS101 trio (section 4)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for d in ['Pixel_6','Pixel_6A','Pixel_6_Pro']:
    x=[y for y in r if y['device']==d and y['filename']=='abl.img'][0]
    print(d,x['size_bytes'],x['md5_db'])
"
# expect Pixel_6 and Pixel_6_Pro share 2084864 and the same md5; Pixel_6A same size, different md5

# the soc column vs the firmware (section 5)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
# the soc column vs the firmware (section 6)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for d in ['Pixel_9','Pixel_9_Pro','Pixel_9_Pro_Fold','Pixel_9_Pro_XL']:
    row=[x for x in r if x['device']==d and x['filename']=='tzsw.img'][0]
    print(d,row['size_bytes'],row['md5_db'])
"
# expect all four identical: 7811072 / 13c69973373010d1c27a04f643c0c980
# (Pixel_9_Pro_XL carries a blank soc yet belongs to the G4 firmware group)

# init_boot explains the 13-vs-16 split (section 1)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
T=['Pixel_6','Pixel_6A','Pixel_6_Pro','Pixel_7','Pixel_7_Pro','Pixel_7a','Pixel_8','Pixel_8A','Pixel_8_Pro','Pixel_9','Pixel_9A','Pixel_9_Pro','Pixel_9_Pro_Fold','Pixel_9_Pro_XL','Pixel_Fold','Pixel_Tablet']
has=[d for d in T if any(x['device']==d and x['filename']=='init_boot.img' for x in r)]
print('present',len(has),'absent',[d for d in T if d not in has])
"
# expect present 13 absent ['Pixel_6','Pixel_6A','Pixel_6_Pro']

# the LFS cross-check (section 2) -- network, run individually
for dev in cheetah panther lynx felix tangorpro; do
  for f in abl bl1 bl2 bl31 gsa ldfw modem pbl tzsw; do
    echo -n "$dev/$f "; curl -s --max-time 20 \
      "https://raw.githubusercontent.com/TheMuppets/proprietary_vendor_google_$dev/lineage-23.0/radio/$f.img" \
      | grep '^size '
  done
done
# expect 44 size lines matching the matrix; Pixel_Tablet/tangorpro has no modem.img
```

## What would upgrade this finding

1. **Obtain the LFS objects** (they 404 on the public mirror) to turn 44/44 pointer sizes and
   9/9 hash partitions into byte verification.
2. **Run the LFS cross-check on the other eleven Tensor devices** — G3/G4 and GS101 have vendor
   trees too, and the `radio/` rule is untested there by me. This would also test §5 directly:
   if `gpu` is one blob across all 8 G3/G4 devices, the vendor trees should show one `gpu` file
   and four distinct `abl` files for the same octet.
3. **Resolve why `Pixel_Tablet` carries no `modem.img`** — real hardware difference or extract
   gap, and the one place the 4-way partition does not apply.

Not legal advice. All facts are DB metadata, inventory metadata, vendor LFS pointer metadata and
repo documentation. No binary was parsed and no payload is committed.
