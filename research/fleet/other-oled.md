# `oled` — 157 display rows that are really one touch panel filed twice

Analysis date: 2026-11-24. Analyst: OC-1 (`100milionseek`), issue
[#2061](https://github.com/adineo-cmd/open-device/issues/2061).

Inputs:
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows) for the
census; 56 `LIMIT_*.img` payloads (19 distinct filenames) plus 2 `LIMIT_*.ini`
files under `…/second-device/{larry,instantnoodle}/tree-odm/firmware/tp/`; and
`research/fleet/other-touch.md` §6, which already decoded the `LIMITIMG`
container for the same files. Every
number below is command output. No payload is committed; samples are ≤16 bytes
of hex.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** The `oled` subfamily is 157 rows, 19 devices, 33 filenames,
4,068,320 B — the 8th of thirteen `other` subfamilies by rows and 12th by bytes,
the second-smallest bucket in the family. It is a clean, well-behaved bucket in
every mechanical sense: no duplicate rows, no cross-vendor ambiguity, and
`db_type=OLED` is *exactly* co-extensive with `blob_subfamily=oled` on all 157
rows.

What it is not is a coherent category. All 157 rows are `LIMIT_*` files living at
`firmware/tp/` — the directory `other-touch.md` establishes as **panel and touch
firmware**, where 660 rows are already filed `touch`. The 371 `LIMIT_` rows in the
matrix split exactly two ways, `touch` 214 / `oled` 157, across 47 filenames with
**zero** names in common. So `LIMIT_` is not two kinds of artefact; it is one kind
of artefact carrying two labels.

The split is not random. It tracks the **controller IC**: 18 of the 19 ICs
appearing in `LIMIT_` names land in exactly one subfamily. The single exception,
`NT36672C`, splits 46/8 on the *order of a token* in the filename —
`LIMIT_NF_NT36672C_*` → `touch`, `LIMIT_NT36672C_NF_*` → `oled`, 54/54 with no
exceptions.

And it fails outright in two places, which is the substance of this report:

1. **One byte-identical payload is filed under both labels.**
   `LIMIT_SY761_SAMSUNG.img` (`oled`) and `LIMIT_S6SY761_SAMSUNG.img` (`touch`)
   are the **same md5**, the same 15,628 B, on the **same four devices**. The
   `_NEW` pair repeats it. 16 `oled` rows (10.2%) and 12 `touch` rows sit on these
   two cross-filed md5s. No property of the bytes can distinguish them, because
   there is no difference.
2. **The subfamily label is contradicted by the payload's own content.** Two
   `LIMIT_*.ini` files exist on disk and describe a **capacitive touch**
   factory-test threshold table — open/short tests, TX/RX nodes, noise
   peak-to-peak, DAC calibration. Their `.img` siblings are labelled `oled`. And
   the matrix contains **zero** `.ini` rows at all, so the database cannot see
   this file type exists.

`LIMITIMG` itself needs no new work: `other-touch.md` §6 decoded it, and I
reproduce that decode independently on `larry`'s 41 files (41/41, 449 records)
and extend it to all 56 on disk (56/56, 539 records).

---

## 0. Headline

1. **`[F]` `db_type=OLED` is exactly the subfamily.** 157 rows, all
   `blob_subfamily=oled`, all `LIMIT_*`, no exceptions in either direction. Unlike
   `fastchg` — where `db_type=FASTCHG` sat on 305 of 315 rows and told you nothing
   — this axis is perfectly consistent and therefore adds no information beyond
   the subfamily name. See §2.
2. **`[F]` All 157 rows live at `firmware/tp/`.** Every one. The same directory
   holds 660 rows filed `touch`, 115 blank, 82 `fastchg`, 74 `misc`. See §1.
3. **`[F]` `LIMIT_` splits exactly two ways with zero overlap.** 371 rows =
   `touch` 214 + `oled` 157; 47 distinct names; **0** names appear under both.
   See §4.
4. **`[F]` The split tracks the controller, 18 of 19 pure.** The one split IC is
   `NT36672C` (46 `touch` / 8 `oled`), and it splits on token *order*:
   `LIMIT_NF_NT36672C_*` → `touch`, `LIMIT_NT36672C_NF_*` → `oled`, **54/54**.
   See §4.2.
5. **`[F]` `SY761` and `S6SY761` are one part, filed as two.** Same md5
   `16b6abb01521207896c3c42ed7bf0b67`, same 15,628 B, same 4 devices
   (`OnePlus_7`, `_7_Pro`, `_7T`, `_7T_Pro`) — one `oled`, one `touch`. The
   `_NEW` variant does it again. See §5.
6. **`[F]` A `LIMIT_*` payload is a touch-test config, not a display file.** Two
   `LIMIT_NF_ILI7807S_DSJM.ini` (47,026 B, plaintext) carry `[PV5_4 Command]`,
   `Protocol=0506`, a build date, and sections for `Open Test_C`, `Short Test`,
   `Raw Data`, TX/RX node counts and DAC calibration — a **capacitive touch**
   factory-test threshold table. See §6.
