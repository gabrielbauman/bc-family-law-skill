#!/usr/bin/env python3
"""Regenerate the Supreme Court Family Rules references (scfr_*) from
BC Laws. Check mode by default; --write to apply (then rerun
scripts/build_forms_index.py)."""

from bclaws_regen import Source, run_cli

run_cli(Source(
    key="scfr",
    doc_id="169_2009",
    multi=True,
    unit="Rule",
    title="Supreme Court Family Rules",
    citation="**B.C. Reg. 169/2009**",
    tagline="These rules govern family law proceedings in the Supreme Court of British Columbia.",
    pad_nums=False,  # SCFR rules are numbered by part: 16-1, 23-2, ...
    style="rules",   # bcl:rule units with titled subrules (### headings)
    slug_max=50,     # the established corpus truncates SCFR slugs
))
