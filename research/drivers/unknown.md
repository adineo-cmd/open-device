# Driver interface: `db_type=UNKNOWN` — 12,756 rows, and the label means "the sniff failed"

Issue #901. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative / [OPEN] unresolved. Every number is from a command run on
**2026-11-28** against the committed matrix
(`upstream-contribution/blob-database/coverage-matrix.csv`, 33,917 data rows),
`torvalds/linux` master, and the upstream taxonomy source.

**No payload exists in this workspace and none was read.** Every statement below
is matrix metadata — filename, size, `db_type`, `db_path`, md5 — public GPL
source, or the upstream enum's own bytes. No file's first bytes are inspected
here [N].

## Headline: `UNKNOWN` is the corpus's largest label, and it is a fallback

The bucket is **12,756 rows / 2,275 filenames / 114 devices / 14,942,303,906 B**
[F]. That is:

| | value | rank |
|---|---:|---:|
| rows | 12,756 | **#1 of 42** `db_type` values |
| share of corpus rows | **37.61%** | — |
| bytes | 14,942,303,906 | #3 |
| share of corpus bytes | 21.41% | — |
| devices | 114 | — |
| distinct md5s | 4,586 | — |

**More than a third of every row in the corpus carries this label.** It is not a
subsystem, and the name does not describe a format — it records that the
classifier's test did not match (§1).

The bucket spans **eight** `blob_family` values [F]:

| `blob_family` | rows | bytes | share of bucket |
|---|---:|---:|---:|
| `other` | 10,587 | 11,962,956,572 | 80.06% |
| `tz` | 1,105 | 77,512,259 | 0.52% |
| `bt` | 347 | 21,557,656 | 0.14% |
| `gpu` | 305 | 60,919,593 | 0.41% |
| `modem` | 265 | **2,792,904,394** | **18.69%** |
| `boot` | 74 | 24,240,128 | 0.16% |
| `cdsp` | 60 | 27,480 | 0.00% |
| `wifi` | 13 | 2,185,824 | 0.01% |

The row and byte columns rank the families differently, which is the bucket's
defining shape: `modem` is **2.1% of the rows but 18.7% of the bytes** (it is
almost entirely `modem.bin`, §4), while `cdsp` is 60 rows of 27,480 B total —
458 B per row. A `db_type` that holds both a 2.8 GB modem image and a 403-byte
servreg manifest has no common content, only a common failure to match a magic
number.

and eleven named `blob_subfamily` values plus a blank one, of which `misc` is
8,623 rows (67.6%) [F].

## 1. The mechanism: two paths to `UNKNOWN`, and the second one is a `return`

`librephone/device_files.py` assigns `UNKNOWN` two different ways, and the
distinction is the whole finding [F].

**Path A — eleven explicit filename mappings** (lines 189–211):

```python
"gcf.img": Bintypes.UNKNOWN,
"pbl.img": Bintypes.UNKNOWN,
"ldfw.img": Bintypes.UNKNOWN,
"studybk.img": Bintypes.UNKNOWN,
"uefisecapp.img": Bintypes.UNKNOWN,
"cpucp.img": Bintypes.UNKNOWN,
"featenabler.img": Bintypes.UNKNOWN,
"devcfg.img": Bintypes.UNKNOWN,
"aop.img": Bintypes.UNKNOWN,
"aoc.img": Bintypes.UNKNOWN,
"multiimgoem.img": Bintypes.UNKNOWN,
```

**Path B — the fallthrough at line 430**, after the magic table fails:

```python
        except Exception:
            pass
        return Bintypes.UNKNOWN
```

The magic table (§1 of `elf64.md`) has 35 entries covering PNG, AVB, `\x7FELF`,
MSDOS, `ANDR`, DTB, QTI, 10 `FIRMWARE*` variants, `WMD R`, `LIMI`, `FwUp`,
`TFIS`, Mach-O and others. **Anything whose first 4–8 bytes match none of them
lands here.**

Measured over the bucket [F]:

| path | filenames | rows | share of rows | bytes | share of bytes |
|---|---:|---:|---:|---:|---:|
| A — explicit mapping | 10 present (`aoc.img` absent) | **285** | **2.2%** | 123,629,568 | 0.83% |
| B — magic-sniff fallback | 2,265 | **12,471** | **97.8%** | 14,818,674,338 | **99.17%** |

**97.8% of the bucket's rows are there because a 4-byte test failed**, not
because anyone decided the file was unknown. The eleven explicit names are
0.83% of the bytes.

This is the finding no existing note has. `other-tinysys.md` §8.4 correctly
observes that `db_type` has 42 values and none names a container — "a corpus-wide
vocabulary gap". That is the *consequence*. The *cause* is that `UNKNOWN` is the
function's default return, so the bucket is defined by exclusion and its
boundary is whatever the 35 magic entries do not cover.

## 2. Two-thirds of the rows are one subfamily, and that is already documented

8,623 of the 12,756 rows (67.6%) are `blob_family=other` +
`blob_subfamily=misc` [F] — the scope of `research/fleet/other-misc.md`, which
analyses 10,720 rows of that subfamily across all `db_type`s. So the largest
part of this bucket is prior art, and I do not re-derive it.

**What that note cannot supply is the other 4,133 rows (32.4%)**, which sit
outside its scope [F]:

| `blob_family` | `blob_subfamily` | rows |
|---|---|---:|
| `other` | `camera` | 1,493 |
| `tz` | *(blank)* | 1,105 |
| `bt` | *(blank)* | 347 |
| `other` | `media` | 339 |
| `gpu` | *(blank)* | 305 |
| `modem` | *(blank)* | 260 |
| `other` | `touch` | 98 |
| `boot` | *(blank)* | 74 |
| `cdsp` | *(blank)* | 60 |
| `other` | `audio` | 15 |
| `other` | `fastchg` | 10 |
| `wifi` | `wpss` | 9 |
| `modem` | `modem-config` | 5 |
| `other` | `sensors` | 5 |
| `other` | `tinysys` | 4 |
| `wifi` | `wifi-bt-combo` | 4 |
| **total** | | **4,133** |

A `UNKNOWN` label on a TrustZone row, a Bluetooth row and a camera row means the
same thing in each case — no magic matched — and nothing more. The subfamily is
the only thing that says what the file is.

## 3. The bucket is dominated by segments, not by files

7,566 of the 12,756 rows (**59.3%**) are `.bNN` PIL segments — the payload
tiles of split firmware containers — across 1,144 distinct filenames and 815
`(device, db_path, stem)` groups, averaging **9.28 segments per group** [F].

| class | rows | share of rows | bytes | share of bytes | files |
|---|---:|---:|---:|---:|---:|
| `.bXX` segments | 7,566 | 59.3% | 900,910,455 | 6.03% | 1,144 |
| everything else | 5,190 | 40.7% | 14,041,393,451 | **93.97%** | 1,131 |

The inversion matters: **59% of the rows are 6% of the bytes.** A row-count
ranking puts this bucket first, but a reader who weights by rows is weighting
segment tiles at ~6 KB each against 3.3 GB partition images.

The suffix naming is also not uniform. Of the 191 distinct `.bXX` suffixes [F]:

| suffix form | distinct | rows |
|---|---:|---:|
| decimal `b00`–`b99` | 85 | 6,155 |
| hex / 3–4 digit (`b0a`, `b5a`, `b111`, `b0204`) | 106 | 1,411 |

