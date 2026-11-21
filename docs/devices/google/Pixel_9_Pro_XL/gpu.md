# google Pixel_9_Pro_XL (komodo) — `gpu` family: 8 devices, 1 firmware signature, 3 `soc` labels

Analysis date 2026-11-21. Analyst: OC-3 (issue [#1748](https://github.com/adineo-cmd/open-device/issues/1748)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows),
`device-inventory.csv` (249 devices), `torvalds/linux` master, TheMuppets
`proprietary_vendor_google_komodo` (lineage-23.0 / 24.0) plus the seven sibling Pixel
trees for the octet comparison.

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art and prior results

The container format is documented upstream and I do not claim it:
`torvalds/linux` `drivers/gpu/drm/panthor/panthor_fw.c` (complete GPL parser), and
icecream95's "Fun with CSF firmware" (2022-09-12) whose `csffw dump` transcript shows the
same section model on a Rockchip RK3588 / Mali-G610. Neither covers a Pixel device and
neither compares builds.

Established in this lab, **cited not re-derived**: the container walk and `hdr.size`
semantics ([#1676](https://github.com/adineo-cmd/open-device/issues/1676)); the
`hdr.size`→revision-band ladder ([#1694](https://github.com/adineo-cmd/open-device/issues/1694));
the CONFIG VA correction ([#1712](https://github.com/adineo-cmd/open-device/issues/1712));
the `caiman`/`tokay` byte identity
([#1730](https://github.com/adineo-cmd/open-device/issues/1730)).

## Verdict

`Pixel_9_Pro_XL` (`komodo`) has **5 `gpu` rows / 1,474,560 B**, all `mali_csffw-rNNpM.bin`
at 294,912 B, 5 distinct md5. Its `soc` column is **blank**.

The headline result is not about this device alone — it needs the full octet:

> **All 8 G3/G4 Pixel devices carry one identical GPU firmware signature on the matrix's
> own branch, while the `soc` column assigns them 3 different values.**

That is only visible from the matrix side, not the vendor side, which is why #1676 could
not state it (§3).

## Correction first — what I got wrong in my SEARCH comment

My SEARCH comment on this issue claimed #1676 analysed only six of the eight G3/G4 devices
and that `komodo` needed analysing for the set to be complete. **Both claims were false.**
#1676 fetched and hashed all eight devices on lineage-24.0 — 40 files — to build its §6
"distinct md5 across the 8 devices" table. `komodo` was among them.

[F] I verified this rather than assuming: the `komodo` lineage-24.0 files I downloaded this
session are **byte-identical** to the ones #1676 already had on disk (`cmp`, 5/5).

[I] The mistake's cause: #1676's honest-negative 6 reads *"Only `lynx` and `caiman` were
verified against lineage-23.0"*. I misread a **branch**-verification limit as a
**device**-coverage limit. That was my error, not an ambiguity in the note.

I posted the correction on the issue before writing this file. The corrected delta is
narrower and is what §1–§3 deliver.

## 1. The device's 5 `gpu` rows

| file | size (B) | md5 | `interface_documented` |
|---|---:|---|---|
| `mali_csffw-r50p0.bin` | 294,912 | `27c9b2b908b9ba9b4bc9809a9ad00ba6` | `n` |
| `mali_csffw-r51p0.bin` | 294,912 | `10d86c50fbf11b8ee2ba9fd4e233ca24` | `n` |
| `mali_csffw-r52p0.bin` | 294,912 | `f34ea071c8e12c8bc7aca02dd45db20a` | `n` |
| `mali_csffw-r53p0.bin` | 294,912 | `02e26e697898bcde4dee30320a6f79e7` | `n` |
| `mali_csffw-r54p0.bin` | 294,912 | `23cdc2df701a24775eeeb26b2c251baa` | `n` |

[F] 5 rows, 5 distinct md5, total **1,474,560 B**, `db_path`
`google/komodo/vendor/firmware`. 59 matrix rows for the device in total.

[F] All five verify **5/5** against lineage-23.0 — the **first branch check for any device
outside `lynx`, `caiman`, `akita` and `tokay`**. Branch-checked rows rise from 20 to 25
(see §2 for the full octet, which takes it to 40).

[F] Branch replacement follows the established pattern:

```
komodo lineage-23.0: r50p0 r51p0 r52p0 r53p0 r54p0          all 294,912 B
komodo lineage-24.0: r51p0 r54p1 r54p2 r54p3 legacy-r56p0  294,912 / 299,008x3 / 303,104
```

[F] `komodo`'s lineage-24.0 set is **byte-identical to `tokay`'s and `caiman`'s**, 5/5
(`cmp`-verified).

## 2. The whole octet, branch-verified: 40/40

This is the real new work. #1676 checked lineage-23.0 for 2 devices; #1694/#1712/#1730
added 3 more. I fetched the remaining devices and now have **all 8 × 5 = 40 files
verified against lineage-23.0**, with none missing:

| device | codename | `r50p0` | `r51p0` | `r52p0` | `r53p0` | `r54p0` |
|---|---|---|---|---|---|---|
| Pixel_8 | `shiba` | `27c9b2b9` | `10d86c50` | `f34ea071` | `02e26e69` | `23cdc2df` |
| Pixel_8A | `akita` | `27c9b2b9` | `10d86c50` | `f34ea071` | `02e26e69` | `23cdc2df` |
| Pixel_8_Pro | `husky` | `27c9b2b9` | `10d86c50` | `f34ea071` | `02e26e69` | `23cdc2df` |
| Pixel_9 | `tokay` | `27c9b2b9` | `10d86c50` | `f34ea071` | `02e26e69` | `23cdc2df` |
| Pixel_9A | `tegu` | `27c9b2b9` | `10d86c50` | `f34ea071` | `02e26e69` | `23cdc2df` |
| Pixel_9_Pro | `caiman` | `27c9b2b9` | `10d86c50` | `f34ea071` | `02e26e69` | `23cdc2df` |
| Pixel_9_Pro_Fold | `comet` | `27c9b2b9` | `10d86c50` | `f34ea071` | `02e26e69` | `23cdc2df` |
| Pixel_9_Pro_XL | `komodo` | `27c9b2b9` | `10d86c50` | `f34ea071` | `02e26e69` | `23cdc2df` |

[F] **One distinct signature across all 8 devices, 0 missing files.** Every value matches
the matrix exactly.

[I] This closes #1676's honest-negative 6 (*"the other 11 devices' matrix rows were not
individually re-hashed"*) for the G3/G4 half: it is no longer extrapolated, it is measured.

## 3. The result the matrix side gives and the vendor side cannot: 1 signature, 3 labels

#1676 §6 describes lineage-24.0, where the octet splits **two** ways (3/5, `r49p0` vs
`r51p0`). On the matrix's own branch there is no split at all — and that is what exposes
the `soc` column.

[F] The matrix's `soc` values for the same 8 devices whose firmware is byte-identical:

| device | codename | `soc` column | `in_builds_csv` | firmware signature |
|---|---|---|---|---|
| Pixel_8 | `shiba` | Google Tensor **G3** | `y` | `27c9b2b9…` |
| Pixel_8A | `akita` | Google Tensor **G3** | `y` | `27c9b2b9…` |
| Pixel_8_Pro | `husky` | Google Tensor **G3** | `y` | `27c9b2b9…` |
| Pixel_9 | `tokay` | Google Tensor **G4** | `y` | `27c9b2b9…` |
| Pixel_9A | `tegu` | **(blank)** | **`n`** | `27c9b2b9…` |
| Pixel_9_Pro | `caiman` | Google Tensor **G3** | `y` | `27c9b2b9…` |
| Pixel_9_Pro_Fold | `comet` | Google Tensor **G3** | `y` | `27c9b2b9…` |
| Pixel_9_Pro_XL | `komodo` | **(blank)** | **`n`** | `27c9b2b9…` |

[F] **1 firmware signature, 3 distinct `soc` values** — `Google Tensor G3` (5 devices),
`Google Tensor G4` (1), blank (2).

[I] This is the cleanest available statement of the defect, and it is the one thing that
*requires* the matrix side. On lineage-24.0 the bytes differ, so a reader can always say
"the firmware distinguishes them, the label might be right". On lineage-23.0 the firmware
distinguishes **nothing** — and the column still gives three different answers.

[N] **It does not prove any label wrong.** G3 and G4 are both reported to use Mali-G715
MP7, so one shared GPU binary is expected across them. The claim is limited to: **the
`soc` column is not derived from the GPU firmware**, and on this branch it cannot be.

### 3.1 The blank `soc` is explained, and #1676's open question 8 is now answered

#1676 honest-negative 8 left open whether the blank `soc` on `tegu`/`komodo` was a parse
failure or a genuinely empty source field. It is the latter, and the provenance is
recorded in `device-inventory.csv`'s `soc_source` column:

[F] `device-inventory.csv` has a `soc_source` column, and the correlation is exact:

| `soc_source` | `soc` non-blank | devices |
|---|---|---:|
| `builds.csv` | yes | 122 |
| `builds.csv` | **no** | **0** |
| (blank) | no | 126 |
| `devices.sql.bz2` | no | 1 |

[F] **No device has a populated `soc_source` and a blank `soc`.** And both blank-`soc`
Pixel devices carry `in_builds_csv = n`:

| device | `in_builds_csv` | `soc` | `soc_source` |
|---|---|---|---|
| Pixel_9A (`tegu`) | **`n`** | blank | blank |
| Pixel_9_Pro_XL (`komodo`) | **`n`** | blank | blank |
| Pixel_9 (`tokay`) | `y` | Google Tensor G4 | `builds.csv` |

[I] So the blank is **upstream absence, not a parse failure**: these two devices are not in
the `builds.csv` source, so there was nothing to populate. `soc_source` is effectively a
provenance stamp, and it is honest about the gap. This is a *good* property of the schema
that #1676 did not know about — it claimed the matrix had no provenance column, which is
true of `coverage-matrix.csv` but **not** of `device-inventory.csv`.

[F] One exception exists fleet-wide, and it is not a counter-example: `razer/Phone2`
(`aura`) has `soc` blank with `soc_source = devices.sql.bz2` — a different source that
supplied the device without a SoC.

## 4. Container and schema, verified on this device

[F] All five `komodo` lineage-23.0 builds parse cleanly and land on the #1694 ladder:

| build | size | `hdr.size` | CONFIG | schema | table ends at `hdr.size` |
|---|---:|---:|---:|---|---|
| `r50p0` | 294,912 | 968 | 5 | TILER | ✅ |
| `r51p0` | 294,912 | 972 | 5 | GEOMETRY | ✅ |
| `r52p0` | 294,912 | 972 | 5 | GEOMETRY | ✅ |
| `r53p0` | 294,912 | 972 | 5 | GEOMETRY | ✅ |
| `r54p0` | 294,912 | 792 | 2 | MINIMAL | ✅ |

[F] **5/5 exact**, `magic 0xc3f13a6e`, `major 0`, `version_hash 0x02080000`. This is a
**consistency check, not new evidence** — `komodo`'s files were already among the 24 builds
#1694 derived the ladder from.

## 5. Honest negatives

1. **Identical firmware does not prove a mislabelled SoC.** G3 and G4 both reportedly use
   Mali-G715 MP7, so sharing one GPU binary is expected. The claim is limited to "the `soc`
   column is not derived from the GPU firmware" [N].
2. **I compared only the 5 `gpu` files**, not the other ~54 rows per device. If those differ
   between `komodo` and `tokay`, the SoCs plausibly differ too — and I did not check [N].
3. **I did not read `GPU_ID` on hardware**, so no measured Mali model for any of these 8
   devices [N].
4. **Web search was unavailable while writing this.** Metasearch returned "No results
   found" for every query including control queries, so no published-spec cross-check was
   made for `komodo`'s SoC. Everything in this note is repo-verifiable or vendor-tree
   verifiable; nothing rests on a web claim [N].
5. **The `soc_source` finding is about `device-inventory.csv`, not `coverage-matrix.csv`.**
   The matrix itself still has no provenance column, so #1676's Rule 1 item 1 stands for the
   matrix [I].
6. **I did not trace how `builds.csv` is produced** or why `tegu`/`komodo` are absent from
   it [OPEN].
7. **No payload is committed**; all parsing used local downloads of public vendor trees.
8. **`interface_documented = n`** on all 5 rows; inherited from #1676 §5.5, cause not
   investigated [N].

## 6. Rule 1 — corrections for the lead, not applied here

1. **`coverage-matrix.csv` still needs a `source_ref` column** (branch or release tag).
   Unchanged from #1676 — this issue is a further demonstration, since the same 40 rows read
   as "1 signature" on lineage-23.0 and "2 signatures" on lineage-24.0.
2. **`device-inventory.csv` already has the provenance discipline the matrix lacks**
   (`soc_source`, `source_artifacts`, `mainline_basis_or_note`). The two files should be
   reconciled rather than the matrix reinvented — §3.1 shows the inventory schema is
   already correct and honest about its gaps.
3. **`soc` column**: 8 devices, 1 firmware signature, 3 labels (§3).
4. **`docs/REPO-STATE-MAP.md:18`** still reads "5 per-SoC GPU docs"; there are now five
   device-level Mali notes in addition.
5. **`interface_documented`** is wrong for these 5 rows — mainline documents the interface
   and §4 exercises it.
6. **#1676 honest-negative 8 is now closed** by §3.1. The note should stop carrying it as
   open, or point at this file.

## 7. Reproduce

```sh
# run from the repo root

# the 5 rows
python3 -I -c "
import csv
r=[x for x in csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv'))
   if x['device']=='Pixel_9_Pro_XL' and x['blob_family']=='gpu']
for x in r: print(x['filename'], x['size_bytes'], x['md5_db'])
print('rows',len(r),'distinct md5',len({x['md5_db'] for x in r}),
      'total',sum(int(x['size_bytes']) for x in r))"

# 1 signature, 3 soc labels across the 8 G3/G4 devices (the headline, section 3)
python3 -I -c "
import csv
from collections import Counter
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
devs=['Pixel_8','Pixel_8A','Pixel_8_Pro','Pixel_9','Pixel_9A','Pixel_9_Pro',
      'Pixel_9_Pro_Fold','Pixel_9_Pro_XL']
sigs=set(); socs=Counter()
for d in devs:
    xs=[x for x in r if x['device']==d and 'mali' in x['filename'].lower()]
    sigs.add(tuple(x['md5_db'][:8] for x in sorted(xs,key=lambda y:y['filename'])))
    socs[sorted({x['soc'] for x in xs})[0]]+=1
print('firmware signatures:',len(sigs))
print('soc values:',dict(socs))
print('=> 1 signature,',len(socs),'labels')"

# the blank soc is upstream absence, not a parse failure (section 3.1)
python3 -I -c "
import csv
inv=list(csv.DictReader(open('upstream-contribution/blob-database/device-inventory.csv')))
bad=[x for x in inv if x['soc'].strip() and not x['soc_source'].strip()]
print('soc set but soc_source blank:',len(bad),'(0 = soc_source is always stamped)')
for c in ('tegu','komodo'):
    x=[y for y in inv if y['build_codename']==c][0]
    print(c,'in_builds_csv=',x['in_builds_csv'],'soc=',repr(x['soc']),'soc_source=',repr(x['soc_source']))"

# the full octet against lineage-23.0: expect one signature, 40/40
for v in shiba husky akita tokay tegu caiman comet komodo; do
  for f in r50p0 r51p0 r52p0 r53p0 r54p0; do
    printf '%s %s ' "$v" "$f"
    curl -s -L "https://raw.githubusercontent.com/TheMuppets/proprietary_vendor_google_$v/lineage-23.0/proprietary/vendor/firmware/mali_csffw-$f.bin" | md5sum
  done
done | awk '{print $3}' | sort -u | wc -l
# expect 5 (one md5 per rNNpM, shared by all 8 devices)
```

## What would upgrade this finding

1. Compare the ~54 **non-`gpu`** rows of the 8 devices. If they differ while the GPU
   firmware does not, the shared GPU is real and the G3/G4 labels may all be correct.
2. Read `GPU_ID` on a Pixel 8 and a Pixel 9 — the single measurement every note in this
   series has had to leave open.
3. Trace why `tegu` and `komodo` are absent from `builds.csv` — that is the upstream cause
   of both blank `soc` values.

Not legal advice. All facts are DB metadata, public GPL kernel source, public vendor trees,
and firmware-stored ASCII config names.
