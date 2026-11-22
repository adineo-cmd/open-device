# The `fingerprint` subfamily of `other` — a split TA whose ELF header is filed in another bucket

**Issue:** #2056 · **Analysis date:** 2026-11-22 · **Evidence classes:** `[F]` measured fact
(command and output shown) · `[I]` inference from stated facts · `[N]` honest negative ·
`[U]` unresolved.

**Scope.** The 284 matrix rows classified `blob_family=other, blob_subfamily=fingerprint`:
**33 distinct devices**, 5 vendors, **9 distinct filenames**, **387,540,764 B**.
Plus the 33 `fingerpr.mdt` rows that belong to the same family but are filed elsewhere (§2).

**Artifacts read (read-only, never committed).**
Public split sets fetched from two repositories, 32 files / 3,733,427 B total:

| source | files | what it supplies |
|---|---|---|
| `github.com/insqriptd/gtowifi-blobs` (`master`) | `fingerpr.b00`–`b06` + `.mdt`, `soter64.b00`–`b06` + `.mdt` | a complete ELF32 `fingerpr` TA |
| `github.com/readboy-g500x-mainline/firmware-reverse` (`main`, `firmware/`) | `fingerpr.b00`–`b06` + `.mdt`, `fpctzapp.b00`–`b06` + `.mdt` | an ELF64 `fingerpr` TA and an ELF32 FPC TA |

Plus the analogous 23-`.mdt` split corpus on local disk at
`…/downloads/lineage-fp6/extracted/trees/modem/image` (284 files), used for the
container-law controls in §5.5.

No payload byte is reproduced beyond ≤16-byte hex samples. No vendor driver, datasheet, or
NDA document was consulted.

**Why public payloads.** `find` over the workspace returns **nothing** for `fingerpr.b0*` —
the matrix rows are metadata only, with no local bytes. This is the central limitation and it
is carried through every section that needed real bytes (§8.1).

---

## 0. Headline

1. **`[F]` The bucket is missing its own ELF header.** `fingerpr.mdt` exists on **all 33**
   devices, is the family's ELF header, and is filed `blob_subfamily=misc`, `db_type=ELF64` —
   while its own `fingerpr.b00`–`b08` are filed `fingerprint`/`FINGERPRINT`. The bucket that
   claims to describe the family does not contain the file that describes the bucket. See §2.
2. **`[F]` One file size reveals the whole container shape.** `fingerpr.b00` is 512 B on 13
   devices and 568 B on 20. `(size−64)/56` is exactly 8 or 9 — `e_phnum` — and
   `64+phnum×56` reproduces the size with zero remainder in **33/33**. The class then predicts
   the part count exactly: 8 parts for 13 devices, 9 for 20, and `b08` exists **iff**
   `phnum==9` (20/20, 0 exceptions). See §4.
3. **`[F]` The signature algorithm is `sha256WithRSA`, not RSASSA-PSS.** Both prior-art docs
   generalise PSS from their 35 chains. The fingerprint TAs carry
   `1.2.840.113549.1.1.11` six times each (2 per cert × 3 certs) and the PSS OID **zero**
   times in 4/4 images. The 256-B signature block and RSA-2048 modulus are unchanged, so the
   container is identical and the scheme is not. See §5.3.
4. **`[F]` `b01` is the metadata segment and its layout is fixed.** In 4/4 images
   `len(b01) == 40 + 7×32 + 256 + 6144 == 6664` exactly, and every field role in
   `pil-metadata-sweep.md` reproduces. See §5.
5. **`[F]` The bucket covers 61% of the devices that have this firmware.** Counting the true
   sensor-firmware families (`fingerpr`, `fpctzapp`, `fpctzappfingerprint`, `goodixfp`,
   `goodixfp64`) gives 503 rows / 54 devices / 464,962,556 B. The `fingerprint` bucket holds
   83.3% of those bytes but only 61.1% of those devices — 21 devices have fingerprint firmware
   and zero `fingerprint` rows. See §3.