So 1,411 rows use hexadecimal or extended segment numbering that a
`b00`–`b99` pattern would not match. `docs/devices/xiaomi/Mi_12/other.md`
already records this shape for the `hpnv21` family ("spanning b5a..bc2 with the
gaps ba5 and bb4, plus 3-digit continuations b10c/b111"); I confirm it is
bucket-wide, at 106 suffixes.

## 4. The three files that carry 45% of the bytes

Concentration is extreme [F] — the top 5 filenames are 50.19% of the bytes and
the top 200 of 2,275 names are 92.50%:

| filename | rows | devices | bytes | share of bucket |
|---|---:|---:|---:|---:|
| `dsp.img` | 61 | 61 | 3,321,888,768 | **22.23%** |
| `modem.bin` | 29 | 20 | 2,106,261,880 | **14.10%** |
| `vm-bootsys.img` | 5 | 5 | 1,349,980,160 | **9.03%** |
| `fsg.img` | 21 | 21 | 418,992,128 | 2.80% |
| `night_align_lsc_tbl_40963072.bin` | 6 | 6 | 301,989,888 | 2.02% |

Each resolves differently, and only the first is prior art.

**`dsp.img` is documented.** 61 rows / 61 devices at exactly **67,108,864 B ×38**
and **33,554,432 B ×23** — 64 MiB and 32 MiB, a partition extent, not an image
size. `other-misc.md` §2.1 calls it "the clearest case in the whole corpus" and
`research/fleet/dsp-tz-map.md` records it as ext4. I cite both and add nothing.

**`modem.bin` is not.** 29 rows / 20 devices / 2,106,261,880 B at 18 distinct
sizes from 43,332,816 to 105,373,576 B, 20 distinct md5s [F]. It sits at
`*/modem/images/<build-id>/` on the Pixel 6/8/9 families and on eight Samsung
Galaxy S10/Note10/F62/Tab S6 devices. The build-id directories are real and
structured — `g5300o-250320-250425-B-13407682`, `g5123b-145971-250328-B-13284995`,
`g5400c-250320-250508-B-13464352` — i.e. `<chip>-<6 digit>-<6 digit>-<letter>-<8 digit>`,
11 rows carrying one [F]. That is a vendor build identifier, and it is the only
provenance the corpus holds for the file.

**`vm-bootsys.img` is the bucket's shared-content case.** 5 rows on
`Mi_12S`, `Mi_12S_Pro`, `Mi_12S_Ultra`, `Mi_12T_Pro`, `Poco_F5_Pro` at
`xiaomi/<codename>/radio`, every one **269,996,032 B with the same md5** [F].
One file, five devices, 1.35 GB of the bucket's bytes. A virtual-machine boot
image shared across a Xiaomi family is `[I]` from the name and path; I did not
read it.

## 5. No `UNKNOWN` filename appears in mainline — and that is the honest verdict

Seven code searches over `torvalds/linux` [F]:

| query | result |
|---|---|
| `"dsp.img"` | **0** |
| `"vm-bootsys.img"` | **0** |
| `"fsg.img"` | **0** |
| `"devcfg.img"` | **0** |
| `"uefisecapp.img"` | **0** |
| `"modem.bin"` | **0** |
| `"sequence_manifest.bin"` | **0** |

Positive controls in the same session returned the expected hits
(`"ipa_fws.mdt"` → 1, `drivers/net/ipa/ipa_main.c`), so the zeros are real
absences and not a broken query [F].

**So there is no filename→loader verdict table for this bucket, and inventing
one would be the error.** What can be said is narrower and still useful: the
bucket contains no file whose *name* is a `request_firmware()` target. Some of
its contents certainly reach drivers — `dsp.img` is the ext4 container the DSP
trustlets are read from (`dsp-tz-map.md`), and the `.bNN` segments belong to
`.mdt` containers that `mdt_loader.c` parses — but in every such case the loader
opens a *different* filename and this bucket holds the carrier.

That is the same structural finding as `cell_wifi_gps_bluetooth.md` and
`storage.md`: **the bucket names a container, and the driver targets something
inside it.** Here the label is weaker still, because it names nothing at all.

## 6. Metadata files: 1,098 rows of manifests and version stamps

82 filenames / 1,098 rows / 110,728,981 B (0.74%) are not firmware payloads [F]:

| ext | rows | files | bytes |
|---|---:|---:|---:|
| `.jsn` | 226 | 8 | 129,036 |
| `.tlv` | 284 | 28 | 31,261,104 |
| `.xml` | 49 | 2 | 598,876 |
| `.txt` | 303 | 21 | 1,440,496 |
| `.ver` | 77 | 18 | 2,893 |
| `.dig` | 76 | 2 | 2,432 |
| `.msc` | 83 | 3 | 77,294,144 |

These are the servreg manifests (`modemr.jsn` ×61, `cdspr.jsn` ×60,
`battmgr.jsn` ×30), digest files (`mbn_hw.dig` / `mbn_sw.dig`, each **32 B** on
38 rows — the size of a SHA-256), and the version strings (`*.ver`, 2,893 B
across 77 rows, ~38 B each) [F]. `Data.msc` (54 rows, 46,909,531 B) and
`gptauuid.xml` (45 rows, 315,114 B) are already analysed in `other-misc.md`
§4.5 and §4.3 respectively; I cite rather than re-derive.

**48 rows are zero bytes**, and all 48 carry the MD5 of the empty string
(`d41d8cd98f00b204e9800998ecf8427e`) [F] — `oem_hw.txt` ×16, `oem_hw_null.txt`
×12, `oem_sw_null.txt` ×12, plus 8 `dgain_mask_*` / `eye_retouch_chinese.bin`
rows. That is 84.2% of the corpus's 57 zero-byte rows (the other 9 are `CELL`).
A zero-byte row is not a missing row: it is a file that shipped empty.

## 7. Filename → loader verdict

There is no verdict table, because the bucket is not a class. What the corpus
supports [F]:

| observation | rows | meaning |
|---|---:|---|
| `.bXX` segment tiles | 7,566 | payload of a split container; the `.mdt` that owns them is filed under another `db_type` |
| partition-sized `.img` | 544 | 52 names; `dsp.img` is ext4 (`dsp-tz-map.md`), `devcfg.img`/`aop.img`/`cpucp.img` are the 11 explicit-`UNKNOWN` names, others `[OPEN]` |
| `.bin` blobs | 3,360 | 956 names; camera tuning tables, modem builds, vendor blobs — no shared grammar |
| metadata | 1,098 | manifests, digests, version stamps (§6) |
| zero-byte | 48 | shipped empty (§6) |

**The single honest statement: 97.8% of this bucket is defined by what the
classifier failed to recognise, so any driver verdict must be made per filename
and not per `db_type`.** That is the opposite of `ELF64` (where one mechanism
explains the whole label) and the opposite of `CELL_WIFI_GPS_BLUETOOTH` (where
one filename is the whole bucket).

## 8. Rule 1 pass

| file | before | after |
|---|---|---|
| `docs/REPO-STATE-MAP.md` driver row | 6 `db_type`-scoped notes | 7, adding `unknown.md` |
| `research/CORRECTIONS.md` | 16 data rows | **no row added** — nothing in this note contradicts a prior claim; `other-tinysys.md` §8.4's figures all verify (§9) |

I did **not** edit `research/fleet/other-tinysys.md`. It is another agent's
in-flight file (verified unchanged at md5 `d1a8b9df…` across my session), and
its §8.4 claim is correct as written — 12,756 rows, 544 `.img`, 42 `db_type`
values all reproduce exactly. My note adds the mechanism and the bucket-wide
scope; it corrects nothing.

## 9. Honest negatives

1. **I did not read any file in this bucket.** No magic bytes, no header, no
   partition table. Every claim about *what a file is* is `[I]` from its name,
   path, size and family, or `[F]` from a cited note that did read it.

2. **`modem.bin` is unidentified beyond its path.** 2.1 GB, 14.10% of the
   bucket, and all the corpus establishes is that it sits under
   `*/modem/images/<build-id>/`. Whether it is an Exynos modem image, a
   Qualcomm one, or something else is `[OPEN]`. I do not claim a vendor.

3. **`vm-bootsys.img`'s content is `[OPEN]`.** Five devices, one md5, 270 MB
   each. "Virtual-machine boot image" is `[I]` from the filename.

4. **The `[F]`/`[I]` boundary on the 4,133 out-of-scope rows is thin.** I know
   their family, subfamily, rows and bytes. I do not know their formats.

5. **`other-misc.md`'s 10,720-row scope and this bucket's 8,623-row overlap are
   not the same set.** The note counts all `db_type`s in its subfamily; this
   bucket is one `db_type` in that subfamily. I did not attempt to reconcile the
   row-by-row intersection, because the note's own scope is `blob_subfamily`,
   not `db_type`, and a naive subtraction would be wrong.

6. **The 35-entry magic table is quoted from upstream, not audited.** I read
   `MAGIC_NUMBERS` to establish what `UNKNOWN` excludes. I did not verify that
   each of the 35 entries is reachable, or that a file matching two entries
   resolves the same way here as upstream.

7. **The build-id grammar is `[I]`.** `<chip>-<6 digit>-<6 digit>-<letter>-<8 digit>`
   is a pattern I observed on 11 paths, not a documented format.

## 10. Reproduce

Every command below was run on 2026-11-28 and exits 0.

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='UNKNOWN']
tot=sum(int(r['size_bytes']) for r in d); allb=sum(int(r['size_bytes']) for r in rows)
print('rows',len(d),'files',len({r['filename'] for r in d}),'devices',len({r['device'] for r in d}))
print('bytes',tot)
print('row share %.2f%%  byte share %.2f%%'%(100*len(d)/len(rows),100*tot/allb))
print('distinct sizes',len({int(r['size_bytes']) for r in d}),'md5s',len({r['md5_db'] for r in d}))
print('families',dict(Counter(r['blob_family'] for r in d)))
print('subfamilies',dict(Counter(r['blob_subfamily'] for r in d)))
print('priorities',dict(Counter(r['priority'] for r in d)))
print('isa empty',sum(1 for r in d if not r['isa_identified'].strip()))
print('interface_documented',dict(Counter(r['interface_documented'] for r in d)))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
rc=Counter(r['db_type'] for r in rows); bc=Counter()
for r in rows: bc[r['db_type']]+=int(r['size_bytes'])
print('rank by rows:')
for i,(t,c) in enumerate(rc.most_common(5),1): print('  #%d %-28s rows=%-6d bytes=%d'%(i,t,c,bc[t]))
print()
d=[r for r in rows if r['db_type']=='UNKNOWN']
explicit={'gcf.img','pbl.img','ldfw.img','studybk.img','uefisecapp.img','cpucp.img','featenabler.img','devcfg.img','aop.img','aoc.img','multiimgoem.img'}
ex=[r for r in d if r['filename'] in explicit]; fb=[r for r in d if r['filename'] not in explicit]
tot=sum(int(r['size_bytes']) for r in d)
print('explicit-map rows %d (%.1f%%) bytes %d (%.2f%%)'%(len(ex),100*len(ex)/len(d),sum(int(r['size_bytes']) for r in ex),100*sum(int(r['size_bytes']) for r in ex)/tot))
print('fallback rows %d (%.1f%%) bytes %d (%.2f%%)'%(len(fb),100*len(fb)/len(d),sum(int(r['size_bytes']) for r in fb),100*sum(int(r['size_bytes']) for r in fb)/tot))"
```

```bash
python3 -I -c "
import csv,re
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='UNKNOWN']
tot=sum(int(r['size_bytes']) for r in d)
seg=[r for r in d if re.search(r'\.[bB][0-9a-fA-F]+$',r['filename'])]
rest=[r for r in d if r not in seg]
print('segments rows %d (%.1f%%) bytes %d (%.2f%%) files %d'%(len(seg),100*len(seg)/len(d),sum(int(r['size_bytes']) for r in seg),100*sum(int(r['size_bytes']) for r in seg)/tot,len({r['filename'] for r in seg})))
print('rest     rows %d (%.1f%%) bytes %d (%.2f%%) files %d'%(len(rest),100*len(rest)/len(d),sum(int(r['size_bytes']) for r in rest),100*sum(int(r['size_bytes']) for r in rest)/tot,len({r['filename'] for r in rest})))
suf=Counter(re.search(r'\.([bB][0-9a-fA-F]+)$',r['filename']).group(1).lower() for r in seg)
dec=[s for s in suf if re.fullmatch(r'b\d\d',s)]; oth=[s for s in suf if s not in dec]
print('distinct suffixes',len(suf),'decimal',len(dec),'rows',sum(suf[s] for s in dec))
print('                    hex/extended',len(oth),'rows',sum(suf[s] for s in oth))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='UNKNOWN']
tot=sum(int(r['size_bytes']) for r in d)
agg=Counter()
for r in d: agg[r['filename']]+=int(r['size_bytes'])
run=0
for i,(f,b) in enumerate(agg.most_common(),1):
    run+=b
    if i in (1,2,3,5,10,20,50,100,200,500): print('top %-4d names -> %6.2f%% of bytes'%(i,100*run/tot))
