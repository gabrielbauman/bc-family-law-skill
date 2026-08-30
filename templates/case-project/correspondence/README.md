# Correspondence

Final, sent communications and the formal offers that carry costs
consequences — the things that are *not* on the court record but still
have to be preserved and provable. This folder fills the gap between
`output/` (drafts that may be abandoned) and `filings/` (what the court
has actually received).

What lives here:

- **Sent letters and emails** in their final, as-sent form — to the
  other party, their lawyer, the registry, third parties. Once sent, a
  letter is a fact with a date, not a draft; keep the version that
  actually went out.
- **Formal offers to settle** (SCFR Rule 11-1; PCFR settlement
  offers) and any "without prejudice" / Calderbank offers. These are
  **served but deliberately not filed** until costs are argued after
  judgment — a judge should not see an offer before deciding the case —
  so they cannot live in `filings/`, yet they are exactly what wins or
  defeats a costs award. Keep each offer, its service proof, and its
  expiry.

What does *not* live here:

- Drafts being worked on → `output/`.
- Letters and emails *received* as evidence → `evidence/` (they are
  primary source material; an admission in the other side's email is
  evidence like any other).
- Anything actually filed with the court → `filings/`.

## Treat as a record, like filings/

Once something is sent, it is immutable: do not edit the as-sent
version — the project's PreToolUse and pre-commit hooks guard this folder
the same as `evidence/` and `filings/`. If a follow-up is needed, write a
new dated item. Cite
correspondence by filename in CASE.md; a settlement offer with costs
significance also gets a line in CASE.md's procedural history.

## Naming

Date, direction, and subject:
`2025-04-12_to-opposing-counsel_disclosure-demand.pdf`,
`2025-09-01_offer-to-settle_parenting-and-support.pdf`.

## Privacy

This folder can contain "without prejudice" material and settlement
positions. Like `strategy/`, none of it is quoted into filings or
open correspondence except an offer formally put before the court on
the costs question after judgment.