7. **`[F]` The matrix cannot see `.ini` files at all.** 0 of 33,917 rows have that
   extension. The two files on disk are invisible to the census. See §6.3.
8. **`[F]` `LIMITIMG` closes 56/56 with 539 records** — reproducing
   `other-touch.md` §6's 41/41 / 449-record result on its own file set, extending
   it to the 15 `instantnoodle` files, and correcting a wrong figure in my own
   `other-fastchg.md` §7.1 (§8).
9. **`[N]` A tempting hypothesis is refuted.** "Record magic `OPPO` ⇒ oled,
   `SLPO` ⇒ touch" fails on **37 of 56** files (**23 of 41** in `larry` alone).
   Recorded as a negative. See §7.2.
10. **`[N]` No ISA, no interface, no public spec.** `isa_identified` blank on
    157/157, `interface_documented=n` on 157/157, `sha256_if_listed` absent on
    157/157. No in-tree `LIMITIMG` consumer and no public `PV5_4` documentation
    was found. See §9.

---

## 1. The subfamily in numbers

```
python3 -I -c "
import csv,collections
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
o=[r for r in rows if r['blob_subfamily']=='oled']
print(len(o), len({r['device'] for r in o}), len({r['filename'].split('/')[-1] for r in o}),
      len({r['md5_db'] for r in o}), sum(int(r['size_bytes']) for r in o))"
```

```
157 19 33 42 4068320
```

Column profile:

```
vendor        {'oneplus': 125, 'realme': 32}
blob_family   {'other': 157}
db_type       {'OLED': 157}
priority      {'P3': 146, 'P2': 11}
iface         {'n': 157}
isa           {'': 157}
sha256        present: 0/157
soc           blank: 36/157
filename prefix {'LIMIT': 157}
```

Zero full-row duplicates (`157` unique of `157`) and zero blank `md5_db`. So,
like `fastchg` and unlike `nfc`/`misc`, the published row count is the honest
count and there is no dedup to report.

### 1.1 Rank inside `other` `[F]`

`oled` is **8th of 13 by rows** (157) and **12th of 13 by bytes** (4,068,320) —
only `gpu-compute` is smaller by bytes. Share of the `other` family: **1.048%**
of rows, **0.0287%** of bytes. Share of the whole corpus (33,917 rows /
69,797,539,502 B): **0.4629%** of rows, **0.00583%** of bytes.

The two ranks disagree by four places, which is the whole story of this bucket:
its rows are many relative to their size, because `LIMIT_` payloads are small
config tables (median 20,368 B, §3) rather than firmware images.

### 1.2 Row inflation is mild `[F]`

157 rows resolve to **116 distinct `(device, filename)` pairs** — **1.35 rows per
pair**. That is far lower than `touch` (1.95) or `fastchg` (2.48), because
`oled`'s directory fan-out is smaller.

Rows-per-pair histogram: `1×95, 2×9, 3×4, 4×8`.

### 1.3 Every row is at `firmware/tp/` `[F]`

```
python3 -I -c "
import csv,collections,re
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
o=[r for r in rows if r['blob_subfamily']=='oled']
def leaf(r):
    m=re.search(r'/firmware/([^/]+)',r['db_path']); return m.group(1) if m else 'NONE'
print(collections.Counter(leaf(r) for r in o))"
```

```
Counter({'tp': 157})
```

**157 of 157.** No `oled` row sits anywhere else. The same directory, corpus-wide,
carries `touch` 660, blank 115, `fastchg` 82, `misc` 74 — so `tp` is a
five-label directory and `oled` is its second-largest tenant.

---

## 2. `db_type` is a perfect synonym for the subfamily `[F]`

```
python3 -I -c "
import csv,collections
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
o=[r for r in rows if r['db_type']=='OLED']
print(len(o), collections.Counter(r['blob_subfamily'] for r in o),
      sum(1 for r in o if r['filename'].split('/')[-1].startswith('LIMIT_')))"
```

```
157 Counter({'oled': 157}) 157
```

Every `db_type=OLED` row is `blob_subfamily=oled` and every one is a `LIMIT_`
file. The converse holds too: 157 `oled` rows, 157 of them `db_type=OLED`.

This is worth stating because it is the *opposite* of the `fastchg` situation.
There, `db_type` was `FASTCHG` on 305 rows and `UNKNOWN` on 10, while the rows
themselves spanned four unrelated hardware classes — the label was actively
misleading. Here the two columns agree perfectly and therefore neither one
constrains the other. A reader who dedupes on `db_type` and a reader who dedupes
on `blob_subfamily` get the same 157 rows.

**`[I]`** The practical consequence: for `oled` there is no second opinion inside
the database. Anything wrong with the subfamily assignment is invisible to a
`db_type` cross-check, which is exactly why §5's cross-filing survived.

---

## 3. What the 33 filenames are

Classifying by controller token — the leading token after `LIMIT_`, skipping the
modifier tokens `NF`, `AGING`, `NEW`, `OLD`, `HBP`, `BOEB8`, `TEST`:

```
python3 -I -c "
import csv,collections
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
o=[r for r in rows if r['blob_subfamily']=='oled']
def ic(n):
    b=n.replace('LIMIT_','').replace('.img','')
    for t in b.split('_'):
        if t and t not in ('NF','AGING','NEW','OLD','HBP','BOEB8','TEST'): return t
    return b
agg=collections.defaultdict(lambda:[0,0,set()])
for r in o:
    k=ic(r['filename'].split('/')[-1]); agg[k][0]+=1
    agg[k][1]+=int(r['size_bytes']); agg[k][2].add(r['device'])
for k,(n,b,d) in sorted(agg.items(),key=lambda x:-x[1][0]):
    print(k,n,len(d),b)"
```

| controller | rows | devices | bytes | is it a display driver? |
|---|---:|---:|---:|---|
| ILI7807S | 51 | 8 | 1,283,544 | `[I]` Ilitek display DDIC |
| S3910 | 32 | 9 | 554,592 | `[I]` Samsung display DDIC |
| S3706 | 20 | 4 | 82,736 | `[I]` Samsung display DDIC |
| SY761 | 16 | 4 | 250,048 | `[I]` **Samsung touch IC** — see §5 |
| NT36672C | 8 | 4 | 294,112 | `[I]` Novatek, both display and touch parts |
| FT3681 | 8 | 4 | 162,944 | `[I]` FocalTech touch IC |
| ST80Y | 6 | 3 | 268,944 | `[I]` Sitronix display DDIC |
| FT3658U | 6 | 3 | 197,100 | `[I]` FocalTech touch IC |
| NT36523 | 4 | 4 | 469,248 | `[I]` Novatek |
| TD4377 | 4 | 4 | 104,512 | `[I]` Novatek/Analogix-class DDIC |
| NT36532 | 1 | 1 | 200,260 | `[I]` Novatek |
| NT36536 | 1 | 1 | 200,280 | `[I]` Novatek |

Totals reconcile to **157 rows / 4,068,320 B** across 12 controllers, 33 names.

Vendor attribution from the matrix (`oneplus` 125, `realme` 32) is the OEM, not
the silicon vendor — all 12 controllers here are third-party panel or touch ICs.

### 3.1 Size distribution contradicts "limit table" as a blanket reading `[F]`

```
min 4,108   median 20,368   max 200,280   sum 4,068,320
```

The median is a plausible config-table size and the minimum (4,108 B for
`LIMIT_S3706_SAMSUNG.img`) is tiny. But **`LIMIT_NT36536_HUAXING.img` is
200,280 B** and `LIMIT_NT36523_BOE.img` is 117,312 B — 5–10× the median, and
larger than several complete `FW_*` firmware images in the `touch` bucket.

So "`LIMIT_` is a small limit table" is true of the central tendency and false of
the tail. `[U]` What those two large files actually contain was not determined:
`LIMIT_NT36523_BOE.img` is on disk and decodes as an ordinary 20-record
`LIMITIMG`, but `LIMIT_NT36536_HUAXING.img` is not on disk (§9.2), so the
extremes were not byte-inspected.

### 3.2 The suffix family `[F]`

Treating `AGING`, `HBP`, `BOEB8`, `NEW`, `OLD` as orthogonal modifiers:

| suffix set | rows |
|---|---:|
| *(base)* | 121 |
| `NEW` | 12 |
| `AGING` | 8 |
| `HBP` | 7 |
| `OLD` | 4 |
| `AGING+HBP` | 3 |
| `HBP+BOEB8` | 1 |
| `AGING+HBP+BOEB8` | 1 |

`[I]` `AGING` is the only modifier with an obvious meaning for a panel artefact
(an accelerated-aging compensation table). `HBP` and `BOEB8` are unexplained
`[U]`, and I did not find a public expansion for either.

---

## 4. The `LIMIT_` split: 371 rows, two labels, zero overlap `[F]`

The sharpest structural fact about this bucket. Over **all** `LIMIT_` rows in the
matrix, not just `oled`:

```
python3 -I -c "
import csv,collections
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
lim=[r for r in rows if r['filename'].split('/')[-1].startswith('LIMIT_')]
print(len(lim), collections.Counter(r['blob_subfamily'] for r in lim))
byname=collections.defaultdict(set)
for r in lim: byname[r['filename'].split('/')[-1]].add(r['blob_subfamily'])
print(len(byname), sum(1 for v in byname.values() if len(v)>1))"
```

```
371 Counter({'touch': 214, 'oled': 157}) 47 0
```

- 371 `LIMIT_` rows.
- Exactly two subfamilies: `touch` 214, `oled` 157. **No third label.**
- 47 distinct filenames.
- **0** filenames appear under both subfamilies.

`371 = 214 + 157` exactly, and the 47 names partition cleanly into 14 `touch`
names and 33 `oled` names. There is no filename-level ambiguity anywhere in the
corpus.

### 4.1 So the label is a property of the name, decided once `[F]`

