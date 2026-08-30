#!/usr/bin/env python3
"""Shared machinery for regenerating BC Laws references (FLA, PCFR, SCFR).

Fetches the current consolidation from the BC Laws CiviX API as XML and
renders the per-section/per-rule markdown files plus the index file in
the format used by references/. Stdlib only.

The BC Laws content is licensed under the King's/Queen's Printer License
of British Columbia (https://www.bclaws.gov.bc.ca/standards/2014/QP-License_1.0.html)
— review it before redistributing regenerated output.

Used by regen_fla.py, regen_pcfr.py, and regen_scfr.py. Each defines a
Source and calls run_cli().
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
import time
import unicodedata
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

BASE = "https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg"
UA = "bc-family-law-skill reference regenerator (github; respectful use)"
NS = {
    "act": "http://www.gov.bc.ca/2013/legislation/act",
    "reg": "http://www.gov.bc.ca/2013/legislation/regulation",
    "bcl": "http://www.gov.bc.ca/2013/bclegislation",
    "in": "http://www.qp.gov.bc.ca/2013/inline",
    "oasis": "http://docs.oasis-open.org/ns/oasis-exchange/table",
}


@dataclass
class Source:
    key: str              # file prefix: fla / pcfr / scfr
    doc_id: str           # civix id: 11025 / 120_2020 / 169_2009
    multi: bool           # multi-part document with a _00 TOC
    unit: str             # "Section" or "Rule"
    title: str            # display title for the index
    citation: str         # e.g. "**[SBC 2011] CHAPTER 25**"
    tagline: str = ""     # editorial line under the citation, if any
    currency_line: bool = False  # include "This Act is current to ..." line
    pad_nums: bool = True  # zero-pad to 3 digits (FLA/PCFR); SCFR's
                           # part-number rules ("16-1") are not padded
    style: str = "act"     # "act": bcl:section units (FLA, PCFR).
                           # "rules": bcl:rule units with titled subrules
                           # rendered as ### headings (SCFR).
    slug_max: int = 0      # truncate filename slugs to this many chars
                           # (0 = no limit); the SCFR corpus uses 51


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def part_doc_ids(source: Source) -> list[str]:
    """Enumerate the document ids that make up the source."""
    if not source.multi:
        return [source.doc_id]
    toc = fetch(f"{BASE}/{source.doc_id}_00/xml").decode("utf-8", "replace")
    ids = sorted(
        {m.group(1) for m in re.finditer(r'href="(%s_\d+)#' % re.escape(source.doc_id), toc)}
    )
    if not ids:
        sys.exit(f"error: no part links found in {source.doc_id}_00 TOC")
    return ids


def currency_date(source: Source) -> str | None:
    doc = f"{source.doc_id}_00" if source.multi else source.doc_id
    html = fetch(f"{BASE}/{doc}/xml").decode("utf-8", "replace")
    m = re.search(r"current to (\w+ \d+, \d{4})", html)
    return m.group(1) if m else None


def qn(tag: str) -> str:
    prefix, _, local = tag.partition(":")
    return f"{{{NS[prefix]}}}{local}"


def text_of(el: ET.Element | None) -> str:
    if el is None:
        return ""
    return "".join(el.itertext()).replace("\xa0", " ").strip()


# ---------------------------------------------------------------------------
# number / slug handling


def num_to_file_num(num: str, pad: bool) -> str:
    """Turn a section/rule label into a safe filename token.

    '3.1' -> '003_1', '87-96' -> '087_96' (pad); '16-1' -> '16_1' (no pad).
    Editorial annotation is stripped ('*36' -> '36') and any character that
    is not alphanumeric becomes '_' ('30 and 31' -> '30_and_31'), so no
    label can produce a filename with spaces or shell metacharacters.
    """
    num = num.replace("*", "").strip()
    parts = re.split(r"[.\-]", num)
    cleaned = [re.sub(r"[^0-9A-Za-z]+", "_", p).strip("_") for p in parts]
    cleaned = [p for p in cleaned if p]
    if pad and cleaned:
        cleaned[0] = cleaned[0].zfill(3)
    return "_".join(cleaned)


def slugify(text: str) -> str:
    # Match the established corpus convention: lowercase; apostrophes
    # vanish (child's -> childs); diacritics are stripped; hyphens
    # survive; any other punctuation or space becomes "_".
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower().replace("'", "").replace("’", "")
    text = re.sub(r"[^a-z0-9-]+", "_", text)
    return text.strip("_")


def filename(source: Source, num: str, marginal: str) -> str:
    # Each source lives in its own folder (references/generated/<key>/), so
    # the filename needs no <key>_ prefix — the folder is the namespace.
    slug = slugify(marginal)
    if source.slug_max:
        slug = slug[: source.slug_max]
    base = f"{source.unit.lower()}_{num_to_file_num(num, source.pad_nums)}"
    return f"{base}_{slug}.md" if slug else f"{base}.md"


# ---------------------------------------------------------------------------
# inline text rendering

# Only references to the source's OWN unit may link: "rule 62 [desc]"
# inside the PCFR links, but "section 183 [desc] of the Family Law Act"
# inside the PCFR refers to a different statute and must stay plain —
# a bare number can't be resolved across statutes. Only singular
# references link ("sections 94 and 215" stays plain), and the optional
# subsection suffix may be numeric or lettered ("section 170 (g)").

_REF_TAILS: dict[str, re.Pattern] = {}


def ref_tail(unit: str) -> re.Pattern:
    if unit not in _REF_TAILS:
        w = re.escape(unit.lower())
        _REF_TAILS[unit] = re.compile(
            rf"(?P<word>(?i:{w}))\s+(?P<num>\d[\d.]*(?:-\d[\d.]*)?)\s*(?P<sub>\((?:\d[\d.]*|[a-z])\))?\s*$"
        )
    return _REF_TAILS[unit]


def render_inline(el: ET.Element, link_map: dict[str, str], unit: str, bold_terms: bool = False) -> str:
    """Render a text element's mixed content to one markdown line.

    Defined terms (in:term) are bolded only inside definition blocks —
    in running text the corpus keeps them as plain quoted words.
    """
    out: list[str] = []

    def emit(s: str | None):
        if s:
            out.append(s)

    emit(el.text)
    for child in el:
        if child.tag == qn("in:term"):
            term = "".join(child.itertext())
            out.append(f'**"{term}"** ' if bold_terms else f'"{term}"')
        elif child.tag == qn("in:desc"):
            desc = "".join(child.itertext())
            # If the text so far ends in "<unit> N (x)" and N resolves to
            # a known file, fold the reference and the bracketed
            # description into one link — the established corpus format.
            prefix = "".join(out)
            m = ref_tail(unit).search(prefix)
            target = link_map.get(m.group("num")) if m else None
            if m and target:
                linktext = prefix[m.start():].rstrip() + f" {desc}"
                out = [prefix[: m.start()], f"[{linktext}]({target})"]
            else:
                out.append(desc)
        else:  # any other inline element: keep its text content
            emit("".join(child.itertext()))
        emit(child.tail)
    line = "".join(out).replace("\xa0", " ")
    return re.sub(r"[ \t]+", " ", line).strip()


# ---------------------------------------------------------------------------
# block rendering — every block carries a kind and nesting level so the
# corpus blank-line rhythm can be reproduced exactly: two blank lines
# before definitions, numeric subsections, and top-level prose; one
# blank line before lettered/roman items and nested continuation prose.

Block = tuple[str, int, str]  # (kind: text|def|num|item|table, level, markdown)

NUMBERED = {qn(t) for t in (
    "bcl:subsection", "bcl:paragraph", "bcl:subparagraph", "bcl:clause", "bcl:subclause",
)}
# hnote = amendment-history notes ("[am. B.C. Reg. ...]"). They are not
# operative text, so they are not rendered inline — but they carry the
# provenance that flags currency risk, so they are captured (in parse_units)
# and appended as a labelled "Amendments:" footer to each unit.
SKIP = {qn("bcl:num"), qn("bcl:marginalnote"), qn("bcl:hnote")}


def render_children(el: ET.Element, link_map: dict, unit: str, level: int, in_def: bool = False, bullet: bool = False) -> list[Block]:
    blocks: list[Block] = []
    for child in el:
        blocks.extend(render_node(child, link_map, unit, level, in_def, bullet))
    return blocks


def render_node(el: ET.Element, link_map: dict, unit: str, level: int, in_def: bool = False, bullet: bool = False) -> list[Block]:
    tag = el.tag
    if tag in SKIP:
        return []
    if tag == qn("bcl:text"):
        line = render_inline(el, link_map, unit, bold_terms=in_def)
        return [("text", level, line)] if line else []
    if tag in NUMBERED:
        num = text_of(el.find(qn("bcl:num")))
        kind = "num" if num[:1].isdigit() else "item"
        blocks: list[Block] = []
        first_text_seen = False
        for sub in el:
            if sub.tag in SKIP:
                continue
            if sub.tag == qn("bcl:text") and not first_text_seen:
                line = render_inline(sub, link_map, unit, bold_terms=in_def)
                if num:
                    prefix = f"- **({num})**" if bullet else f"**({num})**"
                    blocks.append((kind, level, f"{prefix} {line}".rstrip()))
                elif line:
                    blocks.append((kind, level, f"- {line}" if bullet else line))
                first_text_seen = True
            else:
                blocks.extend(render_node(sub, link_map, unit, level + 1, in_def, bullet))
        if not first_text_seen:
            blocks.insert(0, (kind, level, f"- **({num})**" if bullet else f"**({num})**"))
        return blocks
    if tag == qn("bcl:definition"):
        blocks = []
        first_text_seen = False
        for sub in el:
            if sub.tag in SKIP:
                continue
            if sub.tag == qn("bcl:text") and not first_text_seen:
                line = render_inline(sub, link_map, unit, bold_terms=True)
                if line:
                    blocks.append(("def", level, line))
                first_text_seen = True
            else:
                blocks.extend(render_node(sub, link_map, unit, level + 1, in_def=True, bullet=bullet))
        return blocks
    if tag == qn("oasis:table") or tag == qn("bcl:table"):
        return render_table(el, level)
    # unknown containers: recurse transparently at the same level
    return render_children(el, link_map, unit, level, in_def, bullet)


def render_table(el: ET.Element, level: int) -> list[Block]:
    rows_md: list[str] = []
    for row in el.iter(qn("oasis:row")):
        cells = []
        for entry in row.iter(qn("oasis:entry")):
            cells.append(re.sub(r"\s+", " ", " ".join(entry.itertext())).strip())
        if cells:
            rows_md.append("| " + " | ".join(cells) + " |")
    return [("table", level, "\n".join(rows_md))] if rows_md else []


# ---------------------------------------------------------------------------
# document assembly


@dataclass
class Unit:
    num: str
    marginal: str
    blocks: list[Block]
    part: tuple[str, str] | None       # (num, title)
    division: tuple[str, str] | None   # (num, title)
    amendments: str = ""               # amendment-history annotation, verbatim


def parse_units(xml_bytes: bytes, link_map: dict[str, str] | None, source: Source) -> list[Unit]:
    root = ET.fromstring(xml_bytes)
    units: list[Unit] = []
    unit = source.unit
    container = qn("bcl:rule") if source.style == "rules" else qn("bcl:section")

    def parse_rule(el) -> tuple[str, str, list[Block]]:
        """SCFR-style rule: number + title, subrules with ### headings."""
        num = text_of(el.find(qn("bcl:num")))
        title = text_of(el.find(qn("bcl:text")))
        blocks: list[Block] = []
        for sub in el:
            if sub.tag in SKIP or sub.tag == qn("bcl:text"):
                continue
            if sub.tag == qn("bcl:subrule"):
                marginal = text_of(sub.find(qn("bcl:marginalnote")))
                if marginal:
                    blocks.append(("h3", 0, f"### {marginal}"))
                snum = text_of(sub.find(qn("bcl:num")))
                first_text_seen = False
                for el2 in sub:
                    if el2.tag in SKIP:
                        continue
                    if el2.tag == qn("bcl:text") and not first_text_seen:
                        line = render_inline(el2, link_map or {}, unit)
                        blocks.append(("num", 0, f"**({snum})** {line}".rstrip()))
                        first_text_seen = True
                    else:
                        blocks.extend(render_node(el2, link_map or {}, unit, 1, bullet=True))
            else:
                blocks.extend(render_node(sub, link_map or {}, unit, 0, bullet=True))
        return num, title, blocks

    def walk(el, part, division):
        for child in el:
            if child.tag == qn("bcl:part"):
                pnum = text_of(child.find(qn("bcl:num")))
                ptitle = text_of(child.find(qn("bcl:text")))
                walk(child, (pnum, ptitle), None)
            elif child.tag == qn("bcl:division"):
                dnum = text_of(child.find(qn("bcl:num")))
                dtitle = text_of(child.find(qn("bcl:text")))
                walk(child, part, (dnum, dtitle))
            elif child.tag == container:
                if source.style == "rules":
                    num, marginal, blocks = parse_rule(child)
                else:
                    num = text_of(child.find(qn("bcl:num")))
                    marginal = text_of(child.find(qn("bcl:marginalnote")))
                    blocks = render_children(child, link_map or {}, unit, 0, in_def=False)
                if not num:
                    continue
                amendments = text_of(next(child.iter(qn("bcl:hnote")), None))
                units.append(Unit(num, marginal, blocks, part, division, amendments=amendments))
            elif source.style == "rules" and child.tag == qn("bcl:section"):
                continue  # appendix schedules — not part of the rules corpus
            else:
                walk(child, part, division)

    walk(root, None, None)
    return units