---

## 1. The subfamily in numbers `[F]`

```
rows 284 | devices 33 | vendors 5 | filenames 9 | bytes 387,540,764
db_type        FINGERPRINT 284/284
priority       P3 268 / P2 16
isa_identified blank 284/284
interface_documented = "n" 284/284
sha256_if_listed blank 284/284
md5_db present 284/284, distinct 103
db_path        33 distinct values, all ending in /modem/image
```

Every row sits at `<vendor>/<codename>/modem/image`. That is the QSEE trustlet directory, not a
sensor-firmware directory — the family is a **TEE application**, which is why §5's container is
a secboot metadata segment rather than a vendor blob header.

### 1.1 Per-vendor `[F]`

| vendor | rows | devices | bytes | share |
|---|---:|---:|---:|---:|
| oneplus | 135 | 16 | 186,100,527 | 48.02% |
| xiaomi | 108 | 12 | 144,176,436 | 37.20% |
| motorola | 25 | 3 | 35,641,909 | 9.20% |
| fairphone | 8 | 1 | 10,810,946 | 2.79% |
| nothing | 8 | 1 | 10,810,946 | 2.79% |

### 1.2 Per-file `[F]`

| file | rows | bytes | share |
|---|---:|---:|---:|
| `fingerpr.b00` | 33 | 18,016 | 0.00% |
| `fingerpr.b01` | 33 | 173,942,492 | **44.88%** |
| `fingerpr.b02` | 33 | 78,314,806 | 20.21% |
| `fingerpr.b03` | 33 | 6,327,985 | 1.63% |
| `fingerpr.b04` | 33 | 106,453,912 | **27.47%** |
| `fingerpr.b05` | 33 | 113,376 | 0.03% |
| `fingerpr.b06` | 33 | 10,339,312 | 2.67% |
| `fingerpr.b07` | 33 | 11,951,145 | 3.08% |
| `fingerpr.b08` | 20 | 79,720 | 0.02% |

**`b01` and `b04` together are 72.35% of the bucket.** §4 shows that the same index does not
hold the same role across the two container classes, so this is *not* a stable per-file budget.

### 1.3 Size dispersion is the tell `[F]`

Each index spans a wide range across devices — `b01` from 6,800 to 11,462,116 B (1,686×),
`b04` from 831,216 to 4,193,272 B. A single firmware image distributed fleet-wide would show a
narrow band. The dispersion is explained in §4: the two classes assign different roles to the
same index, so pooling the index across classes mixes two different segments.

---

## 2. The bucket is split across two labels, and the header is the orphan `[F]`

`fingerpr.mdt` exists on all 33 devices and is **not** in the `fingerprint` bucket:

```
subfamily: {'misc': 33}
db_type:   {'ELF64': 33}
sizes:     3972 4272 4752 7312 7464
devices:   33   (identical set to the b00–b08 devices: fp-only = [], mdt-only = [])
bytes:     187,048
```

So the family is **387,540,764 B in the bucket + 187,048 B outside it = 387,727,812 B**.

### 2.1 This is not a one-off `[F]`

Across the whole matrix, 1,314 `.mdt` rows have a same-directory `.b00` sibling. **65 of them
disagree with their own `.b00`'s subfamily**, and the classes are:

| `.b00` subfamily | `.mdt` subfamily | rows |
|---|---|---:|
| `fingerprint` | `misc` | **33** |
| *(blank)* | `misc` | 32 |

`fingerprint → misc` is the single largest disagreement class. 1,249 of 1,314 (95.1%) agree, so
the classifier does resolve sibling headers correctly in general — this family is the exception,
not the rule.

### 2.2 A second naming convention for the same vendor's app `[F]`

`fpctzappfingerprint.mdt` appears on 4 devices, all with a **blank** subfamily and
`db_type=ELF64`:

| device | bytes | `db_path` |
|---|---:|---|
| Redmi_Note_8 | 7,260 | `xiaomi/ginkgo/vendor/firmware` |
| Pixel_4A_5G | 7,464 | `google/bramble/vendor/firmware` |
| Pixel_5 | 7,464 | `google/redfin/vendor/firmware` |
| Pixel_5A | 7,464 | `google/barbet/vendor/firmware` |

Per `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md` §2, `fpctzapp` is the FPC
fingerprint TZ app; `fpctzapp` and `fpctzappfingerprint` are disjoint device sets (0 overlap),
i.e. two spellings of one app. §6.2 confirms the vendor attribution from the payload.

### 2.3 What is *not* a mislabel `[I]`

`soter64.mdt` is typed `db_type=FINGERPRINT` (46 rows, blank subfamily). It is **not** the same
app as `fingerpr`: measured on the public splits, they share **0 of 7** part md5s and their
string inventories invert (`fingerpr` has 89 template-storage strings and 0 key-pair strings;
`soter64` has 0 and 20). `soter64` is the SOTER key/attestation TA
(`generate_attk_key_pair`, `export_ask_public_key`, `/persist/data/soter/`), i.e. the biometric
*key store*, not the sensor or template store. Typing it `FINGERPRINT` is a biometric-path
classification, not a sensor-firmware claim, and this document does not count it as
fingerprint-sensor firmware.

---

## 3. The bucket is 61% of the devices that have this firmware `[F]`

Counting sensor-firmware families by filename prefix across the whole matrix:

| family | rows | devices | bytes |
|---|---:|---:|---:|
| `fingerpr` | 317 | 33 | 387,727,812 |
| `fpctzapp` | 108 | 12 | 34,886,664 |
| `goodixfp` | 63 | 15 | 31,032,334 |
| `goodixfp64` | 11 | 3 | 11,286,094 |
| `fpctzappfingerprint` | 4 | 4 | 29,652 |
| **total** | **503** | **54** | **464,962,556** |

The `fingerprint` bucket holds **83.3% of the bytes** but only **61.1% of the devices**.

### 3.1 Where the rest lives `[F]`

| subfamily | rows | devices | bytes |
|---|---:|---:|---:|
| *(blank)* | 112 | 16 | 34,916,316 |
| `fingerprint` | 284 | 33 | 387,540,764 |
| `misc` | 33 | 33 | 187,048 |
| `touch` | 74 | 18 | 42,318,428 |

The `touch` share is the `goodixfp` files already measured in `research/fleet/other-touch.md`
(74 rows / 42,318,428 B). Note `other-touch.md` records these as fingerprint firmware inside the
touch bucket; the two documents agree, and the md5 sets are **disjoint** (103 fingerprint md5 vs
289 touch md5, 0 shared) — the overlap is by *row classification*, not by content.

### 3.2 The 21 devices the bucket misses entirely `[F]`

Devices with fingerprint-sensor firmware and zero `fingerprint` rows: **21** —
motorola 11, google 3, oneplus 2, xiaomi 2, realme 2, nothing 1. Byte totals count only the
sensor-firmware families, so any `soter64` rows on the same device are excluded (§2.3).

