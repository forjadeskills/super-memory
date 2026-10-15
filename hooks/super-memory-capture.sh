#!/usr/bin/env bash
#
# Super-Memory capture hook.
#
# Runs when a Claude Code session ends (a "Stop" hook). It asks a small, cheap
# model to distill the finished session into clean one-fact memories, then
# applies them to your memory directory. Silent by design: if nothing is worth
# remembering, nothing is written.
#
# It never touches hand-written memory files — see lib/apply.py.

set -euo pipefail

# --- 1. Never run inside our own distiller call (recursion guard) ----------
if [ -n "${SUPER_MEMORY_RUNNING:-}" ]; then
  exit 0
fi

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$HERE")"

# --- 2. Config (override via env) ------------------------------------------
MEM_DIR="${SUPER_MEMORY_DIR:-$HOME/.super-memory/memories}"
MODEL="${SUPER_MEMORY_MODEL:-claude-haiku-4-5}"
MAX_BYTES="${SUPER_MEMORY_MAX_BYTES:-200000}"   # tail of transcript to read
CLAUDE_BIN="${SUPER_MEMORY_CLAUDE_BIN:-claude}"

mkdir -p "$MEM_DIR"

# --- 3. Read the hook payload from stdin -----------------------------------
INPUT="$(cat || true)"
TRANSCRIPT="$(printf '%s' "$INPUT" | python3 -c \
  'import sys,json;
try:
    print(json.load(sys.stdin).get("transcript_path",""))
except Exception:
    print("")' 2>/dev/null || true)"

[ -z "$TRANSCRIPT" ] || [ ! -f "$TRANSCRIPT" ] && exit 0

# Skip trivially short sessions — not worth a model call.
LINES="$(wc -l < "$TRANSCRIPT" 2>/dev/null || echo 0)"
if [ "$LINES" -lt 4 ]; then
  exit 0
fi

# --- 4. Build the distiller prompt -----------------------------------------
TODAY="$(date +%Y-%m-%d)"
RULES="$(cat "$ROOT/lib/distill-prompt.md")"
INDEX=""
[ -f "$MEM_DIR/MEMORY.md" ] && INDEX="$(cat "$MEM_DIR/MEMORY.md")"
SESSION="$(tail -c "$MAX_BYTES" "$TRANSCRIPT")"

PROMPT="$RULES

## Session date
$TODAY

## Current memory index (for update/dedup decisions)
$INDEX

## Session transcript (JSONL, may be truncated to the most recent part)
$SESSION

Now output the JSON object."

# --- 5. Distill, then apply ------------------------------------------------
# The guard env var stops this inner Claude call from firing the hook again.
OPS="$(SUPER_MEMORY_RUNNING=1 "$CLAUDE_BIN" -p "$PROMPT" \
        --model "$MODEL" \
        2>/dev/null || true)"

[ -z "$OPS" ] && exit 0

printf '%s' "$OPS" | python3 "$ROOT/lib/apply.py" "$MEM_DIR" || true

exit 0
