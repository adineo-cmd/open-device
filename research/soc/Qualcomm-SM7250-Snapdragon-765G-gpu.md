# Qualcomm SM7250 Snapdragon 765G — GPU core identification and firmware

Issue #2029. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative. Every number is from a command run 2026-11-21 against
`upstream-contribution/blob-database/coverage-matrix.csv` (33,917 rows),
`data/fleet/devices-001-222.csv`, `torvalds/linux` master, and
`linux-firmware` `main`.

Companion documents, cited and **not** re-derived here:

| document | owns |
|---|---|
| `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md` | the `fpctzapp` fingerprint-TZ mislabel (§2); the `a619_gmu.bin` fleet invariant (§3); the split-segment law (§4) |
| `research/soc/Qualcomm-SM7325-Snapdragon-778G-5G-gpu.md` | `adreno-635.0` → `0x06030500` → a660 firmware; the DT-name/marketing-name/firmware-name three-way split |
| `research/laptop/qualcomm-adreno-a650-fleet.md` | the a650 co-residency occupancy table (§4) and the `pdx215` relabel (§4.1) |
| `research/soc/Qualcomm-SM8250-Snapdragon-865-gpu.md` | the a650 zap container internals (§4), the `a650_zap.mdt` build census (§3.1), and the `martini` SM8350 mislabel (§2.1) |

**There is no SM7250 payload on disk in this workspace.** `data-fetch/` holds
`second-device/instantnoodle` (SM8250) and `second-device/larry` (SM6375) only.
Every payload statement below is therefore matrix-derived (filename, size,
md5), and **no ELF parsing is claimed for this SoC** [N].

## 1. The GPU is an Adreno 620 — and mainline cannot bind it

**Verdict: Qualcomm Adreno 620, chip ID `0x06020000` — the only revision gap in
mainline's a6xx device-tree run, and absent from the driver catalog too.** Not
Mali, not PowerVR.

The commercial identification is public and uncontested:

| carrier | claim | source | date |
|---|---|---|---|
| Qualcomm product brief | "Adreno 620 GPU", "10% faster graphics rendering compared to the standard Snapdragon 765" | qualcomm.com prod_brief_qcom_sd765g_5g_1.pdf | 2026-11-21 |
| XDA | "Adreno 620 (15% speed-binned GPU on 765G)" | xda-developers.com | 2026-11-21 |
| notebookcheck | "In the Snapdragon 765G, the Adreno 620 is tuned to offer up to 20% more performance than the standard SD 765" | notebookcheck.net | 2026-11-21 |
| nanoreview | "GPU name Adreno 620", "Architecture Adreno 600", 750 MHz | nanoreview.net | 2026-11-21 |

So the marketing identity is **not** the finding, and this document does not
claim it. The finding is what mainline does with it, in §1.2 and §1.3.

### 1.1 The chip ID the compatible string would produce

`find_chipid()` (`adreno_device.c:142-185`) parses `qcom,adreno-XYZ.W` into
`(core<<24)|(major<<16)|(minor<<8)|patch`, where `core = r/100`,
`major = (r%100)/10`, `minor = r%10` (`:156-165`). For an Adreno 620 that is
core `6`, major `2`, minor `0`, patch `0`:

```
qcom,adreno-620.0  ->  0x06020000
```

[F] computed from the parse, and cross-checked against the catalog's own
neighbouring entries, which all follow the rule: `adreno-615.0` → `0x06010500`,
`adreno-619.0` → `0x06010900`, `adreno-621.0` → `0x06020100`,
`adreno-623.0` → `0x06020300`, `adreno-650.2` → `0x06050002`,
`adreno-660.1` → `0x06060001`.

### 1.2 The catalog has no a620 entry — `0x06020000` is unbound

`a6xx_catalog.c` carries **19 `ADRENO_CHIP_IDS` entries covering 21 chip IDs**
(two entries list two IDs each). **None of the 21 is `0x06020000`** [F]:

```
$ grep -c "ADRENO_CHIP_IDS(" a6xx_catalog.c
19
$ grep -c "0x06020000" a6xx_catalog.c
0
```

The only `0x0602xxxx` IDs in the whole table are `0x06020100` and `0x06020300`
— a621 and a623. The entry that *looks* like a620 is a621
(`a6xx_catalog.c:947-958`):

