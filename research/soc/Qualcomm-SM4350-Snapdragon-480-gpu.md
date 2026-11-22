# Qualcomm SM4350 Snapdragon 480 — GPU core identification and firmware

Issue #2023. Evidence classed [F] fact / [I] inference / [H] hypothesis /
[N] negative. Every number is command output from a session on **2026-11-22**
against `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 rows,
123 devices, 27 SoC labels), `torvalds/linux` master at
`4843f6873f7c4835e62f2c73ba0fd538e57a2f22`, and linux-firmware `main`
(`WHENCE`, 540,253 B).

The GPU identity of this SoC is **not new** — it is already asserted in this
repo and §1 cites it rather than re-deriving it. The new work is the matrix
census (§2–§5), the mainline reachability finding (§6), the linux-firmware gap
(§7), the build arithmetic (§8), and a matrix-defect note (§9). §10 records a
hypothesis this session **disproved**, which is why it is not a headline.

Companion documents:

| document | owns | this note |
|---|---|---|
| `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md` (#2024) | the "SM4350 is Adreno-619-class" assertion (§1), the `fpctzapp` family damage (§2.2), the `.mdt` split law (§4) | cites; adds the SM4350 slice, the four singletons, the zap-family split tally |
| `research/soc/Qualcomm-SM7250-Snapdragon-765G-gpu.md` (#2029) | the `a619_gmu.bin` fleet invariant and the `a630_sqe.fw` seven-build census (§3.3) | cites; adds the SM4350 row to both censuses |
| `research/soc/Qualcomm-SM8350-Snapdragon-888-soc.md` (#823) | the 53,672 B `a660_gmu.bin` on `Nord_200` (§9.5); house format | cites; extends into the a660 build arithmetic (§8) |
| `research/laptop/qualcomm-adreno-a650-fleet.md` | the vendor-partition-superset law (§4) | cited in §10 |
| `research/soc/Google-Tensor-GS201-gpu.md` (#2017) | format precedent | format only |

**No SM4350 payload exists in this workspace.** `data-fetch/` is empty. Every
statement below is matrix metadata — filename, size, md5, `db_type` — plus
upstream source text. **No ELF or container parsing is claimed for this SoC**
[N].

## 0. Verdict

| question | answer | class |
|---|---|---|
| SoC | SM4350 = Snapdragon 480; platform codename `holi`; the corpus's only device is `Nord_200` (`oneplus/dre`) | [F] |
| GPU | **Adreno 619**, `ADRENO_6XX_GEN1`, `revn = 619` — **cited**, not re-derived | [F] cited |
| GPU chip ID | `0x06010900` — shared with the machine-less catch-all entry at `a6xx_catalog.c:920` | [F] |
| Firmware mainline names | `a630_sqe.fw` (SQE) + `a619_gmu.bin` (GMU) + `a615_zap.mdt` (zap) | [F] |
| Firmware the corpus holds | 7 GPU rows, 4 of which are matrix singletons | [F] |
| Is the SM4350 catalog entry reachable? | **No.** It is gated on `.machine = "qcom,sm4350"`, and no mainline DT declares that compatible; the machine-less duplicate at `:920` is the only reachable path | [F] |
| Does linux-firmware ship the zap image mainline names? | **No.** `a615` appears nowhere in `WHENCE` or the `qcom/` tree | [F] |
| Upstream vs vendor SQE size | Vendor `a630_sqe.fw` is **smaller than upstream in all seven builds** | [F] measured, [H] cause |
| postmarketOS | Device page exists, marked **not booting** | [F] |

The headline findings are §6 (the declared SM4350 binding is **dead code** —
a machine-gated entry whose compatible exists in exactly one file in all of
mainline, the catalog itself) and §7 (the zap image that entry names **does not
exist in linux-firmware in any form**, so even the reachable path cannot load a
zap shader from upstream firmware).

## 1. The GPU is an Adreno 619 — cited, not re-derived

This is settled prior art in this repo:

- `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md` §1 states *"SoC is
  Adreno-619-class (SM4350/SM4375/SM6375/SM7225)"*, citing
  `research/laptop/qualcomm-adreno-gmu-content.md:265` and
  `implementations/adreno-fleet/gmu-analysis.md:217`.
- The same document records that SM4375's live set is `a619_gmu.bin` +
  `a630_sqe.fw` + `a615_zap.mdt` — the same three filenames SM4350 uses [F].
- Public spec sources agree: Snapdragon 480 = Adreno 619.

I add one independent confirmation from the kernel side, which is new only in
that it is stated here rather than in a sibling note. `a6xx_catalog.c` binds
SM4350 to `revn = 619` with exactly that SQE/GMU pair:

```
870:		.machine = "qcom,sm4350",
871:		.chip_ids = ADRENO_CHIP_IDS(0x06010900),
872:		.family = ADRENO_6XX_GEN1,
873:		.revn = 619,
874:		.fw = {
875:			[ADRENO_FW_SQE] = "a630_sqe.fw",
876:			[ADRENO_FW_GMU] = "a619_gmu.bin",
877:		},
878:		.gmem = SZ_512K,
879:		.quirks = ADRENO_QUIRK_4GB_VA,
882:		.zapfw = "a615_zap.mdt",
```

So the identity chain is `SM4350 → 0x06010900 → revn 619 → {a630_sqe.fw,
a619_gmu.bin, a615_zap.mdt}` [F].

### 1.1 The only local `a619_gmu.bin` is a synthetic fixture, not this build

`implementations/adreno650/fixtures/a619_gmu.bin` is 32,768 B — the same size as
the corpus build — but its digest is `26d0589fd5b07d9782a32e64ecfae2b6`, and the
corpus build is `9e23c52057bb573dee9ba31f1fdba4fa` [F]. It is a test fixture, not
a device dump. **It is therefore not usable as evidence about SM4350**, and I
make no claim from it. This is recorded because the size coincidence invites
exactly the wrong inference.

## 2. What the matrix holds — the slice, measured

**44 rows / 1 device / 146,412,066 B / 44 distinct filenames.**

Every row belongs to `Nord_200` at `oneplus/dre`. There is no second SM4350
device anywhere in the corpus [F], which bounds every generalisation in this
document: the SM4350 slice is a **single device's dump**, not a fleet.

| family | rows | files | bytes | share |
|---|---:|---:|---:|---:|
| `boot` | 3 | 3 | 109,060,096 | **74.49%** |
| `other` | 24 | 24 | 27,556,304 | 18.82% |
| `adsp` | 6 | 6 | 8,873,216 | 6.06% |
| `wifi` | 3 | 3 | 737,078 | 0.50% |
| `gpu` | 7 | 7 | 178,504 | **0.12%** |
| `modem` | 1 | 1 | 6,868 | 0.00% |

`boot` is three files and three quarters of the bytes: `boot.img` 100,663,296 B
(68.75% of the whole slice on its own), `dtbo.img` 8,388,608 B, `vbmeta.img`
8,192 B [F]. The GPU family — the thing this note is about — is **178,504 B, or
0.122% of the device** [F].

That ratio is the reason a "GPU firmware audit" of a vendor dump is so often
disappointing: the files that matter are three orders of magnitude smaller than
the boot image they sit next to.

## 3. The seven GPU rows, and four of them are singletons

| filename | bytes | md5 | `db_type` | build frequency |
|---|---:|---|---|---|
| `a615_zap.mdt` | 6,708 | `7b236017131fe37e9b784aef1c3b3f19` | `ELF64` | **1 device** |
| `a619_gmu.bin` | 32,768 | `9e23c52057bb573dee9ba31f1fdba4fa` | `GPU` | 24 devices |
| `a630_sqe.fw` | 32,448 | `b6cc3da77ffded391f6024ee0598f199` | `GPU` | **1 device** |
| `a660_gmu.bin` | 53,672 | `6e2c4e020a8c1d4abd492e9f49117ec8` | `AUDIO` | **1 device** |
| `a660_sqe.fw` | 40,496 | `08b7662ccd6815333aed6bce9bd69bd7` | `AUDIO` | 21 devices |
| `a660_zap.mdt` | 6,708 | `5a7aefea3491cfae23e44529a3549ed7` | `ELF64` | **1 device** |
| `sequence_manifest.bin` | 5,704 | `252630742d895255d66b5be984bdabda` | `UNKNOWN` | 25 devices |

Byte split of the 178,504 B:

| group | bytes | share of gpu |
|---|---:|---:|
| live Adreno 619 set (`a615_zap` + `a619_gmu` + `a630_sqe`) | 71,924 | **40.29%** |
| a660 set (`a660_gmu` + `a660_sqe` + `a660_zap`) | 100,876 | **56.51%** |
| `sequence_manifest.bin` | 5,704 | 3.20% |

**More than half the GPU bytes on this device belong to a GPU the SoC does not
have.** That is the vendor-partition-superset pattern already documented at
`research/laptop/qualcomm-adreno-a650-fleet.md` §4 and at
`Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md` §3 — an a660 set shipped alongside
a 619-class part, inert on this hardware. §10 shows this is not an anomaly but
the corpus's most common shape.

### 3.1 Four of the seven builds exist on exactly one device in 33,917 rows

`a615_zap.mdt`, `a630_sqe.fw`, `a660_gmu.bin` and `a660_zap.mdt` each appear on
`Nord_200` and nowhere else [F]. The other three are fleet-shared.

Ranking the 105 GPU-bearing devices by singleton count, `Nord_200` is **11th of
the 51 devices that have any singleton at all** (54 of the 105 have zero):

| device | gpu rows | singleton builds | SoC label |
|---|---:|---:|---|
| `Moto_G_Power` | 23 | 20 | SM6115 (662) |
| `Moto_G32` | 23 | 20 | SM6225 (680 4G) |
| `Moto_G200` | 28 | 19 | SM8350-AC (888+) |
| `Moto_E7_Plus` | 14 | 12 | SM4250 (460) |
| `Moto_G_Stylus_5G` | 32 | 11 | (blank) |
| `G_Stylus_5G-2-2022` | 19 | 9 | (blank) |
| `Moto_G82_5G` | 19 | 9 | SM6375 (695) |
| `Defy_2021` | 14 | 9 | SM6115 (662) |
| `Phone_2` | 11 | 6 | SM8475 (8+ Gen1) |
| `Moto_G52` | 14 | 5 | SM6225 (680 4G) |
| **`Nord_200`** | **7** | **4** | **SM4350 (480)** |
| `Edge_40_Pro` | 7 | 4 | SM8550 (8 Gen2) |

Eight devices sit at exactly 4 singletons, `Nord_200` among them [F].

The honest reading: a high singleton count is a property of **which vendor and
which capture**, not of the SoC. `Nord_200` has 7 GPU rows and 4 singletons
because OnePlus shipped a mostly-stock vendor partition with only the
device-specific zap images customised; the Motorola devices at the top of the
table shipped dozens of per-device builds. Singleton count therefore says
nothing about SM4350.

### 3.2 `a619_gmu.bin` is a fleet-wide invariant, and this SoC adds one row

The corpus holds **one** build of `a619_gmu.bin`: `9e23c520…`, 32,768 B, on 24
devices across 12 distinct SoC labels from SM4350 to SM8350-AC [F]. The
SM7250 note (§3.3) already established this; I add that the same 32,768 bytes
also ship as `a618_gmu.bin` on `Galaxy_A71` and `Mi_A3` [F], so the vendor's own
filename is not stable for this content.

| SoC label | devices carrying `9e23c520…` |
|---|---:|
| SM6375 (695) | 7 |
| SM7250 (765G) | 4 |
| (blank) | 3 |
| SM7325 (778G) | 2 |
| SM4350 (480) | 1 |
| SM4375 (4 Gen 1) | 1 |
| SM7225 (750G) | 1 |
| SM7325-AE (778G 5G) | 1 |
| SM8250 (865) | 1 |
| SM8350 (888) | 1 |
| SM8350-AC (888+) | 1 |
| `ÿ`SM6375 (695 5G) | 1 |

The last row is a label defect — a stray `0xFF` byte before `Qualcomm` [F]; it
appears in §10 again.

**Consequence for SM4350:** the presence of `a619_gmu.bin` on a dump is not
evidence of a 619-class SoC, because 23 other devices spanning five SoC
generations carry the identical bytes. The SM4350 evidence is the **zap**
image, not the GMU.

### 3.3 `a630_sqe.fw` has seven builds, and `Nord_200`'s is one of the four singletons

51 rows / 51 devices / 7 builds, sizes 32,136–32,504 B [F]:

| build | bytes | devices |
|---|---:|---|
| `21693ef6f2d6` | 32,456 | 19 |
| `df35307c61ea` | 32,264 | 15 |
| `42b0a1566c41` | 32,304 | 13 |
| `b6cc3da77ffd` | 32,448 | **1** (`Nord_200`) |
| `ed7a02a8aa1f` | 32,272 | 1 (`Moto_E7_Plus`) |
| `b0f92bf1bb63` | 32,504 | 1 (`Phone_2`) |
| `d172aac301b0` | 32,136 | 1 (`Redmi_Note_7_Pro`) |

The three large builds cover 47 of 51 devices; the four singletons are four
different vendors' one-offs. `Nord_200`'s 32,448 B build is not near a cluster
boundary — it is an island between 32,456 and 32,304 [F].

## 4. The split-segment law, and where it actually holds

`research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md` §4 states the
`mdt == b00 + b01` arithmetic. Tested matrix-wide over every stem that has
`b00`, `b01` and an `mdt`, it holds **669 of 1,314** [F] — so it is *not* a
general law, and a dump-completeness check built on it would produce 645 false
positives.

Restricted to the **zap family**, it is nearly exact: **41 of 42** [F].

| stem | stems tested | `mdt == b00+b01` |
|---|---:|---:|
| `a610_zap` | 11 | 11 |
| `a615_zap` | 7 | 7 |
| `a660_zap` | 3 | 3 |
| `fpctzapp` | 12 | 12 |
| `egtzappf` | 8 | 8 |
| `a740_zap` | 1 | **0** |

The single exception is `Edge_40_Pro`'s `a740_zap`, where `mdt` 4,044 B equals
`b00` 148 B + **`b02`** 3,896 B — i.e. the *second* segment is the payload and
`b01` (1,072 B) is something else [F]. So the correct statement is "the mdt
equals the header segment plus the payload segment", and which segment carries
the payload is per-family.

Everything that fails the matrix-wide test is a different container shape:
`cdsp_dtb` (13), `adsp_dtb` (12), `modem_dtb` (10) and the GUID-named
segments (`05B04A44-…`, `32552B22-…`) all fail 0-for-N [F]. Those are DT
containers and secure-app containers, not PIL images, and they do not obey
`mdt == b00+b01` at all.

### 4.1 All per-device signing variance is confined to `b01`

For the 7 devices that ship `a615_zap.bNN`:

| segment | bytes | builds across the 7 |
|---|---:|---:|
| `b00` | 148 | **1** (`3cf41f9f08f8`) |
| `b01` | 6,712 | **7** |
| `b02` | 1,984 | **1** (`890f8bd5a208`) |

And `mdt == b00 + b01` = 6,860 B holds **7 of 7** for these devices [F].

`a660_zap` has the identical shape on its 3 split devices — `b00` 148 B one
build (`e1901644`), `b02` 1,976 B one build (`e1341c9f`), `b01` 6,712 B **three**
builds [F].

This is a sharper statement than "the mdt is per-device signed". **The header
segment and the trailing segment are vendor-invariant; every per-device
signature lives in `b01`.** A census that hashes whole `.mdt` files will see
per-device variance and conclude "per-device firmware"; a census that hashes
segments sees that only one segment actually varies.

## 5. `Nord_200` ships no split segments at all — and that is common

All six `.mdt` files on this device are unsplit:

| `.mdt` | siblings in this device's dump |
|---|---|
| `a615_zap.mdt` | **none** |
| `a660_zap.mdt` | **none** |
| `evass.mdt` | **none** |
| `goodixfp.mdt` | **none** |
| `ipa_fws.mdt` | **none** |
| `vpu20_4v.mdt` | **none** |

Zero `.b00`, `.b01` or `.b02` rows on the whole device [F].

Matrix-wide this is not unusual. Of 123 devices, **91 carry at least one
`.mdt`** and **63 carry at least one `.bNN`**, leaving **28 devices with `.mdt`
but no `.bNN`** [F] — `Nord_200` is one of those 28.

The consequence matters for anyone writing a dump-completeness check: an
`mdt`-without-`b00`/`b01` condition would flag **28 of 91** devices, and the
right interpretation is that those dumps hold whole-image PIL containers rather
than truncated split sets. `Nord_200`'s 6,708 B `a615_zap.mdt` sits inside the
range of the split devices' 6,860 B whole containers, so the size is consistent
with a complete container and not with a fragment [I] — but see N3: I cannot
prove it without the bytes.

Every one of the six stems *does* have split siblings elsewhere in the corpus
[F]:

| stem | devices with segments, matrix-wide |
|---|---:|
| `ipa_fws` | 41 |
| `a615_zap` | 7 |
| `goodixfp` | 6 |
| `evass` | 3 |
| `a660_zap` | 3 |
| `vpu20_4v` | 2 |

So the device is not shipping an unusual *kind* of file; it is a whole-image
capture of stems that other vendors ship split.

## 6. Mainline declares an SM4350 binding that cannot be reached

This is the central new finding, and it is a negative.

`a6xx_catalog.c` contains **11** entries with `.revn`, of which **3** are
machine-gated:

| line | `.machine` | chip ID | `revn` |
|---|---|---|---:|
| `:820` | `qcom,sm7150` | — | 618 |
| `:870` | **`qcom,sm4350`** | `0x06010900` | 619 |
| `:895` | `qcom,sm6375` | `0x06010901` | 619 |

The other 8 entries carry no `.machine` and are catch-alls [F].

### 6.1 Chip ID `0x06010900` appears twice

The SM4350 chip ID is not unique in the table. It is claimed by both the
machine-gated entry at `:870` and a **machine-less duplicate** at `:920`:

| field | `:870` (gated) | `:920` (catch-all) |
|---|---|---|
| `.machine` | `"qcom,sm4350"` | *absent* |
| `.chip_ids` | `0x06010900` | `0x06010900` |
| `.revn` | 619 | 619 |
| SQE / GMU | `a630_sqe.fw` / `a619_gmu.bin` | same |
| `.zapfw` | `a615_zap.mdt` | same |
| `.quirks` | `ADRENO_QUIRK_4GB_VA` | `ADRENO_QUIRK_HAS_CACHED_COHERENT \| ADRENO_QUIRK_4GB_VA` |

The two entries differ in exactly one functional respect: the catch-all adds
`ADRENO_QUIRK_HAS_CACHED_COHERENT` [F].

### 6.2 The gate can never open, so the gated entry is dead

`adreno_info()` walks the gpulist in order and skips any entry whose machine is
not the running machine's compatible:

```c
if (info->machine && !of_machine_is_compatible(info->machine))
	continue;
