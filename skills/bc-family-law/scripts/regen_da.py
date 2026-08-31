#!/usr/bin/env python3
"""Regenerate the Divorce Act references (da_*) from the Justice Laws
Website. Check mode by default; --write to apply."""

from bclaws_regen import Source, run_cli
from justicelaws_regen import build_federal

run_cli(Source(
    key="da",
    doc_id="D-3.4",
    multi=False,
    unit="Section",
    title="Divorce Act",
    citation="**R.S.C., 1985, c. 3 (2nd Supp.)**",
    tagline="An Act respecting divorce and corollary relief.",
), build_fn=build_federal)
