# Google Tensor GS201 (Tensor G2) — GPU core identification and firmware

Issue #2017. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative. Every number is from a command run **2026-11-22** against
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 rows),
`linux-firmware` `main` (`WHENCE`, 540,253 B), `torvalds/linux` master at
`4843f6873f7c4835e62f2c73ba0fd538e57a2f22`, and the postmarketOS `pmaports`
tree on GitLab.

This is the **first Mali part** in the per-SoC GPU family. The six documents
that precede it (MSM8998, SM4375, SM7250, SM7325, SM8250, SM8350) are all
Qualcomm Adreno, and every structural rule they establish — `a6xx` chip IDs,
`.mdt` split segments, `a660_zap` containers, GMU block containers — has **no
counterpart here**. The Mali path is a different driver (`panthor`), a different
firmware naming scheme, and a different boot chain.

Companion documents:

| document | owns | this note |
|---|---|---|
| `derekross/omarchy-mobile` `device/cheetah/GPU-PLAN.md` | **the working GS201 GPU port**: Mali-G710 / arch 10.8.6 / r0p0 identification, `GPU_ID` `0xa8620004`, register base, IRQs, CMU_G3D clocks, the Panthor + Mesa 26.2.4 path | cites §1 and §3; adds the matrix census, the five-revision family, the linux-firmware gap, and the mainline/Mesa/postmarketOS absences |
| `research/soc/Qualcomm-*-gpu.md` (6) | the Adreno per-SoC notes and the house format | format precedent only; no technical overlap |
| `research/fleet/gpu-bdwlan.md` | Adreno `bdwlan` board data | adjacent family, not this SoC |
| `research/soc/Qualcomm-SM8350-Snapdragon-888-soc.md` | the SoC-package companion pattern (#823) | format precedent |

**No GS201 payload exists in this workspace.** `data-fetch/` holds
`second-device/instantnoodle` (SM8250) and `second-device/larry` (SM6375) only.
Every payload statement below is matrix metadata — filename, size, md5 — and
**no ELF or container parsing is claimed for this SoC** [N].

## 0. Verdict

| question | answer | class |
|---|---|---|
| SoC identity | GS201 = Tensor G2 = `s5p9855`; device codenames `panther` (Pixel 7), `cheetah` (7 Pro), `lynx` (7a), `felix` (Fold), `tangorpro` (Tablet) | [F] |
| GPU | **ARM Mali-G710**, arch **10.8**, product major 2, marketed **MP7** — not Adreno, not PowerVR | [F] |
| GPU arch revision | **r0p0**, status 4, `GPU_ID` `0xa8620004` — cited from prior art, and consistent with the matrix's `r50p0`…`r54p0` naming | [F] cited, [I] consistency |
| Driver | `panthor` (`drivers/gpu/drm/panthor/`), `arm,mali-valhall-csf` | [F] |
| Firmware the driver requests | `arm/mali/arch10.8/mali_csffw.bin` | [F] |
| Firmware the corpus holds | `mali_csffw-r{50,51,52,53,54}p0.bin`, all 278,528 B, 5 revisions × 5 devices | [F] |
| Do those names ever meet? | **No.** linux-firmware has 0 `mali_csffw-r*` files; the driver builds its path from the arch number | [F] |
| Mainline GS201 support | **None.** `dts/google/` holds only Tensor G5; binding lists 3 non-Google SoCs | [F] |
| Mesa support | **Partially.** The model table has no `PAN_PROD_ID(10,8,2)` row, so both Gallium and PanVK refuse the device; the fix is a 2-line table row, published | [F] |
| postmarketOS GS201 support | **None.** 9 candidate packages probed, all 404 | [N] |
| Boot chain | ARM TF-A shaped (`bl1`/`bl2`/`bl31`/`tzsw`/`pvmfw`/`abl`), **not** Qualcomm shaped | [F] |
| Upstream firmware size vs corpus | Upstream arch10.8 is **4,096 B larger** than the corpus's 278,528 B, and arch11.8 is 4,096 B larger than G3/G4's 294,912 B — invariant, unexplained | [F] measured, [H] cause |

The three headline findings are the **name-space collision** (§4: the corpus's
filenames and the driver's filenames are different languages that never
intersect), the **generation split** (§3: GS201 and G3/G4 firmware differ by
exactly 16,384 B with zero digest overlap — and upstream arch10.8→arch11.8
differs by the same 16,384 B, §4.1), and the **narrow Mesa gap** (§5.4: one
missing product-id row, not a missing driver).

## 1. The GPU is an ARM Mali-G710 — and three independent sources agree

**Verdict: ARM Mali-G710, Valhall CSF generation, arch 10.8, product major 2,
r0p0, marketed as MP7.** Not Adreno, not PowerVR, not Immortalis.

| # | evidence | class |
|---|---|---|
| 1 | **Prior art `dmesg`.** `omarchy-mobile` `GPU-PLAN.md` §1 records `dmesg.txt:4006`: "GPU identified as 0x2 arch 10.8.6 r0p0 status 4", and derives `GPU_ID` `0xa8620004` (Panthor prints `id 0xa862`). Status dated 2026-10-12. | [F] cited |
| 2 | **Public specification.** Every spec sheet for Tensor G2 lists **Mali-G710 MP7** (Android Police, 91mobiles, NotebookCheck, XDA — fetched 2026-11-22). XDA's G2-vs-G1 table gives "ARM Mali G710 MP07" against G1's "Mali G78 MP20". | [F] cited |
| 3 | **The corpus's own filenames.** All five firmware revisions are named `mali_csffw-…`, i.e. **Mali CSF firmware**. `csffw` = Command Stream Frontend firmware, the Valhall-CSF/kbase interface. No Qualcomm Adreno SoC in this matrix carries a `mali_*` file, and no Mali SoC carries an `a6xx` file (§3.2). | [F] |

The three are independent: (1) is a runtime register read on the device, (2) is
the vendor's marketing name, (3) is a filename convention in the firmware
corpus. They agree.

### 1.1 Decoding `GPU_ID` `0xa8620004` against the driver's own macros

The prior art states the `dmesg` line and the raw ID separately. They can be
reconciled exactly, because the kernel defines the field layout in
`drivers/gpu/drm/panthor/panthor_gpu_regs.h:10-16`:

```c
#define   GPU_ARCH_MAJOR(x)   ((x) >> 28)
#define   GPU_ARCH_MINOR(x)   (((x) & GENMASK(27, 24)) >> 24)
#define   GPU_ARCH_REV(x)     (((x) & GENMASK(23, 20)) >> 20)
#define   GPU_PROD_MAJOR(x)   (((x) & GENMASK(19, 16)) >> 16)
#define   GPU_VER_MAJOR(x)    (((x) & GENMASK(15, 12)) >> 12)
#define   GPU_VER_MINOR(x)    (((x) & GENMASK(11, 4)) >> 4)
#define   GPU_VER_STATUS(x)   ((x) & GENMASK(3, 0))
```

Applying them to `0xa8620004`:

| field | bits | value |
|---|---|---|
| `ARCH_MAJOR` | `0xa` | **10** |
| `ARCH_MINOR` | `0x8` | **8** |
| `ARCH_REV` | `0x6` | **6** |
| `PROD_MAJOR` | `0x2` | **2** |
| `VER_MAJOR` | `0x0` | r**0** |
| `VER_MINOR` | `0x00` | p**0** |
| `VER_STATUS` | `0x4` | 4 |

That is exactly "arch 10.8.6, product 0x2, r0p0, status 4" [F]. The decode is
arithmetic on a cited value, not a new measurement, and it matters twice: arch
10.8 is the string the driver interpolates into the firmware path (§4.2), and
`PROD_MAJOR` 2 is the key the model table looks up (§1.2).

### 1.2 The driver's model table maps it to "Mali-G710" by name

`drivers/gpu/drm/panthor/panthor_hw.c:16-17` and `:130-131`:

```c
#define GPU_PROD_ID_MAKE(arch_major, prod_major) \
	(((arch_major) << 24) | (prod_major))
...
	case GPU_PROD_ID_MAKE(10, 2):
		return "Mali-G710";
```

`GPU_PROD_ID_MAKE(10, 2)` = `0x0a000002`, which is the `(arch_major, prod_major)`
pair from §1.1. So the kernel itself will print **"Mali-G710"** for this part,
and the binding requires `arm,mali-valhall-csf` alongside a SoC-specific
compatible that does not exist for Google (§5).

The full table (`panthor_hw.c:120-170`) places G710 at the head of the Valhall-10
generation, and it is worth recording because the naming is not monotonic in the
product id [F]:

| `GPU_PROD_ID_MAKE` | name |
|---|---|
| `(10, 2)` | **Mali-G710** |
| `(10, 3)` | Mali-G510 |
| `(10, 4)` | Mali-G310 |
| `(10, 7)` | Mali-G610 |
| `(11, 2)` | Mali-G715-Immortalis / Mali-G715 (split on core count ≥ 10 + ray intersection, else ≥ 7) |
| `(11, 3)` | Mali-G615 |
| `(12, 0)` | Mali-G720-Immortalis / Mali-G720 (≥ 10 + RT, else ≥ 6) |
| `(12, 1)` | Mali-G620 |
| `(13, 0)` | Mali-G925-Immortalis / Mali-G725 |
| `(13, 1)` | Mali-G625 |
| `(14, 0)` / `(14, 1)` / `(14, 3)` | Mali-G1-Ultra / -Premium / -Pro |

Two things matter here. First, the product major is a **silicon-configuration
code, not a rank**: `(10,2)` is G710, the most capable Valhall-10 part, while
`(10,3)`/`(10,4)` are the *lower* G510/G310 and `(10,7)` is G610. Reading the
number as a tier would invert the ordering. Second, the switch is on
`GPU_PROD_ID_MAKE(GPU_ARCH_MAJOR, GPU_PROD_MAJOR)` — **arch major and product
major only** — with arch minor and the whole revision field dropped. So the
model name is a function of two fields, not of the whole `GPU_ID` [F].

That has a direct consequence for Mesa (§5.4): Mesa keys on
`PAN_PROD_ID(arch_major, arch_minor, prod_major)` — **three** fields, including
arch minor — so the kernel's key `(10,2)` and Mesa's key `(10,8,2)` are not the
same number in different bases; they are different *functions*. A kernel that
names the part does not imply a Mesa that accepts it, and that is exactly the
state measured here.

## 2. What the matrix holds — the slice, measured

**225 rows / 5 devices / 1,014,982,980 B / 65 distinct filenames.**

| device | codename | rows | files | bytes | families |
|---|---|---:|---:|---:|---|
| `Pixel_7a` | `lynx` | 49 | 49 | 222,815,520 | boot 9, other 30, gpu 5, wifi 3, tz 1, modem 1 |
| `Pixel_Tablet` | `tangorpro` | 46 | 46 | 136,697,788 | boot 9, other 30, gpu 5, wifi 1, tz 1 |
| `Pixel_7_Pro` | `cheetah` | 45 | 45 | 219,054,998 | boot 9, other 28, gpu 5, wifi 1, tz 1, modem 1 |
| `Pixel_7` | `panther` | 44 | 44 | 218,744,333 | boot 9, other 27, gpu 5, wifi 1, tz 1, modem 1 |
| `Pixel_Fold` | `felix` | 41 | 41 | 217,670,341 | boot 9, other 24, gpu 5, wifi 1, tz 1, modem 1 |

Family totals across the slice:

| family | rows | files | bytes | share |
|---|---:|---:|---:|---:|
| `other` | 139 | 45 | 154,361,687 | 15.2% |
| `boot` | 45 | 9 | 510,562,304 | **50.3%** |
| `gpu` | 25 | 5 | 6,963,200 | 0.7% |
| `wifi` | 7 | 4 | 11,872,749 | 1.2% |
| `tz` | 5 | 1 | 1,740,800 | 0.2% |
| `modem` | 4 | 1 | 329,482,240 | **32.5%** |

**The GPU is 0.69% of the bytes.** `boot` and `modem` are 82.76% between them, and
both are dominated by single large images (`boot.img` 67,108,864 B ×5;
`modem.img` 82,370,560 B ×4). The family a reverse engineer wants is 6,963,200 B
of 1,014,982,980 B [F].

Every device contributes exactly **9 boot images** and exactly **5 GPU images** —
the slice is unusually regular, because all five devices are the same SoC with
the same partition layout. `Pixel_Tablet` is 136.7 MB against the others' ~218 MB
purely because it has no `modem.img` [F].

## 3. The GPU firmware family: five revisions, one size, two generations

### 3.1 Five revisions × five devices, all 278,528 B, all byte-identical

The slice's 25 GPU rows are a complete 5×5 grid:

| revision | bytes | md5 | devices |
|---|---:|---|---:|
| `mali_csffw-r50p0.bin` | 278,528 | `4887611e86d3dc361eab5aeb2255e3b8` | 5 |
| `mali_csffw-r51p0.bin` | 278,528 | `fcb3378116154b4e21a7f0bbb8bbc610` | 5 |
| `mali_csffw-r52p0.bin` | 278,528 | `acd5ecb0d4cc0a79c5dd03cc78db370f` | 5 |
| `mali_csffw-r53p0.bin` | 278,528 | `56b489dd03afc0de337049e231489878` | 5 |
| `mali_csffw-r54p0.bin` | 278,528 | `7d1d546c5ec3455b6ade6f3501cb54ff` | 5 |

Three facts follow, and the first is the interesting one:

1. **Each revision has exactly one digest across all five devices.** `r50p0` on
   `panther` is the same bytes as `r50p0` on `tangorpro`. So the five files are
   **five alternative builds of one firmware**, not five device-specific ones.
   A vendor tree ships all five and selects at runtime; the matrix captured the
   whole set [F].
2. **All five are exactly 278,528 B** = 272.0 KiB = 68 × 4096. The size does not
   vary by revision, which means the five builds differ in content but not in
   layout — consistent with one image with per-revision patch content [I].
3. **Revision patch level is `p0` on all five.** The corpus has `r50p0` through
   `r54p0` and **never** a non-zero patch level (§3.3).

### 3.2 The GPU is the only family where every device agrees

Of the 45 filenames present on more than one device, **19 are byte-identical and
26 differ**. The five `mali_csffw-*` files are in the identical set — and they
are the *only* GPU-related filenames at all, so **the GPU firmware is the single
most stable family in the slice** [F].

The identical set is worth listing in full, because it separates
generation-invariant artifacts from device-customised ones:

| byte-identical across all 5 devices (19) |
|---|
| `mali_csffw-r50p0.bin`, `-r51p0`, `-r52p0`, `-r53p0`, `-r54p0` |
| `modem.img` (82,370,560 B) |
| `mfc_fw.bin` (720,072 B), `edgetpu-janeiro.fw` (1,011,648 B) |
| `st54j_fw.bin`, `d3m2.ec.bin`, `evt.ec.bin`, `proto11.ec.bin` |
| `libchre_log_database.bin`, `focaltech_ts_fw.bin` |
| `esim-full-v0.img`, `esim-full-v1.img`, `esim-full-v0-security.img`, `esim-full-ofl-v1.img` |
| `MICRONMT128GAXAT2U310104_MICRONMT256GAXAT4U310104.img` |

| divergent (26) |
|---|
| every boot-chain image (`abl`, `bl1`, `bl2`, `bl31`, `boot`, `dtbo`, `init_boot`, `pvmfw`, `tzsw`, `vbmeta`) |
| `aoc.bin`, `gsa.img`, `ldfw.img`, `pbl.img` |
| `fw_bcmdhd.bin` |
| the `cs35l41` audio-amp set (`R-` variants) and `cs40l26` set |
| `goodix_firmware.bin`, `st54j_conf_PROTO1.bin` |

The pattern is clean: **SoC-level and silicon-level artifacts are identical
(GPU, modem, TPU, NFC, storage); device-level and board-level artifacts diverge
(boot images, audio amps, touch controllers, Wi-Fi calibration)** [F] for the
grouping, [I] for the reading.

### 3.3 The `r54p3` build that actually matters is not in the corpus

The prior art records the **stock vendor** firmware as
`mali_csffw-r54p3.bin` (kbase r54p3 ABI) from `vendor-firmware.txt` and
`dmesg.txt:3972` on `cheetah`.

**The corpus does not contain `r54p3`.** It contains `r54p0`. Patch level 0, not
3. Every one of the five revisions is `p0`:

```
r50p0  r51p0  r52p0  r53p0  r54p0      ← corpus, 278,528 B each
r54p3                                  ← prior art's stock listing, absent
```

So the matrix captured a **different build of the same revision series** than the
device's own vendor partition reports. Two readings, and I cannot choose between
them from metadata alone:

- the matrix's dumps came from a firmware package or an OTA payload whose
  `r54p0` predates the `r54p3` the device later ran [H], or
- `r54p0` and `r54p3` are both present on a real device in different partitions
  (`vendor/firmware` vs a `_a`/`_b` slot or a recovery copy) and the census
  collected only one [H].

What is **not** in doubt: a reader who takes the matrix's five files as "the
GS201 GPU firmware" will not have the file the prior art says the device
actually boots [F] for the absence, [N] for the explanation.

### 3.4 The generation split: GS201 and G3/G4 are 16,384 B apart, with no overlap

The matrix holds Mali firmware for four Tensor labels. Measured:

| SoC label | rows | size | distinct md5 |
|---|---:|---:|---:|
| `Google Tensor GS201` | 25 | **278,528** | 5 |
| `Google Tensor G3` | 25 | **294,912** | 5 |
| `Google Tensor G4` | 5 | **294,912** | 5 |
| *(blank)* — `Pixel_9A`, `Pixel_9_Pro_XL` | 10 | **294,912** | 5 |

`294,912 − 278,528 = 16,384` = **exactly 16.0 KiB**. And the digest sets are
completely disjoint:

```
GS201 ∩ G3 = 0
GS201 ∩ G4 = 0
G3   ∩ G4 = 5      ← G3 and G4 ship identical Mali firmware
```

Three conclusions:

1. **The Mali firmware changed by one 16 KiB block between Tensor G2 and G3**,
   and not at all between G3 and G4 [F]. That is consistent with the public
   record: G3 and G4 both ship a **Mali-G715 MP7** (XDA, Beebom, Wccftech,
   fetched 2026-11-22), so the same GPU firmware serving both is expected —
   while G2's G710 is a different product and gets a different build [F]/[I].
2. **G3 and G4 sharing all five digests is a real invariant, not a copy error.**
   `Pixel_8` (G3), `Pixel_9` (G4) and the blank-labelled `Pixel_9A` all carry
   `27c9b2b908b9…` for `r50p0` and the same pattern for the other four [F].
3. **A 16 KiB step is small enough that the two builds could be confused.** Any
   pipeline that deduplicates firmware by size alone, or that assumes "Mali CSF
   firmware is ~288 KiB", will silently mix G2 and G3 images. Size is a
   generation discriminator here only because the delta is a clean power of two
   — and it is a **fragile** one, since a future revision could change size
   without changing generation [I].

### 3.5 The blank and mislabelled rows in §3.4's table

The §3.4 table has four rows and two of them are not clean SoC labels. Both are
recorded in full in §9.1; the short version, because it affects how §3.4 should
be read [F]:

| device | label | actual SoC (public) |
|---|---|---|
| `Pixel_9A` | **blank** | Tensor G4 |
| `Pixel_9_Pro_XL` | **blank** | Tensor G4 |
| `Pixel_9_Pro` | `Google Tensor G3` | Tensor G4 |
| `Pixel_9_Pro_Fold` | `Google Tensor G3` | Tensor G4 |

The consequence for §3.4 is only that the "blank" row (10 rows) and the "G3" row
(25 rows) both contain G4 devices. **It does not disturb the size law**: every
one of those rows is 294,912 B with the same five digests, so the generation
split holds regardless of what the label says — the digests are the reliable
key, which is the whole point of §9.1. GS201's own five devices are correctly
labelled, so §2, §3.1–§3.4 and §4–§8 are unaffected [F].

## 4. Two firmware name-spaces that never meet

This is the most important structural finding in the note, and it is a
consequence of the GPU being Mali rather than Adreno. On the Qualcomm side the
driver and the corpus speak the same language: `a660_zap.mbn`, `cdsp.mdt`,
`qdsp6sw.mbn` are names the kernel's own DT and the vendor tree both use. **On
the Mali side they do not.**

### 4.1 linux-firmware ships seven arch-addressed images, and zero `rNNpN` names

`WHENCE` (`main`, 540,253 B, fetched 2026-11-22), the `Driver: panthor` block at
`:11638`:

```
Driver: panthor - Arm Mali CSF firmware
File: arm/mali/arch10.8/mali_csffw.bin      Version: arch10.8
File: arm/mali/arch10.10/mali_csffw.bin     Version: arch10.10
File: arm/mali/arch10.12/mali_csffw.bin     Version: arch10.12
File: arm/mali/arch11.8/mali_csffw.bin      Version: arch11.8
File: arm/mali/arch12.8/mali_csffw.bin      Version: arch12.8
File: arm/mali/arch13.8/mali_csffw.bin      Version: arch13.8
File: arm/mali/arch14.8/mali_csffw.bin      Version: arch14.8
```

Seven entries, licence `LICENCE.mali_csffw` (`:11654`). `grep -c "mali_csffw-r"`
= **0** — the string does not occur in `WHENCE` at all [F]. And the corpus's
entire naming scheme is `mali_csffw-rNNpN.bin`. **The two vocabularies share the
stem `mali_csffw` and nothing else.**

I fetched all seven upstream images to compare sizes (2026-11-22):

| upstream path | bytes | pages (4096) | md5 | magic |
|---|---:|---:|---|---|
| `arm/mali/arch10.8/mali_csffw.bin` | 282,624 | 69 | `cd95e83312eec65ff523025b52badb4a` | `6e3af1c3` |
| `arm/mali/arch10.10/mali_csffw.bin` | 282,624 | 69 | `cd95e83312eec65ff523025b52badb4a` | `6e3af1c3` |
| `arm/mali/arch10.12/mali_csffw.bin` | 282,624 | 69 | `cd95e83312eec65ff523025b52badb4a` | `6e3af1c3` |
| `arm/mali/arch11.8/mali_csffw.bin` | 299,008 | 73 | `64fc3695e92756f111f6bc7287ff1569` | `6e3af1c3` |
| `arm/mali/arch12.8/mali_csffw.bin` | 307,200 | 75 | `15f238b54dbf8aadcbccab55c47c05ac` | `6e3af1c3` |
| `arm/mali/arch13.8/mali_csffw.bin` | 311,296 | 76 | `98bd8fc1e193f03917fb6e87a2b0529c` | `6e3af1c3` |
| `arm/mali/arch14.8/mali_csffw.bin` | 344,064 | 84 | `bc2ee99629e05c1c9e88d442680e11aa` | `6e3af1c3` |

Three things fall out [F]:

1. **All seven share one magic, `6e3af1c3`**, and every size is a whole number of
   4096-byte pages. They are one container format, differentiated by content.
2. **arch10.8, arch10.10 and arch10.12 are byte-identical** — one digest,
   `cd95e833…`. The three Valhall-10 arch directories are copies of the same
   image. That is exactly the symlink pattern the prior art recorded on a real
   install (`GPU-PLAN.md:268-270`: `arch10.8/mali_csffw.bin -> ../arch10.10/mali_csffw.bin`),
   now confirmed as content-identical at the source rather than only in a
   distribution's packaging [F].
3. **The upstream sizes are one page larger than the corpus's.** arch10.8 is
   282,624 B = 69 pages; the GS201 corpus files are 278,528 B = 68 pages. Exactly
   **4,096 B** apart. And arch11.8 is 299,008 B = 73 pages against the G3/G4
   corpus's 294,912 B = 72 pages — again **exactly 4,096 B** [F].

That last point is the interesting one and it is *not* something I can explain
from metadata. Two readings [H]:

- the vendor ships the CSF image **without** a 4 KiB trailing page (a signature,
  a padding block, or a metadata page) that upstream appends or retains, or
- the corpus's dumps are **truncated by one page** — a plausible collection
  artefact if the capture tool sized the file from a partition entry rather than
  the ELF/container header.

I cannot choose between them without the bytes, and I do not have GS201 payload
in this workspace (§0) [N]. What I *can* say is that the 4 KiB delta is
**invariant across both generations**: G2 is one page below arch10.8, and G3/G4
is one page below arch11.8. A truncation artefact would plausibly be constant
like this; a vendor-vs-upstream packaging difference would too. The observation
does not discriminate.

Note also that the **16,384 B generation step from §3.4 survives this**: the
corpus's G2→G3 delta (16,384 B) and the upstream arch10.8→arch11.8 delta
(299,008 − 282,624 = 16,384 B) are **the same number**. The generation step is
real in both name-spaces, which strengthens §3.4 considerably [F].

### 4.2 The driver builds its path from the arch number, so it can never open the corpus's files

`drivers/gpu/drm/panthor/panthor_fw.c`:

```c
:31   #define CSF_FW_NAME "mali_csffw.bin"
...
:811  snprintf(fw_path, sizeof(fw_path), "arm/mali/arch%d.%d/%s",
:812           (u32)GPU_ARCH_MAJOR(ptdev->gpu_info.gpu_id),
:813           (u32)GPU_ARCH_MINOR(ptdev->gpu_info.gpu_id),
:814           CSF_FW_NAME);
:816  ret = request_firmware(&fw, fw_path, ptdev->base.dev);
```

and the `MODULE_FIRMWARE` list at `:1559-1565` is the same seven arch paths as
`WHENCE`. The two are consistent by construction: the driver asks for
`arm/mali/arch10.8/mali_csffw.bin` and linux-firmware ships exactly that file.

For GS201, `GPU_ARCH_MAJOR` = 10 and `GPU_ARCH_MINOR` = 8 (§1.1), so the request
is `arm/mali/arch10.8/mali_csffw.bin` — **and the corpus's
`mali_csffw-r54p0.bin` is never requested by any upstream code path** [F].

This is a hard, mechanical conclusion, not a stylistic one. `request_firmware()`
takes the literal string built at `:811`; there is no fallback that tries
`-rNNpN` variants, and `CSF_FW_NAME` is a compile-time constant. **A GS201 owner
who copies the corpus's five files into `/lib/firmware` gets a Panthor that
fails to load**, because it will look for `arch10.8/mali_csffw.bin` and find
nothing. Conversely, the arch-addressed image linux-firmware already ships is the
one that works — which is precisely what the prior art reports
(`GPU-PLAN.md:265-277`: the installed `arch10.8` file loads, and the vendor's
`r54p3` blob is "a kbase-ABI blob for r54p3, so do not try it with Panthor") [F]
cited.

So the corpus's GPU family is **documentation of what the vendor ships, not a
drop-in for upstream**. That distinction matters for anyone using this matrix as
a firmware source: for Adreno the two roles coincide, for Mali they do not.

### 4.3 What the corpus's `rNNpN` names actually mean

The `r50p0`…`r54p0` numbering is **kbase DDK revision** numbering — the
proprietary Mali kernel driver's release train — not Panthor's. The prior art
states the stock device file is `mali_csffw-r54p3.bin` and calls it a "kbase
r54p3 ABI" blob. That reading is consistent with everything measured here [F]
for the naming, [I] for the ABI claim:

- the corpus holds five consecutive revisions of one product line, all one size
  (§3.1), which is what a DDK release train looks like;
- the driver-side model table (§1.2) keys on **product ID**, not revision, so
  Panthor is indifferent to which `rNNpN` the vendor selected;
- the vendor selects at runtime, which is why all five ship on all five devices
  (§3.1).

The corpus's `p0`-only coverage (§3.3) therefore means the matrix captured five
*base* releases and missed the patch levels the shipping devices actually ran.
That is a collection gap, not a vendor gap [I].

## 5. Upstream support: the kernel knows the part, mainline does not know the SoC

Two different questions with two different answers, and conflating them is the
easy mistake here.

### 5.1 The GPU driver supports the part — fully, today

`panthor` is mainline, the `arm,mali-valhall-csf` binding exists, and the
kernel's own model table names the part:

```c
panthor_hw.c:16-17   #define GPU_PROD_ID_MAKE(arch_major, prod_major) \
                             (((arch_major) << 24) | (prod_major))
panthor_hw.c:130-131     case GPU_PROD_ID_MAKE(10, 2):
                             return "Mali-G710";
```

`GPU_PROD_ID_MAKE(10,2)` = `0x0a000002`, which is the `(arch_major,
prod_major)` pair decoded from `0xa8620004` in §1.1. So **the driver will print
"Mali-G710" for a GS201 GPU and will load `arm/mali/arch10.8/mali_csffw.bin`**,
which linux-firmware ships (§4.1). The GPU half of the problem is solved
upstream [F].

### 5.2 The binding lists three SoC compatibles and none is Google's

`Documentation/devicetree/bindings/gpu/arm,mali-valhall-csf.yaml` (4,970 B,
fetched 2026-11-22), `:19-24`:

```yaml
  compatible:
    oneOf:
      - items:
          - enum:
              - mediatek,mt8196-mali
              - nxp,imx95-mali            # G310
              - rockchip,rk3588-mali
          - const: arm,mali-valhall-csf
```

Exactly **three** SoC-specific compatibles, and the string `google` does not
occur anywhere in the file [F]. A GS201 GPU node therefore cannot be described
in a mainline DT without adding a compatible — the generic
`arm,mali-valhall-csf` alone is not sufficient, because the binding requires the
`items` pair.

This is the precise upstream gap: **not the driver, the binding.** That is a
much smaller and more tractable delta than "mainline doesn't support the GPU",
and it is the one the prior art's own TODO points at.

### 5.3 Mainline has no GS201 device tree at all — it jumps GS101 → G5

`arch/arm64/boot/dts/google/` holds **6** entries (GitHub contents API,
`ref=master`, 2026-11-22):

| entry | bytes |
|---|---:|
| `Makefile` | 140 |
| `lga.dtsi` | 8,355 |
| `lga-pixel-common.dtsi` | 295 |
| `lga-blazer.dts` | 254 |
| `lga-frankel.dts` | 253 |
| `lga-mustang.dts` | 260 |

Every one is Tensor **G5** (`laguna`) — `lga.dtsi` opens with
`Google Tensor G5 (laguna) SoC rev B0`, `Copyright 2024-2025 Google LLC`, and
contains **no** `gpu`, `mali` or `panthor` node at all (`grep` = 0 hits) [F].

Code search against `torvalds/linux` master, 2026-11-22:

| query | total | note |
|---|---:|---|
| `repo:torvalds/linux GS201` | **0** | — |
| `repo:torvalds/linux google,gs201` | **0** | — |
| `repo:torvalds/linux tensor g2` | 9 | all GS101 or unrelated: `gs101-pmu.c`, `phy-gs101-ufs.c`, `phy-samsung-ufs.h`, `exynos-regs-pmu.h`, `gaudi2_regs.h` |

So mainline's Tensor coverage is **G1 (GS101, partial) and G5 (laguna, a DT
only)** — and **G2/GS201, G3 and G4 are all absent** [F]. The SoC generation this
issue is about falls in a hole between two supported endpoints.

