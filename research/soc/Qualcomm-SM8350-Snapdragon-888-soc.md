# Qualcomm SM8350 Snapdragon 888 — SoC package: CPU, DSP, boot chain, TrustZone, firmware census

Issue #823. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative. Every number is from a command run **2026-11-22** against
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 rows),
`data/fleet/devices-001-222.csv`, `torvalds/linux` master at
`4843f6873f7c4835e62f2c73ba0fd538e57a2f22`, `linux-firmware` `main`
(`WHENCE`, 540,253 B), and the postmarketOS `pmaports` tree on GitLab.

This is the **SoC-package** note. The GPU core identification for this SoC is a
separate, already-committed deliverable and is **cited, not re-derived**.

Companion documents:

| document | owns | this note |
|---|---|---|
| `research/soc/Qualcomm-SM8350-Snapdragon-888-gpu.md` | Adreno 660 three-way proof (§1), the 11 GPU rows / 7 filenames (§3), `a619_gmu.bin`+`a630_sqe.fw` dead entries (§3.1), the two `a660_zap.mdt` builds (§3.2), `sequence_manifest.bin` byte-identity (§3.3), a6xx µC ISA (§4) | cites §1, §3-§4; adds CPU, DSP, boot chain, TZ, firmware census |
| `research/soc/Qualcomm-SM7250-Snapdragon-765G-gpu.md` §2.1 | the `tundra` → SM8350-AC relabel and the 3,286-row undercount arithmetic | cites; does not re-derive the Jaccard tables |
| `research/laptop/qualcomm-adsp-bm2n-variant-matrix.md` | the `bm2n*` fleet matrix and its vendor-tree provenance | cites §3 of that doc for the six digests |
| `research/qualcomm/docs/bootchain-census.md` | AOP/SHRM/CPUCP build-string census | cites for the negative on SHRM |
| `research/fleet/wifi-wpss.md` §7 | the `-AC` suffix is a distinct part number, not a merge | cites |
| `docs/devices/motorola/Moto_G200/cdsp.md` | Hexagon 780 marketing name, `hexagon-v68` toolchain arch, `e_machine` 164 on public CDSP witnesses | cites §1 of that doc |
| `research/fleet/pil-metadata-sweep.md` | the SHA-384 PIL hash-slot law, **SM8250 + SDM845 only** | records that it does **not** cover SM8350 |

**No SM8350 payload exists in this workspace.** `data-fetch/` holds
`second-device/instantnoodle` (SM8250) and `second-device/larry` (SM6375) only.
Every payload statement below is matrix metadata — filename, size, md5 — and
**no ELF parsing is claimed for this SoC** [N].

## 0. Verdict

| question | answer | class |
|---|---|---|
| SoC identity | SM8350 = Snapdragon 888 = platform codename **lahaina**; board ID **439** (`QCOM_ID_SM8350`) | [F] |
| CPU topology | **4× Cortex-A55 + 3× Cortex-A78 + 1× Cortex-X1** — one 8-core `cpu-map/cluster0`, not a 4+4 split | [F] |
| GPU | Adreno 660, chip ID `0x06060001`, `ADRENO_6XX_GEN4` — cited from the GPU note | [F] |
| Compute DSP | Hexagon 780 is the **marketing** name and `hexagon-v68` the toolchain arch; the corpus records `isa_identified` EMPTY on all 18 CDSP rows | [F] marketing, [N] ISA proof |
| Remoteproc set | **4** PAS nodes: `adsp`, `cdsp`, `mpss` (modem), `slpi` | [F] |
| TrustZone / reserved memory | **25** regions, **703,791,104 B = 671.19 MiB**, fully enumerated | [F] |
| `qcom/sm8350/` in linux-firmware | **exactly 1 entry, and it is a symlink**; **0** real files | [F] |
| Board-DT firmware requests that resolve | **1 of 11** distinct paths (only `a660_zap.mbn`) | [F] |
| Split-segment law `mdt == b00+b01` | **23 of 23** stems, zero exceptions; 15 further stems are self-contained | [F] |
| `b00` size form | `52+32N` (ELF32) on 8 stems, `64+56N` (ELF64) on 15, neither on 0; the `32`/`64` filename suffix matches the header **7 of 7** | [F] |
| postmarketOS support | **OnePlus only** (`lemonade`, `lemonadep`), on a **fork pinned to 6.7 / 2024-01-16** | [F] |

The two headline findings are the linux-firmware absence (§6) and the
postmarketOS fork (§8). Neither is a restatement of public marketing.

## 1. CPU: 4×A55 + 3×A78 + 1×X1 — one cluster in the DT, three in silicon

**Verdict: four Cortex-A55, three Cortex-A78, one Cortex-X1.** The public
marketing text describes the Snapdragon 888 as a "1+3+4" arrangement, which
matches. What does **not** match is the DT: mainline describes **one**
`cpu-map` cluster containing all eight cores.

The eight `cpu@` nodes in `sm8350.dtsi` (117,937 B, 4,634 lines):

| node | line | `compatible` | `reg` | `qcom,freq-domain` |
|---|---:|---|---|---|
| `cpu0` | 57 | `arm,cortex-a55` | `0x0` | `cpufreq_hw 0` |
| `cpu1` | 81 | `arm,cortex-a55` | `0x100` | `cpufreq_hw 0` |
| `cpu2` | 100 | `arm,cortex-a55` | `0x200` | `cpufreq_hw 0` |
| `cpu3` | 119 | `arm,cortex-a55` | `0x300` | `cpufreq_hw 0` |
| `cpu4` | 138 | `arm,cortex-a78` | `0x400` | `cpufreq_hw 1` |
| `cpu5` | 157 | `arm,cortex-a78` | `0x500` | `cpufreq_hw 1` |
| `cpu6` | 176 | `arm,cortex-a78` | `0x600` | `cpufreq_hw 1` |
| `cpu7` | 195 | `arm,cortex-x1` | `0x700` | `cpufreq_hw 2` |

Three facts follow, and all three are DT facts rather than inference:

1. **The big-core count is three, not four.** `cpu4`-`cpu6` are A78; `cpu7`
   alone is X1. A "4+4" reading of this SoC would put four A78 in the middle
   cluster and none of the DT supports it [F].
2. **One `cpu-map` cluster, not three.** `sm8350.dtsi:214-250` declares
   `cpu-map { cluster0 { core0 … core7 } }` — eight `coreN` children under a
   single `cluster0`. There is no `cluster1` or `cluster2` node. The three
   frequency domains are therefore expressed **only** through
   `qcom,freq-domain`, not through the topology description [F].
3. **One shared L3, referenced by all eight cores.** `l3_0` is declared
   **once**, nested inside `cpu0`'s `l2_0`, at `:73-77` with
   `cache-level = <3>` and `cache-unified`. Every one of the eight cores' L2
   nodes points at it via `next-level-cache = <&l3_0>` — eight references, at
   `:72`, `:96`, `:115`, `:134`, `:153`, `:172`, `:191` and `:210` — and
   `grep -c "l3_0: l3-cache"` returns **1**. A single L3 across all eight cores
   is the shared-cluster/DSU arrangement, not three independent L3s [F].

`cpu7` is the only core with an explicitly named L2 (`l2_700`, `:206-211`);
the others rely on the same pattern with their own labels. The
`enable-method` on every core is `"psci"` [F].

Practical consequence for a port: the DT will describe an 8-core single-cluster
machine to any consumer that reads `cpu-map`, while `qcom,freq-domain` and
`cpufreq_hw` carry the real three-domain structure. A scheduler or thermal
consumer that derives cluster structure from `cpu-map` alone will see one
cluster [I].

Three things this section deliberately does not cover, because they belong to
the core rather than the package: the **MIDR values** for each of the three
clusters, the **vendor `lahaina.dtsi`**, which describes the same eight cores
with `qcom,kryo` ×8, three `cpu-map` clusters and a 2048 prime capacity, and the
**CPUCP** co-processor. Those are in
`Qualcomm-SM8350-Snapdragon-888-cpu.md` §2–§5. Note in particular that mainline
is the outlier here: this is one of the few Qualcomm SoCs in mainline that names
real ARM cores (`arm,cortex-a55`/`a78`/`x1`) instead of `qcom,kryo`.

## 2. GPU and DSP core identification

### 2.1 GPU — cited, not repeated

The GPU is an **Adreno 660**, chip ID `0x06060001`, family `ADRENO_6XX_GEN4`.
Three independent proofs, the catalog entry at `a6xx_catalog.c:1079-1098`, the
`.zapfw`/`.gmu`/`.sqe` filenames, the 11 GPU rows / 7 filenames, the two
`a660_zap.mdt` builds, and the `a619_gmu.bin` + `a630_sqe.fw` dead-entry
argument are all owned by `Qualcomm-SM8350-Snapdragon-888-gpu.md` §1-§4 [F].

Two SoC-package-relevant additions only:

- The GPU node is `gpu@3d00000` (`sm8350.dtsi:2039-2062`) with
  `compatible = "qcom,adreno-660.1", "qcom,adreno"` and **`status = "disabled"`**
  in the SoC dtsi. The GMU node is `gmu@3d6a000` (`:2120`) with
  `compatible = "qcom,adreno-gmu-660.1", "qcom,adreno-gmu"` [F].
- The GPU OPP table (`:2065-2118`) carries **10** levels, `315 MHz` to
  `840 MHz`, the top level gated on `RPMH_REGULATOR_LEVEL_TURBO_L1`, with the
  dtsi's own comment `/* note: downstream checks gpu binning for 670 Mhz */`
  (`:2064`). The binning note is a comment, not a binding [F].