```

Two facts combine:

1. `qcom,sm4350` occurs in **exactly one file in all of mainline** — the
   catalog that declares it. GitHub code search over `torvalds/linux` for
   `"qcom,sm4350"` returns total **1**, path
   `drivers/gpu/drm/msm/adreno/a6xx_catalog.c` [F].
2. There is no `sm4350.dtsi` and no `holi.dtsi` in
   `arch/arm64/boot/dts/qcom` (664 files; `'4350' -> []`, `'holi' -> []`) [F].

So no device tree can make `of_machine_is_compatible("qcom,sm4350")` true, the
gate at `:870` never opens, and the **catch-all at `:920` is the only reachable
path** for chip ID `0x06010900` [F].

**This is a real behavioural difference, not a cosmetic one.** A 619-class part
reporting `0x06010900` gets `ADRENO_QUIRK_HAS_CACHED_COHERENT`; if a DT ever
declared `qcom,sm4350` it would get the `:870` entry and *lose* that quirk. The
declared SM4350 binding is therefore not merely unreachable — it is the
wrong branch to want.

### 6.3 SM6375 is the contrast, and it shows the gate is real

`qcom,sm6375` returns **40** hits in mainline, including
`arch/arm64/boot/dts/qcom/sm6375.dtsi` and the Sony board
`sm6375-sony-xperia-murray-pdx225.dts`, whose root compatible is
`"sony,pdx225", "qcom,sm6375"` [F]. So the `:895` gate **does** open on that
hardware, and the mechanism is live — it is only SM4350 that has no DT.

One detail worth recording: `sm6375.dtsi` (59,637 B) contains **no GPU node and
no `zap-shader` node** — it has `gpucc`, `pil-gpu-ucode@8aa1a000` and GPU thermal
zones, but no `gpu@3d00000`. By contrast `sm8250.dtsi` has
`gpu: gpu@3d00000` and `gpu_zap_shader: zap-shader` [F]. So even where the
machine gate opens, mainline does not yet instantiate a GPU for this family.

## 7. linux-firmware ships no `a615_zap` in any form

The zap image the catalog names is absent upstream, which is the second half of
the dead-binding story.

**The `qcom/` tree has 91 entries, and zero of them is a `.mdt` or a `.mbn` at
top level** [F]. Zap images live in per-SoC subdirectories:

```
qcom/apq8096/a530_zap.mbn        File
qcom/qrb4210/a610_zap.mbn        File
qcom/qcs615/a612_zap.mbn         File
qcom/qcs8300/a623_zap.mbn        File
qcom/sdm845/a630_zap.mbn         File
qcom/sm8150/a640_zap.mbn         File
qcom/sm8250/a650_zap.mbn         File
qcom/qcm6490/a660_zap.mbn        File
qcom/sa8775p/a663_zap.mbn        File
qcom/qcm2290/a702_zap.mbn        File
qcom/shikra/a704_zap.mbn         File
qcom/sm8450/a730_zap.mbn         File
qcom/sm8550/a740_zap.mbn         File
...
```

with compatibility aliases as **symlinks**, not copies:

```
Link: qcom/a530_zap.mdt -> apq8096/a530_zap.mbn
Link: qcom/qcs6490/a660_zap.mbn -> ../qcm6490/a660_zap.mbn
Link: qcom/sm8350/a660_zap.mbn -> ../qcm6490/a660_zap.mbn
Link: qcom/maili/gen81400_zap.mbn -> ../hawi/gen81100_zap.mbn
```

`WHENCE` lists **24** `File:` zap images and **4** `Link:` zap aliases [F].

**`a615` does not appear in `WHENCE` at all** — not as a `File:`, not as a
`Link:`, not as a substring [F]. Neither does `a619`. The `qcom/` tree has no
`a615_zap.*`, no `a619_gmu.bin`, and no `sm4350/` subdirectory [F].

The closest 619-class zap images upstream are:

| upstream file | SoC dir | note |
|---|---|---|
| `a610_zap.mbn` | `qrb4210` | one revn below SM4350's 619 |
| `a612_zap.mbn` | `qcs615` | not 619 |

Neither is `a615_zap`, and the kernel requests by exact filename [F], so there
is no substitution path. **The SM4350 GPU cannot load a zap shader from
upstream firmware.**

### 7.1 The kernel's own fallback does not rescue it

`adreno_gpu.c` resolves the zap name from `.zapfw`, then optionally overrides it
from a DT `firmware-name` property on the `zap-shader` node, then calls
`adreno_request_fw()`, then `qcom_mdt_load()`. If the node is absent it returns
`-ENODEV` and marks the zap shader unavailable:

```c
np = of_get_available_child_by_name(dev->of_node, "zap-shader");
if (!np) {
	zap_available = false;
	return -ENODEV;
}
```

For SM4350 **both** inputs are missing: no DT node (no DT at all, §6.2) and no
firmware file (§7). So `a6xx_zap_shader_init()` cannot succeed [F].

## 8. Vendor builds are all smaller than upstream, for SQE

Comparing the corpus's builds against linux-firmware `main`:

| filename | upstream bytes | upstream md5 | corpus sizes | corpus rows byte-identical to upstream |
|---|---:|---|---|---:|
| `a630_sqe.fw` | 34,188 | `9f2540d789d9fd4699a566d97fcabded` | 32,136 / 32,264 / 32,272 / 32,304 / 32,448 / 32,456 / 32,504 | **0 of 51** |
| `a660_sqe.fw` | 43,292 | `aef1fcec7a927d0ceb2bc5d8903eb298` | 40,496 / 43,068 | **0 of 30** |
| `a660_gmu.bin` | 55,252 | `cd3a235218418f51360888637c1cb2ac` | 53,672 / 55,252 / 55,256 | **1 of 21** (`FP5`) |

Two observations:

1. **Every one of the seven `a630_sqe.fw` vendor builds is smaller than the
   upstream build** — the largest vendor build, 32,504 B, is 1,684 B short of
   upstream's 34,188 B [F]. Same for `a660_sqe.fw`: both vendor builds are
   smaller (40,496 and 43,068 vs 43,292) [F]. A uniform direction across nine
   builds is a pattern, not noise; the likely explanation is that upstream
   images carry extra header or signature sections, but I have not verified
   that [H].
2. **`a660_gmu.bin` breaks the pattern**: the upstream build is byte-identical
   to `FP5`'s, and the other two vendor builds (53,672 and 55,256) are on either
   side of it [F]. So GMU images are not uniformly smaller.

`Nord_200`'s own `a660_gmu.bin` (53,672 B) is the *smallest* of the three
`a660_gmu.bin` builds and 1,580 B below upstream [F] — consistent with the
`Qualcomm-SM8350-Snapdragon-888-soc.md` §9.5 note that flagged it.

**None of this says anything about whether the blobs work.** Size and digest
comparison cannot distinguish "older build" from "different signing envelope"
from "different feature set" [N].

## 9. Matrix defect: the a660 rows are typed `AUDIO`

Both a660 files on this device are `db_type = AUDIO`, not `GPU`:

| filename | `db_type` values, matrix-wide |
|---|---|
| `a660_gmu.bin` | `AUDIO` × **21** (all rows) |
| `a660_sqe.fw` | `AUDIO` × **30** (all rows) |

Against the correct typing for the other GPU files (`a619_gmu.bin` `GPU` ×24,
`a630_sqe.fw` `GPU` ×51, `a615_zap.mdt` `ELF64` ×27) [F].

This is a systematic mislabel, not a per-device error: **every** a660 row in the
corpus carries `AUDIO`. A GPU census keyed on `db_type = 'GPU'` would silently
drop both a660 files — and on `Nord_200` that is 100,876 of 178,504 GPU bytes,
**56.51%** of the family [F].

The `blob_family` column is correct for these rows; only `db_type` is wrong.
This note does not change the CSV (see N7).

## 10. The four-generation quartet is not an anomaly — my hypothesis was wrong

`Nord_200` carries Adreno generations `a615`, `a619`, `a630` and `a660`
together. My first reading was that this must be a labelling error: a 4-series
SoC should not have 6-series firmware. **That reading is wrong**, and the
evidence is strong enough that I am recording the correction rather than
quietly dropping it.

**16 devices carry that exact quartet**, across four vendors and eight
non-blank SoC labels [F]:

| device | SoC label |
|---|---|
| `Nord_200` | SM4350 (480) |
| `Nord_CE2` | SM6375 (695) |
| `Nord_CE3` | `ÿ`SM6375 (695 5G) |
| `Edge_30_Neo` | SM6375 (695) |
| `Moto_G34_5G` | SM6375 (695) |
| `Moto_G82_5G` | SM6375 (695) |
| `Moto_G84_5G` | SM6375 (695) |
| `Realme_10_Pro` | SM6375 (695) |
| `Realme_9_Pro` | SM6375 (695) |
| `Edge_30` | SM7325-AE (778G 5G) |
| `Edge_30_Fusion` | SM7250 (765G) |
| `Moto_G_5G_2024` | SM4375 (4 Gen 1) |
| `Moto_G200` | SM8350-AC (888+) |
| `Xperia_5_III` | SM8350 (888) |
| `Moto_G_Stylus_5G` | (blank) |
| `G_Stylus_5G-2-2022` | (blank) |

All 16 carry all four of `a615_zap.mdt`, `a619_gmu.bin`, `a630_sqe.fw` and
`a660_gmu.bin` [F].

In the wider corpus, generation-count distribution over all devices with any
`aNNN_` file:

| distinct Adreno generations | devices |
|---:|---:|
| 1 | 21 |
| 2 | 25 |
| 3 | 14 |
| **4** | **18** |
| 5 | 7 |
| 6 | 1 |

26 devices carry ≥4 generations, 18 of them exactly 4 [F]. The record holder is
`Phone_2` with six (`610/630/660/662/710/730`) [F].

**So the quartet is a vendor-partition superset, exactly as
`research/laptop/qualcomm-adreno-a650-fleet.md` §4 describes** — the vendor
partition ships a firmware set covering several SKUs that share a board or a
build target, and the device loads only the subset its chip needs. Reporting it
as a labelling error would have been a false positive, and the size of the
population (16 devices, 4 vendors, 8 SoC labels) is what makes it conclusive rather
than suggestive.

What remains true and worth keeping: the **a660 bytes on `Nord_200` are inert**.
The SoC is a 619 part (§1) and cannot execute `a660_*` firmware [I]. The
interesting question is not "why is there a660 here" — that is normal — but
"why is this particular a660 build a singleton" (§3.1, §8), which is a
build-provenance question, not an anomaly.

## 11. Honest negatives

Each item below is a thing this note does **not** establish.

**N1 — No SM4350 payload bytes were examined.** `data-fetch/` is empty and no
`dre` or `Nord_200` dump exists in the workspace. The only local `a619_gmu.bin`
is a synthetic test fixture with a different digest (§1.1). Every statement
about file content is filename, size, md5 and `db_type` — nothing about internal
structure, entry tables, or signature layout [N].

**N2 — The slice is one device, so nothing here is SoC-wide.** `Nord_200` is the
only SM4350 device in 123. Every count in §2–§5 describes one vendor's dump. I
have deliberately not written "SM4350 devices ship X"; where a claim is about
the SoC it is sourced from the kernel, not from the corpus [N].

**N3 — I cannot confirm `Nord_200`'s `a615_zap.mdt` is a complete container.**
At 6,708 B it sits inside the range of the split devices' 6,860 B whole
containers, which is *consistent* with completeness [I], but "consistent with"
is not "is". Establishing it needs the bytes and a PIL header parse [N].

**N4 — The direction of the SQE size delta is measured, not explained.** §8
shows all nine vendor SQE builds are smaller than upstream. The
extra-header/signature hypothesis is marked [H] and untested [N].

**N5 — I do not know why `Nord_200`'s four builds are singletons.** §3.1
establishes *that* they are (each on exactly one device in 33,917 rows) and §8
establishes how they compare to upstream. Whether this is a capture artifact, a
vendor branch, or a genuinely device-unique signing pass is not determinable
from metadata [N].

**N6 — The `0x06010900` duplication is reported, not fixed.** §6.1 records that
two catalog entries claim the same chip ID. I have not proposed a patch and am
not asserting which entry is intended; I only establish which one is reachable
[F] and that the two differ by one quirk [F].

**N7 — The `AUDIO` mislabel is reported, not fixed.** §9 records it; this commit
does not change the CSV. A matrix-wide `db_type` relabel is a separate change
with its own blast radius [N].

**N8 — No runtime verification, and none is possible from this evidence.**
postmarketOS marks the device *"not booting"* with the note *"Can't test while
my N200 is being borrowed"* [F]. There is therefore no working-mainline report
for this SoC to cite, and no dmesg to corroborate the §1 identity chain. The
`SM4350 → 0x06010900 → revn 619` chain is read from source, not from hardware
[N].

**N9 — §6.2's "dead code" conclusion depends on code search completeness.**
`repo:torvalds/linux "qcom,sm4350"` returning exactly 1 hit is strong evidence,
and the 664-file DT directory enumeration (`'4350' -> []`, `'holi' -> []`)
corroborates it independently. But code search indexes default branches and I
did not clone the tree, so an out-of-tree DT or a DT added on a non-default
branch would not appear [N].

**N10 — The `a740_zap` exception is unexplained.** §4 records that it satisfies
`mdt == b00 + b02` instead of `b00 + b01`. I have not established why that
family orders its segments differently, and I have not generalised from one
sample [N].

**N11 — `sequence_manifest.bin` / `unified_ksqs.bin` are counted, not
characterised.** §3 lists the manifest's size and build frequency; the
`unified_ksqs.bin` on this device (796,357 B, `dae8b801…`) is filed under
`other`/`FIRMWARE6`, not `gpu`, and is not analysed here. The 25-device
clustering of both files is already tabulated at
`research/laptop/fragmentation-half.md:153`; I cite it and add nothing [N].

**N12 — The `ÿ` label defect is reported, not investigated.** One SM6375 device
carries a leading `0xFF` byte in its `soc` string (§3.2, §10). It changes no
count in this note because I match on exact strings, but it would corrupt a
naive `startswith('Qualcomm')` filter [F].

## Reproduce

All commands run 2026-11-22 from the repo root. `python3 -I` throughout; no
third-party modules.

**Slice totals and the family table (§2):**

```sh
python3 -I - <<'PY'
import csv
from collections import Counter
cm=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
s=[r for r in cm if r['soc'].strip()=='Qualcomm SM4350 Snapdragon 480']
tot=sum(int(r['size_bytes']) for r in s)
print(len(s), len({r['device'] for r in s}), tot, len({r['filename'] for r in s}))
for f,n in Counter(r['blob_family'] for r in s).most_common():
    rs=[r for r in s if r['blob_family']==f]
    by=sum(int(r['size_bytes']) for r in rs)
    print(f, len(rs), len({r['filename'] for r in rs}), by, round(100*by/tot,2))
