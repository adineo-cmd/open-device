# The `touch` subfamily of `other` — panel firmware, fingerprint firmware, and a 74% byte-share that is neither

**Issue:** #2064 · **Analysis date:** 2026-11-21 · **Evidence classes:** `[F]` measured fact
(command and output shown) · `[I]` inference from stated facts · `[N]` honest negative ·
`[U]` unresolved.

**Scope.** The 880 matrix rows classified `blob_family=other, blob_subfamily=touch`:
**71 distinct devices**, 8 vendors, 125 distinct filenames, 516,418,690 B.

**Artifacts read (read-only, never committed).**
`…/second-device/larry/tree-odm/firmware/tp/` — 131 files, 18,429,750 B, 23 panel directories;
`…/mediatek/extract/trees/vendor/firmware/` — 14 Goodix files, 1,236,480 B.
No payload byte is reproduced beyond ≤16-byte hex samples.

**Clean-room.** Everything below was produced by `struct.unpack_from` against files on disk and
by reading public kernel sources. No vendor driver, datasheet, or NDA document was consulted.

---

## 0. Headline

1. **`[F]` The bucket is 74.7% not-touch.** `aoc.bin` accounts for 16 rows and
   **385,991,552 B of 516,418,690 B** — 74.7439% of the subfamily's bytes — filed as
   `TOUCHSCREEN` under `google/*/vendor/firmware`. The genuine panel-firmware family
   (`FW_*`/`LIMIT_*`) is 660 rows but only 73,886,385 B. See §3.
2. **`[F]` `_FAE` is not a format marker.** The suffix spans **6** distinct container formats
   across 37 files. A name-grammar reading of `FW_*_FAE.img` predicts one format. This is the
   concrete refutation of the "naming grammar is DB-derivable" framing in
   `upstream/per-soc-methods.md` L250. See §5.2.
3. **`[F]` The Goodix GT9886 container is fully specified and closes arithmetically.**
   `0x100` header + 11 segment descriptors summing to 88,064 B = exactly 88,320 B, **14/14**
   files, with one byte-identical descriptor table across all 14. Checksum is
   **`BE16(sum(bytes[6:])) mod 2^16`**, **14/14**. See §6.
4. **`[F]` That checksum is the same *family* as mainline, in a different container.**
   `goodix_fwupload.c` in `torvalds/linux@master` accumulates `(data[i]<<8)+data[i+1]` — a
   big-endian byte sum — but over a fixed **36,878 B** `hw_info/pid/vid` layout. None of the 14
   files match it; all are 88,320 B. See §7.
5. **`[F]` 13 `gt9886_firmware_*` files collapse to 7 distinct payloads.** Six SoC-suffixed
   names share one byte-identical binary (`md5 bfaefcab276398f6e369e8837b2fa2c8`). See §6.4.
6. **`[F]` `gt9886_firmware_6885b0.bin` is named GT9886 but self-identifies as GT9885**
   (and `goodix_firmware.bin` does too). A filename/header disagreement the database cannot see.
   See §6.3.
7. **`[N]` No ISA is recorded for any of the 880 rows, and none was resolved here.**
   `isa_identified` is blank on 880/880; `interface_documented=n` on 880/880. See §9.

---

## 1. The subfamily in numbers

```
python3 -I -c "
import csv,collections
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
t=[r for r in rows if r['blob_subfamily']=='touch']
print(len(t), len({r['device'] for r in t}), len({r['vendor'] for r in t}),
      len({r['filename'].split('/')[-1] for r in t}), sum(int(r['size_bytes']) for r in t))"
```

```
880 71 8 125 516418690
```

| vendor | rows | devices |
|---|---:|---:|
| oneplus | 509 | 20 |
| realme | 158 | 2 |
| google | 99 | 17 |
| motorola | 78 | 13 |
| xiaomi | 25 | 9 |
| sony | 7 | 7 |
| nothing | 3 | 2 |
| lenovo | 1 | 1 |

(Device counts sum to 71 across vendors with no device listed under two vendors.)

`db_type` is again incoherent for this bucket — five labels, and one of them is a file
*format* rather than a device class:

| `db_type` | rows | what it actually is |
|---|---:|---|
| `TOUCHSCREEN` | 410 | panel firmware, plus `aoc.bin` |
| `TOUCHSCREEN5` | 196 | panel firmware |
| `TOUCHSCREEN3` | 110 | panel firmware |
| `UNKNOWN` | 98 | Goodix GT9916 panel firmware |
| `TOUCHSCREEN4` | 41 | panel firmware |
| `ELF64` | 25 | **Goodix fingerprint** partition images |

Priority is almost entirely un-triaged: **P3 860 / P2 20**, no P1.
`isa_identified` is blank on **880 of 880**; `interface_documented=n` on **880 of 880**.

### 1.1 Row inflation `[F]`

880 rows resolve to only **452 distinct `(device, filename)` pairs** — **1.95 rows per pair**.
90 of those pairs carry more than one `size_bytes` value. The cause is panel-directory fan-out:
one file name appears once per panel directory. `Realme_9_Pro` carries
`FW_NF_NT36672C_TIANMA.img` **7 times**, at 7 distinct `db_path` values
(`realme/oscar/odm/firmware/tp/{20121,21039,216E9,216EA,21708,…}`) with a single distinct size.