print('distinct names',len(agg))
print()
for f in ('dsp.img','modem.bin','vm-bootsys.img','fsg.img'):
    g=[r for r in d if r['filename']==f]
    print('%-16s rows=%-3d dev=%-3d bytes=%-11d sizes=%-3d md5s=%d'%(f,len(g),len({r['device'] for r in g}),sum(int(r['size_bytes']) for r in g),len({int(r['size_bytes']) for r in g}),len({r['md5_db'] for r in g})))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='UNKNOWN']
om=[r for r in d if r['blob_family']=='other' and r['blob_subfamily']=='misc']
print('UNKNOWN & (other,misc): %d of %d = %.1f%%'%(len(om),len(d),100*len(om)/len(d)))
out=[r for r in d if not (r['blob_family']=='other' and r['blob_subfamily']=='misc')]
print('outside that scope: %d = %.1f%%'%(len(out),100*len(out)/len(d)))
for (f,s),c in Counter((r['blob_family'],r['blob_subfamily']) for r in out).most_common():
    print('   %-8s %-12s %d'%(f,s or '(blank)',c))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='UNKNOWN']
EMPTY='d41d8cd98f00b204e9800998ecf8427e'
z=[r for r in d if int(r['size_bytes'])==0]
print('zero-byte rows in bucket',len(z),'all empty-string md5',all(r['md5_db']==EMPTY for r in z))
print('filenames',dict(Counter(r['filename'] for r in z)))
print('devices',len({r['device'] for r in z}))
cz=[r for r in rows if int(r['size_bytes'])==0]
print('corpus zero-byte',len(cz),'by db_type',dict(Counter(r['db_type'] for r in cz)))
print()
for e in ('.jsn','.tlv','.xml','.txt','.ver','.dig','.msc'):
    g=[r for r in d if r['filename'].lower().endswith(e)]
    print('%-5s rows=%-4d files=%-3d %d'%(e,len(g),len({r['filename'] for r in g}),sum(int(r['size_bytes']) for r in g)))"
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
lines=t.split(chr(10))
n=sum(1 for l in lines if 'Bintypes.UNKNOWN' in l and '\"' in l and not l.strip().startswith('#'))
print('  explicit UNKNOWN mappings',n)
for i,l in enumerate(lines,1):
    if 'return Bintypes.UNKNOWN' in l: print('  fallthrough at line',i)
