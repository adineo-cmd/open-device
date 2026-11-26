# Driver interface: `db_type=STORAGE` — 40 rows, 5 filenames, UFS part numbers with no loader

Issue #895. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative / [OPEN] unresolved. Every number is from a command run on
**2026-11-27** against the committed matrix
(`upstream-contribution/blob-database/coverage-matrix.csv`, 33,917 data rows),
`torvalds/linux` master, and the public LineageOS device trees for the devices
in this bucket.

**No payload exists in this workspace and none was read.** Every statement below
is matrix metadata — filename, size, `db_type`, `db_path`, md5 — public GPL
source, or a published kernel log. No vendor image is parsed and no UFS
descriptor is decoded [N].

## Headline: `STORAGE` is five UFS flash part numbers, and nothing in the kernel loads them

The bucket is **five filenames on eight Pixel devices**, every one at
`google/<codename>/vendor/firmware`, and every one a **UFS device part number
with the vendor name glued to the front** [F]:

| filename | vendor | part field | rows | bytes |
|---|---|---|---:|---:|
| `KIOXIATHGJFJT1E45BATPC0100.img` | KIOXIA | `THGJFJT1E45BATPC` | 8 | 1,048,764 |
| `KIOXIATHGJFJT2T85BAT0C0100.img` | KIOXIA | `THGJFJT2T85BAT0C` | 8 | 1,048,764 |
| `MICRONMT128GBCAV2U310103.img` | MICRON | `MT128GBCAV2U3101` | 8 | 1,036,476 |
| `MICRONMT128GBCAV2U310104.img` | MICRON | `MT128GBCAV2U3101` | 8 | 1,036,476 |
| `SAMSUNGKLUDG4UHGC-B0E13103.img` | SAMSUNG | `KLUDG4UHGC-B0E13` | 8 | 774,332 |

Totals: **40 rows / 5 filenames / 8 devices / 39,558,496 B (37.73 MiB)**,
`blob_family` `other` and `blob_subfamily` `misc` on all 40, `priority` `P3` on
all 40, `isa_identified` **empty on all 40** [F].

Every device carries **all five** files, not a subset — 8 × 5 = 40 exactly [F].
That is a fixed kit: a device image ships one firmware per UFS part it might be
built with, and the bootloader or a userspace flasher picks the matching one.

**No kernel driver reads any of them**, and that is provable rather than
assumed. The two mainline UFS files that would hold such a call contain none [F]:

| file | bytes | `request_firmware` | `filp_open` | `kernel_read` | these names |
|---|---:|---:|---:|---:|---:|
| `drivers/ufs/host/ufs-qcom.c` | 85,746 | **0** | **0** | **0** | **0** |
| `drivers/ufs/core/ufshcd.c` | 321,556 | **0** | — | — | **0** |

Google's own downstream driver, `drivers/ufs/ufs-google.c`, is no different:
**0** `request_firmware`, **0** `.img` [F]. Its single `firmware` mention is a
PHY-patch timing message (`"phy firmware update took %lld usec"`) and its single
`MICRON` mention is a reset quirk — neither touches a file [F].

## The 5 filenames, and the part-number decomposition

The filenames are `<VENDOR><part><suffix>.img`, and the part field is the string
the kernel prints as the SCSI model. From a published Pixel kernel log [F]:

```
scsi 0:0:0:0: Direct-Access     KIOXIA   THGJFLT2E46BATPB 0100 PQ: 0 ANSI: 6
scsi 0:0:0:0: Direct-Access     KIOXIA   THGJFGT1E45BAIPB 0100 PQ: 0 ANSI: 6
```

Two observed devices, both `KIOXIA`, both revision `0100`, with part numbers
`THGJFLT2E46BATPB` and `THGJFGT1E45BAIPB`. Our corpus files are
`THGJFJT1E45BATPC` and `THGJFJT2T85BAT0C` — the same `THGJF` family, different
individual parts [F]. So the filename is not opaque: it names a specific flash
part, which is exactly what a per-part firmware image should do.

