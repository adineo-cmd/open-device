# `nfc` — NFC controller firmware across the fleet (75 rows, 46 devices)

Analysis date: 2026-11-22. Analyst: OC-1 (`100milionseek`), issue
[#2060](https://github.com/adineo-cmd/open-device/issues/2060).

Inputs:
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows) for the
census; two payloads already on disk from earlier sessions (Samsung `sec_s3nrn4v`
on FP6, NXP `sn100u` on `instantnoodle`); and the mainline
`torvalds/linux` NFC subsystem sources plus the LWN posting of
`[PATCH v4 0/6] nfc: s3fwrn5: support the S3NRN4V variant`
(retrieved 2026-11-22). Every number below is command output. No payload is
committed; samples are ≤16 bytes of hex.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** The `nfc` bucket is small — 75 rows, 46 devices, 0.221% of the
matrix rows and 0.0139% of its bytes — but it is unusually dense in vendors: its
**8 filenames resolve to three different silicon vendors** — Samsung
(`sec_s3nrn*`), STMicroelectronics (`st54*`) and NXP (`sn100u`) — and **no device
carries two of them**. Compare the other `other` subfamilies, which spread 33–125
filenames across their rows; `nfc` gets three vendors out of eight names. That
makes it a clean natural experiment in how three NFC controller families ship
firmware into an Android vendor tree.

The payoff is a **complete byte-level decode of the Samsung container**, which
turns out to be the `s3fwrn5` format that mainline already parses: 44-byte header,
two 128-byte signature blobs, then the image in 4096-byte sectors. The arithmetic
closes to the byte (`44 + 128 + 128 + 45×4096 = 184,620`) and the same rule
explains a **second, different Samsung part** (`sec_s3nrn82`, 151,852 B =
`44 + 128 + 128 + 37×4096`). Independently, the mainline kernel documents all
eight header fields in a comment block, and my decode — done before I found that
comment — agrees with it 8/8.

The bucket also carries two defects and one correction. `sn100u.bin` is NXP
**NFC** firmware filed under `db_type=AUDIO` on all 7 rows. `Galaxy_A21S` has
three **exactly duplicated** rows. And the prior-art interface note for FP6 says
the device has *no* NFC firmware file and that its controller identity is
`[OPEN]`; both statements are false against the file it cites (§8).

---

## 1. What the bucket contains `[F]`

| property | value |
|---|---|
| rows | **75** (72 after removing exact duplicates — §1.4) |
| devices | **46** |
| vendors | **6** |
| distinct filenames | **8** |
| total bytes | **9,677,922** |
| distinct `md5_db` | **35** |
| `db_type` | `NFC` **68**, `AUDIO` **7** |
| `blob_family` | `other` **75/75** |
| `blob_subfamily` | `nfc` **75/75** |
| `interface_documented` | `n` **72**, pointer to `interface-nfc.md` **3** |
| `isa_identified` | blank **75/75** |
| `sha256_if_listed` | blank **75/75** |
| `soc` | blank **32/75** |
| priority | `P3` 68, `P2` 4, `P1` 3 |

Unlike `hyp` (`research/fleet/tz-hyp.md`, one filename, one `db_type`, one path
leaf), this bucket is heterogeneous on every axis except family and subfamily.
There is no single file to describe; there are eight, from three vendors, in two
different directory conventions.

The two blank columns are worth stating plainly: **no row in this bucket has an
ISA** and **no row has a SHA-256**. Whatever ISA claims eventually get made here
will come from payload work, not from the matrix.

### 1.1 Position inside `other` `[F]`

| metric | value |
|---|---|
| `nfc` rows / all matrix rows | 75 / 33,917 = **0.221%** |
| `nfc` bytes / all matrix bytes | 9,677,922 / 69,797,539,502 = **0.0139%** |
| rank by rows among the 13 `other` subfamilies | **9th** |
| rank by bytes among the 13 `other` subfamilies | **8th** |

For scale: `misc` is 10,720 rows and 8.50 GB; `camera` is 1,611 rows and 4.56 GB
(both decimal GB). `nfc` is 9.23 MiB — **878× smaller than `misc` by bytes**, not
three orders of magnitude. It ranks above `esim` (41 rows), `sensors` (5),
`tinysys` (4) and `gpu-compute` (3) by rows, and above `esim`, `audio`, `tinysys`,
`oled` and `gpu-compute` by bytes.

### 1.2 Three silicon vendors, disjoint by device `[F]`

| silicon vendor | filenames | rows | devices | bytes | share of bucket bytes |
|---|---|---:|---:|---:|---:|
| Samsung | `sec_s3nrn4v_firmware`, `sec_s3nrn4v_hwreg`, `sec_s3nrn4v_swreg`, `sec_s3nrn82_firmware` | 38 | 17 | 3,129,464 | 32.34% |
| STMicroelectronics | `st54j_fw`, `st54l_fw`, `st54l_conf` | 30 | 22 | 5,116,832 | 52.87% |
| NXP | `sn100u` | 7 | 7 | 1,431,626 | 14.79% |

`[F]` **No device carries more than one of the three.** 46 devices = 17 + 22 + 7
exactly, with no overlap. So vendor choice here is a per-device decision, not a
per-SoC or per-Android-version one.

`[F]` It is also not an SoC-vendor proxy. The Samsung parts appear on
**Qualcomm** devices (15 rows with a `Qualcomm …` `soc`), the STMicro parts on
**Google Tensor** devices (19 rows) and Qualcomm devices (3 rows), and NXP on
Qualcomm devices (6 rows). The NFC controller is a discrete part sourced
independently of the application processor.

### 1.3 Device coverage `[F]`

Rows per device: 29 devices carry 1 row, 8 carry 2, 8 carry 3, and 1
(`Galaxy_A21S`) carries 6.

The 3-row pattern is a coherent triple — firmware + `hwreg` + `swreg` — and it is
how **8 of the 46 devices** ship: FP6, `Galaxy_S20_FE`, and all six Motorola
devices (`fogos`/`hawao`/`denver`/`rhode`/`rhodep`/`bangkk` = Moto_G34_5G, G42,
G52, G82_5G, G84_5G, G_Stylus_5G). `Galaxy_A21S` carries the same triple **twice
over** — 6 rows for 3 files (§1.4).

The 2-row pattern is the `st54l_fw` + `st54l_conf` pair on the eight Pixel 8/9
family devices. Everything else is a lone firmware file.

