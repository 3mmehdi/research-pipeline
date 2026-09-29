#!/usr/bin/env python3
"""Finalize a Zhutov-style Protocole d'Expérimentation into a vault-compliant Markdown file.

Takes the French body produced by the orchestrator in Phase 10, prepends
frontmatter that matches the vault's CLAUDE.md conventions (with a wikilink
back to the source briefing), and writes the file to
<output-dir>/<YYYY-MM-DD>-<slug>-protocole.md. Prints the final path on stdout.
"""
from __future__ import annotations

import argparse
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
    language: str,
    briefing_stem: str,
    today: str,
) -> str:
    tags = ["protocol", "research-pipeline", "zhutov", f"lang/{language}"]
    lines = [
        "---",
        "type: protocol",
        "status: draft",
        f"created: {today}",
        f"updated: {today}",
        f'topic: "{yaml_escape(topic)}"',
        f"language: {language}",
        f'related_briefing: "[[{briefing_stem}]]"',
        f"tags: [{', '.join(tags)}]",
        "---",
    ]
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--body-file", required=True, help="Path to a markdown file containing the protocol body (no frontmatter)")
    p.add_argument("--topic", required=True)
    p.add_argument("--slug", default=None, help="Optional; derived from topic if omitted")
    p.add_argument(
        "--briefing-filename",
        required=True,
        help="Filename of the sibling briefing doc, e.g. 2026-04-20-foo.md — used for the wikilink",
    )
    p.add_argument("--output-dir", required=True)
    p.add_argument("--language", default="fr")
    args = p.parse_args()

    body_path = Path(args.body_file)
    if not body_path.exists():
        print(f"ERROR: body file not found: {body_path}", file=sys.stderr)
        return 1

    body = body_path.read_text(encoding="utf-8").strip()

    slug = args.slug or slugify(args.topic)
    today = date.today().isoformat()
    briefing_stem = Path(args.briefing_filename).stem

    frontmatter = build_frontmatter(
        topic=args.topic,
        language=args.language,
        briefing_stem=briefing_stem,
        today=today,
    )

    header = (
        f"\n\n> Plan d'action généré par `research-pipeline` Phase 10 à partir du briefing "
        f"[[{briefing_stem}]]. À réviser, compléter, et cocher au fil des expérimentations.\n\n"
    )

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{today}-{slug}-protocole.md"
    out_path.write_text(frontmatter + header + body + "\n", encoding="utf-8")

    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
