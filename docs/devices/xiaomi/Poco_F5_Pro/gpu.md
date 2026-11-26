# xiaomi Poco_F5_Pro — `gpu` family status (6 rows)

Analysis date: 2026-11-25. Analyst: OC-3 (issue [#1802](https://github.com/adineo-cmd/open-device/issues/1802)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows, `feat/open-device-site` @ `4d0e7d8`), `upstream-contribution/blob-database/device-inventory.csv` (249 rows). No payloads fetched — this checkout has no vendor tree and no LFS objects, so **every hash statement here is metadata only**. No `websearch` (HTTP 402).

**Verdict: the `gpu` family is PRESENT and coherent — 6 rows, 236,328 B, 6 distinct md5 — but the slice is not one GPU's firmware.** It is a **three-generation stack** (Adreno 660 + 662 + 730) that ships the `a660_sqe.fw` microcode in a *host-generation-specific* build. `Poco_F5_Pro` is one of exactly **9 devices** carrying this precise 6-file set, and that cohort turns out to be one of the most tightly-coupled groups in the whole corpus — **79 md5 clusters across 6 families** have a device set *exactly* equal to it.

## 1. Device identity

| fact | value | source |
|---|---|---|
| model key | `Poco_F5_Pro` | `device-inventory.csv` [F] |
| vendor | `xiaomi` | inventory [F] |
| build codename | `mondrian` | inventory [F] |
| `soc` | **blank** | inventory [F] |
| `soc_source` | **blank** | inventory [F] |
| `in_builds_csv` | `y` | inventory [F] |
| matrix rows, whole device | 821 / 1,309,085,295 B | matrix [F] |
| `gpu` rows | **6** / 236,328 B / 6 md5 | matrix [F] |
| `gpu` share of family | 6 of 781 rows = **0.77%** | matrix [F] |

Family context: `gpu` = **781 rows / 105 devices / 86 filenames / 303 md5**.

`soc` is blank, so the SoC cannot be read off the inventory. It is recoverable from `db_path` (`xiaomi/mondrian`) and from sibling notes — `Mi_12S/cdsp.md:59` classes `mondrian` as **SM8475** [I, that note's own reading]. This note never relies on the SoC label; every claim below is a filename/hash statement.

## 2. The 6 rows

| filename | bytes | md5 | `db_type` | `db_path` |
|---|---:|---|---|---|
| `a660_sqe.fw` | 43,068 | `6d13f9e90b8466a88edbb6fd710423d2` | `AUDIO` | `xiaomi/mondrian/vendor/firmware` |
| `a662_gmu.bin` | 55,888 | `17eb42a34811c5cb69e21c5a022d92e9` | `GPU` | `xiaomi/mondrian/vendor/firmware` |
| `a730_sqe.fw` | 74,676 | `0e6419525409a27110557297228aa80d` | `UNKNOWN` | `xiaomi/mondrian/vendor/firmware` |
| `a730_zap.mdt` | 3,564 | `51fb7578838815fab95393f01ce4874b` | `ELF64` | `xiaomi/mondrian/vendor/firmware` |
| `gmu_gen70000.bin` | 57,272 | `68a929d8ed6eba1bc9f20f605a19daa7` | `UNKNOWN` | `xiaomi/mondrian/vendor/firmware` |
| `sequence_manifest.bin` | 1,860 | `941df8acf2804cc0bb2e0db75135668e` | `UNKNOWN` | `xiaomi/mondrian/vendor/gpu/kbc` |

6 rows, 6 distinct md5 — no duplicate capture. Two `db_path` values; the manifest is the only row outside `vendor/firmware`.

Reproduce:

```bash
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g=[x for x in r if x['device']=='Poco_F5_Pro' and x['blob_family']=='gpu']
print(len(g), sum(int(x['size_bytes']) for x in g), len({x['md5_db'] for x in g}))
"
```

→ `6 236328 6`

## 3. Three Adreno generations in one 6-row slice

`a660` (Adreno 660) + `a662` (Adreno 662) + `a730` (Adreno 730). That is *not* a corpus defect — it is the vendor-partition-superset pattern already established at `research/soc/Qualcomm-SM8350-Snapdragon-888-gpu.md:95-144`, where `Xperia_5_III` carries a complete second GPU's matched set [F, prior art].

But the direction here is **inverted** relative to that prior art. In the Xperia case the strays were *older* parts; here `a730` is the **newest** name in the slice. So the naive reading "the extra names are leftovers" is wrong for this device.

### 3.1 The slice splits into one complete pair and one orphan

`a660_sqe.fw` and `a662_gmu.bin` are **different generations** — 660 SQE microcode next to 662 GMU firmware. There is no `a662_sqe.fw` and no `a660_gmu.bin` on this device. So the pairing is *cross-generation*, not matched.

`a730_sqe.fw` + `a730_zap.mdt` form the only same-generation *pair* (SQE + zap) in the slice, and `gmu_gen70000.bin` is the GMU slot for that generation — which is why **`a730_gmu.bin` has 0 rows fleet-wide**: the naming law switched to `gmu_gen*` at gen 7 (see §5, Rule 1).

## 4. The 9-device cohort, and why it is the real subject

`gmu_gen70000.bin` is carried by exactly **9 devices**, and those 9 are *set-identical* to #1790's 9-device `boot`-set cohort:

```
Mi_12, Mi_12S, Mi_12S_Pro, Mi_12S_Ultra, Mi_12T_Pro, Mi_12_Pro, Phone_2, Poco_F5, Poco_F5_Pro
```

On those 9, **5 of the 6 files are byte-identical** and only `a730_zap.mdt` varies:

| filename | sizes across the 9 | md5 across the 9 | |
|---|---:|---:|---|
| `a660_sqe.fw` | 1 | 1 | CONST |
| `a662_gmu.bin` | 1 | 1 | CONST |
| `a730_sqe.fw` | 1 | 1 | CONST |
| `gmu_gen70000.bin` | 1 | 1 | CONST |
| `sequence_manifest.bin` | 1 | 1 | CONST |
| `a730_zap.mdt` | **3** | **9** | vary |

Reproduce:

```bash
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g=[x for x in r if x['blob_family']=='gpu']
dev=defaultdict(dict)
for x in g: dev[x['device']][x['filename']]=(int(x['size_bytes']),x['md5_db'])
nine=sorted(d for d,f in dev.items() if 'gmu_gen70000.bin' in f)
print(len(nine))
for f in sorted(dev['Poco_F5_Pro']):
    print(f, len({dev[d][f][0] for d in nine}), len({dev[d][f][1] for d in nine}))
"
```

→ `9`, then five lines ending `1 1` and one `a730_zap.mdt 3 9`.

### 4.1 The `a730_zap.mdt` size ladder — the only per-device discriminator

| bytes | devices |
|---:|---|
| 3,264 | `Mi_12`, `Mi_12_Pro` |
| 3,564 | `Mi_12S`, `Mi_12S_Pro`, `Mi_12S_Ultra`, `Mi_12T_Pro`, **`Poco_F5_Pro`** |
| 4,044 | **`Poco_F5`**, `Phone_2` |

9 rows, 9 md5 — every device has its own zap build. `Poco_F5` and `Poco_F5_Pro` are **not in the same size class**.

`a730_zap.mdt` appears **only** as `.mdt` on these devices — no `b00`/`b01` segments are captured in this family, so the `mdt == b00 + b01` law is **untestable here**, not violated.

### 4.2 The cohort is one of the most tightly coupled groups in the corpus

Across the whole matrix, **79 md5 clusters in 6 families** have a device set *exactly* equal to those 9 devices:

| family | clusters == the nine | clusters ⊇ the nine | total clusters |
|---|---:|---:|---:|
| `tz` | 31 | 37 | 1,826 |
| `other` | 25 | 37 | 5,702 |
| `adsp` | 11 | 13 | 1,889 |
| `gpu` | 5 | 5 | 303 |
| `cdsp` | 4 | 5 | 576 |
| `modem` | 3 | 8 | 1,657 |

Reproduce:

```bash
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
nine={'Mi_12','Mi_12S','Mi_12S_Pro','Mi_12S_Ultra','Mi_12T_Pro','Mi_12_Pro','Phone_2','Poco_F5','Poco_F5_Pro'}
fam=defaultdict(lambda: defaultdict(set))
for x in r: fam[x['blob_family']][x['md5_db']].add(x['device'])
for f,m in sorted(fam.items()):
    e=sum(1 for v in m.values() if v==nine)
    if e: print(f,e,len(m))
"
```

This is independently corroborated: `Mi_12S/cdsp.md:59` already records the same 9-device set as the `cdsp.b01/b03/b09/b15` quartet's cluster [F, prior art]. My §4.2 extends that from one quartet to 79 clusters.

## 5. Four laws of Adreno GMU naming — all exact, zero violations

Scope: the **92 Adreno devices** in `gpu` (105 total − 13 Mali `Pixel_*` carrying only `mali_csffw-*`).

### Rule 1 — `a7xx_gmu.bin` never exists; the `_gmu.bin` naming stops at a662

0 rows for `a7\d\d_gmu.bin`. The generations that ever use `_gmu.bin` are **{618, 619, 630, 640, 650, 660, 662}** — dead stop at 662. Every 7xx/8xx part uses `gmu_gen*` instead: `gmu_gen70000.bin`, `gmu_gen70200.bin`, `gmu_gen70900.bin`, `gmu_gen70e00.bin`.

This is the resolution of the apparent "missing `a730_gmu.bin`": it is **not a gap**, it is the naming law.

### Rule 2 — `gmu_gen*` ⇔ (no `aNNN_*` file) OR (max `aNNN` ≥ 730)

**92/92 devices, 0 violations.**

```bash
python3 -I -c "
import csv,re
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g=[x for x in r if x['blob_family']=='gpu']
dev=defaultdict(set)
for x in g: dev[x['device']].add(x['filename'])
hi={d:max([int(m.group(1)) for n in f for m in [re.match(r'a(\d{3})_',n)] if m], default=None) for d,f in dev.items()}
gen={d for d,f in dev.items() if any(n.startswith('gmu_gen') for n in f)}
adreno={d for d in dev if hi[d] is not None or d in gen}
print(len(adreno), sum(1 for d in adreno if (d in gen)!=(hi[d] is None or hi[d]>=730)))
"
```

→ `92 0`

### Rule 3 — exactly 9 devices carry *both* naming styles, and all 9 have max generation 730

The overlap is the §4 cohort. **No** device with max gen ≤ 699 carries `gmu_gen*` (0 of 58).

### Rule 4 — the `AUDIO` band is generation-bounded, a contiguous 650/660 pair

| generation | `_gmu.bin`/`_sqe.fw` rows | `db_type` |
|---|---:|---|
| a618 | 2 | `GPU` |
| a619 | 24 | `GPU` |
| a630 | 59 | `GPU` |
| a640 | 7 | `GPU` |
| **a650** | **28** | **`AUDIO`** |
| **a660** | **51** | **`AUDIO`** |
| a662 | 9 | `GPU` |

The `AUDIO` mislabel itself is **prior art** (`research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-soc.md:643-665`, `research/drivers/audio.md:41`) and is not claimed. What that prior art does *not* state is the **band shape**: it reads the defect as tracking "the generation" of the filename (`SM4375-soc.md:665`). The data says otherwise — `a662_gmu.bin`, the *newest* `_gmu.bin`, is correctly `GPU`, and `a618`–`a640` are all correctly `GPU`. The defect is a **contiguous two-generation band {650, 660}**, not an age trend, and it stops dead at 662.

## 6. `a660_sqe.fw` — the two builds are a generation split, not nightly drift

`a660_sqe.fw` has exactly 2 builds fleet-wide across 30 devices:

| bytes | md5 | devices | max `aNNN` on those devices |
|---:|---|---:|---|
| 40,496 | `08b7662ccd6815333aed6bce9bd69bd7` | 21 | **660** (all 21) |
| 43,068 | `6d13f9e90b8466a88edbb6fd710423d2` | 9 | **730** (all 9) |

**The law: `a660_sqe.fw @ 43,068 B` ⇔ the device's max Adreno name is 730. 30/30, 0 violations.**

```bash
python3 -I -c "
import csv,re
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g=[x for x in r if x['blob_family']=='gpu']
dev=defaultdict(set)
for x in g: dev[x['device']].add(x['filename'])
hi={d:max([int(m.group(1)) for n in f for m in [re.match(r'a(\d{3})_',n)] if m], default=None) for d,f in dev.items()}
xs={x['device']:int(x['size_bytes']) for x in g if x['filename']=='a660_sqe.fw'}
print(len(xs), sum(1 for d in xs if (xs[d]==43068)!=(hi[d]==730)))
"
```

→ `30 0`

### 6.1 This contradicts the recorded "nightly drift" explanation

Two prior-art notes attribute the 40,496 → 43,068 difference to **nightly drift**:

- `research/drivers/audio.md:64` — "The `a660_sqe.fw` size drift 40,496 → 43,068 B **across nightlies** is the same drift already recorded in `research/laptop/fragmentation-half.md` line 154"
- `research/laptop/fragmentation-half.md:154` — "`a660_sqe.fw` … 2 [md5 clusters] … (size drifted 40,496 → 43,068 B **between nightlies**)"

Nightly drift predicts the two builds should be **interleaved** across devices of the same generation. They are not: the split is **perfectly** by host generation. If size were independent of generation, the chance that all 9 a730-class devices land in one bucket is `2 / C(30,9)` = `2/14,307,150` ≈ **1 in 7.2 million**.

A decisive control is in the same slice: **`a660_gmu.bin` has 3 sizes** (53,672 ×1, 55,252 ×1, 55,256 ×19) and **all 21 of its devices have max gen 660** — i.e. the *genuine* drift file drifts *within* one generation, exactly as "nightly drift" predicts. The SQE file does not. So the corpus contains both patterns, and only the GMU one is drift.

**Reading [I]:** the 43,068 B build is the a660-compatible SQE microcode **as packaged for a gen-7 host** — a co-resident build for devices whose live GPU is a730. It is not a newer nightly of the same artifact, because a newer nightly would appear on gen-660 devices too, and it appears on none of them.

### 6.2 The two populations are disjoint and differ structurally

| | 21-device population | 9-device population |
|---|---|---|
| `a660_sqe.fw` | 40,496 | 43,068 |
| `a660_gmu.bin` | **present** (21/21) | **absent** (0/9) |
| `a662_gmu.bin` | absent | **present** (9/9) |
| `a730_sqe.fw` | absent (0/21) | **present** (9/9) |

Reproduce:

```bash
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g=[x for x in r if x['blob_family']=='gpu']
dev=defaultdict(set)
for x in g: dev[x['device']].add(x['filename'])
a=('a660_sqe.fw','a660_gmu.bin')
print(sum(1 for d in dev if all(f in dev[d] for f in a)))
print(sum(1 for d in dev if 'a660_sqe.fw' in dev[d] and 'a660_gmu.bin' not in dev[d]))
"
```

→ `21` and `9`

So the 21 genuine Adreno-660 devices have a **complete matched pair** (`a660_sqe` + `a660_gmu`); the 9 have a **deliberately broken pair** (`a660_sqe` + `a662_gmu`, generations 660 and 662). A device whose live GPU were a660 would have no GMU firmware at all under the 9-device arrangement — which is only coherent if its live GPU is **not** a660.

**This is the strongest argument that `Poco_F5_Pro`'s live GPU is a730 and the a660/a662 names are the co-resident set, not the binding.** It is a structural argument from presence/absence, not a payload claim.

## 7. `sequence_manifest.bin` — 5 sizes, and the 1,860 B build is the cohort's

All 50 `sequence_manifest.bin` rows in the corpus are `gpu`-family and all sit under a `…/gpu/kbc` path — 0 outside.

| bytes | rows | md5 | devices |
|---:|---:|---:|---|
| **1,860** | 9 | 1 | **the §4 cohort** |
| 1,872 | 10 | 1 | `Edge_40_Pro`, `Mi_13`, `Mi_13_Pro`, `Nord_CE4`, `OnePlus_11_5G`, `OnePlus_12R`, `Poco_F6_PRo`, `Redmi_K60_Pro`, `Xperia_1_V`, `Xperia_5_V` |
| 2,280 | 3 | 1 | — |
| 2,692 | 3 | 1 | — |
| 5,704 | 25 | 1 | — |

The 1,860 B build is **exactly** the 9-device cohort, one md5. Note `Mi_13`/`Mi_13_Pro` sit in the 1,872 B group, *not* with the Mi_12 family — so this manifest does not track the Mi-numbering, it tracks the build cohort.

## 8. `db_type` is not a format classifier — three defects visible in 6 rows

| row | `db_type` | what the name says | correct? |
|---|---|---|---|
| `a660_sqe.fw` | `AUDIO` | GPU SQE microcode | **no** — prior art `SM4375-soc.md:643` |
| `a662_gmu.bin` | `GPU` | GPU GMU firmware | yes |
| `a730_sqe.fw` | `UNKNOWN` | GPU SQE microcode | **no** — should be GPU |
| `a730_zap.mdt` | `ELF64` | ELF container | yes |
| `gmu_gen70000.bin` | `UNKNOWN` | GPU GMU firmware | **no** — should be GPU |
| `sequence_manifest.bin` | `UNKNOWN` | GPU KBC manifest | undetermined |

**3 of 6 rows are mislabelled.** The `AUDIO` one is prior art; the two `UNKNOWN`s on `a730_sqe.fw` and `gmu_gen70000.bin` are **new** — every gen-7 Adreno row in this slice is typed `UNKNOWN`, so a consumer filtering `db_type = 'GPU'` recovers **1 of the 3** actual GPU microcode files on this device.

```bash
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g=[x for x in r if x['device']=='Poco_F5_Pro' and x['blob_family']=='gpu']
print(sum(1 for x in g if x['db_type']=='GPU'), len(g))
"
```

→ `1 6`

## 9. Honest negatives

1. **No payload inspection.** No vendor tree, no LFS objects (the server returns 404 for `media.githubusercontent.com`). Every md5 above is a **DB column value**, never a byte I hashed. `isa_identified` and `sha256_if_listed` are empty on **6/6** rows.
2. **SoC unknown from the inventory.** `soc` and `soc_source` are both blank. The SM8475 class comes from a sibling note's reading (`Mi_12S/cdsp.md:59`), marked [I]. I did not verify it externally (websearch HTTP 402).
3. **No `a730` GMU file to compare.** `a730_gmu.bin` has 0 rows, so Rule 1 is established by *absence*, not by inspecting a gen-7 GMU artifact under the legacy name.
4. **`mdt == b00 + b01` untestable.** `a730_zap.mdt` has no captured segments in this family.
5. **`sequence_manifest.bin` content unknown.** 5 sizes, all one md5 each, all under `gpu/kbc`; nothing here says what a KBC manifest contains.
6. **"Live GPU is a730" is inference, not proof.** §6.2's argument is presence/absence of the matched pair. A payload disassembly of `a730_sqe.fw` would settle it and is not possible here.

## 10. Corrections for the lead (Rule 1 — not applied)

### 10.1 `device-inventory.csv` has 4 duplicate `model` keys; 2 of them contradict themselves on `soc`

The inventory is 249 rows / **245 distinct `model`** values. Four models appear twice:

| model | rows | `soc` values | matrix rows joined |
|---|---:|---:|---:|
| `Phone_2` | 2 | **2** (`SDM845` / `SM8475`) | **654** |
| `Xperia_1_II` | 2 | **2** (`''` / `SM8250`) | 26 |
| `TX2_Tablet` | 2 | 1 (`''`) | 0 |
| `Redmi_Note_10_Pro` | 2 | 1 (`''`) | 0 |

`Phone_2` is the serious one. The two rows are:

```
vendor=''         codename='aura'  soc='Qualcomm SDM845 Snapdragon 845'
vendor='nothing'  codename='Pong'  soc='Qualcomm SM8475 Snapdragon 8+ Gen1'
```

These are **two different devices sharing a model string**: a Razer `aura` (SDM845) and a Nothing `Pong` (SM8475). The inventory separately carries `Phone2` / `razer` / `aura`, so `Phone_2`+`aura` is a near-duplicate of an existing row, while the 654 matrix rows for `Phone_2` are **100%** `nothing/Pong`.

**Consequence: any join on `model` that takes the first match assigns the wrong SoC to all 654 rows.** This is not hypothetical — the first row is the wrong one:

```bash
python3 -I -c "
import csv
from collections import defaultdict
inv=list(csv.DictReader(open('upstream-contribution/blob-database/device-inventory.csv')))
bym=defaultdict(list)
for x in inv: bym[x['model']].append(x)
print(bym['Phone_2'][0]['soc'])
print(bym['Phone_2'][1]['soc'])
"
```

→ `Qualcomm SDM845 Snapdragon 845`, then `Qualcomm SM8475 Snapdragon 8+ Gen1`.

**Recommended fix:** make `(model, build_codename)` the join key, not `model`. Every one of these 4 cases resolves cleanly on codename (matrix `db_path` codename matches exactly one inventory row: `Pong`→Pong, `pdx215`→pdx215). A first-match join on `model` is wrong for **680 matrix rows**.

Note this also means the "device key is `model`" convention in `device-inventory.csv` is **not sound** — it is only sound for 245 of 249 rows.

### 10.2 The `soc`/`soc_source` blankness invariant has a second exception

The recorded rule is "`soc` blank ⇔ `soc_source` blank, 248/249, exception `razer Phone2`/`aura`". Verified: the XOR count is still exactly **1** row — but that row is `Phone2` (`soc=''`, `soc_source='devices.sql.bz2'`), so the invariant and its exception stand. No correction needed; recorded here because #1802 touches it.

### 10.3 `a660_sqe.fw` "nightly drift" — §6.1 above

`research/drivers/audio.md:64` and `research/laptop/fragmentation-half.md:154` both explain the 40,496/43,068 split as nightly drift. It is a **generation split, 30/30 with 0 violations**, and the same note's own `a660_gmu.bin` 3-size case is the true drift control. Suggest rewording both to distinguish the two mechanisms.

### 10.4 `a730_sqe.fw` / `gmu_gen70000.bin` typed `UNKNOWN`

Every gen-7 Adreno microcode row in this slice is `UNKNOWN`. Suggest extending the existing `db_type`-mislabel note (`research/drivers/audio.md`) from the `AUDIO` band to the `UNKNOWN` gen-7 rows, since the consumer-facing consequence is the same: filtering on `GPU` loses them.
