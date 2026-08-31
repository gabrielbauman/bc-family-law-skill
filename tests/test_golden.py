"""End-to-end golden test for the regen renderer.

Runs a committed capture of a real BC Laws part (FLA Part 1) through the
full pipeline and asserts each section renders exactly to the shipped corpus
under references/generated/fla/. This catches regressions that the synthetic
unit fixtures can't: schema drift, the exact blank-line rhythm, mixed-content
rendering, and cross-reference handling on genuine XML.

Sections 2, 3, and 3.1 carry no intra-statute cross-references, so they
render without the two-pass link map. Section 1 is deliberately excluded —
its definition text folds "section 247 [..]" and friends into links, which
needs the full statute's section map; that path is covered separately by
RenderInlineTest and TwoPassTest.
"""

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "bc-family-law", "scripts"))

from bclaws_regen import Source, filename, parse_units, unit_markdown  # noqa: E402

FIXTURE = Path(os.path.dirname(__file__)) / "fixtures" / "fla_part1.xml"
CORPUS = (
    Path(os.path.dirname(__file__))
    / ".."
    / "skills"
    / "bc-family-law"
    / "references"
    / "generated"
    / "fla"
)


def act_source() -> Source:
    return Source(
        key="fla",
        doc_id="11025",
        multi=True,
        unit="Section",
        title="Family Law Act",
        citation="**[SBC 2011] CHAPTER 25**",
    )


class GoldenRenderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.units = parse_units(FIXTURE.read_bytes(), None, act_source())
        cls.by_num = {u.num: u for u in cls.units}

    def _assert_matches_corpus(self, num: str):
        self.assertIn(num, self.by_num, f"fixture missing section {num}")
        unit = self.by_num[num]
        expected = (CORPUS / filename(act_source(), unit.num, unit.marginal)).read_text(
            encoding="utf-8"
        )
        self.assertEqual(unit_markdown(act_source(), unit), expected)

    def test_section_2_general_interpretation(self):
        self._assert_matches_corpus("2")

    def test_section_3_spouses(self):
        self._assert_matches_corpus("3")

    def test_section_3_1_companion_animals(self):
        self._assert_matches_corpus("3.1")


if __name__ == "__main__":
    unittest.main()