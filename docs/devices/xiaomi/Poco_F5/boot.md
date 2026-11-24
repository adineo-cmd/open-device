# xiaomi Poco_F5 (marble) — `boot` family: 9 devices, one identical 14-file set, 0 of 14 shared builds

Analysis date 2026-11-24. Analyst: OC-3 (issue [#1790](https://github.com/adineo-cmd/open-device/issues/1790)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows),
`device-inventory.csv` (249 rows).

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art

The boot chain is one of the better-studied families in this repo, but **not on this device**:

- [`research/qualcomm/docs/bootchain-census.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/research/qualcomm/docs/bootchain-census.md)
  — a genuine byte-level census, but of **Fairphone FP6 (QCM6490)** only. It decodes `xbl` as a
  multi-ELF container, `aop`/`cpucp`/`aop_config`/`shrm` as **RV32 RISC-V**, `qupfw` as
  `EM_QDSP6`, and the AVB footers on `boot`/`vendor_boot`. Its machine-readable companion
  `research/qualcomm/results/bootchain-census.json` carries a `partitions` key with 19 entries.
  **`marble` appears 0 times in it** (`grep -c marble` → `0`).
- `docs/devices/xiaomi/Poco_F5/leverage-families.md` — a **16-line stub**, scope `MODEM`
  (`bm2n06/08/12/13/14/15.bin`), ending "Deep-RE status: none yet". Zero `boot` rows.
- `docs/devices/xiaomi/Poco_12C/boot.md` — the only xiaomi `boot` note, and it is **MTK**
  (`lk`/`preloader_raw`/`gz`/`tee`), a different filename set entirely.
- `upstream-contribution/blob-database/recon.md:126-127` — the family size table, source of a
  claim corrected in §6.

**So the container and ISA work is done — on a different SoC, and I cannot redo it here**
(the matrix is metadata-only; no payload and no LFS object is present on this server). What the
FP6 census structurally cannot see is any *cross-device* statement, because it studied one
device. That is the gap this note fills.

## Verdict

`Poco_F5` (`marble`) has **14 `boot` rows / 336,936,960 B / 14 distinct md5**. All 14 sit in
`db_path = xiaomi/marble/radio`, `isa_identified` empty, `interface_documented = n`,
`priority = P3`, `sha256_if_listed` empty:

| file | size (B) | md5 | `db_type` |
|---|---:|---|---|
| `boot.img` | 201,326,592 | `59d36c26d44fe69ad9cb50afd0b41057` | `BOOT` |
| `recovery.img` | 104,857,600 | `e2799b7375ef3604464531adc667c465` | `BOOT` |
| `dtbo.img` | 25,165,824 | `7377db3e3c905bc6d49265296102f8da` | `DTB` |
| `uefi.img` | 2,760,704 | `4cdf217a5ec40b256131bf15009c8048` | `ELF64` |
| `xbl.img` | 1,093,632 | `adcc79015b1a400148d6bfc5c0548830` | `UEFIBOOT` |
| `xbl_ramdump.img` | 872,448 | `fbe8ee560a3f67447a5e9f7e4155e9b2` | `ELF64` |
| `aop.img` | 237,568 | `e03361d926466f8b123d4be7e1bab966` | `UNKNOWN` |
| `abl.img` | 204,800 | `b45e6c09a9faa15d7fd8246198b932c1` | `UEFIBOOT` |
| `cpucp.img` | 159,744 | `ded7d9733f6fbbb008189be9c18aa3b9` | `UNKNOWN` |
| `xbl_config.img` | 114,688 | `bee3493dba06adad32f17458ffae2e66` | `ELF64` |
| `shrm.img` | 65,536 | `5d13bcccd24c8d992b6d5a1d5fac0910` | `ELF64` |
| `qupfw.img` | 53,248 | `b3f266c85f926a8809a188fcec8b4379` | `ELF64` |
| `aop_config.img` | 16,384 | `7243f8d066cc9b82c0e2f9777706e64b` | `ELF64` |
| `vbmeta.img` | 8,192 | `953f37d405a8ac135c7e51e5a487ea66` | `AVB` |

`Poco_F5` has 819 matrix rows / 1,077,771,666 B in total: `other` 402, `wifi` 179, `tz` 91,
`adsp` 68, `modem` 39, `cdsp` 19, `boot` 14, `gpu` 6, `bt` 1. `soc` and `soc_source` are both
blank; `in_builds_csv = y`; codename `marble`.

> **The headline.** Nine devices in the fleet share `Poco_F5`'s **exactly identical** 14-file
> boot set — including its sibling `Poco_F5_Pro`. Sort those 14 sizes into a vector and the nine
> collapse to **3** groups; sort the 14 md5s and they stay **9**. **`Poco_F5` and `Poco_F5_Pro`
> have byte-for-byte identical size vectors and 0 of 14 shared files.** On this family the size
> column does not identify a build; it does not even identify a device.

## 1. The filename set is a clean subset of a 16-file full chain

[F] Taking the largest observed boot set as the reference — `FP6`'s 16 files — `Poco_F5`'s set is
**exactly that set minus two entries, with nothing extra**:

```
missing: cpucp_dtb.img, init_boot.img
extra  : (none)
```

[F] That exact shape is not unique to this device: **9 devices** carry precisely the same 14-file
set, and their sets compare equal:

| device | 14-file set == `Poco_F5`'s |
|---|---|
| `Mi_12` | yes |
| `Mi_12_Pro` | yes |
| `Mi_12S` | yes |
| `Mi_12S_Pro` | yes |
| `Mi_12S_Ultra` | yes |
| `Mi_12T_Pro` | yes |
| `Phone_2` | yes |
| `Poco_F5` | yes |
| `Poco_F5_Pro` | yes |

[F] Fleet-wide there are **23 distinct boot-set shapes over 123 devices**, so set shape is a weak
identifier on its own — the 14-file shape is the 4th most common (9 devices), behind 8-file (17),
9-file (13) and 5-file (11). [F] The cohort is **8 xiaomi + 1 nothing** — `Phone_2` (`Pong`) is
the sole non-xiaomi member. [I] Since eight of the nine are one vendor's 2022 flagship line, the
shape is more likely fixed by the platform generation than by the OEM, but with n=1 outside
xiaomi I cannot separate the two.

[F] `cpucp_dtb.img` exists on only **6 devices fleet-wide** (`FP6`, `Nord_4`, `OnePlus_12`,
`OnePlus_13`, `Pad_2_Pro`, `Pad_Pro`) — and those 6 are exactly the devices carrying the full
16/17-file chain. `Poco_F5` pairs `cpucp.img` with **no** DTB companion.

## 2. Size is not a build identifier — the 14-dimensional test

This is the part the single-device FP6 census could not produce.

[F] Within the 9-device cohort, per filename:

| filename | distinct sizes | distinct md5 | size constant? | md5 constant? |
|---|---:|---:|---|---|
| `aop_config.img` | 1 | 9 | **yes** | no |
| `dtbo.img` | 1 | 9 | **yes** | no |
| `qupfw.img` | 1 | 9 | **yes** | no |
| `recovery.img` | 1 | 9 | **yes** | no |
| `uefi.img` | 1 | 9 | **yes** | no |
| `vbmeta.img` | 1 | 9 | **yes** | no |
| `abl.img` | 2 | 9 | no | no |
| `aop.img` | 2 | 9 | no | no |
| `boot.img` | 2 | 9 | no | no |
| `cpucp.img` | 2 | 9 | no | no |
| `shrm.img` | 2 | 9 | no | no |
| `xbl.img` | 2 | 9 | no | no |
| `xbl_config.img` | 3 | 9 | no | no |
| `xbl_ramdump.img` | 3 | 9 | no | no |

[F] **Six of 14 filenames are size-constant across all nine devices; zero of 14 are md5-constant.**
On all 14, the partition induced by size is **not** the partition induced by md5 (0/14). Six
filenames are therefore **indistinguishable by size** on this cohort.

[F] The collapse is measurable at the device level. Building a 14-vector for each device over the
sorted filename list:

| vector | distinct values over 9 devices | groups |
|---|---:|---|
| size | **3** | `{Mi_12, Mi_12_Pro}` · `{Mi_12S, Mi_12S_Pro, Mi_12S_Ultra, Mi_12T_Pro, Poco_F5, Poco_F5_Pro}` · `{Phone_2}` |
| md5 | **9** | all singletons |

[F] **`Poco_F5` and `Poco_F5_Pro` land in the same size group.** They are two different devices
(`marble` / `mondrian`) with **identical filename sets, identical sizes on all 14 files, and
zero shared bytes**:

| | `Poco_F5` | `Poco_F5_Pro` | same? |
|---|---|---|---|
| filename set | 14 files | 14 files | **yes** |
| total bytes | 336,936,960 | 336,936,960 | **yes** |
| md5 shared | — | — | **0 of 14** |

[N] This is why the note is framed as a negative: **on `marble` there is no size or shape
signature that separates it from its own sibling.** Only the md5s do.

## 3. Fleet-wide, size buckets hide multiple builds

[F] The same test over all 26 boot filenames, pooled across devices:

| filename | rows | distinct sizes | distinct md5 | md5-per-size |
|---|---:|---:|---:|---:|
| `boot.img` | 125 | 16 | 122 | 7.6× |
| `dtbo.img` | 118 | 6 | 115 | 19.2× |
| `vbmeta.img` | 115 | 3 | 112 | **37.3×** |
| `recovery.img` | 86 | 14 | 64 | 4.6× |
| `abl.img` | 79 | 23 | 69 | 3.0× |
| `xbl.img` | 63 | 21 | 59 | 2.8× |
| `xbl_config.img` | 63 | 21 | 59 | 2.8× |
| `qupfw.img` | 63 | 7 | 58 | 8.3× |
| `aop.img` | 40 | 13 | 36 | 2.8× |
| `cpucp.img` | 30 | 11 | 29 | 2.6× |
| `shrm.img` | 30 | 8 | 29 | 3.6× |
| `init_boot.img` | 29 | **1** | **29** | **29.0×** |
| `aop_config.img` | 21 | 5 | 21 | 4.2× |
| `uefi.img` | 21 | 6 | 21 | 3.5× |
| `xbl_ramdump.img` | 21 | 10 | 21 | 2.1× |

[F] **23 of 26 boot filenames** contain at least one size value that hides more than one md5. The
worst single bucket is `boot.img` at **100,663,296 B (96 MiB)**, which holds **53 distinct
builds**.

[F] The converse never happens: **no md5 maps to more than one size** — 0 of 26 filenames. So
`md5 ⇒ size` is a hard law here, while `size ⇒ md5` is false almost everywhere.

[F] `init_boot.img` is the cleanest illustration: **29 devices, exactly one size (8,388,608 B),
29 distinct md5.** Every device's `init_boot.img` is the same length and a different build.

[F] Only **3 of 26** filenames have a size count equal to their md5 count — `lk.img` (2 rows),
`preloader_raw.img` (2), `xbl_cfg.elf` (2), all trivially small samples where every row is
unique anyway. **Size is a usable identity proxy on none of the substantive filenames.**

[I] Practical consequence: any cross-device census that groups boot blobs by `(filename, size)`
— a natural and tempting key, since `dtbo.img` at 24 MiB comes within one duplicate of being
exact (71 md5 on 72 devices, the `Realme` pair of §4) — will silently merge distinct builds on
23 of 26 filenames. **Group by md5.**

## 4. The 192 MiB `boot.img` cohort spans three SoCs

[F] `boot.img` on `Poco_F5` is exactly **192 MiB**. That value is shared by **21 rows / 21
devices / 21 distinct md5** — so again a shared size with no shared content:

```
Mi_12  Mi_12S  Mi_12S_Pro  Mi_12S_Ultra  Mi_12T_Pro  Mi_12_Pro  Mi_13  Mi_13_Pro
Nord_4  Nord_CE4  OnePlus_11_5G  OnePlus_12  OnePlus_12R  OnePlus_9  OnePlus_9RT
OnePlus_9_Pro  Pad_Pro  Poco_F5  Poco_F5_Pro  Poco_F6_PRo  Redmi_K60_Pro
```

[F] Of these 21, only 3 have a populated `soc`, and they are **three different SoCs**:

| device | `soc` |
|---|---|
| `OnePlus_9RT` | Qualcomm SM8250 Snapdragon 865 |
| `OnePlus_9_Pro` | Qualcomm SM8350 Snapdragon 888 |
| `OnePlus_11_5G` | Qualcomm SM8550 Snapdragon 8 Gen2 |

[N] So the 192 MiB figure is **not** an SoC marker and **not** a build marker — it is a
partition-cap artefact that persists across three SoC generations. The other 18 devices having
blank `soc` means I cannot extend the SoC axis; recorded as an honest negative rather than
inferred.

[F] The same holds for the other round partition sizes: `recovery.img` at 100 MiB is **28
devices / 28 md5**, and `dtbo.img` at 24 MiB is **72 devices / 71 md5** — the single duplicate
being `Realme_10_Pro` and `Realme_9_Pro` sharing one `dtbo.img`.

## 5. `db_type` is uniform per filename here — unlike `gpu`

[F] In the `boot` family, `db_type` is a pure function of the filename: **26 filenames, 0 with
more than one `db_type`**. (The `gpu` family is the same, 86 filenames / 0; the *content*
family that is not is `gpu`'s `a530*` case in the sibling note.)

[F] The 14 backend values are not obviously semantic:

| `db_type` | Poco_F5 files |
|---|---|
| `BOOT` | `boot.img`, `recovery.img` |
| `ELF64` | `uefi`, `xbl_ramdump`, `xbl_config`, `shrm`, `qupfw`, `aop_config` |
| `UEFIBOOT` | `xbl.img`, `abl.img` |
| `UNKNOWN` | `aop.img`, `cpucp.img` |
| `DTB` | `dtbo.img` |
| `AVB` | `vbmeta.img` |

[I] The `UNKNOWN` on `aop`/`cpucp` is a **classification gap, not evidence**: the FP6 census
proves both are RISC-V ELF payloads on a comparable SoC, and `research/qualcomm/docs/bootchain-census.md`
records `aop`/`cpucp`/`aop_config` as `EM_RISCV` after parsing. So a `UNKNOWN` `db_type` here
means "the classifier did not open it", not "not an ELF". I did **not** open them either.

[F] A telling asymmetry in the same family: `aop_config.img` is `ELF64` on all 21 rows while
`aop.img` is `UNKNOWN` on all 40 — the companion is typed and the main image is not.

## 6. Rule 1 — corrections for the lead, not applied here

**6.1 `recon.md:127` claims the `boot` family includes `vendor_boot`. It has 0 rows.**

The text reads:

> `| boot | 1,038 | 23.86 GB | **incl. boot.img/vendor_boot (67 MB each × many devices) — these are the FREE kernel images, not blobs**; also xbl/abl/uefi chains |`

[F] Measured on the matrix it describes:

```
rows whose filename contains 'vendor_boot' : 0
rows of size 67 MiB (70,254,592 B)         : 0
rows whose filename contains 'boot'        : 125 (boot.img only)
```

[F] `vendor_boot.img` is **entirely absent from the matrix** — as are `super.img`,
`system.img` and `product.img` (0 rows each). The census simply does not enumerate those
partitions. The `boot` family's 23.86 GB is real (`boot.img` 13.08 GB + `recovery.img` 7.54 GB
+ `dtbo.img` 2.41 GB + the rest), but **none of it is `vendor_boot`**.

[F] The `67 MB` figure is also unsupported: no row in the whole matrix is 67 MiB. The common
`boot.img` sizes are 100,663,296 (96 MiB), 201,326,592 (192 MiB) and 67,108,864 (64 MiB) — the
last is the nearest, and it is 64 MiB, not 67.

[F] Two downstream restatements inherit the error and should be corrected together:
`research/fleet/fragmentation-desktop.md:74` ("the free-kernel `boot.img`/`vendor_boot` rows…")
and `research/laptop/fragmentation-half.md:69` (which lists `vendor_boot` among the `boot`
family). The correct statement is that the family is dominated by `boot.img`/`recovery.img`,
which are *Android boot images*, and that `vendor_boot` was never enumerated.

**6.2 The "free kernel images" framing is right but the count basis is footnoted wrong.** The
`boot` family is 1,038 rows, but only **1,009** are unique `(device, filename)` pairs — see §7 —
so any per-device average should divide by 1,009.

## 7. 27 duplicate rows, none of them on this device

[F] The `boot` family has 1,038 rows but **1,009 unique `(device, filename)` pairs**: 27 pairs
appear twice. Every one of the 27 is an **exact** repeat — identical size, identical md5, in 0
cases a differing payload:

```
exact (size+md5 identical): 27
same size, different md5  :  0
different size            :  0
```

[F] They concentrate in one vendor and one cause:

| source | pairs |
|---|---:|
| `xiaomi/Mi439/radio` (`Redmi_8`) | 5 |
| `samsung/a21s/radio` (`Galaxy_A21S`) | 4 |
| `…/radio` **and** `…/vendor/etc` for the same device (18 samsung + `lenovo/heart`) | 18 |

[F] By vendor: `samsung` 17 devices, `xiaomi` 1 (`Redmi_8`), `lenovo` 1. **`Poco_F5` has none** —
its 14 rows are 14 unique pairs.

[I] The `radio` + `vendor/etc` pattern is a **dual-location capture of the same file**, not a
duplicate device build; the `Mi439`/`a21s` cases are a straight double-extraction. Either way the
rows are byte-identical, so they inflate counts but not byte totals.

## 8. Honest negatives

1. **No blob was fetched or parsed.** Every claim above is a property of the matrix columns
   `filename`, `size_bytes`, `md5_db`, `db_type`, `db_path`, `device`. Nothing here requires or
   asserts file content.
2. **No independent hash.** `sha256_if_listed` is empty on **14/14** rows, and
   `isa_identified` is empty on 14/14. The one `md5_db` column is the only content witness, and
   it is a single source — so "identical" / "different" throughout means *the database says so*,
   not that I recomputed anything.
3. **No LFS or vendor tree in this checkout.** `find -type d -name proprietary` → none;
   `find -type d -name 'marble*'` → none; no `.gitattributes` with `filter=lfs`. So the
   #1670/#1682 style of LFS-sha256 cross-check is **impossible here**, not merely skipped.
4. **`soc` is not established.** `soc` and `soc_source` are both blank. The 192 MiB cohort
   includes three *different* known SoCs (§4), so I cannot argue the SoC from firmware shape. I
   make no claim that `marble` is any particular part.
5. **`Poco_F5` vs `Poco_F5_Pro`: 0/14 shared bytes, and I cannot say why.** Different codenames,
   same everything else. Whether this is a real hardware difference or just two signing runs of
   one build is not decidable from the matrix — there is no build-id, no signature, no payload.
   [OPEN]
6. **The `cpucp_dtb.img` absence is not adjudicated.** It is missing from 117 of 123 devices, so
   I cannot tell "this SoC has no CPUCP DTB" from "the extractor missed it". The 6 devices that
   do have it all carry the 16/17-file full set, which is mild evidence the extractor is
   complete for those, but that is [I], not [F]. [OPEN]
7. **`init_boot.img` absence is unexplained for this device.** 29/123 devices have it, including
   every Google Tensor and several xiaomi/oneplus. `Poco_F5` does not. Since `boot.img` is 192 MiB
   (no ramdisk split evident from size), the plausible reading is a pre-GKI layout — but **10 of
   the other 20 devices at exactly 192 MiB *do* have `init_boot.img`** (`Mi_13`, `Mi_13_Pro`,
   `Nord_4`, `Nord_CE4`, `OnePlus_11_5G`, `OnePlus_12`, `OnePlus_12R`, `Pad_Pro`,
   `Poco_F6_PRo`, `Redmi_K60_Pro`), so size does not settle it. Left [OPEN].
8. **No container, ISA, or entry-point claim.** The `db_type` values are repeated as delivered
   and flagged as a classifier output (§5), not verified. Everything byte-level about `marble`'s
   boot chain remains unexamined.
9. **Web search unavailable.** `websearch` returned **HTTP 402** and `gh search code/repos` gave
   empty output for all three queries on 2026-11-24. Recorded in the SEARCH comment; no claim
   here depends on external prior art.

## 9. Reproduce

```bash
# run from the repo root
M=upstream-contribution/blob-database/coverage-matrix.csv

# the 14 rows (section "Verdict")
python3 -I -c "
import csv
r=list(csv.DictReader(open('$M')))
b=[x for x in r if x['device']=='Poco_F5' and x['blob_family']=='boot']
print(len(b), sum(int(x['size_bytes']) for x in b), len({x['md5_db'] for x in b}))
"
# expect: 14 336936960 14

# Poco_F5 is the full 16-file set minus exactly two, with nothing extra (section 1)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('$M')))
b=[x for x in r if x['blob_family']=='boot']
dev=defaultdict(set)
for x in b: dev[x['device']].add(x['filename'])
full=dev['FP6']
print('missing', sorted(full-dev['Poco_F5']), 'extra', sorted(dev['Poco_F5']-full))
print('devices with exactly 14:', sum(1 for f in dev.values() if len(f)==14))
print('all equal Poco_F5 set:', all(f==dev['Poco_F5'] for f in dev.values() if len(f)==14))
"
# expect: missing ['cpucp_dtb.img', 'init_boot.img'] extra [] / 9 / True

# the size-vector vs md5-vector collapse (section 2)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('$M')))
b=[x for x in r if x['blob_family']=='boot']
dev=defaultdict(set)
for x in b: dev[x['device']].add(x['filename'])
nine=[d for d,f in dev.items() if len(f)==14]
sz=defaultdict(dict); md=defaultdict(dict)
for x in b:
    if x['device'] in nine and x['filename'] in dev['Poco_F5']:
        sz[x['device']][x['filename']]=x['size_bytes']; md[x['device']][x['filename']]=x['md5_db']
fs=sorted(dev['Poco_F5'])
print('size vectors', len({tuple(sz[d][f] for f in fs) for d in nine}))
print('md5  vectors', len({tuple(md[d][f] for f in fs) for d in nine}))
"
# expect: size vectors 3 / md5 vectors 9

# Poco_F5 vs Poco_F5_Pro share sizes but not bytes (section 2)
python3 -I -c "
import csv
r=list(csv.DictReader(open('$M')))
m={}
for x in r:
    if x['blob_family']=='boot' and x['device'] in ('Poco_F5','Poco_F5_Pro'):
        m.setdefault(x['filename'],{})[x['device']]=(x['size_bytes'],x['md5_db'])
same_sz=sum(1 for f,v in m.items() if v['Poco_F5'][0]==v['Poco_F5_Pro'][0])
same_md=sum(1 for f,v in m.items() if v['Poco_F5'][1]==v['Poco_F5_Pro'][1])
print(len(m), same_sz, same_md)
"
# expect: 14 14 0

# size never implies md5 fleet-wide, and md5 always implies size (section 3)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('$M')))
b=[x for x in r if x['blob_family']=='boot']
by=defaultdict(list)
for x in b: by[x['filename']].append(x)
n=0
for f,xs in by.items():
    g=defaultdict(set)
    for x in xs: g[x['size_bytes']].add(x['md5_db'])
    if any(len(v)>1 for v in g.values()): n+=1
print('filenames with a multi-build size bucket:', n, 'of', len(by))
bad=0
for f,xs in by.items():
    g=defaultdict(set)
    for x in xs: g[x['md5_db']].add(x['size_bytes'])
    bad+=sum(1 for v in g.values() if len(v)>1)
print('md5 mapping to >1 size:', bad)
"
# expect: 23 of 26 / 0

# vbmeta: 3 sizes hide 112 builds; init_boot 1 size hides 29
python3 -I -c "
import csv
r=list(csv.DictReader(open('$M')))
b=[x for x in r if x['blob_family']=='boot']
for f in ['vbmeta.img','init_boot.img']:
    xs=[x for x in b if x['filename']==f]
    print(f, len(xs), len({x['size_bytes'] for x in xs}), len({x['md5_db'] for x in xs}))
"
# expect: vbmeta.img 115 3 112 / init_boot.img 29 1 29

# the 192 MiB cohort spans 3 known SoCs (section 4)
python3 -I -c "
import csv
r=list(csv.DictReader(open('$M')))
inv={x['model']:x for x in csv.DictReader(open('upstream-contribution/blob-database/device-inventory.csv'))}
xs=[x for x in r if x['blob_family']=='boot' and x['filename']=='boot.img' and x['size_bytes']=='201326592']
print(len(xs), len({x['md5_db'] for x in xs}), sorted(inv[x['device']]['soc'] for x in xs if inv[x['device']]['soc']))
"
# expect: 21 21 ['Qualcomm SM8250 ...', 'Qualcomm SM8350 ...', 'Qualcomm SM8550 ...']

# vendor_boot is absent; 67 MiB never occurs (section 6)
python3 -I -c "
import csv
r=list(csv.DictReader(open('$M')))
print('vendor_boot rows', sum(1 for x in r if 'vendor_boot' in x['filename'].lower()))
print('67MiB rows', sum(1 for x in r if x['size_bytes']=='70254592'))
"
# expect: vendor_boot rows 0 / 67MiB rows 0

# 1038 rows -> 1009 unique pairs, all 27 dups exact (section 7)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('$M')))
b=[x for x in r if x['blob_family']=='boot']
g=defaultdict(list)
for x in b: g[(x['device'],x['filename'])].append(x)
print('rows',len(b),'unique',len(g))
print('exact dups', sum(1 for xs in g.values() if len(xs)>1 and len({(y['size_bytes'],y['md5_db']) for y in xs})==1))
print('Poco_F5 dups', sum(1 for k,xs in g.items() if k[0]=='Poco_F5' and len(xs)>1))
"
# expect: rows 1038 unique 1009 / exact dups 27 / Poco_F5 dups 0
```

## What would upgrade this finding

- **A payload, or any second hash.** Everything here rests on one `md5_db` column. One
  independent digest — of any single one of the 14 files — would convert the entire size-vs-md5
  section from single-source to verified.
- **The actual `marble` boot chain.** `bootchain-census.md`'s method (parse `xbl` as multi-ELF,
  decode `aop`/`cpucp`/`shrm` for `e_machine`) would settle the `UNKNOWN` `db_type` values and
  give the first byte-level statement about this SoC.
- **`vendor_boot` extraction.** It is the one absent partition that the census method already
  knows how to read (FP6 §AVB), and its absence is the largest single hole in this family.
