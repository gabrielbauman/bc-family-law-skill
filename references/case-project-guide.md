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
├── inbox/              # User drop zone for anything new — swept at session start
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

### The division of labour: the model maintains the structure

The folder layout, handlers, indexes, and citation discipline are
infrastructure the model maintains — the user should never have to
think about them, and most won't read any of these rules. Their side of
the contract is small, and it should be said out loud when the project
is created:

- *"You never need to file anything yourself. Drop new material —
  court documents, statements, exports, photos of paper — into
  `inbox/`, or honestly anywhere; I'll find it, file it, and tell you
  where it went."*
- *"Don't edit what's already in `evidence/` or `filings/`. If
  something there is wrong, tell me and we'll replace it together."*
- *"Everything is committed to git, so nothing you add or I move can
  be lost."*

Then assume the user will do the wrong thing anyway — rename folders,
drop a filing at the root, edit a research file, paste a scan over an
original — and treat cleaning that up as routine work, not a fault to
correct them over. The sweep below is how.

## Session-start sweep

The model commits after every session, so at session start the working
tree should be clean. **Anything `git status` reports is information:**
material the user dropped, a change they made by hand, or leftovers
from an interrupted session. Run the sweep after reading CASE.md
(its context is what makes new files identifiable) and before the
user's actual request — and run it again mid-session whenever the user
says they've added something.

1. If the project isn't a git repository yet, initialize one and make
   a baseline commit before anything else.
2. Run `git status --porcelain` and classify what it shows:
   - **Untracked files** (in `inbox/` or anywhere): identify each —
     read enough to classify. Court-issued or court-stamped documents →
     `filings/`, and **read them for dates and deadlines immediately**
     (a dropped order or served application often starts a clock the
     user hasn't noticed). Source material → the right `evidence/`
     subfolder, creating the handler README if it's a new source type.
     Case law full text → `authorities/`. Counsel guidance → `strategy/`.
     Drafts → `output/`.
   - **Modified files in `evidence/` or `filings/`**: stop — these are
     immutable. The likely stories are a deliberate replacement (better
     scan) or an accident; ask which before committing or reverting.
     Never silently revert a user's change — it may be the correction.
   - **Modified case files** (CASE.md, research, strategy): read the
     diff as user input — they may have corrected a fact or added
     knowledge. Reconcile it into the file properly (citations,
     labelling) rather than overwriting it.
   - **Deletions**: ask.
3. Before filing, check for duplicates of material already in
   `evidence/` (re-exports are common). When renaming a dropped file to
   the naming conventions, preserve the original filename in the
   handler or commit message — filenames are sometimes provenance.
4. A file that doesn't seem to belong to the case at all may have
   landed there by mistake — ask rather than filing it.
5. Batch the questions (provenance, unclear placement) into one round
   rather than interrogating file-by-file; handle the obvious silently
   and report what went where.
6. Record consequences: new filings go into CASE.md's procedural
   history; new deadlines into Next Steps; new evidence into the
   relevant handler and `research/index.md` if extracted.
7. Commit the intake (`intake: File pay statements and FMC order from
   inbox`), then proceed to the user's request.

Leftovers that look like a *previous session's* unfinished work (a
half-edited draft in `output/`) get reviewed against CASE.md's next
steps and committed with an honest note — not discarded.

## Deadlines leave the file

CASE.md's Next Steps is the project's tickler system, but it only works
when the user opens the project — and missed deadlines are how
self-represented parties lose cases they could have won. Deadlines must
also live where the user lives:

- Every Next Steps item carries the action, the hard date, and the
  source of that date (the order, rule, or notice that set it).
- When a new hard date lands, offer a calendar file: write a minimal
  `.ics` into `output/` for the user to import — one VEVENT per
  deadline, with an alarm far enough ahead to act on (court deadlines
  need lead time for drafting and service; a week's warning beats a
  same-day one). The model writes this by hand; no tooling needed:

  ```text
  BEGIN:VCALENDAR
  VERSION:2.0
  PRODID:-//case-project//EN
  BEGIN:VEVENT
  UID:form4-deadline-20260409@case-project
  DTSTART;VALUE=DATE:20260409
  SUMMARY:COURT DEADLINE: file and serve Form 4 financial statement
  DESCRIPTION:Set by order of 2026-03-10. Needs drafting and service time.
  BEGIN:VALARM
  TRIGGER:-P7D
  ACTION:DISPLAY
  DESCRIPTION:Form 4 due in one week
  END:VALARM
  END:VEVENT
  END:VCALENDAR
  ```

- If a calendar integration is connected, offer to write the dates
  directly instead (with the user's consent). CASE.md remains the
  source of truth either way.

## If integrations are available

Check what tools the session actually has — never assume any. When they
exist, they shorten the project's intake and deadline paths; nothing in
this guide depends on them.

- **Email access**: at the user's explicit direction, the session-start
  sweep can extend to mail — registry notices, served documents,
  scheduling letters — filing attachments like any inbox drop. Scope it
  narrowly: a family-dispute mailbox contains the other party's
  correspondence and possibly privileged lawyer mail. Scan only what
  the user asks you to scan, and treat reading their mail as the
  privilege it is.
- **Calendar access**: write court dates and deadlines directly, with
  consent, in addition to CASE.md.
- **CanLII access** (API token or MCP server): see `case-law.md` —
  existence verification and treatment checks for authorities.
- Standing reminders ("review my case every Monday") belong in the
  user's assistant scheduling facility, not in the project — suggest it
  once for a user juggling deadlines.

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

1. Read CASE.md.
2. Run the session-start sweep (above) — file what the user dropped,
   reconcile what they changed.
3. Check deadlines — CASE.md's Next Steps plus anything new filings
   just introduced — against today's date, and surface anything urgent
   before the user's actual question.
4. Do the requested work, loading the references the phase requires
   (see SKILL.md's phase table), extracting per `document-handling.md`,
   drafting into `output/`.
5. Update CASE.md and any touched research files; run the pre-commit
   review; commit and push.
