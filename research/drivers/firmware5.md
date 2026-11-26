# Driver interface: `db_type=FIRMWARE5` — 3 rows, 1 filename, no kernel loader

Issue #883. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative / [OPEN] unresolved. Every number is from a command run on
**2026-11-26** against the committed matrix
(`upstream-contribution/blob-database/coverage-matrix.csv`, 33,917 data rows),
`torvalds/linux` master, and the public LineageOS device trees for the three
devices in this bucket.

**No payload exists in this workspace and none was read.** Every statement below
is matrix metadata — filename, size, `db_type`, `db_path`, md5 — public GPL
source, or a published device-tree file list. No vendor ELF is parsed and no
instruction is disassembled [N].

## Headline: `FIRMWARE5` is one filename, and it cannot be kernel-loaded

The bucket is **`anc.bin`** — three rows, three devices, three sizes, and it
lives at `vendor/etc/camera/` on all three [F]. There is no driver to find,
because the kernel's firmware search path does not include that directory:

```c
static const char * const fw_path[] = {
	fw_path_para,
	"/lib/firmware/updates/" UTS_RELEASE,
	"/lib/firmware/updates",
	"/lib/firmware/" UTS_RELEASE,
	"/lib/firmware"
};
```

That is the whole of `drivers/base/firmware_loader/main.c`'s search path [F].
`vendor/etc/camera/anc.bin` is unreachable by `request_firmware()`. Whatever
consumes it is a userspace camera process — and the vendor libraries that ship
beside it on all three devices say which: `libanc_hdr.so`, `libanc_supervq.so`,
`libancbase.so` [F].

**The label is not a loader class at all.** The `FIRMWARE*` `db_type` family
spans haptics, bokeh, touchscreen and camera — five unrelated subsystems — and
`FIRMWARE5` holds exactly one filename in the entire corpus [F]:

| `db_type` | rows | files | what it actually holds |
|---|---:|---:|---|
| `FIRMWARE` | 42 | 8 | `brightLut.bin`, `eyesMaskNew.bin`, `haptic_rtp_lighthouse.bin`, `haptic_rtp_silk.bin` |
| `FIRMWARE10` | 8 | 3 | `fusion_mecp.bin`, `intsense_config_singlebokeh.bin`, `singlebokeh_mecp.bin` |
| `FIRMWARE5` | **3** | **1** | **`anc.bin`** |
| `FIRMWARE6` | 25 | 1 | `unified_ksqs.bin` |
| `FIRMWARE8` | 1 | 1 | `haptic_ram.bin` |
| `FIRMWARE9` | 1 | 1 | `GT9897_05.01.FF.17_4D6C5476.bin` |

So "identify the driver that loads `FIRMWARE5`" has a precise negative answer:
**none exists, and none can**, and the number `5` encodes nothing about a driver.

## The 3 rows

| device | `db_path` | bytes | md5 | SoC |
|---|---|---:|---|---|
| `Edge_40_Pro` | `motorola/rtwo/vendor/etc/camera` | 8,484,289 | `d858b23eb760919279d082f23c3371ef` | SM8550 Snapdragon 8 Gen2 |
| `FP5` | `fairphone/FP5/vendor/etc/camera` | 2,572,971 | `778849a74de8182be3abe15f2dfc01bc` | QCM6490 |
| `Poco_F5_Pro` | `xiaomi/mondrian/vendor/etc/camera` | 4,783,048 | `d54f594bd569d7c41d490c424fef5282` | *(blank)* |

Totals: **3 rows / 1 filename / 3 devices / 15,840,308 B**, `blob_family` `other`
on all three, `isa_identified` **empty on all three** [F].

Three different sizes and three different md5s means these are three different
models, not one file shipped three times — which matters for §3.

## 1. The name collision that a filename classifier gets wrong

`anc.bin` is a genuine homograph. The overwhelming majority of `anc.bin` hits on
GitHub are **audio** codec calibration files: `wcd9306_anc.bin`, `wcd9320_anc.bin`,
`wcd9310_anc.bin`, `wcd9330_anc.bin`, under `system/etc/firmware/wcd93xx/` [F].
"ANC" there means **active noise cancellation**, and those files are loaded by the
WCD93xx audio codecs.

The corpus contains **zero** of them [F]:

| probe | result |
|---|---|
| rows whose filename contains `wcd` and `anc` | **0** |
| rows with filename exactly `anc.bin` | **3**, all `db_path` ending `camera` |
| rows whose filename contains `anc` (any) | 24 rows / 16 filenames, all camera or GAN-model paths |

