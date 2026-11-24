# `fastchg` — a charging bucket that is 95% not charging (315 rows, 28 devices)

Analysis date: 2026-11-24. Analyst: OC-1 (`100milionseek`), issue
[#2055](https://github.com/adineo-cmd/open-device/issues/2055).

Inputs:
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows) for the
census; the payloads already on disk from earlier sessions — 43 files under
`…/second-device/instantnoodle/tree-odm/firmware/fastchg/` and 76 files under
`…/second-device/larry/tree-odm/firmware/tp/`; and the mainline `torvalds/linux`
sources for the two container formats that could plausibly be in scope. Every
number below is command output. No payload is committed; samples are ≤16 bytes
of hex.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** The `fastchg` subfamily is 315 rows, 28 devices, 40 filenames,
36,989,007 B — 2.10% of the `other` family's rows and 0.26% of its bytes, sixth
of thirteen `other` subfamilies by bytes and sixth by rows. That size is not what
makes it interesting. What makes it interesting is that **only 4.96% of its bytes
are fast-charge firmware.**

Measured by the directory the row actually lives in, the bucket is three
unrelated things:

| what the rows really are | rows | devices | bytes | share of bytes |
|---|---:|---:|---:|---:|
| charging firmware at `firmware/fastchg/` | 192 | 8 | 1,834,392 | 4.96% |
| **panel DDIC firmware at `firmware/tp/`** | **82** | **18** | **12,213,591** | **33.02%** |
| **flash-memory firmware at `firmware/ufs/`** | **31** | **6** | **22,683,484** | **61.32%** |
| battery-gauge firmware at `vendor/firmware/` | 10 | 5 | 257,540 | 0.70% |

The subfamily label contradicts `db_path` on **123 of 315 rows** — 39.05% — and
those 123 rows carry **95.04%** of the bytes. The pattern is not random: the
label was assigned from the *filename*, not the path, and the filenames involved
are shared with subfamilies where the same file is correctly filed. §4 gives the
mechanism, §5 the refutation.

The payoff is the **container**, which turns out to be one format wrapping six
different payload dialects. `FwUp` is an 80-byte header, a declared body, and a
128-byte trailer. It closes arithmetically on **80/80** files by a rule the
database does not know: `80 + size@0x0C + 128 == filesize`. The same wrapper
holds the real VOOC charger firmware, the panel DDIC blobs, and inside the
`_FAE` variant the body appears *bare* — `len(FW_*) − len(*_FAE) == 208 == 80 + 128`
on **36 of 37** pairs, so `_FAE` is the body with the wrapper stripped. The
one exception is a genuinely different build, and it is the informative case
(§6.3).

Two defects are recorded and not fixed, and one prior-art note is confirmed
correct rather than corrected.

---

## 0. Headline

1. **`[F]` The bucket is 95.04% not-fastchg by bytes.** 192 of 315 rows sit at
   `firmware/fastchg/` and hold 1,834,392 B. The remaining 123 rows sit at
   `firmware/tp/` (82), `firmware/ufs/` (31) and `vendor/firmware/` (10), and
   hold 35,154,615 B. See §3.
2. **`[F]` `firmware/ufs/` alone is 61.32% of the bucket.** 31 rows on 6 devices,
   22,683,484 B, all SAMSUNG / SKhynix / MICRON part numbers — UFS and eMMC
   *flash storage* firmware, filed under a charging subfamily. See §3.3.
3. **`[F]` The `FwUp` container closes on 80/80 files.** `80 + u32@0x0C + 128 ==
   len(file)`, no exceptions, across 43 VOOC payloads and 37 panel payloads. The
   header carries a **self-referential embedded path** at `0x14` whose basename
   matches the on-disk name or declares the rename. See §6.
4. **`[F]` `_FAE` is usually the bare body.** On **36 of 37** `FW_*` / `FW_*_FAE`
   pairs the size difference is **exactly 208 B = 80 + 128**, and the `_FAE`
   bytes are found verbatim inside the `FW_*` file starting at offset 80
   (`FW_S3910_TIANMA.img` case: `f in a → True`). So `_FAE` is normally not a
   different firmware build — it is the same build, unwrapped. The **one
   exception** (`21221/FW_FT3518_SAMSUNG.img`, Δ = 510 B, `_FAE` not contained
   in `FW_`) is a genuinely different build and proves the suffix does not
   *guarantee* identity. See §6.3.
5. **`[F]` The wrapper hides six body dialects.** 37 wrapped panel containers
   split **24 binary / 13 ASCII Intel HEX**; the 41 `LIMIT_*` files use a
   *different* container, `LIMITIMG`. `[F]` §7.
6. **`[F]` One panel IC family spans four subfamilies.** `S3910` appears in 85
   rows across `fastchg` (23), `touch` (25), `oled` (32), `misc` (5);
   `S3706` in 60 rows across `fastchg` (20), `oled` (20), `misc` (20). Not one
   filename is shared between them (`0 / 40`). See §5.
7. **`[F]` A vendor rename the database cannot see.** In all 20 `oplus_vooc_fw.bin`
   copies the embedded path reads **`oppo_vooc_fw.bin`** — `oplus` on disk,
   `oppo` inside. See §6.4.
8. **`[N]` No public spec for `FwUp`.** Not in `torvalds/linux`, not in web
   search, no datasheet. The format below is derived from bytes and arithmetic
   alone. See §9.
9. **`[N]` No ISA recorded and none resolved.** `isa_identified` is blank on
   315/315; `sha256_if_listed` absent on 315/315; `interface_documented=n` on
   315/315. The vector-table evidence in §8 is suggestive per-file, not a
   resolved ISA. See §9.

