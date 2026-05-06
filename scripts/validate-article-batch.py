#!/usr/bin/env python3
"""Validate a Help Center Article Factory batch YAML.

Usage:
    scripts/validate-article-batch.py process/batches/<file>.yml

Exit 0 on pass, 1 on hard fails, 2 on script error.

Checks:
- batch size <= 10
- no duplicate slug
- batch_id, workflow, mode declared at top level
- workflow == "article-v2" (only supported value today)
- each article has: slug, priority, audience, job_to_be_done, source_hints
- mode in {v2_rewrite, new_article, minor_edit}
- audience in {seller_br, buyer_br, both}
- if mode != new_article, articles/<slug> directory exists
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

VALID_MODES = {"v2_rewrite", "new_article", "minor_edit"}
VALID_AUDIENCES = {"seller_br", "buyer_br", "both"}
SUPPORTED_WORKFLOWS = {"article-v2"}
MAX_BATCH_SIZE = 10


def fail_list(msgs: list[str]) -> int:
    for m in msgs:
        print(f"FAIL {m}", file=sys.stderr)
    return 1


def validate_article(idx: int, art: Any, batch_mode: str) -> list[str]:
    fails: list[str] = []
    where = f"articles[{idx}]"

    if not isinstance(art, dict):
        return [f"{where}: must be a mapping"]

    slug = art.get("slug")
    if not isinstance(slug, str) or not slug:
        fails.append(f"{where}: missing or empty 'slug'")
    elif slug != slug.strip().lower().replace(" ", "-"):
        fails.append(f"{where}: slug={slug!r} must be lowercase-kebab")

    priority = art.get("priority")
    if not isinstance(priority, int) or priority < 1:
        fails.append(f"{where}: priority must be a positive integer (got {priority!r})")

    audience = art.get("audience")
    if audience not in VALID_AUDIENCES:
        fails.append(f"{where}: audience={audience!r} must be one of {sorted(VALID_AUDIENCES)}")

    jtbd = art.get("job_to_be_done")
    if not isinstance(jtbd, str) or not jtbd.strip():
        fails.append(f"{where}: job_to_be_done is required and must be non-empty")

    if "source_hints" not in art:
        fails.append(f"{where}: source_hints is required (can be empty arrays)")
    else:
        hints = art["source_hints"]
        if not isinstance(hints, dict):
            fails.append(f"{where}: source_hints must be a mapping")
        else:
            for k in ("ios_files", "backend_files"):
                if k in hints and not isinstance(hints[k], list):
                    fails.append(f"{where}: source_hints.{k} must be a list (got {type(hints[k]).__name__})")

    article_mode = art.get("mode") or batch_mode
    if article_mode not in VALID_MODES:
        fails.append(f"{where}: mode={article_mode!r} must be one of {sorted(VALID_MODES)}")
    elif article_mode != "new_article" and isinstance(slug, str) and slug:
        if not (ARTICLES_DIR / slug).is_dir():
            fails.append(
                f"{where}: mode={article_mode!r} but articles/{slug} does not exist "
                f"(use mode=new_article for greenfield articles)"
            )

    return fails


def validate_batch(path: Path) -> list[str]:
    fails: list[str] = []

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"could not read {path}: {exc}"]

    try:
        data = yaml.safe_load(text) or {}
    except yaml.YAMLError as exc:
        return [f"could not parse {path}: {exc}"]

    if not isinstance(data, dict):
        return [f"{path.name}: top-level must be a mapping"]

    batch_id = data.get("batch_id")
    if not isinstance(batch_id, str) or not batch_id:
        fails.append("batch_id is required (non-empty string)")

    workflow = data.get("workflow")
    if workflow not in SUPPORTED_WORKFLOWS:
        fails.append(f"workflow={workflow!r} must be one of {sorted(SUPPORTED_WORKFLOWS)}")

    mode = data.get("mode")
    if mode not in VALID_MODES:
        fails.append(f"mode={mode!r} must be one of {sorted(VALID_MODES)}")

    articles = data.get("articles")
    if not isinstance(articles, list):
        return fails + ["articles must be a list"]

    if len(articles) == 0:
        fails.append("articles list is empty")
    if len(articles) > MAX_BATCH_SIZE:
        fails.append(f"batch size {len(articles)} exceeds max {MAX_BATCH_SIZE}")

    seen_slugs: set[str] = set()
    for i, art in enumerate(articles):
        slug = art.get("slug") if isinstance(art, dict) else None
        fails.extend(validate_article(i, art, mode if isinstance(mode, str) else "v2_rewrite"))
        if isinstance(slug, str) and slug:
            if slug in seen_slugs:
                fails.append(f"articles[{i}]: duplicate slug {slug!r} in batch")
            seen_slugs.add(slug)

    return fails


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an article batch YAML")
    parser.add_argument("path", help="path to a batch YAML file")
    args = parser.parse_args()

    path = Path(args.path).resolve()
    if not path.is_file():
        print(f"ERROR: {args.path} not found", file=sys.stderr)
        return 2

    fails = validate_batch(path)
    if fails:
        return fail_list(fails)
    try:
        rel = path.relative_to(REPO_ROOT)
    except ValueError:
        rel = path
    print(f"OK {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
