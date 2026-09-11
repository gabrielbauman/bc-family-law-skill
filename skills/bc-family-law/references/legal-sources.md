# Legal Sources: Provenance and Currency

The statute, regulation, and rule texts under `generated/` are reproductions.
Law changes; reproductions do not. Read this file before relying on a
reference for anything time-sensitive, and tell the user when currency
matters to their question.

## What is here, and where it came from

| Folder | Source | Citation | Official source |
|--------|--------|----------|-----------------|
| `generated/fla/` | Family Law Act (BC) | SBC 2011, c. 25 | https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/11025_01 |
| `generated/pcfr/` | Provincial Court Family Rules | B.C. Reg. 120/2020 | https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/120_2020 |
| `generated/scfr/` | Supreme Court Family Rules | B.C. Reg. 169/2009 | https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/169_2009_00 |
| `generated/da/` | Divorce Act (Canada) | R.S.C. 1985, c. 3 (2nd Supp.) | https://laws-lois.justice.gc.ca/eng/acts/d-3.4/ |
| `generated/csg/` | Federal Child Support Guidelines | SOR/97-175 | https://laws-lois.justice.gc.ca/eng/regulations/sor-97-175/ |
| `generated/ssag/` | Spousal Support Advisory Guidelines: The Revised User's Guide (April 2016), Rogerson & Thompson | Advisory publication, not legislation | https://www.justice.gc.ca/eng/fl-df/spousal-epoux/ssag-ldfpae.html |

**Snapshot currency**, by suite, because the sources do not all declare
the same thing:

| Suite | Freshness signal |
|-------|------------------|
| `fla/` | Index states BC Laws' "current to" date (**August 25, 2026**) |
| `scfr/` | Index states BC Laws' "current to" date (**September 1, 2026**) |
| `pcfr/` | **No "current to" date exists** — BC Laws publishes none for this document. The per-rule `_Amendments:_` footers are the only signal; the most recent instrument reflected is B.C. Reg. 17/2026 |
| `da/`, `csg/` | Index states the consolidation and last-amended dates declared by the Justice Laws XML |

Amendments made after those dates are not reflected here. When a
procedural question turns on the PCFR, prefer
`python3 <skill>/scripts/check_freshness.py`, which compares the whole
corpus against the live consolidation, over reading a date off the
index — for that suite there is no date to read.

## How each text is organized

Each source is split into one file per section, rule, or chapter under
`references/generated/<suite>/`, named `section_<number>_<slug>.md`,
`rule_<number>_<slug>.md`, or `chapter_<number>_<slug>.md`, with internal
cross-references converted to relative links. Start from the suite's
`index.md` and follow links to the sections you need — load only what the
question requires.

Appendices to the two rule sets are reproduced too, as
`appendix_<label>_<slug>.md`, and listed at the foot of the suite index.
They are operative text, not annexes: **PCFR Appendix 1** lists the early
resolution registries, and Rule 6(a) makes a new Provincial Court case's
entire first step turn on whether the registry is on it — Form 1 plus a
needs assessment, parenting education and a consensual dispute resolution
session before any application can be filed, or Form 3 directly. **SCFR
Appendix B** is the costs tariff Rule 16-1 assesses under, and **Appendix
C** is the fee schedule. The one appendix deliberately omitted is SCFR
Appendix A, ~390 KB of blank forms: the court publishes fillable copies,
which is what a litigant should actually file, and `forms-guide.md`
already maps each form to the rule requiring it.

Where the official source carries per-section amendment history, each
file ends with an `_Amendments:_` footer listing the instruments that
amended it (e.g. `[am. B.C. Reg. 214/2023, s. 2.]` for the BC
regulations; the federal statutes' amendment history). The footer is
provenance, not operative text — treat it as metadata for flagging
currency, never as part of the enactment. BC *acts* (the FLA) carry no
per-section history in the BC Laws XML, so their files have no footer;
the index's "current to" line is the only freshness signal for those.

`forms-guide.md` is generated from the rule texts by
`scripts/build_forms_index.py`; regenerate it whenever the rule files
are refreshed.

## Rules for using these texts

1. **Prefer these texts over model memory.** When the answer turns on
   statutory wording, quote from the file, not from recall. Model
   training data may reflect an older or misremembered version.

2. **Flag currency when it matters.** If a question depends on a recent
   amendment, a transition provision, or anything dated near or after
   the snapshot date, say so and point the user to the official source
   to confirm the current wording. BC Laws and the Justice Laws Website
   are free and authoritative.

3. **The SSAG User's Guide is advisory.** It is a respected academic
   publication that BC courts routinely use, but it is not law. Do not
   present SSAG ranges as entitlements; entitlement is decided first,
   under the FLA or Divorce Act, before ranges become relevant.

4. **Tables and amounts live elsewhere.** The Federal Child Support
   Tables (the dollar amounts) are not reproduced here. Look up amounts
   at https://www.justice.gc.ca/eng/fl-df/child-enfant/cst-orpe.html or
   with the official calculator at
   https://www.justice.gc.ca/eng/fl-df/child-enfant/cst-orpe/look-rech.aspx.

5. **Refreshing the snapshot.** Each source has a regeneration script
   that fetches the current consolidation from the official XML API and
   rebuilds the per-section files under `references/generated/<suite>/`:

   ```bash
   python3 scripts/regen_fla.py     # Family Law Act        (BC Laws)
   python3 scripts/regen_pcfr.py    # PC Family Rules       (BC Laws)
   python3 scripts/regen_scfr.py    # SC Family Rules       (BC Laws)
   python3 scripts/regen_da.py      # Divorce Act           (Justice Laws)
   python3 scripts/regen_csg.py     # Child Support G/L     (Justice Laws)
   ```

   Default is **check mode**: fetch, compare with this folder, report
   what changed, exit non-zero on drift. Run
   `python3 scripts/check_freshness.py` to check all five sources at
   once (it exits non-zero if any has drifted); a scheduled GitHub
   Action (`.github/workflows/check-freshness.yml`) runs it weekly.
   `--write` applies the refresh; after writing,
   review `git diff` (the diff is the amendment report), rerun
   `scripts/build_forms_index.py`, and update the snapshot line above.
   The SSAG User's Guide has no script — it is a static 2016
   publication; if a revised edition ever appears, rebuild manually
   from the official source above.