---

## 1. The subfamily in numbers

```
python3 -I -c "
import csv,collections
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
f=[r for r in rows if r['blob_subfamily']=='fastchg']
print(len(f), len({r['device'] for r in f}), len({r['filename'].split('/')[-1] for r in f}),
      sum(int(r['size_bytes']) for r in f))"
```

```
315 28 40 36989007
```

Column profile:

```
db_type  {'FASTCHG': 305, 'UNKNOWN': 10}
priority {'P3': 302, 'P2': 13}
iface    {'n': 315}
isa      {'': 315}
sha256   present: 0/315
soc      blank: 54/315
```

Distinct `md5_db`: **79** over 315 rows; blank: **0**. Zero full-row duplicates
(`315` unique of `315`), so unlike `nfc`/`misc` this subfamily carries no
surplus rows and the published count is the honest count.

### 1.1 Rank inside `other` `[F]`

```
python3 -I -c "
import csv,collections
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
o=[r for r in rows if r['blob_family']=='other']
agg=collections.defaultdict(lambda:[0,0])
for r in o: agg[r['blob_subfamily'] or '<blank>'][0]+=1; agg[r['blob_subfamily'] or '<blank>'][1]+=int(r['size_bytes'])
for i,(k,(n,b)) in enumerate(sorted(agg.items(),key=lambda x:-x[1][1]),1): print(i,k,n,b)"
```

| rank | subfamily | rows | bytes |
|---:|---|---:|---:|
| 1 | misc | 10,720 | 8,498,193,635 |
| 2 | camera | 1,611 | 4,563,019,282 |
| 3 | touch | 880 | 516,418,690 |
| 4 | fingerprint | 284 | 387,540,764 |
| 5 | sensors | 5 | 86,541,968 |
| **6** | **fastchg** | **315** | **36,989,007** |
| 7 | media | 470 | 29,190,348 |
| 8 | nfc | 75 | 9,677,922 |
| 9 | esim | 41 | 8,407,085 |
| 10 | audio | 422 | 5,418,315 |
| 11 | tinysys | 4 | 4,132,864 |
| 12 | oled | 157 | 4,068,320 |
| 13 | gpu-compute | 3 | 2,523,240 |

`fastchg` is **6th of 13 by rows and 6th of 13 by bytes** — the only subfamily in
this list whose two ranks agree. Corpus share: **0.9287%** of rows, **0.05299%**
of bytes.

### 1.2 Row inflation `[F]`

315 rows resolve to only **127 distinct `(device, filename)` pairs** — **2.48
rows per pair**. The cause is directory fan-out exactly as in `touch`: one file
name appears once per panel or fastchg directory.

Rows-per-pair histogram: `1×103, 2×4, 3×8, 5×4, 20×8`. The eight 20-row pairs are
the OnePlus 8 / 8 Pro / 8T / 9R devices, each carrying `oplus_vooc_fw.bin` in 9
directories and `rk826` in another 9 plus 2 stragglers.

---

## 2. What the 40 filenames are

Classifying by leading token over all 315 rows:

```
python3 -I -c "
import csv,collections
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
f=[r for r in rows if r['blob_subfamily']=='fastchg']
def cls(n):
    b=n.split('/')[-1]
    if b.startswith(('oplus_vooc','oppo_vooc')): return 'VOOC'
    if b.startswith('batt_fw'): return 'BATT'
    if b.startswith('FW_'): return 'PANEL'
    return 'FLASH'
agg=collections.defaultdict(lambda:[0,set(),0,set()])
for r in f:
    a=agg[cls(r['filename'])]; a[0]+=1; a[1].add(r['device']); a[2]+=int(r['size_bytes']); a[3].add(r['filename'].split('/')[-1])
for k,(n,d,b,nm) in agg.items(): print(k,n,len(d),len(nm),b)"
```

| class | rows | devices | filenames | md5 | bytes | % of bytes |
|---|---:|---:|---:|---:|---:|---:|
| VOOC charging | 192 | 8 | 3 | 22 | 1,834,392 | 4.96% |
| PANEL DDIC `FW_*` | 82 | 18 | 20 | 32 | 12,213,591 | 33.02% |
| FLASH-memory part | 31 | 6 | 15 | 23 | 22,683,484 | 61.32% |
| BATT gauge `batt_fw` | 10 | 5 | 2 | 2 | 257,540 | 0.70% |
| **total** | **315** | **28** | **40** | **79** | **36,989,007** | **100.00%** |

The percentages sum to `100.00` by command. Note that the totals reconcile on
every axis: row counts sum to 315, distinct md5s sum to 79 (the four classes are
disjoint by md5), and percentage shares sum to exactly 100.00.

### 2.1 The three real fast-charge files `[F]`

| filename | rows | devices | distinct md5 | distinct sizes |
|---|---:|---:|---:|---|
| `oplus_vooc_fw.bin` | 100 | 8 | 11 | 5 (6,464–6,736) |
| `oplus_vooc_fw_rk826.bin` | 80 | 4 | 8 | 6 (12,432–14,352) |
| `oplus_vooc_fw_rt5125.bin` | 12 | 4 | 3 | 1 (10,940) |

Eight devices carry them, and **all eight are OnePlus**: `OnePlus_7`, `OnePlus_7_Pro`,
`OnePlus_7T`, `OnePlus_7T_Pro`, `OnePlus_8`, `OnePlus_8_Pro`, `OnePlus_8T`,
`OnePlus_9R`. The size spread is version drift across panel directories, not
distinct parts — `oplus_vooc_fw.bin` and its `rk826` sibling vary *per directory*
inside one device.