And mainline's audio side does not reference the string either — `wcd9335.c`
(160,967 B) and `wcd938x.c` (114,937 B) contain **0** `anc*.bin` occurrences [F].
The collision exists in the wider Android ecosystem, not in this corpus and not
in this kernel tree.

**This is the trap for the next reader.** A classifier keyed on the basename
`anc.bin` will recall the audio codec and file these three rows under sound. The
`db_path` is the field that discriminates, and it says `camera` on all three.

## 2. The bucket is a classifier artifact, and one md5 proves it

The camera bucket's `anc*` files total **11 rows**, split across **two different
`db_type`s** [F]:

| `db_type` | rows | files |
|---|---:|---|
| `FIRMWARE5` | **3** | `anc.bin` |
| `TOUCHSCREEN` | **8** | `anc_1080p.bin`, `anc_4k.bin`, `anc_cn.bin`, `anc_eu.bin`, `anc_front.bin`, `anc_main.bin`, `anc_ob_mask_1352_2400.bin`, `anc_wide.bin` |

`TOUCHSCREEN` is as wrong as `FIRMWARE5` — these are camera tuning models, not
touch controller firmware. The decisive proof is that **the same payload carries
two labels** [F]:

| md5 | filename | device | `db_type` |
|---|---|---|---|
| `778849a74de8182be3abe15f2dfc01bc` | `anc.bin` | `FP5` | **`FIRMWARE5`** |
| `778849a74de8182be3abe15f2dfc01bc` | `anc_front.bin` | `FP5` | **`TOUCHSCREEN`** |
| `778849a74de8182be3abe15f2dfc01bc` | `anc_wide.bin` | `FP5` | **`TOUCHSCREEN`** |

One byte-identical payload, three filenames, two `db_type` values. A per-file
classifier would have to give all three the same label; this database gives them
different ones. The classification is therefore **per row, not per file** [F for
the labels, I for the mechanism].

## 3. `anc.bin` is the wide-camera model under a generic name

On FP5 the plain `anc.bin` is byte-identical to `anc_wide.bin` — same md5, same
2,572,971 B [F]. The sibling set on that device is:

| file | bytes | md5 | reading |
|---|---:|---|---|
| `anc.bin` | 2,572,971 | `778849a7…` | **= `anc_wide.bin`** |
| `anc_wide.bin` | 2,572,971 | `778849a7…` | wide camera |
| `anc_front.bin` | 2,572,971 | `778849a7…` | front camera — also identical |
| `anc_main.bin` | 3,675,661 | `67bcdb04…` | main camera — the only distinct one |

So on FP5, `anc.bin`, `anc_front.bin` and `anc_wide.bin` are **one payload** and
`anc_main.bin` is the other [F]. The unqualified name is not a fourth model; it is
a copy of the front/wide model under the generic name the HAL falls back to [I].

That reading is consistent with the other devices but not proven by them: on
`Edge_40_Pro` the single `anc.bin` is 8,484,289 B and its sibling is
`anc_ob_mask_1352_2400.bin` at 12,979,200 B, a mask for a 1352×2400 sensor [F].
`Poco_F5_Pro` ships `anc.bin` at 4,783,048 B with no `anc_*` sibling in the corpus
[F]. Whether the unqualified name resolves to a particular camera on those two is
`[OPEN]`.

## 4. The loader contract: userspace, named by adjacency

No source opens the file. What the corpus and the LineageOS file lists establish
is the **neighbourhood**, and it is consistent across all three devices [F]:

| device | `libanc*` libraries shipped | `anc.bin` | `vidhance` |
|---|---|---|---|
| `Edge_40_Pro` | `libAncHumanSegFigureFusion.so`, `libanc_supervq.so`, `libancbase_rt_fusion.so` | yes | yes |
| `FP5` | `libanc_hdr.so`, `libanc_single_rt_bokeh.so`, `libanc_single_rt_bokeh_rear.so`, `libanc_supervq.so` | yes | no |
| `Poco_F5_Pro` | `libanc_dc_base.so`, `libanc_hdr.so`, `libanc_supervq.so`, `libancbase.so` | yes | yes |

FP5 additionally ships a whole `AncSuperNight` family beside it —
`cache_AncSuperNight`, `dgain_mask_AncSuperNight.bin`, `hc_opr_lite_cache_AncSuperNight`,
`siq_ocl_cache_AncSuperNight`, `superiq_model_AncSuperNight` [F]. "SuperNight" and
"SuperVQ" are night-mode and video-quality feature names, and a `dgain_mask` is a
digital-gain mask [I].

