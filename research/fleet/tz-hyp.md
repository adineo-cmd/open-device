# `hyp` — the Qualcomm hypervisor partition across the fleet (63 rows, 63 devices)

Analysis date: 2026-11-22. Analyst: OC-1 (`100milionseek`), issue
[#2065](https://github.com/adineo-cmd/open-device/issues/2065).

Inputs:
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows) for the
census; three payload-decoded `hyp.img` images for the container work
(SDM845, SM8250, QCM6490 — all already on disk from earlier sessions); and the
vendor specification *Secure Boot and Image Authentication — Technical Overview*
(Joona Kannisto, Qualcomm Finland RFFE Oy, © 2024), retrieved 2026-11-22.
Every number below is command output. No payload is committed; samples are
≤16 bytes of hex.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** The `hyp` bucket is the narrowest in the corpus — **one filename,
one `db_type`, one `db_path` leaf, 63 rows for 63 devices** — and the most
valuable per byte. It is the Qualcomm hypervisor (QHEE), and it is the only
partition in the fleet where I can show a **complete generational rewrite of the
signed-image container** from decoded payloads: three generations, three
different header bases, three different signature algorithms, and a
`w[1]` field that turns out to be the **MBN format version**. That last point
answers an open item that `research/fleet/pil-metadata-sweep.md` §9 has carried
since it was written.

The bucket also carries a fleet census story worth stating plainly: **11 of the
63 rows are exactly 8 MiB (2²³)**, all Motorola, and they are 60.2% of the
bucket's bytes. Those rows are almost certainly **partition-size** records
rather than image sizes, but I cannot prove it from the matrix alone (§4.4).

---

## 1. What the bucket contains `[F]`

| property | value |
|---|---|
| rows | **63** |
| devices | **63** (exactly one row per device) |
| vendors | **8** |
| distinct filenames | **1** — `hyp.img` |
| total bytes | **153,300,992** |
| distinct `md5_db` | **58** |
| `db_type` | `SECUREBOOT` **63/63** |
| `db_path` leaf | `radio` **63/63** |
| `blob_family` | `tz` **63/63** |
| `blob_subfamily` | `hyp` **63/63** |
| `interface_documented` | `n` **63/63** |
| `isa_identified` | `AArch64` **1/63** (FP6 only) |
| `sha256_if_listed` | present **1/63** (FP6 only) |
| priority | `P3` 59, `P2` 3, `P1` 1 |

This is a maximally clean bucket: every row agrees on family, subfamily,
filename, `db_type`, and the `db_path` leaf. There is no naming drift to
reconcile and no second filename to classify.

### 1.1 Position inside the `tz` family `[F]`

| metric | value |
|---|---|
| `tz`-family rows | 4,264 across 87 devices |
| `hyp` rows | 63 |
| `hyp` share of `tz` rows | **1.48%** |
| `tz`-family bytes | 665,173,154 |
| `hyp` share of `tz` bytes | **23.05%** |

All 63 `hyp` devices also appear in the `tz` family — `hyp` is never an orphan
partition. `hyp` is 1.5% of the family's rows but 23% of its bytes, because the
8 MiB cluster is large.

### 1.2 Vendor and size distribution `[F]`

| vendor | rows | devices | bytes | size range observed |
|---|---:|---:|---:|---|
| motorola | 21 | 21 | 97,476,608 | 520,192 – 8,388,608 |
| oneplus | 18 | 18 | 26,398,720 | 397,312 – 3,739,648 |
| xiaomi | 13 | 13 | 16,265,216 | 372,736 – 1,458,176 |
| fairphone | 3 | 3 | 5,795,840 | 409,600 – 3,702,784 |
| google | 3 | 3 | 1,241,088 | 413,696 |
| nothing | 2 | 2 | 4,935,680 | 1,257,472 – 3,678,208 |
| realme | 2 | 2 | 794,624 | 397,312 |
| fxtec | 1 | 1 | 393,216 | 393,216 |

| size class | rows | bytes |
|---|---:|---:|
| < 512 KiB | 26 | 12,075,008 |
| 1 – 2 MiB | 21 | 30,351,360 |
| 2 – 4 MiB | 5 | 18,599,936 |
| **exactly 8 MiB** | **11** | **92,274,688** |

There is a gap: **no row falls between 512 KiB and 1 MiB**. The population is
bimodal — a compact cluster (26 rows under 512 KiB) and a large cluster (16 rows
at 1 MiB and above, 11 of them at exactly 8 MiB).

`[F]` All 63 sizes are multiples of 4,096.

### 1.3 SoC coverage `[F]`

19 distinct SoC strings across 38 rows; **25 rows have a blank `soc` cell**
(39.7% of the bucket). SoC coverage is therefore a minority property of this
bucket, not a majority one. The SoCs named are:

`MSM8998` (835), `QCM6490`, `SM4250` (460), `SM4375` (4 Gen 1), `SM6115` (662),
`SM6225` (680 4G), `SM6375` (695), `SM7225` (750G), `SM7250` (765G),
`SM7325-AE` (778G / 778G+), `SM8150` / `SM8150-AC` (855), `SM8250` (865),
`SM8350` / `SM8350-AC` (888 / 888+), `SM8475` (8+ Gen1), `SM8550` (8 Gen2).