Rows-per-pair histogram: `1×295, 2×52, 3×36, 4×16, 5×25, 6×12, 7×16`.

Distinct `md5_db` across all 880 rows: **289**.

### 1.2 `TOUCHSCREENn` is not a stable axis `[F]`

`TOUCHSCREEN3/4/5` look like a taxonomy, but **27 of 71 devices carry more than one** of them,
and no filename ever carries two (`0 / 125` filenames have >1 `db_type`). The suffix tracks the
generation of the *device row* that first ingested the file, not the file. Treat
`TOUCHSCREEN` and `TOUCHSCREEN3/4/5` as one class.

### 1.3 A data defect in the `soc` column `[F]`

78 rows (all on one device) carry a `soc` value beginning with `\xff`:
`'ÿQualcomm SM6375 Snapdragon 695 5G'`. No row on that device carries the clean string, so
these 78 rows will not join on `soc`. Verified: `clean twin exists: 0`.

---

## 2. Family classification

Classifying the 125 filenames by leading token, over all 880 rows:

```
python3 -I -c "
import csv,collections
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
t=[r for r in rows if r['blob_subfamily']=='touch']
def fam(n):
    b=n.split('/')[-1]
    if b.startswith(('FW_','LIMIT_')): return 'panel FW_/LIMIT_'
    if b.startswith('goodixfp'): return 'fingerprint goodixfp.*'
    if b.startswith('aoc'): return 'aoc.bin'
    if b.startswith('cs40l2'): return 'haptics cs40l2x'
    if b.startswith(('goodix-','goodix_','goodix.')): return 'goodix-* named'
    if b.startswith('synaptics'): return 'synaptics*'
    if b.startswith(('gt9','s6sy','s3908')): return 'bare IC name'
    if b.startswith('touch'): return 'touch*'
    return 'other'
c=collections.Counter(); by=collections.Counter()
for r in t: f=fam(r['filename']); c[f]+=1; by[f]+=int(r['size_bytes'])
for k,v in c.most_common(): print(k,v,by[k])"
```

| family | rows | bytes | is it touch? |
|---|---:|---:|---|
| panel `FW_*`/`LIMIT_*` | 660 | 73,886,385 | yes |
| fingerprint `goodixfp.*` | 74 | 42,318,428 | **no** |
| haptics `cs40l2x` | 53 | 41,944 | **no** |
| `goodix-*` named (GT9916) | 36 | 7,367,936 | yes |
| bare IC name (`gt9886_*`, `s6sy*`) | 22 | 2,977,232 | yes |
| `aoc.bin` | 16 | 385,991,552 | **no** |
| `synaptics*` | 14 | 3,028,917 | yes |
| `touch*` (`touch_module_id_0x*.img`) | 5 | 806,296 | yes |

Totals reconcile to **880 rows / 516,418,690 B**.

Device-level: **57 of 71** devices carry genuine panel firmware. The remaining 14 are
fingerprint-only or `aoc.bin`-only.

---

## 3. `aoc.bin`: 74.7% of the bytes, none of the subject

```
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
a=[r for r in rows if r['filename'].split('/')[-1]=='aoc.bin']
print(len(a), sum(int(r['size_bytes']) for r in a), sorted({r['size_bytes'] for r in a}))
for r in a[:4]: print(r['device'], r['vendor'], r['size_bytes'], r['db_type'], r['db_path'])"
```

```
16 385991552 ['15158976','21328448','29234048']
Pixel_6A       google 15158976 TOUCHSCREEN google/bluejay/vendor/firmware
Pixel_Tablet   google 21328448 TOUCHSCREEN google/tangorpro/vendor/firmware
Pixel_8_Pro    google 29234048 TOUCHSCREEN google/husky/vendor/firmware
Pixel_6_Pro    google 15158976 TOUCHSCREEN google/raven/vendor/firmware
```

**`[F]` 385,991,552 / 516,418,690 = 74.7439%.** Three distinct sizes only:
15,158,976 / 21,328,448 / 29,234,048. All three are multiples of **64** (gcd of the three is
64), but **not** of 256 — remainders 192 / 64 / 128 — so they are not page- or sector-aligned
in any obvious way. I am not asserting an alignment rule.

`[I]` `aoc` is the always-on-camera / ISP block on Google Tensor parts, not a touch controller.
The evidence is positional, not payload-level: every one of the 16 rows sits in
`google/<codename>/vendor/firmware` beside the panel firmware, on a Tensor SoC, and the file is
1–2 orders of magnitude larger than any panel firmware in this subfamily (largest genuine panel
file: **392,133 B**, `larry/22668/FW_NF_ILI7807S_HUAXING.img`; `aoc.bin` is **38.7–74.6×** that). The payload was **not** analysed — no
local copy exists (`find` over the workspace returns nothing). This is a `[I]`, and it is the
one classification in this document that rests on placement rather than bytes.

`[N]` Confirming it would need a Pixel `vendor` partition. That is a concrete, small next step,
and it is not blocked on anything but a download.

**Consequence for any future count:** quoting "the touch subfamily is 516 MB" overstates the
panel-firmware subject by **7.0×** (516,418,690 / 73,886,385). Even excluding only `aoc.bin`
leaves 130,427,138 B, still 1.77× the panel firmware. The panel-firmware subject is 73,886,385 B
= **14.3075%** of the bucket.

---

## 4. Local artifacts

Two independent corpora, both hash-checked against the matrix.

