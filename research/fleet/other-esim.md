# `esim` — eUICC firmware images across the fleet (41 rows, 17 devices)

Analysis date: 2026-11-25. Analyst: OC-1 (`100milionseek`), issue
[#2054](https://github.com/adineo-cmd/open-device/issues/2054).

Inputs:
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows) for the
census; LineageOS device-tree `proprietary-files.txt` for `tokay`, `caiman`,
`komodo`, `comet`, `husky`, `shiba`, `oriole`, `raven`, `panther`, `cheetah`,
`felix`, `redfin`, `barbet` and `bramble` (fetched 2026-11-25) as an independent
corroboration of what each device actually ships; the XDA
`[GUIDE] Fix Pixel eSIM / eUICC` thread (published 2026-08-03, fetched
2026-11-24) and spwoodcock.dev's GrapheneOS write-up (2026-08-05, fetched
2026-11-24) for the updater's config-key table; GlobalPlatform
`GPC_SPE_134` "Open Firmware Loader for Tamper Resistant Secure Hardware v2.0"
(published 2023-10-09, fetched 2026-11-24) and ETSI TS 103 465 V15.2.0 for the
`OFL` term; and STMicroelectronics' `st54l`/`st54k` product pages
(fetched 2026-11-24) for the combo-chip architecture. Every number below is
command output. No payload is committed; samples are ≤16 bytes of hex.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** The `esim` bucket is the smallest but one of the most *regular*
subfamilies in the whole `other` family: 41 rows, 17 devices, 6 filenames,
**13 distinct payloads**. Every row is a Google Pixel, every row is filed under a
single directory convention (`…/priv-app/EuiccSupportPixel…`), and all 41 rows
carry `db_type=ESIM` — a string **no other row in the 33,917-row corpus uses**.

What makes it worth a note is that the payload is **per-platform, not
per-device**: 41 rows resolve to 13 md5 values, and every one of those 13 sizes
maps to exactly one md5. So the bucket is not 41 firmware images; it is 13, each
shipped on between 2 and 5 devices that share a platform.

The filename grammar decodes, and one token is a published standard rather than
a vendor invention: **`ofl` is GlobalPlatform's Open Firmware Loader** — a
mechanism for "loading firmware … into Tamper Resistant Secure Hardware
(typically an SE)". That is the single most useful result here, because it
identifies both the class of artifact and the correct standards family
(GlobalPlatform, not GSMA SGP.22) without opening the file.

The bucket also turns out to be **hardware-coupled to the `nfc` subfamily**: the
`-P23` suffix on the APK directory matches, **17 of 17**, the devices that carry
`st54l_fw.bin` in the `nfc` bucket, and the un-suffixed directory matches the
`st54j` set **9 of 9**. Since ST54L and ST54J are single-die NFC-controller +
secure-element parts, that is the expected architecture, and it means the two
subfamilies are describing one chip from two directions.

Two defects: the matrix files `Pixel_9_Pro` and `Pixel_9_Pro_Fold` as
**`Google Tensor G3`**, which is wrong on public record (the Pixel 9 family is
Tensor G4), and two Pixel 9-family devices have a blank `soc`. No payload is on
disk and no public source describes the `.img` container, so the byte-level
layout is `[N]`/`[U]` and is not claimed anywhere below.

---

## 0. Headline

1. **`[F]` The bucket is 41 rows / 17 devices / 6 basenames / 8,407,085 B,
   and 13 distinct payloads.** 0.1209% of the corpus's rows and 0.0120% of its
   bytes; 0.2736% of `other` rows and 0.0594% of `other` bytes. It is **#10 of
   13** `other` subfamilies by rows and **#9 by bytes** — below the 284-row /
   29,190,348-B subfamily median on rows, but only just below the median on
   bytes (8,407,085 B against a 29,190,348-B median).
2. **`[F]` Every row is Google, and `db_type=ESIM` is unique to this bucket.**
   All 41 rows have `vendor=google`. `db_type` takes 42 distinct values across
   the corpus, and `ESIM` appears on exactly these 41 rows — no other subfamily
   borrows it. Compare `misc`, where the matrix types 757 `.mdt` rows `ELF64`
   regardless of what they are.
3. **`[F]` 41 rows → 13 payloads, and the size↔md5 map is a bijection.** Six
   filenames carry 13 distinct `(size, md5_db)` pairs; the number of distinct
   sizes (13) equals the number of distinct md5 values (13) equals the number of
   pairs (13). `md5_db` is populated on **41 of 41** rows, so this is a complete
   result, not a sample. The payload is a function of *platform*, not device.
