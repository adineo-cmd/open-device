# Driver interface: `db_type=CELL_WIFI_GPS_BLUETOOTH` — 78 rows, one filename, and no kernel loader for it

Issue #871. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative / [OPEN] unresolved. Every number is from a command run on
**2026-11-27** against the committed matrix
(`upstream-contribution/blob-database/coverage-matrix.csv`, 33,917 data rows),
`torvalds/linux` master, and public source for the devices in this bucket.

**No payload exists in this workspace and none was read.** Every statement below
is matrix metadata — filename, size, `db_type`, `db_path`, md5 — public GPL
source, or a published bring-up note. No vendor image is parsed and no
filesystem is walked here [N].

## Headline: the bucket is one filename, and the kernel never opens it

`CELL_WIFI_GPS_BLUETOOTH` is **`modem.img` on 78 devices** — one filename, one
row per device, every one at `<vendor>/<codename>/radio` [F]:

| `db_type` | rows | filenames | devices | bytes |
|---|---:|---:|---:|---:|
| `CELL_WIFI_GPS_BLUETOOTH` | **78** | **1** | **78** | **17,641,529,344** |

That is **0.23% of the corpus's rows but 25.28% of its bytes** — the second
largest `db_type` by bytes after `BOOT` (30.46%), ahead of `UNKNOWN` (21.41%)
[F]. A single filename carries a quarter of the corpus.

**No kernel driver loads `modem.img`.** A code search for
`repo:torvalds/linux "modem.img"` returns **0** [F]. What mainline loads is
`modem.mdt`, and **59 of these 78 devices ship both** [F]. So `modem.img` is the
carrier *partition*; the thing remoteproc requests is an ELF inside it. The
`db_type` names the container, not a driver.

## The 78 rows

| device | codename path | bytes | md5 |
|---|---|---:|---|
| `Edge_30` | `motorola/dubai/radio` | 414,187,520 | `138f957f…` |
| `Edge_30_Fusion` | `motorola/tundra/radio` | 414,187,520 | `858e72a4…` |
| `Edge_30_Neo` | `motorola/miami/radio` | 414,187,520 | `15344c30…` |
| `Edge_40_Pro` | `motorola/rtwo/radio` | 414,187,520 | `1f03b538…` |
| `G_Stylus_5G-2-2022` | `motorola/milanf/radio` | 414,187,520 | `d87e50e1…` |
| `Moto_G200` | `motorola/xpeng/radio` | 414,187,520 | `98aaf14a…` |
| `Moto_G34_5G` | `motorola/fogos/radio` | 414,187,520 | `e6503ea9…` |
| `Moto_G82_5G` | `motorola/rhodep/radio` | 414,187,520 | `3c6819f5…` |
| `Moto_G84_5G` | `motorola/bangkk/radio` | 414,187,520 | `ce847934…` |
| `Moto_G_5G_2024` | `motorola/fogo/radio` | 414,187,520 | `49e22d65…` |
| `Moto_G_Stylus_5G` | `motorola/denver/radio` | 414,187,520 | `c11692f2…` |

The eleven 414,187,520-byte rows above are all Motorola and all have **distinct
md5s** — same extent, different payload (§4). The remaining 67 rows are
enumerated by the Reproduce block rather than pasted here.

Bucket totals [F]: `blob_family` `modem` on **78/78**, `blob_subfamily` empty on
**78/78**, `isa_identified` **empty on 78/78**, `interface_documented` `n` on
**77** and `y (qualcomm-fp6/docs/interface-cellular.md)` on exactly **1**
(`FP6`), `priority` P1 ×1 (`FP6`), P2 ×7, P3 ×70.

Eight vendors, 78 rows [F]:

| vendor | rows | bytes | share of bucket |
|---|---:|---:|---:|
| motorola | 21 | 6,443,499,520 | 36.52% |
| xiaomi | 13 | 3,951,284,224 | 22.40% |
| oneplus | 18 | 3,556,564,992 | 20.16% |
| google | 18 | 2,288,578,560 | 12.97% |
| fairphone | 3 | 528,994,304 | 3.00% |
| nothing | 2 | 387,792,896 | 2.20% |
| realme | 2 | 374,022,144 | 2.12% |
| fxtec | 1 | 110,792,704 | 0.63% |

46 distinct sizes, 67 distinct md5s across 78 rows; 7 md5s repeat (§5) [F].

## 1. The label is a taxonomy string from an external enum, applied filename-first

`CELL_WIFI_GPS_BLUETOOTH` is not a format verdict this repo invented. It is a
literal in `fabiorafaelcoutada/librephone`:

```python
# librephone/typedefs.py
CELL_WIFI_GPS_BLUETOOTH = "CELL_WIFI_GPS_BLUETOOTH"

# librephone/device_files.py
"modem.img": Bintypes.CELL_WIFI_GPS_BLUETOOTH,
```

The mapping is **filename → bintype**, and `upstream-contribution/blob-database/recon.md`
§204 records that this repo's family assignment is "filename-first with upstream
bintype fallback" [F].

So `db_type` here answers *"what is this file called"*, not *"what loads it"*.
The name itself names three radio functions plus a filename: cellular, Wi-Fi,
GPS/BT — a **contents claim about one partition**, made from its name. That is
why a single filename owns the label, and why the label says nothing about a
kernel entry point.

**Consequence:** a query filtered on `db_type` for a driver gets a container
name back. The honest key for "what loads this" is the file *inside* the
container, which is `modem.mdt` (§2).

## 2. Mainline loads `modem.mdt`, never `modem.img` — and 59 of 78 devices ship both

Two mainline files name the modem firmware, and both name the MDT [F]:

```c
/* drivers/remoteproc/qcom_q6v5_mss.c:2115 */
qproc->hexagon_mdt_image = "modem.mdt";

/* drivers/remoteproc/qcom_q6v5_pas.c — .firmware_name */
static const struct qcom_pas_data sm8550_mpss_resource = {
	.crash_reason_smem = 421,
	.firmware_name = "modem.mdt",
	.dtb_firmware_name = "modem_dtb.mdt",
	...
```

`qcom_q6v5_mss.c` is 71,201 B with **5** `request_firmware` call sites, none of
which names `modem.img` [F]. `qcom_q6v5_pas.c` is 52,404 B with **50**
`qcom_pas_data` structs, of which **8** set `.firmware_name = "modem.mdt"` —
`sm6375`, `mpss_init`, `sc8180x`, `sdx55`, `sm8450`, `sm8550`, `sm8650`,
`sm8750` — and **3** also set `.dtb_firmware_name = "modem_dtb.mdt"` (`sm8550`,
`sm8650`, `sm8750`) [F].

The corpus agrees with the driver rather than with the bucket label [F]:

| filename | `db_type` | devices | path |
|---|---|---:|---|
| `modem.mdt` | **`ELF64`** | **59** | `*/modem/image` |
| `modem.img` | `CELL_WIFI_GPS_BLUETOOTH` | **78** | `*/radio` |

Set arithmetic over the 78 [F]:

| relation | count |
|---|---:|
| devices with `modem.img` | 78 |
| devices with `modem.mdt` | 59 |
| **both** | **59** |
| `modem.img` only | 19 |
| `modem.mdt` only | 0 |

Every device that has an MDT also has the image; **not one has an MDT without
one**. The 19 image-only devices are `OnePlus_8`, `OnePlus_8_Pro`, `Pad_2_Pro`,
`Pad_Pro`, and the whole Pixel 6/7/8/9 family plus `Pixel_Fold` [F].

So on 59 of 78 devices the kernel's target and this bucket's filename sit in the
same tree: the bucket holds the partition image, and the kernel reads the ELF
that is *inside* it. `modem.img` is what you flash; `modem.mdt` is what
`request_firmware()` opens.