Combined with the row-level check from `other-fastchg.md` §3.1 (no
`(device, db_path, filename)` triple ever carries two subfamilies), the picture is:

- A `LIMIT_` filename has one subfamily, globally.
- Every row carrying that name inherits it.
- Nothing about the *path* or the *device* changes it.

That is the same mechanism `other-fastchg.md` §4 identified for `FW_` names. It
means the `oled`/`touch` boundary is decided entirely at the moment a filename is
first seen, and is never revisited.

### 4.2 The split tracks the controller — 18 of 19 pure `[F]`

Grouping all 371 `LIMIT_` rows by controller token:

```
controller  subfamily distribution
FT3518      {'touch': 50}                 PURE
GT9886      {'touch': 16}                 PURE
S3908       {'touch': 52}                 PURE
S6SY761     {'touch': 12}                 PURE
S6SY771     {'touch': 12}                 PURE
S6SY791     {'touch': 8}                  PURE
S6SY792     {'touch': 18}                 PURE
NT36672C    {'touch': 46, 'oled': 8}      SPLIT
ILI7807S    {'oled': 51}                  PURE
S3910       {'oled': 32}                  PURE
S3706       {'oled': 20}                  PURE
SY761       {'oled': 16}                  PURE
FT3681      {'oled': 8}                   PURE
ST80Y       {'oled': 6}                   PURE
FT3658U     {'oled': 6}                   PURE
NT36523     {'oled': 4}                   PURE
TD4377      {'oled': 4}                   PURE
NT36532     {'oled': 1}                   PURE
NT36536     {'oled': 1}                   PURE
```

**18 of 19 controllers are pure.** The 19th, `NT36672C`, splits 46 `touch` / 8
`oled` — and it splits on the *position* of the `NF` token, with no exceptions:

| filename | token order | subfamily | rows |
|---|---|---|---:|
| `LIMIT_NF_NT36672C_DSJM.img` | `NF` as prefix | touch | 17 |
| `LIMIT_NF_NT36672C_TIANMA.img` | `NF` as prefix | touch | 29 |
| `LIMIT_NT36672C_NF_JDI.img` | `NF` as infix | oled | 4 |
| `LIMIT_NT36672C_NF_BOE.img` | `NF` as infix | oled | 4 |

**54 of 54 rows** obey `NF`-prefix ⇒ `touch`, `NF`-infix ⇒ `oled`.

`[I]` `NF` plausibly abbreviates the panel maker (`NEW`-something, or a
Novatek-internal line code) but I found no public expansion and did not guess
one. What matters is that the subfamily follows the **spelling**, not any
property of the payload: the same controller `NT36672C` is `touch` or `oled`
depending on where a 2-character token sits in the filename.

`[N]` Note also that the `NF_` prefix is **not** a general rule:
`LIMIT_NF_ILI7807S_*` (51 rows) and `LIMIT_NF_TD4377_DSJM.img` are `oled`
despite carrying the same prefix. Only for `NT36672C` does the token position
correlate.

---

## 5. Two labels on one payload `[F]`

This is the defect that makes the bucket non-coherent, and it is provable
entirely from matrix columns — no payload access needed.

### 5.1 `SY761` ≡ `S6SY761`

| filename | subfamily | rows | devices | size | md5 |
|---|---|---:|---:|---:|---|
| `LIMIT_SY761_SAMSUNG.img` | **oled** | 4 | 4 | 15,628 | `16b6abb01521207896c3c42ed7bf0b67` |
| `LIMIT_S6SY761_SAMSUNG.img` | **touch** | 8 | 4 | 15,628 | `16b6abb01521207896c3c42ed7bf0b67` |
| `LIMIT_SY761_SAMSUNG_NEW.img` | **oled** | 4 | 4 | 15,628 | `837f580b3d939e64085e0047a8221dd9` |
| `LIMIT_S6SY761_SAMSUNG_NEW.img` | **touch** | 4 | 4 | 15,628 | `837f580b3d939e64085e0047a8221dd9` |

Identical md5, identical size, identical device set:

```
LIMIT_SY761_SAMSUNG.img    devices: OnePlus_7, OnePlus_7T, OnePlus_7T_Pro, OnePlus_7_Pro
LIMIT_S6SY761_SAMSUNG.img  devices: OnePlus_7, OnePlus_7T, OnePlus_7T_Pro, OnePlus_7_Pro
```

The payload is the same bytes. One filename calls it `oled`, the other `touch`,
and the matrix records both.

`[I]` `S6SY` is Samsung's touch-controller prefix; `SY761` is the same part
number with the prefix dropped. This is an **orthographic** difference — the
names differ only by whether the `S6` vendor prefix was written. That is
consistent with a file being ingested twice from two source trees where the
manufacturing name and the marketing name were used.

`[N]` I found no public document that states `SY761` and `S6SY761` are the same
part. The conclusion rests on the identical md5, size and device set in the
matrix, which is `[F]`, plus the prefix convention, which is `[I]`.

### 5.2 How much of `oled` does this affect `[F]`