### 5.4 Mesa: the part needs a one-line model-table entry, and it is not there

This corrects the claim I made in Gate 0 D8, which was based on grepping
`src/panfrost/lib/pan_props.c` and finding no `G710`. That grep was right and the
conclusion was wrong: the model table is **not** in `pan_props.c`, it moved to
`src/panfrost/model/pan_model.c` (10,812 B, fetched 2026-11-22). Measured there:

| `PAN_PROD_ID` | variant | shortname | counters | line |
|---|---|---|---|---|
| `(10, 8, 7)` | 0 | `G610` | `"G710"` | `:95` |
| `(10, 12, 4)` | 0-4 | `G310v1`…`G310v5` | `"G710"` | `:98,100,102,104,106` |
| `(11, 8, 2)` | 4 | `G715-Immortalis`, `G715` | `"G715"` | `:109,113` |
| `(11, 8, 3)` | 4 | `G615` | `"G715"` | `:116` |

`PAN_PROD_ID(10, 8, 2)` — the id `0xa8620004` maps to (§1.1, `pan_model.h:39-40`)
— **has 0 occurrences in the file** [F]. The string `"G710"` *does* appear six
times, but only in the **performance-counters column** of the G610 and G310
rows: G610 and G710 share a counter layout, which is why the counter group is
named `"G710"` while the model is named `"G610"`. So a naive `grep G710` on
Mesa finds hits and proves nothing; the question is whether the **product id**
is present, and it is not.

