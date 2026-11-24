# Qualcomm SM4375 Snapdragon 4 Gen 1 — SoC package: CPU, DSP, boot chain, TrustZone, firmware census

Issue #811. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative / [OPEN] unresolved. Every number is command output from a run on
**2026-11-24** against
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows),
`torvalds/linux` master, the `linux-firmware` tree on `git.kernel.org`, and the
postmarketOS `pmaports` tree on GitLab.

**No payload exists in this workspace and none was read.** Every statement below
is matrix metadata — filename, size, md5, `db_type`, family label — or public
GPL source. No ELF is parsed here and no instruction is disassembled [N].

This is the **SoC-package** note. The GPU core identification for this SoC is a
separate, already-committed deliverable
(`research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md`, #2024) and is
**cited, never re-derived**.

## 0. Verdict

| question | answer | class |
|---|---|---|
| SoC identity | SM4375 = Snapdragon 4 Gen 1; board codename **`fogo`** (the only codename in the slice's `db_path`) | [F] |
| SoC ID in mainline | **none** — no `QCOM_ID_SM4375`; the `qcom,ids.h` table stops at 781 and never names this part | [N] |
| CPU topology | **2× Cortex-A78 + 6× Cortex-A55**, 8 cores, 6 nm, announced 2022-10-06 | [F] from public spec |
| CPU instruction-level ID | **not obtainable from this corpus** — `isa_identified` is empty on all 364 rows and there is no SM4375 device tree to read a `cpu-map` from | [N] |
| CPU cluster shape | **not in mainline**; the nearest structural precedent (`sm4450.dtsi`) is 6+2 with one `cpu-map` cluster and two `freq-domain`s | [F] |
| GPU | Adreno 619 — **cited from the GPU note** | [F] |
| GPU firmware in-kernel | `a619_gmu.bin` + `a630_sqe.fw` + `a615_zap.mdt`, from `a6xx_catalog.c:873-886` (`machine = "qcom,sm4350"`) and `:898-915` (`qcom,sm6375`) — **no SM4375 entry exists** | [F] |
| DSP units in the slice | **4**: `adsp`, `cdsp`, `venus`, `ipa_fws` | [F] |
| DSP units mainline declares | **3** remoteprocs on the sibling `sm6375.dtsi`: `mss`, `adsp`, `cdsp` — **no venus, no slpi, no npu, no spss** | [F] |
| Boot chain | **8 rows / 8 filenames / 132,997,120 B**; 4 of the 8 are exact-MiB partition dumps = **99.34%** of the family | [F] |
| TrustZone family | **50 rows / 50 filenames / 16,039,093 B**, 11 stems + 4 `.img` | [F] |
| TZ big-image shape | `hyp.img` **8.00 MiB** + `tz.img` **4.00 MiB** + `uefisecapp.img` **2.00 MiB** — the exact trio that **11** corpus devices ship | [F] |
| Split law `mdt == b00+b01` | **17 of 17** testable stems, zero exceptions; 6 untestable, all single-file MDTs | [F] |
| `.b00` header law | ELF32 = `52 + 32N` (10 stems), ELF64 = **`64 + 56N`** (7 stems), **0 non-fits** | [F] |
| `slpi` / `npu` / `spss` in the slice | **absent** — 0 rows of each | [N] |
| `.mbn` in the corpus | **0 of 33,917 rows** | [N] |
| `qcom/a619_gmu.bin` in linux-firmware | **404**; `a630_gmu.bin` is **200** | [N, F] |
| Mainline `sm4375.dtsi` | **does not exist**; 0 of 664 DT entries; `qcom.yaml` 0 hits | [N] |
| postmarketOS device package | **none** — 0 of 479 `device/` dirs; wiki `srsearch` 0 hits for 4 queries | [N] |

The findings that are new to this repository, and not restatements of #2024, are
§1.3 (the sibling-DT trap), §3.3 (the `adsp`-labelled-`MODEM` defect is
corpus-wide and total), §4.2 (`rpm.img` as a pre-AOP generation marker),
§5.2 (the 8/4/2 MiB TZ trio), §6.2 (the 14-file delta against the SM6375
sibling), §6.4 (94% of the `gpu` family is one fingerprint TA), and **§7.2 — a
correction to the ELF64 header formula published in #805**.

## 1. CPU: 2× A78 + 6× A55, and why no device tree can confirm it

### 1.1 The topology, from public spec

The SoC is an **8-core 2+6**: two Cortex-A78 performance cores and six
Cortex-A55 efficiency cores, on a 6 nm process, announced 2022-10-06 [F]
(nanoreview SOC page; Qualcomm product brief; both retrieved 2026-11-24).

| source | cores | clocks | process | class |
|---|---|---|---|---|
| nanoreview, `qualcomm-snapdragon-4-gen-1` | 2× A78 + 6× A55 | 2000 / 1800 MHz | 6 nm | [F] |
| Qualcomm product brief (SM4375) | "2 performance + 6 efficiency" | — | 6 nm | [F] |

The `2 + 6` split is **not** a "4 + 4" and not a 1+3+4 tri-cluster. That matters
because two of the four sibling SoCs in this tier are shaped differently:
`sm4450.dtsi` (Snapdragon 4 Gen 2, SM4450) is also 6+2 but at 2.2/1.95 GHz, and
`sm6375.dtsi` (Snapdragon 695) is 6+2 as well. So the *core count* is a
tier constant; the *frequency* and the *codename* are not.

### 1.2 MIDR: what the kernel would expect, and what the corpus cannot show

The kernel names the implementor and part number separately, and composes the
MIDR from them. From `arch/arm64/include/asm/cputype.h` [F]:

```
:58    #define ARM_CPU_IMP_ARM              0x41
:58    #define ARM_CPU_IMP_QCOM             0x51
:74    #define ARM_CPU_PART_CORTEX_A55      0xD05
:80    #define ARM_CPU_PART_CORTEX_A78      0xD41
:43-46 #define MIDR_CPU_MODEL(imp, partnum)
         ((imp) << 24) | (0xf << 16) | ((partnum) << 4)
```

Arithmetic, exact:

| core | part number | MIDR |
|---|---|---|
| Cortex-A78 | `0xD41` | **`0x410fd410`** |
| Cortex-A55 | `0xD05` | **`0x410fd050`** |

Both are ARM-implemented parts (`imp` = `0x41`), not Qualcomm-implemented ones.
This is the **opposite** of the MSM8998 case documented in
`Qualcomm-MSM8998-Snapdragon-835-soc.md` §1.2, where both clusters report
Qualcomm part numbers (`0x510F8000` / `0x510F8010`) because Kryo 280 was a
Qualcomm design. SM4375's cores are stock ARM cores carrying Qualcomm's
marketing name, exactly as `cputype.h:241-246` says for the next tier up:

```
:243  * - Qualcomm Kryo 6XX Gold IDs itself as ARM_CPU_PART_CORTEX_A78
:244  * - Qualcomm Kryo 6XX Silver IDs itself as MIDR_CORTEX_A55
```

That comment block is about Kryo 6XX. The Snapdragon 4 Gen 1 is a Kryo part of
an unstated series, and there is **no** corresponding line for it in
`cputype.h` [N].

Two consequences follow, and both are negative:

1. **No instruction-level proof exists in this corpus** [N]. `isa_identified` is
   empty on **364 of 364** rows and `sha256_if_listed` on **364 of 364**; there
   is no payload in the workspace to disassemble. The MIDR values above are
   arithmetic on a public header, not observations.
2. **KPTI-safety is decidable for the little cluster and not asserted for the
   big one** [F, I]. `arch/arm64/kernel/cpufeature.c:1695` lists
   `MIDR_ALL_VERSIONS(MIDR_CORTEX_A55)` in the KPTI-safe range. There is **no**
   `MIDR_CORTEX_A78` entry anywhere in `cpufeature.c` — `grep -c CORTEX_A78`
   returns 0 — so the A78 cores fall through to the feature-register path,
   which is the normal treatment for a core that is not Meltdown-safe [I].

### 1.3 The sibling-DT trap: `sm6375.dtsi` gives all eight cores one compatible

There is no SM4375 DT to read. The nearest published analogue in this tier is
`sm6375.dtsi`, and it is **actively misleading** if copied [F]:

```
arch/arm64/boot/dts/qcom/sm6375.dtsi
  cpu0..cpu7  compatible = "qcom,kryo660"     (all eight, identical string)
  cpu0..cpu5  clocks/freq-domain = <&cpufreq_hw 0>
  cpu6..cpu7  clocks/freq-domain = <&cpufreq_hw 1>
  cpu-map     cluster0 { core0..core5 }  cluster1 { core6, core7 }
```

So the DT encodes the 6+2 split **three ways** — `freq-domain`, `cpufreq_hw`
clock index, and `cpu-map` cluster — while giving **one** `compatible` string to
two physically different core types. A consumer that derives cluster structure
from `compatible` sees a homogeneous 8-core machine; a consumer that reads
`cpu-map` sees 6+2 [F].

Now compare `sm4450.dtsi`, which is the same 6+2 shape but resolves the core
types honestly [F]:

```
sm4450.dtsi:50-176   cpu0..cpu5  compatible = "arm,cortex-a55"
sm4450.dtsi:176-212  cpu6..cpu7  compatible = "arm,cortex-a78"
sm4450.dtsi          cpu-map   cluster0 { core0..core7 }   (ONE cluster)
sm4450.dtsi          freq-domain 0 (x6), 1 (x2)
```

Three structural facts, all [F]:

| SoC | cores | `compatible` | `cpu-map` clusters | `capacity-dmips-mhz` |
|---|---|---|---|---|
| `sm6375` | 8 | `qcom,kryo660` ×8 | **2** (`cluster0`, `cluster1`) | **none** |
| `sm4450` | 8 | `arm,cortex-a55` ×6, `arm,cortex-a78` ×2 | **1** | **none** |
| SM4375 | 8 | **no DT** | **no DT** | **no DT** |

So the two closest published 6+2 SoCs disagree with each other on *both*
`compatible` style and cluster count. Predicting SM4375's DT from either would
be a guess [H]. What can be said is that SM4375's cores are stock ARM parts
(§1.2), so the `sm4450` style — `arm,cortex-a78` / `arm,cortex-a55` — is the
better-motivated of the two, and the `sm6375` style would be a
misdescription [I].

Note the `capacity-dmips-mhz` column: **neither** sibling carries it, while
MSM8998 does (`1024` / `1536`). For a 6+2 with a single `cpu-map` cluster the
kernel derives capacity from `freq-domain`; the explicit hint is unnecessary.
That is consistent with `sm8350.dtsi` too, which uses one `cpu-map` cluster and
three `freq-domain`s with no dmips hints [F].

### 1.4 Machine identity: the SoC ID does not exist

| probe | result | class |
|---|---|---|
| `QCOM_ID_SM4375` in `include/dt-bindings/arm/qcom,ids.h` | **absent**; 308 defines, highest value 781 (`IPQ9670`) | [N] |
| `qcom_board_id(SM4375)` in `drivers/soc/qcom/socinfo.c` | **absent**; 295 entries | [N] |
| `grep -i '4375\|holi' socinfo.c` | **0** | [N] |
| `QCOM_ID_SM4350` (the tier's 480) | **also absent** | [N] |
| `QCOM_ID_SM4450` (the successor) | **present** = 568 at `:274` | [F] |
| `QCOM_ID_SM7325` = 475 at `:239`; `QCOM_ID_SM6375` = 507 at `:251` | present | [F] |

So the mainline ecosystem knows this part's **predecessor-adjacent** siblings
(4325/4450/6375/7325) but has never assigned an ID to SM4375 itself. Two things
follow: a bootloader `qcom,msm-id` for this SoC would reference a number that
mainline has not registered, and `socinfo.c`'s `soc_id[]` table would print the
raw number rather than a name [I].

## 2. GPU — cited, four lines

The GPU is an **Adreno 619**, family `ADRENO_6XX_GEN1`, firmware
`a619_gmu.bin` + `a630_sqe.fw` + `a615_zap.mdt`. Every proof — the catalog
entry, the `fpctzapp` fingerprint-TA mislabel, the `talos`=QCS615 trap, the
byte-identity to the SM8350 Xperia_5_III's `a619_gmu.bin`, and the zero-mainline
-DT enumeration — is owned by
`research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md` §1-§5 [F]. **Cited,
not re-derived.**

SoC-package additions only:

- The catalog has **three** entries with `.revn = 619` and only **three**
  `.machine =` strings in the whole file — `qcom,sm7150` at `:820`,
  `qcom,sm4350` at `:870`, `qcom,sm6375` at `:895` [F]. There is **no
  `machine = "qcom,sm4375"`** entry [N]. The 619 GPU on this SoC matches by
  falling through to the `.chip_ids = ADRENO_CHIP_IDS(0x06010900)` /
  `.revn = 619` default, not by a name match [I].
- The third 619 entry (`:916-944`) is the *un-named* one: same chip id, same
  `a619_gmu.bin`, but with five speedbins (`{120,4}{138,3}{169,2}{180,1}`)
  instead of three. So there are **two** speedbin tables for the same GPU and
  the DT is what selects between them [F]. Which one `fogo` uses is not
  discoverable from the corpus [OPEN].
- `research/laptop/qualcomm-adreno-gmu-content.md` §4 already generalises the
  filename set as "a615-family (a615, a616, a618, a619)" — consistent with
  `a6xx_catalog.c:63` and `:506` [F].

## 3. DSP: four units, and one label defect that is corpus-wide

### 3.1 What mainline declares in this tier

`sm6375.dtsi` — the closest published sibling — declares exactly **three**
remoteprocs and one WCN3990 wifi node [F]:

```
:1526  remoteproc_mss:  remoteproc@6080000   compatible = "qcom,sm6375-mpss-pas"
:1567  remoteproc_adsp: remoteproc@a400000   compatible = "qcom,sm6375-adsp-pas"
:1605  remoteproc_cdsp: remoteproc@b300000   compatible = "qcom,sm6375-cdsp-pas"
:1735  wifi:            wifi@c800000         compatible = "qcom,wcn3990-wifi"
```

and the PAS driver has the matching three entries [F]:

```
drivers/remoteproc/qcom_q6v5_pas.c
:2051  qcom,sm6375-adsp-pas  -> sm6350_adsp_resource  (adsp.mdt,  pas_id 1,  ssr "lpass")
:2052  qcom,sm6375-cdsp-pas  -> sm8150_cdsp_resource  (cdsp.mdt,  pas_id 18, ssr "cdsp")
:2053  qcom,sm6375-mpss-pas  -> sm6375_mpss_resource   (modem.mdt, pas_id 4,  ssr "mpss")
```

There is **no** `qcom,sm4375-*-pas` compatible anywhere in that driver [N]. A
port would have to add one, and the natural starting point is the `sm6375`
triple since the firmware filenames match byte-for-byte in style (`adsp.mdt`,
`cdsp.mdt`, `modem.mdt`).

The reserved-memory map corroborates the three-unit model and adds a fourth
carve-out with no driver behind it [F]:

```
sm6375.dtsi:571  pil_adsp_mem   pil-adsp@86700000   32.00 MiB
sm6375.dtsi:581  pil_cdsp_mem   pil-cdsp@88700000   30.00 MiB
sm6375.dtsi:591  pil_video_mem  pil-video@8a500000   5.00 MiB   <- nobody claims this
sm6375.dtsi:595  pil_ipa_fw_mem pil-ipa-fw@8aa00000  0.0625 MiB
sm6375.dtsi:600  pil_ipa_gsi_mem pil-ipa-gsi@8aa10000 0.039 MiB
sm6375.dtsi:605  pil_gpu_micro_code_mem              0.008 MiB
```

`pil_video_mem` is 5 MiB reserved for the video block, and `grep -c venus
sm6375.dtsi` returns **0** — the sibling SoC reserves memory for the venus
subsystem but declares no node for it [F]. That is the same gap §3.4 shows in
this slice.

### 3.2 What the slice ships

| unit | rows | bytes | shape | mainline driver | class |
|---|---|---|---|---|---|
| `adsp` | 44 | 24,095,430 | `.mdt` + `.b00`–`.b34` (34 segments) + 3 `.jsn` + 6 `bm2n*.bin` | yes (`qcom_q6v5_pas`) | [F] |
| `cdsp` | 12 | 3,058,107 | `.mdt` + 10 segments + `cdspr.jsn` | yes (`qcom_q6v5_pas`) | [F] |
| `venus` | 13 | — (**in `other`**) | `.mdt` + 12 segments | **no node in `sm6375.dtsi`** | [F, N] |
| `ipa_fws` | 6 | — (**in `modem`**) | `.mdt` + 5 segments | yes (`qcom_ipa`) | [F] |
| `slpi` | **0** | — | — | n/a | [N] |
| `npu` | **0** | — | — | n/a | [N] |
| `spss1p`/`spss2p` | **0** | — | — | n/a | [N] |

The `adsp` family is a clean 34-segment set. Its largest segment is
`adsp.b25` at **6,548,872 B** (27.2% of the family); the smallest non-header is
`adsp.b10` at 260 B. The `bm2n` files are the QCA Bluetooth patch set —
6 of them, `bm2n{06,08,12,13,14,15}.bin` [F].

That 6-file `bm2n` shape is a **fleet signature**, not a per-device accident [F]:

| SoC | `bm2n` files |
|---|---|
| SM8475 (8+ Gen 1) | **53** |
| *(blank-soc device)* | **51** |
| SM8550, SM8350, SM8350-AC, SM7250, SM7325, SM7325-AE, SM8250, SM6375, SM6225, SM4375, QCM6490 | **6** each — the *same* six names |

Fourteen devices ship `bm2n` at all, and eleven of them ship exactly
`{06,08,12,13,14,15}`. The two 8-series parts ship a superset that runs
`00`–`27`, `31`–`38`, `40`–`55`. So the `bm2n` file count is a crude but exact
proxy for the SoC tier [F] — and SM4375 sits on the low side, with the same six
files as an SM8350.

### 3.3 The `adsp` family carries `db_type=MODEM` — corpus-wide and total

This is not an SM4375 defect. It is a property of the entire matrix [F]:

```
blob_family = 'adsp' -> db_type distribution
  MODEM: 3281
```

**3,281 of 3,281** `adsp` rows in 33,917 carry `db_type = MODEM`. There is no
second value. So the `db_type` column is not usable to separate `adsp` from
`modem` — only `blob_family` does. On this slice all 44 `adsp` rows are `MODEM`
and all 44 `modem` rows are `CELL` except `modem.img` (`CELL_WIFI_GPS_BLUETOOTH`)
and the two `.jsn` files (`UNKNOWN`) [F].

By contrast `cdsp` is clean (`COMPUTE` 880, `UNKNOWN` 60) and `tz` is rich
(`UNKNOWN` 1105, `DRM` 1083, `SECURITY` 735, `ELF64` 517, `FINGERPRINT` 436,
`CERT` 262, `BOOT` 63, `SECUREBOOT` 63) [F]. So the defect is specific to the
`adsp` label, and a consumer that filters DSP trustlets by `db_type` will lose
every one of them.

### 3.4 `venus`: 13 files on the device, no node in mainline

The device ships a complete split `venus` set — `.mdt` 8,220 B plus 12 segments
spanning `.b00`–`.b10` and `.b19` — filed in `blob_family = other` [F]. Mainline's
`sm6375.dtsi` reserves 5 MiB for `pil_video_mem` and declares no venus node
(§3.1). And `linux-firmware` ships venus only as per-version monoliths
(`venus-1.8`, `-4.2`, `-5.2`, `-5.4`, `-6.0`), each a single `venus.mbn` with a
`venus.mdt` **symlink** [F] — never as a per-SoC split set. So the split form on
this device has no upstream consumer at all [N].

The `venus` stem is one of the two stems in this slice where the ELF header
count exceeds the segment count by a wide margin (§7.2): 20 phdrs, 12 segments,
**8 missing indices** (`11`–`18`). Compare `adsp` (36 phdrs, 34 segments, 2
missing) and `modem` (36 phdrs, 33 segments, 3 missing). Zero-`p_filesz`
program headers produce no file, which is the mechanism already established in
`research/fleet/wifi-wpss.md:77-79` — a header counted in the table but with no
extractable body [F].

## 4. Boot chain: 8 images, and `rpm.img` as a generation marker

### 4.1 The eight rows

| file | bytes | MiB | `db_type` | exact power of 2? |
|---|---|---|---|---|
| `boot.img` | 100,663,296 | **96.00** | `BOOT` | yes |
| `dtbo.img` | 25,165,824 | **24.00** | `DTB` | yes |
| `xbl.img` | 5,242,880 | **5.00** | `UEFIBOOT` | **no** (5 MiB is 2^22+2^20) |
| `abl.img` | 1,048,576 | **1.00** | `UEFIBOOT` | yes |
| `rpm.img` | 524,288 | 0.50 | `ELF64` | yes |
| `xbl_config.img` | 262,144 | 0.25 | `ELF64` | yes |
| `qupfw.img` | 81,920 | 0.078 | `ELF64` | **no** (81,920 = 80 KiB) |
| `vbmeta.img` | 8,192 | 0.008 | `AVB` | yes |

Four of the eight are exact-MiB **partition dumps** (`boot`, `dtbo`, `xbl`,
`abl`) totalling **132,120,576 B = 99.34%** of the family [F]. The other four
are real firmware or metadata. So the boot family is a partition image, not a
firmware set — the same mixed-column pattern #805 §4.2 documented, and the same
conclusion: **do not** count boot-chain bytes as firmware bytes.

The 96 MiB `boot.img` is 12.84% of the whole slice. It is a partition dump
whose contents were not inspected [N].

Absent from the slice [N]: `aop.img`/`aop.mdt`, `cpucp.img`, `cpucp_fw.img`,
`bl.img`, `dtb.img`, `recovery.img`, `super.img`, `vendor_boot.img`,
`init_boot.img`, `devinfo.img`. So the extracted set is the *radio* partition
plus a handful of bootloader partitions — consistent with `db_path` being
`motorola/fogo/radio` for all 8 (§6.1).

### 4.2 `rpm.img` is a pre-AOP marker — only 8 SoCs in the corpus ship it

This is the one boot-chain finding that is genuinely diagnostic [F]:

| marker | SoCs in corpus | members |
|---|---|---|
| ships `rpm.img` | **8** | blank-soc (5 devices), SM4250, **SM4375**, SM6115, SM6225, SM6375, SM7325-AE, and a `\xff`-prefixed SM6375 duplicate |
| ships `aop*` | **14** | MSM8998, SM7225, SM7250, SM7325-AE, SM8150, SM8150-AC, SM8250, SM8350, SM8350-AC, SM8475, SM8550, QCM6490, … |

The two sets overlap on only **SM7325-AE**. SM4375 is on the `rpm` side and
**not** the `aop` side [F]. That is a generation statement: an `rpm.img` means
the resource-power-manager firmware is still a separate loadable image rather
than having been folded into the always-on processor block. It matches
`sm6375.dtsi:645`, which declares `rpm: remoteproc { compatible =
"qcom,sm6375-rpm-proc", "qcom,rpm-proc" }` — a real RPM remoteproc node, not an
AOP one [F].

The `sm6375.dtsi` line `:545 xbl_aop_mem: xbl-aop@80700000` shows the same
generation straddle: the *AOP* address space exists, but the RPM is still its
own processor. So "AOP present" and "RPM absent" are not the same axis, and this
slice is the evidence [I].

### 4.3 `qupfw.img` has no mainline consumer

`qupfw.img` is 81,920 B, `db_type = ELF64`, filed in the boot family [F]. Six
SoCs in the corpus ship it at 81,920 B; the corpus mode is 57,344 B (23 rows)
[F]. `grep -c qupfw` returns **0** in `sm6375.dtsi`, `sm8350.dtsi` and
`sm4450.dtsi`, and the `qcom,scm.yaml` binding does not mention it [F]. So the
partition is real, shipped, and has no device-tree description — the QUP
firmware is loaded by the bootloader, not by Linux [I].

## 5. TrustZone: the 8/4/2 MiB trio, and the reserved map that does not exist

### 5.1 The three big images are corpus modes

| file | here | corpus mode | rank of this size |
|---|---|---|---|
| `hyp.img` | **8,388,608** (8.00 MiB) | 8,388,608 (**11 rows**) | **1st** |
| `tz.img` | **4,194,304** (4.00 MiB) | 4,194,304 (**11 rows**) | **1st** |
| `uefisecapp.img` | **2,097,152** (2.00 MiB) | 126,976 (18 rows) | **2nd** |
| `keymaster.img` | 524,288 (0.50 MiB) | 524,288 (11 rows) | 1st |
| `devcfg.img` | 131,072 (0.125 MiB) | 57,344 (22 rows) | 2nd |

All five are at or near the corpus mode for their filename [F]. `hyp.img` is
the largest single thing in the tz family at 8.00 MiB, and `tz.img` is next at
4.00 MiB.

### 5.2 The exact 8/4/2 trio is shared by 11 devices across 6 SoCs

This is the finding [F]. Of the 11 devices whose `hyp.img` is 8,388,608 B, **all
11** also ship `tz.img` at exactly 4,194,304 B and `uefisecapp.img` at exactly
2,097,152 B:

| SoC | devices |
|---|---|
| *(blank)* | `G_Stylus_5G-2-2022`, `Moto_G_Stylus_5G` |
| **SM4375** | **`Moto_G_5G_2024`** |
| SM6375 | `Edge_30_Neo`, `Moto_G34_5G`, `Moto_G82_5G`, `Moto_G84_5G` |
| SM7250 | `Edge_30_Fusion` |
| SM7325-AE | `Edge_30` |
| SM8350-AC | `Moto_G200` |
| SM8550 | `Edge_40_Pro` |

The span is SM4375 (4-series, 2022) through SM8550 (8 Gen 2, 2022) — the same
two-year window. So the trio is a **build-generation** signature in the Motorola
tree, not a per-SoC one [F, I]. The 11 `hyp.img` md5s are all **distinct** [F] —
same size, different content — so the trio is a size law only, and anyone
treating 8 MiB as "the same hypervisor" would be wrong.

The 63 `hyp.img` rows across the corpus range from 4,096-multiple to small:
the mode is 8 MiB (11), then 520,192 (10), 1,257,472 (9), 491,520 (4),
1,458,176 (4). Every one is a multiple of 4,096, which corroborates
`research/fleet/tz-hyp.md` §1.2 ("all 63 sizes are multiples of 4,096") [F].

### 5.3 The TZ family has no reserved-memory map to compare against

#805 §5.1 could read `tz_mem` out of `msm8998.dtsi` — 45.00 MiB at `0x86200000`
— and compare it to SM8150's 57 MiB at the same base. That is **not possible
here** [N]:

| file | `hyp_mem` | `tz_mem` |
|---|---|---|
| `msm8998.dtsi` | — | **present**, 45.00 MiB @ `0x86200000` |
| `sm8150.dtsi` | — | present, 57.00 MiB @ same base |
| `sm8350.dtsi` | present, 6.00 MiB @ `0x80000000` | **absent** |
| `sm8250.dtsi` | present | **absent** |
| `sm6375.dtsi` | present, 6.00 MiB @ `0x80000000` | **absent** |
| `sm4450.dtsi` | **absent** | **absent** |

`grep -c tz_mem` returns 0 for all four modern SoCs. So from `sm8350` onward
mainline stopped describing the TZ window as a named `tz_mem` region; what
remains is `hyp_mem` at **6.00 MiB** (`0x80000000`, `sm6375.dtsi:538-542`) plus
`hyp_reserved_mem` at `0xd0000000` on SM8350 [F].

That creates a clean size contradiction worth recording [F]:

- `hyp.img` on this device is **8.00 MiB**;
- `hyp_mem` in the sibling DT is **6.00 MiB**.

The image is 2 MiB larger than the sibling's reservation. Either SM4375's
reservation differs from SM6375's, or the extraction's `hyp.img` is a
partition-level dump rather than the firmware body, or the DT's 6 MiB is the
sibling's under-provisioning. **Not resolved** [OPEN]. The same 8-vs-6 gap
would exist on the four SM6375 devices in §5.2, so it is a fleet-wide question,
not an SM4375 peculiarity [I].

The total of the seven TZ-ish exact-MiB images is **15.125 MiB**
(`hyp` 8 + `tz` 4 + `uefisecapp` 2 + `keymaster` 0.5 + `devcfg` 0.125 +
`prov` 0.25 + `storsec` 0.125) [F]. With the 6 MiB `hyp_mem` plus 30 MiB
`cdsp_secure_heap_mem` plus the 81 MiB `removed_mem`, the sibling DT reserves
**446.44 MiB** across 18 regions [F]. So the secure world is described at
roughly 40 MiB and the extracted secure firmware is 15 MiB — the remainder is
trustlet workspace, not firmware [I].

Note that `tz.img` has **no** `.mdt` companion [N]: `tz.mdt`, `keymaster.mdt`,
`devcfg.mdt`, `uefisecapp.mdt` and `hyp.mdt` are all absent. These four are
monolithic signed images, not split-set firmware. That is the opposite of every
trustlet in §6.5, which is split.

## 6. The slice: 9 families, 22 `db_type`s, and one 94% mislabel

### 6.1 The family table

| family | rows | files | bytes | % of slice |
|---|---:|---:|---:|---:|
| `modem` | 44 | 44 | 533,518,555 | **68.05** |
| `boot` | 8 | 8 | 132,997,120 | 16.96 |
| `other` | 74 | 74 | 65,119,724 | 8.31 |
| `adsp` | 44 | 44 | 24,095,430 | 3.07 |
| `tz` | 50 | 50 | 16,039,093 | 2.05 |
| `wifi` | 99 | 99 | 4,226,548 | 0.54 |
| `gpu` | 19 | 19 | 3,187,475 | 0.41 |
| `cdsp` | 12 | 12 | 3,058,107 | 0.39 |
| `bt` | 14 | 14 | 1,798,120 | 0.23 |

**364 rows = 364 distinct filenames**, one device, 784,040,172 B = **0.73 GiB**
[F]. There is no duplication to exploit — unlike #805, where 871 rows mapped to
423 filenames across 2 devices. A single-device slice gives **no** Jaccard or
cross-device variance signal, which is why §7 falls back to a corpus-wide test
instead of an intra-slice one.

The distribution is extremely concentrated: `modem.img` alone (414,187,520 B) is
**52.8%** of the slice and **77.63%** of its own family; the top 10 files are
**88.61%** of all bytes [F]. Twenty-five files are exact powers of two, totalling
52,473,520 B = **6.7%** of the slice — and 20 of those 25 are 512-byte `.b00`
headers [F].

### 6.2 `db_path` is the only multi-directory signal, and it is 7-way

| `db_path` | rows | bytes | dominant families |
|---|---:|---:|---|
| `motorola/fogo/modem/image` | 307 | 141,809,923 | wifi 97, other 60, tz 45, modem 42 |
| `motorola/fogo/radio` | 19 | **629,526,528** | boot 8, tz 5, other 3, modem 2 |
| `motorola/fogo/vendor/firmware` | 15 | 599,188 | other 10, gpu 5 |
| `motorola/fogo/bluetooth/image` | 13 | 749,544 | bt 13 |
| `motorola/fogo/vendor/lib/rfsa/adsp` | 6 | 8,873,216 | adsp 6 |
| `motorola/fogo/vendor/gpu/kbc` | 2 | 802,061 | gpu 1, other 1 |
| `motorola/fogo/vendor/etc/wifi` | 2 | 1,679,712 | wifi 2 |

The `radio` directory is **19 rows / 629,526,528 B = 80.3%** of the slice [F].
That is where `modem.img`, `boot.img`, `dtbo.img`, `xbl.img`, `abl.img`,
`hyp.img` and `tz.img` live — i.e. the radio partition image plus the small
bootloader images. Every family except `gpu`, `bt`, `cdsp` and `wifi` has at
least one member in `radio`.

**Contrast with its SM6375 sibling.** `Moto_G34_5G` is the same vendor, the same
`fogo`-family naming, and the same 17 named `bdwlan` files — but its codename in
`db_path` is **`fogos`**, not `fogo` [F]. Its slice is 358 rows and differs from
`fogo` by only **14 files on this side and 8 on that side** [F]:

| only on `fogo` (SM4375), 14 files | bytes | family |
|---|---:|---|
| `tbase.{mdt,b00..b07}` | 355,681 | other |
| `modem.b24` | 106,688 | modem |
| `novatek_ts_fw.bin`, `novatek_ts_mp.bin` | 139,264 ×2 | other |
| `aw_skt.bin` | 109,968 | other |
| `aw882xx_pid_2113_acf.bin` | 1,968 | other |

| only on `fogos` (SM6375), 8 files | bytes | family |
|---|---:|---|
| `modem.b23` | 6,105,991 | modem |
| `sec_s3nrn4v_firmware.bin` | 184,620 | other |
| `chipone_firmware.bin` | 80,432 | other |
| `sec_s3nrn4v_hwreg.bin`, `_swreg.bin` | 3,232, 336 | other |
| `efs1.bin`, `efs2.bin`, `efs3.bin` | 512 ×3 | modem |

So the two devices are **94.09%** identical by filename set (Jaccard 0.9409,
350 shared of 372 union), with 243 of the 350 shared filenames md5-identical
[F]. The delta is almost entirely **component choice**, not SoC: different
touch controller (`novatek` on `fogo`, `chipone` on `fogos`), different secure
element (`sec_s3nrn4v` on `fogos`), a different audio amp (`aw882xx`/`aw_skt`
on `fogo`), one `modem.b##` segment, and the whole `tbase` trustlet. The
three `efs*.bin` on `fogos` are per-device calibration, which is exactly why a
different device has a different set [I].

`tbase` is worth one line because it is rare [F]: only **8** devices in the
corpus ship it, across **3** SoC labels — 4 on a blank-soc Motorola set, 3 on
SM6115, and **1** on SM4375. It is a TZ trustlet (split `.mdt` + 8 segments,
`b00` = 308 B) filed under `other`, not `tz` [F].

### 6.3 `wifi`: 96 `bdwlan` files, of which 17 name another device

The wifi family is 99 files / 4,226,548 B, and **all 96** `bdwlan*` files are
exactly **26,328 B** [F]. That matches `research/fleet/wifi-wpss.md:531`
exactly — SM4375 is one of the nine `b`-only parts, and every `b` is 26,328 B
because it is a raw, unwrapped body.

The breakdown [F]:

| class | count | pattern |
|---|---:|---|
| `bdwlan.<hex>` | 76 | `bdwlan.b04` … `bdwlan.205` |
| `bdwlanu.<hex>` | 2 | `bdwlanu.b65`, `bdwlanu.b69` |
| `bdwlan_<name>_<ipa\|epa>.bin` | 17 | 13 `ipa`, 4 `epa` |
| `bdwlan.bin` | 1 | the default |
| `aoa_cldb_falcon.bin`, `aoa_cldb_swl14.bin` | 2 | 839,856 B each |
| `regdb.bin` | 1 | 19,348 B |

Two facts about the 17 **named** files, both [F]:

1. **All 17 boards belong to other devices.** The names are
   `bangkk, corfup, corfuq, corfur, cypfg, denver, fogo, fogor, fogos, ibiza,
   miami, milanf, penang, pnangn, rhodei, rhodep` — and `develop` maps
   `miami`→`Edge_30_Neo`, `fogos`→`Moto_G34_5G`, `bangkk`→`Moto_G84_5G`.
   Exactly **one** (`fogo`) is this device's own codename. So 16 of 17 are
   other products' board files shipped in this vendor partition.
2. **All four Motorola devices in this `fogo`-family cluster ship the identical
   17 names** — `fogo`, `fogos`, `bangkk`, `miami` all carry the same 17-file
   set, and 15 of the 17 are md5-identical across all four. The two that differ
   are `bdwlan_fogo_epa.bin` (3 devices share one hash, `Edge_30_Neo` has
   another) and `bdwlan_fogos_ipa.bin` (all four differ) [F].

So the named-`bdwlan` set is a **vendor-partition constant**, not a per-device
artefact, and its filenames are a **board catalogue** rather than a statement
about the SoC in the handset [F, I]. Any tool that infers "this device is a
`fogos`" from a `bdwlan_fogos_ipa.bin` present on a `fogo` device would be
wrong.

The numeric `bdwlan.<hex>` names use the full hex alphabet — `b3a`, `b5d`,
`b6a` appear — while the MBN-segment suffixes in this slice use **decimal** digits
only (`.`+two decimal digits) [F]. That is worth stating because the two look
alike: `adsp.b16` is segment 16 decimal, and `bdwlan.b16` would be a hex
suffix. In this slice the distinction is clean — the `bNN` stems that carry an
`.mdt` use only `0-9` in their suffixes, and only the `bdwlan`/`bdwlanu` names
use `a-f` [F].

### 6.4 The `gpu` family is 94.07% one fingerprint TA

This is #2024's finding measured from the family side [F]:

| what | rows | bytes | share of `gpu` bytes |
|---|---:|---:|---:|
| `fpctzapp.*` (fingerprint TA) | 9 | 2,998,383 | **94.07%** |
| `a660_*` (co-resident, unusable) | 3 | 102,460 | 3.21% |
| real Adreno 619 firmware (`a619_gmu`, `a630_sqe`, `a615_zap.*`) | 6 | 80,928 | **2.54%** |
| `sequence_manifest.bin` | 1 | 5,704 | 0.18% |

So **2.54%** of the labelled GPU bytes are live GPU firmware, and the family is
0.41% of the slice [F]. The on-device consequence: the `gpu` folder in the
vendor partition is ~3 MiB of which ~81 KB is the GPU [I].

`sequence_manifest.bin` is `db_type=UNKNOWN`, 5,704 B, and appears on 50 rows
across 15 SoC labels [F] — a vendor build artefact, not GPU firmware, and it is
in this family only because it lives in `vendor/gpu/kbc/` [I].

### 6.5 The `a660` rows carry `db_type=AUDIO`, corpus-wide and totally

#2024 §3 established the *co-residency* — three `a660_*` files on an Adreno 619
SoC. The label defect is the new observation, and it is total [F]:

| file | corpus rows | `db_type` values | `blob_family` values |
|---|---:|---|---|
| `a660_gmu.bin` | 21 | **`AUDIO`** (only) | `gpu` (only) |
| `a660_sqe.fw` | 30 | **`AUDIO`** (only) | `gpu` (only) |
| `a660_zap.mdt` | 21 | `ELF64` | `gpu` |

And it is not confined to `a660`. **Every** `AUDIO`-labelled row inside
`blob_family = gpu` in the whole matrix is one of four filenames [F]:

```
AUDIO, family=gpu, 79 rows:
  a660_sqe.fw   30
  a660_gmu.bin  21
  a650_gmu.bin  14
  a650_sqe.fw   14
```

Four SoC-adjacent GPU filenames — two Adreno generations — carry the `AUDIO`
label on all 79 of their rows, and **no** other GPU filename ever does. So this
is a single mislabel rule applied to a specific set of files, not a per-device
slip [F]. A consumer that selects GPU firmware by `db_type ∈ {GPU}` will find
`a619_gmu.bin` and miss `a660_gmu.bin`/`a650_gmu.bin` entirely.

Note the asymmetry: `a660_zap.mdt` is `ELF64` while `a660_gmu.bin` and
`a660_sqe.fw` are `AUDIO`, and `a619_gmu.bin` is correctly `GPU` [F]. So the
defect correlates with the *generation* of the filename, not with the row.

## 7. Two laws this slice can test

### 7.1 `mdt == b00 + b01` holds 17 of 17, and the 6 untestable stems are one thing

| set | count |
|---|---:|
| stems with an `.mdt` | 23 |
| testable (has `.mdt`, `.b00`, `.b01`) | **17** |
| equal | **17** |
| unequal | **0** |
| untestable | **6** |

The 6 untestable stems are **all** single-file MDTs with no segments at all:
`a660_zap` (6,708 B), `evass` (8,068), `evass-lt` (8,068), `vpu20_1v` (8,068),
`vpu20_2v` (8,068), `vpu20_4v` (8,068) [F]. Zero are "segmented but missing
`.b00`" — unlike #805's `cpe_9340` case, which was the whole reason that note
had to split the untestable set in two.

A detail that #2024 §4 already established and this appears to contradict:
`a615_zap.b02` (1,984 B) is referenced by neither `.b00` nor `.b01`, yet the
`mdt == b00+b01` identity still holds exactly (148 + 6,712 = 6,860) [F]. So the
law is **not** "the `.mdt` contains every segment" — it is "the `.mdt` is exactly
header-plus-first-two-segments, and later segments are independently loaded".
#2024's "orphan `.b02`" framing is correct and this section corroborates it
rather than correcting it.

The six untestable MDTs are also a **size coincidence worth recording**: all six
are exactly **8,068 B**, but all six md5s are distinct [F]:

| file | bytes | md5 |
|---|---:|---|
| `evass.mdt` | 8,068 | `2475ccea0aad83d9…` |
| `evass-lt.mdt` | 8,068 | `1a5a853c7fae82a5…` |
| `vpu20_1v.mdt` | 8,068 | `fc7c6aa3fcfad7d2…` |
| `vpu20_2v.mdt` | 8,068 | `612c2f6d7dbbe57b…` |
| `vpu20_4v.mdt` | 8,068 | `7f0db1fcb6774646…` |
| `a660_zap.mdt` | 6,708 | `c9d12833b4a7b92d…` |

So five of the six share a size and none share content — identical header
geometry, different bodies. `a660_zap.mdt` is the odd one at 6,708 B, and 6,708
is the self-contained-`.mdt` build that
`Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md` §4 already characterised [F].

### 7.2 `.b00` = ELF header + phdr table: `52 + 32N` / `64 + 56N`, and a correction to #805

**This section corrects a formula published in #805.** That note
(`Qualcomm-MSM8998-Snapdragon-835-soc.md:703-706`) states:

> `b00` size decomposes as an ELF header plus 32 B per program header:
> `52 + 32N` for ELF32, `64 + 32N` for ELF64. … exactly one fits neither —
> `cmnlib64`'s **400 B** (400 − 64 = 336, not a multiple of 32 …)

The ELF64 constant is wrong. An ELF64 program header is **56 bytes**, not 32
(the 32-byte figure is the ELF32 size). With the correct constant,
`400 = 64 + 56×6`, and `cmnlib64` is not exceptional at all [F].

The corpus-wide test is decisive, and it is a two-part proof:

**(a) No `.b00` size is ambiguous between the two formulae.** Of the 1,314
`.b00` rows there are **40 distinct sizes**. Thirty-seven fit only `52 + 32N`
(556 rows); three fit only `64 + 56N` (758 rows); and **zero fit both**, zero
fit neither [F]:

| ELF64 sizes (`64 + 56N`) | rows | N |
|---|---:|---:|
| 400 | 7 | **6** |
| 512 | 269 | **8** |
| 568 | 482 | **9** |

| ELF32 sizes (`52 + 32N`), selected | rows | N |
|---|---:|---:|
| 148 | 76 | 3 |
| 308 | 147 | 8 |
| 468 | 22 | 13 |
| 692 | 36 | 20 |
| 1,204 | 22 | 36 |

Because the two arithmetic families are disjoint, every `.b00` in the corpus is
classified without ambiguity [F].

**(b) The derived phdr count never falls below the segment count.** Across all
1,314 `.b00`-bearing stems, `phdr − nseg` is never negative [F]:

| `phdr − nseg` | stems |
|---:|---:|
| 0 | **1,069** |
| +1 | 89 |
| +2 | 32 |
| +3 | 77 |
| +4 | 12 |
| +8 | 35 |

**(c) The seven 400-byte headers are all `cmnlib64`, all six-segment, all
seven devices.** [F]

```
cmnlib64.b00 = 400 = 64 + 56×6   and nseg = 6 on all seven
  SM8250        OnePlus_8_Pro
  MSM8998       OnePlus_7T, OnePlus_7
  SM8150        OnePlus_7_Pro
  SM8150-AC     OnePlus_7T_Pro
  SM8250        OnePlus_8
  (blank)       Mi_A3
```

So `cmnlib64` is a **six-segment ELF64 trustlet with 6 program headers** —
exactly the shape every other ELF64 trustlet has. #805's `[F, OPEN]` on that
stem resolves to `[F]`, and the `[OPEN]` in its §9 item 6 should be read as
closed. The `64` in the filename does **not** predict the ELF class (that
conjecture in #805 was right and is unaffected); it is the *header size* that
was miscomputed.

**On this slice the corrected law holds without exception** [F]:

| class | stems | `b00` | phdr | nseg | missing indices |
|---|---:|---:|---:|---:|---|
| ELF32 | `a615_zap` | 148 | 3 | 3 | — |
| ELF32 | `adsp` | 1,204 | 36 | 34 | 11, 35 |
| ELF32 | `cdsp` | 468 | 13 | 10 | 7, 10, 12 |
| ELF32 | `goodixfp`, `gpqese`, `hdcpsrm`, `tbase` | 308 | 8 | 8 | — |
| ELF32 | `ipa_fws` | 212 | 5 | 5 | — |
| ELF32 | `modem` | 1,204 | 36 | 33 | 16, 23, 35 |
| ELF32 | `venus` | 692 | 20 | 12 | 11–18 |
| **ELF64** | `dxhdcp2`, `eseservice`, `faceauth_ta`, `featenabler`, `fpctzapp`, `loadalgota64`, `soter64` | 512 | **8** | 8 | — |

Ten ELF32 stems, seven ELF64 stems, and the seven ELF64 ones are all
`512 = 64 + 56×8` with 8 segments and **no** missing index [F]. Under the old
32-byte constant those seven read `64 + 32×14 = 512` and claim 14 program
headers for 8 segments. The reason the error stayed invisible is that 512 is not
an ELF32 size at all — `(512 − 52) / 32 = 14.375` — so the two forms never
compete for it, and only the *segment-count* cross-check separates "8 headers,
8 segments" from "14 headers, 8 segments".

The same distinction explains the 568-byte ELF64 family (482 rows, `N = 9`) —
which under `52+32N` would be `(568−52)/32 = 16.125`, a non-integer, so it can
never be ELF32 [F].

## 8. Mainline and postmarketOS: nothing, four different ways

| probe | result | class |
|---|---|---|
| `arch/arm64/boot/dts/qcom` entries | 1,328; `4375`→`[]`, `holi`→`[]`, `blair`→`[]`, `4350`→`[]`, `fogo`→`[]` | [N] |
| `sm4375.dtsi` | absent | [N] |
| GitHub code search `sm4375 repo:torvalds/linux` | **total_count 0** | [N] |
| GitHub code search `"qcom,sm4375"` | **0**; `"qcom,holi"` **0**; `sm4375.dtsi` **0** | [N] |
| `Documentation/devicetree/bindings/arm/qcom.yaml` | `4375`, `holi`, `blair`, `4350` → **0 hits each** | [N] |
| `QCOM_ID_SM4375` / `socinfo.c` | absent | [N] |
| `a6xx_catalog.c` `machine = "qcom,sm4375"` | absent (3 `.machine` strings total) | [N] |
| `qcom,sm4375-*-pas` in `qcom_q6v5_pas.c` | absent | [N] |
| `linux-msm.github.io/mainline-status/soc/sm4375` | **404**; index lists 34 SoC pages, none for 4375/4350/6375 | [N] |
| `gitlab.com/.../pmaports` `device/` dirs | 479 scanned across `main` (13), `community` +126, `testing` +1,083 — **0** match `4375`, `holi`, `g5g`, `fogo` | [N] |
| postmarketOS wiki `srsearch` | `SM4375` **0**, `holi` **0**, `Snapdragon 4 Gen 1` **0**, `Moto G 5G 2024` **0** | [N] |
| `qcom/a619_gmu.bin` in `linux-firmware` | **404** | [N] |
| `qcom/a615_zap.mbn` | **404** | [N] |
| `qcom/a630_gmu.bin` | **200** | [F] |

### 8.1 The linux-firmware gap is specific to this GPU generation

The `qcom/` tree ships 60 entries. The Adreno firmware present is
`a612_rgmu.bin`, `a623_gmu.bin`, `a630_gmu.bin`, `a630_sqe.fw`, `a640_gmu.bin`,
`a650_gmu.bin`, `a650_sqe.fw`, `a660_gmu.bin`, `a660_sqe.fw`, `a663_gmu.bin`
[F]. `a615`, `a616`, `a617`, `a618`, `a619` and `a620` are **all absent** [N].

The kernel, meanwhile, asks for `a619_gmu.bin` on three catalog entries
(`a6xx_catalog.c:876, 901, 925`) [F]. So mainline names a firmware file that
linux-firmware does not ship — the GPU works on these SoCs only if the
proprietary partition supplies it, which is exactly what this device's
`vendor/gpu/kbc/a619_gmu.bin` (32,768 B, md5 `9e23c52057bb…`) is [F, I].

`WHENCE` lists `a630_gmu.bin` with **no version string** while
`a630_sqe.fw` carries `v2.07` [F] — so the GMU blob's provenance is a
`capability`/`extract` entry without a release tag. That is consistent with it
being a re-hosted vendor file rather than an upstream-authored one [I].

The `.mdt`/`.mbn` naming split matters here too: `WHENCE` uses
`qcom/sm8350/a660_zap.mbn` (a `.mbn`, symlinked) while every device in this
corpus ships `a660_zap.mdt` [F]. The corpus contains **zero** `.mbn` files of any
name across 33,917 rows [N] — the same negative #805 reported, corroborated on a
different slice.

### 8.2 What a port would have to build

Nothing in this list is new work that this note performs; it is the delta a
future port faces [I]:

1. `sm4375.dtsi` + a board file, from scratch. The `sm4450.dtsi` CPU block is the
   better template (§1.3).
2. A `QCOM_ID_SM4375` in `qcom,ids.h` and a `soc_id[]` entry. The number is not
   public in mainline; the vendor bootloader would have it.
3. Three PAS compatibles (`adsp`/`cdsp`/`mpss`) mapped onto the `sm6375`
   resource structs, since the firmware filenames match.
4. A venus node, or an explicit acknowledgement that the 13 venus files on this
   device are unclaimed.
5. `a619_gmu.bin` into linux-firmware, or a `linux-firmware`-free path.

## 9. Honest negatives

1. **No instruction-level CPU proof exists in this corpus, and I did not
   manufacture one** [N]. `isa_identified` is empty on all 364 rows; there is no
   SM4375 device tree to supply a MIDR; no payload was read. §1.2 gives the
   arithmetic (`0x410fd410`, `0x410fd050`) and says plainly that observing
   either needs `MIDR_EL1` from a booted device.
2. **The CPU topology is public spec, not measurement** [F for the source]. The
   matrix cannot confirm 2+6 from any column; the device's own `dtbo.img` is a
   24 MiB partition dump I did not unpack.
3. **I did not parse a single ELF, MDT or ext4 image** [N]. §7.2's
   `52 + 32N` / `64 + 56N` result is inferred from *sizes only* — the two
   constants are the ELF32 and ELF64 program-header sizes, applied to sizes that
   partition perfectly, with the segment count as an independent cross-check.
   The program-header count is not directly observed.
4. **The `64 + 56N` correction contradicts two shipped notes, and both are now
   corrected in place** [F]. This note's §7.2 is the authority; per Rule 1 it
   was applied to `research/soc/Qualcomm-MSM8998-Snapdragon-835-soc.md` §7.1
   (whose `[F, OPEN]` on `cmnlib64` resolves to `[F]`, and whose §9 item 6 now
   reads resolved) **and** to `research/soc/Qualcomm-SM8350-Snapdragon-888-soc.md`
   §6.5, where the same `64 + 32N` constant had produced an ELF64 row of
   `64+32×14` with a spurious `N − segments = 6`, and a matrix-wide claim of
   "38 of 122 stems fit neither". Under the correct constant that becomes
   `64+56×8` with `N − segments = 0`, and **0 of 122** non-fits. So the error
   entered at #823 and propagated to #805, not the other way round; the
   SM8350 note's §1/§4/§6.5 did contain it and an earlier draft of this item
   said otherwise.
5. **`hyp.img` 8.00 MiB vs `hyp_mem` 6.00 MiB is unexplained** [OPEN]. §5.3
   states the three possible readings and satisfies none of them.
6. **I cannot say which speedbin table the `fogo` GPU uses** [OPEN]. §2 records
   that the catalog has two 619 entries with different speedbin sets and the DT
   selects between them; this device has no DT.
7. **The `dsp.img` 32 MiB contents were not inspected** [N, OPEN]. It is 4.28% of
   the slice. The 64 MiB form (15 SoCs) is documented elsewhere as ext4 with
   `/adsp`, `/cdsp`, `/sdsp` inside; the 32 MiB form (7 SoCs, including this one)
   has no such precedent in the repo. Whether the halved size means a different
   filesystem layout is [OPEN].
8. **`modem.img` 414,187,520 B was not opened** [N]. It is 52.8% of the slice and
   the single largest object. All that is stated about it is its size and
   `db_type`.
9. **`evass` / `evass-lt` / `vpu20_*` are single-file MDTs I cannot identify**
   [OPEN]. Six stems, all exactly 8,068 B, all `db_type=ELF64`, all filed under
   `other`. The `vpu20` set appears on 11 SoC labels; `evass` on 13. I did not
   determine what they are.
10. **The `bdwlan` "vendor catalogue" reading is inference** [I]. §6.3's claim
    that 16 of 17 named files belong to other products rests on the
    `db_path`→codename mapping plus the fact that exactly one name matches. It
    is not proof that the vendor ships foreign board files deliberately.
11. **I did not verify the 17 named `bdwlan` md5 equality claim against payload**
    [F]. The 15-of-17 identical figure is `md5_db`, a database column, not a
    re-hash.
12. **`interface_documented` is `n` on 364 of 364 and `sha256_if_listed` is empty
    on 364 of 364** [F]. So this slice contributes **nothing** to an interface
    spec or a hash-verification pass. That is a property of the extraction, not
    of the firmware.
13. **The 22 `db_type` values include 94 `UNKNOWN`** [F], 25.8% of the slice.
    Four of those are `a615_zap.b01/.b02`, `fpctzapp.b01…b07` — i.e. real
    trustlet segments that the labeler could not type.
14. **`tbase` on this device is not explained** [OPEN]. §6.2 notes that only 8
    devices corpus-wide ship it and 3 SoC labels own them; SM4375 is the
    singleton. Whether `tbase` is SoC-specific or a Motorola platform choice is
    not decidable from 8 rows.

## Reproduce

Every number above is regenerated by these commands. All are `python3 -I`,
stdlib only, run from the repository root.

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm SM4375 Snapdragon 4 Gen 1']
tot=sum(int(r['size_bytes']) for r in s)
print('slice',len(s),'devices',len({r['device'] for r in s}),'bytes',tot,'files',len({r['filename'] for r in s}))
for f in sorted({r['blob_family'] for r in s}):
    rs=[r for r in s if r['blob_family']==f]
    b=sum(int(r['size_bytes']) for r in rs)
    print(f,len(rs),len({r['filename'] for r in rs}),b,round(100*b/tot,2))
print(Counter(r['db_type'] for r in s).most_common())
print('isa',sum(1 for r in s if r['isa_identified'].strip()),'iface',Counter(r['interface_documented'] for r in s).most_common(),'sha',sum(1 for r in s if r['sha256_if_listed'].strip()))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm SM4375 Snapdragon 4 Gen 1']
by={r['filename']:int(r['size_bytes']) for r in s}
print('mdt',len([f for f in by if f.endswith('.mdt')]))
import re
print('bNN',len([f for f in by if re.fullmatch(r'.*\.b[0-9]{2}\$',f)]))
print('pow2',len([f for f in by.values() if f and (f&(f-1))==0]))
print(Counter(r['db_path'] for r in s).most_common())
print('top10',round(100*sum(sorted(by.values())[-10:])/sum(by.values()),2))
for f in ('modem.img','boot.img','dtbo.img','xbl.img','abl.img','hyp.img','tz.img','uefisecapp.img','dsp.img'):
    print(f,by[f],round(by[f]/1048576,4))"
```

```bash
python3 -I -c "
import csv,re
from collections import defaultdict
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm SM4375 Snapdragon 4 Gen 1']
stem=defaultdict(dict)
for r in s:
    m=re.match(r'^(.+?)\.(mdt|b([0-9]{2}))\$',r['filename'])
    if m: stem[m.group(1)][m.group(2)]=int(r['size_bytes'])
test=[k for k,v in stem.items() if all(x in v for x in ('mdt','b00','b01'))]
eq=[k for k in test if stem[k]['mdt']==stem[k]['b00']+stem[k]['b01']]
un=[k for k,v in stem.items() if 'mdt' in v and not all(x in v for x in ('b00','b01'))]
print('testable',len(test),'equal',len(eq),'untestable',len(un),sorted(un))
for k in sorted(test):
    v=stem[k]; b=v['b00']; idx=sorted(int(x[1:]) for x in v if re.fullmatch(r'b\d\d',x))
    n32=(b-52)/32.0; n64=(b-64)/56.0
    cls,ph=('ELF32',int(n32)) if n32==int(n32) else (('ELF64',int(n64)) if n64==int(n64) else ('?',-1))
    print(k,cls,b,ph,len(idx),[i for i in range(ph) if i not in idx])"
```

```bash
python3 -I -c "
import csv,re
from collections import Counter,defaultdict
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
sizes=Counter(int(r['size_bytes']) for r in rows if r['filename'].endswith('.b00'))
a=[s for s in sizes if (s-52)%32==0 and s>=52]
b=[s for s in sizes if (s-64)%56==0 and s>=64]
print('distinct b00',len(sizes),'rows',sum(sizes.values()))
print('E32-only',len([s for s in a if s not in b]),'rows',sum(sizes[s] for s in a if s not in b))
print('E64-only',len([s for s in b if s not in a]),'rows',sum(sizes[s] for s in b if s not in a))
print('both',[s for s in a if s in b],'neither',[s for s in sizes if s not in a and s not in b])
print('E64 sizes',sorted([(s,sizes[s],(s-64)//56) for s in b]))
tri=defaultdict(dict)
for r in rows:
    m=re.match(r'^(.+?)\.(b([0-9]{2}))\$',r['filename'])
    if m: tri[(r['soc'].strip(),r['device'],m.group(1))][m.group(2)]=int(r['size_bytes'])
d=Counter(); neg=0
for k,v in tri.items():
    if 'b00' not in v: continue
    b0=v['b00']; n=len(v)
    ph=(b0-52)//32 if (b0-52)%32==0 else (b0-64)//56
    d[ph-n]+=1
    if ph<n: neg+=1
print('delta dist',sorted(d.items()),'negative',neg)
print('cmnlib64',[ (k,v.get('b00')) for k,v in tri.items() if k[2]=='cmnlib64'])"
```

```bash
python3 -I -c "
import csv
from collections import Counter,defaultdict
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
print('adsp db_type',Counter(r['db_type'] for r in rows if r['blob_family']=='adsp').most_common())
print('gpu AUDIO',Counter(r['filename'] for r in rows if r['blob_family']=='gpu' and r['db_type']=='AUDIO').most_common())
for fn in ('a660_gmu.bin','a660_sqe.fw','a660_zap.mdt'):
    rs=[r for r in rows if r['filename']==fn]
    print(fn,len(rs),sorted({r['db_type'] for r in rs}),sorted({r['blob_family'] for r in rs}))
trio=defaultdict(dict)
for r in rows:
    if r['filename'] in ('hyp.img','tz.img','uefisecapp.img'):
        trio[(r['soc'].strip(),r['device'])][r['filename']]=int(r['size_bytes'])
m=[k for k,v in trio.items() if v=={'hyp.img':8388608,'tz.img':4194304,'uefisecapp.img':2097152}]
print('8/4/2 trio',len(m),sorted(m))
print('rpm socs',len({r['soc'].strip() for r in rows if r['filename']=='rpm.img'}))
print('aop socs',len({r['soc'].strip() for r in rows if r['filename'].startswith('aop')}))"
```

```bash
python3 -I -c "
import csv,re,itertools
from collections import defaultdict
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
devs=('Moto_G_5G_2024','Moto_G34_5G','Moto_G84_5G','Edge_30_Neo')
D={d:{r['filename']:(int(r['size_bytes']),r['md5_db']) for r in rows if r['device']==d} for d in devs}
for a,b in itertools.combinations(devs,2):
    A,B=set(D[a]),set(D[b]); sh=A&B
    print(a,b,round(len(sh)/len(A|B),4),len(sh),sum(1 for f in sh if D[a][f][1]==D[b][f][1]))
print('only-fogo',sorted(set(D['Moto_G_5G_2024'])-set(D['Moto_G34_5G'])))
print('only-fogos',sorted(set(D['Moto_G34_5G'])-set(D['Moto_G_5G_2024'])))"
```

```bash
curl -s "https://api.github.com/repos/torvalds/linux/contents/arch/arm64/boot/dts/qcom?ref=master&per_page=1000" | python3 -I -c "import json,sys;n=[x['name'] for x in json.load(sys.stdin)];print(len(n),[f for f in n if '4375' in f or 'holi' in f or 'fogo' in f])"
for f in a619_gmu.bin a615_zap.mbn a630_gmu.bin; do printf '%s ' "$f"; curl -s -o /dev/null -w '%{http_code}\n' "https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/qcom/$f"; done
curl -s "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/arch/arm64/include/asm/cputype.h" | grep -n 'CORTEX_A78\|CORTEX_A55\|ARM_CPU_IMP_ARM'
curl -s "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/gpu/drm/msm/adreno/a6xx_catalog.c" | grep -n 'machine = \|revn = 619\|a619_gmu.bin'
curl -s "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/remoteproc/qcom_q6v5_pas.c" | grep -c 'qcom,sm4375'
curl -sL "https://wiki.postmarketos.org/api.php?action=query&list=search&srsearch=SM4375&format=json&srlimit=5" | python3 -I -c "import json,sys;print(json.load(sys.stdin)['query']['searchinfo'])"
```

## Sources

| claim | source | access |
|---|---|---|
| 364 rows / 1 device / 784,040,172 B / 364 filenames; 9-family table; 22 `db_type`s; `isa_identified` empty 364/364; `interface_documented` `n` 364/364; `sha256_if_listed` 0/364; 101 stems | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-24 |
| `mdt == b00+b01` 17/17; 6 untestable stems all single-file MDTs; `.b00` class + phdr + missing-index table | same | 2026-11-24 |
| 40 distinct `.b00` sizes; 37 ELF32-only (556 rows) / 3 ELF64-only (758 rows) / 0 both / 0 neither; `phdr−nseg` distribution; `cmnlib64` 400 = 64+56×6 on 7 devices | same | 2026-11-24 |
| `adsp` → `MODEM` 3,281/3,281; `AUDIO` within `gpu` = 79 rows, 4 filenames only; `a660_*` label sets | same | 2026-11-24 |
| 8/4/2 MiB `hyp`/`tz`/`uefisecapp` trio, 11 devices, 6 SoC labels, 11 distinct `hyp.img` md5s | same | 2026-11-24 |
| `rpm.img` 8 SoCs vs `aop*` 14 SoCs, overlap only SM7325-AE | same | 2026-11-24 |
| 7-way `db_path` table; `radio` 19 rows / 629,526,528 B = 80.3% | same | 2026-11-24 |
| 4-device Jaccard (0.8244–0.9409); `fogo`-only 14 files, `fogos`-only 8; 243/350 md5-identical | same | 2026-11-24 |
| 96 `bdwlan*` all 26,328 B; 76 hex + 2 `bdwlanu` + 17 named + `bdwlan.bin`; 17 named shared by 4 devices, 15 md5-identical | same | 2026-11-24 |
| `gpu` family split: `fpctzapp` 94.07%, `a660` 3.21%, real 2.54%, manifest 0.18% | same | 2026-11-24 |
| `bm2n` 6-file set on SM4375 + 10 other SoCs; 51/53 on two 8-series parts; 14 devices total | same | 2026-11-24 |
| `tbase` on 8 devices / 3 SoC labels; SM4375 the singleton | same | 2026-11-24 |
| 25 power-of-two files = 52,473,520 B = 6.7%; top-10 = 88.61%; `modem.img` = 52.8% of slice, 77.63% of family | same | 2026-11-24 |
| `cpus.yaml` enum `kryo240`…`kryo780`, `kryo660` `:223`, `kryo670` `:224`; no 4xx-series number for this part | `Documentation/devicetree/bindings/arm/cpus.yaml` | 2026-11-24 |
| `ARM_CPU_IMP_ARM` 0x41, `ARM_CPU_IMP_QCOM` 0x51; `CORTEX_A55` 0xD05 `:74`, `CORTEX_A78` 0xD41 `:80`; `MIDR_CPU_MODEL` `:43-46`; Kryo 6XX note `:241-246` | `arch/arm64/include/asm/cputype.h` | 2026-11-24 |
| A55 in the KPTI-safe list `:1695`; **no** `CORTEX_A78` entry anywhere; `KRYO_4XX_SILVER` `:1704`, `:1871` | `arch/arm64/kernel/cpufeature.c` | 2026-11-24 |
| `sm6375.dtsi`: 8× `qcom,kryo660`, 2 `cpu-map` clusters, `freq-domain` 0×6/1×2, 3 remoteprocs, `rpm-proc`, `pil_video_mem` 5 MiB, `hyp_mem` 6 MiB @ `0x80000000`, 18 reserved regions / 446.44 MiB, no `tz_mem`, no venus node | `arch/arm64/boot/dts/qcom/sm6375.dtsi` | 2026-11-24 |
| `sm4450.dtsi`: 6× `arm,cortex-a55` + 2× `arm,cortex-a78`, 1 `cpu-map` cluster, 2 `freq-domain`s, no `hyp_mem`, no `tz_mem` | `arch/arm64/boot/dts/qcom/sm4450.dtsi` | 2026-11-24 |
| `sm8350.dtsi` / `sm8250.dtsi`: `hyp_mem` 6 MiB, no `tz_mem`; SM8350 also `hyp_reserved_mem` @ `0xd0000000` | `sm8350.dtsi`, `sm8250.dtsi` | 2026-11-24 |
| `a6xx_catalog.c`: only 3 `.machine =` strings (`sm7150` `:820`, `sm4350` `:870`, `sm6375` `:895`); three `.revn = 619` at `:873,898,922`; `a619_gmu.bin` at `:876,901,925`; `a615_zap.mdt` at `:801,882,907,932`; a615-family comment `:63`, `:506` | `drivers/gpu/drm/msm/adreno/a6xx_catalog.c` | 2026-11-24 |
| `qcom,sm6375-{adsp,cdsp,mpss}-pas` at `:2051-2053`; resource structs `sm6350_adsp_resource` `:1135`, `sm6375_mpss_resource` `:1151`, `sm8150_cdsp_resource` `:1310`; **no** `sm4375` compatible | `drivers/remoteproc/qcom_q6v5_pas.c` | 2026-11-24 |
| `QCOM_ID_SM4375` absent; `SM4450` 568 `:274`, `SM7325` 475 `:239`, `SM6375` 507 `:251`; 308 defines, max 781 | `include/dt-bindings/arm/qcom,ids.h` | 2026-11-24 |
| `qcom_board_id(SM4375)` absent; 295 `qcom_board_id(` entries; 0 hits for `4375`/`holi` | `drivers/soc/qcom/socinfo.c` | 2026-11-24 |
| `qcom.yaml` 0 hits for `4375`/`holi`/`blair`/`4350`; `qcom,sm4450` `:1066`, `qcom,sm6375` `:1103`, `qcom,sm7325` `:1129` | `Documentation/devicetree/bindings/arm/qcom.yaml` | 2026-11-24 |
| 1,328 DT entries; `4375`/`holi`/`blair`/`4350`/`fogo` all `[]`; `sm6375.dtsi` + 1 board, `sm4450.dtsi` + 1, `sm7325.dtsi` + 7, `kodiak.dtsi` | GitHub contents API on `arch/arm64/boot/dts/qcom/` | 2026-11-24 |
| GitHub code search `sm4375 repo:torvalds/linux` = 0; `"qcom,sm4375"` = 0; `"qcom,holi"` = 0; `sm4375.dtsi` = 0 | GitHub search/code API | 2026-11-24 |
| `qcom/` 60 entries; `a619_gmu.bin` 404, `a615_zap.mbn` 404, `a630_gmu.bin` 200; no `a615`/`a616`/`a617`/`a618`/`a619`/`a620`; venus only as `venus-N.N/venus.mbn` + `.mdt` symlink | `git.kernel.org/.../linux-firmware.git/tree/qcom` and `plain/qcom/<name>` | 2026-11-24 |
| `WHENCE`: `a630_gmu.bin` versionless, `a630_sqe.fw` v2.07, `a660_zap.mbn` under `qcm6490/` with `qcs6490`+`sm8350` symlinks; `.mbn` naming throughout | `WHENCE` (540,393 B) | 2026-11-24 |
| 0 `.mbn` rows of any name in 33,917 | coverage matrix | 2026-11-24 |
| 479 `device/` dirs (main 13, community 126, testing 1,083 minus overlap); 0 matches `4375`/`holi`/`g5g`/`fogo`; `linux-postmarketos-qcom-sm4375` 404 | GitLab `pmaports` tree + file API (default branch `master`) | 2026-11-24 |
| wiki `srsearch` 0 hits for `SM4375`, `holi`, `Snapdragon 4 Gen 1`, `Moto G 5G 2024` | `wiki.postmarketos.org/api.php` | 2026-11-24 |
| 34 SoC pages listed; `soc/sm4375`, `soc/sm4350`, `soc/sm6375` all 404 | `linux-msm.github.io/mainline-status/` index + per-page fetch | 2026-11-24 |
| 2× A78 @2000 MHz + 6× A55 @1800 MHz, 6 nm, announced 2022-10-06 | nanoreview `qualcomm-snapdragon-4-gen-1` | 2026-11-24 |
| SM4375 part number on the Snapdragon 4 Gen 1 product brief | Qualcomm product brief (docs.qualcomm.com) | 2026-11-24 |
| Snapdragon 4 Gen 2 = SM4450, 2× A78 + 6× A55, 4 nm, 2023-06-26 | Qualcomm 4 Gen 2 brief; nanoreview; WikiChip | 2026-11-24 |
| GPU identity, `fpctzapp` mislabel proof, `talos`=QCS615 trap, zero-DT enumeration, `a660` co-residency | `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md` §1-§5 | 2026-11-20 |
| `b`-only 9 parts including SM4375; every `b` is 26,328; `b<NN> ≡ phdr NN`; zero-`p_filesz` yields no file | `research/fleet/wifi-wpss.md:531,613,764,1197`, `:77-79` | 2026-11-24 |
| SM4375 fleet CDSP row: 1 device / 12 rows / 12 files | `research/cdsp-fleet/census.md:212` | 2026-11-24 |
| SM4375 in the `hyp` census; 63 `hyp` rows all 4,096-multiples | `research/fleet/tz-hyp.md:104`, §1.2 | 2026-11-24 |
| SM4375 slice shape 364 rows / 0.78 ratio / `all` families | `research/soc/per-soc-method-plans.md:66` | 2026-11-24 |
| `adsp`-family group style; `.b00` = header + phdr table; `qupfw` has no mainline binding | `research/soc/Qualcomm-SM8350-Snapdragon-888-soc.md` §1, §4, §6.5 | 2026-11-24 |
| `mdt == b00+b01` 27/27, `tz_mem` 45 MiB @ `0x86200000`, `cmnlib64` `[OPEN]` — **and the `64+32N` ELF64 constant this note corrects (§7.2)** | `research/soc/Qualcomm-MSM8998-Snapdragon-835-soc.md:689-720`, §9.6 | 2026-11-24 |
| `52+32N` / `64+32N` on 8 / 15 stems, "38 of 122 neither", ELF64 row `64+32×14` with `N − segments = 6` — **the same error, corrected in place per Rule 1 (§7.2)** | `research/soc/Qualcomm-SM8350-Snapdragon-888-soc.md` §1, §4, §6.5, §9.16-17 | 2026-11-24 |
| a615-family (a615/a616/a618/a619) firmware set | `research/laptop/qualcomm-adreno-gmu-content.md` §4 | 2026-11-24 |
