"""Tests for the reference regeneration pipeline.

Covers the pure functions in bclaws_regen and justicelaws_regen that turn
XML labels into filenames and markdown. The regression cases at the bottom
pin the bug where federal labels like "*36" (a spent provision marker) and
"30 and 31" (a repealed section pair) leaked into filenames as a literal
asterisk and spaces, breaking the generated index links.

Run from the repository root:

    python3 -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from bclaws_regen import (  # noqa: E402
    Source,
    filename,
    num_to_file_num,
    slugify,
    unit_markdown,
)
import justicelaws_regen  # noqa: E402


def da_source() -> Source:
    return Source(
        key="da",
        doc_id="D-3.4",
        multi=False,
        unit="Section",
        title="Divorce Act",
        citation="**R.S.C., 1985, c. 3 (2nd Supp.)**",
    )


class NumToFileNumTest(unittest.TestCase):
    def test_pads_plain_numbers(self):
        self.assertEqual(num_to_file_num("9", pad=True), "009")
        self.assertEqual(num_to_file_num("36", pad=True), "036")
        self.assertEqual(num_to_file_num("87-96", pad=True), "087_96")

    def test_decimal_subsections(self):
        self.assertEqual(num_to_file_num("3.1", pad=True), "003_1")
        self.assertEqual(num_to_file_num("6.1", pad=True), "006_1")

    def test_unpadded_rule_numbers(self):
        self.assertEqual(num_to_file_num("16-1", pad=False), "16_1")

    def test_strips_editorial_asterisk(self):
        self.assertEqual(num_to_file_num("*36", pad=True), "036")

    def test_joins_multi_section_label(self):
        self.assertEqual(num_to_file_num("30 and 31", pad=True), "30_and_31")

    def test_never_emits_spaces_or_metacharacters(self):
        labels = ["*36", "30 and 31", "9.", "-", "a b/c", " 42 ", "3..1",
                  "16 & 17", "'quoted'", "87-96"]
        for label in labels:
            token = num_to_file_num(label, pad=True)
            self.assertRegex(token, r"^[0-9A-Za-z_]*$", f"unsafe token for {label!r}")


class FilenameTest(unittest.TestCase):
    def test_spent_provision_section(self):
        self.assertEqual(
            filename(da_source(), "36", "Commencement"),
            "da_section_036_commencement.md",
        )

    def test_repealed_pair_section(self):
        self.assertEqual(
            filename(da_source(), "30 and 31", ""),
            "da_section_30_and_31.md",
        )

    def test_no_space_or_asterisk_in_any_generated_name(self):
        for num, marginal in [("*36", "Commencement"), ("30 and 31", ""),
                              ("3.1", "Companion animals")]:
            name = filename(da_source(), num, marginal)
            self.assertRegex(name, r"^[0-9A-Za-z_.-]+\.md$", f"unsafe filename for {num!r}")


class SlugifyTest(unittest.TestCase):
    def test_apostrophe_dropped(self):
        self.assertEqual(slugify("child's"), "childs")

    def test_diacritics_stripped(self):
        self.assertEqual(slugify("Bébé"), "bebe")

    def test_hyphen_preserved(self):
        self.assertEqual(slugify("non-application"), "non-application")

    def test_spaces_to_underscores(self):
        self.assertEqual(slugify("Short Title"), "short_title")


class ParseFederalTest(unittest.TestCase):
    """Regression for federal labels leaking editorial markers into output."""

    XML = (
        "<Statute><Body>"
        "<Heading level=\"1\"><TitleText>Short Title</TitleText></Heading>"
        "<Section>"
        "<Label>1</Label><MarginalNote>Short title</MarginalNote>"
        "<Text>This Act is the <DefinedTermEn>Test Act</DefinedTermEn>.</Text>"
        "</Section>"
        "<Section>"
        "<Label>*36</Label><MarginalNote>Commencement</MarginalNote>"
        "<Text>This Act comes into force on a day to be fixed.</Text>"
        "</Section>"
        "<Section><Label>30 and 31</Label><MarginalNote></MarginalNote></Section>"
        "</Body></Statute>"
    )

    def setUp(self):
        self.units, self.currency = justicelaws_regen.parse_federal(
            self.XML.encode("utf-8"), da_source()
        )

    def test_strips_asterisk_from_label(self):
        labels = [u.num for u in self.units]
        self.assertIn("36", labels)
        self.assertNotIn("*36", labels)

    def test_preserves_repealed_pair_label(self):
        labels = [u.num for u in self.units]
        self.assertIn("30 and 31", labels)

    def test_every_unit_maps_to_a_safe_filename(self):
        for u in self.units:
            name = filename(da_source(), u.num, u.marginal)
            self.assertRegex(name, r"^[0-9A-Za-z_.-]+\.md$",
                             f"unsafe filename for section {u.num!r}: {name!r}")

    def test_commencement_filename_is_clean(self):
        commencement = next(u for u in self.units if u.num == "36")
        self.assertEqual(
            filename(da_source(), commencement.num, commencement.marginal),
            "da_section_036_commencement.md",
        )

    def test_heading_has_no_stray_asterisk(self):
        commencement = next(u for u in self.units if u.num == "36")
        md = unit_markdown(da_source(), commencement)
        self.assertIn("# Section 36 — Commencement", md)
        self.assertNotIn("*", md)


if __name__ == "__main__":
    unittest.main()