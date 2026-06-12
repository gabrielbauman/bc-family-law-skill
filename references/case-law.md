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

If a case you need is not in `authorities/`, give the user the CanLII URL
and ask them to fetch it (or fetch it yourself if you have web access and
the user agrees). Until the text is in the folder, the case may be
*discussed as a lead* ("there is a line of cases on X worth obtaining")
but never cited, quoted, or relied on.

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
