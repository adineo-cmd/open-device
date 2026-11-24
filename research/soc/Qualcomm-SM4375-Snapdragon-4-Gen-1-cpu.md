# Qualcomm SM4375 Snapdragon 4 Gen 1 — CPU: the vendor device tree, the revision trap, and an erratum that changed its scope

Issue #847. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative / [OPEN] unresolved. Every number is command output from a run on
**2026-11-24** against
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows,
28 distinct SoC labels), `torvalds/linux` master and the v5.4/v5.5–v5.15 tags,
`gregkh/linux` v5.4.x stable tags, and the public Motorola vendor kernel trees
named in `## Sources`.

**No payload exists in this workspace and none was read.** Every statement below
is matrix metadata — filename, size, `db_type`, family label — or public GPL
source. No vendor ELF is parsed here and no instruction is disassembled [N].

This is the **CPU** note. The SoC package, GPU, DSP, boot chain and TrustZone
census for SM4375 are owned by
`research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-soc.md` (#811) and are
**cited, never re-derived**. §7.2 records the one fact in that note this note
contradicts; §9 records the corrections to this note's own GATE 0.

## 0. Verdict

| question | answer | class |
|---|---|---|
| CPU topology | **6 + 2**: six little, two big — vendor `cpu-map` clusters `cluster0`×6 / `cluster1`×2 | [F] |
| `compatible` on all eight nodes | **`qcom,kryo`** — one string for two core types | [F] |
| `capacity-dmips-mhz` | **1024 (little ×6) / 1946 (big ×2)** — present, contrary to #811's prediction | [F] |
| `freq-domain` | `<&cpufreq_hw 0 6>` ×6, `<&cpufreq_hw 1 2>` ×2 — the core counts are *in the phandle args* | [F] |
| Platform codename | **`blair`** (SM6375 family base), device ID 578 = **`BLAIR-LITE`** | [F] |
| `qcom,msm-id` | **`<507 0x10000>, <578 0x10000>`** — 507 named in mainline, **578 is not** | [F] |
| Little cluster revision | **A55 r2p0** → MIDR **`0x412FD050`** | [I] |
| Big cluster revision | **A78 r1p1** → MIDR **`0x411FD411`** | [I] |
| `[N]` from #811 ("no instruction-level proof") | **still true of the corpus** — `isa_identified` empty 364/364; but the vendor DT supplies the cluster geometry and a real device supplies the revisions | [F], [I] |
| Erratum 1024718 scope | **r0p0–r2p0**, widened to *all versions* by `c0b15c25d251` (2021-02-03) | [F] |
| Does erratum 1024718 hit **this** silicon | **yes** — A55 r2p0 is inside the documented range | [F], [I] |
| A78 errata in the device's kernel | **zero** `CORTEX_A78` matches in v5.4 `cpufeature.c` and `cpu_errata.c` | [N] |

The headline is not the topology — #811 had 2+6 from public spec. The headline
is that **the platform is `blair`, not `holi`**, and that the vendor device tree
for this exact device is public, which turns three of #811's `[H]`/`[N]` items
into `[F]`.

## 1. What #811 established, and what it recorded as open

#811 §1 owns the public-spec topology (2× A78 + 6× A55, 6 nm, announced
2022-10-06), the MIDR arithmetic from `cputype.h`, the sibling-DT comparison
against `sm6375.dtsi` and `sm4450.dtsi`, and the machine-identity negative.
Four specific records are what this note has to answer:

1. §1.2 table: MIDRs `0x410fd410` / `0x410fd050`. Both are **r0p0** values,
   derived as arithmetic with no revision data.
2. §1.2 consequence 1: *"No instruction-level proof exists in this corpus"* —
   `isa_identified` empty on 364 of 364 rows.
3. §1.3 table row for `sm6375`: `cpu-map` clusters = **2**.
4. §1.3 conclusion: *"Predicting SM4375's DT from either would be a guess [H]"*
   and *"the `sm4450` style … is the better-motivated of the two"*.

Items 1 and 4 are answered by material #811 did not consult; item 3 is
contradicted; item 2 stands, and this note explains exactly how far past it the
evidence reaches.

## 2. The platform is `blair`, not `holi`

#811 does not name a platform codename for SM4375. The device's own vendor
kernel does, and it is not the codename the marketing material suggests.

The LineageOS `fogo` board config — `fogo` is the build codename of
`Moto_G_5G_2024`, the sole device in this slice (§5) — inherits a shared tree:

```
device/motorola/fogo/BoardConfig.mk:9
  include device/motorola/sm6375-common/BoardConfigCommon.mk
device/motorola/fogo/BoardConfig.mk:25
  TARGET_KERNEL_CONFIG += vendor/ext_config/moto-holi-fogo.config
```

So two codenames appear before reaching the kernel: `sm6375` in the include
path and `holi` in the config filename. The kernel then contradicts both:

```
arch/arm64/boot/dts/vendor/qcom/blair-moto-fogo-base.dts:15
  #include "blair.dtsi"
arch/arm64/boot/dts/vendor/qcom/blair.dtsi:18
  model = "Qualcomm Technologies, Inc. Blair "
arch/arm64/boot/dts/vendor/qcom/blair.dtsi:20
  qcom,msm-id = <507 0x10000>, <578 0x10000>;
```

`blair` is the SM6375-family platform; `holi` is the SM4350/SM480 family. The
vendor `socinfo.c` names both explicitly [F]:

```
drivers/soc/qcom/socinfo.c (vendor)
  :782   { 454, "HOLI" },
  :783   { 507, "BLAIR" },
  :784   { 578, "BLAIR-LITE" },
  :785   { 565, "BLAIRP" },
  :786   { 628, "BLAIRP-XR" },
  :787   { 647, "BLAIRP-LTE" },
```

