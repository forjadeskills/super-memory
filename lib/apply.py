#!/usr/bin/env python3
"""Super-Memory applier.

Reads a JSON object of memory operations on stdin and applies them to a memory
directory, SAFELY:

  * It only ever touches files it owns (frontmatter `managed_by: super-memory`).
    Hand-written memory files are never read, moved, or deleted.
  * In MEMORY.md it only rewrites the block between its own markers. Everything
    outside the markers is left byte-for-byte untouched.
  * Secrets are scrubbed from every stored body as a second line of defence.

Usage:  apply.py <memory_dir>
Input (stdin):
  {"memories": [
     {"action":"upsert","name":...,"title":...,"hook":...,
      "description":...,"type":...,"body":...},
     {"action":"delete","name":...}
  ]}

Stdlib only — no dependencies, so beginners can read every line.
"""

import json
import os
import re
import sys

MANAGED_TAG = "super-memory"
START = "<!-- super-memory:start (auto-managed, do not edit by hand) -->"
END = "<!-- super-memory:end -->"
VALID_TYPES = {"user", "feedback", "project", "reference"}

# --- secret scrubbing ------------------------------------------------------
# Belt-and-suspenders: the distiller is told not to store secrets, but we also
# redact anything that *looks* like one before it ever hits disk.
SECRET_PATTERNS = [
    re.compile(r"\b(sk|rk)-[A-Za-z0-9]{16,}\b"),          # OpenAI-style keys
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),        # GitHub tokens
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),                  # AWS access key id
    re.compile(r"\bey[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),  # JWT
    re.compile(r"(?i)\b(password|passwd|senha|secret|token|api[_-]?key)\b\s*[:=]\s*\S+"),
    re.compile(r"\b[0-9a-fA-F]{40,}\b"),                  # long hex blobs
]


def scrub(text):
    if not text:
        return text
    for pat in SECRET_PATTERNS:
        text = pat.sub("[REDACTED]", text)
    return text


def slugify(name):
    name = (name or "").strip().lower()
    name = re.sub(r"[^a-z0-9]+", "-", name).strip("-")
    return name or "untitled"


def esc(text):
    """Make a value safe for a single-line YAML frontmatter field."""
    return str(text).replace("\n", " ").replace('"', "'").strip()


def is_managed(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            head = fh.read(400)
        return f"managed_by: {MANAGED_TAG}" in head
    except OSError:
        return False


def write_memory(mem_dir, m):
    name = slugify(m.get("name"))
    mtype = m.get("type", "project")
    if mtype not in VALID_TYPES:
        mtype = "project"
    title = esc(m.get("title") or name)
    hook = esc(scrub(m.get("hook") or ""))
    desc = esc(scrub(m.get("description") or ""))
    body = scrub((m.get("body") or "").strip())

    content = (
        "---\n"
        f"name: {name}\n"
        f'title: "{title}"\n'
        f'hook: "{hook}"\n'
        f'description: "{desc}"\n'
        "metadata:\n"
        f"  type: {mtype}\n"
        f"  managed_by: {MANAGED_TAG}\n"
        "---\n\n"
        f"{body}\n"
    )
    path = os.path.join(mem_dir, f"{name}.md")
    # Never clobber a hand-written file that happens to share the name.
    if os.path.exists(path) and not is_managed(path):
        return None
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return name


def delete_memory(mem_dir, name):
    name = slugify(name)
    path = os.path.join(mem_dir, f"{name}.md")
    if os.path.exists(path) and is_managed(path):
        os.remove(path)
        return name
    return None


def read_frontmatter(path):
    """Tiny frontmatter reader: returns the needed fields for the index."""
    fields = {}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return fields
    if not lines or lines[0].strip() != "---":
        return fields
    for line in lines[1:]:
        if line.strip() == "---":
            break
        mt = re.match(r"\s*([A-Za-z_]+):\s*(.*)$", line)
        if mt:
            key, val = mt.group(1), mt.group(2).strip().strip('"')
            fields[key] = val
    return fields


def rebuild_index(mem_dir):
    """Regenerate ONLY the managed block of MEMORY.md from managed files."""
    rows = []
    for fn in sorted(os.listdir(mem_dir)):
        if not fn.endswith(".md") or fn == "MEMORY.md":
            continue
        path = os.path.join(mem_dir, fn)
        if not is_managed(path):
            continue
        fm = read_frontmatter(path)
        title = fm.get("title") or fm.get("name") or fn[:-3]
        hook = fm.get("hook") or ""
        line = f"- [{title}]({fn})"
        if hook:
            line += f" — {hook}"
        rows.append(line)

    block = START + "\n" + ("\n".join(rows) if rows else "") + "\n" + END

    index_path = os.path.join(mem_dir, "MEMORY.md")
    existing = ""
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as fh:
            existing = fh.read()

    if START in existing and END in existing:
        new = re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            block.replace("\\", "\\\\"),
            existing,
            flags=re.DOTALL,
        )
    else:
        header = existing.rstrip()
        if not header:
            header = "# Memory index\n"
        new = header + "\n\n" + block + "\n"

    with open(index_path, "w", encoding="utf-8") as fh:
        fh.write(new)


def main():
    if len(sys.argv) < 2:
        print("usage: apply.py <memory_dir>", file=sys.stderr)
        return 2
    mem_dir = sys.argv[1]
    os.makedirs(mem_dir, exist_ok=True)

    raw = sys.stdin.read().strip()
    if not raw:
        return 0
    # Be forgiving: pull the first {...} block out if the model added prose.
    mt = re.search(r"\{.*\}", raw, re.DOTALL)
    if not mt:
        return 0
    try:
        data = json.loads(mt.group(0))
    except json.JSONDecodeError:
        return 0

    memories = data.get("memories", [])
    if not isinstance(memories, list):
        return 0

    changed = []
    for m in memories:
        if not isinstance(m, dict):
            continue
        action = m.get("action", "upsert")
        if action == "delete":
            r = delete_memory(mem_dir, m.get("name"))
            if r:
                changed.append(f"- deleted {r}")
        else:
            r = write_memory(mem_dir, m)
            if r:
                changed.append(f"~ saved   {r}")

    rebuild_index(mem_dir)

    if changed:
        print("Super-Memory updated:", file=sys.stderr)
        print("\n".join(changed), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
