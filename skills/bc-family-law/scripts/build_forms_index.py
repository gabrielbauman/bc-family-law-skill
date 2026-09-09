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
PCFR_DIR = REFS / "generated" / "pcfr"
SCFR_DIR = REFS / "generated" / "scfr"

# PCFR cites forms as: Form 3 [Application About a Family Law Matter]
PCFR_PATTERN = re.compile(r"Form (\d+(?:\.\d+)?) \[([^\]]+)\]")
# SCFR cites forms as: Form F35 (no bracketed name in the rule text)
SCFR_PATTERN = re.compile(r"Form (F\d+(?:\.\d+)?)\b")


def natural_key(form_no: str):
    return [float(p) for p in form_no.lstrip("F").split(".")]


def scan(pattern, directory):
    forms = defaultdict(lambda: {"names": set(), "rules": set()})
    for path in sorted(directory.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            number = match.group(1)
            entry = forms[number]
            entry["rules"].add(path.name)
            if pattern is PCFR_PATTERN:
                entry["names"].add(match.group(2))
    return forms


def rule_links(rules, prefix):
    return ", ".join(
        f"[{r.removesuffix('.md')}]({prefix}/{r})" for r in sorted(rules)
    )


def main():
    pcfr = scan(PCFR_PATTERN, PCFR_DIR)
    scfr = scan(SCFR_PATTERN, SCFR_DIR)
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
        "**This file is long — grep it for the form number you need**",
        "(`grep 'Form 4 ' forms-guide.md`) rather than reading it whole. The",
        "tables below list every form in both rule sets; almost no question",
        "needs more than a handful.",
        "",
        "## Starting a case: the forms that come first",
        "",
        "**Provincial Court.** Which form starts the case depends on the",
        "registry. A registry listed in",
        "[PCFR Appendix 1](generated/pcfr/appendix_1_early_resolution_registries.md)",
        "is an *early resolution registry* (Rule 6(a)): there the case starts",
        "with a **Form 1** Notice to Resolve a Family Law Matter, and a needs",
        "assessment, parenting education and a consensual dispute resolution",
        "session must be completed before an application can be filed",
        "([Rule 10](generated/pcfr/rule_010_early_resolution_requirements_must_be_met_before_application_filed.md)).",
        "Everywhere else the case starts with a **Form 3** Application About a",
        "Family Law Matter. Check the appendix before naming a form — the list",
        "changed with B.C. Reg. 17/2026, so it is not something to recall.",
        "",
        "The rest of the early sequence: **Form 6** Reply to an Application",
        "About a Family Law Matter (with Counter Application), **Form 4**",
        "Financial Statement wherever support is in issue, **Form 10**",
        "Application for Case Management Order for interim relief, and",
        "**Form 12** Application About a Protection Order.",
        "",
        "**Supreme Court.** A family law case starts with a **Form F3** Notice",
        "of Family Claim ([Rule 4-1](generated/scfr/rule_4_1_notice_of_family_claim.md)),",
        "answered by a **Form F4** Response",
        "([Rule 4-3](generated/scfr/rule_4_3_responding_to_a_notice_of_family_claim.md));",
        "financial disclosure is **Form F8** ([Rule 5-1](generated/scfr/rule_5_1_financial_disclosure.md)),",
        "and interim relief is applied for by **Form F31** notice of",
        "application ([Rule 10-6](generated/scfr/rule_10_6_usual_application_procedure.md)).",
        "",
        "Form names above are quoted from the rule texts; confirm the current",
        "blank form at the court's forms page before filing.",
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
        lines.append(f"| Form {number} | {names} | {rule_links(entry['rules'], 'generated/pcfr')} |")

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
        lines.append(f"| Form {number} | {rule_links(scfr[number]['rules'], 'generated/scfr')} |")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REFS.parent)}: {len(pcfr)} PCFR forms, {len(scfr)} SCFR forms")


if __name__ == "__main__":
    main()
