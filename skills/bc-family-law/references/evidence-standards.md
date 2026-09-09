# Evidence and Accuracy Standards

Every rule in this file traces to a real mistake that had to be found and
fixed before it reached a courtroom. In family litigation the other party
and the judge are actively testing your documents for errors. One wrong
date, one misattributed quote, one overstated claim — discovered once —
taints every other statement the litigant makes. Credibility is the
self-represented litigant's scarcest asset.

## Contents

- [The three kinds of statements](#the-three-kinds-of-statements)
- [Citation requirements by source type](#citation-requirements-by-source-type)
- [Quoting conversations: complete sequences only](#quoting-conversations-complete-sequences-only)
- [Red flags: catch yourself before the other side does](#red-flags)
- [Applying the standards by document type](#applying-the-standards-by-document-type)
- [The pre-commit review](#the-pre-commit-review)

## The three kinds of statements

Everything written in a case is one of three things. Confusing them is the
root of most accuracy failures.

**1. Documented fact** — supported by a specific primary source you can
point to: a message ID, an email file, a page of a filing, a pay stub.
State it plainly, and cite it.

> Ms. A started employment at [employer] in July 2024 (Financial
> Statement sworn 2025-03-14, Part 2; pay stub `evidence/paystubs/...`).

**2. Inference** — a conclusion drawn from documented facts. Inferences are
valuable; cases are argued on them. But they are only safe when labelled,
because a labelled inference invites the reader to check the reasoning,
while a disguised one reads as a false claim of fact once questioned.
Signal with: "This suggests...", "The evidence is consistent with...",
"Based on [source], it appears...".

> Browser history shows apartment searches beginning seven months before
> the move-out date. This suggests the departure was planned, not sudden.

**3. Party testimony** — what the user tells you happened. It matters — it
will become sworn evidence — but until corroborated by a document it is one
person's account, and the other party may swear the opposite. Label it:
"Per [user]...", "[User] states that...". When producing analysis, note
explicitly which claims rest on testimony alone, so the user knows where
their case depends on being believed.

A useful test for any sentence you write: *if opposing counsel asked "how
do you know that?", what would the answer be?* A document → fact (cite it).
Reasoning → inference (label it). "The user told me" → testimony (label it).

## Citation requirements by source type

Citations must let a reader find the exact source in seconds, because that
is what a judge or the other party will try to do.

| Source | Cite with | Example |
|--------|-----------|---------|
| Chat message | Message ID + full timestamp + sender | ID 5003, 2021-03-02T18:16:10, [sender] |
| Email | Full filename incl. date/time/parties | `2024-05-04_1352_A_to_B_Practical_matters.eml` |
| Letter / document | Filename + date (+ page for PDFs) | `letter_2018-12-29.txt` |
| Court filing | Document name + filing date + paragraph/page | Reply (Form 6) filed 2025-03-14, Sched. 14 |
| Financial record | Document + period + line | T1 2023, line 23600 |
| Screenshot | Filename + what it captures + capture date | `browser-history-2023-10-04.png` |
| Case law | Style of cause + neutral citation + paragraph | *Austin v. Goerz*, 2007 BCCA 586 at para. 58 |

Dates and times: use unambiguous formats (`2024-05-01`,
`2021-03-02T18:16:10`). If a date is approximate or inferred, mark it:
"~July 2024 (inferred from pay stub year-to-date amounts)". An inferred
date presented as exact is an error waiting to be exposed.

## Quoting conversations: complete sequences only

Chat logs are the richest and most dangerous evidence source. The
temptation is to quote the helpful messages and skip the rest. Resist it —
selective quoting gets discovered (the other side has the same chat
history), and "you left out the next message where you apologized" is
devastating in cross-examination.

When excerpting a conversation:

1. **Every message carries its ID and full timestamp.** IDs make quotes
   verifiable against the export; timestamps establish sequence and gaps.
2. **No dropped messages within a quoted block.** If you quote IDs
   12345–12350, all six messages appear — including the ones that don't
   help.
3. **No ellipsis ("...") to skip content.** If a conversation is too long,
   split it into clearly labelled separate blocks with the gap stated
   ("[no messages between these blocks on this topic]"), never an elided
   single block.

4. **Start the block where the conversation starts, not where the
   keyword hits.** The rule above says nothing may be dropped inside a
   block; this one says where a block begins and ends. A keyword search
   finds the message that mentions rent — it does not find the two
   messages before it that establish what the parties were talking
   about, or the reply afterwards that says "ok" and contains no keyword.
   Begin at the start of the conversational turn or sitting in which the
   topic arises, and end where it is dropped. The error runs both ways:
   a block that starts at the keyword reads as cherry-picked the moment
   the other side produces the same log, and a block that swallows the
   whole day dumps private material into a document the other party and
   the court will read. When the boundary is genuinely arguable, quote
   the wider range and say in the extraction why it was drawn there.

`examples/research-extraction.md` shows these rules applied to a real
two-block extract, including the gap statement and a note on why
keyword-free replies were kept.
4. **Reproduce text exactly** — typos, slang, and all. Cleaning up quotes
   is paraphrasing inside quotation marks.

Format for chat excerpts:

| ID | Timestamp | Sender | Message |
|----|-----------|--------|---------|
| 12345 | 2021-03-02T18:16:10 | [party A] | exact text |
| 12346 | 2019-07-10T05:16:58 | [party B] | exact text |

In the source case, early extracts made with ellipses and missing IDs all
had to be redone months later under deadline pressure. Extract it right
the first time.

## Red flags

Catch these in your own drafts before the other side does:

- A date, time, or amount with no source behind it.
- A characterization of someone's intent or mental state ("she pretended
  to...", "he never intended to...") — you cannot document a mind. State
  the observable conduct instead.
- A gap filled with something plausible. Plausible is not sourced.
- "Always" / "never" claims — one counterexample destroys them. "I am not
  aware of any occasion when..." survives.
- Overstated evidence: if a message *suggests* something, do not write
  that it *proves* it.
- One interpretation presented as the only one, where the facts honestly
  admit others. Address the alternative; pretending it doesn't exist just
  hands it to the other side.
- Mathematical claims you haven't recomputed (totals, durations,
  "X months between A and B"). Arithmetic errors are the easiest
  credibility hits to avoid.
- **Calendar claims computed from memory.** Which weekday a date fell
  on, whether it was a holiday, whether two dates are the same week —
  these come up constantly in family matters ("he said he'd send it
  Friday", "that was my parenting weekend") and a model's recall of
  them is unreliable. Compute the day of week rather than asserting it,
  and check BC statutory holidays against a source; the rules
  themselves turn on holidays in short time periods (SCFR Rule 21-2(1)
  excludes them from periods under 7 days).

## Applying the standards by document type

- **Timelines** — every event cites its source; approximate dates marked;
  testimony-based events attributed ("per [user]").
- **Research/analysis documents** — separate what the evidence shows, what
  testimony claims, and what may be inferred. Analysis is where inference
  belongs — labelled.
- **Affidavits and testimony** — facts within the deponent's own knowledge.
  Perceptions framed as perceptions ("I understood...", "It appeared to
  me..."). No argument — see `trial-preparation.md` for the facts-vs-
  argument discipline.
- **Pleadings and applications** — only claims the evidence can support;
  the other side will test every assertion.
- **Correspondence with the other party** — documented facts only, no
  characterizations; assume every email will be an exhibit someday. Keep
  settlement discussions out of evidence-bound documents (see
  `evidence-strategy.md` on settlement privilege).

## The pre-commit review

In a git-tracked case project, review every change against these standards
before committing:

1. Each factual claim cited to a primary source — or reworded as
   inference/testimony.
2. No assertions dressed as fact that are actually interpretation.
3. Quotes verbatim against the source; chat blocks complete with IDs.
4. Characterizations of events or conduct supported by the cited evidence.
5. No silently assumed details.

Fix problems before committing, not after. The git history of a case
project is also its audit trail: a clean history of well-cited changes is
how the user reconstructs, months later, why every statement in their
trial materials is safe to swear to.