`[F]` So **17 of 46 devices are multi-file**, and the two modules split cleanly by
vendor: 9 Samsung `s3nrn4v` devices (firmware + register pair) and 8 STMicro
`st54l` devices (firmware + config). No other device carries more than one NFC
file, which includes every NXP device and every `st54j`/`s3nrn82` device.

### 1.4 Three exactly duplicated rows `[F]`

`Galaxy_A21S` contributes 6 rows that are really **3** — each of its three
filenames appears twice with all 14 columns identical:

| filename | rows | md5 |
|---|---:|---|
| `sec_s3nrn4v_firmware.bin` | 2 | `0937a0da…` |
| `sec_s3nrn4v_hwreg.bin` | 2 | `ea9eda9f…` |
| `sec_s3nrn4v_swreg.bin` | 2 | `e0967bb7…` |

`[F]` This is not an `nfc`-specific artefact. The whole 33,917-row matrix holds
**46 rows that are exact 14-column duplicates**, and `nfc` supplies **3 of
them**. By subfamily the duplicate surplus is `misc` 30, unlabelled 11, `nfc` 3,
`modem-config` 1, `audio` 1.

So the honest row count is **72 unique rows / 46 devices**, and every percentage
in this document is computed on the 75-row form as the matrix publishes it, with
the duplicate caveat attached. I did not modify the matrix to deduplicate it —
that is a corpus-wide decision, not a per-issue one (§9).

### 1.5 Two directory conventions `[F]`

| `db_path` leaf | rows |
|---|---:|
| `firmware` | 44 |
| `nfc` | 17 |
| `etc` | 14 |

The three conventions map onto the manufacturers:

- **Samsung** puts the firmware under `vendor/firmware/nfc/` and the two register
  images under `vendor/etc/nfc/` — the `nfc` leaf is Samsung-only (17 rows).
- **Motorola and Fairphone** (same Samsung silicon) put the firmware in plain
  `vendor/firmware/` and the register images in plain `vendor/etc/` — no `nfc`
  subdirectory at all.
- **Google, OnePlus and Xiaomi** put everything in plain `vendor/firmware/`.

`[F]` This is why the `db_path` leaf is a bad key for this bucket: the *same*
Samsung part is filed `vendor/firmware/nfc` on Samsung devices and
`vendor/firmware` on Motorola devices. Nothing about the file changes; only the
OEM's packaging convention does.

---

## 2. The payload set `[F]`

The full per-filename table, from a single `csv.DictReader` pass:

| filename | rows | devices | sizes | distinct md5 | vendors |
|---|---:|---:|---|---:|---|
| `st54j_fw.bin` | 14 | 14 | 195,560 / 219,688 / 219,952 | 3 | google 10, xiaomi 4 |
| `sec_s3nrn4v_firmware.bin` | 11 | 10 | 184,620 | **5** | motorola 6, fairphone 1, samsung 4 |
| `sec_s3nrn4v_hwreg.bin` | 10 | 9 | 3,232 | **8** | motorola 6, fairphone 1, samsung 3 |
| `sec_s3nrn4v_swreg.bin` | 10 | 9 | 336 | **6** | motorola 6, fairphone 1, samsung 3 |
| `st54l_fw.bin` | 8 | 8 | 261,825 | **1** | google 8 |
| `st54l_conf.bin` | 8 | 8 | 2,142 | **8** | google 8 |
| `sec_s3nrn82_firmware.bin` | 7 | 7 | 151,852 | 2 | samsung 7 |
| `sn100u.bin` | 7 | 7 | 204,518 | 2 | oneplus 7 |

`[F]` All eight filenames are **nfc-only**: none appears under any other
`blob_subfamily`. Conversely there are **0** rows in the matrix with
`db_type=NFC` outside this subfamily. The bucket and the type agree exactly,
except for the 7 `sn100u.bin` rows — the `AUDIO` defect in §4.2.

### 2.1 Two payloads exist on disk `[F]`

| payload | path (workspace) | bytes | md5 |
|---|---|---:|---|
| `sec_s3nrn4v_firmware.bin` | `…/lineage-fp6/extracted/trees/vendor-firmware/` | 184,620 | `e0bde9905c681de2255e29206ce35f9f` |
| `sn100u.bin` | `…/data-fetch/second-device/instantnoodle/tree-vendor/firmware/` | 204,518 | `78497dde174ed97a77798a526534e286` |

`[F]` The FP6 file's **sha256** is
`407a4d07e712397d72b178c93198f83ec55eb3f3afe006be1ef9c42534281e83`, which is
exactly the short hash `407a4d07e712397d` that
`research/qualcomm/results/census.md` line 697 records for this path. The census
short hash is therefore a **sha256 prefix**, not an md5 — a distinction the
interface note got backwards (§8).

`[F]` `sec_s3nrn4v_hwreg.bin` and `sec_s3nrn4v_swreg.bin` are **not** on disk.
Only the firmware file was extracted for FP6. The register images are
census-only here and are not decoded (§7).

### 2.2 The FP6 matrix row and the FP6 payload disagree `[F]`

The 11 `sec_s3nrn4v_firmware.bin` rows are all 184,620 B but carry **5 distinct
md5**:

| md5 | rows | devices |
|---|---:|---|
| `6bc45226…` | 4 | Moto_G42, Moto_G_Stylus_5G, Moto_G52, Moto_G82_5G |
| `dbe509cb…` | 2 | Moto_G34_5G, Moto_G84_5G |
| `f92752bd…` | 2 | Galaxy_F62, Galaxy_S20_FE |
| `0937a0da…` | 2 | Galaxy_A21S (the duplicate pair) |
| `f2be6a09…` | 1 | **FP6** |

`[F]` The FP6 row's md5 is `f2be6a09…`. The payload on disk is `e0bde990…`. They
differ. The sha256 matches the census exactly, so **the file is the FP6 file**;
the matrix's md5 cell for that row does not describe it.

This is the same shape of defect #2065 found for `hyp` on FP6 (`tz-hyp.md` §2.1):
one cell wrong while the other agrees. Here the *census* row is right and the
*matrix* md5 cell is wrong. I recorded it and did not edit the matrix (§9).

