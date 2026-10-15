---
name: super-memory
description: Persistent, low-noise memory for Claude Code. Use when recalling what you know about this user/project, writing a durable fact worth remembering next session, or reviewing and pruning stored memories. Auto-captures at session end; also works on demand.
---

# Super-Memory

Super-Memory gives Claude Code a long-term memory that reads like a human
curator wrote it: **one clean fact per file, no noise**. It fills in
automatically at the end of each session, and you can also drive it by hand.

Memory lives in `$SUPER_MEMORY_DIR` (default `~/.super-memory/memories/`):
a folder of one-fact `.md` files plus a `MEMORY.md` index.

## Recall (start of work)

Read `MEMORY.md` — it is a one-line-per-fact index. For any line whose hook
looks relevant to the task at hand, open that file and load the fact. Treat
these as background context that was true when written: if a fact names a file,
flag, or value, verify it still exists before relying on it.

## Write a fact (on demand)

Only save something durable and reusable. One fact per file. Keep it tight.
Four types: `user`, `feedback`, `project`, `reference`. Write a file with this
exact frontmatter so the index and the auto-capture tool stay consistent:

```markdown
---
name: kebab-case-slug
title: "Short Human Title"
hook: "one-line hook shown in the index"
description: "one-line relevance summary used to decide recall"
metadata:
  type: project
  managed_by: super-memory
---

The fact, in the user's language. For feedback/project, say why and how to apply.
Link related memories with [[their-slug]].
```

Then regenerate the index: `python3 <repo>/lib/apply.py "$SUPER_MEMORY_DIR"`
with empty input, or just add a matching `- [Title](slug.md) — hook` line inside
the `super-memory` markers in `MEMORY.md`.

Do **not** save: anything derivable from code or git history, one-off chatter,
secrets, or a near-duplicate of an existing fact — update the existing one
instead (same `name`), or delete it if it is now wrong.

## Review / prune

Run `/memory-review` (or read `MEMORY.md`) to see every managed fact. Delete the
file for anything stale and rerun the applier to refresh the index. Only files
tagged `managed_by: super-memory` are ever touched by the tool — hand-written
memories are safe.

## How auto-capture works

A `Stop` hook (`hooks/super-memory-capture.sh`) runs when a session ends. It
sends the transcript and the current index to a small model with the rules in
`lib/distill-prompt.md`, which returns a strict JSON list of create/update/delete
operations. `lib/apply.py` applies them safely. If nothing is worth remembering,
nothing is written. This is the whole point: automatic, but quiet.
