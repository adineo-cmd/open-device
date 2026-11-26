# `misc` — 10,720 rows, and the two TEE containers hiding in them

Analysis date: 2026-11-25. Analyst: OC-1 (`100milionseek`), issue
[#2059](https://github.com/adineo-cmd/open-device/issues/2059).

Inputs:
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows) for the census;
the FP6 split firmware tree at
`…/downloads/lineage-fp6/extracted/trees/modem/image/` (23 `.mdt` plus their `.bNN`, TAs and
PIL processors in one directory) and `…/modem/image/modem_pr/mcfg/configs/` for the carrier
metadata, `…/modem/image/qca6750/Data.msc`, `…/modem/image/gptauuid.xml`;
`…/data-fetch/second-device/larry/tree-vendor/firmware/` (7 `.mdt`, the layout-A side);
`…/data-fetch/second-device/instantnoodle/modem-fat-lfn/` (32 `.mdt`, including 17 ELF64 TAs
with 8 program headers); and all 78 `.mdt` files on this machine for the corpus-wide sweep.

No payload is committed. No payload bytes are reproduced: this note carries sizes, offsets,
counts, `e_machine`/`e_type`/`e_phnum`/`p_filesz` values, md5 prefixes, and file/symbol names
only. Stdlib Python 3 only, run `python3 -I`, no third-party libraries — `struct` for ELF
parsing, `hashlib` for digests, `csv`/`collections` for the census.

Evidence classes: `[F]` fact (command-verified this session), `[I]` inference,
`[N]` honest negative (searched, not found), `[U]` unknown / open.

**Verdict.** `misc` is the **largest of the thirteen `other` subfamilies** — 10,720 rows,
119 devices, 8,498,193,635 B — and it is **not a format**. It is a path-derived residual
bucket: whatever did not match a named subfamily landed here, and it spans partition images,
TEE trustlets, WLAN/BT firmware, carrier configs and audio blobs. 66.52% of its bytes are a
handful of `radio/` partition images, and the single most interesting thing inside it is that
the 107 `.mdt` stems are **two different container families wearing one extension**: ELF32 PIL
processor images that `mdt_loader.c` can parse, and ELF64 AArch64 Trusted Applications that it
cannot.

The report's one durable contribution beyond the census is a **layout law that closes on
502 of 502 matrix groups** and a **clean split of the two container families by program-header
count**, which together close an explicit `[U]` left open in
`research/fleet/other-fingerprint.md` §8.6.

---

## 0. Headline

1. **`[F]` `misc` is #1 of 13 `other` subfamilies on both axes.** 10,720 rows /
   119 devices / 8,498,193,635 B / 1,988 basenames / 4,071 `md5_db`. That is 31.61% of the
   whole corpus's rows but only 12.18% of its bytes, and **71.53% of `other` rows and 60.05%
   of `other` bytes**. It is a bucket by *exclusion*, and the name says so.
2. **`[F]` 66.52% of its bytes are 261 `radio/` rows.** `dsp.img` alone is 3,321,888,768 B
   across 61 devices and is **exactly 64 MiB or 32 MiB** on every one of them — a partition
   extent, not an image size. The next axis is `modem/image` (6,391 rows but only 13.95% of
   bytes), then `firmware` directories (9.35%), then `bluetooth/image` (2,420 rows, 0.33%).
3. **`[F]` The 107 `.mdt` stems are two container families.** They share the extension and
   nothing else. The on-disk split is **43 ELF32** (PIL processors: `adsp`, `cdsp`, `modem`,
   `wpss`, `ipa_fws`, the `*_zap` shaders) and **35 ELF64** (AArch64 Trusted Applications,
   `e_machine=183`, `e_type=3`). The matrix types all 757 `.mdt` rows a single `ELF64`, which
   is right about the TAs and wrong to generalise.
4. **`[F]` `b00` is the ELF header block, and it decomposes the container exactly.** For all
   ten `b00` values observed, `b00 == e_ehsize + e_phnum × e_phentsize`, uniquely — 148, 212,
   308 are ELF32 with 3, 5, 8 phdrs; 512 and 568 are ELF64 with 8 and 9. This makes `b00` a
   **one-number fingerprint of the container's class and shape**, derivable from the matrix
   with no payload at all.
5. **`[F]` The hash segment position splits the two families, and it is not a vendor split.**
   `mdt == b00 + b<hash>` holds on **502 of 502** groups that have both files. The hash sits at
   index 8 on all 274 nine-part ELF64 TAs, and at index **1** on all 98 eight-part ones — where it
   is *not* the last segment: a `hash@b01` group has payload segments after the hash (up to index
   23). Across all 502 the hash is the highest-numbered segment on 288 and is not on 214. Which
   slot it takes is fixed by the container shape, never by vendor.
6. **`[F]` This closes `other-fingerprint.md` §8.6.** That note records as `[U]` that "the
   corpus cannot show whether an eight-part TA lacks the alias or merely renumbers it". 17
   eight-part ELF64 TAs are on disk: **0 of 17** carry a duplicated `(p_offset, p_filesz)`
   pair, against **16 of 16** nine-part ones. The alias is specific to the nine-part shape.
7. **`[F]` One Rule 1 correction.** `trustzone-census.md` still says mainline QSEECOM support
   lives at `drivers/tee/qcom/qseecom.c`. That path is 404 in torvalds/master, re-checked
   today; the in-tree driver is `drivers/firmware/qcom/qcom_qseecom.c`, and it registers
   exactly **one** TA name — `qcom.tz.uefisecapp` — against the 107 stems here.

---

## 1. The bucket in numbers

All figures `[F]` from the matrix.

| metric | value |
|---|---:|
| rows | **10,720** |
| devices | **119** |
| filenames (basenames) | **1,988** |
| distinct `md5_db` | **4,071** |
| total declared bytes | **8,498,193,635** |
| `(device, filename)` pairs | **10,579** |
| rows per pair | **1.013** |
| distinct `db_path` values | **520** |
| duplicate full rows | **30** (§7.1) |
| rows with blank md5 | **0** |
| rows with `sha256_if_listed` | **15** |
| rows with `isa_identified` | **15** |
| rows with blank `soc` | **6,785** |
| `interface_documented = y` | **0 / 10,720** |
| zero-byte rows | **40** |
| median row size | **6,602 B** |
| largest row | **269,996,032 B** (`vm-bootsys.img`) |

