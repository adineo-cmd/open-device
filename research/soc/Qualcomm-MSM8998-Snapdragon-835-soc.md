# Qualcomm MSM8998 Snapdragon 835 — SoC package: CPU, DSP, boot chain, TrustZone, firmware census

Issue #805. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative / [OPEN] unresolved. Every number is command output from a run on
**2026-11-22** against
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows),
`torvalds/linux` master, the `linux-firmware` tree on `git.kernel.org`, and the
postmarketOS `pmaports` tree on GitLab.

**No payload exists in this workspace and none was read.** Every statement below
is matrix metadata — filename, size, md5, `db_type`, family label — or public
GPL source. No ELF is parsed here and no instruction is disassembled [N].

This is the **SoC-package** note. The GPU core identification for this SoC is a
separate, already-committed deliverable and is **cited, never re-derived**.

## 0. Verdict

| question | answer | class |
|---|---|---|
| SoC identity | MSM8998 = Snapdragon 835, platform codename `msmcobalt`/`apqcobalt`; board ID **292** (`QCOM_ID_MSM8998`) | [F] |
| CPU topology | **4 + 4 Kryo 280** — two `cpu-map` clusters, `cpu0`–`cpu3` at MPIDR `0x0`–`0x3` (`capacity-dmips-mhz` 1024) and `cpu4`–`cpu7` at `0x100`–`0x103` (1536) | [F] |
| CPU instruction-level ID | **not obtainable from this corpus** — `isa_identified` is empty on all 871 rows and mainline's DT does not encode a MIDR for either cluster | [N] |
| GPU | Adreno 540, chip ID `0x05040001`, `ADRENO_5XX` — **cited from the GPU note** | [F] |
| DSP set in the slice | **6** classes: `adsp`, `cdsp`, `slpi`, `npu`, `venus`, `spss` | [F] |
| DSP set mainline boots | **3** remoteprocs: `mss` (modem), `slpi`, `adsp` — **no `cdsp`, no `npu`** | [F] |
| Boot chain, real images | **12 rows / 6 filenames**; only **2.1%** of the family's bytes | [F] |
| Boot chain, partition dumps | **5 rows / 3 filenames** = 352,321,536 B = **97.9%** of the family | [F] |
| TrustZone family | **168 rows / 85 filenames / 15 stems / 19,779,884 B** | [F] |
| TZ reserved window | `tz_mem` **45.00 MiB** at `0x86200000`; **15** reserved regions totalling **225.08 MiB** | [F] |
| Split law `mdt == b00+b01` | **27 of 27** testable stems, zero exceptions; of the 7 untestable, **6** are single-file MDTs and **1** (`cpe_9340`) has segments but no `.b00` | [F] |
| Code-variance law | a stem varies in a **code** segment across the two devices **iff** it is one of the 4 real PAS remoteprocs — **34 of 34** | [F] |
| `mba.mbn` in the corpus | **0 of 33,917 rows**; the corpus contains **zero `.mbn` files of any name** | [N] |
| `qcom/msm8998/` in linux-firmware | **does not exist** — 0 files, 0 links | [N] |
| linux-firmware a540 payload | `a540_gpmu.fw2` **404**, `a540_zap.mdt` **404**; `a530_pm4.fw`/`a530_pfp.fw` **present** | [N, F] |
| Mainline board DT for these two devices | **none** — 0 `guacamole*`, 0 `hotdog*` under `qcom/` | [N] |
| postmarketOS packaging | both devices in this slice are packaged as **SM8150**, not MSM8998 | [F] |

The three findings that are new to this repository, and not restatements of
#2018 or of the device notes, are:

1. **Code-segment variance is a perfect remoteproc detector** (§7.2) — 34 of 34
   stems, and the four exceptions to the `b01`-only law are exactly the four
   real remote processors.
2. **`mba.mbn` is absent from the entire 33,917-row corpus** (§4.3), so the
   modem remoteproc mainline describes cannot be booted from this corpus at
   all — a corpus-wide negative, not a device negative.
3. **The slice ships firmware for two units mainline MSM8998 does not
   support** (§3.3) — `cdsp` (22 rows) and `npu` (10 rows) — which is
   independent, non-GPU evidence that these 871 rows are not an MSM8998.

Companion documents — what is cited rather than rebuilt:

| document | owns | this note |
|---|---|---|
| `research/soc/Qualcomm-MSM8998-Snapdragon-835-gpu.md` (#2018) | Adreno 540 identity and `a5xx_catalog.c` binding (§1); the three-ground mislabel proof (§2); the four-device byte-identical GPU control (its §2.2); the zero-a540 census (§3) | cites §1–§3 in full; the GPU section here is three lines long |
| `research/soc/per-soc-method-plans.md:74` | the sentence "OnePlus 7 / 7T carry MSM8998 835 (they are SM8150)" | cites; does not re-announce |
| `docs/devices/oneplus/OnePlus_7/tz.md` (#1472) | the 83-row tz decomposition (§3), the `tz.img` 2×2 md5 pairing (§2, §4), the finding that the differing files fall exactly on `.b01`/`.mdt`/`.img` (§4) | cites §4 for the device-level law; §7 here generalises it to the package |
| `docs/devices/oneplus/OnePlus_7/boot.md` (#1466) | the `boot` family's mixed `size_bytes` column and the fleet-wide 364/1,038 = 86.8% figure | re-derives for this slice only |
| `docs/devices/oneplus/OnePlus_7T_Pro/boot.md` (#1484) | the completed four-device md5 matrix (§5) and the codename↔SoC anchor | cites §5 for the per-file table; §6.2 here supplies the **whole-package** file-set identity |
| `research/fleet/tz-hyp.md` | the `hyp` container format and the two `hyp.img` hashes on these devices (§4.2) | cites |
| `research/fleet/wifi-wpss.md` | the `wpss`/`bdwlan` grammar, the `b<NN> ≡ phdr NN` proof, and the board-id indexing | cites; the 68 `wifi` rows are not re-analysed |
| `research/cdsp-fleet/census.md` | the fleet CDSP census, in which this SoC is one row (`:207`) | cites |
| `research/laptop/qualcomm-adsp-bm2n-fleet.md` | the `bm2n` BT-patch fleet matrix | cites; the 16 `bt` filenames are not re-analysed |
| `research/fleet/dsp-tz-map.md` | the `dsp.img` container is **ext4**, proven on OnePlus 6 | cites for the container; §3.4 here only reports this slice's size and device-invariance |

## 1. CPU: 4 + 4 Kryo 280, and why the DT cannot name the cores

**Verdict: eight cores in two clusters of four, all declared
`compatible = "qcom,kryo280"`, all booted by PSCI.** The 4+4 split is encoded
in three independent places — the MPIDR `reg` values, the
`capacity-dmips-mhz` figures, and the `cpu-map` node — and the three agree.

### 1.1 The eight nodes

`msm8998.dtsi` is **77,917 B**. The CPU nodes run from `:140` to `:228`:

| node | line | `reg` | `capacity-dmips-mhz` | `next-level-cache` | idle states |
|---|---:|---|---:|---|---|
| `cpu0` | 140 | `0x0 0x0` | 1024 | `l2_0` | `little_cpu_sleep_0/1` |
| `cpu1` | 155 | `0x0 0x1` | 1024 | `l2_0` | same |
| `cpu2` | 165 | `0x0 0x2` | 1024 | `l2_0` | same |
| `cpu3` | 175 | `0x0 0x3` | 1024 | `l2_0` | same |
| `cpu4` | 185 | `0x0 0x100` | **1536** | `l2_1` | `big_cpu_sleep_0/1` |
| `cpu5` | 200 | `0x0 0x101` | **1536** | `l2_1` | same |
| `cpu6` | 210 | `0x0 0x102` | **1536** | `l2_1` | same |
| `cpu7` | 220 | `0x0 0x103` | **1536** | `l2_1` | same |

[F] `cpu-map` at `:230` declares exactly two clusters: `cluster0` holds
`cpu0`–`cpu3`, `cluster1` holds `cpu4`–`cpu7`. This is the opposite shape to
SM8350, where the DT puts all eight cores in one cluster — a useful control
that the `cpu-map` node is authored per-SoC and not normalised [F].

[F] The `0x100` offset in `cpu4`–`cpu7`'s MPIDR is the Aff1 field, i.e. a
distinct physical cluster. The DT and the address space agree; nothing is
inferred from marketing.

### 1.2 MIDR: the kernel has the IDs, the DT does not carry them

[F] `arch/arm64/include/asm/cputype.h` defines Qualcomm's implementor code
`ARM_CPU_IMP_QCOM 0x51` and part numbers `0x800` (Kryo 2xx Gold), `0x801`
(Kryo 2xx Silver), `0x802`/`0x803` (3xx), `0x804`/`0x805` (4xx). With
`MIDR_CPU_MODEL(imp, partnum) = (imp<<24) | (0xf<<16) | (partnum<<4)`:

```
MIDR_QCOM_KRYO_2XX_GOLD    0x51008000
MIDR_QCOM_KRYO_2XX_SILVER  0x51008010
```

[I] An MSM8998 core therefore reads one of those two MIDRs at runtime, and
`arch/arm64/kernel/cpufeature.c:1701-1702` lists both in the KPTI-safe table —
which is itself evidence that these cores are Meltdown-immune by MIDR, not by
probe.

[F] But **the DT does not encode it**: all eight nodes say `qcom,kryo280` and
nothing else. `Documentation/devicetree/bindings/arm/cpus.yaml` does list
`qcom,kryo280` among its `compatible` enum (alongside `kryo240`…`kryo780`), so
the string is legitimate, but it is a *marketing-generation* label, not a MIDR.

**This is the instruction-level negative of the note** [N]: with no payload and
no DT MIDR, I cannot show a Kryo 280 instruction. What I can show is the exact
MIDR value the kernel expects, the two clusters, and the functional split.
Anything stronger would require reading a booted device's `MIDR_EL1`, which is
outside this corpus.

### 1.3 Machine identity

[F] `QCOM_ID_MSM8998` is **292** (`include/dt-bindings/arm/qcom,ids.h:143`) and
`drivers/soc/qcom/socinfo.c:384` carries `{ qcom_board_id(MSM8998) }`.
Mainline's OnePlus 5 common DT pins the same number in the bootloader
handshake: `qcom,msm-id = <292 0x20001>` (8998 **v2.1**) in
`msm8998-oneplus-common.dtsi:20`.

[I] So the SoC identity is triangulated: socinfo table, bootloader `msm-id`, and
the PMIC set the boards include. The 871 rows in the slice, by contrast, carry
no such identity — they carry a string in a CSV column.

## 2. GPU — cited, three lines

[F] The GPU is an **Adreno 540**, chip ID `0x05040001`, family `ADRENO_5XX`,
bound in `a5xx_catalog.c:134-151` to `a530_pm4.fw` / `a530_pfp.fw` /
`a540_gpmu.fw2` / `a540_zap.mdt`, with `gmem = SZ_1M` and
`.quirks = ADRENO_QUIRK_LMLOADKILL_DISABLE`. I re-read that entry this session
and it is unchanged from #2018 §1.2.

[F] The slice's 8 `gpu` rows / 4 filenames are `a630_gmu.bin`, `a630_sqe.fw`,
`a640_gmu.bin`, `a640_zap.mdt` — an **a6xx** set with a GMU, which an a5xx
Adreno 540 cannot load, and all four are byte-identical across the two devices.

Everything else about the GPU — the three-ground mislabel proof, the
four-device control, the zero-`a540` census — is **#2018 §2–§3** and is not
restated here.

## 3. DSP: six classes in the slice, three in mainline

### 3.1 The remoteproc set mainline actually declares

[F] `msm8998.dtsi` contains exactly **three** remoteproc nodes:

| node | line | `compatible` | MMIO | PAS id | `sysmon_name` |
|---|---:|---|---|---:|---|
| `remoteproc_mss` | 1465 | `qcom,msm8998-mss-pil` | `0x04080000` | — (MSS path) | `modem` |
| `remoteproc_slpi` | 1661 | `qcom,msm8998-slpi-pas` | `0x05800000` | 12 | `slpi` |
| `remoteproc_adsp` | 3260 | `qcom,msm8998-adsp-pas` | `0x17300000` | 1 | `adsp` |

[F] The driver side confirms and narrows it. `qcom_q6v5_pas.c:2007-2008` maps
only two 8998 compatibles:

```c
{ .compatible = "qcom,msm8998-adsp-pas", .data = &msm8996_adsp_resource },
{ .compatible = "qcom,msm8998-slpi-pas", .data = &msm8996_slpi_resource_init },
```

[F] Both descriptors are **borrowed from MSM8996**, not written for 8998:
`msm8996_adsp_resource` (`:1214`) is `firmware_name = "adsp.mdt"`, `pas_id = 1`,
`ssr_name = "lpass"`, `ssctl_id = 0x14`; `msm8996_slpi_resource_init` (`:1501`)
is `firmware_name = "slpi.mdt"`, `pas_id = 12`, `ssr_name = "dsps"`,
`ssctl_id = 0x16`. [I] On this SoC the two DSPs are treated as MSM8996-class
silicon, which matches the 4+4 Kryo 280 / Hexagon 682 generation.

[F] `qcom_q6v5_mss.c:2391` defines `msm8998_mss` with
`.hexagon_mba_image = "mba.mbn"`, and `:2115` sets
`qproc->hexagon_mdt_image = "modem.mdt"`. So the modem path wants **two** files,
one of which is a `.mbn`.

### 3.2 What the slice ships

[F] Class census of DSP-class stems in the 871 rows (`.jsn` sidecars counted in
the same row, since they belong to the same stem):

| stem | family label | rows | files | bytes | `.jsn` sidecars |
|---|---|---:|---:|---:|---|
| `adsp` | `adsp` | 34 | 17 | 27,471,208 | `adspr.jsn` 403 B, `adspua.jsn` 555 B |
| `cdsp` | `cdsp` | 22 | 11 | 7,057,150 | `cdspr.jsn` 403 B |
| `slpi` | **`other`** | 48 | 24 | 12,269,976 | `slpir.jsn` 403 B, `slpius.jsn` 405 B |
| `npu` | **`other`** | 10 | 5 | 121,096 | — |
| `venus` | **`other`** | 12 | 6 | 2,222,528 | — |
| `spss1p`/`spss2p` | **`other`** | 16 | 8 | 2,152,032 | — |

[F] The `slpi` row's 48 rows split as 44 on the `slpi.*` stem itself
(22 files, 12,268,360 B) plus 4 `.jsn` rows (2 files, 1,616 B).

[F] The `adsp` stem has **17** files: `.mdt`, `.b00`–`.b13`, and the two `.jsn`
sidecars. It has **no `.b14` or above**, which is unusual rather than
incidental. Fleet-wide device counts per segment slot:

```
b00-b10, b12, b13   56 devices
b11                 35
b14-b18             52
b19-b23             50
b25                 48
b24                 39
b26, b27            37
b28, b29            36
```

[F] So **52 other devices carry `adsp.b14`** and this slice carries none of it.
The drop-off is not a cliff: `b00`–`b10` are on 56 devices, `b14`–`b18` on 52,
`b19`–`b23` on 50, then `b24` on 39 and `b28`/`b29` on 36. This slice's ADSP
image is the short form of the family — it stops four slots before the modal
device does [F].

[F] `cdsp` has **11** files: `.mdt`, `.b00`–`.b06`, `.b08`, `.b10`, and
`cdspr.jsn` — note the **gaps** at `.b07` and `.b09`. Segment numbering is a
program-header index and need not be dense (the `wpss` note proves
`b<NN> ≡ phdr NN` exactly); the gaps here are a real property of this build.

### 3.3 The finding: two of the six classes have no mainline driver

[F] The slice carries `cdsp.*` (22 rows) and `npu.*` (10 rows). Mainline
MSM8998 has **neither**:

```
grep -c 'cdsp' msm8998.dtsi   ->  0
grep -c 'npu'  msm8998.dtsi   ->  0
grep 'msm8998' qcom_q6v5_pas.c -> only -adsp-pas and -slpi-pas
```

[F] Compare SM8150, the SoC these devices actually are:
`sm8150.dtsi:3367` has `qcom,sm8150-cdsp-pas`. The contrast is exact — the
cdsp node exists one generation later and not here.

[I] This is a **fourth independent ground** for the mislabel, and unlike
#2018's grounds it is not GPU-specific. An MSM8998 has three remote processors;
the slice ships firmware for six DSP-class units including a compute DSP and an
NPU. A device cannot boot firmware for a processor its SoC does not have.

[F] The corpus-wide control: only 5 SoC labels carry **both** a `cdsp` family
and `npu.*` files — MSM8998 835 (this slice), SM7225, SM8150, SM8150-AC, and
SM8250. Every one of the other four is an SoC whose mainline DT *does* have a
cdsp node. MSM8998 is the only label where the firmware outruns the silicon.

### 3.4 Two honesty notes on `dsp.img`

[F] The largest single file in the slice is **not** any of the above: it is
`dsp.img`, **67,108,864 B = 64.00 MiB exactly**, on both devices, byte-identical.
It is labelled `blob_family=other`, `db_type=UNKNOWN`.

[F] `research/fleet/dsp-tz-map.md` §1 proves on OnePlus 6 that a Qualcomm
`dsp.img` of this kind is an **ext4 filesystem** with `/adsp`, `/cdsp` and
`/sdsp` directories holding 57 ELFs of `e_machine` 164. [I] The 64.00 MiB
round size here says partition dump, not image — the same mixed-column trap the
`boot` family has (§4.2) — and by the OnePlus 6 precedent it is very likely an
ext4 wrapper around adsp+cdsp+sdsp payload. **I did not verify that for this
device**; it needs the payload, which is out of scope [OPEN].

[F] The slice's `isa_identified` column is **empty on all 871 rows** and
`interface_documented` is `n` on all 871. So the matrix asserts nothing about
any DSP's ISA here. Hexagon 682 is the generational name a reader would expect
for an 835, but this corpus does not attest it [N].

## 4. Boot chain: 12 real rows / 6 images inside a family that is 97.9% partition dumps

### 4.1 The 17 rows

[F] The `boot` family is **17 rows / 9 filenames / 359,960,576 B**, split 8 rows
on `OnePlus_7` and 9 on `OnePlus_7T` (the extra row is a `recovery.img` the 7
does not have).

| file | size (B) | MiB | `db_type` | devices | kind |
|---|---:|---:|---|---|---|
| `xbl.img` | 3,182,592 | 3.035 | UEFIBOOT | 2 | real |
| `xbl_config.img` | 126,976 | 0.121 | ELF64 | 2 | real |
| `abl.img` | 225,280 | 0.215 | UEFIBOOT | 2 | real |
| `aop.img` | 204,800 | 0.195 | UNKNOWN | 2 | real |
| `qupfw.img` | 73,728 | 0.070 | ELF64 | 2 | real |
| `vbmeta.img` | 4,096 (7) / 8,192 (7T) | — | AVB | 2 | real |
| `boot.img` | 100,663,296 | **96.00** | BOOT | 2 | partition |
| `dtbo.img` | 25,165,824 | **24.00** | DTB | 2 | partition |
| `recovery.img` | 100,663,296 | **96.00** | BOOT | 1 (7T) | partition |

### 4.2 The mixed-column trap, re-derived

[F] Five rows are exact MiB multiples and hold **352,321,536 B of 359,960,576 B
= 97.9%** of the family. The other twelve rows — 6 distinct images, each
present on both devices — hold **7,639,040 B = 2.1%**.

[F] This is the same defect #1466 documented fleet-wide (364 of 1,038 boot rows
MiB-exact, 86.8% of family bytes — I re-ran that query and both figures are
unchanged). The consequence for *this* SoC package is blunt: **any byte-weighted
statement about "the boot chain" of these devices is a statement about
partition capacity** [F, I].

[F] The `vbmeta.img` size difference is the one genuinely interesting row:
**4,096 B on the 7 and 8,192 B on the 7T**, a clean doubling, both labelled
`AVB`. [I] A vbmeta image's size is `header + one descriptor per chained
partition` (each descriptor 64 B, with a 256 B header and auxiliary block); a
doubling is consistent with the 7T chaining roughly twice as many partitions as
the 7. I did **not** verify a descriptor count — that needs the payload [OPEN].

### 4.3 `mba.mbn` is absent from the entire corpus

[F] This is the sharpest negative in the note:

```
files in the corpus whose name ends .mbn:        0
rows whose name ends .mbn, of 33,917:            0
mba.mbn rows anywhere:                           0
mba.* rows anywhere, any spelling:               0
filename containing "mba":                       2
    oprec_camback_calibration.bin
    oprec_record_ID4_CamBack.bin
```

[F] Mainline requires it: `msm8998_mss.hexagon_mba_image = "mba.mbn"`
(`qcom_q6v5_mss.c:2391`). The MSS loader loads the MBA first, then the MDT.

[I] Therefore **the modem remoteproc on an MSM8998 cannot be booted from this
corpus at all** — the corpus has `modem.mdt` (§6) but no MBA, and the MBA is
what authenticates and starts the modem's own boot. This is not a defect of
these two devices; it is a corpus-wide absence of one file class, and it means
any "boot the modem from the matrix" workflow is blocked before it starts.

[F] The same absence explains why `ipa_fws.mdt` sits alone: `ipa_fws` is
`db_type=ELF64`, 7,020 B, and has no `.bNN` segments at all — it is one of the
6 genuinely single-file stems of §7.1.

### 4.4 The boot chain the device actually has

[I] Reading the **6 real `boot`-family images** (12 rows — one per device) as a
chain, and pulling in the `tz`-family images and the reserved-memory map (§5)
where the chain needs them:

1. **PBL** (in SoC ROM, absent from any corpus by construction) →
2. **`xbl.img`** (`UEFIBOOT`, 3.03 MiB) — the UEFI-stage bootloader; its
   mainline role is to set up the framebuffer the `simplefb` node inherits, and
   the pmOS wiki's OnePlus-5 instructions extract the display base address from
   exactly this file (`strings …/xbl | grep 'Display Reserved'`);
3. **`xbl_config.img`** (`ELF64`, 127 KiB) — XBL's configuration blob;
4. **`abl.img`** (`UEFIBOOT`, 225 KiB) — the Android bootloader, which
   implements fastboot;
5. **`aop.img`** — the Always-On Processor image;
6. **`qupfw.img`** (`ELF64`, 74 KiB) — QUP firmware;
7. **`tz.img` / `hyp.img` / `keymaster.img` / `devcfg.img`** — the secure side
   (§5);
8. **`boot.img`** — the Android boot image (kernel+ramdisk), here a 96 MiB
   partition dump, not an image.

[F] `qupfw` has **no mainline binding** — a GitHub code search over
`torvalds/linux` returns 0 hits for a qupfw binding. `abl` likewise has no
mainline node; it is a UEFI application, not a Linux concern. [I] Two of the
nine `boot` filenames are therefore opaque to the kernel entirely, and their
absence from `msm8998.dtsi` is correct rather than a gap.

## 5. TrustZone: the 45 MiB window, and the 12 MiB the sibling SoC adds

### 5.1 The reserved-memory map

[F] `msm8998.dtsi` declares **15** fixed-base reserved regions under
`reserved-memory` (`:30`–`:119`), totalling **236,015,616 B = 225.08 MiB**,
plus one `alloc-ranges` region (`mdata_mem`, `:114`–`:118`) that has no fixed
base.

| region | base | size (B) | MiB | gap before |
|---|---|---:|---:|---:|
| `hyp_mem` | `0x85800000` | 6,291,456 | 6.00 | — |
| `xbl_mem` | `0x85e00000` | 1,048,576 | 1.00 | 0 |
| `smem_mem` | `0x86000000` | 2,097,152 | 2.00 | 1,048,576 |
| `tz_mem` | `0x86200000` | 47,185,920 | **45.00** | 0 |
| `rmtfs_mem` | `0x88f00000` | 2,097,152 | 2.00 | 0 |
| `spss_mem` | `0x8ab00000` | 7,340,032 | 7.00 | 27,262,976 |
| `adsp_mem` | `0x8b200000` | 27,262,976 | 26.00 | 0 |
| `mpss_mem` | `0x8cc00000` | 117,440,512 | **112.00** | 0 |
| `venus_mem` | `0x93c00000` | 5,242,880 | 5.00 | 0 |
| `mba_mem` | `0x94100000` | 2,097,152 | 2.00 | 0 |
| `slpi_mem` | `0x94300000` | 15,728,640 | 15.00 | 0 |
| `ipa_fw_mem` | `0x95200000` | 65,536 | 0.06 | 0 |
| `ipa_gsi_mem` | `0x95210000` | 20,480 | 0.02 | 0 |
| `gpu_mem` | `0x95600000` | 1,048,576 | 1.00 | 4,108,288 |
| `wlan_msa_mem` | `0x95700000` | 1,048,576 | 1.00 | 0 |

[F] Two structural facts fall out:

- **`hyp` → `xbl` → `smem` → `tz` → `rmtfs` is contiguous from `0x85800000` to
  `0x890fffff`** — a **57.00 MiB span** holding **56.00 MiB of reservation**,
  i.e. one 1 MiB hole between `xbl_mem` and `smem_mem` and nothing else. This is
  the secure-side block, and it is contiguous *by construction*: the bootloader
  places these windows adjacent so TrustZone, the hypervisor and the
  shared-memory driver each get a fixed, non-overlapping reservation.
- **There are exactly three gaps** in the whole map — that same 1,048,576 B
  before `smem_mem`, 27,262,976 B between `rmtfs_mem` and `spss_mem`, and
  4,108,288 B between `ipa_gsi_mem` and `gpu_mem`. [I] Gaps are where the
  bootloader's own allocations fall (the `mem-attach`/`rpmh` regions), which is
  why they are not named here.

### 5.2 The generational delta: `tz_mem` grows 12 MiB, at the same base

[F] This is a clean, checkable comparison:

| SoC | `tz_mem` base | size | MiB |
|---|---|---|---|
| MSM8998 (835) | `0x86200000` | `0x2d00000` | **45** |
| SM8150 (855) | `0x86200000` | `0x3900000` | **57** |

[F] Same base, +12 MiB (+12,582,912 B). [I] The secure world's reserved window
is pinned to a fixed physical address across one generation and simply enlarged;
the TEE did not move, it grew. That is consistent with the SM8150 tz family
carrying more trustlets than 8998's 15 stems — but I did not test the
correspondence between window size and stem count across the fleet, so this is
an observation, not a law [I, OPEN].

### 5.3 The tz family in the slice

[F] `blob_family=tz` is **168 rows / 85 filenames / 15 stems / 19,779,884 B**,
83 rows on `OnePlus_7` and 85 on `OnePlus_7T`.

[F] The 15 stems are not a clean 9 + 6 split, because two stems ship **both**
forms:

| shape | count | stems |
|---|---:|---|
| split only (`.b00`–`.b07` + `.mdt`) | 7 | `hdcp1`, `hdcp2p2`, `hdcpsrm`, `smplap32`, `smplap64`, `soter64`, `widevine` |
| **both** split and monolithic | 2 | `cmnlib` (`.b00`–`.b05` + `.mdt` + `cmnlib.img` 397,312 B), `cmnlib64` (same shape, `cmnlib64.img` 516,096 B) |
| monolithic only | 6 | `tz.img` 3,190,784 B, `hyp.img` 491,520 B, `keymaster.img` 262,144 B, `devcfg.img` 57,344 B, `multiimgoem.img` 16,384 B, `uefisecapp.img` 126,976 B |

[F] So 9 stems carry segments and 8 carry an `.img`, with `cmnlib`/`cmnlib64`
in both sets. `docs/devices/oneplus/OnePlus_7/tz.md` already records this and
notes the two `.img` forms exceed their own segment sums by 6,514 B and
11,554 B respectively [OPEN].

[F] Only **two** tz files are single-device, both 7T-only: `multiimgoem.img`
(16,384 B) and `uefisecapp.img` (126,976 B). Everything else is on both.

[F] The per-file decomposition, the `tz.img` 2×2 md5 pairing, and the
generation-specific `mdt − b01 == b00` identity are all **`docs/devices/oneplus/OnePlus_7/tz.md` §2–§5**.
What this note adds about tz is one generalisation (§7.2), not a re-analysis.

## 6. The slice: 9 families, 21 `db_type`s, and one label defect

### 6.1 The family table

[F] **871 rows / 2 devices / 1,079,157,014 B / 423 distinct filenames.**

| family | rows | files | bytes | share |
|---|---:|---:|---:|---:|
| `modem` | 70 | 35 | 473,076,826 | **43.84%** |
| `boot` | 17 | 9 | 359,960,576 | **33.36%** |
| `other` | 452 | 212 | 186,754,850 | 17.31% |
| `adsp` | 34 | 17 | 27,471,208 | 2.55% |
| `tz` | 168 | 85 | 19,779,884 | 1.83% |
| `cdsp` | 22 | 11 | 7,057,150 | 0.65% |
| `bt` | 32 | 16 | 3,046,992 | 0.28% |
| `wifi` | 68 | 34 | 1,790,304 | 0.17% |
| `gpu` | 8 | 4 | 219,224 | 0.02% |
| **total** | **871** | **423** | **1,079,157,014** | |

[F] Per device:

| device | codename | rows | files | bytes |
|---|---|---:|---:|---:|
| `OnePlus_7` | `guacamoleb` | 433 | 418 | 494,092,577 |
| `OnePlus_7T` | `hotdogb` | 438 | 423 | 585,064,437 |

[F] No filename appears in more than one family — 0 of 423 are cross-labelled,
so the family partition is a clean partition of the filename set.

[F] `db_type` spans **21** values: UNKNOWN 360, ELF64 120, WIFI_BLUETOOTH 66,
CELL 60, DRM 48, SECURITY 34, MODEM 34, FINGERPRINT 34, FASTCHG 26, OLED 22,
COMPUTE 20, TOUCHSCREEN 18, GPU 6, BOOT 5, UEFIBOOT 4, BLUETOOTH 4, DTB 2,
SECUREBOOT 2, CELL_WIFI_GPS_BLUETOOTH 2, AVB 2, WIFI 2.

[F] Two columns are empty across the whole slice: `isa_identified` (871 empty)
and `sha256_if_listed` (0 populated). Whatever ISA claims the corpus makes
fleet-wide, it makes none here.

### 6.2 The four devices are one firmware family, 99.5% by file set

[F] The `soc` column assigns these four devices **two different labels**. Their
filename sets do not agree with that split:

| device | `soc` label | files |
|---|---|---:|
| `OnePlus_7` | MSM8998 835 | 418 |
| `OnePlus_7_Pro` | SM8150 855 | 420 |
| `OnePlus_7T` | MSM8998 835 | 423 |
| `OnePlus_7T_Pro` | SM8150-AC 855+ | 421 |

[F] Jaccard overlap of the *filename sets*:

```
OnePlus_7     ~ OnePlus_7_Pro    418 / 420 -> 0.9952
OnePlus_7T    ~ OnePlus_7T_Pro   421 / 423 -> 0.9953
OnePlus_7     ~ OnePlus_7T       418 / 423 -> 0.9882
OnePlus_7     ~ OnePlus_7T_Pro   417 / 422 -> 0.9882
OnePlus_7_Pro ~ OnePlus_7T_Pro   418 / 423 -> 0.9882
OnePlus_7_Pro ~ OnePlus_7T       420 / 423 -> 0.9929
```

[F] The ordering is the finding, and it is not the one the `soc` column predicts.
**The two same-codename pairs (7↔7_Pro, 7T↔7T_Pro) are 0.9952/0.9953 — the two
highest. The four cross-grouping pairs are 0.9882/0.9882/0.9882/0.9929, and
7_Pro↔7T is the odd one at 0.9929, above the other three.** That is the
codename grouping, not the `soc` grouping — and it is the same signal the
per-file md5 table gives, measured on filenames alone.

[F] And **every one of the 8 non-`other` families has an identical filename
set** across the `OnePlus_7T` ↔ `OnePlus_7T_Pro` pair — name-for-name, not
byte-for-byte:

```
adsp   17/17 identical sets
cdsp   11/11 identical sets
tz     85/85 identical sets
gpu     4/4  identical sets
wifi   34/34 identical sets
bt     16/16 identical sets
modem  35/35 identical sets
boot    9/9  identical sets
other 212/210 (2 in 7T but not 7T_Pro: gfp9508.mdt, gfp9608.mdt)
```

[F] Across all four devices, **314 of the 417 shared filenames are
md5-identical**. [I] The `soc` column says {7, 7T} are 835 and {7_Pro, 7T_Pro}
are 855/855+. The file sets say all four are one build family with a
per-SKU overlay. The firmware is the primary evidence and the column is a
hand-entered string — which is exactly the argument #2018 makes in its §2.2,
now shown at
package scale rather than GPU scale.

[F] `docs/devices/oneplus/OnePlus_7T_Pro/boot.md` §5 already established the
per-file md5 grouping for `boot` and showed the codenames
(`guacamole`/`guacamoleb`, `hotdog`/`hotdogb`) follow the md5 groups, not the
`soc` column. This section is that finding's **package-wide** counterpart: the
whole 423-filename set, not 9 boot rows.

### 6.3 The label defect: 118 rows of DSP trustlets filed under `other`

[F] The slice has real `adsp` and `cdsp` families, but five DSP-class stems are
labelled `other`:

```
slpi.*      44 rows   blob_family=other
npu.*       10 rows   blob_family=other
venus.*     12 rows   blob_family=other
spss1p.*     8 rows   blob_family=other
spss2p.*     8 rows   blob_family=other
```

[F] Adding `rtic.*` (18 rows / 9 files) and `cppf.*` (18 rows / 9 files) gives
**118 rows / 59 files** of DSP-class or trustlet payload outside the DSP
families. Note this is a *union* of two different groupings: `cppf` also
appears inside §6.4's eSE group, and `rtic` there gets its own row — so the
118 measures how much payload the family label hides, not how much is
unclassified.

[I] Any census that groups by `blob_family` — including
`research/cdsp-fleet/census.md`'s per-SoC table, where this SoC shows
`2 devices / 22 rows / 11 files` — is measuring the *label*, and the label
undercounts the DSP surface here by 118 rows. Recorded as a data-quality
finding; I did not change any row.

### 6.4 What the 452 `other` rows actually are

[F] The `other` family is 17.31% of the bytes but **51.9% of the rows** (452 of
871), so it cannot be left as "misc". Grouping its 212 filenames by stem:

| group | rows | files | bytes | share of `other` |
|---|---:|---:|---:|---:|
| `dsp.img` partition dump | 2 | 1 | 134,217,728 | **71.87%** |
| fingerprint (`fingerpr`, `gfp*`) | 22 | 12 | 14,000,512 | 7.50% |
| SLPI DSP (`slpi`, `slpir`, `slpius`) | 48 | 24 | 12,269,976 | 6.57% |
| boot logo (`LOGO.img`) | 2 | 1 | 9,986,048 | 5.35% |
| display panel + touch (`FW_*`, `LIMIT_*`) | 78 | 30 | 6,592,208 | 3.53% |
| eSE trustlets (9 stems: `cpe_9340`, `cppf`, `eseservi`, `gpqese`, `gptest`, `haventkn`, `mldapta`, `securemm`, `voicepri`) | 170 | 85 | 2,584,484 | 1.38% |
| `venus` video | 12 | 6 | 2,222,528 | 1.19% |
| `spss` secure processor | 16 | 8 | 2,152,032 | 1.15% |
| storage GPT (`data.msc`, `gptauuid.xml`) | 4 | 2 | 1,193,724 | 0.64% |
| `rtic` trustlet | 18 | 9 | 594,522 | 0.32% |
| keystore material (`keym*`, `crypt*`, `asym*`) | 12 | 6 | 589,856 | 0.32% |
| `npu` trustlet | 10 | 5 | 121,096 | 0.06% |
| fast charge (`oplus_vooc_fw.bin`) | 10 | 1 | 67,088 | 0.04% |
| `storsec.img` | 2 | 1 | 49,152 | 0.03% |
| signature manifests (`.dig`, `.txt`) | 14 | 7 | 46,868 | 0.03% |
| camera calibration | 22 | 11 | 27,136 | 0.01% |
| haptics (`awinic_*`) | 8 | 2 | 26,172 | 0.01% |
| IPA offload (`ipa_uc.mdt`) | 2 | 1 | 13,720 | 0.01% |
| **total** | **452** | **212** | **186,754,850** | |

[F] One dominant fact: **`dsp.img` alone is 71.87% of `other` and 12.4% of the
whole slice**, so any analysis of `other` that does not handle `dsp.img`
separately is dominated by a single partition dump.

[F] The display group is vendor-specific and self-identifying: `FW_S3706_SAMSUNG`
and `FW_S6SY761_SAMSUNG` are touch controller firmware (Samsung's S6SY761 is a
touchscreen IC), `FW_NT36672C_NF_JDI`/`_BOE` are Novatek display driver ICs for
JDI and BOE panels, and `LIMIT_*` are the per-panel limit tables. [I] The
`_FAE`/`_NEW`/`_OLD`/`_TEST` suffixes are field-application-engineering and
qualification variants, i.e. development artefacts shipping on a retail
partition.

[F] The eSE group is the largest by file count (85) and among the smallest by
bytes (1.38%). It is **9 stems**, and 8 of them share one shape: `.mdt` +
`.b00`–`.b07` split trustlets whose per-device payload runs from **28,212 B**
(`cppf`) to **186,227 B** (`voicepri`). The ninth, **`cpe_9340`, is the
outlier** — 13 files, a 724 B `.mdt`, and segments numbered
`.b01/.b03/.b05/…/.b20` with no `.b00` and no dense numbering: 416,960 B,
i.e. **32.3% of the group's bytes in one stem** [F].

[I] These are the embedded Secure Element applets (GP QESE, eSE service,
keymaster-in-SE, etc.), which live in the `tz` world functionally but were
filed as `other` here. `cpe_9340` is the outlier structurally as well as
numerically, and §7.1 records why.

[F] The keystore material is notable for what it *is not*: 6 `.sig` files,
`asym1p.sig` 20,592 B / `asym2p.sig` 20,624 / `crypt2p.sig` 37,088 /
`crypt1p.sig` 41,152 / `keym2p.sig` 83,664 / `keym1p.sig` 91,808 — a
20–90 KiB spread. [I] These are signed licence/feature containers, and their
presence as **separate files** rather than segments means they are not PIL
images at all. No payload was read to confirm [OPEN].

## 7. Two laws the two-device sample can actually test

The 871 rows are two devices of one product family, so most fleet laws cannot
be tested here. Two can.

### 7.1 `mdt == b00 + b01` holds 27 of 27, and the 7 untestable stems are not one thing

[F] 34 stems carry a `.mdt`. Of those, 27 also carry both `.b00` and `.b01`:

```
testable stems (mdt + b00 + b01):  27
  mdt == b00 + b01:                27
  violations:                       0
```

[F] The 7 remaining stems are **not** one uniform group, and the distinction
matters:

| stem | `.mdt` | segments besides `.mdt` | why untestable |
|---|---:|---:|---|
| `a640_zap` | 6,860 | 0 | single-file MDT |
| `gfp9508` | 7,464 | 0 | single-file MDT |
| `gfp9558` | 7,464 | 0 | single-file MDT |
| `gfp9608` | 7,260 | 0 | single-file MDT |
| `ipa_fws` | 7,020 | 0 | single-file MDT |
| `ipa_uc` | 6,860 | 0 | single-file MDT |
| `cpe_9340` | **724** | **12** | **has `.b01` but no `.b00`** |

[F] Six of them are genuinely self-contained: their `.mdt` is the whole image
and there is no `.b00`/`.b01`/`.bNN` at all.

[F] **`cpe_9340` is a third structural case, and a rule written from the other
six would get it wrong.** It carries `.b01`, `.b03`, `.b05`, `.b06`, `.b07`,
`.b09`, `.b11`, `.b13`, `.b15`, `.b16`, `.b18`, `.b20` — twelve segments, not
one — and it is the
**only stem in the slice with a `.b01` but no `.b00`**. Its `.mdt` is 724 B
against **416,960 B** of total segment bytes, so the `.mdt` is a 724-byte
header over a 407 KiB image, not the image. The `mdt == b00 + b01` test simply
has no left-hand addend here; the stem is untestable, not self-contained.

[I] That makes the slice's `.mdt` stems fall into **three** shapes, not two:
fully split with a `.b00` header (27), header-only with no segments (6), and
segmented-but-`b00`-less (1). A rule that reads "no `.b00` ⇒ self-contained"
would be wrong on `cpe_9340`.

[F] The law is exact here, including for the `tz` stems, and that is
*consistent with* `tz.md` §5's fleet finding that this device is on the clean
side of a 190-of-399 fleet violation. [I] But 27/27 on a two-device sample says
nothing about the fleet — it says that both devices in this slice are the same
build. The distinction matters and is the reason `tz.md` §5, not this section,
is the authority on the law's reach.

[F] The `mdt` decomposition, per stem and identical for both devices:

| stem | `.mdt` | `.b00` | `.b01` | check |
|---|---:|---:|---:|---|
| `cmnlib` | 20,228 | 244 | 19,984 | 244 + 19,984 = 20,228 |
| `cmnlib64` | 20,384 | 400 | 19,984 | 400 + 19,984 = 20,384 |
| `hdcp1` | 7,464 | 512 | 6,952 | 7,464 |
| `hdcp2p2` | 7,464 | 512 | 6,952 | 7,464 |
| `hdcpsrm` | 7,464 | 512 | 6,952 | 7,464 |
| `smplap32` | 7,260 | 308 | 6,952 | 7,260 |
| `smplap64` | 7,464 | 512 | 6,952 | 7,464 |
| `soter64` | 7,464 | 512 | 6,952 | 7,464 |
| `widevine` | 7,464 | 512 | 6,952 | 7,464 |
| `adsp` | 7,820 | 532 | 7,288 | 7,820 |
| `cdsp` | 7,580 | 436 | 7,144 | 7,580 |
| `modem` | 9,260 | 1,108 | 8,152 | 9,260 |
| `slpi` | 8,380 | 756 | 7,624 | 8,380 |

[F] `b00` size decomposes as an ELF header plus 32 B per program header:
`52 + 32N` for ELF32, `64 + 32N` for ELF64. Across all 27 testable stems:
**13 fit ELF32, 13 fit ELF64, and exactly one fits neither** — `cmnlib64`'s
**400 B** (400 − 64 = 336, not a multiple of 32; 400 − 52 = 348, not either)
[F, OPEN]. Worked examples: `cmnlib` 244 = 52+32·6; `smplap32` 308 = 52+32·8;
`adsp` 532 = 52+32·15; `cdsp` 436 = 52+32·12; `slpi` 756 = 52+32·22;
`modem` 1108 = 52+32·33; `spss1p` 148 = 52+32·3; `npu`/`venus` 212 = 52+32·5.
The **thirteen** 512 B headers are all `64 + 32·14`, and they are the whole
ELF64 side of the table.

[F] That single exception is worth recording because the SM8350 note found **0
non-fits on 23 stems** — so `.b00` size is not universally a clean
header+phdr sum.

[F] `cmnlib64` is anomalous twice over. Its 400 B header is *not* the 512 B that
every other 64-bit trustlet in this slice uses (thirteen do), and it is the only
`*64` stem that fails both formulae. So the `64` suffix does **not**
predict the ELF class here: `cmnlib64`'s header is neither the 52-byte ELF32
base nor the 64-byte ELF64 base plus whole program headers [F, OPEN].

### 7.2 Code-segment variance is a perfect remoteproc detector — 34 of 34

This is the note's one genuinely new law. `tz.md` §4 established, for the *tz*
family only, that the files differing between OnePlus_7 and OnePlus_7T fall
exactly on `.b01`, `.mdt` and `.img`, and never on a code segment. Tested across
**all 34 `.mdt`-carrying stems in the slice**, the pattern splits cleanly and
the split is not arbitrary [F]:

```
stems whose code segments (b02+) DIFFER between the two devices:   4
stems whose code segments are identical:                          30

the 4 that differ, exactly:
  adsp    b00 b01 b02 b03 b04 b05 b08 b09 b10 b11 b12 mdt
  cdsp    b01 b05 b08 mdt
  modem   b01 b04 b07 b09 b13 b19 b21 b24 b26 b31 img mdt
  slpi    b00 b01 b02 b03 b04 b12 b14 b15 b16 b17 b18 b19 b20 mdt
```

[F] Those four stems are precisely the four real remote processors of §3.1 —
`adsp`, `cdsp`, `modem`, `slpi`. The correspondence is **34 of 34, with no
exception in either direction**:

- every stem whose code differs is a real remoteproc (4 of 4);
- every stem whose code is identical is not (30 of 30) — including all 9 tz
  stems that carry segments, all 85 tz files, and the `npu`/`venus`/`spss`
  trustlets.

[F] The 30 code-identical stems are themselves three groups: **16** differ in
exactly `{mdt, b01}`, **11** are byte-identical outright (`a640_zap`,
`cpe_9340`, `eseservi`, `gfp9558`, `gfp9608`, `gpqese`, `ipa_fws`, `ipa_uc`,
`mldapta`, `spss1p`, `spss2p`), and **3** differ in something else entirely
(`cmnlib` and `cmnlib64` in `{b01, img, mdt}`; `gfp9508` in `{mdt}` alone).
There is no two-way split here; the three-way one is the measured shape [F].

[I] **Why this works, and why it is useful.** `b01` is the program-header table:
it carries per-build segment addresses, sizes and the hash slot, so it
necessarily changes when a build is re-signed — which is why `tz.md` §4 sees it
differ everywhere. A *code* segment, `b02` onward, only changes when the
payload itself changed. The two devices in this slice are the same hardware
family (§6.2) with the same silicon, so the only payloads that need to differ
are the ones whose contents encode per-SKU configuration — and the four
remoteprocs are exactly those, because the modem, ADSP, CDSP and SLPI images
are built per **carrier/market SKU**, while the TrustZone trustlets and the
static trustlets are not.

[I] **Practical consequence for the lab.** Code-segment variance across a
matched device pair is a *labelling-free* remoteproc detector: it identifies
which stems are real PAS images without consulting `blob_family`, `db_type`, or
any vendor document. On this slice it would have recovered the correct
`slpi` classification that §6.3 shows the label got wrong.

### 7.3 Size is device-invariant even where content is not

[F] Every tz segment has the **same size** on both devices — **0 of 77** segment
names (`*.mdt` and `*.bNN`) differ in size — while **24 of 85** files differ in
content. [F] The same holds for `wifi` (34 files, **0** differing) and `cdsp`
(11 files, **0** size differences, but 4 content differences in `b01`, `b05`,
`b08`, `mdt`).

[F] Counter-example inside the same slice: `adsp` has **5** segments whose
**sizes** differ — `b08` (549,872 → 345,432), `b09` (116 → 76),
`b10` (9,317,340 → 9,424,440), `b11` (549,120 → 344,672) and
`b12` (3,848 → 2,696), reading `OnePlus_7` → `OnePlus_7T`. Note the
directions disagree: `b08`, `b09`, `b11` and `b12` all **shrink** while `b10`
**grows** by 107,100 B. [I] So
size-invariance is a property of *static* payloads, not of the corpus; a real
remoteproc's image can and does change size between SKUs. This is the same
signal as §7.2 seen from the size column instead of the hash column.

## 8. Mainline and postmarketOS status

### 8.1 Mainline: real support, for other boards

[F] `arch/arm64/boot/dts/qcom/` carries **15** `msm8998-*` files:
`msm8998.dtsi`, `msm8998-clamshell.dtsi`, and 13 board files — of which two
are includes, not boards (`msm8998-clamshell.dtsi` for the three clamshells,
`msm8998-sony-xperia-yoshino.dtsi` for the three Sonys), leaving **11 real
board DTs**.

[F] `Documentation/devicetree/bindings/arm/qcom.yaml` enumerates **11** board
`compatible`s against `const: qcom,msm8998` — the count and the list agree
exactly: `asus,novago-tp370ql`, `fxtec,pro1`, `hp,envy-x2`, `lenovo,miix-630`,
`oneplus,cheeseburger`, `oneplus,dumpling`, `qcom,msm8998-mtp`,
`sony,xperia-lilac`, `sony,xperia-maple`, `sony,xperia-poplar`, `xiaomi,sagit`.

[F] The Sony models are easy to conflate, and the codenames do not help: three
different phones ship under them — `lilac` = **Xperia XZ1 Compact**,
`maple` = **Xperia XZ Premium**, `poplar` = **Xperia XZ1** (read from each DT's
`model` property, 2026-11-22).

[F] **Neither device in this slice has a DT under either label**: 0 files match
`guacamole`, 0 match `hotdog`, and the `sm8150-*` set is `sm8150-hdk`,
`sm8150-mtp`, `sm8150-microsoft-surface-duo`, three Sony `kumano` files and
`sm8150.dtsi` — no OnePlus board at all.

[F] `linux-msm.github.io/mainline-status/soc/msm8998` (fetched 2026-11-22)
records the support matrix: GCC 4.19, pinctrl 4.19, UART 4.19, I2C 4.8, SPI 6.4,
UFS 5.1, SD/eMMC 4.2, PCIe 5.2, **ADSP 5.5, SLPI 5.5, MDSP 5.5**, and
**CDSP `N/A`, FastRPC/compute `N`**. That last pair is the third-party
confirmation of §3.3 — an MSM8998 has no CDSP to support.

[F] The LKML record matches: `[PATCH 09/16] remoteproc: qcom: pas: Add MSM8998
ADSP and SLPI support`, Sibi Sankar, 2019-11-18, added exactly two descriptors
(`msm8998_adsp_resource`, `msm8998_slpi_resource`), and v2 on 2019-12-18 kept it
at two. A follow-up thread on 2021-05-07 collapsed them onto the MSM8996
resources — which is the state the code is in today (§3.1).

[F] `arch/arm64/configs/defconfig` has the pieces enabled: `QCOM_Q6V5_PAS=m`
(1525), `QCOM_Q6V5_MSS=m` (1524), `QCOM_Q6V5_ADSP=m` (1523), `QCOM_SYSMON=m`,
`QCOM_RPMPD=y`, `QCOM_SMEM=y`, `DRM_MSM=m`, `ATH10K_SNOC=m`.

### 8.2 linux-firmware ships no MSM8998 payload

[F] The `qcom/` directory of `linux-firmware` (`git.kernel.org`, `?h=main`,
fetched 2026-11-22) has **31 subdirectories and no `msm8998` entry**. Of the
files an Adreno 540 needs:

```
qcom/a530_pm4.fw     HTTP 200
qcom/a530_pfp.fw     HTTP 200
qcom/a530_zap.mdt    HTTP 404
qcom/a540_gpmu.fw2   HTTP 404
qcom/a540_zap.mdt    HTTP 404
qcom/msm8998/adsp.mdt HTTP 404
qcom/msm8998/slpi.mdt HTTP 404
qcom/msm8998/modem.mdt HTTP 404
qcom/msm8998/mba.mbn  HTTP 404
```

[F] The A5xx listing is exactly three entries — `a530_pfp.fw`, `a530_pm4.fw`,
`a530v3_gpmu.fw2` — so the 530 firmware that *does* ship is present, and the
540-specific GMU and ZAP are not.

[I] Combined with §4.3, the picture is consistent and bleak: **no public
firmware exists for this SoC's modem boot (no MBA), no public a540 GMU/ZAP, and
no public MSM8998 directory at all.** Whatever runs an 835 in the mainline
community runs it from a vendor dump.

### 8.3 postmarketOS packages these two devices as SM8150

[F] `gitlab.com/postmarketOS/pmaports`, `device/testing`, 2026-11-22:

```
device-oneplus-guacamole   OnePlus 7 Pro    depends linux-postmarketos-qcom-sm8150
device-oneplus-hotdogb     OnePlus 7T       depends linux-postmarketos-qcom-sm8150
```

[F] Their `deviceinfo` files name SM8150 DTs directly:

```
device-oneplus-guacamole: deviceinfo_dtb="qcom/sm8150-oneplus-guacamole"
device-oneplus-hotdogb:   deviceinfo_dtb="qcom/sm8150-oneplus-hotdogb"
```

[F] **There is no `device-oneplus-guacamoleb` package in any of
`device/{main,community,testing,archived}`.** The OnePlus 7 *Pro* is packaged;
the OnePlus 7 (non-Pro, `guacamoleb`) is not.

[F] Package age: `device-oneplus-guacamole`'s most recent commit is 2024-06-23
(`treewide: drop PMOS_NO_OUTPUT_REDIRECT`, MR 5240); `device-oneplus-hotdogb`
was added 2023-10-16 (MR 4451) and last touched 2024-04-22 (`devices: use
consistent pkgver`, MR 4994).

[F] By contrast the *genuine* 835 devices are packaged differently:
`device-oneplus-cheeseburger` (OnePlus 5) uses
`deviceinfo_dtb="qcom/msm8998-oneplus-cheeseburger"` and does **not** depend on
a `linux-postmarketos-qcom-*` vendor kernel — it tracks a closer-to-mainline
config with `deviceinfo_kernel_cmdline_mainline`. `device-oneplus-cheeseburger-downstream`
and `linux-oneplus-msm8998-downstream` sit in `device/archived`.

[F] The postmarketOS wiki agrees. The `Qualcomm Snapdragon 835 (MSM8998)` page
(mirror revision 2023-08-01) lists CPU "4x 2.45 GHz Kryo 280 Gold, 4x 1.9 GHz
Kryo 280 Silver", GPU "Adreno 540", 10 nm, **Mainline: yes**, and per-component
state: CPU *Partial*, Storage *Works*, USB *Works*, Display *Partial*, GPU
**Broken**, Pinctrl *Works*, Audio *Works*, WiFi *Works*, Bluetooth *Works*,
Modem *Partial*, GPS *Works*.

[F] The wiki's `OnePlus 7 (oneplus-guacamoleb)` page (last edited
2023-04-23) states **Chipset: Qualcomm Snapdragon 855 (SM8150)**, CPU
"1x2.96 GHz Kryo 485 & 3x2.42 GHz Kryo 485 & 4x1.78 GHz Kryo 485",
GPU **Adreno 640**, and covers `guacamoleb`, `guacamole` and `hotdogb`
together. That is a **fourth independent, non-lab source** putting these
devices on SM8150 — after #2018's LineageOS evidence [F].

[I] So the honest statement of community support is: **MSM8998 has real
mainline support for 11 boards, none of which are in this slice; the two
devices in this slice are supported as SM8150 boards instead.** The 835 wiki
page's "Mainline: yes" and the slice's "MSM8998 835" label describe the same
SoC string and two disjoint sets of hardware.

## 9. Honest negatives

1. **No instruction-level CPU proof exists in this corpus, and I did not
   manufacture one** [N]. `isa_identified` is empty on all 871 rows; mainline's
   DT gives all eight cores one `qcom,kryo280` string with no MIDR; no payload
   was read. §1.2 states the MIDR the kernel expects (`0x51008000` /
   `0x51008010`) and says plainly that observing it needs `MIDR_EL1` from a
   booted device.
2. **I did not parse a single ELF, MDT or ext4 image** [N]. Every size, hash and
   device count is the matrix or the DT. The `dsp.img`-is-ext4 claim is
   *borrowed* from `research/fleet/dsp-tz-map.md` on OnePlus 6 and explicitly
   **not** verified here (§3.4).
3. **The `b01`-only variance law is prior art** [F]. `docs/devices/oneplus/OnePlus_7/tz.md`
   §4 established it for the tz family on 2026-11-20. My §7.2 generalises it to
   all 34 stems and adds the remoteproc correspondence; the underlying law is
   not mine and I claim no credit for it.
4. **The 2×2 md5 grouping is prior art too** [F].
   `docs/devices/oneplus/OnePlus_7T_Pro/boot.md` §5 built the four-device table
   for `boot`. §6.2 extends it to the 423-filename set; the per-file table is
   theirs.
5. **`mdt == b00 + b01` on 27/27 is a two-device result, not a fleet law** [F, I].
   `tz.md` §5 shows the law fails on 190 of 399 fleet-wide. This slice is on the
   clean side because both its devices are one build.
6. **I cannot explain `cmnlib64.b00 = 400`** [OPEN]. It fits neither
   `52 + 32N` nor `64 + 32N`. Every other `.b00` in the slice fits one of the
   two. Recorded, not resolved — resolving it needs the header.
7. **`multiimgoem.img` and `uefisecapp.img` are 7T-only and unexplained** [OPEN].
   Both are tz-family, both single-device. I did not determine whether the 7
   genuinely lacks these partitions or the extraction missed them; a stock
   partition walk would settle it.
8. **`vbmeta.img` doubling from 4,096 to 8,192 B is an inference, not a
   measurement** [I, OPEN]. The descriptor-count explanation is consistent with
   the AVB format but was not verified against the payload.
9. **`dsp.img` 12.4% of the slice is a partition dump whose contents I did not
   inspect** [N, OPEN]. The OnePlus 6 precedent says ext4 with adsp/cdsp/sdsp
   inside; this device's 64.00 MiB round size is consistent with that but is not
   proof.
10. **The `blob_family` label defect (§6.3) is reported, not fixed** [F]. I
    changed no row: `slpi`/`npu`/`venus`/`spss` remain `other`. Fixing the
    matrix is outside this issue's file wall.
11. **`blob_subfamily` is unhelpful for this slice** [F]: 349 rows blank, 336
    `misc`, and the rest a thin tail (`wpss` 68, `fastchg` 26, `camera` 22,
    `oled` 22, `touch` 18, `fingerprint` 16, `media` 12, `hyp` 2). No
    DSP-class subfamily exists, which is why §6.3 had to group by stem.
12. **I did not verify the reserved-memory map against a running device** [N].
    §5.1 is read from `msm8998.dtsi`, which is mainline's model of the SoC, not
    the vendor's. A vendor `xbl`/`dtbo` would be the authority, and the two
    devices' `dtbo.img` are 24 MiB partition dumps I did not unpack.

## Reproduce

Every number above is regenerated by these commands. All are `python3 -I`,
stdlib only, run from the repository root.

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm MSM8998 Snapdragon 835']
tot=sum(int(r['size_bytes']) for r in s)
print('slice',len(s),'devices',len({r['device'] for r in s}),'bytes',tot,'files',len({r['filename'] for r in s}))
for f in sorted({r['blob_family'] for r in s}):
    rs=[r for r in s if r['blob_family']==f]
    b=sum(int(r['size_bytes']) for r in rs)
    print(f,len(rs),len({r['filename'] for r in rs}),b,round(100*b/tot,2))
for d in sorted({r['device'] for r in s}):
    rs=[r for r in s if r['device']==d]
    print(d,len(rs),len({r['filename'] for r in rs}),sum(int(r['size_bytes']) for r in rs))
print(Counter(r['db_type'] for r in s).most_common())"
```

```bash
python3 -I -c "
import csv,re
from collections import defaultdict
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm MSM8998 Snapdragon 835']
st=defaultdict(lambda: defaultdict(dict)); fam={}
for r in s:
    m=re.match(r'^(.+?)\.(mdt|b\d\d|img)$',r['filename'])
    if m:
        st[m.group(1)][m.group(2)][r['device']]=r['md5_db']
        fam.setdefault(m.group(1),r['blob_family'])
code=[];flat=[]
for name in sorted(st):
    d=st[name]
    if 'mdt' not in d: continue
    diff={k for k in d if len(set(d[k].values()))>1}
    (code if diff-{'mdt','b01','img'} else flat).append(name)
real={'adsp','cdsp','modem','slpi'}
print('code-varies',len(code),sorted(code))
print('flat',len(flat))
print('match',len([x for x in code if x in real])+len([x for x in flat if x not in real]),'of',len(code)+len(flat))"
```

```bash
python3 -I -c "
import csv,re
from collections import defaultdict
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm MSM8998 Snapdragon 835']
stem=defaultdict(dict)
for r in s:
    m=re.match(r'^(.+?)\.(mdt|b\d\d)\$',r['filename'])
    if m: stem[m.group(1)][m.group(2)]=int(r['size_bytes'])
test=[k for k,v in stem.items() if 'mdt' in v and 'b00' in v and 'b01' in v]
eq=[k for k in test if stem[k]['mdt']==stem[k]['b00']+stem[k]['b01']]
selfc=[k for k,v in stem.items() if 'mdt' in v and ('b00' not in v or 'b01' not in v)]
withmdt=[k for k,v in stem.items() if 'mdt' in v]
single=[k for k in selfc if len(stem[k])==1]
segless=[k for k in selfc if len(stem[k])>1]
print('all bNN stems',len(stem),'with mdt',len(withmdt),'testable',len(test),'equal',len(eq))
print('untestable',len(selfc),'-> single-file MDT',len(single),'segmented but no b00',len(segless),segless)
print('bNN stems without mdt',sorted(set(stem)-set(withmdt)))
for k in sorted(test):
    v=stem[k]; print(k,v['mdt'],v['b00'],v['b01'],v['mdt']==v['b00']+v['b01'])"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
b=[r for r in rows if r['blob_family']=='boot' and r['soc'].strip()=='Qualcomm MSM8998 Snapdragon 835']
part=[r for r in b if int(r['size_bytes'])%1048576==0]
tot=sum(int(r['size_bytes']) for r in b); pt=sum(int(r['size_bytes']) for r in part)
print('boot rows',len(b),'partition-dump rows',len(part),'bytes',tot,'dump bytes',pt,round(100*pt/tot,1))
for r in sorted(b,key=lambda r:r['filename']):
    v=int(r['size_bytes']); print(r['filename'],v,round(v/1048576,4),r['device'],r['db_type'])"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
print('mbn rows in 33917:',sum(1 for r in rows if r['filename'].endswith('.mbn')))
print('mba rows:',sum(1 for r in rows if r['filename'].startswith('mba')))
fns={r['filename'] for r in rows if r['soc'].strip()=='Qualcomm MSM8998 Snapdragon 835'}
for w in ('mba.mbn','mba.mdt','adsp.mbn','modem.mdt','adsp.mdt','slpi.mdt','cdsp.mdt','npu.mdt','venus.mdt','ipa_fws.mdt'):
    print(w,'PRESENT' if w in fns else 'ABSENT')
lbl=Counter()
for soc in sorted({r['soc'].strip() for r in rows}):
    rs=[r for r in rows if r['soc'].strip()==soc]
    c=Counter(r['blob_family'] for r in rs); n=sum(1 for r in rs if r['filename'].startswith('npu'))
    if c.get('cdsp') and n: print('cdsp+npu label:',repr(soc),c['cdsp'],n)"
```

```bash
python3 -I -c "
import csv
from collections import defaultdict
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
devs=['OnePlus_7','OnePlus_7_Pro','OnePlus_7T','OnePlus_7T_Pro']
h=defaultdict(dict)
for r in rows:
    if r['device'] in devs: h[r['device']][r['filename']]=r['md5_db']
for a in devs:
    for b in devs:
        if a>=b: continue
        sh=set(h[a])&set(h[b]); j=len(sh)/len(set(h[a])|set(h[b]))
        same=sum(1 for k in sh if h[a][k]==h[b][k])
        print(a,b,'shared',len(sh),'identical',same,'jaccard',round(j,4))"
```

```bash
python3 -I -c "
import csv
from collections import defaultdict,Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm MSM8998 Snapdragon 835']
o=[r for r in s if r['blob_family']=='other']
def g(f):
    l=f.lower()
    if f=='dsp.img': return 'dsp-dump'
    if l.startswith(('fw_','limit_')): return 'panel-touch'
    if l.startswith(('goldresult','arccali')) or 'golden' in l or 'calibration' in l or 'distortion' in l: return 'cam-cal'
    if l.startswith('logo'): return 'logo'
    if l.startswith(('keym','crypt','asym')): return 'keystore'
    if l.endswith(('.dig','.txt')): return 'sig-manifest'
    if l.startswith(('cpe_9340','cppf','eseservi','gpqese','gptest','haventkn','mldapta','securemm','voicepri')): return 'ese'
    if l.startswith('rtic'): return 'rtic'
    if l.startswith('npu'): return 'npu'
    if l.startswith('venus'): return 'venus'
    if l.startswith(('slpi','slpir','slpius')): return 'slpi'
    if l.startswith(('spss1p','spss2p')): return 'spss'
    if l.startswith('fingerpr'): return 'finger'
    if l.startswith('gfp'): return 'finger-gfp'
    if l.startswith('ipa_uc'): return 'ipa'
    if 'vooc' in l: return 'fastchg'
    if 'haptic' in l: return 'haptic'
    if l in ('data.msc','gptauuid.xml'): return 'gpt'
    if l.startswith('storsec'): return 'storsec'
    return 'uncl'
grp=defaultdict(list)
for r in o: grp[g(r['filename'])].append(r)
tot=sum(int(r['size_bytes']) for r in o)
for k in sorted(grp,key=lambda k:-sum(int(r['size_bytes']) for r in grp[k])):
    rs=grp[k]; b=sum(int(r['size_bytes']) for r in rs)
    print(k,len(rs),len({r['filename'] for r in rs}),b,round(100*b/tot,2))
fg=[r for r in o if g(r['filename']) in ('finger','finger-gfp')]
print('finger merged',len(fg),len({r['filename'] for r in fg}),sum(int(r['size_bytes']) for r in fg),round(100*sum(int(r['size_bytes']) for r in fg)/tot,2))
print('total',len(o),len({r['filename'] for r in o}),tot)"
```

```bash
python3 -I -c "
import csv
from collections import defaultdict
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm MSM8998 Snapdragon 835']
tz=[r for r in s if r['blob_family']=='tz']
sz=defaultdict(lambda: defaultdict(set))
for r in tz: sz[r['filename'].rsplit('.',1)[0]][r['filename'][-3:]].add(int(r['size_bytes']))
bad=[(k,e) for k,v in sz.items() for e,x in v.items() if len(x)>1]
print('tz stems',len(sz),'size differences',len(bad),bad)
for fam in ('wifi','cdsp','bt','gpu'):
    rs=[r for r in s if r['blob_family']==fam]
    d=[f for f in {r['filename'] for r in rs} if len({r['md5_db'] for r in rs if r['filename']==f})>1]
    print(fam,len({r['filename'] for r in rs}),'differing:',d)"
```

Mainline and firmware facts:

```bash
curl -s https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/boot/dts/qcom/msm8998.dtsi -o /tmp/m8.dtsi
wc -c < /tmp/m8.dtsi
grep -n 'compatible = "qcom,.*-pas"\|compatible = "qcom,.*-pil"' /tmp/m8.dtsi
grep -c 'npu' /tmp/m8.dtsi || true
grep -c 'cdsp' /tmp/m8.dtsi || true
```

```bash
for n in a530_pm4.fw a530_pfp.fw a530_zap.mdt a540_gpmu.fw2 a540_zap.mdt; do
  printf '%-20s ' "$n"
  curl -s -o /dev/null -w '%{http_code}\n' \
    "https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/qcom/$n"
done
```

```bash
curl -s "https://gitlab.com/api/v4/projects/postmarketOS%2Fpmaports/repository/files/device%2Ftesting%2Fdevice-oneplus-hotdogb%2Fdeviceinfo/raw?ref=master" | grep -i 'dtb\|codename'
curl -s "https://gitlab.com/api/v4/projects/postmarketOS%2Fpmaports/repository/files/device%2Ftesting%2Fdevice-oneplus-guacamole%2FAPKBUILD/raw?ref=master" | grep -i 'linux-postmarketos'
```

## Sources

| claim | source | access |
|---|---|---|
| 871 rows / 2 devices / 1,079,157,014 B / 423 filenames; family table; per-device split; 21 `db_type`s; `isa_identified` empty 871/871; `interface_documented` `n` 871/871; `sha256_if_listed` 0/871; `blob_subfamily` distribution | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-22 |
| 27/27 `mdt == b00+b01`; 7 untestable stems = 6 single-file MDTs + `cpe_9340` (12 segments, no `.b00`); per-stem segment tables | same | 2026-11-22 |
| 34 `.mdt` stems; code-variance 4 vs 30; 34/34 remoteproc correspondence | same | 2026-11-22 |
| tz size-invariance (0 of 77 segment names); 24 of 85 tz files differ in content; wifi 0 differing; cdsp 4 content / 0 size; bt only `bluetooth.img`; adsp 5 size diffs | same | 2026-11-22 |
| 118 rows of DSP-class stems labelled `other` (`slpi` 44, `npu` 10, `venus` 12, `spss1p` 8, `spss2p` 8) | same | 2026-11-22 |
| `dsp.img` 67,108,864 B = 64.00 MiB on both devices, byte-identical | same | 2026-11-22 |
| four-device filename Jaccard, all six pairs (0.9882–0.9953); 314 of 417 md5-identical; per-family identical sets | same | 2026-11-22 |
| 8 CPU nodes, `qcom,kryo280`, `reg` 0x0–0x3 / 0x100–0x103, `capacity-dmips-mhz` 1024/1536, `l2_0`/`l2_1`, `cpu-map` two clusters | `arch/arm64/boot/dts/qcom/msm8998.dtsi:140-228,230-262` | 2026-11-22 |
| `msm8998.dtsi` 77,917 B | `wc -c` on the fetched file | 2026-11-22 |
| 3 remoteproc nodes and MMIO: `-mss-pil` `0x04080000`, `-slpi-pas` `0x05800000`, `-adsp-pas` `0x17300000` | `msm8998.dtsi:1465,1661,3260` | 2026-11-22 |
| `wifi@18800000` `qcom,wcn3990-wifi`; `gpu@5000000` `qcom,adreno-540.1` | `msm8998.dtsi:3373,1526` | 2026-11-22 |
| 15 reserved regions / 236,015,616 B; `tz_mem` 45.00 MiB at `0x86200000`; contiguity and gaps | `msm8998.dtsi:30-119`, `:114-118` | 2026-11-22 |
| SM8150 `tz_mem` 57 MiB at the same base | `arch/arm64/boot/dts/qcom/sm8150.dtsi:718-720` | 2026-11-22 |
| SM8150 has `sm8150-cdsp-pas` at `:3367`; SM8250 at `:3790` | `sm8150.dtsi`, `sm8250.dtsi` | 2026-11-22 |
| `ARM_CPU_IMP_QCOM` 0x51; KRYO_2XX_GOLD 0x800 / SILVER 0x801 → MIDR `0x51008000` / `0x51008010` | `arch/arm64/include/asm/cputype.h:58,128-129,218-219` | 2026-11-22 |
| both Kryo 2xx MIDRs in the KPTI-safe list | `arch/arm64/kernel/cpufeature.c:1701-1702` | 2026-11-22 |
| `qcom,kryo280` is a documented `compatible` in the enum | `Documentation/devicetree/bindings/arm/cpus.yaml` | 2026-11-22 |
| `QCOM_ID_MSM8998` = 292 | `include/dt-bindings/arm/qcom,ids.h:143` | 2026-11-22 |
| `qcom_board_id(MSM8998)` in the socinfo table | `drivers/soc/qcom/socinfo.c:384` | 2026-11-22 |
| `qcom,msm-id = <292 0x20001>` (8998 v2.1) | `arch/arm64/boot/dts/qcom/msm8998-oneplus-common.dtsi:20` | 2026-11-22 |
| `msm8998-adsp-pas` → `msm8996_adsp_resource` (`adsp.mdt`, pas_id 1, lpass, 0x14); `msm8998-slpi-pas` → `msm8996_slpi_resource_init` (`slpi.mdt`, pas_id 12, dsps, 0x16) | `drivers/remoteproc/qcom_q6v5_pas.c:2007-2008,1214-1226,1501-1513` | 2026-11-22 |
| `msm8998_mss.hexagon_mba_image = "mba.mbn"`; `hexagon_mdt_image = "modem.mdt"` | `drivers/remoteproc/qcom_q6v5_mss.c:2391,2115,2916` | 2026-11-22 |
| defconfig: `QCOM_Q6V5_ADSP/MSS/PAS`, `QCOM_SYSMON`, `QCOM_RPMPD`, `QCOM_SMEM`, `DRM_MSM`, `ATH10K_SNOC` | `arch/arm64/configs/defconfig:1523-1526,1575,1557,1023,505` | 2026-11-22 |
| 15 `msm8998-*` DT files; 0 `guacamole*`; 0 `hotdog*`; `sm8150-*` has no OnePlus board | GitHub contents API on `arch/arm64/boot/dts/qcom/` | 2026-11-22 |
| MSM8998 board list under `const: qcom,msm8998` | `Documentation/devicetree/bindings/arm/qcom.yaml` | 2026-11-22 |
| ADSP 5.5 / SLPI 5.5 / MDSP 5.5; CDSP `N/A`; FastRPC `N`; GPU Broken; CPU Partial; Modem Partial | `linux-msm.github.io/mainline-status/soc/msm8998` | 2026-11-22 |
| `[PATCH 09/16] … Add MSM8998 ADSP and SLPI support`, Sibi Sankar, two descriptors only | LKML 2019-11-18 (`lists.openwall.net/linux-kernel/2019/11/18/953`) | 2026-11-22 |
| `[PATCH v2 3/5]` same subject, two descriptors | LKML 2019-12-18 (`…/2019/12/18/603`) | 2026-11-22 |
| 2021-05-07 thread collapsing the descriptors onto MSM8996 resources | LKML `…/2021/05/07/687` | 2026-11-22 |
| `qcom/` = 31 subdirs, no `msm8998`; `a530_pm4.fw`/`a530_pfp.fw` 200; `a530_zap.mdt`/`a540_gpmu.fw2`/`a540_zap.mdt` 404; `qcom/msm8998/*` 404 | `git.kernel.org/.../linux-firmware.git/tree/qcom/?h=main` and `plain/qcom/<name>` | 2026-11-22 |
| `device-oneplus-guacamole` / `device-oneplus-hotdogb` in `device/testing`, both `linux-postmarketos-qcom-sm8150`; `deviceinfo_dtb="qcom/sm8150-oneplus-*"` | GitLab `pmaports` file API | 2026-11-22 |
| no `device-oneplus-guacamoleb` in `device/{main,community,testing,archived}` | GitLab `pmaports` tree API (paged) | 2026-11-22 |
| `device-oneplus-guacamole` last commit 2024-06-23 (MR 5240); `device-oneplus-hotdogb` added 2023-10-16 (MR 4451), last 2024-04-22 (MR 4994) | GitLab `pmaports` commits API | 2026-11-22 |
| `device-oneplus-cheeseburger` uses `qcom/msm8998-oneplus-cheeseburger`, no vendor kernel dep; downstream packages archived | GitLab `pmaports` file/tree API | 2026-11-22 |
| 835 page: 4×Kryo 280 Gold + 4×Silver, Adreno 540, 10 nm, Mainline yes, per-component states | postmarketOS wiki `Qualcomm Snapdragon 835 (MSM8998)` (mirror rev 2023-08-01) | 2026-11-22 |
| OnePlus 7 page: Chipset SM8150, Adreno 640, covers `guacamoleb`/`guacamole`/`hotdogb`; last edited 2023-04-23 | postmarketOS wiki `OnePlus 7 (oneplus-guacamoleb)` | 2026-11-22 |
| `a5xx_catalog.c:134-151` Adreno 540 → `0x05040001`, `ADRENO_5XX`, `a530_pm4.fw`/`a530_pfp.fw`/`a540_gpmu.fw2`/`a540_zap.mdt` | `drivers/gpu/drm/msm/adreno/a5xx_catalog.c` | 2026-11-22 |
| Adreno 540 identity, three-ground mislabel proof, four-device GPU control, zero-a540 census | `research/soc/Qualcomm-MSM8998-Snapdragon-835-gpu.md` §1-§3 | 2026-11-20 |
| OnePlus 7/7T are SM8150 | `research/soc/per-soc-method-plans.md:74` | 2026-11-20 |
| tz 83-row decomposition, `tz.img` 2×2, `b01`/`mdt`/`img` variance boundary, 190-of-399 fleet violation | `docs/devices/oneplus/OnePlus_7/tz.md` §2-§5 | 2026-11-20 |
| `boot` mixed-column defect; 364/1,038 MiB-exact, 86.8% of family bytes | `docs/devices/oneplus/OnePlus_7/boot.md` | 2026-11-20 |
| four-device boot md5 matrix; codename↔SoC anchor; `soc` column wrong for the two MSM8998 rows | `docs/devices/oneplus/OnePlus_7T_Pro/boot.md` §5 | 2026-11-21 |
| `dsp.img` is an ext4 filesystem with `/adsp`,`/cdsp`,`/sdsp` and 57 `e_machine` 164 ELFs (OnePlus 6) | `research/fleet/dsp-tz-map.md` §1-§2 | 2026-11-17 |
| `hyp` container format; the two `hyp.img` hashes on these devices | `research/fleet/tz-hyp.md` §1.1, §4.2 | 2026-11-20 |
| `wpss`/`bdwlan` grammar, `b<NN> ≡ phdr NN`, board-id indexing | `research/fleet/wifi-wpss.md` §2-§4 | 2026-11-20 |
| fleet CDSP census row: MSM8998 `2 devices / 22 rows / 11 files` | `research/cdsp-fleet/census.md:207` | 2026-11-20 |
| `bm2n`/QCA BT patch fleet matrix | `research/laptop/qualcomm-adsp-bm2n-fleet.md`, `qualcomm-qca-bt-fleet.md` | 2026-11-20 |
| SM8350 SoC-package house format; `.b00` = `52+32N`/`64+32N` with 0 non-fits on 23 stems; `qupfw` has no mainline binding | `research/soc/Qualcomm-SM8350-Snapdragon-888-soc.md` (its §1, §4, §6.5) | 2026-11-22 |