## 3. The containment proof: `modem.img` is large enough to hold its own segments, 63/63

If `modem.img` is the carrier partition, then for any device whose extracted
contents are also in the matrix, the image must be **at least** as large as the
sum of those contents. That is testable without a payload, and it does not fail
[F]:

| | |
|---|---:|
| devices with both `radio/modem.img` and `*/modem/image` rows | **63** |
| devices where `size(modem.img) ≥ Σ size(segments)` | **63** |
| violations | **0** |
| ratio range | 1.067 – 3.508 |

The tightest margins are the tablet and Nothing devices — `Pad_Pro` 1.067,
`Pad_2_Pro` 1.086, `Phone_1` 1.143, `FP6` 1.170, `FP5` 1.176 — and the loosest
are the Motorola `Moto_G84_5G` at 3.508 and `G_Stylus_5G-2-2022` at 3.476,
whose images are 414 MB against ~119 MB of extracted segments [F].

The ratio spread is itself informative: it is not a constant, so `modem.img` is
not "the segments concatenated". It is a **filesystem** holding them, and the
slack is free space plus files the census did not extract.

This also explains the 19 image-only devices without an intermediate step: for
them the ingest kept the container and recorded no contents. That is a census
gap, not a container difference (§8.3).

## 4. The size distribution is a partition-extent signature, not an image size

All 78 sizes are exact multiples of 4,096 — **0 exceptions** — but only **21**
are exact multiples of 1 MiB [F]. A compiled artifact would not respect a
4 KiB boundary 78 times out of 78; a partition extent does.

Two clusters make the mechanism explicit. Each is a single size with **every
payload different** [F]:

| bytes | = KB | = MiB | devices | distinct md5s |
|---|---:|---:|---:|---:|
| 414,187,520 | 404,480 | 395 | **11** | **11** |
| 188,743,680 | 184,320 | 180 | **10** | **10** |

Same slot, twenty-one different contents. The size is the **extent the vendor
reserved**; the md5 is what was written into it.

And the larger cluster pins to a real partition table. `414,187,520 ÷ 1024 =
**404,480 KB**`, which is exactly the `modem_a` size in a Qualcomm BSP partition
table — recorded in `research/drivers/msdos.md` (Headline table) beside
`core_nhlos_a` at 174,080 KB, where `modem_a` also carries GPT type GUID
`EBD0A0A2-B9E5-4433-87C0-68B6B72699C7` = **Microsoft Basic Data**, i.e. a FAT
volume [F].

So the 395 MiB cluster is eleven devices whose `modem` partition happens to be
404,480 KB. The image is a dump of that partition, and its size is the
partition's size — not the firmware's.

## 5. The `soc` column: 27 blanks, 23 spellings, one mojibake

`soc` is blank on **27 of 78** rows and carries 23 distinct non-blank values
across the other 51 [F]. The blanks are not a vendor pattern: `Pad_Pro`,
`Pad_2_Pro`, `Pixel_9A`, `Pixel_9_Pro_XL`, `FP6`, `OnePlus_13`, `Nord_4` and
others are all blank while sibling devices are populated.

One row carries a corrupted label — `Nord_CE3`, `soc` =
`ÿQualcomm SM6375 Snapdragon 695 5G` [F]. That is the `U+00FF` defect already
recorded in `research/CORRECTIONS.md` (row dated 2026-11-26): the character is
**`U+00FF`** (ÿ, UTF-8 `\xc3\xbf`), not `U+FFFD`, and it prefixes `soc` on
**506 rows**, all `Nord_CE3`. I cite that row rather than re-deriving it, and I
add no CORRECTIONS entry.

What is *new* here is a within-bucket vocabulary split that the existing
correction does not state: the same part appears twice, spelled two ways [F]:

| `soc` in this bucket | rows |
|---|---:|
| `Qualcomm SM6375 Snapdragon 695` | 7 |
| `ÿQualcomm SM6375 Snapdragon 695 5G` | 1 |

Eight rows on one part number, two spellings, and the `5G` suffix present on
only one of them. A `soc`-keyed join over this bucket splits an 8-row device
family into 7 and 1. That is a data-shape note, not a correction — the `ÿ` row
is already documented and the `5G` variant is the upstream DB's own string.

## 6. Filename → loader verdict

| filename | rows | verdict |
|---|---:|---|
| `modem.img` | 78 | **No kernel loader.** It is the `modem` partition image at `*/radio`. Mainline requests `modem.mdt` (`qcom_q6v5_mss.c:2115`, `qcom_q6v5_pas.c` ×8 structs), which lives at `*/modem/image` on 59 of the 78 devices. The image's interior is FAT16 on the 4 devices where it has been walked (§8.2), and its size tracks the partition extent, not a payload (§4). Format `[OPEN]` for the other 74. |

The bucket is one row per device and every row resolves the same way: a
container, not a driver target.

## 7. Rule 1 pass

| file | before | after |
|---|---|---|
| `research/drivers/msdos.md` §1 | already states that all five of its devices ship both `core_nhlos.img` and `modem.img`, and that `modem.img` is the FAT volume | adds the reverse pointer: this bucket is that filename on 78 devices, 59 of which also carry `modem.mdt`, so the contrast in `msdos.md` §1 is a 5-row slice of a 78-row class |
| `docs/REPO-STATE-MAP.md` driver row | 4 `db_type`-scoped notes under `research/drivers/` | 5, adding `cell_wifi_gps_bluetooth.md` |

`research/CORRECTIONS.md` gains **no** row. The `U+00FF` defect is already
correctly recorded (§5), and nothing else in this note contradicts a prior
claim — the FAT16 interior is cited, not re-derived, and the containment result
is new rather than corrective.

## 8. Honest negatives

1. **I did not walk any filesystem.** The FAT16 reading of `modem.img` is
   established elsewhere in this repo — `three-device-sharing.md` §5 (OnePlus 6,
   119,820,288 B, `MSDOS5.0`, 404 files / 113,443,924 B) and
   `qdsp6sw-container.md` (OnePlus 8, 192,278,528 B, 654 files) — and published
   externally for OnePlus 8T (`modem_a` FAT16 on `/dev/sde4`, mounted at
   `/mnt/modemfw`). That is **4 devices** out of 78. I do **not** claim FAT16 for
   the other 74; the general statement is `[I]` from those four, not `[F]`.

2. **The 19 image-only devices are a census gap, not a container difference.**
   `OnePlus_8` and `OnePlus_8_Pro` each carry 370 `/modem/image` rows and 32
   `.mdt` files — but **no file named `modem.mdt`**; the modem image inside is
   named per-component. `Pad_Pro` (339 rows, 23 `.mdt`) and `Pad_2_Pro` (361
   rows, 25 `.mdt`) are the same. So "no `modem.mdt`" does not mean "no modem
   firmware"; it means the vendor's naming differs. The Pixel family has no
   `/modem/image` rows at all [F].

3. **Which process flashes `modem.img` is not established.** `tqftpserv`
   serving `image/modem_pr` is documented for one device (OnePlus 8T) and I
   class the mechanism `[I]` beyond it. I do not claim fastboot, nor a specific
   userspace daemon, for the fleet.

4. **The 63/63 containment result is a lower bound, not a size law.** The
   ratios range 1.067–3.508 and I do not claim a formula. It proves the image is
   big enough to be a container; it does not prove it is one on the 15 devices
   with no `/modem/image` rows (63 + 15 = 78).

5. **`interface_documented` is `y` on exactly one row.** `FP6` carries the flag
   with `qualcomm-fp6/docs/interface-cellular.md`. The other 77 are `n` [F]. So
   the corpus itself records that this filename's interface is undocumented for
   77 of 78 devices.

