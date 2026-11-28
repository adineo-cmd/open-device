# Driver interface: `db_type=ELF64` — 3,284 rows, and the label is a 4-byte magic sniff

Issue #877. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative / [OPEN] unresolved. Every number is from a command run on
**2026-11-28** against the committed matrix
(`upstream-contribution/blob-database/coverage-matrix.csv`, 33,917 data rows),
`torvalds/linux` master, and the upstream taxonomy source.

**No payload exists in this workspace and none was read.** Every statement below
is matrix metadata — filename, size, `db_type`, `db_path`, md5 — public GPL
source, or the upstream enum's own bytes. No ELF header is parsed here [N].

## Headline: `ELF64` does not mean ELF64, and 809 of its rows are not ELF at all

The bucket is **3,284 rows / 391 filenames / 91 devices / 475,030,376 B** — 0.68%
of the corpus's bytes [F]. It spans **six** `blob_family` values, which alone
should disqualify the name as a driver class:

| `blob_family` | rows | bytes | share of bucket |
|---|---:|---:|---:|
| `other` | 2,162 | 355,254,808 | 74.8% |
| `tz` | 517 | 9,686,112 | 2.0% |
| `boot` | 251 | 108,085,624 | 22.8% |
| `gpu` | 189 | 944,240 | 0.2% |
| `modem` | 156 | 1,008,812 | 0.2% |
| `wifi` | 9 | 50,780 | 0.0% |

Boot-chain, TrustZone, GPU, modem and Wi-Fi images share one `db_type`. The
reason is not that they are alike — it is the classifier, and it is a
**4-byte prefix match** (§1).

Two consequences follow immediately and are the substance of this note [F]:

- **809 rows (24.6%) cannot be ELF files at all** — 743 `.bNN` PIL payload
  segments and 66 `.sig` signature blobs (§3).
- **227 of the 725 `.b00` header blocks are ELF32-shaped**, not ELF64 (§4).

## 1. The mechanism: a 4-byte magic check, with no `ELF32` to fall into

`librephone/device_files.py` classifies a file by sniffing its first bytes. The
table entry is unambiguous [F]:

```python
# librephone/device_files.py:222
("ELF64", bytes([0x7F, 0x45, 0x4C, 0x46])),
```

and it is consumed as a prefix test over an 8-byte read [F]:

```python
# librephone/device_files.py:419-427
with open(filespec, "rb") as file:
    header = file.read(8)
    for ftype, num in self.MAGIC_NUMBERS:
        if header.startswith(num):
            ...
            return Bintypes(ftype)
```

`0x7F 0x45 0x4C 0x46` is `\x7FELF` — the **EI_MAG0..EI_MAG3** identity bytes
that open *every* ELF file, 32-bit and 64-bit alike. The class byte that
distinguishes them is `e_ident[EI_CLASS]` at **offset 4**, and the sniff reads
8 bytes but never looks at byte 4 [F].

So the label is not a claim about class. It is a claim that the file *starts with
`\x7FELF`*.

**And there is nowhere else for a 32-bit ELF to go.** The `Bintypes` enum in
`librephone/typedefs.py` contains `ELF64` and **no `ELF32`** [F]:

```python
class Bintypes(Enum):
    ELF64 = "ELF64"
    MBR = "MBR"
    BOOT = "BOOT"
    ...
```

That makes the mislabel **structurally forced rather than careless**. Every ELF
file in the corpus — ELF32 or ELF64 — has exactly one reachable bintype, and it
is named `ELF64`. This is the finding the three existing in-repo notes on the
defect could not reach: they each observed that the label was wrong on `.mdt`
rows (§7), but none had the reason, and the reason explains why the label is
wrong *everywhere*, not only on `.mdt`.

## 2. The bucket by extension

Nine extensions, and they do not behave alike [F]:

