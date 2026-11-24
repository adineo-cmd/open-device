# Qualcomm MSM8998 Snapdragon 835 — CPU: eight cores, two clusters, and the slice that is not this SoC

Issue #841. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative / [OPEN] unresolved. Every number is command output from a run on
**2026-11-24** against
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows,
123 devices, 28 distinct SoC labels), `torvalds/linux` master, and public
device-capture transcripts named in `## Sources`.

**No payload exists in this workspace and none was read.** Every statement below
is matrix metadata — filename, size, md5, `db_type`, family label — or public
GPL source, or a byte-length check on a public upstream file. No vendor ELF is
parsed here and no instruction is disassembled [N]. Where this note quotes a
`/proc/cpuinfo` capture, that capture is a public text file; the SoC's own
firmware was not executed.

This is the **CPU** note. The SoC package, DSP, boot chain, TrustZone and
firmware census for MSM8998 are owned by
`research/soc/Qualcomm-MSM8998-Snapdragon-835-soc.md` (#805) and are **cited,
never re-derived**. The GPU is owned by
`research/soc/Qualcomm-MSM8998-Snapdragon-835-gpu.md` (#2018).

This note has one job #805 did not do, and one correction it has to make.

## 0. Verdict

| question | answer | class |
|---|---|---|
| CPU topology | **4 + 4**, two `cpu-map` clusters, `compatible = "qcom,kryo280"` on all eight nodes | [F] |
| MPIDR affinity | `0x0`–`0x3` (little), `0x100`–`0x103` (big) | [F] |
| Cluster weight ratio | `capacity-dmips-mhz` 1024 × 4 / 1536 × 4 = **1 : 1.5** | [F] |
| Implementer | **`0x51` = Qualcomm**, not `0x41` (ARM) | [F] |
| Part numbers | **`0x800` gold, `0x801` silver** | [F] |
| Reported MIDR | **gold `0x51AF8001`, silver `0x51AF8014`** | [F] |
| ISA baseline | ARMv8.0-A: **8** `/proc/cpuinfo` feature flags, **no** `atomics`, **no** `asimdhp`, **no** `asimddp` | [F] |
| Kryo 280 microarchitecture | semi-custom **Cortex-A73** (big) + **Cortex-A53** (little) | [I] |
| CPU DVFS in DT | **none** — `msm8998.dtsi` has 0 `cpufreq_hw` nodes and 0 `qcom,freq-domain` | [F] |
| The 871-row slice | **OnePlus 7 / 7T = SM8150**, `qcom,kryo485`, 1+3+4 — **not** this SoC | [F] |
| Instruction-level proof for *the slice* | **SM8150 parts `0x804`/`0x805` variant `0xd` rev `14`** | [F] |
| Instruction-level proof for *MSM8998* | **two independent public captures**, `0x800`/`0x801` rev `1`/`4` | [F] |

The headline is not the topology — #805 already had it. The headline is that
**this issue's own slice is the wrong SoC**, and that the instruction-level
proof it asks for is obtainable, just not from the slice.

## 1. What #805 established, and what it recorded as impossible

#805 §1 owns the MSM8998 DT topology: eight nodes, all `qcom,kryo280`, `reg`
`0x0`–`0x3` then `0x100`–`0x103`, `capacity-dmips-mhz` 1024 and 1536,
`cpu-map` two clusters, `qcom,msm-id = <292 0x0>` in the SoC dtsi and
`<292 0x20001>` in the OnePlus common board file. All of that is [F] there and
is [F] here; I re-ran it (§3) rather than trusting it, and it holds.

#805 §9.1 then recorded an honest negative, and the verdict table carried it as
`[N]`:

> **CPU instruction-level ID** — **not obtainable from this corpus** —
> `isa_identified` is empty on all 871 rows and mainline's DT does not encode a
> MIDR for either cluster

That statement is correct about *the corpus*, and it is the sentence this note
is written to settle. The issue asks for "instruction-level proof". A CSV of
firmware filenames will never contain it. A booted device does.

So this note changes the class from `[N]` to `[F]`, and it changes the source
from "the corpus" to "public captures of devices running this SoC". That is a
class change and it needs to be declared, not smuggled in as if #805 had said it
all along.

## 2. The delta: the slice is SM8150, and the issue is named MSM8998

This is the single most important thing in the note, and it is not a
technicality.

[F] The label `Qualcomm MSM8998 Snapdragon 835` selects **871 rows**, and the
rows belong to exactly **two devices**:

```
device        rows   bytes
OnePlus_7      433   494,092,577
OnePlus_7T     438   585,064,437
```

[F] Those two devices are **SM8150** hardware. #805 §0 and §8.3 established this
from four independent sources, and #2018's LineageOS evidence predates it.
`per-soc-method-plans.md:70-75` states the consequence in the project's own
words:

> OnePlus 7 (`guacamoleb`) and OnePlus 7T (`hotdogb`) carry "MSM8998 835"
> (they are SM8150). Consequence: the MSM8998 cluster's entire 871-row blob
> content is actually SM8150-family firmware; the genuine-835 devices (mata,
> joan, nx659j, cheeseburger, walleye, taimen) have **zero** blob rows.

[F] I re-verified the device set and the row split from the matrix (§3, R1).
[F] I re-verified that `arch/arm64/boot/dts/qcom/` carries **15** `msm8998-*`
files and **0** `guacamole*` or **0** `hotdog*` files (§3, R7) — so mainline
agrees that these two boards are not 835 boards.

[I] Therefore a note titled `Qualcomm-MSM8998-Snapdragon-835-cpu.md` has two
honest options: describe MSM8998 and say the slice is not it, or describe the
slice and rename. The deliverable path is fixed by the issue, so this note takes
the first option and states the mismatch in the first section rather than the
last.

### 2.1 Why the two CPUs are not interchangeable

| property | MSM8998 (Snapdragon 835) | SM8150 (Snapdragon 855) | class |
|---|---|---|---|
| `compatible` | `qcom,kryo280` | `qcom,kryo485` | [F] |
| shape | **4 + 4** | **1 + 3 + 4** | [F] |
| MPIDR `reg` | `0x0-0x3`, `0x100-0x103` | `0x0`, `0x100`…`0x700` | [F] |
| `capacity-dmips-mhz` | 1024 ×4 / 1536 ×4 | 488 ×4 / 1024 ×4 | [F] |
| `qcom,freq-domain` | **none** | `0,0,0,0,1,1,1,2` | [F] |
| `cpu-map` clusters | **2** | **1** | [F] |
| L2 cache nodes | **2** (per cluster) | **8** (per core) + 1 L3 | [F] |
| reported MIDR | `0x51AF8001` / `0x51AF8014` | `0x51DF804E` / `0x51DF805E` | [F] |
| ISA flags | 8 | 16 | [F] |
| `cpufreq_hw` references | **0** | **17** | [F] |

Every row of that table is command output (§3). Not one of the differences is
cosmetic: the two SoCs disagree on core count per cluster, on cache topology, on
DVFS architecture, and on the instruction set the cores actually advertise.

[I] A reader who reads "871 rows / 2 devices" in the issue and then reads an
MSM8998 CPU analysis would reasonably conclude the analysis describes the
firmware. It does not. It cannot. There is no MSM8998 firmware in this
repository to describe.

## 3. MSM8998's real CPU, from the DT

### 3.1 The eight nodes

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

[F] All eight are `compatible = "qcom,kryo280"`, `device_type = "cpu"`,
`enable-method = "psci"` (8 of 8). The 4+4 split is encoded in three
independent places — `reg`, `capacity-dmips-mhz`, `cpu-map` — and the three
agree.

[F] `cpu-map` at `:230` declares exactly two clusters. `cluster0` holds
`cpu0`–`cpu3`; `cluster1` holds `cpu4`–`cpu7`.

[F] Only **2** `l2-cache` nodes exist, both `cache-level = <2>`, shared across
each cluster by `next-level-cache`. There is **no L3 node** in `msm8998.dtsi`
(zero `cache-level = <3>`). SM8150 by contrast has 8 L2 nodes plus one `l3_0` at
`cache-level = <3>`.

[I] So the DT describes a classic big.LITTLE 4+4 with per-cluster L2 and no
shared L3 — which is what A73 + A53 wants, and is the opposite of the DynamIQ
1+3+4 with per-core L2 and a shared L3 that SM8150 describes.

### 3.2 No CPU DVFS node at all

This is a fact about MSM8998 that #805 does not state and that matters for
anyone porting.

[F] `msm8998.dtsi` contains **zero** `cpufreq_hw` references and **zero**
`qcom,freq-domain` properties. Its 8 CPU nodes carry no `clocks`, no
`operating-points-v2`, and no `power-domains` — grep over the `:140`–`:228`
range returns **0** hits for all four properties.

[F] `sm8150.dtsi` contains **17** `cpufreq_hw` references, **8**
`qcom,freq-domain` properties, and every CPU node has a `clocks = <&cpufreq_hw N>`.

[F] The MSM8998 dtsi does carry a `rpmpd` power controller
(`compatible = "qcom,msm8998-rpmpd"`, `:366`) with an OPP table of RPM SMD
levels, and **9** `operating-points-v2` references overall — but none of them
attach to a CPU node. They serve DSI, GPU and MDP.

[I] MSM8998 has no EPSS. Its CPU frequency scaling is the older RPM/RPMh path,
not the `qcom-cpufreq-hw` EPSS path. `drivers/cpufreq/qcom-cpufreq-nvmem.c`'s
match table lists `qcom,msm8996`, `qcom,apq8096`, `qcom,qcs404` and others but
**0** entries for `msm8998` — so in mainline the 835's CPU DVFS is not wired up
by either driver. That is a real mainline gap and it is `[OPEN]` here rather
than asserted as working.

### 3.3 Machine identity

[F] `qcom,msm-id = <292 0x0>` in `msm8998.dtsi`; the OnePlus 5 common board file
pins `<292 0x20001>` (8998 **v2.1**). 292 is `QCOM_ID_MSM8998`.

[I] The slice rows carry no such identity. They carry a string in a CSV column,
and that string is wrong for the devices (§2).

## 4. The MIDR, and an arithmetic error this note corrects

This is the part #805 got numerically wrong, and it propagated to two other
documents.

### 4.1 The kernel's constants

[F] `arch/arm64/include/asm/cputype.h`:

```
:58   #define ARM_CPU_IMP_QCOM        0x51
:128  #define QCOM_CPU_PART_KRYO_2XX_GOLD    0x800
:129  #define QCOM_CPU_PART_KRYO_2XX_SILVER  0x801
:43   #define MIDR_CPU_MODEL(imp, partnum) \
        ((_AT(u32, imp) << MIDR_IMPLEMENTOR_SHIFT) | \
         (0xf           << MIDR_ARCHITECTURE_SHIFT) | \
         ((partnum)     << MIDR_PARTNUM_SHIFT))
```

[F] Evaluating that macro at `imp = 0x51`:

| part | `MIDR_CPU_MODEL(0x51, part)` |
|---|---|
| `0x800` gold | **`0x510F8000`** |
| `0x801` silver | **`0x510F8010`** |

### 4.2 The error

[F] #805 §1.2, and by citation `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-soc.md:93`
and `docs/REPO-STATE-MAP.md:23`, state the values as:

```
MIDR_QCOM_KRYO_2XX_GOLD    0x51008000
MIDR_QCOM_KRYO_2XX_SILVER  0x51008010
```

[F] Those two constants are **wrong by one nibble**. The macro puts `0xf` in the
architecture field; `0x51008000` has `0x0` there. Computed value
`0x510F8000` ≠ published value `0x51008000`.

[I] The `0x0` in the published value is the *rev/variant* field being zero in
`pytorch/cpuinfo`'s alternative spelling (`src/arm/midr.h` writes
`CPUINFO_ARM_MIDR_KRYO280_GOLD 0x51AF8001`), and the two conventions got
crossed. The kernel's own macro yields `0x510F8000`; a real device reports
`0x51AF8001`. Neither is `0x51008000`.

[F] Correcting three places is Rule 1 work done in the same session as this
note; the before/after is in §7.

### 4.3 What a real MSM8998 reports

[F] Two independent public captures, different devices, different kernels:

| | taimen (Pixel 2 XL), kernel 4.4.210 | APQ8098 (`chemag/cpuinfo` test vector) |
|---|---|---|
| `CPU implementer` | `0x51` | `0x51` |
| `CPU architecture` | `8` | — |
| `CPU variant` | `0xa` | `0xa` |
| `CPU part` cores 0–3 | `0x801` | `0x801` |
| `CPU revision` cores 0–3 | `4` | `4` |
| `CPU part` cores 4–7 | `0x800` | `0x800` |
| `CPU revision` cores 4–7 | `1` | `1` |
| `Hardware` | `Qualcomm Technologies, Inc MSM8998` | `Qualcomm Technologies, Inc APQ8098` |

[F] So the little cluster is `0x801` at revision 4 and the big cluster is
`0x800` at revision 1, giving the reported MIDRs:

```
silver (cores 0-3)  0x51AF8014
gold   (cores 4-7)  0x51AF8001
```

[F] Those two words decode to `part = 0x801/0x800`, `variant = 0xa`,
`arch = 0xf`, `rev = 0x4/0x1` — and the revision nibbles are *exactly* what
`pytorch/cpuinfo`'s `midr.h` encodes (`...14` silver, `...01` gold). Two
independent sources agreeing on a revision number is not a coincidence.

[F] Masking either against the kernel's model mask (`MIDR_CPU_MODEL_MASK`, which
covers implementer, part and architecture) yields `0x510F8010` and `0x510F8000`
— i.e. the kernel's constants, confirmed against hardware.