The span is **MSM8998 (2017) through SM8550 (2022)** — five SoC generations, all
Qualcomm. `[N]` No MediaTek, Exynos, or Tensor device carries a `hyp` row.

### 1.4 A data defect in the `soc` column `[F]`

One `hyp` row — `Nord_CE3` (oneplus) — carries a `soc` value whose first byte is
`0xFF`:

```
Nord_CE3   soc = '\xffQualcomm SM6375 Snapdragon 695 5G'   (utf-8: c3bf 5175616c...)
```

`[F]` This is **not** unique to `hyp`: the same `0xFF`-prefixed value appears on
**506 rows fleet-wide**, all of them `Nord_CE3`, spread over at least nine
subfamilies (`''` 212, `wpss` 81, `touch` 78, `misc` 62, `camera` 35, `media`
16, `oled` 16, `fastchg` 5, `hyp` 1). There is exactly **one** distinct corrupt
value in the corpus and **zero** clean `Qualcomm SM6375 Snapdragon 695 5G`
values, so the defect is a single bad cell that propagated across the device's
rows — a `0xFF` sentinel that leaked into a text field, not a parsing artefact of
this analysis.

`[I]` Practical consequence for anyone joining on `soc`: `Nord_CE3` will not
match `Realme_9_Pro`/`Realme_10_Pro`/`Nord_CE2`/`Moto_G34_5G` etc. on the SoC
string even though all are SM6375. The `hyp` bucket is SM6375-heavy (7 rows), so
this matters here. `[U]` Whether the upstream export should be fixed is out of
scope for this issue; recorded so the next analyst does not re-derive it.

---

## 2. The payload set `[F]`

Three `hyp.img` images were already on disk. Two are the controls used by
`research/fleet/pil-metadata-sweep.md`; the third (FP6) is the census subject of
`research/qualcomm/docs/trustzone-census.md`. No new download was needed.

| tag | SoC | path (repo-relative to the workspace, not committed) | bytes | md5 |
|---|---|---|---:|---|
| SDM845 | Snapdragon 845 | `data-fetch/enchilada/hyp.img` | 397,312 | `cb7ed1e9…` |
| SM8250 | Snapdragon 865 | `data-fetch/second-device/instantnoodle/hyp.img` | 450,560 | `e25f3c81…` |
| QCM6490 | QCM6490 (Lanai) | `lineage-fp6/…/partitions-tzbt/hyp.img` | 1,683,456 | `7937f78a…` |

`[F]` The FP6 image at `partitions-tzbt/hyp.img` and at
`trees-tzbt/trustzone/hyp.img` are byte-identical (`7937f78a…`), so the two
extraction trees agree.

### 2.1 The FP6 row's two hashes disagree `[F]`

The matrix row for FP6 carries both an `md5_db` and a `sha256_if_listed`. They
cannot both describe the file I measured:

| source | value |
|---|---|
| matrix `md5_db` | `43fd89a2d79cd853c2509ff3139c3e12` |
| matrix `sha256_if_listed` | `210cc7647547dec8…` |
| measured md5 of local file | `7937f78ad20025e1061d872f59b58fae` |
| measured sha256 of local file | `210cc7647547dec82215b8d771595f75c2de3ff95611ffaade8fed67d86c2887` |