### 4.1 `larry` ODM panel fleet `[F]`

`larry` is OnePlus Nord CE 3 Lite 5G / Nord N30 5G, SM6375
(`research/fleet/second-device-larry.md`). Its ODM tree carries the touch fleet:

```
find …/larry/tree-odm/firmware/tp -type f | wc -l          → 131
find … -type f -printf "%f\n" | sed 's/_.*//' | sort | uniq -c
                                                          → 88 FW, 43 LIMIT
```

131 files / **18,429,750 B** across **23 panel directories**.

```
20121 21039 21095 21221 21291 21341 21629 2162B 21653 216E9 216EA 21707 21708
22035 22041 22045 22241 22273 22601 22602 22667 22668 22821
```

### 4.2 Hash reconciliation `[F]`

```
python3 -I  (md5 each local file; look up (dir, filename) in the matrix)
larry files: 131 | md5 matches a matrix row: 78 | no matrix row: 53 | md5 mismatch: 0
```

**Zero mismatches** — where the matrix and disk overlap, they agree byte-for-byte. The 53
unmatched files are a real gap, not a discrepancy: 8 of the 23 directories
(`21341 21629 2162B 21653 22601 22602 22667 22668`) are **owned by no matrix device at all**.
`larry`'s own matrix identity `Nord_CE3` lists only 15 of the 23 directories.

`[I]` The 8 orphan directories are panel variants shipped in the ODM image that the census
pipeline never attributed to an identity. They are the cheapest available expansion of this
subfamily: 53 files, already on disk, zero download cost.

### 4.3 Goodix GT9886 `[F]`

```
python3 -I  (14 files in …/mediatek/extract/trees/vendor/firmware)
14 / 14 exact md5 match against matrix touch rows.
```

1,236,480 B total, every file exactly **88,320 B**.

---

## 5. Container formats in `larry` `[F]`

Magic census over all 131 files:

| container | n | bytes | how identified |
|---|---:|---:|---|
| `LIMITIMG` | 41 | 1,131,548 | ASCII `LIMITI` + `MG` |
| `FwUp` | 38 | 7,931,050 | ASCII `FwUp` |
| raw `00010000` | 22 | 3,063,808 | 4-byte magic |
| `IntelHEX` | 13 | 4,895,321 | leading `:` + `\r\n` |
| raw `02174102` | 6 | 401,110 | 4-byte magic |
| raw `00000962` | 3 | 272,232 | 4-byte magic |
| raw `5b505635` | 2 | 94,052 | 4-byte magic |
| raw `2b471848` | 2 | 374,745 | 4-byte magic |
| raw `00000060` | 2 | 246,828 | 4-byte magic |
| raw `3c66696c` | 2 | 19,056 | 4-byte magic |

Total 131 / 18,429,750 B.

### 5.1 The name grammar predicts far less than the files deliver `[F]`

Crosstab of trailing name token × container:

| token | containers observed |
|---|---|
| `AGING` | `LIMITIMG` |
| `BOE` | `LIMITIMG`, `FwUp` |
| `DSJM` | `FwUp`, `LIMITIMG`, `5b505635` |
| `HUAXING` | `FwUp`, `LIMITIMG` |
| `JDI` | `FwUp`, `LIMITIMG` |
| `SAMSUNG` | `FwUp`, `LIMITIMG` |
| `TEST` | `00010000`, `FwUp` |
| `TIANMA` | `FwUp`, `LIMITIMG` |
| `VXN` | `FwUp`, `LIMITIMG` |
| `config` | `3c66696c` |
| **`FAE`** | **6 formats** |

Panel-vendor tokens are *reasonably* consistent (two containers each). `_FAE` is not.

### 5.2 `[F]` `_FAE` spans six formats

37 files carry `_FAE` in the name, in six mutually incompatible containers:

| container | `_FAE` files |
|---|---:|
| Intel HEX | 13 |
| raw `00010000` | 11 |
| raw `02174102` | 6 |
| raw `00000962` | 3 |
| raw `2b471848` | 2 |
| raw `00000060` | 2 |

`FW_NF_ILI7807S_TIANMA_FAE.img` is **ASCII Intel HEX** (358,761 B of text).
`FW_NF_NT36672C_TIANMA_FAE.img` is a **139,264 B binary** starting `00 01 00 00 …`.
`FW_FT3518_SAMSUNG_FAE.img` starts `02 17 41 02`. `FW_GT9886_SAMSUNG_FAE.img` starts
`00 00 09 62`. `FW_FT3681_BOE_FAE.img` starts `00 00 00 60`. `FW_S3910_TIANMA_FAE.img` starts
`2b 47 18 48` and contains the ASCII tag `BOOT_CONFIG`.

**This is the single most useful negative result in this document.** `per-soc-methods.md` L250
lists the `FW_*`/`LIMIT_*` grammar as `METADATA (DB-derivable grammar)` and rates the work
"small". The grammar is real and it is DB-derivable — but it carries **no format information**.
`_FAE` means "factory-engineering variant", and which container that implies depends on the
controller, not the name.

---

## 6. `LIMITIMG` — the limit/aging container `[F]`

### 6.1 Header

```
LIMIT_NF_ILI7807S_TIANMA.img  (25,980 B)
0000 4c 49 4d 49 54 49 4d 47 fe e7 03 00 00 00 00 00 |LIMITIMG........|
0010 4c 00 00 00 d0 00 00 00 90 01 00 00 4c 14 00 00 |L...........L...|
```