4. **`[F]` Three shipping shapes, not one ladder.** Devices ship 1, 3 or 4 of the
   six filenames, and the split is clean:
   - **1 file** (`esim-full-v1.img` only) — 8 devices: Pixel 4a 5G, 5, 5a,
     9, 9a, 9 Pro, 9 Pro Fold, 9 Pro XL.
   - **4 files** (`v0`, `v0-security`, `ofl-v1`, `v1`) — 6 devices: Pixel 6,
     6 Pro, 7, 7 Pro, 7a, Fold.
   - **3 files** (`v1`, `v1-m40`, `v1-m41`) — 3 devices: Pixel 8, 8a, 8 Pro.
5. **`[F]` `ofl` is GlobalPlatform's Open Firmware Loader.** `GPC_SPE_134`
   defines OFL as "a standardized mechanism for loading firmware (memory images
   which typically contain the Operating System …) into Tamper Resistant Secure
   Hardware (typically an SE)", with "cryptographic protection based on ECC" and
   a "multicast mode where one image can be used to update multiple TRSHs". So
   `esim-full-ofl-v1.img` is named for a *load path into a secure element*, not
   a version — which is why it coexists with `v0` and `v1` rather than replacing
   one of them. This is the only token in the grammar that resolves to a
   published specification, and it names the correct standards family for this
   bucket: GlobalPlatform, not GSMA SGP.22 (§4).
6. **`[F]` The `-P23` APK suffix is an exact predictor of the secure element.**
   The 8 devices shipping `EuiccSupportPixel-P23` are exactly the 8 devices
   carrying `st54l_*` in the `nfc` bucket; the 9 devices shipping the
   un-suffixed `EuiccSupportPixel` are exactly the 9 carrying `st54j_fw.bin`.
   **17 of 17, no exceptions either way.** ST54L is a single die integrating an
   NFC controller and a secure element, so the coupling is architectural.
7. **`[F]` Two SoC defects.** `Pixel_9_Pro` (59 rows) and `Pixel_9_Pro_Fold`
   (64 rows) are filed as `Google Tensor G3`; the Pixel 9 family is Tensor G4
   on public record. `Pixel_9A` (54 rows) and `Pixel_9_Pro_XL` (59 rows) have a
   blank `soc`. The corpus uses `Google Tensor G4` on exactly one device
   (`Pixel_9`, 59 rows), so the vocabulary exists and was not applied.
8. **`[N]` The container is not publicly described, and no payload is on disk.**
   Seven targeted searches found no format analysis; GitHub code search returns
   only ROM file manifests. I did not obtain a payload: the blobs live inside a
   multi-GB factory image, TheMuppets' `proprietary_vendor_google` branches stop
   at `lineage-19.1`, and LineageOS device trees list the files without carrying
   them. So every byte-level statement about `.img` is **not made**.

---

## 1. The bucket in numbers `[F]`

| quantity | value |
|---|---:|
| rows | 41 |
| devices | 17 |
| distinct basenames | 6 |
| distinct `md5_db` | 13 |
| distinct `(size, md5)` pairs | 13 |
| distinct `db_path` | 17 |
| bytes | 8,407,085 |
| vendors | 1 (`google`, 41/41) |
| `db_type` values | 1 (`ESIM`, 41/41) |
| `sha256_if_listed` populated | 0 / 41 |
| `isa_identified` populated | 0 / 41 |
| `interface_documented` = `n` | 41 / 41 |
| `priority` | P3 29, P2 12 |
| blank `soc` | 2 |

Row share of the corpus is 0.1209% and byte share is 0.0120% — a 10× gap, which
is the opposite of `misc` (12.18% of bytes on 31.61% of rows). The whole bucket
is 8.4 MB; the single largest file in it (2,259,554 B) is 26.9% of the bucket by
itself.

### 1.1 Rank inside `other` `[F]`

All thirteen `other` subfamilies, ordered by rows:

| # | subfamily | rows | bytes | devices | basenames |
|---:|---|---:|---:|---:|---:|
| 1 | `misc` | 10,720 | 8,498,193,635 | 119 | 1,988 |
| 2 | `camera` | 1,611 | 4,563,019,282 | 72 | 410 |
| 3 | `touch` | 880 | 516,418,690 | 71 | 125 |
| 4 | `media` | 470 | 29,190,348 | 53 | 40 |
| 5 | `audio` | 422 | 5,418,315 | 83 | 124 |
| 6 | `fastchg` | 315 | 36,989,007 | 28 | 40 |
| 7 | `fingerprint` | 284 | 387,540,764 | 33 | 9 |
| 8 | `oled` | 157 | 4,068,320 | 19 | 33 |
| 9 | `nfc` | 75 | 9,677,922 | 46 | 8 |
| **10** | **`esim`** | **41** | **8,407,085** | **17** | **6** |
| 11 | `sensors` | 5 | 86,541,968 | 5 | 1 |
| 12 | `tinysys` | 4 | 4,132,864 | 2 | 2 |
| 13 | `gpu-compute` | 3 | 2,523,240 | 3 | 1 |

`esim` ranks 10th on rows and 9th on bytes — it edges above `sensors` only
because `sensors` is five very large files. It sits *below* the medium row count
(284) but its 6 basenames make it the **second-narrowest namespace** in the
family after `gpu-compute` (1) and `sensors` (1), tied with `tinysys` (2). That
narrowness is the finding: 41 rows over 6 names is a tightly constrained
vocabulary, not a grab bag.

### 1.2 Six filenames, thirteen payloads `[F]`

| filename | rows | bytes | distinct `(size,md5)` |
|---|---:|---:|---:|
| `esim-full-v1.img` | 17 | 7,312,460 | **5** |
| `esim-full-ofl-v1.img` | 6 | 363,538 | 2 |
| `esim-full-v0-security.img` | 6 | 415,880 | 2 |
| `esim-full-v0.img` | 6 | 241,800 | 2 |
| `esim-full-v1-m40.img` | 3 | 43,668 | 1 |
| `esim-full-v1-m41.img` | 3 | 29,739 | 1 |

`esim-full-v1.img` is 87.0% of the bucket's rows-weighted byte total and carries
five different payloads across four generations — it is the only name that
appears in all three shipping shapes. The other five names are generation-locked.

### 1.3 Device coverage `[F]`

| device | rows | bytes | files shipped |
|---|---:|---:|---|
| Pixel_6 | 4 | 290,934 | `v0`, `v0-security`, `ofl-v1`, `v1` |
| Pixel_6_Pro | 4 | 290,934 | same |
| Pixel_7 | 4 | 199,838 | same |
| Pixel_7_Pro | 4 | 199,838 | same |
| Pixel_7a | 4 | 199,838 | same |
| Pixel_Fold | 4 | 199,838 | same |
| Pixel_8 | 3 | 49,411 | `v1`, `v1-m40`, `v1-m41` |
| Pixel_8A | 3 | 49,411 | same |
| Pixel_8_Pro | 3 | 49,411 | same |
| Pixel_4A_5G | 1 | 2,259,554 | `v1` |
| Pixel_5 | 1 | 2,259,554 | `v1` |
| Pixel_5A | 1 | 2,259,554 | `v1` |
| Pixel_9 | 1 | 19,794 | `v1` |
| Pixel_9A | 1 | 19,794 | `v1` |
| Pixel_9_Pro | 1 | 19,794 | `v1` |
| Pixel_9_Pro_Fold | 1 | 19,794 | `v1` |
| Pixel_9_Pro_XL | 1 | 19,794 | `v1` |

2.41 rows per device. The 17 devices are 17 of the 19 Pixels in the corpus —
the two absent are `Pixel_6A` and `Pixel_Tablet` (§5.2).

---

## 2. The filename grammar `[F]`

Six names, four independent axes:

```
esim-full-<stage>-<part>[-<config>].img
         └ v0 / v1        │        └ m40 / m41
                          └ ofl-v1, v0-security
```

Read the six strings as one vocabulary:

| name | stage | part | config | note |
|---|---|---|---|---|
| `esim-full-v0.img` | `v0` | — | — | base, v0 |
| `esim-full-v0-security.img` | `v0` | `security` | — | v0 with a security part |
| `esim-full-ofl-v1.img` | `v1` | `ofl` | — | v1 delivered by Open Firmware Loader |
| `esim-full-v1.img` | `v1` | — | — | base, v1 |
| `esim-full-v1-m40.img` | `v1` | — | `m40` | v1, config m40 |
| `esim-full-v1-m41.img` | `v1` | — | `m41` | v1, config m41 |

