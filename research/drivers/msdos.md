# Driver interface: `db_type=MSDOS` — 5 rows, 1 filename, a partition with no loader

Issue #889. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative / [OPEN] unresolved. Every number is from a command run on
**2026-11-26/27** against the committed matrix
(`upstream-contribution/blob-database/coverage-matrix.csv`, 33,917 data rows),
`torvalds/linux` master, Qualcomm's `qualcomm-linux/qcom-ptool`, and the
public LineageOS device trees for the five devices in this bucket.

**No payload exists in this workspace and none was read.** Every statement below
is matrix metadata — filename, size, `db_type`, `db_path`, md5 — public GPL
source, or a published partition table. No vendor image is parsed and no
filesystem is walked [N].

## Headline: `MSDOS` names a partition slot, not a driver

The bucket is **`core_nhlos.img`** — five rows, five devices, four distinct
sizes, and it is a **raw A/B partition image** written by
`fastboot flash core_nhlos`, never mounted, never read by
`request_firmware()` [F].

The decisive structural fact is the GPT type GUID. In a Qualcomm BSP partition
table for this SoC family, `core_nhlos_a` and `modem_a` sit side by side and
carry **different** type GUIDs [F]:

| partition | size | GPT type GUID | meaning |
|---|---:|---|---|
| `modem_a` | 404,480 KB | `EBD0A0A2-B9E5-4433-87C0-68B6B72699C7` | **Microsoft Basic Data** — a FAT volume |
| `core_nhlos_a` | 174,080 KB | `6690B4CE-70E9-4817-B9F1-25D64D888357` | vendor-specific, no filesystem type |

`EBD0A0A2-…` is `GPT_MS_BASIC_DATA` in every GPT header that names it [F], and
Qualcomm's own `qcom-ptool` assigns the same GUID to plain-data partitions such
as `fdemeta` while reserving `6690B4CE-…` for `core_nhlos_a` [F]. So `modem` is
declared as a filesystem partition and `core_nhlos` is not. That is the whole
difference, and it is why one gets mounted and the other does not.

**The label is not a loader class.** `MSDOS` is an upstream `bintypes` value —
one of 42 `db_type` values present in the matrix — and it labels **exactly one
filename in all 33,917 rows** [F]:

| `db_type` | rows | files | devices | bytes |
|---|---:|---:|---:|---:|
| `MSDOS` | **5** | **1** | **5** | **720,809,984** |

A `db_type` covering one filename cannot be a driver class. It is a
content-sniff verdict, and §4 shows the sniff is not even reliable.

## The 5 rows

| device | vendor | `db_path` | bytes | MiB | md5 | SoC |
|---|---|---|---:|---:|---|---|
| `FP4` | fairphone | `fairphone/FP4/radio` | 114,601,984 | 109.29 | `be4f32bc3df8702655e086a16703f32c` | SM7225 Snapdragon 750G |
| `Realme_9_Pro` | realme | `realme/oscar/radio` | 153,731,072 | 146.61 | `bcab9cc0b85265d38e95a7be26b96c61` | SM6375 Snapdragon 695 |
| `Nord_CE3` | oneplus | `oneplus/larry/radio` | 144,932,864 | 138.22 | `a89fdd654b21010e36f08c3b563fd627` | SM6375 Snapdragon 695 5G |
| `Nord_CE2` | oneplus | `oneplus/oscaro/radio` | 153,812,992 | 146.69 | `5035e4ee5c3aa07d63063b0c56d0d66c` | SM6375 Snapdragon 695 |
| `Realme_10_Pro` | realme | `realme/luigi/radio` | 153,731,072 | 146.61 | `bcab9cc0b85265d38e95a7be26b96c61` | SM6375 Snapdragon 695 |

Totals: **5 rows / 1 filename / 5 devices / 720,809,984 B (687.42 MiB)**,
`blob_family` `other` and `blob_subfamily` `misc` on all five,
`isa_identified` **empty on all five**, priority P2 ×1 (FP4) and P3 ×4 [F].