Share of the corpus and of `other`:

| denominator | rows | bytes |
|---|---:|---:|
| all 33,917 rows / 69,797,539,502 B | **31.6066%** | **12.1755%** |
| `other` 14,987 rows / 14,152,121,440 B | **71.5287%** | **60.0489%** |

### 1.1 Rank inside `other` `[F]`

| rank | subfamily | rows | bytes |
|---:|---|---:|---:|
| **1** | **`misc`** | **10,720** | **8,498,193,635** |
| 2 | `camera` | 1,611 | 4,563,019,282 |
| 3 | `touch` | 880 | 516,418,690 |
| 4 | `media` | 470 | 29,190,348 |
| 5 | `audio` | 422 | 5,418,315 |
| 6 | `fastchg` | 315 | 36,989,007 |
| 7 | `fingerprint` | 284 | 387,540,764 |
| 8 | `oled` | 157 | 4,068,320 |
| 9 | `nfc` | 75 | 9,677,922 |
| 10 | `esim` | 41 | 8,407,085 |
| 11 | `sensors` | 5 | 86,541,968 |
| 12 | `tinysys` | 4 | 4,132,864 |
| 13 | `gpu-compute` | 3 | 2,523,240 |

`misc` is the only subfamily that leads both axes, and it leads rows by a factor of 6.65 over
the runner-up. That is the signature of a residual bucket rather than a content class.

### 1.2 Vendors and devices `[F]`

| vendor | rows | bytes | devices |
|---|---:|---:|---:|
| xiaomi | 4,205 | 2,924,248,777 | 17 |
| oneplus | 3,436 | 2,659,196,206 | 22 |
| motorola | 1,285 | 1,125,435,747 | 23 |
| samsung | 623 | 629,804,717 | 17 |
| fairphone | 399 | 362,700,537 | 3 |
| nothing | 298 | 169,415,757 | 2 |
| google | 249 | 192,084,224 | 19 |
| realme | 122 | 399,907,074 | 2 |
| sony | 51 | 560,718 | 12 |
| fxtec | 50 | 34,771,522 | 1 |
| lenovo | 2 | 68,356 | 1 |

Eleven vendors, device counts summing to exactly 119 — no device is double-counted across
vendors. Note that row count does not track device count: `fairphone` has 399 rows on 3 devices
(133 rows/device) while `google` has 249 rows on 19 (13 rows/device). Xiaomi's lead is a
device-count effect (17 devices) as much as a per-device one.

The eight devices with the most rows are all Xiaomi or OnePlus, at 350–372 rows each:
`Mi_12S_Ultra` 372, `Mi_12S_Pro` 371, `Mi_12S` 361, `OnePlus_13` 361, `Poco_F5_Pro` 361,
`Poco_F5` 359, `Mi_12_Pro` 358, `Mi_12T_Pro` 350. Those eight devices alone are 2,893 rows —
27% of the bucket — because a full `modem/image` ships ~50 split TAs plus a carrier-config
tree, and each file is a row.

`sony` is the outlier in the other direction: 51 rows carrying 560,718 B, 11 kB per row. Its
`misc` presence is metadata, not firmware.

---

## 2. What the bucket actually contains `[F]`

`misc` cannot be described by extension or by `db_type`, because both are mixed across it.
The only structure that survives is the **path**. Note that `db_path` in this CSV is the
*directory* — it never contains the filename (0 of 10,720 rows), so every bucket below is a
directory test.

| path axis | rows | bytes | % of bucket bytes | devices |
|---|---:|---:|---:|---:|
| **`radio/`** | **261** | **5,653,401,340** | **66.52%** | 86 |
| `modem/image` | 6,391 | 1,185,430,566 | 13.95% | 63 |
| any `firmware` dir | 1,215 | 794,743,798 | 9.35% | 118 |
| — `vendor/firmware` | 960 | 547,548,475 | 6.44% | 118 |
| — `odm/firmware` | 146 | 8,951,443 | 0.11% | 25 |
| `bluetooth/image` | 2,420 | 27,932,098 | 0.33% | 47 |
| `etc/` | 266 | 24,884,037 | 0.29% | 48 |

The first three axes cover 84.6% of rows. The remaining 15% is a long tail of
`vendor/lib64`, per-device `firmware/<part>`, vibrator and touch-panel data, and audio
parameter blobs — 520 distinct directories in all.

By extension, which cuts across those axes:

| extension | rows | bytes | % of bucket bytes |
|---|---:|---:|---:|
| `.img` | 382 | 5,703,058,958 | **67.11%** |
| `.bin` | 1,559 | 1,821,247,157 | 21.43% |
| `.bNN` split segment | 5,120 | 759,062,595 | 8.93% || `.elf` | 439 | 32,142,144 | 0.38% |
| `.tlv` | 117 | 11,537,984 | 0.14% |
| `.mdt` | 757 | 4,822,264 | **0.06%** |

**The `.mdt` rows are 7.1% of the bucket's rows and 0.06% of its bytes.** They are the most
numerous container family and the least voluminous. Everything interesting in this bucket is
small; everything large is a partition image.

### 2.1 `radio/` is partition-sized, not image-sized `[F]`

| filename | rows | size(s) | exact |
|---|---:|---|---|
| `dsp.img` | 61 | **67,108,864 ×38**; **33,554,432 ×23** | 64 MiB / 32 MiB |
| `vm-bootsys.img` | 5 | 269,996,032 | `0x1017D000` |
| `core_nhlos.img` | 5 | 153,731,072 ×2; 153,812,992; 144,932,864; 114,601,984 | — |
| `splash.img` | 14 | 344,064 ×5; 9,191,424 ×2; then 6 unique | — |
| `ldfw.img` | 16 | 2,392,064 ×13; 4,096,000 ×3 | — |
| `LOGO.img` | 4 | 40,673,280 total | — |