```c
.chip_ids = ADRENO_CHIP_IDS(0x06020100),
.family = ADRENO_6XX_GEN3,
.fw = {
    [ADRENO_FW_SQE] = "a650_sqe.fw",
    [ADRENO_FW_GMU] = "a621_gmu.bin",
},
.gmem = SZ_512K,
...
.zapfw = "a620_zap.mbn",
```

`0x06020100` decodes as **adreno-621.0**, not 620. The `.zapfw` string
`a620_zap.mbn` and the `a620_hwcg` reglist (`a6xx_catalog.c:131`, used at
`:960`) are the only a620-named things in the file, and both belong to the
a621 chip ID.

A correction to an easy overstatement: this entry's **missing `.revn` is not
unusual**. Eight of the 19 entries have no `.revn` — `0x06010200`,
`0x06010800` (one of its two entries), `0x06020100`, `0x06020300`,
`0x06030500`, `0x06060300`, `0x06090000`, and the a7xx pair [F]. So the
absence proves nothing by itself. What it does mean is mechanical:
`MSM_PARAM_GPU_ID` returns `info->revn` (`adreno_gpu.c:379`), which is 0 for
those entries, and `MSM_PARAM_CHIP_ID` then folds the speedbin into the high
word (`adreno_gpu.c:392-393`) because it cannot rely on revn being set.

What the missing chip ID means at runtime, from `adreno_device.c:49-66` and
`:187-208`:

```c
static const struct adreno_info *adreno_info(uint32_t chip_id)
{
    for (...) for (...) for (int k = 0; info->chip_ids[k]; k++)
        if (info->chip_ids[k] == chip_id)
            return info;
    return NULL;            /* <-- 0x06020000 lands here */
}
...
bool adreno_has_gpu(struct device_node *node)
{
    ret = find_chipid(node, &chip_id);
    if (ret) return false;
    info = adreno_info(chip_id);
    if (!info) {
        pr_warn("%pOF: Unknown GPU revision: %"ADRENO_CHIPID_FMT"\n", ...);
        return false;
    }
    return true;
}
```

[F] `ADRENO_CHIPID_FMT` is `"08x"` (`adreno_gpu.h:71`), so a DT node
`compatible = "qcom,adreno-620.0"` produces
`"Unknown GPU revision: 06020000"` and the GPU is not brought up.

### 1.3 The binding schema does not list a620 either

The absence is not just a missing table row. `Documentation/devicetree/
bindings/display/msm/gpu.yaml` enumerates **18** adreno compatibles, and
`qcom,adreno-620.0` is **not** among them [F]:

```
qcom,adreno-330.2  610.0  612.0  615.0  618.0  619.0  619.1
qcom,adreno-621.0  623.0  630.2  635.0  640.1  650.2  660.1
qcom,adreno-663.0  680.1  690.0  730.1
```

```bash
$ grep -c "adreno-620" gpu.yaml
0
$ grep -c "adreno-621" gpu.yaml
1
```

So a620 is absent from **both** places a mainline GPU has to be known: the
driver catalog and the DT schema. A `qcom,adreno-620.0` node would fail
`dtbs_check` against the schema, and if it got past that it would hit the
`adreno_info()` NULL path in §1.2.

### 1.4 There is no SM7250 device tree — and a621 *is* bound, elsewhere

Enumerated the whole directory rather than guessing a filename:

```
arch/arm64/boot/dts/qcom: 664 files
  'sm7250' -> []          ('pm7250b.dtsi' is a PMIC, not the SoC)
  '7650'   -> []          'lito' -> []   'atoll' -> []
  'sm6350' -> ['sm6350.dtsi', 'sm6350-sony-xperia-lena-pdx213.dts']
  'sar2130p' -> ['sar2130p.dtsi', 'sar2130p-qar2130p.dts']
```

[F] via the GitHub contents API, 2026-11-21. `sm6350.dtsi` (95,496 B) carries
`compatible = "qcom,adreno-619.0"` at `:1525` — the *next* part down.

**And the part above is bound too.** A code search for `qcom,adreno-6` under
`arch/arm64/boot/dts/qcom` returns **15 SoC `.dtsi` files**, and their
compatible strings cover every revision in this neighbourhood except one [F]:

```
talos    612.0    sdm670   615.0    sm6115   610.0    sm6350   619.0
sm8350   660.1    sc7180   618.0    sm8150   640.1    sdm845   630.2
sm8250   650.2    kodiak   635.0    monaco   623.0    lemans   663.0
sc8180x  680.1    sar2130p 621.0    sc8280xp 690.0
```