---

## 3. Composition by `db_path` — the bucket's real denominator `[F]`

The directory immediately below `…/firmware/`:

```
python3 -I -c "
import csv,collections,re
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
f=[r for r in rows if r['blob_subfamily']=='fastchg']
def leaf(r):
    m=re.search(r'/firmware/([^/]+)',r['db_path'])
    return m.group(1) if m else 'NO-FIRMWARE-DIR'
c=collections.Counter(); b=collections.Counter()
for r in f: c[leaf(r)]+=1; b[leaf(r)]+=int(r['size_bytes'])
for k,v in c.most_common(): print(k,v,b[k])"
```

| `firmware/<leaf>` | rows | bytes | % bytes |
|---|---:|---:|---:|
| `fastchg` | 192 | 1,834,392 | 4.96% |
| `tp` | 82 | 12,213,591 | 33.02% |
| `ufs` | 31 | 22,683,484 | 61.32% |
| *(no `firmware/` component — `vendor/firmware` root)* | 10 | 257,540 | 0.70% |

**Agreement test:** rows whose leaf equals the subfamily name — `192 / 315 =
60.95%`. So **123 rows (39.05%)** sit under a directory that names a different
concern, and those rows carry **35,154,615 B (95.04%)** of the bucket.

### 3.1 This is not a `db_path` artefact `[F]`

It is important to establish that `tp/` and `ufs/` are genuinely different trees
and not a mis-parse of one path. Evidence:

- `firmware/tp/` holds **1,088 rows corpus-wide**, distributed
  `touch 660, oled 157, <blank> 115, fastchg 82, misc 74`. The `fastchg` share is
  the *fourth* largest of five, and the same directory is majority-`touch`.
- `firmware/ufs/` holds **31 rows corpus-wide — all 31 of them `fastchg`.** The
  directory is used exactly once in the entire matrix, and always mislabelled.
- No row anywhere carries two subfamilies for one `(device, db_path, filename)`
  triple: **0 conflicting keys** corpus-wide. So the labels are internally
  consistent; they are just wrong about what the directory means.

### 3.2 `firmware/tp/` is where panel firmware lives `[F]`

The `fastchg` rows under `tp/` are 82, on 18 devices, 20 filenames. Sample
`db_path` values, all of the form `…/odm/firmware/tp/<hexcode>`:

```
oneplus/benz/odm/firmware/tp/23061        Nord_CE4   FW_S3910_TIANMA.img
oneplus/avalon/odm/firmware/tp/24211      Nord_4     FW_S3910_TIANMA_HBP.img
oneplus/hotdogb/odm/firmware/tp/18865     OnePlus_7T FW_S3706_SAMSUNG_NEW.img
oneplus/larry/odm/firmware/tp/22035       (touch:   LIMIT_/FW_/_FAE variants)
realme/oscar/odm/firmware/tp/22035        Realme_9_Pro FW_S3910_TIANMA.img
```

The `<hexcode>` directory convention and the `FW_`/`LIMIT_` name grammar are the
same ones `research/fleet/other-touch.md` documents for the `touch` subfamily —
because it is the same directory. These 82 rows are panel DDIC firmware.

### 3.3 `firmware/ufs/` is flash-storage firmware `[F]`

The 15 filenames under `ufs/` are part numbers, not opaque labels:

| filename | rows | bytes |
|---|---:|---:|
| `SAMSUNG-KLUEG4RHHD-B0G1.bin` | 4 | 803,024 |
| `SKhynix-HN8T274EJKX130.bin` | 4 | 790,736 |
| `SKhynix-HN8T05DEHKX073.bin` | 3 | 659,664 |
| `SAMSUNG-KLUFG8RHHD-B0G1.bin` | 3 | 803,024 |
| `SAMSUNG-KLUEG4RHGB-B0E1.bin` | 2 | 790,736 |
| `SKhynix-HN8T05BZGKX015.bin` | 2 | 446,672 |
| `SAMSUNG-KLUGGARHHD-B0G1.bin` | 2 | 803,024 |
| `SAMSUNG-KLUDG4UHDC-B0E1.bin` | 2 | 520,400 |
| `SAMSUNG-KLUEG8UHDC-B0E1.bin` | 2 | 520,400 |
| `SAMSUNG-KLUFG8RHDB-B0E1.bin` | 2 | 520,400 |
| `SAMSUNG-KLUFG8RHGB-B0E1.bin` | 1 | 790,736 |
| `SKhynix-HN8T15DEHKX075.bin` | 1 | 659,664 |
| `SKhynix-HN8T174EJKX075.bin` | 1 | 790,736 |
| `MICRON-MT001TAYAX8U40.bin` | 1 | 1,435,388 |
| `MICRON-MT128GBCAV2U31.bin` | 1 | 1,040,592 |

Six devices carry them — `Nord_4`, `Nord_CE4`, `OnePlus_11_5G`, `OnePlus_12`,
`OnePlus_12R`, `Pad_Pro` — at six distinct `db_path` values, **every one ending
in `/firmware/ufs`**:

```
oneplus/aston/odm/firmware/ufs     oneplus/avalon/odm/firmware/ufs
oneplus/benz/odm/firmware/ufs      oneplus/caihong/odm/firmware/ufs
oneplus/salami/odm/firmware/ufs    oneplus/waffle/odm/firmware/ufs
```

`[I]` These are per-device UFS/eMMC *storage* firmware images, selected by the
flash part actually fitted during manufacture. The `SAMSUNG-` and `SKhynix-`
prefixes plus a `K`/`HN8T` part code and a `-B0G1`-style revision suffix are the
standard shape of a memory vendor's part number. `[N]` I did not find a public
datasheet for any of the 15 within this session and did not decode a payload —
none of the 15 exists on disk (see §9.2).

