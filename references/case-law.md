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
a sentence why it matters, give the CanLII URL, and ask the user to
download the full text into `authorities/` (offer to fetch it yourself
only if you have web access and the user agrees). Then stop. Until the
text is in the folder, the case may be *discussed as a lead* ("there is
a line of cases on X worth obtaining") but never cited, quoted,
pinpointed, or relied on in any document — no matter how well you think
you know it. Feeling confident about a remembered case is precisely the
failure mode this rule exists to stop.

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

## If a CanLII connection is available

CanLII offers an API (token required) and MCP servers exist for it. If
the session has one connected, use it — it makes the workflow above
faster and safer. As of this writing the API serves metadata and
citation-network data, not decision full text, so it *supplements* the
`authorities/` rule; nothing about the rule changes.

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
