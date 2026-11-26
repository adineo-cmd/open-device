# Qualcomm SM7325 Snapdragon 778G 5G — CPU: the vendor device tree #811 did not have, and two claims it got wrong

Issue #853. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative / [OPEN] unresolved. Every number is command output from a run on
**2026-11-26** against
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows),
`device-inventory.csv`, `torvalds/linux` master, the public Motorola vendor
kernel tree `android_kernel_motorola_sm7325` (lineage-22.2, `Makefile`
`SUBLEVEL = 302`), the mainline DT binding `cpufreq-qcom-hw.yaml`, and the
`deviceinfohw.ru` capture database.

**No payload exists in this workspace and none was read.** Every statement below
is matrix metadata — filename, size, `db_type`, family label — public GPL source,
or a published device capture. No vendor ELF is parsed here and no instruction is
disassembled [N].

This is the **CPU** note. The SoC package, GPU, DSP, boot chain and TrustZone
census for SM7325 are owned by
`research/soc/Qualcomm-SM7325-Snapdragon-778G-soc.md` (#811) and the GPU by
`research/soc/Qualcomm-SM7325-Snapdragon-778G-5G-gpu.md` (#2030); both are
**cited, never re-derived**. §3 and §4 record the two facts in #811 this note
contradicts. §2.2 records a correction to my own #847 note.

## 0. Verdict

| question | answer | class |
|---|---|---|
| CPU topology | **1 + 3 + 4** — one prime, three gold, four silver; vendor `cpu-map` clusters `cluster0`×4 / `cluster1`×3 / `cluster2`×1 | [F] |
| Prime core | **ARM Cortex-A78**, not Cortex-X1 — a real `sm7325` capture reports `FAMILY Cortex-A78 Cortex-A78 Cortex-A55` | [F] |
| `compatible` on all eight nodes | **`qcom,kryo`** in the vendor DT; **`qcom,kryo670`** in mainline via the 537 B overlay | [F] |
| `capacity-dmips-mhz` | **1024 (silver ×4) / 1946 (gold ×3) / 1985 (prime ×1)** — identical in vendor and mainline | [F] |
| `freq-domain` | vendor `<&cpufreq_hw 0 4>` / `1 4` / `2 4` with `#freq-domain-cells = <2>`; mainline `0` / `1` / `2` with `<1>` | [F] |
| The second phandle cell | **not a core count.** It is `4` for all three clusters on every 1+3+4 part and `6`/`2` on the 6+2 parts — it is the vendor driver's `max_cores` boost threshold | [F] |
| Vendor `cpu-map` clusters | **3** — `cluster0`=CPU0–3, `cluster1`=CPU4–6, `cluster2`=CPU7. Mainline folds all 8 into **one** `cluster0` | [F] |
| Platform codename | **`yupik`** (MSM-ID 475), `model = "Qualcomm Technologies, Inc. Yupik"`; `qcom,msm-id = <475 0x10000>, <515 0x10000>` | [F] |
| SoC ID | **475** = `QCOM_ID_SM7325` at `qcom,ids.h:239`; vendor `socinfo.c:792` names the same 475 **`YUPIK`** | [F] |
| Prime MIDR (predicted) | **`0x411FD411`** (A78 r1p1) — the same value as the gold cores, so **two** distinct MIDRs on the device, not three | [I] |
| Silver MIDR (predicted) | **`0x412FD050`** (A55 r2p0) | [F] |
| `CORTEX_A78` in the kernel's erratum lists | **present, three times** at master — `cpu_errata.c:402`, `cpu_errata.c:669`, `proton-pack.c:882` | [F] |
| Slice CPU evidence | **none** — 67 rows, 0 CPU-bearing files, `isa_identified` empty 67/67 | [N] |
| Mainline DTS | `kodiak.dtsi` (202,322 B) is the SoC include; `sm7325.dtsi` is a 537 B overlay; 4 real SM7325 boards exist and **neither of this slice's devices is one** | [F] |

The two corrections to #811 are §3 (the Prime is an A78, so its MIDR is
`0x411FD411` and not `0x410fd440`) and §4 (`CORTEX_A78` is *not* absent from the
erratum/mitigation lists). Both are recorded in flight in
`research/CORRECTIONS.md`. The correction to my own note is §2.2.

## 1. Scope: what #811 owns, and the one thing it could not see

#811 §1 established the 1+3+4 topology from public spec, the `kodiak.dtsi`
capacity and `freq-domain` values, the `sm7325.dtsi` overlay and the
`sc7280.dtsi` → `kodiak.dtsi` rename, and §1.5 recorded honestly that
instruction-level proof is not available for this part. §4, §5, §6 and §7 own
boot, TrustZone, the slice census and the container laws. None of that is
rebuilt here.

What #811 could not see is the **vendor device tree**. Its §1.2 opens:

> Unlike SM4375 (#811), which has **no** device tree at all in mainline, SM7325
> is one of the best-described parts in this repo.

The comparison is backwards. SM4375 has a *vendor* DT (`blair.dtsi`) and no
mainline DT; SM7325 has *both* — a mainline DT and a Motorola vendor DT,
`yupik.dtsi`, which is 144,296 B and which #811 never examined. That file is the
subject of §2, and it is what makes §3 decidable.

The vendor tree is
`LineageOS/android_kernel_motorola_sm7325`, branch `lineage-22.2`, which both
slice devices build from (§7). Its `arch/arm64/boot/dts/vendor/qcom/` holds 998
files, of which 139 match `yupik` and 15 match `berlin` (`yupik-berlin-*`
overlays, §7.2).

## 2. The vendor device tree exists: `yupik.dtsi` and three `cpu-map` clusters

### 2.1 Geometry

`yupik.dtsi`, 144,296 B, `model = "Qualcomm Technologies, Inc. Yupik"` at `:29`
and `qcom,msm-id = <475 0x10000>, <515 0x10000>` at `:31` [F]. The `cpu-map`
node is at `:211` and has **three** children [F]:

```
yupik.dtsi:211    cpu-map {
yupik.dtsi:212      cluster0 {   core0..core3  -> CPU0..CPU3    (4 cores)
yupik.dtsi:230      cluster1 {   core0..core2  -> CPU4..CPU6    (3 cores)
yupik.dtsi:244      cluster2 {   core0        -> CPU7           (1 core)
```

Per-core values, all eight nodes measured [F]:

| node | `reg` | `capacity-dmips-mhz` | `dynamic-power-coefficient` | `freq-domain` | `cpu-idle-states` |
|---|---|---|---:|---|---|
| `CPU0` `:62` | `0x0` | 1024 | 100 | `<&cpufreq_hw 0 4>` | `&SLVR_OFF &SLVR_RAIL_OFF` |
| `CPU1` `:85` | `0x100` | 1024 | 100 | `<&cpufreq_hw 0 4>` | `&SLVR_OFF &SLVR_RAIL_OFF` |
| `CPU2` `:103` | `0x200` | 1024 | 100 | `<&cpufreq_hw 0 4>` | `&SLVR_OFF &SLVR_RAIL_OFF` |
| `CPU3` `:121` | `0x300` | 1024 | 100 | `<&cpufreq_hw 0 4>` | `&SLVR_OFF &SLVR_RAIL_OFF` |
| `CPU4` `:139` | `0x400` | **1946** | **520** | `<&cpufreq_hw 1 4>` | `&GOLD_OFF &GOLD_RAIL_OFF` |
| `CPU5` `:157` | `0x500` | 1946 | 520 | `<&cpufreq_hw 1 4>` | `&GOLD_OFF &GOLD_RAIL_OFF` |
| `CPU6` `:175` | `0x600` | 1946 | 520 | `<&cpufreq_hw 1 4>` | `&GOLD_OFF &GOLD_RAIL_OFF` |
| `CPU7` `:193` | `0x700` | **1985** | **552** | `<&cpufreq_hw 2 4>` | `&GOLD_OFF &GOLD_RAIL_OFF` |

Three capacities, three power coefficients, three domain indices, three
`cpu-map` clusters — **4 + 3 + 1** [F].

Mainline `kodiak.dtsi` (202,322 B) carries the **same** capacity and power
coefficient vectors and the same three domain indices, but folds the map [F]:

| property | vendor `yupik.dtsi` | mainline `kodiak.dtsi` |
|---|---|---|
| `cpu-map` clusters | **3** — 4 / 3 / 1 | **1** — `cluster0` with 8 `coreN` at `:404` |
| `cpu-map` core labels | `core0`–`core3`, then `core0`–`core2`, then `core0` | `core0`–`core7` |
| `capacity-dmips-mhz` | 1024×4 / 1946×3 / 1985×1 | **identical** |
| `dynamic-power-coefficient` | 100×4 / 520×3 / 552×1 | **identical** |
| `freq-domain` indices | `0`×4 / `1`×3 / `2`×1 | **identical** |
| `#freq-domain-cells` | **`<2>`** at `:2700` | **`<1>`** at `:7130` |
| CPU node labels | `CPU0`–`CPU7` (upper case) | `cpu0`–`cpu7` (lower case) |
| `compatible` | `qcom,kryo` ×8 | `qcom,kryo` ×8 in `kodiak.dtsi`, rebound to `qcom,kryo670` by `sm7325.dtsi` |
| CPU `operating-points-v2` | **absent on all 8** | `cpu0_opp_table` / `cpu4_opp_table` / `cpu7_opp_table` |
| CPU OPP rows | 0 | 11 + 13 + 14 = **38** |

So the 4/3/1 split is **not** invisible in mainline — it is recoverable from
`freq-domain` alone, which is exactly what #811 §1.2 reported. What mainline
cannot show is that the vendor firmware describes the same split as three
`cpu-map` clusters. The two descriptions agree completely on the numbers and
differ only in whether the map is flattened [F].

Two further structural differences are worth naming because they change what
the DVFS path actually is [F]:

- **Vendor has no CPU OPP tables at all.** All eight vendor CPU nodes lack
  `operating-points-v2`; the vendor `yupik.dtsi` defines exactly 3
  `operating-points-v2` nodes (all bandwidth, `:3162`, `:3173`, `:3190`) and
  references them 12 times, never from a CPU node. Frequencies come entirely
  from the EPSS LUT ([F] for the absence, [I] for the consequence).
- **Vendor declares the idle states, mainline declares the power domains.**
  `yupik.dtsi` references `&SLVR_OFF`, `&SLVR_RAIL_OFF`, `&GOLD_OFF`,
  `&GOLD_RAIL_OFF` from all eight CPU nodes but defines **none** of them; they
  live in `yupik-pm.dtsi` at `:91`, `:105`, `:139`, `:153` as
  `qcom,pm-cpu-level@1` (C3) and `@2` (C4). Mainline is the opposite: `kodiak.dtsi`
  defines four `arm,idle-state` nodes at `:443`–`:473` and references them from
  **`cpu_pd0`–`cpu_pd7`** at `:874`–`:919`, never from a CPU node (0
  `cpu-idle-states` properties in the file). Same hardware, two different DT
  idioms [F].

The idle-state grouping is a **fourth** cluster encoding, and it is coarser than
the other three: mainline gives `little_cpu_sleep_*` to `cpu_pd0`–`cpu_pd3` and
`big_cpu_sleep_*` to `cpu_pd4`–`cpu_pd7` — a **4 + 4** split that contradicts
the **4 + 3 + 1** split of `freq-domain` in the same file. The vendor tree agrees
with the vendor `cpu-map` instead: `SLVR_*` for CPU0–CPU3, `GOLD_*` for CPU4–CPU7,
so it is 4 + 4 there too. Neither tree separates the prime core at the idle-state
level [F].

That is the honest reading of §2.1: **the prime core is a distinct DVFS domain
and a distinct `cpu-map` cluster, but not a distinct power/idle domain.** A
consumer that keys on idle states sees 4+4; one that keys on `freq-domain` sees
4+3+1 [F].

### 2.2 The frequency-domain block, and the second cell that is not a core count

This section corrects my own #847 note.

`yupik.dtsi` declares the block at `:2678`:

```
yupik.dtsi:2678  cpufreq_hw: qcom,cpufreq-hw {
yupik.dtsi:2679    compatible = "qcom,cpufreq-hw-epss";
yupik.dtsi:2680    reg = <0x18591000 0x1000>, <0x18592000 0x1000>,
yupik.dtsi:2681          <0x18593000 0x1000>;
yupik.dtsi:2682    reg-names = "freq-domain0", "freq-domain1",
yupik.dtsi:2683                "freq-domain2";
yupik.dtsi:2688    qcom,lut-row-size = <4>;
yupik.dtsi:2689    qcom,no-accumulative-counter;
yupik.dtsi:2700    #freq-domain-cells = <2>;
```

Three 0x1000 windows, three `dcvshN_int` interrupts, `#freq-domain-cells = <2>`
[F]. Each CPU then passes **two** cells — domain index and a second value that
is `4` for all three clusters.

#847 §3.1 read that second cell as a **core count**, and wrote:

> each CPU passes a domain index **and a core count**: `0 6` for the six little
> cores, `1 2` for the two big ones. So the cluster split is encoded **three
> independent ways** — `cpu-map`, `freq-domain` domain index, and
> `freq-domain` core count.

On `blair.dtsi` (6 + 2) that happens to be true. On `yupik.dtsi` it is false,
because all three clusters — 4, 3 and 1 cores — carry `4` [F]:

| platform file | clusters | second cell per domain | second cell == cluster size? |
|---|---|---|---|
| `blair.dtsi` (SM4375) | 6 / 2 | `6`, `2` | **yes** |
| `holi.dtsi` (SM4350) | 6 / 2 | `6`, `2` | **yes** |
| `yupik.dtsi` (SM7325) | 4 / 3 / 1 | `4`, `4`, `4` | **no** |
| `lahaina.dtsi` (SM8350) | 4 / 3 / 1 | `4`, `4`, `4` | **no** |
| `shima.dtsi` (SM74xx) | 4 / 3 / 1 | `4`, `4`, `4` | **no** |

Five vendor platform files, measured [F]. The value tracks the *part*, not the
*cluster*: every 1+3+4 part says `4` three times, every 6+2 part says `6` then
`2`. So "the core count itself is redundant with both" (#847 §3.1) is wrong for
three of the five platforms, and a reader who trusted it would conclude that
`yupik` has a 4-core gold cluster and a 4-core prime cluster.

What the value **is** is visible in the vendor driver. `qcom-cpufreq-hw.c`
(vendor, `lineage-22.2`) reads both cells at `:663-674` and passes the second
one as `max_cores`:

```c
ret = of_parse_phandle_with_args(cpu_np, "qcom,freq-domain",
                                 "#freq-domain-cells", 0, &args);
...
ret = qcom_cpu_resources_init(pdev, cpu, args.args[0],
                              args.args[1]);
```

and `max_cores` is used for exactly one thing — marking boost OPPs (`:473`):

```c
if (core_count != max_cores)
        c->table[i].flags  = CPUFREQ_BOOST_FREQ;
```

where `core_count` is `FIELD_GET(LUT_CORE_COUNT, data)`, `LUT_CORE_COUNT` =
`GENMASK(18, 16)` (`:28`). So `max_cores` is the **boost-detection threshold**
for that domain's LUT, not a cluster size. On `blair` the threshold equals the
cluster size; on `yupik` it does not [F for the driver, I for why Qualcomm chose
`4`].

Mainline does not have this property at all. `drivers/cpufreq/qcom-cpufreq-hw.c`
reads only `args.args[0]` (`:323`, `:558`), never `args[1]`; the binding
`cpufreq-qcom-hw.yaml:95-96` declares `'#freq-domain-cells': const: 1`; and
`kodiak.dtsi:7130` accordingly says `<1>` [F]. The single-cell form is the
upstream contract, and the vendor two-cell form is a downstream extension whose
second cell mainline has no use for.

There is a second trap in the same block. The vendor compatible is
`"qcom,cpufreq-hw-epss"`, which appears **0** times in mainline's match table
(mainline has `qcom,cpufreq-hw`, `qcom,cpufreq-epss`, `qcom,shikra-epss` at
`:440-442`) and **0** times in the binding's compatible enum [F]. Mainline's
`kodiak.dtsi:7116` uses the two-string form
`"qcom,sc7280-cpufreq-epss", "qcom,cpufreq-epss"` instead. A vendor DT dropped
into a mainline tree does not bind [I].

### 2.3 What the vendor DT does not say

- **No core name anywhere.** `cortex-a78`, `cortex-x1`, `cortex-a55`, `kryo670`
  and `kryo6` each appear **0** times in `yupik.dtsi`; all eight nodes say
  `compatible = "qcom,kryo"` [F]. Likewise `kryo670` appears 0 times in
  `kodiak.dtsi` — only the 537 B `sm7325.dtsi` overlay names the generation [F].
- **No `arm,armv8-*` capability node.** `yupik.dtsi` has `arm,armv8-timer` at
  `:727` and `arm,armv8-pmuv3` at `:3003` and nothing that names an ISA version
  [F].
- **No `capacity-dmips-mhz` outside the CPU nodes** and no `clock-frequency`
  property; the only clock source is the LUT [F].

So the vendor DT settles *shape* — 4 + 3 + 1, three domains, three clusters — and
says nothing about *which* ARM core is in each cluster. That question is §3.

## 3. Correction 1: the Prime core is a Cortex-A78, not a Cortex-X1

### 3.1 #811's claim and its source

#811 §1.4 derives all three cluster MIDRs from the NOTES block in
`arch/arm64/include/asm/cputype.h:239-246`, which reads [F]:

```c
/*
 * NOTES:
 * - Qualcomm Kryo 5XX Prime / Gold ID themselves as MIDR_CORTEX_A77
 * - Qualcomm Kryo 5XX Silver IDs itself as MIDR_QCOM_KRYO_4XX_SILVER
 * - Qualcomm Kryo 6XX Prime IDs itself as MIDR_CORTEX_X1
 * - Qualcomm Kryo 6XX Gold IDs itself as ARM_CPU_PART_CORTEX_A78
 * - Qualcomm Kryo 6XX Silver IDs itself as MIDR_CORTEX_A55
 */
```

Applying that to Kryo 670, #811 concluded `0x410fd440` for the prime
(`ARM_CPU_PART_CORTEX_X1` = `0xD44`, `cputype.h:82`) and recorded it in its
verdict table at `:30` and `:192` [F for the arithmetic].

#811 did hedge once, in §1.4: *"this note does not claim the 778G's prime core is
literally an X1 (the 1+3+4 Kryo 670 Prime is a vendor-named core, §1.1)
[OPEN]."* But the hedge is contradicted by the same section's table, which
assigns the prime a concrete X1 MIDR and marks it `[F] for the mapping`.

### 3.2 The counter-evidence, with a control experiment

`deviceinfohw.ru` is an app that dumps `CpuInfo` on a booted device. Its
`FAMILY` field prints one core name per cluster, in cluster order. Two `sm7325`
captures from this slice's own device family report **three tokens for three
clusters, with prime and gold both A78** [F]:

| item | `PRODUCT` | kernel | `CPU` | `FAMILY` | `CLUSTERS` | `REVISION` |
|---|---|---|---|---:|---|---|
| 103878 | `berlna_global` | `5.4.254-moto-g5f3fd71e25f0` | `sm7325` | `Cortex-A78 Cortex-A78 Cortex-A55` | `1 x 2.40 GHz 3 x 2.40 GHz 4 x 1.80 GHz` | `r1p1 r1p1 r2p0` |
| 103829 | `redwood_global` | `5.4.259-qgki-g743eab27f070` | `sm7325` | `Cortex-A78 Cortex-A78 Cortex-A55` | `1 x 2.40 GHz 3 x 2.40 GHz 4 x 1.80 GHz` | `r1p1 r1p1 r2p0` |
| 103714 | `Spacewar` | `5.4.274-qgki-gb9208bd1031f` | `sm7325` | `Cortex-A78 Cortex-A78 Cortex-A55` | `1 x 2.52 GHz 3 x 2.40 GHz 4 x 1.80 GHz` | `r1p1 r1p1 r2p0` |

`berlna` is one of the two devices in this slice (`Edge_2021`); `Spacewar` is
`Phone_1` from the SM7325-AE sibling label. All three agree.

The field is only usable if it can distinguish A78 from X1 at all. It can — this
is the control experiment, run over items 103700–103900 of the same database [F]:

| item | `CPU` | `FAMILY` | domains |
|---|---|---|---|
| 103708 | `sm8350` | `Cortex-X1 Cortex-A78 Cortex-A55` | 3 |
| 103878 | `sm7325` | `Cortex-A78 Cortex-A78 Cortex-A55` | 3 |
| 103883 | `sm6375` | `Cortex-A78 Cortex-A55` | 2 |
| 103786 | `sm4350` | `Kryo-4xx-a76 Kryo-4xx-a55` | 2 |
| 103881 | `sm8650` | `Cortex-X4 Cortex-A720 Cortex-A720 Cortex-A520` | 4 |
| 103880 | `s5e9925` | `Cortex-X2 Cortex-A710 Cortex-A510` | 3 |

`sm8350` (Snapdragon 888) is a genuine X1 part and prints **`Cortex-X1`**;
`sm8650` prints `Cortex-X4`; `s5e9925` prints `Cortex-X2`. So the field reports
X-series cores when they exist. On `sm7325` it does not report one [F].

Cross-check: the same database on a 4-core-X1 part would be a stronger control,
but none is reachable in the scanned range; `sm8350` is the decisive one because
it is the same Kryo 6XX generation and the same 1+3+4 layout, and it differs from
`sm7325` in exactly the prime token [F for the data, I for the generation
argument].

Independent published specs agree, and they are not derived from the same
database [F]:

| source | prime core |
|---|---|
| `en.wikipedia.org/wiki/Kryo`, section *Kryo 670* | `1 Kryo 670 Prime (ARM Cortex-A78 based)` |
| GSMArena, Snapdragon 778G announcement table | `1x Kryo 670 (A78) @ 2.4 GHz` |
| Android Authority, *Kryo CPU numbering* | "The Kryo 670 is a cut-down version of the Kryo 680 and **doesn't feature the Cortex-X1**" |
| NanoReview, SM7325 | `1 core Kryo 670 Prime (Cortex-A78)` |
| devicespecifications, Motorola Edge 30 (SM7325-AE) | `1x 2.52 GHz Cortex-A78, 3x 2.4 GHz Cortex-A78, 4x 1.8 GHz Cortex-A55` |
| CPU-Boss, 778G | `1x Cortex-A78 (Kryo 670 Prime), 3x Cortex-A78 (Kryo 670 Gold)` |

Six independent sources, one answer. The X1 is in Kryo 680 (SM8350) and the
Kryo 670 drops it — which is precisely what the control experiment shows [F].

### 3.3 What `cputype.h`'s NOTES block actually asserts

The block is not wrong; #811's application of it is. It says **Kryo 6XX Prime**
reports `MIDR_CORTEX_X1`. Kryo 6XX is a *family*, and the family contains at
least two members — Kryo 680, which has an X1 prime, and Kryo 670, which does
not. A note keyed on the family cannot settle a member [F for the text, I for
the family membership].

The kernel agrees that the note is a family-level statement, not a per-part
table: `cputype.h` has **no** `QCOM_CPU_PART_KRYO_6XX_*` at all. The
Qualcomm-private part numbers are `KRYO` `0x200`, `KRYO_2XX_GOLD`/`_SILVER`,
`KRYO_3XX_GOLD`/`_SILVER`, `KRYO_4XX_GOLD` `0x804` / `_SILVER` `0x805`, and
`ORYON_X1` — nothing for 5XX-with-A77 or 6XX [F]. So there is no kernel constant
that would let a Kryo 670 core report a Qualcomm part number even if Qualcomm
wanted it to; the cores must present stock ARM MIDRs, and the NOTES block is
saying which stock ARM MIDRs the family uses [F].

### 3.4 The MIDR consequence: two distinct MIDRs, not three

The device reports `r1p1 r1p1 r2p0` — big-cluster-first, as #847 §4.2
established from `sm4350`'s `r8p14 r13p14` → variant `0xd`, revision `0xe`
matching `cpufeature.c:1871`'s `MIDR_REV(MIDR_QCOM_KRYO_4XX_SILVER, 0xd, 0xe)`
[F].

With `MIDR_CPU_MODEL(imp, partnum)` = `(imp << 24) | (0xf << 16) | (partnum << 4)`
and `MIDR_CPU_VAR_REV(var, rev)` = `(var << 20) | rev` (`cputype.h:43-49`) [F]:

```
$ python3 -I -c "
m=lambda imp,pn:(imp<<24)|(0xf<<16)|(pn<<4)
r=lambda b,v,rv:b|(v<<20)|rv
print('A78 r0p0 0x%08X'%r(m(0x41,0xD41),0,0))
print('A78 r1p1 0x%08X'%r(m(0x41,0xD41),1,1))
print('X1  r1p0 0x%08X'%r(m(0x41,0xD44),1,0))
print('A55 r0p0 0x%08X'%r(m(0x41,0xD05),0,0))
print('A55 r2p0 0x%08X'%r(m(0x41,0xD05),2,0))"
A78 r0p0 0x410FD410
A78 r1p1 0x411FD411
X1  r1p0 0x411FD440
A55 r0p0 0x410FD050
A55 r2p0 0x412FD050
```

So the corrected cluster table is [F for the encoding, I for the assignment]:

| cluster | cores | reported `REVISION` | core | MIDR |
|---|---:|---|---|---|
| `cluster0` | 4 | `r2p0` | Cortex-A55 | **`0x412FD050`** |
| `cluster1` | 3 | `r1p1` | Cortex-A78 | **`0x411FD411`** |
| `cluster2` | 1 | `r1p1` | Cortex-A78 | **`0x411FD411`** |

**Two distinct MIDRs on the whole SoC, and CPU0–CPU3 share one of them with
CPU4–CPU6 sharing the other.** The prime and the gold clusters are
*indistinguishable by MIDR*. #811's table implied three distinct values
(`0x412fd050`, `0x410fd410`, `0x410fd440`); the real device can only produce two,
and the gold value is `0x411FD411` rather than `0x410fd410` because the silicon is
r1p1 and not r0p0 [I].

This is the sharpest available test, and it is why the correction matters
beyond bookkeeping: `get_cpu_id()` cannot tell a 778G's prime core from its gold
cores, so any per-cluster policy keyed on MIDR must fall back to
`cpu-map`/`freq-domain`. That is the same conclusion #811 §1.5 reached by a
different road, and the correction strengthens it [I].

## 4. Correction 2: `CORTEX_A78` is in the erratum lists

#811 §1.4 corollary 1 states [F for its own measurement, wrong as a claim]:

> `cpufeature.c` has **zero** occurrences of `CORTEX_A78` (it appears in no
> erratum or mitigation list at all)

The parenthetical is false. The count is real; the inference from it is not,
because `CORTEX_A78` is not confined to `cpufeature.c`. At `torvalds/linux`
master, word-boundary `CORTEX_A78` appears in three places outside it [F]:

| file | line | enclosing config | list |
|---|---:|---|---|
| `arch/arm64/kernel/cpu_errata.c` | `402` | `CONFIG_ARM64_ERRATUM_4118414` | TLBI completion (`ERRATA_MIDR_RANGE_LIST`) |
| `arch/arm64/kernel/cpu_errata.c` | `669` | `CONFIG_ARM64_ERRATUM_3194386` | `erratum_spec_ssbs_list` |
| `arch/arm64/kernel/proton-pack.c` | `882` | — | `spectre_bhb_k32_list` |

Substring counting overstates the other direction — `CORTEX_A78AE` and
`CORTEX_A78C` match too — so the word-boundary count in `cpu_errata.c` is **2**,
and the total across the three files is **3** [F].

The two A78 entries are genuine errata for this silicon, and the Kconfig text
names them [F]:

- `CONFIG_ARM64_ERRATUM_4118414`, *"Completion of affected memory accesses might
  not be guaranteed by completion of a TLBI"*, lists **"ARM Cortex-A78 erratum
  4193791"**. It `select`s `ARM64_WORKAROUND_REPEAT_TLBI_SYNC`.
- `CONFIG_ARM64_ERRATUM_3194386`, *"Cortex-*/Neoverse-*: workaround for MSR SSBS
  not self-synchronizing"*, lists **"ARM Cortex-A78 erratum 3324344"**.

Both are `default y`, so an allmodconfig-style build turns them on [F].

A detail worth recording because it is a free consistency check: A78 and X1 share
an erratum number in both lists — `4193791` in 4118414 and `3324344` in 3194386.
That is the same relationship the MIDR analysis in §3.4 found from the other
direction: the two parts are close enough to share errata and far enough apart to
have different part numbers [F for the numbers, I for the reading].

### 4.1 Why the `cpufeature.c` zero is real

`cpufeature.c` at master has genuinely **0** `CORTEX_A78` (any variant) [F]. The
file holds CPU *capability* tables; the erratum tables live in `cpu_errata.c` and
the Spectre mitigations in `proton-pack.c`. So #811 measured one file and drew a
conclusion about the kernel. The correct statement is: *`CORTEX_A78` is absent
from `cpufeature.c`'s capability and DBM lists, but present in two errata lists
and one mitigation list* [F].

That distinction has a practical edge for this SoC. `cpu_has_broken_dbm` is in
`cpufeature.c` and lists only A55 (`:1869`), so the A78 clusters do not get the
DBM workaround — consistent with #811's other conclusion that the Gold cores need
no workaround *for DBM*. They still take the SSBS and TLBI errata [F].

### 4.2 What the vendor 5.4.302 tree carries

The vendor tree's kernel is `Makefile` `VERSION = 5` / `PATCHLEVEL = 4` /
`SUBLEVEL = 302` [F]. In that tree [F]:

- `cputype.h` defines `ARM_CPU_PART_CORTEX_A78` `0xD41` at `:79`,
  `ARM_CPU_PART_CORTEX_X1` `0xD44` at `:80`, `_A78C` `0xD4B` at `:85`,
  `_X1C` `0xD4C` at `:86`, and has **no** NOTES block (`NOTES` count 0) and no
  `KRYO_6XX` token.
- `cpu_errata.c` has **2** word-boundary `CORTEX_A78`: `:848` inside
  `cpu_enable_ssbd_mitigation` under `CONFIG_ARM64_ERRATUM_3194386`, and `:1180`
  inside `spectre_bhb_loop_affected`'s `spectre_bhb_k32_list`.
- `proton-pack.c` **does not exist** in this tree (404), so the Spectre-BHB
  table lives in `cpu_errata.c` as in mainline pre-5.10 — `v5.10` was the first
  tag with `proton-pack.c`, and it still had 0 `CORTEX_A78` there [F].
- `arch/arm64/Kconfig:622` defines `CONFIG_ARM64_ERRATUM_3194386` with the same
  help text, including "ARM Cortex-A78 erratum 3324344" [F].
- `CONFIG_ARM64_ERRATUM_4118414` is **absent** from that Kconfig, so the TLBI
  workaround is not available on this kernel at all [F].
- `cpufeature.c` has `MIDR_ALL_VERSIONS(MIDR_CORTEX_A55)` at `:1036` in
  `kpti_safe_list` (inside `#ifdef CONFIG_COMPAT`) and at `:1163` in
  `cpu_has_broken_dbm` under `CONFIG_ARM64_ERRATUM_1024718` [F].

So on the kernel these two devices actually run, the A78 clusters take the SSBS
erratum and the Spectre-BHB K=32 mitigation, and do not take the TLBI workaround
[F for the code, I for the consequence]. `lahaina-qgki_defconfig` sets none of
these explicitly, so Kconfig defaults apply — and 3194386 defaults to `y` [F].

## 5. The slice: 67 rows that cannot identify a CPU

The SM7325 slice is small and contains nothing that could carry an instruction
[F]:

| metric | value |
|---|---|
| rows | **67** |
| distinct filenames | **39** |
| total bytes | **346,793,472** = 330.73 MiB |
| devices | **2** — `Edge_20` (`berlin`, 31 rows), `Edge_2021` (`berlna`, 36 rows) |
| families | `other` 29, `adsp` 12, `bt` 8, `gpu` 8, `boot` 6, `wifi` 4 |
| `isa_identified` empty | **67 of 67** |

Filename scan for `cpu` or `cpufreq`: **0 matches** [F]. The only executable-class
rows are four 8 KB `.mdt` GPU/DSP containers (`evass.mdt`, `evass-lt.mdt`,
`vpu20_2v.mdt`, `vpu20_4v.mdt`) and a 64 MiB `dsp.img` partition dump — none is a
CPU artefact, and none is parsed here [F]. Boot is 3 filenames × 2 devices
(`boot.img` 100,663,296 B, `dtbo.img` 25,165,824 B, `vbmeta.img` 8,192 B) =
**72.57% of the slice by bytes**, and `dtbo.img` is a DTB container that could in
principle hold a `cpu-map` — but its 24 MiB is a size class shared by 72 corpus
devices, so nothing about its contents is knowable from metadata [N].

This is the same conclusion #811 §1.5 reached and it is unchanged: **CPU identity
for this SoC comes from DT and published capture, never from this slice's bytes**
[N].

## 6. ISA: `armv8-2a-dotprod`, and two build-system traps

The LineageOS build declares the ISA explicitly [F]:

```
sm7325-common/BoardConfigCommon.mk:10  TARGET_ARCH_VARIANT := armv8-2a-dotprod
sm7325-common/BoardConfigCommon.mk:17  TARGET_2ND_ARCH_VARIANT := armv8-a
sm7325-common/BoardConfigCommon.mk:13  TARGET_CPU_VARIANT := generic
sm7325-common/BoardConfigCommon.mk:14  TARGET_CPU_VARIANT_RUNTIME := kryo385
sm7325-common/BoardConfigCommon.mk:48  TARGET_BOARD_PLATFORM := lahaina
```

`armv8-2a-dotprod` is correct for these cores: A78 and A55 are ARMv8.2-A parts,
and the dot-product extension is the ARMv8.2 addition the build is opting into.
Userspace sees it as `HWCAP_ASIMDDP` (`arch/arm64/include/uapi/asm/hwcap.h:46`,
`1 << 20`), gated in the kernel by `ID_AA64ISAR0_EL1.DP`
(`cpufeature.c:3198`) [F]. So the build target and the silicon agree [F for both
halves, I for the pairing].

Two traps sit beside it [F]:

1. **`TARGET_CPU_VARIANT_RUNTIME := kryo385`.** Kryo 385 is Cortex-A75 + A55, the
   Snapdragon 845 generation. It is a *scheduler tuning* choice — the name tells
   the compiler which latency model to use — and it is two generations older than
   the silicon. A reader who treats this string as an identity claim would
   conclude the SoC is an A75/A55 part. It is not. The same `kryo385` appears in
   `fogo`'s `sm6375-common` (#847 §8), so it is a house habit in these trees, not
   a per-SoC statement [F].
2. **`TARGET_BOARD_PLATFORM := lahaina`.** `lahaina` is SM8350's platform name
   (Snapdragon 888) — see `research/soc/Qualcomm-SM8350-Snapdragon-888-soc.md`
   §1. The vendor kernel tree for SM7325 is Motorola's `lahaina` branch, reused
   across the whole 2021–2022 Qualcomm lineup, so the *kernel* platform name is
   `lahaina` while the *SoC* platform name is `yupik` (§7). Three names for what
   a user would call one device: `lahaina` (kernel branch), `yupik` (SoC DT),
   `kodiak` (mainline SoC include) [F].

Neither trap invalidates the build; both mislead a reader who greps for an
identity.

## 7. Platform identity: `yupik`, not `lahaina`; and an inventory discrepancy

### 7.1 Three IDs, one SoC

`yupik.dtsi:31` declares `qcom,msm-id = <475 0x10000>, <515 0x10000>` [F].
Both numbers resolve, in two different tables [F]:

| ID | mainline `qcom,ids.h` | vendor `socinfo.c` |
|---:|---|---|
| 475 | `QCOM_ID_SM7325` at `:239` | `{ 475, "YUPIK" }` at `:792` |
| 499 | `QCOM_ID_SM7325P` at `:246` | `{ 499, "YUPIKP" }` at `:797` |
| 515 | **absent** | `{ 515, "YUPIK-LTE" }` at `:798` |
| 497 | absent | `{ 497, "YUPIK-IOT" }` at `:795` |
| 498 | absent | `{ 498, "YUPIKP-IOT" }` at `:796` |

So mainline names the SoC and vendor names the platform, for the same number —
exactly the `blair`/`BLAIR` pattern #847 §2 documented. `YUPIK` is to SM7325 what
`BLAIR` is to SM6375, and `lahaina.dtsi` is a *different* SoC (`model =
"Qualcomm Technologies, Inc. Lahaina"`, `qcom,msm-id = <415 0x10000>, <456
0x10000>, <501 0x10000>`, 151,073 B) whose own vendor `cpu-map` also happens to
be 4/3/1 [F].

That last coincidence is the reason §2.2 needed five platforms: `lahaina` and
`yupik` are different SoCs with the same cluster shape, so a single-platform
check cannot tell a per-part constant from a per-cluster one.

### 7.2 The slice's devices, and the mainline boards that are not them

`device-inventory.csv` maps the two slice devices to SoC labels and build
codenames [F]:

| model | codename | `soc` | `soc_source` | matrix rows |
|---|---|---|---:|---:|
| `Edge_20` | `berlin` | `Qualcomm SM7325 Snapdragon 778G 5G` | `builds.csv` | 31 |
| `Edge_2021` | `berlna` | `Qualcomm SM7325 Snapdragon 778G 5G` | `builds.csv` | 36 |

Both build from `sm7325-common`: `berlin/BoardConfig.mk:9` and
`berlna/BoardConfig.mk:9` each `include device/motorola/sm7325-common/BoardConfigCommon.mk`,
and the vendor DT has 15 `berlin` files, including
`yupik-berlin-common-overlay.dtsi` (4,598 B, which `#include`s
`yupik-moto-common-overlay.dtsi` and three `yupik-berlin-*` fragments) [F]. The
device is a `yupik` board, and the `berlin`/`berlna` distinction lives entirely in
overlays [F].

Mainline has **4** real SM7325 boards and neither slice device is one [F]:

| DTS | `model` |
|---|---|
| `sm7325-motorola-dubai.dts` | `Motorola Edge 30` |
| `sm7325-nothing-spacewar.dts` | `Nothing Phone (1)` |
| `sm7325-xiaomi-lisa.dts` | `Xiaomi 11 Lite 5G NE` |
| `sm7325-xiaomi-taoyao.dts` | `Xiaomi 12 Lite 5G` |

`berlin` and `berlna` appear **0** times in `arch/arm64/boot/dts/qcom/` [F].

### 7.3 An inventory discrepancy this note does not fix

Investigating §7.2 turned up a real inconsistency in the committed data, which is
reported here rather than silently corrected because `device-inventory.csv` is a
generated projection and the `soc` column is sourced from `builds.csv`, outside
this note's remit [F]:

| source | `Edge_30` / `dubai` SoC |
|---|---|
| `device-inventory.csv` | `Qualcomm SM7250 Snapdragon 765G` |
| `coverage-matrix.csv` (338 rows, all `db_path` under `dubai/`) | `Qualcomm SM7325-AE Snapdragon 778G 5G` |
| `arch/arm64/boot/dts/qcom/sm7325-motorola-dubai.dts` | `Motorola Edge 30` on `sm7325` |
| LineageOS wiki, `dubai` | `Qualcomm SM7325-AE Snapdragon 778G+ 5G` |
| GSMArena, Edge 30 | `SM7325-AE Snapdragon 778G+ 5G` |
| `/e/OS` device page, `dubai` | `SM7325-AE Snapdragon 778G+ 5G` |

`Edge_30_Fusion` (`tundra`) **is** SM7250 with 639 rows, so the inventory row for
`dubai` reads like a copy of the `tundra` row. Four independent sources plus the
matrix itself say `dubai` is SM7325-AE. Recorded as [OPEN]; no file was edited,
because (a) the field is generated, (b) `Edge_30` is not in this slice, and
(c) changing a `soc` label would silently move 338 rows between SoC slices and
invalidate every count that quotes them [OPEN].

## 8. Rule 1 pass

Three files needed in-place fixes. Before/after:

| file | before | after |
|---|---|---|
| `research/soc/Qualcomm-SM7325-Snapdragon-778G-soc.md` §1.4 table + §0 verdict row + §1.4 corollary 1 | Prime = `MIDR_CORTEX_X1` `0x410fd440`; "`CORTEX_A78` … appears in no erratum or mitigation list at all" | Prime = Cortex-A78, `0x411FD411`; `CORTEX_A78` present in `cpu_errata.c:402`, `cpu_errata.c:669`, `proton-pack.c:882` |
| `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-cpu.md` §3.1 + §0 verdict row + §7.1 table | "the core counts are *in the phandle args*"; "the core count itself is redundant with both" | second phandle cell is the driver's `max_cores` boost threshold, not a core count; `yupik`/`lahaina`/`shima` disprove the core-count reading |
| `research/CORRECTIONS.md` | 13 rows | 15 rows, one for each correction above |
| `docs/REPO-STATE-MAP.md` CPU/SoC row | 6 sections; SM7325 described as "one `cpu-map` cluster" with no vendor DT | 7 sections; SM7325 records the vendor 3-cluster DT and the A78 prime |

The `REPO-STATE-MAP.md` SoCs-remaining count is **unchanged at 21**, because this
note adds a CPU section for a SoC that already had one — it does not add a SoC.

## 9. Honest negatives

1. **No payload was read, and none exists in this workspace.** Every MIDR in §3.4
   is arithmetic on `cputype.h` plus a published `REVISION` string; no
   `MRS x0, MIDR_EL1` was observed [N].

2. **The prime/A78 assignment is `[I]`, not `[F]`.** It rests on a `FAMILY` field
   in a third-party app's capture plus six published specs. It is not a MIDR read.
   The strongest single piece of evidence is the `sm8350` control (§3.2), which
   shows the field *can* report `Cortex-X1` and does not report it here [N for a
   direct read, F for the field's discriminating power].

3. **The `0x411FD411` prime MIDR is a prediction, not an observation.** It follows
   from A78 r1p1, which follows from the `REVISION r1p1` token. If the prime were
   an A78 at a different revision, the value would differ. No capture of
   `/proc/cpuinfo` for a `berlna` was found [OPEN].

4. **The `max_cores` reading in §2.2 is `[I]` for intent.** The driver code is
   `[F]` — `args[1]` is passed as `max_cores` and compared against
   `LUT_CORE_COUNT`. *Why* Qualcomm wrote `4` for the 3-core and 1-core clusters
   on `yupik` is not knowable from the DT; it would need a LUT dump [OPEN].

5. **The slice contributes zero CPU evidence.** 67 rows, 0 CPU filenames, 0
   `.b00`, `isa_identified` empty 67/67. Nothing in §2–§4 is derived from this
   slice's bytes [N].

6. **`#freq-domain-cells = <2>` is a downstream extension with no binding.**
   Mainline's `cpufreq-qcom-hw.yaml` constrains it to `<1>`, and the vendor
   compatible `qcom,cpufreq-hw-epss` matches neither the binding nor mainline's
   match table. The two-cell form is documented nowhere upstream, so its second
   cell's meaning was inferred from driver code only [OPEN for a spec, F for the
   code].

7. **The 4+4 idle-state split in §2.1 is unexplained.** Mainline gives
   `cpu_pd4`–`cpu_pd7` the same `big_cpu_sleep_*` states, which merges the prime
   into the gold cluster at the power level while `freq-domain` separates them.
   Whether the hardware really has a distinct prime power domain is not settled
   here [OPEN].

8. **`Edge_30`'s SoC label in `device-inventory.csv` contradicts four sources
   (§7.3)** and was not corrected, for the reasons given there [OPEN].

9. **`CONFIG_ARM64_ERRATUM_4118414` does not exist in the vendor 5.4.302 tree**,
   so the A78 TLBI erratum is unmitigated on the kernel these devices run. That
   is a statement about the config surface, not a claim that the device is
   exploitable [F for the absence, OPEN for impact].

## 10. Reproduce

Every command below was run on 2026-11-26 and exits 0.

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm SM7325 Snapdragon 778G 5G']
print('rows',len(s),'files',len({r['filename'] for r in s}),'bytes',sum(int(r['size_bytes']) for r in s))
print('devices',dict(Counter(r['device'] for r in s)))
print('families',dict(Counter(r['blob_family'] for r in s)))
print('cpu-named files',[r['filename'] for r in s if 'cpu' in r['filename'].lower()])
print('isa empty',sum(1 for r in s if not r['isa_identified'].strip()))
print('boot bytes pct',round(100*sum(int(r['size_bytes']) for r in s if r['blob_family']=='boot')/sum(int(r['size_bytes']) for r in s),2))"
```

```bash
python3 -I -c "
m=lambda imp,pn:(imp<<24)|(0xf<<16)|(pn<<4)
r=lambda b,v,rv:b|(v<<20)|rv
print('A78 r0p0 0x%08X'%r(m(0x41,0xD41),0,0))
print('A78 r1p1 0x%08X'%r(m(0x41,0xD41),1,1))
print('X1  r1p0 0x%08X'%r(m(0x41,0xD44),1,0))
print('A55 r2p0 0x%08X'%r(m(0x41,0xD05),2,0))
print('A78 r1p1 == X1 r1p1?', r(m(0x41,0xD41),1,1)==r(m(0x41,0xD44),1,1))"
```

```bash
python3 -I -c "
import re,urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x'}),timeout=60).read().decode()
        except Exception as e:
            if '404' in str(e): return None
            if i==n-1: raise
            time.sleep(8*(i+1))
B='https://raw.githubusercontent.com/LineageOS/android_kernel_motorola_sm7325/lineage-22.2/arch/arm64/boot/dts/vendor/qcom/'
y=get(B+'yupik.dtsi')
print('yupik bytes',len(y.encode()))
print('model',re.findall(r'model = \"([^\"]+)\"',y)[:1])
print('msm-id',re.findall(r'qcom,msm-id = <[^>]+>(?:, <[^>]+>)*',y))
print('cpu nodes',len(re.findall(r'CPU[0-9]: cpu@[0-9a-f]+',y)))
print('capacity',re.findall(r'capacity-dmips-mhz = <([0-9]+)>',y))
print('dpc',re.findall(r'dynamic-power-coefficient = <([0-9]+)>',y))
print('freq-domain',re.findall(r'qcom,freq-domain = <&cpufreq_hw ([0-9]+) ([0-9]+)>',y))
print('cells',re.findall(r'#freq-domain-cells = <(\d+)>',y))
print('kryo670',y.count('kryo670'),'cortex strings',len(re.findall(r'arm,cortex-a\d+',y)))"
```

```bash
python3 -I -c "
import re,urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x'}),timeout=60).read().decode()
        except Exception as e:
            if '404' in str(e): return None
            if i==n-1: raise
            time.sleep(8*(i+1))
B='https://raw.githubusercontent.com/LineageOS/android_kernel_motorola_sm7325/lineage-22.2/arch/arm64/boot/dts/vendor/qcom/'
def clus(t):
    i=t.find('cpu-map {'); st=t.find('{',i); d=0
    for j in range(st,len(t)):
        if t[j]=='{': d+=1
        elif t[j]=='}':
            d-=1
            if d==0: b=t[i:j+1]; break
    out={}
    for m in re.finditer(r'(cluster\d) \{(.*?)\n\t\t\t\};',b,re.S):
        out[m.group(1)]=len(re.findall(r'cpu = <&CPU\d>',m.group(2)))
    return out
for n in ('blair.dtsi','holi.dtsi','yupik.dtsi','lahaina.dtsi','shima.dtsi'):
    t=get(B+n)
    if not t: print(n,'ABSENT'); continue
    fds=re.findall(r'qcom,freq-domain = <&cpufreq_hw (\d+) (\d+)>',t)
    per={}
    for d,v in fds: per.setdefault(int(d),set()).add(int(v))
    sizes=[clus(t)[k] for k in sorted(clus(t))]
    vals=[sorted(per[k])[0] for k in sorted(per)] if per else []
    print('%-14s clusters=%-12s 2nd=%-12s equal=%s'%(n,sizes,vals,sizes==vals))
    time.sleep(2)"
```

```bash
python3 -I -c "
import re,urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x'}),timeout=60).read().decode()
        except Exception as e:
            if '404' in str(e): return None
            if i==n-1: raise
            time.sleep(8*(i+1))
B='https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/'
for f in ('kernel/cpu_errata.c','kernel/proton-pack.c','kernel/cpufeature.c'):
    t=get(B+f)
    wb=len(re.findall(r'CORTEX_A78\b',t))
    print('%-22s word-boundary CORTEX_A78 = %d'%(f,wb))
    for m in re.finditer(r'CORTEX_A78\b',t):
        ln=t[:m.start()].count(chr(10))+1
        print('     :%d  %s'%(ln,t.split(chr(10))[ln-1].strip()))
    time.sleep(2)"
```

```bash
python3 -I -c "
import re,urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x'}),timeout=60).read().decode()
        except Exception as e:
            if '404' in str(e): return None
            if i==n-1: raise
            time.sleep(8*(i+1))
k=get('https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/boot/dts/qcom/kodiak.dtsi')
print('kodiak bytes',len(k.encode()))
i=k.find('cpu-map {'); st=k.find('{',i); d=0
for j in range(st,len(k)):
    if k[j]=='{': d+=1
    elif k[j]=='}':
        d-=1
        if d==0: b=k[i:j+1]; break
print('cpu-map children',re.findall(r'\n\t\t\t(\w+) \{',b))
print('cores in map',len(re.findall(r'cpu = <&',b)))
print('capacity',re.findall(r'capacity-dmips-mhz = <([0-9]+)>',k))
print('dpc',re.findall(r'dynamic-power-coefficient = <([0-9]+)>',k))
print('cells',re.findall(r'#freq-domain-cells = <(\d+)>',k))
print('kryo670',k.count('kryo670'))
s=get('https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/boot/dts/qcom/sm7325.dtsi')
print('sm7325.dtsi bytes',len(s.encode()),'kryo670 rebinds',s.count('compatible = \"qcom,kryo670\"'))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
b='upstream-contribution/blob-database/'
m=list(csv.DictReader(open(b+'coverage-matrix.csv')))
inv=list(csv.DictReader(open(b+'device-inventory.csv')))
for dev in ('Edge_30','Edge_30_Fusion'):
    d=[r for r in m if r['device']==dev]
    print(dev,'rows',len(d),dict(Counter(r['soc'].strip() for r in d)))
for r in inv:
    if r['model'] in ('Edge_20','Edge_2021','Edge_30','Edge_30_Fusion'):
        print('%-14s %-9s %-40s %s'%(r['model'],r['build_codename'],r['soc'],r['soc_source']))"
```

```bash
python3 -I -c "
import re,urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x'}),timeout=60).read().decode()
        except Exception as e:
            if '404' in str(e): return None
            if i==n-1: raise
            time.sleep(8*(i+1))
q=get('https://raw.githubusercontent.com/torvalds/linux/master/include/dt-bindings/arm/qcom,ids.h')
d={int(v):n for n,v in re.findall(r'#define\s+QCOM_ID_(\w+)\s+(\d+)',q)}
print('mainline defines',len(d))
for k in (475,499,515):
    print(' id',k,d.get(k,'ABSENT'))
v=get('https://raw.githubusercontent.com/LineageOS/android_kernel_motorola_sm7325/lineage-22.2/drivers/soc/qcom/socinfo.c')
dv={int(k):n for k,n in re.findall(r'\{\s*(\d+),\s*\"([^\"]+)\"\s*\}',v)}
print('vendor entries',len(dv))
for k in (475,497,498,499,515):
    print(' id',k,dv.get(k,'ABSENT'))"
```

```bash
python3 -I -c "
import re,urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x'}),timeout=60).read().decode()
        except Exception as e:
            if '404' in str(e): return None
            if i==n-1: raise
            time.sleep(8*(i+1))
V='https://raw.githubusercontent.com/LineageOS/android_kernel_motorola_sm7325/lineage-22.2/'
mk=get(V+'Makefile')
print('vendor kernel',[l.strip() for l in mk.split(chr(10)) if l.startswith(('VERSION','PATCHLEVEL','SUBLEVEL'))])
cf=get(V+'arch/arm64/kernel/cpufeature.c')
print('vendor A55 lines',[n for n,l in enumerate(cf.split(chr(10)),1) if 'MIDR_CORTEX_A55' in l])
ce=get(V+'arch/arm64/kernel/cpu_errata.c')
print('vendor cpu_errata word-boundary A78',len(re.findall(r'CORTEX_A78\b',ce)),
      [n for n,l in enumerate(ce.split(chr(10)),1) if re.search(r'CORTEX_A78\b',l)])
print('vendor proton-pack exists', get(V+'arch/arm64/kernel/proton-pack.c') is not None)
kc=get(V+'arch/arm64/Kconfig')
print('vendor Kconfig 3194386',[n for n,l in enumerate(kc.split(chr(10)),1) if l.startswith('config ARM64_ERRATUM_3194386')])
print('vendor Kconfig 4118414',[n for n,l in enumerate(kc.split(chr(10)),1) if l.startswith('config ARM64_ERRATUM_4118414')])"
```

```bash
python3 -I -c "
import re,urllib.request,time
def get(u,n=5):
    for i in range(n):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'x'}),timeout=60).read().decode()
        except Exception as e:
            if '404' in str(e): return None
            if i==n-1: raise
            time.sleep(8*(i+1))