The consequence matters for the whole filename: **size cannot identify this
file.** Five different builds share 184,620 B exactly, because the container
size is quantised by the sector count — a build that changes code but not sector
count keeps the size. That is a structural property, not a coincidence, and it is
why `size_bytes` is a weak key for this bucket (§4.1).

### 2.3 `sn100u.bin` is opaque `[F]`

| measurement | value |
|---|---|
| bytes | 204,518 |
| md5 | `78497dde174ed97a77798a526534e286` |
| Shannon entropy | **7.9957 bits/byte** |
| chi-square vs uniform (df 255) | **1,414.5** (uniform expectation ≈255) |
| byte histogram range | max 1,538, min 726, expected 798.9 |
| repeated 16-byte blocks | **0** |
| ELF magic | absent |
| `0xFF` run | none |
| gzip / xz / zlib / bzip2 / lz4 / zstd magic | none at offset 0 |

`[F]` 7.9957 bits/byte with zero repeated 16-byte blocks and a chi-square an
order of magnitude above uniform means the image is **encrypted or compressed
with no recoverable structure**. There is no header, no magic, no padding, no
sector alignment.

`[F]` The maximum-entropy reading is consistent with the driver: mainline
`drivers/nfc/nxp-nci/firmware.c` treats the file as an **opaque byte stream**.
It never parses a header — it wraps the stream in `0xC0 WRITE` chunks with a
CRC-CCITT over each chunk, and it uses `0xF1 GETVERSION` / `0xE0 CHECKINTEGRITY`
to let the *controller* validate. So there is nothing for a host-side parser to
find, by design.

This is an honest negative, not a failed analysis: **the file is not decodable
without the controller or a key, and no amount of static work here would change
that.** I record the measurement and stop (§7).

---

## 3. The Samsung container, decoded `[F]`

This is the substantive result of the issue. The FP6 payload
`sec_s3nrn4v_firmware.bin` (184,620 B) is a `s3fwrn5`-format image.

### 3.1 The kernel specification, and 8/8 field agreement `[F]`

`torvalds/linux` `drivers/nfc/s3fwrn5/firmware.c` carries a comment block that is
a complete byte-level specification of the container:

```
0x00 - 0x0B : Date and time string (w/o NUL termination)
0x10 - 0x13 : Firmware version
0x14 - 0x17 : Signature address
0x18 - 0x1B : Signature size
0x1C - 0x1F : Firmware image address
0x20 - 0x23 : Firmware sectors count
0x24 - 0x27 : Custom signature address
0x28 - 0x2B : Custom signature size
#define S3FWRN5_FW_IMAGE_HEADER_SIZE 44
```

`[F]` I decoded the payload **before** locating this comment, by walking the
`(offset, size)` pairs at `0x14` upward. Every field agrees:

| offset | field | decoded value | kernel spec |
|---|---|---|---|
| `0x00–0x0B` | date | `202509010445` (ASCII, 12 B, all digits) | date/time string, no NUL |
| `0x0C–0x0F` | — | `ffffffff` | unlisted (gap) |
| `0x10–0x13` | version | `0x020b0065` | firmware version |
| `0x14–0x17` | `sig_off` | **44** | signature address |
| `0x18–0x1B` | `sig_size` | **128** | signature size |
| `0x1C–0x1F` | `img_off` | **300** | image address |
| `0x20–0x23` | `img_sectors` | **45** | sectors count |
| `0x24–0x27` | `csig_off` | **172** | custom signature address |
| `0x28–0x2B` | `csig_size` | **128** | custom signature size |

`[F]` The struct in `firmware.h` matches too: `char date[13]` (12 bytes copied
plus a forced `'\0'`), `u32 version`, `const void *sig`, `u32 sig_size`,
`const void *image`, `u32 image_sectors`, `const void *custom_sig`,
`u32 custom_sig_size`. And the parser `s3fwrn5_fw_request_firmware()` reads each
field at exactly the offsets above, refusing the file if
`size < S3FWRN5_FW_IMAGE_HEADER_SIZE`.

`[F]` The version field is **byte-reversed relative to the field order**, which
is why it is worth writing down: the four bytes on disk are `65 00 0b 02` and the
little-endian `u32` at `0x10` is `0x020b0065`. The driver's
`s3fwrn5_fw_check_version()` compares it as a struct of four bytes —
`major`, `build1`, `build2`, `target` — so `0x65 / 0x00 / 0x0b / 0x02` is
`major=0x65, build1=0x00, build2=0x0b, target=0x02`. I label that `[F]` for the
byte values and `[U]` for what each nibble means.

### 3.2 Arithmetic closure: exact, and it predicts a second part `[F]`

```
44 (header) + 128 (sig [44,172)) + 128 (custom sig [172,300)) + 45×4096 (image [300,184620))
  = 184,620 = file size exactly
```

`[F]` `45 × 4096 = 184,320 = 184,620 − 300`, so the image runs from `0x12C` to
EOF with no tail. This is the same two-way check #2065 used on `hyp`: an identity
on the header words *and* the byte offsets actually present.

`[F]` The rule generalises to a **different Samsung part**. `sec_s3nrn82_firmware.bin`
is 151,852 B on all 7 rows, and

```
300 + 37×4096 = 151,852  exactly
```

`[F]` No other candidate prefix closes on both files. Testing every plausible
prefix (`4`, `44`, `172`, `300`, `344`) against every size in the bucket, only
**`300`** yields exact multiples, and only for these two files:

| size | `size − 300` | `/4096` | closes? |
|---|---:|---:|---|
| 184,620 | 184,320 | **45.000** | yes (`s3nrn4v`) |
| 151,852 | 151,552 | **37.000** | yes (`s3nrn82`) |
| 3,232 | 2,932 | 0.716 | no (`hwreg`) |
| 336 | 36 | 0.009 | no (`swreg`) |
| 204,518 | 204,218 | 49.858 | no (`sn100u`, NXP) |
| 195,560 | 195,260 | 47.671 | no (`st54j`) |
| 219,688 | 219,388 | 53.562 | no (`st54j`) |
| 219,952 | 219,652 | 53.626 | no (`st54j`) |
| 261,825 | 261,525 | 63.849 | no (`st54l`) |
| 2,142 | 1,842 | 0.450 | no (`st54l_conf`) |

So the `300 + N×4096` law holds on **2 of 2** Samsung firmware files and on
**0 of 6** non-Samsung files. It is a real vendor-container invariant, not a
numerological hit.