The same six-line block appears verbatim in two unrelated vendor trees
(`android_kernel_oneplus_sm8350`, `android_kernel_samsung_sm7325`), so it is a
shared Qualcomm table, not a Motorola edit [F].

The conclusion is that **SM4375 boots from the `blair` device tree, as
`BLAIR-LITE`, and reports SoC ID 578** [F]. The `holi` string in the build
config is a lower-case re-use of the SM4350-era config name inside the shared
`sm6375-common` tree — it is a filename, not an identity [I]. A `Hardware:`
line of `holi` on a real unit would therefore be **expected and misleading**,
which is exactly why §8 refuses to treat that field as evidence.

> Note for the reader: this note initially reasoned from a `holi` attribution
> inherited from GATE 0. The vendor DT is what refuted it. The correction is
> recorded in §9.

## 3. The device tree, node by node

`blair.dtsi` is 94,327 B and declares eight CPUs. Everything below is measured
from that file [F].

### 3.1 Geometry

| property | value | note |
|---|---|---|
| CPU nodes | **8** (`CPU0`–`CPU7`) | `reg` `0x0`–`0x700`, stride `0x100` |
| `compatible` | **`qcom,kryo`** ×8 | one string, two core types |
| `cpu-map` clusters | **2** — `cluster0` = `CPU0`–`CPU5`, `cluster1` = `CPU6`–`CPU7` | 6 + 2 |
| `capacity-dmips-mhz` | **1024** ×6, **1946** ×2 | present |
| `dynamic-power-coefficient` | **100** ×6, **520** ×2 | present |
| `qcom,freq-domain` | `<&cpufreq_hw 0 6>` ×6, `<&cpufreq_hw 1 2>` ×2 | `#freq-domain-cells = <2>` |
| L2 nodes | **8** (`L2_0`–`L2_7`), one per core | `cache-level = <2>` |
| L3 nodes | **1** (`L3_0`), shared | `cache-level = <3>` |
| `enable-method` | `psci` ×8 | |
| `cpu-release-addr` | `<0x0 0x50000000>` ×8 | |

The `freq-domain` encoding is the load-bearing one. The node declares

```
blair.dtsi:1291   #freq-domain-cells = <2>;
```

and each CPU passes a domain index **and a core count**: `0 6` for the six
little cores, `1 2` for the two big ones. So the cluster split is encoded
**three independent ways** — `cpu-map`, `freq-domain` domain index, and
`freq-domain` core count — and the core count itself is redundant with both.
A consumer reading only `compatible` sees a homogeneous 8-core machine [F].

### 3.2 The frequency domain block

```
blair.dtsi:1279  cpufreq_hw: qcom,cpufreq-hw {
blair.dtsi:1280    compatible = "qcom,cpufreq-hw-epss";
blair.dtsi:1281    reg = <0x0fd91000 0x1000>, <0x0fd92000 0x1000>;
blair.dtsi:1282    reg-names = "freq-domain0", "freq-domain1";
blair.dtsi:1285    qcom,lut-row-size = <4>;
blair.dtsi:1286    qcom,lut-max-entries = <12>;
```

Two register windows 0x1000 apart, **12 LUT entries per domain**, row size 4.
Twelve is the ceiling on the number of OPPs the EPSS hardware can hold; the
actual OPP table lives in firmware and is read through this interface, which is
why there is no `opp-hz` list for the CPUs in this file [I]. There is a
`ddr-bw-opp-table` with 11 `BW_OPP_ENTRY` rows, but that is memory bandwidth,
not CPU DVFS [F].

### 3.3 What the vendor DT does **not** say

- No `arm,cortex-a78` or `arm,cortex-a55` string anywhere — all eight are
  `qcom,kryo` [F].
- No `qcom,msm-id` per core, and **no MIDR of any kind** [N]. The device tree
  cannot state a MIDR; that comes from the silicon (§4).
- No `clocks` or `operating-points-v2` on the CPU nodes themselves [N].

## 4. The revision trap: two of #811's four MIDRs are wrong for this silicon

### 4.1 The observation

`deviceinfohw.ru` item **108157**, device `fogo` / `moto g 5G - 2024`, reports
[F]:

| field | value |
|---|---|
| `CPU` | `sm4375` |
| `CORES` | `8` |
| `FAMILY` | `Cortex-A78 Cortex-A55` |
| `CLUSTERS` | `2 x 2.02 GHz 6 x 1.80 GHz` |
| `CLOCK_SPEED` | `300 - 2016 MHz` |
| `REVISION` | **`r1p1 r2p0`** |
| `TECHPROCESS` | `6 nm` |
| `GPU_MODEL` | `Adreno (TM) 619` |
| `KERNEL` | `5.4.274-moto-00507-gecc19605af65` |

The `REVISION` field is two `rXpY` tokens, big cluster first — the same field
order as `FAMILY` (`Cortex-A78` then `Cortex-A55`) and `CLUSTERS`
(`2 x 2.02` then `6 x 1.80`) on the same page.

#811's MIDR table used r0p0 for both clusters. This device is **r1p1** on the
big cluster and **r2p0** on the little one.

### 4.2 Why `rXpY` is variant X, revision Y — proven, not assumed

This is the one methodological claim the note has to earn, because the whole
delta rests on it. It is provable from a sibling part.