PY
```

Expect `44 1 146412066 44`, then `boot 3 3 109060096 74.49`,
`other 24 24 27556304 18.82`, `adsp 6 6 8873216 6.06`, `wifi 3 3 737078 0.5`,
`gpu 7 7 178504 0.12`, `modem 1 1 6868 0.0`.

**The seven GPU rows, their `db_type`, and the byte split (§3):**

```sh
python3 -I - <<'PY'
import csv
from collections import Counter
cm=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g=[r for r in cm if r['soc'].strip()=='Qualcomm SM4350 Snapdragon 480' and r['blob_family']=='gpu']
freq=Counter((r['filename'],r['md5_db']) for r in cm)
tot=sum(int(r['size_bytes']) for r in g)
for r in sorted(g,key=lambda r:r['filename']):
    print(r['filename'], int(r['size_bytes']), r['md5_db'], r['db_type'], freq[(r['filename'],r['md5_db'])])
live=sum(int(r['size_bytes']) for r in g if r['filename'] in ('a615_zap.mdt','a619_gmu.bin','a630_sqe.fw'))
a660=sum(int(r['size_bytes']) for r in g if r['filename'].startswith('a660_'))
man=sum(int(r['size_bytes']) for r in g if r['filename']=='sequence_manifest.bin')
print('total',tot,'live',live,round(100*live/tot,2),'a660',a660,round(100*a660/tot,2),'manifest',man,round(100*man/tot,2))
PY
```

Expect seven rows; `a615_zap.mdt 6708 … ELF64 1`, `a619_gmu.bin 32768 … GPU 24`,
`a630_sqe.fw 32448 … GPU 1`, `a660_gmu.bin 53672 … AUDIO 1`,
`a660_sqe.fw 40496 … AUDIO 21`, `a660_zap.mdt 6708 … ELF64 1`,
`sequence_manifest.bin 5704 … UNKNOWN 25`; then
`total 178504 live 71924 40.29 a660 100876 56.51 manifest 5704 3.2`.

**Singleton ranking over the 105 GPU-bearing devices (§3.1):**

```sh
python3 -I - <<'PY'
import csv
from collections import Counter,defaultdict
cm=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
freq=Counter((r['filename'],r['md5_db']) for r in cm)
per=defaultdict(lambda:[0,0])
for r in cm:
    if r['blob_family']!='gpu': continue
    per[r['device']][0]+=1
    if freq[(r['filename'],r['md5_db'])]==1: per[r['device']][1]+=1
