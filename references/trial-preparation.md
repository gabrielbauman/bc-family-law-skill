# Trial Preparation for the Self-Represented Litigant

Everything in this guide generalizes counsel's coaching from a real
three-day BC Provincial Court family trial run by a self-represented
party. The structural rules (order of proceedings, the facts/argument
boundary, *Browne v. Dunn*, hearsay) are standard litigation practice —
but they are exactly the things self-represented litigants don't know
they don't know, and each shaped the outcome.

## Contents

- [Back-planning from the trial date](#back-planning-from-the-trial-date)
- [The trial book](#the-trial-book)
- [Order of proceedings](#order-of-proceedings)
- [Opening statement: preview, don't argue](#opening-statement)
- [Direct evidence: facts only, chronologically](#direct-evidence)
- [The evidence binder](#the-evidence-binder)
- [Argue the legal test element by element](#argue-the-legal-test-element-by-element)
- [Cross-examination](#cross-examination)
- [Hearsay](#hearsay)
- [Your own witnesses](#your-own-witnesses)
- [Closing argument](#closing-argument)
- [Book of authorities](#book-of-authorities)
- [Adjournments](#adjournments)
- [Courtroom practicalities](#courtroom-practicalities)

## Back-planning from the trial date

The moment trial dates are set, build the calendar backwards and record
it in CASE.md: the trial-preparation/pre-trial conference (in Provincial
Court typically ~45 days before trial — confirm against the scheduling
order), any ordered exchange of trial materials and witness lists,
disclosure updates (financial statements may need refreshing), and
service deadlines. Trial preparation expands to fill whatever time
exists; the trial book alone took weeks of iteration in the source case.
Start the moment dates are set, not when the conference is looming.

## The trial book

The single most valuable artifact a self-represented litigant can build
(template: `templates/trial-book/`). One bound PDF in two parts:

- **Part 1 — Trial presentation**: opening statement, chronology/timeline,
  direct evidence narrative, closing argument, cross-examination plans.
  This part is *for the user* — their script and safety net under stress.
- **Part 2 — Evidence binder**: the exhibits, tabbed and indexed. This
  part is *for the court* — copies for the judge, the other party, the
  witness stand, and the user.

Building it forces every preparation decision early: what the story is,
which exhibits prove it, what each witness must be asked. Iterate it in
the case project's `output/` folder under version control, and apply the
review standards in `evidence-standards.md` on every revision.

## Order of proceedings

A family trial generally runs:

1. Opening statements
2. The claimant's evidence (direct testimony, then cross-examination)
3. The responding party's evidence (direct, then cross)
4. Closing arguments

**Who goes first follows the burden of proof** — the party who must prove
entitlement presents first. If the user is responding, consider asking
the judge to permit a brief responding opening immediately after the
claimant's opening, so the court hears the shape of the dispute from
both sides before any evidence. Judges often allow it; it costs nothing
to ask.

## Opening statement

The opening *outlines*; it does not argue. Tell the judge who you are,
what is and is not in dispute, what the evidence will show, and what
orders you seek. Two pages is plenty. Arguments, authorities, and
adjectives belong in closing. A judge hearing argument in an opening
learns only that the speaker doesn't know the difference.

## Direct evidence

Direct evidence is the user telling their story, under oath, in
chronological order. Counsel's rules from the source case:

- **Chronology is the structure.** Start at the beginning, move through
  time, refer to the evidence binder by tab as you go ("Tab B-2 is the
  message I sent that night").
- **Tell it, don't read it.** Some judges allow reading a prepared
  statement, but testimony read from a script is visibly less credible.
  Prepare the narrative in writing (trial book Part 1), then deliver it
  from memory with notes as a safety net.
- **Facts only — no argument, no conclusions.** What you saw, did, said,
  and experienced; what the documents show. What it all *means* is
  closing argument. Arguing during testimony invites objections and
  signals unreliability.
- **Perceptions are admissible when framed as perceptions.** "I
  understood the relationship to be over" (your state of mind — fine).
  "The relationship was over" (a conclusion — save it for closing).

The reframing table counsel applied, generalized:

| Don't testify | Testify instead |
|---------------|-----------------|
| "That was a lie" | "She told me X; the document at Tab C says Y" |
| "He was pretending to look for work" | "He applied for positions when I asked" |
| "I was forced into the provider role" | "After she lost her job, I paid the household expenses" |
| "She did the bare minimum" | (state the specific facts, or omit) |
| "This proves she planned to leave" | (facts now; the conclusion belongs in closing) |

The test for every sentence of planned testimony: *observed fact or
document → keep; conclusion from facts → reframe as perception, move to
closing, or delete.*

## The evidence binder

- **Documents only — no commentary.** Descriptions, summaries, "what this
  shows" notes, and relevance explanations are argument; in the binder
  they draw objections and look like coaching. Each exhibit carries only
  source attribution, date, and verbatim content. In the source case,
  counsel ordered all commentary stripped late in preparation — build it
  clean from the start.
- **Tabs and an index.** Letter or letter-number tabs (A, B-1, B-2...),
  a front index listing every tab, pages numbered within tabs.
- **Complete excerpts.** Chat conversations appear as full sequences per
  `evidence-standards.md` — the other side has the same export.
- **Copies**: court + other party + witness + yourself.
- Apply `evidence-strategy.md` to every tab: each exhibit earns its place
  by proving an element someone must prove, and is screened for what it
  gives the other side, for settlement privilege, and for sympathy.

## Argue the legal test element by element

Find the controlling legal test for each issue and structure *everything*
— evidence, cross, closing — around its elements. Courts decide by
walking tests; submissions organized any other way force the judge to do
the mapping.

Worked example: whether a relationship was "marriage-like" (FLA s. 3) is
assessed holistically using the *Molodowich v. Penttinen* factors as
adopted in BC (e.g. *Austin v. Goerz*, 2007 BCCA 586): shelter and
sleeping arrangements; sexual and personal behaviour; division of
household services; social presentation as a couple; economic
interdependence; conduct toward children; how the community perceived
them. No single factor decides — which means preparation addresses every
factor, including the unhelpful ones: for each, what the evidence shows,
which tab proves it, what the other side will say, and the response.
A factor ignored is a factor conceded.

(Verify any authority against full text in `authorities/` before citing —
`case-law.md`.)

## Cross-examination

Cross-examination is not an interview; it is controlled extraction of
admissions.

- **Only ask questions you know the answer to**, established by a
  document or prior statement you can produce.
- **Closed questions, yes/no answers.** Never "why", "how", or "tell me
  about" — open questions hand the witness the floor to say something
  unexpected and damaging.
- **Lead with the document**: "You said X. I'm showing you Tab D-3. It
  says Y. Correct?"

**The rule in *Browne v. Dunn*** (standard practice; cite only per
`case-law.md` if relied on in argument): if you intend to contradict a
witness's evidence in argument, you must put your version to them in
cross-examination so they can respond. It cuts both ways:

- Contradictory evidence never put to the witness may get little weight —
  plan cross from the closing backwards: every contradiction you want to
  argue gets put to the witness.
- Evidence you *don't* challenge in cross may be treated as accepted —
  know which of their assertions you dispute, and challenge each.
- Limits: not every point needs confronting. Documents with dates speak
  for themselves; put to the witness the topics where you need their
  admission or where fairness requires they get to respond.

## Hearsay

An out-of-court statement offered to prove the truth of what it says is
hearsay and presumptively inadmissible — letters or statements from
friends and family who are not present to be cross-examined, "my mother
saw...", a neighbour's written note. If the other party tenders evidence
from an absent person, object: the author must attend and be available
for cross-examination. Symmetrically: if the user needs what a third
party knows, that person must come testify — a support letter is not a
witness. (Documents the parties themselves wrote to each other are
generally fine — they're party statements, not third-party hearsay.)

## Your own witnesses

A witness earns their seat by having personally observed something
relevant that the user cannot prove alone. For each: what facts they
saw, which issue those facts go to, and what cross-examination will ask
them. Prepare witnesses by reviewing what they remember — never by
telling them what to say. Coached testimony collapses under cross.

## Closing argument

Closing is where argument finally lives: connect the evidence the judge
actually heard to the elements of the legal test, with authorities.

- Walk the test element by element; for each, the supporting evidence by
  tab and the inference you ask the court to draw.
- Address the other side's evidence directly — explain why it falls
  short on their burden, using their own exhibits where possible.
- Cite authorities per `case-law.md` (verified, pinpointed), and have the
  book of authorities ready.
- Credibility submissions tie to specifics: contradictions put to the
  witness in cross (per *Browne v. Dunn*), not general character attacks.
- Write it before trial, leave gaps for what actually happens, and
  update it each evening of trial — the source case revised closing
  after day two based on admissions obtained in cross.

## Book of authorities

A bound volume of the full text of every case cited in closing, tabbed,
with a front index (template: `templates/book-of-authorities/`). Copies
for the judge and the other party. Every case in it must be in
`authorities/` and every pinpoint verified. Bring it even if the other
side brings nothing — handing the judge the authority opened to the
paragraph is self-represented advocacy at its most credible.

## Adjournments

If trial dates become impossible, act *immediately* — adjournments get
harder as trial approaches. In Provincial Court, PCFR Rule 114 governs
(see `pcfr_rule_114_adjourning_trial_date.md`): without consent apply
more than 45 days out; with consent more than 7 days out; inside that,
only "special circumstances," applied for as soon as practicable. Hard
lessons from the source case, where a near-trial application was
dismissed: a bare assertion of difficult circumstances is not enough —
the application and supporting affidavit must give the court *specific,
detailed* reasons with evidence attached. A denial on the papers is not
necessarily final (the trial judge can be asked on day one), but plan as
if the trial proceeds.

## Courtroom practicalities

- Address a Provincial Court judge as "Your Honour"; in the BC Supreme
  Court, address the judge as "Justice [name]" (check the court's current
  guidance for self-represented litigants before your first appearance).
- Stand to speak and when the judge enters or leaves. Speak to the judge,
  not to the other party — even (especially) during disagreements.
- Consider a one-page neutral chronology of key dates as a handout for
  the judge — facts and dates only, no argument, every date sourced. In
  the source case the judge used it throughout. Trim anything the
  evidence doesn't prove.
- Bring: trial book copies, book of authorities, filed pleadings, pens
  and a notepad for tracking testimony (you will cross-examine on what
  is said), and water.
- Plan each trial day's evening: review the day's testimony against the
  cross and closing plans, and adjust.
