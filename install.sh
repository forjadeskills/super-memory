#!/usr/bin/env bash
#
# Super-Memory installer for Claude Code.
#
# Safe by default: it installs the skill + the auto-capture hook, and points the
# memory at a SANDBOX folder (~/.super-memory/memories) so you can watch what it
# writes before trusting it with your real memory. Nothing you already have is
# modified except an additive entry in ~/.claude/settings.json (backed up first).

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SKILLS_DIR="$CLAUDE_DIR/skills"
COMMANDS_DIR="$CLAUDE_DIR/commands"
SETTINGS="$CLAUDE_DIR/settings.json"
MEM_DIR="${SUPER_MEMORY_DIR:-$HOME/.super-memory/memories}"

echo "Super-Memory — installing"
echo "  repo:     $REPO"
echo "  memories: $MEM_DIR"
echo

mkdir -p "$SKILLS_DIR" "$COMMANDS_DIR" "$MEM_DIR" "$CLAUDE_DIR"
chmod +x "$REPO/hooks/super-memory-capture.sh"

# 1. Skill + review command (symlink so `git pull` keeps them current).
ln -sfn "$REPO/skills/super-memory" "$SKILLS_DIR/super-memory"
ln -sfn "$REPO/commands/memory-review.md" "$COMMANDS_DIR/memory-review.md"
echo "  installed skill  -> $SKILLS_DIR/super-memory"
echo "  installed command-> /memory-review"

# 2. Register the Stop hook in settings.json (additive, de-duplicated, backed up).
HOOK_CMD="$REPO/hooks/super-memory-capture.sh"
[ -f "$SETTINGS" ] && cp "$SETTINGS" "$SETTINGS.bak.$(date +%s)"

HOOK_CMD="$HOOK_CMD" SETTINGS="$SETTINGS" python3 - <<'PY'
import json, os

settings_path = os.environ["SETTINGS"]
hook_cmd = os.environ["HOOK_CMD"]

try:
    with open(settings_path) as fh:
        cfg = json.load(fh)
except (OSError, ValueError):
    cfg = {}

hooks = cfg.setdefault("hooks", {})
stop = hooks.setdefault("Stop", [])

# Already present? do nothing.
present = any(
    h.get("command") == hook_cmd
    for group in stop
    for h in group.get("hooks", [])
)
if not present:
    stop.append({"hooks": [{"type": "command", "command": hook_cmd}]})

with open(settings_path, "w") as fh:
    json.dump(cfg, fh, indent=2)
    fh.write("\n")
print("  registered Stop hook in", settings_path)
PY

echo
echo "Done. Auto-capture runs when a Claude Code session ends."
echo "Memories + index will appear in: $MEM_DIR"
echo
echo "Point it at a different folder any time with:"
echo "  export SUPER_MEMORY_DIR=/path/to/memories"
echo
echo "Uninstall: remove the Stop entry from $SETTINGS and delete the symlinks above."
