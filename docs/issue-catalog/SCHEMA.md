# Issue catalog schema

Four JSONL files live in this directory. Each line is one JSON object with the
same shape:

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Stable opaque identifier |
| `key` | string | Namespaced issue key, unique within a file |
| `title` | string | Issue title |
| `body` | string | Full issue body, including the claim-protocol text |
| `labels` | array of string | GitHub labels (`area:*`, `type:*`, `device-type:*`, etc.) |

## Files and key namespaces

| File | Key prefix | Scope |
| --- | --- | --- |
| `issues.jsonl` | mixed | Full published corpus (2,836 records at last generation) |
| `device-packages.jsonl` | `devicepkg:` | One sustained package per device |
| `coverage-packages.jsonl` | `coverage:` | Coverage gaps by family |
| `full-coverage.jsonl` | `full:` | Full-coverage deep-RE packages |

The files are *not* subsets of one another: each uses its own key namespace.
Counts in the table above are whatever the committed files contain; do not
copy them into prose without re-running `tools/check_catalogs.py`.

## Validation

```bash
python3 tools/check_catalogs.py
```

It checks JSON parseability, required fields, duplicate `id` and `key` values,
and prints record counts. CI runs it on every push and pull request.

## Generation and drift

`docs/issue-catalog/README.md` states these files are generated
deterministically from the committed CSV and Markdown corpus. The publisher in
`tools/issue-publisher/` is the authoritative writer. If you edit a catalog by
hand, also fix its source so the next generation does not undo your change.

README counts and the live GitHub issue count will differ: the catalog records
all atomic issues ever generated, while GitHub's "open issues" count excludes
closed and already-done ones. State which number you are quoting.