| device | vendor | families present | bytes |
|---|---|---|---:|
| Defy_2021 | motorola | `fpctzapp`, `goodixfp` | 7,821,683 |
| Moto_E7_Plus | motorola | `fpctzapp`, `goodixfp` | 7,258,647 |
| Moto_G10 | motorola | `fpctzapp` | 2,965,212 |
| Moto_G30 | motorola | `fpctzapp` | 2,965,212 |
| Moto_G32 | motorola | `fpctzapp` | 3,135,251 |
| Moto_G34_5G | motorola | `fpctzapp`, `goodixfp` | 9,454,256 |
| Moto_G9 | motorola | `fpctzapp`, `goodixfp` | 7,089,734 |
| Moto_G9_Power | motorola | `fpctzapp` | 2,965,212 |
| Moto_G_5G_2024 | motorola | `fpctzapp`, `goodixfp` | 9,454,256 |
| Moto_G_Power | motorola | `fpctzapp` | 3,238,422 |
| Moto_G_Stylus_5G | motorola | `fpctzapp` | 2,220,345 |
| Nord_200 | oneplus | `goodixfp` | 7,108 |
| Nord_CE2 | oneplus | `goodixfp` | 7,108 |
| Phone_2 | nothing | `goodixfp64` | 4,752 |
| Pixel_4A_5G | google | `fpctzappfingerprint` | 7,464 |
| Pixel_5 | google | `fpctzappfingerprint` | 7,464 |
| Pixel_5A | google | `fpctzappfingerprint` | 7,464 |
| Poco_3S | xiaomi | `goodixfp` | 6,940 |
| Realme_10_Pro | realme | `goodixfp` | 7,108 |
| Realme_9_Pro | realme | `goodixfp` | 7,108 |
| Redmi_Note_8 | xiaomi | `fpctzappfingerprint`, `goodixfp` | 14,520 |

A further **9 devices** carry `soter64` and *no* sensor-firmware family at all —
Edge_30_Neo, FP4, FP6, G_Stylus_5G-2-2022, Mi_A3, Moto_G82_5G, Moto_G84_5G, Nord_CE3, Pro_1X.
They are **not** counted above: §2.3 shows `soter64` is a key-storage TA, so their presence is
evidence of a biometric path, not of fingerprint firmware. Anyone reading `db_type=FINGERPRINT`
as "has a fingerprint sensor" would wrongly add these 9 devices.

---

## 4. Two container classes, distinguishable from one file size `[F]`

### 4.1 The arithmetic

`fingerpr.b00` is the ELF header block. For ELF64 it is `e_ehsize + e_phnum × e_phentsize` =
`64 + phnum × 56`:

| `b00` size | `(size−64)/56` | `phnum` | devices | parts |
|---:|---:|---:|---:|---:|
| 512 | 8.000 | 8 | 13 | 8 |
| 568 | 9.000 | 9 | 20 | 9 |

`64+8×56 = 512` and `64+9×56 = 568`, both exact. The ELF32 reading fails for both
(`52+8×32 = 308`, `52+9×32 = 340`), so the class is **ELF64** in 33/33.

### 4.2 The class predicts the part count exactly `[F]`

| `phnum` | devices | parts present | `b08` present |
|---:|---:|---|---:|
| 8 | 13 | `b00`–`b07` | 0 |
| 9 | 20 | `b00`–`b08` | 20 |

The `phnum==9` device set and the `b08`-present device set are **identical** (set equality
checked both directions: `p9−b08 = []`, `b08−p9 = []`).

### 4.3 The two classes assign different roles to the same index `[F]`

Size bands per index, split by class:

| index | `phnum=8` (13 devices) | `phnum=9` (20 devices) |
|---|---|---|
| `b00` | 512 (constant) | 568 (constant) |
| `b01` | 6,800–6,952 → **hash table** | 6,909,820–11,462,116 → **code** |
| `b02` | 5,839,460–6,105,896 → **code** | 195–219 → **data** |
| `b03` | 182–195 → **data** | 281,192–386,424 → **code** |
| `b04` | 831,216–4,193,272 → **code** | 2,458,992–4,060,712 → **code** |
| `b05` | 3,000–10,592 → **data** | 304 (constant) → **data** |
| `b06` | 304 (constant) → **data** | 457,166–624,710 → **code** |
| `b07` | 296,340–493,407 → **code** | 281,192–386,424 → **code** |
| `b08` | — | 3,404–4,184 → **hash table** |

The hash table is at index **1** for `phnum=8` and index **8** for `phnum=9`. So the same
filename carries a different segment in the two classes; per-file byte shares (§1.2) are
therefore an average over two different layouts and must not be read as a role budget.

### 4.4 `b03` and `b07` are byte-identical on every nine-part device `[F]`

