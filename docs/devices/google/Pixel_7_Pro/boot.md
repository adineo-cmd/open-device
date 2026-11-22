# google Pixel_7_Pro (cheetah) — `boot` family: a two-axis structure, and the size column that carries nothing

Analysis date 2026-11-21. Analyst: OC-3 (issue [#1664](https://github.com/adineo-cmd/open-device/issues/1664)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows,
1,038 of them `boot`), `device-inventory.csv`.

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art and prior results

The `boot` family has one substantial in-repo analysis:
[`docs/devices/oneplus/OnePlus_7/boot.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/oneplus/OnePlus_7/boot.md)
(#1466) established the **mixed-column** finding: `size_bytes` in `boot` rows is sometimes a
partition dump (exact MiB multiples) and sometimes a real built image (irregular). It
measured 364/1,038 rows MiB-exact carrying 86.8% of the family's 23,864,283,348 B, and
[`OnePlus_7T_Pro/boot.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/oneplus/OnePlus_7T_Pro/boot.md)
(#1484) refined that to 354/1,009 = 91.0% after de-duplication.

**I do not re-derive that finding and I am not claiming it.** What this note adds is a
different axis, which #1466 could not see because its 8 Qualcomm rows are all irregular.

## Verdict

`Pixel_7_Pro` (`cheetah`, "Google Tensor GS201") has **9 `boot` rows / 102,121,472 B**,
9 distinct md5, **9/9 4096-aligned**.

The family-level result is the interesting part. On the 13 Tensor devices, the `boot` family
splits into two groups with **opposite properties**:

> **The five "payload" files have a constant size and 13 distinct md5 each — the size column
> carries nothing. The four "firmware" files have 3–7 distinct sizes and only 8 distinct md5
> — the size column carries the SoC generation, and the md5 carries the device.**

That is an inversion of the usual reading, and it is checkable (§2, §3).

## 1. The device's 9 `boot` rows

| file | size (B) | md5 | `db_type` |
|---|---:|---|---|
| `boot.img` | 67,108,864 | `a16811dcd6052c0b9a4033ec5cf120e5` | `BOOT` |
| `dtbo.img` | 16,777,216 | `a0de089230ebd2ac9f420bc6cb5cf5cc` | `DTB` |
| `init_boot.img` | 8,388,608 | `be6b233b728a554a2227acb549d32755` | `BOOT` |
| `tzsw.img` | 6,737,920 | `59453d546435b4b8d4dac043fb960f8e` | `BOOT` |
| `abl.img` | 1,941,504 | `88b2fa858e94a6daade25761638c190c` | `UEFIBOOT` |
| `pvmfw.img` | 1,048,576 | `50f4daa12d490e539c0d4d06d7d505e4` | `SECURITY` |
| `bl31.img` | 98,304 | `3d88ddb05dd44c488839ea4b937eccfc` | `BOOT` |
| `bl1.img` | 12,288 | `5fbc782b518162ea78143bb474850d13` | `BOOT` |
| `vbmeta.img` | 8,192 | `38feb1a3a533660bde5be9216c605aec` | `AVB` |

[F] 9 rows, 9 distinct md5, total **102,121,472 B**, all `db_path = google/cheetah/radio`,
`interface_documented = n` on all 9.

[I] This is an **Arm trusted-boot grammar, not Qualcomm**: `bl1`/`bl31` are ARM Trusted
Firmware stages, `tzsw` is Samsung TZ software, `abl` is the Android bootloader, `pvmfw` is
the protected-VM firmware, `vbmeta` is AVB. No `.mdt`/`.bXX` split anywhere — so the whole
Qualcomm toolchain from the #1466/#1472 notes does not apply here.

[I] The `db_type` column is doing real work on this device and is **not** a rename of
`blob_family`: `UEFIBOOT` for `abl`, `SECURITY` for `pvmfw`, `AVB` for `vbmeta`, `DTB` for
`dtbo`. Four of nine rows carry a type that is more specific than "boot".

## 2. The inversion: constant size, distinct bytes

[F] Across the **13 Tensor devices**, the 9 files split cleanly by how much information the
size column carries:

| file | distinct sizes (13 devices) | distinct md5 | what `size_bytes` carries |
|---|---:|---:|---|
| `boot.img` | **1** | 13 | **nothing** |
| `dtbo.img` | **1** | 13 | **nothing** |
| `init_boot.img` | **1** | 13 | **nothing** |
| `pvmfw.img` | **1** | 13 | **nothing** |
| `vbmeta.img` | **1** | 13 | **nothing** |
| `bl1.img` | 3 | 8 | SoC generation |
| `bl31.img` | 3 | 8 | SoC generation |
| `tzsw.img` | 3 | 8 | SoC generation |
| `abl.img` | 7 | 8 | device |

[F] The five constant-size files are the exact round numbers you would guess:

```
boot.img        67,108,864 B  = 64 MiB    (all 13)
dtbo.img        16,777,216 B  = 16 MiB    (all 13)
init_boot.img    8,388,608 B  =  8 MiB    (all 13)
pvmfw.img        1,048,576 B  =  1 MiB    (all 13)
vbmeta.img           8,192 B  = 8 KiB     (all 13)
```

[I] **This is the opposite of #1466's reading.** #1466 treats MiB-exactness as evidence of a
*partition dump* rather than a built image, and on its Qualcomm rows that is right. Here the
MiB-exact files are the **most** device-specific ones — 13 distinct md5 out of 13 devices —
and the irregular files are the **shared** ones. So MiB-exactness says nothing about
whether a blob is a dump or a build; it says something about which layer of the boot chain
the file belongs to.

[N] **I tested the tempting generalisation and it is false.** "MiB-exact ⇒ device-unique"
fails on 8 fleet-wide filenames: `vbmeta.img` (0% MiB-exact but 97% device-unique),
`qupfw.img`, `xbl_config.img`, `shrm.img`, `rpm.img`, `aop_config.img`, `uefi.img`,
`xbl_ramdump.img`. The inversion is a property of **this family**, not of the matrix.

[I] The mechanism is plausible and I state it as inference only: the five constant-size files
are **partition images** whose length is the partition's declared capacity (a fixed A/B
slot size per Tensor generation), while the four variable files are **code blobs** whose
length is whatever the toolchain emitted. The md5 differs across the five because each
carries that device's kernel, DTBO, ramdisk and AVB metadata — content differs, length does
not.

## 3. The firmware files partition by SoC generation, then by device

[F] For the four variable files, **size uniquely determines the SoC generation, with no
exceptions**:

| file | GS201 (5 devs) | G3 (3 devs) | G4 (5 devs) | size→generation pure |
|---|---:|---:|---:|---|
| `bl1.img` | 12,288 | 16,384 | 20,480 | ✅ |
| `bl31.img` | 98,304 | 110,592 | 114,688 | ✅ |
| `tzsw.img` | 6,737,920 | 7,864,320 | 7,811,072 | ✅ |
| `abl.img` | *(4 sizes)* | *(2 sizes)* | 2,740,224 | ✅ |

[F] And for all four, **md5 is a strict refinement of size**: same md5 ⇒ same size (0
counterexamples), and same size does **not** imply same md5.

[F] The md5 partition is **identical for all four files**, which is a strong internal
consistency result — four independent binaries, four different sizes, one sharing topology:

| devices sharing an md5 | count | which |
|---|---:|---|
| `Pixel_9`, `Pixel_9_Pro`, `Pixel_9_Pro_Fold`, `Pixel_9_Pro_XL` | 4 | G4 flagship group |
| `Pixel_8`, `Pixel_8_Pro` | 2 | G3 |
| `Pixel_7`, `Pixel_7_Pro` | 2 | GS201 |
| `Pixel_8A`, `Pixel_9A`, `Pixel_7a`, `Pixel_Fold`, `Pixel_Tablet` | 1 each | the rest |

[F] `partition(abl.img) == partition(bl1.img) == partition(bl31.img) ==
partition(tzsw.img)` — verified as set equality, **True**.

[I] So `abl.img` is the informative one: it has **7 distinct sizes** but the **same 8-way
sharing topology** as `bl1.img`, which has only 3. **Size and sharing are independent
axes.** A parser that grouped devices by `abl` size would split `Pixel_7a`/`Pixel_Fold`/
`Pixel_Tablet` apart even though their sharing behaviour is identical to every other file.

### 3.1 The "A" suffix predicts uniqueness — 12/12

[F] Within every generation that has an "A" variant, that device is the **only** one that
does not share its firmware with a sibling:

| generation | shared group | unique device |
|---|---|---|
| G3 | `Pixel_8`, `Pixel_8_Pro` | **`Pixel_8A`** |
| G4 | `Pixel_9`, `Pixel_9_Pro`, `Pixel_9_Pro_Fold`, `Pixel_9_Pro_XL` | **`Pixel_9A`** |

[F] Tested across all 4 generations × 4 firmware files: **12/12**, zero failures. (GS201 has
no "A" variant; `Pixel_7a` is a different product line and is also unique, but it is not the
"A-suffix" rule.)

[I] The plausible reading: the "A" line is a cost-reduced variant that ships a different
secure-boot configuration even on the same silicon, so its trusted-firmware stages are
rebuilt. That is consistent with `Pixel_8A`/`Pixel_9A` also being the two devices whose
`soc` cell is **blank** in the matrix (established in #1748 §3.1 — both have
`in_builds_csv = n`).

[N] But that coincidence is **not proof of a causal link**. Two devices is two data points,
and the blank `soc` is explained by absence from `builds.csv`, not by firmware content.

### 3.2 The GS101 predecessor lacks `init_boot.img`, and that is the whole 8-vs-9 split

[F] The Pixel 6 generation (`GS101`: `Pixel_6`, `Pixel_6A`, `Pixel_6_Pro`) has **8** boot
rows; every later Tensor device has **9**. The difference is exactly one file:

```
GS101  : abl bl1 bl31 boot dtbo        pvmfw tzsw vbmeta   (8, no init_boot)
GS201+ : abl bl1 bl31 boot dtbo init_boot pvmfw tzsw vbmeta (9)
```

[F] `init_boot.img` presence tracks the generation exactly: absent on all 3 GS101 devices,
present on all 16 GS201/G3/G4 devices. No exceptions in either direction.

[I] This is the Android 13 `init_boot` partition split, which is why it appears from the
Pixel 7 onwards and not before. The matrix records the consequence correctly without
recording the cause.

## 4. Family-level counts

[F] The 13-device Tensor `boot` family:

| measure | value |
|---|---:|
| rows | 117 |
| bytes | 1,341,739,008 |
| distinct md5 | 97 |
| rows 4096-aligned | **117 / 117 = 100%** |
| rows MiB-exact | 52 / 117 = 44.4% |

[F] Compare the fleet: 1,010 of 1,038 `boot` rows are 4096-aligned (**97.3%**). Google is
**165/165 = 100%**, as are motorola (189/189), fairphone (35/35), sony (32/32), nothing
(26/26), realme (16/16) and fxtec (9/9). The exceptions are samsung (94/112 = 83.9%),
xiaomi (213/220 = 96.8%), oneplus (226/228 = 99.1%) and lenovo (5/6).

[I] 4096-alignment is near-universal, so it is **not** a discriminating property — the
Tensor family being 100% is a non-finding, and I am recording it as such rather than
presenting it as a result.

## 5. Honest negatives

1. **Web search was unavailable while writing this note.** Metasearch returned "No results
   found" for every query, including control queries, for the whole session. **No claim here
   rests on a web source** [N].
2. **I could not verify these blobs against the vendor tree.** TheMuppets
   `proprietary_vendor_google_cheetah` carries **40 files and none of the 9 boot rows** — it
   ships `mali_csffw`, `aoc.bin`, `gxp_fw_*`, `mfc_fw.bin` and similar, but the boot chain
   comes from factory images (`db_path = google/cheetah/radio`). So unlike the `gpu` notes in
   this series, **nothing here is byte-verified against an upstream source**; every statement
   is matrix-internal. This is the note's main limitation [N].

   > **Correction, 2026-11-22 (issue #1682).** This is wrong, and it is wrong in a way that
   > matters. The blobs *are* in the vendor tree — under **`radio/`**, not
   > `proprietary/vendor/firmware/`, which is the only path I checked. `radio/` holds
   > `abl.img`, `bl1.img`, `bl2.img`, `bl31.img`, `gsa.img`, `ldfw.img`, `modem.img`,
   > `pbl.img`, `tzsw.img` as **git-lfs pointers carrying the sha256 and true size**. All
   > **64/64** sizes match the matrix, and the sha256 partition reproduces the matrix md5
   > partition exactly for `abl`/`bl1`/`bl31`/`tzsw` (10 groups each, set-equal). So §3's
   > matrix-internal result **is** independently confirmed, and 4 of these 9 rows are
   > vendor-verifiable. I mis-scoped the search, not the data. See
   > `docs/devices/google/Pixel_8/boot.md` §3 and #1670. The text above is left visible
   > because the error is instructive: I searched one directory and concluded about the
   > whole tree. [N] → corrected.
3. **`sha256_if_listed` is empty for all 9 rows**, and for 1,027 of 1,038 `boot` rows
   fleet-wide (11 populated). There is no second hash to cross-check the md5s against [N].
4. **The "size ⇒ generation" purity is a 13-device, 3-generation observation.** Four
   generations if GS101 is counted, where `bl1.img` is flat at 12,288 B across GS101 and
   GS201 — so the ladder is not monotonic and I do not claim it is [I].
5. **I did not test the inversion outside the Tensor family beyond the counterexample
   check** (§2), which found 8 fleet-wide filenames where it fails. The claim is scoped to
   this family [N].
6. **The `abl.img` GS201 size spread (4 sizes for 5 devices) is unexplained.** It is the one
   file where size does not track generation cleanly, and I did not investigate why [OPEN].
7. **The "A-variant ⇒ unique firmware" rule is 12/12 but only 2 devices.** It is a pattern,
   not a law [I].
8. **No payload is committed** and no binary was parsed — this note is entirely metadata
   analysis, which is why §2's mechanism is inference rather than measurement [N].

## 6. Rule 1 — corrections for the lead, not applied here

1. **`coverage-matrix.csv` needs a `source_ref` column.** Sixth note in this series to hit
   the same wall. Here it matters more than usual: `db_path = google/cheetah/radio` names a
   location, not a release, so these 9 rows cannot be dated at all (§5.2).
2. **`size_bytes` is not one quantity across the `boot` family.** #1466 found it mixes dumps
   and builds; this note finds it mixes *constant partition capacities* and *variable code
   blobs*, and that in this family the constant ones are the device-specific ones. A single
   column cannot carry both. Splitting `size_bytes` into `declared_partition_size` and
   `artifact_size` would fix both findings at once.
3. **`sha256_if_listed` is 11/1,038 populated on `boot`.** An md5-only column with no
   provenance is not enough to verify a blob, which is exactly what §5.2 ran into.
4. **`docs/REPO-STATE-MAP.md:18`** counts only the 5 `research/soc/` GPU docs; there are now
   seven device-level Mali notes and this is the first Google `boot` note.
5. **`interface_documented = n`** on all 9 rows, and on 1,038/1,038 `boot` rows fleet-wide —
   mainline documents ARM TF `bl1`/`bl31` and AVB `vbmeta` thoroughly, so the column is
   wrong for a large fraction of this family, not just these rows.
6. **`db_type` is more informative than `blob_family` here** (`UEFIBOOT`, `SECURITY`, `AVB`,
   `DTB` vs plain `boot`) and should probably be the analysed column.

## 7. Reproduce

```sh
# run from the repo root

# the 9 rows
python3 -I -c "
import csv
r=[x for x in csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv'))
   if x['device']=='Pixel_7_Pro' and x['blob_family']=='boot']
for x in sorted(r,key=lambda y:-int(y['size_bytes'])):
    print(f\"{x['filename']:16s} {int(x['size_bytes']):>10,} {x['md5_db']} {x['db_type']}\")
print('rows',len(r),'distinct md5',len({x['md5_db'] for x in r}),
      'total',sum(int(x['size_bytes']) for x in r))"

# the inversion (section 2): sizes vs md5 across the 13 Tensor devices
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
t=['Pixel_7','Pixel_7_Pro','Pixel_7a','Pixel_Fold','Pixel_Tablet','Pixel_8','Pixel_8A',
   'Pixel_8_Pro','Pixel_9','Pixel_9A','Pixel_9_Pro','Pixel_9_Pro_Fold','Pixel_9_Pro_XL']
for f in ['abl.img','bl1.img','bl31.img','tzsw.img','boot.img','dtbo.img','init_boot.img',
          'pvmfw.img','vbmeta.img']:
    xs=[x for x in r if x['device'] in t and x['blob_family']=='boot' and x['filename']==f]
    print(f'{f:14s} sizes={len({x[\"size_bytes\"] for x in xs}):>2d} md5={len({x[\"md5_db\"] for x in xs}):>2d}')"
# expect: abl 7/8, bl1 bl31 tzsw 3/8, boot dtbo init_boot pvmfw vbmeta 1/13

# size determines generation (section 3)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
gen={'Pixel_7':'GS201','Pixel_7_Pro':'GS201','Pixel_7a':'GS201','Pixel_Fold':'GS201',
     'Pixel_Tablet':'GS201','Pixel_8':'G3','Pixel_8A':'G3','Pixel_8_Pro':'G3',
     'Pixel_9':'G4','Pixel_9A':'G4','Pixel_9_Pro':'G4','Pixel_9_Pro_Fold':'G4',
     'Pixel_9_Pro_XL':'G4'}
for f in ['bl1.img','bl31.img','tzsw.img']:
    g=defaultdict(set)
    for d in gen:
        xs=[x for x in r if x['device']==d and x['blob_family']=='boot' and x['filename']==f]
        g[xs[0]['size_bytes']].add(gen[d])
    print(f, {s:sorted(v) for s,v in sorted(g.items(),key=lambda kv:int(kv[0]))},
          'pure:', all(len(v)==1 for v in g.values()))"

# the sharing topology is identical for all four firmware files (section 3)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
t=['Pixel_7','Pixel_7_Pro','Pixel_7a','Pixel_Fold','Pixel_Tablet','Pixel_8','Pixel_8A',
   'Pixel_8_Pro','Pixel_9','Pixel_9A','Pixel_9_Pro','Pixel_9_Pro_Fold','Pixel_9_Pro_XL']
def part(f):
    md={d:[x for x in r if x['device']==d and x['blob_family']=='boot'
          and x['filename']==f][0]['md5_db'] for d in t}
    g=defaultdict(list)
    for d,m in md.items(): g[m].append(d)
    return frozenset(frozenset(v) for v in g.values())
ps={f:part(f) for f in ['abl.img','bl1.img','bl31.img','tzsw.img']}
print('all four partitions equal:', len(set(ps.values()))==1)
for b in sorted(ps['abl.img'],key=lambda s:-len(s)): print(' ',len(b),sorted(b))"
# expect: True, then blocks of 4, 2, 2 and five singletons

# init_boot explains the 8-vs-9 split (section 3.2)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for d in ['Pixel_6','Pixel_6A','Pixel_6_Pro','Pixel_7','Pixel_7_Pro']:
    b=[x for x in r if x['device']==d and x['blob_family']=='boot']
    print(d, len(b), 'init_boot' if any(x['filename']=='init_boot.img' for x in b) else 'no init_boot')"
# expect: 8 no init_boot for the three GS101, 9 init_boot for the two GS201
```

## What would upgrade this finding

1. **Get one real boot blob and hash it.** Everything here is matrix-internal because
   TheMuppets does not ship boot blobs (§5.2). A single factory-image `bl1.img` from
   `cheetah` would turn the whole note from metadata analysis into measurement.
2. Explain the `abl.img` GS201 spread (4 sizes for 5 devices) — the one file that breaks the
   generation rule.
3. Test the A-variant rule on a generation that has more than one "A" device, if one exists
   in a later matrix revision.
4. Apply the same two-axis split (constant-size payload vs variable-size firmware) to another
   vendor's `boot` family, to see whether the inversion is Tensor-specific or general.

Not legal advice. All facts are DB metadata. No binary was parsed and no payload is
committed.