The decomposition, measured rather than assumed [F]:

| filename | vendor prefix | remainder | remainder length |
|---|---|---|---:|
| `KIOXIATHGJFJT1E45BATPC0100.img` | `KIOXIA` | `THGJFJT1E45BATPC0100` | 20 |
| `KIOXIATHGJFJT2T85BAT0C0100.img` | `KIOXIA` | `THGJFJT2T85BAT0C0100` | 20 |
| `MICRONMT128GBCAV2U310103.img` | `MICRON` | `MT128GBCAV2U310103` | 18 |
| `MICRONMT128GBCAV2U310104.img` | `MICRON` | `MT128GBCAV2U310104` | 18 |
| `SAMSUNGKLUDG4UHGC-B0E13103.img` | `SAMSUNG` | `KLUDG4UHGC-B0E13103` | 19 |

The suffix length is **not** constant: Kioxia carries 4 trailing characters
(`0100`), Micron 2 (`03`/`04`), Samsung 3 (`103`). I therefore do **not** claim a
single JEDEC field layout — see §7. What *is* clean is that the two Micron files
differ in exactly one character, the last:

```
MICRONMT128GBCAV2U310103   vs   MICRONMT128GBCAV2U310104
                        ^ only differing index (0-based 23 of 24)
```

Two revisions of one part, distinguished by a final digit, both shipped on all
eight devices [F]. That is a fallback pair: the bootloader picks whichever
matches the fitted silicon.

## 1. The same part family is already in this corpus under a different `db_type`

This is the finding the bucket boundary hides, and the reason a filename-keyed
search is not enough.

`research/fleet/other-fastchg.md` §3.3 already documents 15 UFS/eMMC firmware
files across 6 OnePlus/Oppo devices at `*/odm/firmware/ufs`, typed `FASTCHG` [F].
One of them is Micron part `MT128GBCAV2U31`:

| filename | `db_type` | `db_path` | bytes |
|---|---|---|---:|
| `MICRON-MT128GBCAV2U31.bin` | **`FASTCHG`** | `oneplus/aston/odm/firmware/ufs` | 1,040,592 |
| `MICRONMT128GBCAV2U310103.img` | **`STORAGE`** | `google/*/vendor/firmware` ×8 | 1,036,476 |
| `MICRONMT128GBCAV2U310104.img` | **`STORAGE`** | `google/*/vendor/firmware` ×8 | 1,036,476 |

The OnePlus name is hyphenated with a dot extension; the Pixel names glue the
vendor on and append a revision. Strip the vendor prefix and the punctuation and
the OnePlus part `MT128GBCAV2U31` is a **strict prefix** of the Pixel parts
`MT128GBCAV2U310103` / `...104` [F]. Same silicon family, two ingest labels, two
naming conventions.

**They are not the same payload, and that is measurable.** The two halves share
**zero** sizes and **zero** md5s [F]:

| half | `db_type` | rows | files | sizes |
|---|---|---:|---:|---|
| OnePlus/Oppo | `FASTCHG` | 31 | 15 | 446,672 · 520,400 · 659,664 · 790,736 · 803,024 · 1,040,592 · 1,435,388 |
| Pixel | `STORAGE` | 40 | 5 | 774,332 · 1,036,476 · 1,048,764 |

Intersection of sizes: **empty**. Intersection of md5s: **empty**. Intersection
of filenames: **empty** [F]. So these are distinct firmware revisions for the
same part families, not copies of one file under two names — which is what you
expect when two OEMs ship their own validated revision of a vendor's firmware.

**Consequence for a reader:** a query that filters `db_type='STORAGE'` returns
the Pixel half and silently omits the OnePlus half of the same file class, and
vice versa. The right key is the part number with vendor prefix and punctuation
normalised, not `db_type` and not the raw basename.

## 2. Why the Pixel files are the first five entries in the file list

A trap for anyone reading `proprietary-files-vendor.txt` for ordering clues. In
`caiman` (Pixel 9 Pro) the five sit at lines 309–313, immediately before
`vendor/firmware/aoc.bin` [F]:

```
309: vendor/firmware/KIOXIATHGJFJT1E45BATPC0100.img
310: vendor/firmware/KIOXIATHGJFJT2T85BAT0C0100.img
311: vendor/firmware/MICRONMT128GBCAV2U310103.img
312: vendor/firmware/MICRONMT128GBCAV2U310104.img
313: vendor/firmware/SAMSUNGKLUDG4UHGC-B0E13103.img
314: vendor/firmware/aoc.bin
315: vendor/firmware/batt_fw_adi_79_2.bin
```

This is **not** a driver grouping. It is byte-order sort: uppercase `K`, `M`, `S`
sort before lowercase `a`, `b`, so the five part numbers land at the top of the
1,462-line (shiba) / 2,532-line (caiman) `vendor/firmware/` list purely because
their vendor prefixes are capitalised [F]. The `batt_fw` files that follow are a
different class entirely — `db_type=UNKNOWN`, documented in
`research/fleet/other-fastchg.md` §3.4.

## 3. The vendor-ID gap: mainline has no `KIOXIA`

Mainline defines exactly five UFS manufacturer IDs [F]:

```c
#define UFS_VENDOR_MICRON      0x12C
#define UFS_VENDOR_SAMSUNG     0x1CE
#define UFS_VENDOR_SKHYNIX     0x1AD
#define UFS_VENDOR_TOSHIBA     0x198
#define UFS_VENDOR_WDC         0x145
```

There is **no `UFS_VENDOR_KIOXIA`**. A tree-wide search for `KIOXIA` in
`torvalds/linux` returns 5 hits, none of them in `drivers/ufs/` — they are in
MTD/NAND (`drivers/mtd/nand/spi/toshiba.c`), NVMe (`drivers/nvme/host/{pci,core}.c`)
and a sysfs ABI document [F].

Kioxia is the renamed Toshiba Memory Corporation, so `0x198` is the ID a Kioxia
UFS device reports and the symbol is simply still named `TOSHIBA` [I]. But the
naming gap is live rather than historical: **4 of the 5 filenames in this bucket
are Kioxia**, and the corpus ships them on 8 of 8 devices. A reader grepping for
`KIOXIA` in the kernel finds nothing and could wrongly conclude the hardware is
unsupported, when in fact the quirk table matches it under the old name.

The only `MICRON` and `SAMSUNG` uses in mainline are quirk-table entries, not
firmware handling [F]:

```c
{ .wmanufacturerid = UFS_VENDOR_MICRON,
  .model = UFS_ANY_MODEL,
  .quirk = UFS_DEVICE_QUIRK_DELAY_BEFORE_LPM },
{ .wmanufacturerid = UFS_VENDOR_SAMSUNG,
  .model = UFS_ANY_MODEL,
  ...
```

So mainline knows these vendors exist and applies timing workarounds to them. It
never loads their firmware.

## 4. The `soc` column, and what is already documented

The bucket's `soc` values are `Google Tensor G3` on 25 rows, `Google Tensor G4`
on 5, and blank on 10 [F]. That looks like a finding and is not a new one:

| device | codename | `soc` in matrix | actual (public) |
|---|---|---|---|
| `Pixel_8` | `shiba` | Google Tensor G3 | G3 |
| `Pixel_8A` | `akita` | Google Tensor G3 | G3 |
| `Pixel_8_Pro` | `husky` | Google Tensor G3 | G3 |
| `Pixel_9` | `tokay` | Google Tensor G4 | G4 |
| `Pixel_9A` | `tegu` | *(blank)* | G4 |
| `Pixel_9_Pro` | `caiman` | **Google Tensor G3** | G4 |
| `Pixel_9_Pro_Fold` | `comet` | **Google Tensor G3** | G4 |
| `Pixel_9_Pro_XL` | `komodo` | *(blank)* | G4 |

This is **already reported** in `research/fleet/other-esim.md` §7 and §6.1 and in
`research/soc/Google-Tensor-GS201-gpu.md` §3.5 [F]. I cite it rather than
re-deriving it, and I add no CORRECTIONS row for it, because the claim is not
wrong anywhere and the existing notes already name the defect precisely.

