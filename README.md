# 🧠 Super-Memory

**Low-noise, automatic long-term memory for Claude Code.**

Most memory tools for coding agents record *everything* and hope the important
bits survive the noise. Super-Memory does the opposite: it remembers the way a
careful human curator would — **one clean fact per file, and nothing else** —
and it fills in **automatically** at the end of every session.

- 🤫 **Quiet by design.** If a session had nothing worth remembering, nothing is
  written. No transcript dumps, no "every tool call."
- 🏠 **100% local & private.** Runs on your machine. No cloud account, no API key
  beyond the Claude CLI you already use. Secrets are scrubbed before anything
  hits disk.
- ✍️ **Writes like you would.** One fact, one sentence, with the *why*. Four
  honest categories: who you are, how you like to work, project state, and
  pointers to resources.
- 🔁 **Updates instead of piling up.** A new fact that contradicts an old one
  replaces it. Your memory stays small and true.
- 🧰 **Works everywhere Claude Code does** — any project, any repo.
- 🆓 **Free and open (MIT).** Built to help people just starting out with AI
  coding keep a clean memory without any busywork.

## How it works

1. A `Stop` hook fires when your Claude Code session ends.
2. It hands the transcript + your current memory index to a small, cheap model
   with one job: distill durable facts, following strict low-noise rules.
3. The model returns a short list of create / update / delete operations.
4. A tiny dependency-free Python script applies them safely — it **only** ever
   touches files it created, and only rewrites its own block of the index.

That's it. No database to run, no service to babysit.

## Install

Requires the [Claude Code](https://claude.com/claude-code) CLI.

### Option A — as a plugin (recommended, one command)

Inside Claude Code:

```
/plugin marketplace add fabio-reboucas/super-memory
/plugin install super-memory@super-memory
```

That's it — the skill, the `/memory-review` command, and the auto-capture hook
all come with it. Memories go to `~/.super-memory/memories/` by default.

### Option B — manual (clone + install script)

```bash
git clone https://github.com/fabio-reboucas/super-memory.git
cd super-memory
bash install.sh
```

> Use **one** method, not both — otherwise the capture hook runs twice.

The installer adds the skill, a `/memory-review` command, and the auto-capture
hook. By default your memories land in a sandbox folder
(`~/.super-memory/memories/`) so you can see exactly what it writes before you
trust it. Point it anywhere with:

```bash
export SUPER_MEMORY_DIR="$HOME/.super-memory/memories"   # change as you like
export SUPER_MEMORY_MODEL="claude-haiku-4-5"             # the distiller model
```

## Using it

- **Recall** happens when you (or Claude) read `MEMORY.md` at the start of work.
- **Writing** happens automatically at session end — or on demand via the
  `super-memory` skill.
- **Pruning**: run `/memory-review` to list every stored fact and delete any you
  don't want.

## What it will and won't remember

**Will:** your role and stable preferences, how you want Claude to work (with the
reason), ongoing project decisions and constraints that aren't in the code, and
pointers to dashboards / tickets / URLs.

**Won't:** anything it could re-derive from your code or git history, one-off
chatter, secrets or credentials, or a near-duplicate of something it already
knows.

## Safety

- Hand-written memory files are never read, moved, or deleted. The tool only
  touches files tagged `managed_by: super-memory`.
- In `MEMORY.md` it only rewrites the block between its own markers.
- `settings.json` is backed up before the hook is registered.
- Secret-looking strings (API keys, tokens, JWTs, passwords) are redacted.

---

### Em português 🇧🇷

Super-Memory é uma **memória automática e limpa** para o Claude Code. Ela grava
sozinha, ao fim de cada sessão, **só os fatos que valem a pena** — uma frase por
fato, sem lixo — e roda **100% na sua máquina**. Feita pra ajudar quem está
começando no "vibe coding" a ter memória de verdade sem trabalho manual.
Instale com `bash install.sh` e pronto.

---

## License

MIT — see [LICENSE](LICENSE). Contributions welcome.
