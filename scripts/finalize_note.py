#!/usr/bin/env python3
"""Finalize a NotebookLM report download into a vault-compliant .raw/ Markdown file.

Reads the raw .md produced by `notebooklm download report`, prepends
frontmatter that matches the vault's CLAUDE.md conventions, and writes the
file to <output-dir>/<YYYY-MM-DD>-<slug>.md. Prints the final path on stdout.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


def slugify(text: str, max_len: int = 60) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:max_len].rstrip("-") or "untitled"


def yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def build_frontmatter(
    topic: str,
    notebook_id: str,
    language: str,
    sources: list[dict],
    today: str,
) -> str:
    tags = ["research-pipeline", "notebooklm", f"lang/{language}"]
    lines = [
        "---",
        "type: source",
        "status: raw",
        f"created: {today}",
        f"updated: {today}",
        f'topic: "{yaml_escape(topic)}"',
        f"notebook_id: {notebook_id}",
        f"language: {language}",
        f"tags: [{', '.join(tags)}]",
        "sources:",
    ]
    for s in sources:
        title = yaml_escape(str(s.get("title", "")).strip() or s.get("url", ""))
        url = str(s.get("url", "")).strip()
        lines.append(f'  - title: "{title}"')
        lines.append(f"    url: {url}")
    lines.append("---")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Path to raw .md downloaded from NotebookLM")
    p.add_argument("--topic", required=True)
    p.add_argument("--slug", default=None, help="Optional; derived from topic if omitted")
    p.add_argument("--notebook-id", required=True)
    p.add_argument(
        "--sources-json",
        required=True,
        help="Path to a JSON array of {url, title} for the sources that were added",
    )
    p.add_argument("--output-dir", required=True)
    p.add_argument("--language", default="fr")
    args = p.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"ERROR: input not found: {in_path}", file=sys.stderr)
        return 1

    body = in_path.read_text(encoding="utf-8")

    sources_path = Path(args.sources_json)
    if sources_path.exists():
        sources = json.loads(sources_path.read_text(encoding="utf-8"))
    else:
        sources = []
        print(f"WARNING: sources manifest missing at {sources_path}", file=sys.stderr)

    slug = args.slug or slugify(args.topic)
    today = date.today().isoformat()

    frontmatter = build_frontmatter(
        topic=args.topic,
        notebook_id=args.notebook_id,
        language=args.language,
        sources=sources,
        today=today,
    )

    header = (
        f"\n\n# {args.topic}\n\n"
        f"> Rapport généré par NotebookLM via `research-pipeline`. "
        f"Notebook : `{args.notebook_id}`.\n\n"
    )

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{today}-{slug}.md"
    out_path.write_text(frontmatter + header + body, encoding="utf-8")

    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
