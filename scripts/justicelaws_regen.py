#!/usr/bin/env python3
"""Shared machinery for regenerating federal references (Divorce Act,
Federal Child Support Guidelines) from the Justice Laws Website XML.

Federal consolidations are published as single XML documents at
https://laws-lois.justice.gc.ca/eng/XML/<id>.xml and may be reproduced
under the Reproduction of Federal Law Order, SI/97-5 (with due diligence
as to accuracy; not official versions).

Reuses the Source dataclass, markdown renderers, and CLI from
bclaws_regen — only the fetch and XML walk differ (the LIMS schema uses
unprefixed elements: Statute/Regulation > Body > Heading/Section).

Used by regen_da.py and regen_csg.py.
"""

import re
import sys
import urllib.request
from xml.etree import ElementTree as ET

from bclaws_regen import (
    Source, Unit, Block, UA, slugify, filename,
    unit_markdown, index_markdown, run_cli,
)

FED_BASE = "https://laws-lois.justice.gc.ca/eng/XML"

# Block containers whose Label becomes a **(x)** marker
FED_NUMBERED = {"Subsection", "Paragraph", "Subparagraph", "Clause", "Subclause"}
# Elements skipped entirely: editorial history and footnote apparatus
FED_SKIP = {"HistoricalNote", "MarginalNote", "Label", "Footnote", "FootnoteRef",
            "AmendedText", "ReaderNote"}


def fed_fetch(doc: str) -> bytes:
    req = urllib.request.Request(f"{FED_BASE}/{doc}.xml", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def fed_text(el: ET.Element | None) -> str:
    if el is None:
        return ""
    return re.sub(r"\s+", " ", "".join(el.itertext())).replace("\xa0", " ").strip()


def local(el: ET.Element) -> str:
    return el.tag.rsplit("}", 1)[-1]


def render_fed_inline(el: ET.Element, in_def: bool) -> str:
    """Flatten a Text element; bold defined terms inside definitions."""
    out: list[str] = []
    if el.text:
        out.append(el.text)
    for child in el:
        name = local(child)
        if name in ("FootnoteRef", "Footnote"):
            pass  # drop footnote apparatus
        elif name == "DefinedTermEn" and in_def:
            term = "".join(child.itertext())
            out.append(f'**"{term}"** ')
        else:
            out.append("".join(child.itertext()))
        if child.tail:
            out.append(child.tail)
    line = "".join(out).replace("\xa0", " ")
    return re.sub(r"\s+", " ", line).strip()


def render_fed_node(el: ET.Element, level: int, in_def: bool = False) -> list[Block]:
    name = local(el)
    if name in FED_SKIP:
        return []
    if name == "Text":
        line = render_fed_inline(el, in_def)
        return [("text", level, line)] if line else []
    if name in FED_NUMBERED:
        label = fed_text(el.find("Label")).strip("()")
        kind = "num" if label[:1].isdigit() else "item"
        blocks: list[Block] = []
        first_text_seen = False
        for sub in el:
            if local(sub) in FED_SKIP:
                continue
            if local(sub) == "Text" and not first_text_seen:
                line = render_fed_inline(sub, in_def)
                blocks.append((kind, level, f"**({label})** {line}".rstrip()))
                first_text_seen = True
            else:
                blocks.extend(render_fed_node(sub, level + 1, in_def))
        if not first_text_seen and label:
            blocks.insert(0, (kind, level, f"**({label})**"))
        return blocks
    if name == "Definition":
        blocks = []
        first_text_seen = False
        for sub in el:
            if local(sub) in FED_SKIP:
                continue
            if local(sub) == "Text" and not first_text_seen:
                line = render_fed_inline(sub, in_def=True)
                if line:
                    blocks.append(("def", level, line))
                first_text_seen = True
            else:
                blocks.extend(render_fed_node(sub, level + 1, in_def=True))
        return blocks
    if name in ("TableGroup", "table"):
        rows = []
        for row in el.iter():
            if local(row) == "row":
                cells = [fed_text(e) for e in row if local(e) == "entry"]
                if any(cells):
                    rows.append("| " + " | ".join(cells) + " |")
        return [("table", level, "\n".join(rows))] if rows else []
    # transparent recursion through unknown containers
    blocks = []
    for child in el:
        blocks.extend(render_fed_node(child, level, in_def))
    return blocks


def parse_federal(xml_bytes: bytes, source: Source) -> tuple[list[Unit], str | None]:
    root = ET.fromstring(xml_bytes)
    body = next(el for el in root.iter() if local(el) == "Body")

    units: list[Unit] = []
    part: tuple[str, str] | None = None
    division: tuple[str, str] | None = None

    def walk(el):
        nonlocal part, division
        for child in el:
            name = local(child)
            if name == "Heading":
                title = fed_text(child.find("TitleText"))
                lvl = child.get("level", "1")
                if title:
                    if lvl == "1":
                        part, division = ("", title), None
                    else:
                        division = ("", title)
                walk(child)
            elif name == "Section":
                label = fed_text(child.find("Label"))
                marginal = fed_text(child.find("MarginalNote"))
                if not label:
                    continue
                blocks: list[Block] = []
                for sub in child:
                    if local(sub) in FED_SKIP:
                        continue
                    blocks.extend(render_fed_node(sub, 0))
                units.append(Unit(label, marginal, blocks, part, division))
            elif name == "Schedule":
                continue  # schedules (incl. support tables) are out of scope
            else:
                walk(child)

    walk(body)

    lims = "{http://justice.gc.ca/lims}"
    amended = root.get(f"{lims}lastAmendedDate")
    current = root.get(f"{lims}current-date")
    currency = None
    if amended or current:
        bits = []
        if current:
            bits.append(f"Consolidated to {current}")
        if amended:
            bits.append(f"last amended {amended}")
        currency = "; ".join(bits) + "."
    return units, currency


def build_federal(source: Source) -> dict[str, str]:
    print(f"fetch {source.doc_id}.xml", file=sys.stderr)
    xml = fed_fetch(source.doc_id)
    units, currency = parse_federal(xml, source)
    out = {filename(source, u.num, u.marginal): unit_markdown(source, u) for u in units}
    out[f"{source.key}_index.md"] = index_markdown(source, units, currency)
    return out