`[F]` The sector size is a *bootloader-reported* value, not a constant. The
driver reads it from `GET_BOOTINFO` (`bootinfo.sector_size`) and computes
`image_size = sector_size × image_sectors`. 184,320 is divisible by 256, 512,
1024, 2048 **and** 4096 (giving 720/360/180/90/45) but **not** by 8192 or 16384.
So `4096` is the **largest** power-of-two sector size that closes for this file,
which is consistent with the quantisation but not proof of the value on silicon —
that would need the chip's `GET_BOOTINFO` reply. `[I]` 4096.

`[F]` One capacity cross-check: 184,320 B = **180 KiB**, which is **93.8%** of a
192 KiB flash (**196,608 B**), leaving **12,288 B = 12 KiB** spare. Samsung sells
this part as "S3NRN4V (192K)", so a 180 KiB image fits the marketed capacity with
6.25% headroom. `[I]` That is a plausible fit rather than proof: a part's usable
flash need not equal its marketing capacity.

### 3.3 Inside the image: Thumb code, an NDEF AID table, then padding `[F]`

The image region `[300, 184620)` is not uniform. Walking it:

| region | content | evidence |
|---|---|---|
| `300–344` | image-local header | `ffffffff 65000b02 0effffff 21240000 00240000` — the version word `65000b02` is **duplicated** from file offset `0x10` (`[F]`: `d[16:20] == d[304:308]`) |
| `345–176,000` | **ARM Thumb code** | `0x70b5` at 360 = `push {r4,r5,r6,lr}` |
| `176,000–176,110` | descending byte table | first 125, last 68, strictly non-increasing over the sampled run |
| `177,125` | **NFC Forum NDEF Type-4 AID** | `d2760000850101` |
| `177,152` | TLV configuration block | see below |
| `181,030–184,620` | `0xFF` padding | 3,590 B = 1.94% of the file |

`[F]` Thumb density, measured as 16-bit words at even offsets:

| range | `push16` per KiB | `bl`-prefix per KiB |
|---|---:|---:|
| 300–4,096 | 7.55 | 55.03 |
| 4,096–176,000 | 7.15 | 39.51 |
| 176,000–181,030 | 0.81 | 4.68 |

A nearly **9× drop** in `bl` density after 176,000 is what separates the code from
the data table (`39.51 → 4.68` per KiB; `push16` drops `7.15 → 0.81`). Combined
with the trailing `0xFF` run, the executable region is `[345, 176,000)` =
**175,655 B ≈ 171.5 KiB** of Thumb. `[F]` The part is **ARM Cortex-M0
(Thumb-2)**, per the independent S3NRN82 research write-up (the S3NRN4V is the
later part in the same line); the code density here is consistent with it, and
I mark the ISA `[I]` for *this specific file* since I decoded no instructions.

`[F]` The AID at 177,125 is `D2760000850101`, the NFC Forum **NDEF Type-4 tag**
application identifier. Before it sits a tag-length sequence
(`3b 01 03 e1 07`), and the TLV block immediately after carries:

```
e1 04 01 5e 00 ff 05 06      (length 0x15e = 350)
e1 05 00 14 00 ff 05 06      (length 0x014 = 20)
e1 06 00 32 00 ff 05 06      (length 0x032 = 50)
e1 07 00 32 00 ff 05 06      (length 0x032 = 50)
e1 08 00 1e 00
```

`[I]` The `e1 0x` tags with 2-byte lengths and the `ff 05 06` trailer are the
NDEF file-control TLV set; the shape is NFC Forum T4T. I can read the sizes but
cannot name the four files without the tag specification the vendor used.

`[F]` The last non-`0xFF` byte is at 181,029, and the 32 bytes before it are
`08 000000 10 000000 20 000000 40 00 60 83 00 01 … 00 00 44 45 46 00` then
`a5 5a`. `[I]` That trailing `a5 5a` is a 16-bit checksum trailer of unknown
construction; I did not reverse it.

### 3.4 The two signature blobs are recorded, not validated `[F]`

| blob | range | bytes | entropy | first 8 bytes |
|---|---|---:|---:|---|
| `sig` | `[44, 172)` | 128 | 6.55 | `9352e9b806a9b59a` |
| `custom_sig` | `[172, 300)` | 128 | 6.60 | `01155c9e8d6ee91d` |

`[F]` The two blobs are distinct, both 128 B, both high-entropy.
`[F]` Neither contains `sha1(image)` = `48f6d36c51fbbd84f87745f4719881cf2e35a07d`
nor `sha256(image)` = `ada328ddf965518e41576730dadb9eac9dcdbbcff1df6f648f2d4991679aa19a`.

That is the expected result, not a defect: the kernel computes
`SHA1(image)` **at load time** and sends it as `hash_data` alongside the
signature in `ENTER_UPDATE_MODE`. So the digest is never stored in the file — it
is recomputed and shipped over the wire. `[F]` 128 B is the signature size of
RSA-1024, or of `r‖s` ECDSA-P256. Which algorithm is in use is **not
determinable without the public key or the controller** — recorded, `[U]` (§9).

`[F]` The driver chooses between the two blobs at runtime, based on the
bootloader: `s3fwrn5_fw_setup()` tests `bootinfo.hw_version[2]`
(`s3fwrn5_fw_is_custom()`) and picks `custom_sig`/`custom_sig_size` if set,
otherwise `sig`/`sig_size`. So both blobs ship in every image and only one is
used per chip — which explains why the container carries two independent 128-byte
signatures rather than one.

`[F]` The `0xFF` runs sit at `[177,203, 177,452)` and `[181,030, 184,620)`. The
second is the file tail; the first is a gap inside the configuration region.
Total padding ≈ 3,839 B = 2.08%.

`[F]` The `hwreg` and `swreg` register images are the **RF calibration** data,
not firmware. The LWN series names them exactly: *"chip-scoped
`samsung/s3nrn4v/{hwreg,swreg}.bin` paths"*, called *"RF calibration data"*,
loaded by a proprietary `DUAL_OPTION` command and merged into one stream. That
explains their sizes (3,232 B and 336 B), which fit no image container — and it
means the pair belongs to the `rfreg` path, not the `firmware` path.

