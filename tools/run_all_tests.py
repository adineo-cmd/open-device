#!/usr/bin/env python3
"""Run every committed self-test in the repository from any working directory.

Covers three conventions that exist today:

  * Python unittest suites in implementations/*/ (fixtures materialised first)
  * the historic/fp2 check() harness, which unittest discover cannot collect
  * C self-tests compiled with the flags documented in implementations/README.md
  * the archived site generator's Python tests under site/tests/

Exit status is non-zero if any component fails.
"""

import glob
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMPL = os.path.join(ROOT, "implementations")
PY_IGNORE = {"implementations/historic/fp2"}


def rel(path):
    return os.path.relpath(path, ROOT)


def run(cmd, cwd, env=None):
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return proc.returncode, proc.stdout


def python_components():
    found = {}
    for path in glob.glob(os.path.join(IMPL, "**", "test_*.py"), recursive=True):
        found.setdefault(os.path.dirname(path), []).append(path)
    return dict(sorted(found.items()))


def c_components():
    found = {}
    for path in glob.glob(os.path.join(IMPL, "**", "test_*.c"), recursive=True):
        found.setdefault(os.path.dirname(path), []).append(path)
    return dict(sorted(found.items()))


def run_python(directory):
    name = rel(directory)
    if os.path.exists(os.path.join(directory, "make_fixture.py")):
        rc, out = run([sys.executable, "-I", "make_fixture.py"], directory)
        if rc != 0:
            return rc, out
    if name in PY_IGNORE:
        return run([sys.executable, "-I", "test_parsers.py"], directory)
    return run([sys.executable, "-I", "-m", "unittest", "discover", "-q"], directory)


def run_c(directory, build_dir, index):
    tests = sorted(glob.glob(os.path.join(directory, "test_*.c")))
    sources = [p for p in glob.glob(os.path.join(directory, "*.c")) if os.path.basename(p) not in [os.path.basename(t) for t in tests]]
    binary = os.path.join(build_dir, "test_%d" % index)
    cmd = ["cc", "-std=c99", "-Wall", "-Wextra", "-O2", "-o", binary] + tests + sources
    rc, out = run(cmd, directory)
    if rc != 0:
        return rc, out
    return run([binary], directory)


def main():
    results = []
    temp = tempfile.mkdtemp(prefix="open-device-tests-")
    try:
        for directory in python_components():
            rc, out = run_python(directory)
            results.append((rel(directory), rc, out))
        for index, directory in enumerate(c_components()):
            rc, out = run_c(directory, temp, index)
            results.append((rel(directory), rc, out))
        site_tests = os.path.join(ROOT, "site", "tests")
        if os.path.isdir(site_tests):
            rc, out = run([sys.executable, "-I", "-m", "unittest", "discover", "-s", "tests", "-q"], os.path.join(ROOT, "site"))
            results.append(("site/tests", rc, out))
    finally:
        shutil.rmtree(temp, ignore_errors=True)

    failures = 0
    print("%-52s %s" % ("component", "result"))
    print("-" * 62)
    for name, rc, out in results:
        print("%-52s %s" % (name, "PASS" if rc == 0 else "FAIL"))
        if rc != 0:
            failures += 1
            for line in out.splitlines()[-12:]:
                print("    " + line)
    print("-" * 62)
    print("%d components, %d failed" % (len(results), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
