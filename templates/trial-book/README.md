# Trial Book Template

A two-part bound PDF for a self-represented family trial, copied from a
structure that survived a real three-day trial:

- **Part 1 — Trial presentation** (for the user): opening statement,
  chronology, direct evidence narrative, cross-examination plans,
  closing argument.
- **Part 2 — Evidence binder** (for the court): tabbed, indexed
  exhibits. Documents only — all commentary stripped.

Read the skill's `references/trial-preparation.md` before filling any
section, and `references/evidence-strategy.md` before adding any
exhibit. Apply `references/evidence-standards.md` on every revision —
the trial book is where citation discipline pays or fails.

## Use

1. Copy this folder into the case project as `output/trial-book/`.
2. Set the case parameters at the top of `preamble.tex`.
3. Fill the Part 1 skeletons; add a `tab-X.tex` per exhibit group and
   list each exhibit in `part2-exhibits/exhibits.tex`'s index.
4. Build: `latexmk -pdf main.tex` (or `pdflatex main.tex` twice, for
   working cross-references). Requires a TeX distribution (MacTeX /
   TeX Live); if none is installed, Overleaf compiles this project
   as-is.
5. Print copies: judge, other party, witness stand, yourself. Tab the
   physical binders to match the index.

## Conventions

- `\para` numbers paragraphs court-style; `\resetpara` restarts per
  section. Numbered paragraphs let everyone say "paragraph 14" instead
  of "the part about the apartment".
- `\tabref{B-2}` produces a clickable "Tab B-2" — use it everywhere
  Part 1 relies on an exhibit, so each claim is one click from its
  proof.
- `\exhibitheader{tab}{title}{source}{date}` renders the standard
  exhibit header: source and date only, by design. Keep titles neutral
  ("Messages re rent, August 2017", not "Proof she broke her promise").
- Exhibit source files (PDFs, images) live in
  `part2-exhibits/exhibit-files/` and are pulled in with
  `\includepdf` — keep the originals untouched in `evidence/`.