It matters for this bucket in one narrow way: `STORAGE` is the *only* bucket in
which all 8 devices appear together, so a `soc`-filtered query over UFS firmware
would split the kit — `soc='Google Tensor G4'` returns 5 rows of 40, and the
`Pixel_9_Pro`/`Pixel_9_Pro_Fold` rows would be filed under G3. The five filenames
are identical across all eight devices, so **the SoC label is irrelevant to which
firmware a device carries** — the UFS part is, and that is not in the `soc`
column at all [I].

## 5. Filename → loader verdict

| filename | rows | verdict |
|---|---:|---|
| `KIOXIATHGJFJT1E45BATPC0100.img` | 8 | **No kernel loader.** UFS part `THGJFJT1E45BATPC`, revision `0100`. Read by the bootloader or a userspace flasher, not by `request_firmware()`. Format `[OPEN]`. |
| `KIOXIATHGJFJT2T85BAT0C0100.img` | 8 | Same, part `THGJFJT2T85BAT0C`. |
| `MICRONMT128GBCAV2U310103.img` | 8 | Same, Micron part `MT128GBCAV2U3101` rev `03`. Same part family as `FASTCHG`'s `MICRON-MT128GBCAV2U31.bin`, different payload. |
| `MICRONMT128GBCAV2U310104.img` | 8 | Same, rev `04` — the fallback pair to `...103`. |
| `SAMSUNGKLUDG4UHGC-B0E13103.img` | 8 | Same, Samsung part `KLUDG4UHGC-B0E13` rev `103`. |

All five are per-part UFS firmware images shipped as a kit on eight devices, and
**none of the five is referenced by any kernel source** in mainline or in Google's
downstream tree [N].

## 6. Rule 1 pass

| file | before | after |
|---|---|---|
| `research/fleet/other-fastchg.md` §3.3 | documents the 15 `FASTCHG`/`ufs` files correctly, but never mentions that the same part family appears under `STORAGE` with a different naming scheme | adds the cross-bucket note: `MICRON-MT128GBCAV2U31` is a prefix of the Pixel `MT128GBCAV2U310103`/`104` parts, the two halves share zero sizes and zero md5s, and a `db_type`-filtered query misses half the class |
| `docs/REPO-STATE-MAP.md` driver row | 3 `db_type`-scoped notes under `research/drivers/` | 4, adding `storage.md`; the 10 FP6 interface docs are unchanged |

`research/CORRECTIONS.md` gains **no** row. Nothing previously published about
this bucket was wrong: `other-fastchg.md` §3.3's reading of the OnePlus half is
accurate, and the Pixel 9 SoC defect is already correctly documented in two
notes (§4). The cross-bucket link is an addition, not a correction.

## 7. Honest negatives

1. **No payload was read, and none exists here.** The `.img` internal format is
   `[OPEN]`. I do not claim it is a UFS descriptor dump, a SCSI WRITE BUFFER
   image, a vendor container, or compressed. Nothing in this note depends on the
   format.

2. **The suffix field semantics are `[OPEN]`.** The trailing characters are 4 on
   Kioxia (`0100`), 2 on Micron (`03`/`04`) and 3 on Samsung (`103`), so there is
   no single field width and I do not assert a JEDEC layout. The *observation*
   that the two Micron files differ only in the final digit is `[F]`; calling that
   digit a "revision" is `[I]`, supported by the kernel log printing `0100` in a
   separate revision column.

3. **The part-field split is inferred from the vendor prefix, not parsed.** I
   split `KIOXIA`/`MICRON`/`SAMSUNG` off the front because those are the vendor
   strings, then report the remainder. For Samsung the remainder contains its own
   hyphen (`KLUDG4UHGC-B0E13`), so "part field" is not a single well-defined token
   and my 16/16/19-character figures are measurements of my split, not of a
   documented layout.