**The `v0`/`v1` pair is not a size ladder.** On Pixel 6, `v1` (139,023 B) is
larger than `v0` (3,236 B) by 135,787 B — a 43× ratio, consistent with v1 being
the whole image and v0 some small seed. On Pixel 7 the ordering **inverts**:
`v1` (20,489 B) is *smaller* than `v0` (58,832 B) by 38,343 B, and smaller than
`v0-security` (93,680 B) by 73,191 B and than `ofl-v1` (26,837 B) by 6,348 B. So
across the two generations that ship both, `v1` is the largest file on one and
the smallest on the other. **No arithmetic relation between v0 and v1 survives
both** `[F]`, which means the version number is not a content-volume proxy and
the payloads are independently built (§7).

**`m40`/`m41` are configs, not versions.** They appear only on the Pixel 8
generation, only alongside `v1`, and the three files do not partition the v1
size: `v1` = 24,942, `m40` = 14,556, `m41` = 9,913, and `m40 + m41` = 24,469,
which is **473 B short** of `v1`. So `v1` is not `m40 ‖ m41`; it is a third,
slightly larger artifact. The 473-B gap is `[U]` — it could be a header the
per-config files lack, but without the bytes that is not checkable `[N]`.

**`ofl` is a published standard, not a vendor token.** GlobalPlatform's
`GPC_SPE_134` defines the Open Firmware Loader as "a standardized mechanism for
loading firmware … into Tamper Resistant Secure Hardware (typically an SE)" (§4
quotes it in full). The same `OFL` abbreviation appears in ETSI TS 103 465's
glossary as "Open Firmware Loader". This is the **only** token in the six names
that resolves to a public specification, and it reframes the file:
`esim-full-ofl-v1.img` is a v1 image delivered through an OFL load path, which
is the natural reason for it to exist *beside* `v1` rather than instead of it —
though "delivered through OFL" is `[I]` from the name plus the spec, not
something I measured. What the OFL envelope adds in bytes is `[U]` — on Pixel 6,
`ofl-v1` (128,095) is 10,928 B *smaller* than `v1` (139,023), and on Pixel 7 it
is 6,348 B *larger* (26,837 vs 20,489), so the envelope is not simply additive
either `[F]`.

---

## 3. Payload identity is per-platform `[F]`

41 rows collapse to 13 payloads. Grouping by md5 gives the platform clusters
directly, and they align with public device generations:

| size | md5 (first 12) | devices | generation |
|---:|---|---:|---|
| 2,259,554 | `a0f35738893b` | 3 | Pixel 4a 5G / 5 / 5a |
| 139,023 | `2662cbe14e1a` | 2 | Pixel 6 / 6 Pro |
| 20,580 | `60788997fb0c` | 2 | Pixel 6 / 6 Pro |
| 128,095 | `801f8f27bbd1` | 2 | Pixel 6 / 6 Pro |
| 3,236 | `e347ceddbe09` | 2 | Pixel 6 / 6 Pro |
| 93,680 | `c541717efb98` | 4 | Pixel 7 / 7 Pro / 7a / Fold |
| 58,832 | `a6ba80e93e49` | 4 | Pixel 7 / 7 Pro / 7a / Fold |
| 26,837 | `b681ccc6b695` | 4 | Pixel 7 / 7 Pro / 7a / Fold |
| 20,489 | `4ba8547208b5` | 4 | Pixel 7 / 7 Pro / 7a / Fold |
| 24,942 | `8eef7aadcfcd` | 3 | Pixel 8 / 8a / 8 Pro |
| 14,556 | `eb32503c3af6` | 3 | Pixel 8 / 8a / 8 Pro |
| 9,913 | `5816a193bd03` | 3 | Pixel 8 / 8a / 8 Pro |
| 19,794 | `49aabb491ce0` | 5 | Pixel 9 family |

Two consequences worth stating plainly:

**No payload crosses a generation boundary.** Every md5's device set is confined
to one Pixel generation — the largest is 5 devices (Pixel 9 family) and the
smallest is 2. There is **0** md5 shared between, say, a Pixel 7 and a Pixel 8.
This is why 41 rows are 13 payloads rather than 41: the fleet ships one image per
generation, and the per-device rows are duplicates of a platform artifact.

**Size and md5 are in bijection.** 13 distinct sizes, 13 distinct md5, 13 pairs,
and no size maps to two md5s. So for this bucket, `size_bytes` alone identifies
the payload completely — the opposite of `misc`, where 10 `b00` values cover 502
groups and size carries shape but not identity. Careful, though: that bijection
is a property of *this* 13-member set, not a law. At 13 samples with all sizes
distinct, a bijection is what you would get from chance alone, and it says
nothing about how the format would behave on a 14th image.