Two rows share an md5 — `bcab9cc0b85265d38e95a7be26b96c61` on `Realme_9_Pro` and
`Realme_10_Pro` at an identical 153,731,072 B. Same payload, two devices [F].

All four sizes are exact multiples of 4,096 and all are page-aligned to a
multiple of 1,024 bytes:

| bytes | ÷ 4096 | remainder |
|---|---:|---:|
| 114,601,984 | 27,979 | **0** |
| 144,932,864 | 35,384 | **0** |
| 153,731,072 | 37,532 | **0** |
| 153,812,992 | 37,552 | **0** |

No image is off by a single byte. That is a slot extent, not a code size [I] —
the same reading `research/fleet/other-misc.md` §2.1 already applies to this
filename.

## 1. All five devices ship the same container under a second label

This is the finding that makes the bucket a classifier artifact rather than a
subsystem. Every one of the five devices carries **both** `core_nhlos.img` and
`modem.img`, in the same `radio/` directory [F]:

| device | `core_nhlos.img` (`MSDOS`) | `modem.img` (`CELL_WIFI_GPS_BLUETOOTH`) |
|---|---:|---:|
| `FP4` | 114,601,984 | 153,235,456 |
| `Realme_9_Pro` | 153,731,072 | 187,011,072 |
| `Nord_CE3` | 144,932,864 | 178,311,168 |
| `Nord_CE2` | 153,812,992 | 187,092,992 |
| `Realme_10_Pro` | 153,731,072 | 187,011,072 |

Two partition images, two `db_type`s, one `radio/` directory. The labelling is
per row and per filename, and the two labels name different things about
neighbouring files. `modem.img` is never labelled `MSDOS` anywhere in the
corpus — 78 rows, all `CELL_WIFI_GPS_BLUETOOTH` [F] — even though it is the
partition that actually is a FAT volume (§2).

**These five rows are a 5-device slice of a 78-device class.** `modem.img` is
one filename on 78 devices, and **59 of those 78 also ship `modem.mdt`** — the
ELF that `request_firmware()` actually opens (`qcom_q6v5_mss.c:2115`,
`qcom_q6v5_pas.c` ×8 structs). So the contrast in this section is the narrow
case: here two `radio/` partition images sit side by side with two labels; across
the fleet the same `modem.img` filename carries 25.28% of the corpus's bytes on
0.23% of its rows. See `research/drivers/cell_wifi_gps_bluetooth.md`.

## 2. The mount chain: `modem` is mounted, `core_nhlos` is not

FP4's `init/fstab.default` has exactly one firmware-related vfat mount [F]:

```
/dev/block/bootdevice/by-name/modem   /vendor/firmware_mnt   vfat   ro,shortname=lower,...
/dev/block/bootdevice/by-name/bluetooth   /vendor/bt_firmware   vfat   ro,shortname=lower,...
```

There is **no** `core_nhlos` entry. `init/init.qcom.rc` then symlinks the mount
into the loader's search path [F]:

```
symlink /vendor/firmware_mnt /firmware
```

And the kernel is told to look there by the command line, because
`firmware_class.path` is the first entry of the firmware loader's search array:

```c
static const char * const fw_path[] = {
	fw_path_para,
	"/lib/firmware/updates/" UTS_RELEASE,
	"/lib/firmware/updates",
	"/lib/firmware/" UTS_RELEASE,
	"/lib/firmware"
};
```

`firmware_class.path=/vendor/firmware_mnt/image` appears in **2,800** GitHub
repositories [F]. That is the standard Qualcomm cmdline, and it points at the
`modem` partition — the one whose GUID says Microsoft Basic Data.