`deviceinfohw.ru` item **116843**, `Holi for arm64` / Snapdragon 480 Plus /
SM4350, reports `REVISION` = **`r8p14 r13p14`** [F]. Decode the little core's
`r13p14` as variant `13` = `0xd`, revision `14` = `0xe`, and compare against the
kernel:

```
arch/arm64/kernel/cpufeature.c:1871
  MIDR_REV(MIDR_QCOM_KRYO_4XX_SILVER, 0xd, 0xe),
```

`MIDR_REV(m, v, r)` is `MIDR_RANGE(m, v, r, v, r)` (`cputype.h:331`) — an exact
variant-and-revision match, not a range. The kernel's own comment for that line
reads `/* Kryo4xx Silver (rdpe => r1p0) */`, and the SM4350's little core is a
Kryo 4xx Silver design. A device reporting `r13p14` lands exactly on the
`0xd, 0xe` tuple the kernel special-cases for that core.

If `rXpY` meant anything else — package revision, mask set, foundry stepping —
the coincidence would be unexplained. Two decimal numbers `13`/`14` decoding to
the hexadecimal pair `0xd`/`0xe` that the kernel hardcodes for that exact core
family is the encoding being confirmed [F].

Note also that `r13p14` is only expressible in this format because the field is
decimal: variant `13` and revision `14` are single decimal numbers, which is why
a value like `r2p0` cannot be read as hex digits and accidentally match
something.

### 4.3 The decode

`MIDR_CPU_MODEL(imp, part) = (imp << 24) | (0xf << 16) | (part << 4)`
(`cputype.h:43-46`), with the variant in bits 23:20 and the revision in bits
3:0 added on top:

| cluster | part | variant | revision | MIDR |
|---|---|---|---|---|
| Cortex-A78 (`0xD41`) | `0xD41` | `0x1` | `0x1` | **`0x411FD411`** |
| Cortex-A78 r0p0 (for comparison) | `0xD41` | `0x0` | `0x0` | `0x410FD410` |
| Cortex-A55 (`0xD05`) | `0xD05` | `0x2` | `0x0` | **`0x412FD050`** |
| Cortex-A55 r0p0 (for comparison) | `0xD05` | `0x0` | `0x0` | `0x410FD050` |

Both parts are **ARM-implemented** (`imp = 0x41`), not Qualcomm-implemented
(`0x51`). That matches `cputype.h`'s own note that Qualcomm marketing names
sit on stock ARM parts at this tier, and it is the opposite of the MSM8998 case
in `Qualcomm-MSM8998-Snapdragon-835-cpu.md` §4, where Kryo 280 reports
Qualcomm part numbers `0x800`/`0x801`.

So of the four MIDR values in play, **two are wrong for this silicon**: the A78
is `0x411FD411`, not `0x410FD410`; the A55 is `0x412FD050`, not `0x410FD050`
[I]. This is an inference from an observed revision through a proven encoding —
not a disassembly — so it is `[I]`, one class short of `[F]`.

## 5. The slice: 364 rows, one device, and it is the right SoC

Unlike #841, where the slice turned out to be a different SoC entirely, this
slice is correctly labelled. Both halves of that claim were checked.

| measure | value | class |
|---|---|---|
| rows | **364** | [F] |
| distinct files | **364** | [F] |
| total bytes | **784,040,172** | [F] |
| devices | **1** — `Moto_G_5G_2024` | [F] |
| `isa_identified` empty | **364 / 364** | [F] |
| families | 9 — wifi 99, other 74, tz 50, modem 44, adsp 44, gpu 19, bt 14, cdsp 12, boot 8 | [F] |
| `db_type`s | 22 | [F] |

The device row in `device-inventory.csv` carries
`soc_source=builds.csv`, which is the weakest provenance available — the label
is self-reported by the build. It was therefore confirmed externally [F]:

| source | says |
|---|---|
| LineageOS wiki, `devices/fogo/` | `SoC Qualcomm SM4375 Snapdragon 4 Gen 1`, kernel 5.4, model `XT2417-1` |
| `/e/OS` docs, `devices/fogo` | `SoC Qualcomm SM4375 Snapdragon 4 Gen 1` |
| `deviceinfohw` 108157 | `CPU sm4375`, `FAMILY Cortex-A78 Cortex-A55` |
| vendor kernel DT | `blair.dtsi`, `msm-id` includes `578` = `BLAIR-LITE` |
| Qualcomm product brief | part number SM4375, 6 nm |

Four independent sources plus the vendor kernel agree. **No scope inversion
here** [F].

## 6. Erratum 1024718: the scope changed under this SoC's feet

This is the finding #811 did not have, and it is the one with a behavioural
consequence rather than a descriptive one.

### 6.1 What the erratum does

`arch/arm64/Kconfig`, `ARM64_ERRATUM_1024718` [F]:

> This option adds a workaround for ARM Cortex-A55 Erratum 1024718.
> Affected Cortex-A55 cores (…) could cause incorrect update of the hardware
> dirty bit when the DBM/AP bits are updated without a break-before-make. The
> workaround is to disable the usage of hardware DBM locally on the affected
> cores.

Hardware dirty-bit management is a page-table optimisation: without it, every
write to a clean page takes a fault. Disabling it is a real, measurable
performance cost on the affected cluster, not a no-op.

### 6.2 The scope was widened in 2021

The device ships **Linux 5.4** (`5.4.274-moto-...`). In vanilla 5.4 the range is
restricted:

```
arch/arm64/kernel/cpufeature.c (v5.4)
:1101   MIDR_RANGE(MIDR_CORTEX_A55, 0, 0, 1, 0),  // A55 r0p0 -r1p0
```