[I] This is the instruction-level proof the issue asks for. It is not from this
corpus [N] — it is from a booted device's `MIDR_EL1` as exported through
`/proc/cpuinfo`. #805 was right that the corpus cannot supply it and wrong to
file the question as unanswerable.

### 4.4 What the kernel does with those IDs

[F] Both Kryo 2XX MIDRs sit in the KPTI-safe list (`cpufeature.c:1701-1702`,
`kpti_safe_list`), so an 835 is declared Meltdown-immune by MIDR rather than by
probe:

```
:1701   MIDR_ALL_VERSIONS(MIDR_QCOM_KRYO_2XX_GOLD),
:1702   MIDR_ALL_VERSIONS(MIDR_QCOM_KRYO_2XX_SILVER),
```

[F] `MIDR_ALL_VERSIONS(m) = MIDR_RANGE(m, 0, 0, 0xf, 0xf)` (`cputype.h:332`) —
it matches any variant and any revision, which is why the DT-less, revision-
varying reality of shipping 835s does not break the match.

## 5. The ISA, at flag level

[F] `/proc/cpuinfo` `Features`, both MSM8998 captures identical:

```
fp asimd evtstrm aes pmull sha1 sha2 crc32
```

That is **8** flags. Both SM8150 captures, also identical to each other:

```
fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm lrcpc dcpop asimddp
```

That is **16** flags, and the 8 extra are exactly:

```
atomics asimdhp asimddp asimdrdm cpuid dcpop fphp lrcpc
```

[F] The MSM8998 set is a strict subset: **0** flags present on 835 and absent on
855; 8 shared.

[I] This is the cleanest single-line instruction-level discriminator between the
two SoCs in this note. `atomics` (ARMv8.1 LSE) and `asimddp` (dot product) are
architectural-level markers: their absence pins Kryo 280 at **ARMv8.0-A**, and
their presence puts Kryo 485 at **ARMv8.2-A**. A note that claimed the 871-row
slice was 835 firmware would have to explain how 835 cores acquired LSE.

[I] It also means the two clusters are *not* distinguishable by ISA on MSM8998 —
all eight cores report the same 8 flags, which is consistent with A73 and A53
both being ARMv8.0-A parts.

## 6. Kryo 280 is a semi-custom Cortex-A73 / A53

[I] ARM's "Built on ARM Cortex Technology" licence let Qualcomm take A73 and
A53 and change the cache and memory subsystem while keeping the pipeline. Kryo
280 is the flagship example: **4 × Cortex-A73** big at 2.45 GHz and
**4 × Cortex-A53** little at 1.90 GHz, 10 nm, 2 MB L2 on the performance
cluster and 1 MB on the efficiency cluster. `pytorch/cpuinfo/src/arm/uarch.c`
independently maps `Q 0x800 → UARCH_CORTEX_A73` and `Q 0x801 → UARCH_CORTEX_A53`,
which is the same pairing derived from the other direction.