print(len(per), sum(1 for v in per.values() if v[1]==0))
for d,(rows,sing) in sorted(per.items(),key=lambda x:-x[1][1])[:12]:
    print(d,rows,sing)
print(sorted(Counter(v[1] for v in per.values()).items()))
PY
```

Expect `105 54`, the top twelve of §3.1 ending `Nord_200 7 4`, and the
distribution `[(0,54),(1,21),(2,10),(3,2),(4,8),(5,1),(6,1),(9,3),(11,1),(12,1),(19,1),(20,2)]`.

**The three filename censuses (§3.2, §3.3):**

```sh
python3 -I - <<'PY'
import csv
from collections import Counter
cm=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for fn in ('a619_gmu.bin','a618_gmu.bin','a630_sqe.fw','a615_zap.mdt'):
    rs=[r for r in cm if r['filename']==fn]
    print(fn,len(rs),len({r['device'] for r in rs}),len({r['md5_db'] for r in rs}),sorted({int(r['size_bytes']) for r in rs}))
for fn in ('a660_gmu.bin','a660_sqe.fw'):
    for md5,n in Counter(r['md5_db'] for r in cm if r['filename']==fn).most_common():
        rs=[r for r in cm if r['filename']==fn and r['md5_db']==md5]
        print(fn,md5[:12],int(rs[0]['size_bytes']),n)