- `[0x00:0x08)` magic `LIMITIMG`
- `[0x08:0x0c)` `le32` per-controller constant (see 6.2)
- `[0x0c:0x10)` zero
- `[0x10:…]` monotonic `le32` offset table, one entry per record

### 6.2 Structural checks — all 41/41 `[F]`

| check | result |
|---|---|
| `table[0] == 0x10 + 4 × count` | **41 / 41** |
| offset table monotonic | **41 / 41** |
| `le32 @ record+4 == (next offset − this offset)` | **449 / 449** records |
| last record ends exactly at EOF | **41 / 41** |

**449 records** total. Per-file record counts: `5×3, 7×11, 8×2, 10×1, 12×11, 14×1, 15×11, 20×1`.

### 6.3 Record magic `[F]`

```
record magics: {'OPPO': 367, 'SLPO': 82}   (449 records)
```

Two record magics, both 4 ASCII bytes. Record layout beyond `magic(4) + le32 span(4)` varies by
controller and is **`[U]`** — e.g. the `NT36672C` record continues `01 00 06 00` while the
`ILI7807S` record continues `01 00 00 00`, and the field at `+12` is not a length
(distinct values 13984, 204, 396, 588, 16384 across 11–12 records each).

### 6.4 `le32 @ 0x08` is a per-controller constant `[F]`

| controller | `le32 @ 0x08` | files |
|---|---:|---:|
| FT3518 | 382 | 11 (incl. the corrupt file, §6.5) |
| FT3681 | 510 | 2 |
| GT9886 | 62 | 3 |
| ILI7807S | 255998 | 11 |
| NT36523 | 2097150 | 1 |
| NT36672C | 8190 | 11 |
| S3910 | 2046 | 1 |
| TD4377 | 254 | 1 |

`[I]` Seven of the nine distinct values are `2^k − 2` for integer `k`
(62=2⁶−2, 254=2⁸−2, 510=2⁹−2, 2046=2¹¹−2, 8190=2¹³−2, 255998, 2097150=2²¹−2).
`255998` is not (`255998+2 = 256000`, not a power of two), so the pattern is suggestive, not
established. **`[U]` what the field means.** It is stable per controller, which is enough to use
it as a controller fingerprint.

### 6.5 One corrupt file `[F]`

`21221/LIMIT_FT3518_SAMSUNG.img` (29,720 B) has `le32 @ 0x08 = 400556414 = 0x17e0017e`.
Decomposed: `low16 = 0x017e = 382` — exactly the FT3518 constant — and `high16 = 0x17e0 = 6112
= 382 × 16`. The file's own offset table is still monotonic and its records still span correctly,
so the table is intact; only this field is damaged. It is the sole outlier among 41 files and
should be excluded from any per-controller inference.

Records by controller across all `LIMITIMG` files:
`ILI7807S 165, NT36672C 132, FT3518 84, NT36523 20, FT3681 16, GT9886 15, S3910 10, TD4377 7`.

---

## 7. `FwUp` — the main panel container `[F]`

38 files, 7,931,050 B.

```
FW_NF_ILI7807S_TIANMA.img  (358,969 B)
0000 46 77 55 70 05 13 26 fa 00 00 00 00 69 79 05 00 |FwUp..&.....iy..|
0010 00 00 00 80 74 70 2f 32 30 31 32 31 2f 46 57 5f |....tp/20121/FW_|
0020 4e 46 5f 49 4c 49 37 38 30 37 53 5f 54 49 41 4e |NF_ILI7807S_TIAN|
0030 4d 41 2e 69 6d 67 00 00 00 00 00 00 00 00 00 00 |MA.img..........|
```

| offset | size | meaning | evidence |
|---|---|---|---|
| `0x00` | 4 | magic `FwUp` | 38/38 |
| `0x04` | 4 | unidentified; 22 distinct values | `[U]` |
| `0x08` | 4 | zero, 38/38 | `[F]` |
| `0x0c` | 4 | **payload length** | `[F]` |
| `0x10` | 4 | flag, always `00 00 00 80` | 38/38 |
| `0x14` | 188 | NUL-padded ASCII build path | `[F]` |
| `0xd0` | — | payload begins (208-byte header) | `[F]` |

**Closure: `208 + le32@0x0c == filesize` — 38 / 38 `[F]`.** The header is a fixed 208 bytes.

### 7.1 The embedded build path is a provenance record `[F]`

`[0x14:0xd0)` holds a relative path such as `tp/20121/FW_NF_ILI7807S_TIANMA.img`. Measured
against each file's actual location:

| observation | count |
|---|---:|
| path present (non-empty) | 37 / 38 |
| path ends with the file's own basename | 29 / 38 |
| path names a *different* basename | 8 / 38 |
| path points at the file's own directory | 16 / 38 |
| path points at a **different** directory | 21 / 38 |
| path empty | 1 / 38 |

The 21 cross-directory paths cite `20121` (9), `21311` (2), `21095` (1), `21707` (1), and 8 are
bare `tp/` with no panel directory.

`[F]` **These are build-time paths, not install paths.** A file at `22041/FW_FT3518_SAMSUNG.img`
records `tp/21311/FW_FT3518_SAMSUNG.img`. The ODM image re-homed the file into a second panel
directory without rewriting the header.