[I] The `capacity-dmips-mhz` ratio corroborates it: 1536/1024 = **1.5**. A73 is
roughly 1.5–1.7× A53 per MHz at the same process, which is what the DT is
encoding. The number is not decorative.

[I] Because the part numbers are Qualcomm's (`0x800`/`0x801`, implementer
`0x51`), the cores do **not** self-identify as A73/A53. Contrast SM8150, which
*also* reports Qualcomm part numbers (`0x804`/`0x805`) even though its cores are
not semi-custom — see §8.

## 7. Rule 1 pass: three stale MIDR constants corrected

The `0x51008000` / `0x51008010` error from §4.2 appears in three files. All
three are corrected in this same session, respecting file walls.

| file | before | after |
|---|---|---|
| `Qualcomm-MSM8998-Snapdragon-835-soc.md` §1.2 code block | `0x51008000` / `0x51008010` | `0x510F8000` / `0x510F8010` (macro output), plus a dated correction note naming the observed device MIDRs |
| `Qualcomm-MSM8998-Snapdragon-835-soc.md` §9.1 | same two values inside the "no instruction-level proof" negative | corrected values, plus a 2026-11-24 note that device captures now supply the proof and pointing here |
| `Qualcomm-MSM8998-Snapdragon-835-soc.md` Sources row for `cputype.h` | asserts `→ MIDR 0x51008000 / 0x51008010` | `0x510F8000` / `0x510F8010`, cites the macro line `:43`, and names the device captures |
| `Qualcomm-SM4375-Snapdragon-4-Gen-1-soc.md:93` | `(0x51008000 / 0x51008010)` | `(0x510F8000 / 0x510F8010)` |
| `docs/REPO-STATE-MAP.md` CPU/SoC core-ID row | `MIDR 0x51008000/0x51008010`; "4 per-SoC CPU core-ID sections"; "23 SoCs remain" | corrected MIDRs, **5** sections, **22** SoCs remain |

[F] A row is also added to `research/CORRECTIONS.md`, because this is a
numerical claim this project published and then had to fix.

[F] After these edits the occurrences of `0x51008000` left in the repository
are exactly two sets, both deliberate: the ones in this note (§4.2, §7), and a
single line in `Qualcomm-MSM8998-Snapdragon-835-soc.md:111` that quotes the old
value inside the correction note. Grep over `*.md` returns no other hit
(2026-11-24). No document still asserts it as a live MIDR.

## 8. The slice's actual CPU: SM8150, Kryo 485

For completeness — because the issue's slice is this hardware — the CPU the 871
rows run on.

[F] `sm8150.dtsi` is **132,399 B**. Eight nodes, all `compatible =
"qcom,kryo485"`, `enable-method = "psci"`:

| node | line | `reg` | `capacity-dmips-mhz` | `freq-domain` |
|---|---:|---|---:|---:|
| `cpu0` | 52 | `0x0` | 488 | 0 |
| `cpu1` | 81 | `0x100` | 488 | 0 |
| `cpu2` | 105 | `0x200` | 488 | 0 |
| `cpu3` | 129 | `0x300` | 488 | 0 |
| `cpu4` | 153 | `0x400` | 1024 | 1 |
| `cpu5` | 177 | `0x500` | 1024 | 1 |
| `cpu6` | 201 | `0x600` | 1024 | 1 |
| `cpu7` | 225 | `0x700` | 1024 | **2** |

[F] `cpu-map` at `:249` declares **one** cluster with all eight cores in it —
the DynamIQ shape. The capacity ratio 1024/488 = **2.10**, much wider than
MSM8998's 1.5.