PY
```

Expect `a619_gmu.bin 24 24 1 [32768]`, `a618_gmu.bin 2 2 1 [32768]`,
`a630_sqe.fw 51 51 7 [32136, 32264, 32272, 32304, 32448, 32456, 32504]`,
`a615_zap.mdt 27 27 18 [6684, 6708, 6860]`, then the a660 build rows of §8.

**The split-segment law, matrix-wide and zap-only (§4):**

```sh
python3 -I - <<'PY'
import csv
from collections import defaultdict
cm=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
segs=defaultdict(dict); mdt={}
for r in cm:
    fn=r['filename']
    if '.b' in fn and fn.rsplit('.b',1)[1].isdigit():
        stem,ext=fn.rsplit('.b',1); segs[(r['device'],stem)][int(ext)]=int(r['size_bytes'])
    elif fn.endswith('.mdt'):
        mdt[(r['device'],fn[:-4])]=int(r['size_bytes'])
tot=ok=zt=zo=0
for k,d in segs.items():
    if 0 not in d or 1 not in d or k not in mdt: continue
    tot+=1; ok += mdt[k]==d[0]+d[1]
    if 'zap' in k[1]:
        zt+=1; zo += mdt[k]==d[0]+d[1]
print('all',ok,tot,'zap',zo,zt)
for stem in sorted({s for (_,s) in segs if 'zap' in s}):
    keys=[k for k in segs if k[1]==stem and k in mdt]
    print(stem,len(keys),sum(1 for k in keys if mdt[k]==segs[k].get(0,0)+segs[k].get(1,0)))