---

## 4. `ofl` = Open Firmware Loader, and why that matters `[F]`

The prior-art search surfaced no format analysis, but it surfaced one dead-on
specification, and the file naming confirms it. GlobalPlatform publishes
**"Open Firmware Loader for Tamper Resistant Secure Hardware v2.0"**
(`GPC_SPE_134`, formerly `GPC_FST_134`, published 2023-10-09), whose own abstract
reads:

> The Open Firmware Loader (OFL) provides a standardized mechanism for loading
> firmware (memory images which typically contain the Operating System, but may
> also contain additional data like applets or file systems) into Tamper
> Resistant Secure Hardware (typically an SE). It defines the cryptographic
> protection based on ECC, the roles involved in firmware loading, and the
> administrative rights for the different operations. It also contains a
> multicast mode where one image can be used to update multiple TRSHs.

That description is almost a specification of this bucket:

- "memory images which typically contain the Operating System" — an `.img` that
  is a whole-firmware image, not a profile and not a filesystem.
- "into Tamper Resistant Secure Hardware (typically an SE)" — the target is the
  **secure element**, which §5 independently shows is the ST54L/ST54J die.
- "cryptographic protection based on ECC" — the image is expected to be
  cryptographically wrapped, which is why it would not look like a plain
  loadable blob.
- "multicast mode where one image can be used to update multiple TRSHs" — a
  documented OFL capability for shipping **one image to many devices**.

The terminology also appears in ETSI TS 103 465 V15.2.0's glossary, where `OFL` =
"Open Firmware Loader" sits alongside `IDS` = "Image Delivery Server" and `PPI` =
"Primary Platform Interface" — i.e. OFL belongs to the *firmware-delivery* half of
the eUICC standards family, distinct from profile delivery.

That distinction is the useful one, because eSIM work usually reaches for GSMA
SGP.22 and stops. SGP.22 governs **profiles** — subscription credentials
delivered from an SM-DP+ over ES9+/ES10 to an already-running eUICC. It says
nothing about replacing the eUICC's own firmware. Firmware replacement is the
IDS/OFL/PPI axis, which is GlobalPlatform, and which is exactly the axis these
six filenames live on. So the correct prior art to cite for this bucket is
GlobalPlatform, not GSMA — and the `ofl` token in the filename is the evidence.

What that gives us, and what it does not:

- It tells us the **class** of the artifact: `esim-full-ofl-v1.img` is a firmware
  memory image carried in an OFL load container, targeting the secure element,
  wired for an OFL PKI (X.509 in v2.0).
- OFL's "multicast" capability is a **tempting but unproven** explanation for the
  §3 result that one payload ships on up to five devices. The correlation is
  suggestive — one image, many targets is exactly the shape of multicast — but
  "the same platform ships the same vendor firmware" explains the same data
  with no spec at all. So the multicast link is `[U]`, and I am recording it as
  an hypothesis rather than dressing it as a finding.
- It does **not** give the byte layout of a Qualcomm- or ST-specific `.img`. OFL
  standardises the *mechanism* of loading — the roles, the ECC protection, the
  administrative rights — not the silicon vendor's on-media image format. Public
  OFL documentation does not describe ST54L's internal image layout. Hence §8 `[N]`.

---

## 5. The NFC coupling: one chip, two subfamilies `[F]`

### 5.1 `-P23` predicts the secure element 17 of 17 `[F]`

The `db_path` for every row ends in one of two APK directories —
`EuiccSupportPixel-P23` or `EuiccSupportPixel`. Crossing that against the secure
element each device carries in the `nfc` bucket:

| APK directory | devices | secure element in `nfc` | count |
|---|---:|---|---:|
| `EuiccSupportPixel-P23` | 8 | **ST54L** (`st54l_fw.bin`, `st54l_conf.bin`) | **8 / 8** |
| `EuiccSupportPixel` | 9 | **ST54J** (`st54j_fw.bin`) | **9 / 9** |

**17 of 17, with zero crossovers in either direction.** The P23 devices are
Pixel 8, 8a, 8 Pro, 9, 9a, 9 Pro, 9 Pro Fold, 9 Pro XL. The un-suffixed devices
are Pixel 4a 5G, 5, 5a, 6, 6 Pro, 7, 7 Pro, 7a, Fold.

