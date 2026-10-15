---
description: Review and prune Super-Memory's stored facts
---

List every fact Super-Memory currently holds, so the user can keep it clean.

1. Read `MEMORY.md` in the memory directory (default `~/.super-memory/memories/`,
   or `$SUPER_MEMORY_DIR`). Show the facts between the `super-memory` markers as a
   numbered list: title — hook.
2. For any fact the user says is stale, wrong, or noise, delete its `.md` file
   (only files tagged `managed_by: super-memory`).
3. Regenerate the index by running the applier with empty input:
   `echo '{"memories":[]}' | python3 <repo>/lib/apply.py "$SUPER_MEMORY_DIR"`.
4. Report what was removed and what remains. Be concise.

Never touch files that are not tagged `managed_by: super-memory`.