### 3.4 The 10 `batt_fw` rows are a different class again `[F]`

`batt_fw_adi_79_2.bin` (25,334 B) and `batt_fw_adi_79_3.bin` (26,174 B) sit at
`vendor/firmware` root — not under any `firmware/<leaf>`:

```
google/tokay/vendor/firmware   Pixel_9
google/tegu/vendor/firmware    Pixel_9A
google/komodo/vendor/firmware  Pixel_9_Pro_XL
google/comet/vendor/firmware   Pixel_9_Pro_Fold
google/caiman/vendor/firmware  Pixel_9_Pro
```

Five Pixel 9-family devices, 5 rows each × 2 files = 10, `db_type=UNKNOWN` on
**all 10** — the only `UNKNOWN` rows in the bucket. `adi` is Analog Devices;
`[I]` these are battery fuel-gauge or charger-IC firmware. They are at least
*adjacent* to charging, which is more than can be said for the other 113
non-fastchg rows — but they are not VOOC, and `batt_fw` is not in the `fastchg`
directory.

---

## 4. The assignment mechanism `[F]`

Why are panel and storage rows labelled `fastchg`? The label was derived from the
**filename**, not the path. The test:

```
python3 -I -c "
import csv,collections
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
fw=[r for r in rows if r['filename'].split('/')[-1].startswith(('FW_','LIMIT_'))]
byname=collections.defaultdict(set)
for r in fw: byname[r['filename'].split('/')[-1]].add(r['blob_subfamily'] or '<blank>')
print(len(byname), sum(1 for v in byname.values() if len(v)>1))"
```

```
127 0
```

**None of the 127 distinct `FW_`/`LIMIT_` filenames appears under two
subfamilies.** Likewise:

- `(device, filename)` pairs with >1 subfamily: **0 of 524**.
- `fastchg`'s own 40 filenames that appear under another subfamily anywhere in
  the matrix: **0 of 40**.

So every one of the 40 filenames has a single, globally consistent subfamily
label. Combined with §3.1's finding that no *row* is contradictory, the picture
is: subfamily is a property assigned once per filename and then inherited by
every row carrying that name, regardless of where the file actually sits.

### 4.1 That rule does not fit the filename shapes, which is the defect `[F]`

A four-way rule over `FW_`/`LIMIT_` shape — `LIMIT_` → `oled`, `_sys_edge_touch_config`
→ `misc`, `_FAE` → `touch`, plain `FW_<ic>_<panel>` → `fastchg` — predicts only
**459 of 1,088** rows (42.19%):

```
filename shape                         subfamily distribution
FW_<ic>..._sys_edge_touch_config       {'misc': 9, 'touch': 1}
FW_<ic>_<panel>                        {'<blank>': 56, 'touch': 234, 'fastchg': 82, 'misc': 14}
FW_<ic>_<panel>_FAE                    {'<blank>': 59, 'touch': 211, 'misc': 51}
LIMIT_<ic>_<panel>                     {'touch': 214, 'oled': 157}
```

The same plain `FW_<ic>_<panel>` shape splits across **four** outcomes, and
`LIMIT_` splits across two. Whatever assigned these labels is neither the path
(§3) nor the name shape (§4.1) in a recoverable way.

`[I]` The most economical explanation consistent with all the measurements: the
label was attached when a file was *first* ingested, per source tree or batch,
and never revisited — the same failure mode `other-touch.md` §1.2 diagnosed for
`TOUCHSCREEN3/4/5`, where the numeric suffix "tracks the generation of the
*device row* that first ingested the file, not the file."

`[U]` The ingest provenance is not recoverable from the matrix alone. I did not
guess it and did not re-label any row.

---

## 5. One IC family, four subfamilies `[F]`

This is the sharpest consequence of §4. `S3910` and `S3706` are panel driver ICs.
Counting rows containing the token in the filename, anywhere in the matrix:

```
python3 -I -c "
import csv,collections
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for ic in ('S3910','S3706'):
    sel=[r for r in rows if ic in r['filename'].split('/')[-1]]
    print(ic, len(sel), dict(collections.Counter(r['blob_subfamily'] for r in sel)))"
```

| IC | total rows | subfamilies and rows |
|---|---:|---|
| `S3910` | 85 | `oled` 32, `touch` 25, `fastchg` 23, `misc` 5 |
| `S3706` | 60 | `fastchg` 20, `oled` 20, `misc` 20 |

Per subfamily, with bytes and filenames:

| IC | subfamily | rows | devices | bytes | filenames |
|---|---|---:|---:|---:|---:|
| `S3910` | fastchg | 23 | 9 | 4,736,315 | 6 |
| `S3910` | touch | 25 | 10 | 5,165,360 | 8 |
| `S3910` | oled | 32 | 9 | 554,592 | 10 |
| `S3910` | misc | 5 | 5 | 53,586 | 1 |
| `S3706` | fastchg | 20 | 4 | 2,083,200 | 3 |
| `S3706` | oled | 20 | 4 | 82,736 | 3 |
| `S3706` | misc | 20 | 4 | 2,079,040 | 3 |

The naming differs by subfamily but the IC is the same:

```
fastchg  FW_S3910_TIANMA.img      FW_S3706_SAMSUNG.img
touch    FW_S3910_TIANMA_FAE.img  (no S3706)
oled     LIMIT_S3910_TIANMA.img   LIMIT_S3706_SAMSUNG.img
misc     FW_S3910_TIANMA_sys_edge_touch_config.img   FW_S3706_SAMSUNG_NEW_FAE.img
```