That is 15 distinct revisions — 610, 612, 615, 618, 619, **621**, 623, 630,
635, 640, 650, 660, 663, 680, 690. **620 is the only gap in the run.** So
mainline binds the part below SM7250's GPU (619, on `sm6350`), the part above
it (621, on `sar2130p` at `:1698`), and every neighbour out to 690 — but not
SM7250's own Adreno 620. `sar2130p.dtsi` even binds it with no `firmware-name`
override, and there is no `sar2130p`/`qar2130p` entry in linux-firmware
`WHENCE` at all [F], so that neighbouring binding has no upstream payload
either.

SM7250 is absent from mainline twice over: no SoC DT, and no a620 in either
the catalog or the schema — while all fifteen of its neighbours are bound. It
*is* named in `drivers/soc/qcom/socinfo.c:453` (`{ qcom_board_id(SM7250) }`),
so the SoC ID is known to the kernel; the GPU side simply was never wired up
[F].

## 2. What the matrix says — and the 639-row block that is not SM7250

The committed slice for `soc == "Qualcomm SM7250 Snapdragon 765G"`:

```
raw slice          938 rows   4 devices   2,004,311,260 B
Edge_30_Fusion     639 rows                 843,007,454 B
corrected          299 rows   3 devices   1,161,303,806 B
```

The `Edge_30_Fusion` block is **68.1% of the rows** and 42.1% of the bytes.
Family split, raw and corrected (raw sums to 938, corrected to 299):

| family | raw rows | corrected rows |
|---|---:|---:|
| other | 310 | 81 |
| wifi | 217 | 14 |
| modem | 155 | 117 |
| tz | 122 | 27 |
| adsp | 38 | 3 |
| boot | 34 | 24 |
| **gpu** | **34** | **24** |
| cdsp | 21 | 3 |
| bt | 7 | 6 |

Per device, corrected:

| device | rows | bytes |
|---|---:|---:|
| Pixel_4A_5G (`bramble`) | 105 | 387,070,176 |
| Pixel_5 (`redfin`) | 103 | 387,213,136 |
| Pixel_5A (`barbet`) | 91 | 387,020,494 |

### 2.1 `Edge_30_Fusion` / `tundra` is a Snapdragon 888+ (SM8350-AC) device

This is the correction of the day, and I got it wrong first. The 639 rows are
labelled `Qualcomm SM7250 Snapdragon 765G`, but the handset is a
**Snapdragon 888+ / SM8350-AC** device:

| carrier | claim | source | date |
|---|---|---|---|
| GSMArena | "Qualcomm SM8350 Snapdragon 888+ 5G (5 nm)", "GPU Adreno 660" | gsmarena.com/motorola_edge_30_fusion-11851.php | 2026-11-21 |
| DeviceSpecifications | "Qualcomm Snapdragon 888+ (SM8350-AC)", "Qualcomm Adreno 660, 840 MHz" | devicespecifications.com | 2026-11-21 |
| Motorola support | "Processor - Snapdragon® 888+ 5G" | en-us.support.motorola.com | 2026-11-21 |
| nanoreview (vs Edge 30) | 888 Plus / Adreno 660 vs 778G Plus / Adreno 642L | nanoreview.net | 2026-11-21 |

The label-independent evidence is in the corpus, and it is decisive in the
direction of *md5 overlap*, not filenames. `tundra`'s `a6xx` filename set is
**exactly equal** to `Moto_G200`'s (the matrix's only SM8350-AC device) and
also exactly equal to `Edge_30`'s:

```
tundra        9 a6xx files  (motorola/tundra)
Moto_G200     9 a6xx files  (motorola/xpeng,  SM8350-AC)   set-equal to tundra
Edge_30       9 a6xx files  (motorola/dubai,  SM7325-AE)   set-equal to tundra
```

Filename sets are equal across three devices on three different SoCs, so
**filenames carry no platform information here at all** (§3). I first called
`tundra`'s set a "strict subset" of `Moto_G200`'s; that was wrong, and the
equality is the stronger reason to distrust filenames.

What *does* discriminate is whole-device md5 overlap. Jaccard against
`tundra`'s 584 distinct md5s:

| device | Jaccard | shared / 584 | SoC (as labelled) |
|---|---:|---:|---|
| `Moto_G200` | **0.142** | 147 | SM8350-AC 888+ |
| `OnePlus_9_Pro` | 0.126 | 131 | SM8350 888 |
| `OnePlus_9RT` | 0.125 | 131 | SM8250 865 — itself a known mislabel |
| `Edge_30` | 0.083 | 70 | SM7325-AE 778G |
| `Phone_1` | 0.054 | 53 | SM7325-AE 778G+ |

