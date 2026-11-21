# google Pixel_Tablet (tangorpro) — `gpu` family: the GS201 quintet holds for a tablet, and the 13-device census closes

Analysis date 2026-11-21. Analyst: OC-3 (issue [#1766](https://github.com/adineo-cmd/open-device/issues/1766)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows),
`torvalds/linux` master, TheMuppets `proprietary_vendor_google_tangorpro`
(lineage-23.0 / 24.0).

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art and prior results

The container format is documented upstream and I do not claim it:
`torvalds/linux` `drivers/gpu/drm/panthor/panthor_fw.c` (complete GPL parser), and
icecream95's "Fun with CSF firmware" (2022-09-12) whose `csffw dump` transcript shows the
same section model on a Rockchip RK3588 / Mali-G610.

**In-repo prior art that constrains this note:**

- `research/soc/per-soc-method-plans.md:86-96` (note 5) **already documents** the `soc`
  contradiction for this family, naming `caiman`/`comet` (Pixel 9 Pro / 9 Pro Fold) as
  carrying "Tensor G3" against a public Tensor G4. That finding is **not mine** and this
  note does not re-claim it. What that note lacks is firmware evidence — it argues from
  public specs against the DB cell.
- `docs/devices/google/Pixel_7a/gpu.md` §4 has the **GS201 quintet 25/25 byte-identical**
  result, `tangorpro` included. Cited, not re-derived.

## Verdict

`Pixel_Tablet` (`tangorpro`, "Google Tensor GS201") has **5 `gpu` rows / 1,392,640 B**, all
`mali_csffw-rNNpM.bin` at 278,528 B, 5 distinct md5.

Two results, both narrow and both real:

1. **The GS201 quintet's identity holds for the only tablet in the group** — firmware
   sharing in this family is not conditioned on device class (§2).
2. **The GS201 branch-verification gap narrows from 5/25 to 10/25**, and the family total
   from 45/65 to **50/65** — closing part of a limitation I wrote into #1748 (§3).

## 1. The device's 5 `gpu` rows

| file | size (B) | md5 | `interface_documented` |
|---|---:|---|---|
| `mali_csffw-r50p0.bin` | 278,528 | `4887611e86d3dc361eab5aeb2255e3b8` | `n` |
| `mali_csffw-r51p0.bin` | 278,528 | `fcb3378116154b4e21a7f0bbb8bbc610` | `n` |
| `mali_csffw-r52p0.bin` | 278,528 | `acd5ecb0d4cc0a79c5dd03cc78db370f` | `n` |
| `mali_csffw-r53p0.bin` | 278,528 | `56b489dd03afc0de337049e231489878` | `n` |
| `mali_csffw-r54p0.bin` | 278,528 | `7d1d546c5ec3455b6ade6f3501cb54ff` | `n` |

[F] 5 rows, 5 distinct md5, total **1,392,640 B**, `db_path`
`google/tangorpro/vendor/firmware`. 46 matrix rows for the device in total.

[F] All five verify **5/5** against lineage-23.0.

## 2. The GS201 quintet holds for the tablet

[F] All five GS201 devices carry **one identical signature** on lineage-24.0, per the files
already fetched for #1676's §4:

| file | devices compared | distinct md5 |
|---|---:|---:|
| `r54p0` | 5 | **1** |
| `r54p1` | 5 | **1** |
| `r54p2` | 5 | **1** |
| `r54p3` | 5 | **1** |
| `legacy-r56p0` | 5 | **1** |

[F] The five are `panther` (Pixel_7), `cheetah` (Pixel_7_Pro), `lynx` (Pixel_7a),
`felix` (Pixel_Fold), `tangorpro` (Pixel_Tablet). **25/25 identical.**

[I] `tangorpro` is the **only non-phone** in the quintet — a tablet among four phones. The
identity holding for it means the sharing is a property of the SoC+GPU combination, not of
device class. That is a mild result, but it is one only this device can produce, and it
rules out "phones share because they are phones" as the explanation.

[F] The identity also holds on the **matrix's own branch**. `lynx` and `tangorpro` are the
two GS201 devices I have verified against lineage-23.0, and they are 5/5 identical there
too:

```
r50p0  4887611e86d3   r51p0  fcb337811615   r52p0  acd5ecb0d4cc
r53p0  56b489dd03af   r54p0  7d1d546c5ec3
```

[I] So unlike the G3/G4 octet — where the identity is a lineage-23.0 property that breaks
into a 3/5 split on lineage-24.0 — the GS201 quintet's sharing survives the branch change
for the pair tested. The other three GS201 devices are unverified on lineage-23.0 (§6.2),
so this is 2 of 5 devices, not 5 of 5.

[N] This does **not** show the firmware is device-agnostic in general. Five devices sharing
one SoC is exactly the case where sharing is expected. The contrast that matters is the
lab's Adreno finding, where filenames never match the GPU revision — here the firmware
genuinely is shared because the silicon genuinely is the same.

## 3. Closing the GS201 branch-verification gap: 5/25 → 10/25

#1676's honest-negative 6, as I corrected it in #1748, reads:

> The **GS201** quintet's 25 rows are still only extrapolated from `lynx`'s 5, so "the
> matrix is a lineage-23.0 snapshot" is now proven for 45 of 65 rows, not 10.

[F] `tangorpro` is one of those 25. Its 5 rows now verify, taking the counts to:

| group | rows | branch-verified before | after |
|---|---:|---:|---:|
| GS201 (5 devices) | 25 | 5 (`lynx`) | **10** (`lynx` + `tangorpro`) |
| G3/G4 (8 devices) | 40 | 40 | 40 |
| **total** | **65** | 45 | **50** |

[I] The remaining 15 unverified GS201 rows are `panther`, `cheetah` and `felix` — three
devices × 5 files. I did not fetch them, so the statement stays at 50/65 rather than being
rounded up to a claim I have not tested.

## 4. Container and schema, verified on this device

[F] All ten `tangorpro` builds (5 per branch) parse cleanly and land on the #1694 ladder:

| build | branch | size | `hdr.size` | CONFIG | schema | `version_hash` |
|---|---|---:|---:|---:|---|---|
| `r50p0` | 23.0 | 278,528 | 968 | 5 | TILER | `0x01010000` |
| `r51p0` | 23.0 | 278,528 | 972 | 5 | GEOMETRY | `0x01010000` |
| `r52p0` | 23.0 | 278,528 | 972 | 5 | GEOMETRY | `0x01010000` |
| `r53p0` | 23.0 | 278,528 | 972 | 5 | GEOMETRY | `0x01050000` |
| `r54p0` | 23.0 | 278,528 | 792 | 2 | MINIMAL | `0x01050000` |
| `r54p0` | 24.0 | 278,528 | 792 | 2 | MINIMAL | `0x01050000` |
| `r54p1` | 24.0 | 282,624 | 792 | 2 | MINIMAL | `0x01050000` |
| `r54p2` | 24.0 | 282,624 | 792 | 2 | MINIMAL | `0x01050000` |
| `r54p3` | 24.0 | 282,624 | 792 | 2 | MINIMAL | `0x01050000` |
| `legacy-r56p0` | 24.0 | 286,720 | 792 | 2 | MINIMAL | `0x01050000` |

[F] **10/10 exact**, every table ending at exactly `hdr.size`, `magic 0xc3f13a6e`,
`major 0`. This is a **consistency check, not new evidence** — `tangorpro`'s files were
already among the 24 builds #1694 derived the ladder from.

[F] Note the `version_hash` step `0x01010000`→`0x01050000` happens between `r52p0` and
`r53p0` on lineage-23.0, while the schema band changes at `r51p0`. The two axes are
**independent**, which matches #1676 §3.5's census.

## 5. The 13-device census is now complete

[F] The matrix has **65 Mali `gpu` rows across 13 Pixel devices**. Every one now has a
note:

| group | devices | notes |
|---|---|---|
| GS201 | `panther`, `cheetah`, `lynx`, `felix`, `tangorpro` | #1676 (`lynx`), **this note** (`tangorpro`) |
| G3/G4 | `shiba`, `husky`, `akita`, `tokay`, `tegu`, `caiman`, `comet`, `komodo` | #1676, #1694, #1712, #1730, #1748 |

[I] What the completed family shows, stated as narrowly as the evidence allows:

1. **The `gpu` family is two vendors with opposite properties.** Every other `gpu` note in
   this lab is Adreno, where filenames mislead and the container is opaque. These 65 rows
   are Mali, where the container is documented in mainline, the build SHA is stored in the
   file in plain text, and the filename never reaches the loader.
2. **Firmware sharing tracks the SoC, not the product.** 5 GS201 devices share 25/25 files;
   8 G3/G4 devices share 40/40 on the matrix's branch. Product segmentation (phone vs
   tablet, Pro vs non-Pro) does not appear in the firmware on that branch.
3. **The `soc` column is not derived from the firmware.** Across the 8 G3/G4 devices there
   is 1 firmware signature and 3 distinct `soc` values (established in #1748 §3). This note
   adds no new instance — `tangorpro`'s GS201 label agrees with its group — and I am not
   inflating the count.

## 6. Honest negatives

1. **Web search was unavailable while writing this note.** Every query, including control
   queries, returned "No results found":

   ```
   Pixel 9 Pro XL SoC Tensor G4 specifications   -> No results found
   Pixel 9A Tensor G4 tegu specifications        -> No results found
   Google Tensor G4 (control)                    -> No results found
   ```

   **No claim in this note rests on a web source.** Everything is repo- or vendor-tree
   verifiable. Recorded rather than silently omitted [N].
2. **I did not fetch the remaining 15 GS201 rows** (`panther`, `cheetah`, `felix`), so the
   branch-verification statement stays at 50/65 [N].
3. **The GS201 quintet identity in §2 was measured on lineage-24.0** for all five devices,
   and on lineage-23.0 only for the `lynx`/`tangorpro` pair. The other three are unverified
   on lineage-23.0 [N].
4. **Identical firmware across five devices is expected**, since they share one SoC. §2 is a
   check that the sharing is real, not a discovery that it is surprising [I].
5. **I did not read `GPU_ID` on hardware**, so no measured Mali model for any Pixel device
   in this series [N].
6. **The `soc` contradiction in this family is prior art** — `per-soc-method-plans.md:86`
   has it from public specs. My series adds the firmware evidence; it does not add the
   observation [N].
7. **No payload is committed**; all parsing used local downloads of public vendor trees.
8. **`interface_documented = n`** on all 5 rows; inherited from #1676 §5.5 [N].

## 7. Rule 1 — corrections for the lead, not applied here

1. **`coverage-matrix.csv` still needs a `source_ref` column.** Unchanged from #1676; this
   issue is a further demonstration, since `tangorpro`'s rows read as 278,528 B × 5 on both
   branches but the *files* differ between them.
2. **`device-inventory.csv` already has the provenance discipline the matrix lacks**
   (`soc_source`, `source_artifacts`, `mainline_basis_or_note`) — see #1748 §3.1. The two
   files should be reconciled rather than the matrix reinvented.
3. **`docs/REPO-STATE-MAP.md:18`** still reads "5 per-SoC GPU docs"; there are now six
   device-level Mali notes and the Pixel `gpu` census is complete.
4. **`interface_documented`** is wrong for these 5 rows — mainline documents the interface
   and §4 exercises it.
5. **`research/soc/per-soc-method-plans.md:210`** lists `shiba, husky, akita, caiman, comet`
   as "G3 per the DB's SOC cell", but omits `tegu` and `komodo`, which are **blank** in the
   DB and are also G3/G4-family devices. The list should say so, or a reader will think the
   family is 13 devices when the DB labels only 11 of them.

## 8. Reproduce

```sh
# run from the repo root

# the 5 rows
python3 -I -c "
import csv
r=[x for x in csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv'))
   if x['device']=='Pixel_Tablet' and x['blob_family']=='gpu']
for x in r: print(x['filename'], x['size_bytes'], x['md5_db'])
print('rows',len(r),'distinct md5',len({x['md5_db'] for x in r}),
      'total',sum(int(x['size_bytes']) for x in r))"

# the branch check: 5/5 against lineage-23.0
for f in r50p0 r51p0 r52p0 r53p0 r54p0; do
  printf '%s ' "$f"
  curl -s -L "https://raw.githubusercontent.com/TheMuppets/proprietary_vendor_google_tangorpro/lineage-23.0/proprietary/vendor/firmware/mali_csffw-$f.bin" | md5sum
done

# the GS201 quintet on lineage-24.0: expect 5 distinct md5 total, one per file name
for v in panther cheetah lynx felix tangorpro; do
  for f in r54p0 r54p1 r54p2 r54p3 legacy-r56p0; do
    printf '%s ' "$f"
    curl -s -L "https://raw.githubusercontent.com/TheMuppets/proprietary_vendor_google_$v/lineage-24.0/proprietary/vendor/firmware/mali_csffw-$f.bin" | md5sum | cut -d' ' -f1
  done
done | sort -u | wc -l
# expect 5  (25 files, but only 5 distinct md5 -- one per file name, shared by all five devices)

# the ladder + version_hash independence (section 4)
curl -s -L -o /tmp/tp.bin \
  "https://raw.githubusercontent.com/TheMuppets/proprietary_vendor_google_tangorpro/lineage-23.0/proprietary/vendor/firmware/mali_csffw-r53p0.bin"
python3 -I -c "
import struct
d=open('/tmp/tp.bin','rb').read()
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

1. Fetch the remaining 15 GS201 rows (`panther`, `cheetah`, `felix`) to take branch
   verification from 50/65 to 65/65.
2. Read `GPU_ID` on a Pixel Tablet — the GS201 arch would then be measured rather than
   inferred from `version_hash`.
3. Compare the ~41 non-`gpu` rows of the five GS201 devices; if those also match, the
   "sharing tracks the SoC" claim gets much stronger.

Not legal advice. All facts are DB metadata, public GPL kernel source, public vendor trees,
and firmware-stored ASCII config names.