Corpus-wide **0 of 127** `FW_`/`LIMIT_` names are shared across subfamilies (§4),
so the split is entirely at the *name-variant* level. A reader who trusted
`blob_subfamily` would conclude that `S3910` is four different kinds of hardware.
It is one panel driver, and every one of its 85 rows is filed at `firmware/tp/`
(§3.2).

### 5.1 The same directory holds four container formats side by side `[F]`

`…/larry/tree-odm/firmware/tp/22035/` is the decisive artefact. Four files, same
IC, same panel vendor, same directory:

| file | bytes | md5 | magic / first bytes |
|---|---:|---|---|
| `LIMIT_S3910_TIANMA.img` | 15,836 | `1f6229883451c7e5999af87d63fc943c` | `LIMITIMG` |
| `FW_S3910_TIANMA.img` | 209,738 | `b72cb7c3252bdf43ebb1007c81acc398` | `FwUp` |
| `FW_S3910_TIANMA_FAE.img` | 209,530 | `a94482fe15523246e12815230cb9beed` | `2b 47 18 48` (bare body) |
| `FW_S3910_TIANMA_sys_edge_touch_config.img` | 9,528 | `e288e8a34a8045c4e40823069f7dcf8a` | `<filter-conf>` XML |

Four formats, one panel, one directory. This is the concrete refutation of any
"`blob_subfamily` describes a format" reading, and it independently confirms
`other-touch.md`'s headline that `_FAE` "is not a format marker."

---

## 6. The `FwUp` container `[F]`

### 6.1 The closure

Every `FwUp` file on disk satisfies:

```
80 + u32_le@0x0C + 128 == filesize
```

Tested over 43 VOOC payloads and 37 panel containers:

```
python3 -I -c "
import struct,glob
files=[p for p in sorted(glob.glob('instantnoodle/tree-odm/firmware/fastchg/*/*'))
                +sorted(glob.glob('larry/tree-odm/firmware/tp/*/FW_*.img'))
       if open(p,'rb').read(4)==b'FwUp']
ok=sum(1 for p in files
       if (lambda d: 80+struct.unpack_from('<I',d,12)[0]+128==len(d))(open(p,'rb').read()))
print(len(files), ok)"
```

```
80 80
```

**80 of 80.** No exceptions, no rounding, no sector alignment needed.

### 6.2 Field layout

Verified field by field; the counts are over all 80 files.

| offset | size | content | verification |
|---|---:|---|---|
| `0x00` | 4 | magic `FwUp` (`46 77 55 70`) | 80/80 |
| `0x04` | 4 | `u32` — varies per file | 80/80 present, 30+ distinct values — `[U]` |
| `0x08` | 4 | `u32` — `0` on 73/80, `10` on 7/80 | bimodal, `[U]` |
| `0x0C` | 4 | **body length** | closes 80/80 (§6.1) |
| `0x10` | 4 | `0x80000000` | **80/80 identical** — a flag/endianness marker `[I]` |
| `0x14` | 60 | **NUL-terminated embedded path** | 80/80 terminated |
| `0x50` | 16 | body begins here for 4 of the 5 body dialects | see §7 |

Header size is therefore **80 (`0x50`)** and the header ends exactly where the
path field ends.

### 6.3 The embedded path — and `_FAE` decoded `[F]`

The path field at `0x14` is a **self-referential provenance record**. Over the 80
files:

| relationship of embedded basename to on-disk basename | files |
|---|---:|
| identical | 15 |
| path differs, basename same | 37 |
| **basename differs** | **28** |
| empty | 0 |

Representative values:

```
fastchg/21619/oplus_vooc_fw_rk826.bin
fastchg/20161/oplus_vooc_fw_rt5125.bin
tp/22035/FW_S3910_TIANMA.img
tp/20121/FW_NF_ILI7807S_TIANMA.img
```

This field is what makes `_FAE` intelligible. For 36 of the 37 `FW_*` / `FW_*_FAE`
pairs, the size delta is **exactly 208**:

```
FW_S3910_TIANMA.img       209,738
FW_S3910_TIANMA_FAE.img   209,530     Δ = 208 = 80 + 128
```

and the `_FAE` bytes are found verbatim inside the wrapped file, starting at
offset 80:

```
python3 -I -c "
a=open('larry/tree-odm/firmware/tp/22035/FW_S3910_TIANMA.img','rb').read()
f=open('larry/tree-odm/firmware/tp/22035/FW_S3910_TIANMA_FAE.img','rb').read()
print(len(a),len(f),f in a, a.find(f[:24]))"
```

```
209738 209530 True 80
```

So in the normal case **`_FAE` is the bare body**; the wrapped `FW_*` file is
header + that same body + trailer. `_FAE` is not a different format and not an
abbreviation for a firmware update mode: it is the payload with the container
removed.

**The one exception `[F]`.** `…/tp/21221/FW_FT3518_SAMSUNG.img` is 67,110 B and
its `_FAE` sibling is 66,600 B — a delta of **510**, not 208 — and the `_FAE`
bytes are **not** contained in the wrapped file at all:

```
whole FAE in FW_?  False
FAE first 24 in FW_ at: -1
FAE last 24  in FW_ at: -1
FAE head      : 02 17 41 02 ad 09 e4 02 10 58 22 02 00 …
FW_ body head : 02 17 41 02 a8 95 e4 02 10 58 22 02 00 …
```