y=get('https://raw.githubusercontent.com/torvalds/linux/master/Documentation/devicetree/bindings/cpufreq/cpufreq-qcom-hw.yaml')
i=y.find('#freq-domain-cells')
print(y[i:i+80])
print('vendor compatible in binding?', y.count('cpufreq-hw-epss'))
print('sm7325 in binding?', y.count('sm7325'))
c=get('https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/include/asm/cputype.h')
print('KRYO_6XX in cputype.h', c.count('KRYO_6XX'))
print('X1 part', re.findall(r'ARM_CPU_PART_CORTEX_X1\s+(0x[0-9A-F]+)',c))
print('A78 part', re.findall(r'ARM_CPU_PART_CORTEX_A78\s+(0x[0-9A-F]+)',c))"
```

## Sources

| claim | source | access |
|---|---|---|
| 67 rows / 39 files / 346,793,472 B / 2 devices; families `other` 29, `adsp` 12, `bt` 8, `gpu` 8, `boot` 6, `wifi` 4; `isa_identified` empty 67/67; 0 CPU-named files; boot 72.57% | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-26 |
| `Edge_20`=`berlin` / `Edge_2021`=`berlna`, both `soc_source=builds.csv`; `Edge_30`=`dubai` labelled SM7250 | `upstream-contribution/blob-database/device-inventory.csv` | 2026-11-26 |
| `yupik.dtsi` 144,296 B; `model` `:29`; `msm-id` `:31` `<475 0x10000>, <515 0x10000>`; `cpu-map` `:211` with 3 clusters 4/3/1; 8 CPU nodes `:62`–`:193`; capacities 1024×4/1946×3/1985×1; dpc 100×4/520×3/552×1; `freq-domain` `0 4`/`1 4`/`2 4`; `cpufreq_hw` `:2678` with 3 windows; `lut-row-size 4` `:2688`; `cells <2>` `:2700`; 0 `kryo670`, 0 `arm,cortex-a*`; 0 CPU `operating-points-v2` | `android_kernel_motorola_sm7325` lineage-22.2 `arch/arm64/boot/dts/vendor/qcom/yupik.dtsi` | 2026-11-26 |
| `SLVR_OFF` `:91`, `SLVR_RAIL_OFF` `:105`, `GOLD_OFF` `:139`, `GOLD_RAIL_OFF` `:153` as `qcom,pm-cpu-level@1/@2` | same tree, `yupik-pm.dtsi` (4,737 B) | 2026-11-26 |
| `blair.dtsi` 94,327 B clusters 6+2 second cell `6`/`2`; `holi.dtsi` 6+2 `6`/`2`; `lahaina.dtsi` 151,073 B 4/3/1 `4`/`4`/`4`, `model` `Lahaina`, `msm-id` `<415>, <456>, <501>`; `shima.dtsi` 98,872 B 4/3/1 `4`/`4`/`4` | same tree, `arch/arm64/boot/dts/vendor/qcom/` | 2026-11-26 |
| 998 files in vendor `dts/vendor/qcom/`; 139 match `yupik`, 15 match `berlin` | GitHub contents API, same tree | 2026-11-26 |
| `berlin/BoardConfig.mk:9` and `berlna/BoardConfig.mk:9` inherit `sm7325-common`; `yupik-berlin-common-overlay.dtsi` 4,598 B | `LineageOS/android_device_motorola_berlin` and `_berlna` lineage-22.2; vendor DT | 2026-11-26 |
| `TARGET_ARCH_VARIANT := armv8-2a-dotprod`, `TARGET_CPU_VARIANT_RUNTIME := kryo385`, `TARGET_BOARD_PLATFORM := lahaina`, `TARGET_KERNEL_CONFIG := vendor/lahaina-qgki_defconfig vendor/lineage_moto-lahaina.config` | `LineageOS/android_device_motorola_sm7325-common` `BoardConfigCommon.mk:10,14,44,48` | 2026-11-26 |
| vendor `qcom-cpufreq-hw.c`: `args[1]` → `max_cores` at `:673`, used at `:473` as `core_count != max_cores`; `LUT_CORE_COUNT` `GENMASK(18,16)` `:28`; `qcom,lut-row-size`/`qcom,lut-max-entries` read at `:649`,`:652`; match table `qcom,cpufreq-hw-epss` at `:743` | same vendor tree, `drivers/cpufreq/qcom-cpufreq-hw.c` | 2026-11-26 |
| mainline driver reads `args.args[0]` only at `:323`,`:558`; match table `:440-442` has no `cpufreq-hw-epss` | `torvalds/linux` master `drivers/cpufreq/qcom-cpufreq-hw.c` | 2026-11-26 |
| `'#freq-domain-cells': const: 1` at `:95-96`; no `sm7325`, no `cpufreq-hw-epss` in the compatible enum | `Documentation/devicetree/bindings/cpufreq/cpufreq-qcom-hw.yaml` | 2026-11-26 |
| `kodiak.dtsi` 202,322 B; one `cpu-map` cluster at `:404` with 8 `coreN`; capacities and dpc identical to vendor; `freq-domain` 0/1/2; `cells <1>` `:7130`; `cpufreq_hw` `:7115` compatible `"qcom,sc7280-cpufreq-epss","qcom,cpufreq-epss"` with 3 windows; 4 `arm,idle-state` at `:443`–`:473` referenced from `cpu_pd0` `:874`–`cpu_pd7` `:919`; 0 `cpu-idle-states`; 0 `kryo670`; CPU OPP tables 11+13+14 rows | `arch/arm64/boot/dts/qcom/kodiak.dtsi`, master | 2026-11-26 |
| `sm7325.dtsi` 537 B / 17 lines / 8 `compatible = "qcom,kryo670"` rebinds | `arch/arm64/boot/dts/qcom/sm7325.dtsi`, master | 2026-11-26 |
| 4 SM7325 boards: `motorola,dubai` (Motorola Edge 30), `nothing,spacewar`, `xiaomi,lisa`, `xiaomi-taoyao`; 0 `berlin`/`berlna` | GitHub contents API + the four DTS files, master | 2026-11-26 |
| `QCOM_ID_SM7325`=475 `:239`, `QCOM_ID_SM7325P`=499 `:246`, 515 absent, 308 defines | `include/dt-bindings/arm/qcom,ids.h`, master | 2026-11-26 |
| vendor `socinfo.c`: `{475,"YUPIK"}` `:792`, `{497,"YUPIK-IOT"}` `:795`, `{498,"YUPIKP-IOT"}` `:796`, `{499,"YUPIKP"}` `:797`, `{515,"YUPIK-LTE"}` `:798` | vendor tree, `drivers/soc/qcom/socinfo.c` | 2026-11-26 |
| `CORTEX_A78` word-boundary at `cpu_errata.c:402` (`ARM64_ERRATUM_4118414`) and `:669` (`ARM64_ERRATUM_3194386`), `proton-pack.c:882` (`spectre_bhb_k32_list`); 0 in `cpufeature.c` | `arch/arm64/kernel/{cpu_errata,proton-pack,cpufeature}.c`, master | 2026-11-26 |
| Kconfig 4118414 "ARM Cortex-A78 erratum 4193791", `select ARM64_WORKAROUND_REPEAT_TLBI_SYNC`, `default y`; 3194386 "ARM Cortex-A78 erratum 3324344", `default y` | `arch/arm64/Kconfig`, master | 2026-11-26 |
| vendor kernel 5.4.302; `cputype.h` A78 `0xD41` `:79`, X1 `0xD44` `:80`, 0 `KRYO_6XX`, no NOTES; `cpu_errata.c` 2 word-boundary A78 at `:848`,`:1180`; no `proton-pack.c`; `Kconfig:622` 3194386, no 4118414; `cpufeature.c` A55 at `:1036` (KPTI, `CONFIG_COMPAT`) and `:1163` (broken DBM, `CONFIG_ARM64_ERRATUM_1024718`) | vendor tree, `android_kernel_motorola_sm7325` lineage-22.2 | 2026-11-26 |
| `ARM_CPU_PART_CORTEX_A78` `0xD41` `:80`, `ARM_CPU_PART_CORTEX_X1` `0xD44` `:82`, `ARM_CPU_IMP_ARM` `0x41` `:54`, `ARM_CPU_IMP_QCOM` `0x51` `:58`, `KRYO_4XX_SILVER` `0x805` `:133`, `MIDR_CPU_MODEL` `:43`, `MIDR_CPU_VAR_REV` `:48`, NOTES `:239-246` | `arch/arm64/include/asm/cputype.h`, master | 2026-11-26 |
| `HWCAP_ASIMDDP` `(1 << 20)` at `:46`, `HWCAP_ASIMDDP` gated by `ID_AA64ISAR0_EL1.DP` at `cpufeature.c:3198` | `arch/arm64/include/uapi/asm/hwcap.h`; `cpufeature.c`, master | 2026-11-26 |
| `qcom,kryo670` at `cpus.yaml:224` among 16 enumerated `kryo` values plus `qcom,kryo` at `:243` | `Documentation/devicetree/bindings/arm/cpus.yaml`, master | 2026-11-26 |
| `sm7325` `FAMILY Cortex-A78 Cortex-A78 Cortex-A55`, `REVISION r1p1 r1p1 r2p0`, `CLUSTERS 1 x 2.40 3 x 2.40 4 x 1.80`, kernel `5.4.254-moto`, `berlna_global` (item 103878); `redwood_global` (103829); `Spacewar` (103714) | `deviceinfohw.ru` item 103878, 103829, 103714 | 2026-11-26 |
| control set: `sm8350` `Cortex-X1 Cortex-A78 Cortex-A55` (103708); `sm8650` `Cortex-X4 Cortex-A720 Cortex-A720 Cortex-A520` (103881); `s5e9925` `Cortex-X2 Cortex-A710 Cortex-A510` (103880); `sm6375` `Cortex-A78 Cortex-A55` (103883); `sm4350` `Kryo-4xx-a76 Kryo-4xx-a55` (103786) | `deviceinfohw.ru` items as listed | 2026-11-26 |
| Kryo 670 Prime is Cortex-A78; Kryo 670 "doesn't feature the Cortex-X1" | `en.wikipedia.org/wiki/Kryo`; GSMArena 778G announcement; `androidauthority.com/qualcomm-snapdragon-kryo-cpu-numbers-1080105`; `nanoreview.net/en/soc/qualcomm-snapdragon-778g-5g`; `cpu-boss.com/en/cpu-qualcomm-snapdragon-778g`; `devicespecifications.com/en/model/d9ea5952` | 2026-11-26 |
| `dubai` = SM7325-AE Snapdragon 778G+ 5G, `XT2203-1`, kernel 5.4 | `wiki.lineageos.org/devices/dubai`; `doc.e.foundation/devices/dubai`; GSMArena Edge 30 | 2026-11-26 |