So the contract is: a vendor camera library reads a per-camera model from
`vendor/etc/camera/`, selected by filename, with no kernel involvement [I]. The
library names are the evidence; the format is not.

**The file lists prove shipping, not loading.** All three devices carry
`vendor/etc/camera/anc.bin` in `proprietary-files.txt` with **no** leading `-`
prefix, meaning LineageOS treats it as required rather than optional and copies it
verbatim [F]. A required file in a blob list is evidence that the device image
needs it; it is not evidence of which process opens it, and no `proprietary-files.txt`
can supply that.

## 5. Mainline has no camera firmware loader at all

This is the sharper negative, and it is not about this file. The Qualcomm camera
driver in mainline is `camss`, and none of its files call `request_firmware()` [F]:

| file | bytes | `request_firmware` | `anc` |
|---|---:|---:|---:|
| `camss.c` | 139,860 | **0** | **0** |
| `camss-vfe.c` | 55,809 | **0** | **0** |
| `camss-ispif.c` | 39,484 | **0** | **0** |
| `camss-csid.c` | 32,305 | **0** | **0** |

A tree-wide search of `drivers/media/platform/qcom` for `request_firmware` returns
exactly **two** files, and both are video codecs, not camera [F]:

```
drivers/media/platform/qcom/iris/iris_firmware.c
drivers/media/platform/qcom/venus/firmware.c
```

So the honest statement is not "mainline lacks a driver for `anc.bin`". It is
**mainline has no Qualcomm camera firmware loader for any camera firmware** [N].
`anc.bin` is not a special omission; it is one of a whole class that upstream
does not load.

Downstream, `CAMERA_ICP` — the camera ICP firmware that the camera bucket does
contain — appears in mainline exactly once, and only as a reserved-memory label on
a 2023+ SoC [F]:

```
arch/arm64/boot/dts/qcom/nord.dtsi
```

That is a memory carve-out, not a loader.

## 6. Filename → loader verdict

| filename | rows | verdict |
|---|---:|---|
| `anc.bin` | 3 | **No kernel loader.** Userspace camera model at `vendor/etc/camera/`, consumed by `libanc*`. Not reachable via `request_firmware()`. |
| `anc_front.bin` | 1 | Same contract; same md5 as FP5's `anc.bin`. Mislabelled `TOUCHSCREEN`. |
| `anc_wide.bin` | 1 | Same contract; same md5 as FP5's `anc.bin`. Mislabelled `TOUCHSCREEN`. |
| `anc_main.bin` | 1 | Same contract; the only distinct FP5 payload. Mislabelled `TOUCHSCREEN`. |
| `anc_ob_mask_1352_2400.bin` | 1 | Same directory, a 1352×2400 sensor mask. Mislabelled `TOUCHSCREEN`. |
| `anc_1080p.bin`, `anc_4k.bin` | 2 | Resolution-named variants on `Redmi_K60_Pro`. Mislabelled `TOUCHSCREEN`. |
| `anc_cn.bin`, `anc_eu.bin` | 2 | Region-named variants on `Mi_12T_Pro`. Mislabelled `TOUCHSCREEN`. |

Every one of the 11 is a camera userspace artifact, and **11 of 11 carry a
`db_type` that names a different subsystem** — 3 as `FIRMWARE5` and 8 as
`TOUCHSCREEN` [F].

## 7. Rule 1 pass

| file | before | after |
|---|---|---|
| `research/fleet/other-camera.md` §6 | `FIRMWARE5 | 3` row with no file named anywhere in the repo | adds a pointer to this note and the fact that the bucket is one filename, `anc.bin`, that `TOUCHSCREEN | 8` in the same table is the same `anc*` family, and that FP5's `anc.bin`/`anc_front.bin`/`anc_wide.bin` share one md5 |
| `docs/REPO-STATE-MAP.md` driver row | 10 FP6 interface docs under `research/qualcomm/docs/` | 11 driver-interface notes, adding `research/drivers/firmware5.md`; no count of FP6 docs changes |

`research/CORRECTIONS.md` gains no row: this note corrects no previously
published claim. `other-camera.md` §6 never asserted what `FIRMWARE5` *was*, only
that the bucket had 3 rows — which is still true [F].

## 8. Honest negatives

1. **No payload was read, and none exists here.** The file's internal format is
   `[OPEN]`. I do not claim it is a neural network, a LUT, a tuning blob or a
   container. Only that it is a per-camera userspace model named by the libraries
   beside it.

2. **No source opens `anc.bin`.** GitHub code search returns 111 hits for
   `vendor/etc/camera/anc.bin` and every one is a `proprietary-files.txt` line
   [F]. The loader is proprietary. §4's contract is inferred from library
   adjacency, and that inference is `[I]`, not `[F]`.

