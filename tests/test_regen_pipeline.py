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
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "bc-family-law", "scripts"))

from bclaws_regen import (  # noqa: E402
    Source,
    Unit,
    filename,
    link_appendices,
    parse_schedule,
    index_markdown,
    num_to_file_num,
    parse_units,
    render_inline,
    render_table,
    slugify,
    two_pass,
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


def act_source() -> Source:
    return Source(
        key="fla",
        doc_id="11025",
        multi=True,
        unit="Section",
        title="Family Law Act",
        citation="**[SBC 2011] CHAPTER 25**",
    )


def rules_source() -> Source:
    # Mirrors regen_scfr.py: rules are numbered by part and render with
    # titled subrules as ### headings.
    return Source(
        key="scfr",
        doc_id="169_2009",
        multi=True,
        unit="Rule",
        title="Supreme Court Family Rules",
        citation="**B.C. Reg. 169/2009**",
        pad_nums=False,
        style="rules",
        slug_max=50,
    )


# Namespaces matching NS in bclaws_regen.py, for building fixtures.
BC_NS = (
    'xmlns:bcl="http://www.gov.bc.ca/2013/bclegislation" '
    'xmlns:in="http://www.qp.gov.bc.ca/2013/inline" '
    'xmlns:oasis="http://docs.oasis-open.org/ns/oasis-exchange/table" '
    'xmlns:reg="http://www.gov.bc.ca/2013/legislation/regulation" '
    'xmlns:act="http://www.gov.bc.ca/2013/legislation/act"'
)


def render_text(text_xml: str, link_map=None, unit="Section", bold=False) -> str:
    """Render one <bcl:text> payload through render_inline."""
    el = ET.fromstring(f"<bcl:text {BC_NS}>{text_xml}</bcl:text>")
    return render_inline(el, link_map or {}, unit, bold_terms=bold)


def section(num: str, marginal: str, *body: str) -> str:
    return (
        f"<bcl:section><bcl:marginalnote>{marginal}</bcl:marginalnote>"
        f"<bcl:num>{num}</bcl:num>{''.join(body)}</bcl:section>"
    )


def act_xml(*sections: str) -> bytes:
    return (
        f"<act:act {BC_NS}><act:content>{''.join(sections)}</act:content></act:act>"
    ).encode("utf-8")


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
            "section_036_commencement.md",
        )

    def test_repealed_pair_section(self):
        self.assertEqual(
            filename(da_source(), "30 and 31", ""),
            "section_30_and_31.md",
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
        "<HistoricalNote>"
        "<HistoricalNoteSubItem>R.S., 1985, c. 3 (2nd Supp.), s. 2</HistoricalNoteSubItem>"
        "<HistoricalNoteSubItem>2019, c. 16, s. 1</HistoricalNoteSubItem>"
        "</HistoricalNote>"
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
            "section_036_commencement.md",
        )

    def test_heading_has_no_stray_asterisk(self):
        commencement = next(u for u in self.units if u.num == "36")
        md = unit_markdown(da_source(), commencement)
        self.assertIn("# Section 36 — Commencement", md)
        self.assertNotIn("*", md)

    def test_historical_note_captured(self):
        sec1 = next(u for u in self.units if u.num == "1")
        self.assertEqual(
            sec1.amendments,
            "R.S., 1985, c. 3 (2nd Supp.), s. 2; 2019, c. 16, s. 1",
        )

    def test_historical_note_rendered_as_footer(self):
        sec1 = next(u for u in self.units if u.num == "1")
        md = unit_markdown(da_source(), sec1)
        self.assertIn(
            "_Amendments: R.S., 1985, c. 3 (2nd Supp.), s. 2; 2019, c. 16, s. 1_",
            md,
        )

    def test_no_footer_without_history(self):
        sec30 = next(u for u in self.units if u.num == "30 and 31")
        md = unit_markdown(da_source(), sec30)
        self.assertNotIn("_Amendments:", md)


