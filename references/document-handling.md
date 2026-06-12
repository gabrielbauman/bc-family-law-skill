# Document Handling: Evidence In, Research Out

The pipeline that keeps a case project trustworthy: primary sources land
in `evidence/` and never change; anything extracted from them lands in
`research/` with full provenance; case documents cite the primary
sources. This file covers the mechanics. The accuracy rules that govern
every extraction are in `evidence-standards.md` — read both before
processing evidence.

## The two kinds of source material

**Single documents** — a court order, a letter, an email, a PDF
statement. If the file is directly readable, it usually needs no
research copy at all: read it and cite it where you need it. Extract
one only when the source can't be read directly (a scanned PDF needing
transcription) — and then the research file is a verbatim
transcription, nothing more.

**Record collections** — a chat export, browser history, transaction
logs, a folder of emails. Queried repeatedly with different filters;
extractions are purpose-built subsets. Collections are where most of a
relationship's documentary evidence lives (the source case turned on a
110,000-message chat export), and where extraction discipline matters
most.

## Handlers: every source gets a README

Each evidence source (file or folder) gets a `README.md` beside it — a
*handler* — written the first time the source is touched, so every later
session queries it the same way instead of rediscovering the format.

For a **single document**, record: what it is, the file format, how to
extract text (e.g. `pdftotext file.pdf -`), and the citation format for
referencing it.

For a **record collection**, record:

- **Summary**: record count, date range, participants/parties.
- **Schema**: the structure, with one representative record pasted in.
- **Query templates**: working commands for the common operations —
  list, filter by date range, filter by sender, keyword search. With
  these in place, any future question ("find every message about rent
  in 2019") starts from a tested command instead of from zero.
- **Citation format**: which field is the stable ID, and the required
  citation form (see `evidence-standards.md`).

Pick the simplest adequate tool and record the exact commands:

| Format | Tool |
|--------|------|
| JSON | `jq` |
| CSV/TSV | `mlr` (miller), `csvtool`, or `jq -Rs` |
| PDF | `pdftotext` (poppler), plus page-targeted extraction for citations |
| Email (.eml) | `cat` is usually fine; name files `YYYY-MM-DD_HHMM_Sender_to_Recipient_Subject.eml` so filenames are citations |
| HTML | `pup`, or Python with BeautifulSoup |
| Images/screenshots | Read directly; name files descriptively with capture dates |

Example handler queries for a Telegram-style JSON export:

```bash
# Messages in a date range
jq '.messages[] | select(.date >= "2019-07-01" and .date <= "2019-07-31")' messages.json

# Keyword search, case-insensitive
jq '.messages[] | select((.text | type == "string") and (.text | test("rent"; "i")))' messages.json

# A specific ID range (for verifying excerpt completeness)
jq '.messages[] | select(.id >= 5001 and .id <= 5014)' messages.json
```

## What earns a research file

A research file is a derivative copy, and derivative copies can drift
out of sync with the truth. Create one only when it adds something a
direct read of the source cannot:

1. **Query extracts from collections** — a filtered, complete-sequence
   view into a corpus too large to re-read (the messages about rent, in
   order, with IDs).
2. **Derived analysis** — tabulations, statistics, timelines assembled
   across many sources, with the script or method recorded.
3. **Transcriptions** — verbatim text of sources that can't be read
   directly.

A research file that merely mirrors a readable document is indirection
with no payoff — it can only go stale. Don't create it; cite the
document.

## Extraction workflow

1. **Check `research/index.md` first** — the extraction may already
   exist. Duplicate extractions drift apart and create contradictory
   versions of the same evidence.
2. **Read the handler**; run the appropriate query.
3. **Save to `research/`** as a markdown file containing:
   - **Purpose** — the question this extraction answers
   - **Source + query** — file and the exact command used (reproducibility
     is the audit trail)
   - **Date of extraction**
   - **The content**, cited per `evidence-standards.md` (message IDs,
     full timestamps, complete sequences, no ellipsis)
   - Any **analysis clearly separated** from the quoted material —
     quotes are evidence; what they suggest is labelled inference
4. **Update `research/index.md`** — one line per document: file, purpose,
   source.

## Research is leads, not truth

Research files summarize and interpret. They go stale as new evidence
arrives, and summaries inherit their author's framing. So:

- When writing case documents (affidavits, trial books, submissions),
  cite `evidence/` and `filings/` directly — never cite a research file
  as the source of a fact.
- When a research file claims something, verify the citation before
  relying on it; if it cites nothing, treat it as a hypothesis.
- When research turns out wrong, fix or delete it and note the
  correction in the commit message — a wrong summary left standing will
  be trusted by a future session.

Authoritativeness, in order: `filings/` (the court record) →
`evidence/` (primary sources) → `authorities/` (case law full text) →
CASE.md (the maintained synthesis) → `research/` (hints) → `output/`
(drafts; may be abandoned) → `strategy/` (private notes, never evidence).

## Scripts for derived analysis

When an analysis needs computation (frequency counts over messages,
income tabulations), put the script in `scripts/`, make it read from
`evidence/` and print its results, and cite the script in the research
file it produced. A judge will never see the script — but the user must
be able to explain exactly how a statistic in their trial book was
computed, and "here is the script and the raw export" is an answer that
survives cross-examination. A number nobody can reproduce is a number
the other side gets to call invented.
