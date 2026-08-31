# AGENTS.md

Guidance for agents working in this repository — a skill that gives
self-represented litigants in British Columbia a legal-information and
document-preparation assistant backed by reproduced statutes, court rules,
and practice guides.

## Generated vs. hand-written

- `references/generated/` is downstream output. Never hand-edit it; it is
  rendered by `scripts/regen_*.py` from the BC Laws / Justice Laws XML APIs.
- `SKILL.md`, `references/*.md` (outside `generated/`), `templates/`,
  `scripts/`, `evals/`, and `tests/` are hand-maintained. The exception is
  `references/forms-guide.md`, which `scripts/build_forms_index.py` generates.

## Regenerating the legal texts

Each source has a script: `regen_fla.py`, `regen_pcfr.py`, `regen_scfr.py`,
`regen_da.py`, `regen_csg.py`. The SSAG has no script (static 2016 text).

- Default is **check mode**: fetch the current consolidation, diff it
  against `references/generated/`, exit non-zero on drift.
- `--write` applies the refresh. Then review `git diff` (the diff is the
  amendment report), rerun `scripts/build_forms_index.py`, and update the
  snapshot date in `references/legal-sources.md`.
- `python3 scripts/check_freshness.py` checks all five sources at once; a
  GitHub Action (`.github/workflows/check-freshness.yml`) runs it weekly.

## Tests

    python3 -m unittest discover -s tests

The tests pin the regen pipeline's filename/slug helpers and its renderers
(cross-reference folding, blank-line rhythm, tables, rules style, federal
rendering). Extend them whenever `scripts/bclaws_regen.py` or
`scripts/justicelaws_regen.py` changes.

## Conventions

- Commits are scoped (`area: summary`); one self-contained change each.
- A change under `references/generated/` should accompany a script change
  or a documented refresh, with the reason in the commit body.
- The reproduced legal texts carry third-party terms (see the Licensing
  section of `README.md` and `references/legal-sources.md`); only original
  content is MIT-licensed. Don't move reproduced text into MIT files.