`tundra` clusters with the **888 family**, not the 778G pair, and not with the
Pixels at all (3 of 584, 0.5%). Byte-level corroboration: of the 9 `a6xx`
files, **7 are byte-identical to `Moto_G200`'s**, and the two that differ are
`a660_zap.b01` (6,712 B) and `a660_zap.mdt` (6,860 B) [F]. Those are the same
two segments the SM8250 document identified as the hash/metadata layer and the
container that wraps it (`a650_zap.mdt` = `b00` + `b01`, §4.1). The **code**
segment `a660_zap.b02` (1,976 B, `e1341c9f…`) is *identical* across `tundra`,
`Moto_G200` and `Edge_30` — so the difference between these devices is in the
signature layer, not the payload. I note that the hash differs while the only
loadable segment does not, which means the hash covers more than `b02` alone;
I have not established what, and no `a660` payload is on disk here to test it
[I].

Two segments are shared by **exactly three** devices — `a660_zap.b00`
(`e1901644…`, 148 B) and `a660_zap.b02` (`e1341c9f…`, 1,976 B): `Moto_G200`
(SM8350-AC), `tundra`, and `Edge_30` (SM7325-AE), all Motorola, three
different SoC labels [F].

**Consequence for SM8350 — and a correction to my own first count.** The
SM8250 document already identified **two** causes of the SM8350 undercount:
`martini`/`OnePlus_9RT` (652 rows) and `OnePlus_9` (651 rows, blank `soc`).
`tundra` is a **third**, not a second:

| stage | rows | devices |
|---|---:|---:|
| labelled SM8350 (AC + non-AC) | 1,344 | 3 |
| + `martini` relabel (SM8250 doc §2.1) | 1,996 | 4 |
| + `OnePlus_9` blank `soc` filled | 2,647 | 5 |
| + `tundra` relabel (this document) | **3,286** | **6** |

[F] for the arithmetic. SM8350-AC alone goes from 651 rows / 1 device to
1,290 rows / 2 devices. I did not rebuild the CSV — see honest negative 7.

**A third mislabel, in the other dataset.** `data/fleet/devices-001-222.csv`
files **both** `Edge_30` (338 rows) and `Edge_30_Fusion` (639 rows) under
SM7250, whereas `coverage-matrix.csv` files `Edge_30` under SM7325-AE. The
matrix is right about `Edge_30` (its `a660_*` set matches the SM7325 doc's
`0x06030500` → a660 binding); the fleet CSV is wrong about it. So the fleet
CSV's SM7250 population is **1,276 non-empty rows / 5 devices /
2,809,472,500 B**, and removing `tundra` alone leaves 637 rows / 4 devices /
1,966,465,046 B. Removing **both** Motorolas gives **299 rows / 3 devices /
1,161,303,806 B** — which is byte-for-byte the matrix's corrected figure [F].
That agreement is the cross-check: the two datasets differ only in which
Motorola device they mislabel, not in the underlying content.

**A stale note in the plan.** `research/soc/per-soc-method-plans.md:87-90` says
"`tundra` (Moto Edge 30 Fusion, public SM7325-AE) carries SM7250 with 639
rows". The **public-SoC value is wrong** — the device is SM8350-AC, not
SM7325-AE. The row count and the observation that it is "the SM7250 cluster's
largest contributor" are both correct. Reported here, not edited there — that
file is another issue's deliverable.

## 3. Filenames cannot identify this SoC — three devices, three SoCs, one set

The corrected slice holds **24 `gpu` rows / 8 distinct filenames** across three
devices (raw: 34 rows / 15 filenames). Every device carries the *same* eight:

| filename | bytes | md5 | carrier |
|---|---:|---|---|
| `a615_zap.mdt` | 6,708 | `8062f46460807bdb810c5f964d434f56` | all 3 |
| `a619_gmu.bin` | 32,768 | `9e23c52057bb573dee9ba31f1fdba4fa` | all 3 |
| `a620_zap.mdt` | 6,860 | `2007880ea1b007b3e4fc7393a0cc02f6` | all 3 |
| `a630_sqe.fw` | 32,264 | `df35307c61eaaf826f62bada432d47ee` | all 3 |
| `a650_gmu.bin` | 41,548 | `a2b9504e3d1cb8686ae7fcca21a11e1a` | all 3 |
| `a650_sqe.fw` | 31,632 | `353e247b2c4ea8c16c49cb31b574edc1` | all 3 |
| `a650_zap.mdt` | 6,860 | `1d776a3cfede2c8c2aec952f7d0f176f` | all 3 |
| `fpctzappfingerprint.mdt` | 7,464 | 3 distinct md5s | one per device |