class BcHnoteTest(unittest.TestCase):
    """BC regulations carry amendment history in bcl:hnote; capture it."""

    XML = (
        '<reg:regulation xmlns:reg="http://www.gov.bc.ca/2013/legislation/regulation"'
        ' xmlns:bcl="http://www.gov.bc.ca/2013/bclegislation">'
        "<reg:content>"
        "<bcl:section>"
        "<bcl:marginalnote>Purpose</bcl:marginalnote>"
        "<bcl:num>1</bcl:num>"
        "<bcl:text>The purpose.</bcl:text>"
        "<bcl:hnote>[am. B.C. Reg. 214/2023, s. 2.]</bcl:hnote>"
        "</bcl:section>"
        "</reg:content>"
        "</reg:regulation>"
    )

    def setUp(self):
        self.source = Source(
            key="pcfr", doc_id="120_2020", multi=False,
            unit="Rule", title="PCFR", citation="**test**",
        )
        self.units = parse_units(self.XML.encode("utf-8"), None, self.source)

    def test_hnote_captured(self):
        self.assertEqual(self.units[0].amendments, "[am. B.C. Reg. 214/2023, s. 2.]")

    def test_hnote_rendered_as_footer(self):
        md = unit_markdown(self.source, self.units[0])
        self.assertIn("_Amendments: [am. B.C. Reg. 214/2023, s. 2.]_", md)

    def test_hnote_not_inline_in_body(self):
        md = unit_markdown(self.source, self.units[0])
        body = md.split("_Amendments:")[0]
        self.assertNotIn("am. B.C. Reg", body)


class RenderInlineTest(unittest.TestCase):
    """Cross-reference folding and defined-term bolding in render_inline."""

    def test_folds_own_section_reference(self):
        self.assertEqual(
            render_text(
                'section 247 <in:desc>[regulations respecting child support]</in:desc>',
                link_map={"247": "section_247_regulations_respecting_child_support.md"},
            ),
            "[section 247 [regulations respecting child support]]"
            "(section_247_regulations_respecting_child_support.md)",
        )

    def test_leaves_unresolved_reference_plain(self):
        self.assertEqual(
            render_text(
                'section 247 <in:desc>[regulations respecting child support]</in:desc>',
            ),
            "section 247 [regulations respecting child support]",
        )

    def test_leaves_plural_reference_plain(self):
        self.assertEqual(
            render_text('sections 94 and 215 <in:desc>[commencement]</in:desc>'),
            "sections 94 and 215 [commencement]",
        )

    def test_folds_decimal_section_number(self):
        self.assertEqual(
            render_text(
                'section 3.1 <in:desc>[companion animals]</in:desc>',
                link_map={"3.1": "section_003_1_companion_animals.md"},
            ),
            "[section 3.1 [companion animals]](section_003_1_companion_animals.md)",
        )

    def test_folds_lettered_subsection_suffix(self):
        self.assertEqual(
            render_text(
                'section 170 (g) <in:desc>[matters that may be provided for]</in:desc>',
                link_map={"170": "section_170_matters_that_may_be_provided_for.md"},
            ),
            "[section 170 (g) [matters that may be provided for]]"
            "(section_170_matters_that_may_be_provided_for.md)",
        )

    def test_bolds_defined_term_in_definition(self):
        self.assertEqual(
            render_text('<in:term>child</in:term>', unit="Section", bold=True),
            '**"child"**',
        )

    def test_plain_term_in_running_text(self):
        self.assertEqual(
            render_text('<in:term>child</in:term>', unit="Section", bold=False),
            '"child"',
        )


class UnitMarkdownStructureTest(unittest.TestCase):
    """The exact blank-line rhythm and subsection/paragraph markup."""

    def test_subsection_and_paragraphs(self):
        units = parse_units(
            act_xml(
                section(
                    "37",
                    "Best interests of child",
                    "<bcl:subsection><bcl:num>1</bcl:num>"
                    "<bcl:text>the parties and the court must consider:</bcl:text>"
                    "<bcl:paragraph><bcl:num>a</bcl:num>"
                    "<bcl:text>the child's health.</bcl:text>"
                    "</bcl:paragraph>"
                    "</bcl:subsection>",
                )
            ),
            None,
            act_source(),
        )
        md = unit_markdown(act_source(), units[0])
        self.assertEqual(
            md,
            "# Section 37 — Best interests of child\n\n\n"
            "**(1)** the parties and the court must consider:\n\n"
            "**(a)** the child's health.\n",
        )