### 7.2 Payload duplication `[F]`

38 `FwUp` files carry only **24 distinct payloads** (`md5` over `[0xd0:]`):

| payload | copies | panel directories |
|---|---:|---|
| `7984c81152ec…` | 4 | 20121, 216E9, 216EA, 21708 |
| `08dd377f9cec…` | 4 | 20121, 216E9, 216EA, 21708 |
| `57bdb2b62597…` | 4 | 20121, 216E9, 216EA, 21708 |
| `26f9e1f086bb…` | 4 | 22601, 22602, 22667, 22668 |
| `744137cf7215…` | 2 | 21629, 2162B |
| `db56c1ffc6f2…` | 2 | 22041, 22241 |

`[I]` Panel directories are **not** independent firmware sets. `20121`, `216E9`, `216EA`,
`21708` are four names for one physical panel configuration; likewise `22601/22602/22667/22668`
and `21629/2162B`. Combined with §6.5's corrupt file and §4.2's 8 orphan directories, the 23
directories represent roughly 13–15 genuinely distinct configurations.

### 7.3 `_TEST` and `_FAE` are re-encodings, not copies `[F]`

For the `NT36672C` families, the `_TEST.bin` and `_FAE.img` variants are the same length as the
`FwUp` payload (139,264 B) but **not** byte-identical to it or to each other:

```
20121/FW_NF_NT36672C_TIANMA.img       payload 139264  md5 57bdb2b62597
20121/FW_NF_NT36672C_TIANMA_FAE.img   139264 (after 8-byte prefix) md5 4566d621f449
20121/FW_NF_NT36672C_TIANMA_TEST.bin  139264 (after 8-byte prefix) md5 38e232b36fd5
```

Byte-diff between `FAE` and the `FwUp` payload: **88,318 of 139,264 bytes differ**, first at
offset 0, last at `0x21ff7`. Between `TEST` and payload: **81,747** differ. Between `FAE` and
`TEST`: **54,448** differ.

`[I]` These carry different header/address fields over largely the same image, consistent with
the `FwUp` payload being zero-prefixed in its first 16 bytes (`00…00`) while `FAE`/`TEST` begin
with a populated descriptor (`8b 33 01 00 00 80 01 00 40 70 02 00 …`). `[U]` the exact
transformation — it is not a constant XOR, and the byte multisets differ
(`same byte multiset: False`).

---

## 8. Intel HEX `_FAE` files `[F]`

13 files, 4,895,321 B, **108,851 records**, **0 bad checksums**.

| record type | count | note |
|---|---:|---|
| `0x00` data | 108,720 | 1,739,520 data bytes total |
| `0x01` EOF | 13 | last line in 13/13 files |
| `0x02` extended segment | 20 | payloads `1000` ×13, `2000` ×7 |
| `0x03` start segment | 13 | |
| `0xAF` **vendor** | 59 | 5 distinct payloads |
| `0xB0` **vendor** | 26 | 4 distinct payloads |

`[F]` Types `0xAF` and `0xB0` are **non-standard**. They carry valid Intel HEX checksums
(`sum(record) & 0xff == 0` on all 85) and all sit at address `0x0000`, at the **head** of each
file (record indices 0–6). The 5 distinct `0xAF` payloads are
`000000013fff01, 01d00001efff02, 01f00001f1ff03, 01400001cfff05, 020000021fff04`;
the 4 distinct `0xB0` payloads are `02090002, 02070003, 02087002, 02067003`.

`[I]` The `0xAF` payloads end in an incrementing tag (`…01` … `…05`) and encode
`(offset, length)`-shaped pairs — consistent with a vendor region manifest emitted before the
data records. `[U]` the semantics.

**Practical note for any parser:** a strict Intel HEX reader will reject these 13 files on
record type. They are valid Intel HEX *with vendor extensions*.

---

## 9. Goodix GT9886 container — fully specified `[F]`

14 files, 88,320 B each, 1,236,480 B total. All 14 hash-match matrix `touch` rows exactly.

### 9.1 Header

```
gt9886_firmware_6885a1.bin
0000 00 01 58 fa c7 28 4e 4f 52 5f 47 31 00 00 0a 39 |..X..(NOR_G1...9|
0010 38 38 36 00 00 00 00 08 02 02 a9 0b 93 02 02 00 |886.............|
```

| offset | size | field | evidence |
|---|---|---|---|
| `0x00` | 4 | magic `00 01 58 fa` | 14/14 |
| `0x04` | 2 | **`BE16` checksum** | see 9.2 |
| `0x06` | 6 | ASCII tag `NOR_G1` | 14/14 |
| `0x0c` | 2 | zero | 14/14 |
| `0x0e` | 1 | chipid string length = `0x0a` | 14/14 |
| `0x0f` | 4 | **chipid ASCII** (`9886` / `9885`) | 14/14 |
| `0x13` | 4 | zero | 14/14 |
| `0x17` | 1 | version (0,3,5,8) | 14/14 |
| `0x18` | 2 | `02 02` on 12 files, `00 00` on 1, `02 01` on 1 | `[U]` |
| `0x1a` | 6 | per-file build bytes | `[U]` |
| `0x20` | 88 | **11 segment descriptors, stride 8** | 14/14 |
| `0x78` | 136 | zero padding | 14/14 |
| `0x100` | — | segment data | `[F]` |

### 9.2 Checksum `[F]`

