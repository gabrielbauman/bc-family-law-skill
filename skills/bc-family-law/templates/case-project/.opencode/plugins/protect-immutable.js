// Guard the case record: block edits to EXISTING files under evidence/,
// filings/, and correspondence/ — those folders are extracted FROM, never
// edited. Creating a NEW file there (intake) is allowed.
//
// This is the OpenCode equivalent of the Claude Code PreToolUse hook in
// .claude/settings.json + .claude/hooks/protect-immutable.py. Like that
// hook, the git pre-commit guard (.githooks/pre-commit) is the tool-agnostic
// backstop; this plugin adds the same early block for OpenCode sessions.
//
// A deliberate, user-confirmed replacement of a source is legitimate: create
// the new file and commit it with `git commit --no-verify` so the git guard
// allows it.

import { join, isAbsolute, normalize } from "node:path"
import { existsSync } from "node:fs"

export const ProtectImmutable = async ({ directory, worktree }) => {
  const root = worktree ?? directory ?? process.cwd()
  const IMMUTABLE = ["evidence", "filings", "correspondence"]

  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool !== "edit" && input.tool !== "write") return

      const raw = output.args?.filePath ?? output.args?.path
      if (!raw) return

      const path = normalize(isAbsolute(raw) ? raw : join(root, raw)).replace(/\\/g, "/")
      const folder = IMMUTABLE.find((f) => path.split("/").includes(f))

      if (folder && existsSync(path)) {
        throw new Error(
          `${folder}/ is immutable — it is the case record. Extract FROM it ` +
            "into research/; never edit or overwrite it. Adding new files is " +
            "fine. For a deliberate, user-confirmed replacement, commit with " +
            "`git commit --no-verify`.",
        )
      }
    },
  }
}