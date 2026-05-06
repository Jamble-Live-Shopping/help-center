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
        fails.append(f"{where}: source_hints is required")
    else:
        hints = art["source_hints"]
        if not isinstance(hints, dict):
            fails.append(f"{where}: source_hints must be a mapping")
        else:
            ios_present = "ios_files" in hints
            backend_present = "backend_files" in hints
            if not ios_present:
                fails.append(f"{where}: source_hints.ios_files is required (use [] if none)")
            if not backend_present:
                fails.append(f"{where}: source_hints.backend_files is required (use [] if none)")
            ios_files = hints.get("ios_files") if ios_present else None
            backend_files = hints.get("backend_files") if backend_present else None
            if ios_present and not isinstance(ios_files, list):
                fails.append(f"{where}: source_hints.ios_files must be a list (got {type(ios_files).__name__})")
                ios_files = None
            if backend_present and not isinstance(backend_files, list):
                fails.append(f"{where}: source_hints.backend_files must be a list (got {type(backend_files).__name__})")
                backend_files = None
            # If both lists are present and both empty, require an explicit
            # justification. Empty source_hints with no rationale is a strong
            # smell: every v2 article should be traceable to iOS or backend.
            if (
                isinstance(ios_files, list)
                and isinstance(backend_files, list)
                and len(ios_files) == 0
                and len(backend_files) == 0
            ):
                justification = hints.get("justification")
                if not isinstance(justification, str) or not justification.strip():
                    fails.append(
                        f"{where}: source_hints.ios_files and backend_files are both empty; "
                        f"add source_hints.justification (non-empty string) explaining why "
                        f"the article needs no source of truth (e.g. 'copy-only metadata test')"
                    )

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
    seen_priorities: list[int] = []
    for i, art in enumerate(articles):
        slug = art.get("slug") if isinstance(art, dict) else None
        fails.extend(validate_article(i, art, mode if isinstance(mode, str) else "v2_rewrite"))
        # Collect priority for batch-level uniqueness + ordering checks.
        if isinstance(art, dict):
            pr = art.get("priority")
            if isinstance(pr, int) and pr >= 1:
                seen_priorities.append(pr)
        if isinstance(slug, str) and slug:
            if slug in seen_slugs:
                fails.append(f"articles[{i}]: duplicate slug {slug!r} in batch")
            seen_slugs.add(slug)

    # Batch-level priority checks (run after per-article validation so we
    # only inspect well-formed integers). Priorities must be unique and
    # listed in ascending order.
    if len(seen_priorities) != len(set(seen_priorities)):
        dups = sorted({p for p in seen_priorities if seen_priorities.count(p) > 1})
        fails.append(
            f"duplicate priorities in batch: {dups}; each article must have a unique priority"
        )
    if seen_priorities != sorted(seen_priorities):
        fails.append(
            f"priorities must be listed in ascending order; got {seen_priorities}"
        )

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