`MIDR_CPU_VAR_REV(v, r) = (v << 4) | r` (`cputype.h:48`), so that range is
`rv` in `[0x00, 0x10]`. An A55 at **r2p0** has `rv = 0x20`, which is **outside**
the range — vanilla 5.4 would leave hardware DBM enabled on this silicon.

Upstream fixed that:

```
commit c0b15c25d25171db4b70cc0b7dbc1130ee94017d   (2021-02-03)
arm64: Extend workaround for erratum 1024718 to all versions of Cortex-A55

  The erratum 1024718 affects Cortex-A55 r0p0 to r2p0. However we apply
  the work around for r0p0 - r1p0. … Thus extend the work around for all
  versions of A55, to cover for r2p0 and any future revisions.
```

That commit states the affected range explicitly as **r0p0 to r2p0** — and this
device's little cluster is r2p0, the last revision in the documented range [F].

The backport landed in the 5.4 stable line at **5.4.102**:

| tag | `cpu_has_broken_dbm` range |
|---|---|
| `v5.4.100` | `MIDR_RANGE(MIDR_CORTEX_A55, 0, 0, 1, 0)` |
| `v5.4.101` | `MIDR_RANGE(MIDR_CORTEX_A55, 0, 0, 1, 0)` |
| `v5.4.102` | `MIDR_ALL_VERSIONS(MIDR_CORTEX_A55)` |
| `v5.4.103`–`v5.4.270` | `MIDR_ALL_VERSIONS(MIDR_CORTEX_A55)` |

The device runs `5.4.274`, so it is **past** the backport and its little cluster
**does** lose hardware DBM [I] — provided the vendor tree kept the upstream
line, which §6.3 checks.

#811's version of this fact was the mainline-master text ("all revisions") with
no revision data to connect it to this part. The revision data is what makes it
apply, and the backport boundary is what makes the device's own kernel version
load-bearing.

### 6.3 The vendor tree agrees

```
drivers/soc/qcom/socinfo.c — not relevant; the check is cpufeature.c
android_kernel_motorola_sm6375 (lineage-22.2), arch/arm64/kernel/cpufeature.c
:1163    MIDR_ALL_VERSIONS(MIDR_CORTEX_A55),
```

The Motorola/LineageOS 5.4.300 tree carries `MIDR_ALL_VERSIONS`, not the
`MIDR_RANGE` of vanilla early-5.4 — i.e. it took the backport [F]. So the
workaround is active on this device on both the shipping kernel and any
LineageOS build [I].

### 6.4 The big cluster: no errata at all in 5.4

Counts below are `CORTEX_A78` substring occurrences, so they include the
`A78AE` and `A78C` variants:

| file | v5.4 | vendor 5.4.300 | mainline master |
|---|---|---|---|
| `arch/arm64/kernel/cpufeature.c` | **0** | **0** | **0** |
| `arch/arm64/kernel/cpu_errata.c` | **0** | **4** | **5** |
| `arch/arm64/include/asm/cputype.h` | **0** | **6** | **10** |

`MIDR_CORTEX_A78` does not exist in vanilla 5.4's `cputype.h` at all — the
constant was added later (0 occurrences at `v5.5`, `v5.6`, `v5.7`, `v5.8` and
`v5.15`; 9 by `v6.1`). The vendor tree backported the part-number defines for `A78` and
`A78C`, and two errata blocks in `cpu_errata.c` that reference them: the SSBS
self-synchronising workaround (`CONFIG_ARM64_ERRATUM_3194386`) and the
Spectre-BHB K=32 loop bound [F].

The consequence is scope-specific and worth stating plainly: on **the shipping
kernel**, the big cluster gets no errata workarounds from `cpu_errata.c`
beyond those two backports, and `cpufeature.c` has literally no A78 path [F].
Whether that is a gap or simply reflects A78 having few applicable errata at
this level is `[OPEN]`; this note does not claim a vulnerability.

## 7. What this changes about #811's sibling-DT analysis

#811 §1.3 built its prediction on two mainline SoCs, `sm6375.dtsi` and
`sm4450.dtsi`, and concluded the answer was `[H]`. With the vendor DT available,
the answer is not a guess.

### 7.1 The prediction that was right

#811 §1.3: *"the `sm4450` style — `arm,cortex-a78` / `arm,cortex-a55` — is the
better-motivated of the two."*

`sm4450.dtsi` (measured, master) [F]:

| property | value |
|---|---|
| `compatible` | `arm,cortex-a55` ×6, `arm,cortex-a78` ×2 |
| `cpu-map` clusters | **1**, containing all 8 |
| `capacity-dmips-mhz` | absent |
| `freq-domain` | `0` ×6, `1` ×2 |

Actual `blair.dtsi` for SM4375 [F]:

| property | value |
|---|---|
| `compatible` | `qcom,kryo` ×8 |
| `cpu-map` clusters | **2** — 6 + 2 |
| `capacity-dmips-mhz` | **1024 / 1946** |
| `freq-domain` | `<&cpufreq_hw 0 6>` ×6, `1 2` ×2 |

The structural split (`freq-domain` 6/2) matches `sm4450`. The naming does
not — SM4375 is *less* honest than either sibling, using one `qcom,kryo` string
for both clusters. So the "better-motivated" guess was half right: right about
the 6/2 domain split, wrong about `compatible` [F].

### 7.2 A correction to #811's `sm6375` row

#811 §1.3's table records `sm6375` as having **2** `cpu-map` clusters:

> | `sm6375` | 8 | `qcom,kryo660` ×8 | **2** (`cluster0`, `cluster1`) | **none** |

Measured against current master, that is not what the file says [F]:

```
arch/arm64/boot/dts/qcom/sm6375.dtsi
  cpu-map at :214   one child, cluster0
  cluster0 cores    cpu0..cpu7   (8 cores)
```

The only `cluster1` tokens in the file are `cluster1-thermal` and its trip
points (`:2042`, `:2046`, `:2052`, `:2058`) — thermal zones, not `cpu-map`
children. The file has **1** `cpu-map` cluster holding all 8 cores, the same
shape as `sm4450`.

This is stable across every tag that has the file: `cluster0`-only and 8 cores
at `v6.2`, `v6.3`, `v6.4`, `v6.5`, `v6.6`, `v6.7`, `v6.8`, `v6.9`, `v6.10`,
`v6.11`, `v6.12`, `v6.13` and master (`v6.0`/`v6.1` do not have the file) [F].
So this is not a recent regression — #811's row was wrong when written.

The correction is applied in place in that note's §1.3 table (§10, Rule 1).

### 7.3 The codename `holi` is not this SoC's

GATE 0 for this issue floated `holi` as the platform. That was wrong, and the
mechanism of the error is worth recording, because it will recur: `holi` is a
real Qualcomm codename, it appears in this device's build config filename, and
it is the SM4350/SM480 platform — a *different, adjacent* part whose Device Info
HW page is titled `Holi for arm64` and reports `CPU sm4350`.

| codename | SoC | evidence |
|---|---|---|
| `holi` | SM4350 / SM480 | vendor `socinfo.c:782` `{ 454, "HOLI" }`; `deviceinfohw` 116843 `CPU sm4350` |
| `blair` | SM6375 | vendor `socinfo.c:783` `{ 507, "BLAIR" }`; `blair.dtsi` `msm-id` 507 |
| `blair-lite` | **SM4375** | vendor `socinfo.c:784` `{ 578, "BLAIR-LITE" }`; `blair.dtsi` `msm-id` 578 |

So SM4375 is a **`blair` derivative**, cut down from SM6375 — not an SM4350
derivative [I]. That has a practical consequence for anyone porting: the
nearest mainline base is `sm6375.dtsi`, not `sm4350`-anything, and `sm6375.dtsi`
already exists in mainline with a working `cpu-map` and `cpufreq-hw` node [F].

## 8. What a `Hardware:` string is worth

The build for this device carries `holi` in a config path, and the audio mixer
name on the real unit is `holifogo5gnasnd`. Both contain `holi`. Neither is a
SoC ID.

This matters because the most-cited tool for Qualcomm SoC naming,
`Dr-Noob/cpufetch`, keys on exactly that string:

```c
src/arm/soc.c:637
  SOC_EQ(tmp, "SM4375", "4 Gen 1", SOC_SNAPD_SM4375, soc, 6)
```

`SOC_EQ` compares against `tmp`, which is the `Hardware:` field [F]. So
`cpufetch` will correctly name this SoC **only if** the device's `Hardware:`
line reads `SM4375`. On a device whose `Hardware:` line reads `holi` — which is
what a `blair`-family build can plausibly emit — `cpufetch` names nothing, or
names the wrong part. The tool is a string matcher, not a MIDR decoder.

That is the honest reason this note does not cite any `Hardware:` value as
identity evidence. Identity comes from `blair.dtsi` (`msm-id` 578), from the
`CPU sm4375` line on the Device Info HW page, and from four independent
specification sources [F].

## 9. Correction of record: this note's own GATE 0

GATE 0 for #847 asserted three things that the subsequent work changed. They are
recorded here rather than silently dropped, because the difference between them
is the substance of the note.

| GATE 0 said | status | what the evidence showed |
|---|---|---|
| platform is `holi`, "same BSP family as SM4350" | **wrong** | `blair.dtsi` + `socinfo.c:784` `{ 578, "BLAIR-LITE" }`. `holi` = SM4350. §2, §7.3 |
| erratum 1024718 "affects all A55 revisions, so the whole little cluster runs with hardware DBM disabled" | **right conclusion, wrong reason** | The scope at mainline master is all revisions, but the *device's* 5.4 kernel needed the 5.4.102 backport to get there, and the documented affected range is r0p0–r2p0. §6 |
| the delta is `[N]` → `[I]` on MIDRs from "observed revision" | **held** | §4.2 proves the encoding; §4.3 gives the values |

The `holi` error is the interesting one. It came from a real observation — the
string exists on the device — and from a real Qualcomm table, just the wrong
row of it. That is the failure mode this repository's `[H]` class exists for.

## 10. Rule 1 pass

Two in-place edits to another note, plus one to the repo map. All in this
session, all listed before → after.

| file | before | after |
|---|---|---|
| `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-soc.md` §1.3 code block | `cpu-map  cluster0 { core0..core5 }  cluster1 { core6, core7 }` | `cpu-map  cluster0 { core0..core7 }` (one cluster, all eight) |
| `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-soc.md` §1.3 prose + table | `sm6375` `cpu-map` clusters **2**; "the 6+2 split **three ways**"; "disagree with each other on *both*" | clusters **1** (8 cores); "**two ways**"; "agree on cluster count and disagree on `compatible` style"; correction note added pointing at §7.2 here |
| `docs/REPO-STATE-MAP.md` CPU/SoC core-ID row | `5 per-SoC CPU core-ID sections`; SM4375 described as "MIDRs … are `cputype.h` arithmetic and instruction-level proof is recorded as absent"; `22 SoCs remain` | `6 per-SoC CPU core-ID sections`; SM4375 now also carries the vendor `blair` DT geometry, the r1p1/r2p0 MIDRs `0x411FD411`/`0x412FD050`, and the erratum-1024718 backport boundary; `21 SoCs remain` |