**Rule: the `BE16` at `0x04` equals `sum(bytes[6:]) mod 2^16`.** Holds **14 / 14**.

Candidate rules tested, same 14 files:

| rule | matches |
|---|---:|
| `BE16(sum(bytes[6:]))` | **14 / 14** |
| `LE16(sum(bytes[6:]))` | 0 / 14 |
| `BE16(sum(bytes[4:]))` | 0 / 14 |
| `BE16(sum(bytes[0x20:]))` | 0 / 14 |
| `BE16(sum(bytes[0x78:]))` | 0 / 14 |
| `BE16(sum(bytes[0x100:]))` | 0 / 14 |
| `BE16(sum(all bytes))` | 0 / 14 |

The checksum therefore covers the descriptor table and the zero padding as well as the segment
data, and it **excludes** the magic and the checksum field itself. Body length is even on all
14 (needed for a 16-bit sum).

`[F]` A correction to my own earlier reading: I first described this as
"`byteswap16(sum(body))`", which was an artifact of unpacking the field little-endian. Read as
`BE16` it is a plain byte sum — the same accumulation mainline uses (§10).

### 9.3 Segment table closes arithmetically `[F]`

11 descriptors at `0x20`, stride 8, each `(u16 type, u16 length, u16 w2, u16 w3)`.
**All 14 files carry one byte-identical descriptor table.**

| # | type | length | w2 | w3 | file offset |
|---:|---:|---:|---:|---:|---|
| 0 | 1 | 2,048 | `0000` | `00ff` | `0x00100` |
| 1 | 3 | 8,192 | `0000` | `0040` | `0x00900` |
| 2 | 3 | 8,192 | `0000` | `0060` | `0x02900` |
| 3 | 3 | 8,192 | `0000` | `0080` | `0x04900` |
| 4 | 3 | 8,192 | `0000` | `00a0` | `0x06900` |
| 5 | 3 | 8,192 | `0000` | `00c0` | `0x08900` |
| 6 | 3 | 8,192 | `0100` | `0000` | `0x0a900` |
| 7 | 3 | 8,192 | `0100` | `0020` | `0x0c900` |
| 8 | 3 | 8,192 | `0100` | `0040` | `0x0e900` |
| 9 | 3 | 4,096 | `0100` | `0060` | `0x10900` |
| 10 | 2 | 16,384 | `0000` | `0000` | `0x11900` |

Sum of lengths = **88,064**. `0x100 + 88,064 = 88,320` = filesize. **14 / 14 `[F]`.**

Type histogram `[1,3,3,3,3,3,3,3,3,3,2]` — one `type=1` descriptor first, nine `type=3`, one
`type=2` (the 16,384 B block) last. `[I]` `type=3` is a code bank (8,192 B is the natural
Goodix SRAM bank size; mainline uses `GOODIX_FW_SECTION_LENGTH 0x2000`), `type=2` the DSP image
(mainline `GOODIX_FW_DSP_LENGTH 0x1000`), `type=1` a config block. **`[U]` the type semantics**
— the lengths agree with mainline's two named constants, the type *numbers* are unverified.

### 9.4 Naming defects `[F]`

Chipid histogram across the 14 files: **`9886` ×12, `9885` ×2**.

| file | chipid in header | version |
|---|---|---|
| `goodix_firmware.bin` | `9885` | 3 |
| **`gt9886_firmware_6885b0.bin`** | **`9885`** | 5 |

`gt9886_firmware_6885b0.bin` is named for GT9886 and self-identifies as **GT9885**. Its
neighbour `gt9886_firmware_6885b1.bin` correctly says `9886` (version 8). Both are 88,320 B and
both pass the checksum, so this is not corruption — it is a mislabelled file.

`[I]` A device flashing `6885b0` gets GT9885 firmware. Whether that is a deliberate fallback or a
packaging error cannot be decided from the file alone. **`[U]`**

The `goodix_firmware.bin` case is expected: it is the generic name, and it happens to hold a
GT9885 image.

### 9.5 Payload collapse `[F]`

```
gt9886_firmware_* files: 13
distinct (size, md5): 7
```

| md5 | copies | names |
|---|---:|---|
| `bfaefcab276398f6e369e8837b2fa2c8` | **6** | 6781v01, 6853v01, 6873v01, 6877v01, 6885v01, 6893v01 |
| `3e7fd375e0e9fb4753c1c75457481f64` | 2 | 6877af, 6885af |
| `b43351355430703eb3b4ec7e12d4ac1d` | 1 | 6885a1 |
| `b8bf2736cc2e0ab5962770526e1bfd4d` | 1 | 6885b1 |
| `3e156e49881ad2aadc4b204c90d2be67` | 1 | 6885b0 |
| `b48bae75e4fb026da87805ba200d0c79` | 1 | 6785a4 |
| `5d6b249bfd023e3fa69e6577a3f1810d` | 1 | 6785ae |

**`[F]` The `6781 / 6853 / 6873 / 6877 / 6885 / 6893` suffixes do not distinguish firmware.**
Six files with six different SoC-number suffixes are one byte-identical 88,320 B binary. The
`…v01` suffix likewise carries no information — five of the six are the same file.

`[I]` These suffixes are the *build host's* SoC list, not a payload selector: one firmware image
was copied out under six per-SoC names during packaging. Any future census that counts
"firmware variants" by filename will overcount by ~2×.

