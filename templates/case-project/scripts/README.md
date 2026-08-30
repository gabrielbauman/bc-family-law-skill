# Scripts

Reproducible analysis over the case file: a script that reads a chat
export and prints every message mentioning rent, a script that totals
the income figures across paystubs. Scripts make extractions auditable —
anyone can rerun one and get the same result, which is exactly what a
court wants to hear about how a number was reached.

Two rules:

- **Scripts read; they never write evidence.** A script may read
  `evidence/` and `filings/` and print to the terminal or write into
  `research/` or `output/`. It must never modify a file under
  `evidence/` or `filings/` — those are immutable (the project's git
  pre-commit hook enforces this).
- **Record the command.** When a script produces an extraction that
  lands in `research/`, put the exact command in that research file's
  `source:` frontmatter, so the extraction can be reproduced and cited.

## Included

- `build_research_index.py` — regenerates the registry table in
  `research/index.md` from each research file's frontmatter. Run it
  after adding or removing a research document.