`research/CORRECTIONS.md` gains no row: the `sm6375` cluster count was never a
claim published outside the repository, and Rule 1's correction log is for
claims that other documents cite. All three edits above are self-contained.

## 11. Honest negatives

- **No MIDR observation exists for this device.** No public `/proc/cpuinfo`
  from any `fogo` unit was found; GitHub code search for `"CPU part" blair`,
  `fogo cpuinfo`, and `"b.Part" "0xd05" 0xd41` returned 0 hits each. The MIDRs
  in §4.3 are `[I]`, derived from an observed revision. `[N]`
- **The corpus still cannot prove the ISA.** `isa_identified` is empty on
  **364 of 364** rows; there is no payload here to disassemble. #811's `[N]`
  stands unchanged. `[N]`
- **`sm4450.dtsi` was not re-derived for `capacity-dmips-mhz` beyond the
  negative** — it is absent there and present in `blair.dtsi`, and this note
  does not explain why. `[OPEN]`
- **The two A78 backports in the vendor tree were counted, not analysed.** This
  note does not assert which erratum IDs the device is exposed to on the big
  cluster. `[OPEN]`
- **`qcom,msm-id` 578 is not in mainline.** `qcom,ids.h` has 308 defines and no
  `QCOM_ID` for 578, 507-adjacent device IDs, or SM4375; `socinfo.c` has no
  SM4375 entry. So a bootloader passing 578 gets a raw number from a mainline
  kernel, not a name. `[N]`
- **`holi` appears in this device's build tree and is not this SoC.** The
  filename `moto-holi-fogo.config` is inherited from `sm6375-common` and is
  misleading; this note does not explain why that tree uses it. `[OPEN]`

## 12. Reproduce

Every command below was run on 2026-11-24 and exits 0.

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm SM4375 Snapdragon 4 Gen 1']
print('rows',len(s),'files',len({r['filename'] for r in s}),'bytes',sum(int(r['size_bytes']) for r in s))
print('devices',dict(Counter(r['device'] for r in s)))
print('families',len({r['blob_family'] for r in s}),'db_types',len({r['db_type'] for r in s}))
print('isa_identified empty',sum(1 for r in s if not r['isa_identified'].strip()))
print('top families',Counter(r['blob_family'] for r in s).most_common(9))"
```

```bash
python3 -I -c "
def midr(imp,var,part,rev): return (imp<<24)|(var<<20)|(0xf<<16)|(part<<4)|rev
print('A78 r0p0 0x%08X'%midr(0x41,0,0xD41,0))
print('A78 r1p1 0x%08X'%midr(0x41,1,0xD41,1))
print('A55 r0p0 0x%08X'%midr(0x41,0,0xD05,0))
print('A55 r2p0 0x%08X'%midr(0x41,2,0xD05,0))"
```

```bash
python3 -I -c "
print('deviceinfohw field order is big-first; SM4350 proves the encoding')
print('r13p14 -> variant',13,'=0x%x'%13,'revision',14,'=0x%x'%14)
print('cpufeature.c MIDR_REV(MIDR_QCOM_KRYO_4XX_SILVER, 0xd, 0xe)')
print('match',(13,14)==(0xd,0xe))"
```

```bash
python3 -I -c "
def vr(v,r): return (v<<4)|r
lo,hi=vr(0,0),vr(1,0)
print('v5.4.101 range MIDR_RANGE(A55,0,0,1,0) -> rv',lo,'..',hi)
for lbl,v,r in (('r0p0',0,0),('r1p0',1,0),('r2p0',2,0),('r2p1',2,1)):
    rv=vr(v,r); print(' A55',lbl,'rv',rv,'in range?',lo<=rv<=hi)
print('MIDR_ALL_VERSIONS range -> rv 0..255, always true')"
```

```bash
python3 -I -c "
import re,urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(u,timeout=60).read().decode()
        except Exception as e:
            if i==n-1: raise
            time.sleep(8*(i+1))
B='https://raw.githubusercontent.com/LineageOS/android_kernel_motorola_sm6375/lineage-22.2/arch/arm64/boot/dts/vendor/qcom/'
bl=get(B+'blair.dtsi')
print('== blair.dtsi',len(bl.encode()),'B')
print('compatibles',sorted(set(re.findall(r'compatible = \"(qcom,kryo[0-9]*)\"',bl))))
print('cpu nodes',len(re.findall(r'CPU[0-9]: cpu@[0-9a-f]+',bl)))
print('capacity',re.findall(r'capacity-dmips-mhz = <([0-9]+)>',bl))
print('freq-domain',re.findall(r'qcom,freq-domain = <&cpufreq_hw ([0-9]+) ([0-9]+)>',bl))
print('clusters',re.findall(r'\n\t\t\t(cluster\d) \{',bl))
print('msm-id',re.findall(r'qcom,msm-id = <[^>]+>(?:, <[^>]+>)*',bl))
print('l2',bl.count('cache-level = <2>'),'l3',bl.count('cache-level = <3>'))
print('dwcells',re.findall(r'#freq-domain-cells = <(\d+)>',bl))
"
```

```bash
python3 -I -c "
import re,urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(u,timeout=60).read().decode()
        except Exception as e:
            if i==n-1: raise
            time.sleep(8*(i+1))
B='https://raw.githubusercontent.com/torvalds/linux/master/'
s=get(B+'arch/arm64/boot/dts/qcom/sm6375.dtsi')
i=s.find('cpu-map {')
start=s.find('{',i); d=0
for k in range(start,len(s)):
    if s[k]=='{': d+=1
    elif s[k]=='}':
        d-=1
        if d==0: end=k+1; break