---

## 10. Mainline comparison — where the delta actually is

### 10.1 `goodix_fwupload.c` `[F]`

Present in `torvalds/linux@master`, `drivers/input/touchscreen/goodix_fwupload.c`:

```c
struct goodix_fw_header {
	u8 hw_info[4];
	u8 pid[8];
	u8 vid[2];
} __packed;

#define GOODIX_FW_SECTION_LENGTH	0x2000
#define GOODIX_FW_DSP_LENGTH		0x1000

static u16 goodix_firmware_checksum(const u8 *data, int size)
{
	u16 checksum = 0;
	int i;
	for (i = 0; i < size; i += 2)
		checksum += (data[i] << 8) + data[i + 1];
	return checksum;
}
```

`expected_size = 14 + 4*0x2000 + 0x1000 = **36,878**`.

Comparison with the 14 local files:

| property | mainline | local GT9886 |
|---|---|---|
| total size | 36,878 B fixed | 88,320 B fixed |
| header | 14 B `hw_info/pid/vid` | 256 B + 11-descriptor table |
| magic | none | `00 01 58 fa` |
| checksum | BE16 byte sum over body | **BE16 byte sum over `bytes[6:]`** |
| section sizes | 4×8,192 + 4,096 | 2,048 + 8×8,192 + 4,096 + 16,384 |

`[F]` **The checksum *family* matches; the container does not.** Mainline's accumulation is the
same big-endian byte sum, and its `0x2000`/`0x1000` constants match two of the observed segment
lengths — but no local file satisfies mainline's size or header test
(`88320 − 36878 = 51,400`). Feeding these files to `goodix_fwupload.c` would fail
`"Firmware has wrong size"`.

`[I]` These are the GTX8-generation ("Normandy"/"Yellowstone") images that mainline's
`goodix_fwupload.c` targets by *checksum convention* but not by *container*. The GT9886 is
explicitly one of the two ICs the out-of-tree GTX8 driver supports.

### 10.2 What mainline has, per controller

| controller | mainline driver | firmware loading |
|---|---|---|
| Goodix GT9xxx (generic) | `goodix.c` | **yes** — `goodix_fwupload.c` |
| Goodix GT9916 (Berlin) | `goodix_berlin_core.c` (811 lines) | no — `struct goodix_berlin_fw_version` has `__le16 checksum` + state/buffer fields; update listed as not supported |
| Goodix GTX8 / GT9886 | *not in master* | patch `[PATCH v2 0/3]` (2026-02-28) says "Firmware updates … is not included"; `goodix_gtx8.c` returns 404 |
| Novatek NT36672C | `novatek-nvt-ts.c` (350 lines) | **no firmware code at all** — 0 matches for firmware/checksum/upload |
| Ilitek ILI7807S | `ilitek_ts_i2c.c` (687 lines) | version *read* only (`ILITEK_TP_CMD_GET_FW_VER 0x40`) |
| FocalTech FT3518 | none in `drivers/input/touchscreen/` | — |
| Synaptics S3908/S3910 | RMI4 core only | no panel-firmware loader |

Verified by directory listing of `drivers/input/touchscreen` on 2026-11-21: no
`focaltech*` and no `goodix_gtx8*` file exists.

`[N]` **So: of the six controllers whose containers this document describes, mainline has a
firmware loader for exactly one — and it does not accept these files.**

### 10.3 Public prior art `[N]`

Searched 2026-11-21 for the `LIMITIMG` and `FwUp` container formats, for the FocalTech `_FAE`
blob layout, for the Synaptics S3908/S3910 `.img` layout, and for `"NOR_G1"` Goodix. **No public
description of any of them was found.** The `NOR_G1` tag, the `LIMITIMG` offset table, the
`FwUp` 208-byte header, and the `OPPO`/`SLPO` record magics appear in no indexed source. The one
public signal — the GTX8 patch's "The checksum method differs yet again" — is a statement that
the format is unknown upstream, not a description of it.

This is the gap this document fills, and it is worth stating plainly: **`per-soc-methods.md`
declared touch payload RE "blocked: needs packages". The packages were the whole obstacle.**

---

## 11. Honest negatives

1. **`[N]` No ISA resolved for any of the 880 rows.** `isa_identified` is blank on 880/880.
   Nothing in `larry`'s 131 files or the 14 Goodix files names a core. The Goodix GT9886 is an
   8051-class controller per its vendor lineage, but **no byte in these files proves it** — I did
   not find a vector table, a reset jump, or an ISA string. I am not asserting 8051.
2. **`[N]` No interface resolved.** `interface_documented=n` on 880/880. The files are opaque
   images with no bus metadata; the bus (I2C vs SPI) is a property of the device tree, not the
   blob.
3. **`[N]` `aoc.bin` was not analysed.** No local copy exists. Its classification as non-touch is
   positional (`[I]`), not payload-level. See §3.
4. **`[N]` No disassembly was attempted.** No Xtensa, 8051, or ARM backend is available in this
   environment (capstone 5.0.7 has no Xtensa backend, and none of these targets are Xtensa
   anyway). Everything here is container-level.
5. **`[U]` `FwUp` `bytes[0x04:0x08]`.** 22 distinct values, no correlation found with size,
   panel, controller, or the embedded path. Reported as unidentified rather than guessed.
