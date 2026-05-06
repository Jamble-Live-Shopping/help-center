#!/usr/bin/env python3
"""Regenerate the committed sample reviewer pack.

The committed sample under `_work/sample-batch/` is the canonical
reference for what a real review session produces. It is built from
the in-repo fixture worktree at
`tests/fixtures/batch-coordinator/sample-worktree/`, which ships real
pt-BR / EN bodies plus tiny 1x1 PNG fixtures.

This script:
  1. assembles a `summary.json` that points at the in-repo fixture
     worktree (paths absolute at generation time),
  2. invokes `scripts/render-reviewer-pack.py` to produce
     `summary.html` with file:// URIs into the developer's local
     clone,
  3. post-processes the HTML so every `file://<repo_root>/` prefix is
     rewritten as a path relative to the output dir
     (`_work/sample-batch/`). The committed sample then opens
     consistently from any clone of the repo, with images and inline
     previews working out of the box.

Run when the renderer template changes or when the fixture bodies are
updated. Idempotent: running twice produces the same HTML byte-for-byte.

Usage:
    python3 scripts/generate-sample-reviewer-pack.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_WORKTREE = REPO_ROOT / "tests" / "fixtures" / "batch-coordinator" / "sample-worktree"
OUTPUT_DIR = REPO_ROOT / "_work" / "sample-batch"
RENDER_PACK = REPO_ROOT / "scripts" / "render-reviewer-pack.py"


def _build_summary() -> dict:
    """Compose a 2-article batch result against the fixture worktree.

    Article #1 is `ready` (clean validate, all mockups, full audit
    triplet). Article #2 is `blocked` to demonstrate the BLOCKED badge
    + blocker list in the same pack.
    """
    wt = str(SAMPLE_WORKTREE)
    return {
        "batch_id": "sample-batch",
        "batch_path": "tests/fixtures/batch-coordinator/sample-worktree/(synthetic)",
        "worktree_base": str(SAMPLE_WORKTREE.parent),
        "articles": [
            {
                "slug": "wishlist-favorites-demo",
                "audience": "buyer_br",
                "intercom_id": 99001,
                "worktree": wt,
                "branch": "feat/sample-wishlist-favorites-demo",
                "validate_returncode": 0,
                "validate_output": (
                    "=== wishlist-favorites-demo ===\n\n"
                    "Validated 1 article(s): 0 hard fail(s), 2 soft warn(s)\n"
                    "  warn  [toc_missing_pt] pt-br.md has 6 H2 sections (>=6) but no TOC.\n"
                    "  warn  [must_answer_en] keyword 'favoritos' not found in en.md\n"
                ),
                "hard_fail_count": 0,
                "soft_warn_count": 2,
                "mockups_declared": 2,
                "mockups_present": 2,
                "missing_mockups": [],
                "audit_files_present": 3,
                "audit_skeleton_unfilled": False,
                "em_dash_count_pt": 0,
                "em_dash_count_en": 0,
                "rdollar_leak_en_count": 0,
                "pt_br_md_path": "articles/wishlist-favorites-demo/pt-br.md",
                "en_md_path": "articles/wishlist-favorites-demo/en.md",
                "mockup_pngs": [
                    "assets/mockups/wishlist-favorites-demo__overview__pt-br__v3.png",
                    "assets/mockups/wishlist-favorites-demo__overview__en__v3.png",
                ],
                "status": "ready",
                "blockers": [],
            },
            {
                "slug": "notification-settings-demo",
                "audience": "both",
                "intercom_id": 99002,
                "worktree": wt,
                "branch": "feat/sample-notification-settings-demo",
                "validate_returncode": 1,
                "validate_output": (
                    "=== notification-settings-demo ===\n\n"
                    "FAIL [em_dash]: pt-br.md has 3 em-dash(es)\n"
                    "Validated 1 article(s): 1 hard fail(s), 1 soft warn(s)\n"
                ),
                "hard_fail_count": 1,
                "soft_warn_count": 1,
                "mockups_declared": 2,
                "mockups_present": 2,
                "missing_mockups": [],
                "audit_files_present": 3,
                "audit_skeleton_unfilled": False,
                "em_dash_count_pt": 3,
                "em_dash_count_en": 0,
                "rdollar_leak_en_count": 0,
                "pt_br_md_path": "articles/notification-settings-demo/pt-br.md",
                "en_md_path": "articles/notification-settings-demo/en.md",
                "mockup_pngs": [
                    "assets/mockups/notification-settings-demo__settings__pt-br__v3.png",
                    "assets/mockups/notification-settings-demo__settings__en__v3.png",
                ],
                "status": "blocked",
                "blockers": ["validate exit 1", "1 validator hard fail(s)"],
            },
        ],
    }


def main() -> int:
    if not SAMPLE_WORKTREE.exists():
        print(f"ERROR: fixture worktree missing: {SAMPLE_WORKTREE}", file=sys.stderr)
        return 2

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary_json = OUTPUT_DIR / "summary.json"
    summary_html = OUTPUT_DIR / "summary.html"

    summary = _build_summary()
    summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(RENDER_PACK), "--input", str(summary_json), "--output", str(summary_html)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        return proc.returncode

    # Post-process: replace every `file://<repo_root>/` prefix with a
    # path relative to the output directory. The committed HTML then
    # opens consistently from any clone of the repo.
    repo_root_uri = REPO_ROOT.as_uri().rstrip("/") + "/"
    rel_prefix = ""  # we want plain relative paths, no scheme.
    # `_work/sample-batch/summary.html` is two directories below the
    # repo root, so the relative ref to the repo root is `../../`.
    relative_to_repo = "../../"

    body = summary_html.read_text(encoding="utf-8")
    body_patched = body.replace(repo_root_uri, relative_to_repo)
    if body_patched == body:
        print(
            "WARN: no file:// URIs were rewritten; the renderer may have "
            "changed and this script needs an update.",
            file=sys.stderr,
        )
    summary_html.write_text(body_patched, encoding="utf-8")

    # Also strip absolute paths from summary.json so the committed
    # JSON does not leak the developer's username. Replace with a
    # repo-relative marker; render-reviewer-pack.py also accepts these
    # shapes when the JSON is hand-edited.
    json_text = summary_json.read_text(encoding="utf-8")
    json_text = json_text.replace(str(SAMPLE_WORKTREE), "{REPO_ROOT}/tests/fixtures/batch-coordinator/sample-worktree")
    json_text = json_text.replace(str(SAMPLE_WORKTREE.parent), "{REPO_ROOT}/tests/fixtures/batch-coordinator")
    summary_json.write_text(json_text, encoding="utf-8")

    print(f"OK regenerated {summary_html} ({summary_html.stat().st_size} bytes)")
    print(f"OK regenerated {summary_json} ({summary_json.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