3. **"ANC" is not expanded anywhere I could find.** The audio reading (active
   noise cancellation) is a different subsystem and the corpus has 0 such rows;
   the camera reading is not documented publicly. I do not guess the acronym.

4. **The `FIRMWARE*` numbering is unexplained.** `FIRMWARE` through `FIRMWARE10`
   exist as separate `db_type` values covering haptics, bokeh, touch, camera and
   GPU-adjacent files. Whether the number is an ordinal from a vendor enum, a
   size band, or an ingest sequence is `[OPEN]` — but it demonstrably does not
   identify a driver, since `FIRMWARE5` holds one camera filename.

5. **`Poco_F5_Pro` has a blank `soc`.** Its row is one of the corpus's blank-SoC
   rows, so the device→SoC link for this bucket is 2 of 3, not 3 of 3 [F].

6. **Whether `anc.bin` is a fallback name is inference.** §3 rests on FP5, where
   the three files are byte-identical. On `Edge_40_Pro` and `Poco_F5_Pro` there is
   no sibling to compare, so the "generic fallback" reading is `[I]`.

7. **The 8 `TOUCHSCREEN` rows are reported, not fixed.** This note does not edit
   the CSV. `research/fleet/other-camera.md` §6 already establishes the
   report-only convention for `db_type` defects in this bucket.

## 9. Reproduce

Every command below was run on 2026-11-26 and exits 0.

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='FIRMWARE5']
print('rows',len(d),'files',len({r['filename'] for r in d}),'devices',len({r['device'] for r in d}),'bytes',sum(int(r['size_bytes']) for r in d))
print('filenames',sorted({r['filename'] for r in d}))
print('families',dict(Counter(r['blob_family'] for r in d)))
print('isa empty',sum(1 for r in d if not r['isa_identified'].strip()))
for r in d: print('  %-14s %-9d %-34s %s'%(r['device'],int(r['size_bytes']),r['db_path'],r['md5_db']))"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
print('wcd+anc rows',sum(1 for r in rows if 'wcd' in r['filename'].lower() and 'anc' in r['filename'].lower()))
print('anc-containing rows',sum(1 for r in rows if 'anc' in r['filename'].lower()))
a=[r for r in rows if r['filename']=='anc.bin']
print('anc.bin rows',len(a),'all camera path',all('camera' in r['db_path'] for r in a))"
```

```bash
python3 -I -c "
import csv
from collections import defaultdict
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
cam=[r for r in rows if r['filename'].startswith('anc') and 'camera' in r['db_path']]
print('camera-path anc* rows',len(cam))
from collections import Counter
print('by db_type',dict(Counter(r['db_type'] for r in cam)))
for r in sorted(cam,key=lambda x:(x['device'],x['filename'])):
    print('  %-12s %-28s %-9d %-11s %s'%(r['device'],r['filename'],int(r['size_bytes']),r['db_type'],r['md5_db']))
by=defaultdict(set)
for r in cam: by[r['md5_db']].add((r['filename'],r['device'],r['db_type']))
for m,v in by.items():
    if len({x[0] for x in v})>1:
        print('shared md5',m)
        for x in sorted(v): print('   ',x)"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for t in sorted({r['db_type'] for r in rows if r['db_type'].startswith('FIRMWARE')}):
    x=[r for r in rows if r['db_type']==t]
    print('%-11s rows=%-4d files=%-3d devices=%-4d %s'%(t,len(x),len({r['filename'] for r in x}),len({r['device'] for r in x}),sorted({r['filename'] for r in x})[:4]))"
```

```bash
python3 -I -c "
import urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x'}),timeout=60).read().decode()
        except Exception as e:
            if '404' in str(e): return None
            if i==n-1: raise
            time.sleep(8*(i+1))
t=get('https://raw.githubusercontent.com/torvalds/linux/master/drivers/base/firmware_loader/main.c')
print('main.c bytes',len(t.encode()))
i=t.find('static const char * const fw_path[]')
print(t[i:i+230])
print('vendor/etc on path?', 'vendor/etc' in t)"
```

```bash
python3 -I -c "
import urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x'}),timeout=60).read().decode()
        except Exception as e:
            if '404' in str(e): return None
            if i==n-1: raise
            time.sleep(8*(i+1))
B='https://raw.githubusercontent.com/torvalds/linux/master/drivers/media/platform/qcom/camss/'
for f in ('camss.c','camss-vfe.c','camss-ispif.c','camss-csid.c'):
    t=get(B+f)
    print('%-16s %-7d request_firmware=%d anc=%d'%(f,len(t.encode()),t.count('request_firmware'),t.lower().count('anc')))
    time.sleep(2)"