```
md5s spanning both subfamilies: 2
oled rows on a cross md5:  16 / 157 (10.2%)
touch rows on a cross md5: 12 / 214 (5.6%)
oled bytes on a cross md5: 250,048 / 4,068,320 (6.15%)
```

Only 2 of the 42 distinct `oled` md5s are cross-filed, but they account for
**10.2% of `oled` rows** and **6.15% of its bytes** — because `SY761` rows are
spread over 4 devices each.

The other 8 md5s that carry more than one filename are all *within* one
subfamily — 6 are `oled` `S3910` `_HBP`/`_AGING` variants that are byte-identical
to their base, and 2 are `touch` `S3908` `_BOE`/`_SAMSUNG` pairs:

| md5 | subfamily | filenames sharing it |
|---|---|---|
| `23c0057e51`, `5292fa5f53`, `83eaecea6a` | oled | `S3910_TIANMA` + `S3910_TIANMA_HBP` |
| `a03d429370` | oled | `S3910_BOE` + `S3910_BOE_HBP` |
| `436285ab8d` | oled | `S3910_BOE_AGING` + `S3910_BOE_HBP_AGING` |
| `3431b213b5` | oled | `S3910_BOEB8_HBP_AGING` + `S3910_BOE_AGING` + `S3910_BOE_HBP_AGING` |
| `b399da0ed0` | touch | `S3908_BOE` + `S3908_SAMSUNG` |
| `c45cb8e334` | touch | `S3908_BOE_AGING` + `S3908_SAMSUNG_AGING` |

Those are **duplicate content under different names within one label** — a
distinct phenomenon from §5's mislabelling, and not evidence against the split.
The 6 `S3910` cases say that `_HBP` and `_AGING` modifiers frequently do not
change the bytes; the 2 `S3908` cases say the same for the panel-vendor token.

### 5.3 The cross-filed pairs are the only *inter*-subfamily collisions `[F]`

```
python3 -I -c "
import csv,collections
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
lim=[r for r in rows if r['filename'].split('/')[-1].startswith('LIMIT_')]
m=collections.defaultdict(set)
for r in lim: m[r['md5_db']].add(r['blob_subfamily'])
print(sum(1 for v in m.values() if len(v)>1), 'of', len(m))"
```

```
2 of 72
```

**2 of 72** distinct `LIMIT_` md5s span both subfamilies — and both are the
`SY761`/`S6SY761` pair. So the cross-filing is not a systemic bleed; it is one
specific duplicate with two names, recorded twice.

That is worth emphasising in the other direction too: the `oled`/`touch`
boundary is 97.2% clean at payload level. The problem is not that the split is
arbitrary across the board — it is that it is arbitrary *here*, and the database
has no mechanism to notice.

---

## 6. A `LIMIT_` payload is a touch-test config `[F]`

The direct content evidence. Two files, not `.img` but `.ini`:

```
…/larry/tree-odm/firmware/tp/21629/LIMIT_NF_ILI7807S_DSJM.ini   47,026 B
…/larry/tree-odm/firmware/tp/2162B/LIMIT_NF_ILI7807S_DSJM.ini   47,026 B
md5 (both) = 89c522a2ea79…
```

Both are byte-identical, 758 lines of UTF-8 text:

```
[PV5_4 Command]
Protocol=0506
Date=2021/09/23 10:22:06
Version=2.0.5
Timing_Info_Raw=03,A3,F1,29,F1,30,00,08,20,02,01,00,14,00,96,FF,…
Timing_Info_Value=1441435692331708657,241,48,0,2080,2,1,20,150,255,100,…
Noise Peak to Peak(IC Only)=0xF1,0x1D,0x01,0x00,0x96,0xF0,0x0A,0xFF,…
```

### 6.1 What the sections are `[F]`

59 section headers, and they name a capacitive touch panel's production tests:

```
[PV5_4 Command]              [Get MP Threshold]       [Program Customer Data]
[Host Download]              [FW Upgrade]             [FW Ver. Check]
[Noise Peak to Peak(IC Only)]
[Noise Peak To Peak(With Panel)]
[Noise Peak To Peak(With Panel) (LCM OFF)]
[Doze Peak To Peak]          [Peak To Peak_TD (LCM OFF)]
[Short Test]                 [Open Test_C]            [Pin Test ( INT and RST )]
[Calibration Data(DAC)]
[Raw Data(Have BK)]          [Raw Data(No BK)]        [Doze Raw Data]
[Node Type]
```

The vocabulary is unambiguous: **TX/RX nodes**, **open/short tests**, **noise
peak-to-peak with the panel on and off**, **DAC calibration**, **pin test on INT
and RST**. These are capacitive-touchscreen manufacturing tests. No section is
named `Gamma`, `Display`, `OLED` or `LCD`, and no section is a `VCOM` curve — a
display-driver limit table would be built from those, not from open/short tests.
(The string `VCOM` does occur exactly once, as a bare `VCOM=4` key at line 270,
not as a section and not as a curve.)

Keyword census over the 758 lines:

| keyword | occurrences |
|---|---:|
| `Panel` | 28 |
| `LCM` | 24 |
| `TX` | 9 |
| `VCOM` | 1 |
| `Node` | 1 |
| `Touch` | **0** |
| `Display` | **0** |
| `OLED` | **0** |
| `LCD` | **0** |
| `RX` | **0** |
| `Sensor` | **0** |
| `DDIC` | **0** |
| `Gamma` | **0** |

`[I]` The file never uses the word "touch" — but it counts TX nodes, runs open
and short tests, and calibrates DAC against panel noise. That is a touch
controller's test suite. A display DDIC limit table would not have an
`Open Test_C` or a `Short Test`; it would have gamma and common-voltage curves,
of which there are none.

### 6.2 The `.img` and the `.ini` are the same artefact in two encodings `[F]`

`LIMIT_NF_ILI7807S_DSJM` exists as `.ini` in directories `21629` and `2162B`, and
as `.img` in `21341` and `21707`. The `.img` form is a `LIMITIMG` container with
15 `OPPO` records:

```
img 25,980 B, 15 records, le32@0x08 = 0x3e7fe = 255,998
rec0  @0x004c span=132   OPPO  body=01 00 00 00 cc 00 00 00 …
rec7  @0x0550 span=4860  OPPO  body=0a 00 03 00 4c 06 00 00 …
```

`[N]` The `.ini`'s `0xF1`-prefixed command opcodes (`0xF1,0x01`, `0x04`, `0x05`,
`0x08`, `0x1D`, `0x32`, `0x33`) could not be matched into the `.img` records: only
`0xF1,0x08` occurs as a byte pair. **So I cannot show that the `.img` is a compiled
form of the `.ini`.** What I can show is that they are the same *name*, the same
*artefact class* (both named `LIMIT_`), and that one is text and one is binary.
The relationship between the two encodings is `[U]`.

### 6.3 The database cannot see `.ini` files at all `[F]`

```
python3 -I -c "
import csv,collections
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
print(sum(1 for r in rows if r['filename'].lower().endswith('.ini')))"
```

```
0
```

**Zero** of 33,917 rows carry an `.ini` filename. The extension census of the
matrix is `bin` 5,984, `img` 2,914, `mdt` 1,772, `b01`–`b06` in the thousands —
no text formats at all.

So the coverage matrix records a `.ini` file's *sibling* but never the `.ini`
itself. Two consequences:

1. The `LIMIT_` population in the matrix (371 rows) is **incomplete** — two
   `LIMIT_` artefacts on disk in one device tree alone are missing.
2. More importantly for this issue: **the only file in the corpus that states in
   plain text what a `LIMIT_` artefact is for, is the one file type the database
   does not ingest.** The classification had no access to the clearest evidence
   about its own correctness.

---

## 7. `LIMITIMG` — reproduced, not re-derived `[F]`

`research/fleet/other-touch.md` §6 decoded this container on `larry`'s 41 files.
I reproduce it here independently, and extend it to all **56** files in the
workspace (the 41 plus 15 from `instantnoodle`), because this issue's population
is `oled` and because my own `other-fastchg.md` §7.1 got it wrong (§8).

### 7.1 The decode, re-derived `[F]`

```
LIMITIMG  <le32 @0x08>  <zero @0x0c>  <offset table at 0x10>
count = (le32@0x10 − 0x10) / 4
```

All 56 on-disk `LIMIT_*.img` files carry the `LIMITIMG` magic — no other container
appears — and every check passes on the whole set:

| check | `larry` (41) | all on disk (56) |
|---|---|---|
| magic `LIMITIMG` | 41 / 41 | **56 / 56** |
| `table[0] == 0x10 + 4 × count` | 41 / 41 | **56 / 56** |
| offset table monotonic | 41 / 41 | **56 / 56** |
| record span `le32@rec+4 == next − this` | 408 / 408 | **483 / 483** |
| last record ends exactly at EOF | 41 / 41 | **56 / 56** |
| **records** | **449** | **539** |
| record magics | `OPPO` 367, `SLPO` 82 | `OPPO` **454**, `SLPO` **85** |

Per-file record counts over all 56: `3×8, 5×3, 6×1, 7×11, 8×2, 10×7, 12×11,
14×1, 15×11, 20×1` — still **no file has 11 records**, the false assumption that
produced the retracted "24/41".

On `larry`'s 41 files this matches `other-touch.md` §6.2 on every figure — 41/41,
449 records, `OPPO` 367 / `SLPO` 82 — and the per-controller constants at
`le32@0x08` match §6.4 too (`FT3518` 382, `FT3681` 510, `GT9886` 62, `ILI7807S`
255,998, `NT36672C` 8,190, `S3910` 2,046, `TD4377` 254, `NT36523` 2,097,150).
The 15 `instantnoodle` files add 90 records on the same rules.

`[U]` Record layout beyond `magic(4) + span(4)` — same status as
`other-touch.md` §6.3. `[F]` `SY761` and `S6SY761` have no `LIMITIMG` on disk, so
their byte-identical status rests on the matrix md5s (§5.1), not on a decode.