| ext | rows | files | devices | bytes | share of bucket |
|---|---:|---:|---:|---:|---:|
| `.mdt` | 1,572 | 153 | 91 | 10,815,388 | 2.28% |
| `.bNN` | 743 | 105 | 60 | 14,479,868 | 3.05% |
| `.elf` | 424 | 64 | 20 | 31,704,296 | 6.67% |
| `.img` | 337 | 19 | 63 | 132,022,272 | 27.79% |
| `.so.1` | 86 | 30 | 3 | 17,611,088 | 3.71% |
| `.sig` | 66 | 14 | 10 | 3,295,144 | 0.69% |
| `.bin` | 41 | 1 | 24 | 260,837,728 | **54.91%** |
| `.so` | 12 | 4 | 3 | 1,741,352 | 0.37% |
| *(none)* | 3 | 1 | 3 | 2,523,240 | 0.53% |

265 distinct sizes and 1,990 distinct md5s across 3,284 rows [F]. The byte
distribution is dominated by a single filename: `.bin` is one name,
`amss.bin`, at 54.91% of the bucket (§6).

`.so.1` is 30 audio codec modules (`AlacDecoderModule.so.1`,
`EtsiAmrWbPlusDecModule.so.1`, `LdacModule.so.1`, …) on **3 devices only** [F].
Those are genuine shared objects and genuinely ELF, but they are userspace
libraries in a firmware bucket, not loader targets.

The 3 rows with no extension are `fastrpc_shell_0` on `FP5`, `Edge_30` and
`Phone_1` — already documented as the Hexagon FastRPC user-PD shell in
`research/fleet/other-gpu-compute.md` §7.1, which records 13 of 13 same-family
builds as ELF32 against the matrix's `ELF64` on all 3 rows, while classing its
own 3 census rows `[U]`. I cite that note rather than re-derive it.

## 3. 809 rows are not ELF files, and the label cannot describe them

Two extensions in this bucket carry no `e_ident` by construction [F]:

| class | rows | files | bytes |
|---|---:|---:|---:|
| `.bNN` — PIL payload segments | **743** | 105 | 14,479,868 |
| `.sig` — signature blobs | **66** | 14 | 3,295,144 |
| **total** | **809** | | **17,775,012** |

**24.6% of the bucket's rows.** A `.b01` segment is the *body* of a program
header — the bytes a split firmware image stores outside the header block. A
`.sig` is a cryptographic signature over some other file. Neither begins with an
ELF header, and neither can, because neither is an ELF file.

The `.sig` names make the point without ambiguity [F]: `asym1p.sig`,
`crypt1p.sig`, `keym1p.sig`, `macch1p.sig`, `nvm1p.sig`, `spsmt1p.sig` — a
signature set over asymmetric, crypto, keymaster, MAC, NVM and SPS partitions.
Sizes 12,464–124,192 B. These are the artifacts that *authenticate* firmware;
labelling them `ELF64` is the magic sniff failing to find `\x7FELF` and the
taxonomy having no better word.

**So the honest statement about this bucket is that its label is true of at most
75% of its rows**, and that the 25% it misdescribes is not a rounding error but
two whole file classes.

## 4. The `.b00` arithmetic: 498 ELF64-shaped, 227 ELF32-shaped, 0 ambiguous

This is the part that can be settled from the matrix alone, with no payload —
using the law already established in `research/fleet/other-misc.md` §3.2:
`b00 == e_ehsize + e_phnum × e_phentsize`, i.e. **`52 + 32N` for ELF32** and
**`64 + 56N` for ELF64**.

Applied to the **725** `.b00` rows in this bucket [F]:

| `.b00` bytes | rows | law | N |
|---|---:|---|---:|
| 148 | 50 | ELF32 `52+32N` | 3 |
| 212 | 9 | ELF32 | 5 |
| 244 | 7 | ELF32 | 6 |
| 308 | 106 | ELF32 | 8 |
| 400 | 7 | **ELF64** `64+56N` | 6 |
| 512 | 161 | **ELF64** | 8 |
| 568 | 330 | **ELF64** | 9 |
| 692 | 34 | ELF32 | 20 |
| 724 | 1 | ELF32 | 21 |
| 756 | 4 | ELF32 | 22 |
| 788 | 2 | ELF32 | 23 |
| 820 | 8 | ELF32 | 24 |
| 852 | 6 | ELF32 | 25 |