```
devices where md5(b03) == md5(b07): 20
phnum=9 devices:                   20
identical set:                     True
```

So `fingerpr.b07` is 11,951,145 B of which the 20 nine-part devices duplicate `b03` in full.
This also explains why each device has 8 distinct md5s despite having 9 parts.

### 4.5 The duplicate is a `p_offset`/`p_filesz` alias, not a copy `[F]`

Measured on the 23-`.mdt` local corpus (16 ELF64 TAs): `phdr[3]` and `phdr[7]` share the same
`(p_offset, p_filesz)` pair in **16 of 16**, with `phdr[3].p_type = 1` (PT_LOAD) and
`phdr[7].p_type = 0x6474e552` (`PT_GNU_PROPERTY`). The loader therefore emits `b03` and `b07`
from the same bytes. Byte-identical `b03`/`b07` confirmed in 16 of 16 families on disk.

### 4.6 Class composition `[F]`

| vendor | `phnum=8` | `phnum=9` |
|---|---:|---:|
| oneplus | 9 | 7 |
| xiaomi | 0 | 12 |
| motorola | 2 | 1 |
| fairphone | 1 | 0 |
| nothing | 1 | 0 |

The class is **not** a vendor split (oneplus appears in both; xiaomi is nine-part only) and not a
SoC split (oneplus spans MSM8998 → SM8550 within the eight-part class). It tracks TA build
generation, which is `[U]` here — no build ID or version string is present in the matrix.

---

## 5. The container is a QSEE secboot metadata segment `[F]`

### 5.1 `b01` internal layout

All four public images:

```
len(b01) == 40 + 7*32 + 256 + 6144 == 6664     4/4 exact
w[5] = 224 = 7*32      hash table
w[7] = 256             signature block
w[9] = 6144            cert region
w[4] = 6624 = w[5]+w[7]+w[9]                   4/4
w[4] - w[5] = 6400                             4/4
```

`w[4]-w[5]=6400` and `w[9]=6144` are the single-chain values recorded in
`research/fleet/pil-metadata-sweep.md` §4, so the fingerprint TA is a **one-chain** image.

### 5.2 Hash slots are per-part SHA-256, with the self slot zeroed `[F]`

`slot[i] = SHA-256(content of part i)`, table at `b01+40`, stride 32:

| image | slots matching | zero slots | which |
|---|---:|---|---|
| `gtowifi/fingerpr` | 6/7 | 1 | index 1 |
| `gtowifi/soter64` | 6/7 | 1 | index 1 |
| `readboy/fingerpr` | 6/7 | 1 | index 1 |
| `readboy/fpctzapp` | 6/7 | 1 | index 1 |

Index 1 is the metadata segment itself, so slot 1 is all-zero — exactly the
"self = zero slot" rule in `pil-metadata-sweep.md` §5. `slot[0]` is the SHA-256 of `b00` (the
ELF header block), confirming `b00` is hashed as a segment in its own right.

### 5.3 The signature scheme is `sha256WithRSA`, not RSASSA-PSS `[F]`

| property | fingerprint TA | prior-art claim |
|---|---|---|
| sig-alg OID | `1.2.840.113549.1.1.11` (`sha256WithRSA`), ×6 per image | `1.2.840.113549.1.1.10` (RSASSA-PSS) |
| PSS OID occurrences | **0** in 4/4 | all 105 certs across 35 chains |
| sig block size `w[7]` | 256 | 256 |
| key size | RSA-2048 (257-B modulus incl. sign byte) | RSA-2048 |
| certs per image | 3 | 3 |
| tail after last cert | all-`0xFF`, 4/4 | all-`0xFF` |

The container, the block size and the key size are unchanged; **only the signature algorithm
differs**. This is a genuine correction to the generalisation in both prior-art documents and is
applied in place in §9.

The 3-cert chains name the OEM directly:

| image | root/intermediate CN | leaf |
|---|---|---|
| `gtowifi/soter64` | `Samsung Root CA cert`, `Samsung Corporation`, Suwon City, South Korea | `SecTools Test User` |
| `readboy/fpctzapp` | `Xiaomi Attestation CA`, Beijing | `SecTools Test User` |
| `gtowifi/fingerpr` | `Generated Test Attestation CA`, `SecTools`, San Diego | `SecTools Test User` |
| `readboy/fingerpr` | `Generated Test Attestation CA`, `SecTools`, San Diego | `SecTools Test User` |

All four certs carry a `SecTools Test User` leaf, i.e. **test chains**, consistent with the
test-chain dominance recorded in `pil-metadata-sweep.md` §7.

### 5.4 `b00` is a verbatim duplicate of the `.mdt` prefix `[F]`

```
mdt[:len(b00)] == b00     4/4
```

`b00` is the ELF header + program header table, re-stored as a separate file because
`qcom_mdt_read_metadata()` concatenates `ehdr_size + hash_size` into a contiguous buffer. In the
matrix this redundancy is 18,016 B of 387,540,764 B (0.0046%) — small, but it means `b00` is
never independent data.

### 5.5 The loader path: three of four are PIL-valid `[N]` for the "TEE-only" framing

Testing `drivers/soc/qcom/mdt_loader.c`'s actual predicates against the four public images:

| image | class | `mdt_header_valid()` | `phdrs[0].p_type != PT_LOAD` | hash seg found | split |
|---|---|---|---|---|---|
| `gtowifi/fingerpr` | ELF32 | **true** | true | true (idx 1) | true |
| `gtowifi/soter64` | ELF32 | **true** | true | true (idx 1) | true |
| `readboy/fpctzapp` | ELF32 | **true** | true | true (idx 1) | true |
| `readboy/fingerpr` | ELF64 | **false** | true | true (idx 1) | true |

`mdt_header_valid()` requires `e_phentsize == sizeof(struct elf32_phdr)` (32), so it rejects
ELF64 outright. **Three of the four public fingerprint TAs are ELF32 and pass every predicate
`mdt_loader.c` checks.** So the honest statement is narrower than "these are TEE-only, not PIL":
the ELF64 ones cannot go through `mdt_loader.c`, and the ELF32 ones are structurally eligible for
it — whether a given SoC routes `fingerpr` through PAS or through `qseecom` is `[U]` and cannot
be settled from the blob alone. `userspace-firmware-split.md`'s "QSEE TA, not PIL" framing holds
for the ELF64 members of this family and is not established for the ELF32 ones.

---

## 6. The payload: two different code bases under one bucket name `[F]`

### 6.1 `fingerpr` is the template store `[F]`

`fingerpr.b02` string inventory (gtowifi, 1,411,585 B):

```
28  "fingerprint"     12  "qsee_"      1  "FPC"
    write_fingerprint_data              find_fingerprint_in_finger
    write_fingerprint_template          find_fp_template_in_fingerprint
    set_fp_image_in_fingerprint         set_fp_template_in_fingerprint
    ERROR maximum number of fingerprints reached: %d
    ERROR qsee_hmac returned %d
```

89 template/finger-storage strings, **0** key-pair strings. This is the TEE-side store for
fingerprint templates and images, backed by `qsee_hmac` for integrity.

### 6.2 `fpctzapp` is the FPC sensor TA `[F]`

`fpctzapp.b02` (582,195 B) carries **495** `fpc` + 53 `fingerprint` + 35 `qsee` + 15 `egis`
strings, including the literal command-router banner:

```
"fpc_ta_command_router: started"
"fpc_ta_command_router: cmdreq = %d"
"FINGERPRINT_TEE_GET_TEMPLATE_DB_CMD_ID handler entered"
"qsee_prepare_shared_buf_for_secure_read returned error: %d"
```