6. **No payload, and no offset.** The 414,187,520-byte cluster matching
   `modem_a`'s 404,480 KB is `[F]`; that every one of the eleven images *is* that
   partition's dump is `[I]` from the size match alone. I did not read a
   partition table on those devices.

7. **The `ÿ` row is prior art.** §5 cites `research/CORRECTIONS.md`; I did not
   re-verify the 506-row count beyond confirming it in the matrix.

8. **The `5G` spelling split is reported, not resolved.** I do not know whether
   `Qualcomm SM6375 Snapdragon 695` and `... 695 5G` are the same part in the
   upstream DB's vocabulary or two entries; I only report that this bucket
   contains both, on 7 + 1 rows.

## 9. Reproduce

Every command below was run on 2026-11-27 and exits 0.

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='CELL_WIFI_GPS_BLUETOOTH']
print('rows',len(d),'files',len({r['filename'] for r in d}),'devices',len({r['device'] for r in d}))
print('bytes',sum(int(r['size_bytes']) for r in d))
print('families',dict(Counter(r['blob_family'] for r in d)))
print('subfamilies',dict(Counter(r['blob_subfamily'] for r in d)))
print('priorities',dict(Counter(r['priority'] for r in d)))
print('interface_documented',dict(Counter(r['interface_documented'] for r in d)))
print('isa empty',sum(1 for r in d if not r['isa_identified'].strip()))
print('sizes',len({int(r['size_bytes']) for r in d}),'md5s',len({r['md5_db'] for r in d}))
print('all end /radio',all(r['db_path'].endswith('/radio') for r in d))
print('rows==devices',len(d)==len({r['device'] for r in d}))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='CELL_WIFI_GPS_BLUETOOTH']
tot=len(rows); totb=sum(int(r['size_bytes']) for r in rows)
b=sum(int(r['size_bytes']) for r in d)
print('rows share %.2f%%'%(100*len(d)/tot))
print('bytes share %.2f%%'%(100*b/totb))
agg=Counter()
for r in rows: agg[r['db_type']]+=int(r['size_bytes'])
print('top db_types by bytes:')
for k,v in agg.most_common(5): print('  %-30s %15d %5.2f%%'%(k,v,100*v/totb))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='CELL_WIFI_GPS_BLUETOOTH']
print('vendor rows and bytes:')
for v in sorted({r['vendor'] for r in d}):
    g=[r for r in d if r['vendor']==v]
    print('  %-12s %-3d %14d'%(v,len(g),sum(int(r['size_bytes']) for r in g)))