The two bodies agree for the first 4 bytes and then diverge (`ad 09 e4` vs
`a8 95 e4`), converging again at bytes 9–14. `[I]` Two builds of the same
format, at the same header version, differing in build-specific fields — i.e.
exactly the case where `_FAE` *is* a separate artefact. So the correct statement
is not "`_FAE` is always the body" but "`_FAE` is the body in 36 of 37 pairs on
this corpus, and the 37th is a different build with the same container header."
Anyone treating the suffix as a format marker would be wrong both ways: it
usually marks *absence* of a wrapper, and occasionally marks a different build.

### 6.4 The `oppo` → `oplus` rename `[F]`

Of the 28 basename mismatches, 20 are one specific vendor rename:

```
embedded = oppo_vooc_fw.bin      on disk = oplus_vooc_fw.bin      × 20
```

The remaining 8 are empty-path anomalies where the field is present but
unpopulated (`FW_NF_ILI7807S_HUAXING.img` ×4, `FW_NF_ILI7807S_DSJM.img` ×3,
`FW_NF_TD4377_DSJM.img` ×1).

`[I]` The file was authored by BBK/Oppo under the `oppo_` name and renamed to
`oplus_` when the OnePlus brand split off; the embedded path was not rewritten.
This is a fact about the payload that no `filename` column can express — the
database records `oplus_vooc_fw.bin` and is correct about the on-disk name, while
the file itself says `oppo`.

### 6.5 The 128-byte trailer `[F]`

The trailer is opaque. Measured properties:

- 128 bytes, **no plain digest match**: tested `md5`, `sha1`, `sha224`, `sha256`,
  `sha384`, `sha512`, `sha3_256`, `blake2b` over `header‖body`, `body‖header`,
  `body`, and `header`, forwards and reversed — **0 of 80 matches** on every
  combination.
- Entropy **6.371–6.676 bits/byte** over 10,240 bytes with **30 zero bytes** and
  all 256 values present — high-entropy data, not padding.
- It is a **bijection with `(header, body)`**: 41 distinct `(header, body)` pairs
  → **41 distinct trailers**, and **0 pairs with two trailers**. Where the same
  body appears under different headers (3 cases), the trailers differ; where the
  same header and body recur, the trailer is identical.

`[I]` A signature or keyed digest over the header (including the path string) and
the body. `[U]` The algorithm is not recoverable from 80 samples without the
producer's key, and I did not guess one. It is **not** a checksum the kernel
recomputes: §9.1 records that no in-tree consumer of this format exists.

Header `0x04` remains unresolved. It is neither the body length (§6.1 shows that
is `0x0C`), nor a constant, nor monotonically related to size; it takes 30+
distinct values and on some files exceeds 32 bits of plausible meaning
(`4196799237`). Recorded as `[U]`, not guessed.

---

## 7. Six body dialects under one wrapper `[F]`

The `FwUp` header is constant but the body is not. Over the 37 wrapped panel
containers on disk:

```
python3 -I -c "
import struct,glob,collections
pan=[p for p in sorted(glob.glob('larry/tree-odm/firmware/tp/*/FW_*.img'))
     if open(p,'rb').read(4)==b'FwUp']
c=collections.Counter()
for p in pan:
    d=open(p,'rb').read(); b=d[80:80+struct.unpack_from('<I',d,12)[0]]
    c['ASCII Intel HEX' if b[:1]==b':' else 'binary']+=1
print(len(pan), dict(c))"
```

```
37 {'binary': 24, 'ASCII Intel HEX': 13}
```

Magics per dialect:

| dialect | files | body magic(s) |
|---|---:|---|
| ASCII Intel HEX | 13 | `3a303730` = `":070"` — the start of an Intel HEX record |
| binary | 24 | `00010000` ×11, `02174102` ×6, `00000962` ×3, `2b471848` ×2, `00000060` ×2 |

So a single `FwUp` wrapper carries at minimum: an **ASCII text format** (Intel
HEX), and **five distinct binary headers**. The `_FAE` counterpart of the Intel
HEX body is *also* Intel HEX (`FW_NF_ILI7807S_TIANMA_FAE.img` starts `3a303730`),
consistent with §6.3's "`_FAE` is the body."

### 7.1 `LIMITIMG` is a second, separate container `[F]`

The 41 `LIMIT_*` files on disk are not `FwUp` at all. All 41 begin `4c 49 4d 49`
= `LIMI`, i.e. `LIMITIMG`:

```
LIMITIMG <u32@0x08> 0  <offset table…>
sec@0x4c: 4f 50 50 4f 84 00 00 00 01 00 00 00 cc 00 00 00 …
          O  P  P  O  <len>  <ver>  <…>
```

The body is a **section table** of 11 little-endian `u32` offsets beginning at
`0x10`, followed by sections whose first bytes are the ASCII tag `OPPO`.

`[N]` The section table did **not** validate uniformly. Testing "offsets
strictly ascending AND last offset < filesize" passes on **24 of 41** files. The
offset tuples cluster into 12 distinct shapes, the largest group being 10 files
sharing one tuple starting `[64, 4696, 9328, …]`. On 8 files the tuple contains
values like `1330663503` that cannot be an offset — so for those, what I read as
the table is not the table (the header is longer, or the table is not at `0x10`).
**`LIMITIMG` is therefore only partly decoded.** I state the magic, the section
tag and the 11-word offset region as `[F]`; the full layout is `[U]`.

Sizes span 9,324–117,312 B across 11 distinct values, and the 41 files are small
next to their `FW_` siblings — e.g. `S3910_TIANMA` is 15,836 B as `LIMIT_` versus
209,738 B as `FW_`, a **13.2×** ratio. `[I]` `LIMIT_` is a configuration/limit
table, not a firmware image; `FW_` is the image. I am not claiming that of all 41,
only of the `S3910_TIANMA` pair I measured.