**`core_nhlos` is never mounted by anything.** A code search for
`"core_nhlos" path:fstab*` returns **0** hits [F]. The only references to
`by-name/core_nhlos` outside partition tables are `fixup-mountpoints` scripts in
`mer-hybris/hybris-boot` and its forks, which rewrite *device node names* for
halium boot — a name-mapping table, not a mount [F].

So the honest statement about this partition is not "it has no driver". It is
**nothing reads it as a filesystem at all**: it is written once by fastboot and
consumed by the modem firmware itself, if at all.

## 3. The A/B slot layout, and what the size means

Qualcomm's `qcom-ptool` defines the pair with a shared size and distinct GUIDs
[F]:

```
- {name: core_nhlos_a, size: "174080KB", type-guid: "6690B4CE-70E9-4817-B9F1-25D64D888357"}
- {name: core_nhlos_b, size: "174080KB", type-guid: "77036CD4-03D5-42BB-8ED1-37E5A88BAA34"}
```

174,080 KB = 178,257,920 B = **170.00 MiB**. Every corpus image fits inside it
with slack [F]:

| corpus size | MiB | slack in a 170.00 MiB slot |
|---|---:|---:|
| 114,601,984 | 109.29 | 63,655,936 B |
| 144,932,864 | 138.22 | 33,325,056 B |
| 153,731,072 | 146.61 | 24,526,848 B |
| 153,812,992 | 146.69 | 24,444,928 B |

The slot size is fixed and the image sizes vary below it, so **the file is not
the partition** — it is an image written into it. A different board uses a
different slot: `nord-spinor-ufs.yaml` declares `core_nhlos_a` at
**122,880 KB** (120.00 MiB), and **four of our five rows — three of the four distinct
sizes — are larger than it** [F]. So the
slot size is board-specific and cannot be used to infer anything about the
payload.

## 4. The label is unreliable, and `recon.md` has a defect to match

If `MSDOS` meant "this file is a FAT volume", it would be a useful label. It is
not, on two counts.

**First, the same label appears on a file that is not mounted as a filesystem,
while the file that *is* a FAT volume gets a different label** (§1, §2). The
sniff and the mount disagree.

**Second, `recon.md` §3 misdescribes the corpus's one stray byte.** It reads:

> one row (Phone_2/aura) even has a blank vendor; a stray `\ufffd` byte precedes
> one SOC value.

The actual character is **`U+00FF`** (ÿ), and it is not one row [F]:

| probe | value |
|---|---|
| `U+FFFD` (replacement char, `EF BF BD`) in the matrix | **0** occurrences |
| `U+00FF` (ÿ, `C3 BF`) in the matrix | **506** occurrences |
| rows whose `soc` cell contains `U+00FF` | **506** |
| distinct devices affected | **1** — `Nord_CE3` |
| distinct `soc` value | **1** — `ÿQualcomm SM6375 Snapdragon 695 5G` |
| position within the string | **index 0** on all 506 |

Raw bytes from the CSV line confirm the codepoint [F]:

```
b'Nord_CE3,oneplus,\xc3\xbfQualcomm SM6375 Snapdragon 695 5G,other,misc,core_nhlos.img,...'
```

`\xc3\xbf` is UTF-8 for `U+00FF`. `\ufffd` would be `\xef\xbf\xbd` and it does
not occur in the file. So the defect is real, but its description in `recon.md`
names the wrong codepoint and understates it by 506 rows. That is reported in
§7, not fixed — `recon.md` is a provenance record of the ingest and rewriting it
would destroy the evidence of what the ingest actually produced.

## 5. Mainline loads the modem by MDT, from `/lib/firmware`

The mainline modem loader is `qcom_q6v5_mss.c`, and it never touches this
partition [F]:

| file | bytes | `nhlos` | `firmware_mnt` | `request_firmware` |
|---|---:|---:|---:|---:|
| `drivers/remoteproc/qcom_q6v5_mss.c` | 71,201 | **0** | **0** | 5 |
| `drivers/firmware/qcom/qcom_scm.c` | 77,380 | **0** | **0** | 0 |

