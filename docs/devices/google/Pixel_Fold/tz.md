# google Pixel_Fold (felix) — `tz` family: one `gsa.img` row, and GS201's 4-way firmware split

Analysis date 2026-11-22. Analyst: OC-3 (issue [#1760](https://github.com/adineo-cmd/open-device/issues/1760)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows),
TheMuppets `proprietary_vendor_google_*` `radio/` trees (lineage-23.0), git-lfs pointers.

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art

- [`Pixel_7_Pro/tz.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/google/Pixel_7_Pro/tz.md)
  (#1670) — `gsa.img` is a Google security-chip image, not TrustZone; the `tz` placement
  follows the repo's documented taxonomy; LFS sha256 reproduces the matrix md5 partition.
- [`Pixel_8/tz.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/google/Pixel_8/tz.md)
  (#1688) — ten files across three `blob_family` labels share one partition on G3/G4; the
  family label does not determine sharing.
- [`Pixel_7_Pro/boot.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/google/Pixel_7_Pro/boot.md)
  (#1664) — the two-axis split; the A-suffix rule (12/12); and an **open question** about
  `abl.img`'s GS201 size spread.

**This is the third `gsa.img` note in a row, so I am not going to restate #1670.** The row
itself is one line. What is new is that `Pixel_Fold` is the least-shared Tensor device
measured so far, and GS201 is the least-shared Tensor generation — a result that required
looking at the generation as a whole, which no prior note did.

I also close one of #1664's honest negatives (§4).

## Verdict

`Pixel_Fold` (`felix`, "Google Tensor GS201") has **1 `tz` row**: `gsa.img`, 348,160 B,
md5 `2ff1d240eba3ddf7eb5eb9a6a709215a`, `db_type = SECURITY`,
`db_path = google/felix/radio`, `priority = P3`, 4096-aligned.

`Pixel_Fold` has 41 matrix rows: `other` 24, `boot` 9, `gpu` 5, `tz` 1, `modem` 1, `wifi` 1.

> **The headline.** `Pixel_Fold` shares **none** of its eight firmware files with any other
> GS201 device. On GS201 the firmware splits **4 ways across 5 devices** — `Pixel_7`+`Pixel_7_Pro`,
> and then `Pixel_7a`, `Pixel_Fold`, `Pixel_Tablet` each alone — while G4 splits **2 ways across
> 5 devices**. GS201 is the least-shared Tensor generation, and `Pixel_Fold` is one of three
> GS201 singletons that are **not** A-suffix devices.

## 1. The single row

| field | value |
|---|---|
| `filename` | `gsa.img` |
| `size_bytes` | 348,160 |
| `md5_db` | `2ff1d240eba3ddf7eb5eb9a6a709215a` |
| `sha256_if_listed` | *(empty)* |
| `db_type` | `SECURITY` |
| `db_path` | `google/felix/radio` |
| `blob_family` | `tz` |
| `interface_documented` | `n` |
| `priority` | `P3` |

[F] 1 row, 348,160 B, 4096-aligned, `soc = Google Tensor GS201`.

[F] `gsa.img` is 348,160 B on **all five** GS201 devices — the size is generation-constant
while the md5 varies within the generation (§2). This is the same ladder #1670 measured
(278,528 / 348,160 / 380,928 / 409,600 across GS101/GS201/G3/G4).

## 2. `Pixel_Fold` shares no firmware with any GS201 sibling

[F] Across all eight vendor-shipped firmware files, `Pixel_Fold` is a **singleton**:

| file | `Pixel_Fold` size (B) | md5 | shares with |
|---|---:|---|---|
| `abl.img` | 1,970,176 | `55daeac01874be5dfbd30df7944b318b` | *(none)* |
| `bl1.img` | 12,288 | `9a3a96a894ab3ef5cda6e38a257532b6` | *(none)* |
| `bl2.img` | 536,576 | `730bc3a6238c20c9df0b4795eaa3fc85` | *(none)* |
| `bl31.img` | 98,304 | `3f4eacd061579aa32435867f19331ee3` | *(none)* |
| `gsa.img` | 348,160 | `2ff1d240eba3ddf7eb5eb9a6a709215a` | *(none)* |
| `ldfw.img` | 2,392,064 | `3aa713ba1556ce95b95cc5b553c961d3` | *(none)* |
| `pbl.img` | 40,960 | `a73c8f5169157412bc32b41f8b7ad649` | *(none)* |
| `tzsw.img` | 6,737,920 | `c875c5591f8cbd7bf2c41d4aaee2dd32` | *(none)* |

[F] All eight files, zero sharing. `Pixel_Fold` is a singleton on 8 of 8.

## 3. GS201 splits 4 ways; G4 splits 2 ways

[F] The partition per generation, for the same five files:

| generation | devices | groups | partition |
|---|---:|---:|---|
| GS101 | 3 | 2 | `2 \| 1` |
| **GS201** | **5** | **4** | **`2 \| 1 \| 1 \| 1`** |
| G3 | 3 | 2 | `2 \| 1` |
| **G4** | **5** | **2** | **`4 \| 1`** |

[F] On GS201 the partition is **identical for all eight firmware files** — one partition,
not eight (`len(set(partitions.values())) == 1`, **True**):

```
['Pixel_7', 'Pixel_7_Pro']  |  ['Pixel_7a']  |  ['Pixel_Fold']  |  ['Pixel_Tablet']
```

[F] On G4, five devices collapse to two groups: the four flagships (`Pixel_9`, `Pixel_9_Pro`,
`Pixel_9_Pro_Fold`, `Pixel_9_Pro_XL`) plus `Pixel_9A` alone.

[I] **The reading.** Both generations have five devices, but GS201 is a *product-diverse*
generation — a foldable (`Pixel_Fold`) and a tablet (`Pixel_Tablet`) alongside three phones —
while G4 is four variants of one phone plus an A-variant. The firmware is built per product,
so product diversity shows up directly as partition diversity. GS201 is the only Tensor
generation where device count and sharing do not track each other.

### 3.1 Six devices are singletons on all 8 firmware files, and four are not A-suffix

[F] Devices that share none of the eight firmware files with anyone:

| device | generation | singleton on | A-suffix? |
|---|---|---:|---|
| `Pixel_6A` | GS101 | 8/8 | yes |
| `Pixel_7a` | GS201 | 8/8 | yes |
| **`Pixel_Fold`** | **GS201** | **8/8** | **no** |
| **`Pixel_Tablet`** | **GS201** | **8/8** | **no** |
| `Pixel_8A` | G3 | 8/8 | yes |
| `Pixel_9A` | G4 | 8/8 | yes |

[I] This **refines** #1664's A-suffix rule rather than contradicting it. #1664 tested
"within every generation that has an A variant, the A device is the only one that does not
share" — that is 12/12 and still true. But it also noted, parenthetically, that GS201 "has no
A variant; `Pixel_7a` is a different product line and is also unique". That understates it:
GS201 has **three** singletons (`Pixel_7a`, `Pixel_Fold`, `Pixel_Tablet`), not one.

[I] The better statement is that **singleton status tracks product distinctness, and the
A-suffix is one instance of that** — a cost-reduced variant is a distinct product. A foldable
and a tablet are also distinct products. The A-suffix is a *sufficient* marker in the
generations that have one, not the general rule.

## 4. Closing #1664's open question: `abl.img`'s GS201 size spread

#1664's honest-negative 6 read:

> "**The `abl.img` GS201 size spread (4 sizes for 5 devices) is unexplained.** It is the one
> file where size does not track generation cleanly, and I did not investigate why."

[F] It does track cleanly — the size partition **is** the md5 partition:

| device | `abl.img` size |
|---|---:|
| `Pixel_7`, `Pixel_7_Pro` | 1,941,504 |
| `Pixel_7a` | 1,908,736 |
| `Pixel_Fold` | 1,970,176 |
| `Pixel_Tablet` | 1,900,544 |

[F] `partition(abl.img size) == partition(abl.img md5)` on GS201: **True** (4 groups each,
same membership).

[I] So there was never an anomaly. #1664 expected "size ⇒ generation" and found 4 sizes on
one generation, which looked like a violation. But on GS201 the *md5* also splits 4 ways —
the generation simply has four distinct products. Size and sharing are the same axis here,
not competing ones. The file only looked anomalous because #1664 was comparing against a
per-generation expectation that GS201 does not satisfy.

## 5. Independent verification: 25/25 sizes, 5/5 partitions

[F] `Pixel_Fold`'s five vendor-shipped firmware files, from the LFS pointers:

```
abl.img   1,970,176  bf20de9917dc30ff172fa3fd09dec2fcc5685ea2f5eac31518b4aae98647f5c7
bl1.img      12,288  06d28ca4a7820bb49aa2fc8d976e45bff7905c2195da244f58d20e9a0d20432e
bl31.img     98,304  1ca951d32df9954d3c5d1205cacb4c30949b20dd03e8c03bc513912571989895
tzsw.img  6,737,920  2c1e2dea851dac5be42ad2aea746a7202922d64a2dea0dbad4ce4eedef097519
gsa.img     348,160  350101f922438c416a383d4ec01325f75ff3c5cc3e06c2d570ab9eb96ebac524
```

[F] **Sizes: 25/25.** All five files across all five GS201 devices — 25 LFS pointers — match
the matrix's `size_bytes` exactly.

[F] **Partitions: 5/5 set-equal.** For each of the five files, the LFS sha256 partition equals
the matrix md5 partition:

| file | LFS sha256 groups | matrix md5 groups | equal |
|---|---:|---:|---|
| `abl.img` | 4 | 4 | ✅ |
| `bl1.img` | 4 | 4 | ✅ |
| `bl31.img` | 4 | 4 | ✅ |
| `tzsw.img` | 4 | 4 | ✅ |
| `gsa.img` | 4 | 4 | ✅ |

[F] And every one of the five LFS partitions is the same 4-way split, with `Pixel_Fold` a
singleton in all of them:

```
['Pixel_7', 'Pixel_7_Pro']  |  ['Pixel_7a']  |  ['Pixel_Fold']  |  ['Pixel_Tablet']
```

[I] This is the strongest form of the §3 result available without the bytes: `Pixel_Fold`'s
isolation is confirmed by an **independent hash algorithm, over an independent source**, on
all five files, and it agrees with the matrix in 5/5 partitions and 25/25 sizes.

[N] **Still not byte verification.** The LFS objects return `404` and the batch API says
`"Object does not exist on the server"`. I verified **size and sha256 from pointer text** and
never read a byte (§6.1).

## 6. Honest negatives

1. **Pointer-metadata verification, not byte verification.** No byte of any file was read;
   §5 compares the DB against upstream *metadata* [N].
2. **`sha256_if_listed` is empty on the one row**, so the matrix contributes no hash of its
   own [N].
3. **One row is one row.** The device-level content is a single 348,160-byte file; everything
   substantive is generation-level [I].
4. **The GS201 4-way split is a 5-device, 2-generation-range observation** (GS201 only, with
   G4 as the contrast). I did not extend it to GS101/G3 beyond the counts in §3 [I].
5. **The "product diversity explains partition diversity" reading is inference**, not
   something I measured. I did not verify that `Pixel_Fold`/`Pixel_Tablet` firmware differs
   *because* they are different form factors — only that it does differ [I].
6. **I did not investigate `bl2`, `ldfw`, `pbl` beyond the matrix md5.** Their singleton
   status in §2 rests on matrix md5 alone; only `abl`, `bl1`, `bl31`, `tzsw`, `gsa` were
   LFS-verified (§5) [N].
7. **#1664's honest-negative 6 is closed by §4, but I did not re-verify the other five
   honest negatives in that note** [N].
8. **Gate 0 web search returned nothing usable** for `gsa.img`/`gcf.img` (generic
   factory-image pages only), and mainline code search returned 0 hits. **No claim here rests
   on a web source** [N].
9. **I made a priority-reading error, twice, and it reached a pushed note.** I had been
   reading the *globally-first* row per filename (for `gsa.img` that is `Pixel_6`, which is
   `P2`) and attributing that priority to whichever device I was writing about. That produced
   a wrong claim in #1688 ("`gsa.img` is `P2` on `Pixel_8`") which is now corrected in place
   there, and a wrong Rule 1 item here. The correct per-row values are in §7.2. Recording it
   because the failure mode — a dict keyed by filename instead of `(device, filename)` — will
   recur in any note that quotes per-row attributes [I].
10. **No payload is committed**; only 130-byte pointer files were read.

## 7. Rule 1 — corrections for the lead, not applied here

1. **`blob_family` does not predict sharing**, restated from #1688 with a sharper case: on
   GS201, `gsa.img` (family `tz`) shares a partition with `abl`/`bl1`/`bl31`/`tzsw` (family
   `boot`) and `bl2`/`ldfw`/`pbl` (family `other`). Three families, one partition.
2. **`priority` is inconsistent across devices for the same file.** `gsa.img` is `P2` on
   `Pixel_6`, `Pixel_6A`, `Pixel_6_Pro` and `Pixel_7`, and `P3` on the other twelve devices —
   including every G3/G4 device and `Pixel_Fold`. Same filename, same generation, same size,
   different priority. Census: **P2 ×4, P3 ×12**. The scheme is not explained anywhere I
   could find [OPEN].
3. **`sha256_if_listed` is empty** while the vendor tree publishes a sha256 in its LFS
   pointer — free to harvest, as §5 demonstrates on 25 rows.
4. **`interface_documented = n`** on a row that is a standard stage-1-loader companion.
5. **`docs/REPO-STATE-MAP.md:18`** still counts only the 5 `research/soc/` GPU docs.

## 8. Reproduce

```sh
# run from the repo root

# the single row
python3 -I -c "
import csv
r=[x for x in csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv'))
   if x['device']=='Pixel_Fold' and x['blob_family']=='tz']
for x in r: print(x['filename'],x['size_bytes'],x['md5_db'],x['db_type'],x['db_path'])
print('rows',len(r))"

# Pixel_Fold is a singleton on all 8 firmware files (section 2)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for f in ['abl.img','bl1.img','bl2.img','bl31.img','gsa.img','ldfw.img','pbl.img','tzsw.img']:
    g=defaultdict(list)
    for x in r:
        if x['filename']==f: g[x['md5_db']].append(x['device'])
    mine=[x for x in r if x['device']=='Pixel_Fold' and x['filename']==f][0]['md5_db']
    print(f, 'shares with', [d for d in g[mine] if d!='Pixel_Fold'])"
# expect every line: shares with []

# GS201 splits 4 ways, one partition for all 8 files (section 3)
python3 -I -c "
import csv
from collections import defaultdict
g={'Pixel_7','Pixel_7_Pro','Pixel_7a','Pixel_Fold','Pixel_Tablet'}
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
parts={}
for f in ['abl.img','bl1.img','bl2.img','bl31.img','gsa.img','ldfw.img','pbl.img','tzsw.img']:
    p=defaultdict(list)
    for x in r:
        if x['filename']==f and x['device'] in g: p[x['md5_db']].append(x['device'])
    parts[f]=frozenset(frozenset(v) for v in p.values())
    print(f,'groups',len(p))
print('all 8 files share ONE partition:',len(set(parts.values()))==1)"
# expect 4 groups each, final True

# abl size partition == abl md5 partition on GS201 (section 4)
python3 -I -c "
import csv
from collections import defaultdict
g={'Pixel_7','Pixel_7_Pro','Pixel_7a','Pixel_Fold','Pixel_Tablet'}
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
sp=defaultdict(list); mp=defaultdict(list)
for x in r:
    if x['filename']=='abl.img' and x['device'] in g:
        sp[x['size_bytes']].append(x['device']); mp[x['md5_db']].append(x['device'])
print('size groups',sorted([sorted(v) for v in sp.values()]))
print('same partition:',frozenset(frozenset(v) for v in sp.values())==frozenset(frozenset(v) for v in mp.values()))"
# expect 4 groups and True

# LFS sha256 partition reproduces the matrix (section 5)
for d in panther cheetah lynx felix tangorpro; do
  for f in abl bl1 bl31 tzsw gsa; do
    printf '%s %s ' "$f" "$d"
    curl -s -L "https://raw.githubusercontent.com/TheMuppets/proprietary_vendor_google_${d}/lineage-23.0/radio/${f}.img" \
      | grep '^oid sha256:' | cut -d: -f2
  done
done | awk '{print $1,$3}' | sort -u | awk '{c[$1]++} END {for(k in c) print k, c[k]}' | sort
# expect abl 4, bl1 4, bl31 4, gsa 4, tzsw 4 distinct sha256 -- matching the
# matrix's 4 md5 groups per file

# the six devices that are singletons on all 8 files (section 3.1)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
files=['abl.img','bl1.img','bl2.img','bl31.img','gsa.img','ldfw.img','pbl.img','tzsw.img']
sing=defaultdict(int)
for f in files:
    g=defaultdict(list)
    for x in r:
        if x['filename']==f: g[x['md5_db']].append(x['device'])
    for m,v in g.items():
        if len(v)==1: sing[v[0]]+=1
for d,n in sorted(sing.items(),key=lambda kv:-kv[1]): print(d,n,'/8')"
# expect 6 devices at 8/8: Pixel_6A, Pixel_7a, Pixel_Fold, Pixel_Tablet, Pixel_8A, Pixel_9A
```

## What would upgrade this finding

1. **Identify why GS201's firmware splits 4 ways.** Form-factor is the obvious hypothesis and
   I did not test it — comparing `Pixel_Fold`'s firmware against `Pixel_Tablet`'s on a
   generation where both exist as non-phone products would be the clean test.
2. **Locate the LFS bytes** to turn §5 from a partition comparison into a hash comparison.
3. **Test whether `Pixel_Fold`'s isolation holds on lineage-22.2** — everything here is
   lineage-23.0.

Not legal advice. All facts are DB metadata, git-lfs pointer metadata from public vendor
trees, and repo documentation. No binary was parsed and no payload is committed.