def two_pass(source: Source, parts_xml: list[bytes]) -> list[Unit]:
    # pass 1: discover unit numbers and filenames for the link map
    link_map: dict[str, str] = {}
    for xml in parts_xml:
        for u in parse_units(xml, None, source):
            link_map[u.num] = filename(source, u.num, u.marginal)
    # pass 2: render with links resolved
    units: list[Unit] = []
    for xml in parts_xml:
        units.extend(parse_units(xml, link_map, source))
    return units


def unit_markdown(source: Source, u: Unit) -> str:
    # Corpus blank-line rhythm: two blank lines before definitions,
    # numeric subsections, and a section's opening prose; one blank line
    # before lettered/roman items and any continuation prose — both the
    # tail of a definition and "sandwich text" that resumes after a list
    # of items at the section level.
    lines: list[str] = [f"# {source.unit} {u.num} — {u.marginal}"]
    if source.style == "rules":
        # SCFR rhythm: three blanks after the title; two blanks on
        # either side of a subrule heading; one between everything else.
        prev = None
        for i, (kind, level, text) in enumerate(u.blocks):
            blanks = 3 if i == 0 else (2 if "h3" in (kind, prev) else 1)
            lines.extend([""] * blanks)
            lines.append(text)
            prev = kind
    else:
        for i, (kind, level, text) in enumerate(u.blocks):
            wide = kind in ("def", "num") or (kind in ("text", "table") and i == 0)
            lines.append("")
            if wide:
                lines.append("")
            lines.append(text)
    if u.amendments:
        lines.append("")
        lines.append("")
        lines.append(f"_Amendments: {u.amendments}_")
    return "\n".join(lines) + "\n"