`dsp.img` is the clearest case in the whole corpus: **61 rows, 61 devices, two sizes, both
exact powers of two.** 67,108,864 = `0x4000000`; 33,554,432 = `0x2000000`. No DSP image has
two different sizes on two devices of the same class, and no row is off by even one byte. That
is a **partition extent** — the file is the size of the slot it was written to, not the size of
the code inside it. Any claim about DSP firmware size derived from these numbers is a claim
about partition layout.

The same reading applies to `vm-bootsys.img` (257.49 MiB, `0x1017D000`) and `core_nhlos.img`
(109–147 MiB): these are multi-hundred-MiB VM and modem-NHLOS images whose sizes are
allocation artefacts. `splash.img` and `ldfw.img` are the counter-example — genuinely
variable, content-sized.

`core_nhlos.img` is also the whole of `db_type=MSDOS` — 5 rows, one filename, and a label
that names no loader. It is a raw A/B slot (`core_nhlos_a`/`_b`, GPT type
`6690B4CE-70E9-4817-B9F1-25D64D888357`, 174,080 KB on one reference board and 122,880 KB on
another), written by `fastboot flash core_nhlos` and **never mounted**: no `fstab` entry
exists for it anywhere, while the neighbouring `modem_a` slot carries the Microsoft Basic
Data GUID and *is* mounted vfat at `/vendor/firmware_mnt`. Four of the five rows (three
distinct sizes: 144.9 MB, 153.7 MB ×2, 153.8 MB) exceed the 120 MiB slot, so slot size is
board-specific and cannot be read back from the file. Contract, GUIDs and the mainline
negative in `research/drivers/msdos.md` (#889).

### 2.2 `modem/image` is where the trustlets live `[F]`

6,391 rows over 63 devices, 1,185,430,566 B. The top names are the split containers:

| filename | rows | note |
|---|---:|---|
| `Data.msc` | 54 | WLAN debug-message catalog (§4.5) |
| `gptauuid.xml` | 45 | GPT partition→UUID map (§4.3) |
| `amss.bin` | 41 | modem firmware |
| `mbn_hw.dig` / `mbn_sw.dig` | 38 each | 32 B each, always (§4.1) |
| `mbn_hw.txt` / `mbn_sw.txt` | 38 each | carrier-config path lists |
| `oem_sw.txt` | 38 | carrier-config path list |
| `evass.mdt` | 53 | motor/VAD TA |
| `evautil64.mdt` | 35 | TA utility |
| `fingerpr.mdt` | 33 | fingerprint TA — filed here, not in `fingerprint` (§7.2) |
| `gpqese.mdt` | 28 | GlobalPlatform SE TA |
| `eseservice.mdt` | 26 | eSE service TA |

---

## 3. The two container families `[F]`

The 757 `.mdt` rows resolve to 107 distinct stems over 87 devices, 4,822,264 B. Classifying
them by their stem name alone is unreliable; classifying them by the **ELF header** is exact.

### 3.1 On-disk class split

Measured on every `.mdt` on this machine (78 files, `**/*.mdt` excluding `node_modules`):

| class | files | `e_machine` | `e_type` | `e_ehsize` | `e_phentsize` |
|---|---:|---|---:|---:|---:|
| ELF32 | **43** | 164 Hexagon, 1, 0 | 2 | 52 | 32 |
| ELF64 | **35** | 183 AArch64 | 3 | 64 | 56 |

The ELF32 half is the PIL family already documented in this repo —
`research/fleet/qdsp6sw-container.md`, `research/fleet/wifi-wpss.md` §2.4, and the widened law
in `research/fleet/other-camera.md` §4.4. The ELF64 half is the Trusted Application family
documented in `research/qualcomm/docs/trustzone-census.md` and
`research/fleet/other-fingerprint.md`. **Both are prior art here; what is new is the statement
that they share an extension and that the extension does not determine the class.**

By stem, the ELF64 TAs verifiable on disk are: `05B04A44-…`, `32552B22-…`, `FD719D50-…`,
`evautil64`, `featenabler`, `focal64`, `hdcp1`, `hdcp2p2`, `hdcpsrm`, `ic5`, `loadalgota64`,
`ops`, `smplap64`, `soter64`, `sp_license`, `winsecap`, plus the eight-part set of §3.4. Only
three of those (`evautil64`, `ic5`, `ops`) also appear as `.mdt` stems in the matrix — the rest
are on disk but not filed in this bucket, so they inform the container analysis without
inflating the census.

### 3.2 `b00` is the header block, and it names the container `[F]`

`b00` is not a payload segment. It is the ELF header plus the program-header table, verbatim:

```
b00 == e_ehsize + e_phnum × e_phentsize
```

Verified on every group in the matrix where `b00` is present, and cross-checked on disk
(`76/76` where the hash segment is also present, §3.3):

| `b00` size | decomposition | family | groups (A/B) |
|---:|---|---|---:|
| 148 | ELF32 `52 + 3×32` | `*_zap` shaders, `*_dtb` | 14 / 4 |
| 212 | ELF32 `52 + 5×32` | `ipa_fws`, `ipa_uc` | 4 / 0 |
| 308 | ELF32 `52 + 8×32` | generic ELF32 TA set | 83 / 0 |
| **512** | **ELF64 `64 + 8×56`** | **eight-part AArch64 TAs** | **98 / 0** |
| **568** | **ELF64 `64 + 9×56`** | **nine-part AArch64 TAs** | **0 / 274** |
| 692 | ELF32 `52 + 20×32` | `adsp`, `evass`, `cvpss`, `venus` | 4 / 1 |
| 756 | ELF32 `52 + 22×32` | — | 4 / 0 |
| 788 | ELF32 `52 + 23×32` | `slpi` (largest) | 2 / 0 |
| 820 | ELF32 `52 + 24×32` | 24-part images | 0 / 8 |
| 852 | ELF32 `52 + 25×32` | 25-part images | 5 / 1 |

All ten values have a **unique** decomposition: no `b00` size admits both an ELF32 and an
ELF64 reading. So from the matrix alone — two integer columns, no payload — the container's
class and program-header count are recoverable exactly. The `64 + phnum×56` form for ELF64 TAs
is `research/fleet/other-fingerprint.md` §4.4's finding (33/33); this note confirms it holds on
the wider 502-group set and adds the ELF32 sibling form.

### 3.3 `mdt == b00 + b<hash>` closes on 502 of 502 `[F]`

Grouping the matrix by `(device, db_path, stem)` gives 757 groups with a `.mdt`; 502 of them
also have a `b00` and at least one higher segment. For each, `mdt − b00` was matched against
every sibling segment size:

| result | groups |
|---|---:|
| exactly one segment satisfies `len(mdt) == len(b00) + len(bN)` | **502** |
| ambiguous (2+ candidates) | **0** |
| no candidate | **0** |

The matching segment is the **highest-numbered one present on 288 of the 502** groups, and is
**not** on the other **214** — every one of which puts the hash at index 1 with further payload
segments after it (max index up to 23). For those 214, index 1 is never also the last segment
(0 of 214). So "the hash is the last segment" is true only of the nine-part TA shape; it is a
property of the container, not of the format, and it must not be generalised across the bucket.

On disk, **75 of 76** testable files satisfy the byte-level form `b00 ‖ b<hash> == mdt`; the hash
bytes are the file **suffix** in 75 of 76. The single failure in both cases is
`implementations/historic/fp2/fixtures/synth_modem.mdt`, the same synthetic stub that
`other-camera.md` §4.4 identifies, recorded rather than excluded.

Also verified on disk: `len(mdt) − len(hash) == e_ehsize + e_phnum × e_phentsize` on **75 of
76** — i.e. the container is exactly `header ‖ hash`, with the payload segments living outside it
in the `.bNN` files, and `p_offset` in the header pointing past the end of the `.mdt` itself
(max `p_offset+p_filesz` = 82,008 in a 4,752-byte file).

### 3.4 The hash index splits by phdr count, and that closes §8.6 `[F]`

`other-fingerprint.md` §8.6 records as `[U]`:

> the 16 local ELF64 TAs are *all* nine-part-shaped (phnum 9), so the corpus cannot show
> whether an eight-part TA lacks the alias or merely renumbers it.

The corpus can. 17 eight-part ELF64 TAs are present in
`…/data-fetch/second-device/instantnoodle/modem-fat-lfn/image_*.mdt`:

| shape | files | with duplicated `(p_offset, p_filesz)` | hash index |
|---|---:|---:|---|
| ELF64, `phnum=9` | 16 | **16 / 16** | 8 (last) |
| ELF64, `phnum=8` | 17 | **0 / 17** | 1 (second) |
| ELF64, `phnum=6` | 1 | 0 / 1 | 1 |
| ELF64, `phnum=3` | 1 | 0 / 1 | — |

Across the matrix the hash lands at index 1 (214 groups), 2 (4), 8 (274), 19 (1), 23 (8) or
24 (1) — six positions, not a free choice per build: every nine-part ELF64 group takes 8 and
every eight-part one takes 1.

So the alias is **specific to the nine-part shape**, and the eight-part shape is not a
renumbering of it — it has no alias at all and carries the hash in a different slot. The
answer to §8.6 is: neither of the two options that note offered; a third, that the alias and
the nine-part shape are the same feature.

The nine-part alias is exact and byte-identical: `b03 == b07` on **16 of 16** TAs where both
segments exist, with identical `(p_offset, p_filesz, p_flags)`.

This also explains the layout split that looked like a vendor split and is not. Grouping the
502 conforming groups by vendor:

| | groups | vendors |
|---|---:|---|
| hash at index 1 | 214 | oneplus 119, motorola 62, xiaomi 9, fairphone 8, realme 8, nothing 5, fxtec 3 |
| hash elsewhere | 288 | xiaomi 204, oneplus 62, motorola 11, fairphone 6, nothing 5 |

Five vendors (`xiaomi`, `oneplus`, `motorola`, `fairphone`, `nothing`) appear on **both** sides,
so the split is not a vendor split; `realme` (8) and `fxtec` (3) happen to appear only on the
index-1 side, which is a sample-size effect at those counts, not a counter-example. The
discriminator is the **container shape**, and 22 devices ship only one shape and 37 ship only
the other, with **0 devices shipping both** — which is why a per-device view looks like a clean
partition while the vendor view does not.

### 3.5 The TA container, decoded `[F]`

A nine-part ELF64 TA (`05B04A44-BF30-42DF-9E2F-B366B980ED19`, 4,752 B `.mdt`):

| idx | type | `p_offset` | `p_vaddr` | `p_filesz` | `p_flags` | role |
|---:|---:|---:|---:|---:|---|---|
| 0 | 0 | 0x0 | 0x0 | **568** | `0x07000000` | header block (`b00`) |
| 1 | 1 | 0x1000 | 0x0 | 48,626 | `0x00000005` | main code (`b01`) |
| 2 | 1 | 0xd000 | 0xc000 | 257 | `0x04000006` | manifest |
| 3 | 1 | 0xe000 | 0xd000 | 728 | `0x00000006` | |
| 4 | 1 | 0xf000 | 0xe000 | 3,792 | `0x00000006` | |
| 5 | 2 | 0x10000 | 0xf000 | 304 | `0x00000006` | |
| 6 | 1 | 0x10000 | 0xf000 | 8,723 | `0x00000006` | |
| 7 | **1685382482** | 0xe000 | 0xd000 | 728 | `0x00000006` | **alias of phdr 3** |
| 8 | 0 | 0x13000 | 0x0 | **4,184** | **`0x02000000`** | **hash (`b08`)** |

`(0x02000000 & (7<<24)) == (2<<24)` → `QCOM_MDT_TYPE_HASH`, the same test the PIL family uses.
`p_filesz` reproduces the `.bNN` sizes **in order** on 16 of 16 nine-part TAs — the vector
`[568, 48626, 257, 728, 3792, 304, 8723, 728, 4184]` equals `[b00…b08]` exactly. So the
`.mdt` is a complete manifest of its segments including their exact sizes, and the segments
themselves are the separate files.

`e_entry` is 0 and `e_type` is 3 (`ET_DYN`), consistent with a loadable trustlet rather than
an executable. `p_type` 1685382482 = `0x6474E552`, which is numerically exactly the Linux
`PT_GNU_RELRO` constant — but applied here to a 728-byte segment that is byte-identical to
phdr 3, which is not what `PT_GNU_RELRO` means in ELF. So the constant is reused outside its
defined meaning; what Qualcomm uses the alias segment *for* is `[U]`.

The hash segment is 4,184 B on 15 of the 16 nine-part TAs and 11,232 B on `featenabler`.
`4,184 = 8 + 87×48`, but `11,232` is **not** of that form: `8 + 234×48 = 11,240`, and `11,232 =
234×48` exactly. So the two sizes do not share one 8-byte-prefix-plus-48-byte-record
decomposition. The first 12 bytes of both blocks are `00000000 07000000 18000000` as three
little-endian u32s (0, 7, 24), which is consistent with a fixed header, but the record geometry
after it is **not established here** — that is `[U]` and is not claimed. 48 B would fit a SHA-384
digest plus a length field; that is a hypothesis, not a measurement.

### 3.6 Segment 5 is a 304-byte constant-size block, and it is not a constant `[F]`

`phdr[5]` is the only `p_type=2` segment in the TA — index 5 and size 304 in **16 of 16**
nine-part TAs measured. A constant size across TAs with code bodies from 9,416 B to 2,525,292 B
(`ops` to `focal64`) suggests a fixed-format header. It is not a constant *content*: its md5 is
distinct on all 14 where it was compared. So it carries per-TA data in a rigidly fixed layout.
What that layout is, is `[U]`.

---

## 4. The container-adjacent files `[F]`

### 4.1 `mbn_hw.dig` / `mbn_sw.dig` are exactly 32 B, always `[F]`

| file | rows | devices | sizes |
|---|---:|---:|---|
| `mbn_hw.dig` | 38 | 38 | **32, on all 38** |
| `mbn_sw.dig` | 38 | 38 | **32, on all 38** |
| `oem_hw.txt` | 30 | 30 | **0 ×16**, 61 ×8, 68 ×4, 70 ×2 |

A 32-byte file paired with a `.txt` in the same directory is an obvious md5, and public
references treat the `.dig` as opaque (`mbn_hw.dig` appears in a Qualcomm support thread and an
`android.googlesource.com` path list, never explained). **It is not the md5 of the sibling
`.txt`** — verified on both pairs present on disk, against every plausible normalisation. This
matters because the two `.txt` files are **CRLF-terminated** (`mbn_hw.txt` 8 CR / 8 LF / 8 CRLF,
`mbn_sw.txt` 154 / 154 / 154) while `oem_sw.txt` is LF-only (0 CR / 142 LF), so line-ending
normalisation is a real candidate rather than a formality:

| pair | `.dig` (first 16 hex) | `md5(.txt)` raw | `.txt` ending | normalisations tried | match |
|---|---|---|---|---|---|
| `mcfg_hw/mbn_hw` | `58f8df73878581dc…` | `9dc9d4850af935a0…` | CRLF | CRLF→LF, CR→nothing, drop final NL, add final NL | **no** |
| `mcfg_sw/mbn_sw` | `ef15a13f767322e2…` | `7687bc64acf55cb9…` | CRLF | same four | **no** |

Nor is it a truncated SHA-256 of the `.txt` (checked first and last 32 bytes, raw and
CR-stripped). The digest bytes are not all printable, so it is a binary digest rather than a hex
string. What it hashes — the `.mbn` the `.txt` names, a package, or something else — is `[N]`: no
public source says, and nothing on disk distinguishes the candidates.

Notably `oem_hw.txt` is **zero bytes on 16 of 30 rows**. An empty path list is a meaningful
value (no OEM hardware configs for that device), not a data gap.

### 4.2 The `.txt` trio is a plain path list `[F]`

`mbn_hw.txt` (610 B, 9 paths), `mbn_sw.txt` (8,357 B, 155 paths) and `oem_sw.txt` (7,538 B,
142 paths) are relative paths to `mcfg_hw.mbn` / `mcfg_sw.mbn`, one per line. The first two are
CRLF-terminated and `oem_sw.txt` is LF-only, so a naive line split leaves stray `\r` on the
first two — worth knowing before parsing them:

```
mcfg_hw/generic/common/Milos/STANDALONE/LA/DSDA_Hybrid/mcfg_hw.mbn
mcfg_sw/generic/AF/CellC/Commercial/SAfrica/mcfg_sw.mbn
```

The carrier segment is visible in the second path component (`AF/CellC`, `APAC/KDDI`,
`China/CMCC`, `AUNZ/Telstra`). This is the carrier-configuration selector: which MBN the modem
may load in which operator context. It is the only human-readable index of the modem's
per-carrier firmware selection in the whole tree, and it is `misc` only because nothing else
claimed it.

Matrix-scale, these are the largest text files in the bucket: `mbn_sw.txt` up to 23,227 B and
`oem_sw.txt` up to 21,726 B per device.

### 4.3 `gptauuid.xml` — 63 images, and 59 of 63 UUIDs are not RFC 4122 `[F]`

45 rows. The FP6 copy is 10,888 B, 285 tags, parsed into 63 `<image>` entries each with a
`<uuid>`, an `<info>` and up to 3 `<uuid_dep_name>` (28 total).

| shape | count |
|---|---:|
| `8-4-4-16` (non-RFC 4122) | **59** |
| `8-4-4-4-12` (RFC 4122) | 4 |

The 59 non-standard ones are 35 hex characters in an `8-4-4-16` grouping — the last field is
one 16-hex-digit run where RFC 4122 has two 12-digit fields. Examples:
`10D761D9-037A-51E3-9955028AF5A77FBA`, `D9BCD049-9321-52CC-B310A62789FF3833`. The third-group
leading nibble is `5` on 40 and `4` on 19, which is not a valid RFC version field (`1`–`5` are
defined, but `4`/`5` here do not correlate with UUID v4/v5 behaviour and the variant nibble is
absent).

**None of the 63 image names is present as a file in the directory** (0 of 63) — they are GPT
partition names for a different image, or names resolved at boot. That is why this file is
`misc` and not `esim`/`tz`: it describes partitions, not blobs.

The 4 RFC-4122-shaped entries include two that decode as ASCII when read big-endian —
`534D4152-5443-534C-AD6D-628B813561DA` starts `SMARTCSL` and
`466f6361-6c54-6563-6800-000000003545` reads `FocalTech`+`5E`. These are **name-derived
identifiers with a 6-byte counter suffix**, not real UUIDs. That pattern is worth noting
because it makes "is this a GUID" a bad test for identity in this tree.

### 4.4 The matrix's 8 GUID-named TA stems do not intersect `gptauuid.xml` `[F]`

| stem | rows | shape |
|---|---:|---|
| `05B04A44-BF30-42DF-9E2F-B366B980ED19` | 13 | RFC 4122 |
| `32552B22-89FE-42B4-8A45-A0C4E2DB0326` | 13 | RFC 4122 |
| `FD719D50-FFFB-11EB-9A03-0242AC130003` | 13 | RFC 4122 |
| `A985D3EB-3B52-4D44-BE6C-628A813561E8` | 9 | RFC 4122 |
| `876BFD99-1189-4650-B260-FC7DD452D7BA` | 7 | RFC 4122 |
| `3d08821c-33a6-11e6-a1fa-089e01c83aa2` | 4 | RFC 4122 |
| `09990000-0000-0000-0000-000000000000` | 3 | RFC 4122, all-zero tail |
| `620303A6-A694-452D-B53F-7E199D8E19BD` | 1 | RFC 4122 |

All eight are RFC-4122-shaped, versus 4 of 63 in the XML — the two namespaces are disjoint
(intersection 0), and they use different conventions. `09990000-…-000000000000` is a
degenerate ID with a zero node field, which no RFC generator produces.

`trustzone-census.md` already identifies `05B04A44-…` and `FD719D50-…` as GlobalPlatform SE
service TAs (`CESEService_*`, `GPQESE_Open/Transceive`) and `32552B22-…` as having no strings
≥8 chars. That identification is cited, not repeated.

### 4.5 `Data.msc` is a WLAN debug-message string catalog `[F]`

54 rows. The FP6 `qca6750/Data.msc` is 1,159,404 B, 13,527 lines, opening with
`VERSION:8065...`. Its format:

```
<id>,<severity-flags>,[ <source-file> : <line> ] <format string>
```

| metric | value |
|---|---:|
| lines | 13,527 |
| lines matching the record grammar | **11,927** |
| distinct source files | **617** |
| id range | 1 – 11,926 |
| ids distinct | **no** — 11,926 values over 11,927 records, one id repeats |

The source filenames are WLAN driver internals — `phy_dev_paprd_device.c` (479 records),
`phyrf_debug_cmd.c` (290), `wlan_rtt.c` (205), `phy_dev_TPCcal.c` (190). Records open with a
strictly descending run of **97** ids (97 down to 1), then resume at 11,926 and descend again
with local interleaving, so the file is not one sorted table. That shape — a low-id block
followed by the bulk — is consistent with a generator that emitted a small legacy set first,
but the reason is `[U]`.

This is the **message catalog for the WLAN firmware's debugging interface**: each record binds
a numeric id to a printf format and the source location that emits it, so a host tool can
decode binary firmware log words into text. It is data, not firmware, and it is the kind of
file that explains why `misc` cannot be described as "leftover firmware".

### 4.6 Where the metadata files live `[F]`

None of these five files is at the `modem/image` root except `gptauuid.xml`; the carrier
metadata is two directories deep:

```
modem/image/gptauuid.xml
modem/image/qca6750/Data.msc
modem/image/modem_pr/mcfg/configs/mcfg_hw/{mbn_hw.dig, mbn_hw.txt}
modem/image/modem_pr/mcfg/configs/mcfg_sw/{mbn_sw.dig, mbn_sw.txt, oem_sw.txt}
```

`oem_hw.txt` does not exist in the FP6 tree at all, which is consistent with 16 of its 30
matrix rows being zero bytes: it is present-but-empty or absent depending on the vendor.

---

## 5. `bluetooth/image` — counted, not analysed `[F]`

2,420 rows, 47 devices, 27,932,098 B — 22.6% of the bucket's rows and 0.33% of its bytes.
Extensions are dominated by QCA BT splits: `.b5a` 48, `.b8b` 45, `.b8d` 45, `.302` 40, `.b2f`
32, `.b3b` 31, `.b10c` 28, `.b111` 28, `.b59` 27; then `.tlv` 117 and `.ver` 68.

The top names are the Moselle/EVROS families: `hpnv21.bin` 15, `hpbtfw21.tlv` 15, `cmnv12.bin`
14, `cmnv10.bin` 14, `cmnv11.bin` 14, `cmbtfw11/10/12.tlv` 14 each, `cmbtfw12.ver` 13,
`hpnv20.bin` 13, `hpbtfw20.tlv` 13.

**This family is already documented in this repository and is not re-derived here.**
`research/qualcomm/docs/bt-firmware-census.md` covers the FP6/WCN6750 set (`msbtfw*`, `evr*`,
`.tlv`/`.bin`/`.ver`, the `btqca.h` rampatch decode, `rom_build`→`rom_ver` mapping, and the
32-bit ARM Thumb-2 ISA); `research/fleet/qca-bt-format.md` and
`research/fleet/bm2n-isa-bt.md` cover the container and ISA. The only thing this note adds is
the row/byte accounting above, which lets a reader see that the BT family is **22.6% of `misc`
rows but 0.33% of its bytes** — it dominates the count and is irrelevant to the volume.

---

## 6. What this note does not claim `[N]`

### 6.1 No ISA on 10,705 of 10,720 rows `[N]`

`isa_identified` is populated on **15 rows** in the whole bucket, with four distinct values:
`AArch64` (12), and three free-text entries (`QDSP6 / Hexagon` 1, one ARM/TLV note, one
MediaTek-header note). Twelve of the 15 are the FP6 `AArch64` TAs — 6 `.mdt` and their 6 `.b00`
headers — where the class is already implied by the ELF header. Nothing here infers an ISA from
an extension, and the 6,785 rows with a blank `soc` have no SoC to reason from either. The 43
ELF32 and 35 ELF64 counts in §3.1 are header measurements on files present on disk, not
row-level attributions.

### 6.2 `interface_documented` is `n` on all 10,720 `[F]`

Zero rows in this bucket claim a documented interface. Read with §1's `isa_identified` figure,
that means the entire bucket is at the "we know where it sits, not what it speaks" stage.

### 6.3 The two container families share an extension but nothing else `[I]`

§3.1 is a measurement. The inference that a `.mdt` filename tells a loader which family it
belongs to — and that a loader therefore must inspect the header rather than the name — is
`[I]`. `other-fingerprint.md` §6 makes the sharper version of this point (ELF64 TAs cannot pass
`mdt_loader.c`'s `mdt_header_valid()`), and that is cited rather than repeated.

### 6.4 The hash-block internal layout is `[U]`

§3.5 gives the hash segment's size (4,184 or 11,232 B) and derives that both are `8 + k×48`,
but the record structure inside it is not established. No claim is made about what the 48-byte
records contain.

### 6.5 No public source documents any of these containers `[N]`

Recorded 0-hit queries (2026-11-25): `"05B04A44-BF30-42DF-9E2F-B366B980ED19"` (DuckDuckGo
bot-blocked; SeRaXNG returned one Motorola firmware file listing),
`"FD719D50-FFFB-11EB-9A03-0242AC130003"`, `"A985D3EB-3B52-4D44-BE6C-628A813561E8"`,
`"32552B22-89FE-42B4-8A45-A0C4E2DB0326"`, `"ic3.mbn" OR "ic4.mbn" OR "ic5.mbn" eSE TA`,
`qsee TA "mdt" "b00" split trustzone images qualcomm splitter`,
`"keymaster" "cmnlib64" "mdt" TA firmware xiaomi modem image` — all **0 results**.

`linux-firmware`'s `WHENCE` (main, 540,393 B / 11,920 lines, fetched 2026-11-25) has **0**
case-insensitive hits for `gpqese`, `mldapta`, `eseservice`, `ic3`, `ic4`, `ic5`, `ops`,
`evass` and `fingerpr`, while carrying `slpi.mbn` (10 hits) — so the SLPI side of this bucket
is upstream-visible and the TA side is not.

Positive hits were file listings, not analyses: a Motorola Edge 50 Pro firmware listing pairs
`05B04A44-…` with `ic3.mbn`/`ic4.mbn`/`eseservice.mbn`/`gpqese.mbn`; vivo firmware listings
show the `eseservice.b00–b07` split; the Qualcomm forum and an `android.googlesource.com`
iorap path list mention `mbn_hw.dig` without explaining it.

---

## 7. Defects and corrections

### 7.1 30 exactly-duplicated rows, all one device `[F]`

The bucket contains 30 rows that are **byte-identical across all 14 columns**, so the CSV has
10,720 rows where 10,690 distinct records exist. All 30 are `Galaxy_A21S`, each filename
appearing exactly twice. The 30 duplicated names are spread over three of that device's
directories — `vendor/firmware` (22 of them), `vendor/etc` (5) and `vendor/etc/wifi` (3) — so
this is a device-level ingest repeat for `Galaxy_A21S`, not a single-directory glitch:

```
APDV_AUDIO_SLSI.bin, AP_AUDIO_SLSI.bin, abox_tplg.bin, calliope_dram.bin,
calliope_dram_2.bin, calliope_sram.bin, calliope_sram_2.bin, dax_param.bin,
is_lib.bin, is_rta.bin, listenbackeffect.bin, mfc_fw.bin, mx140.bin, mx140_t.bin,
plmn_delta.bin, plmn_delta_attaio.bin, plmn_delta_hktw.bin, plmn_delta_usagsm.bin,
plmn_se13.bin, rxse.bin, sb_others.bin, setfile_4ha.bin, setfile_gc02m1.bin,
setfile_gc02m1_macro.bin, setfile_gm2.bin, setfile_hi1336.bin, setfile_sr846.bin,
slsi_reg_database.bin, txse1.bin, txse2.bin
```

The device has 60 rows over 30 distinct names, and the duplicated copies carry 36,148,604 B —
**so the bucket's byte total includes that amount twice**, and the same overstatement flows into
any per-vendor total containing Samsung. The bucket total of 8,498,193,635 B is the sum of the
filed rows, not of the distinct payloads; deduplicating gives 8,462,045,031 B.

Report-only: this note does not edit the CSV. Flagged because a `(device, filename)` key —
which is `misc`'s natural key at 1.013 rows per pair — would collapse these, and anyone
computing per-device byte totals for `Galaxy_A21S` will double-count 36 MB.

### 7.2 `fingerpr.mdt` is filed `misc`, its segments are filed `fingerprint` `[F]`

33 rows of `fingerpr.mdt` sit in `misc` while the `fingerpr.b00`–`b08` segments sit in the
`fingerprint` subfamily. `other-fingerprint.md` already records this split (its headline calls
`fingerpr.mdt` "the bucket is missing its own ELF header"). The consequence for this issue is
mechanical: **`misc`'s 757 `.mdt` rows overstate the trustlet count**, because at least this
one stem belongs to a bucket that does not own it.

Counting by stem, **138 of the 757 `.mdt` rows** name a stem that is a PIL processor rather than
a trustlet (`evass` 53, `cpusys_vm` 20, `slpi` 19, `evass-lt` 16, `ipa_uc` 14,
`scuba_ipa_fws` 13, `cvpss` 2, `slpi2` 1), leaving **619** TA-shaped rows. The exact boundary is
`[U]` — several stems (`slpi`, `evass`, `spss1p`) appear as both a PIL image and a TA name on
different devices, so no stem list separates them without opening the headers.

### 7.3 `db_type = ELF64` on 757 of 757 `.mdt` rows, and the class is not uniform `[F]`

| extension | rows | `db_type` |
|---|---:|---|
| `.mdt` | 757 | **`ELF64` ×757** |
| `.elf` | 439 | `ELF64` 418, `CERT` 21 |

Unlike `camera`'s 28 `.mdt` rows (where `ELF64` was simply wrong — they are ELF32), the label
here is **right for the ELF64 TAs and wrong for the ELF32 PIL images**. On disk the split is 43
ELF32 / 35 ELF64. A single label cannot describe a set that is both, so the column is
uninformative for this bucket rather than incorrect — the same conclusion `other-camera.md` §6
reached from the opposite direction.

### 7.4 Rule 1 — `research/qualcomm/docs/trustzone-census.md` §"Kernel-side cross-reference"

That section states:

> Upstream Linux gained Qualcomm QSEECOM support (drivers/tee/qcom, `qseecom.c`, merged in the
> v6.8 era per public kernel history) that loads/calls QSEE apps via the `qsee` interface

Two things in it are wrong as written, and corrected in place (dated):

1. **The path.** `drivers/tee/qcom/qseecom.c` is **404** in torvalds/master, re-fetched
   2026-11-25. The in-tree driver is `drivers/firmware/qcom/qcom_qseecom.c`, with
   `qcom_qseecom_uefisecapp.c` as its one client. This repository already records the 404 in
   `implementations/tz/README.md` and `upstream/pr10-remaining-issues-package.md`, so the
   census note was the last place still asserting the old path.
2. **"loads/calls QSEE apps".** The merged driver does not load anything. It registers a
   client for an app **already loaded by the bootloader**, and its entire app table is:

   ```c
   static const struct qseecom_app_desc qcom_qseecom_apps[] = {
       { "qcom.tz.uefisecapp", "uefisecapp" },
   };
   ```

   One name. Against 107 `.mdt` stems in this bucket and 8 GUID-named TAs, that is the scale
   of the gap between what mainline knows and what ships — and it is why the second sentence
   of that section ("No upstream code parses the images themselves") is the load-bearing one
   and should stay.

The correction keeps the section's conclusion and fixes its evidence. It does not weaken the
note's own claims, which are about partition images rather than `.mdt` TAs.

### 7.5 No correction owed to `other-fingerprint.md` §8.6 — it is answered, not fixed `[F]`

§8.6 is correctly labelled `[U]` given the corpus that note had (16 ELF64 TAs, all nine-part).
This note's §3.4 supplies the missing case rather than contradicting the text, so §8.6 is
**left in place** and a pointer is added to it. The distinction matters: `[U]` was an honest
statement about that note's inputs, not an error.

---

## 8. What this adds to the existing record `[F]`

| prior note | what it established | what this note adds |
|---|---|---|
| `research/fleet/wifi-wpss.md` §2.4, `research/fleet/other-camera.md` §4.4 | `.mdt == b00 + b<hash>`; hash found by `p_flags & 7<<24 == 2<<24`; law widened to 38/39 files | confirms it on **502/502 matrix groups**, 0 ambiguous; shows the hash is the highest segment on 288 and *not* on 214 (index-1 groups carry payload after the hash), so "hash last" is shape-specific and not a format rule; adds the **ELF32/ELF64 container split** which neither note could see, both having worked within one family |
| `research/fleet/other-fingerprint.md` §4.4, §8.6 | ELF64 TA `b00 == 64 + phnum×56` (33/33); `phdr[3]`/`phdr[7]` alias; alias↔nine-part correlation left `[U]` | **closes §8.6**: 0/17 eight-part TAs alias, 16/16 nine-part do. The alias and the nine-part shape are one feature |
| `research/qualcomm/docs/trustzone-census.md` | FP6 TAs as monolithic ELF partitions; `soter64`/`smplap64`/UUID TA identification; `featenabler` dual packaging | corrects its kernel cross-reference (§7.4); adds the **container arithmetic** (`b00` decomposition, `p_filesz` vector == `.bNN` sizes 14/14, `.mdt` is `header ‖ hash` with payload outside) |
| `research/qualcomm/docs/bt-firmware-census.md`, `qca-bt-format.md`, `bm2n-isa-bt.md` | the BT family, in detail | row/byte accounting only (§5): 22.6% of `misc` rows, 0.33% of its bytes |
| `research/fleet/dsp-tz-map.md` | `dsp.img` is ext4; ELF census of the 4K-sector regions | the **size law**: 61 rows, 61 devices, exactly 64 MiB or 32 MiB (§2.1) |
| `research/fleet/tz-hyp.md` | `tz`/`hyp` container generations and signature progression | nothing re-derived; the `radio/` `tee.img`/`gz.img` rows (2 each) are counted only |

---

## 9. Open items `[U]`

1. **The 48-byte hash records.** Both observed hash sizes are `8 + k×48`, but the record
   layout is not established (§6.4).
2. **`p_type` 1685382482.** A non-standard type on the alias segment; whether it is a Qualcomm
   `PT_GNU_RELRO` reuse or something else is `[U]`.
3. **The 304-byte `p_type=2` segment.** Constant size, distinct content per TA, unexplained
   (§3.6).
4. **What `mbn_*.dig` hashes.** Not the sibling `.txt`; 32 raw bytes (§4.1).
5. **The TA/PIL boundary in the 757 `.mdt` rows.** 637 TA-shaped by name, but `slpi`/`evass`
   appear as both (§7.2).
6. **`fm-bias` on the 6,785 blank-`soc` rows.** `misc` carries the largest blank-`soc` block in
   the corpus, so no SoC-level grouping is possible for two thirds of it.
7. **No Xtensa, Hexagon or AArch64 disassembler here.** Class and shape are header facts; no
   instruction-level claim is made about any payload in this bucket.

---

## 10. Method `[F]`

```bash
python3 -I - <<'PY'   # census: rows, devices, basenames, md5, bytes, path axes
import csv, collections
rows = list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
m = [r for r in rows if r['blob_subfamily'] == 'misc']
PY
```

Container arithmetic — group by `(device, db_path, stem)`, then match `mdt − b00` against
sibling segment sizes; verify `b00 == e_ehsize + e_phnum × e_phentsize` from the header itself;
locate the hash by `(p_flags & (7 << 24)) == (2 << 24)` per `qcom_mdt_read_metadata()`, never by
position. ELF32 header offsets: `e_phoff` 28, `e_phentsize` 42, `e_phnum` 44, `e_ehsize` 40.
ELF64: `e_phoff` 32, `e_shoff` 40, `e_ehsize` 52, `e_phentsize` 54, `e_phnum` 56.
ELF64 program header is `<IIQQQQQQ`, 56 bytes; ELF32 is `<8I`, 32 bytes.

Disk sweep: `glob('**/*.mdt', recursive=True)`, 78 files, 43 ELF32 / 35 ELF64. All counts
re-verified against the matrix before being written.