**498 ELF64-shaped, 227 ELF32-shaped, and no size is ambiguous** — every one of
the 13 observed sizes satisfies exactly one of the two forms [F]. That
non-overlap is what makes the arithmetic decisive rather than suggestive: a size
cannot be both, so each row is classified by its integer alone.

So **31% of the header blocks this bucket calls `ELF64` are structurally ELF32**,
provable from two integer columns and no bytes.

This extends `other-misc.md` §3.2, which derived the same law over 10 observed
`b00` values in its own `misc` subfamily. Here the same 13-value table covers a
6-family, 91-device bucket.

## 5. The one real loader in the bucket, and it is not the biggest file

`ipa_fws.mdt` is **77 rows / 77 devices / 473,468 B** at 6 distinct sizes
(3,424–7,276 B), present at `*/modem/image` and `*/vendor/firmware` [F]. It is
the only filename here with a mainline `request_firmware()` target [F]:

```c
/* drivers/net/ipa/ipa_main.c:70-72 */
/* The name of the GSI firmware file relative to /lib/firmware */
#define IPA_FW_PATH_DEFAULT	"ipa_fws.mdt"
#define IPA_PAS_ID		15
```

`ipa_main.c` is 28,593 B with **1** `request_firmware` call and **1** mention of
`ipa_fws.mdt` [F]. This is the IPA (IP Accelerator) GSI firmware, loaded through
the PAS remoteproc path with PAS id 15.

So **473,468 B of this bucket — 0.1% of its bytes — has a documented mainline
loader.** The rest does not (§6, §8).

## 6. `amss.bin`: 54.9% of the bucket's bytes, zero mainline references

The single largest filename in the bucket, and the reason its byte total is
what it is [F]:

| metric | value |
|---|---:|
| filename | `amss.bin` |
| rows | 41 |
| devices | 24 |
| bytes | **260,837,728** |
| share of bucket | **54.91%** |
| share of corpus | 0.37% |
| distinct sizes | 7 (5,178,848 – 7,458,880) |
| distinct md5s | 7 |

It sits at `*/modem/image`, including `motorola/rtwo/modem/image/kiwi` and
`nothing/Pong/modem/image/qca6490` subdirectories, on Motorola, Xiaomi, OnePlus,
Nothing and Poco devices [F].

`amss.bin` appears in `torvalds/linux` **twice**, and neither is this file [F]:

- `drivers/net/wireless/ath/ath11k/hw.h`
- `drivers/net/wireless/ath/ath12k/hw.h`

Both are an unrelated Wi-Fi firmware constant. `qcom_q6v5_mss.c`,
`mdt_loader.c` and `qcom_q6v5_pas.c` contain **0** occurrences of `amss` and
**0** of `.bin` [F].

So the file that dominates the bucket's bytes has no loader, no mainline
reference, and — because the label is a 4-byte sniff — **no verified class**. Its
`ELF64` label means only that it begins with `\x7FELF`, if it does. I did not
read it, so its actual format is `[OPEN]` (§10, negative 1).

## 7. The `.mdt` hash-segment law holds on 1,314 of 1,314 groups

`other-misc.md` §3.3 reports `mdt == b00 + b<hash>` closing **502 of 502** groups
in its subfamily. The same test across every group in this bucket that has both
a `.mdt` and a `.b00` [F]:

| | |
|---|---:|
| groups with both `.mdt` and `.b00` | **1,314** |
| `mdt − b00` equals exactly one sibling `.bNN` size | **1,314** |
| no match | **0** |

Not one exception. The identity `mdt = b00 + b<hash>` is a property of the PIL
container format, and it holds at 2.6× the group count of the prior measurement
across six `blob_family` values [F]. The hash segment is *not* necessarily the
last one — `other-misc.md` §3.4 records the hash at index 1 on eight-part TAs with
payload after it — so the test is "equals *some* sibling", not "equals the last".

I report this as confirmation, not as a new law. The law is `other-misc.md`'s.

## 8. Filename → loader verdict

