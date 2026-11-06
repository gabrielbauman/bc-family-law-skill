# Case Project Instructions

**Before substantive work: invoke the `bc-family-law` skill, then read
`CASE.md`.** The skill carries the legal references, the practice guides,
and the authoritative, fuller version of everything summarized here
(`references/case-project-guide.md`); CASE.md carries this case. This
file is the standalone working rules, so any agent can run the project
correctly even when the skill is not loaded — when it is, the skill's
guide governs.

This is a BC family law case project. The user is a litigant; documents
produced here may be sworn, filed, and tested in court. Accuracy is not a
style preference — it is the case.

## Project structure

```
root/
├── CASE.md          # Case dashboard — read first, update after changes
├── authorities.md   # Authorities: case → principle → application (created when case law accumulates)
├── inbox/           # User drop zone — swept at session start
├── evidence/        # Primary sources. IMMUTABLE. README handler per source.
├── filings/         # Filed court documents. IMMUTABLE.
├── correspondence/  # Final sent letters/emails + formal offers to settle. Not filed, but the record.
├── authorities/     # Full text of every authority cited anywhere
├── research/        # Extractions and analysis — leads, not sources. See index.md.
├── output/          # Work-in-progress drafts. NOT the record.
├── scripts/         # Reproducible analysis (reads evidence, never writes it)
└── strategy/        # Private strategic notes and counsel's guidance. NEVER evidence.
```

`authorities.md` and `scripts/` are created when the case first needs them.

## Immutability is enforced, not just asked

`evidence/`, `filings/`, and `correspondence/` (once sent) are the record:
extract FROM them into `research/`; never edit, rename, or "fix" them.
Guards back this up, so a stray edit can't reach history unnoticed:

- a **Claude Code PreToolUse hook** (`.claude/settings.json` +
  `.claude/hooks/protect-immutable.py`) blocks edits to existing files there;
- an **OpenCode plugin** (`.opencode/plugins/protect-immutable.js`) does the
  same when the project is opened in OpenCode;
- a **git pre-commit hook** (`.githooks/pre-commit`) blocks committing
  such a change — this one applies to any tool that commits.

The one exception is a genuine, user-confirmed replacement (a better
scan of the same document): make the new file and commit it with
`git commit --no-verify`. `correspondence/` (sent letters and offers to
settle) is guarded the same way.

## Session start: sweep for user changes

This project commits as it works, so `git status` should be clean at
session start. Anything it reports is user activity or an interrupted
session — handle it before substantive work, per the sweep in the
skill's `references/case-project-guide.md`:

- File new material: court documents → `filings/` (**read for deadlines
  immediately, and check each date against today**); sources →
  `evidence/` with a handler; case law → `authorities/`; counsel
  guidance → `strategy/`; sent letters and offers → `correspondence/`.
  Read the destination folder's README before naming the file — each
  states its own convention, and once a file is committed into a record
  folder the guard blocks the rename. Check for duplicates; preserve
  original filenames in the commit message.
- Treat modified case files (CASE.md, research, strategy) as user input
  and reconcile them properly. Ask about modified `evidence/`/`filings/`,
  deletions, and anything that doesn't look case-related.
- Batch questions, record new filings and deadlines in CASE.md, commit
  as `intake: ...`, and report what went where.

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
there, ask the user to obtain it — name the case, tell them to search
canlii.org for it — and stop citing it (you can keep helping with
everything that doesn't depend on it). Never cite from memory, however
confident, and never hand over a CanLII URL you constructed from the
citation pattern: a guessed link is the same failure as a guessed
case. The skill's `scripts/canlii.py resolve` returns the real one.

The same discipline applies to citations **already in** a document you
are asked to edit or review — a draft from another tool or an earlier
session may carry invented pinpoints, and everyone assumes those were
checked. Audit them before touching the argument, and report what you
find rather than silently deleting it.

## Folder rules

- `research/` is **leads, not truth** — verify against primary sources
  before relying; cite primary sources, not research, in case documents.
  Add frontmatter to each research file and rerun
  `scripts/build_research_index.py` so `research/index.md` stays current.
- `output/` is **not the record** — drafts may be outdated or abandoned.
  Never mine output for case facts. When a document is final, it leaves
  `output/`: filed documents → `filings/`, sent letters and offers →
  `correspondence/`; then delete the draft.
- `strategy/` is **private and one-directional**: it informs drafting;
  its content never appears in evidence, filings, or correspondence.
  Consult counsel's guidance there before revising any court-bound
  document, and treat it as controlling.
- Court-bound documents stay **clean**: no AI commentary, no disclaimers,
  no TODO markers inside the documents themselves.

## Git workflow

Commit after each meaningful change; push to the **private** remote.
Message format: `<area>: <what changed>` (+ why when not obvious), e.g.
`research: Extract rent discussions from 2019 messages`.

**Pre-commit review (every commit):** re-read the diff against the
evidence standards above — every fact cited, every inference labelled,
every quote verbatim, no assumed details. Fix problems before committing.

## Reminders

- Deadlines first: when reading CASE.md, check Next Steps against
  today's date and surface anything urgent before the user's question.
  A date that has already passed is a different problem — see the
  skill's `references/missed-deadlines.md`. Never write a calendar
  reminder for a deadline that is gone, and read CASE.md's own
  Last Updated stamp as a signal: months stale usually means nobody has
  been watching the file.
- Check `research/index.md` before extracting — it may already exist.
- Update CASE.md (and its Last Updated stamp) after any change to the
  case's facts, status, or deadlines.
- This project holds intensely private information about real people,
  including children. Keep the remote private; include third-party and
  child details only as the legal issues require (skill:
  `references/case-project-guide.md`, Privacy and safety).