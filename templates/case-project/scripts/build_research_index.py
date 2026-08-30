#!/usr/bin/env python3
"""Regenerate the registry table in research/index.md from the research files.

Each research document carries a small frontmatter block; this script reads it
and rewrites the table between the GENERATED markers in research/index.md, so
the index can never drift from the files it describes. Run from the project
root:

    python3 scripts/build_research_index.py

Every file in research/ (except index.md) must start with frontmatter:

    ---
    purpose: what this extraction shows, in one line
    source: the evidence/filings file + exact query or command used
    primary_source: short label for the index's "Primary source" column
    extracted: 2025-04-12
    ---

A file missing this block is reported, not silently skipped — an unindexed
research file is the exact drift this script exists to prevent.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "research"
INDEX = RESEARCH / "index.md"

BEGIN = "<!-- BEGIN GENERATED REGISTRY -->"
END = "<!-- END GENERATED REGISTRY -->"
FIELDS = ("purpose", "source", "primary_source", "extracted")


def parse_frontmatter(text: str) -> dict | None:
    """Return the leading --- frontmatter block as a dict, or None if absent."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    meta = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return meta
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return None  # unterminated block — treat as malformed


def main() -> None:
    if not INDEX.exists():
        sys.exit(f"error: {INDEX} not found; run from the project root")

    rows, problems = [], []
    for path in sorted(RESEARCH.glob("*.md")):
        if path.name == "index.md":
            continue
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        if meta is None:
            problems.append(f"{path.name}: missing or malformed frontmatter")
            continue
        missing = [f for f in FIELDS if not meta.get(f)]
        if missing:
            problems.append(f"{path.name}: missing field(s) {', '.join(missing)}")
        rows.append((
            f"[{path.name}]({path.name})",
            meta.get("purpose", "?"),
            meta.get("primary_source", "?"),
            meta.get("extracted", "?"),
        ))

    table = ["| File | Purpose | Primary source | Extracted |",
             "|------|---------|----------------|-----------|"]
    for f, purpose, primary, extracted in rows:
        table.append(f"| {f} | {purpose} | {primary} | {extracted} |")
    if not rows:
        table.append("| _(no research documents yet)_ | | | |")

    text = INDEX.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        sys.exit(f"error: {INDEX} is missing the {BEGIN} / {END} markers")
    head, _, rest = text.partition(BEGIN)
    _, _, tail = rest.partition(END)
    INDEX.write_text(
        f"{head}{BEGIN}\n" + "\n".join(table) + f"\n{END}{tail}",
        encoding="utf-8",
    )

    print(f"wrote research/index.md: {len(rows)} document(s)")
    for p in problems:
        print(f"  WARNING {p}", file=sys.stderr)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
