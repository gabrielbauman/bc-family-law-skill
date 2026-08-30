#!/usr/bin/env python3
"""CanLII API helper: verify citations, check treatment, browse decisions.

The CanLII REST API (https://github.com/canlii/API_documentation) serves
case METADATA and CITATION NETWORKS — not full text, and it has no
free-text search. What it does support maps exactly onto this skill's
case-law workflow:

  resolve   verify a citation exists and see its canonical title/URL
  citing    what cites this case (look for negative treatment)
  cited     what this case cites
  recent    newest decisions in a database (e.g. bcca, bcsc, bcpc)
  databases list database ids (courts/tribunals), filterable

An API key is required: request one via CanLII's feedback form
(https://www.canlii.org/en/feedback/feedback.html — free, manual
approval). Provide it with --key or the CANLII_API_KEY environment
variable. Full text still comes from canlii.org in the browser — this
tool only makes the authorities/ verification workflow faster and
catches overturned cases.

Examples:

    python3 canlii.py resolve "2007 BCCA 586"
    python3 canlii.py resolve "1999 CanLII 1527 (ON CA)"
    python3 canlii.py citing "2007 BCCA 586"
    python3 canlii.py recent bcsc --after 2026-05-01 --count 20
    python3 canlii.py databases --jurisdiction bc
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.canlii.org/v1"
UA = "bc-family-law-skill canlii helper (single interactive lookups)"

# Court codes that don't map to a databaseId by simple lowercasing.
SPECIAL_DBS = {
    "SCC": "csc-scc",
    "CSC": "csc-scc",
    "FC": "fct",
    "FCA": "fca",
    "TCC": "tcc",
}


def db_for_court(code: str) -> str:
    code = code.replace(" ", "").replace(".", "").upper()
    return SPECIAL_DBS.get(code, code.lower())


def parse_citation(text: str) -> tuple[str, str]:
    """Return (databaseId, caseId) from a citation string.

    Handles neutral citations ("2007 BCCA 586") and CanLII citations
    ("1999 CanLII 1527 (ON CA)"). Raises ValueError otherwise — e.g.
    for report-series citations like "[1999] 1 SCR 242", which have no
    derivable id; look those up on canlii.org instead.
    """
    text = text.strip()
    m = re.search(r"\b(\d{4})\s+CanLII\s+(\d+)\s*\(([^)]+)\)", text, re.I)
    if m:
        year, number, court = m.group(1), m.group(2), m.group(3)
        return db_for_court(court), f"{year}canlii{number}"
    m = re.search(r"\b(\d{4})\s+([A-Z][A-Za-z]{1,9})\s+(\d+)\b", text)
    if m:
        year, court, number = m.group(1), m.group(2), m.group(3)
        if court.upper() == "CANLII":
            raise ValueError(
                "a CanLII citation needs its court, e.g. \"1999 CanLII 1527 (ON CA)\""
            )
        return db_for_court(court), f"{year}{court.lower()}{number}"
    raise ValueError(
        f"could not parse {text!r} as a neutral or CanLII citation; "
        "report-series citations ([1999] 1 SCR 242) must be looked up on canlii.org"
    )


def call(path: str, key: str, params: dict | None = None, dry_run: bool = False):
    qs = dict(params or {})
    url = f"{API}/{path}?{urllib.parse.urlencode(qs)}" if qs else f"{API}/{path}"
    if dry_run:
        print(f"[dry-run] GET {url}")
        return None
    qs["api_key"] = key
    url = f"{API}/{path}?{urllib.parse.urlencode(qs)}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            sys.exit("error: CanLII rejected the API key (HTTP %d). Check "
                     "CANLII_API_KEY, or request a key via "
                     "https://www.canlii.org/en/feedback/feedback.html" % e.code)
        if e.code == 404:
            sys.exit("not found (HTTP 404): no record for that id. The citation "
                     "may be wrong, the case may predate neutral citations, or "
                     "the court may not be in CanLII's collection — verify on "
                     "https://www.canlii.org before concluding it doesn't exist.")
        sys.exit(f"error: CanLII returned HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:200]}")
    except json.JSONDecodeError:
        sys.exit("error: unparseable response from CanLII (the API returns "
                 "malformed JSON for some auth errors — check your key)")


def fmt_case(c: dict) -> str:
    case_id = c.get("caseId")
    if isinstance(case_id, dict):
      case_id = case_id.get("en") or next(iter(case_id.values()), "")
    return f"- {c.get('title', '?')} — {c.get('citation', '?')}  [{c.get('databaseId', '?')}/{case_id}]"


def cmd_resolve(args, key):
    db, case_id = parse_citation(args.citation)
    data = call(f"caseBrowse/en/{db}/{case_id}/", key, dry_run=args.dry_run)
    if data is None:
        return
    print(f"title:     {data.get('title')}")
    print(f"citation:  {data.get('citation')}")
    print(f"decided:   {data.get('decisionDate')}   docket: {data.get('docketNumber')}")
    print(f"url:       {data.get('url')}")
    if data.get("keywords"):
        print(f"keywords:  {data['keywords']}")
    print("\nverified: the citation resolves on CanLII. Confirm the title matches")
    print("the case you intend, then download the full text from the url above")
    print("into authorities/ — metadata alone never supports a citation.")


def cmd_citator(args, key, direction: str):
    db, case_id = parse_citation(args.citation)
    data = call(f"caseCitator/en/{db}/{case_id}/{direction}", key, dry_run=args.dry_run)
    if data is None:
        return
    cases = data.get(direction, [])
    label = "cases citing this case" if direction == "citingCases" else "cases this case cites"
    print(f"{len(cases)} {label}:")
    for c in cases:
        print(fmt_case(c))
    if direction == "citingCases" and cases:
        print("\nTreatment is not classified by the API: read the citing cases")
        print("(at least the appellate ones) to check whether any overturn,")
        print("reverse, or qualify this case before relying on it.")


def cmd_recent(args, key):
    params = {"offset": 0, "resultCount": args.count}
    if args.after:
        params["decisionDateAfter"] = args.after
    data = call(f"caseBrowse/en/{args.database}/", key, params, dry_run=args.dry_run)
    if data is None:
        return
    for c in data.get("cases", []):
        print(fmt_case(c))


def cmd_databases(args, key):
    data = call("caseBrowse/en/", key, dry_run=args.dry_run)
    if data is None:
        return
    for d in data.get("caseDatabases", []):
        if args.jurisdiction and d.get("jurisdiction") != args.jurisdiction:
            continue
        print(f"{d.get('databaseId'):12} {d.get('jurisdiction'):3} {d.get('name')}")


def main():
    ap = argparse.ArgumentParser(
        description="CanLII metadata/citator helper (no full text, no search — see module docstring)."
    )
    ap.add_argument("--key", default=os.environ.get("CANLII_API_KEY", ""),
                    help="API key (default: CANLII_API_KEY env var)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the request URL instead of calling")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("resolve", help="verify a citation and fetch its metadata")
    p.add_argument("citation", help='e.g. "2007 BCCA 586" or "1999 CanLII 1527 (ON CA)"')

    p = sub.add_parser("citing", help="cases that cite this case (treatment check)")
    p.add_argument("citation")

    p = sub.add_parser("cited", help="cases this case cites")
    p.add_argument("citation")

    p = sub.add_parser("recent", help="newest decisions in a database")
    p.add_argument("database", help="databaseId, e.g. bcca, bcsc, bcpc")
    p.add_argument("--after", help="decisions on/after this date (YYYY-MM-DD)")
    p.add_argument("--count", type=int, default=10)

    p = sub.add_parser("databases", help="list case databases")
    p.add_argument("--jurisdiction", help="filter, e.g. bc, ca")

    args = ap.parse_args()
    if not args.key and not args.dry_run:
        sys.exit("error: no API key. Set CANLII_API_KEY or pass --key. Keys are "
                 "free on request via https://www.canlii.org/en/feedback/feedback.html")
    try:
        if args.cmd == "resolve":
            cmd_resolve(args, args.key)
        elif args.cmd == "citing":
            cmd_citator(args, args.key, "citingCases")
        elif args.cmd == "cited":
            cmd_citator(args, args.key, "citedCases")
        elif args.cmd == "recent":
            cmd_recent(args, args.key)
        elif args.cmd == "databases":
            cmd_databases(args, args.key)
    except ValueError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()