### 2.2 Compute DSP — the identification is marketing, and the corpus says so

**Verdict: the SM8350 compute DSP is Hexagon 780 by marketing name and
`hexagon-v68` by toolchain architecture. The corpus contains no ISA proof, and
this note does not manufacture one.**

| claim | evidence | class |
|---|---|---|
| Hexagon 780 / `hexagon-v68` for SM8350 | public spec pages, fetched 2026-11-21, recorded in `docs/devices/motorola/Moto_G200/cdsp.md:15` | [F] for the citation |
| executable container is QDSP6 ELF, `e_machine` 164 | public CDSP witnesses parsed in `Moto_G200/cdsp.md:106` | [F] for those witnesses |
| **no segment of any SM8350 DSP image was disassembled** | `Moto_G200/cdsp.md:106` records `isa_identified` EMPTY on **all 18** corpus rows | [N] |
| the `cdsp`/`adsp` blobs in *this* slice are the same family | §6.3 below: 16 and 26 split segments, `mdt == b00+b01` on both | [F] |

So the honest position is: the *name* is settled and the *container format* is
settled on public witnesses, but **nothing in this repository identifies the
instruction set from an SM8350 payload** [N]. The 18 CDSP rows in this slice
are 6,008,371 B total; their largest segment is 2,739,464 B (45.71% of the
family) in the `Moto_G200` sibling document's measurement, which is a size
observation and not a decode [I].

Two negative results that matter for a future DSP note:

- `research/fleet/pil-metadata-sweep.md` establishes the SHA-384 hash-slot law
  across 16 SM8250 and 12 SDM845 images, 28/28 with zero exceptions. It contains
  **zero** mentions of SM8350 [F]. The law is therefore *unverified* for this
  SoC, not disproved — a follow-up needs SM8350 payloads, which are absent [N].
- `drivers/mailbox/qcom-cpucp-mbox.c` binds only
  `qcom,nord-cpucp-mbox` and `qcom,x1e80100-cpucp-mbox` (`:204-205`). There is
  **no** `sm8350` CPUCP mailbox compatible, and `sm8350.dtsi` carries a
  `cpucp_fw_mem` reserved region (`:452`, 0x80b00000/0x100000) but **no CPUCP
  node** [F]. The reserved hole exists; the driver binding does not.

## 3. The remoteproc set — four PAS nodes, two of them borrowing another SoC's descriptor

`sm8350.dtsi` declares **four** `remoteproc` nodes:

| label | node | line | `compatible` | MMIO |
|---|---|---:|---|---|
| `adsp` | `remoteproc@3000000` | 1889 | `qcom,sm8350-adsp-pas` | `0x03000000`+`0x10000` |
| `mpss` | `remoteproc@4080000` | 2225 | `qcom,sm8350-mpss-pas` | `0x04080000`+`0x10000` |
| `slpi` | `remoteproc@5c00000` | 2267 | `qcom,sm8350-slpi-pas` | `0x05c00000`+`0x4000` |
| `cdsp` | `remoteproc@a300000` | 2509 | `qcom,sm8350-cdsp-pas` | `0x0a300000`+`0x10000` |

Each carries a `memory-region` pointing at its `pil_*` carve-out (§5), a
`qcom,qmp = <&aoss_qmp>`, and an `smp2p_*` state pair. `slpi`'s MMIO window is
`0x4000`, one quarter the size of the other three [F].

### 3.1 The driver side: two descriptors are shared with other SoCs

`drivers/remoteproc/qcom_q6v5_pas.c` maps the four compatibles to resource
descriptors, and **two of the four are not SM8350-specific**:

| compatible | line | descriptor | descriptor's own origin | firmware name it asks for |
|---|---:|---|---|---|
| `qcom,sm8350-adsp-pas` | 2061 | `sm8350_adsp_resource` (`:1198`) | SM8350 | **`adsp.mdt`** |
| `qcom,sm8350-cdsp-pas` | 2062 | `sm8350_cdsp_resource` (`:1415`) | SM8350 | **`cdsp.mdt`** |
| `qcom,sm8350-slpi-pas` | 2063 | `sdm845_slpi_resource_init` (`:1515`) | **SDM845** | **`slpi.mdt`** |
| `qcom,sm8350-mpss-pas` | 2064 | `mpss_resource_init` (`:1466`) | **generic** | **`modem.mdt`** |

This is a real structural fact and it is easy to miss: **SM8350 has no
SM8350-named SLPI or modem resource descriptor.** The SLPI node reuses the
SDM845 one, including its `ssr_name = "dsps"` and `ssctl_id = 0x16`; the modem
node reuses the shared `mpss_resource_init` with `pas_id = 4`,
`minidump_id = 3` and `auto_boot = false` [F].

The `sm8350_adsp_resource` / `sm8350_cdsp_resource` pair, in contrast, is the
**shared** one for newer parts: `qcom,sar2130p-adsp-pas` (`:2022`),
`qcom,sc7280-adsp-pas` (`:2025`), `qcom,sm8450-adsp-pas` (`:2065`) and
`qcom,sm8450-cdsp-pas` (`:2066`) all point at them [F]. So the SM8350 ADSP/CDSP
descriptors are the *donor*, and the SM8350 SLPI/modem descriptors are the
*borrower*. Both directions occur in one SoC.

Descriptor details worth recording, since they are what a port must satisfy:

| field | `adsp` | `cdsp` | `slpi` (sdm845) | `mpss` (generic) |
|---|---:|---:|---:|---:|
| `crash_reason_smem` | 423 | 601 | 424 | 421 |
| `pas_id` | 1 | 18 | 12 | 4 |
| `minidump_id` | — | 7 | — | 3 |
| `auto_boot` | true | true | true | **false** |
| `proxy_pd_names` | `lcx`,`lmx` | `cx`,`mxc` | `lcx`,`lmx` | `cx`,`mss` |
| `load_state` | `adsp` | `cdsp` | `slpi` | — |
| `ssr_name` | `lpass` | `cdsp` | **`dsps`** | — |
| `ssctl_id` | `0x14` | `0x17` | `0x16` | — |

`auto_boot = false` on the modem is the notable asymmetry: ADSP, CDSP and SLPI
come up with the driver, the modem does not [F].

### 3.2 Where the firmware name actually comes from

`qcom_q6v5_pas.c:923-932` reads `firmware-name` from the DT node and falls back
to `desc->firmware_name` only if the property is absent:

```c
fw_name = desc->firmware_name;
ret = of_property_read_string(pdev->dev.of_node, "firmware-name", &fw_name);
```

So the `.mdt` strings in the descriptor table are **defaults**, and every SM8350
board DT overrides them with a `.mbn` path (§6.2). `sm8350.dtsi` itself sets
**zero** `firmware-name` properties — `grep -c "firmware-name"` returns 0 — so
the SoC dtsi alone would request the four `.mdt` defaults, and only the board
DTs redirect to `.mbn` [F].

## 4. Boot chain: what the corpus actually holds

The slice contains **13 `boot`-family rows / 10 distinct filenames** and **98
`tz`-family rows / 98 distinct filenames**. The chain images present, by device:

| image | family | OnePlus_9_Pro | Xperia_5_III |
|---|---|---:|---:|
| `xbl.img` | boot | 4,313,088 | ABSENT |
| `xbl_config.img` | boot | 221,184 | ABSENT |
| `abl.img` | boot | 217,088 | ABSENT |
| `aop.img` | boot | 245,760 | ABSENT |
| `qupfw.img` | boot | 57,344 | ABSENT |
| `shrm.img` | boot | 49,152 | ABSENT |
| `cpucp.img` | boot | 110,592 | ABSENT |
| `tz.img` | tz | 3,932,160 | ABSENT |
| `hyp.img` | tz | 3,739,648 | ABSENT |
| `devcfg.img` | tz | 53,248 | ABSENT |
| `keymaster.img` | tz | 286,720 | ABSENT |
| `uefisecapp.img` | tz | 126,976 | ABSENT |
| `multiimgoem.img` | tz | 16,384 | ABSENT |
| `featenabler.img` | tz | 90,112 | ABSENT |
| `vbmeta.img` | boot | 8,192 | 8,192 |
| `boot.img` | boot | 201,326,592 | 100,663,296 |
| `dtbo.img` | boot | 25,165,824 | 25,165,824 |

**The asymmetry is the finding.** The Xperia 5 III contributes **three** chain
images and nothing else — `boot.img`, `dtbo.img`, `vbmeta.img`. It has no
`xbl`, no `tz`, no `hyp`, no `abl`. The OnePlus 9 Pro contributes the full
fourteen-image chain. Any statement of the form "the SM8350 boot chain is X"
is therefore a statement about **one device**, and this slice cannot confirm the
chain on the Sony side at all [F].

Three observations from the sizes:

1. **`boot.img` differs in kind, not degree.** 201,326,592 B and 100,663,296 B
   are both exact multiples of 1 MiB (192 and 96 MiB) and of 4096 (49,152 and
   24,576 sectors). `dtbo.img` is identical in size on both devices
   (25,165,824 B = 24 MiB) but **differs in md5** — same size, different bytes,
   which is what a per-device DTB-overlay set looks like [F]/[I].
2. **`dsp.img` is exactly 64 MiB.** The OnePlus carries `dsp.img` at
   67,108,864 B = 64 MiB exactly = 16,384 sectors. A power-of-two round number
   of that size is a partition-sized container, not a file-sized artifact; on
   the OnePlus 6 the analogous `dsp.img` was proven to be **ext4**
   (`research/fleet/dsp-tz-map.md` §1), and this note does not claim the SM8350
   one has the same format because no payload is on disk [I]/[N].