def index_markdown(source: Source, units: list[Unit], currency: str | None) -> str:
    lines = [f"# {source.title}", "", source.citation, ""]
    if source.tagline:
        lines += ["", source.tagline, ""]
    if currency:
        lines += ["", currency, ""]
    lines += ["", "---", "", "", "## Table of Contents", ""]
    part = division = None
    for u in units:
        if u.part != part:
            part = u.part
            division = None
            if part:
                if part[0]:
                    heading = f"### Part {part[0]}" + (f" — {part[1]}" if part[1] else "")
                else:
                    heading = f"### {part[1]}"
                lines += ["", heading, ""]
        if u.division != division:
            division = u.division
            if division:
                if division[0]:
                    dheading = f"**Division {division[0]}" + (f" — {division[1]}" if division[1] else "") + "**"
                else:
                    dheading = f"**{division[1]}**"
                lines += ["", dheading, ""]
        fn = filename(source, u.num, u.marginal)
        lines.append(f"- [{source.unit} {u.num} — {u.marginal}]({fn})")
    return "\n".join(lines) + "\n"


def build(source: Source, verbose: bool = True) -> dict[str, str]:
    """Fetch and render everything. Returns {filename: content}."""
    ids = part_doc_ids(source)
    parts_xml: list[bytes] = []
    for i, doc in enumerate(ids):
        if verbose:
            print(f"fetch {doc} ({i + 1}/{len(ids)})", file=sys.stderr)
        parts_xml.append(fetch(f"{BASE}/{doc}/xml"))
        time.sleep(0.5)  # be polite to the public API
    units = two_pass(source, parts_xml)
    currency = None
    if source.currency_line:
        date = currency_date(source)
        if date:
            currency = f"This Act is current to {date}."
    out = {filename(source, u.num, u.marginal): unit_markdown(source, u) for u in units}
    out["index.md"] = index_markdown(source, units, currency)
    return out