Only **one** of the eight filenames is a620-named, and it is the wrong kind of
file (§3.1). Two of the three `a650_*` builds are **byte-identical to the
SM8250 slice's** — `a650_gmu.bin` `a2b9504e…` (14 rows, 5 of them SM8250) and
`a650_sqe.fw` `353e247b…` (14 rows, 5 of them SM8250) [F] — so those are the
a650 co-residency already tabulated at
`research/laptop/qualcomm-adreno-a650-fleet.md` §4, not SM7250 firmware.

The third is **not** shared, and that distinction matters: `a650_zap.mdt`
`1d776a3c…` appears on **exactly the three Pixel rows and nowhere else** in
the 33,917-row matrix [F]. The SM8250 slice's `a650_zap.mdt` builds are
`7c8bf961…` (OnePlus 8/8T/8 Pro/9R) and `b56d71ce…` (Xperia 1 II / 5 II,
7,116 B) — no overlap. So the Pixel trio carries its *own* zap shader build
while sharing the GMU and SQE images with the SM8250 slice. That is exactly
the signature-split behaviour the SM8250 document §5.1 proved: the zap shader
is device-signed, the GMU and SQE wrappers are not.

`a619_gmu.bin` and `a630_sqe.fw` are the Adreno 619 set — one generation
*below* this SoC, and shared fleet-wide (§3.3).

**So 0 of 24 GPU rows on the corrected slice can bind to an Adreno 620**, and
that is not a corpus gap: §1.2-1.3 show mainline has nothing to bind to either.

### 3.1 The `a620_zap.mdt` spelling problem

`a6xx_catalog.c:958` asks for **`a620_zap.mbn`**. The corpus holds
**`a620_zap.mdt`** — 7 rows, 3 builds, all 6,860 B [F]:

| md5 | size | carriers | SoC (as labelled) |
|---|---:|---|---|
| `2007880ea1b007b3e4fc7393a0cc02f6` | 6,860 | Pixel_4A_5G, Pixel_5, Pixel_5A | SM7250 |
| `97098b9c43d6a1b1e57238fda83c5279` | 6,860 | Xperia_1_II, Xperia_5_II | blank / SM8250 |
| `a99d8d3e89b8dbddb9eb8e266d06cd60` | 6,860 | Galaxy_Tab_A7_LTE, Galaxy_Tab_A7_Wifi | blank |

Only 3 of the 7 rows sit on an SM7250-labelled device, and those three are the
co-residency rows. Both Xperias are SM8250 `kona` hardware — `Xperia_5_II`
(`pdx206`) is labelled SM8250 in the matrix, and the `Xperia_1_II` row's
`sony/pdx215` path is a `db_path` mislabel for `pdx203`/kona, established from
its byte-identical `touch_module_id_0x83.img` at
`research/laptop/qualcomm-adreno-a650-fleet.md` §4.1 — so they carry an
a620-named blob for the same superset reason. So `a620_zap.mdt`
**is not evidence of an SM7250 GPU** — it is evidence that Qualcomm's vendor
partitions ship neighbouring generations together, the same pattern the SM8250
and SM8350 documents both recorded.

The `.mdt`-vs-`.mbn` mismatch matters operationally, and I checked the code
rather than assuming: `adreno_request_fw()` (`adreno_gpu.c:536-605`) tries
`qcom/<fwname>`, then `<fwname>` (legacy, no prefix), then `qcom/<fwname>`
again via the usermode helper. **It never substitutes an extension.** A
`.mbn` request will not fall back to an `.mdt` file. So even on a hypothetical
kernel that bound `0x06020000`, the corpus's file would not be found by name.

### 3.2 `fpctzappfingerprint.mdt` is not GPU firmware

Already established corpus-wide at
`research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md` §2 — a fingerprint
trustzone app mislabelled `gpu`, four devices, two sizes. I cite it and do not
re-derive it. It accounts for 3 of the 24 corrected GPU rows, all 7,464 B, and
the three Pixel rows carry three *different* md5s (`90ad4f6a…`, `04fb536c…`,
`c79ade54…`) — which is itself consistent with a per-device signed app, not a
shared GPU blob.

