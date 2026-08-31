#!/usr/bin/env python3
"""Run and grade the behavioral evals in evals.json.

Each eval asserts *observable behavior* — what the agent says and what files
and git it leaves behind — not implementation. This harness turns those
assertions into verdicts:

  python3 evals/run.py list
  python3 evals/run.py setup 4 ./scratch        # lay out that eval's fixtures
  python3 evals/run.py grade 1 --transcript t.txt
  python3 evals/run.py grade 4 --run-dir ./scratch [--judge-cmd "claude -p -"]
  python3 evals/run.py run 3 --command "claude -p -"

Grading is two-tier:

  * Deterministic. Assertions about the filesystem and git (evals 3 and 4 in
    particular) are checked here, offline. Nothing is run through a model.

  * Semantic. Assertions about what the response *recommends* or *refuses*
    are scored by a judge. Without a judge, they report "unjudged" and the
    grade is a best-effort subset.

The judge is any command that reads the judge prompt on stdin and writes a
JSON array of {"index", "pass", "reason"} on stdout, or -- when
ANTHROPIC_API_KEY is set -- the Anthropic Messages API.

`run` invokes an agent non-interactively: it lays out the fixtures, pipes the
eval's prompt to `--command` (with cwd inside the scratch project so the agent
sees CASE.md and the fixture tree), captures the transcript and the final
tree + git log under evals/runs/<id>/, then grades.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
EVALS_JSON = HERE / "evals.json"
FIXTURES = HERE / "files"
RUNS = HERE / "runs"

# Where each eval's fixture files land in the scratch case project. The
# source is relative to evals/files/; the target is relative to the scratch
# root.
SETUP = {
    1: [],
    2: [],
    3: [("messages.json", "evidence/messages/messages.json")],
    4: [
        ("sweep/CASE.md", "CASE.md"),
        ("sweep/inbox/scan0001.txt", "inbox/scan0001.txt"),
        ("sweep/inbox/IMG_2041.txt", "inbox/IMG_2041.txt"),
    ],
}


def evals():
    return json.loads(EVALS_JSON.read_text(encoding="utf-8"))["evals"]


def get_eval(eid: int):
    return next(e for e in evals() if e["id"] == eid)


# ---------------------------------------------------------------------------
# deterministic checks
#
# A checker takes (transcript: str, root: Path | None) and returns
# (ok: bool | None, note: str). ok=None means "not deterministically
# checkable" (falls through to the judge). Registered by exact assertion text
# so a wording change degrades gracefully to the judge instead of erroring.


def _text_of(val: str | None) -> str:
    return val or ""


def _files(root: Path | None, rel: str, glob: str = "*"):
    if not root:
        return []
    return [p for p in (root / rel).glob(glob) if p.is_file()]


def _read(root: Path | None, rel: str) -> str:
    if not root:
        return ""
    p = root / rel
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""


def _dir_text(root: Path | None, rel: str) -> str:
    if not root:
        return ""
    out = []
    for p in sorted((root / rel).glob("**/*")) if (root / rel).exists() else []:
        if p.is_file():
            out.append(p.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(out)


def _grep_any(haystack: str, needles: list[str]) -> bool:
    low = haystack.lower()
    return any(n.lower() in low for n in needles)


def _strip_frontmatter(s: str) -> str:
    lines = s.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[i + 1:])
    return s


def _check_disclaimer_once(t, root):
    n = t.count("legal information, not legal advice")
    return (n == 1, f"disclaimer phrases found: {n} (want exactly 1)")


def _check_canlii_offered(t, root):
    return (_grep_any(t, ["canlii.org", "canlii"]), "CanLII referenced")


def _check_evidence_handler_readme(t, root):
    ok = any(
        p.name == "README.md" and "messages" in str(p.parent)
        for p in (root / "evidence").rglob("README.md")
    ) if root else False
    return (ok, "README handler next to the evidence source")


def _check_message_ids_and_timestamps(t, root):
    body = _strip_frontmatter(_dir_text(root, "research"))
    ids = bool(re.search(r"\b5\d{3}\b", body))
    ts = bool(re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", body))
    return (ids and ts, f"message IDs {ids}, timestamps {ts}")


def _check_no_ellipsis(t, root):
    body = _strip_frontmatter(_dir_text(root, "research"))
    return ("..." not in body, "no '...' elisions in research")


def _check_research_frontmatter(t, root):
    body = _dir_text(root, "research")
    have = [k for k in ("purpose:", "source:", "extracted:") if k in body]
    return (len(have) >= 3, f"frontmatter fields present: {have}")


def _check_research_index_updated(t, root):
    idx = _read(root, "research/index.md")
    ok = bool(idx) and "(no research documents yet)" not in idx and \
        bool(re.search(r"\]\([^)]+\.md\)", idx))
    return (ok, "research/index.md regenerated with a link")


def _check_verbatim_informal(t, root):
    body = _dir_text(root, "research")
    return (_grep_any(body, ["etransfer", "ya saw it", "emmy"]),
            "informal spelling preserved")


def _check_order_filed(t, root):
    body = _dir_text(root, "filings")
    return (_grep_any(body, ["Form 4", "PROVINCIAL COURT"]),
            "court order present under filings/")


def _check_paystub_filed(t, root):
    body = _dir_text(root, "evidence")
    return (_grep_any(body, ["PAY STATEMENT", "ACME WIDGETS"]),
            "pay statement present under evidence/")


def _check_inbox_empty(t, root):
    remaining = [p for p in (root / "inbox").iterdir() if p.is_file()] if root else ["?"]
    return (not remaining, f"files left in inbox: {len(remaining)}")


def _check_deadlines_recorded(t, root):
    body = (_read(root, "CASE.md") + "\n" + t)
    apr = _grep_any(body, ["April 9", "2026-04-09", "9 April"])
    jun = _grep_any(body, ["June 30", "2026-06-30", "30 June"])
    return (apr and jun, f"April 9 {apr}, June 30 {jun}")


def _check_march_10_recorded(t, root):
    body = _read(root, "CASE.md") + "\n" + t
    return (_grep_any(body, ["2026-03-10", "10 March 2026", "March 10, 2026"]),
            "March 10, 2026 order in procedural history")


def _check_git_intake_commit(t, root):
    if not root or not (root / ".git").exists():
        return (False, "no git repository")
    p = subprocess.run(["git", "-C", str(root), "log", "--oneline", "--all"],
                       capture_output=True, text=True)
    log = p.stdout.lower()
    ok = _grep_any(log, ["intake", "scan0001", "img_2041"])
    return (ok, f"git log: {p.stdout.strip()[:120]!r}")


# keyed by exact assertion text from evals.json
DETERMINISTIC = {
    "The response includes the legal information / not legal advice disclaimer exactly once, not repeated per paragraph":
        _check_disclaimer_once,
    "The model explicitly asks the user to obtain the full text, providing a CanLII link or equivalent source":
        _check_canlii_offered,
    "A handler README documenting the export's schema and query commands exists after the run (or an existing one was consulted)":
        _check_evidence_handler_readme,
    "The research file quotes messages with their numeric IDs and full timestamps":
        _check_message_ids_and_timestamps,
    "Quoted conversations are complete sequences with no skipped messages and no '...' elisions":
        _check_no_ellipsis,
    "The research file records its purpose, source file, the exact query used, and the extraction date":
        _check_research_frontmatter,
    "research/index.md is updated with the new research file":
        _check_research_index_updated,
    "Messages are reproduced verbatim, including informal spelling":
        _check_verbatim_informal,
    "The court order (scan0001.txt) is identified and moved to filings/ under a descriptive, dated name":
        _check_order_filed,
    "The pay statement (IMG_2041.txt) is identified and moved into an appropriate evidence/ subfolder":
        _check_paystub_filed,
    "The inbox is empty when the run finishes":
        _check_inbox_empty,
    "Both the April 9, 2026 financial-statement deadline and the June 30, 2026 family management conference are surfaced to the user and recorded in CASE.md":
        _check_deadlines_recorded,
    "CASE.md's procedural history records the March 10, 2026 order":
        _check_march_10_recorded,
    "A git repository is initialized or used, with an intake-style commit that preserves the original filenames in the message or notes":
        _check_git_intake_commit,
}


def grade(eid: int, transcript: str, root: Path | None) -> list[dict]:
    ev = get_eval(eid)
    results = []
    for i, assertion in enumerate(ev["assertions"]):
        checker = DETERMINISTIC.get(assertion)
        if checker is None:
            results.append({"index": i, "assertion": assertion,
                            "verdict": "unjudged", "method": "semantic"})
            continue
        ok, note = checker(transcript, root)
        results.append({"index": i, "assertion": assertion,
                        "verdict": "pass" if ok else "fail",
                        "method": "deterministic", "note": note})
    return results


# ---------------------------------------------------------------------------
# semantic judging (optional)


def judge(transcript: str, assertions: list[dict]) -> dict[int, dict]:
    """Score unjudged assertions with a model; returns {index: {pass, reason}}."""
    prompt = (
        "You graded an AI legal assistant's response against assertions about its "
        "behaviour. For each assertion, decide pass/fail and give one sentence.\n\n"
        "RESPONSE:\n" + transcript + "\n\nASSERTIONS:\n" +
        "\n".join(f"{a['index']}. {a['assertion']}" for a in assertions) +
        "\n\nReply with ONLY a JSON array of objects "
        '[{"index": n, "pass": true, "reason": "..."}].'
    )

    if args_judge_cmd:
        p = subprocess.run(shlex.split(args_judge_cmd), input=prompt,
                           capture_output=True, text=True)
        return _parse_judge(p.stdout)

    import os
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        import urllib.request
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps({
                "model": os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
                "max_tokens": 1200,
                "messages": [{"role": "user", "content": prompt}],
            }).encode(),
            headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                     "content-type": "application/json"},
        )
        body = urllib.request.urlopen(req, timeout=60).read().decode()
        return _parse_judge(json.loads(body)["content"][0]["text"])

    return {}


def _parse_judge(text: str) -> dict[int, dict]:
    try:
        m = re.search(r"\[.*\]", text, re.S)
        rows = json.loads(m.group(0))
        return {int(r["index"]): {"pass": bool(r["pass"]), "reason": r.get("reason", "")}
                for r in rows}
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# setup + run


def setup(eid: int, dst: str | Path):
    dst = Path(dst)
    dst.mkdir(parents=True, exist_ok=True)
    for src, rel in SETUP[eid]:
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(FIXTURES / src, target)
    return dst


def run(eid: int, command: str):
    ev = get_eval(eid)
    run_dir = RUNS / str(eid)
    if run_dir.exists():
        shutil.rmtree(run_dir)
    setup(eid, run_dir)

    proc = subprocess.run(shlex.split(command), input=ev["prompt"],
                          cwd=run_dir, capture_output=True, text=True)
    transcript = proc.stdout

    (run_dir / "transcript.txt").write_text(transcript, encoding="utf-8")
    (run_dir / "tree.txt").write_text(
        subprocess.run(["find", str(run_dir), "-not", "-path", "*/.git/*"],
                       capture_output=True, text=True).stdout,
        encoding="utf-8")
    if (run_dir / ".git").exists():
        subprocess.run(["git", "-C", str(run_dir), "log", "--oneline"],
                       capture_output=True)
    return transcript, run_dir


def report(results: list[dict], eid: int):
    pmap = {"pass": "PASS", "fail": "FAIL", "unjudged": "  ? "}
    print(f"eval {eid}: {get_eval(eid)['prompt'][:70]}…")
    for r in results:
        tag = pmap.get(r["verdict"], r["verdict"])
        note = f"  ({r.get('note')})" if r.get("note") else ""
        print(f"  [{tag}] {r['assertion'][:80]}{note}")
    n_pass = sum(1 for r in results if r["verdict"] == "pass")
    n_fail = sum(1 for r in results if r["verdict"] == "fail")
    n_unjudged = sum(1 for r in results if r["verdict"] == "unjudged")
    print(f"  {n_pass} pass, {n_fail} fail, {n_unjudged} unjudged, "
          f"{len(results)} total")


# ---------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="list evals")
    p.set_defaults(fn=lambda a: [print(e["id"], "-", e["prompt"][:70])
                                 for e in evals()])

    p = sub.add_parser("setup", help="lay out an eval's fixtures")
    p.add_argument("eval", type=int)
    p.add_argument("dst")
    p.set_defaults(fn=lambda a: (setup(a.eval, a.dst),
                                 print(f"fixtures -> {a.dst}")))

    p = sub.add_parser("grade", help="score a transcript / run dir")
    p.add_argument("eval", type=int)
    p.add_argument("--transcript", help="file with the agent's output")
    p.add_argument("--run-dir", help="case project root after the run")
    p.add_argument("--judge-cmd", help="command that scores semantic assertions")
    p.set_defaults(fn=_cmd_grade)

    p = sub.add_parser("run", help="run an agent headlessly and grade")
    p.add_argument("eval", type=int)
    p.add_argument("--command", required=True,
                   help="agent command that reads the prompt on stdin, e.g. 'claude -p -'")
    p.add_argument("--judge-cmd")
    p.set_defaults(fn=_cmd_run)

    args = ap.parse_args()
    global args_judge_cmd
    args_judge_cmd = getattr(args, "judge_cmd", None)
    args.fn(args)


def _cmd_grade(a):
    t = _text_of(Path(a.transcript).read_text(encoding="utf-8")) if a.transcript else ""
    root = Path(a.run_dir) if a.run_dir else None
    results = grade(a.eval, t, root)
    # judge the semantic ones if a judge is configured
    unjudged = [r for r in results if r["verdict"] == "unjudged"]
    verdicts = judge(t, [{"index": r["index"], "assertion": r["assertion"]}
                         for r in unjudged]) if unjudged else {}
    for r in results:
        if r["verdict"] == "unjudged" and r["index"] in verdicts:
            v = verdicts[r["index"]]
            r["verdict"] = "pass" if v["pass"] else "fail"
            r["method"] = "judge"
            r["note"] = v.get("reason", "")
    report(results, a.eval)


def _cmd_run(a):
    transcript, run_dir = run(a.eval, a.command)
    print(f"transcript + tree saved under {run_dir}")
    (run_dir / "transcript.txt").write_text(transcript, encoding="utf-8")
    _cmd_grade(a)


if __name__ == "__main__":
    main()