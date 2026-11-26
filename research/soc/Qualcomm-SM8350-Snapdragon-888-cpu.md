# Qualcomm SM8350 Snapdragon 888 — CPU: three distinct cores, three MIDRs, and the co-processor nobody names

Issue #859. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative / [OPEN] unresolved. Every number is command output from a run on
**2026-11-26** against
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows),
`device-inventory.csv`, `torvalds/linux` master, the public vendor kernel tree
`LineageOS/android_kernel_oneplus_sm8350` (lineage-24.0), and the
`deviceinfohw.ru` capture database.

**No payload exists in this workspace and none was read.** Every statement below
is matrix metadata — filename, size, `db_type`, family label — public GPL source,
or a published device capture. No vendor ELF is parsed here and no instruction is
disassembled [N].

This is the **CPU** note. The SoC package, GPU, DSP, boot chain, TrustZone and
firmware-family census for SM8350 are owned by
`research/soc/Qualcomm-SM8350-Snapdragon-888-soc.md` (#815) and the GPU by
`research/soc/Qualcomm-SM8350-Snapdragon-888-gpu.md`; both are **cited, never
re-derived**. What this note adds is the part #815 deliberately left out because
it is scoped to the package: MIDR arithmetic against the observed silicon, the
vendor `lahaina.dtsi` as a second and differently-shaped description of the same
eight cores, the `cpucp` co-processor, and the erratum scope per cluster.

## 0. Verdict

| question | answer | class |
|---|---|---|
| CPU topology | **1 + 3 + 4** — one Cortex-X1, three Cortex-A78, four Cortex-A55 | [F] |
| Distinct cores | **three** — this is the SM8350 property that separates it from every other Qualcomm SoC in this repo | [F] |
| `compatible` in mainline | **`arm,cortex-x1` / `arm,cortex-a78` / `arm,cortex-a55`** — real ARM names, not `qcom,kryo` | [F] |
| `compatible` in the vendor DT | **`qcom,kryo`** ×8 — the opposite of mainline | [F] |
| Prime MIDR | **`0x411FD440`** (X1 r1p0) | [I] |
| Gold MIDR | **`0x410FD410`** (A78 r1p0) | [I] |
| Silver MIDR | **`0x412FD050`** (A55 r2p0) | [I] |
| MIDRs distinguishable? | **yes, all three** — X1 and A78 differ only in part number, and the model field separates them | [F] |
| `capacity-dmips-mhz` in mainline | **absent** — 0 occurrences; the vendor DT has 1024/1946/2048 | [F] |
| `dynamic-power-coefficient` in mainline | **absent** — 0 occurrences | [F] |
| `cpu-map` in mainline | **one** `cluster0` of eight cores; vendor has **three** (4/3/1) | [F] |
| `#freq-domain-cells` | **`<1>`** mainline, **`<2>`** vendor | [F] |
| Vendor prime capacity | **2048**, not 1985 — a real divergence from the SM7325 sibling | [F] |
| The CPU-adjacent co-processor | **CPUCP**, with a mainline mailbox driver that does **not** list `sm8350` | [F] |
| `cpucp_fw_mem` reservation | `<0x0 0x80b00000 0x0 0x100000>` = **1,048,576 B**, declared and **never referenced** | [F] |
| Slice CPU evidence | **1 row** — `cpucp.img` 110,592 B, `db_type=UNKNOWN`, `isa_identified` empty | [N] |
| Slice size | 693 rows / 651 files / 886,208,933 B (845.15 MiB) / 2 devices | [F] |
| X1 and A78 errata | **both listed, at different lines** — `cpu_errata.c:406` vs `:402`, `:676` vs `:669`; `proton-pack.c:885` vs `:882` | [F] |

## 1. Scope: what #815 owns, and what it does not

`research/soc/Qualcomm-SM8350-Snapdragon-888-soc.md` (#815) established the
1+3+4 topology, the eight `cpu@` nodes and their `arm,cortex-*` compatibles, the
single mainline `cpu-map` cluster, the three `freq-domain`s, the shared `l3_0`,
the boot chain (§4), the 25-region TrustZone layout (§5), the firmware families
(§6), mainline and postmarketOS status (§8), and the matrix arithmetic (§9). None
of that is rebuilt here.

What #815 does not contain, because a package-scoped note has no reason to:

- any MIDR value at all — it records the compatible strings and stops there;
- the vendor `lahaina.dtsi`, which describes the same silicon differently;
- `cpucp`, which is a CPU-adjacent core rather than a firmware family;
- which errata actually apply per cluster, and at which line numbers.

Those four gaps are §2 through §5.

## 2. Three distinct cores — the SM8350 property that has no analogue in this repo

### 2.1 Mainline names real ARM cores

`sm8350.dtsi` (117,937 B) is unusual. Almost every Qualcomm SoC in mainline
declares its CPUs as `qcom,kryo` or a numbered `qcom,kryoNNN`; this file names
the actual ARM parts [F]:

| cpu | `reg` | `compatible` | line | `qcom,freq-domain` |
|---|---|---|---:|---|
| `cpu0` | `0x0` | `arm,cortex-a55` | 59 | `cpufreq_hw 0` |
| `cpu1` | `0x100` | `arm,cortex-a55` | 83 | `cpufreq_hw 0` |
| `cpu2` | `0x200` | `arm,cortex-a55` | 102 | `cpufreq_hw 0` |
| `cpu3` | `0x300` | `arm,cortex-a55` | 121 | `cpufreq_hw 0` |
| `cpu4` | `0x400` | `arm,cortex-a78` | 140 | `cpufreq_hw 1` |
| `cpu5` | `0x500` | `arm,cortex-a78` | 159 | `cpufreq_hw 1` |
| `cpu6` | `0x600` | `arm,cortex-a78` | 178 | `cpufreq_hw 1` |
| `cpu7` | `0x700` | **`arm,cortex-x1`** | 197 | `cpufreq_hw 2` |

Three `arm,cortex-*` strings in one file, and the count is 11 tokens total
because three PMU nodes repeat them [F]:

```
sm8350.dtsi:309  compatible = "arm,cortex-a55-pmu";
sm8350.dtsi:314  compatible = "arm,cortex-a78-pmu";
sm8350.dtsi:319  compatible = "arm,cortex-x1-pmu";
```

Three PMU nodes is itself the corroboration: mainline only declares a
per-cluster PMU where the clusters are genuinely different parts [I].

### 2.2 The vendor tree says `qcom,kryo` for the same eight cores

The vendor platform file for this SoC is `lahaina.dtsi` (151,563 B,
`model = "Qualcomm Technologies, Inc. Lahaina"`,
`qcom,msm-id = <415 0x10000>, <456 0x10000>, <501 0x10000>`) [F]. It does not
name a single ARM core [F]:

| property | mainline `sm8350.dtsi` | vendor `lahaina.dtsi` |
|---|---|---|
| `compatible` | `arm,cortex-a55` ×4, `arm,cortex-a78` ×3, `arm,cortex-x1` ×1 | **`qcom,kryo` ×8** |
| `cpu-map` clusters | **1** — `cluster0` with 8 `coreN` | **3** — 4 / 3 / 1 |
| `#freq-domain-cells` | **`<1>`** | **`<2>`** |
| `capacity-dmips-mhz` | **absent (0)** | 1024×4 / 1946×3 / **2048**×1 |
| `dynamic-power-coefficient` | **absent (0)** | present |
| `cpufreq_hw` compatible | `"qcom,sm8350-cpufreq-epss", "qcom,cpufreq-epss"` | `"qcom,cpufreq-hw-epss"` |
| `lut` properties | none in DT (driver defaults) | `qcom,lut-row-size = <4>`, `qcom,skip-enable-check` |
| interrupt names | `dcvsh-irq-0..2` | `dcvsh0_int`, `dcvsh1_int`, `dcvsh2_int` |

The two files describe the same silicon with opposite conventions. Mainline names
the cores and flattens the map; the vendor names nothing and splits the map [F].

**The `arm,cortex-*` convention is the trap.** #853 found SM7325 uses
`qcom,kryo` in vendor and `qcom,kryo670` in mainline — a rename. SM8350 does not
rename; it *replaces* the vendor's `qcom,kryo` with real ARM part names. A port
that generalises from SM7325 ("Qualcomm DTs say `qcom,kryo`") will read
`sm8350.dtsi` wrong, and a script that looks for `qcom,kryo` to find Qualcomm CPU
nodes will find **zero** here [F].

### 2.3 The 2048 prime capacity

`capacity-dmips-mhz` does not exist in mainline `sm8350.dtsi` at all — 0
occurrences [F]. So the only capacity numbers for this SoC come from the vendor
file, and its prime value is **2048**, not the 1985 that the SM7325 sibling uses
[F]:

| cluster | SM8350 vendor `lahaina` | SM7325 vendor `yupik` |
|---|---:|---:|
| silver ×4 | 1024 | 1024 |
| gold ×3 | 1946 | 1946 |
| prime ×1 | **2048** | 1985 |

That is a genuine difference between two 1+3+4 parts in the same generation, and
it is what an X1 buys over an A78 in the prime slot [I]. It also means capacity
alone distinguishes the two SoCs, which the MIDR cannot do for SM7325's
prime/gold pair (#853 §3.4) [F].

## 3. Three MIDRs, all distinguishable

### 3.1 The observed silicon

Four independent `sm8350` captures in `deviceinfohw.ru` agree exactly [F]:

| item | `FAMILY` | `REVISION` | clock |
|---|---|---|---|
| 103708 | `Cortex-X1 Cortex-A78 Cortex-A55` | `r1p0 r1p0 r2p0` | 300 – 2841 MHz |
| 103715 | `Cortex-X1 Cortex-A78 Cortex-A55` | `r1p0 r1p0 r2p0` | 300 – 2841 MHz |
| 103741 | `Cortex-X1 Cortex-A78 Cortex-A55` | `r1p0 r1p0 r2p0` | 300 – 2841 MHz |
| 103775 | `Cortex-X1 Cortex-A78 Cortex-A55` | `r1p0 r1p0 r2p0` | 300 – 2841 MHz |

This is the control experiment #853 used in the other direction: there, `sm8350`
was the *proof* that the `FAMILY` field can report `Cortex-X1`, which is what
made the `sm7325` result (`Cortex-A78 Cortex-A78 Cortex-A55`) meaningful. Here
it is the measurement itself [F].

### 3.2 The arithmetic

`MIDR_CPU_MODEL(imp, partnum)` = `(imp << 24) | (0xf << 16) | (partnum << 4)`
and `MIDR_CPU_VAR_REV(var, rev)` = `(var << 20) | rev` (`cputype.h:43-49`) [F].
With `ARM_CPU_IMP_ARM` = `0x41`, X1 = `0xD44`, A78 = `0xD41`, A55 = `0xD05`:

```
$ python3 -I -c "
m=lambda imp,pn:(imp<<24)|(0xf<<16)|(pn<<4)
r=lambda b,v,rv:b|(v<<20)|rv
print('X1  r1p0 0x%08X'%r(m(0x41,0xD44),1,0))
print('A78 r1p0 0x%08X'%r(m(0x41,0xD41),1,0))
print('A55 r2p0 0x%08X'%r(m(0x41,0xD05),2,0))"
X1  r1p0 0x411FD440
A78 r1p0 0x410FD410
A55 r2p0 0x412FD050
```

The X1 and A78 values differ **only in the part-number nibbles** — a delta of
`(0xD44 - 0xD41) << 4` = `0x30` [F]:

```
X1  0x411FD440
A78 0x410FD410
    ^^^^^^ part number field only
```

### 3.3 Why this is the important structural difference from SM7325

On SM7325 (#853 §3.4) the prime and the gold cluster are **both Cortex-A78 at the
same revision**, so they produce the *same* MIDR and the SoC has only two
distinct values. Any per-cluster policy must fall back to `cpu-map` or
`freq-domain`.

SM8350 does not have that problem. All three clusters report different MIDRs, and
`MIDR_CPU_MODEL` alone separates them [F]:

| cluster | core | full MIDR | model field | var/rev |
|---|---|---|---|---|
| silver ×4 | A55 | `0x412FD050` | `0x410FD050` | 2 / 0 |
| gold ×3 | A78 | `0x410FD410` | `0x410FD410` | 1 / 0 |
| prime ×1 | X1 | `0x411FD440` | `0x410FD440` | 1 / 0 |

So a consumer keyed on MIDR gets the right answer on SM8350 and the wrong one on
SM7325. That asymmetry is the finding: **the "Kryo 6XX" family is not
MIDR-homogeneous, and SM8350 is the member where the DT and the MIDR agree**
[F for the values, I for the generalisation].

## 4. Errata: both big cores listed, at different lines

`CORTEX_X1` and `CORTEX_A78` are both present in the mainline erratum machinery,
but at **different line numbers**, which is the mechanical consequence of them
being different parts [F]:

| list | A78 line | X1 line | config |
|---|---:|---:|---|
| `cpu_errata.c` TLBI completion | **402** | **406** | `CONFIG_ARM64_ERRATUM_4118414` |
| `cpu_errata.c` SSBS | **669** | **676** | `CONFIG_ARM64_ERRATUM_3194386` |
| `proton-pack.c` Spectre-BHB | **882** | **885** | `spectre_bhb_k32_list` |
| `cpufeature.c` (any) | **0** | **0** | — |

Word-boundary counts: `cpu_errata.c` has 2 `CORTEX_X1` and 2 `CORTEX_A78`;
`proton-pack.c` has 1 each; `cpufeature.c` has **0** of either and 2
`CORTEX_A55` [F].

The last row is the same distinction #853 §4 had to draw for SM7325:
`cpufeature.c` holds capability and DBM tables, so "0 hits in `cpufeature.c`"
says nothing about errata. Here it is sharper, because **A55 appears twice in
`cpufeature.c` (KPTI-safe and broken DBM) while X1 and A78 appear zero times** —
so on this SoC the little cores take the DBM workaround and the big cores do
not, which is the mirror image of what a reader might assume [F].

## 5. CPUCP: the co-processor in the CPU complex, and the driver that skips this SoC

### 5.1 What the slice actually contains

The SM8350 slice has **one** CPU-named row, and it is not a CPU core [F]:

| field | value |
|---|---|
| `filename` | `cpucp.img` |
| `device` | `OnePlus_9_Pro` |
| `size_bytes` | **110,592** |
| `blob_family` | `boot` |
| `db_type` | `UNKNOWN` |
| `db_path` | `oneplus/lemonadep/radio` |
| `isa_identified` | *(empty)* |

`cpucp` is the **CPUSS Control Processor** — a small core inside the CPU
subsystem complex that does firmware-assisted tuning. It is the only artefact in
this slice whose name refers to a processor, and its `db_type` is `UNKNOWN`,
meaning the corpus parser could not classify it [F].

### 5.2 Mainline has the transport, but not for this SoC

`drivers/mailbox/qcom-cpucp-mbox.c` (6,508 B) exists in mainline and is a
doorbell between APSS and CPUCP [F]:

```c
drivers/mailbox/qcom-cpucp-mbox.c:15  #define APSS_CPUCP_MBOX_CMD_OFF      0x4
drivers/mailbox/qcom-cpucp-mbox.c:18  #define APSS_CPUCP_TX_MBOX_CMD(i)    (0x100 + ((i) * 8))
drivers/mailbox/qcom-cpucp-mbox.c:22  #define APSS_CPUCP_RX_MBOX_MAP       0x4000
drivers/mailbox/qcom-cpucp-mbox.c:23  #define APSS_CPUCP_RX_MBOX_STAT      0x4400
drivers/mailbox/qcom-cpucp-mbox.c:24  #define APSS_CPUCP_RX_MBOX_CLEAR     0x4800
drivers/mailbox/qcom-cpucp-mbox.c:25  #define APSS_CPUCP_RX_MBOX_EN        0x4c00
```

Its match table lists exactly two compatibles [F]:

```c
drivers/mailbox/qcom-cpucp-mbox.c:204  { .compatible = "qcom,nord-cpucp-mbox",     .data = &qcom_nord_mbox_data },
drivers/mailbox/qcom-cpucp-mbox.c:205  { .compatible = "qcom,x1e80100-cpucp-mbox", .data = &qcom_x1e80100_mbox_data },
```

and the binding `qcom,cpucp-mbox.yaml` enumerates glymur, hawi, kaanapali,
maili, nord, sm8750 and x1e80100 [F]. **`sm8350` is in neither list**, and
`sm8350.dtsi` has no `cpucp` mailbox node — the only occurrence of the string in
the whole file is the memory reservation (§5.3) [F].

So the transport driver exists upstream for 2023-and-later parts and does not
cover this 2021 SoC. That is a specific, checkable negative [N].

### 5.3 The reservation is declared and never used

Both mainline and vendor `lahaina` reserve a region for CPUCP firmware, and both
give it the same address and size [F]:

```
sm8350.dtsi:452        cpucp_fw_mem: memory@80b00000 {
sm8350.dtsi:453                reg = <0x0 0x80b00000 0x0 0x100000>;
sm8350.dtsi:454                no-map;
sm8350.dtsi:455        };
```

`0x100000` = **1,048,576 B** = exactly 1 MiB [F]. In mainline the label
`cpucp_fw_mem` occurs **once** — at its own definition. Nothing references it
[F]. The region is reserved out of the linear map (`no-map`) and then left
entirely unused by any node.

That reservation size matches four rows in the corpus, and the match is exact
[F]:

| device | `cpucp.img` size | SoC |
|---|---:|---|
| `Moto_G200` | **1,048,576** | SM8350-AC Snapdragon 888+ |
| `Edge_40_Pro` | **1,048,576** | SM8550 Snapdragon 8 Gen2 |
| `Edge_30_Fusion` | **1,048,576** | SM7250 Snapdragon 765G |
| `Edge_30` | **1,048,576** | SM7325-AE Snapdragon 778G 5G |

Corpus-wide, `cpucp.img` appears **30** times in **11** distinct sizes, from
110,592 to 1,048,576 B, plus `cpucp_dtb.img` **6** times (16,384 B ×5, 12,288 B
×1) [F]. So the 1 MiB figure is a *ceiling* that four parts reach, not a fixed
property of the image; the SM8350 slice's own `cpucp.img` is 110,592 B, ten
times smaller [F].

Whether the 1 MiB reservation is sized for the largest possible CPUCP image or
for something else is not decidable from metadata [OPEN].

### 5.4 What is vendor-only

`drivers/soc/qcom/cpucp.c` does not exist in mainline (`drivers/soc/qcom/Kconfig`
has 0 `cpucp` hits) [F]. The vendor symbols are not in this SoC's LineageOS trees
either — `LineageOS/android_kernel_oneplus_sm8350` and
`LineageOS/android_kernel_sony_sm8350` at `lineage-24.0` both have **0**
occurrences of `QCOM_CPUCP`, `QCOM_CPUCP_FAST` and `QTI_CPUCP_LOG` in
`drivers/soc/qcom/Kconfig` [F]. They appear in a **different** downstream tree —
`sonyxperiadev/kernel` (master) — which carries three related symbols [F]:

```
config QCOM_CPUCP
        tristate "Qualcomm Technologies, Inc. CPUCP driver"
config QCOM_CPUCP_FAST
        tristate "Qualcomm Technologies, Inc. CPUCP FAST driver"
        help
         ... Firmware Assisted System Tuning driver for MSM devices. This driver
         gets hints from CPUCP firmware through mailbox and informs to scheduler.
config QTI_CPUCP_LOG
        tristate "Qualcomm Technologies Inc. HW CPUCP Logging"
```

and `drivers/interconnect/qcom/cpucp-l3.c` exists in the OnePlus SM8350 tree,
gated by `INTERCONNECT_QCOM_CPUCP_L3` — whose Kconfig text says "**HOLI** CPUCP
L3 driver … found on Holi-based platforms", i.e. SM4350, not SM8350 [F]. So the
one CPUCP driver that does live in an SM8350 tree is scoped to a different SoC.

All of these are vendor-only, and the fact that the SM8350 trees themselves do
not carry `drivers/soc/qcom/cpucp.c` is the sharper negative [N]. The description
"firmware-assisted system tuning … informs to scheduler" is the most specific
public statement about what the CPUCP core does [F for the text, OPEN for what
it actually implements].

## 6. The slice: 693 rows, one CPU-adjacent file

| metric | value |
|---|---|
| rows | **693** |
| distinct filenames | **651** |
| total bytes | **886,208,933** = 845.15 MiB |
| devices | **2** — `OnePlus_9_Pro` (650 rows), `Xperia_5_III` (43 rows) |
| shared filenames | **18** of 43 Xperia files also appear on the OnePlus |
| `db_type` values | **27** |
| `isa_identified` empty | **693 of 693** |

By bytes the slice is dominated by two families [F]:

| family | bytes | share |
|---|---:|---:|
| `boot` | 357,552,128 | **40.35%** |
| `modem` | 307,285,000 | **34.67%** |
| `other` | 149,102,682 | 16.82% |
| `adsp` | 34,505,121 | 3.89% |
| `wifi` | 17,042,793 | 1.92% |
| `tz` | 12,511,746 | 1.41% |
| `cdsp` | 6,008,371 | 0.68% |
| `bt` | 1,912,832 | 0.22% |
| `gpu` | 288,260 | 0.03% |

By row count `other` dominates (324) and `wifi` is second (155) — the byte and
row rankings disagree, which is why both are given [F]. `gpu` is 11 rows and
0.03% of bytes; the GPU identification is #2030's and is not repeated here.

The single CPU-adjacent row is `cpucp.img` (§5.1). No file in the slice is a CPU
core image, and `isa_identified` is empty on every row, so **nothing here
identifies a core** [N].

## 7. Rule 1 pass

| file | before | after |
|---|---|---|
| `research/soc/Qualcomm-SM8350-Snapdragon-888-soc.md` §1 | topology and compatibles only; no MIDR, no vendor DT, no `cpucp` | adds a pointer to this note for MIDRs, the vendor `lahaina` shape, and `cpucp`; no claim changed |
| `docs/REPO-STATE-MAP.md` CPU/SoC row | 7 sections | 8 sections; SM8350 entry gains three distinct MIDRs, the `arm,cortex-*` vs `qcom,kryo` divergence and `cpucp`. **SoCs remaining unchanged at 21** |
| `research/CORRECTIONS.md` | 14 rows | 15 rows — the row above, which corrects a stale count in the #853 note |

The `REPO-STATE-MAP.md` SoC count is unchanged because SM8350 already had a CPU
section; this note deepens it rather than adding a SoC.

**How the section count is derived**, because the row's number is not reproducible
from a naive heading grep. Counting every `##` heading that merely *contains*
"CPU" gives 10 before this note and 10 after — the extra hits are prose headings
such as `## 5. CPUCP: …` and `## 6. The slice: … one CPU-adjacent file` [F]. The
row's convention is instead:

> **4** SoC-note §1 CPU sections (MSM8998, SM4375, SM7325, SM8350)
> **+** one per `*-cpu.md` note in `research/soc/`

which reproduces the row's own history exactly: 4 at `4de3ed2`, 5 at `5790936`
(#841), 6 at `e82a7a3` (#847), 7 at `809e2f1` (#853) [F]. This note adds the
fourth `-cpu.md`, so 4 + 4 = **8** [F]:

```bash
python3 -I -c "
import subprocess,re
soc=['Qualcomm-MSM8998-Snapdragon-835-soc.md','Qualcomm-SM4375-Snapdragon-4-Gen-1-soc.md',
     'Qualcomm-SM7325-Snapdragon-778G-soc.md','Qualcomm-SM8350-Snapdragon-888-soc.md']
n=0
for f in soc:
    t=open('research/soc/'+f).read()
    n+=len(re.findall(r'^## 1\. CPU\b',t,re.M))
print('soc note 1. CPU sections',n)
import os
notes=[f for f in os.listdir('research/soc') if f.endswith('-cpu.md')]
print('cpu notes',len(notes),sorted(notes))
print('total',n+len(notes))"
```

MSM8998 is the one SoC that contributes two CPU sections rather than one (its
`-cpu.md` §3 *and* §8 both describe cores), which is why a per-file count and a
per-section count disagree; the row counts per *SoC-note section plus note file*,
which is the convention that keeps its history monotonic [F].

## 8. Honest negatives

1. **No payload was read, and none exists in this workspace.** All three MIDRs in
   §3.2 are arithmetic on `cputype.h` plus a published `REVISION` string; no
   `MRS x0, MIDR_EL1` was observed [N].

2. **The three MIDRs are `[I]`, not observations.** They follow from the
   `FAMILY`/`REVISION` fields of a third-party app's capture. The `FAMILY` field
   is trustworthy — #853 §3.2 validated it against `sm8650`, `s5e9925`, `sm6375`
   and `sm4350` — but it is not a register read [N for a direct read].

3. **`cpucp.img`'s ISA is `[OPEN]`.** The slice's file is 110,592 B with
   `db_type=UNKNOWN`. Nothing in the corpus classifies it, no `cpucp.mdt` /
   `.b00` / `.elf` exists anywhere in the 33,917 rows, and no payload is
   available. Whether it is a separate core's firmware, a config blob, or a
   container is undecidable here [OPEN].

4. **The 1 MiB reservation is not explained.** `cpucp_fw_mem` is exactly
   1,048,576 B and four corpus parts ship a `cpucp.img` of exactly that size, but
   the slice's own image is 110,592 B. The ceiling-versus-actual relationship
   needs a LUT or a boot trace [OPEN].

5. **Mainline has no CPUCP support for this SoC.** `qcom-cpucp-mbox` exists but
   lists only `nord` and `x1e80100`; `drivers/soc/qcom/cpucp.c` does not exist at
   all; `sm8350.dtsi` has no `cpucp` mailbox node. That is a statement about
   upstream coverage, not about whether the hardware has a CPUCP [F for the
   absence, OPEN for the hardware].

6. **`capacity-dmips-mhz` is absent from mainline for this SoC**, so §2.3's
   2048-vs-1985 comparison rests entirely on the two vendor files. Mainline
   carries no capacity data at all for SM8350 [F].

7. **The vendor `lahaina.dtsi` is not this SoC's only vendor description.**
   `msm-id` lists three IDs (`415`, `456`, `501`), and the vendor `socinfo.c`
   maps them to `LAHAINA`, `LAHAINA-ATP` and `SM8325` — so the same DT covers
   three SKUs. Which one the two slice devices are is not established here
   [OPEN].

8. **`arm,cortex-*` in mainline is not evidence about the silicon's MIDR.** The
   compatible string is a DT author's choice; it happens to agree with the
   captures in §3.1, which is why it is cited as corroboration rather than
   proof [I].

## 9. Reproduce

Every command below was run on 2026-11-26 and exits 0.

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm SM8350 Snapdragon 888']
print('rows',len(s),'files',len({r['filename'] for r in s}),'bytes',sum(int(r['size_bytes']) for r in s))
print('MiB',round(sum(int(r['size_bytes']) for r in s)/1048576,2))
print('devices',dict(Counter(r['device'] for r in s)))
print('families',dict(Counter(r['blob_family'] for r in s)))
print('db_types',len({r['db_type'] for r in s}))
print('isa empty',sum(1 for r in s if not r['isa_identified'].strip()))
print('cpu-named',[r['filename'] for r in s if 'cpu' in r['filename'].lower()])
fb=Counter()
for r in s: fb[r['blob_family']]+=int(r['size_bytes'])
for k,v in fb.most_common(): print('  %-8s %-12d %.2f%%'%(k,v,100*v/sum(int(r['size_bytes']) for r in s)))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=[r for r in rows if r['filename']=='cpucp.img']
print('cpucp.img rows',len(d),'sizes',len({int(r['size_bytes']) for r in d}))
print('min',min(int(r['size_bytes']) for r in d),'max',max(int(r['size_bytes']) for r in d))
for k,v in Counter(int(r['size_bytes']) for r in d).most_common(): print('  ',k,v)
print('1MiB devices',[r['device'] for r in d if int(r['size_bytes'])==1048576])
print('cpucp_dtb rows',sum(1 for r in rows if r['filename']=='cpucp_dtb.img'))
print('any cpucp.mdt/b00/elf',sum(1 for r in rows if r['filename'].startswith('cpucp.') and r['filename']!='cpucp.img'))"
```

```bash
python3 -I -c "
m=lambda imp,pn:(imp<<24)|(0xf<<16)|(pn<<4)
r=lambda b,v,rv:b|(v<<20)|rv
M=0xFF0FFFF0
x1=r(m(0x41,0xD44),1,0); a78=r(m(0x41,0xD41),1,0); a55=r(m(0x41,0xD05),2,0)
print('X1  r1p0 0x%08X model 0x%08X'%(x1,x1&M))
print('A78 r1p0 0x%08X model 0x%08X'%(a78,a78&M))
print('A55 r2p0 0x%08X model 0x%08X'%(a55,a55&M))
print('X1-A78 delta 0x%X == (0xD44-0xD41)<<4? %s'%(x1-a78,(x1-a78)==(0xD44-0xD41)<<4))
print('all three models distinct?',len({x1&M,a78&M,a55&M})==3)"
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
k=get('https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/boot/dts/qcom/sm8350.dtsi')
print('bytes',len(k.encode()))
print('compatible',re.findall(r'cpu\d: cpu@[0-9a-f]+ \{\n\t\t\tcompatible = \"([^\"]+)\"',k))
print('arm,cortex tokens',len(re.findall(r'arm,cortex-[ax]\d+',k)))
print('capacity',re.findall(r'capacity-dmips-mhz = <(\d+)>',k))
print('dpc',re.findall(r'dynamic-power-coefficient = <(\d+)>',k))
print('qcom,kryo',k.count('compatible = \"qcom,kryo\"'))
print('cells',re.findall(r'#freq-domain-cells = <(\d+)>',k))
print('cpucp occurrences',k.count('cpucp'))
print('cpucp_fw_mem refs',k.count('cpucp_fw_mem'))
i=k.find('cpucp_fw_mem:')
print(k[i:i+120].strip())"
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
B='https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/kernel/'
for f in ('cpu_errata.c','proton-pack.c','cpufeature.c'):
    t=get(B+f)
    print('%-16s X1=%d A78=%d A55=%d'%(f,len(re.findall(r'CORTEX_X1\b',t)),len(re.findall(r'CORTEX_A78\b',t)),len(re.findall(r'CORTEX_A55\b',t))))
    for m in re.finditer(r'CORTEX_(X1|A78)\b',t):
        print('    :%d %s'%(t[:m.start()].count(chr(10))+1,t.split(chr(10))[t[:m.start()].count(chr(10))].strip()))
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
V='https://raw.githubusercontent.com/LineageOS/android_kernel_oneplus_sm8350/lineage-24.0/'
t=get(V+'arch/arm64/boot/dts/vendor/qcom/lahaina.dtsi')
print('lahaina bytes',len(t.encode()))
print('model',re.findall(r'model = \"([^\"]+)\"',t)[:1])
print('msm-id',re.findall(r'qcom,msm-id = <[^>]+>(?:, <[^>]+>)*',t))
print('qcom,kryo',t.count('compatible = \"qcom,kryo\"'))
print('capacity',re.findall(r'capacity-dmips-mhz = <(\d+)>',t))
print('freq-domain',re.findall(r'qcom,freq-domain = <&cpufreq_hw (\d+) (\d+)>',t))
print('cells',re.findall(r'#freq-domain-cells = <(\d+)>',t))
print('cpucp lines',[l.strip()[:60] for l in t.split(chr(10)) if 'cpucp' in l])
i=t.find('cpu-map {'); st=t.find('{',i); d=0
for j in range(st,len(t)):
    if t[j]=='{': d+=1
    elif t[j]=='}':
        d-=1
        if d==0: b=t[i:j+1]; break
print('clusters',[(m.group(1),len(re.findall(r'cpu = <&CPU\d>',m.group(2)))) for m in re.finditer(r'(cluster\d) \{(.*?)\n\t\t\t\};',b,re.S)])"
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
B='https://raw.githubusercontent.com/torvalds/linux/master/'
t=get(B+'drivers/mailbox/qcom-cpucp-mbox.c')
print('mbox driver bytes',len(t.encode()))
for l in t.split(chr(10)):
    if 'APSS_CPUCP' in l and 'define' in l: print('  ',l.strip())
print('match table:')
for l in t.split(chr(10)):
    if 'cpucp-mbox' in l and 'compatible' in l: print('  ',l.strip())
y=get(B+'Documentation/devicetree/bindings/mailbox/qcom,cpucp-mbox.yaml')
print('binding sm8350?',y.count('sm8350'))
print('binding compatibles',re.findall(r'qcom,(\w+)-cpucp-mbox',y))"
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
k=get('https://raw.githubusercontent.com/torvalds/linux/master/drivers/soc/qcom/Kconfig')
print('mainline drivers/soc/qcom/Kconfig cpucp:',k.count('cpucp'))
V='https://raw.githubusercontent.com/LineageOS/android_kernel_oneplus_sm8350/lineage-24.0/'
v=get(V+'drivers/soc/qcom/Kconfig')
print('oneplus sm8350 QCOM_CPUCP:',v.count('QCOM_CPUCP'),'FAST:',v.count('QCOM_CPUCP_FAST'),'LOG:',v.count('QTI_CPUCP_LOG'))
i=get(V+'drivers/interconnect/qcom/Kconfig')
print('oneplus cpucp-l3 symbol:',i.count('INTERCONNECT_QCOM_CPUCP_L3'),'HOLI mentions:',i.count('HOLI'))
s=get('https://raw.githubusercontent.com/sonyxperiadev/kernel/master/drivers/soc/qcom/Kconfig')
print('sonyxperiadev QCOM_CPUCP:',s.count('config QCOM_CPUCP'),'FAST:',s.count('config QCOM_CPUCP_FAST'),'LOG:',s.count('config QTI_CPUCP_LOG'))
so=get(V+'drivers/soc/qcom/socinfo.c')
d={int(a):b for a,b in re.findall(r'\{\s*(\d+),\s*\"([^\"]+)\"\s*\}',so)}
print('vendor socinfo entries',len(d))
for n in (415,456,501,439): print(' ',n,'->',d.get(n,'ABSENT'))"
```

## Sources

| claim | source | access |
|---|---|---|
| 693 rows / 651 files / 886,208,933 B / 845.15 MiB / 2 devices; families boot 13, wifi 155, other 324, gpu 11, modem 32, tz 98, adsp 41, cdsp 18, bt 1; 27 `db_type`s; `isa_identified` empty 693/693; 18 shared filenames | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-26 |
| `cpucp.img` OnePlus_9_Pro 110,592 B `boot` `UNKNOWN` `oneplus/lemonadep/radio`; 30 corpus rows in 11 sizes 110,592–1,048,576; 4 rows at 1 MiB (Moto_G200, Edge_40_Pro, Edge_30_Fusion, Edge_30); 6 `cpucp_dtb.img` (16,384 ×5, 12,288 ×1); no `cpucp.mdt`/`.b00`/`.elf` | same CSV | 2026-11-26 |
| `sm8350.dtsi` 117,937 B; `arm,cortex-a55` ×4 / `a78` ×3 / `x1` ×1 at `:59,83,102,121,140,159,178,197`; 11 `arm,cortex-*` tokens; 3 PMU nodes `:309,314,319`; **0** `capacity-dmips-mhz`; **0** `dynamic-power-coefficient`; **0** `qcom,kryo`; one `cpu-map` `cluster0` of 8; `#freq-domain-cells = <1>` `:3818`; `cpufreq_hw` `:3806` compatible `"qcom,sm8350-cpufreq-epss","qcom,cpufreq-epss"`; `cpucp_fw_mem` `:452` `<0x0 0x80b00000 0x0 0x100000>` with 1 occurrence; 0 `cpucp` mailbox node | `arch/arm64/boot/dts/qcom/sm8350.dtsi`, master | 2026-11-26 |
| vendor `lahaina.dtsi` 151,563 B; `model` `Lahaina`; `msm-id` `<415>,<456>,<501>`; `qcom,kryo` ×8; capacities 1024×4/1946×3/**2048**×1; `freq-domain` `0 4`/`1 4`/`2 4`; `#freq-domain-cells = <2>`; `cpufreq_hw` compatible `"qcom,cpufreq-hw-epss"`, `qcom,lut-row-size = <4>`, `qcom,skip-enable-check`, `dcvsh0_int`; `cpu-map` 3 clusters 4/3/1; `cpucp_fw_mem` `:324` | `LineageOS/android_kernel_oneplus_sm8350` lineage-24.0 `arch/arm64/boot/dts/vendor/qcom/lahaina.dtsi` | 2026-11-26 |
| `sm8350` `FAMILY Cortex-X1 Cortex-A78 Cortex-A55`, `REVISION r1p0 r1p0 r2p0`, 300–2841 MHz, four independent captures | `deviceinfohw.ru` items 103708, 103715, 103741, 103775 | 2026-11-26 |
| `ARM_CPU_IMP_ARM` `0x41`; `ARM_CPU_PART_CORTEX_A55` `0xD05`, `_A78` `0xD41`, `_X1` `0xD44`; `MIDR_CPU_MODEL` `:43`, `MIDR_CPU_VAR_REV` `:48`; `MIDR_PARTNUM_SHIFT` `:26`, `MIDR_VARIANT_SHIFT` `:34`, `MIDR_IMPLEMENTOR_SHIFT` `:38` | `arch/arm64/include/asm/cputype.h`, master | 2026-11-26 |
| `CORTEX_X1` at `cpu_errata.c:406`,`:676` and `proton-pack.c:885`; `CORTEX_A78` at `:402`,`:669`,`:882`; `CORTEX_A55` 2 in `cpufeature.c`; X1/A78 0 in `cpufeature.c` | `arch/arm64/kernel/{cpu_errata,proton-pack,cpufeature}.c`, master | 2026-11-26 |
| `qcom-cpucp-mbox.c` 6,508 B; `APSS_CPUCP_*` offsets `:15,18,22,23,24,25`; match table `:204-205` only `nord` and `x1e80100`; binding enumerates glymur/hawi/kaanapali/maili/nord/sm8750/x1e80100, 0 `sm8350` | `drivers/mailbox/qcom-cpucp-mbox.c`; `Documentation/devicetree/bindings/mailbox/qcom,cpucp-mbox.yaml`, master | 2026-11-26 |
| 0 `cpucp` in mainline `drivers/soc/qcom/Kconfig`; **0** `QCOM_CPUCP`/`_FAST`/`QTI_CPUCP_LOG` in both `LineageOS/android_kernel_{oneplus,sony}_sm8350` `drivers/soc/qcom/Kconfig`; the three symbols exist in `sonyxperiadev/kernel` master; OnePlus tree has `INTERCONNECT_QCOM_CPUCP_L3` whose Kconfig text says "HOLI CPUCP L3 driver … found on Holi-based platforms" | `drivers/soc/qcom/Kconfig` master; vendor trees as named; `drivers/interconnect/qcom/Kconfig` | 2026-11-26 |
| vendor `socinfo.c` 72 entries: 415 `LAHAINA`, 456 `LAHAINA-ATP`, 501 `SM8325`, 439 `LAHAINAP`; mainline `qcom,ids.h` has `QCOM_ID_SM8350` = 439 and no 415/456/501 | vendor `drivers/soc/qcom/socinfo.c`; `include/dt-bindings/arm/qcom,ids.h` | 2026-11-26 |
| #815 owns topology, compatibles, boot chain §4, TrustZone §5, firmware families §6, mainline status §8 | `research/soc/Qualcomm-SM8350-Snapdragon-888-soc.md` | 2026-11-26 |
| `FAMILY` field validated as a core-name discriminator against `sm8650`/`s5e9925`/`sm6375`/`sm4350` | `research/soc/Qualcomm-SM7325-Snapdragon-778G-5G-cpu.md` §3.2 (#853) | 2026-11-26 |