class IndexMarkdownTest(unittest.TestCase):
    """Part/division headings and the table of contents list."""

    UNITS = [
        Unit("1", "Definitions", [], ("1", "Interpretation"), None),
        Unit("3", "Spouses and relationships between spouses", [], ("1", "Interpretation"), None),
        Unit("4", "Purposes of Part", [], ("2", "Resolution of Family Law Disputes"), ("1", "Resolution Out of Court Preferred")),
    ]

    def test_part_and_division_headings(self):
        md = index_markdown(act_source(), self.UNITS, None)
        self.assertIn("### Part 1 — Interpretation", md)
        self.assertIn("### Part 2 — Resolution of Family Law Disputes", md)
        self.assertIn("**Division 1 — Resolution Out of Court Preferred**", md)

    def test_links_use_relative_filenames(self):
        md = index_markdown(act_source(), self.UNITS, None)
        self.assertIn(
            "- [Section 3 — Spouses and relationships between spouses]"
            "(section_003_spouses_and_relationships_between_spouses.md)",
            md,
        )

    def test_currency_line_when_present(self):
        md = index_markdown(da_source(), self.UNITS, "This Act is current to August 25, 2026.")
        self.assertIn("This Act is current to August 25, 2026.", md)


class RenderTableTest(unittest.TestCase):
    # BC Laws tags rows <oasis:trow>, not the <oasis:row> of the bare OASIS
    # exchange model. An earlier version of this test used <oasis:row>,
    # which no BC Laws document emits, so render_table passed its test
    # while silently dropping every real table — including PCFR
    # Appendix 1. Keep the trow case first: it is the one that ships.
    def test_bclaws_trow_table_to_pipe_markdown(self):
        root = ET.fromstring(
            f'<oasis:table {BC_NS}>'
            "<oasis:tgroup><oasis:tbody>"
            "<oasis:trow><oasis:entry><oasis:line>Item</oasis:line></oasis:entry>"
            "<oasis:entry><oasis:line>Early Resolution Registry</oasis:line></oasis:entry></oasis:trow>"
            "<oasis:trow><oasis:entry><oasis:line>1</oasis:line></oasis:entry>"
            "<oasis:entry><oasis:line>Abbotsford</oasis:line></oasis:entry></oasis:trow>"
            "</oasis:tbody></oasis:tgroup>"
            "</oasis:table>"
        )
        self.assertEqual(
            render_table(root, 0),
            [("table", 0, "| Item | Early Resolution Registry |\n"
                          "| --- | --- |\n"
                          "| 1 | Abbotsford |")],
        )

    def test_plain_oasis_row_still_renders(self):
        root = ET.fromstring(
            f'<oasis:table {BC_NS}>'
            "<oasis:row><oasis:entry>a</oasis:entry><oasis:entry>b</oasis:entry></oasis:row>"
            "<oasis:row><oasis:entry>1</oasis:entry><oasis:entry>2</oasis:entry></oasis:row>"
            "</oasis:table>"
        )
        self.assertEqual(
            render_table(root, 0),
            [("table", 0, "| a | b |\n| --- | --- |\n| 1 | 2 |")],
        )

    def test_ragged_rows_are_padded(self):
        # A row with fewer cells than the header would otherwise produce a
        # malformed markdown table that renders as raw pipes.
        root = ET.fromstring(
            f'<oasis:table {BC_NS}>'
            "<oasis:trow><oasis:entry>a</oasis:entry><oasis:entry>b</oasis:entry></oasis:trow>"
            "<oasis:trow><oasis:entry>1</oasis:entry></oasis:trow>"
            "</oasis:table>"
        )
        self.assertEqual(
            render_table(root, 0),
            [("table", 0, "| a | b |\n| --- | --- |\n| 1 |  |")],
        )

    def test_empty_table_yields_no_block(self):
        root = ET.fromstring(f'<oasis:table {BC_NS}/>')
        self.assertEqual(render_table(root, 0), [])