The **sha256 matches the matrix exactly**; the **md5 does not**. Since a file
has one md5 and one sha256, at least one cell is wrong. `[I]` The most likely
reading is that the md5 column was populated from a different build (or a
different partition's row) while the sha256 came from the correct file — the
sha256 is a full match on a 64-hex string, which is hard to reach by accident.
`[U]` Which cell is authoritative cannot be settled from the matrix; the payload
on disk agrees with the sha256, so I treat the sha256 as the correct
identification of FP6's `hyp.img` and flag the md5 as inconsistent.

`[F]` Separately, `docs/devices/fairphone/FP6/tz.md` line 22 records the DB-vs-
census comparison for this row as **"OK"** at 1,683,456 B with "md5
corpus-unique". That size comparison is correct. The md5 uniqueness claim is not
tested here and I do not contradict it — but the *value* in the matrix column is
not the value of the file. Both statements can be true only if the "unique md5"
claim was made against a hash computed elsewhere.

---

## 3. The container, generation by generation `[F]`

All three images are ELF64 AArch64 and all three put their signing metadata in a
**`PT_NULL` (`p_type == 0`) program-header segment with `p_memsz == 0`** — that
is, a segment the loader does not map. `[F]` On all three, `seg[0]` (also
`PT_NULL`) has `filesz == 64 + phnum × 56` exactly, i.e. the ELF header plus the
program header table, matching the pattern already recorded in
`research/fleet/qsee-crossgen.md`.

`[F]` The metadata segment is **the last `PT_NULL` segment with `filesz > 0`** in
all three images. On SDM845/SM8250 it is phdr index **1** (file offset 4,096); on
QCM6490 it is phdr index **6** (file offset 1,671,168).

`[F]` The trailing bytes after the last segment's `offset + filesz` are **all
zero** in all three images (688 / 1,144 / 1,152 bytes). This is the reverse of
the metadata segment's own tail, which is `0xFF`.

### 3.1 Header words, decoded

| word | SDM845 (MBNv5) | SM8250 (MBNv6) | QCM6490 (MBNv7) | meaning |
|---|---:|---:|---:|---|
| `w[0]` | 4 | 0 | 0 | image-specific `[U]` |
| **`w[1]`** | **5** | **6** | **7** | **MBN format version** (§3.2) |
| `w[2]` | 0 | 0 | 24 | signer-metadata block size − 200 `[U]` |
| `w[3]` | 0 | 0 | 224 | signer-metadata block size = `7 × 32` |
| `w[4]` | 6,528 | 6,592 | 224 | metadata size after the header |
| `w[5]` | 128 | 192 | 336 | hash table = `phnum × width` |
| `w[6]` | −1 | −1 | 104 | signature size (MBNv7 only) |
| `w[7]` | 256 | 256 | 3,360 | cert-chain capacity |
| `w[8]` | −1 | −1 | 104 | OEM signature size (MBNv7 only) |
| `w[9]` | 6,144 | 6,144 | 3,360 | cert-chain capacity (per chain) |
| `w[10]` | 2,600,464,680 | 0 | 0 | payload `[U]` |
| `w[11]` | 451,633,870 | 120 | 0 | header-extension size (SM8250) `[U]` |
| `w[12]` | 88,332,660 | 0 | 21 | `[U]` |

`[F]` `w[5] == phnum × digest width` holds on all three: 4×32 = 128 (SDM845,
SHA-256), 4×48 = 192 (SM8250, SHA-384), 7×48 = 336 (QCM6490, SHA-384). This
extends the 28/28 rule in `pil-metadata-sweep.md` §5 to a **31st, structurally
different** image.

### 3.2 `w[1]` is the MBN format version — proven from the certificate itself `[F]`

This closes the open item at `research/fleet/pil-metadata-sweep.md` §9:

> "Whether w[1] (5 vs 6) is a secboot metadata format version and whether it
> flips with the hash width or with the SoC generation (only one SoC per value
> observed)."

Three independent lines of evidence, in increasing strength:

1. **The values line up with the version sequence.** `w[1]` = 5, 6, 7 on
   SDM845, SM8250, QCM6490 respectively — increasing with platform generation,
   not with hash width (SM8250 and QCM6490 both use SHA-384 but differ at
   `w[1]` = 6 vs 7). That alone refutes the "flips with hash width" half of the
   question.
2. **The vendor specification names the format.** The Qualcomm paper describes
   "the hash segment of Qualcomm Technologies' latest Signed Image Format (**MBN
   version 7**)" and separately describes **MBNv5** as the version that encoded
   image metadata "into the Organizational Unit (OU) fields of the leaf
   certificate". That is a version-numbered format with a documented v5/v7
   behavioural difference.
3. **The certificate CN prints the number.** `[F]` FP6's QTI chain carries the
   literal string `SRoT MBNv7 Image Signing Root CA 6` (and `… Root CA 6 SubCA
   1`) in its certificate subjects — the string `MBNv7` appears in the image at
   metadata offset 1,094 and is the root CA's own name. `[N]` Neither the SDM845
   nor the SM8250 image contains any `MBNv\d` string anywhere; their chains are
   named `QCT Root CA 1` / `OEM Attestation CA` / `QUALCOMM Attestation CA`.

Point 3 is decisive: the image whose `w[1] == 7` is the image whose certificate
says `MBNv7`. `w[1]` is the MBN format version.

`[F]` And the MBNv5 behaviour the spec describes is directly observable: the
SDM845 leaf certificate's **OU fields carry the image metadata** —

```
subject = C=US, CN=SecTools Test User, L=San Diego, O=SecTools, ST=California,
          OU = 01 0000000000000015 SW_ID,
          OU = 02 600000000051459B HW_ID,
          OU = 04 0051 OEM_ID,
          OU = 05 000000A8 SW_SIZE,
          OU = 06 459B MODEL_ID,
          OU = 07 0001 SHA256,
          OU = 03 0000000000000000 DEBUG,
          OU = 13 0001 IN_USE_SOC_HW_VERSION
```

That is the "metadata in the OU fields" arrangement the paper says MBNv5 used,
sitting in the image whose `w[1]` is 5. `[F]` The SM8250 leaf (w[1] = 6) has a
bare subject (`C=US, ST=California, CN=SecTools Test User, O=SecTools, L=San
Diego`) with **no** OU metadata fields — consistent with the spec's statement
that "the latest two new versions of the Signed Image Format (MBNv6 and MBNv7)
have moved this information into a standalone metadata field". `[F]` The QCM6490
leaf is likewise bare (`C=US, ST=California, O=SecTools, L=San Diego`), with the
metadata in the two 224-byte blocks instead (§3.5).