It loads via the MDT loader — `qcom_mdt_read_metadata()`,
`request_firmware(&fw, rproc->firmware, ...)`, and the `mba`/`msadp` pair — with
firmware resolved from `/lib/firmware` by name, not from a mounted partition
[F]. A tree-wide search for `nhlos`, `core_nhlos` and `firmware_mnt` in
`torvalds/linux` returns **0** hits for all three [N].

So the honest negative is not "mainline lacks a driver for `core_nhlos.img`".
It is **`core_nhlos` is not a firmware file that any kernel loads** — it is a
partition image whose contents, if the modem reads them at all, are read by the
modem's own firmware from a raw block device.

## 6. Filename → loader verdict

| filename | rows | verdict |
|---|---:|---|
| `core_nhlos.img` | 5 | **No kernel loader, no mount.** Raw A/B partition image (`core_nhlos_a`/`_b`, GUID `6690B4CE-…`), written by `fastboot flash core_nhlos`, never in any `fstab`, never on the `firmware_class.path` chain. Contents `[OPEN]`. |

The bucket has one filename and one verdict. The adjacent `modem.img` — the
same `radio/` directory, the same devices, a different label — *is* the mounted
FAT volume, and that is the contrast this note exists to record.

## 7. Rule 1 pass

| file | before | after |
|---|---|---|
| `research/fleet/other-misc.md` §2.1 | lists `core_nhlos.img` with its four sizes and reads them as partition extents — accurate, but never names the partition role, the GPT GUID, or the `MSDOS` label | adds the `core_nhlos_a`/`_b` slot identity, the 170.00 MiB hawi size, the fact that four of five rows exceed a different board's 120 MiB slot, the GUID contrast against `modem_a`, and a pointer to this note |
| `docs/REPO-STATE-MAP.md` driver row | 2 `db_type`-scoped notes under `research/drivers/` | 3, adding `msdos.md`; the 10 FP6 interface docs are unchanged |
| `research/CORRECTIONS.md` | 15 rows | 16 — one row for the `recon.md` §3 codepoint/multiplicity defect (§4) |

The `recon.md` defect gets a CORRECTIONS row rather than an edit because
`recon.md` records what the ingest produced; correcting the record in place
would erase the evidence.

## 8. Honest negatives

1. **No payload was read, and none exists here.** Whether `core_nhlos.img` is
   internally a FAT volume, a raw ELF chain, an ext4 image or something else is
   `[OPEN]`. I deliberately do **not** infer format from the `MSDOS` label,
   because §1 and §2 show that label disagrees with the mount table on
   neighbouring files.

2. **No source opens `core_nhlos.img`.** All 43 GitHub hits for the exact
   filename are LineageOS wiki templates, `proprietary-firmware.txt` lines, or
   TheMuppets `Android.mk` copy rules [F]. There is no consumer source to read.

3. **"NHLOS" is expanded only by third parties.** "Non-High-Level Operating
   System" is the standard expansion in Qualcomm platform write-ups, but I found
   no Qualcomm document stating it, and I do not cite it as `[F]`. The
   `core_` prefix and the `apnhlos` partition name are the only in-repo
   evidence, and neither expands the acronym.

4. **The 506-row `U+00FF` defect's origin is `[OPEN]`.** Whether it is a
   mangled `ÿ` from a vendor string, a genuine lead byte, or an encoding slip in
   the upstream ingest cannot be determined from the CSV alone. Only the
   codepoint and the count are `[F]`.

5. **Whether the modem reads this partition is `[I]` at best.** The partition
   exists, is written by fastboot, and has a vendor GPT type — so something
   expects it. But no public source shows a reader, and mainline certainly is
   not one. I do not claim it is dead space.

