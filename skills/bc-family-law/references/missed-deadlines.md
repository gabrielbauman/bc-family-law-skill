# Missed Deadlines, Missed Appearances, and Dormant Files

Most of this skill assumes a deadline is ahead of you. Often it is not.
A self-represented litigant misses a date because they were overwhelmed,
because the order arrived in a pile of mail they could not face, because
they did not realise a conference was mandatory, or because the case went
quiet for a year while life happened. By the time they ask for help, the
question is no longer "how do I meet this" but "what now".

That moment is where this skill can do the most good and where it most
easily does harm. The harm is cheerfulness: reading an order, spotting a
date, and writing it into Next Steps or a calendar file without checking
it against today. A reminder for a deadline that blew five months ago
tells the user everything is fine when it is not, and it costs them the
weeks in which the situation was still cheap to fix.

## Check every date against today, before anything else

Whenever a date enters the file — from an order, a served document, a
notice, the user's own account — compare it to today's date before doing
anything with it. Three outcomes, and they lead to different work:

- **Future** — the normal path. Record it, surface it, offer the
  calendar file (see `case-project-guide.md`, "Deadlines leave the file").
- **Past, and complied with** — confirm what was filed or attended,
  record it in CASE.md's procedural history, and move on.
- **Past, and possibly not complied with** — stop and work through this
  file before answering whatever the user actually asked. They may not
  know they missed it; a stale CASE.md ("last updated" months ago, next
  steps that were never ticked off) is itself a signal that nobody has
  been watching the file.

Never write an `.ics` for a date that has passed. If every date in a
document is past, say so plainly and explain what that means, rather
than filing the document tidily and reporting success.

## Establish what actually happened before diagnosing

The user is often the only source, they may be embarrassed, and shame
makes for vague answers. Ask directly and without editorial: did you
file it? did you go? did you hear anything after? "I don't know" and "I
think so" are common and honest — record them as testimony, not fact
(`evidence-standards.md`), and check the registry rather than guessing.

The registry is the cheapest source of truth here. A phone call or a
file search tells the user what was filed, what orders exist, and
whether anything was made in their absence. Recommend it before any
strategy: advising someone to apply to set aside an order that was never
made wastes the little energy they have.

## Provincial Court

| Situation | Where to look |
|-----------|---------------|
| Failed to comply with a rule or an order | `generated/pcfr/rule_147_non-compliance_with_rules.md` |
| Missed a court appearance | `generated/pcfr/rule_148_failure_of_party_to_attend_court_appearance.md` |
| A conference went ahead without you | `generated/pcfr/rule_045_family_management_conference_may_proceed.md` |
| An order was made while you were absent | `generated/pcfr/rule_054_orders_made_in_the_absence_of_a_party_judge.md` |
| Asking to change, suspend or cancel such an order | `generated/pcfr/rule_159_judge_may_change_suspend_or_cancel_orders_made_in_absence_of_party.md` |
| Getting back before a judge | `generated/pcfr/rule_156_requesting_conference_or_hearing.md` |
| Restarting a case that has gone quiet | `generated/pcfr/rule_042_intention_to_proceed_family_management_conferences.md` |

Two things are worth telling a frightened user early, because both are
usually true and both are hard to believe from the outside. Non-compliance
with the rules is treated as an *irregularity* unless a judge orders
otherwise (Rule 147(2)) — the default is that it is fixable, not fatal.
And Rule 159 exists precisely because orders get made in people's
absence; the court expects to be asked to revisit them.

That is not a promise the order will be undone. Rule 147(1) also lets a
judge order costs, impose a fine, disregard a filed document, or dismiss
an application. Explain both halves. The honest summary is usually: this
is recoverable, it is more work than it would have been, and the sooner
you move the better it looks.

## Supreme Court

| Situation | Where to look |
|-----------|---------------|
| Extending a time limit — including after it expired | `generated/scfr/rule_21_2_time.md` (Rule 21-2(2)) |
| Extending by consent for pleadings and documents | `generated/scfr/rule_21_2_time.md` (Rule 21-2(3)) |
| No step taken for a year | `generated/scfr/rule_21_2_time.md` (Rule 21-2(4)) — Form F48 notice of intention to proceed, then 28 days |
| Costs exposure from the delay | `generated/scfr/rule_16_1_costs.md`, `post-judgment.md` |

Rule 21-2(2) is the important one and it is easy to miss on a first
read: the court may extend a period "even though the application for the
extension or the order granting the extension is made after the period
of time has expired." An expired deadline is not automatically a closed
door. Consent under Rule 21-2(3) is cheaper still — where the other side
is reasonable, ask them before asking the court.

## Limitation periods are the exception

Everything above is procedural and generally curable. Limitation periods
are not, and they are the one clock where being late can end a claim
outright.

**FLA s. 198(2)** gives a spouse two years to start a proceeding for
property division (Part 5), pension division (Part 6), or *spousal
support* (Part 7). The two years run from the date of divorce or nullity
for married spouses, and **from the date of separation for unmarried
spouses** — which is the trap, because an unmarried person who separates
and asks only about the children may have no idea a clock is running on
everything else. See `generated/fla/section_198_time_limits.md`.

Two qualifications matter in practice, and both are commonly missed:

- **s. 198(5) suspends the clock** while the parties are engaged in
  family dispute resolution with a family dispute resolution
  professional. Someone who spent eight months in mediation may have
  more time than a calendar suggests. Establish the dates.
- **Child support has no such limit.** s. 198(2) does not cover it, and
  s. 198(1) leaves a proceeding startable at any time. Do not let a
  limitation worry stop a parent from pursuing child support.

Raise s. 198 during intake for anyone who separated from an unmarried
partner, whatever they came to ask about, and record the separation date
and the resulting deadline in CASE.md. If the two years have run or are
close, say so immediately and recommend a lawyer — this is exactly the
consequential, hard-to-reverse decision where unbundled advice is worth
the money.

Appeal periods are short and also hard: see `post-judgment.md` and
`generated/fla/section_233_appeals_from_provincial_court_orders.md`.

## Terms that expired on their own

Interim orders often run "until the family management conference" or
"until further order of the court". When the triggering event has passed,
whether the term survives is a live question, not something to assume in
either direction — and the parties may have been operating for months on
an arrangement that no longer has an order behind it. Flag it, quote the
wording of the term, and treat the answer as something to confirm with
the registry or a lawyer rather than something to decide.

## What to write down

A file that has gone off the rails needs its CASE.md to say so honestly,
because the next session will trust whatever it finds there:

- Procedural history records what was ordered and, separately, what is
  known or unknown about compliance. "Form 4 financial statement ordered
  by 2026-04-09; whether it was filed is not established" is a useful
  entry. "Form 4 filed" without a source is a lie the file will repeat.
- Next Steps leads with the recovery step and its own new deadline.
- The commit message says what was discovered, so the history shows when
  the problem surfaced.

Then answer the question the user actually asked. Someone who has just
learned they missed two court dates still needs to know what happens
next, and leaving them with only bad news is its own kind of failure.