This is not a coincidence of naming. STMicroelectronics describes **ST54L** as a
"single die integrating an NFC controller (contactless front-end - CLF) and a
secure element (SE)", and **ST54K** as integrating "an NFC controller, a secure
element and a UWB secure, fine-ranging subsystem host". An ST deck
(`CC_04_eSIM_and_NFC_for_Smarter_Connectivity.pdf`) lists the ST54L offering as
"NFC+eSE, NFC+eSIM and NFC+eSE+eSIM". So the eSIM secure element and the NFC
controller are the **same packaged die** on this generation, which is why the
eSIM image's directory name tracks the NFC part number exactly.

`research/fleet/other-nfc.md` §4.1 already established the `st54l`/`st54j` split
from the NFC side. This note establishes the same partition from the eSIM side
and finds it identical — the two subfamilies are describing one chip.

### 5.2 Two Pixels have NFC firmware but no eSIM image `[F]`

The corpus has 19 Pixels; 17 are in this bucket. The two absent:

| device | `nfc` files | `esim` rows | total matrix rows |
|---|---|---:|---:|
| `Pixel_6A` | `st54j_fw.bin` | **0** | 37 |
| `Pixel_Tablet` | — | **0** | — |

`Pixel_6A` is the interesting one: it carries an ST54J and 37 matrix rows, yet
ships no `esim-full-*.img`. The XDA config table independently separates it —
`Pixel 6a → P21 (ST54K)` while `Pixel 6 / 6 Pro → P21 (ST54K+ST33J)` — and notes
its menu entries are prefixed `GGL_B3_ST54K…`, a different prefix family from the
rest. So the 6a is a known outlier in the secure-element pairing, and its absence
from this bucket is consistent with that rather than a corpus gap `[I]`. Whether
it truly lacks the file or the extractor skipped it is `[N]` — I did not obtain
a 6a payload to check.

### 5.3 The matrix and the ROM trees agree 13 of 13 `[F]`

The matrix is a derived artifact, so the filenames were cross-checked against
LineageOS device-tree `proprietary-files.txt`, which lists what each ROM actually
extracts. Every device checked matched the matrix's filename set exactly:

| device (LineageOS tree) | files listed | matches matrix |
|---|---|---|
| `oriole`, `raven` | `v0`, `v0-security`, `ofl-v1`, `v1` | yes |
| `panther`, `cheetah`, `felix` | `v0`, `v0-security`, `ofl-v1`, `v1` | yes |
| `shiba`, `husky` | `v1`, `v1-m40`, `v1-m41` | yes |
| `tokay`, `caiman`, `komodo`, `comet` | `v1` | yes |
| `redfin`, `barbet`, `bramble` | `v1` | yes |

**13 of 13 devices agree**, and the trees also confirm the directory suffix
(`EuiccSupportPixel-P23` on `tokay`/`caiman`/`komodo`/`comet`/`shiba`/`husky`,
un-suffixed on the rest). So the matrix's `db_path` values reproduce the real
vendor layout, not a normalised approximation. This is the strongest external
check available without payloads.

---

## 6. Defects in the record `[F]`

### 6.1 `Pixel_9_Pro` and `Pixel_9_Pro_Fold` are labelled Tensor G3, and they are G4 `[F]`

The matrix assigns `Google Tensor G3` to two Pixel 9-family devices:

| device | `soc` in matrix | rows |
|---|---|---:|
| `Pixel_9` | `Google Tensor G4` | 59 |
| `Pixel_9A` | *(blank)* | 54 |
| `Pixel_9_Pro` | **`Google Tensor G3`** | 59 |
| `Pixel_9_Pro_Fold` | **`Google Tensor G3`** | 64 |
| `Pixel_9_Pro_XL` | *(blank)* | 59 |

Public record is unambiguous: the Pixel 9, 9 Pro and 9 Pro XL are "powered by the
fourth-generation Google Tensor system-on-chip, marketed as 'Google Tensor G4'"
(Wikipedia, *Google Pixel 9*, fetched 2026-11-25); the Pixel 9 Pro Fold is "powered
by the fourth-generation of Google's Tensor series of chips (marketed as 'Google
Tensor G4')" (*Pixel 9 Pro Fold*, same date); the Pixel 9a's infobox lists
`Google Tensor G4`. So **all five** Pixel 9-family devices are G4.

The corpus proves its own vocabulary was available: `Google Tensor G4` appears on
exactly one device (`Pixel_9`, 59 rows), and `Google Tensor G3` on four
(`Pixel_8`, 52; `Pixel_8A`, 54; `Pixel_8_Pro`, 52; and the two mislabelled 9s).
The two blank rows are a separate, milder defect — `Pixel_9A` and `Pixel_9_Pro_XL`
have no `soc` on any of their 54 and 59 rows.