print('  MAGIC_NUMBERS entries',sum(1 for l in lines if l.strip().startswith('(\"') and 'bytes([' in l))"
```

```bash
python3 -I -c "
import urllib.request,json,time,urllib.parse
tok=open('/tmp/.ghtok').read().strip()
def q(query,n=5):
    u='https://api.github.com/search/code?q='+urllib.parse.quote(query)
    for i in range(n):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x','Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}),timeout=60)
            return json.loads(r.read().decode())
        except Exception as e:
            if '404' in str(e): return None
            time.sleep(10*(i+1))
    return None
for name in ('dsp.img','vm-bootsys.img','fsg.img','devcfg.img','uefisecapp.img','modem.bin','sequence_manifest.bin','ipa_fws.mdt'):
    d=q('repo:torvalds/linux \"%s\"'%name)
    print('%-22s -> %s'%(name,d.get('total_count') if d else '?'))
    time.sleep(4)"
```

## Sources

| claim | source | access |
|---|---|---|
| 12,756 rows / 2,275 filenames / 114 devices / 14,942,303,906 B; 37.61% of corpus rows, 21.41% of bytes; #1 of 42 `db_type` by rows, #3 by bytes; 2,125 sizes; 4,586 md5s; `isa_identified` empty on 12,741 | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-28 |
| `blob_family`: `other` 10,587 / `tz` 1,105 / `bt` 347 / `gpu` 305 / `modem` 265 / `boot` 74 / `cdsp` 60 / `wifi` 13; `blob_subfamily` `misc` 8,623 | same CSV | 2026-11-28 |
| 8,623 of 12,756 rows (67.6%) are `other`+`misc`; 4,133 rows (32.4%) outside, led by `other/camera` 1,493 and `tz` 1,105 | same CSV | 2026-11-28 |
| `.bXX` segments: 7,566 rows (59.3%) / 6.03% of bytes / 1,144 files / 815 groups / 9.28 avg; 191 suffixes, 85 decimal (6,155 rows) vs 106 hex-or-extended (1,411 rows) | same CSV | 2026-11-28 |
| top 5 filenames = 50.19% of bytes, top 200 of 2,275 = 92.50%; `dsp.img` 3,321,888,768 (22.23%), `modem.bin` 2,106,261,880 (14.10%), `vm-bootsys.img` 1,349,980,160 (9.03%) | same CSV | 2026-11-28 |
| `dsp.img` 61 rows / 61 devices at 67,108,864 ×38 and 33,554,432 ×23 = 64 MiB / 32 MiB | same CSV; `research/fleet/other-misc.md` §2.1; `research/fleet/dsp-tz-map.md` | 2026-11-28 |
| `modem.bin` 29 rows / 20 devices, 18 sizes 43,332,816–105,373,576, 20 md5s, at `*/modem/images/<build-id>/`, 11 rows with a `g####-######-######-B-########` directory | same CSV | 2026-11-28 |
| `vm-bootsys.img` 5 rows / 5 devices, all 269,996,032 B, 1 md5, `xiaomi/<codename>/radio` | same CSV | 2026-11-28 |
| 48 zero-byte rows, all `d41d8cd98f00b204e9800998ecf8427e`; `oem_hw.txt` ×16, `oem_hw_null.txt` ×12, `oem_sw_null.txt` ×12; 48 of the corpus's 57 zero-byte rows (84.2%) | same CSV | 2026-11-28 |
| metadata: `.jsn` 226/8, `.tlv` 284/28, `.xml` 49/2, `.txt` 303/21, `.ver` 77/18, `.dig` 76/2, `.msc` 83/3; `mbn_hw.dig`/`mbn_sw.dig` 32 B ×38 each | same CSV | 2026-11-28 |
| 11 explicit `Bintypes.UNKNOWN` filename mappings at lines 189–211; `return Bintypes.UNKNOWN` fallthrough at line 430; 35 `MAGIC_NUMBERS` entries | `fabiorafaelcoutada/librephone` `librephone/device_files.py` (21,371 B) | 2026-11-28 |
| explicit-map filenames account for 285 rows (2.2%) / 123,629,568 B (0.83%); fallback 12,471 rows (97.8%) / 14,818,674,338 B (99.17%) | matrix + the 11-name list above | 2026-11-28 |
| `repo:torvalds/linux` returns **0** for `dsp.img`, `vm-bootsys.img`, `fsg.img`, `devcfg.img`, `uefisecapp.img`, `modem.bin`, `sequence_manifest.bin`; **1** for `ipa_fws.mdt` (positive control) | GitHub code search | 2026-11-28 |
| `db_type` has 42 values and none names a container; `UNKNOWN` covers 12,756 rows, 544 of them `.img`, out of 2,914 total `.img` rows | `research/fleet/other-tinysys.md` §8.4 | 2026-11-28 |
| `dsp.img` is ext4; the size law 61 rows / 61 devices / 64 MiB or 32 MiB | `research/fleet/dsp-tz-map.md`; `research/fleet/other-misc.md` §2.1 | 2026-11-28 |
| `Data.msc` and `gptauuid.xml` analysed | `research/fleet/other-misc.md` §4.5, §4.3 | 2026-11-28 |
| `hpnv21` family uses hex segment suffixes `b5a..bc2` with 3-digit continuations `b10c`/`b111` | `docs/devices/xiaomi/Mi_12/other.md` | 2026-11-28 |
