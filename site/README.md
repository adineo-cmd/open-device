# site/ — archived Python generator

**This directory is not deployed.** The live website is the Astro project at the
repository root (`astro.config.mjs`, `src/`, `public/`), built with
`npm install && npm run build` and published by
`.github/workflows/pages.yml` to
<https://adineo-cmd.github.io/open-device/>.

`site/` is the original Python generator, kept as provenance for how the first
version of the site was produced. Its `build.py`, `lib/` and `data/` are useful
for understanding the dataset, and `site/tests/` are still run by
`tools/run_all_tests.py`. Do not add new site features here — add them to `src/`.

`site/out/` contains generated HTML from an older build. It is not the
published site and may contain historical wording (including the pre-rename
repository name) until regenerated. Source files are checked for stale names by
`tools/check_stale_names.py`; generated output is intentionally excluded.