### 3.3 The `a619_gmu.bin` build is a fleet-wide invariant, not an SM7250 artifact

`9e23c52057bb573dee9ba31f1fdba4fa` (32,768 B) appears on **26 devices across
11 distinct non-blank SoC labels** — from SM4350 (480) to SM8350-AC (888+)
[F]. Its presence on an SM7250 device therefore says nothing about that
device's GPU.

One detail worth recording, because it is stronger than the label argument:
the same 32,768 bytes are shipped under **two different filenames** — as
`a619_gmu.bin` on 24 devices and as `a618_gmu.bin` on 2 (`Galaxy_A71`, `Mi_A3`)
[F]. The vendor's own filename is not stable for this content, which is
independent reason not to key a census on filenames.

`a630_sqe.fw` shows the same shape: the corrected slice's build
(`df35307c…`, 32,264 B) is one of **seven** builds of that filename in the
corpus, spanning sizes 32,136–32,504 B [F].

`a650_sqe.fw` is the opposite case — a **single** build (`353e247b…`,
31,632 B) across all 14 rows. I am not going to turn those two observations
into a law: `a660_gmu.bin` alone has three builds (55,256 B ×19, 53,672 B on
SM4350, 55,252 B on QCM6490) and `a630_sqe.fw` has seven, so neither filename
class is uniformly per-generation nor uniformly invariant. The stable
statement is only the per-file one.

## 4. What mainline would need, and what exists

For the a620 chip ID to work, mainline would need a catalog entry, a DT
binding, and three payloads. Of those five, **only `a650_sqe.fw` exists** —
and that one is borrowed from the a650 generation by the a621 entry, not
shipped for a620:

| requirement | mainline state | corpus state | linux-firmware state |
|---|---|---|---|
| catalog entry for `0x06020000` | **absent** (`grep -c` = 0 of 21 IDs) | — | — |
| `qcom,adreno-620.0` in a SoC DT | **absent** (0 of 15 bound a6xx revisions) | — | — |
| `a620_gmu.bin` or `a621_gmu.bin` | a621 entry at `:951` asks `a621_gmu.bin` | **0 rows** | **404** |
| `a650_sqe.fw` | a621 entry at `:950` asks it | 14 rows, 1 build | present (`v1.12`) |
| `a620_zap.mbn` | a621 entry at `:958` asks it | **0 rows** (only `.mdt`, 7 rows) | **404** |

[F] `a621_gmu.bin`, `a620_gmu.bin` and `a620_zap.mbn` are all zero-row in the
33,917-row matrix; `qcom/a621_gmu.bin` and `qcom/a620_zap.mbn` both return 404
from linux-firmware `main`. linux-firmware ships **no** `a619_*`, `a620_*` or
`a621_*` file of any kind — its a6xx set is exactly
`a612_rgmu.bin, a623_gmu.bin, a630_{gmu.bin,sqe.fw}, a640_gmu.bin,
a650_{gmu.bin,sqe.fw}, a660_{gmu.bin,sqe.fw}, a663_gmu.bin` plus the per-SoC
zap `.mbn`s.

That is the honest bottom line for this SoC: **Adreno 620 is a mainline blind
spot, not a corpus gap.** The corpus cannot supply what the kernel never asks
for, and linux-firmware does not ship it either. The one part of the chain
that *does* exist upstream is `a650_sqe.fw`, which the a621 entry borrows from
the a650 generation — the same cross-generation borrowing the SM7325 document
recorded for `0x06030500`.

## 5. The SM7250 slice in context

| dataset | SM7250 rows | devices | bytes |
|---|---:|---:|---:|
| `coverage-matrix.csv` (raw label) | 938 | 4 | 2,004,311,260 |
| `coverage-matrix.csv` (corrected, `tundra` removed) | 299 | 3 | 1,161,303,806 |
| `data/fleet/devices-001-222.csv` (non-empty, raw) | 1,276 | 5 | 2,809,472,500 |
| `data/fleet/devices-001-222.csv` (`tundra` removed) | 637 | 4 | 1,966,465,046 |
| `data/fleet/devices-001-222.csv` (both Motorolas removed) | 299 | 3 | 1,161,303,806 |
| `per-soc-method-plans.md:55` (plan) | 938 | 4 | 2.00 GB |

The plan row matches the **raw** matrix exactly (938 rows, 2.00 GB, 4 devices),
so it inherits the `tundra` mislabel and is otherwise arithmetically correct —
unlike the SM8250 plan row, whose "8 devices" matched no count in either
dataset (`Qualcomm-SM8250-...-gpu.md` §7 note 9). Here the plan's 4 devices and
the corrected 3 differ only by `tundra`, so the plan is internally consistent
with its own inputs [F].