---

## 8. The VOOC payloads, and what the bodies are `[F]`

### 8.1 The three charge-controller parts are three different MCUs `[F]`

The body of each VOOC file begins with what looks like an ARM Cortex-M vector
table — initial stack pointer, then a reset vector with the Thumb bit set. Testing
`SP % 4 == 0` and `RV & 1` across all 43:

| filename | body offset of SP/RV | distinct SP | distinct RV | vector-table shape |
|---|---|---:|---:|---|
| `oplus_vooc_fw.bin` | `+0x00` | `0x00828800` (1) | 4 values | **13/20** |
| `oplus_vooc_fw_rk826.bin` | `+0x80` (inner 128-B prefix) | `0x20000800` (1) | 8 values | **20/20** |
| `oplus_vooc_fw_rt5125.bin` | `+0x00` | `0x200005e8` (1) | `0x00000131` (1) | 3/3 |

Three distinct stack-pointer values — `0x00828800`, `0x20000800`, `0x200005e8` —
in three disjoint address regions. `[I]` Three different microcontrollers, which
matches the three part suffixes: the base `oplus_vooc_fw.bin`, `rk826`, and
`rt5125`.

`[N]` The base file's shape test passes only 13/20 at `+0x00`, and the failures
are informative rather than random: reset vectors like `0x0082109e` and
`0x0082f69d` are plausible code addresses in the same 8 MB region, and
`0x0082109e % 4 == 2`, which is legal for a Thumb branch target but fails my
"`SP % 4 == 0` and `RV & 1`" test only because I additionally required `SP` to be
4-aligned (it is) — the actual failures come from reset vectors whose low bit is
even. So **13/20 is a lower bound, not a refutation**; the base file is not
uniformly parseable as a plain vector table.

`rk826` is the interesting one: its body has a **128-byte inner prefix** before
the vector table at `+0x80`, and that prefix is itself structured —
`00 00 34 55 b0 34 00 00 64 00 00 00 64 00 00 00` — with `u32@+0x04 = 13488`
(plausible payload length) and `u32@+0x08 = u32@+0x0C = 100`. So `rk826` is a
container-inside-a-container. `[U]` That inner prefix is not decoded.

### 8.2 No disassembler, so no instruction-level claims `[N]`

No ARM/Thumb, AArch64 or Xtensa disassembler is available in this environment.
Per the standing rule, the vector-table reading above is reported as a **word-class
shape test (`[I]` for these specific files)**, not as a decoded ISA. `isa_identified`
stays blank on 315/315 rows and I am not filling it in.

Confirming by independent means that the body is code: `rk826`'s body shows
dense, structured data from `+0x100` onward — nonzero-byte density 225–237 of 256
per 0x100 block, with recognisable Thumb idioms in the raw bytes (`70 47` = `bx lr`
at `+0x108`, `f0 bd` = `pop {r4-r7,pc}` at `+0x402`). That is a per-file
observation on 3 files, marked `[I]`, not an ISA assignment.

### 8.3 The panel bodies are not the same kind of object `[F]`

The panel containers' bodies are, per §7, either ASCII Intel HEX or one of five
binary headers — but none of the five binary magics is a vector table. e.g.
`FW_S3910_TIANMA.img` body starts `2b 47 18 48` with `u32`s `0x04, 0x18, 0x44,
0x0226e8, 0x02375e` at `+0x04…+0x14`, then the ASCII tag `BOOT_CONFIG` at
`+0x1C`. `[I]` A boot configuration block followed by segment data, i.e. a
*flash-image container*, not code with a vector table.

This is the substantive difference the `fastchg` label erases: the 192 charging
rows are MCU firmware images, and the 82 panel rows are display-driver images in
a different container with a different internal layout.

---

## 9. Honest negatives

### 9.1 No public specification for `FwUp` `[N]`

- `torvalds/linux`: no occurrence of the `FwUp` magic in `drivers/power/supply`,
  `drivers/misc`, or `drivers/firmware`. There is **no in-tree consumer**; the
  payloads are loaded by a vendor userspace daemon. This also means the 128-byte
  trailer is *not* a kernel-verified digest — contrast the `s3fwrn5` container in
  `other-nfc.md`, where the kernel parses the header 8/8 and recomputes a SHA1 at
  load.
- Web search for `"FwUp" oppo vooc firmware container header` returns 8 results,
  **all** about `fwup-home/fwup` — an unrelated embedded-Linux image updater
  (`.fw` = ZIP). Zero results for this format.
- No datasheet or specification for `rk826`, `rt5125`, or the `FwUp` wrapper was
  found. `[N]`

Accordingly the whole of §6 is derived from bytes plus arithmetic closure. Where
closure is not exact I say so: `LIMITIMG` (§7.1) is only partly decoded, header
`0x04` (§6.5) is unresolved, and the `rk826` inner prefix (§8.1) is not decoded.

### 9.2 The flash-memory payloads are not on disk `[N]`

None of the 15 `SAMSUNG-`/`SKhynix-`/`MICRON-` filenames and none of the 2
`batt_fw` filenames exists anywhere in the local workspace:

```
find . \( -name "SAMSUNG-KLU*" -o -name "SKhynix-*" -o -name "MICRON-*" -o -name "batt_fw*" \) | wc -l
0
```

So §3.3 and §3.4 classify those 41 rows **by filename and path only**. The
61.32% of the bucket's bytes that they represent is the part of this issue I could
not verify at byte level. That is the single largest gap in this report and I am
stating it rather than filling it with inference.