SCHEDULE_XML = (
    f"<bcl:schedule {BC_NS}>"
    "<bcl:scheduletitle>Appendix 1 — Early Resolution Registries</bcl:scheduletitle>"
    "<bcl:centertext>[en. B.C. Reg. 17/2026, s. 13.]</bcl:centertext>"
    "<oasis:table><oasis:tgroup><oasis:tbody>"
    "<oasis:trow><oasis:entry><oasis:line>Item</oasis:line></oasis:entry>"
    "<oasis:entry><oasis:line>Early Resolution Registry</oasis:line></oasis:entry></oasis:trow>"
    "<oasis:trow><oasis:entry><oasis:line>1</oasis:line></oasis:entry>"
    "<oasis:entry><oasis:line>Abbotsford</oasis:line></oasis:entry></oasis:trow>"
    "</oasis:tbody></oasis:tgroup></oasis:table>"
    "</bcl:schedule>"
)


class AppendixTest(unittest.TestCase):
    """Appendices are operative text, not decoration.

    PCFR Rule 6(a) makes a new case's entire first step — Form 1 and the
    early resolution requirements, or Form 3 — turn on whether the
    registry is listed in Appendix 1, so an unreproduced appendix leaves
    the reader holding a rule that points at nothing.
    """

    def rules_pcfr(self, **kw) -> Source:
        return Source(key="pcfr", doc_id="120_2020", multi=False, unit="Rule",
                      title="Provincial Court Family Rules",
                      citation="**B.C. Reg. 120/2020**", **kw)

    def test_schedule_becomes_appendix_unit(self):
        u = parse_schedule(ET.fromstring(SCHEDULE_XML), {}, self.rules_pcfr())
        self.assertEqual(u.kind, "appendix")
        self.assertEqual(u.num, "1")
        self.assertEqual(u.marginal, "Early Resolution Registries")
        self.assertEqual(u.amendments, "[en. B.C. Reg. 17/2026, s. 13.]")
        self.assertIn("| 1 | Abbotsford |", u.blocks[0][2])

    def test_appendix_filename_and_heading(self):
        src = self.rules_pcfr()
        u = parse_schedule(ET.fromstring(SCHEDULE_XML), {}, src)
        self.assertEqual(filename(src, u.num, u.marginal, u.kind),
                         "appendix_1_early_resolution_registries.md")
        self.assertTrue(unit_markdown(src, u).startswith(
            "# Appendix 1 — Early Resolution Registries"))

    def test_skip_appendices_drops_the_forms_appendix(self):
        # SCFR Appendix A is ~390 KB of blank forms; the court publishes
        # fillable copies, so the corpus omits it by label.
        xml = SCHEDULE_XML.replace("Appendix 1 —", "Appendix A —")
        src = self.rules_pcfr(skip_appendices=("A",))
        self.assertIsNone(parse_schedule(ET.fromstring(xml), {}, src))

    def test_appendix_index_section(self):
        src = self.rules_pcfr()
        u = parse_schedule(ET.fromstring(SCHEDULE_XML), {}, src)
        rule = Unit("6", "Parts that apply in certain registries", [], None, None)
        md = index_markdown(src, [rule, u], None)
        self.assertIn("### Appendices", md)
        self.assertIn("[Appendix 1 — Early Resolution Registries]"
                      "(appendix_1_early_resolution_registries.md)", md)
        # the appendix must not also appear in the main rule list
        self.assertNotIn("- [Rule 1 — Early Resolution Registries]", md)


