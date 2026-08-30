#!/usr/bin/env python3
"""Freshness check: compare every shipped legal source against the live
consolidation and report drift.

Runs each regen_*.py in its default check mode — which fetches the current
text from BC Laws / Justice Laws, diffs it against references/generated/,
and exits non-zero on any change — then summarises the lot and exits
non-zero if any source has drifted. It is the skill's amendment monitor:

    python3 scripts/check_freshness.py      # run by hand or from cron/CI

A scheduled workflow (.github/workflows/check-freshness.yml) runs it
weekly. On drift, refresh with the matching `regen_<source>.py --write`
and rerun scripts/build_forms_index.py.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ("fla", "pcfr", "scfr", "da", "csg")


def run_check(source: str) -> tuple[str, str]:
    """Return (status, message) for one source: ok, drift, or error."""
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / f"regen_{source}.py")],
        capture_output=True,
        text=True,
    )

    summary = ""
    for line in proc.stdout.splitlines():
        if " generated | " in line:
            summary = line.strip()
            break
    if summary.startswith(f"{source}: "):
        summary = summary[len(source) + 2:]

    if proc.returncode == 0:
        return "ok", summary or "current"

    if summary:
        return "drift", summary

    last = proc.stderr.strip().splitlines()
    return "error", (last[-1] if last else "failed (no output)")


def main() -> int:
    drifted = 0
    errored = 0
    for source in SOURCES:
        status, message = run_check(source)
        label = {"ok": "OK   ", "drift": "DRIFT", "error": "ERROR"}[status]
        print(f"{label} {source}: {message}")
        if status == "drift":
            drifted += 1
        elif status == "error":
            errored += 1

    if errored:
        print("\nSome sources could not be checked (network?). Try again.")
        return 1
    if drifted:
        print(f"\n{drifted} source(s) drifted. Refresh with "
              "`python3 scripts/regen_<source>.py --write`, then rerun "
              "`scripts/build_forms_index.py`.")
        return 1
    print("\nAll references current.")
    return 0


if __name__ == "__main__":
    sys.exit(main())