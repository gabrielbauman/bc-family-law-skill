# AGENTS.md

Guidance for agents working in this repository. The skill itself lives in
`skills/bc-family-law/`; the rest of the repository is packaging, docs, and
dev tooling around it.

## Generated vs. hand-written

- `skills/bc-family-law/references/generated/` is downstream output. Never
  hand-edit it; it is rendered by `skills/bc-family-law/scripts/regen_*.py`
  from the BC Laws / Justice Laws XML APIs.
- `skills/bc-family-law/SKILL.md`, `skills/bc-family-law/references/*.md`
  and `references/examples/` (outside `generated/`),
  `skills/bc-family-law/templates/`, and
  `skills/bc-family-law/scripts/` are hand-maintained, as are the repo-level
  `evals/` and `tests/`. The exception is `skills/bc-family-law/references/forms-guide.md`,
  which `skills/bc-family-law/scripts/build_forms_index.py` generates.

## Regenerating the legal texts

Each source has a script: `regen_fla.py`, `regen_pcfr.py`, `regen_scfr.py`,
`regen_da.py`, `regen_csg.py` (under `skills/bc-family-law/scripts/`). The
SSAG has no script (static 2016 text).

- Default is **check mode**: fetch the current consolidation, diff it
  against `skills/bc-family-law/references/generated/`, exit non-zero on drift.
- `--write` applies the refresh. Then review `git diff` (the diff is the
  amendment report), rerun `skills/bc-family-law/scripts/build_forms_index.py`,
  and update the snapshot date in
  `skills/bc-family-law/references/legal-sources.md`.
- `python3 skills/bc-family-law/scripts/check_freshness.py` checks all five
  sources at once; a GitHub Action (`.github/workflows/check-freshness.yml`)
  runs it weekly.

## Tests

    python3 -m unittest discover -s tests

The tests pin the regen pipeline's filename/slug helpers and its renderers
(cross-reference folding, blank-line rhythm, tables, rules style, federal
rendering), plus a golden test that renders a real BC Laws part and compares
it to the shipped corpus. Extend them whenever `bclaws_regen.py` or
`justicelaws_regen.py` (under `skills/bc-family-law/scripts/`) change.

## Evals

    python3 evals/run.py list
    python3 evals/run.py run 4 --command "claude -p -"

The behavioral evals in `evals/evals.json` are graded by `evals/run.py`: a
deterministic grader for the filesystem/git assertions, plus an optional LLM
judge for the semantic ones (`--judge-cmd`, or `ANTHROPIC_API_KEY`). Grading
is offline except for the judge.

Two fixture notes worth knowing before editing an eval:

- **Eval 4's dates are deliberately in the past.** The order fixture is
  dated 10 March 2026 and sets 9 April and 30 June 2026, so the eval
  exercises the missed-deadline path (`references/missed-deadlines.md`)
  rather than ordinary intake. If you ever move those dates forward, the
  eval quietly stops testing what it is for.
- **Eval 5 turns on PCFR Appendix 1.** Vancouver is not an early
  resolution registry, so the answer is a Form 3 filed directly — which
  is the opposite of what a model answering from memory tends to say, and
  is only derivable from the reproduced appendix.

A deterministic checker must be written against what the skill actually
ships, not against invented input: two of them failed correct runs
because one counted the scaffold's own `inbox/README.md` as unswept
material and the other read boilerplate in the generated
`research/index.md` as if it were an extraction.

## Conventions

- Commits are scoped (`area: summary`); one self-contained change each.
- A change under `skills/bc-family-law/references/generated/` should
  accompany a script change or a documented refresh, with the reason in the
  commit body.
- The reproduced legal texts carry third-party terms (see the Licensing
  section of `README.md` and `skills/bc-family-law/references/legal-sources.md`);
  only original content is MIT-licensed. Don't move reproduced text into
  MIT files.