`[F]` The mainline `rfreg` section size is `S3FWRN5_RFREG_SECTION_SIZE 252` and
the checksum is "sum of little-endian `u32` over the whole file, `& 0xffff`".
Neither register file's size is a multiple of 252 (3,232 = 12×252 + 208;
336 = 1×252 + 84; combined 3,568 = 14×252 + 40), so **the section size does not
confirm from the sizes alone** — plausible, since the file is chunked at send
time and need not be a whole number of sections. Recorded `[U]`.

---

## 4. Fleet-level findings

### 4.1 `st54j_fw.bin` is the counter-example: size *does* identify it `[F]`

The Samsung files have fixed size and variable md5 (§2.2). STMicro is the
opposite — one md5 per size, and the size tracks the SoC generation:

| size | md5 | devices | `soc` |
|---:|---|---|---|
| 195,560 | `c0ca215a…` | Pixel_4A_5G, Pixel_5, Pixel_5A | Qualcomm SM7250 Snapdragon 765G |
| 219,688 | `86a23d64…` | Mi_13, Mi_13_Pro, Poco_F6_PRo, Redmi_K60_Pro | (blank) |
| 219,952 | `034f1063…` | Pixel_6, 6A, 6_Pro, 7, 7_Pro, 7a, Fold | Tensor GS101 / GS201 |

`[F]` Three sizes, three md5, and **no size carries two md5**. So for ST54J,
`(size, md5)` is a complete key. `[F]` The progression is
195,560 → 219,688 → 219,952, i.e. **+24,128 B** from SM7250 to SM8550 and only
**+264 B** from SM8550 to Tensor. `[I]` The 264-byte step is small enough to be a
config/table change rather than a code-generation change.

`[F]` `st54l_fw.bin` inverts the pattern once more: **8 rows, 1 size, 1 md5** —
every Pixel 8/9 family device ships the *identical* ST54L image (261,825 B,
`557b3729…`), while `st54l_conf.bin` is 2,142 B with **8 distinct md5**, one per
device. So on ST54L the *configuration* is per-device and the *firmware* is not.

`[F]` That gives a clean three-row summary of how these vendors version:

| vendor/family | firmware md5 | config/RF md5 |
|---|---|---|
| Samsung `s3nrn4v` | 5 across 11 rows | 8 (hwreg) / 6 (swreg) across 10 |
| Samsung `s3nrn82` | 2 across 7 rows | — (no register pair) |
| STMicro `st54j` | 1 per size, 3 sizes | — |
| STMicro `st54l` | **1 across 8 rows** | **8 across 8 rows** |

`[F]` `261,825 = 3 × 5 × 5 × 3,491`. There is no power-of-two or sector
structure in the ST54L size. `[F]` `st54j`'s 219,952 and 219,688 are also not
sector-aligned (`−300` gives 219,652 and 219,388, neither divisible by 4096). So
**the STMicro container is not the Samsung container** and no shared rule should
be inferred.

### 4.2 `db_type=AUDIO` is wrong on all 7 `sn100u.bin` rows `[F]`

All 7 rows are `db_type` `AUDIO`, `blob_subfamily` `nfc`, path
`oneplus/<codename>/vendor/firmware`. There is no audio file in the bucket and
none of the other 68 rows is `AUDIO`.

`[F]` The file is the **NXP SN100U NFC controller firmware**. NXP's own firmware
repository publishes it as `sn1xx/64-bit/libsn100u_fw.so`
(`github.com/NXP/nfc-NXPNFCC_FW`), and the SN100x part is documented as a
single-die *"Secure Element and NFC Controller"*.

`[F]` The repo already says so, in a document that predates this issue:
`research/drivers/audio.md` line 54 labels the row *"**NFC** — NXP SN100U
controller FW"*, line 179 heads a section *"`sn100u.bin` (7 rows) — not audio"*,
and lines 203–204 conclude *"`sn100u.bin` should be re-typed `NFC`, not `AUDIO`"*.
So this is not a new claim — it is a claim the audio sweep already made and the
matrix has not absorbed. I record it and do not edit the matrix (§9).

`[F]` The misclassification is not a path artefact. The file sits in
`vendor/firmware` — the same leaf as 417 of the 422 `audio` rows and as all 14
`st54j_fw.bin` rows, so path alone cannot distinguish them. What separates the
buckets is the *filename*: the 422 `audio` rows are 418 `.bin` + 3 `.1` + 1
`.img` coefficient blobs across 124 distinct names, whose prefixes are `cs*`
(Cirrus) 147 rows, `aw*` (Awinic) 114, `rt*` 24, plus `soundboosterparam.bin`
and `spkamp.bin` — and **not one of the 124 names begins with `sn`**. So
`sn100u` could not have been classified by an audio-prefix rule at all. `[I]`
The `AUDIO` label came from something other than path or filename prefix — most
plausibly a nearby-row context carry-over during census generation, which I
cannot reconstruct from the matrix alone.

### 4.3 The register pair is 2 of the 3 Samsung device classes `[F]`

`hwreg` (3,232 B) and `swreg` (336 B) appear on **9 devices each**, with 8 and 6
distinct md5 respectively — i.e. they vary per device, unlike the firmware whose
size is fixed. Devices with the pair: FP6, `Galaxy_S20_FE`, `Galaxy_A21S`, and
all six Motorola codenames.

`[F]` They are **absent** on `Galaxy_F62`, `Galaxy_S10*`, `Galaxy_Note_10*` —
i.e. on the `s3nrn82` devices, which carry no register pair at all. So the
register-image convention arrived with `s3nrn4v`.

`[F]` They are also absent on all STMicro and NXP devices. So "NFC firmware ships
alone" is the norm in this bucket: **only 17 of 46 devices carry more than one
file**, split into 9 Samsung `s3nrn4v` devices (firmware + register pair) and 8
STMicro `st54l` devices (firmware + config). `hwreg`/`swreg` themselves appear on
9 devices; nothing else carries the register pair.

### 4.4 `st54j_fw.bin` and `st54k_conf_38.4MHz.bin` are byte-identical `[F]`

`research/qualcomm/results/…` no — `docs/devices/xiaomi/Mi_13/other.md` line 139
records that `st54k_conf_38.4MHz.bin` is byte-identical to `st54j_fw.bin` (same
md5 `86a23d642374de60b397caa8d0ecaccb`, same size 219,688 B), and flags the
reason `[OPEN]`.