### 9.3 The on-disk corpus is a subset of the matrix `[N]`

- `instantnoodle/tree-odm/firmware/fastchg/` holds **43 files in 43 directories,
  425,054 B** — but only the **3** VOOC filenames appear in the matrix for
  `OnePlus_8`. §1.2 of `third-device-instantnoodle.md` already noted this tree
  carries 25 fastchg blobs the matrix does not list.
- `larry/tree-odm/firmware/tp/` holds **76 `FW_*.img` files** and 41 `LIMIT_*.img`.
  `larry` is `Nord_CE3`, and the matrix gives `Nord_CE3` **5 panel rows** in
  `fastchg` — so 37+ of the 76 wrapped containers are outside the matrix.
- The 58 `LIMIT_` files found workspace-wide are a superset of the 41 in
  `larry/tp` alone, i.e. other devices' trees also carry them.

Conclusion: the container results in §6–§8 are from **80 files on 2 device trees**,
not from 315 rows. They generalise to the format, not to a byte census of the
subfamily.

### 9.4 No interface documentation and no `sha256` `[N]`

`interface_documented=n` on 315/315 and `sha256_if_listed` absent on 315/315.
`db_type` is `FASTCHG` on 305 and `UNKNOWN` on the 10 `batt_fw` rows; the label
adds no information beyond the subfamily name for the other 305.

### 9.5 Report-only: two defects found, not fixed

1. **The 123 mislabelled rows.** §3. A row at `firmware/tp/` is not fast-charge
   firmware, and a row at `firmware/ufs/` is not either. I did **not** re-label
   them: re-labelling is a database migration touching 123 rows across 5
   subfamilies, and `other-touch.md`'s 660-row figure is correct *for
   `blob_subfamily=touch`* — moving rows in would silently invalidate a published
   census. It needs an owner decision, not a drive-by edit.
2. **The `_FAE` 208-byte delta.** §6.3. In 36 of 37 pairs, `FW_*` and `FW_*_FAE`
   are the same bytes with and without an 80+128-byte wrapper, so a tool that
   treats them as distinct payloads is double-counting. The 37th pair
   (`21221/FW_FT3518_SAMSUNG.img`) is a genuinely different build, so the
   suffix cannot be used as a dedup key in either direction.

---

## 10. Method

1. **Census first, from the CSV only.** All of §1–§5 is reproducible from
   `coverage-matrix.csv` with stdlib `csv` + `collections`; no payload access
   needed. Every table is a printed command output pasted verbatim.
2. **Directory as an independent axis.** Because `blob_subfamily` and `db_path`
   are separate columns, the `db_path` leaf (`firmware/<leaf>`) gives a second,
   independent classification of the same rows. The disagreement between them is
   the finding in §3, and §3.1 checks that the disagreement is not a path-parsing
   artefact.
3. **Container decode by arithmetic closure.** For `FwUp` I did not posit a format
   and look for confirmation. I read `u32@0x0C` from the bytes, noticed
   `80 + that + 128 == filesize` on one file, and then tested the rule on all 80.
   It held 80/80 (§6.1). The `_FAE` relation (§6.3) was found the same way: a
   constant 208-byte delta across 37 pairs, then `f in a → True` at offset 80 —
   and then checking the rule for exceptions, which is how the 36/37 qualifier
   and the `21221` counter-example were found rather than left as a false 37/37.
4. **Every number re-derived before writing.** Percentages are recomputed and
   asserted to sum to 100.00 (table, §2); sub-counts are asserted to sum to
   totals (192 = 100+80+12; 82 = per-name sum; 31 flash rows). Where a count did
   **not** reconcile I say so rather than rounding it away — that is why §7.1
   reports `24/41` for `LIMITIMG` instead of an 11-section story.
5. **Negative tests are run and reported.** Eight digest algorithms × four input
   arrangements × forwards/reversed for the trailer (§6.5) — reported as 0/80
   rather than as "probably a signature." The `find` for the flash payloads
   (§9.2) is reported as `0` rather than replaced by inference from part numbers.
6. **No disassembler, no ISA claim.** §8.2. Vector-table tests are shape tests,
   marked `[I]` per file; `isa_identified` is left blank.
7. **Rule 1 was checked, and there was nothing to correct.** See §10.1.

### 10.1 Rule 1 check

Rule 1 says a wrong statement in an existing note should be corrected in place,
not merely contradicted in a new file — **provided** the correction is not itself
false. I checked every prior note that mentions this material:

| note | claim | verdict |
|---|---|---|
| `other-touch.md` L25/L145 | panel `FW_*`/`LIMIT_*` = 660 rows / 73,886,385 B | **correct** — re-measured exactly 660 / 73,886,385 for `blob_subfamily=touch`. Correctly scoped; *not* a corpus-wide claim. No edit. |
| `other-touch.md` L304–307 | `_FAE` spans six container formats | **correct**, and §7 extends the count rather than contradicting it |
| `second-device-larry.md` L63–70 | `larry` has no `firmware/fastchg/`; VOOC pair 0/2 there | **correct** — verified; `larry/…/firmware/` has only `tp/`. No edit. |
| `third-device-instantnoodle.md` | VOOC pair byte-exact on OnePlus 8 | **correct** — independently reproduced (§8.1 SP/RV values match its md5s) |
| `three-device-sharing.md` L127 | OP6 census has no odm tree, so VOOC cannot appear there | **correct** — scope fact |

The one place where the *absence* of prior art mattered — that `firmware/tp/` in
`fastchg` holds panel firmware — is a gap, not an error, so it is new material
here and no existing sentence needed correcting. **No Rule 1 edit was made, and
none was warranted.**