4. **No source opens these files.** All 140–141 GitHub hits for each exact
   filename are `proprietary-files-vendor.txt` lines in LineageOS Google device
   trees and their forks [F]. The consumer is proprietary.

5. **The kernel log evidence is from a different device than our five files.**
   `THGJFLT2E46BATPB` and `THGJFGT1E45BAIPB` are observed parts on a Pixel with a
   published log; our corpus parts are `THGJFJT1E45BATPC` and `THGJFJT2T85BAT0C`
   [F]. The *shape* of the model string is `[F]`; that our exact parts appear in
   that field is `[I]` by family resemblance.

6. **Which process flashes the image is not established.** The bootloader is the
   likely consumer — per-part selection at boot is the standard UFS model — but I
   found no source that shows it, so the mechanism is `[I]`. I do not claim it is
   the bootloader as `[F]`.

7. **The `soc` mislabel is prior art, not mine.** §4 cites
   `other-esim.md` §7/§6.1 and `Google-Tensor-GS201-gpu.md` §3.5. I did not
   independently verify the Wikipedia SoC sourcing those notes rest on.

8. **The `FASTCHG` half is out of scope.** Its 31 rows belong to whatever issue
   owns that bucket. I use them only as the contrast that makes the `STORAGE`
   boundary visible, and I did not re-audit `other-fastchg.md` §3.3's 15 filenames.

## 8. Reproduce

Every command below was run on 2026-11-27 and exits 0.

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='STORAGE']
print('rows',len(d),'files',len({r['filename'] for r in d}),'devices',len({r['device'] for r in d}))
print('bytes',sum(int(r['size_bytes']) for r in d))
print('families',dict(Counter(r['blob_family'] for r in d)))
print('subfamilies',dict(Counter(r['blob_subfamily'] for r in d)))
print('priorities',dict(Counter(r['priority'] for r in d)))
print('isa empty',sum(1 for r in d if not r['isa_identified'].strip()))
print('socs',dict(Counter(r['soc'] for r in d)))
for f in sorted({r['filename'] for r in d}):
    v=[r for r in d if r['filename']==f]
    print('  %-34s rows=%-2d size=%-8d md5=%s'%(f,len(v),int(v[0]['size_bytes']),v[0]['md5_db']))"
```

```bash
python3 -I -c "
import csv
from collections import defaultdict
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='STORAGE']
by=defaultdict(set)
for r in d: by[r['device']].add(r['filename'])
print('every device carries all 5 files:',all(len(v)==5 for v in by.values()))
for dv in sorted(by): print('  %-18s %d files  %s'%(dv,len(by[dv]),sorted(by[dv])[0][:18]))
print('device x file =',sum(len(v) for v in by.values()),'= 8 x 5 =',8*5)"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
st=[r for r in rows if r['db_type']=='STORAGE']
fc=[r for r in rows if r['db_type']=='FASTCHG' and '/ufs' in r['db_path']]
print('STORAGE rows/files/sizes:',len(st),len({r['filename'] for r in st}),sorted({int(r['size_bytes']) for r in st}))
print('FASTCHG/ufs rows/files/sizes:',len(fc),len({r['filename'] for r in fc}),sorted({int(r['size_bytes']) for r in fc}))
print('size intersection:',sorted(set(int(r['size_bytes']) for r in st)&set(int(r['size_bytes']) for r in fc)))
print('md5 intersection:',set(r['md5_db'] for r in st)&set(r['md5_db'] for r in fc) or 'EMPTY')
print('filename intersection:',set(r['filename'] for r in st)&set(r['filename'] for r in fc) or 'EMPTY')
print()
for r in rows:
    if 'MT128GBCAV2U31' in r['filename']:
        print('  %-34s %-10d %-9s %s'%(r['filename'],int(r['size_bytes']),r['db_type'],r['db_path']))"
```

```bash
python3 -I -c "
names=['KIOXIATHGJFJT1E45BATPC0100.img','KIOXIATHGJFJT2T85BAT0C0100.img','MICRONMT128GBCAV2U310103.img','MICRONMT128GBCAV2U310104.img','SAMSUNGKLUDG4UHGC-B0E13103.img']
for f in names:
    b=f[:-4]
    v=next(x for x in ('KIOXIA','MICRON','SAMSUNG') if b.startswith(x))
    print('%-34s vendor=%-8s rest=%-20r len=%d'%(f,v,b[len(v):],len(b[len(v):])))