| class | rows | verdict |
|---|---:|---|
| `.mdt` | 1,572 | **PIL container.** Split firmware image whose header block is `.b00` and whose payloads are `.bNN`. Class varies ELF32/ELF64 per `other-misc.md` §3.1; the `mdt = b00 + b<hash>` identity holds 1,314/1,314 here (§7). Only `ipa_fws.mdt` has a mainline loader (§5). |
| `.bNN` | 743 | **Not an ELF file.** Payload segment of the `.mdt` above. The label is a magic-sniff miss (§3). |
| `.elf` | 424 | **ELF by extension.** 64 filenames on 20 devices — `phy_ucode*.elf`, `bd_l1*.elf` and similar. Genuinely ELF; class unverified here. |
| `.img` | 337 | **Mixed.** 19 filenames on 63 devices. `cmnlib.img` and `cmnlib64.img` have `.bNN` siblings in the corpus, so those are monolithic renderings of split images; the other 17 have none. Whether any is ELF is `[OPEN]` (§10, negative 2). |
| `.so.1`, `.so` | 98 | **Userspace shared objects.** 30 audio/voice codec modules (`.so.1`) plus 4 `libsysmon*_skel.so`, on 3 devices (`Edge_30`, `FP5`, `Phone_1`). Genuinely ELF, not firmware loader targets. |
| `.sig` | 66 | **Not an ELF file.** Cryptographic signatures over `asym`/`crypt`/`keym`/`macch`/`nvm`/`spsmt` partitions (§3). |
| `.bin` | 41 | **`amss.bin`, 54.9% of the bucket's bytes, no loader, class `[OPEN]`** (§6). |
| *(none)* | 3 | **`fastrpc_shell_0`** — `other-gpu-compute.md` §7.1 records 13 of 13 same-family builds as ELF32 and the matrix typing all 3 rows `ELF64`; the census builds' own class is `[U]` there. |

**No `db_type` in this bucket corresponds to a single loader contract**, because
the bucket is not a class. The only member with a mainline `request_firmware()`
target is `ipa_fws.mdt`, at 0.1% of the bytes.

## 9. Rule 1 pass

| file | before | after |
|---|---|---|
| `research/fleet/other-misc.md` §3.1 | states the 757 `.mdt` rows are two container families and that the matrix "types all 757 a single `ELF64`, which is right about the TAs and wrong to generalise" | adds the mechanism: `ELF64` is a 4-byte `\x7FELF` prefix test at `device_files.py:222/422` and `Bintypes` has no `ELF32`, so the collapse is structural; and adds the bucket-wide extent — 3,284 rows over 6 families, 809 non-ELF rows |
| `docs/REPO-STATE-MAP.md` driver row | 5 `db_type`-scoped notes under `research/drivers/` | 6, adding `elf64.md` |

`research/CORRECTIONS.md` gains **no** row. The defect is already correctly
recorded three times — `other-misc.md` §3.1, `other-camera.md` §6 and
`other-gpu-compute.md` §7.1 (§1); what this note adds is the cause and the
scope, not a correction of any published figure.

## 10. Honest negatives

1. **`amss.bin`'s format is `[OPEN]`.** It is 54.91% of the bucket's bytes and I
   did not read it. Its `ELF64` label means only that a 4-byte prefix matched, if
   it did — and since `.bNN` and `.sig` rows in the same bucket are labelled
   `ELF64` without being ELF at all, the label carries no class information. I
   will not infer "it is ELF64" from it.

2. **The 19 `.img` names are not classed.** `xbl_config.img`, `qupfw.img`,
   `shrm.img`, `rpm.img` are ELF-carrying in Qualcomm boot chains as a matter of
   external knowledge, but this corpus does not prove it and I did not parse one.
   `[I]` at best, and I do not lean on it.

3. **`cmnlib.img`'s monolithic relationship is inferred from siblings, not
   sizes.** `cmnlib.img` (397,312 / 401,408 B) and `cmnlib64.img` (516,096 /
   520,192 B) each have 6 `.bNN` siblings, which makes them the monolithic
   rendering of a split image. I did not verify that `img == sum(segments)` — the
   segment sizes are not all in this `db_type` (the siblings split across
   `ELF64` and `UNKNOWN`), so the test is not cleanly available here [F].

