#!/usr/bin/env python3
"""Regenerate the Family Law Act references (fla_*) from BC Laws.

Default is check mode: fetch the current consolidation, compare with
references/, report drift. Use --write to apply, then review `git diff`,
update the snapshot date in references/legal-sources.md, and rerun
scripts/build_forms_index.py.
"""

from bclaws_regen import Source, run_cli

run_cli(Source(
    key="fla",
    doc_id="11025",
    multi=True,
    unit="Section",
    title="Family Law Act",
    citation="**[SBC 2011] CHAPTER 25**",
    currency_line=True,
))