This matters beyond bookkeeping: §3 groups payloads by platform, and a query that
filters `soc = 'Google Tensor G4'` would return only `Pixel_9` — silently dropping
4 of the 5 devices in the 19,794-B cluster, whose payload *is* the G4 one.

### 6.2 The `-P23` suffix does not mean "Pixel 8" `[F]`

An easy misreading, worth pre-empting because the matrix invites it. The eight
`-P23` devices split **3 Pixel 8 + 5 Pixel 9**, and the XDA config table assigns
them different keys — `Pixel 8 → P23 (ST54L)`, `Pixel 9 → P24 (ST54L)`. Both are
true because they are different namespaces:

- The **directory suffix** `-P23` is a *package* label. The ROM trees ship the
  same `EuiccSupportPixel-P23` APK on Pixel 8 and Pixel 9 alike (§5.3), so within
  the filesystem there is one P23 package spanning two generations.
- The **config key** `P24` is an *updater menu* label, visible only inside the
  running updater's dropdown, and it differs per generation.

So `-P23` on a Pixel 9 directory does **not** contradict `P24` in the updater;
they are two different identifiers that happen to share a number for the Pixel 8.
Anyone using `-P23` as a generation discriminator would mis-bin the five Pixel 9
devices. This is `[F]` for the directory side (ROM trees) and `[F]` for the
updater side (XDA + spwoodcock both give `P24` for `tokay`); that the two
namespaces are independent is `[I]` from those two observations.

---

## 7. What this adds to the existing record `[F]`

| prior note | what it says | what this note adds |
|---|---|---|
| `research/fleet/other-nfc.md` §4.1, §1.2 | `st54l_fw.bin` 8 rows / **1** md5 (261,825 B, one payload for every Pixel 8/9 device); `st54l_conf.bin` 8 rows / **8** md5; the ST54L/ST54J vendor split is disjoint by device | the **eSIM-side confirmation**: the same 8 devices are exactly the `-P23` set (17/17 with the 9 `st54j`), so the NFC split is reproduced from an independent subfamily |
| `research/fleet/other-misc.md` §4.3 | `gptauuid.xml` "describes partitions, not blobs", which is why it is `misc` and not `esim`/`tz` | keeps that boundary honest: `esim` is **blobs** — 13 firmware payloads — where `misc`'s `gptauuid.xml` is metadata. The two buckets do not overlap |
| `research/fleet/other-misc.md` §1.1, `other-camera.md` §1.1 | rank tables listing `esim` at 41 rows / 8,407,085 B | unchanged — both tables agree with §1.1 here, and this note is the detail behind that row |
| `docs/REPO-STATE-MAP.md` | no `esim` row | row added |

The `misc` cross-reference is worth keeping explicit: `other-misc.md` §4.3
excluded `gptauuid.xml` from `esim` on the grounds that it names partitions
rather than carrying payload. That call is vindicated here — every one of the 41
`esim` rows is an actual firmware image with its own md5, which `gptauuid.xml`
(63 partition names, 0 present as files) is not.

---

## 8. Honest negatives `[N]`

- **The `.img` container is not publicly described.** Seven searches
  (2026-11-25) returned no format analysis: `esim-full-v1.img format eUICC
  firmware image ST54L`; `GSMA eUICC firmware image format "esim-full"`;
  `ST54L ST54K eUICC firmware image format parser github`; `euiccpixel apk
  OtaUpdateMenu firmware image assets`; `"esim-full-v1-m40" OR
  "esim-full-v1-m41"`; `"GGL_P24_ST54L_GSMALIVE" firmware entry naming`;
  `esim-full "ofl" image open field load eUICC`. GitHub code search for
  `esim-full-v1.img` returns 509 hits and every one inspected is a ROM file
  manifest (`*-vendor.mk`, `proprietary-files.txt`), not a parser. Where the
  payload sits inside a factory image is covered by no note I could find.
- **No payload is on disk, so no header was read.** `find` over the workspace for
  `esim-full*` and `*EuiccSupport*` returns 0 files. Everything in §2–§3 is
  therefore derived from `size_bytes` and `md5_db`, which is a real but shallow
  evidence base: it establishes *which* payloads are distinct and *where* they
  ship, and says nothing about what is inside them.