So the generational sequence is:

| MBN | `w[1]` | metadata location | observed on |
|---|---:|---|---|
| v5 | 5 | **leaf-cert OU fields** | SDM845 |
| v6 | 6 | standalone field, 168-B header, 120-B chain extension | SM8250 |
| v7 | 7 | standalone field, 64-B header + two 224-B signer blocks | QCM6490 |

### 3.3 Signature algorithm: a three-generation progression `[F]`

| tag | `w[1]` | signature alg (OID count) | public key | sig block | digest |
|---|---:|---|---|---:|---|
| SDM845 | 5 | `RSASSA-PSS` 1.2.840.113549.1.1.10 ×6 | RSA-2048 | 256 B | SHA-256 |
| SM8250 | 6 | `RSASSA-PSS` ×6 | RSA-2048 | 256 B | SHA-384 |
| QCM6490 | 7 | `ecdsa-with-SHA384` 1.2.840.10045.4.3.3 ×12 | EC P-384 (`secp384r1` ×6) | **104 B** | SHA-384 |

`[F]` All 12 certificates parsed with `openssl x509 -inform DER` confirm the
algorithm: SDM845 and SM8250 certs report `Signature Algorithm: rsassaPss` and
`Public-Key: (2048 bit)`; all six QCM6490 certs report `ecdsa-with-SHA384` and
`Public-Key: (384 bit)`. `[N]` No `sha256WithRSA` (1.2.840.113549.1.1.11) OID
appears in any of the three images.

This is the vendor spec's statement — "All devices supporting the new secure
boot format use ECDSA signatures using the NIST P384 curve. Older versions of
the Qualcomm Technologies secure boot architecture support RSA PSS and RSA
PKCS#1 v1.5 signature formats" — confirmed **on one partition name across three
SoCs**. `[F]` Note it also corrects a natural but wrong generalisation: SHA-384
does **not** imply ECDSA. SM8250 is SHA-384 **with RSA-2048 PSS**; only QCM6490
pairs SHA-384 with ECDSA.

`[I]` The 104-byte signature is DER ECDSA: `30 64 02 30 …` — a SEQUENCE holding
two 48-byte INTEGERs, 102 bytes of content, padded to the declared 104. This
matches the independent observation in `research/fleet/qdsp6sw-container.md`
§"102 bytes padded to the declared 104 with two `0x00`".

### 3.4 The legacy container closes exactly — and its "6400" rule does not generalise `[F]`

Both legacy images satisfy a 4-term closure:

| tag | base | `w[5]` hash | `w[7]` sig | `w[9]` certs | sum | `filesz` |
|---|---:|---:|---:|---:|---:|---:|
| SDM845 | 40 | 128 | 256 | 6,144 | **6,568** | 6,568 |
| SM8250 | 168 | 192 | 256 | 6,144 | **6,760** | 6,760 |

`[F]` `w[4] == w[5] + w[7] + w[9]` on both (6,528 and 6,592), and
`w[4] − w[5] == 6,400` on both — reproducing `pil-metadata-sweep.md` §4.

`[F]` **But MBNv7 breaks it.** QCM6490 has `w[4] = 224` and `w[5] = 336`, so
`w[4] − w[5] = −112`. The "`w[4]-w[5] = 6400 + 12800×(chains-1)`" rule recorded in
`pil-metadata-sweep.md` §4 and repeated in `qsee-crossgen.md` is therefore a
property of the **v5/v6 container only**, not of the hash segment as such. In
v7, `w[4]` no longer denotes "size after the hash table"; it denotes the
metadata-block region that precedes the table, and the table sits after it.

This is the same class of scope error the PSS note in `pil-metadata-sweep.md` §7
corrects for the signature OID: a rule that is true across all 28 swept images
but is not true of the format. `[I]` The general form is
`filesz = header + Σ(metadata blocks) + hash table + Σ(sig + certs)`, which
degenerates to the 4-term form when there is one metadata block and one chain.

### 3.5 MBNv7 layout: 14/14 arithmetic closure `[F]`

The QCM6490 metadata segment is 11,136 B and decomposes exactly:

| region | bytes | ends at |
|---|---:|---:|
| hash-segment header | 64 | 64 |
| QTI signer metadata | 224 | 288 |
| OEM signer metadata | 224 | 512 |
| hash table (`7 × 48`) | 336 | 848 |
| QTI signature (ECDSA P-384) | 104 | 952 |
| QTI certificate chain | 3,360 | 4,312 |
| OEM signature (ECDSA P-384) | 104 | 4,416 |
| OEM certificate chain | 3,360 | 7,776 |
| `0xFF` padding | 3,360 | **11,136** |

`[F]` `64 + 224 + 224 + 336 + 104 + 3,360 + 104 + 3,360 + 3,360 = 11,136` ==
`filesz`, exactly.

`[F]` Every boundary was verified against the bytes, not just the arithmetic:

- Hash table base is `64 + 224 + 224 = 512`, and 512 is the base that produces
  **5/7 digest hits** (§3.6) — no other base in 0…1,200 produces more.
- `seg[848:852]` is `30 65 02 31 00` — a DER SEQUENCE of length 101 holding a
  P-384 signature, i.e. the QTI signature at exactly the predicted offset.
- `seg[952:956]` is `30 82 02 72` — the first QTI certificate's outer SEQUENCE.
- `[F]` The QTI chain's last non-`0xFF` byte is at segment offset **2,902**, and
  the next non-`0xFF` byte after that is at **4,312** — exactly the predicted OEM
  signature offset. The gap 2,903…4,311 is pure `0xFF`.
- `seg[4312:4316]` is `30 64 02 30` — the OEM signature. `seg[4416:4420]` is
  `30 82 02 56` — the first OEM certificate.
- `[F]` The OEM chain's last non-`0xFF` byte is at **6,364**, and **every** byte
  from 7,776 to 11,136 is `0xFF`.

`[F]` The two signer metadata blocks are **224 bytes each and differ in exactly
6 bytes**:

| offset in block | QTI | OEM |
|---:|---|---|
| 8 | `00` | `01` |
| 136 | `00` | `0x89` |
| 137 | `00` | `02` |
| 140 | `00` | `01` |
| 220 | `0x5A` | `0x56` |
| 221 | `0x55` | `0x5A` |