PY
```

Expect `all 669 1314 zap 41 42`, then `a610_zap 11 11`, `a615_zap 7 7`,
`a660_zap 3 3`, `a740_zap 1 0`, `egtzappf 8 8`, `fpctzapp 12 12`.

**Segment invariance across the split devices (§4.1):**

```sh
python3 -I - <<'PY'
import csv
from collections import Counter
cm=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for stem in ('a615_zap','a660_zap'):
    for ext in (0,1,2):
        rs=[r for r in cm if r['filename']==f'{stem}.b0{ext}']
        if rs: print(stem,ext,len(rs),len({r['md5_db'] for r in rs}),sorted({int(r['size_bytes']) for r in rs}))
    m=[r for r in cm if r['filename']==stem+'.mdt' and r['device'] in {r2['device'] for r2 in cm if r2['filename'].startswith(stem+'.b')}]
    print(stem,'paired mdt',len(m),len({r['md5_db'] for r in m}),sorted({int(r['size_bytes']) for r in m}))
PY
```

Expect `a615_zap 0 7 1 [148]`, `a615_zap 1 7 7 [6712]`, `a615_zap 2 7 1 [1984]`,
`a615_zap paired mdt 7 7 [6860]`, then the a660 equivalents
`0 3 1 [148]`, `1 3 3 [6712]`, `2 3 1 [1976]`, `paired mdt 3 3 [6860]`.

**Sibling absence, matrix-wide and per device (§5):**

```sh
python3 -I - <<'PY'
import csv
cm=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
seg={r['device'] for r in cm if '.b' in r['filename'] and r['filename'].rsplit('.b',1)[1].isdigit()}
md={r['device'] for r in cm if r['filename'].endswith('.mdt')}
print(len(seg),len(md),len(md-seg))
nord=[r['filename'] for r in cm if r['device']=='Nord_200' and r['filename'].endswith('.mdt')]
print(len(nord),sorted(nord))
print(sum(1 for r in cm if r['device']=='Nord_200' and r['filename'].rsplit('.b',1)[-1].isdigit()))
PY
```

Expect `63 91 28`, then `6` and the six stems, then `0`.

**The catalog's machine gates and the duplicated chip ID (§6):**

```sh
python3 -I - <<'PY'
import subprocess
u='https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/gpu/drm/msm/adreno/a6xx_catalog.c'
src=subprocess.run(['curl','-s',u],capture_output=True,text=True).stdout
lines=src.split(chr(10))
print('revn',sum(1 for l in lines if '.revn =' in l),'machine',sum(1 for l in lines if '.machine =' in l))
for i,l in enumerate(lines,1):
    if '.machine =' in l or '0x0601090' in l: print(i,l.strip())