The fleet CSV's SM7250 set is **10 devices**: the five with files
(`Edge_30_Fusion`, `Edge_30`, and the three Pixels) plus five single-row
`builds-csv-only` / `listed-not-populated` entries (`Edge_`, `Moto_G_5G`,
`Moto_G_5G_Plus`, `Pixel_4A`, `Pixel_4XL`) that carry no files. Its
"corrected 4-device" count still includes `Edge_30`, which the matrix places
on SM7325-AE — so **the two datasets cannot both be right about `Edge_30`**,
and the matrix's answer is the one supported by the a660 binding. Once both
Motorolas are removed, though, the two datasets agree exactly (299 / 3 /
1,161,303,806), which is why I treat the disagreement as a labelling bug
rather than a content bug.

## 6. Honest negatives

1. **The Adreno 620 identification is not new.** Four public carriers, cited in
   §1. This document adds the mainline structural absence (§1.2-1.3) and the
   corpus correction (§2.1), not the identification [F].
2. **No SM7250 payload exists on disk here**, so no ELF header, segment table or
   digest was computed for this SoC. Every payload claim is matrix metadata [N].
3. **The a620 chip-ID absence is inferred from the catalog and the schema, not
   from a boot log.** I did not run a mainline kernel on SM7250 hardware; §1.2
   and §1.3 are static reads [I].
4. **`Edge_30_Fusion`'s true SoC is established from public carriers plus md5
   clustering, not from a device tree.** The matrix carries no DT for it, and
   no payload was opened [F] for the carriers and the byte-identical segments,
   [I] for the platform attribution.
5. **The a621 entry's missing `.revn` is not explained.** It is not unique
   (§1.2), so I am not claiming it as a signal — I only record its mechanical
   consequence for `MSM_PARAM_GPU_ID` [N] for the cause.
6. **The `a620_zap.mdt` 6,860 B shape is not parsed here.** It matches the
   Pixel trio's `a650_zap.mdt` size exactly (6,860 B), which is suggestive of
   the same `148 + 6,712` split, but the SM8250 document owns that decode and
   no a620 payload is on disk to test [N].
7. **The 3,286-row SM8350 figure is arithmetic, not a rebuild.** I did not
   regenerate `coverage-matrix.csv`; the relabel is a recommendation [F] for
   the arithmetic, [N] for the rebuild.
8. **`fpctzappfingerprint.mdt`'s format is not analysed.** Cited from the SM4375
   document, which owns it [N].
9. **No disassembly of any kind.** Nothing was decoded [N].
10. **The fleet CSV's `Edge_30` label is not corrected.** Both datasets are
    generated artifacts; this document records the disagreement and the
    evidence, and a rebuild is a separate task [N].
11. **I corrected four of my own claims during verification** and left the
    record here rather than silently rewriting: the "strict subset" in §2.1
    (it is set-equality), the "every other a6xx entry has a `.revn`" in §1.2
    (eight of 19 do not), an earlier draft's claim that all three `a650_*`
    builds were byte-identical to the SM8250 slice's (§3 — only two are), and
    an earlier draft's "only two mainline DT bindings in this range" (§1.4 —
    there are fifteen, and 620 is the only gap).

## Reproduce

```bash
python3 -I -c "
import csv
from collections import Counter
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in rows if r['soc'].strip()=='Qualcomm SM7250 Snapdragon 765G']
print('raw',len(s),len({r['device'] for r in s}),sum(int(r['size_bytes']) for r in s))
c=[r for r in s if r['device']!='Edge_30_Fusion']
print('corrected',len(c),len({r['device'] for r in c}),sum(int(r['size_bytes']) for r in c))
print(Counter(r['blob_family'] for r in c).most_common())"
```

```bash
python3 -I -c "
import csv
rows=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
def md(d): return {r['md5_db'] for r in rows if r['device']==d}
ef=md('Edge_30_Fusion')
for d in ('Moto_G200','OnePlus_9_Pro','Edge_30','Phone_1'):
    o=md(d); print(d, len(ef&o), f'{100*len(ef&o)/len(ef):.1f}%')"
```