blk=s[i:end]
print('mainline sm6375 cpu-map line',s[:i].count(chr(10))+1)
print('top-level children',re.findall(r'\n\t\t\t(\w+) \{',blk))
print('cores',len(re.findall(r'cpu = <&',blk)))
print('cluster1 tokens in file',[n for n,l in enumerate(s.split(chr(10)),1) if 'cluster1' in l])
m=get(B+'arch/arm64/boot/dts/qcom/sm4450.dtsi')
print('sm4450 compatibles',sorted(set(re.findall(r'compatible = \"(arm,cortex-a\d+)\"',m))))
print('sm4450 capacity',re.findall(r'capacity-dmips-mhz = <([0-9]+)>',m))
"
```

```bash
python3 -I -c "
import re,urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(u,timeout=60).read().decode()
        except Exception as e:
            if i==n-1: raise
            time.sleep(8*(i+1))
V='https://raw.githubusercontent.com/LineageOS/android_kernel_motorola_sm6375/lineage-22.2/'
si=get(V+'drivers/soc/qcom/socinfo.c')
for k in ('HOLI','BLAIR','BLAIR-LITE'):
    print(k,[l.strip() for l in si.split(chr(10)) if '\"'+k+'\"' in l][:1])
ct=get(V+'arch/arm64/include/asm/cputype.h')
print('vendor A78 part',re.findall(r'ARM_CPU_PART_CORTEX_A78\s+(0x[0-9A-Fa-f]+)',ct))
cf=get(V+'arch/arm64/kernel/cpufeature.c')
i=cf.find('cpu_has_broken_dbm')
print('vendor dbm range',[l.strip() for l in cf[i:i+400].split(chr(10)) if 'MIDR' in l])
"
```

```bash
python3 -I -c "
import re,urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(u,timeout=60).read().decode()
        except Exception as e:
            if i==n-1: raise
            time.sleep(8*(i+1))
B='https://raw.githubusercontent.com/torvalds/linux/'
for tag in ('v5.4','v5.4.100','v5.4.101','v5.4.102'):
    u=B+('' if tag=='v5.4' else '')+tag+'/arch/arm64/kernel/cpufeature.c'
    try:
        t=urllib.request.urlopen(u,timeout=60).read().decode()
    except Exception:
        t=get('https://raw.githubusercontent.com/gregkh/linux/'+tag+'/arch/arm64/kernel/cpufeature.c')
    i=t.find('cpu_has_broken_dbm')
    print(tag,[l.strip() for l in t[i:i+400].split(chr(10)) if 'MIDR' in l])
"
```

```bash
python3 -I -c "
import urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(u,timeout=60).read().decode()
        except Exception as e:
            if i==n-1: raise
            time.sleep(8*(i+1))
for tag,base in (('v5.4','https://raw.githubusercontent.com/torvalds/linux/'),
                 ('v6.1','https://raw.githubusercontent.com/torvalds/linux/'),
                 ('master','https://raw.githubusercontent.com/torvalds/linux/')):
    p='arch/arm64/include/asm/cputype.h'
    t=get(base+tag+'/'+p)
    print(tag,'CORTEX_A78 count',t.count('CORTEX_A78'))
i=get('https://raw.githubusercontent.com/torvalds/linux/v5.4/arch/arm64/kernel/cpu_errata.c')
print('v5.4 cpu_errata A78 count',i.count('CORTEX_A78'))
"
```

```bash
python3 -I -c "
import re,urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(u,timeout=60).read().decode()
        except Exception as e:
            if i==n-1: raise
            time.sleep(8*(i+1))
q=get('https://raw.githubusercontent.com/torvalds/linux/master/include/dt-bindings/arm/qcom,ids.h')
d={int(v):n for n,v in re.findall(r'#define\s+QCOM_ID_(\w+)\s+(\d+)',q)}
print('defines',len(d))
for k in (454,472,507,568,578):
    print(' id',k,d.get(k,'ABSENT'))
