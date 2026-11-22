# xiaomi Poco_12C (earth) — `boot` family: two MTK devices, 13 shared filenames, 2 shared bytes

Analysis date 2026-11-22. Analyst: OC-3 (issue [#1772](https://github.com/adineo-cmd/open-device/issues/1772)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows),
`device-inventory.csv` (249 rows).

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art

MediaTek is the least-covered vendor in this lab, but it is not uncovered:

- [`research/mediatek/rosemary-census.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/mediatek/rosemary-census.md)
  — a full architecture census of **MT6785 (Helio G95)** on `Redmi_10S` (`rosemary`): the
  `mtk_hdr` record chain (magic `0x58881688`), the GFH preloader grammar per U-Boot
  `mtk_image.h` (`FILE_INFO`/`BL_INFO`/`BROM_CFG`/`ANTI_CLONE`/`BROM_SEC_CFG`), `lk` as
  **ARM32 Little Kernel** (first word `0xea000007`), `preloader_raw` load address `0x200F10`
  with `sig_type=5`, `tee → atf` as ARM Trusted Firmware, and the tinysys/CCU/HiFi3 core
  identifications.
- `upstream-contribution/blob-database/recon.md:219` — records that `lk.img`/`gz.img` carry
  "container labels" for rosemary, i.e. their ISA is **not** established there.

**So I am not going to re-derive MTK's container grammar.** It is documented, on a different
SoC, and nothing in this note depends on it. What is new is a *structural* result about this
device pair that the rosemary census could not see, because it studied one device.

## Verdict

`Poco_12C` (`earth`) has **5 `boot` rows / 77,455,360 B**, 5 distinct md5, **5/5
4096-aligned**:

| file | size (B) | md5 | `db_type` |
|---|---:|---|---|
| `boot.img` | 67,108,864 | `0cf9fa1024d737ec6a300bd9ce997cff` | `BOOT` |
| `dtbo.img` | 8,388,608 | `19ee51784aad46bec6d7a4690636427e` | `DTB` |
| `lk.img` | 1,642,496 | `0fd9e1ea13728597ff5d0d849de9578c` | `UNKNOWN` |
| `preloader_raw.img` | 311,296 | `9ab6f8569fe8447d2e9c3093de62bc0a` | `UNKNOWN` |
| `vbmeta.img` | 4,096 | `4a5d5d60c3afeef36546325d10c9b541` | `AVB` |

All `db_path = xiaomi/earth/radio`, `interface_documented = n`, `isa_identified` empty,
`priority = P3`, `sha256_if_listed` empty. `Poco_12C` has 18 matrix rows / 149,326,319 B in
total: `other` 9, `boot` 5, `wifi` 2, `modem` 1, `bt` 1.

> **The headline.** Only **two** devices in the whole 123-device fleet carry the MTK
> firmware set: `Poco_12C` and `Redmi_10S`. They share **13 filenames**, and of those
> **exactly 2 share bytes** — both `MT6631` FM-radio coefficients, a combo part common to
> both boards. **Every SoC-specific image differs**, and the reason is legible in the
> filenames: the connectivity firmware differs by one token, `1a_1` vs `2a_1`, a
> **chip-revision marker** rather than a device marker.

## 1. The MTK set exists on exactly two devices

[F] Only `Poco_12C` and `Redmi_10S` carry `lk.img`, `preloader_raw.img`, `gz.img`, `tee.img`,
`scp.img`, `sspm.img`, `spmfw.img` or `md1img.img`. Every one of those eight filenames has
exactly **2 rows** in the matrix, one per device.

| device | codename | rows | bytes |
|---|---|---:|---:|
| `Poco_12C` | `earth` | 18 | 149,326,319 |
| `Redmi_10S` | `rosemary` | 89 | 163,136,897 |

[F] `Poco_12C` has 18 rows and `Redmi_10S` has 89. They share **13 filenames**:

```
boot.img  dtbo.img  gz.img  lk.img  md1img.img  preloader_raw.img  scp.img
spmfw.img  sspm.img  tee.img  vbmeta.img  mt6631_fm_v1_coeff.bin  mt6631_fm_v1_patch.bin
```

[F] **Only 2 of the 13 share an md5** — and both are FM-radio coefficients for the same
combo chip:

| file | Poco_12C | Redmi_10S | same md5 |
|---|---:|---:|---|
| `boot.img` | 67,108,864 | 67,108,864 | **no** |
| `dtbo.img` | 8,388,608 | 8,388,608 | **no** |
| `lk.img` | 1,642,496 | 1,781,760 | **no** |
| `preloader_raw.img` | 311,296 | 348,160 | **no** |
| `vbmeta.img` | 4,096 | 8,192 | **no** |
| `gz.img` | 2,830,336 | 1,253,376 | **no** |
| `tee.img` | 2,560,000 | 2,560,000 | **no** |
| `scp.img` | 630,784 | 2,330,624 | **no** |
| `sspm.img` | 507,904 | 663,552 | **no** |
| `spmfw.img` | 53,248 | 16,384 | **no** |
| `md1img.img` | 63,746,048 | 60,178,432 | **no** |
| `mt6631_fm_v1_coeff.bin` | 1,092 | 1,092 | **YES** |
| `mt6631_fm_v1_patch.bin` | 1,028 | 1,028 | **YES** |

[F] The two shared files are byte-identical on both devices — **one md5 each across the pair**,
and each appears on **exactly these two devices and no others** in the fleet:

```
mt6631_fm_v1_coeff.bin  1092 B  8ed159e339b3363b6ad0edc3d1aa35f5   (2 rows, 1 md5)
mt6631_fm_v1_patch.bin  1028 B  7fee6d2d9dc4defc1f825e7edf1e0d19   (2 rows, 1 md5)
```

[I] `MT6631` is a MediaTek **connectivity combo** part (WiFi/BT/FM), and these two files are
its FM-radio calibration coefficients and patch. They are shared because the *combo chip* is
the same on both boards, even though the SoCs differ. So the sharing boundary here is **not
the SoC** — it is the peripheral. Every SoC-attached image differs; the one shared thing is
the one shared chip.

[F] `tee.img` is the sharpest case of the opposite: **identical size (2,560,000 B), different
md5** (`5cd356edde75…` vs `6da75e38ae44…`). Same slot, rebuilt content.

[I] This is the opposite of every Google result in this series, where firmware is shared
per-SoC and only payloads differ. These are two different MTK SoCs (`Poco_12C` is
MT6833-class, `Redmi_10S` is MT6785 per the rosemary census) and **no SoC-attached image is
shared** across that boundary — not even the parts that look generic.

## 2. `1a_1` vs `2a_1`: the filenames encode a chip revision

This is the part I did not expect, and it is the most reusable finding here.

[F] Both devices carry the **same five connectivity filenames**, differing only in one token:

| stem | `Poco_12C` | `Redmi_10S` | family |
|---|---|---|---|
| patch MCU | `soc1_0_patch_mcu_**1a_1**_hdr.bin` (25,934) | `soc1_0_patch_mcu_**2a_1**_hdr.bin` (22,350) | `other` |
| BT RAM | `soc1_0_ram_bt_**1a_1**_hdr.bin` (571,045) | `soc1_0_ram_bt_**2a_1**_hdr.bin` (570,949) | `bt` |
| MCU RAM | `soc1_0_ram_mcu_**1a_1**_hdr.bin` (105,656) | `soc1_0_ram_mcu_**2a_1**_hdr.bin` (122,712) | `other` |
| WiFi RAM | `soc1_0_ram_wifi_**1a_1**_hdr.bin` (197,596) | `soc1_0_ram_wifi_**2a_1**_hdr.bin` (196,764) | `wifi` |
| WiFi code | `WIFI_RAM_CODE_soc1_0_**1a_1**.bin` (640,288) | `WIFI_RAM_CODE_soc1_0_**2a_1**.bin` (636,700) | `wifi` |

[F] These are the **only 10 rows** in the entire matrix matching `soc1_0*` or
`WIFI_RAM_CODE_soc*`, and they are exactly 5 per device.

[I] The `soc1_0` prefix is MediaTek's connectivity-subsystem generation (`soc1_0` = the
MT66xx combo family). The `1a_1` / `2a_1` infix is a **hardware revision of that subsystem**,
not a device or product code — the two devices run different combo-chip revisions. The
`_hdr` suffix marks the image as carrying an `mtk_hdr` container header, which is why the
rosemary census could parse `lk` and `preloader_raw` through the same record chain.

[I] **Why this matters for the matrix.** `filename` is the only column that carries this
information, and it is free text. A consumer who normalises filenames (stripping version
tokens) would collapse these ten rows to five and wrongly conclude the two devices share
firmware. There is no `chip_revision` or `subsystem_generation` column to preserve what the
filename encodes.

### 2.1 The same connectivity firmware is split across three `blob_family` values

[F] The five files above are filed under **three different families on the same device**:

| file | `Poco_12C` family |
|---|---|
| `soc1_0_ram_bt_1a_1_hdr.bin` | **`bt`** |
| `soc1_0_ram_wifi_1a_1_hdr.bin` | **`wifi`** |
| `WIFI_RAM_CODE_soc1_0_1a_1.bin` | **`wifi`** |
| `soc1_0_patch_mcu_1a_1_hdr.bin` | **`other`** |
| `soc1_0_ram_mcu_1a_1_hdr.bin` | **`other`** |

[F] The assignment is **identical on both devices** (4/4 stems agree), so it is a deliberate
role-based split, not a per-device accident.

[I] This is a *correct* split — BT firmware under `bt`, WiFi under `wifi` — and it is worth
noting precisely because it contradicts the pattern in #1688, where ten files sharing one
partition carried three arbitrary family labels. Here the family follows function. The two
observations together say the same thing from opposite sides: **`blob_family` is a role
label, and it neither predicts nor prevents sharing.**

## 3. `vbmeta` is 4,096 here and 8,192 on the other MTK device

[F] `vbmeta.img` is **4,096 B** on `Poco_12C` and **8,192 B** on `Redmi_10S`. Both are exact
4096-multiples, so both are single AVB footer blocks — one is a 1-block image, the other
2-block.

[I] I flag this only to record that `vbmeta` size is **not** a constant across MTK devices, in
contrast to the Google family where #1664 found `vbmeta` at one size across 19 devices. The
MTK set has no such regularity, which is consistent with §1's finding that nothing is shared.

## 4. `soc` is blank, and that is consistent with the inventory

[F] `Poco_12C`'s matrix rows all carry `soc = ''`, and `device-inventory.csv` shows
`in_builds_csv = y` **with** `soc_source = ''`.

[N] That combination looks like a contradiction of the rule I established in #1748 ("`soc`
blank ⇔ `soc_source` blank", 248/249). It is not: the rule is about `soc_source`, not
`in_builds_csv`. **101 devices** have `in_builds_csv = y` with a blank `soc`, because the
`builds.csv` cell itself is empty. `Poco_12C` is one of them. The #1748 rule still holds at
248/249 with the single known exception (`Phone2`/`aura`, `soc_source = 'devices.sql.bz2'`),
re-verified here.

[I] So the blank `soc` is **not** a matrix defect for this device — it faithfully reflects an
empty upstream cell. But it does mean the MTK SoC for `Poco_12C` is **unrecorded anywhere in
the database**, and the only reason this note can say anything about its silicon is the
filename evidence in §2.

## 5. Honest negatives

1. **No binary was fetched or parsed.** This note is matrix-and-inventory metadata only. I did
   not verify `mtk_hdr` magic, the GFH chain, or any ISA claim for `Poco_12C`. The MTK
   container grammar in §2 is **cited from the rosemary census**, not measured here [N].
2. **I did not establish `Poco_12C`'s SoC.** The `soc` cell is blank and I did not resolve it.
   "MT6833-class" in §1 is inference from the `1a_1` token and the file set, **not** a
   verified fact, and I do not claim the chip identity [I].
3. **The `1a_1`/`2a_1` reading is inference.** I showed the token differs and that it is not a
   device code (both are `soc1_0`), but I did not find documentation that it means a hardware
   revision. The reading is consistent with MTK naming conventions, not confirmed by one [I].
4. **`sha256_if_listed` is empty on all 5 rows**, and there is no vendor tree for
   `xiaomi/earth` equivalent to TheMuppets, so **unlike the Google notes there is no second
   hash at all** — not even pointer metadata. Every statement here is single-source [N].
5. **Two devices is two devices.** The "no SoC-attached image is shared across the MTK SoC
   boundary" result rests on one pair. A third MTK device could share with either. **And my
   first draft of this note claimed "zero shared bytes"** — false: the two `mt6631_fm_v1_*`
   files are byte-identical. I had tabulated 11 of the 13 shared filenames and generalised
   from them without checking the other two. Corrected in §1; recorded rather than silently
   patched [I].
6. **`lk.img`/`gz.img` ISA is not established** (per `recon.md:219`) and I did not attempt it;
   their `db_type = UNKNOWN` is accurate, not a defect [N].
7. **The 76 files unique to `Redmi_10S`** (`audio_dsp`, the `aw8622` haptics configs, the
   `CFR_para_*` camera set) are not analysed — they reflect the different product, not the
   SoC, and are out of scope for a `boot` note [N].
8. **Gate 0 web search was not usable** for this device; **no claim rests on a web source** [N].
9. **No payload is committed**; no file was read.

## 6. Rule 1 — corrections for the lead, not applied here

1. **`filename` is the only carrier of chip-revision information**, and nothing preserves it
   (`.2`). `soc1_0_..._1a_1_hdr` vs `soc1_0_..._2a_1_hdr` is a hardware-revision distinction
   living in free text. A `chip_revision` or `subsystem_generation` column would make it
   queryable instead of regex-parsed.
2. **`blob_family` is a role label, not a sharing or provenance label** — restated from
   #1688/#1760 with a case where the split is *correct* (`.2.1`: `bt`/`wifi`/`other` by
   function). Worth fixing the documentation of the column rather than the data.
3. **MTK is represented by 2 devices.** `Poco_12C` (18 rows) and `Redmi_10S` (89 rows) are the
   entire MediaTek footprint of a 123-device matrix. `README.md:78` highlights the MTK
   findings while the matrix holds two devices — the gap between the research and the census
   is the largest in the lab.
4. **`Poco_12C`'s SoC is blank and unresolvable from the database.** The `builds.csv` cell is
   empty and no other column substitutes.
5. **`interface_documented = n` and `isa_identified` empty on all 5 rows**, while the rosemary
   census has already established the ISA for `lk`/`preloader_raw` on the sibling device.
   That knowledge exists in-repo and is not joined into the matrix.

## 7. Reproduce

```sh
# run from the repo root

# the 5 boot rows
python3 -I -c "
import csv
r=[x for x in csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv'))
   if x['device']=='Poco_12C' and x['blob_family']=='boot']
for x in sorted(r,key=lambda y:-int(y['size_bytes'])):
    print(f\"{x['filename']:20s} {int(x['size_bytes']):>10,} {x['md5_db']} {x['db_type']}\")
print('rows',len(r),'bytes',sum(int(x['size_bytes']) for x in r),
      'md5',len({x['md5_db'] for x in r}))"
# expect 5 rows / 77455360 B / 5 md5

# only two devices carry the MTK set (section 1)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for f in ['lk.img','preloader_raw.img','gz.img','tee.img','scp.img','sspm.img','spmfw.img','md1img.img']:
    xs=[x for x in r if x['filename']==f]
    print(f, len(xs), 'rows', sorted({x['device'] for x in xs}))"
# expect 2 rows each, both Poco_12C and Redmi_10S

# 13 shared filenames, only 2 shared md5 (section 1)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
a={x['filename']:x['md5_db'] for x in r if x['device']=='Poco_12C'}
b={x['filename']:x['md5_db'] for x in r if x['device']=='Redmi_10S'}
sh=set(a)&set(b)
print('shared filenames',len(sh))
print('shared md5',sum(1 for f in sh if a[f]==b[f]))
print('which:',sorted(f for f in sh if a[f]==b[f]))"
# expect 13 shared filenames, 2 shared md5 (the two mt6631_fm_v1 files)

# the 1a_1 / 2a_1 token (section 2)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
xs=[x for x in r if x['filename'].startswith('soc1_0') or x['filename'].startswith('WIFI_RAM_CODE_soc')]
print('rows',len(xs),'devices',sorted({x['device'] for x in xs}))
for x in sorted(xs,key=lambda y:(y['device'],y['filename'])):
    print(x['device'],x['filename'],x['size_bytes'],x['blob_family'])"
# expect 10 rows, 5 per device, 1a_1 vs 2a_1, and families bt/wifi/other

# the #1748 soc rule still holds (section 4)
python3 -I -c "
import csv
inv=list(csv.DictReader(open('upstream-contribution/blob-database/device-inventory.csv')))
bad=[x for x in inv if (x['soc'].strip()=='')!=(x['soc_source'].strip()=='')]
print('soc/soc_source violations:',len(bad),[x['model'] for x in bad])
print('in_builds_csv=y with blank soc:',sum(1 for x in inv if x['in_builds_csv']=='y' and not x['soc'].strip()))"
# expect 1 violation (Phone2) and 101
```

## What would upgrade this finding

1. **Fetch and parse `Poco_12C`'s `lk.img` and `preloader_raw.img`** against the rosemary
   census's grammar. That would establish the SoC and the ISA, and would tell us whether the
   `mtk_hdr` chain is stable across MTK generations — the census only has one.
2. **Find a third MTK device** to test whether anything at all is shared across the MTK set.
3. **Confirm what `1a_1`/`2a_1` denotes** from MTK documentation or a third device's filename.

Not legal advice. All facts are DB metadata and repo documentation. No binary was parsed and
no payload is committed.