PY
```

Expect `revn 11 machine 3`, then lines `820`, `870`, `871`, `895`, `896`, `920`
as tabulated in §6.1 — in particular `0x06010900` at both `871` and `920`, and
`0x06010901` at `896`.

**The DT absence and the linux-firmware absence (§6.2, §7):**

```sh
curl -s "https://api.github.com/repos/torvalds/linux/contents/arch/arm64/boot/dts/qcom?ref=master" \
 | python3 -I -c "import json,sys; n=[x['name'] for x in json.load(sys.stdin)]; print(len(n)); [print(k,[f for f in n if k in f][:3]) for k in ('4350','holi','6375')]"
curl -s "https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/qcom/?h=main" \
 | python3 -I -c "import re,sys; h=sys.stdin.read(); n=sorted(set(re.findall(r'tree/qcom/([A-Za-z0-9_.\-]+)\?h=main',h))); print(len(n)); print([x for x in n if x.endswith(('.mdt','.mbn'))]); print([x for x in n if 'a615' in x or 'a619' in x])"
curl -s "https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/WHENCE" \
 | python3 -I -c "import sys; t=sys.stdin.read(); print(t.count('File: qcom/'), sum(1 for l in t.split(chr(10)) if 'zap' in l and l.startswith('File:')), sum(1 for l in t.split(chr(10)) if 'zap' in l and l.startswith('Link:')), 'a615' in t, 'a619' in t)"
