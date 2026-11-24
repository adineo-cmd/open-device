#!/usr/bin/env python3
"""Fail if source files still refer to the pre-rename repository name.

RENAME.md is excluded: it is the historical record of the rename. Generated
site/out/ HTML is excluded because it is rebuilt from source. Fix source files,
not generated output.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = "librephone-blob-research"
SKIP_DIRS = {".git", "out", "node_modules", "dist", "__pycache__"}
SKIP_FILES = {"RENAME.md", "LICENSE", "LICENSE-CODE", "LICENSE-DOCS", "check_stale_names.py"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".woff", ".woff2", ".pdf", ".zip"}


def sources():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name in SKIP_FILES or os.path.splitext(name)[1] in SKIP_EXT:
                continue
            yield os.path.join(base, name)


def main():
    hits = []
    for path in sources():
        try:
            with open(path, encoding="utf-8") as handle:
                lines = handle.readlines()
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(lines, 1):
            if OLD in line:
                hits.append((os.path.relpath(path, ROOT), number, line.strip()))
    if hits:
        print("stale repository name in %d source lines:" % len(hits))
        for path, number, line in hits:
            print("  %s:%d: %s" % (path, number, line[:160]))
        return 1
    print("no stale repository name in source files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