3. **`modem.img` (219,983,872 B) is not the sum of the split modem segments.**
   The split set is `modem.mdt` 8,788 B plus 26 `modem.bNN` totalling
   87,277,378 B = 87,286,166 B, leaving **132,697,706 B unaccounted**. So
   `modem.img` is a container that holds the split set plus roughly 1.5× its
   size in other content — it is not a flat concatenation of what the census
   captured [F] for the arithmetic, [N] for what the remainder is.

OnePlus-only images beyond the standard chain, all under
`oneplus/lemonadep/radio`: `oplus_sec.img` 294,912; `oplusstanvbk.img`
9,162,752; `qweslicstore.img` 262,144; `engineering_cdt.img` 1,048,576;
`splash.img` 344,064; `bluetooth.img` 1,912,832 [F]. These are OEM additions,
not Qualcomm chain stages.

## 5. TrustZone layout: 25 reserved regions, 671.19 MiB

`sm8350.dtsi:419-555` is one `reserved-memory` node containing **25** regions —
24 with a label, plus the unlabelled `smem@80900000` node. Total reserved:
**703,791,104 B = 671.19 MiB**.

| region | base | size | MiB | role |
|---|---|---:|---:|---|
| `hyp_mem` | `0x80000000` | `0x00600000` | 6.00 | hypervisor |
| `xbl_aop_mem` | `0x80700000` | `0x00160000` | 1.38 | XBL/AOP handoff |
| `cmd_db` | `0x80860000` | `0x00020000` | 0.12 | RPMh command DB |
| `reserved_xbl_uefi_log` | `0x80880000` | `0x00014000` | 0.08 | XBL UEFI log |
| `smem` | `0x80900000` | `0x00200000` | 2.00 | shared memory, hwlock 3 |
| `cpucp_fw_mem` | `0x80b00000` | `0x00100000` | 1.00 | CPUCP firmware |
| `cdsp_secure_heap` | `0x80c00000` | `0x04600000` | 70.00 | CDSP secure heap |
| `pil_camera_mem` | `0x85200000` | `0x00500000` | 5.00 | camera PAS |
| `pil_video_mem` | `0x85700000` | `0x00500000` | 5.00 | video PAS |
| `pil_cvp_mem` | `0x85c00000` | `0x00500000` | 5.00 | CVP PAS |
| `pil_adsp_mem` | `0x86100000` | `0x02100000` | 33.00 | ADSP PAS |
| `pil_slpi_mem` | `0x88200000` | `0x01500000` | 21.00 | SLPI PAS |
| `pil_cdsp_mem` | `0x89700000` | `0x01e00000` | 30.00 | CDSP PAS |
| `pil_ipa_fw_mem` | `0x8b500000` | `0x00010000` | 0.06 | IPA firmware |
| `pil_ipa_gsi_mem` | `0x8b510000` | `0x0000a000` | 0.04 | IPA GSI |
| `pil_gpu_mem` | `0x8b51a000` | `0x00002000` | 0.01 | GPU zap shader |
| `pil_spss_mem` | `0x8b600000` | `0x00100000` | 1.00 | SPSS |
| `pil_modem_mem` | `0x8b800000` | `0x10000000` | 256.00 | modem PAS |
| `rmtfs_mem` | `0x9b800000` | `0x00280000` | 2.50 | RMTFS, client-id 1 |
| `hyp_reserved_mem` | `0xd0000000` | `0x00800000` | 8.00 | hypervisor reserved |
| `pil_trustedvm_mem` | `0xd0800000` | `0x076f7000` | 118.96 | TrustedVM |
| `qrtr_shbuf` | `0xd7ef7000` | `0x00009000` | 0.04 | QRTR shared buffer |
| `chan0_shbuf` | `0xd7f00000` | `0x00080000` | 0.50 | IPC channel 0 |
| `chan1_shbuf` | `0xd7f80000` | `0x00080000` | 0.50 | IPC channel 1 |
| `removed_mem` | `0xd8800000` | `0x06800000` | 104.00 | removed from Linux |

Every region carries `no-map` except `cmd_db` (which is `no-map` too) and the
`smem` node, which is `no-map` with `hwlocks = <&tcsr_mutex 3>` [F].

### 5.1 The layout is contiguous by construction — and the gaps are the signal

Sorting by base and testing `end(N) == start(N+1)`:

- **15 consecutive pairs are exactly contiguous** — `xbl_aop_mem`→`cmd_db`→
  `reserved_xbl_uefi_log`, then `smem`→`cpucp_fw_mem`→`cdsp_secure_heap`→
  `pil_camera_mem`→`pil_video_mem`→`pil_cvp_mem`→`pil_adsp_mem`→
  `pil_slpi_mem`→`pil_cdsp_mem`→`pil_ipa_fw_mem`→`pil_ipa_gsi_mem`, and
  `pil_modem_mem`→`rmtfs_mem`, and `hyp_reserved_mem`→`pil_trustedvm_mem`→
  `qrtr_shbuf`→`chan0_shbuf`→`chan1_shbuf` [F].
- **Six gaps exist**, and each is a specific size: 1 MiB after `hyp_mem`,
  432 KiB after `reserved_xbl_uefi_log`, 912 KiB after `pil_gpu_mem`, 1 MiB
  after `pil_spss_mem`, 8 MiB after `chan1_shbuf`, and one very large 857,600
  KiB (838.67 MiB) hole between `rmtfs_mem` (ends `0x9ba80000`) and
  `hyp_reserved_mem` (`0xd0000000`) [F].

The four small gaps (1 MiB, 432 KiB, 912 KiB, 1 MiB, 8 MiB) are alignment or
guard holes. The 838.67 MiB hole between `0x9ba80000` and `0xd0000000` is
**not** reserved in the DT at all — it is the region the bootloader is free to
hand to Linux as system RAM. That is the single most useful number in this
section for a memory-map reconstruction: the reserved block below `0xd0000000`
occupies `0x80000000`-`0x9ba80000` plus the two `0xd...` clusters, and the
middle is the kernel's [F] for the arithmetic, [I] for the "handed to Linux"
reading.

### 5.2 TrustZone-adjacent nodes that do exist

| node | line | detail |
|---|---:|---|
| `firmware/scm` | 293-300 | `compatible = "qcom,scm-sm8350", "qcom,scm"`; `qcom,dload-mode = <&tcsr 0x13000>`; `sram = <&minidump_config>`; `#reset-cells = <1>` |
| `aoss_qmp` | 3292 | `power-management@c300000`; driver binds `qcom,sm8350-aoss-qmp` (`qcom_aoss.c:652`) |
| `tcsr_mutex` | 1878 | `qcom,tcsr-mutex` at `hwlock@1f40000`, backs `smem`'s hwlock 3 |
| `ipcc` | 704 | `mailbox@408000` |

`scm` is the only node that names the secure monitor, and it names it as
**SM8350-specific** (`qcom,scm-sm8350`) while the SLPI/modem PAS descriptors are
borrowed (§3.1) — the reverse of the usual pattern [F].

## 6. Firmware families: what ships, what is absent

### 6.1 The slice in nine families

693 rows / 2 devices / 886,208,933 B / 651 distinct filenames.

| family | rows | files | bytes | share of bytes |
|---|---:|---:|---:|---:|
| `other` | 324 | 297 | 149,102,682 | 16.8% |
| `wifi` | 155 | 154 | 17,042,793 | 1.9% |
| `tz` | 98 | 98 | 12,511,746 | 1.4% |
| `adsp` | 41 | 35 | 34,505,121 | 3.9% |
| `modem` | 32 | 31 | 307,285,000 | **34.7%** |
| `cdsp` | 18 | 18 | 6,008,371 | 0.7% |
| `boot` | 13 | 10 | 357,552,128 | **40.3%** |
| `gpu` | 11 | 7 | 288,260 | 0.03% |
| `bt` | 1 | 1 | 1,912,832 | 0.2% |

Per device: `OnePlus_9_Pro` 650 rows / 626 files / 748,523,070 B;
`Xperia_5_III` 43 rows / 43 files / 137,685,863 B. The Xperia contributes 6.2%
of rows but 15.5% of bytes, entirely because its single `boot.img` is 100 MiB
[F].

**Two families dominate and neither is interesting.** `boot` (40.3%) is
`boot.img` + `dtbo.img` + the chain images; `modem` (34.7%) is `modem.img`
(219,983,872 B) plus the split modem set. Together they are 75% of the slice's
bytes and 45 of 693 rows. The DSP and TZ families — the ones a reverse engineer
wants — are **2.7%** of bytes between them [F].

**The `wifi` family is almost entirely one device.** 152 of 155 rows are
`OnePlus_9_Pro`; the Xperia contributes 3. Of the 155, **146 are
`bdwlan.eNN`** board-data files under `oneplus/lemonadep/modem/image`, one per
hex suffix from `e01` to `ee1` with gaps. Distinct bdwlan sizes cluster at
59,868 / 59,872 / 59,932 B [F].

### 6.2 linux-firmware ships **one symlink** for this SoC

This is the central finding of the note. `WHENCE` in `linux-firmware` `main`
contains, for the SM8350 directory:

```
File: qcom/sm8350/...    → 0 entries
Link: qcom/sm8350/...    → 1 entry
RawFile: qcom/sm8350/... → 0 entries
                            ─────────
                            total 1
```

The single entry is `WHENCE:7280`:

```
Link: qcom/sm8350/a660_zap.mbn -> ../qcm6490/a660_zap.mbn
```