```

Expect `664`, `[]` for `4350`, `[]` for `holi`, two filenames for `6375`; then
`91`, `[]`, `[]`; then `393 24 4 False False` — 393 `File: qcom/` entries in
all, 24 of them zap images, 4 zap `Link:` aliases, and `a615`/`a619` absent.

**The upstream-versus-vendor comparison (§8):**

```sh
for f in a630_sqe.fw a660_gmu.bin a660_sqe.fw; do
  curl -s "https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/qcom/$f" \
   | python3 -I -c "import sys,hashlib; d=sys.stdin.buffer.read(); print('$f',len(d),hashlib.md5(d).hexdigest())"
done
```

Expect `a630_sqe.fw 34188 9f2540d789d9fd4699a566d97fcabded`,
`a660_gmu.bin 55252 cd3a235218418f51360888637c1cb2ac`,
`a660_sqe.fw 43292 aef1fcec7a927d0ceb2bc5d8903eb298`. Compare against the corpus
sizes printed by the §3.3 block.

**The `AUDIO` mislabel (§9):**

```sh
python3 -I - <<'PY'
import csv
from collections import Counter
cm=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
for fn in ('a660_gmu.bin','a660_sqe.fw','a619_gmu.bin','a630_sqe.fw','a615_zap.mdt'):
    print(fn,Counter(r['db_type'] for r in cm if r['filename']==fn).most_common())
PY
```

Expect `AUDIO` 21 for `a660_gmu.bin`, `AUDIO` 30 for `a660_sqe.fw`, `GPU` 24,
`GPU` 51, `ELF64` 27.

**The quartet population and generation distribution (§10):**

```sh
python3 -I - <<'PY'
import csv,re
from collections import Counter,defaultdict
cm=list(csv.DictReader(open('upstream-contribution/blob-database/coverage-matrix.csv')))
g=defaultdict(set)
for r in cm:
    m=re.match(r'a(\d{3})_',r['filename'])
    if m: g[r['device']].add(m.group(1))
print(sorted(Counter(len(v) for v in g.values()).items()))
q=sorted(d for d,v in g.items() if v>={'615','619','630','660'})
print(len(q))
for d in q: print(d,sorted({r['soc'] or '(blank)' for r in cm if r['device']==d})[0])
PY
```

Expect `[(1,21),(2,25),(3,14),(4,18),(5,7),(6,1)]` and `16` followed by the
sixteen device rows of §10.

## Sources

| source | what it gave | fetched |
|---|---|---|
| `upstream-contribution/blob-database/coverage-matrix.csv` (33,917 rows, 123 devices, 27 SoC labels) | every count, size, digest, `db_type` and `blob_family` in §2–§5, §8–§10 | in-repo |
| `docs/REPO-STATE-MAP.md` | the GPU doc counts updated in this commit | in-repo |
| `research/soc/Qualcomm-SM4375-Snapdragon-4-Gen-1-gpu.md` (#2024) | the SM4350 = Adreno-619-class assertion, the `fpctzapp` damage, the split law | in-repo |
| `research/soc/Qualcomm-SM7250-Snapdragon-765G-gpu.md` (#2029) | the `a619_gmu.bin` invariant and `a630_sqe.fw` census | in-repo |
| `research/soc/Qualcomm-SM8350-Snapdragon-888-soc.md` (#823) | the 53,672 B `a660_gmu.bin` note; house format | in-repo |
| `research/laptop/qualcomm-adreno-a650-fleet.md` | the vendor-partition-superset law (§10) | in-repo |
| `research/laptop/fragmentation-half.md:153`, `research/fleet/deep-re-notes.md:97` | the `sequence_manifest` / `unified_ksqs` clustering cited in N11 | in-repo |
| `torvalds/linux` `a6xx_catalog.c`, 44,014 B, master `4843f6873f7c` | the SM4350 entry, the duplicated chip ID, all 11 `.revn` and 3 `.machine` sites | 2026-11-22 |
| `torvalds/linux` `adreno_gpu.c` (33,870 B), `adreno_device.c` (10,280 B) | `zap_shader_load_mdt()`, the `zap-shader` node lookup, `adreno_info()`'s machine gate | 2026-11-22 |
| `torvalds/linux` `a6xx_gpu.c` (87,809 B) | `a6xx_zap_shader_init()` | 2026-11-22 |
| `torvalds/linux` `arch/arm64/boot/dts/qcom/` (664 files), `sm6375.dtsi` (59,637 B), `sm8250.dtsi` | the DT absence; the `sm6375` contrast; the missing GPU node | 2026-11-22 |
| linux-firmware `WHENCE` (540,253 B, `main`) and the `qcom/` tree (91 entries) | the 24 `File:` / 4 `Link:` zap images, and every absence in §7 | 2026-11-22 |
| linux-firmware `qcom/a630_sqe.fw`, `a660_gmu.bin`, `a660_sqe.fw` | upstream sizes and digests for §8 | 2026-11-22 |
| postmarketOS wiki, `OnePlus_Nord_N200_(oneplus-dre)` | "not booting", Adreno 619, SM4350, category testing (N8) | 2026-11-22 |
| GitHub code search (authenticated) | the 13 queries of Gate 0 and the `qcom,sm4350` single-hit result in §6.2 | 2026-11-22 |