print()
print('alignment:')
print('  all 4096-aligned',all(int(r['size_bytes'])%4096==0 for r in d))
print('  exact MiB multiples',sum(1 for r in d if int(r['size_bytes'])%1048576==0))
print()
for s in (414187520,188743680):
    g=[r for r in d if int(r['size_bytes'])==s]
    print('%d B = %d KB = %d MiB -> %d devices, %d distinct md5'%(s,s//1024,s//1048576,len(g),len({r['md5_db'] for r in g})))"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='CELL_WIFI_GPS_BLUETOOTH']
img={r['device'] for r in d}
mdt={r['device'] for r in rows if r['filename']=='modem.mdt'}
pil={r['device'] for r in rows if r['db_path'].endswith('/modem/image')}
print('modem.img devices',len(img))
print('modem.mdt devices',len(mdt),'db_types',{r['db_type'] for r in rows if r['filename']=='modem.mdt'})
print('/modem/image devices',len(pil))
print('both img+mdt',len(img&mdt))
print('img only',len(img-mdt))
print('mdt only',len(mdt-img))
print('pil without modem.mdt',sorted(pil-mdt))"
```

```bash
python3 -I -c "
import csv
from collections import defaultdict
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='CELL_WIFI_GPS_BLUETOOTH']
img={r['device']:int(r['size_bytes']) for r in d}
pil=defaultdict(int)
for r in rows:
    if r['db_path'].endswith('/modem/image'): pil[r['device']]+=int(r['size_bytes'])
common=sorted(set(img)&set(pil))
ok=[dv for dv in common if img[dv]>=pil[dv]]
print('devices with both:',len(common))
print('containment holds:',len(ok))
print('violations:',len(common)-len(ok))
rs=sorted((img[dv]/pil[dv],dv) for dv in common if pil[dv])
print('ratio min %.3f (%s)  max %.3f (%s)'%(rs[0][0],rs[0][1],rs[-1][0],rs[-1][1]))"
```

```bash
python3 -I -c "
import urllib.request,time,re
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x'}),timeout=90).read().decode()
        except Exception as e:
            if '404' in str(e): return None
            if i==n-1: raise
            time.sleep(8*(i+1))
t=get('https://raw.githubusercontent.com/torvalds/linux/master/drivers/remoteproc/qcom_q6v5_mss.c')
print('qcom_q6v5_mss.c bytes',len(t.encode()))
print('  request_firmware',t.count('request_firmware'))
print('  modem.img',t.count('modem.img'),'  modem.mdt',t.count('modem.mdt'))
for l in t.split(chr(10)):
    if 'hexagon_mdt_image =' in l: print('  ',l.strip())
time.sleep(2)
p=get('https://raw.githubusercontent.com/torvalds/linux/master/drivers/remoteproc/qcom_q6v5_pas.c')
print('qcom_q6v5_pas.c bytes',len(p.encode()))
structs=re.findall(r'static const struct qcom_pas_data (\w+)\s*=\s*\{(.*?)\n\};',p,re.S)
print('  qcom_pas_data structs',len(structs))
print('  naming modem.mdt',len([1 for n,b in structs if chr(34)+'modem.mdt'+chr(34) in b]))
print('  naming modem_dtb.mdt',len([1 for n,b in structs if 'modem_dtb.mdt' in b]))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='CELL_WIFI_GPS_BLUETOOTH']
print('distinct soc incl blank',len({r['soc'] for r in d}))
print('blank',sum(1 for r in d if not r['soc'].strip()))
for s,n in sorted(Counter(r['soc'] for r in d).items()):
    if 'SM6375' in s: print('  %-46r %d'%(s,n))
print('rows with U+00FF in soc (whole matrix)',sum(1 for r in rows if chr(0x00ff) in r['soc']))
print('all such rows are Nord_CE3',all(r['device']=='Nord_CE3' for r in rows if chr(0x00ff) in r['soc']))"
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
t=get('https://raw.githubusercontent.com/fabiorafaelcoutada/librephone/main/librephone/device_files.py')
print('device_files.py bytes',len(t.encode()))
for l in t.split(chr(10)):
    if 'modem.img' in l: print('  ',l.strip())
time.sleep(2)
u=get('https://raw.githubusercontent.com/fabiorafaelcoutada/librephone/main/librephone/typedefs.py')
print('typedefs.py bytes',len(u.encode()))
for l in u.split(chr(10)):
    if 'CELL_WIFI' in l: print('  ',l.strip())"
