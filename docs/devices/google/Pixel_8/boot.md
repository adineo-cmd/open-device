# google Pixel_8 (shiba) — `boot` family: the vendor tree explains the two-axis split, and a 64/64 hash confirmation

Analysis date 2026-11-22. Analyst: OC-3 (issue [#1682](https://github.com/adineo-cmd/open-device/issues/1682)).
Inputs: `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows),
TheMuppets `proprietary_vendor_google_*` `radio/` trees (lineage-23.0), git-lfs pointers.

Evidence classes: **[F]** fact (command output) / **[I]** inference / **[H]** hypothesis /
**[N]** negative / **[OPEN]** unresolved.

## Prior art and prior results

`docs/devices/google/Pixel_7_Pro/boot.md` (#1664) established the **two-axis split** on the
13 Tensor devices: five payload files have one constant size and 13 distinct md5, while four
firmware files have 3–7 sizes and only 8 distinct md5. It also established that the md5
partition is **identical for `abl`, `bl1`, `bl31` and `tzsw`**.

That note's **biggest stated limitation** was that it could not verify any of it:

> "TheMuppets `proprietary_vendor_google_cheetah` carries 40 files and none of the 9 boot
> rows … **nothing here is byte-verified against an upstream source**; every statement is
> matrix-internal."

[F] **That limitation was wrong, and this note fixes it.** The blobs are in the vendor tree —
just under `radio/`, not `proprietary/vendor/firmware/`. `radio/` holds `abl.img`, `bl1.img`,
`bl2.img`, `bl31.img`, `gsa.img`, `ldfw.img`, `modem.img`, `pbl.img`, `tzsw.img` (plus
`gcf.img`/`gsa_bl1.img` on newer devices), stored as **git-lfs pointers that carry the
sha256 and true size**.

I found this while working #1670 on `gsa.img` and I am correcting #1664's honest-negative 2
in place at the same commit as this note.

## Verdict

`Pixel_8` (`shiba`, "Google Tensor G3") has **9 `boot` rows / 103,690,240 B**, 9 distinct
md5, **9/9 4096-aligned**. It shares all four firmware files with `Pixel_8_Pro` and no
other device.

Two results, and the first is the one that matters:

> **1. The vendor tree mechanically explains #1664's two-axis split.** A file is shared
> across devices exactly when the vendor ships it in `radio/`. 9 of 9 files, zero
> exceptions.
>
> **2. The matrix's md5s are now independently confirmed by upstream sha256.** 64/64 sizes
> and all four partitions reproduce exactly.

## 1. The device's 9 `boot` rows

| file | size (B) | md5 | `db_type` | in `radio/` |
|---|---:|---|---|---|
| `boot.img` | 67,108,864 | `0d1ea6a89735c08a363475dfdbb4fc04` | `BOOT` | no |
| `dtbo.img` | 16,777,216 | `ee658f14d5658f1b24258a9d0a94512c` | `DTB` | no |
| `init_boot.img` | 8,388,608 | `03e9865994cb27ba1fef55b34cd33123` | `BOOT` | no |
| `tzsw.img` | 7,864,320 | `2fba0c145c12139493f5d5089e08134c` | `BOOT` | **yes** |
| `abl.img` | 2,367,488 | `d47de42bbefe34b632376c7513c1edca` | `UEFIBOOT` | **yes** |
| `pvmfw.img` | 1,048,576 | `79d0ff7773fb9ef6e24533481ba8907b` | `SECURITY` | no |
| `bl31.img` | 110,592 | `e61e243965d4386c416d68efc5af2a33` | `BOOT` | **yes** |
| `bl1.img` | 16,384 | `b58673f8e0dc86f181cb74c48da57aca` | `BOOT` | **yes** |
| `vbmeta.img` | 8,192 | `93de10435d04b83c49a1d2df05bd19cd` | `AVB` | no |

[F] 9 rows, 9 distinct md5, total **103,690,240 B**, all `db_path = google/shiba/radio`,
`interface_documented = n` on all 9. `Pixel_8` has 52 matrix rows in total.

[F] Upstream sha256 for the four firmware files, from the LFS pointers:

```
abl.img   2,367,488  0cc2a7d8413d33cdfcca042ec0a458aad772593014dfa6ff736f612926981213
bl1.img      16,384  9e66cdbc941377b85d8b5eda7a113ed4ac9849aff89977aa39cf90fbb6b25e5a
bl31.img    110,592  47842199b9f28472d7f25b7eb4bcf7a2ad061c27c94a6d5367311e496ccdc755
tzsw.img  7,864,320  bf47fb157659c9cd158cb059ba1cb6988e0f775565af365fc43851096023e534
```

## 2. The mechanism: `radio/` presence explains the two-axis split

#1664 observed the split but could not say *why*. The vendor tree answers it.

[F] `radio/` is the extracted **firmware-update partition set**. It ships the boot-chain and
security stages the vendor is licensed to redistribute — and it does **not** ship the
device-specific payload images (`boot`, `dtbo`, `init_boot`, `pvmfw`, `vbmeta`), which are
built per-device and live only in factory images.

[F] Testing "is it in `radio/`" against "is its md5 shared across devices" over **all 9**
boot filenames that appear on the 16 Tensor devices:

| file | devices | distinct md5 | distinct sizes | in `radio/` | md5 shared? | rule |
|---|---:|---:|---:|---|---|---|
| `abl.img` | 16 | 10 | 8 | **yes** | yes | ✅ |
| `bl1.img` | 16 | 10 | 3 | **yes** | yes | ✅ |
| `bl31.img` | 16 | 10 | 4 | **yes** | yes | ✅ |
| `tzsw.img` | 16 | 10 | 4 | **yes** | yes | ✅ |
| `boot.img` | 16 | 16 | 1 | no | no | ✅ |
| `dtbo.img` | 16 | 16 | 1 | no | no | ✅ |
| `init_boot.img` | 13 | 13 | 1 | no | no | ✅ |
| `pvmfw.img` | 16 | 16 | 1 | no | no | ✅ |
| `vbmeta.img` | 16 | 16 | 1 | no | no | ✅ |

[F] **9 of 9, zero exceptions:** a file's md5 is shared across devices **iff** the vendor
ships it in `radio/`.

[N] The other four boot filenames in the matrix — `aop.img`, `qupfw.img`, `xbl.img`,
`xbl_config.img` — appear only on the three older Qualcomm Pixels (`Pixel_4A_5G`, `Pixel_5`,
`Pixel_5A`), which are outside this note's 16-device scope. Each has 3 rows and 3 distinct
md5. **I did not check their vendor trees**, so I do not claim the rule covers them (§5.6).

### 2.0 Reconciling with #1664's numbers

#1664 reports "13 distinct md5" and "8 distinct md5". Those are correct on its own scope —
**13 Tensor devices, excluding the GS101 trio** (`Pixel_6`, `Pixel_6A`, `Pixel_6_Pro`).
This note uses **16 Tensor devices**. Both are right; the difference is the device set:

| file | 13-device set (#1664) | 16-device set (this note) |
|---|---|---|
| `abl.img` | 13 rows, **8** md5, 7 sizes | 16 rows, **10** md5, 8 sizes |
| `bl1.img` | 13 rows, **8** md5, 3 sizes | 16 rows, **10** md5, 3 sizes |
| `bl31.img` | 13 rows, **8** md5, 3 sizes | 16 rows, **10** md5, 4 sizes |
| `tzsw.img` | 13 rows, **8** md5, 3 sizes | 16 rows, **10** md5, 4 sizes |

[F] Reproduced exactly: on the 13-device set all four files give 8 md5, and the five payload
files give 13 md5. The rule is invariant to the choice of scope — only the counts move.

[I] The reading is that `radio/` contains **silicon-vendor firmware** — ARM Trusted Firmware
stages, the Samsung TZ image, the Android bootloader — which is identical for every device
built on the same SoC, because it is built once by the silicon vendor. The payload images
are built per product from that product's kernel and device tree, so they cannot collide.

[I] **This also explains the size axis.** #1664 found the payload files have one constant
size (64/16/8/1 MiB, 8 KiB). Those are **partition capacities**, fixed by the A/B slot
layout, which is the same across a generation. The firmware files vary in size because they
are ordinary compiled binaries. Both axes fall out of the same fact: what kind of artifact
the file is.

### 2.1 The one file that needed care

[F] `boot.img` has **2 distinct sizes** across 19 Pixel devices, which looked at first like a
counterexample to "payload ⇒ constant size". It is not: the split is by **platform
generation**, not device:

| size | devices |
|---:|---|
| 67,108,864 (64 MiB) | the 16 Tensor devices (`Pixel_6` … `Pixel_9_Pro_XL`) |
| 100,663,296 (96 MiB) | `Pixel_4A_5G`, `Pixel_5`, `Pixel_5A` — the older Qualcomm Pixels |

[F] And md5 is device-unique **throughout** (19 md5 for 19 devices), so the file is payload
in both size classes. The 2 sizes are two partition layouts, not two sharing behaviours.

[I] I flag this because my first framing of the rule ("payload ⇒ 1 size") was wrong and I
corrected it to "payload ⇒ md5 not shared". The corrected rule is the one that holds 9/9.

## 3. Upstream sha256 confirmation: 64/64 and all four partitions

This is the part #1664 could not do.

[F] **Sizes: 64/64.** All four firmware files across all 16 Pixel devices — 64 LFS pointers —
match the matrix's `size_bytes` exactly.

[F] **Partitions: 4/4.** For each of `abl`, `bl1`, `bl31`, `tzsw`, the sha256 partition
computed from the LFS pointers is **set-equal** to the matrix's md5 partition:

| file | LFS sha256 groups | matrix md5 groups | equal |
|---|---:|---:|---|
| `abl.img` | 10 | 10 | ✅ |
| `bl1.img` | 10 | 10 | ✅ |
| `bl31.img` | 10 | 10 | ✅ |
| `tzsw.img` | 10 | 10 | ✅ |

[F] And the four partitions are **identical to each other** — `len(set(parts.values())) == 1`.
Two hash algorithms, two sources, one grouping:

```
n=4  Pixel_9, Pixel_9_Pro, Pixel_9_Pro_Fold, Pixel_9_Pro_XL
n=2  Pixel_6, Pixel_6_Pro
n=2  Pixel_7, Pixel_7_Pro
n=2  Pixel_8, Pixel_8_Pro
n=1  Pixel_6A, Pixel_7a, Pixel_8A, Pixel_9A, Pixel_Fold, Pixel_Tablet
```

[I] `Pixel_8`'s own position: it shares all four firmware files with **`Pixel_8_Pro`** and
with no other device — the G3 pair, as #1664 predicted.

[I] **This is the strongest confirmation of the matrix in this series.** Every earlier Google
note either stayed matrix-internal or re-hashed a vendor file with the same md5, which is
circular. Here an **independent hash over independent metadata** reproduces the DB's
grouping exactly, on four files and 64 rows.

[N] **Still not byte verification.** The LFS objects themselves return `404`
(`media.githubusercontent.com`) and the batch API says `"Object does not exist on the
server"` — they were never uploaded. I verified **size and sha256 from the pointer text**,
never the bytes. This proves the DB agrees with upstream *metadata*; it does not prove
anything about file contents (§5.1).

## 4. The `tzsw` placement, and why it is not a mislabel

`Pixel_8`'s TrustZone image (`tzsw.img`) sits in `blob_family = boot`, not `tz`. That looks
wrong and is not — `upstream/pr10-remaining-issues-package.md:195-199` groups `tzsw` in the
**boot chain** and `gsa` in the **TrustZone set**, and the matrix follows that taxonomy.

[F] Confirmed on this device: `tzsw.img` is `boot`; the only `tz`-family Google security file
is `gsa.img` (established in #1670). Google's actual TrustZone binary is filed under `boot`.

[I] Worth stating once because it is counter-intuitive, but it is documented taxonomy, not a
defect, and I am not filing it.

## 5. Honest negatives

1. **Pointer-metadata verification, not byte verification.** The LFS objects are absent from
   the server, so no byte of any boot blob was read. §3 compares the DB against upstream
   *metadata* [N].
2. **`sha256_if_listed` is empty for all 9 rows**, so the matrix contributes no hash of its
   own; the upstream sha256 comes from the vendor tree, not the DB [N].
3. **The `radio/` rule is 9 files over the 16 Tensor devices.** It is a strong pattern (9/9)
   but it is one vendor's tree, one device generation range, and I did not test whether
   Qualcomm trees show the same structure [I].
4. **My first statement of the rule was wrong** ("payload ⇒ 1 size"); `boot.img` has 2 sizes.
   Corrected to "payload ⇒ md5 not shared", which holds 9/9 (§2.1). Recorded rather than
   silently fixed [I].
5. **`radio/` presence is not proof of *why* files are shared** — §2's silicon-vendor
   explanation is inference from the file set, not something I measured [I].
6. **The four older-Pixel filenames were not tested against their vendor trees.**
   `aop`, `qupfw`, `xbl`, `xbl_config` appear only on `Pixel_4A_5G`/`Pixel_5`/`Pixel_5A`, and
   each has 3 rows / 3 md5. I did not read those devices' `radio/` listings, so the rule is
   untested there and I exclude them from the 9/9 claim [N].
7. **My first version of §2 mixed two device sets** — 19 Pixels for the payload files and 16
   for the firmware files — which produced a table that silently disagreed with #1664's
   counts. Recomputed on one stated 16-device scope and added §2.0 to reconcile. Recorded
   rather than quietly patched [I].
8. **I did not verify that `radio/` is complete** for every device — I read the directory
   listing for several trees, not all 16 [N].
9. **Web search was unavailable** for this session; **no claim rests on a web source** [N].
10. **No payload is committed**; only 130-byte pointer files were read.

## 6. Rule 1 — corrections for the lead, not applied here

1. **`sha256_if_listed` is empty on all 9 rows**, while the vendor tree publishes a sha256
   for 4 of them in `radio/` LFS pointers. That hash is free to harvest and would make
   `md5_db` falsifiable — as §3 demonstrates. Highest-value fix here.
2. **`blob_family = boot` mixes two artifact classes** — vendor-shipped silicon firmware and
   per-device payload images — and they behave oppositely. A `source` column
   (`silicon-vendor` / `product-build`) would capture what §2 had to infer from the vendor
   tree.
3. **`size_bytes` cannot carry both** partition capacity and artifact size. #1664 flagged
   this; §2.1's `boot.img` case shows both meanings inside one filename.
4. **`interface_documented = n`** on all 9 rows; mainline documents ARM TF `bl1`/`bl31` and
   AVB `vbmeta` thoroughly.
5. **`docs/REPO-STATE-MAP.md:18`** still counts only the 5 `research/soc/` GPU docs.

## 7. Reproduce

```sh
# run from the repo root

# the 9 rows
python3 -I -c "
import csv
r=[x for x in csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv'))
   if x['device']=='Pixel_8' and x['blob_family']=='boot']
for x in sorted(r,key=lambda y:-int(y['size_bytes'])):
    print(f\"{x['filename']:16s} {int(x['size_bytes']):>10,} {x['md5_db']} {x['db_type']}\")
print('rows',len(r),'distinct md5',len({x['md5_db'] for x in r}),
      'total',sum(int(x['size_bytes']) for x in r))"

# which filenames the vendor ships in radio/ (section 2)
curl -s "https://api.github.com/repos/TheMuppets/proprietary_vendor_google_shiba/contents/radio?ref=lineage-23.0" \
  | python3 -I -c "import json,sys; print(sorted(i['name'] for i in json.load(sys.stdin)))"
# expect: abl, bl1, bl2, bl31, gcf, gsa, gsa_bl1, ldfw, modem, pbl, tzsw (.img)

# the rule: md5 shared iff shipped in radio/ (section 2, 16 Tensor devices)
python3 -I -c "
import csv
radio={'abl.img','bl1.img','bl2.img','bl31.img','gcf.img','gsa.img','gsa_bl1.img',
       'ldfw.img','modem.img','pbl.img','tzsw.img'}
t16={'Pixel_6','Pixel_6A','Pixel_6_Pro','Pixel_7','Pixel_7_Pro','Pixel_7a','Pixel_Fold',
     'Pixel_Tablet','Pixel_8','Pixel_8A','Pixel_8_Pro','Pixel_9','Pixel_9A','Pixel_9_Pro',
     'Pixel_9_Pro_Fold','Pixel_9_Pro_XL'}
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
px=[x for x in r if x['device'] in t16 and x['blob_family']=='boot']
ok=True
for f in sorted({x['filename'] for x in px}):
    xs=[x for x in px if x['filename']==f]
    n=len(xs); md5=len({x['md5_db'] for x in xs}); shared=md5<n; inr=f in radio
    good = (shared==inr)
    ok = ok and good
    print(f'{f:14s} n={n:>2d} md5={md5:>2d} radio={str(inr):>5s} shared={str(shared):>5s} {good}')
print('rule holds for all files:',ok)"
# expect 9 lines, every one True, final True

# section 2.0: the same test on #1664's 13-device scope reproduces its 8/13 numbers
python3 -I -c "
import csv
g13={'Pixel_7','Pixel_7_Pro','Pixel_7a','Pixel_8','Pixel_8A','Pixel_8_Pro','Pixel_9',
     'Pixel_9A','Pixel_9_Pro','Pixel_9_Pro_Fold','Pixel_9_Pro_XL','Pixel_Fold','Pixel_Tablet'}
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for f in ['abl.img','bl1.img','bl31.img','tzsw.img','boot.img','dtbo.img','pvmfw.img','vbmeta.img']:
    xs=[x for x in r if x['filename']==f and x['device'] in g13]
    print(f'{f:14s} n={len(xs):>2d} md5={len({x[\"md5_db\"] for x in xs}):>2d} sizes={len({x[\"size_bytes\"] for x in xs})}')"
# expect the four firmware files at n=13 md5=8; the payload files at md5=13

# the upstream sha256 partition for the four firmware files (section 3)
for d in oriole bluejay raven panther cheetah lynx felix tangorpro \
         shiba husky akita tokay tegu caiman comet komodo; do
  for f in abl bl1 bl31 tzsw; do
    printf '%s %s ' "$f" "$d"
    curl -s -L "https://raw.githubusercontent.com/TheMuppets/proprietary_vendor_google_${d}/lineage-23.0/radio/${f}.img" \
      | grep '^oid sha256:' | cut -d: -f2
  done
done | awk '{print $1, $3}' | sort -u | awk '{c[$1]++} END {for (k in c) print k, c[k]}' | sort
# expect abl 10, bl1 10, bl31 10, tzsw 10 distinct sha256 -- matching the matrix's
# 10 md5 groups for each file

# Pixel_8 shares all four with Pixel_8_Pro and no one else (section 3)
python3 -I -c "
import csv
from collections import defaultdict
r=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for f in ['abl.img','bl1.img','bl31.img','tzsw.img']:
    g=defaultdict(list)
    for x in r:
        if x['filename']==f: g[x['md5_db']].append(x['device'])
    mine=[x for x in r if x['device']=='Pixel_8' and x['filename']==f][0]['md5_db']
    print(f, 'shares with', [d for d in g[mine] if d!='Pixel_8'])"
# expect every line: shares with ['Pixel_8_Pro']
```

## What would upgrade this finding

1. **Locate the actual LFS bytes** and confirm one md5 against the sha256. That turns §3 from
   a partition comparison into a hash comparison — blocked only on the objects existing.
2. Harvest LFS sha256s for `bl2`, `ldfw`, `modem`, `pbl` too — the matrix has rows for
   them and they are the same kind of pointer.
3. Test whether a Qualcomm vendor tree shows the same `radio/`-presence rule; if it does,
   §2 is a general property of vendor redistribution, not a Pixel quirk.

Not legal advice. All facts are DB metadata, git-lfs pointer metadata from public vendor
trees, and repo documentation. No binary was parsed and no payload is committed.