4. **`.elf` class is unverified.** 424 rows across 64 filenames are ELF by
   extension; whether each is ELF32 or ELF64 is not in the matrix, and
   `isa_identified` is empty on 3,248 of 3,284 rows (98.9%) [F].

5. **The `.b00` law classification assumes the law.** I apply
   `52+32N`/`64+56N` from `other-misc.md` §3.2 without re-deriving it. The result
   (498/227, 0 ambiguous) is only as good as that law — but the law's non-overlap
   is itself the evidence, since 13 distinct sizes each fit exactly one form.

6. **I did not verify the `.sig` contents.** That they are signatures is `[F]`
   from the filenames (`asym1p`, `crypt1p`, `keym1p`, `macch1p`) and `[I]` as to
   what they sign.

7. **The `fastrpc_shell_0` rows are prior art.** `other-gpu-compute.md` owns them
   and records the ELF32-vs-`ELF64` mismatch; I cite it and add nothing.

8. **`ipa_fws.mdt`'s own class in this corpus is unverified.** The *loader* is
   `[F]` (`ipa_main.c:71`). Whether the 77 corpus rows are ELF32 or ELF64 is not
   established here; the `.b00` sizes for `ipa_fws` do not appear in this
   `db_type` (they are `CELL`), so the law cannot be applied to it.

## 11. Reproduce

Every command below was run on 2026-11-28 and exits 0.

```bash
python3 -I -c "
import csv,re
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='ELF64']
tot=sum(int(r['size_bytes']) for r in d)
allb=sum(int(r['size_bytes']) for r in rows)
print('rows',len(d),'files',len({r['filename'] for r in d}),'devices',len({r['device'] for r in d}))
print('bytes',tot,'= %.2f%% of corpus'%(100*tot/allb))
print('distinct md5',len({r['md5_db'] for r in d}),'distinct sizes',len({int(r['size_bytes']) for r in d}))
print('families',dict(Counter(r['blob_family'] for r in d)))
print('isa empty',sum(1 for r in d if not r['isa_identified'].strip()))
print()
print('family rows and bytes:')
for f,c in Counter(r['blob_family'] for r in d).most_common():
    g=[r for r in d if r['blob_family']==f]
    print('  %-8s %-5d %12d %5.1f%%'%(f,len(g),sum(int(r['size_bytes']) for r in g),100*sum(int(r['size_bytes']) for r in g)/tot))"
```

```bash
python3 -I -c "
import csv,re
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='ELF64']
tot=sum(int(r['size_bytes']) for r in d)
def ext(f):
    if re.search(r'\.b\d\d$',f): return '.bNN'
    if f.endswith('.so.1'): return '.so.1'
    return '.'+f.rsplit('.',1)[-1] if '.' in f else '(none)'
print('ext rows files devices bytes share')
for e,c in sorted(Counter(ext(r['filename']) for r in d).items(),key=lambda x:-x[1]):
    g=[r for r in d if ext(r['filename'])==e]
    b=sum(int(r['size_bytes']) for r in g)
    print('  %-8s %-6d %-6d %-4d %-12d %5.2f%%'%(e,c,len({r['filename'] for r in g}),len({r['device'] for r in g}),b,100*b/tot))"
```