The failure mode is hard, and `panvk` says so explicitly
(`src/panfrost/vulkan/panvk_physical_device.c:439-451`):

```c
   device->model = pan_get_model(device->kmod.dev->props.gpu_id, ...);
   ...
   if (!device->model) {
      result = panvk_errorf(instance, VK_ERROR_INCOMPATIBLE_DRIVER,
                            "Unknown gpu_id (%#" PRIx64 ") or variant (%#x)", ...);
```

and `pan_get_model` (`pan_model.c:161-179`) returns `NULL` when no row matches
all four of `gpu_prod_id`, `gpu_variant`, `min_core_count` and
`required_gpu_features`. For `gpu_prod_id = 0x0a0802` no row matches, so **both
drivers refuse the device** — measured in each [F]:

| driver | check | line |
|---|---|---|
| Vulkan (`panvk`) | `if (!device->model)` → `VK_ERROR_INCOMPATIBLE_DRIVER`, `"Unknown gpu_id …"` | `panvk_physical_device.c:446-451` |
| Gallium (GL) | `if (dev->model == NULL)` → `debug_printf("panfrost: Unsupported model %X")`, `return NULL` from screen creation | `src/gallium/drivers/panfrost/pan_screen.c:1060-1064` |

So the gap is not "Mesa lacks G710 support in principle" — it is "two `if`
statements, in two drivers, both keyed on the same table row" [F].

