#!/usr/bin/env python3
"""Regression tests for run-help-article-batch.py and render-reviewer-pack.py.

Mirrors the style of scripts/test-article-factory.py:
- subprocess invocations of the scripts under test
- temp YAML fixtures + checked-in JSON fixtures under tests/fixtures/
- clear PASS / FAIL lines, exit 1 on any failure

What is tested:
- prepare mode: dry-run path with the 1-article and 3-article fixtures
- prepare mode: 4-article batch rejected with exit 2 + human message
- prepare mode: duplicate-slug batch rejected with exit 2
- review mode renderer: ready summary -> exit 0, summary.html structure
- review mode renderer: hard-fail summary -> red badge in HTML
- review mode renderer: missing-PNG summary -> blocker visible in HTML
- summary.html shape: scorecard table + 4 reviewer questions

What is NOT tested in CI:
- real `git worktree add` against origin/main (would require fetched repo
  state). The dry-run path covers preflight and contract semantics; the
  worktree primitives are a thin shell over `git worktree add`, exercised
  manually before opening this PR.

Usage:
    scripts/test-batch-coordinator.py             # run all tests
    scripts/test-batch-coordinator.py --quiet     # only print failures + summary
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
COORDINATOR = SCRIPTS_DIR / "run-help-article-batch.py"
RENDER_PACK = SCRIPTS_DIR / "render-reviewer-pack.py"
FIX = REPO_ROOT / "tests" / "fixtures" / "batch-coordinator"


def _run(args: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(
        args,
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else str(REPO_ROOT),
    )
    return proc.returncode, proc.stdout, proc.stderr


# ---------------------------------------------------------------
# prepare mode tests
# ---------------------------------------------------------------

def test_prepare_one_article_dry_run_succeeds() -> None:
    rc, out, err = _run(
        [
            sys.executable,
            str(COORDINATOR),
            "--mode", "prepare",
            "--batch", str(FIX / "batch-1.yml"),
            "--worktree-base", "/tmp/wt-batch-fixture-1",
            "--dry-run",
        ]
    )
    assert rc == 0, f"prepare 1-article dry-run failed: rc={rc} err={err}"
    assert "fixture-batch-1" in out, f"missing batch_id in output:\n{out}"
    assert "wishlist-and-favorites" in out, f"missing slug in output:\n{out}"
    assert "would-create" in out, f"dry-run did not mark would-create:\n{out}"


def test_prepare_three_articles_dry_run_succeeds() -> None:
    rc, out, err = _run(
        [
            sys.executable,
            str(COORDINATOR),
            "--mode", "prepare",
            "--batch", str(FIX / "batch-3.yml"),
            "--worktree-base", "/tmp/wt-batch-fixture-3",
            "--dry-run",
        ]
    )
    assert rc == 0, f"prepare 3-article dry-run failed: rc={rc} err={err}"
    for slug in ("direct-messages-for-sellers", "wishlist-and-favorites", "notification-settings"):
        assert slug in out, f"missing slug {slug!r} in output:\n{out}"
    assert out.count("would-create") == 3, f"expected 3 would-create lines, got:\n{out}"


def test_prepare_four_articles_rejected_with_cap_message() -> None:
    rc, out, err = _run(
        [
            sys.executable,
            str(COORDINATOR),
            "--mode", "prepare",
            "--batch", str(FIX / "batch-4-rejects.yml"),
            "--worktree-base", "/tmp/wt-batch-fixture-4",
            "--dry-run",
        ]
    )
    assert rc == 2, f"4-article batch should exit 2, got rc={rc}"
    combined = out + err
    assert "coordinator cap is 3" in combined.lower() or "cap is 3" in combined.lower(), (
        f"missing cap rationale in stderr:\n{combined}"
    )


def test_prepare_duplicate_slug_rejected() -> None:
    rc, out, err = _run(
        [
            sys.executable,
            str(COORDINATOR),
            "--mode", "prepare",
            "--batch", str(FIX / "batch-dup-rejects.yml"),
            "--worktree-base", "/tmp/wt-batch-fixture-dup",
            "--dry-run",
        ]
    )
    assert rc == 2, f"duplicate slug must reject with exit 2, got rc={rc}"


def test_prepare_existing_worktree_path_without_force_clean() -> None:
    """When --worktree-base/<slug> already exists and --force-clean is not
    passed, prepare should refuse rather than silently overwrite."""
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "batch"
        existing = base / "wishlist-and-favorites"
        existing.mkdir(parents=True)
        (existing / "marker").write_text("hands off", encoding="utf-8")

        # Run a non-dry-run prepare so the conflict is actually checked.
        # The test doesn't need a real git base ref because prepare_worktree()
        # bails before calling git when the path exists and force_clean is False.
        rc, out, err = _run(
            [
                sys.executable,
                str(COORDINATOR),
                "--mode", "prepare",
                "--batch", str(FIX / "batch-1.yml"),
                "--worktree-base", str(base),
                "--base-ref", "HEAD",
            ]
        )
        # Returns 1 (one slug failed), surfaces exit 3 from prepare_worktree
        # in the per-slug section. Either way, the marker file must survive.
        assert rc != 0, f"prepare should fail when path exists, got rc={rc}"
        assert (existing / "marker").exists(), "marker file was clobbered"


# ---------------------------------------------------------------
# render-reviewer-pack tests
# ---------------------------------------------------------------

def _render(json_in: Path, out_dir: Path) -> tuple[int, Path, str, str]:
    out = out_dir / "summary.html"
    rc, stdout, stderr = _run(
        [
            sys.executable,
            str(RENDER_PACK),
            "--input", str(json_in),
            "--output", str(out),
        ]
    )
    return rc, out, stdout, stderr


def test_render_ready_summary_produces_html_with_scorecard_and_questions() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        rc, html, stdout, stderr = _render(FIX / "sample-summary-ready.json", Path(tmp))
        assert rc == 0, f"render failed: rc={rc} stderr={stderr}"
        assert html.exists(), "summary.html not produced"
        body = html.read_text(encoding="utf-8")
        assert "<table class=\"scorecard\">" in body, "scorecard table missing"
        assert "READY" in body, "ready badge missing"
        assert "Reviewer questions" in body, "reviewer-questions block missing"
        # The 4 questions from the spec.
        assert "Tone, pt-BR" in body
        assert "Mockups" in body
        assert "Factual claims" in body
        assert "Publishable in Intercom today" in body


def test_render_hardfail_summary_marks_blocked_in_html() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        rc, html, stdout, stderr = _render(FIX / "sample-summary-hardfail.json", Path(tmp))
        assert rc == 0, f"render failed: rc={rc} stderr={stderr}"
        body = html.read_text(encoding="utf-8")
        assert "BLOCKED" in body, "blocked badge missing"
        assert "validate exit 1" in body, "blocker reason missing"
        assert "audit_missing" in body, "validator output missing from <pre>"


def test_render_missing_png_summary_lists_missing_pngs() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        rc, html, stdout, stderr = _render(FIX / "sample-summary-missing-png.json", Path(tmp))
        assert rc == 0, f"render failed: rc={rc} stderr={stderr}"
        body = html.read_text(encoding="utf-8")
        assert "Missing mockup PNGs" in body, "missing-PNG section absent"
        assert "screen-x__en" in body, "specific missing PNG not listed"


def test_render_three_articles_all_present_in_scorecard() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        rc, html, stdout, stderr = _render(FIX / "sample-summary-3articles.json", Path(tmp))
        assert rc == 0, f"render failed: rc={rc} stderr={stderr}"
        body = html.read_text(encoding="utf-8")
        for slug in ("direct-messages-for-sellers", "wishlist-and-favorites", "notification-settings"):
            assert slug in body, f"slug {slug!r} missing from pack"
        # Mixed status: 2 ready + 1 blocked in the fixture.
        assert body.count(">READY<") >= 2
        assert body.count(">BLOCKED<") >= 1


def test_render_summary_includes_4_reviewer_questions_in_order() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        rc, html, stdout, stderr = _render(FIX / "sample-summary-ready.json", Path(tmp))
        assert rc == 0, f"render failed: rc={rc} stderr={stderr}"
        body = html.read_text(encoding="utf-8")
        # Strict order: tone -> mockups -> factual -> publishable.
        idx_tone = body.find("Tone, pt-BR")
        idx_mock = body.find("<b>Mockups.")
        idx_fact = body.find("Factual claims")
        idx_pub = body.find("Publishable in Intercom today")
        assert 0 < idx_tone < idx_mock < idx_fact < idx_pub, (
            f"reviewer questions out of order: tone={idx_tone} mock={idx_mock} "
            f"fact={idx_fact} pub={idx_pub}"
        )


def test_render_html_is_self_contained_no_external_js() -> None:
    """Reviewer pack must be a static page with no <script> tags or
    external fetch dependencies. Confirms the no-server constraint."""
    with tempfile.TemporaryDirectory() as tmp:
        rc, html, stdout, stderr = _render(FIX / "sample-summary-3articles.json", Path(tmp))
        assert rc == 0, f"render failed: rc={rc} stderr={stderr}"
        body = html.read_text(encoding="utf-8")
        assert "<script" not in body.lower(), "reviewer pack must contain no <script> tags"
        assert "<form" not in body.lower(), "reviewer pack must contain no <form> tags"


# ---------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------

TESTS = [
    test_prepare_one_article_dry_run_succeeds,
    test_prepare_three_articles_dry_run_succeeds,
    test_prepare_four_articles_rejected_with_cap_message,
    test_prepare_duplicate_slug_rejected,
    test_prepare_existing_worktree_path_without_force_clean,
    test_render_ready_summary_produces_html_with_scorecard_and_questions,
    test_render_hardfail_summary_marks_blocked_in_html,
    test_render_missing_png_summary_lists_missing_pngs,
    test_render_three_articles_all_present_in_scorecard,
    test_render_summary_includes_4_reviewer_questions_in_order,
    test_render_html_is_self_contained_no_external_js,
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Regression tests for the batch coordinator")
    parser.add_argument("--quiet", action="store_true", help="only print failures")
    args = parser.parse_args()

    failures: list[tuple[str, str]] = []
    for fn in TESTS:
        name = fn.__name__
        try:
            fn()
        except AssertionError as exc:
            failures.append((name, str(exc) or "AssertionError"))
            print(f"FAIL {name}: {exc}", file=sys.stderr)
        except Exception as exc:
            failures.append((name, f"{type(exc).__name__}: {exc}"))
            print(f"ERROR {name}: {type(exc).__name__}: {exc}", file=sys.stderr)
        else:
            if not args.quiet:
                print(f"PASS {name}")

    total = len(TESTS)
    print(f"\nRan {total} test(s): {total - len(failures)} pass, {len(failures)} fail")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