[F] `freq-domain` is `0,0,0,0,1,1,1,2`: three domains, so `cpu7` (the prime) is
in its own domain and DVFS can clock it independently of `cpu4`–`cpu6`.

[F] Real SM8150 silicon reports:

| | value | note |
|---|---|---|
| `CPU implementer` | `0x51` | Qualcomm, not ARM |
| `CPU variant` | `0xd` | |
| `CPU part` cores 0–3 | `0x805` | Kryo 485 Silver |
| `CPU part` cores 4–7 | `0x804` | Kryo 485 Gold / Prime |
| `CPU revision` | `14` | `0xe` |
| `Hardware` | `Qualcomm Technologies, Inc SM8150` | |

giving MIDRs `0x51DF805E` (silver) and `0x51DF804E` (gold).

[I] The part-number ordering is the **same** on both SoCs, not inverted: gold is
`0x800` on 835 and `0x804` on 855, silver is `0x801` and `0x805`, so in each
generation gold is the lower of the pair. The trap is a different one —
`0x800`/`0x801` are Kryo 2XX IDs and `0x804`/`0x805` are Kryo 4XX IDs, four
apart, so a mask that tests only the low part-number bits can fold one
generation onto the other.

### 8.1 The erratum that pins the variant and revision

[F] `cpufeature.c:1869-1871`:

```
/* Kryo4xx Silver (rdpe => r1p0) */
MIDR_REV(MIDR_QCOM_KRYO_4XX_SILVER, 0xd, 0xe),
```

`MIDR_REV(m, v, r) = MIDR_RANGE(m, v, r, v, r)`, so this matches variant `0xd`
revision `0xe` exactly — and the real device reports variant `0xd` revision
`14`. **14 = 0xe.** The kernel's broken-DBM erratum list was written against
this exact silicon stepping, and the capture confirms it.

[I] This is a pleasing cross-check: a value in the kernel that looks arbitrary
(`0xd, 0xe`) turns out to be the literal variant/revision of shipping
Snapdragon 855 parts. It also means the erratum is not hypothetical.

[F] By contrast `MIDR_QCOM_KRYO_4XX_GOLD` (`cputype.h:234`) is **defined and
used nowhere** in `cpufeature.c` — 0 references outside its definition. Gold on
SM8150 carries no erratum workaround.

### 8.2 Kryo 485 is not semi-custom

[I] Unlike Kryo 280, Kryo 485 cores are stock Cortex-A76 (prime and gold) and
Cortex-A55 (silver) — `gcc`'s `aarch64-cores.def` maps `0x41/0xd0b` → A76 and
`0x41/0xd05` → A55, and every public spec sheet names A76 + A55. But the
*reported* part numbers are Qualcomm's `0x804`/`0x805`, not ARM's. Qualcomm
renumbered stock ARM cores under its own implementer ID.

[I] So the "implementer `0x51` therefore semi-custom" inference is **false**.
The 835 is semi-custom; the 855 is not; both report `0x51`. Implementer ID tells
you who branded the part, not who designed the pipeline.

## 9. Boot chain and TrustZone — cited, not re-derived

The issue asks for the boot chain and TrustZone mapped. Both are owned by #805
and are cited here in the compressed form a CPU note needs.