### 7.2 A hypothesis that failed `[F]`→`[N]`

Given two record magics and two subfamilies, the obvious hypothesis is that they
correspond. They do not:

| matrix subfamily | files (56) | record-magic mix |
|---|---:|---|
| `oled` | 16 | all-`OPPO` 12, all-`SLPO` 4 |
| `touch` | 40 | all-`OPPO` 33, all-`SLPO` 7 |

Testing "all-`OPPO` ⇒ `oled`, all-`SLPO` ⇒ `touch`":

```
all 56 files:    exceptions 37 of 56
larry only (41): exceptions 23 of 41
```

**37 of the 56 files contradict it** (23 of `larry`'s 41), in both directions —
e.g. `LIMIT_NF_ILI7807S_JDI.img` is all-`SLPO` and labelled `oled`, while
`LIMIT_NF_NT36672C_DSJM.img` is all-`OPPO` and labelled `touch`. At file level
the magics never mix (45 files all-`OPPO`, 11 all-`SLPO`, **0** mixed), yet both
labels use both magics: 33 of 40 `touch` files and 12 of 16 `oled` files are
all-`OPPO`.

`[N]` Record magic is therefore **not** a subfamily discriminator. Both labels
use both magics, in comparable proportion (`oled` 12/16 = 75% `OPPO`, `touch`
33/40 = 82.5% `OPPO`). I record this as a refuted hypothesis rather than dropping
it, because "two magics, two labels" is exactly the kind of coincidence a less
careful report would have presented as a finding.

---

## 8. Rule 1 corrections owed

### 8.1 To my own `other-fastchg.md` §7.1 — applied in place `[F]`

`other-fastchg.md` §7.1 asserted that `LIMITIMG`'s table was "11 little-endian
`u32` offsets" and that the format validated on "**24 of 41** files", concluding
the container was "only partly decoded".

That is **wrong**, and the error was mine. I had assumed a fixed 11-entry table
instead of reading the count. The count is declared at `0x10` and varies per
file; **no file has 11 records** (counts are 5, 7, 8, 10, 12, 14, 15, 20). On the
correct rule the container closes 41/41 with 408/408 record spans.

`other-touch.md` §6 had this right before my note existed. I have corrected
§7.1 in place, added a dated correction notice there, and amended the two other
places in that file that repeated the figure (§9.1's "only partly decoded" list
and §10 item 4). The `/docs/REPO-STATE-MAP.md` row for `fastchg` is corrected
from "only partly decoded 24/41 `[N]`" to "`41/41` structural checks / 449
records `[F]`".

This is a correction of my own work, not of a prior author's — the distinction
matters for Rule 1, and I state it rather than leaving the two files
contradicting each other.

### 8.2 To `other-touch.md` — nothing owed `[F]`

I re-measured every `other-touch.md` claim that touches this material:

| claim | re-measured | verdict |
|---|---|---|
| panel `FW_*`/`LIMIT_*` = 660 rows / 73,886,385 B | 660 / 73,886,385 for `blob_subfamily=touch` | **correct**, and correctly scoped to that subfamily |
| `LIMITIMG` 41/41, 449 records, `OPPO` 367 / `SLPO` 82 | identical | **correct** |
| `le32@0x08` per-controller constants | identical | **correct** |
| `21221/LIMIT_FT3518_SAMSUNG.img` corrupt at `le32@0x08` (`0x17e0017e`) | reproduced: `400556414` | **correct** |
| `_FAE` spans 6 container formats | `other-fastchg.md` §7 extends it | **correct** |

No edit to `other-touch.md` was warranted, so none was made. Its 660-row figure
is right *for its own subfamily*; the fact that 157 further `LIMIT_` rows sit in
`oled` is a gap in that note's scope, not an error in its arithmetic — and
`other-touch.md` never claims to cover the corpus.

---

## 9. Honest negatives

### 9.1 No in-tree consumer and no public spec for `LIMITIMG` or `PV5_4` `[N]`

- `torvalds/linux`: the strings `LIMITIMG` and `PV5_4 Command` do not appear in
  `drivers/gpu`, `drivers/input/touchscreen`, or `drivers/video`. There is no
  parser in-tree; these payloads are read by a vendor factory or update daemon.
- The `0xF1`-prefixed command family in the `.ini` is not a documented mainline
  protocol. Mainline touch drivers (`ilitek_*`, `novatek*`, `focaltech*`) exist
  but none reads this artefact.
- Web search for `"PV5_4" "Timing_Info_Raw"` returns **0** results. Web search
  for `LIMITIMG OPPO panel` returns nothing relevant.

So §6's reading of the `.ini` is from its own section names and key vocabulary
(open/short/TX/noise/DAC), not from documentation. That is why it is marked
`[I]` where it interprets and `[F]` where it counts.

### 9.2 Only part of the `oled` population has payloads on disk `[N]`

The workspace holds **56** `LIMIT_*.img` files — 41 in `larry`'s `firmware/tp/`
and 15 in `instantnoodle`'s — but they are only **19 distinct filenames**:

| tree | files | distinct names | `oled` names covered | `oled` rows | bytes |
|---|---:|---:|---:|---:|---:|
| `larry` | 41 | 14 | 9 / 33 | 74 | 2,152,624 |
| `instantnoodle` | 15 | 6 | 0 / 33 | 0 | 0 |
| both | 56 | 19 | **9 / 33** | **74 / 157** | **2,152,624 / 4,068,320** |

So the byte-level evidence covers **47.1% of `oled` rows and 52.91% of its
bytes**, all from `larry` — `instantnoodle`'s 15 files are entirely `touch`
names. **24 `oled` filenames have no payload on disk at all.** Specifically:

- `SY761` and `S6SY761`, the §5 defect, have **no file on disk in either tree**.
  That finding is entirely from the matrix's `md5_db` column. `[N]`
- Of the two size outliers in §3.1, `LIMIT_NT36523_BOE.img` (117,312 B) **is** on
  disk — one copy in `larry/…/21653`, decodes 20/20 as `LIMITIMG` with 20 `OPPO`
  records — while `LIMIT_NT36536_HUAXING.img` (200,280 B) is not. `[N]`
- All 56 on-disk `LIMIT_*.img` files are `LIMITIMG`; none is another container.

So the byte-level claims in §7 rest on `larry`'s 41 files; the classification
claims in §4–§5 rest on matrix columns for 371 rows. I have kept those two
evidentiary bases labelled separately throughout rather than implying 371
payloads were inspected.

### 9.3 The `.ini` and `.img` relationship is unresolved `[U]`

§6.2. I could not map the `.ini`'s `0xF1` opcodes into the `.img`'s `OPPO`
records (1 of 7 byte-pairs matched, which is consistent with chance). So "the
`.img` is the compiled form of the `.ini`" is a plausible reading I am **not**
asserting.

### 9.4 No ISA, no interface, no sha256 `[N]`

`isa_identified` blank on **157/157**; `interface_documented=n` on **157/157**;
`sha256_if_listed` absent on **157/157**; `soc` blank on 36/157.

The `LIMITIMG` record bodies are configuration data, not code — there is no
vector table, no entry point and no plausible ISA question to answer for the 56
files I have. `[U]` Whether the one 200 KB outlier that is absent from disk
(`LIMIT_NT36536_HUAXING.img`) contains code was not determined; the 117 KB
`NT36523_BOE` file that is on disk carries configuration records, not a vector
table.

### 9.5 Report-only: the defect is not fixed

The `SY761`/`S6SY761` cross-filing (§5) is **reported, not fixed**. Re-labelling
would mean deciding, for 16 `oled` rows and 12 `touch` rows, which of two
identical payloads is the "real" subfamily — and that decision propagates into
`other-touch.md`'s published 214 `LIMIT_` rows and 660 total. It needs an owner,
not a drive-by edit. Same for the two `.ini` files that the matrix cannot ingest
(§6.3): adding them changes the census methodology, not just a row.

---

## 10. Method

1. **Census from the CSV only.** §1–§5 are reproducible from
   `coverage-matrix.csv` with stdlib `csv` + `collections`, with no payload
   access. Every table is pasted command output.
2. **The `db_path` leaf as an independent axis.** All 157 rows sit at
   `firmware/tp/`, the directory `other-touch.md` establishes as touch/panel
   firmware. That is the first sign the bucket's label is not about the
   directory.
3. **Name-level partitioning before interpretation.** Counting
   `(name → set(subfamily))` and getting 47 names / 0 multi-subfamily names
   (§4) establishes that the label is a property of the filename. Only then does
   it make sense to ask *which* property, which is §4.2's controller grouping.
4. **Identity by md5, not by name.** §5 exists because I grouped on
   `(device, md5, size)` rather than trusting filenames. Two filenames sharing an
   md5 on the same device is the whole finding, and it is invisible if you group
   by name.
5. **Prior art reproduced, not assumed.** `LIMITIMG` was re-decoded from the
   files (§7.1) rather than cited, which is how the 41/41-versus-my-24/41
   discrepancy surfaced. Reproducing is what caught my own error; citing would
   have left two notes contradicting each other.
6. **Hypotheses are tested and their failures reported.** §7.2 tests
   `OPPO`/`SLPO` against the labels, gets 37/56 exceptions (23/41 in `larry`),
   and records the refutation. §6.2 states the `.ini`→`.img` mapping as `[U]`
   rather than inferring it.
7. **Two evidentiary bases kept separate.** §9.2 states plainly that §7's byte
   claims cover `larry`'s 41 files (74 `oled` rows, 47.1%) and §4–§5's
   classification claims cover 371 matrix rows, and that the §5 defect rests on
   matrix columns alone because no file exists on disk for it.
8. **Rule 1 checked in both directions.** §8.1 corrects my own prior note in
   place; §8.2 records that nothing in `other-touch.md` needed correcting, with
   each claim re-measured.
