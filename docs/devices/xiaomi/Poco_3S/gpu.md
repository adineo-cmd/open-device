# xiaomi Poco_3S (Mi8937) — `gpu` family: 3 rows, and a `db_type` that tracks the filename, not the function

Analysis date 2026-11-22. Analyst: OC-3 (issue [#1784](https://github.com/adineo-cmd/open-device/issues/1784)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows, 781 `gpu`),
`device-inventory.csv`.

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art

- [`research/soc/Qualcomm-MSM8998-Snapdragon-835-gpu.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/soc/Qualcomm-MSM8998-Snapdragon-835-gpu.md)
  §3.1 `:154-172` — **the decisive prior art.** It already enumerates the a5xx device set and
  records that `a530_pm4.fw` is byte-identical on all six holders. It also states the two
  observations I would otherwise have claimed: that an SDM845 label carrying `a530_*` is a
  generation mismatch, and that the a5xx files belong to a different device set than MSM8998.
- [`research/fleet/gpu-bdwlan.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/fleet/gpu-bdwlan.md)
  `:109` — **contains a stale claim I correct below.** It asserts *"coverage-matrix.csv contains
  no `*zap*` rows at all"*. That is false: the matrix has **373** rows whose filename contains
  `zap`.
- [`research/laptop/sharing-clusters.csv`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/laptop/sharing-clusters.csv)
  — already records the a5xx md5 clusters, e.g. `a530_pm4.fw` at `device_count = 6`
  (`Mi8937;discovery;kirin;mermaid;pioneer;voyager`) and `a506_zap.mdt` / `a512_zap.mdt` as
  singletons. The bare sharing facts are on disk; see honest-negative 6.
- [`Pixel_7a/gpu.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/google/Pixel_7a/gpu.md)
  (#1676) and the Google `gpu` notes — the Mali half of the `gpu` family, where
  `interface_documented = n` on all rows. Not applicable here (no Mali row) but it is the
  same family and the contrast is worth naming.

## Verdict

[F] `Poco_3S` (`Mi8937`, `soc` **blank**) has **19 matrix rows**, 3 of them `gpu` — **43,444 B**
total, **3 distinct md5**, all `priority = P3`, all `db_path = xiaomi/Mi8937/vendor/firmware`:

| file | size (B) | md5 | `db_type` |
|---|---:|---|---|
| `a530_pm4.fw` | 19,652 | `68d56e5b64604195d68ae26108e37da8` | **`WIFI_BLUETOOTH`** |
| `a530_pfp.fw` | 17,108 | `87ff2b00ee546081f760979e7dd55084` | **`WIFI_BLUETOOTH`** |
| `a506_zap.mdt` | 6,684 | `7f9ad7647b164859bddced15ad9be86d` | `ELF64` |

> **The headline.** Three results, in descending order of how much is mine.
>
> **1. `db_type` on this family tracks the filename prefix, not the function.** All **42** `gpu`
> rows in the whole fleet tagged `WIFI_BLUETOOTH` are `a530*` microcode files, on exactly the 6
> a5xx devices — and `a530*` is the Adreno GPU microcode, not Wi-Fi firmware. Meanwhile the
> `zap` shader blobs in the same directory get `ELF64`. The label splits on the name (§3).
>
> **2. `zap` is chip-scoped while the Adreno microcode is family-scoped — and this is visible in
> the driver, not just the data.** Every one of the 6 a5xx devices carries `a530*` microcode but
> a `zap` numbered `a506`/`a508`/`a512`, and **no `a530_zap.mdt` exists in the fleet**. The
> reason is in `a5xx_catalog.c`: `.zapfw` sits in the per-chip entry while the `.fw` PM4/PFP
> slots are borrowed from the a530 entries (§4).
>
> **3. All three `a5xx` `zap` files are exactly 6,684 B with exactly one md5 each.** That
> combination — one size *and* one build per filename — is unique to a5xx in the family.
> `a610_zap.mdt` is also size-constant (6,860 B) but carries **14 md5s**, and `a615`/`a660`
> carry 3 and 2 sizes. So on a5xx the `zap` filename is a reliable identity key; on a6xx it is
> not (§4).
>
> Two prior-art numbers are corrected: the a5xx row count is **49**, not 47, and
> `gpu-bdwlan.md`'s "no `*zap*` rows at all" is wrong by 373.

## 1. The device, and what its `soc` cell does not say

[F] `Poco_3S`: `vendor = xiaomi`, `build_codename = Mi8937`, `soc` **blank**, `soc_source`
**blank**, `in_builds_csv = y`, `blob_rows_devices_sql = 19`. All 19 rows are present in the
matrix.

[F] The codename `Mi8937` is the MSM8937 platform. `Mi8937` appears in **exactly one** device's
`db_path` — this one — so there is no second device to compare a platform-level claim against.

[N] **I do not assert what SoC this device has.** The `soc` cell is blank, the codename implies
MSM8937 (Adreno 505, an `a5xx` part), and the firmware is `a530*` microcode. Those three are
*consistent with* an MSM8937/Adreno-505 device but none of them proves it, and prior art
already records the same family of label mismatch for SDM845 carrying `a530_*`. Recorded as
[OPEN], not concluded.

[F] Row composition: `boot` 3, `other` 1, `gpu` 3, `wifi` 12.

## 2. The three `gpu` rows, and how they sit against the other five a5xx devices

[F] Exactly **6 devices** in the fleet carry a5xx GPU firmware, **49 rows** total:

| device | `soc` label | a5xx rows |
|---|---|---:|
| `Poco_3S` | *(blank)* | **3** |
| `Xperia_10` | *(blank)* | 9 |
| `Xperia_10_Plus` | SDM636 636 | **10** |
| `Xperia_XA2` | SDM845 845 | 9 |
| `Xperia_XA2_Plus` | SDM845 845 | 9 |
| `Xperia_XA2_Ultra` | SDM845 845 | 9 |

[F] The md5 grid (`-` = file absent on that device):

| file | Poco_3S | Xperia_10 | 10_Plus | XA2 | XA2_Plus | XA2_Ultra |
|---|---|---|---|---|---|---|
| `a506_zap.mdt` | `7f9ad764` | - | - | - | - | - |
| `a508_zap.mdt` | - | `2831adca` | `2831adca` | `2831adca` | `2831adca` | `2831adca` |
| `a512_zap.mdt` | - | - | `851eac43` | - | - | - |
| `a530_gpmu.fw2` | - | `2e9ddbd0` | `2e9ddbd0` | `2e9ddbd0` | `2e9ddbd0` | `2e9ddbd0` |
| `a530_pfp.fw` | **`87ff2b00`** | `b501ac92` | `b501ac92` | `b501ac92` | `b501ac92` | `b501ac92` |
| `a530_pm4.fw` | `68d56e5b` | `68d56e5b` | `68d56e5b` | `68d56e5b` | `68d56e5b` | `68d56e5b` |
| `a530v1_pfp.fw` | - | `509665e3` | `509665e3` | `509665e3` | `509665e3` | `509665e3` |
| `a530v1_pm4.fw` | - | `5e04bd3c` | `5e04bd3c` | `5e04bd3c` | `5e04bd3c` | `5e04bd3c` |
| `a530v2_seq.fw2` | - | `105095e4` | `105095e4` | `105095e4` | `105095e4` | `105095e4` |
| `a530v3_gpmu.fw2` | - | `169b8c19` | `169b8c19` | `169b8c19` | `169b8c19` | `169b8c19` |
| `a530v3_seq.fw2` | - | `d0de1846` | `d0de1846` | `d0de1846` | `d0de1846` | `d0de1846` |

[F] **`a530_pm4.fw` is byte-identical on all 6 devices** (19,652 B) — the fleet-wide invariant
prior art already records at `MSM8998…gpu.md:168-170`.

[F] **`a530_pfp.fw` is the single discriminator**: `Poco_3S` carries a **different** build
(`87ff2b00`, 17,108 B) while the other five share one (`b501ac92`, 16,820 B). So the PM4
microcode is fleet-constant and the PFP microcode is not.

[F] The four Xperia SDM845 devices plus `Xperia_10` (blank `soc`) are **md5-identical on all 9
of their shared files**. `Poco_3S` shares exactly one file with them.

## 3. `db_type` tracks the filename prefix, not the function

This is the finding I consider most useful, because it is a defect a consumer would hit.

[F] The `gpu` family spans 781 rows with five `db_type` values:

```
GPU 166 | ELF64 189 | UNKNOWN 305 | AUDIO 79 | WIFI_BLUETOOTH 42
```

[F] **All 42 `WIFI_BLUETOOTH` rows in the `gpu` family are `a530*` files, on exactly the 6 a5xx
devices.** Not one of them is Wi-Fi firmware: `a530_pm4.fw`, `a530_pfp.fw`, `a530_gpmu.fw2`,
`a530v1_*`, `a530v2_seq.fw2`, `a530v3_*` are Adreno GPU microcode, the files
`a5xx_catalog.c` binds to an a5xx Adreno.

[F] The split inside the same directory is by **name**:

| name shape | rows | `db_type` |
|---|---:|---|
| `a530*` (microcode) | 42 | **`WIFI_BLUETOOTH`** |
| `*zap.mdt` (shader) | 7 | **`ELF64`** |

[F] Both are in `xiaomi/Mi8937/vendor/firmware` and `sony/*/vendor/firmware` — the same
directory. So `db_path` does not explain the difference either.

[I] The rule appears to be a **suffix-and-prefix heuristic**: `.fw`/`.fw2` maps to a wireless
bucket unless the name is recognised as GPU, and `a530*` was not recognised; `.mdt` maps to
`ELF64` as a container format. That is a **format guess**, not a function classification.

[F] It is not a one-off. Across the whole matrix, `WIFI_BLUETOOTH` covers **251 distinct
filenames** and 3,294 rows, and its members are genuinely wireless (`bdwlan.b0*`, `regdb.bin`,
`amss20.bin`, `m3.bin`). The 42 `a530*` rows are the only GPU entries in it.

[N] I did **not** determine whether the mislabel comes from a parser rule or a hand edit — the
matrix carries no provenance column for `db_type`. [OPEN]

## 4. The `zap` generation is not the microcode generation

[F] Every a5xx device carries `a530*` microcode. **None carries an `a530_zap`** — and no
`a530_zap.mdt` exists anywhere in the fleet:

```
a530_zap.mdt   0 rows
a540_zap.mdt   0 rows
```

[F] Instead the `zap` name varies per device while the microcode generation is constant:

| device | `zap` file(s) | microcode generation |
|---|---|---|
| `Poco_3S` | `a506` | `a530` |
| `Xperia_10` | `a508` | `a530` |
| `Xperia_XA2` | `a508` | `a530` |
| `Xperia_XA2_Plus` | `a508` | `a530` |
| `Xperia_XA2_Ultra` | `a508` | `a530` |
| `Xperia_10_Plus` | **`a508` and `a512`** | `a530` |

[I] **The mechanism is in the driver's own data structure, and prior art already quotes it.**
`research/soc/Qualcomm-MSM8998-Snapdragon-835-gpu.md:28-40` reproduces the `a5xx_catalog.c`
chip entry for `revn = 540`, and in it:

```c
.fw = {
    [ADRENO_FW_PM4]  = "a530_pm4.fw",
    [ADRENO_FW_PFP]  = "a530_pfp.fw",
    [ADRENO_FW_GPMU] = "a540_gpmu.fw2",
},
.zapfw = "a540_zap.mdt",
```

`.zapfw` is a **field of the per-chip entry**, while the `.fw` array members are inherited from
other entries — `:49` states plainly that the PM4/PFP pair is *"borrowed from the a530
entries"*. So **`zap` is chip-scoped and the PM4/PFP microcode is family-scoped.** That is
exactly the pattern in the table: six devices, one microcode generation, three different `zap`
names.

[N] That reading explains the *shape* but does **not** identify which chip each `a506`/`a508`/
`a512` corresponds to. I did not verify these names against their chip-ID entries in
`a5xx_catalog.c`, and `Poco_3S` carries `a506_zap` while its `Mi8937` codename implies an
Adreno 505 part — a number I cannot reconcile without the actual catalog source. Recorded
[OPEN] rather than asserted.

[F] **All three a5xx `zap` files are exactly 6,684 B** — `a506_zap.mdt`, `a508_zap.mdt`,
`a512_zap.mdt`. Each is a single distinct md5 per filename (`a508` is one md5 across its 5
devices).

[F] That combination is unusual. Across all 147 `zap.mdt` rows there are **10 distinct sizes**,
and no a6xx file matches a5xx's one-size-one-md5 property:

| file | distinct sizes | distinct md5 | range (B) |
|---|---:|---:|---|
| `a506_zap.mdt` | **1** | **1** | 6,684 |
| `a508_zap.mdt` | **1** | **1** | 6,684 |
| `a512_zap.mdt` | **1** | **1** | 6,684 |
| `a610_zap.mdt` | 1 | **14** | 6,860 |
| `a615_zap.mdt` | **3** | 18 | 6,684–6,860 |
| `a660_zap.mdt` | **2** | 11 | 6,708–6,860 |

[F] `a610_zap.mdt` is the one a6xx file that is also size-constant (6,860 B on all 16 rows) —
but it carries **14 distinct md5s**, so size is constant while content is not. **Only a5xx is
one-size *and* one-md5.**

[I] Reading: on a5xx the `zap` payload is a **single build per generation name** and the size is
frozen at 6,684 B. On a6xx the same filename carries many builds at several sizes. So the
`zap` filename is a reliable identity key on a5xx and **not** one on a6xx — which is the
opposite of the usual assumption that a shared filename implies a shared blob.

[F] **`Xperia_10_Plus` is the only device in the fleet carrying two `a5xx` `zap` files**
(`a508` and `a512`), and it is also the only one of the six whose `soc` is not SDM845/blank —
it is labelled SDM636. Both facts are unexplained here. [OPEN]

[N] **`.mdt`-only vs split sets.** All three a5xx `zap` files are **`.mdt` with no `.b00`
companions**, unlike `a610`/`a615`/`a660`/`a740` which are split sets. I did not decode either
form, so I cannot say whether the a5xx `zap` is genuinely single-file or the companions were
not extracted. [OPEN]

## 5. Honest negatives

1. **No blob was fetched or parsed.** Every claim is matrix metadata. Nothing is byte-verified
   beyond the md5 the matrix records.
2. **`Poco_3S`'s SoC is not established.** `soc` is blank; the `Mi8937` codename and `a530*`
   firmware are consistent with MSM8937/Adreno 505 but do not prove it. §1 [OPEN].
3. **I did not check the vendor tree.** Unlike the Pixel notes, I did not fetch a git-lfs
   pointer set for `Mi8937`, so there is **no independent hash** for any of these 3 rows [N].
4. **The `db_type` mechanism is not identified.** I show the correlation (all 42 are `a530*`)
   but not whether a rule or a hand edit produced it, and the matrix has no `db_type`
   provenance [OPEN].
5. **`a530_pfp.fw` differing only on `Poco_3S` is unexplained.** Two sizes (17,108 vs 16,820)
   and two md5s; I did not determine which is newer or whether the difference is a build
   variant [OPEN].
6. **The bare sharing facts are prior art.** `sharing-clusters.csv` already lists the a5xx
   clusters with `device_count` and device lists, and `MSM8998…gpu.md:168-170` already states
   the `a530_pm4.fw` invariant. I re-derive the *interpretation*, not the counts.
7. **Gate 0 web search was unavailable** (`websearch` HTTP 402, `searxng` unmounted). **No claim
   rests on a web source** [N].
8. **`Xperia_10_Plus` carrying two `zap` generations is a single observation.** One device is
   not a pattern; I flag it rather than generalise [N].

## 6. Rule 1 — corrections to prior work

1. **`research/fleet/gpu-bdwlan.md:109` is stale and false.** It states, in a table row about
   the ten on-disk zap files:

   > `coverage-matrix.csv contains no *zap* rows at all`

   **The matrix has 373 rows whose filename contains `zap`**, 147 of them `zap.mdt`, spanning
   **15 GPU `a5xx`/`a6xx` zap basenames** plus 3 false positives (`egtzappf`, `fpctzapp`,
   `fpctzappfingerprint` — FPC/Goodix fingerprint TZ apps, not shader blobs; the trap
   `research/fleet/other-fingerprint.md:152` warns about). Among them are `a615_zap.mdt`
   (27 rows) and `a660_zap.mdt` (21 rows) — the two files that note says it could not check.
   The "Bottom line" at `:120-121` repeats the error: *"the ZAP shader files could not be
   checked against the DB (absent from it)"*. They are present. **This is a correctable claim,
   and correcting it is what makes §4 above possible.**
2. **`research/soc/Qualcomm-MSM8998-Snapdragon-835-gpu.md:156-164` undercounts the a5xx set.**
   It reports **47 rows across 6 devices** and lists `Poco_3S` with 2 files and
   `Xperia_10_Plus` with 9. The matrix has **49 rows**: `Poco_3S` carries **3**
   (`a506_zap.mdt` is omitted from that table) and `Xperia_10_Plus` carries **10**
   (`a512_zap.mdt` is omitted). The prose conclusion — "none is an MSM8998 device" — is
   unaffected, but the count and both per-device cells are wrong.
3. **`a530*` microcode is tagged `db_type = WIFI_BLUETOOTH`** on all 42 rows (§3). GPU
   microcode should not be in a wireless bucket. A data fix, not a research question.
4. **`a506_zap.mdt`, `a512_zap.mdt` and `a508_zap.mdt` are `ELF64`** while the microcode in the
   same directory is `WIFI_BLUETOOTH` — so `db_type` is inconsistent within one `db_path`.
5. **`Poco_3S` has `soc` blank with `in_builds_csv = y`.** Consistent with the known
   `builds.csv` blank-cell pattern (#1748 §3.1), not a new defect — noted so it is not
   re-investigated.

## 7. Reproduce

```sh
# run from the repo root

# the device's 3 gpu rows (section 1)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g=[x for x in r if x['device']=='Poco_3S' and x['blob_family']=='gpu']
print('rows',len(g),'bytes',sum(int(x['size_bytes']) for x in g),'md5',len({x['md5_db'] for x in g}))
for x in sorted(g,key=lambda z:-int(z['size_bytes'])):
    print(f\"{x['filename']:16s} {int(x['size_bytes']):>7,} {x['md5_db']} {x['db_type']}\")"
# expect 3 rows / 43444 B / md5 3, with WIFI_BLUETOOTH on the two a530 files

# the a5xx device set is 6 devices / 49 rows (section 2)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
a5=[x for x in r if x['blob_family']=='gpu' and x['filename'].startswith('a5')]
per=defaultdict(int)
for x in a5: per[x['device']]+=1
print('devices',len(per),'rows',len(a5))
for d in sorted(per): print(' ',d,per[d])"
# expect devices 6 rows 49; Poco_3S 3, Xperia_10_Plus 10, the rest 9

# all 42 WIFI_BLUETOOTH gpu rows are a530* (section 3)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
w=[x for x in r if x['blob_family']=='gpu' and x['db_type']=='WIFI_BLUETOOTH']
print('rows',len(w),'all a530*',all(x['filename'].startswith('a530') for x in w))
print('devices',sorted({x['device'] for x in w}))"
# expect rows 42, all a530* True, 6 devices

# no a530_zap exists, and the a5xx zap sizes are all 6684 (section 4)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for f in ['a530_zap.mdt','a506_zap.mdt','a508_zap.mdt','a512_zap.mdt','a615_zap.mdt','a660_zap.mdt']:
    xs=[x for x in r if x['filename']==f]
    print(f,len(xs),'rows',sorted({int(x['size_bytes']) for x in xs}),'md5s',len({x['md5_db'] for x in xs}))"
# expect a530_zap.mdt 0 rows; the three a5xx all [6684] with 1 md5;
# a615 [6684, 6708, 6860]; a660 [6708, 6860]

# the zap claim in gpu-bdwlan.md is stale (section 6)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
z=[x for x in r if 'zap' in x['filename'].lower()]
print('rows with zap in filename',len(z),'zap.mdt',sum(1 for x in z if x['filename'].endswith('.mdt')))"
# expect 373 and 147
```

## What would upgrade this finding

1. **Fetch the `Mi8937` vendor tree** (TheMuppets or xiaomi vendor repos) for git-lfs pointer
   hashes, giving these 3 rows the independent-hash check the Pixel notes have.
2. **Decode `a506_zap.mdt` vs `a508_zap.mdt` vs `a512_zap.mdt`** — all 6,684 B, all distinct
   md5. The size is frozen, so the difference is content; whether that is a GPU stepping or a
   region map would settle what the `zap` number means.
3. **Establish `Poco_3S`'s real SoC** from an independent source, closing the §1 [OPEN].

Not legal advice. All facts are DB metadata and inventory metadata. No binary was parsed and no
payload is committed.