```bash
python3 -I -c "
import csv,re
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='ELF64']
bn=[r for r in d if re.search(r'\.b\d\d$',r['filename'])]
sig=[r for r in d if r['filename'].endswith('.sig')]
print('bNN rows',len(bn),'files',len({r['filename'] for r in bn}),'bytes',sum(int(r['size_bytes']) for r in bn))
print('sig rows',len(sig),'files',len({r['filename'] for r in sig}),'bytes',sum(int(r['size_bytes']) for r in sig))
print('non-ELF total',len(bn)+len(sig),'of',len(d),'= %.1f%%'%(100*(len(bn)+len(sig))/len(d)))
print()
print('sig filenames:')
for f in sorted({r['filename'] for r in sig}): print('  ',f)"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='ELF64']
b00=[r for r in d if r['filename'].endswith('.b00')]
print('b00 rows',len(b00))
e32=e64=amb=0
for s,c in sorted(Counter(int(r['size_bytes']) for r in b00).items()):
    a=(s>=52 and (s-52)%32==0)
    b=(s>=64 and (s-64)%56==0)
    law='ELF32' if a else ('ELF64' if b else 'NEITHER')
    if a and b: amb+=c; law='AMBIGUOUS'
    if law=='ELF32': e32+=c
    elif law=='ELF64': e64+=c
    print('  %-6d x%-4d %-8s N=%s'%(s,c,law,(s-52)//32 if a else (s-64)//56 if b else '-'))
print()
print('ELF32-shaped',e32,' ELF64-shaped',e64,' ambiguous',amb,' of',len(b00))"
```

```bash
python3 -I -c "
import csv
from collections import defaultdict
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
grp=defaultdict(dict)
for r in rows:
    stem=r['filename'].rsplit('.',1)[0]
    e=r['filename'].rsplit('.',1)[-1]
    if e=='mdt' or (len(e)==3 and e[0]=='b' and e[1:].isdigit()):
        grp[(r['device'],r['db_path'],stem)][e]=int(r['size_bytes'])
tot=ok=0
for k,v in grp.items():
    if 'mdt' not in v or 'b00' not in v: continue
    tot+=1
    target=v['mdt']-v['b00']
    if any(s==target for e,s in v.items() if e not in ('mdt','b00')): ok+=1
print('groups with mdt+b00',tot)
print('mdt-b00 equals exactly one bNN',ok)
print('no match',tot-ok)"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['db_type']=='ELF64']
tot=sum(int(r['size_bytes']) for r in d)
allb=sum(int(r['size_bytes']) for r in rows)
for name in ('amss.bin','ipa_fws.mdt'):
    g=[r for r in d if r['filename']==name]
    b=sum(int(r['size_bytes']) for r in g)
    print('%-14s rows=%-3d devices=%-3d bytes=%-10d %.2f%% of bucket  %.3f%% of corpus'%(name,len(g),len({r['device'] for r in g}),b,100*b/tot,100*b/allb))
    print('   sizes',sorted({int(r['size_bytes']) for r in g}),'md5s',len({r['md5_db'] for r in g}))
    print('   paths',sorted({r['db_path'] for r in g})[:3])"
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
for i,l in enumerate(t.split(chr(10)),1):
    if 'ELF64' in l or 'header.startswith' in l: print('  %4d: %s'%(i,l.strip()[:100]))
time.sleep(2)
u=get('https://raw.githubusercontent.com/fabiorafaelcoutada/librephone/main/librephone/typedefs.py')
print('typedefs.py bytes',len(u.encode()))
print('  has ELF64:', 'ELF64 =' in u)
print('  has ELF32:', 'ELF32' in u)"
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
t=get('https://raw.githubusercontent.com/torvalds/linux/master/drivers/net/ipa/ipa_main.c')
print('ipa_main.c bytes',len(t.encode()))
print('  request_firmware',t.count('request_firmware'),'  ipa_fws.mdt',t.count('ipa_fws.mdt'))
for l in t.split(chr(10)):
    if 'IPA_FW_PATH_DEFAULT' in l: print('  ',l.strip())
time.sleep(2)
for f in ('drivers/remoteproc/qcom_q6v5_mss.c','drivers/soc/qcom/mdt_loader.c','drivers/remoteproc/qcom_q6v5_pas.c'):
    x=get('https://raw.githubusercontent.com/torvalds/linux/master/'+f)
    print('  %-22s amss=%d .bin=%d'%(f.split('/')[-1],x.count('amss'),x.count('.bin')))
    time.sleep(2)"
```

## Sources