6. **`[U]` `LIMITIMG` record fields beyond `magic + span`.** The `OPPO`/`SLPO` records have
   per-controller interiors I could not reduce to a common schema. §6.3 shows the divergence.
7. **`[U]` the `_TEST` ↔ `_FAE` ↔ payload transformation.** Three different encodings of the same
   139,264 B image; the mapping is not a constant XOR and not a permutation. §7.3.
8. **`[U]` the 7 raw-magic containers.** 39 files across `00010000` (22), `02174102` (6),
   `00000962` (3), `5b505635` (2), `2b471848` (2), `00000060` (2), `3c66696c` (2) were
   fingerprinted by magic and byte-counted but not parsed. They are the largest remaining gap in
   `larry` (4,471,831 B of 18,429,750 B = 24.2642%).
9. **`[N]` No `LIMITIMG`/`FwUp` writer or parser was added to `implementations/`.** The
   structural rules in §6.2 and §7 are stated precisely enough to implement, and §6.2's four
   checks each pass 41/41 — but writing a parser was out of scope for this issue and I did not
   claim it works beyond the checks shown.

---

## 12. Corrections to existing text

Per Rule 1, corrected in place rather than only contradicted here:

- `docs/REPO-STATE-MAP.md` — had `media` and `audio` rows but **no `touch` row**. Added.
- `research/soc/per-soc-method-plans.md` L195-197 — the census template says
  "type/size/hashes only". That ceiling is now lifted for the 145 local files; annotated in
  place rather than rewritten, since the plan text is a historical record of method.
- `upstream/per-soc-methods.md` L107-108 — "Blocked: payload RE … (packages not on this box)".
  The packages are on this box now. Annotated in place.

`upstream/per-soc-methods.md` L250 (`METADATA (DB-derivable grammar)`, "small") is **not**
corrected in place: the statement is true about the grammar and the grammar was used. §5.2 shows
why the grammar is insufficient, which is a finding about the payload, not an error in that row.

---

## 13. Numbers, with commands

Every figure in this document traces to one of these.

| figure | value | how |
|---|---|---|
| rows / devices / vendors / filenames / bytes | 880 / 71 / 8 / 125 / 516,418,690 | `blob_subfamily=='touch'` filter |
| `aoc.bin` bytes and share | 385,991,552 / 74.7439% | sum over 16 rows ÷ bucket total |
| devices with panel firmware | 57 of 71 | family set per device |
| distinct `md5_db` | 289 | set size |
| `(device,filename)` pairs | 452 (1.95 rows/pair) | `Counter` over pairs |
| `larry` files / bytes / dirs | 131 / 18,429,750 / 23 | `os.walk` + `getsize` |
| `larry` md5 agreement | 78 match, 53 absent, **0 mismatch** | md5 vs matrix `md5_db` |
| `_FAE` files / formats | 37 / **6** | magic per file |
| `LIMITIMG` files / records | 41 / 449 | offset-table walk |
| `LIMITIMG` closure checks | 41/41 ×4, 449/449 | see §6.2 |
| `FwUp` files / header / closure | 38 / 208 B / 38-38 | `208 + le32@0x0c` |
| `FwUp` distinct payloads | 24 of 38 | md5 over `[0xd0:]` |
| Intel HEX files / records / bad checksums | 13 / 108,851 / **0** | record walk |
| Goodix files / size | 14 / 88,320 B | `getsize` |
| Goodix checksum rule | **14 / 14** | `BE16(sum(bytes[6:]))` |
| Goodix segment closure | **14 / 14** | `0x100 + Σlengths == size` |
| Goodix distinct payloads | 7 of 13 | md5 |
| Goodix chipid | 9886 ×12, 9885 ×2 | `bytes[15:19]` |
| mainline expected size | 36,878 B | `14 + 4*0x2000 + 0x1000` |

---

## 14. What this changes

- **Byte accounting for `touch` must be split.** 74.7% of the subfamily's bytes are one
  non-touch file on 16 Google devices. Any "touch is 516 MB" statement is wrong by ~4×.
- **The `_FAE` name means nothing about format.** Six containers behind one suffix. Any pipeline
  that dispatches on the name will mis-parse 24 of 37 `_FAE` files.
- **The Goodix GT9886 container is now specified well enough to validate.** `0x100 + Σ(lengths)`
  and `BE16(sum(bytes[6:]))` are both checkable in three lines and both pass 14/14. This is the
  first touch container in this repo with a complete, verified structure.
- **Filename SoC suffixes are unreliable.** Six `gt9886_firmware_<soc>` files are one binary;
  one is mislabelled 9885. Variant counting by filename overcounts ~2×.
- **The panel-directory fan-out is ~1.6×.** 23 directories → ~13–15 distinct configurations
  (`FwUp` payload collapse, plus 8 directories no matrix device owns).

## 15. Next steps that are actually unblocked

1. **The 8 orphan panel directories** — 53 files, already on disk, zero download cost (§4.2).
2. **A `LIMITIMG`/`FwUp` parser in `implementations/`** — §6.2 and §7 give the rules; all four
   `LIMITIMG` checks and the `FwUp` closure check are ready-made tests.
3. **One Pixel `vendor` partition** to settle `aoc.bin` (§3) — turns an `[I]` into an `[F]` and
   removes 74.7% of the bucket's bytes from the touch account.
4. **The 39 raw-magic files** (4,471,831 B) — seven containers fingerprinted, none parsed (§11.8).
