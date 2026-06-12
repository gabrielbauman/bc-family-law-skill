# Case Project Instructions

**Before substantive work: invoke the `bc-family-law` skill, then read
`CASE.md`.** The skill carries the legal references and practice guides;
CASE.md carries this case. Nothing works correctly without both.

This is a BC family law case project. The user is a litigant; documents
produced here may be sworn, filed, and tested in court. Accuracy is not a
style preference — it is the case.

## Project structure

```
root/
├── CASE.md         # Case dashboard — read first, update after changes
├── case-law.md     # Authorities: case → principle → application (verified)
├── inbox/          # User drop zone — empty it at session start
├── evidence/       # Primary sources. DO NOT MODIFY. README handler per source.
├── filings/        # Filed court documents. DO NOT MODIFY.
├── authorities/    # Full text of every authority cited anywhere
├── research/       # Extractions and analysis — hints, not sources. See index.md.
├── output/         # Work-in-progress documents. NOT the record.
├── scripts/        # Reproducible analysis scripts (read evidence, print results)
└── strategy/       # Private strategic notes and counsel's guidance. NEVER evidence.
```

## Session start: sweep for user changes

This project commits everything as it works, so `git status` should be
clean at session start. Anything it reports is user activity or an
interrupted session — handle it before substantive work, per the sweep
in the skill's `references/case-project-guide.md`:

- New files (in `inbox/` or anywhere): identify and file them —
  court documents to `filings/` (**read for deadlines immediately**),
  source material to `evidence/` with a handler, case law to
  `authorities/`, counsel guidance to `strategy/`. Check for
  duplicates; preserve original filenames in the commit message.
- Modified `evidence/` or `filings/` files: immutable — ask whether
  it's a replacement or an accident; never silently revert.
- Modified case files: treat the diff as user input and reconcile it
  properly. Deletions or files that don't seem case-related: ask.
- Batch questions; handle the obvious silently; record new filings and
  deadlines in CASE.md; commit as `intake: ...` and report what went
  where.

## Evidence and accuracy standards

The full standard is the skill's `references/evidence-standards.md` —
read it before extracting evidence or writing anything factual. The
non-negotiable core:

1. **Facts cite primary sources** — specific file, message ID, page, or
   filing. No source → write it as inference or testimony, or not at all.
2. **Inferences are labelled** ("the evidence suggests...") — valuable,
   never disguised as fact.
3. **The user's account is party testimony** — "per [user]" until a
   document corroborates it.
4. **Quotes are verbatim and complete** — no paraphrase inside quotation
   marks; chat excerpts carry message IDs and full timestamps, with no
   dropped messages and no "..." elisions.
5. **Unknown stays unknown** — never fill a gap with something plausible.

**Case law:** never cite an authority unless its full text is in
`authorities/` and the pinpoint paragraph and any quote have been verified
against that text (skill: `references/case-law.md`). If the text is not
there, ask the user to obtain it — name the case, give the CanLII link —
and stop. Never cite from memory, however confident.

## Folder rules

- `evidence/` and `filings/` are **immutable**. Extract from them into
  `research/` (skill: `references/document-handling.md`); never edit,
  rename, or "fix" them.
- `research/` is **leads, not truth** — verify against primary sources
  before relying; cite primary sources, not research, in case documents.
- `output/` is **not the record** — drafts may be outdated or abandoned.
  Never mine output for case facts. When a document is filed, move the
  final to `filings/` and remove the draft.
- `strategy/` is **private and one-directional**: it informs drafting;
  its content never appears in evidence, filings, or correspondence.
  Consult counsel's guidance there before revising any court-bound
  document, and treat it as controlling.
- Court-bound documents stay **clean**: no AI commentary, no disclaimers,
  no TODO markers inside the documents themselves.

## Git workflow

Commit after each meaningful change; push to the private remote. Message
format: `<area>: <what changed>` (+ why when not obvious). Examples:

- `research: Extract rent discussions from 2019 messages`
- `case-law: Add stepparent support authorities`
- `output: Draft reply to support application`

**Pre-commit review (every commit):** re-read the diff against the
evidence standards above — every fact cited, every inference labelled,
every quote verbatim, no assumed details. Fix problems before
committing, not after.

Do not commit changes inside `evidence/` or `filings/` except when the
user adds new source material.

## Reminders

- Deadlines first: when reading CASE.md, check Next Steps against
  today's date and surface anything urgent before the user's question.
- Check `research/index.md` before extracting — it may already exist.
- Update CASE.md (and its Last Updated stamp) after any change to the
  case's facts, status, or deadlines.
- This project holds intensely private information about real people,
  including children. Keep the remote private; include third-party and
  child details only as the legal issues require (skill:
  `references/case-project-guide.md`, Privacy and safety).