`[F]` My measurement agrees with the size/md5, and adds the fleet context: the
`86a23d64…` build is the one shared by the four-device SM8550 quartet (Mi_13,
Mi_13_Pro, Poco_F6_PRo, Redmi_K60_Pro). `[I]` A file named `st54k_conf_38.4MHz`
carrying the `st54j` firmware bytes is a packaging error in the vendor tree
(config filename, firmware payload), not a second artifact. I cannot prove the
direction of the error without the vendor package (§9).

---

## 5. `nfc` versus the rest of the firmware record `[F]`

### 5.1 The bucket is not a census of NFC hardware `[F]`

Every device in the bucket has exactly the rows the matrix recorded, and nothing
more — there is no device with a *partial* NFC set that I can detect. 46 devices
divide cleanly into three silicon classes with no leftovers.

But **`nfc` is far from complete coverage of devices that have an NFC
controller.** `[F]` The matrix holds **123 devices** in total, **120** of them
carrying `other`-family rows, and `nfc` rows exist on **46** of those 123. `[F]`
Among the 40 devices with the most matrix rows overall, **30 have no `nfc` row at
all** — e.g. `OnePlus_13`, `Mi_12S_Ultra`, `Mi_12S`, `Poco_F5_Pro`, `OnePlus_12`,
`FP5`, `Nord_4`. Every one of those is a flagship-class device that certainly has
an NFC controller. `[I]` So the bucket is a census of *what the LineageOS vendor
trees shipped as a discrete firmware file*, not a census of NFC hardware; on the
other devices the firmware lives in the controller's OTP/flash or in a partition
the census did not read.

`[F]` That inference is supported directly by the LWN series: the S3NRN4V
*"ships with working firmware"*, and its bootloader *"reports a hardware version
the driver has no flash base address for (so the firmware download step is
skipped)"*. So on the FP6 specifically, the chip is self-sufficient and the
`184,620`-byte file is a **recovery/update** artifact rather than a
must-load-at-boot blob. That is the opposite of the `hyp`/`tz` situation, where
the file *is* the firmware.

### 5.2 What mainline can and cannot load `[F]`

| filename | mainline driver | request name | status |
|---|---|---|---|
| `sec_s3nrn4v_firmware.bin` | `drivers/nfc/s3fwrn5/` | `core.c` hardcodes **`sec_s3fwrn5_firmware.bin`** — *not* the `4v` name | `[F]` the name does not match; the LWN v4 series adds the part but skips download |
| `sec_s3nrn82_firmware.bin` | `drivers/nfc/s3fwrn5/` | same | `[F]` same mismatch |
| `sec_s3nrn4v_hwreg.bin`, `_swreg.bin` | `drivers/nfc/s3fwrn5/` | `s3fwrn5_nci_rf_configure()` takes a **parameter**; `core.c` passes `sec_s3fwrn5_rfreg.bin` | `[F]` name mismatch, but the *format* is the documented `rfreg` one |
| `sn100u.bin` | `drivers/nfc/nxp-nci/` | `nxp_nci_fw_download()` takes a **parameter** | `[F]` no hardcoded name; board/HAL supplies it |
| `st54j_fw.bin`, `st54l_fw.bin`, `st54l_conf.bin` | `drivers/nfc/st-nci/`, `st21nfca` | out-of-tree: `STMicroelectronics/ST54-android-kernel` | `[F]` no mainline parser; the ST driver repo's `README.md` is the two-line string `# ST54-android-kernel` |

`[F]` The load-bearing fact here: **the Samsung firmware format is fully
specified in mainline, but the file *names* in the fleet do not match the name
mainline requests.** A mainline FP6 needs either a rename or a firmware-name
override to use `sec_s3nrn4v_firmware.bin`. The LWN v4 series sidesteps this
because the S3NRN4V skips the download entirely.

`[F]` For STMicro and NXP the situation is the reverse: the names are supplied at
runtime so nothing breaks, but there is **no public byte-level parser** for either
container. `[N]` I searched for one and did not find it; the ST path is a HAL
(`ST54-android-hardware-st-nfc`), and the NXP path is an opaque chunker.

### 5.3 The download protocol differs by vendor, and only one is documented `[F]`

| step | Samsung `s3fwrn5` | NXP `nxp-nci` |
|---|---|---|
| reset | `0x00 RESET` | `0xF0 RESET` |
| identify | `0x01 GET_BOOTINFO` → `hw_version[4]`, `sector_size`, `page_size`, `frame_max_size`, `hw_buffer_size` | `0xF1 GETVERSION`, `0xF4 GET_DIE_ID` |
| integrity | — (`SHA1(image)` sent in `ENTER_UPDATE_MODE`) | `0xE0 CHECKINTEGRITY` |
| write | `0x04 UPDATE_SECTOR` (one whole sector per command) | `0xC0 WRITE` (chunked, CRC-CCITT, `CHUNK_FLAG 0x0400`) |
| read back | — | `0xA2 READ`, `0xA7 LOG` |
| finish | `0x05 COMPLETE_UPDATE_MODE` | `0xF2 GETSESSIONSTATE`, `0xD0 FORCE` |
| timeout | 1000 ms per message | 30 s (`NXP_NCI_FW_ANSWER_TIMEOUT`) |
| return codes | `0x00`–`0x08` (9 codes) | `0x00`–`0xC5` (16 codes) |

`[F]` This is the sharpest structural difference in the bucket. Samsung sectors
the image (`sector_size × image_sectors`) and sends a whole sector per command,
which is why its container is sector-padded to 4096 and why 5 builds share one
size. NXP streams chunks with a per-chunk CRC and a 30-second window, which is why
its image is one continuous opaque blob with no internal alignment (§2.3). The
file format is a **direct consequence** of the transport, in both cases.

`[F]` STMicro's protocol is not in mainline and I could not read it from the
driver repo (the `README.md` is two lines). Not claimed (§7).

---

## 6. What this adds to the existing record `[F]`

Prior art, and what this issue does *not* re-derive:

| artifact | what it already establishes | reused as-is here |
|---|---|---|
| `research/qualcomm/docs/interface-nfc.md` | the NXP `nxp-nci` driver↔controller interface: NCI framing, cold/NCI mode switch, the `0xF0/0xF1/0xE0/0xC0/0xA2/0xF2/0xA7/0xD0/0xF4` command set, 30 s timeout | the whole protocol layer (§5.3 right column) |
| `research/qualcomm/results/census.md:697` | `vendor-firmware/sec_s3nrn4v_firmware.bin`, 184,620 B, sha256 prefix `407a4d07e712397d` | the file's existence and hash |
| `research/drivers/audio.md` §"`sn100u.bin` (7 rows) — not audio" | `sn100u.bin` is NXP SN100 **NFC** firmware and *should be re-typed `NFC`* | the `AUDIO` defect (§4.2) — this issue confirms and counts it |
| `docs/devices/xiaomi/Mi_13/other.md` Group E | `st54j_fw.bin` is STMicroelectronics ST54J CLF+SE firmware; `st54k_conf_38.4MHz.bin` is byte-identical | the ST54J identity (§4.1) and the duplicate (§4.4) |
| `docs/devices/samsung/Galaxy_S20_FE/other.md` | the `sec_s3nrn4v_*` triple is "Samsung SEC S3NRN4V NFC controller firmware + hardware/software register images" | the part identity (§3) |
| `research/fleet/third-device-instantnoodle.md:86` | `sn100u.bin` present in the OnePlus 8 ODM tree | existence only |

**New in this issue:**

1. **First byte-level decode of any NFC firmware file in this repo.** The 44-byte
   header, 300-byte prefix, two 128-byte signature blobs, the Thumb image and the
   trailing NDEF/TLV + padding all mapped, with exact closure
   (`44 + 128 + 128 + 45×4096 = 184,620`).
2. **The `300 + N×4096` law**, verified on a **second Samsung part**
   (`sec_s3nrn82`: `300 + 37×4096 = 151,852`) and on **0 of 6** non-Samsung
   files — so it is a vendor invariant with a control group.
3. **The vendor taxonomy of the bucket**: 8 filenames → 3 silicon vendors, with
   the `sec_` prefix resolved as Samsung, and **zero cross-vendor devices**.
4. **The two signature blobs explained**: they are the standard and *custom*
   signature, and the driver picks one at runtime from `bootinfo.hw_version[2]`
   — which is why every image carries both.
5. **`SHA1(image)` is not stored in the file** — it is recomputed at load. This
   is why no digest appears in either 128-byte blob, and it corrects the
   intuition that a signed image must carry its own digest.
6. **The `AUDIO` misclassification counted fleet-wide** (7/7 rows) and traced to
   its source document, which already said the same thing.
7. **The duplicate-row defect** (3 rows, `Galaxy_A21S`) set against the
   corpus-wide figure (46 duplicate rows in 33,917).
8. **`sn100u.bin` measured as unparseable** (7.9957 bits/byte, 0 repeated 16-byte
   blocks, chi-square 1,414.5) rather than asserted opaque.

---

## 7. Honest negatives `[N]`

- **No ST54J, ST54L or `sec_s3nrn82` payload exists in this workspace.** Their
  container layouts are therefore **not decoded**. The `300 + N×4096` closure for
  `s3nrn82` is arithmetic on a census size, not a byte-level parse — it is `[F]`
  as an identity and `[I]` as a container claim.
- **`sec_s3nrn4v_hwreg.bin` and `sec_s3nrn4v_swreg.bin` are not on disk.** The
  RF-calibration pair is described from the LWN series only; I did not read a
  byte of either. Their `252`-byte relationship to `S3FWRN5_RFREG_SECTION_SIZE`
  is explicitly **not** confirmed (neither size is a multiple of 252).
- **No public byte-level spec for the STMicro or NXP containers.** Searched;
  `ST54-android-kernel`'s `README.md` is two lines and the loader is a HAL. NXP
  ships `libsn100u_fw.so` and the mainline driver never parses a header.
- **`sn100u.bin` is not decodeable here.** 7.9957 bits/byte with zero repeated
  16-byte blocks. No key, no controller, no structure. I record the measurement
  and stop rather than inventing a parse.
- **The signature algorithm is unknown.** Both blobs are 128 B; that fits
  RSA-1024 or `r‖s` ECDSA-P256 equally. No public key, no OID string, no
  verification attempted. `[U]`.
- **The sector size on silicon is 4096 only by inference.** 4096 is the largest
  power-of-two that closes for the file; the actual value comes from the chip's
  `GET_BOOTINFO` reply, which I cannot see.
- **The AID/TLV region is read but not named.** I can show the NFC Forum
  NDEF Type-4 AID `D2760000850101` at 177,125 and four `e1 0x` TLVs with lengths
  350/20/50/50, but not which files they address or what the `ff 05 06` trailer
  means.
- **The trailing `a5 5a` is not reversed.** Two bytes at `181,028`; unknown
  checksum, not claimed.
- **The `soc` column is blank on 32 of 75 rows** and `isa_identified` /
  `sha256_if_listed` are blank on 75/75. Nothing in this document upgrades them.
- **No disassembly.** No ARM/Thumb disassembler in this environment (the same
  limit recorded in `other-touch.md` and `tz-hyp.md`). Every Thumb claim is a
  *statistical* word-class count, not an instruction listing.
- **The three `Galaxy_A21S` duplicate rows are recorded, not fixed.** Deduplicating
  the matrix is a corpus-wide decision.
- **The `st54k_conf_38.4MHz` / `st54j_fw` duplicate direction is unknown.** I can
  show they are byte-identical; I cannot tell which name is the error.
- **No claim about which of the 5 `s3nrn4v` builds is newest.** The FP6 file's
  date field reads `202509010445`; I did not obtain the other four files, so no
  ordering is possible.

---

## 8. Rule 1 corrections applied in place `[F]`

Two existing documents stated, as lab fact, that the FP6 census contains **no NFC
firmware image** and that the FP6 controller identity is `[OPEN]`. Both are
false against the file the same document cites.

**Correction 1 — `research/qualcomm/docs/interface-nfc.md` §1.** The claim

> "The lab's committed FP6 census (modem/vendor/dsp trees, 665 files) contains
> **no NFC firmware image file** (`qualcomm-fp6/results/census.md`, 2026-11-15)."

is contradicted by `research/qualcomm/results/census.md` line 697, which lists
`vendor-firmware/sec_s3nrn4v_firmware.bin` at 184,620 B with sha256
`407a4d07e712397d…`. `[F]` The local payload hashes to exactly that sha256
(§2.1), so the census was right and the interface note misread it as "no image".
The same section's `[OPEN]` item — *"the exact NFC controller part on FP6 (NXP
SN100 family vs other) is not stated in any data available to this box"* — is
answered by the filename: **Samsung S3NRN4V**, confirmed independently by Samsung's
part page and by the mainline LWN series that names the FP6 / SM7635 explicitly.
Both are corrected in place, with the correction noting that the `nxp-nci`
protocol material in that document remains correct but describes **a different
vendor's** part than the one on this device.

