#!/usr/bin/env python3
"""Regenerate references/forms-guide.md from the rule texts in references/.

Every entry in the generated guide is extracted verbatim from the Provincial
Court Family Rules and Supreme Court Family Rules reference files, so the
guide stays verifiable: each form lists the rule files that mention it.

Run from the repository root:

    python3 scripts/build_forms_index.py
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

REFS = Path(__file__).resolve().parent.parent / "references"
OUT = REFS / "forms-guide.md"

# PCFR cites forms as: Form 3 [Application About a Family Law Matter]
PCFR_PATTERN = re.compile(r"Form (\d+(?:\.\d+)?) \[([^\]]+)\]")
# SCFR cites forms as: Form F35 (no bracketed name in the rule text)
SCFR_PATTERN = re.compile(r"Form (F\d+(?:\.\d+)?)\b")


def natural_key(form_no: str):
    return [float(p) for p in form_no.lstrip("F").split(".")]


def scan(pattern, glob):
    forms = defaultdict(lambda: {"names": set(), "rules": set()})
    for path in sorted(REFS.glob(glob)):
        text = path.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            number = match.group(1)
            entry = forms[number]
            entry["rules"].add(path.name)
            if pattern is PCFR_PATTERN:
                entry["names"].add(match.group(2))
    return forms


def rule_links(rules):
    return ", ".join(f"[{r.removesuffix('.md')}]({r})" for r in sorted(rules))


def main():
    pcfr = scan(PCFR_PATTERN, "pcfr_rule_*.md")
    scfr = scan(SCFR_PATTERN, "scfr_rule_*.md")
    if not pcfr or not scfr:
        sys.exit("error: no form references found; run from the repo root")

    lines = [
        "# Court Forms Guide",
        "",
        "Maps form numbers to the rules that require them. Generated from the",
        "rule texts in this folder by `scripts/build_forms_index.py` — every",
        "entry below is extracted verbatim from a rule file, so to confirm what",
        "a form is for, open the linked rule.",
        "",
        "Blank forms and filing instructions:",
        "",
        "- Provincial Court: https://www.provincialcourt.bc.ca/types-of-cases/family-matters/family-forms",
        "- Supreme Court: https://www.bccourts.ca/supreme_court/self-represented_litigants/",
        "- Online filing: https://justice.gov.bc.ca/cso/",
        "",
        "## Provincial Court Family Rules forms",
        "",
        "Form names below are quoted from the rule texts.",
        "",
        "| Form | Name (per rule text) | Referenced by |",
        "|------|----------------------|---------------|",
    ]
    for number in sorted(pcfr, key=natural_key):
        entry = pcfr[number]
        names = "; ".join(sorted(entry["names"]))
        lines.append(f"| Form {number} | {names} | {rule_links(entry['rules'])} |")

    lines += [
        "",
        "## Supreme Court Family Rules forms",
        "",
        "The SCFR text cites form numbers without names. Look up names on the",
        "official forms page above, or read the referencing rule for context.",
        "",
        "| Form | Referenced by |",
        "|------|---------------|",
    ]
    for number in sorted(scfr, key=natural_key):
        lines.append(f"| Form {number} | {rule_links(scfr[number]['rules'])} |")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REFS.parent)}: {len(pcfr)} PCFR forms, {len(scfr)} SCFR forms")


if __name__ == "__main__":
    main()
