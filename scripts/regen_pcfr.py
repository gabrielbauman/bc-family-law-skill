#!/usr/bin/env python3
"""Regenerate the Provincial Court Family Rules references (pcfr_*) from
BC Laws. Check mode by default; --write to apply (then rerun
scripts/build_forms_index.py)."""

from bclaws_regen import Source, run_cli

run_cli(Source(
    key="pcfr",
    doc_id="120_2020",
    multi=False,
    unit="Rule",
    title="Provincial Court Family Rules",
    citation="**B.C. Reg. 120/2020**",
    tagline="These rules govern family law proceedings in the Provincial Court of British Columbia.",
))