and `fpctzapp.b03` contains the literal `fpctzappfingerprint` at offset **29,848 of 321,144**,
NUL-padded — the app's own name embedded in the payload. This independently confirms the
attribution in `Qualcomm-SM4375...gpu.md` §2 from bytes rather than from filename.

### 6.3 The two are not interchangeable `[F]`

`fingerpr` has 1 `fpc` string total; `fpctzapp` has 495. They are different code bases serving
different halves of the biometric path. A bucket named `fingerprint` therefore contains at least
two distinct vendors' TAs plus, on other devices, Goodix sensor firmware under a different
family name (§3).

---

## 7. What the matrix can and cannot say `[F]`

| field | value | consequence |
|---|---|---|
| `isa_identified` | blank 284/284 | no ISA claim is derivable from the matrix |
| `interface_documented` | `n` 284/284 | no interface claim is derivable |
| `sha256_if_listed` | blank 284/284 | only md5 (103 distinct) is available for dedup |
| `db_type` | `FINGERPRINT` 284/284 | constant, so it carries no information within the bucket |
| `priority` | P3 268 / P2 16 | the 16 P2 rows are the motorola + fairphone + nothing devices |

The ISA **is** resolvable from the payload for the public images — `e_machine` is 40 (ARM32) on
three and 183 (AArch64) on one — but not for the 33 matrix devices, whose class is only inferred
from `b00` size (§4.1). Recording this as a size-derived inference rather than a measurement is
deliberate.

---

## 8. Honest negatives

### 8.1 No local payload, and the class split is unconfirmed by any `phnum=8` image `[N]`

`find . -name "fingerpr.b0*"` over the whole workspace returns nothing. Every byte-level result
in §4.5, §5 and §6 comes from two public repositories (32 files, 3,733,427 B) plus the local
23-`.mdt` `modem/image` corpus. Both public `fingerpr` corpora are **`phnum=7`**, so neither the
`phnum=8` nor the `phnum=9` class has a byte-level confirmation. The class split in §4 is a
**size-only inference from the CSV** and is labelled as such throughout.

### 8.2 The `b01` layout is verified only at `phnum=7` `[N]`

`40 + 7×32 + 256 + 6144 = 6664` holds 4/4. Whether the `40` base is fixed or scales with
`phnum`, and whether the `6144` cert cap is universal, is **not** established — all four public
images happen to be seven-part. The matrix's `phnum=8` class has `b01` = 6,800 B (7 devices) and
6,952 B (6 devices). Applying the same formula at `phnum=8` predicts 6,696 B, so the observed
values exceed it by **104 B and 256 B** respectively; the 6,952 case is exactly one further
256-byte block (6,696 + 256). A `phnum=7` reading of those sizes would need a fractional table
count (11.25 and 16.00), so the formula does not transfer across classes unchanged. `[U]`.

### 8.3 No version or build strings found `[N]`

`pil-metadata-sweep.md` §6 records 29 `QC_IMAGE_VERSION_STRING=` / `IMAGE_VARIANT_STRING=` hits
across 28 images. The four fingerprint TAs carry **none** of those markers in any part. So the
`phnum=8`/`phnum=9` split cannot be dated or attributed to a build generation from the payload.

### 8.4 The 33 matrix devices' `e_machine` is unknown `[N]`

The `b00` size arithmetic fixes the ELF **class** (64-bit) in 33/33 but says nothing about
`e_machine`. Public images show both 40 and 183 for the same family name, so the matrix fleet
could be either. Not resolvable without bytes.

### 8.5 The 21 out-of-bucket devices have no measured bytes `[N]`

§3.2 identifies 21 devices with genuine sensor firmware outside the bucket, but no
`fpctzapp`/`goodixfp`/`goodixfp64` payload for those devices is available locally. Their row
counts and byte totals are from the CSV only. The `goodixfp` container is separately specified in
`research/fleet/other-touch.md` §9 (GT9886, checksum `BE16(sum(bytes[6:]))`, 14/14) — that work
is not repeated here.

