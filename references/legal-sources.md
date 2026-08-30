# Legal Sources: Provenance and Currency

The statute, regulation, and rule texts in this folder are reproductions.
Law changes; reproductions do not. Read this file before relying on a
reference for anything time-sensitive, and tell the user when currency
matters to their question.

## What is here, and where it came from

| Prefix | Source | Citation | Official source |
|--------|--------|----------|-----------------|
| `fla_` | Family Law Act (BC) | SBC 2011, c. 25 | https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/11025_01 |
| `pcfr_` | Provincial Court Family Rules | B.C. Reg. 120/2020 | https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/120_2020 |
| `scfr_` | Supreme Court Family Rules | B.C. Reg. 169/2009 | https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/169_2009_00 |
| `da_` | Divorce Act (Canada) | R.S.C. 1985, c. 3 (2nd Supp.) | https://laws-lois.justice.gc.ca/eng/acts/d-3.4/ |
| `csg_` | Federal Child Support Guidelines | SOR/97-175 | https://laws-lois.justice.gc.ca/eng/regulations/sor-97-175/ |
| `ssag_` | Spousal Support Advisory Guidelines: The Revised User's Guide (April 2016), Rogerson & Thompson | Advisory publication, not legislation | https://www.justice.gc.ca/eng/fl-df/spousal-epoux/ssag-ldfpae.html |

**Snapshot currency:** each index file carries its own currency line —
the BC indexes state the "current to" date from BC Laws (most recently
**August 25, 2026**), and the federal indexes state the consolidation and
last-amended dates declared by the Justice Laws XML. Amendments made
after those dates are not reflected here.

## How each text is organized

Each source is split into one file per section, rule, or chapter, named
`<prefix>_section_<number>_<slug>.md` (or `_rule_` / `_chapter_`), with
internal cross-references converted to relative links. Start from the
index file (`fla_index.md`, `pcfr_index.md`, etc.) and follow links to
the sections you need — load only what the question requires.

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
   rebuilds the per-section files in this folder's exact format:

   ```bash
   python3 scripts/regen_fla.py     # Family Law Act        (BC Laws)
   python3 scripts/regen_pcfr.py    # PC Family Rules       (BC Laws)
   python3 scripts/regen_scfr.py    # SC Family Rules       (BC Laws)
   python3 scripts/regen_da.py      # Divorce Act           (Justice Laws)
   python3 scripts/regen_csg.py     # Child Support G/L     (Justice Laws)
   ```

   Default is **check mode**: fetch, compare with this folder, report
   what changed, exit non-zero on drift — run them periodically as an
   amendment monitor. `--write` applies the refresh; after writing,
   review `git diff` (the diff is the amendment report), rerun
   `scripts/build_forms_index.py`, and update the snapshot line above.
   The SSAG User's Guide has no script — it is a static 2016
   publication; if a revised edition ever appears, rebuild manually
   from the official source above.
