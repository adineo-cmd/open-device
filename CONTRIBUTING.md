# Contributing

Thanks for wanting to help. This project has two audiences: a small agent
fleet that works the GitHub issue backlog under a strict claim protocol, and
human contributors who should not have to read 8 KB of agent rules to fix a
typo. This file is the human path. `AGENTS.md` remains the binding contract for
agents.

## Ground rules (all contributors)

1. **Facts, not blobs.** Never commit a proprietary firmware image, blob,
   decompiled output, MAC/serial, or calibration table. `*.bin`, `*.mbn`,
   `*.img`, `*.elf`, `*.so`, `*.zip`, `*.mdt`, `downloads/`, `blobs/` and
   `vendor/` are gitignored; do not work around that.
2. **Clean room.** Implementation code must be derived from published specs,
   public documentation and public GPL headers — not from vendor binaries.
   Each component carries a clean-room statement; keep it accurate.
3. **Verify numbers.** Every count, address, hash and version printed in a
   finding must be reproducible from a command or a committed script.
4. **Negative results count.** A failed hypothesis is a deliverable. Record it
   rather than quietly dropping it.
5. **Prior art first for research.** Before claiming a new *finding*, search
   GitHub (excluding `adineo-cmd/*`), the wider web, arXiv/Scholar and the
   kernel/linux-firmware trees. Record the exact queries and access dates in
   the finding. Format: `research/_template/finding.md`.
6. **Licensing.** Code is GPL-2.0-only, docs and data are CC BY-SA 4.0 (see
   `LICENSE`). By contributing you agree to those terms for the material you
   touch.

## Human quick path

1. Pick an issue labelled `good first issue`, or open a small PR directly for
   docs, fixtures, tests or site fixes.
2. Comment on the issue saying you are working on it. **If the issue already
   has a `CLAIM` comment from an agent, leave it alone** — one issue, one owner
   (`AGENTS.md`, Rule 2). Ask on the issue if unsure.
3. Work on a branch. Python is standard library only; run scripts with
   `python3 -I`. Dependencies for the CLI tools are in `requirements.txt`.
4. Run the checks:
   ```bash
   python3 -m pip install -r requirements.txt   # only for the ISA/CLI tools
   python3 tools/run_all_tests.py               # all component self-tests
   python3 tools/check_stale_names.py
   python3 tools/check_catalogs.py
   python3 tools/check_state_map.py
   ```
5. Push your branch and open a PR against `feat/open-device-site` (see
   `BRANCHING.md`). Fill in the PR template.
6. If you changed a stale number or a broken link, fix it in the same PR and
   list the before/after in your report (Rule 1).

## Where things go

| Change | Directory |
| --- | --- |
| A new finding with evidence | `research/<track>/`, using `research/_template/finding.md` |
| A corrected earlier claim | edit in place **and** add a row to `research/CORRECTIONS.md` |
| A parser, probe or container walker | `implementations/<family>-fleet/`, with `make_fixture.py` and a self-test |
| A CLI extraction/analysis script | `tools/<substrate>/` |
| A derived dataset | `data/` or `upstream-contribution/blob-database/`, with its generator |
| Per-device notes | `docs/devices/<vendor>/<device>/` |
| Website | `src/` (live Astro source); `site/` is the archived generator, not deployed |

## Getting device dumps

The repository ships no firmware. You must supply your own legally obtained
dump; see `docs/EXTERNAL-FIRMWARE-DIRECTORY.md` for public sources. Nothing in
this project asks you to bypass access controls or license agreements.

## Code of conduct

See `CODE_OF_CONDUCT.md`. Security-sensitive reports: see `SECURITY.md`.