The prior art's fix is exactly one table row, and it is public
(`derekross/omarchy-mobile` `packages/mesa/0001-panfrost-add-Mali-G710-to-the-model-table.patch`,
1,909 B, fetched 2026-11-22):

```c
+   VALHALL_MODEL(PAN_PROD_ID(10, 8, 2), 0, "G710",   "G710", MODEL_ANISO(ALL),  MODEL_TB_SIZES(32768, 16384),
+                                              MODEL_RATES_X(4, 8, 16,  64,  64, 16)),
```

with the commit message stating the rationale: G710 and G610 are the same
Valhall shader core, G610 is the fewer-core configuration, so per-core rates and
tile-buffer sizes are the G610 values and the counter layout is the `"G710"`
group G610 already uses. That is a **2-line patch** and it is the whole Mesa
delta [F] cited.

So §5's verdict is narrower than "Mesa doesn't support G710": **Mesa supports
G610 and the counter layout is already named G710; only the `(10,8,2)` model row
is missing, and adding it is 2 lines.** The remaining work is upstreaming that
row, not reverse-engineering the part [I].

## 6. The boot chain is ARM Trusted Firmware shaped, and the Google families are absent upstream

### 6.1 Eleven images per device, and none of them is Qualcomm's

Every GS201 device in the matrix carries the same eleven boot-related images
[F]:

| image | bytes | devices | distinct md5 | matrix family |
|---|---:|---:|---:|---|
| `bl1.img` | 12,288 | 5 | 4 | `boot` |
| `bl2.img` | 536,576 | 5 | 4 | `other` |
| `bl31.img` | 98,304 | 5 | 4 | `boot` |
| `pbl.img` | 40,960 | 5 | 4 | `other` |
| `abl.img` | 1,900,544 / 1,908,736 / 1,941,504 / 1,970,176 | 5 | 4 | `boot` |
| `tzsw.img` | 6,737,920 | 5 | 4 | `boot` |
| `pvmfw.img` | 1,048,576 | 5 | 5 | `boot` |
| `boot.img` | 67,108,864 | 5 | 5 | `boot` |
| `init_boot.img` | 8,388,608 | 5 | 5 | `boot` |
| `dtbo.img` | 16,777,216 | 5 | 5 | `boot` |
| `vbmeta.img` | 8,192 | 5 | 5 | `boot` |

Compare the Qualcomm vocabulary the six Adreno notes document — `xbl`,
`tz`, `hyp`, `aop`, `qupfw`, `shrm`, `cpucp`, `devcfg`, `abl`, `modem`, `dsp`.
On GS201: **`xbl` 0, `tz` 0, `hyp` 0, `aop` 0, `qupfw` 0, `shrm` 0, `cpucp` 0,
`devcfg` 0.** Only `abl` is shared, and on Qualcomm `abl` is the UEFI
application-bootloader while here it sits in the same slot but under an ARM-TF
`bl1`/`bl2`/`bl31` chain [F].

The reading [I]:

| image | what it is |
|---|---|
| `bl1` / `bl2` / `bl31` | ARM Trusted Firmware-A stages 1, 2 and 3.1 — BL1 is ROM-resident in principle but a `bl1.img` partition exists because Google ships a signed BL1 for update |
| `pbl` | primary bootloader — the pre-TF-A ROM/BL0 stage image |
| `abl` | Android bootloader, the UEFI payload that loads `boot.img` |
| `tzsw` | Trusty secure-world OS image (Google's TEE, not QSEE) |
| `pvmfw` | protected-VM firmware, the pKVM/AVF boot component |
| `gsa` | Google Security Assistant firmware (see §6.2) |
| `ldfw` | "little" DSP / low-power-core firmware (see §6.2) |

`bl1`+`bl2`+`bl31` is textbook TF-A. `tzsw` is Trusty, which is Google's TEE and
a completely different secure-world architecture from Qualcomm's QSEE `tz.mbn`
— which is why the `tz` family here contains **one file**, `gsa.img`, and not a
QSEE ELF (§6.2) [I].

**A structural note on the matrix's own labels:** `bl2.img`, `pbl.img` and
`ldfw.img` are filed under `other`, not `boot`, while `bl1`, `bl31`, `abl`,
`tzsw`, `pvmfw`, `boot`, `init_boot`, `dtbo` and `vbmeta` are under `boot`. So
the `boot` family holds **9 of the 11** chain images and the family count
understates the chain. That is a labelling inconsistency, not a data gap —
`bl2` and `pbl` are unambiguously boot-chain components [F] for the labels, [I]
for the correction. It also means the "boot 45 rows / 510,562,304 B" figure in
§2 excludes `bl2` (536,576 × 5) and `pbl` (40,960 × 5).

### 6.2 The Google-specific families have no upstream consumer at all

`WHENCE` string counts (case-insensitive, `main`, 2026-11-22) [F]:

| token | `WHENCE` hits | corpus file | corpus bytes |
|---|---:|---|---:|
| `aoc` | **0** | `aoc.bin` | 21,328,448 |
| `gsa` | **0** | `gsa.img` | 348,160 |
| `tzsw` | **0** | `tzsw.img` | 6,737,920 |
| `pvmfw` | **0** | `pvmfw.img` | 1,048,576 |
| `ldfw` | **0** | `ldfw.img` | 2,392,064 |
| `edgetpu` | **0** | `edgetpu-janeiro.fw` | 1,011,648 |
| `bcmdhd` | **0** | `fw_bcmdhd.bin` | 1,763,971 |

**None of the Google-specific firmware families exists in linux-firmware.** The
Tensor platform's always-on compute (`aoc`), security assistant (`gsa`), Trusty
image (`tzsw`), protected-VM firmware (`pvmfw`), low-power DSP (`ldfw`) and Edge
TPU (`edgetpu`) are all vendor-only [F].

That is the single largest delta between this SoC and every Qualcomm SoC the
repo has covered: on Qualcomm, most of the boot chain has *some* upstream
presence (`qcom/` in linux-firmware is large, `WHENCE` has `qcom/` entries for
many parts). On GS201 the entire security and accelerator stack is
redistributable-nowhere.

`gsa.img` deserves a note. It is the **only** `tz`-family file in the slice
(5 rows, 1 filename, 1,740,800 B = 348,160 × 5), and it is 348,160 B on all five
devices with **four distinct digests** — `Pixel_7` and `Pixel_7_Pro` share
`a8170bede7441f1c089f8f0ae51e4f14`, while `Pixel_7a` (`075d5536881b`),
`Pixel_Fold` (`2ff1d240eba3`) and `Pixel_Tablet` (`5a1af9330a18`) are all
different [F]. So the security-assistant firmware is **device-keyed**, unlike
the GPU firmware which is device-invariant (§3.1). Matrix-wide `gsa.img` is 16
rows / 16 devices / 4 sizes (278,528 / 348,160 / 380,928 / 409,600) and the size
tracks the Tensor generation: GS101 278,528, GS201 348,160, G3 380,928, G4
409,600 [F]. That is a clean generation ladder — and it is a *different*
ladder from the GPU one (§3.4: 278,528 → 294,912), so the two families step
independently: GPU steps +16,384 B once, GSA steps +69,632 / +32,768 / +28,672 B.
Anyone assuming "Tensor G2 firmware is all one size" will be wrong twice over
[F] for the numbers, [I] for the warning.

One genuine collision to record: **GS101's `gsa.img` is 278,528 B — the same
number as GS201's `mali_csffw`.** Two different families, two different SoC
generations, one size. A size-keyed deduplicator would merge them; a digest-keyed
one would not [F].

## 7. Wi-Fi is Broadcom, and `Pixel_7a` diverges inside the family

### 7.1 BCM4389 over PCIe

| device | file | bytes | md5 |
|---|---|---:|---|
| `Pixel_7` | `fw_bcmdhd.bin` | 1,763,971 | `e091fa4a0f55…` |
| `Pixel_7_Pro` | `fw_bcmdhd.bin` | 1,763,971 | `e091fa4a0f55…` |
| `Pixel_Fold` | `fw_bcmdhd.bin` | 1,763,971 | `e091fa4a0f55…` |
| `Pixel_Tablet` | `fw_bcmdhd.bin` | **936,402** | `95fc422a0067…` |
| `Pixel_7a` | `amss20.bin` | 5,353,472 | `861d0bb883ec…` |
| `Pixel_7a` | `m3.bin` | 266,684 | `8ef042c73892…` |
| `Pixel_7a` | `regdb.bin` | 24,278 | `393fc5b04ed9…` |

The chip is **Broadcom BCM4389** over PCIe — confirmed by Google's own
`device/google/gs201/device.mk` and by the `kernel_google-modules_wlan_bcmdhd_bcm4389-pantah`
module tree, both fetched 2026-11-22 [F] cited. `bcmdhd` is Broadcom's
**fullmac** driver (firmware does the 802.11 stack), as distinct from `brcmfmac`
which linux-firmware uses for its 117 `brcm/` entries. `WHENCE` has **0**
`bcmdhd` hits, so this path is vendor-only too [F].

### 7.2 `Pixel_7a` carries a Qualcomm-shaped Wi-Fi triple

Three of the five devices ship one `fw_bcmdhd.bin`. `Pixel_7a` instead ships
`amss20.bin` + `m3.bin` + `regdb.bin` — the **Qualcomm** Wi-Fi/BT firmware
naming convention (`amss` = modem software image, `m3` = the M3 micro-controller
firmware, `regdb` = the regulatory database), all three in the `wifi` family [F].

So within one SoC and one product line, **one device uses Broadcom and the
others use Broadcom with a different file layout** — except `Pixel_7a`, which
carries the Qualcomm triple. Two readings [H]:

- `Pixel_7a` genuinely ships a different Wi-Fi part (a Qualcomm/Broadcom
  dual-source decision on the cost-reduced model), or
- the `Pixel_7a` dump was collected from a different partition or a different
  firmware package and the `wifi` family label caught both stacks.

`amss20.bin` is matrix-wide 50 rows / 31 devices / 14 sizes, and `m3.bin` is 30
rows / 21 devices — both are common Qualcomm-side files, so their presence on a
Tensor device is anomalous [F]. `regdb.bin` is 92 rows / 61 devices, also common.
I record the divergence and the two hypotheses; I cannot settle it from metadata
[N].

Note `Pixel_Tablet`'s `fw_bcmdhd.bin` is **936,402 B against the others'
1,763,971 B** — a different build, not a different chip, since the file name and
the `bcmdhd` driver are the same. Matrix-wide `fw_bcmdhd.bin` is 12 rows / 12
devices / 5 sizes, so per-device builds are normal for this file [F].

## 8. Shared versus divergent: what the SoC fixes and what the board varies

Of the 65 filenames in the slice, **45 appear on more than one device**. Of
those, **19 are byte-identical across every device that has them and 26 differ**
[F].

| identical across all 5 (19) | divergent (26) |
|---|---|
| `mali_csffw-r50p0.bin` … `-r54p0.bin` (5) | `abl.img`, `bl1.img`, `bl2.img`, `bl31.img`, `boot.img`, `dtbo.img`, `init_boot.img`, `pvmfw.img`, `tzsw.img`, `vbmeta.img` |
| `modem.img` | `pbl.img`, `ldfw.img`, `aoc.bin`, `gsa.img` |
| `mfc_fw.bin`, `edgetpu-janeiro.fw` | `fw_bcmdhd.bin` |
| `st54j_fw.bin`, `d3m2.ec.bin`, `evt.ec.bin`, `proto11.ec.bin` | `cs35l41-dsp1-spk-{cali,diag,prot}.bin` and the `R-` variants |
| `libchre_log_database.bin`, `focaltech_ts_fw.bin` | `cs40l26.bin`, `cs40l26-dvl.bin`, `cs40l26-svc.bin` |
| `esim-full-v0.img`, `esim-full-v1.img`, `esim-full-v0-security.img`, `esim-full-ofl-v1.img` | `goodix_firmware.bin`, `st54j_conf_PROTO1.bin` |
| `MICRONMT128GAXAT2U310104_MICRONMT256GAXAT4U310104.img` | |

The split is almost perfectly along **silicon-versus-board** lines [F] for the
grouping, [I] for the reading:

- **Identical (SoC-level):** GPU firmware, modem image, MFC (media) firmware,
  Edge TPU firmware, NFC firmware (`st54j`), embedded-controller images
  (`d3m2`/`evt`/`proto11` — all exactly 1,048,576 B = 1 MiB, three build
  variants shipped on every device), CHRE log database, storage firmware.
  These are the same because the silicon is the same.
- **Divergent (board-level):** every boot-chain image (each device is signed
  with its own keys and carries its own DTB), the audio amplifiers (`cs35l41`
  and `cs40l26` — calibration is per-enclosure), the touch controllers
  (`goodix`/`focaltech`/`novatek`/`synaptics`), Wi-Fi calibration, and the
  per-device `aoc`/`gsa`/`ldfw` builds.

`modem.img` is the strongest single invariant: **82,370,560 B, one md5
(`fd9e4bb59c47…`), on all four devices that have it** [F]. The Samsung Exynos
5300 modem payload does not vary by device within GS201. `Pixel_Tablet` has no
`modem.img` at all — it is the Wi-Fi-only model, which is the entire reason its
slice is 136.7 MB against the others' ~218 MB (§2).

### 8.1 Twenty filenames exist on exactly one device

| device | unique files | what they are |
|---|---:|---|
| `Pixel_Tablet` | 12 | 6 `L2-`/`R2-cs35l41` amp variants, 4 `novatek_ts_*`, `logstrs.bin`, `fw_bcmdhd_monitor.bin` |
| `Pixel_7a` | 6 | `amss20.bin`, `m3.bin`, `regdb.bin`, `hpnv21.bin`, `hpnv21g.bin`, `cs40l26-calib.bin` |
| `Pixel_7_Pro` | 2 | `synaptics.img`, `synaptics_b.img` |
| `Pixel_7`, `Pixel_Fold` | 0 | — |

12 + 6 + 2 = **20**, which is exactly `65 − 45` [F].

`hpnv21.bin` / `hpnv21g.bin` are Bluetooth patch files (the `hpnv*` naming is
the same one #823 documented for SM8350's 84 `hpnv*` files), and their presence
only on `Pixel_7a` is a board-level Bluetooth-part difference [F] for the naming
match, [I] for the reading.

The `cs35l41` amplifier set is the clearest board fingerprint: three files
(`cali` 1,912 B, `diag` 2,604 B, `prot` 4,932 B) appear in **four** naming
variants — bare, `R-`, `L2-`, `R2-` — and `Pixel_Tablet` alone carries all four
prefixes because a tablet has more speakers [F]. The bare and `R-` variants are
on all five devices with **5 distinct digests each** (per-device calibration),
while `L2-`/`R2-` are `Pixel_Tablet`-only. That is exactly the pattern you would
expect from per-enclosure DSP tuning, and it is the reason `cs35l41-*` appears
in both the identical-*filename* and divergent-*content* columns [I].

## 9. Matrix defects this slice exposes

Four defects, three of them in the neighbouring generation rather than in GS201
itself. All are reproducible from the CSV alone.

### 9.1 Two devices have a blank `soc`, and four are mislabelled

| device | rows | `soc` label | actual SoC | Mali digests match |
|---|---:|---|---|---|
| `Pixel_9A` | 54 | **blank** | Tensor G4 | G3/G4 set |
| `Pixel_9_Pro_XL` | 59 | **blank** | Tensor G4 | G3/G4 set |
| `Pixel_9_Pro` | 59 | `Google Tensor G3` | Tensor G4 | G3/G4 set |
| `Pixel_9_Pro_Fold` | 64 | `Google Tensor G3` | Tensor G4 | G3/G4 set |
| `Pixel_9` | 59 | `Google Tensor G4` | Tensor G4 | G3/G4 set |

`Pixel_9A` and `Pixel_9_Pro_XL` have an **empty `soc` string**, yet their five
Mali digests are identical to the G3/G4 set — so they are unlabelled, not
unidentifiable [F]. `Pixel_9_Pro` and `Pixel_9_Pro_Fold` are labelled **G3** but
are **Tensor G4** devices (Wikipedia *Pixel 9*, fetched 2026-11-22); their Mali
digests match both G3 and G4 because G3 and G4 ship identical GPU firmware
(§3.4), so the GPU data cannot discriminate — the label is wrong and the
firmware is consistent with either [F] for the label, [I] for the SoC call.

This is the third instance of the same class of defect: #2029 recorded it for
`tundra`/`martini`, #823 for `OnePlus_9`, and here it is four devices in the
generation after this one. **The `soc` column is not a reliable key; the
firmware digests are.** GS201's own five devices are correctly labelled, so
nothing in §2–§8 depends on the defect [F].

### 9.2 `bl2` and `pbl` are filed under `other`, not `boot`

Recorded in §6.1. `boot` holds 9 of the 11 chain images; `bl2.img` (536,576 B)
and `pbl.img` (40,960 B) sit in `other`, as does `ldfw.img`. The `boot` family
byte total (510,562,304 B) therefore omits `bl2` and `pbl` entirely [F].

This is a labelling inconsistency rather than a data gap — the filenames are
unambiguous. It also means any "boot is N% of the slice" statement is
family-label-dependent [F]:

| accounting | bytes | share of 1,014,982,980 |
|---|---:|---:|
| `boot` family label | 510,562,304 | 50.30% |
| the actual 11-image chain | 513,449,984 | 50.59% |
| difference | 2,887,680 | 0.28 pp |

and `2,887,680 = (536,576 + 40,960) × 5`, i.e. exactly `bl2.img` plus `pbl.img`
across five devices. (The chain total is not `5 × 102,699,008` because `abl.img`
differs in size on three of the five devices — 1,900,544 / 1,908,736 / 1,941,504
/ 1,970,176 B.)

### 9.3 The repo's entire Mali coverage is five filenames on thirteen devices

Matrix-wide, `filename LIKE 'mali%'` is **65 rows / 13 devices**, and the 13
devices span four `soc` values — `Google Tensor GS201` (25), `Google Tensor G3`
(25), `Google Tensor G4` (5), and **blank (10)**. Only **five distinct
filenames** exist in the whole matrix, all `mali_csffw-rNNp0.bin` [F].

So the entire repo's Mali coverage is five filenames on thirteen Tensor devices
and **nothing else**. There is no Mali firmware for any MediaTek, Rockchip, NXP
or Samsung Exynos device in the matrix, even though those are the SoCs the
`panthor` binding and linux-firmware's arch images actually serve (§5.2, §4.1).
The matrix is a Pixel/Tensor corpus with a Qualcomm majority; Mali appears only
because Pixel 6 onward happens to use it [I].

### 9.4 The repo's GPU core-ID count is wrong by one, and this document fixes it

`docs/REPO-STATE-MAP.md:18` reads:

> `| GPU core ID | 27 | PARTIAL | 6 per-SoC GPU docs under research/soc/: MSM8998, SM4375, SM7250, SM7325, SM8250, SM8350; 21 SoCs remain |`

With this note there are **7** per-SoC GPU documents and **20** SoCs remaining.
The row is corrected in this commit, as are the two `gpu` family rows at `:36`
and `:50`, which list the six Adreno documents as the family's artifact set. The
Mali document is a different driver and a different firmware scheme, so it
belongs in those rows but must not be read as a seventh Adreno slice [F].

Note also that the "27" denominator is the count of **distinct non-blank `soc`
labels** in the matrix (`len({r['soc'] for r in cm if r['soc'].strip()})` = 27
over 33,917 rows / 123 devices) [F]. GS201 is one of those 27, so it was always
in the denominator — it was simply unserved.

## 10. Honest negatives

Everything below is a thing this note does **not** establish. Each is a real
limit of the evidence available, not a hedge.

**N1 — No GS201 payload bytes were examined.** `data-fetch/` holds
`second-device/instantnoodle` (SM8250) and `second-device/larry` (SM6375) only.
No GS201 ELF, container or image was opened. Every statement about
`mali_csffw-*` content is *filename, size and md5* — nothing about its internal
structure, entry table, or the meaning of the `rNNpN` revision numbers beyond
the naming [N].

**N2 — The 4 KiB upstream-vs-corpus size delta is unexplained.** §4.1 measured
arch10.8 = 282,624 B upstream against 278,528 B in the corpus, and arch11.8 =
299,008 B against 294,912 B — exactly 4,096 B in both cases. Two hypotheses are
recorded and neither is confirmed. Resolving it needs the bytes on both sides
[N]. (An attempt to fetch the corpus's actual bytes was not made: no GS201
payload is present locally, per N1.)

**N3 — Why the corpus holds only `p0` is unknown.** §3.3 records that the corpus
has `r50p0`…`r54p0` while the prior art says the shipping device runs
`mali_csffw-r54p3.bin`. Whether this is a capture-time gap, a partition
selection, or a genuinely different build is not determinable from metadata
[N].

**N4 — No runtime verification on hardware.** The GPU identity in §1 is cited
from the prior art's `dmesg` and cross-checked against public specs and the
corpus's filenames. No GS201 device was booted for this note, and the
`GPU_ID`→arch→path chain in §1.1/§4.2 is arithmetic on cited values rather than
a live register read [N].

**N5 — `Pixel_7a`'s Qualcomm-shaped Wi-Fi triple is unexplained.** §7.2 records
`amss20.bin` + `m3.bin` + `regdb.bin` on that device alone, against
`fw_bcmdhd.bin` on the other four. Two hypotheses, neither confirmed. This may
be a genuine dual-source hardware decision or a collection artefact [N].

**N6 — The `aoc`, `gsa`, `ldfw`, `tzsw`, `pvmfw`, `edgetpu`, `mfc_fw` formats are
not characterised at all.** §6.2 establishes only that these files exist, their
sizes, and that linux-firmware has no entry for any of them. No container
structure, header, or entry table is described [N].

**N7 — The `bl2`/`pbl`/`ldfw`→`other` mislabel is reported, not fixed.** §9.2
records it; this commit does not change the CSV. A matrix-wide relabel is a
separate change with its own blast radius [N].

**N8 — The Mesa claim is narrower than a first pass suggested, and the first
pass was wrong.** Gate 0 D8 asserted "Mesa has no G710 entry" on the strength of
a `grep G710` over `src/panfrost/lib/pan_props.c` returning 0. The model table is
in `src/panfrost/model/pan_model.c`, the string `"G710"` occurs there six times
(as a performance-counter group name), and the actual gap is the missing
`PAN_PROD_ID(10, 8, 2)` row. §5.4 states the corrected position. The error is
recorded here rather than silently edited out of Gate 0, because the *shape* of
the mistake — grepping a string that appears in an unrelated column — is the
kind that would recur [N].

**N9 — No claim about performance, DVFS or power.** The prior art reports
151→572 MHz DVFS through ACPM. That is cited, not verified, and nothing in this
note depends on it [N].

**N10 — The 16,384 B generation step is measured, not explained.** §3.4 shows
GS201 and G3/G4 firmware differ by exactly 16 KiB with disjoint digests, and
§4.1 shows the same 16,384 B step between upstream arch10.8 and arch11.8. Both
numbers are exactly **four** 4 KiB pages, which is suggestive but not
explanatory; the coincidence of the two measurements is reported as a
consistency check, not as a mechanism [N].

**N11 — The `docs/REPO-STATE-MAP.md` correction touches four rows, not one.**
§9.4 says the GPU core-ID row is corrected; in fact the SoC-package row (`:16`)
and both `gpu` family rows (`:36`, `:50`) are edited too, because all four
carried the count "6 per-SoC GPU docs". The counts are mechanical (`6 → 7`,
`21 → 20` remain) but the edit is wider than a single line, and a reviewer
diffing this commit should expect four changed rows in that file [F].

## Reproduce

All commands run 2026-11-22 from the repo root. `python3 -I` throughout; no
third-party modules.

**Slice totals, family split, per-device profile (§2):**

```sh
python3 -I - <<'PY'
import csv
from collections import Counter
cm=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in cm if r['soc'].strip()=='Google Tensor GS201']
print(len(s), len({r['device'] for r in s}), sum(int(r['size_bytes']) for r in s), len({r['filename'] for r in s}))
for f,n in Counter(r['blob_family'] for r in s).most_common():
    rs=[r for r in s if r['blob_family']==f]
    print(f, len(rs), len({r['filename'] for r in rs}), sum(int(r['size_bytes']) for r in rs))
PY
```

Expect `225 5 1014982980 65` and the six family rows of §2.

**The 5×5 GPU grid and the per-revision digests (§3.1):**

```sh
python3 -I - <<'PY'
import csv
from collections import Counter
cm=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g=[r for r in cm if r['soc'].strip()=='Google Tensor GS201' and r['blob_family']=='gpu']
print(len(g), sorted({int(r['size_bytes']) for r in g}))
for fn in sorted({r['filename'] for r in g}):
    rs=[r for r in g if r['filename']==fn]
    print(fn, len(rs), len({r['md5_db'] for r in rs}), rs[0]['md5_db'])
PY
```

Expect 25 rows, size set `[278528]`, and for each of the five filenames
`5 1 <one digest>` — five rows, one digest, i.e. device-invariant.

**The generation split and digest disjointness (§3.4):**

```sh
python3 -I - <<'PY'
import csv
from collections import Counter
cm=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
m=[r for r in cm if r['filename'].lower().startswith('mali')]
print(len(m), len({r['device'] for r in m}), len({r['filename'] for r in m}))
for soc in ('Google Tensor GS201','Google Tensor G3','Google Tensor G4',''):
    rs=[r for r in m if r['soc']==soc]
    if rs: print(repr(soc), len(rs), sorted({int(r['size_bytes']) for r in rs}))
def S(soc): return {r['md5_db'] for r in m if r['soc']==soc}
a,b,c=S('Google Tensor GS201'),S('Google Tensor G3'),S('Google Tensor G4')
print('GS201&G3',len(a&b),'GS201&G4',len(a&c),'G3&G4',len(b&c))
PY
```

Expect `65 13 5`, the four label rows at 278,528 / 294,912, and
`GS201&G3 0 GS201&G4 0 G3&G4 5`.

**linux-firmware: the panthor block and the absence of `rNNpN` (§4.1):**

```sh
curl -sL "https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/WHENCE?h=main" -o /tmp/WHENCE
wc -c /tmp/WHENCE
grep -c "arm/mali" /tmp/WHENCE
grep -c "mali_csffw-r" /tmp/WHENCE
grep -o "mali_csffw[^ ]*" /tmp/WHENCE | sort -u
```

Expect `540253`, `7`, `0`, and the two-line output `mali_csffw` /
`mali_csffw.bin`.

**Upstream arch images: sizes, digests, shared magic (§4.1):**

```sh
for a in arch10.8 arch10.10 arch10.12 arch11.8 arch12.8 arch13.8 arch14.8; do
  curl -sL "https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/arm/mali/$a/mali_csffw.bin?h=main" -o /tmp/b.bin
  echo "$a $(wc -c < /tmp/b.bin) $(md5sum /tmp/b.bin | cut -c1-32) $(head -c4 /tmp/b.bin | xxd -p)"
done
```

Expect the seven-row table of §4.1: 282,624 / 282,624 / 282,624 / 299,008 /
307,200 / 311,296 / 344,064, three identical digests in the first three rows, and
`6e3af1c3` on all seven.

**The driver's firmware path (§4.2):**

```sh
curl -sL "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/gpu/drm/panthor/panthor_fw.c" -o /tmp/panthor_fw.c
sed -n '31p;811,816p;1559,1565p' /tmp/panthor_fw.c
```

Expect `#define CSF_FW_NAME "mali_csffw.bin"`, the `snprintf` building
`arm/mali/arch%d.%d/%s`, and seven `MODULE_FIRMWARE` lines.

**`GPU_ID` decode and the model-table key (§1.1, §1.2):**

```sh
curl -sL "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/gpu/drm/panthor/panthor_gpu_regs.h" -o /tmp/regs.h
sed -n '10,16p' /tmp/regs.h
python3 -I -c "
x=0xa8620004
print(x>>28, (x&0xf000000)>>24, (x&0xf00000)>>20, (x&0xf0000)>>16, (x&0xf000)>>12, (x&0xff0)>>4, x&0xf)
print(hex((10<<24)|2))
"
```

Expect `10 8 6 2 0 0 4` and `0xa000002`.

**Mainline: `dts/google/` contents and the GS201 code-search negative (§5.3):**

```sh
curl -s "https://api.github.com/repos/torvalds/linux/contents/arch/arm64/boot/dts/google?ref=master" | python3 -I -c "
import json,sys
for x in json.load(sys.stdin): print(x['name'], x.get('size'))
"
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
     "https://api.github.com/search/code?q=repo:torvalds/linux+GS201" \
  | python3 -I -c "import json,sys; print(json.load(sys.stdin).get('total_count'))"
```

Expect the six `lga*`/`Makefile` entries and `0`. The contents call works
unauthenticated; **the code-search call does not** — GitHub returns
`{"message":"Requires authentication","status":"401"}` without a token, so
`$GITHUB_TOKEN` must be set for that second command. This was checked on
2026-11-22: unauthenticated contents `200`, unauthenticated code search `401`.

**The binding's three SoC compatibles (§5.2):**

```sh
curl -sL "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/devicetree/bindings/gpu/arm,mali-valhall-csf.yaml" -o /tmp/bind.yaml
sed -n '18,25p' /tmp/bind.yaml
grep -c google /tmp/bind.yaml
```

Expect the `mediatek,mt8196-mali` / `nxp,imx95-mali` / `rockchip,rk3588-mali`
enum and `0`.

**Mesa: the missing `PAN_PROD_ID(10,8,2)` row (§5.4):**

```sh
curl -sL "https://gitlab.freedesktop.org/mesa/mesa/-/raw/main/src/panfrost/model/pan_model.c" -o /tmp/pan_model.c
grep -c "PAN_PROD_ID(10, 8, 2)" /tmp/pan_model.c
grep -n "PAN_PROD_ID(10, 8," /tmp/pan_model.c
grep -c "G710" /tmp/pan_model.c
curl -sL "https://gitlab.freedesktop.org/mesa/mesa/-/raw/main/src/gallium/drivers/panfrost/pan_screen.c" -o /tmp/pan_screen.c
grep -n "dev->model == NULL" /tmp/pan_screen.c
```

Expect `0`, one line (`:95`, the G610 row), and `6` — zero for the id, six for
the counter-group string (once on the G610 row, five times across the G310v1-v5
rows). That contrast *is* the finding. The last command should print
`1060:   if (dev->model == NULL) {`.

**postmarketOS: nine probes, all 404 (§0):**

```sh
for p in device/testing/linux-postmarketos-gs201 device/testing/linux-google-gs201 \
         device/community/linux-postmarketos-gs201 device/testing/soc-google-gs201 \
         device/testing/device-google-panther device/testing/device-google-cheetah \
         device/testing/device-google-lynx device/testing/device-google-felix \
         device/testing/device-google-tangorpro; do
  enc=$(python3 -I -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "$p")
  echo "$p $(curl -s -o /dev/null -w '%{http_code}' "https://gitlab.com/api/v4/projects/postmarketOS%2Fpmaports/repository/files/$enc%2FAPKBUILD/raw?ref=master")"
done
```

Expect `404` on every line.

**Shared vs divergent census (§8):**

```sh
python3 -I - <<'PY'
import csv
from collections import defaultdict
cm=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in cm if r['soc'].strip()=='Google Tensor GS201']
d=defaultdict(set)
for r in s: d[r['filename']].add(r['md5_db'])
sh={f:v for f,v in d.items() if len([r for r in s if r['filename']==f])>1}
same=[f for f in sh if len(d[f])==1]; diff=[f for f in sh if len(d[f])>1]
print('shared',len(sh),'same',len(same),'diff',len(diff))
print('unique',len([f for f in d if len([r for r in s if r['filename']==f])==1]))
PY
```

Expect `shared 45 same 19 diff 26` and `unique 20`.

**Google families absent from `WHENCE` (§6.2):**

```sh
for k in aoc gsa tzsw pvmfw ldfw edgetpu bcmdhd; do echo "$k $(grep -ci "$k" /tmp/WHENCE)"; done
```

Expect `0` on all seven.

## Sources

| source | what it gave | fetched |
|---|---|---|
| `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 rows, 123 devices, 27 SoC labels) | every count, size and digest in §2–§3, §6.1, §8, §9 | in-repo |
| `docs/REPO-STATE-MAP.md` | the GPU core-ID row corrected in §9.4 | in-repo |
| `research/soc/Qualcomm-SM8350-Snapdragon-888-soc.md` (#823) | house format: Reproduce blocks, Sources table, honest negatives | in-repo |
| `research/soc/Qualcomm-SM7250-Snapdragon-765G-gpu.md` (#2029) | the label-defect precedent (`tundra`/`martini`) | in-repo |
| `derekross/omarchy-mobile` `device/cheetah/GPU-PLAN.md`, 34,661 B, status 2026-10-12 | GPU identity, `GPU_ID` `0xa8620004`, register base, IRQs, CMU_G3D clocks, the working Panthor path, the `r54p3` stock file | 2026-11-22 |
| `derekross/omarchy-mobile` `packages/mesa/0001-panfrost-add-Mali-G710-to-the-model-table.patch`, 1,909 B | the 2-line Mesa fix and its rationale (§5.4) | 2026-11-22 |
| linux-firmware `WHENCE`, 540,253 B, `main` | the seven arch entries, `LICENCE.mali_csffw`, and all seven absence counts | 2026-11-22 |
| linux-firmware `arm/mali/arch*/mali_csffw.bin` (7 files) | sizes, digests, shared magic `6e3af1c3`, the 4 KiB delta | 2026-11-22 |
| `torvalds/linux` `panthor_fw.c` (45,236 B), `panthor_hw.c` (8,529 B), `panthor_gpu_regs.h` (3,738 B) | `CSF_FW_NAME`, the path builder, `MODULE_FIRMWARE`, `GPU_PROD_ID_MAKE`, the `GPU_ID` field macros | 2026-11-22 |
| `torvalds/linux` `arm,mali-valhall-csf.yaml`, 4,970 B | the three SoC compatibles | 2026-11-22 |
| `torvalds/linux` `arch/arm64/boot/dts/google/` | six entries, all Tensor G5 | 2026-11-22 |
| `mesa` `src/panfrost/model/pan_model.c` (10,812 B), `pan_model.h` (4,273 B), `src/panfrost/vulkan/panvk_physical_device.c` (70,680 B) | the model table, `PAN_PROD_ID`, `pan_get_model`, the `VK_ERROR_INCOMPATIBLE_DRIVER` path | 2026-11-22 |
| `postmarketOS/pmaports` on GitLab | nine 404s; the Chromebook + Pixel-3-era device list | 2026-11-22 |
| Google `device/google/gs201/device.mk`; `kernel_google-modules_wlan_bcmdhd_bcm4389-pantah` | BCM4389 Wi-Fi identity | 2026-11-22 |
| public spec sheets (Android Police, XDA, 91mobiles, NotebookCheck, Wikipedia *Pixel 9*, GSMArena) | Mali-G710 MP7 for G2; Mali-G715 MP7 for G3/G4; Pixel 9 Pro = Tensor G4 | 2026-11-22 |