6. **`Nord_CE3`'s SoC string is corrupt** (§4), so device→SoC coverage for this
   bucket is 4 of 5 clean strings and 1 with a leading `U+00FF`. The chip
   identity is still unambiguous from the text that follows.

7. **The 78 `modem.img` rows are not in scope here.** They belong to issue #871
   (`CELL_WIFI_GPS_BLUETOOTH`). This note uses them only as the contrast that
   makes the `MSDOS` label meaningful.

8. **The GPT GUIDs are read from Qualcomm's partition tool, not from the
   devices.** `qcom-ptool` describes reference boards (hawi, nord, monaco,
   lemans, eliza, talos). The five devices here are SM6375/SM7225, and I did not
   verify their on-device GPT. The GUID *meaning* is `[F]`; that these exact
   boards use the same GUID is `[I]`.

## 9. Reproduce

Every command below was run on 2026-11-26/27 and exits 0.

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='MSDOS']
print('rows',len(d),'files',len({r['filename'] for r in d}),'devices',len({r['device'] for r in d}))
print('bytes',sum(int(r['size_bytes']) for r in d))
print('filenames',sorted({r['filename'] for r in d}))
print('families',dict(Counter(r['blob_family'] for r in d)))
print('subfamilies',dict(Counter(r['blob_subfamily'] for r in d)))
print('priorities',dict(Counter(r['priority'] for r in d)))
print('isa empty',sum(1 for r in d if not r['isa_identified'].strip()))
for r in d: print('  %-14s %-11d %-26s %s'%(r['device'],int(r['size_bytes']),r['db_path'],r['md5_db']))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
print('distinct db_type values:',len({r['db_type'] for r in rows}))
d=[r for r in rows if r['db_type']=='MSDOS']
print('MSDOS rows',len(d),'distinct filenames',len({r['filename'] for r in d}))
print('all sizes 4096-aligned:',all(int(r['size_bytes'])%4096==0 for r in d))
for s,c in sorted(Counter(int(r['size_bytes']) for r in d).items()):
    print('  %-11d x%d  /4096=%-6d rem=%d  MiB=%.3f'%(s,c,s//4096,s%4096,s/1048576))
m=Counter(r['md5_db'] for r in d)
print('shared md5s:',[(k,v) for k,v in m.items() if v>1])"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
devs=['FP4','Realme_9_Pro','Nord_CE3','Nord_CE2','Realme_10_Pro']
for dv in devs:
    c=[r for r in rows if r['device']==dv and r['filename']=='core_nhlos.img']
    m=[r for r in rows if r['device']==dv and r['filename']=='modem.img']
    print('%-14s core_nhlos=%-11s %-24s | modem=%-11s %s'%(
        dv,[int(x['size_bytes']) for x in c],[x['db_type'] for x in c],
        [int(x['size_bytes']) for x in m],[x['db_type'] for x in m]))"
```

```bash
python3 -I -c "
raw=open('upstream-contribution/blob-database/coverage-matrix.csv','rb').read()
print('EF BF BD (U+FFFD) count:',raw.count(b'\xef\xbf\xbd'))
print('C3 BF (U+00FF) count:',raw.count(b'\xc3\xbf'))
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
hits=[r for r in rows if any('\u00ff' in v for v in r.values())]
print('rows with U+00FF:',len(hits))
print('devices:',sorted({r['device'] for r in hits}))
print('distinct soc:',sorted({r['soc'] for r in hits if '\u00ff' in r['soc']}))
print('all at index 0:',all(r['soc'].find('\u00ff')==0 for r in hits if '\u00ff' in r['soc']))
print('codepoint: U+%04X'%ord(hits[0]['soc'][0]))"
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
srcs=[('qcom-ptool hawi-ufs','https://raw.githubusercontent.com/qualcomm-linux/qcom-ptool/main/platforms/flavors/hawi-ufs.yaml'),
      ('qcom-ptool nord-spinor-ufs','https://raw.githubusercontent.com/qualcomm-linux/qcom-ptool/main/platforms/flavors/nord-spinor-ufs.yaml'),
      ('meta-qti-bsp scuba-partition','https://raw.githubusercontent.com/aeroratech/meta-qti-bsp/master/conf/machine/partition/scuba-partition.conf')]
for name,u in srcs:
    t=get(u)
    print('== %s (%d B)'%(name,len(t.encode())))
    for l in t.split(chr(10)):
        s=l.strip()
        if 'core_nhlos' in s or '--name=modem_a' in s or 'NON-HLOS' in s: print('   ',s[:150])
    time.sleep(2)
print()
print('174080KB =',174080*1024,'B =',174080*1024/1048576,'MiB')
print('122880KB =',122880*1024,'B =',122880*1024/1048576,'MiB')"
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
t=get('https://raw.githubusercontent.com/LineageOS/android_device_fairphone_FP4/lineage-22.2/init/fstab.default')
print('fstab.default bytes',len(t.encode()))
for l in t.split(chr(10)):
    if 'firmware_mnt' in l or 'bt_firmware' in l or 'nhlos' in l.lower(): print('  ',l.strip()[:120])
print()
print('core_nhlos in fstab?','nhlos' in t.lower())
print()
t2=get('https://raw.githubusercontent.com/LineageOS/android_device_fairphone_FP4/lineage-22.2/init/init.qcom.rc')
print('init.qcom.rc bytes',len(t2.encode()))
for l in t2.split(chr(10)):
    if 'firmware_mnt' in l: print('  ',l.strip()[:120])"
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
for f in ('drivers/remoteproc/qcom_q6v5_mss.c','drivers/firmware/qcom/qcom_scm.c'):
    t=get('https://raw.githubusercontent.com/torvalds/linux/master/'+f)
    print('%-46s %-7d nhlos=%d firmware_mnt=%d request_firmware=%d'%(
        f.split('/')[-1],len(t.encode()),t.lower().count('nhlos'),t.count('firmware_mnt'),t.count('request_firmware')))
    time.sleep(2)"
```

## Sources

| claim | source | access |
|---|---|---|
| 5 rows / 1 filename / 5 devices / 720,809,984 B; `core_nhlos.img`; sizes 114,601,984 / 144,932,864 / 153,731,072 ×2 / 153,812,992; md5s `be4f32bc…` / `bcab9cc0…` ×2 / `a89fdd65…` / `5035e4ee…`; `blob_family=other` ×5; `blob_subfamily=misc` ×5; priority P2 ×1 P3 ×4; `isa_identified` empty ×5 | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-26 |
| 42 distinct `db_type` values present; `MSDOS` covers 1 filename corpus-wide; all four sizes 4096-aligned with remainder 0 | same CSV | 2026-11-26 |
| all five devices carry both `core_nhlos.img` (`MSDOS`) and `modem.img` (`CELL_WIFI_GPS_BLUETOOTH`) in `radio/`; `modem.img` never labelled `MSDOS` (78 rows, all `CELL_WIFI_GPS_BLUETOOTH`) | same CSV | 2026-11-26 |
| `U+FFFD` occurs 0 times in the matrix; `U+00FF` occurs 506 times; all 506 in `soc` at index 0, all `Nord_CE3`, all the string `ÿQualcomm SM6375 Snapdragon 695 5G`; raw bytes `\xc3\xbf` | same CSV, raw byte read | 2026-11-26 |
| `core_nhlos_a` GUID `6690B4CE-70E9-4817-B9F1-25D64D888357` at 174,080 KB (hawi) and 122,880 KB (nord-spinor); `core_nhlos_b` GUID `77036CD4-03D5-42BB-8ED1-37E5A88BAA34` (hawi) vs `E8867782-68AB-46F5-9FA2-68FDFDBB1E13` (nord-spinor) — `_a` GUID is stable, `_b` is not | `qualcomm-linux/qcom-ptool` `platforms/flavors/{hawi-ufs,nord-spinor-ufs}.yaml` | 2026-11-27 |
| `modem_a` 404,480 KB GUID `EBD0A0A2-B9E5-4433-87C0-68B6B72699C7` beside `core_nhlos_a` in one table; `core_nhlos_a` filename `Core_NON-HLOS.bin`, `modem_a` filename `NON-HLOS.bin` | `aeroratech/meta-qti-bsp` `conf/machine/partition/scuba-partition.conf` | 2026-11-27 |
| `qcom-ptool` assigns `EBD0A0A2-…` to `fdemeta` and `6690B4CE-…` to `core_nhlos_a` — same GUID split as the BSP table | `qualcomm-linux/qcom-ptool` `platforms/flavors/sdm845-ufs.yaml`, `hawi-ufs.yaml` | 2026-11-27 |
| `EBD0A0A2-B9E5-4433-87C0-68B6B72699C7` = `GPT_MS_BASIC_DATA` (Microsoft Basic Data) | `HelenOS/helenos` `uspace/lib/label/include/std/gpt.h`; 2,712 GitHub hits labelled "Basic data" | 2026-11-27 |
| FP4 `init/fstab.default`: `by-name/modem` → `/vendor/firmware_mnt` vfat; `by-name/bluetooth` → `/vendor/bt_firmware` vfat; **no** `core_nhlos` entry | `LineageOS/android_device_fairphone_FP4` `lineage-22.2` | 2026-11-27 |
| FP4 `init/init.qcom.rc`: `symlink /vendor/firmware_mnt /firmware` | same tree | 2026-11-27 |
| FP4 `proprietary-firmware.txt` maps `Core_NON-HLOS.bin:core_nhlos.img;AB` and `NON-HLOS.bin:modem.img;AB` as separate A/B partitions (20 lines) | same tree | 2026-11-27 |
| kernel `fw_path[]` = `fw_path_para`, `/lib/firmware/updates/$UTS_RELEASE`, `/lib/firmware/updates`, `/lib/firmware/$UTS_RELEASE`, `/lib/firmware` | `drivers/base/firmware_loader/main.c`, master | 2026-11-26 |
| `firmware_class.path=/vendor/firmware_mnt/image` in 2,800 repos | GitHub code search | 2026-11-27 |
| `qcom_q6v5_mss.c` 71,201 B — 0 `nhlos`, 0 `firmware_mnt`, 5 `request_firmware`; `qcom_scm.c` 77,380 B — 0/0/0 | `torvalds/linux` master | 2026-11-27 |
| `nhlos`, `core_nhlos`, `firmware_mnt` all 0 hits in `torvalds/linux` | GitHub code search `repo:torvalds/linux` | 2026-11-27 |
| `"core_nhlos" path:fstab*` → 0 hits; `"core_nhlos.img"` → 43 hits all wiki/txt/mk | GitHub code search | 2026-11-27 |
| `core_nhlos` is fastboot-flashed beside `modem`, `abl`, `xbl`, `tz`, `hyp`, `dsp` on SM6375/SM4350 | `LineageOS/lineage_wiki` `_includes/templates/device_specific/firmware_update_{realme_sm6375,oneplus_sm6375,oplus_sm4350,oneplus_sm4350}.md` | 2026-11-27 |
| `by-name/core_nhlos_a` → `sda16`/`sde22`/`sde51` etc. in halium `fixup-mountpoints` — name mapping, not a mount | `mer-hybris/hybris-boot` `fixup-mountpoints` | 2026-11-27 |
| `research/fleet/other-misc.md` §2.1 already lists `core_nhlos.img` sizes as partition extents | in-repo | 2026-11-26 |
| `recon.md` §3 says "a stray `\ufffd` byte precedes one SOC value" | in-repo | 2026-11-26 |