# ---------------------------------------------------------------------------
# CLI


def run_cli(source: Source, build_fn=None):
    ap = argparse.ArgumentParser(
        description=f"Regenerate {source.title} references from BC Laws."
    )
    ap.add_argument("--write", action="store_true", help="write into --refs (default: check only)")
    ap.add_argument("--refs", default=str(Path(__file__).resolve().parent.parent / "references" / "generated" / source.key),
                    help="directory to compare/write into (default: that source's generated folder)")
    ap.add_argument("--out", help="write generated files to this directory instead")
    ap.add_argument("--diff-limit", type=int, default=3, help="changed files to show diffs for in check mode")
    args = ap.parse_args()

    generated = (build_fn or build)(source)
    refs = Path(args.refs)

    if args.out:
        outdir = Path(args.out)
        outdir.mkdir(parents=True, exist_ok=True)
        for name, content in generated.items():
            (outdir / name).write_text(content, encoding="utf-8")
        print(f"wrote {len(generated)} files to {outdir}")
        return

    existing = {
        p.name: p.read_text(encoding="utf-8")
        for p in refs.glob("*.md")
    }
    added = sorted(set(generated) - set(existing))
    removed = sorted(set(existing) - set(generated))
    changed = sorted(
        n for n in set(generated) & set(existing) if generated[n] != existing[n]
    )

    if args.write:
        refs.mkdir(parents=True, exist_ok=True)
        for n in removed:
            (refs / n).unlink()
        for n, content in generated.items():
            (refs / n).write_text(content, encoding="utf-8")
        print(f"wrote {len(generated)} files; removed {len(removed)} stale; "
              f"{len(changed)} changed, {len(added)} new")
        print("now: review `git diff`, update the snapshot date in "
              "references/legal-sources.md, and rerun scripts/build_forms_index.py")
        return

    print(f"{source.key}: {len(generated)} generated | "
          f"{len(added)} new, {len(removed)} stale, {len(changed)} changed, "
          f"{len(generated) - len(added) - len(changed)} identical")
    for n in added:
        print(f"  + {n}")
    for n in removed:
        print(f"  - {n}")
    for n in changed[: args.diff_limit]:
        print(f"\n--- diff: {n} ---")
        diff = difflib.unified_diff(
            existing[n].splitlines(), generated[n].splitlines(),
            fromfile=f"references/{n}", tofile="regenerated", lineterm="", n=1,
        )
        for line in list(diff)[:40]:
            print(line)
    if len(changed) > args.diff_limit:
        print(f"\n(… {len(changed) - args.diff_limit} more changed files; "
              f"use --out DIR to inspect everything)")
    sys.exit(1 if (added or removed or changed) else 0)
