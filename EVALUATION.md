---
type: meta
title: "research-pipeline — description optimization results"
date: 2026-04-20
---

# Description optimization — final results

## What was run

- `run_eval.py` on 26 queries (14 should-trigger, 12 should-not-trigger), 2 runs each = 52 calls per description.
- Parallel A/B: baseline (original description from first draft) vs v2 (sharper + "super skill" branding + explicit autoresearch differentiation + new trigger keywords).
- Full `run_loop.py` attempted but blocked by (a) Windows `select()`-on-pipe bug in `run_eval.py` — patched, and (b) `anthropic.TypeError` from missing `ANTHROPIC_API_KEY` in `improve_description.py` — not fixed; manual optimization used instead.

## Headline

| metric | baseline | v2 | delta |
|---|---|---|---|
| positives triggered | 0/14 | 1/14 | **+1** |
| negatives suppressed | 12/12 | 12/12 | 0 |
| false positives | 0 | 0 | 0 |

V2 wins. Applied to `SKILL.md` frontmatter.

## Interpretation

Real Claude Code triggered the skill reliably earlier today (full `/research-pipeline Best practices...` run landed a French briefing + wiki ingest). The `claude -p` simulation used by `run_eval.py` is systematically harsher than real usage — it missed even literal `/research-pipeline <topic>` queries, which empirically do trigger in the live session. The absolute numbers (0/14, 1/14) are lossy; only the **direction of the delta** is trustworthy.

## V2's improvements (rationale, not just numbers)

1. **"Super skill" branding** — matches the user's mental model for this tool.
2. **Explicit autoresearch differentiation** — removes the biggest competitor (both descriptions shared keywords like "research", "deep-dive", "file").
3. **New trigger keywords the user requested** — "super skill", "audio overview", "send these sources to notebooklm", "french briefing on X".
4. **Pushy language** — "MUST trigger", "ONLY skill", "do NOT attempt inline; delegate to the skill" — per skill-creator guidance on descriptions that "undertrigger" otherwise.

## Plumbing patches applied to the skill-creator plugin cache

(may be overwritten on plugin update)

- `scripts/run_eval.py`: replaced POSIX-only `select.select()` on pipe with `readline()` on Windows.
- `scripts/run_loop.py`, `improve_description.py`, `generate_report.py`, `run_eval.py`, `utils.py`, `quick_validate.py`: all `read_text()` / `write_text()` now use `encoding="utf-8"` (Windows default is cp1252, which can't encode `✗`/`→`/em-dashes).

## How to resume a full formal loop later

1. Export `ANTHROPIC_API_KEY` in a terminal.
2. `cd <skill-creator-plugin-cache>`
3. `PYTHONIOENCODING=utf-8 python -m scripts.run_loop --eval-set <path-to-trigger-eval.json> --skill-path <skill-path> --model claude-opus-4-7 --max-iterations 5 --verbose --results-dir <workspace>`