```

```bash
python3 -I -c "
import urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x'}),timeout=60).read().decode()
        except Exception as e:
            if '404' in str(e): return None
            if i==n-1: raise
            time.sleep(8*(i+1))
for repo,name in (('LineageOS/android_device_motorola_rtwo','rtwo'),('LineageOS/android_device_fairphone_FP5','FP5'),('LineageOS/android_device_xiaomi_mondrian','mondrian')):
    t=get('https://raw.githubusercontent.com/%s/lineage-22.2/proprietary-files.txt'%repo)
    lines=[l.strip() for l in t.split(chr(10))]
    anc=[l for l in lines if 'anc' in l.lower() and not l.startswith('#')]
    print('%s: %d lines, %d anc-related'%(name,len(lines),len(anc)))
    for l in anc:
        if 'camera/anc' in l or 'libanc' in l.lower(): print('   ',l)
    time.sleep(2)"
```

## Sources

| claim | source | access |
|---|---|---|
| 3 rows / 1 filename / 3 devices / 15,840,308 B; `anc.bin`; sizes 8,484,289 / 2,572,971 / 4,783,048; md5s `d858b23e…` / `778849a7…` / `d54f594b…`; `blob_family=other` ×3; `isa_identified` empty ×3; `Poco_F5_Pro` SoC blank | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-26 |
| 0 `wcd*anc*` rows; 24 `anc`-containing rows / 16 filenames; 3 `anc.bin` rows all with `camera` in `db_path` | same CSV | 2026-11-26 |
| 11 camera-path `anc*` rows split `FIRMWARE5` 3 / `TOUCHSCREEN` 8; md5 `778849a74de8182be3abe15f2dfc01bc` shared by `anc.bin`, `anc_front.bin`, `anc_wide.bin` on FP5; `anc_main.bin` md5 `67bcdb04…` | same CSV | 2026-11-26 |
| `FIRMWARE*` family: `FIRMWARE` 42/8, `FIRMWARE10` 8/3, `FIRMWARE5` 3/1, `FIRMWARE6` 25/1, `FIRMWARE8` 1/1, `FIRMWARE9` 1/1 | same CSV | 2026-11-26 |
| kernel firmware search path is `fw_path_para`, `/lib/firmware/updates/$UTS_RELEASE`, `/lib/firmware/updates`, `/lib/firmware/$UTS_RELEASE`, `/lib/firmware` (44,500 B file); `vendor/etc` absent | `drivers/base/firmware_loader/main.c`, master | 2026-11-26 |
| `camss.c` 139,860 B, `camss-vfe.c` 55,809 B, `camss-ispif.c` 39,484 B, `camss-csid.c` 32,305 B — **0** `request_firmware`, **0** `anc` in all four | `drivers/media/platform/qcom/camss/`, master | 2026-11-26 |
| only Qualcomm media `request_firmware` users are `iris/iris_firmware.c` and `venus/firmware.c` | GitHub code search `repo:torvalds/linux request_firmware path:drivers/media/platform/qcom` | 2026-11-26 |
| `CAMERA_ICP` appears in mainline once, in `arch/arm64/boot/dts/qcom/nord.dtsi` | GitHub code search `repo:torvalds/linux CAMERA_ICP` | 2026-11-26 |
| `wcd9335.c` 160,967 B and `wcd938x.c` 114,937 B contain 0 `anc*.bin`; `wcd9330.c` and `wcd934x/wcd934x.c` absent at those paths | `sound/soc/codecs/`, master | 2026-11-26 |
| `rtwo` 489-line and `mondrian` 1,126-line and FP5 1,371-line `proprietary-files.txt`; `vendor/etc/camera/anc.bin` present with no `-` prefix on all three; `libanc_hdr.so`, `libanc_supervq.so`, `libancbase.so`, `libAncHumanSegFigureFusion.so`, `libancbase_rt_fusion.so`, `libanc_dc_base.so`, `libanc_single_rt_bokeh*.so`; FP5 `AncSuperNight` family | `LineageOS/android_device_{motorola_rtwo,fairphone_FP5,xiaomi_mondrian}` `lineage-22.2` | 2026-11-26 |
| 111 GitHub hits for `"vendor/etc/camera/anc.bin"`, all `proprietary-files.txt`; 0 consumer source | GitHub code search | 2026-11-26 |
| `research/fleet/other-camera.md` §6 counts `FIRMWARE5 | 3` but never names the file | in-repo | 2026-11-26 |