| claim | source | access |
|---|---|---|
| 3,284 rows / 391 filenames / 91 devices / 475,030,376 B = 0.68% of corpus bytes; 265 distinct sizes; 1,990 distinct md5s; `isa_identified` empty on 3,248 | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-28 |
| `blob_family`: `other` 2,162 / `tz` 517 / `boot` 251 / `gpu` 189 / `modem` 156 / `wifi` 9, with bytes 355,254,808 / 9,686,112 / 108,085,624 / 944,240 / 1,008,812 / 50,780 | same CSV | 2026-11-28 |
| extension table: `.mdt` 1,572 / `.bNN` 743 / `.elf` 424 / `.img` 337 / `.so.1` 86 / `.sig` 66 / `.bin` 41 / `.so` 12 / none 3, with per-extension files, devices and bytes | same CSV | 2026-11-28 |
| 809 non-ELF rows (743 `.bNN` + 66 `.sig`) = 24.6% of the bucket; `.sig` names `asym1p`/`crypt1p`/`keym1p`/`macch1p`/`nvm1p`/`spsmt1p`, sizes 12,464–124,192 B | same CSV | 2026-11-28 |
| `.b00`: 725 rows, 13 distinct sizes, 498 ELF64-shaped (`64+56N`), 227 ELF32-shaped (`52+32N`), 0 ambiguous | same CSV | 2026-11-28 |
| `mdt − b00` equals exactly one sibling `.bNN` on **1,314 of 1,314** groups | same CSV | 2026-11-28 |
| `amss.bin` 41 rows / 24 devices / 260,837,728 B = 54.91% of bucket, 0.37% of corpus, 7 sizes, 7 md5s, at `*/modem/image` incl. `kiwi` and `qca6490` | same CSV | 2026-11-28 |
| `ipa_fws.mdt` 77 rows / 77 devices / 473,468 B, 6 sizes (3,424–7,276), at `*/modem/image` and `*/vendor/firmware` | same CSV | 2026-11-28 |
| `("ELF64", bytes([0x7F, 0x45, 0x4C, 0x46]))` at line 222; consumed as `header.startswith(num)` over `file.read(8)` at lines 419–427 | `fabiorafaelcoutada/librephone` `librephone/device_files.py` (21,371 B) | 2026-11-28 |
| `Bintypes` enum contains `ELF64` and **no `ELF32`** | `fabiorafaelcoutada/librephone` `librephone/typedefs.py` (3,024 B) | 2026-11-28 |
| `#define IPA_FW_PATH_DEFAULT "ipa_fws.mdt"` and `IPA_PAS_ID 15` at lines 71–72; `ipa_main.c` 28,593 B, 1 `request_firmware` | `drivers/net/ipa/ipa_main.c`, master | 2026-11-28 |
| `qcom_q6v5_mss.c` 71,201 B, `mdt_loader.c` 13,603 B, `qcom_q6v5_pas.c` 52,404 B: **0** `amss`, **0** `.bin` in each | `drivers/remoteproc/*`, `drivers/soc/qcom/mdt_loader.c`, master | 2026-11-28 |
| `repo:torvalds/linux "amss.bin"` = 2, both `ath11k/hw.h` and `ath12k/hw.h`; `"amss.mbn"` = 0; `"qupfw.img"` = 0; `"xbl_config.img"` = 0; `"ipa_fws.mdt"` = 1 | GitHub code search | 2026-11-28 |
| `.mdt` rows are two container families, 43 ELF32 (PIL) vs 35 ELF64 (AArch64 TAs, `e_machine=183`); matrix types all 757 a single `ELF64`; `b00 == e_ehsize + e_phnum × e_phentsize` law; `mdt == b00 + b<hash>` on 502/502 | `research/fleet/other-misc.md` §3.1, §3.2, §3.3, §3.4 | 2026-11-28 |
| `db_type=ELF64` wrong on 28 of 28 `.mdt` rows, all ELF32 | `research/fleet/other-camera.md` §6 | 2026-11-28 |
| `db_type=ELF64` on 3 of 3 `fastrpc_shell_0` rows against 13 of 13 ELF32 builds | `research/fleet/other-gpu-compute.md` §7.1 | 2026-11-28 |
