# google Pixel_7 (panther) — `gpu` family: the Pixel census closes at 65/65, with no extrapolation left

Analysis date 2026-11-21. Analyst: OC-3 (issue [#1658](https://github.com/adineo-cmd/open-device/issues/1658)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows),
`device-inventory.csv` (249 devices), `torvalds/linux` master, TheMuppets
`proprietary_vendor_google_{panther,cheetah,lynx,felix,tangorpro}`
(lineage-23.0 / 24.0).

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art and prior results

The container format is documented upstream and I do not claim it:
`torvalds/linux` `drivers/gpu/drm/panthor/panthor_fw.c` (complete GPL parser), and
icecream95's "Fun with CSF firmware" (2022-09-12) whose `csffw dump` transcript shows the
same section model on a Rockchip RK3588 / Mali-G610. Neither covers a Pixel device and
neither compares builds.

**In-repo prior art, and it is most of what can be said about this device:**

`docs/devices/google/Pixel_7a/gpu.md:283-289` (§4) already tabulates `panther`'s five
lineage-24.0 md5s as part of the GS201 quintet's 25/25 byte-identical result. Same device,
same files, same conclusion. **Cited, not re-derived.**

Everything else this note relies on is prior work of mine in the same series: the container
walk and `hdr.size` semantics ([#1676](https://github.com/adineo-cmd/open-device/issues/1676)),
the `hdr.size`→revision-band ladder
([#1694](https://github.com/adineo-cmd/open-device/issues/1694)), the CONFIG VA correction
([#1712](https://github.com/adineo-cmd/open-device/issues/1712)), the octet branch check and
the `soc_source` resolution
([#1748](https://github.com/adineo-cmd/open-device/issues/1748)), and the quintet-on-both-branches
result ([#1766](https://github.com/adineo-cmd/open-device/issues/1766)).

## Verdict

`Pixel_7` (`panther`, "Google Tensor GS201") has **5 `gpu` rows / 1,392,640 B**, all
`mali_csffw-rNNpM.bin` at 278,528 B, 5 distinct md5, and **5/5** of them match lineage-23.0.

There is nothing surprising about this device. Its value to the lab is that it is the last
one needed:

> **The Pixel `gpu` census is complete at 65/65 branch-verified rows — every one of the
> 65 Mali `gpu` rows in the matrix has now been hashed against the branch it claims to
> come from. No row in this family is extrapolated.**

That is a different and stronger statement than "every device has a note" (#1766), and it
is the reason this issue is worth a file of its own.

## Correction first — what I got wrong in my Gate 0 comment

My Gate 0 on this issue claimed that `panther` is "the GS201 reference device" and that
#1676 "derived the quintet's md5s *from* `panther`'s row", creating a latent circularity
that verifying `panther` would check.

**That was wrong.** `docs/devices/google/Pixel_7a/gpu.md:283` reads *"Fetching all five
lineage-24.0 files for each GS201 device and hashing"* — five independent measurements
agreeing, not one device's value propagated to four others. **There is no circularity.**

[F] The two hash sets are visibly different, which confirms independence rather than
copy-paste: the matrix's lineage-23.0 values are `4887611e…`/`fcb33781…`/…, while #1676's
§4 lineage-24.0 table shows `d9c3e31756df`/`3e99962746f3`/… — different branches, different
files, both measured.

I posted this correction on the issue before writing this file. The delta below does not
depend on the false claim: `panther` is simply one of the three outstanding devices, not a
device with special reference status.

## 1. The device's 5 `gpu` rows

| file | size (B) | md5 | `interface_documented` |
|---|---:|---|---|
| `mali_csffw-r50p0.bin` | 278,528 | `4887611e86d3dc361eab5aeb2255e3b8` | `n` |
| `mali_csffw-r51p0.bin` | 278,528 | `fcb3378116154b4e21a7f0bbb8bbc610` | `n` |
| `mali_csffw-r52p0.bin` | 278,528 | `acd5ecb0d4cc0a79c5dd03cc78db370f` | `n` |
| `mali_csffw-r53p0.bin` | 278,528 | `56b489dd03afc0de337049e231489878` | `n` |
| `mali_csffw-r54p0.bin` | 278,528 | `7d1d546c5ec3455b6ade6f3501cb54ff` | `n` |

[F] 5 rows, 5 distinct md5, total **1,392,640 B**, `db_path`
`google/panther/vendor/firmware`. 44 matrix rows for the device in total.

[F] All five verify **5/5** against lineage-23.0.

[F] The five md5s are **identical to `tangorpro`'s and `lynx`'s** — the GS201 signature, as
expected for a device whose `soc` label agrees with its group.

[I] `panther`'s `soc` cell is `Google Tensor GS201` with `soc_source = builds.csv` and
`in_builds_csv = y`. Unlike `caiman`/`comet`/`tegu`/`komodo`, there is **no contradiction
between the label and the firmware** here, and I am not going to invent one. The GS201
quintet is the clean case: one SoC, one label, one signature.

## 2. The GS201 quintet on the matrix's own branch: 25/25, one signature

This is the part that was outstanding. #1676 verified only `lynx` against lineage-23.0;
#1766 added `tangorpro`, taking the group to 10/25. I fetched the remaining three devices
(`panther`, `cheetah`, `felix`) — **15 more files** — and the group is now complete.

[F] **All 5 GS201 devices × 5 files = 25/25 verified against lineage-23.0, zero missing:**

| device | codename | `r50p0` | `r51p0` | `r52p0` | `r53p0` | `r54p0` |
|---|---|---|---|---|---|---|
| Pixel_7 | `panther` | `4887611e` | `fcb33781` | `acd5ecb0` | `56b489dd` | `7d1d546c` |
| Pixel_7_Pro | `cheetah` | `4887611e` | `fcb33781` | `acd5ecb0` | `56b489dd` | `7d1d546c` |
| Pixel_7a | `lynx` | `4887611e` | `fcb33781` | `acd5ecb0` | `56b489dd` | `7d1d546c` |
| Pixel_Fold | `felix` | `4887611e` | `fcb33781` | `acd5ecb0` | `56b489dd` | `7d1d546c` |
| Pixel_Tablet | `tangorpro` | `4887611e` | `fcb33781` | `acd5ecb0` | `56b489dd` | `7d1d546c` |

[F] **One distinct signature across all five devices, per file: 1 distinct md5 × 5 files.**

[I] This upgrades #1766's qualified statement. #1766 could only say the identity held on
lineage-23.0 for the `lynx`/`tangorpro` pair — 2 of 5 devices. It now holds for **all five**.
So the GS201 sharing is not a lineage-24.0 artefact, and unlike the G3/G4 octet it does not
break when the branch changes.

[N] This is still **expected**, not surprising: five devices on one SoC should share GPU
firmware. §2 is a check that the sharing is real and branch-stable, not a discovery.

## 3. The census closes: 65/65

[F] The matrix holds **65 Mali `gpu` rows across 13 Pixel devices** — 25 GS201 + 40 G3/G4 —
totalling **18,759,680 B**:

| group | devices | rows | bytes | branch-verified |
|---|---:|---:|---:|---:|
| GS201 | 5 | 25 | 6,963,200 | **25/25** |
| G3/G4 | 8 | 40 | 11,796,480 | **40/40** |
| **total** | **13** | **65** | **18,759,680** | **65/65** |

[F] The progression, each step measured rather than asserted:

| note | state | rows measured |
|---|---|---:|
| #1676 | GS201 `lynx` + G3/G4 `caiman` | 10 of 65 |
| #1748 | G3/G4 octet complete | 45 of 65 |
| #1766 | + `tangorpro` | 50 of 65 |
| **this note** | + `panther`, `cheetah`, `felix` | **65 of 65** |

[I] **Why this matters beyond a number.** Since #1676 the claim "the matrix is a faithful
lineage-23.0 snapshot" has been *extrapolated* for most of this family — true for the rows
someone happened to check, assumed for the rest. At 65/65 it is measured for every row.
That is the first family in this lab where that is true, and it means the matrix's Mali
`gpu` data can now be used without a branch caveat.

[N] It does **not** generalise. The 65 rows are the `gpu` family only; the same 13 devices
have **613 other rows** (678 total, so 613 non-Mali) covering `boot`, `tz` and other
families that this note says nothing about, and the Adreno families remain unverified in
this sense.

## 4. Container and schema, verified on this device

[F] All five `panther` lineage-23.0 builds parse cleanly and land on the #1694 ladder:

| build | size | `hdr.size` | CONFIG | schema | table ends at `hdr.size` | `version_hash` |
|---|---:|---:|---:|---|---|---|
| `r50p0` | 278,528 | 968 | 5 | TILER | ✅ | `0x01010000` |
| `r51p0` | 278,528 | 972 | 5 | GEOMETRY | ✅ | `0x01010000` |
| `r52p0` | 278,528 | 972 | 5 | GEOMETRY | ✅ | `0x01010000` |
| `r53p0` | 278,528 | 972 | 5 | GEOMETRY | ✅ | `0x01050000` |
| `r54p0` | 278,528 | 792 | 2 | MINIMAL | ✅ | `0x01050000` |

[F] **5/5 exact**, `magic 0xc3f13a6e` on all five, `major 0`, every table ending at exactly
`hdr.size`. This is a **consistency check, not new evidence** — `panther`'s files were
already among the 24 builds #1694 derived the ladder from.

[F] The `version_hash` step `0x01010000`→`0x01050000` again falls between `r52p0` and
`r53p0`, while the schema band changes at `r51p0`. The two axes are independent, matching
#1676 §3.5 and #1766 §4.

## 5. Honest negatives

1. **Web search was unavailable while writing this note.** Metasearch returned "No results
   found" for every query, including control queries, for the whole session. **No claim in
   this note rests on a web source.** Everything is repo- or vendor-tree verifiable [N].
2. **This device contributes almost no new information about itself.** Its lineage-24.0
   hashes were already in #1676 §4; its container behaviour was already in #1694's build
   set. The genuine contribution is the 65/65 closure, and the note says so up front rather
   than dressing up the device-level content [I].
3. **I compared only the 5 `gpu` files**, not the other 39 `panther` rows [N].
4. **I did not read `GPU_ID` on hardware**, so no measured Mali model for any Pixel device
   in this series. Every "GS201" statement is from the DB label plus the firmware signature,
   not from silicon [N].
5. **The 65/65 claim is about branch fidelity only** — it says the matrix's md5s match
   lineage-23.0. It says nothing about whether the matrix's *classification* is right; the
   `blob_family`, `interface_documented` and `soc` columns have their own defects, documented
   in the earlier notes [I].
6. **`interface_documented = n`** on all 5 rows; inherited from #1676 §5.5, cause not
   investigated [N].
7. **No payload is committed**; all parsing used local downloads of public vendor trees.
8. **The GS201 identity in §2 is one signature, but that is a small sample** — five devices
   from one SoC generation. It does not establish that sharing is universal [I].

## 6. Rule 1 — corrections for the lead, not applied here

1. **`coverage-matrix.csv` still needs a `source_ref` column.** Unchanged across five notes.
   This family is the best argument for it: 65 rows that are now *proven* to be a
   lineage-23.0 snapshot, and the matrix itself cannot say so.
2. **`device-inventory.csv` already has the provenance discipline the matrix lacks**
   (`soc_source`, `source_artifacts`, `mainline_basis_or_note`) — see #1748 §3.1. The GS201
   quintet is the clean demonstration: all five have `soc_source = builds.csv`,
   `in_builds_csv = y`, and one correct `soc` value. The two files should be reconciled
   rather than the matrix reinvented.
3. **`docs/REPO-STATE-MAP.md:18`** reads "5 per-SoC GPU docs under `research/soc/`… 22 SoCs
   remain". There are now **seven device-level Mali notes** — `Pixel_7a`, `Pixel_7`,
   `Pixel_8A`, `Pixel_9`, `Pixel_9_Pro`, `Pixel_9_Pro_XL`, `Pixel_Tablet` — which between
   them cover 65 rows across 13 devices, none of which the row counts. (Seven notes for 13
   devices because the `Pixel_7a` note analyses the whole GS201 quintet and the
   `Pixel_9_Pro_XL` note analyses the whole G3/G4 octet.)
4. **`interface_documented`** is wrong for these 5 rows — mainline documents the interface
   and §4 exercises it. All 65 Mali rows say `n`.
5. **`research/soc/per-soc-method-plans.md:210`** lists 14 Tensor devices but omits `tegu`
   and `komodo`, which are in the DB with blank `soc`. Flagged in #1766; still unfixed.

## 7. Reproduce

```sh
# run from the repo root

# the 5 rows
python3 -I -c "
import csv
r=[x for x in csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv'))
   if x['device']=='Pixel_7' and x['blob_family']=='gpu']
for x in r: print(x['filename'], x['size_bytes'], x['md5_db'])
print('rows',len(r),'distinct md5',len({x['md5_db'] for x in r}),
      'total',sum(int(x['size_bytes']) for x in r))"

# the whole 65/65 census: per-group counts
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
m=[x for x in r if 'mali' in x['filename'].lower()]
gs201={'Pixel_7','Pixel_7_Pro','Pixel_7a','Pixel_Fold','Pixel_Tablet'}
a=[x for x in m if x['device'] in gs201]; b=[x for x in m if x['device'] not in gs201]
print('GS201', len(a),'rows', sum(int(x['size_bytes']) for x in a),'B')
print('G3/G4', len(b),'rows', sum(int(x['size_bytes']) for x in b),'B')
print('total', len(m),'rows', sum(int(x['size_bytes']) for x in m),'B',
      'distinct devices', len({x['device'] for x in m}))"

# the GS201 quintet on lineage-23.0: expect 5 distinct md5 total (one per rNNpM)
for v in panther cheetah lynx felix tangorpro; do
  for f in r50p0 r51p0 r52p0 r53p0 r54p0; do
    printf '%s ' "$f"
    curl -s -L "https://raw.githubusercontent.com/TheMuppets/proprietary_vendor_google_$v/lineage-23.0/proprietary/vendor/firmware/mali_csffw-$f.bin" | md5sum | cut -d' ' -f1
  done
done | sort -u | wc -l
# expect 5  (25 files, but only 5 distinct md5 -- one per revision, shared by all five devices)

# the ladder + version_hash independence (section 4)
curl -s -L -o /tmp/px7.bin \
  "https://raw.githubusercontent.com/TheMuppets/proprietary_vendor_google_panther/lineage-23.0/proprietary/vendor/firmware/mali_csffw-r53p0.bin"
python3 -I -c "
import struct
d=open('/tmp/px7.bin','rb').read()
hs=struct.unpack('<I',d[16:20])[0]; off=20; n=0
while off<hs:
    e=struct.unpack('<I',d[off:off+4])[0]
    if (e&0xff)==1: n+=1
    off+=(e>>8)&0xff
print('hdr.size',hs,'CONFIG',n,'ends',off,'equal',off==hs,
      'version_hash=0x%08x'%struct.unpack('<I',d[8:12])[0])"
# expect hdr.size 972, CONFIG 5, equal True, version_hash 0x01050000
```

## What would upgrade this finding

1. Read `GPU_ID` on a Pixel 7 — the GS201 arch would then be measured rather than inferred
   from `version_hash` and the DB label. This is the single measurement every note in this
   series has had to leave open.
2. Apply the same 100% branch check to another family (an Adreno cluster, or the Tensor
   `boot`/`tz` rows) — 65/65 is a property of this family, not yet of the matrix.
3. Compare the ~39 non-`gpu` `panther` rows against lineage-23.0; if they also match, the
   snapshot claim extends beyond `gpu`.

Not legal advice. All facts are DB metadata, public GPL kernel source, public vendor trees,
and firmware-stored ASCII config names.