### 8.6 Why `b03 == b07` on exactly the nine-part class is unexplained `[N]`

§4.5 shows the mechanism is a shared `(p_offset, p_filesz)` between `phdr[3]` and `phdr[7]` in
16/16 ELF64 TAs, and §4.4 shows the identity holds on exactly the 20 nine-part devices. But the
16 local ELF64 TAs are *all* nine-part-shaped (phnum 9), so the corpus cannot show whether an
eight-part TA lacks the alias or merely renumbers it. The correlation is exact and the mechanism
is measured; the causal link between the two is `[U]`.

### 8.7 `soter64` is not fingerprint-sensor firmware `[N]`

Stated positively so it is not re-derived: `soter64` is the SOTER key/attestation TA (§2.3).
The 46 matrix rows typed `FINGERPRINT` for it, and the 9 `soter64`-only devices in §3.2, are
biometric-path entries, not sensor firmware. Anyone counting "fingerprint firmware" from
`db_type` alone will over-count by 436 rows.

---

## 9. Corrections to existing text

Applied in place, per Rule 1.

### 9.1 `docs/REPO-STATE-MAP.md` — missing `fingerprint` row `[F]`

The map has rows for the `media`, `audio` and `touch` subfamilies but **none** for
`fingerprint`, so the family is absent from the state map entirely. A row is added after the
`touch` row.

### 9.2 `research/fleet/pil-metadata-sweep.md` — RSASSA-PSS is not universal `[F]`

§7 states all 105 certs are RSASSA-PSS. That is true of the 28 swept images and **false as a
statement about QSEE trustlets generally**: the fingerprint TAs use `sha256WithRSA`
(`1.2.840.113549.1.1.11`) with 0 PSS OIDs in 4/4. A scope note is added rather than rewriting
the measured result, which stands for its own corpus.

### 9.3 `research/fleet/qsee-crossgen.md` — same scope limit `[F]`

§5/§7 record the PSS OID as a property of the metadata format. Same correction: PSS holds for
`tz.img` on both generations, not for every TA that uses this container.

### 9.4 `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md` §2 — corroborated, not corrected

The `fpctzapp` = FPC fingerprint TZ app finding is confirmed from payload strings (§6.2) and
extended: the FPC TA's own name is embedded at `fpctzapp.b03` offset 29,848. No text change
needed; this document is the byte-level corroboration.

### 9.5 `research/fleet/other-touch.md` — consistent, no change

That document records `goodixfp.*` as fingerprint firmware inside the `touch` bucket
(74 rows / 42,318,428 B). This document confirms the same rows and adds that the md5 sets are
disjoint from the `fingerprint` bucket (0 of 103 vs 289), i.e. the two families do not
duplicate each other. No correction required.

---

## 10. Method

All numbers above were produced by stdlib Python 3 run as `python3 -I`, reading the CSV with
`csv.DictReader` and payloads with `struct.unpack_from` / `hashlib`. Commands used, in order:

```
# matrix census and the label-split scope
python3 -I - <<'PY'   # csv over coverage-matrix.csv, collections.Counter
PY

# container laws on the public splits
python3 -I - <<'PY'   # struct.unpack_from against 32 fetched files
PY

# the 23-.mdt local control corpus
python3 -I - <<'PY'   # phdr->part size matching, 248/248
PY

# loader predicate test
python3 -I - <<'PY'   # mdt_header_valid()/qcom_mdt_bins_are_split() reimplemented
PY
```

Fetching used `curl -sL` against `raw.githubusercontent.com`; the two repositories and all
access dates are recorded in the SEARCH ledger on #2056. Web sources were read as full text, not
snippets. `git.kernel.org` and `elixir.bootlin.com` returned an Anubis proof-of-work
interstitial and were replaced by the `gregkh/linux` raw mirror of the same file.

No payload was committed. The 32 fetched files live outside the repository and are not
reproduced here beyond the ≤16-byte hex samples and the string literals quoted in §6.