So **`qcom/sm8350/` contains exactly one name, and it is a pointer to the
QCM6490 IoT part's shader.** There is no `qcom/sm8350/adsp.mbn`, no `cdsp`, no
`modem`, no `slpi`, no `ipa_fws`. For comparison, measured the same way:

| directory | File | Link | RawFile | total |
|---|---:|---:|---:|---:|
| `qcom/sm8350/` | 0 | 1 | 0 | **1** |
| `qcom/sm8250/` | 4 | 0 | 5 | 9 |
| `qcom/qcm6490/` | 6 | 1 | 5 | 12 |
| `qcom/qcs6490/` | 7 | 12 | 6 | 25 |

The sibling `qcom/qcm6490/` — the IoT/compute variant of the same Kodiak-family
silicon — has **twelve** entries including `adsp.mbn` (12,111,452 B, version
`ADSP.HT.5.5.c8-00256.2-KODIAK-1`), `cdsp.mbn` (`CDSP.HT.2.5.c3-00134-KODIAK-1`),
`ipa_fws.mbn`, `qupv3fw.elf` and `a660_zap.mbn` (1,054,648 B, `v0.09`) [F].

**A methodological correction, recorded because I made it.** A `HEAD` request to
`git.kernel.org` for `qcom/sm8350/a660_zap.mbn` returns **404**, and so does
`qcom/qcs6490/adsp.mbn` — a path that is a known-good symlink. git.kernel.org
does not serve symlinked blobs through `plain/`. So a 404 from that host proves
nothing about presence, and `WHENCE` is the only authoritative manifest. Every
absence claim in this section is a `WHENCE` count, not a `HEAD` probe [F].

### 6.3 Every board DT requests firmware that does not ship

Mainline has **7** SM8350 DT files: `sm8350.dtsi`, `sm8350-mtp.dts`,
`sm8350-hdk.dts`, `sm8350-microsoft-surface-duo2.dts`,
`sm8350-sony-xperia-sagami.dtsi`, `sm8350-sony-xperia-sagami-pdx214.dts`,
`sm8350-sony-xperia-sagami-pdx215.dts`. There is **no** `lemonade`/`lemonadep`
DT and **no** `xpeng` DT — the two devices in this slice have no mainline board
DT at all, and the Xperia is covered only as `pdx214` [F].

The four board DTs set these `firmware-name` values:

| board DT | requests | resolves in WHENCE? |
|---|---|---|
| `sm8350-mtp.dts` | `qcom/sm8350/adsp.mbn` (:43), `cdsp.mbn` (:281), `modem.mbn` (:286), `slpi.mbn` (:308) | 0 of 4 |
| `sm8350-hdk.dts` | `adsp.mbn` (:122), `cdsp.mbn` (:382), `a660_zap.mbn` (:409), `qcom/vpu/vpu20_p4_sm8350.mbn` (:476), `modem.mbn` (:495), `slpi.mbn` (:561), `ipa_fws.mbn` (:936) | **1 of 7** (`a660_zap.mbn`) |
| `sm8350-sony-xperia-sagami.dtsi` | `qcom/sm8350/Sony/sagami/{adsp,cdsp,ipa_fws,modem,slpi}.mbn` (:120, :473, :556, :563, :659) | 0 of 5 |
| `sm8350-microsoft-surface-duo2.dts` | `qcom/sm8350/microsoft/{adsp,cdsp,modem,slpi}.mbn` (:43, :281, :298, :311) | 0 of 4 |

**Eleven distinct paths are requested; one resolves.** The resolving one,
`qcom/sm8350/a660_zap.mbn`, resolves only through the QCM6490 symlink [F].

And `sm8350.dtsi` sets **zero** `firmware-name` properties, so the four
remoteproc nodes inherit the `.mdt` defaults from the PAS descriptor table
(§3.2). Those defaults name `adsp.mdt`, `cdsp.mdt`, `modem.mdt`, `slpi.mdt` —
and `qcom/adsp.mdt` etc. at the top level are also **0** WHENCE entries [F].

The GPU case is the sharpest illustration. `&gpu` is enabled on **one** board
only — `sm8350-hdk.dts:404-406` — and that board is the only one that overrides
the zap shader (`:408-410`). `sm8350-mtp.dts`, `sm8350-microsoft-surface-duo2.dts`
and the whole Sony sagami tree never touch `&gpu`, so on those boards the GPU
stays `status = "disabled"` as the dtsi left it [F]. A `sm8350-mtp` boot
therefore has no GPU regardless of firmware, and an `sm8350-hdk` boot has a GPU
whose zap shader is a symlink to an IoT part's shader.

### 6.4 The split-segment law: 23 of 23, and 15 stems that are not split

The slice contains **38** `.mdt` stems. Classifying each by whether it has
`.b00`/`.b01`:

| class | count | test |
|---|---:|---|
| split | **23** | `size(b00) + size(b01) == size(mdt)` — **23/23 EQUAL, zero exceptions** |
| self-contained | 15 | no `b00`/`b01` in the slice |

The 23 split stems include all four DSP images and all ten TZ applets under
`modem/image`:

| stem | `mdt` | `b00` | `b01` | sum | segments |
|---|---:|---:|---:|---:|---:|
| `modem` | 8,788 | 980 | 7,808 | 8,788 | 26 |
| `adsp` | 8,628 | 916 | 7,712 | 8,628 | 26 |
| `slpi` | 8,468 | 852 | 7,616 | 8,468 | 24 |
| `cdsp` | 7,828 | 596 | 7,232 | 7,828 | 16 |
| `featenabler` | 20,440 | 512 | 19,928 | 20,440 | 8 |
| `haventkn` | 20,440 | 512 | 19,928 | 20,440 | 8 |
| `hdcp1`,`hdcp2p2`,`hdcpsrm`,`loadalgota64`,`smplap64`,`soter64`,`sp_license`,`winsecap`,`mldapta`,`identity_credential`,`eseservice`,`evautil64`,`fingerpr` | 7,312 each | 512 | 6,800 | 7,312 | 8 |
| `evautil`,`gpqese`,`smplap32`,`voicepri` | 7,108 each | 308 | 6,800 | 7,108 | 8 |

The 15 self-contained stems — `a615_zap`, `a660_zap`, `egista`, `evass`,
`evass-lt`, `goodixfp`, `ipa_fws`, `tzhdcp`, `tzsecuredata`, `tzsuntory`,
`tztpm`, `vpu20_1v`, `vpu20_2v`, `vpu20_4v`, `yupik_ipa_fws` — have an `.mdt`
and no segments in this slice. That is a **census gap, not a format property**:
an `.mdt` is always the header+hash pair by construction, so these files are
either genuinely single-file or their segments simply were not collected [I] for
the reading, [N] for which it is.

**A trap I walked into and am recording.** The naive form of the law is "the
segments sum to the `.mdt`". That is false and it is false by two orders of
magnitude: `adsp`'s 26 segments sum to **16,748,845 B** against an 8,628 B
`.mdt`; `cdsp`'s 16 sum to **6,000,030 B** against 7,828. Only the **`b00`+`b01`
pair** equals the `.mdt`, because those two are the ELF header and the hash
segment and everything from `b02` on is payload. The correct statement is
narrow, and the narrow statement holds 23/23 [F].

### 6.5 `b00` encodes the ELF class — and the filename suffix agrees with it

The `b00` size is not arbitrary. It is the ELF header plus the program-header
table, so it decomposes as `52 + 32N` for ELF32 and `64 + 56N` for ELF64 (52- and
64-byte headers, **32-byte ELF32 program headers and 56-byte ELF64 program
headers**). Every one of the 23 split stems fits one of the two forms exactly:

| form | stems |
|---|---:|
| `52 + 32N` (ELF32) | **8** |
| `64 + 56N` (ELF64) | **15** |
| neither | **0** |

And `N` tracks the segment count, with a small constant offset:

| stem | `b00` | form | `N` | segments | `N − segments` |
|---|---:|---|---:|---:|---:|
| `adsp` | 916 | `52+32×27` | 27 | 26 | 1 |
| `cdsp` | 596 | `52+32×17` | 17 | 16 | 1 |
| `slpi` | 852 | `52+32×25` | 25 | 24 | 1 |
| `modem` | 980 | `52+32×29` | 29 | 26 | 3 |
| `evautil`,`gpqese`,`smplap32`,`voicepri` | 308 | `52+32×8` | 8 | 8 | 0 |
| 15 ELF64 stems | 512 | `64+56×8` | 8 | 8 | **0** |

`N − segments` is the count of program headers that do **not** have a `bNN`
file of their own — the `PT_NULL`/hash/certificate entries. That it is zero for
every ELF64 stem and small for the big ELF32 DSP stems, and that `modem` needs
three more than `adsp`, is consistent with the `.mdt` carrying header+hash and
the payload being split off (§6.4) [I] for the interpretation, [F] for the
arithmetic.

[F] **Correction (2026-11-24, from `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-soc.md` §7.2):**
this section originally gave the ELF64 form as `64 + 32N` and the ELF64 row as
`64+32×14` with `N − segments = 6`. Both were wrong: an ELF64 program header is
**56 bytes**, not 32. `512 = 64 + 56×8`, so each ELF64 stem here has **8**
program headers for 8 segments and the residual is **0**, not 6. The count of
stems (15) and the 7-of-7 suffix match are unaffected.

**The filename suffix agrees with the header.** Of the 23 stems, seven carry an
explicit `32` or `64` suffix, and all seven match:

| stem | suffix | `b00` form | verdict |
|---|---|---|---|
| `smplap32` | 32 | ELF32 | **match** |
| `smplap64` | 64 | ELF64 | **match** |
| `evautil64` | 64 | ELF64 | **match** |
| `loadalgota64` | 64 | ELF64 | **match** |
| `soter64` | 64 | ELF64 | **match** |
| `evautil` | — | ELF32 | n/a |
| the other 16 | — | mixed | n/a |

**7 of 7, zero mismatches.** This is a usable rule: on this SoC, a TZ applet
named `…32` is a 32-bit ELF and one named `…64` is a 64-bit ELF, and the `b00`
size confirms it without opening the file. It also means the pairs
`evautil`/`evautil64` and `smplap32`/`smplap64` are the same applet built for two
ELF classes — `evautil` is the 32-bit build of `evautil64`, not a different tool
[F] for the sizes and suffix correlation, [I] for the "same applet, two builds"
reading.

Matrix-wide the law is stronger than this note originally thought, not weaker:
of the **122** distinct stem names carrying both an `.mdt` and a `.b00`, **49**
fit `52+32N` and **73** fit `64+56N`, with **0** fitting neither [F]. The
earlier draft reported "56 / 28 / 38 neither, clustering at `b00 = 568`" — that
was the same wrong constant: `568 = 64 + 56×9`, so the 42 stems at 568 were
ELF64 all along, and so was the 400-byte one. So the two-form law holds
corpus-wide on every `.mdt`+`.b00` stem, not just on this slice [F] — though it
remains a size-level regularity, not a parsed header (§9 item 16).

### 6.6 Three different spellings, and only the third is missing

For each of the four DSP images, three names exist in three places and they do
not agree:

| place | spelling | present? |
|---|---|---|
| board DT `firmware-name` | `qcom/sm8350/adsp.mbn` | no (0 WHENCE) |
| corpus | `adsp.mdt` + `adsp.b00`…`adsp.b25` | yes, 1 device |
| PAS descriptor default | `adsp.mdt` | no (`qcom/adsp.mdt` = 0 WHENCE) |

Matrix-wide, the `.mbn` spellings are **entirely absent from the corpus**:
`adsp.mbn` 0 rows, `cdsp.mbn` 0, `modem.mbn` 0, `slpi.mbn` 0, `ipa_fws.mbn` 0,
`a660_zap.mbn` 0 — out of 33,917 rows. The `.mdt` spellings are present both
inside this slice (1 row each for `adsp`/`cdsp`/`modem`/`slpi`, 2 for
`a660_zap`) and matrix-wide (59, 63, 59, 19 and 21 rows respectively), so the
`.mdt` name is the corpus's normal spelling everywhere, not an SM8350 quirk [F].

So the string in the DT, the string on the device, and the string in
linux-firmware are **three different strings**, and the only one that resolves
upstream is the GPU zap shader — via a symlink to a different SoC. This is a
cleaner statement of the gap than "the firmware is missing": it is missing
under the name that is asked for, present under a name that is not asked for,
and absent under the fallback name as well [F].

### 6.7 Which families are absent outright

Beyond the DSP images, several families a reader might expect are simply not in
the slice:

| expected | present in slice? | note |
|---|---|---|
| `tz.mdt` / `hyp.mdt` / `aop.mdt` / `xbl.mdt` | **no** — 0 rows matrix-wide | the chain is carried as monolithic `.img` (§4) |
| `a660_zap.b00`/`.b01`/`.b02` | **no** — 0 rows in this slice | those 9 rows exist matrix-wide but on `Moto_G200`, `Edge_30_Fusion`, `Edge_30` — not SM8350-labelled (§9.2) |
| `board-2.bin` | **no** — 0 rows matrix-wide | WCN6855 ships it in WHENCE (`ath11k/WCN6855/hw2.0/board-2.bin`) but the corpus never captured it |
| `a630_gmu.bin` | **no** | the a615 entry names it as its GMU firmware; not in the slice |
| `qupv3fw.elf` | **no** | ships for `qcm6490` in WHENCE, not captured here |
| `slpi.bNN` beyond `b01` | **yes**, 24 segments | `slpi` is the only DSP with a `.mdt` on OnePlus and no Sony counterpart |

The `tz` family is the reverse case: **98 rows, 98 distinct filenames, all
present**, but 90 of them are the ten TZ applets' `b00`-`b07` sets under
`oneplus/lemonadep/modem/image` and only 8 are standalone images
(`tz.img`, `hyp.img`, `devcfg.img`, `keymaster.img`, `uefisecapp.img`,
`multiimgoem.img`, `featenabler.img` on OnePlus; `tzhdcp.mdt` on Sony). So "98
TZ rows" sounds like a rich TZ corpus and is really **10 applets plus 1
image set** [F].

## 7. The `.bNN` filename trap: 84 Bluetooth patch files that look like MDT segments

A filename grammar is not a container format. The slice contains **84** files
under `oneplus/lemonadep/bluetooth/image` whose names end in `.bNN` and which
therefore pattern-match an MDT split segment:

```
hpnv10.b03  hpnv10.b04  hpnv10.b06  hpnv10.b07  hpnv10.b08
hpnv10.b0E  hpnv10.b0F  hpnv10.b10  hpnv10.b11  hpnv10.b17
hpnv10.b18  hpnv10.b1a  hpnv10.b1d  ...
hpnv20.*  hpnv21.*  hpnv21g.*
```

Four independent reasons these are **not** MDT segments:

1. **Uppercase and non-sequential suffixes.** `b0E`, `b0F`, `b1a`, `b5A`, `b7C`
   appear. MDT segments are lowercase and strictly sequential from `b00`
   (compare `adsp.b00`…`adsp.b25`, `modem.b00`…`modem.b25`) [F].
2. **The base name has a `.bin` form, not a `.mdt`.** The stems are `hpnv10`,
   `hpnv20`, `hpnv21`, `hpnv21g` — Bluetooth patch-file names — and there is
   **no** `hpnv10.mdt` in the slice, correctly, because there is no container
   [F].
3. **Sizes repeat in groups.** Many of the files are 5,753 B or 5,777 B, and
   multiple distinct suffixes share one md5 (`8aef8eb2…` on 5,753-byte files,
   `61f00949…` on 5,777-byte files). MDT segments do not collide like that;
   Bluetooth patch tables reuse a small set of payloads across antenna/region
   variants [F] for the digests, [I] for the reason.
4. **The directory is `bluetooth/image`,** not `modem/image`. Every genuine MDT
   stem in this slice lives under `modem/image` [F].

The practical rule this supports: **`.bNN` alone is not evidence of an MDT
container.** The discriminator is a bare `.mdt` sibling plus lowercase
sequential suffixes plus the `modem/image` (or `vendor/firmware`) path. Applying
the naive rule inflates the MDT count by 84 files and 4 phantom stems [F].

This matters beyond bookkeeping. The earlier `per-soc-method-plans.md:87-90`
`tundra` note (reported separately) and the `find -iname '*.mdt'` vs
`find -name '*.mdt'` discrepancy noted in #2029 are the same class of error: a
name-shaped heuristic standing in for a structural test.

## 8. Mainline and postmarketOS status

### 8.1 Mainline: SoC support is real; board support is three reference designs

| item | status | evidence |
|---|---|---|
| `sm8350.dtsi` | present, 117,937 B / 4,634 lines | [F] |
| board DTs | 7 files; `mtp`, `hdk`, `surface-duo2`, `sagami` (+`pdx214`/`pdx215`) | [F] |
| **no DT for either device in this slice** | `lemonade`/`lemonadep` absent; Sony covered only as `pdx214` | [F] |
| SoC ID | `QCOM_ID_SM8350` = **439** (`qcom,ids.h:223`); `socinfo.c:464` `qcom_board_id(SM8350)` | [F] |
| **no `SM8350-AC` SoC ID** | `qcom,ids.h` has no `QCOM_ID_SM8350_AC`; the `-AC` part is a matrix label with no mainline ID | [F] |
| PAS driver | 4 compatibles bound (`qcom_q6v5_pas.c:2061-2064`) | [F] |
| AOSS QMP | `qcom,sm8350-aoss-qmp` (`qcom_aoss.c:652`) | [F] |
| SCM | `qcom,scm-sm8350` (`sm8350.dtsi:295`) | [F] |
| PCIe | `qcom,pcie-sm8350`, two controllers (`:1519`, `:1629`) | [F] |
| CPUCP mailbox | **no** `sm8350` compatible in `qcom-cpucp-mbox.c` | [N] |
| SHRM / QUPFW | **no** driver binding; `grep` for `qupfw` in `torvalds/linux` → 0 hits | [N] |

The `SHRM`/`QUPFW` negative is the one that constrains a port: both images are
in the corpus (§4) and neither has a mainline consumer. `research/qualcomm/docs/
bootchain-census.md` already establishes that SHRM appears in vendor trees only
as a Coresight trace probe (`tpdm_shrm`); this slice adds that the SM8350 chain
carries a 49,152 B `shrm.img` with no loader [F]/[N].

### 8.2 postmarketOS: one vendor, one fork, pinned three years back

postmarketOS is **not** on GitHub any more — `postmarketOS/pmaports` returns
404 from the GitHub API. Queried GitLab (`gitlab.com/api/v4/projects/
postmarketOS%2Fpmaports`) instead, 2026-11-22:

| query | result |
|---|---|
| `repository/tree?path=device/testing` pp.1-3 | `device-oneplus-lemonade`, **`device-oneplus-lemonadep`** |
| same over `device/community` | **zero** SM8350 devices |
| same over `device/main` | **zero** SM8350 devices |
| `device/testing/linux-postmarketos-qcom-sm8350/APKBUILD` | **200**, 1,905 B |
| `device/testing/soc-qcom-sm8350/APKBUILD` | **200**, 558 B |
| `device-sony-pdx214` / `pdx215` / `sagami` | **404** in both `testing` and `community` |
| `device-motorola-xpeng` | **404** |

