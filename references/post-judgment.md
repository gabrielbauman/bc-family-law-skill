# After Judgment: Orders, Costs, Appeals, and What Comes Next

The case does not end when the judge finishes reading the reasons. This
guide covers the steps that follow — several of which have short
deadlines that start running immediately.

## Oral reasons vs. the entered order

Judgment often arrives as *oral reasons* delivered in court. The
operative document is the formal **order** that gets drawn up, signed,
and entered with the registry afterwards. After reasons are given:

1. Obtain the reasons (transcript or written reasons) for the record.
2. Watch for the draft order; check every operative term against what
   the judge actually said before it is signed. Drafting errors here are
   much easier to fix before entry than after.
3. File the entered order in the case project's `filings/` folder and
   update CASE.md with the outcome and any compliance obligations.

## Costs: the two courts are completely different

**Provincial Court:** the Provincial Court Family Rules contain **no
general costs regime** — there is no rule entitling a successful party
to costs of the proceeding (and no filing fees to recover). Money can
shift only through narrow conduct-based tools (e.g. conduct orders and
enforcement under the FLA, such as ss. 227–230, for non-compliance with
orders or procedural misconduct). Winning, by itself, triggers nothing.
Do not let a user budget on recovering costs in Provincial Court — and
reassure a losing user that ordinary loss does not mean paying the other
side's costs there.

**Supreme Court:** costs follow the event by default — the successful
party is normally entitled to costs under SCFR Rule 16-1 (see
`generated/scfr/rule_16_1_costs.md`). This cuts both ways and belongs in any
realistic risk assessment *before* choosing Supreme Court or pushing a
weak claim to trial there. Pre-trial settlement offers can affect the
costs outcome, which is one reason offers are made formally even when
settlement looks unlikely.

## Appeals

**From Provincial Court:** FLA s. 233 (see
`generated/fla/section_233_appeals_from_provincial_court_orders.md`) — a party may
appeal a Provincial Court FLA order to the Supreme Court, *except interim
orders*. **The limit is 40 days, beginning the day after the order is
made.** The Supreme Court may extend the time on application, but treat
40 days as the deadline. On appeal the court can confirm or set aside
the order, substitute any order the Provincial Court could have made, or
direct a new hearing.

**From Supreme Court:** appeals go to the BC Court of Appeal under the
Court of Appeal Act and its rules (not reproduced in this skill — check
current requirements at https://www.bccourts.ca/court_of_appeal/, noting
that leave is required for some family orders and limitation periods are
short).

Two postures to support:

- **User considering an appeal:** an appeal is not a re-trial. Appellate
  courts defer heavily to trial findings of fact and credibility;
  realistic grounds are errors of law or palpable and overriding errors
  of fact. Diarize the deadline immediately; the merits conversation can
  follow, the deadline cannot.
- **User who won, watching for an appeal:** note the appeal window in
  CASE.md, keep the entire case file and evidence intact until it
  closes, and do not treat the matter as finished until it does.

## Enforcement

If the order requires the other party to pay or do something and they do
not: support orders can be enrolled with the BC Family Maintenance
Agency's enforcement program (https://www.bcfma.ca — free for
recipients), which monitors and collects; other breaches are addressed
through the FLA's enforcement provisions (Part 10, Division 5 — conduct
orders; s. 230 — enforcement powers) in the court that made the order.

## Variation: final is not always forever

Family orders about parenting and support can be varied when
circumstances change materially — FLA s. 47 (parenting arrangements),
s. 152 (child support), s. 167 (spousal support), and s. 215 (changing
orders generally); Divorce Act s. 17 for divorce-based orders. Property division, by contrast, is essentially final once
decided. If the user's situation changes (income, relocation, the
children's needs), a variation application — not an appeal — is usually
the right tool, and deadlines are not the issue; material change is.

## Closing out the case project

When the appeal window has passed and obligations are stable:

- Record the final outcome and entered order in CASE.md (status:
  concluded), with the appeal window noted as expired.
- Keep `evidence/`, `filings/`, and `authorities/` intact — support and
  parenting orders can return to court years later, and the organized
  record is the user's head start.
- Strip or archive `output/` drafts that were never filed, so a future
  reader doesn't mistake them for the record.
