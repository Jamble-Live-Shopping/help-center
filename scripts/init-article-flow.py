#!/usr/bin/env python3
"""Bootstrap an article flow.yml from the template + an optional batch entry.

Usage:
    scripts/init-article-flow.py --slug <slug>
    scripts/init-article-flow.py --slug <slug> --from-batch process/batches/<file>.yml
    scripts/init-article-flow.py --slug <slug> --from-batch <file> --dry-run

Writes (or prints, with --dry-run) `articles/<slug>/flow.yml` based on
`process/templates/article-flow.yml`. Pre-fills:

- audience              from batch entry
- job_to_be_done        from batch entry
- source_of_truth.ios_files / backend_files   from batch source_hints
- mockup_plan.screens   placeholders (count = batch.mockup_count_target)

Does NOT generate pt-br.md, en.md, mockups, or audit files. The point is
to stamp the contract; the worker (or skill) fills the rest.

When the article folder already has a flow.yml, this script overwrites it
ONLY when --force is passed; otherwise it exits 1 with a message.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = REPO_ROOT / "articles"
TEMPLATE_PATH = REPO_ROOT / "process" / "templates" / "article-flow.yml"


def load_batch_entry(batch_path: Path, slug: str) -> tuple[dict[str, Any] | None, str | None]:
    """Return (article_entry, batch_mode). batch_mode is the top-level batch.mode."""
    try:
        data = yaml.safe_load(batch_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        print(f"ERROR: cannot read batch {batch_path}: {exc}", file=sys.stderr)
        sys.exit(2)

    batch_mode = data.get("mode") if isinstance(data.get("mode"), str) else None
    for art in data.get("articles") or []:
        if isinstance(art, dict) and art.get("slug") == slug:
            return art, batch_mode
    return None, batch_mode


def render_flow(slug: str, batch_entry: dict[str, Any] | None, batch_mode: str | None) -> str:
    """Render the flow.yml as a YAML string, preserving comments from template."""
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    # Defaults if no batch entry provided
    audience = "seller_br"
    jtbd = ""
    ios_files: list[str] = []
    backend_files: list[str] = []
    mockup_count = 0
    # mode resolution order: article.mode -> batch.mode -> fallback
    mode = "v2_rewrite"
    if batch_mode:
        mode = batch_mode

    if batch_entry:
        audience = batch_entry.get("audience") or audience
        jtbd = batch_entry.get("job_to_be_done") or ""
        hints = batch_entry.get("source_hints") or {}
        ios_files = list(hints.get("ios_files") or [])
        backend_files = list(hints.get("backend_files") or [])
        try:
            mockup_count = int(batch_entry.get("mockup_count_target") or 0)
        except (TypeError, ValueError):
            mockup_count = 0
        article_mode = batch_entry.get("mode")
        if isinstance(article_mode, str) and article_mode:
            mode = article_mode

    # Substitute mode + audience + job_to_be_done
    text = template
    text = _replace_yaml_field(text, "mode", mode)
    text = _replace_yaml_field(text, "audience", audience)
    text = _replace_yaml_field(text, "job_to_be_done", _yaml_quote(jtbd))

    # Substitute source_of_truth.ios_files and backend_files
    text = _replace_inline_array(text, "  ios_files:", ios_files)
    text = _replace_inline_array(text, "  backend_files:", backend_files)

    # Substitute mockup_plan.screens with placeholders
    if mockup_count > 0:
        screens_block = _build_screens_block(mockup_count)
        text = _replace_screens_block(text, screens_block)

    # Header comment with provenance
    provenance = (
        f"# Generated from process/templates/article-flow.yml by "
        f"scripts/init-article-flow.py\n"
        f"# slug: {slug}\n"
    )
    if batch_entry:
        batch_id = batch_entry.get("_batch_id") or ""
        provenance += f"# batch entry pre-filled audience, job_to_be_done, source_hints, mockup_plan placeholders\n"
    provenance += "#\n"

    return provenance + text


def _yaml_quote(s: str) -> str:
    if not s:
        return '""'
    if any(ch in s for ch in ['"', "\\", "\n"]):
        return yaml.safe_dump(s).strip()
    return f'"{s}"'


def _replace_yaml_field(text: str, key: str, new_value: str) -> str:
    """Replace a single top-level scalar field. Tolerant on whitespace."""
    out_lines = []
    replaced = False
    for line in text.splitlines():
        stripped = line.lstrip()
        if not replaced and stripped.startswith(f"{key}:"):
            indent = line[: len(line) - len(stripped)]
            out_lines.append(f"{indent}{key}: {new_value}")
            replaced = True
        else:
            out_lines.append(line)
    return "\n".join(out_lines) + ("\n" if text.endswith("\n") else "")


def _replace_inline_array(text: str, key_prefix: str, items: list[str]) -> str:
    """Replace `<key_prefix> [empty]` (or `<key_prefix>` followed by indented list)
    with an inline expansion of items. Targets process/templates/article-flow.yml
    style where ios_files: / backend_files: have a comment after."""
    out_lines = []
    in_target = False
    target_indent = ""
    for line in text.splitlines():
        if line.startswith(key_prefix):
            # Replace this line and absorb following list items at greater indent
            stripped = line[len(key_prefix):].rstrip()
            comment = ""
            if "#" in stripped:
                comment = "  " + stripped[stripped.index("#"):]
            target_indent = line[: len(line) - len(line.lstrip())] + "    "
            if not items:
                out_lines.append(f"{key_prefix} []{comment}")
            else:
                out_lines.append(f"{key_prefix}{comment}")
                for it in items:
                    out_lines.append(f"{target_indent[:-2]}- {it}")
            in_target = True
            continue
        if in_target:
            stripped = line.lstrip()
            # Continuation lines (indented or empty) belong to the previous list
            if line.startswith(target_indent[:-2] + "-") or line.strip() == "":
                # Skip the originals
                if line.strip() == "":
                    in_target = False
                    out_lines.append(line)
                continue
            else:
                in_target = False
        out_lines.append(line)
    return "\n".join(out_lines) + ("\n" if text.endswith("\n") else "")


def _build_screens_block(count: int) -> str:
    lines = []
    for i in range(count):
        lines.append(f"    - name: screen-{i+1}")
        lines.append(f"      purpose: \"\"")
        lines.append(f"      source: ios_required")
    return "\n".join(lines)


def _replace_screens_block(text: str, screens_block: str) -> str:
    """Replace the `screens:` block under `mockup_plan:`. The template ships with
    a commented example + an empty list `[]`; we replace from `screens:` up to
    the first non-indented blank line that closes the block."""
    out_lines = []
    in_target = False
    indent = "    "
    for line in text.splitlines():
        if not in_target and line.lstrip().startswith("screens:"):
            indent_match = line[: len(line) - len(line.lstrip())]
            out_lines.append(f"{indent_match}screens:")
            for sb_line in screens_block.splitlines():
                out_lines.append(sb_line)
            in_target = True
            continue
        if in_target:
            stripped = line.lstrip()
            if line.startswith(indent) or stripped.startswith("- ") or stripped.startswith("#") or stripped == "" or stripped == "[]":
                # Skip until we reach a sibling key at the parent indent level
                if line.strip() == "":
                    in_target = False
                    out_lines.append(line)
                continue
            else:
                in_target = False
        out_lines.append(line)
    return "\n".join(out_lines) + ("\n" if text.endswith("\n") else "")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap articles/<slug>/flow.yml")
    parser.add_argument("--slug", required=True, help="article slug (matches folder name)")
    parser.add_argument("--from-batch", help="path to a batch YAML to pre-fill from")
    parser.add_argument("--dry-run", action="store_true", help="print to stdout, do not write")
    parser.add_argument("--force", action="store_true", help="overwrite existing flow.yml")
    args = parser.parse_args()

    slug: str = args.slug.strip()
    if not slug or slug != slug.lower().replace(" ", "-"):
        print(f"ERROR: --slug must be lowercase-kebab (got {args.slug!r})", file=sys.stderr)
        return 2

    article_dir = ARTICLES_DIR / slug
    flow_path = article_dir / "flow.yml"

    batch_entry = None
    batch_mode = None
    if args.from_batch:
        batch_path = Path(args.from_batch).resolve()
        if not batch_path.is_file():
            print(f"ERROR: --from-batch {args.from_batch} not found", file=sys.stderr)
            return 2
        batch_entry, batch_mode = load_batch_entry(batch_path, slug)
        if batch_entry is None:
            print(f"ERROR: slug {slug!r} not in batch {batch_path.name}", file=sys.stderr)
            return 2

    if flow_path.exists() and not args.force and not args.dry_run:
        print(
            f"ERROR: {flow_path.relative_to(REPO_ROOT)} already exists. "
            f"Use --force to overwrite, or --dry-run to preview.",
            file=sys.stderr,
        )
        return 1

    rendered = render_flow(slug, batch_entry, batch_mode)

    if args.dry_run:
        print(rendered)
        return 0

    if not article_dir.exists():
        article_dir.mkdir(parents=True, exist_ok=True)

    flow_path.write_text(rendered, encoding="utf-8")
    print(f"WROTE {flow_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