So: **OnePlus 9 and 9 Pro only.** Not the Xperia 5 III in this slice, not the
Surface Duo 2, not the Moto G200 (`xpeng`) that carries the `-AC` label.

The kernel package is the finding:

```
_flavor="postmarketos-qcom-sm8350"
pkgver=6.7
pkgrel=1
pkgdesc="Mainline kernel fork for SM8350"
url="https://gitlab.com/sm8350-mainline/linux"
_commit="ffb1b0db511df03829fa0c9682f2412c0db7f717"
```

- It is a **fork**, not mainline: `pkgdesc` says "Mainline kernel fork".
- The fork (`gitlab.com/sm8350-mainline/linux`) was created **2023-12-03**,
  default branch `dev`, description "Linux kernel, patched for sm8350 mobile
  devices", last activity **2026-08-13**.
- The **pinned commit** `ffb1b0db` is dated **2024-01-16**, subject
  `HACK: bluetooth: extend timeout for qca6490`. So the kernel postmarketOS
  actually builds for SM8350 is a 6.7 tree with a January-2024 pin, while
  mainline is at 7.x.
- The `dev` branch head commits are dated **2023-12-02** and are all marked
  `UNFINISHED:` / `UNTESTED:` / `HACK:` — e.g. `UNFINISHED: arm64: dts: qcom:
  sm8350-lemonade(p): More feature bringup`, `UNTESTED: arm64: dts: qcom:
  sm8350: Add 4pin config for uart18 node`, `UNFINISHED: firmware: Add synaptics
  tcm oncell fw loader driver`, `UNFINISHED: bluetooth: Add support for
  qca6490`.

The device package (`device-oneplus-lemonadep/APKBUILD`, 806 B) depends on
`linux-postmarketos-qcom-sm8350`, `soc-qcom-sm8350`, `mkbootimg`, `bootmac`,
and declares `nonfree_firmware` depending on `firmware-oneplus-lemonade`. Its
`deviceinfo` (1,409 B) sets `deviceinfo_dtb="qcom/sm8350-oneplus-lemonadep"` —
**a DT that does not exist in mainline** (§8.1) and therefore comes from the
fork. `deviceinfo_kernel_cmdline` includes `fw_devlink=permissive
clk_ignore_unused pd_ignore_unused`, which is the signature of a tree that boots
without full clock/power-domain description [F].