`[I]` Byte 8 is a boolean that is 0 for the QTI block and 1 for the OEM block —
consistent with a "this block belongs to the OEM signer" flag, or the OEM-ID
binding the spec describes ("Whether the image is bound to an OEM chosen product
identifier"). Bytes 220/221 look like an end-marker or checksum pair. `[U]` The
remaining differing bytes are unassigned; I record the offsets rather than guess
their meaning.

`[F]` Each chain's capacity is 3,360 B but actual use is far lower: QTI 1,952 B
(slack 1,408), OEM 1,950 B (slack 1,410). `[F]` The `0xFF` tail is exactly one
more chain-capacity unit (3,360), so the segment is laid out as a whole number of
3,360-B slots.

### 3.6 Hash-slot semantics hold on the new variant `[F]`

Brute-forcing every base offset 0…1,200 against both digest widths, then reading
each slot:

| tag | alg | base | hits | zero slots | verdict |
|---|---|---:|---:|---|---|
| SDM845 | SHA-256 | 40 | 2/4 | slot1 (self), slot2 (`filesz` 0) | matches `pil-metadata-sweep.md` |
| SM8250 | SHA-384 | 168 | 2/4 | slot1 (self), slot2 (`filesz` 0) | matches `pil-metadata-sweep.md` |
| QCM6490 | SHA-384 | **512** | **5/7** | slot4 (`filesz` 0), slot6 (self) | **new** |

`[F]` On QCM6490 the five hit slots are phdr 0, 1, 2, 3, 5 — each digest equals
`SHA-384(segment[offset : offset+filesz])`. Slot 4 is `PT_GNU_EH_FRAME`-class
(`p_type` 7) with `filesz == 0` and `memsz == 3,061`, so it has no file content
to hash and its slot is zero. Slot 6 is the metadata segment itself, which cannot
hash itself, and its slot is zero.

This is the **same rule set** as the 28 swept images — zero slots occur exactly
at (a) the metadata segment and (b) segments with `filesz == 0` — extended to a
container whose base, signature size, and chain count are all different. `[F]`
`[N]` No SHA-256 digest of any QCM6490 segment appears anywhere in the image, so
the 224-byte `w[3]` field is not a second SHA-256 hash table; `w[3]` is the
signer-metadata block size (224 = 7 × 32), and `[U]` the coincidence that it
equals `phnum × 32` is recorded as an open question rather than a rule.

---

## 4. Fleet-level findings

### 4.1 One filename, eight vendors, five SoC generations `[F]`

The bucket is the cleanest case in the corpus for a "same partition, different
build" comparison: identical filename, identical `db_type`, identical `db_path`
leaf, 58 distinct md5 across 63 rows. Only 5 md5 values repeat, and each repeat
is a same-size pair of sibling devices:

| md5 | size | devices |
|---|---:|---|
| `e25f3c81…` | 450,560 | OnePlus_8, OnePlus_8_Pro |
| `67bf6455…` | 491,520 | OnePlus_7T, OnePlus_7T_Pro |
| `7a9edf0d…` | 491,520 | OnePlus_7, OnePlus_7_Pro |
| `af2ff75b…` | 3,739,648 | OnePlus_9, OnePlus_9_Pro |
| `a302bafa…` | 397,312 | Realme_9_Pro, Realme_10_Pro |

`[I]` These are shared-build pairs — sibling SKUs shipping the same hypervisor
binary. `[F]` One of them is independently confirmed by payload: `e25f3c81…` is
the md5 of the local `instantnoodle/hyp.img` I decoded (OnePlus 8 / 8 Pro share
the SM8250 build).

### 4.2 `hyp` is the hypervisor, and it carries the TZ version triple `[F]`

The version strings inside the payloads identify the component:

| tag | `QC_IMAGE_VERSION_STRING` | `IMAGE_VARIANT_STRING` | `OEM_IMAGE_VERSION_STRING` |
|---|---|---|---|
| SDM845 | `TZ.XF.5.0.1.C5-00083.1` | `WAXAANAAA` | — |
| SM8250 | `TZ.XF.5.8-00274` | `DARAANAAA` | — |
| QCM6490 | `TZ.XF.5.28.0-00021-LANAIAAAAANAZT-1` | `BAFAANAAA` | `be6181077ac3` |

`[F]` Each `hyp.img` carries its platform's **TZ** version triple, not a
hypervisor-specific one — the same `TZ.XF.*` string that the sibling `tz.img`
carries. This matches `pil-metadata-sweep.md` §6 ("hyp: carries its platform's
TZ version triple on both devices") and `trustzone-census.md` ("one TZ build
ships the OS and the hypervisor"). `[I]` QHEE and QTEE are built and signed as
one product line, which is why one version string covers both partitions.

`[F]` Only QCM6490 carries an `OEM_IMAGE_VERSION_STRING` (a 12-hex git-ish
identifier, `be6181077ac3`). The two older images carry none.

### 4.3 Segment shape changes with the container, not with the SoC `[F]`

| tag | `e_type` | entry | phnum | `PT_LOAD` segs | `PT_LOAD` filesz sum | file overhead |
|---|---|---:|---:|---:|---:|---:|
| SDM845 | 2 (`ET_EXEC`) | `0x85710000` | 4 | 1 | 384,336 | 12,976 |
| SM8250 | 2 (`ET_EXEC`) | `0x80040000` | 4 | 1 | 437,128 | 13,432 |
| QCM6490 | **3 (`ET_DYN`)** | **`0x80000000`** | **7** | 3 | 1,613,824 | 69,632 |

`[F]` The two legacy images are `ET_EXEC` with a single `PT_LOAD`; FP6 is
`ET_DYN` (PIE) with three `PT_LOAD` segments, one `PT_TLS`-class (`p_type` 2),
and one `PT_GNU_EH_FRAME`-class (`p_type` 7, `filesz` 0). This confirms
`trustzone-census.md`'s "DYN (PIE), entry 0x80000000, 7 phdrs" for FP6 and adds
the contrast: **the older `hyp.img` builds are non-PIE `ET_EXEC`.** `[I]` The
move to PIE coincides with the MBNv7 container and the ECDSA signature — all
three are properties of the same newer build system, but with n=1 new-generation
sample I cannot separate them.

`[F]` File overhead (`file size − Σ PT_LOAD filesz`) grows 12,976 → 13,432 →
69,632 B. On the legacy pair the overhead is essentially the metadata segment
(6,568 / 6,760) plus the `PT_NULL` header segment (288) plus page alignment. On
FP6 it is metadata (11,136) plus header segment (456) plus ~57 KiB of
page-alignment slack from three separately-aligned `PT_LOAD` segments.

### 4.4 The 8 MiB cluster is a partition-size artefact, not an image size `[I]`

11 Motorola rows are exactly 8,388,608 B = 2²³. Three observations:

1. `[F]` It is a **round power of two**, and the same value appears on 11
   different devices spanning SM4250 (460) through SM8550 (8 Gen2) — five SoC
   generations. Hypervisor binaries do not stay byte-identical in size across
   five generations while every other partition changes.
2. `[F]` On those 11 devices, `hyp` is the **only** 8 MiB row — no other
   subfamily on the same device shares the value (the one exception,
   `Edge_40_Pro`, has an unrelated 8 MiB `init_boot.img`).
3. `[F]` The documented FP6 case shows both numbers side by side:
   `docs/devices/fairphone/FP6/tz.md` line 50 records `hyp.img` as partition
   **8,388,608** but image **1,683,456** — and the actual payload I measured is
   1,683,456 B. The 8 MiB is the *partition*, the smaller number is the *image*.
   `[F]` The same doc records dubai/miami at 8,388,608 and FP4 at 409,600.

`[I]` The matrix's `size_bytes` for the 11 Motorola rows is therefore most
likely the **partition size** (a fixed 8 MiB `hyp` partition, zero-padded),
while the other 52 rows record the **image size**. This would make `size_bytes`
non-uniform in meaning *within a single subfamily* — a real comparability
hazard for anyone summing the bucket. It also means the bucket's 153,300,992 B
total mixes two units.

`[U]` I cannot prove this without a Motorola `hyp.img` payload, and none is on
disk (`[N]` no Motorola payload.bin or `hyp.img` exists in this workspace). What
would settle it: any Motorola `hyp.img` — if it is 8,388,608 B of which the tail
is a long zero run, the partition-size reading is confirmed; if it is a real
~500 KiB ELF padded to 8 MiB, same conclusion; if it is genuinely 8 MiB of
non-zero content, the reading is wrong.

`[F]` Supporting detail from the same subfamily: the 10 Motorola `Moto_G*`
devices at 520,192 B are also a repeated value (10 rows, one size) — plausible
as a shared build across a device family, which is the *other* explanation for
repeated sizes. The difference is that 520,192 is not a round power of two and
does not recur across five SoC generations.

---

## 5. `hyp` versus the rest of the boot chain `[F]`

`[F]` The bucket's `db_type` is `SECUREBOOT` on 63/63 rows, and `db_path` ends
`/radio` on 63/63. Both are consistent with the partition's role: `hyp` ships in
the radio/firmware image set alongside `tz`, `xbl`, `aop`, `devcfg`, and is
verified by the same secure-boot path.

`[F]` Every one of the 63 `hyp` devices also has `tz`-family rows, so `hyp` never
appears alone.

`[N]` `interface_documented` is `n` on all 63 rows, and remains `n` after this
issue. This document describes the **container and identity**, not a runtime
interface. The hypercall interface is documented elsewhere
(`research/qualcomm/docs/interface-gunyah.md`: Linux talks to QHEE over SMCCC
vendor-hyp hypercalls) but that document does not describe `hyp.img`'s bytes, and
I have not attempted to disassemble the payload. `[U]` A real interface
description — which SMCCC function IDs QHEE implements, what the segment at
`va=0xe00000` contains — is out of reach without an AArch64 disassembler and is
not claimed.

`[F]` `isa_identified` is `AArch64` on only 1 of 63 rows (FP6), yet all three
payloads I decoded are `e_machine == 183` (AArch64). The column is a
payload-verification record, not a claim about the rest; 62 rows are simply
un-RE'd. `[I]` Given the partition is Qualcomm-only across five generations and
all three samples are AArch64, AArch64 is near-certain fleet-wide, but I have not
verified it and do not upgrade the column.

---

## 6. What this adds to the existing record `[F]`

| finding | status before | status now |
|---|---|---|
| `w[1]` meaning | open item, `pil-metadata-sweep.md` §9 | **MBN format version**, proven from the cert CN `SRoT MBNv7 …` |
| `w[4]-w[5] = 6400` | stated as a rule for 28/28 | **v5/v6 only**; violated by MBNv7 (`−112`) |
| container forms | two (base 40/SHA-256, base 168/SHA-384) | **three**; adds base 512 / SHA-384 / 104-B ECDSA / dual chain |
| signature algorithms | PSS for all 28 swept | **three generations**: PSS → PSS → ECDSA P-384 |
| metadata location | not stated | **OU fields (v5)** → standalone 168-B (v6) → 64-B + 2×224-B (v7) |
| `hyp` fleet census | not documented | 63 rows / 63 devices / 153,300,992 B / 58 md5 |
| FP6 `hyp` md5 | recorded in matrix | **inconsistent with the payload**; sha256 matches, md5 does not |
| `Nord_CE3` `soc` cell | — | **`0xFF`-prefixed**, 506 rows fleet-wide |

---

## 7. Honest negatives `[N]`

- **No Motorola `hyp.img` payload exists in this workspace.** The 11-row 8 MiB
  cluster and the 10-row 520,192 B cluster are therefore census-only; the
  partition-size-vs-image-size question (§4.4) stays `[U]`.
- **No MediaTek, Exynos, Tensor or Apple device carries a `hyp` row.** The
  bucket is 100% Qualcomm across all 63 rows, so this document says nothing about
  non-Qualcomm hypervisors.
- **`isa_identified` remains blank on 62 of 63 rows.** I decoded three payloads,
  not 63. The column is not upgraded.
- **`interface_documented` remains `n` on 63/63.** No hypercall interface was
  documented; no disassembly was attempted (no AArch64 disassembler in this
  environment, and Xtensa/capstone limits are recorded elsewhere).
- **No SHA-256 digest of any QCM6490 segment appears in the image.** The 224-byte
  `w[3]` field is *not* a second hash table; I could not find any digest width
  other than 48 bytes matching on that image.
- **No `MBNv\d` string exists in the SDM845 or SM8250 images** (0 occurrences
  each), so the v5/v6 version identification rests on `w[1]` + the spec + the OU
  evidence, not on a literal string in those two files.
- **No `sha256WithRSA` OID in any of the three images** — the fingerprint-TA
  finding from `research/fleet/other-fingerprint.md` does not recur here.
- **The `0xFF` `soc` defect is recorded, not fixed.** I do not know which
  pipeline stage introduced it and did not modify the matrix.
- **Only one MBNv7 sample.** Every v7 claim (base 512, 104-B sig, dual chain,
  PIE) is n=1. It is not a fleet-wide generalisation and is labelled as such.
- **The 2,903→4,311 and 6,365→7,775 `0xFF` gaps are measured, not explained.**
  Cert-chain capacity is 3,360 B per chain and actual use is ~1,950 B; why the
  capacity is 3,360 rather than, say, 2,048 is `[U]`.

---

## 8. Rule 1 corrections applied in place `[F]`

Two claims in existing documents were wrong as written and are corrected where
they stand, rather than only contradicted here:

1. **`research/fleet/pil-metadata-sweep.md` §9** — the open item asking whether
   `w[1]` is a secboot metadata format version is now answered in place, with
   the evidence (the `SRoT MBNv7` certificate CN) and a pointer to this document.
2. **`research/fleet/pil-metadata-sweep.md` §4** — the
   `w[4]-w[5] = 6400 + 12800×(chains-1)` row and the paragraph presenting it as a
   fleet rule now carry a scope note: it holds on the 28 swept v5/v6 images and
   is violated by MBNv7, where the same field is `−112`.

`[F]` `research/fleet/qsee-crossgen.md` repeats the 6400 relation in its §3.2
comparison table; that table is explicitly scoped to "the AP-side images already
swept in `pil-metadata-sweep.md`", so it is not false and was **not** edited
(Rule 1 must not manufacture false corrections).

`[F]` `docs/REPO-STATE-MAP.md` has no `hyp` row — line 39 lists `tz` with
`dsp-tz-map.md` + `trustzone-census.md`, and line 53 lists `tz` with
`dsp-tz-map.md` + `qsee-crossgen.md`. A `hyp` row is added pointing at this
document.

---

## 9. Open items `[U]`

- **Which `size_bytes` unit do the 11 Motorola 8 MiB rows use?** Needs one
  Motorola `hyp.img` payload.
- **Is the FP6 md5 cell or the sha256 cell the wrong one?** The payload agrees
  with sha256; the md5 in the matrix is not the file's md5.
- **What do metadata-block bytes 136/137/140 and 220/221 mean?** Measured as
  differing between the QTI and OEM blocks; unassigned.
- **Why is the cert-chain capacity 3,360 B when use is ~1,950 B?** And why is the
  `0xFF` tail also exactly 3,360?
- **`w[0]`** remains image-specific (`4` on SDM845, `0` on the other two) with no
  assigned meaning — the same open item `pil-metadata-sweep.md` §9 carries.
- **`w[3] == phnum × 32` on QCM6490** (224 = 7 × 32) is exact but unexplained; it
  is also the signer-metadata block size, and with n=1 I cannot tell which is
  causal.
- **What is the segment at `va=0xe00000`** (`p_type` 1, `filesz` 385,024,
  `flags` 0x4 = read-only) in the FP6 image? `[I]` read-only, loadable,
  non-executable — plausibly the hypervisor's own rodata or a config blob.
- **Do any of these chains validate against retail fuse state?** Out of scope;
  requires boot-chain evidence beyond blobs.

---

## 10. Method `[F]`

Everything above was produced with stdlib Python only, run as `python3 -I`, plus
`openssl x509 -inform DER` for certificate parsing. No comments or docstrings in
the analysis source.

```python
# container decode: metadata segment = last PT_NULL with filesz > 0
phoff = struct.unpack_from('<Q', d, 32)[0]
phnum = struct.unpack_from('<H', d, 56)[0]
ph = [(struct.unpack_from('<I', d, phoff+i*56)[0],
       struct.unpack_from('<Q', d, phoff+i*56+8)[0],
       struct.unpack_from('<Q', d, phoff+i*56+32)[0],
       struct.unpack_from('<Q', d, phoff+i*56+40)[0]) for i in range(phnum)]
mi = [i for i in range(phnum) if ph[i][0] == 0 and ph[i][2] > 0][-1]
mo, ms = ph[mi][1], ph[mi][2]
```

```python
# base + digest width by brute force: no assumed layout
for width, alg in ((32, 'sha256'), (48, 'sha384')):
    dig = [hashlib.new(alg, d[o:o+f]).digest() if f else None for _, o, f, _ in ph]
    for base in range(0, min(ms, 1200)):
        hits = sum(1 for i, g in enumerate(dig)
                   if g is not None and d[mo+base+i*width:mo+base+(i+1)*width] == g)
```

Verification discipline: every arithmetic closure in §3.4 and §3.5 was checked
two ways — as an identity on the header words, and against the byte offsets
actually found in the segment (DER `30 82` walk, last-non-`0xFF` scan). The
`[F]` marker means both checks passed. Where only the identity holds and the byte
evidence is absent, the claim is marked `[I]` or `[U]`.

Census numbers come from a single `csv.DictReader` pass over
`upstream-contribution/blob-database/coverage-matrix.csv`, filtered on
`blob_subfamily == 'hyp'`; `tz`-family context uses `blob_family == 'tz'`.

Sources and access dates:

| source | retrieved |
|---|---|
| `coverage-matrix.csv` (repo, feat/open-device-site) | 2026-11-22 |
| `hyp.img` ×3 (local payloads, paths in §2) | 2026-11-22 |
| Qualcomm, *Secure Boot and Image Authentication — Technical Overview*, Joona Kannisto, © 2024 | 2026-11-22 |
| `github.com/quic/gunyah-hypervisor` (identity only) | 2026-11-22 |
| `github.com/TravMurav/Qcom-Secure-Launch` (QHEE role only) | 2026-11-22 |
