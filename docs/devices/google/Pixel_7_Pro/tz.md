# google Pixel_7_Pro (cheetah) — `tz` family: one `gsa.img` row, and a provenance check that finally closes

Analysis date 2026-11-21. Analyst: OC-3 (issue [#1670](https://github.com/adineo-cmd/open-device/issues/1670)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows,
4,264 of them `tz`), TheMuppets `proprietary_vendor_google_*` `radio/` trees
(lineage-23.0), git-lfs pointer files.

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art, and it settles the classification question before I start

`Pixel_7_Pro`'s single `tz` row is **`gsa.img`**, not a TrustZone image. The obvious move is
to call that a mislabel. **It is not**, and the repo already says why:

`upstream/pr10-remaining-issues-package.md:195-199` enumerates the radio directory's 45
distinct images and groups them explicitly:

> the boot chain (xbl, xbl_config, xbl_ramdump, shrm, aop, aop_config, cpucp, qupfw, uefi,
> abl, imagefv, devcfg, hyp, storsec, **tzsw**, pbl, bl1/bl2/bl31, multiimgoem), the modem
> set …, **the TrustZone set (tz, cmnlib, cmnlib64, keymaster, uefisecapp, gsa,
> featenabler)** …

[F] So this repo's own taxonomy puts `gsa` in the **TrustZone set** and `tzsw` in the
**boot chain**. The matrix's placement of `gsa.img` under `blob_family = tz` and
`tzsw.img` under `boot` follows that taxonomy exactly. **There is no mislabel here and I am
not going to invent one.** The `gsa`/`tzsw` split is a deliberate, documented grouping of
"secure-world services" vs "boot-chain stages", not a classification error.

Also cited, not re-derived: `docs/devices/google/Pixel_7_Pro/boot.md` (#1664) established
that the 13-device Tensor `boot` family has an 8-way md5 partition that is **identical for
`bl1`, `bl31`, `tzsw` and `abl`**. That result is used here as a control (§3).

## Verdict

`Pixel_7_Pro` (`cheetah`, "Google Tensor GS201") has **1 `tz` row**: `gsa.img`,
348,160 B, md5 `a8170bede7441f1c089f8f0ae51e4f14`, `db_type = SECURITY`,
`db_path = google/cheetah/radio`, `priority = P3`.

That single row is not much to analyse. What is worth reporting is that it is
**independently verifiable**, and that verification produces a result the `gpu`/`boot` notes
could not get:

> **`gsa.img`'s sha256 is published in the vendor tree's git-lfs pointer, and the sha256
> partition across 16 Pixel devices exactly reproduces the matrix's md5 partition — a second
> hash algorithm, from a second source, agreeing with the DB.**

That is the first independent confirmation of a matrix md5 in this series. Every earlier
Google note was matrix-internal or relied on re-hashing vendor files with the same md5; this
one compares md5 against **sha256 from upstream metadata**.

## 1. The single row

| field | value |
|---|---|
| `filename` | `gsa.img` |
| `size_bytes` | 348,160 |
| `md5_db` | `a8170bede7441f1c089f8f0ae51e4f14` |
| `sha256_if_listed` | *(empty)* |
| `db_type` | `SECURITY` |
| `db_path` | `google/cheetah/radio` |
| `blob_family` / `blob_subfamily` | `tz` / *(empty)* |
| `isa_identified` | *(empty)* |
| `interface_documented` | `n` |
| `priority` | `P3` |

[F] 1 row, 348,160 B. `Pixel_7_Pro` has 45 matrix rows in total: `other` 28, `boot` 9,
`gpu` 5, `modem` 1, `tz` 1, `wifi` 1.

[F] `sha256_if_listed` is **empty on all 16 `gsa.img` rows**, and on **0 of 790** rows
belonging to these 16 devices. So the matrix itself carries no second hash here.

## 2. The size ladder: 4 generations, 4 sizes, monotonic

[F] `gsa.img` appears on 16 Pixel devices with exactly **4 distinct sizes**, and size
determines the SoC generation with no exceptions:

| generation | devices | `gsa.img` size | KiB |
|---|---:|---:|---:|
| GS101 | 3 | 278,528 | 272 |
| GS201 | 5 | 348,160 | 340 |
| G3 | 3 | 380,928 | 372 |
| G4 | 5 | 409,600 | 400 |

[F] The ladder is **strictly increasing** (278,528 < 348,160 < 380,928 < 409,600), all four
are exact **4096-byte multiples**, and each size maps to exactly one generation
(`size → generation` pure: **True**).

[I] This is the same shape as the `boot`-family result in #1664 — size carries the
generation, md5 carries the device — but here it is cleaner, because `gsa.img` has **no
`abl`-style exception**. 4 sizes for 4 generations, monotonic, zero counterexamples.

## 3. Independent verification — the part that is actually new

TheMuppets trees keep `radio/gsa.img` as a **git-lfs pointer**, not the bytes. The pointer
file itself contains the object's **sha256 and true size**:

```
version https://git-lfs.github.com/spec/v1
oid sha256:403314b7985aaed6f0ad342da82044290fe75ebe45da488c4c3998de550e7ff3
size 348160
```

[F] That is a real, upstream-published hash — not the matrix's md5, and not derived from it.
I harvested it for all 16 devices.

[F] **All 16 sizes in the pointers match the matrix exactly (16/16):**

| codename | device | LFS size | matrix size | match | sha256 (first 12) |
|---|---|---:|---:|---|---|
| `oriole` | Pixel_6 | 278,528 | 278,528 | ✅ | `fb9ace95349e` |
| `bluejay` | Pixel_6A | 278,528 | 278,528 | ✅ | `848e0d29f47a` |
| `raven` | Pixel_6_Pro | 278,528 | 278,528 | ✅ | `fb9ace95349e` |
| `panther` | Pixel_7 | 348,160 | 348,160 | ✅ | `403314b7985a` |
| `cheetah` | Pixel_7_Pro | 348,160 | 348,160 | ✅ | `403314b7985a` |
| `lynx` | Pixel_7a | 348,160 | 348,160 | ✅ | `3f1c6a5581e1` |
| `felix` | Pixel_Fold | 348,160 | 348,160 | ✅ | `350101f92243` |
| `tangorpro` | Pixel_Tablet | 348,160 | 348,160 | ✅ | `9a71e796fc37` |
| `shiba` | Pixel_8 | 380,928 | 380,928 | ✅ | `24d5b7ff0940` |
| `husky` | Pixel_8_Pro | 380,928 | 380,928 | ✅ | `24d5b7ff0940` |
| `akita` | Pixel_8A | 380,928 | 380,928 | ✅ | `e4abc419a44e` |
| `tokay` | Pixel_9 | 409,600 | 409,600 | ✅ | `801424696d85` |
| `tegu` | Pixel_9A | 409,600 | 409,600 | ✅ | `c12c2942fab0` |
| `caiman` | Pixel_9_Pro | 409,600 | 409,600 | ✅ | `801424696d85` |
| `comet` | Pixel_9_Pro_Fold | 409,600 | 409,600 | ✅ | `801424696d85` |
| `komodo` | Pixel_9_Pro_XL | 409,600 | 409,600 | ✅ | `801424696d85` |

[F] **The sha256 partition is identical to the matrix's md5 partition** — verified as set
equality over the 16 devices, **True**:

```
4 devices  Pixel_9, Pixel_9_Pro, Pixel_9_Pro_Fold, Pixel_9_Pro_XL
2 devices  Pixel_6, Pixel_6_Pro
2 devices  Pixel_7, Pixel_7_Pro
2 devices  Pixel_8, Pixel_8_Pro
1 each     Pixel_6A, Pixel_7a, Pixel_Fold, Pixel_8A, Pixel_9A, Pixel_Tablet
```

[I] **Why this matters.** The matrix's `md5_db` has been unfalsifiable in this series: no
`sha256_if_listed`, no second hash, and re-hashing a vendor file only reproduces the same
md5. Here two independent hash functions over the same upstream objects agree on *which
devices share a binary*. That is the strongest evidence yet that `md5_db` faithfully
represents the real artifacts — and it is the first time the series has had it.

[N] **I could not fetch the bytes.** The LFS objects return `404` from
`media.githubusercontent.com`, and the LFS batch API replies `"Object does not exist on the
server"` — the objects were never uploaded. So this is **pointer-metadata verification, not
byte verification**. It proves the DB agrees with upstream metadata; it does not prove
anything about file contents (§6.1).

### 3.1 A second file confirms the same partition

`gsa_bl1.img` exists on 8 of the 16 devices (G3 and G4 only). Its pointers give a
**different sha256** per device, and its partition **reproduces the same grouping**:

[F] `gsa_bl1.img` — 8 devices, one size (32,768 B), 4 distinct md5:

| devices | count |
|---|---:|
| `Pixel_9`, `Pixel_9_Pro`, `Pixel_9_Pro_Fold`, `Pixel_9_Pro_XL` | 4 |
| `Pixel_8`, `Pixel_8_Pro` | 2 |
| `Pixel_8A` | 1 |
| `Pixel_9A` | 1 |

[F] `partition(gsa_bl1.img LFS sha256) == partition(gsa_bl1.img matrix md5)`: **True**.
[F] `partition(gsa_bl1.img) == partition(gsa.img restricted to those 8 devices)`: **True**.

[I] Two different files, two different hash algorithms, same sharing topology — and the
topology is the one #1664 found for `bl1`/`bl31`/`tzsw`/`abl`. The A-suffix devices
(`Pixel_8A`, `Pixel_9A`) are again the only ones not sharing with a sibling.

## 4. The `tz` family is mostly not TrustZone — 4,264 rows, 1.5% core

[F] The `tz` family is **4,264 rows / 665,173,154 B** across 9 vendors. Classifying every
filename:

| category | rows | share |
|---|---:|---:|
| DRM (`hdcp`, `widevine`, `dxhdcp`) | 1,287 | 30.2% |
| other | 1,262 | 29.6% |
| TZ app/service (`cmnlib`, `cpusys_vm`, `sp_*`, `featenabler`, …) | 650 | 15.2% |
| fingerprint (`soter*`) | 436 | 10.2% |
| certificate (`*license*`, `*cert*`) | 292 | 6.8% |
| TZ-adjacent (`keymaster`, `uefisecapp`, `devcfg`) | 187 | 4.4% |
| **TZ core (`tz.img`)** | **63** | **1.5%** |
| hypervisor (`hyp.*`) | 63 | 1.5% |
| **Google Security Chip (`gsa*`)** | **24** | **0.6%** |

[F] `db_type` confirms the spread: `UNKNOWN` 1,105, `DRM` 1,083, `SECURITY` 735, `ELF64`
517, `FINGERPRINT` 436, `CERT` 262, `BOOT` 63, `SECUREBOOT` 63.

[I] So "the `tz` family" is a **secure-world catch-all**, of which under 2% is the
TrustZone image itself. That is a property of the taxonomy, not an error — but a reader who
assumes `blob_family = tz` means "TrustZone firmware" will be wrong 98% of the time.

[F] Google is a small part of it: **51 rows**, of which 24 are `gsa*` and 15 are
`tz`/`hyp`/`keymaster`/`devcfg`/`uefisecapp`.

[N] **This is not a defect I am filing.** The repo's own `pr10-remaining-issues-package.md`
defines the grouping, and #1664 already documented that Google's boot chain carries `tzsw`.
The two notes together mean Google's actual TrustZone image sits in `boot`, not `tz` — which
is worth stating once, but it follows the documented taxonomy and needs no fix.

## 5. Honest negatives

1. **Pointer-metadata verification, not byte verification.** The LFS objects are not on the
   server (`404` / `"Object does not exist"`), so I verified **size and sha256 from the
   pointer file** and never read a byte of `gsa.img`. §3's agreement is between the DB and
   upstream *metadata* [N].
2. **`sha256_if_listed` is empty on all 16 `gsa.img` rows** and on 0 of 790 rows for these
   devices, so the matrix contributes no second hash of its own [N].
3. **One row is one row.** The device-level content of this note is a single 348,160-byte
   file; everything substantive is family-level or cross-source [I].
4. **I did not verify the LFS sha256 against a matrix md5 by re-hashing.** That is
   impossible without the bytes — the agreement in §3 is a *partition* comparison, which is
   weaker than a hash comparison [N].
5. **The 4-step size ladder is 16 devices / 4 generations.** It is clean here, but `abl.img`
   in #1664 showed the same kind of claim can have exceptions, so I am not generalising
   beyond `gsa.img` [I].
6. **The `gsa` / `tzsw` family assignment is repo taxonomy, not my inference** — I cite
   `pr10-remaining-issues-package.md:195-199` rather than claiming a finding [N].
7. **Web search was unavailable** for most of this session; **no claim here rests on a web
   source** [N].
8. **No payload is committed**; only pointer files were read, and they are 131 bytes of text.

## 6. Rule 1 — corrections for the lead, not applied here

1. **`sha256_if_listed` is empty on 0 of 790 rows for these 16 devices**, and 11 of 1,038
   `boot` rows fleet-wide. Meanwhile the **vendor tree publishes a sha256 for every one of
   these files in its LFS pointer**. That hash is free to harvest and would make `md5_db`
   falsifiable for the whole Google family. Highest-value fix in this note.
2. **`blob_family = tz` is a 98%-imprecise label.** Only 1.5% of its 4,264 rows are the
   TrustZone image. `db_type` already distinguishes `DRM`/`FINGERPRINT`/`CERT`/
   `SECUREBOOT`; splitting `tz` along `db_type` would make the family mean what its name
   says.
3. **`interface_documented = n`** on this row — mainline documents the GSA interface and
   `gsa_bl1.img` is a standard stage-1 loader.
4. **`priority = P3`** on a row that is the only `tz` row for the device; the priority
   scheme is not explained anywhere I could find [OPEN].
5. **`db_path = google/cheetah/radio` names a location, not a release.** Seventh note in
   this series to hit the missing `source_ref`; here it is worse, because the vendor tree has
   *branches* (`lineage-23.0`, `lineage-22.2`) that the matrix cannot express.

## 7. Reproduce

```sh
# run from the repo root

# the single row
python3 -I -c "
import csv
r=[x for x in csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv'))
   if x['device']=='Pixel_7_Pro' and x['blob_family']=='tz']
for x in r: print(x['filename'],x['size_bytes'],x['md5_db'],x['db_type'],x['db_path'])
print('rows',len(r))"

# the size ladder: 4 generations, 4 sizes, monotonic (section 2)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
gen={'Pixel_6':'GS101','Pixel_6A':'GS101','Pixel_6_Pro':'GS101',
     'Pixel_7':'GS201','Pixel_7_Pro':'GS201','Pixel_7a':'GS201','Pixel_Fold':'GS201','Pixel_Tablet':'GS201',
     'Pixel_8':'G3','Pixel_8A':'G3','Pixel_8_Pro':'G3',
     'Pixel_9':'G4','Pixel_9A':'G4','Pixel_9_Pro':'G4','Pixel_9_Pro_Fold':'G4','Pixel_9_Pro_XL':'G4'}
g=defaultdict(set)
for x in r:
    if x['filename']=='gsa.img': g[gen[x['device']]].add(int(x['size_bytes']))
for k in ['GS101','GS201','G3','G4']: print(k, sorted(g[k]))
print('pure:', all(len(v)==1 for v in g.values()))"
# expect 278528 / 348160 / 380928 / 409600, pure: True

# the sha256 partition from the LFS pointers (section 3)
for d in oriole bluejay raven panther cheetah lynx felix tangorpro \
         shiba husky akita tokay tegu caiman comet komodo; do
  printf '%s ' "$d"
  curl -s -L "https://raw.githubusercontent.com/TheMuppets/proprietary_vendor_google_${d}/lineage-23.0/radio/gsa.img" \
    | grep '^oid sha256:' | cut -d: -f2
done | sort -k2 | awk '{print $2}' | sort | uniq -c | sort -rn
# expect: 4 x 801424... , 2 x 403314... , 2 x fb9ace... , 2 x 24d5b7... ,
#         then 6 singletons -- i.e. the same partition as the matrix md5s

# the same partition holds for gsa_bl1.img on the 8 G3/G4 devices (section 3.1)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for f in ['gsa.img','gsa_bl1.img','tzsw.img','bl1.img']:
    g=defaultdict(list)
    for x in r:
        if x['filename']==f: g[x['md5_db']].append(x['device'])
    print(f, len(g), 'groups', sorted(len(v) for v in g.values()), sorted({x['blob_family'] for x in r if x['filename']==f}))"

# the tz family is 98% not TrustZone (section 4)
python3 -I -c "
import csv
from collections import Counter
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
tz=[x for x in r if x['blob_family']=='tz']
print('tz rows',len(tz),'bytes',sum(int(x['size_bytes']) for x in tz))
print(Counter(x['db_type'] for x in tz))
print('TZ core rows:',sum(1 for x in tz if x['filename'].startswith('tz.')))"
```

## What would upgrade this finding

1. **Upload or locate the actual `gsa.img` bytes** and confirm one md5 against the LFS
   sha256. That would turn §3 from a partition comparison into a hash comparison — the
   single most valuable next step, and it is blocked on the LFS objects existing.
2. Harvest LFS sha256s for **all** Google `radio/` files (there are 9 per device) — the
   matrix would then be falsifiable across the whole family, not just `gsa`.
3. Read `GPU_ID`-equivalent identity for the GSA on hardware; every note in this series has
   had to leave silicon-level identity open.

Not legal advice. All facts are DB metadata, git-lfs pointer metadata from public vendor
trees, and repo documentation. No binary was parsed and no payload is committed.