The postmarketOS wiki page for the OnePlus 9 / 9 Pro is flagged **archived**
("This device has been archived … no longer appears in `pmbootstrap` and is
likely broken") as of 2026-11-22. Combined with `device/testing` placement
(not `community`), the honest status is: **unmaintained, in testing, on a
three-year-stale fork, for two OnePlus devices only** [F].

### 8.3 What that means for the firmware gap

The §6.2 absence and the §8.2 fork are the same fact seen twice. A vendor-adjacent
fork can carry `qcom/sm8350/*.mbn` in its own firmware package
(`firmware-oneplus-lemonade`) and never ask linux-firmware for them. Mainline
cannot boot an SM8350 board's DSPs because upstream ships one symlink; the fork
sidesteps that by shipping the vendor blobs out-of-tree. Neither path is a
mainline DSP bring-up [I].

## 9. What the matrix says — and the numbers that disagree

### 9.1 Three counts, three universes

| source | rows | devices | bytes |
|---|---:|---:|---:|
| `coverage-matrix.csv`, label `Qualcomm SM8350 Snapdragon 888` | **693** | **2** | 886,208,933 |
| `coverage-matrix.csv`, label `Qualcomm SM8350-AC Snapdragon 888+` | 651 | 1 | 833,798,522 |
| `data/fleet/devices-001-222.csv`, both labels | 1,301 | 2 | — |
| `per-soc-method-plans.md:62` (plan) | 1,344 | 3 | 1.72 GB |

The plan's 1,344 / 3 is the **laptop-half** universe, which includes
`Moto_G200`. The matrix splits the two labels, so the matrix's SM8350 figure is
693 / 2 and its SM8350-AC figure is 651 / 1. `693 + 651 = 1,344` and
`2 + 1 = 3` — the plan row is **arithmetically exact** and is simply counting
both labels together [F].

The fleet CSV agrees on the union: 1,301 rows over `Moto_G200` (651) and
`OnePlus_9_Pro` (650). It has **no** `Xperia_5_III` rows at all, which is why
its device set is 2 while the matrix's is 2 by a different composition [F].

### 9.2 The blank-`soc` device, and why 1,344 is still right

`OnePlus_9` carries **651** rows with an empty `soc` string. Its md5 set
overlaps `OnePlus_9_Pro`'s on **581 of 589** distinct digests — 98.6%. So
`OnePlus_9` is a second SM8350 device whose label was never filled in, and
adding it gives `693 + 651 + 651 = 1,995` rows over 4 devices for the
non-AC SM8350 alone [F].

This is the same failure mode #2029 documented three ways
(`martini`/`OnePlus_9RT`, `OnePlus_9` blank, `tundra` mislabelled). For SM8350
specifically the undercount is **two** devices, not three: `OnePlus_9` (blank)
and `Moto_G200` (correctly labelled `-AC`, but outside this issue's label) [F].

The honest statement for this note is therefore: **the slice under its own
label is 693 / 2, and that is what §1-§8 describe; the SoC's real footprint in
the matrix is at least 1,995 rows over 4 devices** [F] for the arithmetic.

### 9.3 The `-AC` sibling is a different part number, not a variant label

`SM8350-AC` (`Moto_G200`, 651 rows / 833,798,522 B) is a distinct part number —
`research/fleet/wifi-wpss.md` §7 records that `SM8150`/`SM8150-AC` and
`SM8350`/`SM8350-AC` are **not** merges, unlike the `SM6375` and `SM7325-AE`
marketing-string pairs. Mainline has no `QCOM_ID_SM8350_AC` (§8.1), so the
distinction is a matrix/vendor distinction with no upstream encoding [F].

Its family profile differs from the non-AC slice in one striking way: it carries
**28** `gpu` rows against this slice's 11, and **38** `modem` rows against 32 —
because `Moto_G200`'s dump includes the `a660_zap.b00`/`.b01`/`.b02` segments
that the OnePlus and Sony dumps do not [F].

### 9.4 The nine `a660_zap.bNN` rows are all outside this slice

Matrix-wide, `a660_zap.b00` (148 B), `.b01` (6,712 B) and `.b02` (1,976 B) each
appear **3 times**, on `Moto_G200`, `Edge_30_Fusion` and `Edge_30`. Not one is
SM8350-labelled in the non-AC slice. The `.b02` digest `e1341c9f…` is identical
across all three; the `.b01` digest differs on all three
(`4a7b6db8…`, `9e598a09…`, `0b8ac635…`) [F].

That pattern — identical code segment, divergent hash segment — is the same
shape #2029 found for the `tundra`/`Moto_G200`/`Edge_30` trio, and it is why the
`a660_zap` container is a **device-signed** artifact while `a660_gmu.bin` and
`a660_sqe.fw` are fleet invariants (§9.5) [I].

### 9.5 Two fleet invariants, and one that is not

| file | builds | devices | verdict |
|---|---:|---:|---|
| `a660_gmu.bin` | 3 (55,256 / 55,252 / 53,672 B) | 21 | **55,256 B / `179caf2e…` on 19** |
| `a660_sqe.fw` | 2 (40,496 / 43,068 B) | 30 | **40,496 B / `08b7662c…` on 21** |
| `sequence_manifest.bin` | 5 sizes | 50 | **5,704 B / `252630742d…` on 25** |
| `a660_zap.mdt` | 11 builds | 21 | **no invariant** — 11 distinct digests |

The first three are SoC-generation constants: the same GMU, SQE and KBC manifest
ship on every Adreno 660 part regardless of vendor or signing. `a660_zap.mdt` is
the opposite — **11 distinct builds over 21 devices**, 6,708 B or 6,860 B,
because the zap shader is signed per device [F] for the counts, [I] for the
signing explanation.

The GMU is not even stable within this slice's own family: `FP5` (QCM6490)
carries 55,252 B / `cd3a2352…`, two bytes smaller than the 19-device build, and
`Nord_200` carries 53,672 B / `6e2c4e02…` [F]. So "the a660 GMU is 55,256 B" is
true for 19 of 21 devices, not for the part.

### 9.6 Ten of eighteen shared filenames are byte-identical

Eighteen filenames appear on **both** devices in the slice. Ten share an md5;
eight do not:

| same md5 (10) | different md5 (8) |
|---|---|
| `a660_gmu.bin`, `a660_sqe.fw`, `sequence_manifest.bin`, `unified_ksqs.bin`, `bm2n06`, `bm2n08`, `bm2n12`, `bm2n13`, `bm2n14`, `bm2n15` | `boot.img`, `dtbo.img`, `vbmeta.img`, `regdb.bin`, `a660_zap.mdt`, `evass.mdt`, `ipa_fws.mdt`, `vpu20_4v.mdt` |

The ten identical are all **vendor-neutral or SoC-generation artifacts**: the
Adreno 660 trio, the GPU KBC manifest and blob, and the six `bm2n*` ADSP codec
blobs. The eight different are all **signed or device-customised**: the boot
images, the regulatory DB (19,348 B on OnePlus vs 24,278 B on Sony — different
regulatory domains), the zap shader, and three TZ applets [F].

**The six `bm2n*` digests matching across two vendors is the strongest
single result in this section.** `bm2n06/08/12/13/14/15.bin` are byte-identical
between `oneplus/lemonadep/vendor/lib/rfsa/adsp` and
`sony/pdx214/vendor/lib/rfsa/adsp`. `bm2n13.bin` = `bf635d90…`, which
`research/laptop/qualcomm-adsp-bm2n-variant-matrix.md:53` already proved fleet-wide
across `_sony_sm8350-common`, `_oneplus_sm8350-common` and six other trees — so
this is a **second, independent confirmation** of that document's claim from a
different dataset, not a new claim [F].

## 10. Honest negatives

1. **No SM8350 payload exists on disk here.** `data-fetch/` holds only
   `second-device/instantnoodle` (SM8250) and `second-device/larry` (SM6375).
   Every size and digest in this note is `coverage-matrix.csv` metadata; nothing
   was recomputed from bytes [N].

2. **No disassembly of any kind.** No DSP segment, TZ image, chain image or
   `.mdt` was decoded. The Hexagon 780 / `hexagon-v68` identification is a
   citation of public spec pages via `Moto_G200/cdsp.md:15`, not a result of
   this issue [N].

3. **The DSP ISA is unproven for this SoC specifically.** `Moto_G200/cdsp.md:106`
   records `isa_identified` EMPTY on all 18 corpus CDSP rows, and
   `research/fleet/pil-metadata-sweep.md` — which establishes the SHA-384
   hash-slot law on 28 images — contains **zero** SM8350 mentions. The law is
   unverified here, not disproved [N].

4. **`a660_zap.mdt`'s internal difference between the two devices is not
   characterised.** Same size (6,708 B), different md5 (`2474a662…` vs
   `203d73b4…`). The GPU note (§3.2) owns this and also does not byte-diff it.
   The `b02`-identical / `b01`-divergent pattern in §9.4 is suggestive that the
   divergence sits in the hash segment, but no SM8350 payload is available to
   test it [I]/[N].

5. **The 15 self-contained `.mdt` stems are a census gap, not a format claim.**
   I cannot distinguish "this file genuinely has no split segments" from "the
   census did not collect them". §6.4 states both readings [N].

6. **`dsp.img` is not identified as ext4 here.** Its 67,108,864 B = exactly
   64 MiB is consistent with a partition-sized container, and the OnePlus 6
   analogue was proven ext4, but no SM8350 `dsp.img` payload is on disk [I]/[N].

7. **The 132,697,706 B remainder in `modem.img` is unexplained.** §4 gives the
   arithmetic; what the remainder contains is not determined [N].

8. **The Xperia 5 III's chain is 3 images, and I do not know why.** §4 records
   the absence of `xbl`/`tz`/`hyp`/`abl` for `pdx214` without claiming whether
   the Sony dump simply excluded them or the extraction missed them [N].

9. **No mainline board DT exists for either device in this slice.** `lemonade`,
   `lemonadep` and `xpeng` are all absent from
   `arch/arm64/boot/dts/qcom/`. The Sony is covered as `pdx214`/`pdx215`. This
   is a fact, not a negative I can explain [F].

10. **`SM8350-AC` has no mainline SoC ID.** `qcom,ids.h` has
    `QCOM_ID_SM8350` = 439 and no `_AC` counterpart. Whether the `-AC` part
    reports 439 at runtime is not determined — that would need a `socinfo` read
    from a `Moto_G200`, which is not on disk [N].

11. **The postmarketOS status is a snapshot of 2026-11-22.** It is `device/testing`,
    the wiki page is archived, and the kernel pin is 2024-01-16. This could
    change at any time and the dated sources are given so it can be re-checked
    [F] for the snapshot.

12. **I did not verify that `qcom/sm8350/*` is absent from any *other* firmware
    distribution.** Only `linux-firmware` `main` was measured. A vendor tree or
    a distro fork may carry the files [N].

13. **The `wifi` family contains three touch-panel images.**
    `FW_NF_ILI7807S_{BOE_FAE,DSJM,DSJM_FAE}.img` (358,761 / 392,133 / 391,925 B)
    sit under `oneplus/lemonadep/odm/firmware/tp/21075` — a touch-panel path —
    but are labelled `blob_family = wifi`. Meanwhile 37 rows are correctly
    labelled `other`/`touch`. So the family column misclassifies at least 3
    rows, and the `wifi` family's 155 count is 152 for that reason [F] for the
    mislabel, [N] for whether more exist.

14. **I corrected two of my own errors during verification** and record them
    rather than silently rewriting: (a) an early draft tested the split law as
    "all segments sum to the `.mdt`", which fails by two orders of magnitude —
    the correct and verified form is `b00 + b01 == mdt`, §6.4; (b) an early
    draft read a `404` from `git.kernel.org` for `qcom/sm8350/a660_zap.mbn` as
    absence, when that host does not serve symlinked blobs at all — `WHENCE`
    is the authority, §6.2.

15. **The `per-soc-method-plans.md:87-90` `tundra` error is reported, not
    fixed here.** That line belongs to #2029's deliverable and to the plan
    document; this note cites the corrected arithmetic and leaves the edit to
    its owner.

16. **The `52+32N` / `64+56N` decomposition is inferred from sizes, not read from
    a header.** No `b00` payload was opened. The decomposition is exact on 23 of
    23 stems in this slice and on **122 of 122** stem names matrix-wide (§6.5),
    so it is a strong size-level regularity, not a parsed ELF fact [I].

17. **`N − segments` is not explained for the ELF32 stems.** §6.5 shows it is 0,
    1 or 3 there and reads the residual as `PT_NULL`/hash/certificate headers;
    every ELF64 stem has a residual of exactly 0. That reading is not verified
    against a program-header table [I]/[N].

## Reproduce

Every number above is regenerated by these commands. All are `python3 -I`,
stdlib only, run from the repository root.

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm SM8350 Snapdragon 888']
print('slice',len(s),len({r['device'] for r in s}),sum(int(r['size_bytes']) for r in s))
print('files',len({r['filename'] for r in s}))
for f in sorted({r['blob_family'] for r in s}):
    rs=[r for r in s if r['blob_family']==f]
    print(f,len(rs),len({r['filename'] for r in rs}),sum(int(r['size_bytes']) for r in rs))
print(Counter(r['device'] for r in s).most_common())"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm SM8350 Snapdragon 888']
stems=sorted({r['filename'][:-4] for r in s if r['filename'].endswith('.mdt')})
eq=miss=selfc=0
for st in stems:
    d={r['filename']:int(r['size_bytes']) for r in s if r['filename'].startswith(st+'.')}
    m,b0,b1=d.get(st+'.mdt'),d.get(st+'.b00'),d.get(st+'.b01')
    if b0 is None or b1 is None: selfc+=1
    elif b0+b1==m: eq+=1
    else: miss+=1
print('stems',len(stems),'split-equal',eq,'split-diff',miss,'self-contained',selfc)"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm SM8350 Snapdragon 888']
stems=sorted({r['filename'][:-4] for r in s if r['filename'].endswith('.mdt')})
for st in stems:
    d={r['filename']:int(r['size_bytes']) for r in s if r['filename'].startswith(st+'.')}
    b0=d.get(st+'.b00')
    if b0 is None: continue
    e32,e64=b0-52,b0-64
    f='ELF32 52+32*%d'%(e32//32) if e32>0 and e32%32==0 else ('ELF64 64+56*%d'%(e64//56) if e64>=0 and e64%56==0 else 'neither')
    print(st,b0,f)"
```

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
b00={r['filename'][:-4]:int(r['size_bytes']) for r in rows if r['filename'].endswith('.b00')}
mdt={r['filename'][:-4]:int(r['size_bytes']) for r in rows if r['filename'].endswith('.mdt')}
both=set(b00)&set(mdt)
e32=sum(1 for s in both if b00[s]>52 and (b00[s]-52)%32==0)
e64=sum(1 for s in both if b00[s]>=64 and (b00[s]-64)%56==0)
print('stems',len(both),'e32',e32,'e64',e64,'neither',len(both)-e32-e64)"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for fn in ('adsp.mbn','cdsp.mbn','modem.mbn','slpi.mbn','ipa_fws.mbn','a660_zap.mbn',
           'adsp.mdt','cdsp.mdt','modem.mdt','slpi.mdt','a660_zap.mdt'):
    print(fn, sum(1 for r in rows if r['filename']==fn))"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
o=[r for r in rows if r['device']=='OnePlus_9']
p=[r for r in rows if r['device']=='OnePlus_9_Pro']
mo,mp={r['md5_db'] for r in o},{r['md5_db'] for r in p}
print('OnePlus_9 rows',len(o),'distinct md5',len(mo),'overlap',len(mo&mp))"
```

```bash
python3 -I -c "
import csv
from collections import defaultdict
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g=defaultdict(list)
for r in rows:
    if r['filename'] in ('a660_gmu.bin','a660_sqe.fw','a660_zap.mdt','sequence_manifest.bin'):
        g[(r['filename'],int(r['size_bytes']),r['md5_db'])].append(r['device'])
for k,v in sorted(g.items()): print(k[0],k[1],k[2][:12],len(v))"
```

```bash
curl -sL 'https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/WHENCE?h=main' -o /tmp/WHENCE
grep -c '^File: qcom/sm8350/'  /tmp/WHENCE
grep -c '^Link: qcom/sm8350/'  /tmp/WHENCE
grep -c '^RawFile: qcom/sm8350/' /tmp/WHENCE
grep -n 'qcom/sm8350/' /tmp/WHENCE
```

```bash
for f in sm8350.dtsi sm8350-mtp.dts sm8350-hdk.dts sm8350-sony-xperia-sagami.dtsi \
         sm8350-microsoft-surface-duo2.dts; do
  curl -sL "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/arch/arm64/boot/dts/qcom/$f" -o /tmp/$f
  echo "$f $(wc -c < /tmp/$f)"; grep -c 'firmware-name' /tmp/$f
done
grep -n 'firmware-name' /tmp/sm8350-mtp.dts /tmp/sm8350-hdk.dts
```

```bash
curl -sL 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/remoteproc/qcom_q6v5_pas.c' -o /tmp/pas.c
grep -n 'sm8350' /tmp/pas.c
sed -n '1198,1212p;1415,1430p;1466,1476p;1515,1529p' /tmp/pas.c
```

```bash
curl -s 'https://gitlab.com/api/v4/projects/postmarketOS%2Fpmaports/repository/files/device%2Ftesting%2Flinux-postmarketos-qcom-sm8350%2FAPKBUILD/raw?ref=master'
curl -s 'https://gitlab.com/api/v4/projects/postmarketOS%2Fpmaports/repository/files/device%2Ftesting%2Fsoc-qcom-sm8350%2FAPKBUILD/raw?ref=master'
curl -s 'https://gitlab.com/api/v4/projects/sm8350-mainline%2Flinux' | head -c 600
```

All fetches 2026-11-22. `torvalds/linux` master at
`4843f6873f7c4835e62f2c73ba0fd538e57a2f22` (committed 2026-11-22T01:22:21Z).

## Sources

| claim | source | access |
|---|---|---|
| 693 / 2 / 886,208,933; 651 filenames; family table; per-device split | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-22 |
| 651 / 1 / 833,798,522 for `SM8350-AC`; 28 gpu + 38 modem rows | same | 2026-11-22 |
| `OnePlus_9` 651 rows, blank `soc`, 581/589 md5 overlap | same | 2026-11-22 |
| 23/23 split law; 15 self-contained stems; per-stem segment counts | same | 2026-11-22 |
| `b00` decomposes `52+32N` on 8 stems, `64+56N` on 15, neither on 0; `32`/`64` suffix matches 7/7 | same | 2026-11-22 |
| 122 stem names matrix-wide with `.mdt`+`.b00`: 49 fit `52+32N`, 73 fit `64+56N`, **0** neither | same | 2026-11-24 |
| `.mbn` spellings 0 rows; `.mdt` spellings 1-2 rows | same | 2026-11-22 |
| `a660_zap.b00/.b01/.b02` 3 rows each on `Moto_G200`/`Edge_30_Fusion`/`Edge_30` | same | 2026-11-22 |
| `a660_gmu.bin` 3 builds / 19-device invariant; `a660_sqe.fw` 2 builds; `a660_zap.mdt` 11 builds | same | 2026-11-22 |
| 18 shared filenames, 10 identical / 8 divergent; six `bm2n*` identical | same | 2026-11-22 |
| 84 `hpnv*` BT rows; uppercase non-sequential suffixes; no bare `.mdt` | same | 2026-11-22 |
| 1,301 rows / 2 devices for both SM8350 labels | `data/fleet/devices-001-222.csv` | 2026-11-22 |
| CPU: cpu0-3 A55, cpu4-6 A78, cpu7 X1; one `cpu-map/cluster0`; freq domains 0/1/2; single `l3_0` | `arch/arm64/boot/dts/qcom/sm8350.dtsi` (`:57`-`:250`, `:73-77`) | 2026-11-22 |
| 25 reserved regions / 703,791,104 B; contiguity and gap table | `sm8350.dtsi:419-555` | 2026-11-22 |
| 4 remoteproc nodes and their MMIO; `gpu@3d00000` `status="disabled"`; 10 GPU OPPs 315-840 MHz | `sm8350.dtsi:1889,2225,2267,2509,2039-2062,2120,2065-2118` | 2026-11-22 |
| `qcom,scm-sm8350`; `aoss_qmp`; `qcom,pcie-sm8350` x2 | `sm8350.dtsi:293-300,3292,1519,1629` | 2026-11-22 |
| `sm8350.dtsi` has 0 `firmware-name` properties | `grep -c` on the fetched file | 2026-11-22 |
| 7 SM8350 DT files; no `lemonade`/`lemonadep`/`xpeng` | GitHub contents API on `arch/arm64/boot/dts/qcom/` | 2026-11-22 |
| 11 requested paths, 1 resolving; per-board `firmware-name` line numbers | `sm8350-mtp.dts`, `sm8350-hdk.dts`, `sm8350-sony-xperia-sagami.dtsi`, `sm8350-microsoft-surface-duo2.dts` | 2026-11-22 |
| `qcom/sm8350/` = 0 File + 1 Link + 0 RawFile; `qcm6490` 12; `qcs6490` 25; `sm8250` 9 | `linux-firmware` `WHENCE` (`:7280`), 540,253 B | 2026-11-22 |
| `qcm6490/adsp.mbn` 12,111,452 B `ADSP.HT.5.5.c8-00256.2-KODIAK-1`; `a660_zap.mbn` 1,054,648 B `v0.09` | `WHENCE` + `plain/` HEAD | 2026-11-22 |
| `a660_gmu.bin` `v3.01.0A`; `a660_sqe.fw` `v1.12` | `WHENCE:7273-7276` | 2026-11-22 |
| `WCN6855` 14 WHENCE entries; `bdwlan` 0 WHENCE entries | `WHENCE` | 2026-11-22 |
| 4 PAS compatibles; `sm8350_adsp_resource`/`sm8350_cdsp_resource`; slpi→`sdm845_slpi_resource_init`; mpss→`mpss_resource_init`; descriptor fields | `drivers/remoteproc/qcom_q6v5_pas.c:1198,1415,1466,1515,2022,2025,2061-2066` | 2026-11-22 |
| `firmware-name` DT override precedes descriptor default | `qcom_q6v5_pas.c:923-932` | 2026-11-22 |
| no `sm8350` CPUCP mailbox compatible | `drivers/mailbox/qcom-cpucp-mbox.c:204-205` | 2026-11-22 |
| `qcom,sm8350-aoss-qmp` | `drivers/soc/qcom/qcom_aoss.c:652` | 2026-11-22 |
| `QCOM_ID_SM8350` = 439, no `_AC` id | `include/dt-bindings/arm/qcom,ids.h:223` | 2026-11-22 |
| `qcom_board_id(SM8350)` in the socinfo table | `drivers/soc/qcom/socinfo.c:464` | 2026-11-22 |
| no `qupfw` binding in mainline (0 hits); `shrm` 1 unrelated hit | GitHub code search, `torvalds/linux` | 2026-11-22 |
| `linux-postmarketos-qcom-sm8350` 6.7, `_commit=ffb1b0db…`, fork URL | `pmaports` `device/testing/linux-postmarketos-qcom-sm8350/APKBUILD`, 1,905 B | 2026-11-22 |
| `soc-qcom-sm8350` pkgver 5, 558 B | `pmaports` `device/testing/soc-qcom-sm8350/APKBUILD` | 2026-11-22 |
| `device-oneplus-lemonadep` 806 B; `deviceinfo` 1,409 B; `deviceinfo_dtb`; `fw_devlink=permissive` cmdline | `pmaports` `device/testing/device-oneplus-lemonadep/{APKBUILD,deviceinfo}` | 2026-11-22 |
| `lemonade`/`lemonadep` in `device/testing` only; zero in `community`/`main`; no `pdx214`/`pdx215`/`sagami`/`xpeng` | GitLab `pmaports` tree API, `device/{testing,community,main}` | 2026-11-22 |
| fork created 2023-12-03, branch `dev`, last activity 2026-08-13; pin dated 2024-01-16; `UNFINISHED`/`UNTESTED`/`HACK` head commits 2023-12-02 | GitLab `sm8350-mainline/linux` project + commits API | 2026-11-22 |
| wiki page archived | `wiki.postmarketos.org` OnePlus 9 & 9 Pro page (rendered via search cache; direct fetch blocked by Anubis) | 2026-11-22 |
| Hexagon 780 / `hexagon-v68`; `e_machine` 164; `isa_identified` EMPTY on all 18 rows | `docs/devices/motorola/Moto_G200/cdsp.md:15,106` | 2026-11-21 |
| SHA-384 law is SM8250+SDM845 only, 28/28 | `research/fleet/pil-metadata-sweep.md` §0 | 2026-11-22 |
| `dsp.img` on OnePlus 6 is ext4 | `research/fleet/dsp-tz-map.md` §1 | 2026-11-22 |
| `-AC` is a distinct part number, not a merge | `research/fleet/wifi-wpss.md` §7 | 2026-11-22 |
| `bm2n13.bin` `bf635d90…` fleet-wide across 8 vendor trees | `research/laptop/qualcomm-adsp-bm2n-variant-matrix.md:53` | 2026-11-22 |
| `tundra`→SM8350-AC relabel; 3,286-row undercount | `research/soc/Qualcomm-SM7250-Snapdragon-765G-gpu.md` §2.1 | 2026-11-21 |
| Adreno 660 proof, 11 GPU rows, `a660_zap.mdt` two builds, `sequence_manifest.bin` identity | `research/soc/Qualcomm-SM8350-Snapdragon-888-gpu.md` §1-§4 | 2026-11-20 |
| `SHRM` appears only as a Coresight probe in vendor trees | `research/qualcomm/docs/bootchain-census.md:29` | 2026-11-22 |
