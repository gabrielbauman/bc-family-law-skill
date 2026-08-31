# bc-family-law

A skill for self-represented litigants navigating family law matters in
**British Columbia, Canada** — Provincial Court and Supreme Court. It is
agent-agnostic, working in Claude Code, OpenCode, or any agent that can
load skills.

It was distilled from a real BC Provincial Court family case run by a
self-represented litigant with AI assistance, from first filing through a
three-day trial to judgment. The practice guides encode what that case
learned the hard way: evidence citation discipline, case-law verification,
what belongs in a trial book (and what counsel ordered removed from one),
and the procedural traps that catch self-represented parties.

## What it does

- **Answers BC family law questions** from reproduced legal texts — the
  Family Law Act, Divorce Act, Federal Child Support Guidelines, both
  courts' family rules, and the SSAG User's Guide, split into per-section
  files the model loads on demand instead of answering from memory.
- **Runs a case project**: a git-tracked folder that carries your matter
  across sessions — evidence, filings, research with verifiable citations,
  case law with full texts, drafts, and a single CASE.md dashboard. You
  drop new documents into an inbox (or anywhere); the structure is
  maintained for you, and every session starts by finding, filing, and
  recording whatever you added.
- **Prepares you for court**: practice guides for evidence selection,
  affidavits, cross-examination, and trial; LaTeX templates for a
  two-part trial book and a book of authorities.
- **Holds the line on accuracy**: facts must cite primary sources,
  inferences must be labelled, quotes must be verbatim and complete, and
  no case may be cited without its full text on hand — because in court,
  one exposed error taints everything else you say.

## What it is not

**This is legal information, not legal advice.** No skill makes an AI a
lawyer. It will not predict your outcome, it can make mistakes, and the
reproduced legal texts are a snapshot (see
`skills/bc-family-law/references/legal-sources.md`) — the law may have changed. For advice
about your situation, consult a family lawyer; Legal Aid BC
(legalaid.bc.ca), Access Pro Bono (accessprobono.ca), and Family Justice
Centres offer free help, and many lawyers review single documents or
coach single hearings at unbundled rates. You remain responsible for
everything you file and say in court, and you should check the court's
current practice directions about disclosing AI-prepared materials.

**Jurisdiction**: BC family law only. It will mislead you about other
provinces and countries.

## Install

The repository is a Claude Code plugin and a skills package; either
command installs it from the git repo:

```bash
# as a Claude Code plugin
claude plugin install [owner]/bc-family-law-skill
```

```bash
# via the skills CLI (Claude Code, OpenCode, Cursor, and others)
npx skills add [owner]/bc-family-law-skill
```

Or install by hand: clone the repository and copy (or symlink)
`skills/bc-family-law` into your agent's skills directory — e.g.
`~/.claude/skills/bc-family-law` for Claude Code, or
`~/.config/opencode/skills/bc-family-law` for OpenCode.

Then invoke the skill (in Claude Code, `/bc-family-law`, or just ask a BC
family law question). To start a case project, create an empty folder, open
a coding agent there, and ask to set up a case project.

**Privacy note**: a case project will contain the most sensitive
information your family has. Keep it in a *private* repository, on
hardware you control. Review your AI provider's data handling terms
before putting evidence into any AI tool.

## Layout

The skill is a self-contained folder; the rest of the repository is
packaging, docs, and dev tooling.

```
skills/bc-family-law/     # the skill (this is what gets installed)
  SKILL.md                # entry point and workflow
  references/
    legal-sources.md      # provenance and currency of the legal texts
    evidence-standards.md # citation and accuracy discipline
    case-law.md           # authority verification workflow
    evidence-strategy.md  # what to lead, what to leave out
    trial-preparation.md  # trial book, testimony, cross, closing
    post-judgment.md      # orders, costs, appeals, variation, enforcement
    case-project-guide.md # project structure and lifecycle
    document-handling.md  # evidence extraction mechanics
    party-assessment.md   # intake assessment
    resolution-approaches.md # negotiation → mediation → court
    forms-guide.md        # form number → requiring rules (generated)
    generated/            # downloaded legal texts, one subfolder per source
      fla/  da/  csg/  pcfr/  scfr/  ssag/
  templates/
    case-project/         # scaffold incl. AGENTS.md and CASE.md dashboard
    trial-book/           # two-part LaTeX trial book
    book-of-authorities/  # LaTeX book of authorities
  scripts/
    regen_fla.py ...      # one regeneration script per legal source —
    regen_pcfr.py         #   fetches the current consolidation from the
    regen_scfr.py         #   BC Laws / Justice Laws XML APIs, checks for
    regen_da.py           #   amendments (the git diff IS the amendment
    regen_csg.py          #   report), and rebuilds the references
    bclaws_regen.py       # shared machinery (BC CiviX XML)
    justicelaws_regen.py  # shared machinery (federal LIMS XML)
    build_forms_index.py  # regenerates forms-guide.md from the rule texts
    check_freshness.py    # runs every regen script in check mode (CI uses it)
.claude-plugin/plugin.json # Claude Code plugin manifest
evals/                    # test prompts for skill development
tests/                    # regen-pipeline unit tests
```

## Licensing

- **Original content** (`skills/bc-family-law/SKILL.md`, practice guides,
  templates, scripts): MIT — see `LICENSE`.
- **`skills/bc-family-law/references/generated/fla/`, `pcfr/`, `scfr/`**:
  reproduced from [BC Laws](https://www.bclaws.gov.bc.ca); © King's Printer,
  British Columbia. Not official versions. **Review the King's Printer
  copyright terms (https://www.bclaws.gov.bc.ca/copyright.html) before
  redistributing.**
- **`skills/bc-family-law/references/generated/da/`, `csg/`**: federal
  legislation, reproduced under the Reproduction of Federal Law Order,
  SI/97-5. Not official versions.
- **`skills/bc-family-law/references/generated/ssag/`**: derived from the
  *Spousal Support Advisory Guidelines: The Revised User's Guide* (Rogerson
  & Thompson, April 2016), a Department of Justice Canada publication —
  advisory, not legislation. **Confirm reproduction terms before
  redistributing.**

Refresh instructions for all legal texts:
`skills/bc-family-law/references/legal-sources.md`.