```

## Sources

| claim | source | access |
|---|---|---|
| 78 rows / 1 filename / 78 devices / 17,641,529,344 B; `blob_family=modem` ×78; `blob_subfamily` empty ×78; `isa_identified` empty ×78; `interface_documented` n ×77, y ×1 (`FP6`); `priority` P1 ×1, P2 ×7, P3 ×70; all `db_path` end `/radio`; 46 sizes; 67 md5s | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-27 |
| 0.23% of rows, 25.28% of bytes; #2 `db_type` by bytes after `BOOT` 30.46%, ahead of `UNKNOWN` 21.41% | same CSV, 33,917 rows / 69,797,539,502 B | 2026-11-27 |
| vendor split motorola 21 / oneplus 18 / google 18 / xiaomi 13 / fairphone 3 / nothing 2 / realme 2 / fxtec 1 | same CSV | 2026-11-27 |
| all 78 sizes 4096-aligned, 0 exceptions; 21 exact MiB multiples; 414,187,520 B ×11 devices with 11 distinct md5s; 188,743,680 B ×10 devices with 10 distinct md5s | same CSV | 2026-11-27 |
| `modem.mdt` is `db_type=ELF64` on 59 devices at `*/modem/image`; `img∩mdt` = 59, `img−mdt` = 19, `mdt−img` = 0 | same CSV | 2026-11-27 |
| 63 devices have both `radio/modem.img` and `*/modem/image`; containment holds 63/63; ratio 1.067–3.508 | same CSV | 2026-11-27 |
| `soc` blank ×27, 24 distinct incl blank, 23 non-blank; `Qualcomm SM6375 Snapdragon 695` ×7 vs `ÿQualcomm SM6375 Snapdragon 695 5G` ×1 | same CSV | 2026-11-27 |
| `U+00FF` prefixes `soc` on 506 rows, all `Nord_CE3`, UTF-8 `\xc3\xbf`, not `U+FFFD` | `research/CORRECTIONS.md` (row dated 2026-11-26) | 2026-11-27 |
| `qcom_q6v5_mss.c` 71,201 B, 5 `request_firmware`, 0 `modem.img`, `hexagon_mdt_image = "modem.mdt"` at line 2115 | `drivers/remoteproc/qcom_q6v5_mss.c`, master | 2026-11-27 |
| `qcom_q6v5_pas.c` 52,404 B, 50 `qcom_pas_data` structs, 8 set `.firmware_name = "modem.mdt"` (sm6375, mpss_init, sc8180x, sdx55, sm8450, sm8550, sm8650, sm8750), 3 also set `modem_dtb.mdt` | `drivers/remoteproc/qcom_q6v5_pas.c`, master | 2026-11-27 |
| `repo:torvalds/linux "modem.img"` = **0**; `"modem.mdt"` = 3 files; `"modem_dtb.mdt"` = 1 | GitHub code search | 2026-11-27 |
| `CELL_WIFI_GPS_BLUETOOTH` literal in `librephone/typedefs.py`; `"modem.img": Bintypes.CELL_WIFI_GPS_BLUETOOTH` in `librephone/device_files.py` | `fabiorafaelcoutada/librephone` `main` | 2026-11-27 |
| family mapping is filename-first with upstream bintype fallback | `upstream-contribution/blob-database/recon.md` §204 | 2026-11-27 |
| `modem_a` = 404,480 KB, GPT GUID `EBD0A0A2-B9E5-4433-87C0-68B6B72699C7` = Microsoft Basic Data (FAT volume); `core_nhlos_a` 174,080 KB beside it | `research/drivers/msdos.md`, Headline table | 2026-11-27 |
| `modem.img` FAT16: OnePlus 6 119,820,288 B (`MSDOS5.0`, 404 files / 113,443,924 B); OnePlus 8 192,278,528 B (654 files) | `research/fleet/three-device-sharing.md` §5; `research/fleet/qdsp6sw-container.md` | 2026-11-27 |
| OnePlus 8T: firmware partition `modem_a` FAT16 `/dev/sde4`, mounted `/mnt/modemfw`, `tqftpserv` serves `image/modem_pr` → `/readonly/firmware/image/...` | `jfbobier/Oneplus-8T-kebab-pmos-bringup`, file `docs/research/MODEM.md` (61,986 B), external repo — not a path in this workspace | 2026-11-27 |
| `fastrpc_shell_0` lives inside an on-disk `modem.img` | `research/fleet/other-gpu-compute.md` §2.3 | 2026-11-27 |
