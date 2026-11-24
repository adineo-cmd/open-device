# Qualcomm SM7325 Snapdragon 778G 5G — SoC package: CPU, DSP, boot chain, TrustZone, firmware census

Issue #817. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative / [OPEN] unresolved. Every number is command output from a run on
**2026-11-24** against
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 data rows,
123 devices, 28 distinct SoC labels), `torvalds/linux` master, the
`linux-firmware` tree on `git.kernel.org`, and the postmarketOS `pmaports`
tree plus wiki on GitLab / wiki.postmarketos.org.

**No payload exists in this workspace and none was read.** Every statement below
is matrix metadata — filename, size, md5, `db_type`, family label — or public
GPL source, or a byte-length check on a public upstream file. No vendor ELF is
parsed here and no instruction is disassembled [N].

This is the **SoC-package** note for the `SM7325` label only — the two Motorola
devices `Edge_20` (`berlin`) and `Edge_2021` (`berlna`). GPU core identification
for this SoC is a separate, already-committed deliverable
(`research/soc/Qualcomm-SM7325-Snapdragon-778G-5G-gpu.md`, #2030) and is
**cited, never re-derived** — except where this slice flatly contradicts it,
which is §2.3 and is the largest single finding here.

## 0. Verdict

| question | answer | class |
|---|---|---|
| SoC identity | SM7325 = Snapdragon 778G; board codenames **`berlin`** (Edge 20) and **`berlna`** (Edge 2021) | [F] |
| SoC ID in mainline | **`QCOM_ID_SM7325` = 475** at `qcom,ids.h:239`, and `qcom_board_id(SM7325)` at `socinfo.c:480` | [F] |
| CPU topology | **1× Kryo 670 Prime + 3× Kryo 670 Gold + 4× Kryo 670 Silver**, 8 cores, 6 nm, 2021 — postmarketOS SoC page; DT gives 4/3/1 with three `freq-domain`s | [F] |
| CPU instruction-level ID | **standard ARM MIDRs only** — all 8 cores are `qcom,kryo`/`qcom,kryo670` in DT; per `cputype.h:241-246` the Kryo 6XX clusters report **A78 `0x410fd410`** (Gold), **A55 `0x410fd050`** (Silver) and **X1 `0x410fd440`** (Prime). **No Qualcomm-specific part number is encoded** — `cputype.h` has no `KRYO_6XX_*` part number at all | [F] for the mapping, [I] for the per-cluster split, [OPEN] for the Prime's real core |
| CPU cluster shape | **one `cpu-map` cluster, three `freq-domain`s, three `capacity-dmips-mhz` values (1024 / 1946 / 1985)** — the only SM7325-family DT in mainline and the first full one in this repo | [F] |
| `sm7325.dtsi` parent | **`kodiak.dtsi`, not `sc7280.dtsi`** — `sc7280.dtsi` was renamed by `dd6edcd7d3e4` on 2025-10-30 and **no longer exists** at master; 31 `sc7280*` board files remain against 1 `kodiak.dtsi` | [F] |
| GPU | Adreno 642L marketing / `adreno-635.0` DT / `0x06030500` chip ID / `7c3` helper — **cited from #2030** | [F] |
| GPU firmware mainline binds | `a660_sqe.fw` + `a660_gmu.bin` + `a660_zap.mbn` — **0 of 3 in this slice**; all three exist upstream, but `a660_zap.mbn` **only under `qcom/qcm6490/`**, not under any `qcom/sm7325/` path (§8.3) | [N, F] |
| GPU firmware the sibling ships | **`a660_sqe.fw` + `a660_gmu.bin` + `a660_zap.mdt`/`.b00`/`.b01`/`.b02` are all present on `Edge_30` (SM7325-AE)** — #2030's "zero rows in the entire matrix" was wrong about `.mdt`; it is true only of the `.mbn` spelling | [F] |
| DSP units in the slice | **2**: `adsp` (6 `bm2n` files) and, under `other`, `evass`/`evass-lt`/`vpu20_2v`/`vpu20_4v`. **No `cdsp`, no `venus`, no `ipa_fws`, no `slpi`, no `npu`, no `spss`** | [F] |
| DSP units mainline declares for this SoC | **5** on `kodiak.dtsi`: `mpss` `:3421`, `adsp` `:4466`, `wpss` `:4617`, `cdsp` `:4791`, `venus` `:5018` | [F] |
| Boot chain | **6 rows / 3 filenames / 251,674,624 B**; all 3 are exact-MiB partition dumps = **72.57%** of the whole slice | [F] |
| TrustZone family | **0 rows.** `tz`, `hyp`, `keymaster`, `devcfg`, `uefisecapp` — none appear anywhere in the slice | [N] |
| TZ layout available | **none from this slice**; the sibling `Edge_30` ships the 8.00/4.00/2.00 MiB trio, and `kodiak.dtsi:104` gives `hyp_mem` **6.00 MiB** @ `0x80000000` with **no `tz_mem`** | [F] |
| Split law `mdt == b00+b01` | **0 of 0 testable** — all 5 `.mdt` in the slice are single-file, no `.b00` sibling. The slice contributes nothing to the law either way | [N] |
| `.b00` header law | **not testable on this slice** (no `.b00` at all); applied to the sibling labels it covers all **39 `.b00` rows over 10 distinct sizes**, and every size resolves uniquely — 9 ELF32-only, 1 ELF64-only (512 B, 20 rows, `64+56×8`) | [N, F] |
| `mdt == b00+b01` with a `b02` present | the `b02` segment sits **outside** the `.mdt`; `mdt == b00+b01` still holds exactly on all 3 devices that have one | [F] |
| Monolithic-vs-split law (new) | a monolithic `.mdt` is **exactly `b00 + b01 − 152`** of the split form of the same stem — 10 of 10 stems where both forms exist and the arithmetic applies, offset **152 on all 10**, zero exceptions | [F] |
| `.mbn` in the corpus | **0 of 33,917 rows** | [N] |
| Mainline `sm7325.dtsi` | **exists**, 537 B, a CPU-only overlay rebinding 8 CPUs to `qcom,kryo670`; 8 DT entries match `sm7325`, 4 boards bind `qcom,sm7325` in `qcom.yaml:1129` | [F] |
| Mainline `berlin` / `berlna` board | **neither exists** — the 4 `qcom,sm7325` boards are `motorola,dubai`, `nothing,spacewar`, `xiaomi,lisa`, `xiaomi,taoyao` | [N] |
| postmarketOS device package | **none** — 0 of 1,273 `device/` dirs match `7325`, `kodiak`, `berlna`, or `778`; `berlin` matches only a **Huawei** device of that name | [N] |
| postmarketOS wiki | **pages exist** — SoC page with `mainline = yes` and a device page for `motorola-berlna`, but `packaged = no`, `pmoskernel` empty, and **every** status field blank | [F] |
| linux-firmware | `qcom/a660_gmu.bin` **200** (55,252 B), `qcom/a660_sqe.fw` **200** (43,292 B), `qcom/qcm6490/a660_zap.mbn` **200** (1,054,648 B); `qcom/a619_gmu.bin` **404**; `qcom/sm7325/` and `qcom/sm7325/motorola/dubai` **404** | [F, N] |

The findings new to this repository are §1.3 (the DT is 4+3+1 with three
`freq-domain`s, and the parent file was renamed), §1.5 (the Kryo 6XX MIDR
mapping means this SoC has *no* vendor-private CPU part numbers), §2.3 (the
sibling **does** ship the a660 firmware set, correcting #2030's `[N]`), §4.2
(`dsp.img` is a 64 MiB partition dump that is `other`, not `adsp`), §5.2 (zero
TZ rows plus a sibling trio plus a 6 MiB `hyp_mem`), and §7.2 (a
**monolithic-vs-split** container law that the previous three SoC notes did not
name).

> **Companion note.** This file covers `SM7325` (778G) only. The two other
> `SM7325*` labels in the matrix — `SM7325-AE Snapdragon 778G 5G` (Edge_30, 338
> rows) and `SM7325-AE Snapdragon 778G+ 5G` (Phone_1, 475 rows) — are **not**
> in this slice and are cited only where they answer a question this slice
> cannot (§2.3, §3.3, §5.2). A separate note would own them.

## 1. CPU: 4+3+1, and why the core IDs are standard ARM numbers

### 1.1 The topology, from public spec

The 778G is an 8-core part in a **1+3+4** arrangement — one prime, three gold,
four silver — on a 6 nm process, launched 2021 [F] (postmarketOS SoC page,
retrieved 2026-11-24; Qualcomm product page).

| source | cores | clocks | process | class |
|---|---|---|---|---|
| postmarketOS wiki, `Qualcomm_Snapdragon_778G/778G+/782G_(SM7325)` | 1× 2.4 GHz Kryo 670 Prime + 3× 2.2 GHz Kryo 670 Gold + 4× 1.9 GHz Kryo 670 Silver | 2.4 / 2.2 / 1.9 GHz | 6 nm | [F] |
| postmarketOS wiki, `Motorola_Edge_2021_(motorola-berlna)` | same 1+3+4 shape, Kryo 670 | 2.4 / 2.2 / 1.9 GHz | — | [F] |
| `kodiak.dtsi` (mainline) | 4 + 3 + 1 by `capacity-dmips-mhz` and `freq-domain` | see §1.2 | — | [F] |

The 1+3+4 reading and the DT's 4+3+1 reading are the **same topology described
from opposite ends**: four silver cores at the bottom, three gold in the middle,
one prime at the top. There is no contradiction [F].

### 1.2 Mainline gives a real `cpu-map`, three `freq-domain`s and three capacities

Unlike SM4375 (#811), which has **no** device tree at all in mainline, SM7325 is
one of the best-described parts in this repo. `kodiak.dtsi` (202,322 B) declares
eight CPUs with distinct capacity and frequency-domain values [F]:

| cpu | `reg` | `capacity-dmips-mhz` | `dynamic-power-coefficient` | `operating-points-v2` | `freq-domain` |
|---|---|---|---:|---|---:|
| cpu0 | `0x0 0x0` | 1024 | 100 | `cpu0_opp_table` | 0 |
| cpu1 | `0x0 0x100` | 1024 | 100 | `cpu0_opp_table` | 0 |
| cpu2 | `0x0 0x200` | 1024 | 100 | `cpu0_opp_table` | 0 |
| cpu3 | `0x0 0x300` | 1024 | 100 | `cpu0_opp_table` | 0 |
| cpu4 | `0x0 0x400` | **1946** | **520** | `cpu4_opp_table` | **1** |
| cpu5 | `0x0 0x500` | 1946 | 520 | `cpu4_opp_table` | 1 |
| cpu6 | `0x0 0x600` | 1946 | 520 | `cpu4_opp_table` | 1 |
| cpu7 | `0x0 0x700` | **1985** | **552** | `cpu7_opp_table` | **2** |

Three `capacity-dmips-mhz` values, three `dynamic-power-coefficient` values,
three `operating-points-v2` tables, three `qcom,freq-domain` indices — **four,
three, one** [F]. The OPP table maxima are 2.016 / 2.611 / 3.014 GHz, which is
*higher* than the marketing clocks and matches the pattern that the DT lists
silicon limits while the SKU fuse sets the shipped clock [I].

There is exactly **one** `cpu-map` cluster, with eight `coreN` children, and the
per-cluster structure exists only via `freq-domain` and `capacity-dmips-mhz`,
not via a second `clusterN` [F]:

```
$ grep -c 'qcom,freq-domain = <&cpufreq_hw ' kodiak.dtsi      -> 8
$ grep -o 'qcom,freq-domain = <&cpufreq_hw [0-9]' | sort -u   -> 0, 1, 2  (three)
$ grep -c 'capacity-dmips-mhz'                                -> 8
$ distinct capacity values                                    -> 1024, 1946, 1985
$ grep -c '\t\t\tcluster[0-9]\+ {'                            -> 1
$ grep -c '\t\t\t\tcore[0-9]\+ {'                             -> 8
```

`cpufreq_hw` advertises `#freq-domain-cells = <1>` and three `dcvsh-irq-N`
interrupts — one per domain [F] (`kodiak.dtsi:7124-7130`). The driver side is
`qcom,cpufreq-epss` (`drivers/cpufreq/qcom-cpufreq-hw.c:441`), whose
`epss_soc_data` reads a `per_domain` register block, so the three-domain shape
is not cosmetic [F] for the compatible, [I] for the register layout.

### 1.3 `sm7325.dtsi` is a 537-byte overlay, and its parent was renamed

`sm7325.dtsi` contains nothing but SPDX, two copyright lines, one `#include` and
eight one-line `&cpuN` overrides [F]:

```dts
#include "kodiak.dtsi"

/* SM7325 uses Kryo 670 */
&cpu0 { compatible = "qcom,kryo670"; };
...
&cpu7 { compatible = "qcom,kryo670"; };
```

8 of 8 CPUs rebound to `qcom,kryo670`, and `qcom,kryo670` appears **zero** times
in `kodiak.dtsi` itself — the base file uses plain `qcom,kryo` on all eight and
only the SoC-level overlay names the generation [F]:

```
$ grep -c 'compatible = "qcom,kryo670";' sm7325.dtsi   -> 8
$ grep -c 'kryo670'                      kodiak.dtsi  -> 0
$ grep -c 'compatible = "qcom,kryo";'    kodiak.dtsi  -> 8
```

**The parent file name is a trap.** The original patch series (v1 2024-07-29,
v3 2024-10-20, both in the RULE 0 record) added `sm7325.dtsi` with
`#include "sc7280.dtsi"`. At `torvalds/linux` master today that file does not
exist — commit `dd6edcd7d3e4` (`arm64: dts: qcom: rename sc7280 to kodiak`,
2025-10-30) renamed it, and the 31 surviving `sc7280*` entries are all board
`.dts`/`.dtsi` files, not the SoC include [F]:

```
arch/arm64/boot/dts/qcom listing, 664 entries
  sc7280.dtsi   -> absent
  kodiak.dtsi   -> present
  entries starting "sc7280" -> 31  (boards only)
```

So any analysis keyed on the patch text, on a distro tree older than 2025-10-30,
or on a grep for `sc7280.dtsi` will find the wrong file. The mapping is
**SM7325 ⊂ SC7280/QCM6490/QCS6490 ⊂ Kodiak**, and Kodiak is the current name
[F].

### 1.4 Kryo 670 is not a core ID — the MIDRs are standard ARM part numbers

This is the substantive difference from SM4375, and it answers the issue's
"CPU core identification with instruction-level proof where possible" directly.

`arch/arm64/include/asm/cputype.h:241-246` states the mapping outright [F]:

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

Kryo 670 is a **6XX** part. So:

| cluster | marketing | `cputype.h` says it reports | MIDR encoding | MIDR value |
|---|---|---|---|---|
| Prime (1×) | Kryo 670 Prime | `MIDR_CORTEX_X1` (`ARM_CPU_PART_CORTEX_X1` = `0xD44`) | `MIDR_CPU_MODEL(0x41, 0xD44)` | **`0x410fd440`** |
| Gold (3×) | Kryo 670 Gold | `ARM_CPU_PART_CORTEX_A78` = `0xD41` | `MIDR_CPU_MODEL(0x41, 0xD41)` | **`0x410fd410`** |
| Silver (4×) | Kryo 670 Silver | `MIDR_CORTEX_A55` = `0xD05` | `MIDR_CPU_MODEL(0x41, 0xD05)` | **`0x410fd050`** |

`MIDR_CPU_MODEL(imp, partnum)` is `((imp) << 24) | (0xf << 16) | ((partnum) << 4)`
— implementor, the fixed **architecture nibble `0xf`**, and part number, with the
variant and revision fields left zero (`cputype.h:30,43-47`) [F]. The `0xf` is the
ARMv8 architecture field, which is why every value below has `f` in bits 19:16
and why dropping it yields a wrong number:

```
$ python3 -I -c "
m=lambda imp,pn:(imp<<24)|(0xf<<16)|(pn<<4)
print('X1  0x%08x'%m(0x41,0xD44))
print('A78 0x%08x'%m(0x41,0xD41))
print('A55 0x%08x'%m(0x41,0xD05))"
X1  0x410fd440
A78 0x410fd410
A55 0x410fd050
```

The X1 row is a `cputype.h` mapping only; this note does not claim the 778G's
prime core is literally an X1 (the 1+3+4 Kryo 670 Prime is a vendor-named core,
§1.1) [OPEN].

The **engineering consequence** is what matters: there is **no**
`QCOM_CPU_PART_KRYO_6XX_*` in `cputype.h`. The only Qualcomm-private part
numbers are `KRYO_2XX_GOLD` `0x800`, `KRYO_3XX_SILVER` `0x803`,
`KRYO_4XX_GOLD` `0x804`, `KRYO_4XX_SILVER` `0x805` [F]. Kryo 6XX is absent from
that list, so a Kryo 670 core is **indistinguishable from a stock Cortex-A78 or
Cortex-A55 by MIDR alone** [F]. That, and not a lab gap, is why the matrix's
`isa_identified` column is empty on all 67 rows of this slice (§6.5) and why a
per-SoC "core ID" for this part is a legal identity rather than a silicon
fingerprint [I].

Two corollaries [F]:

1. `cpufeature.c` has **zero** occurrences of `CORTEX_A78` (it appears in no
   erratum or mitigation list at all), while `CORTEX_A55` appears at `:1695` in
   the KPTI-safe list (`kpti_safe_list`, `unmap_kernel_at_el0`) and again at
   `:1869` in the **broken-DBM erratum** list (`cpu_has_broken_dbm`, guarded by
   `CONFIG_ARM64_ERRATUM_1024718`); `MIDR_QCOM_KRYO_4XX_SILVER` appears at
   `:1704` and `:1871`. So this SoC's Silver cores are two distinct cases
   depending on which core they are — an A55 is KPTI-safe *and* carries the DBM
   erratum, while a Kryo 4XX Silver has its own entries — and the Gold cores
   need no workaround at all [F].
2. `Documentation/devicetree/bindings/arm/cpus.yaml` lists `qcom,kryo670` at
   `:224` among 17 enumerated `kryo` values (`kryo240`…`kryo780`) plus a plain
   `qcom,kryo` escape hatch at `:243`. So `qcom,kryo670` is a **documented**
   binding, not a free-form string [F].

### 1.5 What the "instruction-level proof" question actually resolves to

The issue asks for instruction-level proof "where possible". For CPU identity on
this SoC the honest answer is **it is not the right instrument** [N]:

- The matrix holds **no** CPU-bearing payload for these devices. The only
  executable-class rows are four 8 KB `.mdt` GPU/DSP containers (§2, §3) and a
  64 MiB `dsp.img` partition dump that is not parsed here [F].
- A MIDR is a *register* read, not an instruction stream. Proving "this core is
  an A78" from bytes would mean finding the MIDR read path in a kernel or
  bootloader binary and disassembling around `MRS x0, MIDR_EL1` — for which no
  payload exists in this slice [N].
- The identity is therefore established **from the binding + the documented
  mapping** (`qcom,kryo670` → Kryo 6XX → A78/A55 MIDRs) and not from bytes [F
  for the mapping, I for applying it to this part].

That is a weaker claim than SM4375's, and it is the correct one: SM4375's MIDR
was arithmetic on a *public spec* with no DT to confirm it; SM7325's is
arithmetic on a *documented kernel mapping* with a DT that confirms the Kryo 6XX
family but not the individual part number [I].

## 2. GPU — cited from #2030, plus one correction this slice forces

### 2.1 The identity, four names deep

Cited, not rebuilt: `research/soc/Qualcomm-SM7325-Snapdragon-778G-5G-gpu.md`
(#2030) establishes that the SM7325 GPU is [F]:

| register | value |
|---|---|
| marketing | Adreno 642L |
| mainline DT compatible | `qcom,adreno-635.0` at `kodiak.dtsi:3217` |
| chip ID, derived | `0x06030500` |
| catalog firmware binding | `a660_sqe.fw` + `a660_gmu.bin`, `.zapfw = "a660_zap.mbn"` |
| code helper | `adreno_is_7c3()` — `chip_ids[0] == 0x06030500` |

Re-verified this session against master: `a6xx_catalog.c:1124-1142` still reads
`.chip_ids = ADRENO_CHIP_IDS(0x06030500)`, `.family = ADRENO_6XX_GEN4`, the two
`a660_*` firmware names, `.zapfw = "a660_zap.mbn"`, and **no `.revn`** [F]. There
are still exactly **three** `.machine =` strings in the whole catalog
(`qcom,sm7150` `:820`, `qcom,sm4350` `:870`, `qcom,sm6375` `:895`) — **no
`qcom,sm7325` entry**, which is why the chip ID, not the machine, is the join
key [F].

### 2.2 This slice has eight `gpu` rows over four filenames, and none is the right firmware

8 gpu-family rows across the two devices (4 per device), 4 distinct filenames,
byte-identical between `berlin` and `berlna` [F]:

| file | bytes | md5 | `db_type` | belongs to |
|---|---:|---|---|---|
| `a615_zap.mdt` | 6,708 | `222f87861803bae8de24f0eb28bfc0d2` | ELF64 | the a615 entry, `a6xx_catalog.c:801` |
| `a619_gmu.bin` | 32,768 | `9e23c52057bb573dee9ba31f1fdba4fa` | GPU | the a619 entries, `:876`/`:901`/`:925` |
| `a630_sqe.fw` | 32,456 | `21693ef6f2d686ce79ebb3716a099970` | GPU | the a610/a615/a630 entries |
| `sequence_manifest.bin` | 5,704 | `252630742d895255d66b5be984bdabda` | UNKNOWN | vendor KBC manifest, no `adreno` loader |

Zero of the three names mainline needs for `0x06030500` are present [F]. This
re-confirms #2030 §3 without adding to it.

### 2.3 The correction: the sibling ships the entire a660 set, so #2030's `[N]` was too strong

#2030 §3.1 argued that the absence might be a census gap and anchored that on
one claim: "`a660_zap.mbn` appears on **zero** devices in the entire 33,917-row
matrix". That claim is **true but misleading**, and the surrounding
`a660_*` picture is the opposite of what it implies [F]:

```
a660_zap.mbn   0 rows   (the .mbn spelling: genuinely zero)
a660_zap.mdt  21 rows   21 devices
a660_zap.b00   3 rows   Edge_30, Edge_30_Fusion, Moto_G200
a660_zap.b01   3 rows   same three
a660_zap.b02   3 rows   same three
a660_gmu.bin  21 rows   21 devices
a660_sqe.fw   30 rows   30 devices
```

So `a660_zap` **is** in the corpus — as `.mdt` on 21 devices and as a full
three-segment split on three of them. The `.mbn` spelling is zero because the
corpus contains **no `.mbn` file at all**: 0 of 33,917 rows carry that extension
[F]. #2030 generalised from a spelling to a family, and the family is present.

`Edge_30` (`dubai`, SM7325-AE — the same `sm7325.dtsi` family, one SKU up)
carries all six [F]:

| file | bytes | `db_type` | `db_path` |
|---|---:|---|---|
| `a660_zap.b00` | 148 | ELF64 | `motorola/dubai/modem/image` |
| `a660_zap.b01` | 6,712 | UNKNOWN | same |
| `a660_zap.b02` | 1,976 | UNKNOWN | same |
| `a660_zap.mdt` | 6,860 | ELF64 | same |
| `a660_gmu.bin` | 55,256 | **AUDIO** | same |
| `a660_sqe.fw` | 40,496 | **AUDIO** | same |

And the container law holds on all three devices that have the split [F]:

```
Edge_30          mdt=6860  b00+b01=148+6712=6860  MATCH
Edge_30_Fusion   mdt=6860  b00+b01=6860           MATCH
Moto_G200        mdt=6860  b00+b01=6860           MATCH
```

with `b02 = 1,976` sitting **outside** the `.mdt` — a fact §7.1 returns to [F].

**So the verdict on #2030 §3.1 changes**: the SM7325 GPU firmware absence is a
**census-scope gap**, not a property of the hardware [I]. A device that ships
`sequence_manifest.bin` from a `vendor/gpu/kbc` path and an a619/a630 set is
shipping a *coherent but wrong-generation* vendor set, and the sibling proves the
same SoC family can and does ship the right one [F for the sibling, I for the
reading].

**Two mislabels fall out of this, and they are the same defect class #811
found** [F]:

1. **`db_type = AUDIO` on 21 of 21 `a660_gmu.bin` rows and 30 of 30
   `a660_sqe.fw` rows.** Every one of those 51 rows is in `blob_family=gpu`. The
   corpus's GPU firmware is typed as audio. Corpus-wide, `AUDIO` inside
   `blob_family=gpu` is **79 rows over exactly 4 filenames** —
   `a660_gmu.bin` 21, `a660_sqe.fw` 30, `a650_gmu.bin` 14, `a650_sqe.fw` 14 —
   and `AUDIO` inside `blob_family=modem` is **0**. So the defect is
   per-filename-generation, not per-row: every `a6[56]0_{gmu,sqe}` file
   anywhere in the corpus is mistyped, and nothing else is [F].
2. **`a660_zap.b00` = 148 is typed `ELF64` but 148 is an ELF32-header size.**
   `(148 − 52) / 32 = 3` exactly; `(148 − 64) / 56 = 1.5`, not an integer. Under
   the law #811 §7.2 established (`52+32N` for ELF32, `64+56N` for ELF64), 148
   is **ELF32 with 3 program headers** [F]. All 3 `a660_zap.b00` rows say
   ELF64. (The same 148-byte size is used by `a610_zap`, `a615_zap`, `a740_zap`,
   `spss1p/1t/2p` and the `*_dtb` splits — 76 rows over 39 devices corpus-wide,
   of which 50 carry the `ELF64` tag and 26 do not — see §7.3.)

**One more thing this lets me settle**: upstream linux-firmware's
`qcom/a660_gmu.bin` is **55,252 B** with md5
`cd3a235218418f51360888637c1cb2ac` [F]. Exactly **one** corpus row matches it
byte-for-byte: `FP5` (`QCM6490`). The other 20 rows are 55,256 B
(md5 `179caf2e…`, 19 rows) or 53,672 B (`Nord_200`). So the corpus's dominant
`a660_gmu.bin` build is **4 bytes different** from upstream's, and only one
device in 21 ships the upstream build [F]. That is a build-version axis the
filename-keyed census cannot see, and it is why size alone is not a fingerprint
[I].

## 3. DSP: two units in the slice, five remoteprocs in mainline

### 3.1 What the slice has

The `adsp` family is **12 rows / 6 filenames / 17,746,432 B** — and all six
filenames are `bm2n` [F]:

| file | bytes | md5 | on both devices? |
|---|---:|---|---|
| `bm2n06.bin` | 864,824 | `9010bb1a…` | yes, identical |
| `bm2n08.bin` | 3,091,896 | `1275a2d2…` | yes, identical |
| `bm2n12.bin` | 2,623,528 | `5c86c8fc…` | yes, identical |
| `bm2n13.bin` | 1,106,944 | `bf635d90…` | yes, identical |
| `bm2n14.bin` | 103,168 | `805176af…` | yes, identical |
| `bm2n15.bin` | 1,082,856 | `2ce8163c…` | yes, identical |

All six are `db_type = MODEM` despite being in `blob_family = adsp` [F] — the
same family/type disagreement #811 recorded (`adsp` is `MODEM` on 3,281 of
3,281 rows corpus-wide). Here it is 12 of 12 [F].

Indices `{06, 08, 12, 13, 14, 15}` — six of the sixteen `bm2n` slots, missing
`00`–`05`, `07`, `09`–`11`. This is the **canonical six-file `bm2n` set** that
#811 found on 11 SoC labels at exactly 6 files each [F]; SM7325 is another member
of that group [I].

Under `other` sit four more DSP-looking containers, 8 rows [F]:

| file | bytes | `db_type` | subfamily |
|---|---:|---|---|
| `evass.mdt` | 8,068 | ELF64 | misc |
| `evass-lt.mdt` | 8,068 | ELF64 | misc |
| `vpu20_2v.mdt` | 8,068 | ELF64 | media |
| `vpu20_4v.mdt` | 8,068 | ELF64 | media |

All four are **single-file 8,068-byte `.mdt`** with no `.b00` sibling on either
device [F]. That is the untestable class from #811 §7.1 — see §7.1.

`evass` is the video/audio split-processor container (`venus`/`vpu` family
naming), and `vpu20_2v`/`vpu20_4v` are the 2-variant and 4-variant video
processing units [I from the filename grammar; the container shape is [F]].

### 3.2 What the slice does not have — and it is a lot

Zero rows for each of [N]:

```
cdsp    0 rows     (338 on the SM7325-AE sibling, 475 on the 778G+)
venus   0 rows     (the venus.mdt family exists in the corpus, 8,068 B)
ipa_fws 0 rows     (the yupik_ipa_fws name exists in the corpus)
slpi    0
npu     0
spss1p  0
spss2p  0
modem   0 rows     (the whole family: 0 of 67 rows)
tz      0 rows     (see §5)
```

`modem` at **0 rows** is the most striking: on SM4375 the `modem` family was 44
rows / 68.05% of the slice, and on the SM7325-AE sibling it is 37 rows. Here it
is absent entirely, and the only modem-adjacent content is the six `bm2n` DSP
files and the `db_type=MODEM` label on them [F]. This is a census-scope gap of
the same shape as §2.3 — the `radio` directory on `berlna` holds a 64 MiB
`dsp.img` and a 2 MiB `bluetooth.img`, but no `modem.img` [F].

### 3.3 Mainline declares five remoteprocs and one video codec for this SoC

`kodiak.dtsi` is far more complete than any sibling in this repo [F]:

| node | line | compatible | memory region |
|---|---:|---|---|
| `remoteproc_mpss` | `:3421` | `qcom,sc7280-mpss-pas` | `mpss_mem` 246.00 MiB @ `0x8b800000` |
| `remoteproc_adsp` | `:4466` | `qcom,sc7280-adsp-pas` | `adsp_mem` 40.00 MiB @ `0x86700000` |
| `remoteproc_wpss` | `:4617` | `qcom,sc7280-wpss-pas` | `wpss_mem` 25.00 MiB @ `0x9ae00000` |
| `remoteproc_cdsp` | `:4791` | `qcom,sc7280-cdsp-pas` | `cdsp_mem` 30.00 MiB @ `0x88f00000` |
| `venus` | `:5018` | `qcom,sc7280-venus` | `video_mem` 5.00 MiB @ `0x8b200000` |

So mainline expects **four remoteprocs plus a video codec** where the slice has
**two DSP families** [F]. The delta is exact:

- `cdsp`: mainline declares it, slice has 0 rows [N].
- `venus`: mainline declares `qcom,sc7280-venus` as a proper `video-codec`
  node, slice has 0 venus rows — but the slice *does* have `vpu20_2v` and
  `vpu20_4v` under `other` [F]. Whether those are the venus firmware under a
  vendor name is [OPEN]; `venus.mdt` and `vpu20_*.mdt` are both 8,068 B in the
  corpus, which is suggestive and not proof [I].
- `wpss`: mainline declares it (the WLAN subsystem), slice has 0 `wpss` rows
  [N] — but `aoa_cldb_*` and the BT/WLAN files are in `wifi`/`bt`, §3.4.
- `mpss`: mainline declares it, slice has 0 `modem` rows [N].
- `adsp`: **the one that matches** — mainline declares `qcom,sc7280-adsp-pas`
  and the slice's only real DSP family is `adsp` [F].

`qcom_q6v5_pas.c` maps the four compatibles to shared resource tables rather
than per-SoC ones [F]:

```
:2025  { .compatible = "qcom,sc7280-adsp-pas", .data = &sm8350_adsp_resource },
:2026  { .compatible = "qcom,sc7280-cdsp-pas", .data = &sm6350_cdsp_resource },
:2027  { .compatible = "qcom,sc7280-mpss-pas", .data = &mpss_resource_init  },
:2028  { .compatible = "qcom,sc7280-wpss-pas", .data = &sc7280_wpss_resource }
```

Note `sc7280-adsp-pas` borrows the **SM8350** resource table and
`sc7280-cdsp-pas` borrows **SM6350**'s — only `wpss` gets a `sc7280`-specific
table (`:1764`). So on this SoC three of four remoteprocs are described by
another SoC's register layout, and only the WPSS is bespoke [F]. That is a real
"this is the same silicon re-badged" signal, and it is the remoteproc analogue of
§1.4's MIDR story [I].

### 3.4 The BT and WLAN families are complete and byte-identical across both devices

`bt` is 8 rows / 4 filenames / 4,622,684 B, and `wifi` is 4 rows / 2 filenames /
3,359,424 B, with **every md5 identical** between `berlin` and `berlna` [F]:

| file | family | bytes | md5 |
|---|---|---:|---|
| `bluetooth.img` | bt | 2,097,152 | `dc930f4e…` (Edge_20) / `ff5763bd…` (Edge_2021) — **different** |
| `msbtfw10.tlv` | bt | 58,732 | `c961de05…` |
| `msbtfw11.tlv` | bt | 155,420 | `aa679b9c…` |
| `msbtfw11.ver` | bt | 38 | `c295ac65…` |
| `aoa_cldb_falcon.bin` | wifi | 839,856 | `68e130d4…` |
| `aoa_cldb_swl14.bin` | wifi | 839,856 | `d17b34b2…` |

The one exception is `bluetooth.img` — the **partition dump** differs between
devices while the three `msbtfw*` patch files inside it are shared [F]. That is
the same pattern as `boot.img` in §4.1: partition dumps are per-build, the
firmware payloads are fleet artifacts [I].

`msbtfw*` decodes to **WCN6750** through the lab's `btqca.c` rampatch-prefix
rule (`research/soc/per-soc-method-plans.md` §8), which matches the mainline DT:
`sm7325-motorola-dubai.dts:1385` declares `compatible = "qcom,wcn6750-bt"` and
`:280` declares `qcom,wcn6750-pmu` [F]. So the BT chip is **WCN6750**, confirmed
from two independent directions [F].

`aoa_cldb_falcon.bin` / `aoa_cldb_swl14.bin` are 839,856 B each and appear on
**17 devices** corpus-wide, all at exactly that size [F]. They are the WLAN
coexistence calibration database, and their two names are the two supported
coexistence configurations (`falcon`, `swl14`) [I]. **Neither device ships any
`bdwlan*` file** — 0 rows [N] — while the SM7325-AE sibling ships 29 [F]. So
the WLAN calibration on this slice is the *coex* database only, not the
per-board `bdwlan` binary (§6.4).

## 4. Boot chain: three files, three exact-MiB dumps, 72.57% of the slice

### 4.1 The three images

| file | bytes | MiB | `db_type` | md5 |
|---|---:|---:|---|---|
| `boot.img` | 100,663,296 | 96.00 | BOOT | `1b713bfa…` / `c1dacc98…` |
| `dtbo.img` | 25,165,824 | 24.00 | DTB | `14b95f35…` / `801c238a…` |
| `vbmeta.img` | 8,192 | 0.0078 | AVB | `f213b38d…` / `b4b6addf…` |

6 rows, 3 filenames, **251,674,624 B = 72.57% of the entire slice** [F]. All
three sizes are corpus-modal constants, and all six md5s are unique to their
device [F]:

```
boot.img   100,663,296 -> 53 devices corpus-wide share the size
dtbo.img    25,165,824 -> 72 devices share the size
vbmeta.img       8,192 -> 93 devices share the size
```

So the boot family is **3 files of pure size-constant partition dump plus
per-build content**, and nothing about the internal layout is knowable from
metadata [N]. This matches the independent device-level analysis already in
`docs/devices/motorola/Edge_2021/boot.md` (#916), which is cited rather than
rebuilt.

**`boot.img` at 96 MiB is not evidence of anything about the kernel.** It is the
Qualcomm radio-partition magnitude; 53 corpus devices share it across at least
six SoC families [F]. The kernel version, page size, and GKI generation all
remain [OPEN] without a payload — the same conclusion #916 reached for `berlna`
alone, now confirmed to be a property of the size class and not of the device
[I].

### 4.2 `dsp.img` is a 64 MiB partition dump, and it is mislabelled `other`

`Edge_2021` alone carries `dsp.img` at **67,108,864 B = 64.00 MiB**, the
single largest non-boot row in the slice and **19.35%** of it [F]. It is typed:

```
blob_family = other
blob_subfamily = (empty)
db_type = UNKNOWN
db_path = motorola/berlna/radio
md5 = 4a82a6560998770cb7961fc37e5f5680
```

It is the only row in the slice whose family is `other` and whose `db_path` is
`radio` — every other `radio` row on `berlna` is `boot` or `bt` [F]. Corpus-wide
`dsp.img` is **61 rows / 61 distinct devices**, at exactly two sizes: 33,554,432
(23 rows) and 67,108,864 (38 rows) — i.e. 32 MiB and 64 MiB [F]. **All 61 are
`blob_family = other`** [F].

So the corpus consistently files the DSP partition dump as `other` while filing
the `bm2n` payloads as `adsp` [F]. That is arguably correct (a partition image is
not a firmware family) and arguably wrong (it is the ADSP partition) — the point
is that **a family-keyed census will miss `dsp.img` entirely**, and on `berlna`
it is the second-largest file in the device's census [I]. This is a census
blind spot worth naming: 38 devices ship 64 MiB of unclassified DSP partition
dump [F].

### 4.3 `rpm.img`, `aop.img`, `xbl`, `abl` — all absent

Zero rows for `rpm.img`, `aop.img`, `xbl.img`, `abl.img`, `xbl_config.img`,
`qupfw.img`, `aop_config.img`, `devcfg.img`, `keymaster.img`, `hyp.img`,
`tz.img`, `uefisecapp.img`, `prov.img`, `storsec.img`, `init_boot.img`,
`vendor_boot.img`, `recovery.img`, `super.img`, `devinfo.img` [N].

That is **6 boot rows out of the 8-image boot set** SM4375 shipped (#811 §4).
The only pre-AOP marker that would have been testable — `rpm.img` — is absent,
so this slice cannot contribute to that law either way [N].

## 5. TrustZone: zero rows, and a sibling that has the whole set

### 5.1 The honest negative

**The `tz` family is 0 rows in this slice** [N]. No `tz.img`, no `tz.mdt`, no
`hyp.img`, no `keymaster.img`, no `devcfg.img`, no `uefisecapp.img`, no
`cmnlib`, no `qsee`, no `sbl1`, no `tzbsp`. Grepping the 67 filenames for the
repo's TZ grammar returns nothing [N].

This is already documented device-first in
`docs/devices/motorola/Edge_2021/tz.md` (#922), which correctly identifies it
as a **census-scope gap, not structural absence**: `berlna`'s LineageOS
`proprietary-firmware.txt` lists exactly two files (`BTFM.bin`, `dspso.bin`),
and the TEE images are flashed to their own partitions and never read as files
by Android. This note re-establishes the same finding from the matrix side and
adds the SoC-level corroboration below; it does not re-derive #922.

### 5.2 The sibling ships the full TZ set, and the 8/4/2 trio is a fleet constant

`Edge_30` (`dubai`, SM7325-AE — same `sm7325.dtsi`, one SKU up) carries [F]:

| file | bytes | MiB |
|---|---:|---:|
| `hyp.img` | 8,388,608 | **8.00** |
| `tz.img` | 4,194,304 | **4.00** |
| `uefisecapp.img` | 2,097,152 | **2.00** |
| `keymaster.img` | 524,288 | 0.50 |
| `devcfg.img` | 131,072 | 0.125 |
| `aop.img` | 524,288 | 0.50 |

The 8.00 / 4.00 / 2.00 MiB triple is the exact trio #811 §5.2 found on **11
devices across 6 SoC labels**, and `Edge_30` is one of the 11 [F]. Re-verified
this session:

```
devices with hyp.img == 8388608 AND tz.img == 4194304 AND uefisecapp.img == 2097152
  -> 11 devices
  -> 11 distinct hyp.img md5s (zero sharing)
  -> SoC labels: SM6375 x4, blank x2, SM8350-AC, SM8550, SM7250, SM7325-AE, SM4375
```

**So the 8/4/2 trio is present on an SM7325-family device, and `berlna` is
simply not one of the 11.** The absence is a census artefact with a
one-SKU-away counterexample on the same device tree [F].

Note the outlier: `Phone_1` (SM7325-AE Snapdragon 778G+, the *other* sibling)
ships completely different sizes — `hyp` 3,678,208, `tz` 3,723,264,
`uefisecapp` 126,976, `aop` 208,896 [F]. So "the trio" is **not** a property of
the SoC; it is a property of the OEM's partition-flashing pipeline [I]. Eleven
devices sharing it across six SoCs, and one device on the same SoC not sharing
it, is the cleanest available evidence for that [F].

### 5.3 The mainline memory map: `hyp_mem` is 6.00 MiB and there is no `tz_mem`

`kodiak.dtsi`'s `reserved-memory` node has **19 direct children, 18 of them
carrying a `reg`**, summing **390,217,728 B = 372.14 MiB**; the one child with no
`reg` is `adsp_rpc_remote_heap_mem` [F]:

| region | base | bytes | MiB |
|---|---|---:|---:|
| `wlan_ce_mem` | `0x004cd000` | 4,096 | 0.0039 |
| `hyp_mem` | `0x80000000` | 6,291,456 | **6.00** |
| `xbl_mem` | `0x80600000` | 2,097,152 | 2.00 |
| `aop_mem` | `0x80800000` | 393,216 | 0.375 |
| `aop_cmd_db_mem` | `0x80860000` | 131,072 | 0.125 |
| `reserved_xbl_uefi_log` | `0x80884000` | 65,536 | 0.0625 |
| `sec_apps_mem` | `0x808ff000` | 4,096 | 0.0039 |
| `smem_mem` | `0x80900000` | 2,097,152 | 2.00 |
| `cpucp_mem` | `0x80b00000` | 1,048,576 | 1.00 |
| `wlan_fw_mem` | `0x80c00000` | 12,582,912 | 12.00 |
| `adsp_mem` | `0x86700000` | 41,943,040 | 40.00 |
| `cdsp_mem` | `0x88f00000` | 31,457,280 | 30.00 |
| `video_mem` | `0x8b200000` | 5,242,880 | 5.00 |
| `ipa_fw_mem` | `0x8b700000` | 65,536 | 0.0625 |
| `gpu_zap_mem` | `0x8b71a000` | 8,192 | 0.0078 |
| `mpss_mem` | `0x8b800000` | 257,949,696 | 246.00 |
| `wpss_mem` | `0x9ae00000` | 26,214,400 | 25.00 |
| `rmtfs_mem` | `0x9c900000` | 2,621,440 | 2.50 |
| **total (18)** | — | **390,217,728** | **372.14** |

**`hyp_mem` is 6.00 MiB.** SM4375's sibling `sm6375.dtsi` also gives 6.00 MiB
(#811 §5.3), and so do `sm8350.dtsi` and `sm8250.dtsi`. That is now **four**
independent modern SoCs at exactly 6.00 MiB, against a `hyp.img` of 8.00 MiB on
the 11 trio devices [F]. The 8 vs 6 discrepancy is unexplained and is carried
forward as [OPEN] from #811 — this slice narrows nothing about it, because the
slice has no `hyp.img` at all [N].

**There is no `tz_mem` region on this SoC** [F]. `msm8998.dtsi` has a 45 MiB
`tz_mem` at `0x86200000` and `sm8150.dtsi` a 57 MiB one; `kodiak.dtsi`,
`sm6375.dtsi`, `sm8350.dtsi` and `sm8250.dtsi` all have **none** [F]. That is
now **four** modern SoCs with no `tz_mem`, and it is the third independent
confirmation of the "modern SoCs do not reserve a TZ region in DT" law that
#811 §5.3 stated on two [F]. The TZ memory is evidently carved by the
bootloader below the kernel's view [I].

`cpucp_mem` at 1.00 MiB @ `0x80b00000` is worth noting alongside SM4375's
**absence** of any `cpucp` firmware row (#811 §4.3): mainline reserves 1 MiB for
CP-UCP here, and the slice ships no `cpucp*` file [F, N].

## 6. The slice: 67 rows, 39 files, 346,793,472 B

### 6.1 Shape and family table

| metric | value |
|---|---|
| rows | **67** |
| distinct filenames | **39** |
| distinct md5s | **44** (some filenames carry more than one md5 across devices) |
| total bytes | **346,793,472** = 330.73 MiB = 0.323 GiB |
| devices | **2** — `Edge_20` (`berlin`, 31 rows), `Edge_2021` (`berlna`, 36 rows) |
| vendor | `motorola` (both) |
| `priority` | **P3** on 67 of 67 |
| distinct stems | 38 |
| `db_path` values | 14 |

| family | rows | bytes | % of slice |
|---|---:|---:|---:|
| `boot` | 6 | 251,674,624 | **72.57%** |
| `other` | 29 | 69,235,036 | 19.96% |
| `adsp` | 12 | 17,746,432 | 5.12% |
| `bt` | 8 | 4,622,684 | 1.33% |
| `wifi` | 4 | 3,359,424 | 0.97% |
| `gpu` | 8 | 155,272 | **0.04%** |
| **total** | **67** | **346,793,472** | 100% |

Six families, no `modem`, no `tz`, no `cdsp`, no `venus` [F]. Compare SM4375
(nine families, `modem` at 68%) and the two SM7325-AE siblings (nine families
each). This is the **narrowest slice of the four SoC notes in this repo** [F].

The `db_path` split is 14 values but effectively 7 per device, one per
subdirectory, because the only difference between the two trees is `berlin` vs
`berlna` [F]:

| path suffix | Edge_20 rows / B | Edge_2021 rows / B |
|---|---|---|
| `radio` | 4 / 127,934,464 | 5 / 195,043,328 |
| `vendor/lib/rfsa/adsp` | 6 / 8,873,216 | 6 / 8,873,216 |
| `vendor/firmware` | 10 / 112,067 | 13 / 543,303 |
| `bluetooth/image` | 5 / 224,895 | 5 / 224,895 |
| `vendor/gpu/kbc` | 2 / 802,061 | 2 / 802,061 |
| `vendor/etc/wifi` | 2 / 1,679,712 | 2 / 1,679,712 |
| `vendor/etc/camera` | 2 / 266 | 3 / 276 |

`radio` dominates at **93.13% of bytes** (322,977,792 B) while holding 9 of 67
rows — the same inverse relationship #811 found (`radio` 19 rows / 80.3%) [F].

### 6.2 The two devices are one fleet with five per-build differences

Jaccard on filenames is **0.7179** — the lowest of the four comparisons in this
repo's SoC notes, and lower than SM4375's 0.9409 against its sibling [F]:

```
Edge_20   31 files
Edge_2021 36 files
shared    28   (Jaccard 28/39 = 0.7179)
only Edge_20     3
only Edge_2021    8
of the 28 shared, md5-identical: 23  ->  5 md5-different
```

The five md5-different shared files are **exactly the per-build set** [F]:

| file | why it differs |
|---|---|
| `boot.img` | embeds device-specific kernel/DTB |
| `dtbo.img` | device-specific overlays |
| `vbmeta.img` | AVB hash descriptors chain the above |
| `bluetooth.img` | partition dump, per-build |
| `arcsoft_calibration_u_dc.bin` | camera calibration, per-unit |

Every other shared file — all six `bm2n`, all three `msbtfw*`, both
`aoa_cldb_*`, all four `.mdt`, `a619_gmu.bin`, `a630_sqe.fw`,
`sequence_manifest.bin`, `unified_ksqs.bin`, `aw8695_haptic.bin`,
`msnv10/11.bin` — is byte-identical [F]. This is the cleanest available
demonstration that partition dumps and per-unit calibration vary while firmware
payloads do not [I].

The 11 non-shared files are **all `other`** [F]:

`Edge_20` only — `aec_golden_tele.bin` (10 B), `cs35l41-dsp1-spk-cali.bin`
(1,984), `cs35l41-dsp1-spk-prot.bin` (2,840). The Edge 20 has a **Cirrus
CS35L41** speaker amp; the Edge 2021 does not.

`Edge_2021` only — `aec_golden_depth.bin` (10), `aec_golden_wide.bin` (10),
`aw882xx_afe_params.bin` (18,124), `aw882xx_spk_reg.bin` (144), `dsp.img`
(67,108,864), and three `novatek_ts-NT36675-*` touch controller firmwares
(139,264 each). The Edge 2021 has an **Awinic AW882xx** amp, a Novatek
NT36675 touch controller, and the 64 MiB DSP dump.

So the two "same SoC" devices differ in **audio amplifier vendor, touch
controller vendor, camera golden files, and whether the DSP partition was
extracted** — and in nothing else [F]. That is a hardware-variant delta, not a
software one [I].

### 6.3 Top files and a power-of-two check

Top 6 rows by bytes = **321,859,000 B = 92.81%** of the slice [F]:

| file | bytes | % |
|---|---:|---:|
| `boot.img` ×2 | 100,663,296 each | 29.03% each |
| `dsp.img` | 67,108,864 | 19.35% |
| `dtbo.img` ×2 | 25,165,824 each | 7.26% each |
| `bm2n08.bin` | 3,091,896 | 0.89% |

Power-of-two sizes: **9 rows / 71,385,600 B = 20.58%** — but that is almost
entirely `dsp.img` (67,108,864). Excluding it, the only power-of-two files are
`bluetooth.img` ×2 (2 MiB), `vbmeta.img` ×2 (8 KiB), `a619_gmu.bin` ×2 (32 KiB)
and `arcsoft_calibration_u_dc.bin` ×2 (256 B) [F]. Unlike SM4375, where 20 of 25
power-of-two files were 512-B `.b00` splits, this slice has **no `.b00` at all**
[F] — see §7.1.

### 6.4 WLAN calibration: the coex DB is present, `bdwlan` is not

Zero `bdwlan*` rows on either device, against **29** on the SM7325-AE sibling
[F]. The WLAN content is two 839,856-B `aoa_cldb_*` files [F] (§3.4). So the
only WLAN calibration available on this slice is the coexistence database, not
the per-board calibration binary. Any WLAN bring-up work on `berlin`/`berlna`
needs `bdwlan.bin` from somewhere else [I].

### 6.5 The metadata columns are uniformly empty

| column | value across 67 rows |
|---|---|
| `isa_identified` | **empty on 67 of 67** |
| `interface_documented` | **`n` on 67 of 67** |
| `sha256_if_listed` | **empty on 67 of 67** (0 of 67) |
| `md5_db` | present on 67 of 67 |
| `priority` | `P3` on 67 of 67 |

12 distinct `db_type` values over 67 rows, the largest being `UNKNOWN` at 23
[F]. This is the least-analysed slice in the repo: not one row has an ISA tag,
an interface tag, or a sha256 [F]. Every ISA statement in this note therefore
comes from a filename grammar or a public binding, never from the matrix's own
identification [N].

The two `db_type` values that matter are [F]:

- **`ELF64` on 10 rows** — all five `.mdt` stems on both devices and nothing
  else. These are *monolithic* `.mdt` payloads, and their sizes (**6,708** and
  **8,068**) are not `.b00` header sizes at all: 6,708 happens to satisfy
  `52+32N` (N=208) but that reading is absurd for a 6.7 KB file, and **8,068
  fits neither `52+32N` nor `64+56N`** [F]. So on this slice the `ELF64` tag is
  a **stem-level label inherited from the family**, not a property derived from
  the file's own header — the same inheritance #811 §7.2 found for `.b00`
  (§2.3 item 2, §7.3) [F].
- **`FIRMWARE6` on 2 rows** — `unified_ksqs.bin`, 796,357 B, typed as a
  "firmware 6" bucket. Not decoded here [OPEN].

## 7. Container laws: what this slice can and cannot test

### 7.1 `mdt == b00+b01` — zero testable instances, and why that is informative

The slice has **5 `.mdt` files, all single-file** [F]:

| stem | bytes | on Edge_20 | on Edge_2021 | `.b00` sibling? |
|---|---:|---|---|---|
| `a615_zap` | 6,708 | yes | yes | **no** |
| `evass` | 8,068 | yes | yes | **no** |
| `evass-lt` | 8,068 | yes | yes | **no** |
| `vpu20_2v` | 8,068 | yes | yes | **no** |
| `vpu20_4v` | 8,068 | yes | yes | **no** |

So the law is **untestable on 5 of 5** — this slice contributes **0** testable
instances and **0** counterexamples [N]. That is the same class #811 §7.1 named
("6 untestable, all single-file MDTs"), now 5 more [F].

But the *sibling* answers the question the slice cannot [F]:

```
Edge_30          a660_zap  mdt=6860  b00=148  b01=6712  b02=1976
                           6860 == 148+6712        MATCH
Edge_30_Fusion   a660_zap  mdt=6860  148+6712=6860   MATCH
Moto_G200        a660_zap  mdt=6860  148+6712=6860   MATCH
```

**`mdt == b00 + b01` even when a `b02` exists.** The `b02` (1,976 B) is
**outside** the `.mdt` — a segment stored beside the container rather than in
it. #811 §7.1 noted `b02`-onward are independent; this is the first instance in
this repo where a note can show the law holding in the presence of a `b02` on
three independent devices [F].

Corpus-wide, of the 1,314 instances that have `mdt` + `b00` + `b01`, all 1,314
also have a `b02`, and `mdt == b00+b01+b02` holds on **0** of them [F]. So the
"`b02` is outside" reading is corpus-wide, not slice-specific [F].

### 7.2 A new law: a monolithic `.mdt` is `b00 + b01 − 152` of the split form

This is the finding this note adds, and the previous three SoC notes did not
name it.

The same stem name exists in two container forms in the corpus [F]:

- **split** — `.mdt` + `.b00` + `.b01` (+ `.b02` outside), and
  `mdt == b00 + b01`;
- **monolithic** — a single `.mdt` with no `.b00` at all.

Twenty stem names appear in both forms. For ten of them, the monolithic size is
**exactly the split size minus 152 bytes**:

| stem | monolithic `.mdt` | split `b00` | split `b01` | `b00+b01` | `− 152` | delta |
|---|---:|---:|---:|---:|---:|---:|
| `a615_zap` | 6,708 | 148 | 6,712 | 6,860 | **6,708** | 0 |
| `a660_zap` | 6,708 | 148 | 6,712 | 6,860 | **6,708** | 0 |
| `evass` | 8,068 | 692 | 7,528 | 8,220 | **8,068** | 0 |
| `goodixfp` | 7,108 | 308 | 6,952 | 7,260 | **7,108** | 0 |
| `ipa_fws` | 6,868 | 212 | 6,808 | 7,020 | **6,868** | 0 |
| `scuba_ipa_fws` | 6,868 | 212 | 6,808 | 7,020 | **6,868** | 0 |
| `sileadta` | 7,108 | 308 | 6,952 | 7,260 | **7,108** | 0 |
| `vpu20_1v` | 8,068 | 692 | 7,528 | 8,220 | **8,068** | 0 |
| `vpu20_4v` | 8,068 | 692 | 7,528 | 8,220 | **8,068** | 0 |
| `yupik_ipa_fws` | 6,868 | 212 | 6,808 | 7,020 | **6,868** | 0 |

Offsets: `{152: 10}` — **one value, ten stems, zero exceptions** [F].

What 152 might be is [OPEN]. It is not the ELF32 program-header size (32), not
the ELF64 one (56), and not either header size (52 / 64). It is not obviously
`b00 − 148 + …` for any single formula. A plausible reading is that the split
form carries 152 bytes of extra container bookkeeping (a segment table entry
plus padding), but nothing in this workspace verifies that [I]/[OPEN].

The other ten co-form stems do **not** obey it, and the reason is visible in the
data: their monolithic and split sizes are different *builds*, not the same
build in two containers [F]. For example `a615_zap` monolithic also exists at
6,684, and `evass` monolithic at 4,624 / 4,924 / 5,404 — those are genuinely
smaller binaries, not repackagings. So:

**Statement of the law, properly scoped** [F]: *when a monolithic `.mdt` and a
split `.mdt`/`.b00`/`.b01` set are the same build, the monolithic file is
exactly 152 bytes smaller than `b00 + b01`. Ten of ten. The law is a
**repackaging** identity, not a size rule — it cannot be applied without
knowing the two are the same build.*

That scoping is the whole value: the naive version ("monolithic = split − 152
always") is false on 25 of 35 mono sizes, and only 10 are genuine repackagings
[F].

### 7.3 The `.b00` header law, applied to the SM7325 family's siblings

The slice has no `.b00` [N], so #811 §7.2's law (`52+32N` for ELF32, `64+56N`
for ELF64) is not testable here. But the three `SM7325*` labels **together** hold
**39 `.b00` rows over 10 distinct sizes**, and every one of them resolves
cleanly under the law — none is ambiguous, none fits neither [F]:

| size | `(n−52)/32` | `(n−64)/56` | verdict | rows |
|---:|---:|---:|---|---:|
| 148 | **3.0** | 1.5 | ELF32, 3 phdr | 1 |
| 212 | **5.0** | 2.5 | ELF32, 5 phdr | 1 |
| 308 | **8.0** | 4.36 | ELF32, 8 phdr | 6 |
| 340 | **9.0** | 4.93 | ELF32, 9 phdr | 2 |
| 512 | 14.375 | **8.0** | **ELF64, 8 phdr** | 20 |
| 596 | **17.0** | 9.5 | ELF32, 17 phdr | 2 |
| 692 | **20.0** | 11.21 | ELF32, 20 phdr | 2 |
| 1012 | **30.0** | 16.93 | ELF32, 30 phdr | 2 |
| 1044 | **31.0** | 17.5 | ELF32, 31 phdr | 1 |
| 1268 | **38.0** | 21.5 | ELF32, 38 phdr | 2 |

Nine sizes are ELF32-only and exactly one — **512 B, 20 of the 39 rows** — is
ELF64. That 512-B ELF64 class is the TEE/TA container size (`hdcp`, `widevine`,
`featenabler`, `egisfod64`, `loadalgota64`, `mldapta`, `winsecap`, …), and
corpus-wide 512-B `.b00` files span **269 rows over 32 distinct filenames**, all
ELF64 8-phdr [F].

So `a660_zap.b00` (148) and `vpu20_1v.b00` (692) are **ELF32**, and the corpus's
`ELF64` tag on the 148-byte rows is wrong — the same defect as §2.3 item 2, and
the third independent slice where the `db_type` disagrees with the arithmetic
[F]. Corpus-wide there are **76** `.b00` rows of exactly 148 B across **39
devices** and **11 filenames**, and only **50** of them carry the `ELF64` tag;
the other 26 are typed `MODEM` (13) or `COMPUTE` (13), so the mistyping is not
even applied consistently to the same size [F].

`148 = 52 + 32×3` also cross-checks against #811's finding that 148-byte `.b00`
files are 3-segment containers on 7 devices (`a615_zap` there, `a610_zap` /
`a660_zap` / `a740_zap` / `spss*` here) [F]. Consistent [F].

## 8. Mainline and postmarketOS status

### 8.1 Mainline: present and unusually complete

| item | status | evidence |
|---|---|---|
| `QCOM_ID_SM7325` | **475** | `qcom,ids.h:239` |
| `QCOM_ID_SM7325P` | **499** | `qcom,ids.h:246` |
| `qcom_board_id(SM7325)` | present | `socinfo.c:480` |
| `qcom_board_id(SM7325P)` | present | `socinfo.c:487` |
| `sm7325.dtsi` | **present**, 537 B, 8-CPU overlay | master |
| SoC include parent | `kodiak.dtsi`, 202,322 B | master (renamed from `sc7280.dtsi`, 2025-10-30) |
| DT entries matching `sm7325` | **8** (1 SoC + 7 boards) | `arch/arm64/boot/dts/qcom`, 664 entries |
| `qcom,sm7325` boards in `qcom.yaml` | **4** — `motorola,dubai`, `nothing,spacewar`, `xiaomi,lisa`, `xiaomi,taoyao` | `qcom.yaml:1129` |
| `motorola,berlin` / `motorola,berlna` | **neither exists** | absent from `qcom.yaml` and the DT dir |
| CPuFreq | `qcom,cpufreq-epss` | `qcom-cpufreq-hw.c:441` |
| PAS remoteprocs | 4 (`mpss`, `adsp`, `wpss`, `cdsp`) | `kodiak.dtsi:3421,4466,4617,4791` |
| Venus | `qcom,sc7280-venus` | `kodiak.dtsi:5018` |
| GPU | `adreno-635.0` / `0x06030500` | `kodiak.dtsi:3217`; `a6xx_catalog.c:1124` |

**The device gap is the finding**: mainline supports the *SoC* well (4 boards,
8 DT entries, full clock/remoteproc/display stack) and supports **neither of
this slice's two devices** [F]. So the SM7325 work here is a device bring-up
gap, not a SoC support gap — the exact inverse of SM4375, where the SoC itself
was absent [F].

### 8.2 The upstream status page tracks Kodiak, and it is mature

`linux-msm.github.io/mainline-status/soc/kodiak` **exists** and reports [F]:

| block | first supported |
|---|---|
| Clocks (GCC, RPMhCC) | 5.13 |
| Pinctrl | 5.13 |
| UART / SPMI | 5.13 |
| CPU SMP / CPUidle | 5.13 |
| CPUfreq (DVFS) | 5.14 |
| Interconnects | 5.14 |
| I2C / SPI / PCIe | 5.16 |
| **GPU** | **5.16** |
| UFS | 6.8 |
| UFS ICE | 6.1 |
| DDRfreq | 5.18 |
| **ADSP / CDSP remoteproc** | **6.8** |
| FastRPC / compute | 6.8 |
| WLAN | 5.19 |
| IPA | 5.15 |
| LPASS digital codecs | 5.19 |
| DisplayPort / DSI | 5.18 |
| **Venus** | **5.17** |
| CSI / Data Path / VFE | 6.14 |
| EVA | **N** (not supported) |

Three things are worth calling out [F]:

1. **The page is titled "Kodiak — Snapdragon 7c+ Gen 3 (aka 778G)"** and lists
   six SKUs: SC7280, **SM7325**, QCM5430, QCM6490, QCS5430, QCS6490. So upstream
   treats the 778G as an SKU of the SC7280/Kodiak platform, which is exactly
   what §1.3's rename encoded [F].
2. **The tested boards are Qualcomm RB3 Gen 2, Fairphone 5, SHIFTphone 8,
   Thundercomm RUBIK Pi 3** — none of them is a 778G phone, and none is a
   Motorola [F]. The platform is validated on adjacent silicon (QCM6490 in FP5,
   QCS6490 in the RB3), not on SM7325 hardware [I].
3. **EVA is explicitly `N`.** The VFE/EVA camera DSP is the one block upstream
   records as unsupported on this platform, while CSI/Data Path/VFE are at
   6.14 [F]. So the camera front-end is mainline-capable and the EVA coprocessor
   is not [F].

### 8.3 linux-firmware: the a660 set is upstream under a different SoC's path

| path | HTTP | bytes |
|---|---:|---:|
| `qcom/a660_gmu.bin` | **200** | 55,252 |
| `qcom/a660_sqe.fw` | **200** | 43,292 |
| `qcom/qcm6490/a660_zap.mbn` | **200** | 1,054,648 |
| `qcom/a630_gmu.bin` | **200** | 32,768 |
| `qcom/a630_sqe.fw` | **200** | 34,188 |
| `qcom/a619_gmu.bin` | **404** | — |
| `qcom/sm7325/` (directory) | **404** | — |
| `qcom/sm7325/motorola/dubai/` | **404** | — |

`WHENCE` lists the a660 files under `qcm6490/` with `qcs6490` and `sm8350`
symlinks pointing at it [F]:

```
File: qcom/a660_gmu.bin
File: qcom/a660_sqe.fw
File: qcom/qcm6490/a660_zap.mbn
Link: qcom/qcs6490/a660_zap.mbn -> ../qcm6490/a660_zap.mbn
Link: qcom/sm8350/a660_zap.mbn -> ../qcm6490/a660_zap.mbn
```

So **`qcom/sm7325/` does not exist upstream at all**, and the firmware the
SM7325 GPU needs is fetchable only via the QCM6490 path [F]. A board DT asking
for `qcom/sm7325/motorola/dubai/a660_zap.mbn` — which is exactly what
`sm7325-motorola-dubai.dts:701` asks for — will 404 against upstream
linux-firmware [F]. That is a real, current packaging gap for the one SM7325
board mainline does support [I].

Upstream `a660_gmu.bin` at 55,252 B / `cd3a2352…` matches **exactly one**
corpus row (`FP5`); the corpus's dominant build is 55,256 B / `179caf2e…` on 19
devices [F] (§2.3). So even where a device ships an `a660_gmu.bin`, it is
usually **not** the upstream build [I].

### 8.4 postmarketOS: a wiki page for the SoC and for one device, no package

`pmaports` (default branch **`master`**, 1,273 device directories across
`main` 13 / `community` 126 / `testing` 1,083 / `archived` 51) [F]:

```
device dirs matching "7325"  -> 0
device dirs matching "kodiak"-> 0
device dirs matching "berlna"-> 0
device dirs matching "778"   -> 0
device dirs matching "berlin"-> 3, all HUAWEI
                                 (device-huawei-berlin, firmware-huawei-berlin,
                                  linux-huawei-berlin)
```

The `berlin` hit is the **Huawei Berlin** phone, not the Motorola Edge 20 — a
codename collision worth recording because a naive `grep berlin` says "port
exists" [F]. Direct tree probes confirm [F]:

```
testing/linux-postmarketos-qcom-sm7325 -> 404
testing/device-motorola-berlna         -> 404
testing/device-motorola-berlin         -> 404
```

The **wiki** does have content [F]:

- `Qualcomm_Snapdragon_778G/778G+/782G_(SM7325)` — an SoC page with three
  infoboxes (778G, 778G+, 782G), `mainline = yes`, a `community_page` at
  `github.com/sc7280-mainline`, and a status block that is `Y` for cpu, uart,
  storage, usb, display, **gpu**, pinctrl, i2c, spi, audio, video, thermal,
  wifi, bluetooth, gps, camera; `P` for **modem**; and blank for suspend.
- `Motorola_Edge_2021_(motorola-berlna)` — a device page that exists, with
  `chipset = Qualcomm Snapdragon 778G (SM7325)`, `gpu = Adreno 642L`,
  `architecture = aarch64`, **`packaged = no`**, **`pmoskernel` empty**, and
  **every `status_*` field blank**. It also states "U-boot port is currently
  WIP" with `status_uboot = Y`, `status_uboot_secondary = Y`,
  `status_uboot_sd = -`.
- `Motorola_Edge_20_(motorola-berlin)` — **does not exist** (API returns
  `missingtitle`; a search for `motorola-berlin` returns 0 hits).

So the honest postmarketOS status is [F]: **SoC supported and documented, one
of the two devices has a stub wiki page with no package, the other has no page
at all.** Compare SM4375, which had 0 wiki hits on four queries and no page
[F] — SM7325 is materially further along as a platform and in exactly the same
place as a device [I].

## 9. Honest negatives

1. **The `tz` family is 0 rows and no TZ bytes exist in this slice.** Every TZ
   statement in §5 comes from a sibling device, from mainline DT, or from a
   public wiki — none from this slice's own data [N].

2. **The `modem` family is 0 rows.** There is no `modem.img` and no
   `modem.mdt`/`.b00` on either device, so nothing here can speak to modem
   firmware, and the six `bm2n` files labelled `db_type=MODEM` are DSP, not
   modem [N].

3. **The slice has no `.b00` at all, so it cannot test either container law.**
   `mdt == b00+b01` is 0-of-0 and the `52+32N`/`64+56N` header law is
   untestable [N]. §7.2's monolithic-vs-split law is derived from *other*
   devices; this slice is the motivation, not the proof [F for the law, N for
   this slice].

4. **The 152-byte offset in §7.2 is unexplained.** Ten of ten is a strong
   arithmetic result and a weak explanation; nothing here identifies what the
   152 bytes are [OPEN].

5. **`isa_identified` is empty on 67 of 67 rows**, so no ISA claim in this note
   is a matrix identification — every one is a filename grammar or a public
   binding [N].

6. **The CPU per-cluster MIDR split is [I], not [F].** `cputype.h` documents
   that Kryo 6XX Gold reports A78 and Silver reports A55; which of *this* part's
   8 cores is which is read from the DT's `capacity-dmips-mhz` and
   `freq-domain`, not from a MIDR read. The MIDR **values**
   (`0x410fd410`/`0x410fd050`) are arithmetic on documented constants; the
   **assignment** to specific cores is inference [I]. The X1 value
   `0x4100d440` is arithmetic on the same basis and carries the same caveat.

7. **The Prime core's real core is `[OPEN]`.** §1.4 derives the X1 MIDR
   (`0x4100d440`) because `cputype.h` says Kryo 6XX Prime reports
   `MIDR_CORTEX_X1`; that is a *documented mapping*, not evidence that this
   part's prime core is an X1. The DT names nothing beyond
   capacity/freq-domain for cpu7, so the Prime identity is `[OPEN]` [F for the
   mapping, OPEN for this part].

8. **Whether `vpu20_2v`/`vpu20_4v` are the venus firmware under a vendor name
   is [OPEN].** Both are 8,068-B single-file `.mdt` in `other`; `venus.mdt` is
   also 8,068 B in the corpus. Size agreement is suggestive, not proof, and no
   payload is available [OPEN].

9. **`unified_ksqs.bin` (796,357 B, `FIRMWARE6`) is not decoded.** Neither is
   `sequence_manifest.bin` (5,704 B) — both are named-only [OPEN].

10. **#2030's `[N]` on the a660 set is corrected here, but the correction is
    about the corpus, not about hardware.** That `Edge_30` ships the a660 set
    proves the corpus *can* contain it; it does not prove `berlin`/`berlna`
    ship it on-device [F for the sibling, I for the reading].

11. **`db_type=ELF64` on the 148-byte `.b00` rows is wrong under the
    `52+32N`/`64+56N` law**, and this is a corpus data defect this note reports
    rather than fixes — fixing it means re-typing 50 rows across the matrix
    (76 rows carry that size; 50 are tagged `ELF64`, 26 are `MODEM`/`COMPUTE`),
    which is an upstream data PR rather than a per-SoC note [F for the wrong
    tag, OPEN for the right one].

12. **The `AUDIO`-inside-`gpu` defect is corpus-wide and total for
    `a6[56]0_{gmu,sqe}`**: 79 rows over exactly 4 filenames, and 0 `AUDIO` rows
    in `blob_family=modem` [F]. It is named here and left unfixed for the same
    reason as item 11.

13. **`dsp.img` is `other`, not `adsp`, on 61 of 61 corpus rows** — so a
    family-keyed census misses it, and it is **19.35% of the slice** and
    **32.39% of `berlna`'s own bytes** [F for the label, I for the consequence].

14. **`hyp.img` 8.00 MiB vs `hyp_mem` 6.00 MiB remains unexplained**, and this
    slice cannot narrow it because it has no `hyp.img` [N, OPEN].

15. **No payload was opened, no ELF parsed, no instruction disassembled** [N].
    The two byte-length checks in §8.3 are on public upstream files
    (`a660_gmu.bin`, `a660_sqe.fw`) and are size/md5 only.

16. **`qcom/sm7325/` does not exist in linux-firmware**, so the one SM7325 board
    mainline supports requests firmware paths that 404 upstream. This is
    reported, not fixed — it is an upstream packaging PR [F].

## Reproduce

All blocks below are `python3 -I` (stdlib only) or `curl`, run 2026-11-24 from
the repo root. Each prints the numbers this note cites.

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm SM7325 Snapdragon 778G 5G']
print('rows',len(s),'files',len({r['filename'] for r in s}),'bytes',sum(int(r['size_bytes']) for r in s))
print('devices',sorted({r['device'] for r in s}))
print('families',dict(Counter(r['blob_family'] for r in s)))
print('priority',dict(Counter(r['priority'] for r in s)))
print('db_types',len({r['db_type'] for r in s}),dict(Counter(r['db_type'] for r in s).most_common(3)))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm SM7325 Snapdragon 778G 5G']
tot=sum(int(r['size_bytes']) for r in s)
f=Counter(); b=Counter()
for r in s: f[r['blob_family']]+=1; b[r['blob_family']]+=int(r['size_bytes'])
for k,v in f.most_common(): print('%-8s %3d rows %12d B %6.2f%%'%(k,v,b[k],100*b[k]/tot))
print('boot share %.2f%%'%(100*b['boot']/tot))"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d={}
for r in rows:
    if r['soc'].strip()=='Qualcomm SM7325 Snapdragon 778G 5G':
        d.setdefault(r['device'],{})[r['filename']]=(int(r['size_bytes']),r['db_type'],r['md5_db'])
A,B=d['Edge_20'],d['Edge_2021']
sa,sb=set(A),set(B)
print('Edge_20',len(sa),'Edge_2021',len(sb),'shared',len(sa&sb))
print('jaccard %.4f'%(len(sa&sb)/len(sa|sb)))
print('md5-identical of shared',sum(1 for f in sa&sb if A[f][2]==B[f][2]))
print('md5-different',sorted(f for f in sa&sb if A[f][2]!=B[f][2]))
print('only Edge_20',sorted(sa-sb))
print('only Edge_2021',sorted(sb-sa))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm SM7325 Snapdragon 778G 5G']
print('empty isa',sum(1 for r in s if not r['isa_identified']),'of',len(s))
print('interface n',sum(1 for r in s if r['interface_documented']=='n'),'of',len(s))
print('sha256 set',sum(1 for r in s if r['sha256_if_listed']),'of',len(s))
print('md5 set',sum(1 for r in s if r['md5_db']),'of',len(s))
for fam in ('tz','modem','cdsp','venus','ipa_fws','slpi','npu','spss1p','spss2p'):
    print('%-9s %d rows'%(fam,sum(1 for r in s if r['blob_family']==fam)))
print('bdwlan rows',sum(1 for r in s if 'bdwlan' in r['filename']))"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for fn in ('a660_gmu.bin','a660_sqe.fw','a660_zap.mdt','a660_zap.mbn','a660_zap.b00','a660_zap.b01','a660_zap.b02'):
    s=[r for r in rows if r['filename']==fn]
    print('%-16s %2d rows %2d devs types=%s'%(fn,len(s),len({r['device'] for r in s}),dict(Counter(r['db_type'] for r in s))))
print('AUDIO inside gpu:',dict(Counter(r['filename'] for r in rows if r['db_type']=='AUDIO' and r['blob_family']=='gpu')))
print('AUDIO inside modem:',sum(1 for r in rows if r['db_type']=='AUDIO' and r['blob_family']=='modem'))
print('mbn rows',sum(1 for r in rows if r['filename'].endswith('.mbn')))"
```

```bash
python3 -I -c "
import csv,re
from collections import defaultdict,Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
inst=defaultdict(dict)
for r in rows:
    m=re.match(r'^(.+?)\.(mdt|b([0-9]{2}))\$',r['filename'])
    if m: inst[(r['device'],m.group(1))][m.group(2)]=int(r['size_bytes'])
t=[(k,v) for k,v in inst.items() if 'mdt' in v and 'b00' in v and 'b01' in v]
print('testable',len(t),'equal',sum(1 for k,v in t if v['mdt']==v['b00']+v['b01']))
withb02=[(k,v) for k,v in t if 'b02' in v]
print('with b02',len(withb02),'still equal',sum(1 for k,v in withb02 if v['mdt']==v['b00']+v['b01']))
print('mdt==b00+b01+b02',sum(1 for k,v in t if 'b02' in v and v['mdt']==v['b00']+v['b01']+v['b02']))"
```

```bash
python3 -I -c "
import csv,re
from collections import defaultdict,Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
inst=defaultdict(dict)
for r in rows:
    m=re.match(r'^(.+?)\.(mdt|b([0-9]{2}))\$',r['filename'])
    if m: inst[(r['device'],m.group(1))][m.group(2)]=int(r['size_bytes'])
byname=defaultdict(lambda:(set(),set()))
for (d,st),v in inst.items():
    if 'mdt' not in v: continue
    mono,spl=byname[st]
    if 'b00' in v and 'b01' in v: spl.add((v['b00'],v['b01']))
    elif 'b00' not in v: mono.add(v['mdt'])
    byname[st]=(mono,spl)
hits=[]
for st,(mono,spl) in sorted(byname.items()):
    if not mono or not spl: continue
    for m in sorted(mono):
        for (b0,b1) in sorted(spl):
            if b0+b1-152==m: hits.append((st,m,b0,b1))
print('mono==b00+b01-152 hits',len(hits))
print('offsets',dict(Counter(b0+b1-m for _,m,b0,b1 in hits)))
for h in hits: print('  %-14s mono=%-6d b00=%-4d b01=%-5d'%(h[0],h[1],h[2],h[3]))"
```

```bash
python3 -I -c "
import csv
from collections import defaultdict,Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
d=defaultdict(dict)
for r in rows: d[r['device']][r['filename']]=int(r['size_bytes'])
trio=[k for k,v in d.items() if v.get('hyp.img')==8388608 and v.get('tz.img')==4194304 and v.get('uefisecapp.img')==2097152]
md5={r['device']:r['md5_db'] for r in rows if r['filename']=='hyp.img' and int(r['size_bytes'])==8388608}
print('8/4/2 trio devices',len(trio),'distinct hyp md5',len(set(md5.values())))
soc={r['device']:r['soc'].strip() for r in rows}
print(dict(Counter(soc[k] for k in trio).most_common()))
print('dsp.img rows',sum(1 for r in rows if r['filename']=='dsp.img'),
      'sizes',dict(Counter(int(r['size_bytes']) for r in rows if r['filename']=='dsp.img')),
      'families',dict(Counter(r['blob_family'] for r in rows if r['filename']=='dsp.img')))"
```

```bash
python3 -I -c "
m=lambda imp,pn:(imp<<24)|(0xf<<16)|(pn<<4)
print('MIDR X1  0x%08x'%m(0x41,0xD44))
print('MIDR A78 0x%08x'%m(0x41,0xD41))
print('MIDR A55 0x%08x'%m(0x41,0xD05))
for n in (148,692,512):
    print(n,'ELF32?',(n-52)%32==0 and n>=52,'N=',(n-52)//32,'| ELF64?',(n-64)%56==0 and n>=64,'N=',(n-64)//56)
print('8068 = 692+7528-152?',8068==692+7528-152)
print('6708 = 148+6712-152?',6708==148+6712-152)
print('6868 = 212+6808-152?',6868==212+6808-152)"
```

```bash
curl -s -o /dev/null -w "a660_gmu.bin %{http_code}\n" https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/qcom/a660_gmu.bin
curl -s -o /dev/null -w "a660_sqe.fw  %{http_code}\n" https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/qcom/a660_sqe.fw
curl -s -o /dev/null -w "qcm6490 zap  %{http_code}\n" https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/qcom/qcm6490/a660_zap.mbn
curl -s -o /dev/null -w "a619_gmu.bin %{http_code}\n" https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/qcom/a619_gmu.bin
curl -s -o /dev/null -w "sm7325 dir   %{http_code}\n" https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/qcom/sm7325/WHENCE
curl -s https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/qcom/a660_gmu.bin | wc -c
```

```bash
curl -s https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/boot/dts/qcom/sm7325.dtsi | sed -n '8,18p'
curl -s https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/boot/dts/qcom/kodiak.dtsi | grep -n 'capacity-dmips-mhz\|qcom,freq-domain = <&cpufreq_hw\|cluster[0-9] {' | head -20
curl -s https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/boot/dts/qcom/kodiak.dtsi | grep -n 'remoteproc@\|video-codec@\|hyp_mem:'
curl -s https://raw.githubusercontent.com/torvalds/linux/master/include/dt-bindings/arm/qcom,ids.h | grep -n 'SM7325'
curl -s https://raw.githubusercontent.com/torvalds/linux/master/drivers/gpu/drm/msm/adreno/a6xx_catalog.c | sed -n '1123,1146p'
curl -s https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/include/asm/cputype.h | sed -n '236,248p'
curl -s https://raw.githubusercontent.com/torvalds/linux/master/drivers/remoteproc/qcom_q6v5_pas.c | grep -n 'sc7280'
```

```bash
curl -sL "https://wiki.postmarketos.org/api.php?action=parse&page=Qualcomm_Snapdragon_778G/778G%2B/782G_(SM7325)&prop=wikitext&format=json" | python3 -I -c "
import json,sys
w=json.load(sys.stdin)['parse']['wikitext']['*']
print(w[:600])"
curl -sL "https://wiki.postmarketos.org/api.php?action=parse&page=Motorola_Edge_2021_(motorola-berlna)&prop=wikitext&format=json" | python3 -I -c "
import json,sys
w=json.load(sys.stdin)['parse']['wikitext']['*']
print([l for l in w.splitlines() if any(k in l for k in ('packaged','pmoskernel','chipset','gpu =','status_screen'))])"
curl -sL "https://wiki.postmarketos.org/api.php?action=query&list=search&srsearch=motorola-berlin&format=json" | python3 -I -c "
import json,sys; print(json.load(sys.stdin)['query']['search'])"
```

```bash
python3 -I -c "
import json,urllib.request
names=[]
for s in ('main','community','testing','archived'):
    sub=[]
    for p in range(1,14):
        u='https://gitlab.com/api/v4/projects/postmarketOS%2Fpmaports/repository/tree?path=device/'+s+'&per_page=100&page='+str(p)
        try: d=json.load(urllib.request.urlopen(u,timeout=40))
        except Exception: break
        if not d: break
        sub+=[e['name'] for e in d]
    print(s,len(sub))
    names+=sub
print('device dirs',len(names))
for pat in ('7325','kodiak','berlna','778','berlin'):
    print(pat,[n for n in names if pat in n.lower()])"
```

## Sources

| claim | source | access |
|---|---|---|
| 67 rows / 39 files / 346,793,472 B / 2 devices; family table; 14 `db_path`s | `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 rows) | 2026-11-24 |
| `Edge_20` 31 rows, `Edge_2021` 36 rows; codenames `berlin` / `berlna` | `upstream-contribution/blob-database/device-inventory.csv` | 2026-11-24 |
| SoC identity, 1+3+4 Kryo 670, Adreno 642L | postmarketOS wiki `Qualcomm_Snapdragon_778G/778G+/782G_(SM7325)` | 2026-11-24 |
| `motorola-berlna` device page: `packaged = no`, blank statuses | postmarketOS wiki `Motorola_Edge_2021_(motorola-berlna)` | 2026-11-24 |
| `motorola-berlin` page absent (0 hits on `motorola-berlin`) | postmarketOS wiki API `missingtitle` + `srsearch` | 2026-11-24 |
| 1,273 device dirs; 0 match `7325`/`kodiak`/`berlna`/`778`; `berlin` = Huawei | `pmaports` GitLab API, branch `master` | 2026-11-24 |
| `linux-postmarketos-qcom-sm7325` 404; `device-motorola-berlna` 404 | `pmaports` GitLab repository tree API | 2026-11-24 |
| 4+3+1 CPU shape, 3 `freq-domain`s, 3 capacities, 1 `cpu-map`; `hyp_mem` 6.00 MiB; no `tz_mem`; 4 remoteprocs + venus | `kodiak.dtsi` (202,322 B), master | 2026-11-24 |
| `sm7325.dtsi` = 537 B, 8× `qcom,kryo670`; parent `kodiak.dtsi` | `arch/arm64/boot/dts/qcom/sm7325.dtsi` | 2026-11-24 |
| `sc7280.dtsi` renamed to `kodiak.dtsi` by `dd6edcd7d3e4`, 2025-10-30 | `torvalds/linux` commit API, path `sc7280.dtsi` | 2026-11-24 |
| Kryo 6XX Gold = A78 partnum `0xD41`, Silver = A55 partnum `0xD05`; no `KRYO_6XX_*` part | `arch/arm64/include/asm/cputype.h:74,80,128-133,241-246` | 2026-11-24 |
| A55 at `:1695` (KPTI-safe) and `:1869` (broken-DBM erratum); `KRYO_4XX_SILVER` at `:1704`,`:1871`; 0 `CORTEX_A78` hits | `arch/arm64/kernel/cpufeature.c` | 2026-11-24 |
| `qcom,kryo670` documented at `:224` | `Documentation/devicetree/bindings/arm/cpus.yaml` | 2026-11-24 |
| GPU: `adreno-635.0`, `0x06030500`, a660 binding, `adreno_is_7c3()` | `research/soc/Qualcomm-SM7325-Snapdragon-778G-5G-gpu.md` (#2030); re-verified in `a6xx_catalog.c:1124-1142` | 2026-11-24 |
| 3 `.machine =` strings (`sm7150`, `sm4350`, `sm6375`), no `qcom,sm7325`; chip-ID entry carries no `.revn` | `drivers/gpu/drm/msm/adreno/a6xx_catalog.c:820,870,895,1124-1142` | 2026-11-24 |
| `a660_*` corpus rows: 21/30/21/3/3/3 and 0 `.mbn`; `AUDIO`-in-`gpu` = 79 rows / 4 filenames | `coverage-matrix.csv` | 2026-11-24 |
| `a660_zap` split law on 3 devices; `b02` outside `.mdt` | `coverage-matrix.csv`; `Edge_30`, `Edge_30_Fusion`, `Moto_G200` rows | 2026-11-24 |
| upstream `a660_gmu.bin` 55,252 B / `cd3a2352…`, md5-matches `FP5` only | `linux-firmware` on `git.kernel.org`, `WHENCE:7273-7280` | 2026-11-24 |
| `qcom/a619_gmu.bin` 404; `qcom/sm7325/` 404 | same | 2026-11-24 |
| `QCOM_ID_SM7325` 475 `:239`, `QCOM_ID_SM7325P` 499 `:246` | `include/dt-bindings/arm/qcom,ids.h` | 2026-11-24 |
| `qcom_board_id(SM7325)` `:480`, `(SM7325P)` `:487` | `drivers/soc/qcom/socinfo.c` | 2026-11-24 |
| 4 `qcom,sm7325` boards: `motorola,dubai`, `nothing,spacewar`, `xiaomi,lisa`, `xiaomi,taoyao` | `Documentation/devicetree/bindings/arm/qcom.yaml:1129` | 2026-11-24 |
| 664 DT entries; 8 match `sm7325`; `sc7280.dtsi` absent, `kodiak.dtsi` present | GitHub contents API, `arch/arm64/boot/dts/qcom` | 2026-11-24 |
| `sc7280-adsp-pas` → `sm8350_adsp_resource`; `-cdsp` → `sm6350_cdsp_resource`; `-wpss` → `sc7280_wpss_resource` | `drivers/remoteproc/qcom_q6v5_pas.c:2025-2028,1764` | 2026-11-24 |
| CPUfreq via `qcom,cpufreq-epss` | `drivers/cpufreq/qcom-cpufreq-hw.c:441` | 2026-11-24 |
| Kodiak status page: 6 SKUs, 4 tested boards, GPU 5.16, ADSP/CDSP 6.8, Venus 5.17, EVA `N` | `linux-msm.github.io/mainline-status/soc/kodiak` | 2026-11-24 |
| `WCN6750` BT: `msbtfw*` prefix rule | `research/soc/per-soc-method-plans.md` §8; `sm7325-motorola-dubai.dts:280,1385` | 2026-11-24 |
| `mdt == b00+b01` 669/1,314; `mdt == b00+b01+b02` 0/1,314 | `coverage-matrix.csv` | 2026-11-24 |
| monolithic `== b00+b01−152`, 10/10, offsets `{152: 10}` | `coverage-matrix.csv` | 2026-11-24 |
| ELF32 `52+32N` / ELF64 `64+56N`; `cmnlib64` correction | `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-soc.md` §7.2 (#811) | 2026-11-24 |
| 8/4/2 MiB trio on 11 devices / 6 SoC labels, 11 distinct `hyp.img` md5 | `coverage-matrix.csv`; cross-check #811 §5.2 | 2026-11-24 |
| `hyp_mem` 6.00 MiB, no `tz_mem` on 4 modern SoCs | `sm4375`/`sm6375`, `sm8350`, `sm8250`, `kodiak` device trees | 2026-11-24 |
| `dsp.img` 61 rows / 61 devices, 32 or 64 MiB, all `other` | `coverage-matrix.csv` | 2026-11-24 |
| `aoa_cldb_*` 17 devices at 839,856 B; zero `bdwlan` here | `coverage-matrix.csv` | 2026-11-24 |
| `[PATCH v3 3/6] arm64: dts: qcom: Add SM7325 device tree`, 2024-10-20 — parent `sc7280.dtsi`, 8× kryo670 | `lists.openwall.net`, `spinics.net`, message-id `20241020205615.211256-4-danila@jiaxyga.com` | 2026-11-24 |
| `QCOM_ID_SM7325` 475 / `SM7325P` 499 commit pair | `lists.openwall.net`, `[PATCH v2 01/11] dt-bindings: arm: qcom,ids` | 2026-11-24 |
| `berlna` boot family = 3 rows, all unique md5 | `docs/devices/motorola/Edge_2021/boot.md` (#916) | 2026-11-24 |
| `berlna` tz = 0 rows is a census-scope gap; extract list has 2 entries | `docs/devices/motorola/Edge_2021/tz.md` (#922) | 2026-11-24 |
| `berlin` gpu = 4 rows, fleet-shared md5s, 25-device `sequence_manifest.bin` | `docs/devices/motorola/Edge_20/gpu.md` (#928) | 2026-11-24 |
| SM7325 **cluster** shape (3 labels): 4 devices / 880 rows / 1.81 GB; BT = WCN6750 ×12 | `research/soc/per-soc-method-plans.md:335-353`; re-verified against the matrix | 2026-11-24 |
| SM4375 house format and the `64+56N` correction | `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-soc.md` (#811) | 2026-11-24 |

Not legal advice; no proprietary payload accessed or committed — all facts are
metadata (sizes, md5s, paths, `db_type`, family) plus public GPL source and
public wiki/API text.