- **A payload was judged not worth fetching, and I did not fake a decode.** The
  blobs live inside `EuiccSupportPixel.apk` inside a multi-GB Pixel factory
  image. `TheMuppets/proprietary_vendor_google` branches stop at `lineage-19.1`
  (no Pixel 8/9 trees), LineageOS device trees list the files but do not carry
  them, and `developers.google.com/android/images` no longer exposes direct
  `dl.google.com` factory URLs in its HTML. I chose to record the shallow result
  rather than present size-derived inference as format knowledge.
- **The `v1` vs `m40 + m41` gap (473 B) is unexplained.** It is a small, stable
  number across all three Pixel 8 devices, which makes it structural rather than
  noise, but what it contains is `[U]`.
- **`fallback_isdr_patch` is single-sourced.** A GrapheneOS forum post states
  that stack `D.2.0.23 / 20235` "contains a new service named
  `fallback_isdr_patch` in its newer `esim-full-v1.img`", absent from
  `D.2.0.22 / 20225`. I could not corroborate that string in any other source,
  and it does not appear in any of the six filenames here. Recorded as `[U]`,
  not as a component inventory.
- **`Pixel_Tablet` has 0 `esim` rows and 0 `nfc` rows in this corpus.** It is a
  Tensor G1 device and XDA's table does not cover tablets, so whether it ships
  the image at all is `[N]` — the corpus simply has no data.
- **No SHA-256 anywhere.** `sha256_if_listed` is empty on 41 of 41 rows, so
  cross-source payload identity cannot be checked beyond the md5 values already
  in the matrix.

---

## 9. Open items `[U]`

- **What is inside `esim-full-v1.img`?** The one public hint (a GrapheneOS forum
  post) names a service, `fallback_isdr_patch`, in one build. A 19,794-B payload
  is small enough that a header decode is plausible in a single session — if
  anyone obtains the APK. That is the highest-value follow-up and it needs a
  payload, not more matrix analysis.
- **Is `v0` a delta and `v1` a full image, or the reverse?** The sizes invert
  between Pixel 6 and Pixel 7 (§2), which rules out a simple "v1 ⊃ v0" reading
  but does not distinguish a delta from an independent build.
- **What are `m40` and `m41`?** They are config labels that appear only on
  Pixel 8 and do not partition `v1`. Whether they are region variants, carrier
  variants, or memory-layout variants is `[U]`.
- **Why is the 473-B `v1` surplus on Pixel 8?** Possibly a header that the
  per-config images omit; not checkable without bytes.
- **Does `Pixel_6A` genuinely lack the image?** It has an ST54J and 37 matrix
  rows but no `esim` row, and XDA gives it a distinct `GGL_B3_` prefix. Whether
  that reflects a hardware difference or an extraction gap is `[U]`.
- **What is the OFL envelope's byte cost?** It is `-10,928` on Pixel 6 and
  `+6,348` on Pixel 7 relative to bare `v1`, which is not consistent with a fixed
  wrapper. `[U]`.

---

## 10. Method `[F]`

Measurements are reproducible from the matrix with stdlib Python:

```python
# census and the payload bijection
rows = list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
e = [r for r in rows if r['blob_subfamily'] == 'esim']
sizes = {int(r['size_bytes']) for r in e}
md5s  = {r['md5_db'] for r in e}
assert len(e) == 41 and len(sizes) == 13 and len(md5s) == 13

# db_type=ESIM is used by this bucket and no other
assert {r['blob_subfamily'] for r in rows if r['db_type'] == 'ESIM'} == {'esim'}

# the -P23 <-> ST54L coupling
nfc = [r for r in rows if r['blob_subfamily'] == 'nfc']
st54l = {r['device'] for r in nfc if r['filename'].startswith('st54l')}
p23   = {r['device'] for r in e if r['db_path'].endswith('-P23')}
assert p23 == st54l                      # 8 == 8
assert {r['device'] for r in e} - p23 == \
       {r['device'] for r in nfc if r['filename'].startswith('st54j')} & {r['device'] for r in e}
```

Cross-checks that need the network are listed with their access dates in the
preamble: LineageOS `proprietary-files.txt` for 13 device trees (2026-11-25),
XDA and spwoodcock for the config-key table (2026-11-24), GlobalPlatform for
`OFL`, ST for the ST54L/ST54K architecture, and Wikipedia for the Pixel 9 SoC
(2026-11-25). Where a public claim and the matrix disagree, §6 says which is
wrong and on what evidence; where nothing is available, §8 says so.
