#!/usr/bin/env python3
"""PreToolUse guard: keep the record folders immutable.

Wired from .claude/settings.json on Edit and Write. Reads the tool call on
stdin and denies it only when the target is an EXISTING file under evidence/,
filings/, or correspondence/ — those folders are the case record and are
extracted FROM, never edited. Creating a NEW file there is how intake files
things, so it is allowed.

Relative paths are resolved against CLAUDE_PROJECT_DIR (not the hook's CWD),
so a relative file_path cannot slip past the guard. The user replacing a
source they have confirmed is legitimate; let that through at the git layer
with `git commit --no-verify` (see .githooks/pre-commit).
"""

import json
import os
import sys

IMMUTABLE = ("evidence", "filings", "correspondence")


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # nothing parseable — don't get in the way

    raw = (data.get("tool_input") or {}).get("file_path", "")
    if not raw:
        sys.exit(0)

    # Resolve against the project root, never the hook's CWD, so a relative
    # file_path still lands inside the guarded folders before we test it.
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    path = raw if os.path.isabs(raw) else (
        os.path.join(project_dir, raw) if project_dir else os.path.abspath(raw)
    )
    parts = os.path.normpath(path).replace("\\", "/").split("/")

    folder = next((f for f in IMMUTABLE if f in parts), None)
    if folder is None:
        sys.exit(0)

    # New intake files are allowed; only existing record files are protected.
    if os.path.exists(path):
        deny(
            f"{folder}/ is immutable — it is the case record, and editing it "
            "destroys provenance. Extract what you need FROM it into research/ "
            "instead. If the user has confirmed a deliberate replacement of "
            "this source, make the new file and commit with `git commit "
            "--no-verify` so the git guard allows it."
        )

    sys.exit(0)


if __name__ == "__main__":
    main()