# xiaomi Poco_F5 (marble) — `tz` family: 91 rows, 83 md5, and the 8-file gap is one ELF alias

Analysis date 2026-11-24. Analyst: OC-3 (issue [#1796](https://github.com/adineo-cmd/open-device/issues/1796)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows),
`device-inventory.csv` (249 rows).

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art

**The `b03`/`b07` alias is already documented, and I am not claiming it.**

[`research/fleet/other-fingerprint.md:281-297`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/fleet/other-fingerprint.md)
establishes, on the **`fingerprint`** family and from *decoded payloads*:

> `devices where md5(b03) == md5(b07): 20` / `phnum=9 devices: 20` / `identical set: True`
>
> `phdr[3]` and `phdr[7]` share the same `(p_offset, p_filesz)` pair in **16 of 16**, with
> `phdr[3].p_type = 1` (PT_LOAD) and `phdr[7].p_type = 0x6474e552` (`PT_GNU_PROPERTY`). The
> loader therefore emits `b03` and `b07` from the same bytes.

That is the mechanism, decoded, and **this note cannot improve on it** — there are no bytes here.
What §4.4 does *not* do, and what this note adds, is §2–§4 below: the law stated in a form that
is testable across a whole family, the proof that it does **not** generalise on the naive
predictor, and the segment census that makes the exceptions legible.

Other prior art, none on this device:

- `research/fleet/tz-hyp.md` — 63 rows / 63 devices, 3 MBN payloads decoded (hypervisor scope).
  **0 `Poco_F5` hits.**
- `research/qualcomm/docs/trustzone-census.md` — FP6 only. **0 `Poco_F5` hits.**
- `research/fleet/dsp-tz-map.md` — QSEE ELF64 segment map. **0 `Poco_F5` hits.**
- `docs/devices/oneplus/OnePlus_7/tz.md:87` and `motorola/Edge_30/tz.md:40` — both state the
  `mdt + b00..b07` (8-part) split grammar. Neither mentions `b08` or an alias.

## Verdict

`Poco_F5` (`marble`) has **91 `tz` rows / 8,895,181 B / 91 distinct filenames / 83 distinct
md5**. That is **2.13%** of the `tz` family's 4,264 rows. All 91 are
`db_path = xiaomi/marble/radio`, `isa_identified` empty, `sha256_if_listed` empty on **91/91**,
`priority = P3`.

The 14 basenames decompose three ways:

| shape | basenames | rows |
|---|---|---:|
| monolithic `.img` | `tz` (3,911,680 B), `hyp` (1,257,472), `keymaster` (372,736), `uefisecapp` (176,128), `devcfg` (57,344) | 5 |
| 9-segment `mdt + b00..b08` | `hdcp1`, `hdcp2p2`, `hdcpsrm`, `loadalgota64`, `smplap64`, `soter64`, `sp_license` | 63 |
| 10-file `mdt + b00..b08 + img` | `featenabler` | 11 |
| 5-segment `b00..b04` (no `mdt`, no `.img`) | `cpusys_vm` | 5 |

> **The headline.** 91 rows but only **83 distinct md5** — and the gap is not noise. It is
> **exactly 8**, one per aliased basename, and on this device `md5(b03) == md5(b07)` for all
> eight. The same identity holds on **190 of 385** basenames fleet-wide, and it is **not**
> scattered: it is decided per **device**, **22 devices fully aliased and 27 not at all, zero
> mixed**. The predictor is not "nine-part device" — it is whether the set carries a `b08`
> segment, and in `tz` that equivalence holds **385/385**. On the `other` family the same test
> fails **58** times, which is the part a single-family study could not see.

## 1. The 91 rows, and the 8-row gap

[F] The row/md5 arithmetic closes exactly:

```
rows                 91
distinct md5         83
rows - md5            8
aliased basenames     8
```

[F] The eight aliased basenames on this device, with the shared md5 and the duplicated size:

| basename | `b03` = `b07` (B) | md5 |
|---|---:|---|
| `smplap64` | 8,880 | `266d005795c36264de720e05f157c881` |
| `hdcp2p2` | 1,768 | `d5848349ef157284e7fd5c7d9d7e9d8c` |
| `soter64` | 1,048 | `6a4f1a550428afcd0ff594e6341701ef` |
| `hdcp1` | 536 | `0d01a732e8c78c7133cb0a5406342e64` |
| `featenabler` | 472 | `d27cbc578e6550b1e3df76b5f80bc88f` |
| `hdcpsrm` | 472 | `a016fa2c5103c6bab202619c8c4b999f` |
| `loadalgota64` | 424 | `6bc2768cd1016d970aa9d5a07e8ff5df` |
| `sp_license` | 408 | `bc8e0217773bbab8f14507c08e48b4e2` |

[F] **No other md5 collision exists in the file** — the 83 is 91 minus exactly these 8, with
0 residual. `14,008 B` of the device's 8,895,181 B (0.16%) is byte-duplicated by the alias.

[F] Fleet-wide the alias is expensive: **190 aliased pairs, 335,160 B** of the family's
**665,173,154 B** — 0.05%. Poco_F5 carries 4.2% of the duplicated bytes.

[I] Consequence for counting: **a per-device `tz` blob count overstates distinct content by one
per aliased basename.** Any "rows = builds" or "rows = distinct payloads" statement about this
family is wrong on the 190 aliased pairs, and right on the 195 non-aliased ones.

## 2. The law in `tz` is exact — four equivalent forms, zero violations

[F] Over the **385** `(device, basename)` pairs in the `tz` family that carry both a `.b03` and a
`.b07`:

| form of the law | holds |
|---|---|
| `b03 == b07` **⇔** the set carries a `b08` segment | **385 / 385** |
| `b03 == b07` **⇔** `size(b03) ≥ 300 B` | **385 / 385** |
| `b03 == b07` **⇔** device is in the "EQ" class (§3) | **385 / 385** |
| `size(b03) == size(b07)` **⇒** `md5(b03) == md5(b07)` | **190 / 190** |

[F] The size threshold is a **hard gap, not a tuned cut-point**:

```
EQ pairs (b03 == b07) : n=190, b03 size 408 .. 10,760 B   (min 408)
NE pairs (b03 != b07) : n=195, b03 size 130 ..    252 B   (max 252)
```

There is no pair between 252 B and 408 B. The two populations are separated by a void, which is
what makes a threshold expressible at all. [N] I did **not** find a mechanism for the 300-B
boundary — no payload was opened. [OPEN]

[F] The size equality is the *mechanism-free* half of the alias: `size(b03) == size(b07)` on
**190 of 385**, and on those 190 the md5s agree **190/190**. So wherever the loader emits the
same byte count for the two segments, it emits the same bytes.

[I] This is consistent with §4.5 of the fingerprint note (one `(p_offset, p_filesz)` pair served
to two headers) and does not extend it: on `tz` the two segments are equal *in length* in the
aliased case, which is what one shared `p_filesz` implies.

## 3. The split is per device, and perfectly binary

[F] Grouping the 385 pairs by device: **every device is all-or-nothing.**

```
devices where all pairs alias  : 22
devices where no pair aliases  : 27
devices mixed (some/some)      :  0
```

[F] The two classes, in full:

| EQ — all pairs alias (22) | NE — none alias (27) |
|---|---|
| `Edge_40_Pro`, `FP6`, `Mi_12`, `Mi_12S`, `Mi_12S_Pro`, `Mi_12S_Ultra`, `Mi_12T_Pro`, `Mi_12_Pro`, `Mi_13`, `Mi_13_Pro`, `Nord_4`, `Nord_CE4`, `OnePlus_11_5G`, `OnePlus_12`, `OnePlus_13`, `Pad_2_Pro`, `Pad_Pro`, `Phone_2`, `Poco_F5`, `Poco_F5_Pro`, `Poco_F6_PRo`, `Redmi_K60_Pro` | `Edge_30`, `Edge_30_Fusion`, `Edge_30_Neo`, `FP4`, `FP5`, `G_Stylus_5G-2-2022`, `Mi_A3`, `Moto_G200`, `Moto_G34_5G`, `Moto_G82_5G`, `Moto_G84_5G`, `Moto_G_5G_2024`, `Nord_CE2`, `Nord_CE3`, `OnePlus_7`, `OnePlus_7T`, `OnePlus_7T_Pro`, `OnePlus_7_Pro`, `OnePlus_8`, `OnePlus_8_Pro`, `OnePlus_9`, `OnePlus_9RT`, `OnePlus_9_Pro`, `Phone_1`, `Pro_1X`, `Realme_10_Pro`, `Realme_9_Pro` |

[F] And the class is *exactly* the `b08`-presence class, at device level too:

```
EQ devices, any set with b08 : 22 / 22
NE devices, any set with b08 :  0 / 27
```

[I] This is a property of the **TA build generation** that produced the split image, not of the
device's SoC or vendor: the EQ class is 12 xiaomi, 7 oneplus, and one each of fairphone /
nothing / motorola, while NE is 9 motorola, 11 oneplus, 2 realme, 2 fairphone, and one each of
xiaomi / nothing / fxtec. **Every vendor except realme and fxtec appears in both classes**, so
vendor is not the axis. [N] I cannot name the axis — there is no build ID or version string in
the matrix. `other-fingerprint.md:309-311` reaches the same conclusion for the sibling family
("tracks TA build generation, which is `[U]` here"). [OPEN]

## 4. "Nine-part device" is the wrong predictor — the `other` family proves it

This is the part that generalises beyond what a single-family study can see.

[F] Running **the identical test** on the `other` family (561 pairs, which includes the
`fingerprint` family):

| family | pairs | law holds | violations |
|---|---:|---:|---:|
| `tz` | 385 | **385** | **0** |
| `other` | 561 | 503 | **58** |

[F] The 58 violations are concentrated in identifiable basenames:

| basename | violations |
|---|---:|
| `venus` | 26 |
| `slpi` | 19 |
| `evass` | 3 |
| `vpu20_4v`, `brhbtnv10`, `gngbtnv10`, `cvpss` | 2 each |
| `slpi2`, `vpu20_1v` | 1 each |

[F] The failure mode is **not** "no `b08`". Every sampled violation has `b08` and still has
`b03 ≠ b07`:

```
Moto_E7_Plus  venus      b03=   20  b07=   24  has_b08=True
Moto_G200     evass      b03=    8  b07=   24  has_b08=True
Moto_G200     slpi       b03=1454152 b07=371036 has_b08=True
Pad_2_Pro     brhbtnv10  b03=11569  b07=11673 has_b08=True
```

[I] So in `other`, "the set has a `b08`" does **not** imply the alias, whereas in `tz` it does,
385/385. The law is a **family property**, not a segment-count property. Stated as a rule for a
future census:

> In `tz`, `b08`-presence ⇒ `b03`/`b07` alias, exactly. In `other`, it does not — 58
> counterexamples, all with `b08`. Do not generalise the fingerprint note's §4.4 to any family
> without re-running it.

[I] A second reading is available from the same table: the `tz` violations are 0 because the
`tz` sets are *uniformly* generated (a 9- or 10-file scheme with a fixed header layout), while
the `other` bucket is a catch-all that mixes `venus`/`slpi`/`evass` — different firmware
subsystems entirely — under one family label. That would make the "family" a filing artefact
here, which is itself worth knowing. [OPEN]

## 5. Segment census of the `tz` family

[F] Grouping every `tz` row into `(device, basename)` sets by suffix:

| files in set | sets | shape |
|---|---:|---|
| 9 | **183** | `mdt + b00..b07` |
| 10 | **181** | 169 × `mdt + b00..b08`; 12 × `mdt + img + b00..b07` |
| 11 | 21 | `mdt + img + b00..b08` |
| 8 | 14 | 8-segment, no `mdt` |
| 5 | 9 | 5-segment, no `mdt` |
| 4 | 11 | 4-segment, no `mdt` |
| 2, 1 | 3, 365 | `.mdt`+`.img`, monolithic |

[F] All **385** `b07` sets are contiguous `b00`–`b07` — no set has a `b07` with a gap.

[F] The **34** basenames that carry a `b03` but **no** `b07` are not truncations; they are the
short chains:

```
segment counts of b03-without-b07 sets: {4, 5, 8}
b03 size range: 2,760 .. 16,320 B
basenames: cpusys_vm (4-5 segments), cmnlib / cmnlib64 (6-8 segments)
```

[I] The `b03` in a 4-segment set is a *different logical segment* from the `b03` in a 9-segment
set — which is exactly the warning `other-fingerprint.md:277-279` gives for the sibling family
("the same filename carries a different segment in the two classes"). Any per-index role table
must be conditioned on the set's segment count.

[F] `Poco_F5`'s own sets, confirming the shapes above: `cpusys_vm` 5 files; `featenabler` 11
(`mdt`+`img`+`b00`–`b08`); `hdcp1`/`hdcp2p2`/`hdcpsrm`/`loadalgota64`/`smplap64`/`soter64`/
`sp_license` 10 each (`mdt`+`b00`–`b08`); and `tz`/`hyp`/`keymaster`/`uefisecapp`/`devcfg`
monolithic `.img`.

## 6. `db_type` does not track the segment role

[F] Across the 91 rows there are 8 `db_type` values, and the membership is **mostly by basename
with three documented exceptions**:

| `db_type` | rows | membership |
|---|---:|---|
| `DRM` | 27 | `hdcp1.b00`–`.b08` (9), `hdcp2p2` (9), `hdcpsrm` (9) — **segments only, not `.mdt`** |
| `UNKNOWN` | 19 | `featenabler.b01`–`.b08` + `.img` (9), `loadalgota64.b01`–`.b08` (8), `devcfg.img`, `uefisecapp.img` |
| `SECURITY` | 15 | `smplap64.b00`–`.b08` (9), `cpusys_vm.b00`–`.b04` (5), `keymaster.img` |
| `FINGERPRINT` | 10 | all 9 `soter64.*` **plus `soter64.mdt`** |
| `ELF64` | 9 | 7 of the 8 `.mdt` + `featenabler.b00` + `loadalgota64.b00` |
| `CERT` | 9 | all 9 `sp_license.b00`–`.b08` |
| `BOOT` | 1 | `tz.img` |
| `SECUREBOOT` | 1 | `hyp.img` |

[F] The `.mdt → ELF64` rule is **7 of 8, not 8 of 8** — `soter64.mdt` is `FINGERPRINT`,
inherited from its basename rather than its container format. So the classifier applies the
basename's functional bucket *over* the container format in exactly one case, and the format in
the other seven. [I] That inconsistency is the useful part: it shows `db_type` is computed from
the basename, with at least one override, and is not a per-file-format determination.

[F] The DRM basenames make this concrete: `hdcp1.mdt`, `hdcp2p2.mdt`, `hdcpsrm.mdt` are
`ELF64` while **all 27** of their `.b00`–`.b08` segments are `DRM`. The same basename is typed
two ways depending on whether the suffix is `.mdt`.

[F] **`featenabler.b00` and `loadalgota64.b00` are `ELF64`** while every other `*.b00` is typed
by function — `cpusys_vm`/`smplap64` `SECURITY`, `soter64` `FINGERPRINT`, `sp_license` `CERT`,
`hdcp1`/`hdcp2p2`/`hdcpsrm` `DRM`. And `featenabler.b08` is `UNKNOWN` while `featenabler.b00` is
`ELF64`, so within one basename the two `ELF64`-ish segments are typed differently. [I] `b00`
probably *is* an ELF header (which would make `ELF64` correct there and the functional labels
the approximations), but I did not open a file and cannot assert it. `[OPEN]`

[F] `tz.img` — the principal TrustZone image, 3,911,680 B, the largest row on the device — is
typed **`BOOT`**, the same label `boot.img` carries in the `boot` family.

[N] The `BOOT` on `tz.img` is implausible as a function label and I flag it, but I did **not**
open the file, so I cannot say what it is. `SECUREBOOT` on `hyp.img` is at least shape-consistent
with the prior art's framing. `[OPEN]`

[F] `db_type` is not multi-valued per filename here: in the `tz` family, **171 filenames, 0 with
more than one `db_type`**. Same as `boot` (26 / 0) and `gpu` (86 / 0) in the sibling notes.

## 7. Honest negatives

1. **No blob was fetched or parsed.** Every claim is a property of the matrix columns
   `filename`, `size_bytes`, `md5_db`, `db_type`, `db_path`, `device`. In particular I did
   **not** open any `.mdt`, so I have no `phdr` offsets, no `p_type`, and no way to confirm the
   ELF mechanism §2 borrows from prior art.
2. **No independent hash.** `sha256_if_listed` is empty on **91/91** rows and
   `isa_identified` is empty on 91/91. The single `md5_db` column is the only witness, so
   "aliased" here means *the database says the two md5s match* — a claim about the DB, and only
   transitively about bytes.
3. **The alias mechanism is not re-derived.** `other-fingerprint.md:292-297` gives
   `phdr[3]`/`phdr[7]` sharing `(p_offset, p_filesz)` from 16 decoded ELFs. I cite it; I did not
   verify it. My §2 size-equality observation is *consistent* with it, not proof of it.
4. **The 300-B threshold has no mechanism.** I can state it and show the void between 252 B and
   408 B, but I cannot say what makes a 408-B `b03` a shared block and a 252-B one not.
5. **The EQ/NE axis is unidentified.** Not vendor (every major vendor appears in both), not
   `soc` (19 of 22 EQ devices have blank `soc`, so the axis is not testable there either), not
   matrix generation. Prior art on the sibling family also stops at "build generation, `[U]`".
6. **`b08` is not a general alias predictor** — 58 counterexamples in `other`. Any downstream
   doc that adopts "nine-part ⇒ b03/b07 alias" from `other-fingerprint.md` §4.4 will be wrong
   for `venus`/`slpi`/`evass`. That is the practical warning this note exists to give.
7. **`cpusys_vm`'s 5-segment form is unexplained.** It has no `.mdt` and no `.img` on this
   device, unlike every other basename. Whether that is a different container or a census gap
   is not decidable here. `[OPEN]`
8. **`tz.img` typed `BOOT`** is flagged but not adjudicated (§6).
9. **Web search unavailable.** `websearch` returned **HTTP 402**; `gh search` returned empty
   for both code and repo queries on 2026-11-24. Recorded in the SEARCH comment; no claim here
   depends on external prior art.

## 8. Reproduce

```bash
# run from the repo root
M=upstream-contribution/blob-database/coverage-matrix.csv

# the 91 rows / 83 md5 / 8-row gap (section 1)
python3 -I -c "
import csv
r=list(csv.DictReader(open('$M')))
t=[x for x in r if x['device']=='Poco_F5' and x['blob_family']=='tz']
print(len(t), len({x['filename'] for x in t}), len({x['md5_db'] for x in t}), sum(int(x['size_bytes']) for x in t))
"
# expect: 91 91 83 8895181

# the 8 aliased basenames on this device (section 1)
python3 -I -c "
import csv
r=list(csv.DictReader(open('$M')))
t=[x for x in r if x['device']=='Poco_F5' and x['blob_family']=='tz']
m={x['filename']:(int(x['size_bytes']),x['md5_db']) for x in t}
al=[(b,m[b+'.b03'][0]) for b in sorted({f.rsplit('.',1)[0] for f in m})
    if b+'.b03' in m and b+'.b07' in m and m[b+'.b03'][1]==m[b+'.b07'][1]]
print(len(al), sum(s for b,s in al))
"
# expect: 8 14008

# the four forms of the law, 385/385 (section 2)
python3 -I -c "
import csv,re
from collections import defaultdict
r=list(csv.DictReader(open('$M')))
t=[x for x in r if x['blob_family']=='tz']
g=defaultdict(set); d=defaultdict(dict)
for x in t:
    mm=re.match(r'^(.*?)\.(mdt|img|b\d\d)\$',x['filename'])
    if mm: g[(x['device'],mm.group(1))].add(mm.group(2))
    if x['filename'].endswith('.b03'): d[(x['device'],x['filename'][:-4])]['b03']=(int(x['size_bytes']),x['md5_db'])
    elif x['filename'].endswith('.b07'): d[(x['device'],x['filename'][:-4])]['b07']=(int(x['size_bytes']),x['md5_db'])
both={k:v for k,v in d.items() if 'b03' in v and 'b07' in v}
al=lambda v: v['b03'][1]==v['b07'][1]
print('pairs', len(both))
print('b08  form', sum(1 for k,v in both.items() if ('b08' in g[k])==al(v)))
print('size form', sum(1 for k,v in both.items() if (v['b03'][0]>=300)==al(v)))
print('len  form', sum(1 for k,v in both.items() if (v['b03'][0]==v['b07'][0])==al(v)))
print('len->md5 ', sum(1 for v in both.values() if v['b03'][0]!=v['b07'][0] or al(v)))
"
# expect: pairs 385 / each form 385, last line 385

# the size void: EQ min 408, NE max 252 (section 2)
python3 -I -c "
import csv
r=list(csv.DictReader(open('$M')))
t=[x for x in r if x['blob_family']=='tz']
d={}
for x in t:
    f=x['filename']
    if f.endswith('.b03'): d.setdefault((x['device'],f[:-4]),{})['b03']=(int(x['size_bytes']),x['md5_db'])
    elif f.endswith('.b07'): d.setdefault((x['device'],f[:-4]),{})['b07']=(int(x['size_bytes']),x['md5_db'])
b={k:v for k,v in d.items() if 'b03' in v and 'b07' in v}
eq=[v for v in b.values() if v['b03'][1]==v['b07'][1]]
ne=[v for v in b.values() if v['b03'][1]!=v['b07'][1]]
print('EQ', len(eq), min(v['b03'][0] for v in eq), max(v['b03'][0] for v in eq))
print('NE', len(ne), min(v['b03'][0] for v in ne), max(v['b03'][0] for v in ne))
"
# expect: EQ 190 408 10760 / NE 195 130 252

# EQ / NE is per device and perfectly binary (section 3)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('$M')))
t=[x for x in r if x['blob_family']=='tz']
d=defaultdict(dict)
for x in t:
    f=x['filename']
    if f.endswith('.b03'): d[(x['device'],f[:-4])]['b03']=x['md5_db']
    elif f.endswith('.b07'): d[(x['device'],f[:-4])]['b07']=x['md5_db']
b={k:v for k,v in d.items() if 'b03' in v and 'b07' in v}
per=defaultdict(lambda:[0,0])
for (dev,_),v in b.items():
    per[dev][0]+=1; per[dev][1]+= (v['b03']==v['b07'])
print('EQ', sum(1 for n,e in per.values() if e==n),
      'NE', sum(1 for n,e in per.values() if e==0),
      'MIXED', sum(1 for n,e in per.values() if 0<e<n))
"
# expect: EQ 22 NE 27 MIXED 0

# the same test FAILS on other -- 58 counterexamples (section 4)
python3 -I -c "
import csv,re
from collections import defaultdict
r=list(csv.DictReader(open('$M')))
t=[x for x in r if x['blob_family']=='other']
g=defaultdict(set); d=defaultdict(dict)
for x in t:
    mm=re.match(r'^(.*?)\.(mdt|img|b\d\d)\$',x['filename'])
    if mm: g[(x['device'],mm.group(1))].add(mm.group(2))
    if x['filename'].endswith('.b03'): d[(x['device'],x['filename'][:-4])]['b03']=(int(x['size_bytes']),x['md5_db'])
    elif x['filename'].endswith('.b07'): d[(x['device'],x['filename'][:-4])]['b07']=(int(x['size_bytes']),x['md5_db'])
b={k:v for k,v in d.items() if 'b03' in v and 'b07' in v}
al=lambda v: v['b03'][1]==v['b07'][1]
print('pairs', len(b), 'law holds', sum(1 for k,v in b.items() if ('b08' in g[k])==al(v)))
"
# expect: pairs 561 law holds 503

# segment census (section 5)
python3 -I -c "
import csv,re
from collections import defaultdict,Counter
r=list(csv.DictReader(open('$M')))
t=[x for x in r if x['blob_family']=='tz']
g=defaultdict(set)
for x in t:
    mm=re.match(r'^(.*?)\.(mdt|img|b\d\d)\$',x['filename'])
    if mm: g[(x['device'],mm.group(1))].add(mm.group(2))
print(dict(sorted(Counter(len(s) for s in g.values()).items())))
b3=[k for k in g if 'b03' in g[k] and 'b07' not in g[k]]
print('b03-without-b07', len(b3), sorted({len(g[k]) for k in b3}))
"
# expect: {1: 365, 2: 3, 4: 11, 5: 9, 8: 14, 9: 183, 10: 181, 11: 21} / 34 [4, 5, 8]

# db_type counts, and the .mdt exception (section 6)
python3 -I -c "
import csv
from collections import Counter
r=list(csv.DictReader(open('$M')))
t=[x for x in r if x['device']=='Poco_F5' and x['blob_family']=='tz']
print(dict(Counter(x['db_type'] for x in t)))
mdt=[x for x in t if x['filename'].endswith('.mdt')]
print('mdt', len(mdt), 'ELF64', sum(1 for x in mdt if x['db_type']=='ELF64'))
print([x['filename'] for x in mdt if x['db_type']!='ELF64'])
"
# expect: DRM 27, UNKNOWN 19, SECURITY 15, FINGERPRINT 10, ELF64 9, CERT 9, BOOT 1, SECUREBOOT 1
#         mdt 8 ELF64 7 / ['soter64.mdt']
```

## What would upgrade this finding

- **One decoded `.mdt` from this device.** It would confirm the `phdr[3]`/`phdr[7]` alias
  independently of the fingerprint corpus, and would show whether the 300-B boundary is a
  `p_filesz` artefact.
- **A second hash for any one row.** Everything here is single-source; one independent digest
  would convert §1–§4 from "the DB says" to verified.
- **The EQ/NE axis.** If it is a build-generation marker, a version string would name it. The
  matrix has none, so this needs a payload.
