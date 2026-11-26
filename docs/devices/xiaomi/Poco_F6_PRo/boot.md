# xiaomi Poco_F6_PRo — `boot` family status (15 rows)

Analysis date: 2026-11-26. Analyst: OC-3 (issue [#1808](https://github.com/adineo-cmd/open-device/issues/1808)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows, `feat/open-device-site` @ `bd2f775`), `upstream-contribution/blob-database/device-inventory.csv` (249 rows). No payloads fetched — this checkout has no vendor tree and no LFS objects, so **every hash statement is metadata only**. `websearch` HTTP 402.

**Verdict: the `boot` family is PRESENT and complete — 15 rows, 345,812,992 B, 15 distinct md5, all `xiaomi/vermeer/radio`.** The set is exactly the **12-device common core** of the SM8550-class boot chain, and the corpus's larger boot sets are strict supersets of it, extended by exactly `cpucp_dtb.img` then `pvmfw.img` — a perfect nesting ladder with zero exceptions.

The headline is a negative-in-form but strong-in-content result: across the 6 devices carrying this identical 15-file set, **0 of 15 files share an md5, and all 15 device pairs share 0 of 15 files**. Composition is SoC-scoped; bytes are device-scoped. Seven filenames are *size-constant* across all six devices while carrying six distinct builds each — the sharpest demonstration in the corpus that `size_bytes` cannot proxy for a build.

## 1. Device identity

| fact | value | source |
|---|---|---|
| model key | `Poco_F6_PRo` (the DB's own spelling; the real product is "Poco F6 Pro") | `device-inventory.csv` [F] |
| vendor | `xiaomi` | inventory [F] |
| build codename | `vermeer` | inventory [F] |
| `soc` | **blank** | inventory [F] |
| `soc_source` | **blank** | inventory [F] |
| `in_builds_csv` | **`n`** | inventory [F] |
| matrix rows, whole device | 720 / 1,416,159,695 B | matrix [F] |
| `boot` rows | **15** / 345,812,992 B / 15 md5 | matrix [F] |

`in_builds_csv = n` is notable: this device's `soc` cell is blank *and* it was not sourced from `builds.csv`, so the blankness is a census gap rather than a build-metadata gap. `vermeer → SM8550` is a sibling-note mapping [I] (`research/cdsp-fleet/census.md:226`, `Mi_12/adsp.md:104`), never read from `soc`.

## 2. The 15 rows

All 15 sit under `xiaomi/vermeer/radio` — one `db_path`, no duplicates.

| filename | bytes | md5 | `db_type` |
|---|---:|---|---|
| `abl.img` | 233,472 | `20de114e8a86a1e02fabd7a6d39c1e33` | `UEFIBOOT` |
| `aop.img` | 282,624 | `494010363bee6ebdcd7a10742c6819ad` | `UNKNOWN` |
| `aop_config.img` | 16,384 | `ca30e6a339052f8137d55f723db9dffa` | `ELF64` |
| `boot.img` | 201,326,592 | `99baa98cc2914a5d48003d7c22055ee1` | `BOOT` |
| `cpucp.img` | 192,512 | `5640f7dca6e87fda003527eac37948b2` | `UNKNOWN` |
| `dtbo.img` | 25,165,824 | `24a863e3e09d998794ff59bc86ba611f` | `DTB` |
| `init_boot.img` | 8,388,608 | `461d976a8bf99bd6d5eb3b8b4c3ff464` | `BOOT` |
| `qupfw.img` | 57,344 | `1160174059ff44cc2a0213f73316a7b7` | `ELF64` |
| `recovery.img` | 104,857,600 | `7e08c5c41af67aeb15ce9a28cfc9b680` | `BOOT` |
| `shrm.img` | 65,536 | `b4dbe91e45e8f9ca5f819fc8e3b2a887` | `ELF64` |
| `uefi.img` | 2,945,024 | `74c29156877fdc68f66eef1f086eca9c` | `ELF64` |
| `vbmeta.img` | 8,192 | `f1e246560d918b0a6767c81399c7e8ea` | `AVB` |
| `xbl.img` | 1,200,128 | `a1cbafb99f10d5b0f08c19e106832f24` | `UEFIBOOT` |
| `xbl_config.img` | 188,416 | `bb72e7b23af015abd350e18e848cb854` | `ELF64` |
| `xbl_ramdump.img` | 884,736 | `4e4fcd1da0876a3dcd913d0c95f5e6cc` | `ELF64` |

Reproduce:

```bash
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
b=[x for x in r if x['device']=='Poco_F6_PRo' and x['blob_family']=='boot']
print(len(b), sum(int(x['size_bytes']) for x in b), len({x['md5_db'] for x in b}), len({x['db_path'] for x in b}))
"
```

→ `15 345812992 15 1`

## 3. The 15-set is the maximal common core of the SM8550-class boot chain

Exactly **6 devices** carry this precise 15-file set. But **12 devices' sets strictly contain it**, and the containment is *perfectly nested*:

| boot set | count | devices | extra files |
|---|---:|---|---|
| 15 files | 6 | `Mi_13`, `Mi_13_Pro`, `Nord_CE4`, `OnePlus_11_5G`, `Poco_F6_PRo`, `Redmi_K60_Pro` | — |
| 16 files | 4 | `FP6`, `Nord_4`, `OnePlus_12`, `Pad_Pro` | `+ cpucp_dtb.img` |
| 17 files | 2 | `OnePlus_13`, `Pad_2_Pro` | `+ cpucp_dtb.img`, `+ pvmfw.img` |

**Zero exceptions.** No device carries `pvmfw.img` without `cpucp_dtb.img`; no 15-file device carries either. The set-intersection of all 12 is **exactly** the 15 files — so this is the maximal common core, established by computation rather than by inspection:

```bash
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
b=[x for x in r if x['blob_family']=='boot']
dev=defaultdict(set)
for x in b: dev[x['device']].add(x['filename'])
tgt=dev['Poco_F6_PRo']
twelve=[d for d,s in dev.items() if tgt<=s]
print(len(twelve), len(set.intersection(*[dev[d] for d in twelve])), set.intersection(*[dev[d] for d in twelve])==tgt)
"
```

→ `12 15 True`

Per-file presence across the 12: the 15 core files are 12 of 12; `cpucp_dtb.img` is **6 of 12**; `pvmfw.img` is **2 of 12**.

`Poco_F6_PRo` is the 15-file shape, i.e. the core with **neither** optional file. The corpus's other 11 boot filenames never appear on any of the 12: `bl1.img`, `bl31.img`, `lk.img`, `rpm.img`, `tzsw.img`, `dtb.img`, `preloader_raw.img`, `unsparse_super_empty.img`, `xbl_cfg.elf`.

## 4. Headline: six builds, zero shared bytes, all 15 pairs disjoint

Across the 6 devices carrying the identical 15-file set, **0 of 15 files share an md5** — and this is not merely "no file is universal": **every one of the 15 device pairs shares 0 of 15 files**.

| | files |
|---|---:|
| one size across all 6, **6 distinct md5 each** | **7** |
| more than one size | 8 |

The 7 size-constant files:

| filename | size (all six) |
|---|---:|
| `aop_config.img` | 16,384 |
| `boot.img` | 201,326,592 |
| `dtbo.img` | 25,165,824 |
| `init_boot.img` | 8,388,608 |
| `qupfw.img` | 57,344 |
| `recovery.img` | 104,857,600 |
| `shrm.img` | 65,536 |

**All 7 carry 6 distinct md5s.** Size is exactly uninformative on this cohort: it is *constant* for 7 filenames while the bytes differ on every device. This is the #1790 "size hides builds" effect at its maximum — that note found 23 of 26 filenames hiding more than one build in a size bucket; here 7 of 15 filenames hide **six** builds in one bucket.

`xbl.img` is the opposite extreme: **3 sizes, 6 md5** across 6 devices.

Reproduce:

```bash
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
b=[x for x in r if x['blob_family']=='boot']
six=['Mi_13','Mi_13_Pro','Nord_CE4','OnePlus_11_5G','Poco_F6_PRo','Redmi_K60_Pro']
m=defaultdict(dict)
for x in b:
    if x['device'] in six: m[x['filename']][x['device']]=x['md5_db']
print(len(m), sum(1 for f in m if len(set(m[f].values()))==1))
print(sum(1 for f in m if len({m[f][d] for d in six if d in m[f]})==6 and len({int(x['size_bytes']) for x in b if x['filename']==f and x['device'] in six})==1))
"
```

→ `15 0` then `7`

### 4.1 The six devices are six different OEM codenames on one SoC class

| device | codename | `soc` cell |
|---|---|---|
| `Mi_13` | `fuxi` | blank |
| `Mi_13_Pro` | `nuwa` | blank |
| `Nord_CE4` | `benz` | blank |
| `OnePlus_11_5G` | `salami` | `Qualcomm SM8550 Snapdragon 8 Gen2` |
| `Poco_F6_PRo` | `vermeer` | blank |
| `Redmi_K60_Pro` | `socrates` | blank |

Three Xiaomi, two OnePlus, one Nothing; five of six `soc` cells blank. The SM8550 class is carried by the single populated cell plus sibling-note mapping [I] — never by `soc LIKE`, which would silently drop five of the six (the #1754 denominator lesson).

**Composition is SoC-scoped; content is device-scoped.** Six OEMs, one boot-chain shape, zero shared bytes.

## 5. Fleet-wide controls, re-derived

- **`md5 → size` is a function: 0 violations across 947 distinct md5.** No build appears at two sizes anywhere in the family. This is the strongest structural invariant in the `boot` family.
- **`size → md5` is not: 23 of 26 filenames have a size bucket holding more than one md5.** Only `lk.img`, `preloader_raw.img` and `xbl_cfg.elf` partition cleanly — and all three are 2-row or 1-row files, so the pass is vacuous.
- Worst `size → md5` offenders: `xbl.img` and `xbl_config.img` (13 each, across 21 sizes / 59 md5), `abl.img` (12), `aop.img` (11), `cpucp.img` (8).
- `boot.img`: **125 rows, 16 sizes, 122 md5**. Most common size is **100,663,296 B (53 rows)** — *not* this cohort's 201,326,592 B (21 rows).
- `vbmeta.img`: **115 rows, 3 sizes, 112 md5** — confirms the #1790 figure.
- Family totals: **1,038 rows / 123 devices / 26 filenames / 23 distinct boot-set shapes**.

### 5.1 MiB alignment: 4 of 15

`boot.img` (201,326,592 = 192 MiB), `dtbo.img` (24 MiB), `init_boot.img` (8 MiB) and `recovery.img` (100 MiB) are exact MiB multiples. The other 11 are not, and the residues are arbitrary (`xbl.img` 151,552; `uefi.img` 847,872; `shrm.img` 65,536). So MiB alignment is a property of the four Android **partition images**, not of the firmware payloads — consistent with #1466's finding that `size_bytes` is a mixed column.

## 6. The `a740_zap.mdt` dual-capture (a sub-finding, not `boot`)

`Poco_F6_PRo`'s `gpu` family has 5 rows for 4 filenames: **`a740_zap.mdt` is captured twice, at the same 4,044 B but with two different md5s**, from two paths:

```
4044  25a7c5dfd6fde308801706c39209445c  xiaomi/vermeer/odm/firmware
4044  b984b922f475884090a4282face58bee  xiaomi/vermeer/vendor/firmware
```

This is **not** a duplicate row — it is two genuinely different builds of the same file name at the same size. Fleet-wide, `a740_zap.mdt` is 14 rows / 10 devices, and the `odm`/`vendor` split is systematic:

| md5 | where |
|---|---|
| `25a7c5df…` | `odm/firmware` on `Mi_13`, `Mi_13_Pro`, `Poco_F6_PRo`, `Redmi_K60_Pro` (4 devices) |
| `b984b922…` | `vendor/firmware` on the **same 4 devices** |
| `e16ef6b4…` | `Nord_CE4` `vendor/firmware` only |
| `50d58541…` | `OnePlus_11_5G`, `OnePlus_12R` `vendor/firmware` |
| `878f26c1…` | `Edge_40_Pro` `modem/image` |
| `6ac52d8d…` / `c2c264ef…` | `Xperia_1_V` / `Xperia_5_V` |

The four Xiaomi SM8550 devices ship **the same pair** of `a740_zap.mdt` builds — one in `odm/`, one in `vendor/`. All 14 rows are exactly 4,044 B, so **size never distinguishes these seven builds**. This is a `gpu`-family observation recorded here because it surfaced in this device's row set; the `gpu` note for `Poco_F6_PRo` remains a separate deliverable.

## 7. `db_type` on this slice

`UEFIBOOT` ×2 (`abl.img`, `xbl.img`), `ELF64` ×6, `BOOT` ×3, `DTB` ×1, `AVB` ×1, **`UNKNOWN` ×2** (`aop.img`, `cpucp.img`).

The two `UNKNOWN`s are the two the prior art identifies as **32-bit RISC-V** (`EM_RISCV` 243) on the sibling QCM6490 platform (`research/qualcomm/docs/bootchain-census.md`). That is a citation about FP6, **not** a measurement of `vermeer`. The practical consequence stands regardless of ISA: a consumer filtering `db_type='ELF64'` recovers **6 of 15** files and silently loses both housekeeping images.

```bash
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
b=[x for x in r if x['device']=='Poco_F6_PRo' and x['blob_family']=='boot']
print(sum(1 for x in b if x['db_type']=='ELF64'), len(b))
"
```

→ `6 15`

## 8. Honest negatives

1. **No payload inspection whatsoever.** No vendor tree, no LFS objects (server 404 on `media.githubusercontent.com`). Every md5 above is a **DB column value**. `isa_identified` and `sha256_if_listed` are empty on **15/15** rows.
2. **The container grammar is cited, not measured.** `xbl.img` as multi-ELF, `shrm`/`aop`/`cpucp` as RISC-V, `qupfw` as Hexagon — all are `bootchain-census.md` findings on **QCM6490/FP6**. I did not open a `vermeer` image, so I cannot say whether `vermeer`'s `xbl.img` has the same 3-ELF structure. The 3 distinct `xbl.img` sizes here (1,200,128 / 1,208,320 / 1,232,896) are consistent with it and do not prove it.
3. **`dtbo.img` structure unverified for this device.** `research/fleet/boot-dtb.md` proves `dt_table` magic `0xd7b7ab1e` from real payloads; this device's `dtbo.img` is 25,165,824 B, the same size as the `instantnoodle` payload that note examined, but I did not compare bytes.
4. **SoC is inference.** `soc` blank, `in_builds_csv = n`; SM8550 comes from a sibling note [I]. `OnePlus_11_5G`'s populated cell corroborates the class but not this device.
5. **"0 of 15 shared" is a metadata statement.** It means no two of the six devices have the same `md5_db` for any boot filename. Whether the underlying bytes differ in every case cannot be checked here.
6. **`cpucp_dtb.img` / `pvmfw.img` semantics unknown.** I established their presence pattern exactly (6/12 and 2/12, nested) but not what distinguishes devices that carry them. `pvmfw.img` is an Android protected-VM firmware partition; why exactly 2 of 12 SM8550-class devices have it is not answered here.

## 9. Corrections for the lead (Rule 1 — not applied)

### 9.1 `a740_zap.mdt` is a 7-build filename at a single size, and 4 devices ship two of them

Recorded in §6. No existing note covers it; `research/fleet/gpu-bdwlan.md` and the `gpu` census notes do not mention the `odm/`+`vendor/` dual capture. Worth a line wherever `a740` is characterised, because **size cannot distinguish any of the 7 builds** (all 4,044 B) — a size-based dedupe would collapse them to one.

### 9.2 `size → md5` fails on 23 of 26 boot filenames, and the 3 passes are vacuous

`docs/devices/xiaomi/Poco_F5/boot.md` (#1790) records "23 of 26". Re-derived independently here and confirmed. The additional fact worth recording: the 3 filenames that *do* partition cleanly (`lk.img`, `preloader_raw.img`, `xbl_cfg.elf`) have **2, 2 and 2 rows** — so "3 of 26 pass" should not be read as evidence that size is ever a reliable build proxy. It is a small-sample artefact.

### 9.3 The boot-set nesting ladder is a corpus-wide structure, not a `Poco_F6_PRo` curiosity

The 15→16→17 nesting (§3) spans 12 devices and 3 OEMs. If `recon.md`'s `boot` section describes the family as a flat set of shapes (23 distinct shapes over 123 devices), it would be improved by noting that on the SM8550 class the shapes are **nested by construction** — the 15-set is a strict subset of the 16-set, which is a strict subset of the 17-set, with the two optional files being `cpucp_dtb.img` and `pvmfw.img`. I did not verify how `recon.md` currently words it.
