# google Pixel_8 (shiba) — `tz` family: 10 files, 3 family labels, one identical partition

Analysis date 2026-11-22. Analyst: OC-3 (issue [#1688](https://github.com/adineo-cmd/open-device/issues/1688)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows,
4,264 of them `tz`), TheMuppets `proprietary_vendor_google_*` `radio/` trees
(lineage-23.0), git-lfs pointers.

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art

Two in-repo notes bear directly on this device's two rows, and I cite rather than re-derive:

- [`docs/devices/google/Pixel_7_Pro/tz.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/google/Pixel_7_Pro/tz.md)
  (#1670) established that `gsa.img` is a **Google security-chip** image, not TrustZone; that
  the repo's own taxonomy (`upstream/pr10-remaining-issues-package.md:195-199`) puts `gsa` in
  the **TrustZone set** and `tzsw` in the **boot chain**; and that the `gsa.img` sha256
  published in the vendor tree's LFS pointer reproduces the matrix md5 partition exactly.
- [`docs/devices/google/Pixel_8/boot.md`](https://github.com/adineo-cmd/open-device/blob/feat/open-device-site/docs/devices/google/Pixel_8/boot.md)
  (#1682) established that a boot file's md5 is shared across devices **iff** the vendor
  ships it in `radio/`, 9/9 with zero exceptions.

**So the obvious framing for this issue is closed before I start.** `gsa.img` is not a
mislabel; `gsa_bl1.img` is the same kind of artifact; and both are vendor-shipped, which is
why they are shared. I am not going to restate #1670 with a different device name.

What is genuinely new here is a *structural* result that neither note could see, because both
looked at one family at a time.

## Verdict

`Pixel_8` (`shiba`, "Google Tensor G3") has **2 `tz` rows / 413,696 B**, 2 distinct md5,
**2/2 4096-aligned**:

| file | size (B) | md5 | `db_type` |
|---|---:|---|---|
| `gsa.img` | 380,928 | `38043dcebd48e8b426c5d49ece28f67f` | `SECURITY` |
| `gsa_bl1.img` | 32,768 | `3bf35e536678bed81155032874ab343a` | `SECURITY` |

> **The headline is not about these two rows.** On the eight G3/G4 devices, **ten** files
> spanning **three different `blob_family` labels** share **one byte-identical partition** —
> the same 4/2/1/1 grouping — while the family labels say `boot`, `other` and `tz`. The
> family label is not what determines sharing; the vendor tree is.

## 1. The device's 2 rows

[F] 2 rows, 413,696 B, 2 distinct md5, both 4096-aligned, both
`db_path = google/shiba/radio`, `interface_documented = n`, `isa_identified` empty,
`sha256_if_listed` empty, and **both `priority = P3`** — the same priority, unlike the
`P2`/`P3` split I first claimed here (see §7.6, corrected).

[F] `Pixel_8` has 52 matrix rows in total. The `tz` family is 2 of them.

## 2. The partition, and how many files carry it

[F] The 4/2/1/1 partition across the eight G3/G4 devices:

```
n=4  Pixel_9, Pixel_9_Pro, Pixel_9_Pro_Fold, Pixel_9_Pro_XL
n=2  Pixel_8, Pixel_8_Pro
n=1  Pixel_9A
n=1  Pixel_8A
```

[F] **Ten filenames reproduce it exactly** — full 8-device presence, identical set partition:

| file | `blob_family` | `db_type` | Pixel_8 size (B) |
|---|---|---|---:|
| `abl.img` | **boot** | `UEFIBOOT` | 2,367,488 |
| `bl1.img` | **boot** | `BOOT` | 16,384 |
| `bl2.img` | **other** | `UNKNOWN` | 536,576 |
| `bl31.img` | **boot** | `BOOT` | 110,592 |
| `gcf.img` | **other** | `UNKNOWN` | 8,192 |
| `gsa.img` | **tz** | `SECURITY` | 380,928 |
| `gsa_bl1.img` | **tz** | `SECURITY` | 32,768 |
| `ldfw.img` | **other** | `UNKNOWN` | 2,392,064 |
| `pbl.img` | **other** | `UNKNOWN` | 49,152 |
| `tzsw.img` | **boot** | `BOOT` | 7,864,320 |

[F] **Three distinct `blob_family` values — `boot` ×4, `other` ×4, `tz` ×2 — and one
partition.** Also three distinct `db_type` values plus `UNKNOWN` ×4.

[F] Denominator: **73** distinct filenames appear on these eight devices. 30 of them are
present on all eight but with a *different* partition (the per-device payloads `boot`,
`dtbo`, `init_boot`, `pvmfw`, `vbmeta` at 8 groups each; the Mali `rNN` builds at 1 group;
`modem` at 5). So the 10-way identity is a specific class, not a general collapse.

[I] **The reading.** These ten files are the vendor-shipped silicon firmware set — ARM
Trusted Firmware stages, the Android bootloader, the Samsung TZ image, the security-chip
images, and the low-level loaders. They are built **once per SoC** by the silicon vendor, so
every device on that SoC gets the same bytes. The `blob_family` label is assigned per file by
taxonomy and has no bearing on sharing. #1682 found the same mechanism for `boot` alone; this
is the same fact visible across families.

[I] This is why `blob_family` cannot be used as a proxy for "will this file be shared". A
reader who assumed `tz` files are device-unique, or that `other` files are a grab-bag, would
be wrong on both counts for these eight devices.

## 3. `gcf.img`: a third file with the partition, filed under `other`

`gcf.img` is the cleanest illustration and it is new to the repo — no prior note mentions it.

[F] `gcf.img` appears on exactly the eight G3/G4 devices, 8,192 B each, and its md5
partition is **identical** to `gsa_bl1.img`'s:

| devices | count |
|---|---:|
| `Pixel_9`, `Pixel_9_Pro`, `Pixel_9_Pro_Fold`, `Pixel_9_Pro_XL` | 4 |
| `Pixel_8`, `Pixel_8_Pro` | 2 |
| `Pixel_8A` | 1 |
| `Pixel_9A` | 1 |

[F] `partition(gcf.img) == partition(gsa_bl1.img)`: **True**.
[F] `partition(gsa.img restricted to the same 8 devices) == partition(gcf.img)`: **True**.

[F] **LFS verification, 8/8.** All eight `gcf.img` pointers carry `size 8192`, matching the
matrix exactly, and the sha256 partition is **set-equal** to the matrix md5 partition
(**True**):

| codename | device | LFS size | matrix | sha256 (first 12) |
|---|---|---:|---:|---|
| `shiba` | Pixel_8 | 8,192 | 8,192 | `c85017dece6d` |
| `husky` | Pixel_8_Pro | 8,192 | 8,192 | `c85017dece6d` |
| `akita` | Pixel_8A | 8,192 | 8,192 | `0f5cfd0420f1` |
| `tokay` | Pixel_9 | 8,192 | 8,192 | `4c3f9dc5d850` |
| `tegu` | Pixel_9A | 8,192 | 8,192 | `3743b60479f9` |
| `caiman` | Pixel_9_Pro | 8,192 | 8,192 | `4c3f9dc5d850` |
| `comet` | Pixel_9_Pro_Fold | 8,192 | 8,192 | `4c3f9dc5d850` |
| `komodo` | Pixel_9_Pro_XL | 8,192 | 8,192 | `4c3f9dc5d850` |

[F] `gcf.img` is `blob_family = other`, `db_type = UNKNOWN`, `priority = P3` — while its
sibling `gsa_bl1.img`, on the same devices, with the same partition, is
`blob_family = tz`, `db_type = SECURITY`. The two are **not** the same binary (md5 differs
on every device), so this is not a duplicate row; it is two distinct 8 KiB images that
happen to be distributed identically.

[I] The plausible reading is that `gcf.img` is a second security-chip component that simply
was never classified. It is `other`/`UNKNOWN` by omission, not by analysis.

## 4. `modem.bin`, and a duplicate-row caveat

[F] `modem.bin` has **12 rows for 8 devices** — `Pixel_9` carries 2 rows with different sizes
(94,208,604 B and 87,917,140 B) and different `db_path`s
(`google/tokay/vendor/firmware/ntn_modem` vs `google/tokay/modem/images/…`). It has 5 md5
groups and 4 size groups, so it does **not** join the 10-way identity.

[N] I did not investigate the `modem.bin` duplication. It is flagged because a per-device
row count above 1 breaks any "one row per file per device" assumption, and `modem` is a
family I have not analysed in this series.

## 5. The A-suffix devices are singletons on all three security files

[F] Across `gsa.img`, `gsa_bl1.img` and `gcf.img`, the only singleton devices are the
A-suffix models plus the specials:

| file | singleton devices |
|---|---|
| `gsa.img` | `Pixel_6A`, `Pixel_7a`, `Pixel_8A`, `Pixel_9A`, `Pixel_Fold`, `Pixel_Tablet` |
| `gsa_bl1.img` | `Pixel_8A`, `Pixel_9A` |
| `gcf.img` | `Pixel_8A`, `Pixel_9A` |

[F] `Pixel_8A` and `Pixel_9A` are singletons on **all three** files, while `Pixel_8`/`Pixel_8_Pro`
and the four G4 flagships pair up on all three. This is the same A-variant pattern #1664
found for the boot firmware (12/12) and #1670 found for `gsa`.

[I] The A-variants are a distinct product with a distinct firmware build even though
`Pixel_8A` carries `soc = Google Tensor G3`, identical to `Pixel_8`. So `soc` equality does
**not** imply firmware equality here — the same caution #1676/#1748 raised for Mali.

## 6. Honest negatives

1. **Pointer-metadata verification, not byte verification.** The LFS objects return `404`
   from `media.githubusercontent.com` and the batch API replies `"Object does not exist on
   the server"`. I verified **size and sha256 from pointer text** and never read a byte of
   any file [N].
2. **`sha256_if_listed` is empty on both rows**, so the matrix contributes no hash of its own;
   the sha256 evidence comes entirely from the vendor tree [N].
3. **The 10-way partition identity is an 8-device, 2-generation observation.** G3 and G4 only.
   I did not test it on GS101 or GS201 [I].
4. **`gcf.img` is classified `other`/`UNKNOWN` and I did not determine what it is.** I
   established its partition and its size and that it is not a duplicate of `gsa_bl1.img`;
   I did **not** identify the image or its function. Calling it a "security-chip component" in
   §3 is inference from co-location, not from anything I read [I].
5. **I did not verify `bl2.img`, `ldfw.img`, `pbl.img` against LFS pointers** — only
   `gcf.img` and (in #1670/#1682) `gsa*`, `abl`, `bl1`, `bl31`, `tzsw`. Their inclusion in the
   table rests on matrix md5 alone [N].
6. **Two rows is two rows.** The device-level content of this note is 413,696 bytes; every
   substantive result is family-level [I].
7. **`modem.bin`'s duplicate rows are unexplained** (§4) [OPEN].
8. **Gate 0 web search returned nothing usable.** Searches for `gcf.img`, `gsa.img` and
   "Google Security Chip" returned only generic factory-image pages. Mainline code search for
   both filenames returned **0 hits** in `torvalds/linux`. **No claim here rests on a web
   source** [N].
9. **No payload is committed**; only 130-byte pointer files were read.

## 7. Rule 1 — corrections for the lead, not applied here

1. **`blob_family` does not predict sharing.** Ten files with one identical partition carry
   three different family labels (§2). Any consumer that groups by `blob_family` to reason
   about deduplication will get this wrong.
2. **`gcf.img` is `other`/`UNKNOWN` with a `SECURITY`-shaped sibling.** 8 KiB, on all eight
   G3/G4 devices, partition-identical to `gsa_bl1.img`. It is almost certainly a
   security-chip image that was never classified. Lowest-effort high-value fix: classify it.
3. **`modem.bin` has 12 rows for 8 devices** (§4) — duplicate rows with different sizes and
   `db_path`s. Worth a dedupe pass.
4. **`sha256_if_listed` is empty on both rows** while the vendor tree publishes a sha256 in
   its LFS pointer — free to harvest, as §3 demonstrates on 8 devices.
5. **`interface_documented = n`** on both rows; `gsa_bl1.img` is a standard stage-1 loader.
6. **`priority = P3` on all ten files here, including both `tz` rows.** I first wrote that
   `gsa_bl1.img` and `gcf.img` were `P3` while the rest were `P2` — that was wrong. On
   `Pixel_8` every one of the ten is `P3`. The real pattern is across devices, not files:
   `gsa.img` is `P2` on the GS101 trio and `Pixel_7`, and `P3` on the other twelve devices.
   I had read the globally-first row per filename (which happened to be `Pixel_6`, `P2`)
   instead of this device's row. Corrected; see #1760 §7.2 [OPEN].

## 8. Reproduce

```sh
# run from the repo root

# the 2 rows
python3 -I -c "
import csv
r=[x for x in csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv'))
   if x['device']=='Pixel_8' and x['blob_family']=='tz']
for x in r: print(x['filename'],x['size_bytes'],x['md5_db'],x['db_type'])
print('rows',len(r),'bytes',sum(int(x['size_bytes']) for x in r))"
# expect 2 rows, 413696 B

# ten files, three family labels, one partition (section 2)
python3 -I -c "
import csv
from collections import defaultdict
g8={'Pixel_8','Pixel_8A','Pixel_8_Pro','Pixel_9','Pixel_9A','Pixel_9_Pro',
    'Pixel_9_Pro_Fold','Pixel_9_Pro_XL'}
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
def part(f):
    p=defaultdict(list)
    for x in r:
        if x['filename']==f and x['device'] in g8: p[x['md5_db']].append(x['device'])
    return frozenset(frozenset(v) for v in p.values()), sum(len(v) for v in p.values())
tgt,_=part('gcf.img')
fams=defaultdict(int); hits=[]
for f in sorted({x['filename'] for x in r if x['device'] in g8}):
    p,n=part(f)
    if n==8 and p==tgt:
        hits.append(f); fams[[y for y in r if y['filename']==f][0]['blob_family']]+=1
print('files with the identical partition:',len(hits))
print(hits)
print('family labels:',dict(fams))"
# expect 10 files, family labels {'boot':4,'other':4,'tz':2}

# gcf.img partition equals gsa_bl1.img and gsa.img (section 3)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
def part(f,devs=None):
    p=defaultdict(list)
    for x in r:
        if x['filename']==f and (devs is None or x['device'] in devs): p[x['md5_db']].append(x['device'])
    return frozenset(frozenset(v) for v in p.values())
g8={x['device'] for x in r if x['filename']=='gcf.img'}
print('gcf == gsa_bl1 :',part('gcf.img')==part('gsa_bl1.img'))
print('gcf == gsa(8)  :',part('gcf.img')==part('gsa.img',g8))"
# expect True True

# gcf.img LFS sha256 partition == matrix md5 partition (section 3)
for d in shiba husky akita tokay tegu caiman comet komodo; do
  printf '%s ' "$d"
  curl -s -L "https://raw.githubusercontent.com/TheMuppets/proprietary_vendor_google_${d}/lineage-23.0/radio/gcf.img" \
    | grep '^oid sha256:' | cut -d: -f2
done | awk '{print $2}' | sort | uniq -c | sort -rn
# expect: 4 x 4c3f9dc5..., 2 x c85017de..., 1, 1  -- the same 4/2/1/1 partition

# the denominator (section 2)
python3 -I -c "
import csv
from collections import defaultdict
g8={'Pixel_8','Pixel_8A','Pixel_8_Pro','Pixel_9','Pixel_9A','Pixel_9_Pro',
    'Pixel_9_Pro_Fold','Pixel_9_Pro_XL'}
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
print('distinct filenames on the 8 devices:',len({x['filename'] for x in r if x['device'] in g8}))
print('modem.bin rows:',sum(1 for x in r if x['filename']=='modem.bin' and x['device'] in g8))"
# expect 73 and 12

# the tz family context (unchanged from #1670)
python3 -I -c "
import csv
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
tz=[x for x in r if x['blob_family']=='tz']
print('tz rows',len(tz),'bytes',sum(int(x['size_bytes']) for x in tz))
print('google rows',sum(1 for x in tz if x['vendor']=='google'))"
# expect 4264 / 665173154 / 51
```

## What would upgrade this finding

1. **Identify `gcf.img`.** 8 KiB, vendor-shipped, partition-identical to `gsa_bl1.img`, filed
   `other`/`UNKNOWN`. That is the single most tractable open question here.
2. **Verify `bl2`, `ldfw`, `pbl` against their LFS pointers** — the same one-command check
   that confirmed `gcf`, `gsa`, `abl`, `bl1`, `bl31`, `tzsw`.
3. **Test the 10-way identity on GS101/GS201** — it is currently a G3/G4 result.

Not legal advice. All facts are DB metadata, git-lfs pointer metadata from public vendor
trees, and repo documentation. No binary was parsed and no payload is committed.