class LinkAppendicesTest(unittest.TestCase):
    LINKS = {"appendix:1": "appendix_1_early_resolution_registries.md"}

    def test_reference_is_linked(self):
        self.assertEqual(
            link_appendices("a registry listed in Appendix 1 is an early "
                            "resolution registry", self.LINKS),
            "a registry listed in [Appendix 1]"
            "(appendix_1_early_resolution_registries.md) is an early "
            "resolution registry",
        )

    def test_unreproduced_appendix_stays_plain(self):
        # Linking to a file the corpus skipped would be worse than plain text.
        text = "the forms set out in Appendix A"
        self.assertEqual(link_appendices(text, self.LINKS), text)

    def test_already_linked_text_is_not_double_wrapped(self):
        text = "[Appendix 1](appendix_1_early_resolution_registries.md)"
        self.assertEqual(link_appendices(text, self.LINKS), text)


class TwoPassTest(unittest.TestCase):
    """Pass 1 collects filenames; pass 2 resolves cross-references."""

    def test_cross_part_reference_resolves(self):
        part_a = act_xml(section("3", "Spouses and relationships between spouses"))
        part_b = act_xml(
            section(
                "3.1",
                "Companion animals",
                "<bcl:text>an animal, subject to "
                "section 3 <in:desc>[spouses and relationships between spouses]</in:desc>"
                ".</bcl:text>",
            )
        )
        units = two_pass(act_source(), [part_a, part_b])
        md = unit_markdown(act_source(), next(u for u in units if u.num == "3.1"))
        self.assertIn(
            "[section 3 [spouses and relationships between spouses]]"
            "(section_003_spouses_and_relationships_between_spouses.md)",
            md,
        )


class RulesStyleTest(unittest.TestCase):
    """SCFR 'rules' style: titled rules, subrules as ### headings."""

    def test_subrule_heading(self):
        xml = (
            f'<reg:regulation {BC_NS}><reg:content>'
            "<bcl:rule><bcl:num>1-1</bcl:num><bcl:text>Interpretation</bcl:text>"
            "<bcl:subrule><bcl:marginalnote>Definitions</bcl:marginalnote>"
            "<bcl:num>1</bcl:num><bcl:text>In these rules:</bcl:text></bcl:subrule>"
            "</bcl:rule>"
            "</reg:content></reg:regulation>"
        ).encode("utf-8")
        units = parse_units(xml, None, rules_source())
        self.assertEqual(units[0].num, "1-1")
        self.assertEqual(units[0].marginal, "Interpretation")
        md = unit_markdown(rules_source(), units[0])
        self.assertEqual(
            md,
            "# Rule 1-1 — Interpretation\n\n\n\n"
            "### Definitions\n\n\n"
            "**(1)** In these rules:\n",
        )


class FederalRenderingTest(unittest.TestCase):
    """Federal XML: definition bolding and subsection/paragraph labels."""

    XML = (
        "<Statute><Body>"
        "<Section><Label>2</Label><MarginalNote>Definitions</MarginalNote>"
        "<Definition><Text><DefinedTermEn>spouse</DefinedTermEn>"
        " means a married person.</Text></Definition>"
        "</Section>"
        "<Section><Label>8</Label><MarginalNote>Divorce</MarginalNote>"
        "<Subsection><Label>(1)</Label><Text>A court may grant a divorce.</Text>"
        "<Paragraph><Label>(a)</Label><Text>on breakdown.</Text></Paragraph>"
        "</Subsection>"
        "</Section>"
        "</Body></Statute>"
    )

    def setUp(self):
        self.units, _ = justicelaws_regen.parse_federal(
            self.XML.encode("utf-8"), da_source()
        )

    def test_definition_bolds_defined_term(self):
        md = unit_markdown(da_source(), next(u for u in self.units if u.num == "2"))
        self.assertIn('**"spouse"** means a married person.', md)

    def test_subsection_and_paragraph_labels(self):
        md = unit_markdown(da_source(), next(u for u in self.units if u.num == "8"))
        self.assertIn("**(1)** A court may grant a divorce.", md)
        self.assertIn("**(a)** on breakdown.", md)


if __name__ == "__main__":
    unittest.main()