a='MICRONMT128GBCAV2U310103'; c='MICRONMT128GBCAV2U310104'
print('micron differing indices:',[i for i in range(len(a)) if a[i]!=c[i]],'of len',len(a))
k1='KIOXIATHGJFJT1E45BATPC0100'; k2='KIOXIATHGJFJT2T85BAT0C0100'
print('kioxia suffix identical:',k1[-4:]==k2[-4:],repr(k1[-4:]))"
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
h=get('https://raw.githubusercontent.com/torvalds/linux/master/include/ufs/ufs_quirks.h')
print('ufs_quirks.h bytes',len(h.encode()))
for l in h.split(chr(10)):
    if 'UFS_VENDOR' in l and 'define' in l: print('  ',l.strip())
print('KIOXIA in header:', 'KIOXIA' in h.upper())
print()
for f in ('drivers/ufs/host/ufs-qcom.c','drivers/ufs/core/ufshcd.c'):
    t=get('https://raw.githubusercontent.com/torvalds/linux/master/'+f)
    print('%-20s %-7d request_firmware=%d filp_open=%d KIOXIA=%d .img=%d'%(
        f.split('/')[-1],len(t.encode()),t.count('request_firmware'),t.count('filp_open'),t.upper().count('KIOXIA'),t.count('.img')))
    time.sleep(2)"
```

```bash
python3 -I -c "
import urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x'}),timeout=90).read().decode()
        except Exception as e:
            if '404' in str(e): return None
            if i==n-1: raise
            time.sleep(8*(i+1))
t=get('https://raw.githubusercontent.com/LineageOS/android_device_google_caimito/lineage-22.2/caiman/proprietary-files-vendor.txt')
lines=t.split(chr(10))
print('caiman proprietary-files-vendor.txt lines:',len(lines))
print('first vendor/firmware line index:',next(i for i,l in enumerate(lines) if l.strip().startswith('vendor/firmware/')))
for i in range(308,315): print('  %4d: %s'%(i+1,lines[i]))
print('vendor/firmware lines total:',sum(1 for l in lines if 'vendor/firmware/' in l))"
```

```bash
python3 -I -c "
import urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x'}),timeout=90).read().decode()
        except Exception as e:
            if '404' in str(e): return None
            if i==n-1: raise
            time.sleep(8*(i+1))
t=get('https://raw.githubusercontent.com/Reeky-ux/lineage_kernel_google_kodiak/lineage-24.0/google-modules/soc/rdo/drivers/ufs/ufs-google.c')
print('ufs-google.c bytes',len(t.encode()))
for kw in ('request_firmware','.img','KIOXIA','MICRON','firmware'):
    print('  %-18s %d'%(kw,t.count(kw)))
print()
for tag,url in (('gs201','https://raw.githubusercontent.com/kdrag0n/freqbench/master/results/gs201/main/kernel.log'),
                ('zumapro','https://raw.githubusercontent.com/kdrag0n/freqbench/master/results/zumapro/main/kernel.log')):
    t2=get(url)
    print(tag,'kernel.log bytes',len(t2.encode()))
    for l in t2.split(chr(10)):
        if 'KIOXIA' in l and 'Direct-Access' in l: print('  ',l.strip()[:120])
    time.sleep(2)