print('SM4375 present',any(v=='SM4375' for v in d.values()))
"
```

## Sources

| claim | source | access |
|---|---|---|
| 364 rows / 364 files / 784,040,172 B / 1 device / 22 `db_type`s / 9 families; `isa_identified` empty 364/364; families wifi 99, other 74, tz 50, modem 44, adsp 44, gpu 19, bt 14, cdsp 12, boot 8 | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-24 |
| `Moto_G_5G_2024` = build codename `fogo`, `soc_source=builds.csv` | `upstream-contribution/blob-database/device-inventory.csv` | 2026-11-24 |
| `CPU sm4375`, `CORES 8`, `FAMILY Cortex-A78 Cortex-A55`, `CLUSTERS 2 x 2.02 GHz 6 x 1.80 GHz`, `REVISION r1p1 r2p0`, `TECHPROCESS 6 nm`, kernel `5.4.274-moto-00507-gecc19605af65`, `GPU_MODEL Adreno (TM) 619` | `deviceinfohw.ru` item 108157 | 2026-11-24 |
| SM4350 `REVISION r8p14 r13p14`, `FAMILY Kryo-4xx-a76 Kryo-4xx-a55`, `CPU sm4350`, `SOC Snapdragon 480 Plus` | `deviceinfohw.ru` item 116843 | 2026-11-24 |
| `SoC Qualcomm SM4375 Snapdragon 4 Gen 1`, kernel 5.4, `XT2417-1` | `wiki.lineageos.org/devices/fogo/` | 2026-11-24 |
| `SoC Qualcomm SM4375 Snapdragon 4 Gen 1`, `Octa-core Kryo 2 x 2.0 GHz + 6 x 1.8 GHz`, Adreno 619 | `doc.e.foundation/devices/fogo` | 2026-11-24 |
| `fogo` inherits `sm6375-common`; `TARGET_KERNEL_CONFIG += vendor/ext_config/moto-holi-fogo.config` | `LineageOS/android_device_motorola_fogo` `BoardConfig.mk:9,25` | 2026-11-24 |
| `TARGET_BOARD_PLATFORM := holi`, `TARGET_ARCH_VARIANT := armv8-2a-dotprod`, `holi-qgki_defconfig` | `LineageOS/android_device_motorola_sm6375-common` `BoardConfigCommon.mk:50,54` | 2026-11-24 |
| `blair-moto-fogo-base.dts` includes `blair.dtsi`; `model = "Qualcomm Technologies, Inc. Blair "`; `qcom,msm-id = <507 0x10000>, <578 0x10000>` | `android_kernel_motorola_sm6375` (lineage-22.2) `arch/arm64/boot/dts/vendor/qcom/` | 2026-11-24 |
| `blair.dtsi` 94,327 B; 8 CPU nodes all `qcom,kryo`; 2 `cpu-map` clusters 6+2; capacities 1024×6/1946×2; `freq-domain` `0 6`×6 / `1 2`×2; `#freq-domain-cells = <2>`; 8 L2 / 1 L3; `cpufreq_hw` at `:1279` with two 0x1000 windows and `lut-max-entries = 12` | `blair.dtsi`, same tree | 2026-11-24 |
| `{ 454, "HOLI" }`, `{ 507, "BLAIR" }`, `{ 578, "BLAIR-LITE" }`, `{ 565, "BLAIRP" }` — same block in `android_kernel_oneplus_sm8350` and `android_kernel_samsung_sm7325` | `drivers/soc/qcom/socinfo.c` (vendor, `:782-787`) | 2026-11-24 |
| `ARM_CPU_IMP_ARM` 0x41, `ARM_CPU_PART_CORTEX_A55` 0xD05, `ARM_CPU_PART_CORTEX_A78` 0xD41, `MIDR_CPU_MODEL` `:43`, `MIDR_CPU_VAR_REV` `:48`, `MIDR_REV` `:331`, `MIDR_ALL_VERSIONS` `:332`, `midr_is_cpu_model_range` `:334` | `arch/arm64/include/asm/cputype.h`, master | 2026-11-24 |
| `MIDR_QCOM_KRYO_4XX_SILVER` at `cpufeature.c:1871` with `MIDR_REV(..., 0xd, 0xe)`; `MIDR_CORTEX_A55` at `:1695` (KPTI-safe) and `:1869` (broken DBM) | `arch/arm64/kernel/cpufeature.c`, master | 2026-11-24 |
| erratum 1024718 help text "all revisions", `default y`; commit `c0b15c25d251` text "affects Cortex-A55 r0p0 to r2p0" | `arch/arm64/Kconfig`, master; `torvalds/linux` commit `c0b15c25d25171db4b70cc0b7dbc1130ee94017d` (2021-02-03) | 2026-11-24 |
| v5.4 `MIDR_RANGE(MIDR_CORTEX_A55, 0, 0, 1, 0)` at `cpufeature.c:1101`; `MIDR_ALL_VERSIONS` from `v5.4.102` onward; 0 `CORTEX_A78` in v5.4 `cputype.h`, `cpufeature.c`, `cpu_errata.c` | `torvalds/linux` `v5.4`; `gregkh/linux` `v5.4.100`–`v5.4.270` | 2026-11-24 |
| vendor 5.4.300 tree: `MIDR_ALL_VERSIONS(MIDR_CORTEX_A55)` at `cpufeature.c:1163`; `ARM_CPU_PART_CORTEX_A78` present at `cputype.h:79`; 4 `A78` matches in `cpu_errata.c` (SSBS `3194386`, Spectre-BHB K=32) | `android_kernel_motorola_sm6375` lineage-22.2, `Makefile` `SUBLEVEL = 300` | 2026-11-24 |
| mainline `sm6375.dtsi`: one `cpu-map` cluster at `:214`, 8 cores; `cluster1*` tokens only at `:2042`–`:2058` (thermal). Same shape at `v6.2`–`v6.13`; file absent at `v6.0`/`v6.1` | `arch/arm64/boot/dts/qcom/sm6375.dtsi` | 2026-11-24 |
| `sm4450.dtsi`: `arm,cortex-a55` ×6 + `arm,cortex-a78` ×2, one `cpu-map` cluster of 8, no `capacity-dmips-mhz`, `freq-domain` 0×6/1×2 | `arch/arm64/boot/dts/qcom/sm4450.dtsi`, master | 2026-11-24 |
| `qcom,ids.h` 308 defines; no `QCOM_ID` for 578, 507-adjacent device IDs, SM4375 or SM4350; `socinfo.c` 0 SM4375 entries | `include/dt-bindings/arm/qcom,ids.h` and `drivers/soc/qcom/socinfo.c`, master | 2026-11-24 |
| `cpufetch` `SOC_EQ(tmp, "SM4375", "4 Gen 1", SOC_SNAPD_SM4375, soc, 6)` — matches the `Hardware` string, not MIDRs | `Dr-Noob/cpufetch` `src/arm/soc.c:637`, master | 2026-11-24 |
| no SM4375 DTS in mainline; 664 files in `arch/arm64/boot/dts/qcom/`, 0 `sm4375*`, 0 `holi*` | GitHub contents API, `torvalds/linux` master | 2026-11-24 |
