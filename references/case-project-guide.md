# Case Project Guide

A case project is a git-tracked folder of markdown and source files that
carries a family law matter across sessions: the user never re-explains
their case, every fact stays cited, and the work survives the months (or
years) a contested matter takes. The structure below is the one a real
case converged on between first filing and trial — it replaced a more
elaborate design that didn't survive contact with practice.

## When to offer one

Offer a case project when the matter will involve filings, multiple
sessions, or any volume of evidence. Skip it for one-off procedural
questions, and don't push it on a user who is overwhelmed — the project
serves the user, not the other way around. It can start minimal (CASE.md
plus an `evidence/` folder) and grow folders as the case does.

## Structure

Scaffold from `templates/case-project/`:

```
my-case/
├── .claude/CLAUDE.md   # Working rules for the project (from template)
├── CASE.md             # THE DASHBOARD — read first, every session
├── case-law.md         # Authorities table (once case law accumulates)
├── evidence/           # Primary sources. IMMUTABLE. README handler per source.
├── filings/            # Filed court documents. IMMUTABLE.
├── authorities/        # Full text of every authority cited (see case-law.md guide)
├── research/           # Extractions and analysis, with index.md registry
├── output/             # Drafts in progress — NOT the record, may be abandoned
├── scripts/            # Reproducible analysis scripts
└── strategy/           # Private strategic notes. NEVER evidence, never filed.
```

Why so few satellite files? The original design had a dozen top-level
files (timeline.md, parties.md, children.md, finances.md, positions.md,
court-dates.md...). In practice they fragmented the same information and
went stale independently. CASE.md absorbed them all as sections, and one
dashboard kept current beat ten files that weren't. Split a section out
into its own file only when it outgrows the dashboard — and leave a link
behind.

### CASE.md, the dashboard

CASE.md answers, in one read: status and stage, who the parties are,
what is in dispute, key finances, the procedural history with dates, the
key legal issues with the evidence supporting each side, current
priorities, and next steps with deadlines. The template
(`templates/case-project/CASE.md`) reflects the mature shape. Two
maintenance rules:

- **Update it after every session that changes anything** — new filing,
  new deadline, new evidence, position change. Stamp it with a
  last-updated date.
- **Everything in it obeys `evidence-standards.md`** — facts cite
  sources, inferences are labelled, testimony is attributed. The
  dashboard is the synthesis future sessions trust; an error here
  propagates everywhere.

### The two immutable folders

`evidence/` and `filings/` are source material. Nothing edits them, ever
— extraction happens *from* them into `research/` (see
`document-handling.md`). They change only when the user adds new
material. If a file in them is wrong (bad OCR, mis-named), the user
replaces it; the model never "fixes" evidence.

### strategy/ is private and one-directional

Strategic notes — counsel's guidance, candid assessments of the other
party, theories of the case — live in `strategy/` and inform drafting,
but their content never flows into evidence, filings, correspondence, or
anything the other party or court will see. Treat lawyer guidance in
`strategy/` as controlling for drafting decisions (consult it before
revising trial materials), and treat behavioural assessments as working
hypotheses, not facts. Keep the tone of strategy notes professional: in
BC, documents can become disclosable in ways users don't expect, and a
case file full of venom helps nobody.

### output/ is not the record

Drafts live in `output/` until filed. Never treat an output document as
a source of case facts — drafts contain positions that were abandoned,
numbers that were corrected, and text that was never sworn. When a
document is filed: final version moves to `filings/`, the draft is
deleted or archived, CASE.md is updated. Keep output documents clean —
no AI disclaimers, no TODO notes, no metadata inside the document
itself; track open questions in CASE.md or the commit history instead.

## Git workflow

The project is a git repository. The history is the case's audit trail —
how a fact entered the file, when a position changed, which draft went
to the lawyer.

- **Commit after each meaningful change**, grouped logically — one
  subject per commit.
- **Message format**: `<area>: <what changed>` with a why when not
  obvious (`research: Extract rent discussions from 2019 messages`,
  `trial-book: Remove settlement correspondence from Tab D`).
- **Before every commit, run the pre-commit review** from
  `evidence-standards.md` — it exists because uncommitted-and-reviewed
  beats committed-and-wrong.
- **Remote**: private repository only (see Privacy below). Push after
  committing so the case file survives the laptop.

## Privacy and safety

A case project concentrates the most sensitive information a family owns
— children's health records, finances, intimate correspondence,
allegations. Defaults:

- **Private remotes only.** Never a public repository; prefer a private
  remote under the user's own account with 2FA. Mention this when
  setting up the project — users following tutorials default to public
  GitHub.
- **Children's information**: include what the legal issues require,
  nothing more. Use initials in documents that will circulate beyond
  the court file. If a child has changed name or gender identity, use
  the current name and pronouns in working documents; legal documents
  follow the name on the relevant legal records where required.
- **Third parties** (new partners, employers, relatives) appear only as
  the issues require — and remember anything about them in a filing
  becomes public record.
- **The other party's data**: organizing evidence lawfully in the user's
  possession is legitimate. Accessing the other party's accounts,
  devices, or mail is not — surveillance and interception create legal
  exposure and can poison otherwise-good evidence. If provenance of a
  file seems improper, raise it before using it.
- **Court filings are public.** In both BC courts, family files have
  access restrictions but filed material can be seen by the parties and
  in various circumstances others. Draft every filing as if the
  children will someday read it — judges notice restraint, and so do
  grown children.

## Session pattern

1. Read CASE.md. Check Next Steps and any deadlines against today's
   date — surface anything urgent before the user's actual question.
2. Do the requested work, loading the references the phase requires
   (see SKILL.md's phase table), extracting per `document-handling.md`,
   drafting into `output/`.
3. Update CASE.md and any touched research files; run the pre-commit
   review; commit and push.