print()
s=get('https://raw.githubusercontent.com/LineageOS/android_device_google_shusky/lineage-22.2/shiba/proprietary-files-vendor.txt')
sl=s.split(chr(10))
print('shiba list lines',len(sl),'vendor/firmware lines',sum(1 for l in sl if 'vendor/firmware/' in l))
for i in range(280,285): print('  %4d: %s'%(i+1,sl[i]))"
```

## Sources

| claim | source | access |
|---|---|---|
| 40 rows / 5 filenames / 8 devices / 39,558,496 B; sizes 1,048,764 ×2, 1,036,476 ×2, 774,332; md5s `d7fa9883…`, `735e19d5…`, `4dd22882…`, `f1fc6ef2…`, `e105c8bd…`; `blob_family=other` ×40; `blob_subfamily=misc` ×40; `priority=P3` ×40; `isa_identified` empty ×40; `soc` G3 ×25 / G4 ×5 / blank ×10 | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-27 |
| all 8 devices carry all 5 files (8 × 5 = 40); `db_path` all `google/<codename>/vendor/firmware` | same CSV | 2026-11-27 |
| `FASTCHG`/`ufs` half: 31 rows / 15 files / 6 devices, sizes {446,672 · 520,400 · 659,664 · 790,736 · 803,024 · 1,040,592 · 1,435,388}; zero size / md5 / filename overlap with `STORAGE`; `MICRON-MT128GBCAV2U31` is a strict prefix of `MT128GBCAV2U310103`/`104` | same CSV | 2026-11-27 |
| mainline UFS vendor IDs `MICRON 0x12C`, `SAMSUNG 0x1CE`, `SKHYNIX 0x1AD`, `TOSHIBA 0x198`, `WDC 0x145`; **no KIOXIA** | `include/ufs/ufs_quirks.h`, master (4,098 B) | 2026-11-27 |
| `ufs-qcom.c` 85,746 B and `ufshcd.c` 321,556 B: **0** `request_firmware`, **0** `filp_open`, **0** `KIOXIA`, **0** `.img` | `drivers/ufs/{host/ufs-qcom.c,core/ufshcd.c}`, master | 2026-11-27 |
| downstream `ufs-google.c` 95,623 B: **0** `request_firmware`, **0** `.img`, 1 `firmware` (PHY-patch timing), 1 `MICRON` (reset quirk) | `Reeky-ux/lineage_kernel_google_kodiak` `lineage-24.0` | 2026-11-27 |
| `KIOXIA` in `torvalds/linux` = 5 hits, none in `drivers/ufs/` (MTD/NAND, NVMe, sysfs ABI) | GitHub code search `repo:torvalds/linux KIOXIA` | 2026-11-27 |
| `request_firmware path:drivers/ufs` = **0**; `ufs_fw_update` = **0** | GitHub code search `repo:torvalds/linux` | 2026-11-27 |
| kernel prints `KIOXIA THGJFLT2E46BATPB 0100` and `KIOXIA THGJFGT1E45BAIPB 0100` as SCSI model + revision | `kdrag0n/freqbench` `results/{gs201,zumapro}/main/kernel.log` | 2026-11-27 |
| `caiman` `proprietary-files-vendor.txt` 2,979 lines, 2,532 `vendor/firmware/` lines; the 5 part numbers at lines 309–313, immediately before `aoc.bin` at 314 | `LineageOS/android_device_google_caimito` `lineage-22.2` | 2026-11-27 |
| `shiba` list is 1,878 lines with the same 5 at 281–285 | `LineageOS/android_device_google_shusky` `lineage-22.2` | 2026-11-27 |
| 140–141 GitHub hits per exact filename, all `proprietary-files-vendor.txt` | GitHub code search | 2026-11-27 |
| 15 `FASTCHG`/`ufs` filenames, 6 devices, all `*/odm/firmware/ufs`, read as per-device UFS/eMMC storage firmware | `research/fleet/other-fastchg.md` §3.3 | 2026-11-27 |
| Pixel 9 family is Tensor G4; `Pixel_9_Pro`/`Pixel_9_Pro_Fold` mislabelled G3, `Pixel_9A`/`Pixel_9_Pro_XL` blank | `research/fleet/other-esim.md` §7 and §6.1; `research/soc/Google-Tensor-GS201-gpu.md` §3.5 | 2026-11-27 |
| `batt_fw_adi_79_*` are `db_type=UNKNOWN` at `vendor/firmware` root | `research/fleet/other-fastchg.md` §3.4 | 2026-11-27 |
