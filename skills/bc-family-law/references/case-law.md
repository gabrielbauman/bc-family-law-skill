# Case Law: Finding, Verifying, and Citing Authorities

Language models invent case law. The citations look perfect — plausible
style of cause, real-looking neutral citation, a quote that says exactly
what the argument needs — and they are fabricated. Lawyers have been
sanctioned in Canadian courts for filing AI-invented authorities. A
self-represented litigant who cites a non-existent case, or a real case
that doesn't say what they claim, loses the only thing keeping the judge
listening.

The defence is mechanical, not aspirational: **no authority is cited
anywhere unless its full text sits in the project's `authorities/` folder
and the citation has been checked against that text.**

## The authorities folder

Every case project has an `authorities/` folder holding the complete text
of every authority the case relies on (older projects may name this
folder `precedent/` — treat it the same). Sources:

- **CanLII** (https://www.canlii.org) — free, comprehensive, authoritative
  for Canadian case law. Save as text or PDF named
  `style-of-cause-citation.txt` (e.g. `austin-v-goerz-2007-bcca-586.txt`).
- Authorities received from a lawyer or the other party — file them too.

**When a case you need is not in `authorities/`, asking the user for its
full text is a required step, not a fallback.** Name the case, explain in
a sentence why it matters, point them at CanLII (see "Giving the user a
link" below), and ask them to download the full text into
`authorities/`. If you have web access, offer to fetch it yourself and
do so when the user agrees — a downloaded copy the user can open beats
a homework assignment, and it lands in the folder where the
verification rules can reach it. Either way the case is not cited until
that text exists and has been checked against.

**"Stop" means stop citing, not stop helping.** Until the text is in the
folder the case may be *discussed as a lead* — "there is a line of cases
on whether financial dependence is required, worth obtaining" — and you
can keep working on everything that does not depend on it. What you
cannot do is cite it, quote it, pinpoint a paragraph, or write it into a
document, no matter how well you think you know it. Feeling confident
about a remembered case is precisely the failure mode this rule exists
to stop. Say plainly which part you are declining and why, then carry on
with the rest of the request; a bare refusal helps nobody.

## Verification before every citation

Before a citation appears in any document:

1. **The case exists** — full text present in `authorities/`.
2. **The citation is exact** — style of cause spelling, year, court, and
   neutral citation match the text. (*Austin v. Goerz*, 2007 BCCA 586 —
   not 2008, not BCSC.)
3. **The paragraph number is right** — open the file and confirm the
   pinpoint. Paragraph numbering can differ between sources; verify
   against the copy in `authorities/`, which is the copy the user will hand
   the court.
4. **Quotes are verbatim** — character for character. No paraphrase inside
   quotation marks, no trimming that shifts meaning.
5. **Nested citations check out** — if quoting a passage where Case A
   quotes Case B, verify the passage in A, and ideally obtain B as well;
   if B is not in `authorities/`, attribute the quote through A explicitly
   ("as quoted in...").
6. **The case actually supports the point.** Read enough context to
   confirm the passage isn't qualified, distinguished, or from a dissent.
   A technically-accurate quote used against its meaning is worse than no
   citation.

When asked to "add a case that says X": search for real candidates,
provide CanLII links, and verify before citing. If nothing supports X,
say so — do not soften the standard because the argument needs help.

Naming candidates is the one step that still runs on memory, so treat
the names as leads and label them that way to the user. Where
`canlii.py resolve` or a connected CanLII tool is available, check each
candidate exists before you put it in front of someone — a
misremembered style of cause sends a self-represented litigant hunting
for a case that was never there, and they have no way to tell your
confident wrong answer from a right one.

## What a refusal sounds like

The user asked for something small and is getting a no, so the tone
matters. Name the constraint, do the part you can, and make the next
step concrete:

> I can't add that quote yet. *Austin v. Goerz*, 2007 BCCA 586 isn't in
> your `authorities/` folder, and I won't put a paragraph number or a
> quotation into a document I can't check against the actual decision —
> a citation that turns out to be wrong costs you more in credibility
> than the sentence is worth.
>
> Search canlii.org for "Austin v. Goerz" and save the full text to
> `authorities/austin-v-goerz-2007-bcca-586.txt`, and I'll verify the
> passage and draft the paragraph. One thing worth knowing before you
> do: my recollection is that *Austin* may point the other way on this —
> that financial dependence is not *required* for a marriage-like
> relationship — which would make it a case the other side cites, not
> you. That's exactly why I want to read it before it goes in.
>
> Meanwhile I've tightened the rest of the closing; the argument about
> the joint account doesn't depend on this case.

Not preachy, not apologetic, and it leaves the user with work they can
actually do.

## Giving the user a link

A CanLII deep link looks mechanical —
`canlii.org/en/bc/bcca/doc/2007/2007bcca586/2007bcca586.html` — and it
is tempting to construct one from the neutral citation. Don't. A
constructed URL is a guess dressed as a reference, which is the same
failure this whole file exists to prevent, and a 404 sends the user
away thinking the case does not exist.

Two safe options, in order of preference:

1. **Resolve it.** `<skill>/scripts/canlii.py resolve "2007 BCCA 586"`
   returns the case's canonical title and URL from the CanLII API (see
   below). A resolved URL has also confirmed the citation is real.
2. **Hand them a search.** Give the style of cause and neutral citation
   and tell them to search canlii.org for it — a name they can type
   beats a link that might not resolve.

## Auditing citations already in a document

The rules above cover adding a citation. The other half of the job is
finding the ones already there. A user may arrive with a draft
affidavit, written argument, or trial book prepared with another AI
tool, by a former lawyer, or by themselves months ago — and unverified
citations in an existing document are more dangerous than the ones you
decline to write, because everyone assumes they were checked once.

When you are asked to edit, strengthen, or review any document that
cites authority, audit the citations before touching the argument:

1. List every authority the document cites, with its pinpoints.
2. For each, check `authorities/` for the full text.
3. Verify what is there against the six checks below. Pay particular
   attention to pinpoints and quotes — a fabricated citation often has
   a real case attached to an invented paragraph.
4. Report what you found before rewriting anything. Group them: verified,
   unverifiable (no full text — needs obtaining), and wrong (the case
   does not say this, the paragraph is different, the quote is
   paraphrased).

Do not silently delete a citation that fails. The user may have a reason
for it, and they need to know their document had a problem — especially
if it has already been filed or served, where the question becomes
whether to correct the record.

## If a CanLII connection is available

The skill ships `scripts/canlii.py`, a small CLI over the CanLII API
that does exactly the verification steps below — `resolve` a citation,
list what is `citing` a case, list what it `cited`, browse `recent`
decisions in a court database. It needs an API key
(`CANLII_API_KEY`, free but manually approved via CanLII's feedback
form), so check whether one is set before promising the workflow. An
MCP server for CanLII does the same job if the session has one
connected.

As of this writing the API serves metadata and citation-network data,
not decision full text, so it *supplements* the `authorities/` rule;
nothing about the rule changes.

- **Verify existence first.** Before asking the user to fetch anything,
  confirm the style of cause and neutral citation resolve to a real
  case. This kills fabricated or misremembered citations at the
  cheapest possible point.
- **Check treatment.** For each authority relied on, pull the citator:
  what cites it, and whether a later case overturns, reverses, or
  qualifies it. A verbatim, pinpoint-verified quote from a case that
  has since been overturned is the one error full-text verification
  cannot catch. Surface negative treatment to the user immediately.
- **Find better authority.** The citator also answers "what is the
  leading case on this point" and "is there something more recent" —
  the raw material for the adverse-authority work below.
- **Resolve the canonical URL** to give the user for the full-text
  download.

Without a connection, the rules are identical — existence and treatment
just get verified the slower way: by obtaining the full text and
checking the case's citing references on the CanLII website.

## Citation format

BC courts use the neutral citation system:

- First reference: *Style of Cause*, year COURT number at para. N —
  e.g. *Chartier v. Chartier*, [1999] 1 SCR 242 at para. 39 (pre-2000
  SCC uses the SCR format); *Lee v. Lee*, 2014 BCCA 383 at para. 12.
- Subsequent references: *Lee* at para. 14.
- Pinpoint to paragraphs, not pages — paragraphs are stable across
  sources.

## Building a case-law file

Maintain `case-law.md` (or similar) in the case project root once
authorities accumulate: a table of case → principle → how it applies to
this case's facts, each entry backed by a verified file in `authorities/`.
This becomes the skeleton of written argument and the source list for a
book of authorities (`templates/book-of-authorities/`).

When analyzing how an authority applies, the same fact/inference
discipline from `evidence-standards.md` applies: what the case *held* is
quotable fact; whether this case's facts fall inside that holding is
argument, and belongs in submissions, labelled as the user's position.

## Distinguishing and adverse authority

Expect the other party (or the judge) to raise cases against the user's
position. For each authority relied on, note how the other side might
distinguish it; for known adverse authorities, prepare the distinction in
advance (different statutory test, different facts, qualified by a later
case). Finding the other side's best case before they do is cheap
insurance — and if an authority is squarely against the user and cannot
be distinguished, they need to know that *before* choosing to fight the
point, not in the courtroom.