[F] **Boot chain** (#805 §4): the `boot` family is **17 rows / 9 filenames /
359,960,576 B**. Six are real images — `xbl.img` (3,182,592 B, `UEFIBOOT`),
`xbl_config.img` (126,976 B, `ELF64`), `abl.img` (225,280 B, `UEFIBOOT`),
`aop.img` (204,800 B), `qupfw.img` (73,728 B, `ELF64`), `vbmeta.img` (4,096 B on
the 7, 8,192 B on the 7T). Three are partition dumps — `boot.img` and
`recovery.img` at 100,663,296 B each, `dtbo.img` at 25,165,824 B — and they hold
**352,321,536 of 359,960,576 B = 97.9%** of the family. The real chain is
**12 rows / 2.1%** of the bytes.

[F] **TrustZone** (#805 §5): **168 rows / 85 filenames / 19,779,884 B**, 60
distinct sizes. The `tz_mem` reserved window is **45.00 MiB at `0x86200000`**,
inside **15** reserved regions totalling **225.08 MiB**. SM8150's `tz_mem` is
**57 MiB at the same base**.

[I] Neither chain is CPU-specific, and neither can be attributed to the 871 rows
with confidence — because those rows are SM8150 firmware (§2). The boot chain
that mainline would actually use for these two devices is
`sm8150-*`, and there is **no** `sm8150-oneplus-guacamole` DT in mainline (§3,
R7).

## 10. Mainline and postmarketOS status

[F] `arch/arm64/boot/dts/qcom/` carries **15** `msm8998-*` files, for boards
including `msm8998-mtp`, `msm8998-clamshell` (HP Envy x2, Lenovo Miix 630,
ASUS NovaGo, FxTec Pro1), `msm8998-oneplus-cheeseburger` / `-dumpling` (OnePlus
5 / 5T), three Sony Xperia Yoshino boards, and `msm8998-xiaomi-sagit` (Mi 6).

[F] It carries **7** `sm8150-*` files: `sm8150-hdk`, `sm8150-mtp`,
`sm8150-microsoft-surface-duo`, and three Sony Kumano boards.

[F] It carries **0** `guacamole*` and **0** `hotdog*` files. The two devices in
this issue's slice have **no mainline board DT at all**.

[I] So the honest statement of support is: MSM8998 has real mainline support for
a dozen x86-class laptops and two OnePlus phones (the *5*, not the 7); the two
devices in this slice are supported — where they are supported — as SM8150
boards, and even that support has no mainline DT yet.

[F] postmarketOS packages both slice devices against
`linux-postmarketos-qcom-sm8150`, with `deviceinfo_dtb="qcom/sm8150-oneplus-*"`
(#805 §8.3). There is no `guacamoleb` package in any pmaports channel (#805).

## 11. Honest negatives

1. **I did not read a single vendor instruction** [N]. No payload was opened,
   no ELF disassembled, no `MIDR_EL1` read by me. Every MIDR in §4.3 and §8 is a
   value transcribed from a public `/proc/cpuinfo` text capture, which is the
   kernel's own decoding of that register.
2. **The 871-row slice contains zero MSM8998 firmware** [N]. `isa_identified`
   is empty on all 871 rows, and the devices are SM8150. This note therefore
   documents a CPU that the corpus does not cover.
3. **MSM8998 CPU DVFS is `[OPEN]`** [OPEN]. No `cpufreq_hw` node, no
   `freq-domain`, no CPU `operating-points-v2` in the dtsi; no `msm8998` entry
   in `qcom-cpufreq-nvmem.c`'s match table. How an 835 scales CPU frequency in
   mainline today is not established here.
4. **The A73/A53 attribution is [I], not [F]** [I]. It rests on ARM's licensing
   statement, Qualcomm's product brief, and `cpuinfo`'s `uarch.c` mapping. The
   part numbers alone cannot prove it, because Qualcomm renumbered the cores.
5. **`capacity-dmips-mhz` is not a measurement** [N]. 1024/1536 and 488/1024 are
   declared values in the DT; nothing here measures them.
6. **I did not verify the two captures were taken on an 835** beyond the
   `Hardware:` line and the part numbers [I]. `taimen` is a Pixel 2 XL, which is
   835; `APQ8098` is the same silicon without a modem.
7. **The revision nibbles (`1`/`4`) are device-specific** [I]. Different 835
   steppings would report different revisions; the part numbers `0x800`/`0x801`
   are the stable identity.

## 12. Reproduce

Every command below was run on 2026-11-24 and exits 0.

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm MSM8998 Snapdragon 835']
print('rows',len(s),'files',len({r['filename'] for r in s}),'bytes',sum(int(r['size_bytes']) for r in s))
print('devices',dict(Counter(r['device'] for r in s)))
print('families',len({r['blob_family'] for r in s}),'db_types',len({r['db_type'] for r in s}))
print('isa_identified empty',sum(1 for r in s if not r['isa_identified'].strip()))"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm MSM8998 Snapdragon 835']
for dev in ('OnePlus_7','OnePlus_7T'):
    d=[r for r in s if r['device']==dev]
    print(dev,len(d),sum(int(r['size_bytes']) for r in d))
a={r['filename'] for r in s if r['device']=='OnePlus_7'}
b={r['filename'] for r in s if r['device']=='OnePlus_7T'}
print('shared filenames',len(a&b))"
```

```bash
python3 -I -c "
def m(imp,part): return (imp<<24)|(0xf<<16)|(part<<4)
print('gold  0x%08X'%m(0x51,0x800))
print('silver 0x%08X'%m(0x51,0x801))
print('observed gold   0x51AF8001')
print('observed silver 0x51AF8014')
mask=(0xff<<24)|(0xfff<<4)|(0xf<<16)
print('obs gold   & mask 0x%08X'%(0x51AF8001&mask))
print('obs silver & mask 0x%08X'%(0x51AF8014&mask))"
```

```bash
python3 -I -c "
v=(0xd<<20)|0xe
print('cpufeature.c 0xd,0xe ->',hex(v))
print('real SM8150  0xd,14 ->',hex((0xd<<20)|14))
print('match',((0xd<<20)|14)==v)
print('SM8150 silver MIDR 0x%08X'%((0x51<<24)|(0xd<<20)|(0xf<<16)|(0x805<<4)|14))
print('SM8150 gold   MIDR 0x%08X'%((0x51<<24)|(0xd<<20)|(0xf<<16)|(0x804<<4)|14))"
```

```bash
python3 -I -c "
a=set('fp asimd evtstrm aes pmull sha1 sha2 crc32'.split())
b=set('fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm lrcpc dcpop asimddp'.split())
print('MSM8998',len(a),'SM8150',len(b),'shared',len(a&b))
print('SM8150 only',sorted(b-a))
print('MSM8998 only',sorted(a-b))"
```

```bash
python3 -I -c "
import re,urllib.request,time
def get(u,n=4):
    for i in range(n):
        try:
            return urllib.request.urlopen(u,timeout=60).read().decode()
        except Exception as e:
            if i==n-1: raise
            time.sleep(10*(i+1))
B='https://raw.githubusercontent.com/torvalds/linux/master/'
dts=get(B+'arch/arm64/boot/dts/qcom/msm8998.dtsi')
s85=get(B+'arch/arm64/boot/dts/qcom/sm8150.dtsi')
ct=get(B+'arch/arm64/include/asm/cputype.h')
cf=get(B+'arch/arm64/kernel/cpufeature.c')
one=get(B+'arch/arm64/boot/dts/qcom/msm8998-oneplus-common.dtsi')
print('== msm8998.dtsi',len(dts.encode()),'B')
print('compatible',sorted(set(re.findall(r'compatible = \"(qcom,kryo[0-9]+)\"',dts))))
print('capacity',re.findall(r'capacity-dmips-mhz = <([0-9]+)>',dts))
print('freq-domain count',dts.count('qcom,freq-domain'),'cpufreq_hw',dts.count('cpufreq_hw'))
print('cpu-map clusters',len(re.findall(r'\n\t\t\tcluster[0-9]+ \{',dts)))
print('l2 nodes',dts.count('l2-cache'),'l3 nodes',dts.count('cache-level = <3>'))
print('msm-id',re.findall(r'qcom,msm-id = <[^>]+>',dts))
print('oneplus msm-id',re.findall(r'qcom,msm-id = <[^>]+>',one))
print('== sm8150.dtsi',len(s85.encode()),'B')
print('compatible',sorted(set(re.findall(r'compatible = \"(qcom,kryo[0-9]+)\"',s85))))
print('capacity',re.findall(r'capacity-dmips-mhz = <([0-9]+)>',s85))
print('freq-domain',re.findall(r'qcom,freq-domain = <&cpufreq_hw ([0-9]+)>',s85))
print('cpu-map clusters',len(re.findall(r'\n\t\t\tcluster[0-9]+ \{',s85)))
print('cpufreq_hw refs',s85.count('cpufreq_hw'))
print('l2 nodes',s85.count('l2-cache'),'l3 nodes',s85.count('cache-level = <3>'))
print('== per-core nodes')
for m in re.finditer(r'(\w+): cpu@([0-9a-f]+) \{',dts):
    blk=dts[m.start():m.start()+900]
    r=re.search(r'reg = <0x0 0x([0-9a-f]+)>',blk); c=re.search(r'capacity-dmips-mhz = <([0-9]+)>',blk)
    print(' msm8998',m.group(1),dts[:m.start()].count(chr(10))+1,'mpidr=0x'+r.group(1),'cap='+c.group(1))
for m in re.finditer(r'(\w+): cpu@([0-9a-f]+) \{',s85):
    blk=s85[m.start():m.start()+900]
    r=re.search(r'reg = <0x0 0x([0-9a-f]+)>',blk); c=re.search(r'capacity-dmips-mhz = <([0-9]+)>',blk)
    f=re.search(r'qcom,freq-domain = <&cpufreq_hw ([0-9]+)>',blk)
    print(' sm8150',m.group(1),s85[:m.start()].count(chr(10))+1,'mpidr=0x'+r.group(1),'cap='+c.group(1),'fd='+f.group(1))
print('== cpu node property isolation (msm8998 :140-228)')
blk=dts[dts.find('cpu0: cpu@0'):dts.find('cpu7: cpu@700')+900]
for p in ('clocks','operating-points-v2','qcom,freq-domain','power-domains'):
    print(' ',p,blk.count(p))
print('== MIDR')
print('KRYO_2XX_GOLD',re.findall(r'QCOM_CPU_PART_KRYO_2XX_GOLD\s+(0x[0-9a-f]+)',ct))
print('KRYO_2XX_SILVER',re.findall(r'QCOM_CPU_PART_KRYO_2XX_SILVER\s+(0x[0-9a-f]+)',ct))
for pat in ('MIDR_QCOM_KRYO_2XX_GOLD','MIDR_QCOM_KRYO_2XX_SILVER','MIDR_QCOM_KRYO_4XX_SILVER','MIDR_QCOM_KRYO_4XX_GOLD'):
    print(' ',pat,[i+1 for i,l in enumerate(cf.split(chr(10))) if pat in l])
print(' KRYO_4XX_GOLD mentions in cpufeature.c',cf.count('MIDR_QCOM_KRYO_4XX_GOLD'))
"
```

```bash
grep -rn '0x51008000\|0x51008010\|0x510F8000\|0x51AF8001' --include='*.md' . | head -20
```

```bash
python3 -I -c "
import re
def m(imp,part): return (imp<<24)|(0xf<<16)|(part<<4)
print('A73',hex(m(0x41,0xD09)))
print('A53',hex(m(0x41,0xD03)))
print('ratio 1536/1024 =',1536/1024)
print('ratio 1024/488  =',round(1024/488,2))"
```

## Sources

| claim | source | access |
|---|---|---|
| 871 rows / 423 files / 1,079,157,014 B / 2 devices / 21 `db_type`s / 9 families; `isa_identified` empty 871/871; per-device split 433 + 438; 418 shared filenames | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-24 |
| slice devices are SM8150, not MSM8998; genuine-835 devices have 0 blob rows | `research/soc/per-soc-method-plans.md:70-75` | 2026-11-24 |
| `msm8998.dtsi` 77,917 B; 8 `qcom,kryo280` nodes `:140-228`; `reg` `0x0-0x3`/`0x100-0x103`; caps 1024/1536; 2 `cpu-map` clusters at `:230`; 2 L2 nodes, 0 L3; 0 `freq-domain`, 0 `cpufreq_hw`; `qcom,msm-id = <292 0x0>` | `arch/arm64/boot/dts/qcom/msm8998.dtsi`, master | 2026-11-24 |
| `sm8150.dtsi` 132,399 B; 8 `qcom,kryo485`; `reg` `0x0,0x100…0x700`; caps 488×4/1024×4; `freq-domain` `0,0,0,0,1,1,1,2`; 1 `cpu-map` cluster at `:249`; 8 L2 + 1 L3; 17 `cpufreq_hw` refs | `arch/arm64/boot/dts/qcom/sm8150.dtsi`, master | 2026-11-24 |
| `qcom,msm-id = <292 0x20001>` (8998 v2.1) | `arch/arm64/boot/dts/qcom/msm8998-oneplus-common.dtsi:20` | 2026-11-24 |
| `ARM_CPU_IMP_QCOM` 0x51; `KRYO_2XX_GOLD` 0x800 / `SILVER` 0x801; `KRYO_4XX_GOLD` 0x804 / `SILVER` 0x805; `MIDR_CPU_MODEL` macro at `:43`; `MIDR_ALL_VERSIONS` `:332` | `arch/arm64/include/asm/cputype.h` | 2026-11-24 |
| both Kryo 2XX MIDRs in `kpti_safe_list`; broken-DBM `MIDR_REV(MIDR_QCOM_KRYO_4XX_SILVER,0xd,0xe)`; `KRYO_4XX_GOLD` absent | `arch/arm64/kernel/cpufeature.c:1701-1702,1869-1871` | 2026-11-24 |
| real MSM8998: impl `0x51`, var `0xa`, part `0x801` rev 4 (cores 0-3), part `0x800` rev 1 (cores 4-7), `Hardware: … MSM8998` | `newandroidbook.com/ddb/Pixel2XL/` (taimen, kernel 4.4.210) | 2026-11-24 |
| same numbers on APQ8098 | `github.com/chemag/cpuinfo` `test/qcom.sdm835` | 2026-11-24 |
| real SM8150: impl `0x51`, var `0xd`, part `0x805`/`0x804`, rev 14, `Hardware: … SM8150`; two independent dumps | `github.com/kdrag0n/freqbench` `results/sm8150/new/cpuinfo.txt` and `results/sm8150ac/new/cpuinfo.txt`; `github.com/ThomasKaiser/sbc-bench` `results/cpuinfo/Qualcomm-SM8150.cpuinfo` | 2026-11-24 |
| ISA flags 8 vs 16; `atomics`/`asimdhp`/`asimddp`/`dcpop` absent on 835 | same four captures | 2026-11-24 |
| Kryo 280 gold = A73, silver = A53 | `pytorch/cpuinfo` `src/arm/uarch.c` `CHECK_UARCH(arch,cpu,'Q',0x800/0x801,…)`; Qualcomm 835 product brief; ARM "Built on Cortex Technology" | 2026-11-24 |
| Kryo 280 MIDR constants `0x51AF8001` / `0x51AF8014` | `pytorch/cpuinfo` `src/arm/midr.h:28-29` | 2026-11-24 |
| Kryo 485 gold = A76, silver = A55 | `gcc` `aarch64-cores.def` (`0x41/0xd0b`, `0x41/0xd05`); `pytorch/cpuinfo` `src/arm/uarch.c` `0x804/0x805`; WikiChip SD855; NanoReview | 2026-11-24 |
| no `msm8998` entry in cpufreq-nvmem match table; `qcom,cpufreq-hw`/`-epss` in `qcom-cpufreq-hw.c` | `drivers/cpufreq/qcom-cpufreq-nvmem.c:631-636`, `drivers/cpufreq/qcom-cpufreq-hw.c:439-442` | 2026-11-24 |
| 15 `msm8998-*` files, 7 `sm8150-*` files, 0 `guacamole*`, 0 `hotdog*` | GitHub contents API on `arch/arm64/boot/dts/qcom/`, master | 2026-11-24 |
| boot family 17 rows / 9 filenames / 359,960,576 B; 97.9% partition dumps; TZ 168 rows / 85 files / 19,779,884 B; `tz_mem` 45.00 MiB at `0x86200000` | `research/soc/Qualcomm-MSM8998-Snapdragon-835-soc.md` §4, §5 (#805), cited | 2026-11-22 |
| pmOS packages both devices as SM8150; no `guacamoleb` package | `research/soc/Qualcomm-MSM8998-Snapdragon-835-soc.md` §8.3, cited | 2026-11-24 |
| `qcom,kryo280` and `qcom,kryo485` both in the `compatible` enum; 17 `qcom,kryoN` entries | `Documentation/devicetree/bindings/arm/cpus.yaml:213,220` | 2026-11-24 |