**Correction 2 — `research/qualcomm/docs/userspace-firmware-split.md` line 53
(and the same row at `userspace-vs-firmware-split.md` line 53).** The `NFC` row's
firmware column reads *"firmware inside the NFC controller (no image file in the
censused partitions)"*. The parenthetical is false for the same reason; the
corrected row points at `sec_s3nrn4v_firmware.bin` (184,620 B) and its sha256,
and keeps the true part of the statement — the chip *also* holds working firmware
— as a separate clause rather than a replacement.

`[F]` `research/drivers/audio.md` is **not** corrected: its `sn100u.bin`
`AUDIO`→`NFC` finding was already right, and this document only counts and
confirms it (§4.2).

`[F]` `docs/REPO-STATE-MAP.md` had no `nfc` row (its `other`-family rows covered
`media`, `audio`, `touch` and `fingerprint` only). One is added pointing at this
document.

---

## 9. Open items `[U]`

- **Which of the 5 `s3nrn4v` builds is newest?** Needs the other four files; only
  a date field separates them.
- **Is the FP6 matrix `md5_db` cell or the payload the wrong one?** The sha256
  matches the census exactly; the matrix md5 does not match the file. Same shape
  as the FP6 `hyp` defect in `tz-hyp.md` §2.1, unresolved there too.
- **What is the signature algorithm?** 128 B = RSA-1024 or ECDSA-P256 `r‖s`.
  Needs a public key or the controller.
- **What does the `e1 0x` TLV set address, and what is the `ff 05 06` trailer?**
  Four TLVs with lengths 350/20/50/50 after the T4T AID.
- **What is the `a5 5a` trailer at 181,028?** Two bytes, unknown checksum.
- **Why is `st54l_fw.bin` identical across 8 devices while `st54l_conf.bin`
  differs on all 8?** `[I]` firmware is chip-family-wide, config is per-board —
  unproven.
- **What distinguishes the 3 `st54j` builds?** Sizes 195,560 / 219,688 / 219,952
  track SoC generation, but +264 B between SM8550 and Tensor is oddly small.
- **Should the 46 duplicate rows in the matrix be deduplicated?** Corpus-wide
  decision; `nfc` contributes 3.
- **Should `sn100u.bin`'s 7 rows be re-typed `NFC`?** `audio.md` already says yes;
  the matrix still says `AUDIO`.
- **Is the `s3nrn4v` part's usable flash 192 KiB or less?** The image is 180 KiB
  = 93.8% of 192 KiB. The marketing "192K" is not the usable figure.
- **Does the `sec_s3nrn82` file use the same 44/128/128 header?** Arithmetic
  closes; bytes unverified.

---

## 10. Method `[F]`

Everything above was produced with stdlib Python only, run as `python3 -I`. No
comments or docstrings in the analysis source. No disassembler, no `openssl`
needed for this issue.

```python
# container walk: no assumed layout beyond the kernel's own offset table
date      = d[0x00:0x0C].decode()
version   = struct.unpack_from('<I', d, 0x10)[0]
sig_off   = struct.unpack_from('<I', d, 0x14)[0]
sig_size  = struct.unpack_from('<I', d, 0x18)[0]
img_off   = struct.unpack_from('<I', d, 0x1C)[0]
img_sec   = struct.unpack_from('<I', d, 0x20)[0]
csig_off  = struct.unpack_from('<I', d, 0x24)[0]
csig_size = struct.unpack_from('<I', d, 0x28)[0]
assert sig_off + sig_size == csig_off
assert csig_off + csig_size == img_off
```

```python
# the closure test, run against every size in the bucket, not just the one file
for size in all_bucket_sizes:
    r = size - 300
    closes = r > 0 and r % 4096 == 0
```

```python
# Thumb density: 16-bit words at even offsets only
push = sum(1 for i in range(0, len(seg) - 1, 2) if seg[i + 1] == 0xB5)
bl   = sum(1 for i in range(0, len(seg) - 3, 2)
           if (struct.unpack_from('<H', seg, i)[0] & 0xF800) == 0xF000)
```

Verification discipline: every arithmetic closure in §3.2 and §3.3 was checked
two ways — as an identity on the header words, and against the byte offsets
actually present in the file (last-non-`0xFF` scan, AID `find()`, TLV walk). The
`[F]` marker means both checks passed. Where only the identity holds and the byte
evidence is absent, the claim is `[I]` or `[U]`.

Census numbers come from a single `csv.DictReader` pass over
`upstream-contribution/blob-database/coverage-matrix.csv`, filtered on
`blob_subfamily == 'nfc'`; cross-bucket figures use the whole 33,917-row file.

Sources and access dates:

| source | retrieved |
|---|---|
| `coverage-matrix.csv` (repo, feat/open-device-site) | 2026-11-22 |
| `sec_s3nrn4v_firmware.bin` (FP6, local) | 2026-11-22 |
| `sn100u.bin` (instantnoodle, local) | 2026-11-22 |
| `torvalds/linux` `drivers/nfc/s3fwrn5/{firmware.c,firmware.h,core.c,nci.c}` | 2026-11-22 |
| `torvalds/linux` `drivers/nfc/nxp-nci/firmware.c` | 2026-11-22 |
| `lwn.net/Articles/1087764/` — `[PATCH v4 0/6] nfc: s3fwrn5: support the S3NRN4V variant` | 2026-11-22 |
| `semiconductor.samsung.com/…/s3nrn4v/` (part identity, "192K") | 2026-11-22 |
| `st.com/en/secure-mcus/{st54j,st54l}.html` (CLF+SE identity) | 2026-11-22 |
| `github.com/NXP/nfc-NXPNFCC_FW` (`sn1xx/64-bit/libsn100u_fw.so`) | 2026-11-22 |
| `github.com/pr0misc/Samsung_S3NRN82_Research` (Cortex-M0, memory map) | 2026-11-22 |
| `research/qualcomm/results/census.md` (FP6 census, 665 files) | 2026-11-22 |
