#!/usr/bin/env python3
"""Regenerate the Federal Child Support Guidelines references (csg_*)
from the Justice Laws Website. Check mode by default; --write to apply.

The dollar-amount tables (Schedule I) are not reproduced — the official
lookup is linked from references/legal-sources.md."""

from bclaws_regen import Source, run_cli
from justicelaws_regen import build_federal

run_cli(Source(
    key="csg",
    doc_id="SOR-97-175",
    multi=False,
    unit="Section",
    title="Federal Child Support Guidelines",
    citation="**SOR/97-175**",
    tagline=("These guidelines establish a fair standard of support for children "
             "that ensures they continue to benefit from the financial means of "
             "both parents after separation."),
), build_fn=build_federal)