```bash
curl -sL https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/gpu/drm/msm/adreno/a6xx_catalog.c \
  | grep -c 'ADRENO_CHIP_IDS('
curl -sL https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/gpu/drm/msm/adreno/a6xx_catalog.c \
  | grep -c '0x06020000'
curl -sL https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/devicetree/bindings/display/msm/gpu.yaml \
  | grep -c 'adreno-620'
curl -sL https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/gpu/drm/msm/adreno/adreno_device.c \
  | sed -n '49,66p;142,185p;187,208p'
```

```bash
for f in a619_gmu.bin a620_gmu.bin a621_gmu.bin a620_zap.mbn; do
  curl -s -o /dev/null -w "qcom/$f %{http_code}\n" \
    "https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/qcom/$f?h=main"
done
```

All fetches 2026-11-21, `torvalds/linux` master, `linux-firmware` `main`.

## Sources

| claim | source | access |
|---|---|---|
| 938 / 4 / 2,004,311,260 raw; 299 / 3 / 1,161,303,806 corrected; family split; all md5/size | `upstream-contribution/blob-database/coverage-matrix.csv` | 2026-11-21 |
| 1,276 / 5 / 2,809,472,500 non-empty; 637 / 4 / 1,966,465,046; 299 / 3 on both-Motorola removal | `data/fleet/devices-001-222.csv` | 2026-11-21 |
| `tundra` Jaccard 0.142 / 147 of 584 vs `Moto_G200`; 7 of 9 `a6xx` md5s identical | computed from `coverage-matrix.csv` | 2026-11-21 |
| 19 `ADRENO_CHIP_IDS` entries / 21 chip IDs; no `0x06020000`; a621 entry at `:947-958`; 8 of 19 entries lack `.revn` | `.../adreno/a6xx_catalog.c` | 2026-11-21 |
| `find_chipid()` parse; `adreno_info()` NULL path; `adreno_has_gpu()` warning | `.../adreno/adreno_device.c:49-66,142-185,187-208` | 2026-11-21 |
| `ADRENO_CHIPID_FMT` = `"08x"`; `ADRENO_6XX_GEN1..GEN4` enum | `.../adreno/adreno_gpu.h:47-50,71` | 2026-11-21 |
| `MSM_PARAM_GPU_ID` returns `revn`; speedbin folded when revn is 0 | `.../adreno/adreno_gpu.c:379,392-393` | 2026-11-21 |
| `adreno_request_fw()` tries `qcom/` then legacy then helper, no extension fallback | `.../adreno/adreno_gpu.c:536-605` | 2026-11-21 |
| 18 adreno compatibles in the schema; no `adreno-620` | `Documentation/devicetree/bindings/display/msm/gpu.yaml` | 2026-11-21 |
| 664 files, no `sm7250*`; `sm6350.dtsi` `adreno-619.0` at `:1525`; `sar2130p.dtsi` `adreno-621.0` at `:1698`; 15 SoC `.dtsi` bind a6xx, 620 the only gap | GitHub contents API + code search + `arch/arm64/boot/dts/qcom/` | 2026-11-21 |
| `SM7250` board ID known to socinfo | `drivers/soc/qcom/socinfo.c:453` | 2026-11-21 |
| a6xx file set in linux-firmware; no a619/a620/a621; no sar2130p | `linux-firmware` `WHENCE` + `qcom/` HEAD probes | 2026-11-21 |
| Adreno 620 is the 765G GPU | qualcomm.com prod brief; xda-developers.com; notebookcheck.net; nanoreview.net | 2026-11-21 |
| Edge 30 Fusion is SM8350-AC / Adreno 660 | gsmarena.com; devicespecifications.com; en-us.support.motorola.com; nanoreview.net | 2026-11-21 |
| `fpctzapp` is a fingerprint TZ app | `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md` §2 | 2026-11-21 |
| a650 co-residency on the Pixel trio | `research/laptop/qualcomm-adreno-a650-fleet.md` §4 | 2026-11-21 |
| SM7325 `0x06030500` → a660 binding | `research/soc/Qualcomm-SM7325-Snapdragon-778G-5G-gpu.md` §1 | 2026-11-21 |
| `a650_zap.mdt` 4 builds / 2 sizes; `.mbn` vs `.elf` signature-only difference | `research/soc/Qualcomm-SM8250-Snapdragon-865-gpu.md` §3.1, §5.1 | 2026-11-21 |
| SM8350 `martini` (652) + `OnePlus_9` blank `soc` (651) undercounts | `research/soc/Qualcomm-SM8250-Snapdragon-865-gpu.md` §2.1, §7 note 9 | 2026-11-21 |
