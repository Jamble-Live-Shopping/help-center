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
import importlib.util
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


def _load_coordinator_module() -> Any:
    """Load run-help-article-batch.py as a module so we can unit-test
    its small helpers without spawning a subprocess.

    Note: must register the module in sys.modules BEFORE exec_module(),
    otherwise the @dataclass decorator cannot resolve cls.__module__
    when ArticleEntry / ArticleReview are evaluated.
    """
    spec = importlib.util.spec_from_file_location("batch_coord", COORDINATOR)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise RuntimeError("cannot load coordinator module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["batch_coord"] = mod
    spec.loader.exec_module(mod)
    return mod


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


def test_prepare_existing_worktree_path_returns_exit_3() -> None:
    """When --worktree-base/<slug> already exists and --force-clean is not
    passed, prepare must refuse with the documented exit code 3 (so a
    caller can scriptably distinguish "path conflict" from a generic
    failure) and the existing files must survive untouched."""
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "batch"
        existing = base / "wishlist-and-favorites"
        existing.mkdir(parents=True)
        (existing / "marker").write_text("hands off", encoding="utf-8")

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
        assert rc == 3, (
            f"existing-path conflict must propagate exit 3, got rc={rc}\n"
            f"stdout:\n{out}\nstderr:\n{err}"
        )
        assert (existing / "marker").exists(), "marker file was clobbered"


def test_prepare_bootstraps_missing_flow_yml() -> None:
    """Non-dry-run end-to-end: when articles/<slug>/flow.yml does not
    exist on the base ref, prepare must auto-bootstrap it via
    init-article-flow.py and emit writer-packet + checklist + brief
    inside the worktree's _work/ folder. Regression for the friction
    point in the original prepare implementation that printed
    "Bootstrap and re-run" and silently moved on."""
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "wt-bootstrap"
        rc, out, err = _run(
            [
                sys.executable,
                str(COORDINATOR),
                "--mode", "prepare",
                "--batch", str(FIX / "batch-1-new-article.yml"),
                "--worktree-base", str(base),
                "--base-ref", "HEAD",
            ]
        )
        try:
            assert rc == 0, f"prepare bootstrap failed: rc={rc}\nstdout:\n{out}\nstderr:\n{err}"
            wt = base / "fixture-bootstrap-article"
            flow = wt / "articles" / "fixture-bootstrap-article" / "flow.yml"
            assert flow.exists(), f"flow.yml not bootstrapped at {flow}"
            assert "fixture-bootstrap-article" in flow.read_text(encoding="utf-8"), (
                "bootstrapped flow.yml does not reference the slug"
            )
            for fname in (
                "fixture-bootstrap-article__writer-packet.md",
                "fixture-bootstrap-article__checklist.md",
                "fixture-bootstrap-article__brief.md",
            ):
                assert (wt / "_work" / fname).exists(), (
                    f"_work/{fname} not produced after bootstrap"
                )
        finally:
            # Tear the worktree down regardless of test outcome so we do
            # not leak branches in the developer's repo.
            wt = base / "fixture-bootstrap-article"
            if wt.exists():
                _run(["git", "worktree", "remove", "--force", str(wt)], cwd=REPO_ROOT)
            _run(
                ["git", "branch", "-D", "feat/batch-fixture-batch-bootstrap-fixture-bootstrap-article"],
                cwd=REPO_ROOT,
            )


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


def test_render_real_md_files_show_in_preview() -> None:
    """Build a fake worktree with real pt-br.md / en.md / mockup PNGs,
    point a synthesized summary.json at it, render, and assert that the
    actual body text appears in the preview (no "(pt-br.md not found)"
    fallback) and that image src attributes use the file:// URI."""
    png_1x1 = bytes.fromhex(
        "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
        "0000000d49444154789c6300010000000500010d0a2db40000000049454e44ae426082"
    )
    pt_body = "# Lista de desejos\n\nSua lista de desejos fica na página do seu perfil.\n"
    en_body = "# Wishlist\n\nYour wishlist sits on your profile page.\n"

    with tempfile.TemporaryDirectory() as tmp:
        worktree = Path(tmp) / "wt"
        article_dir = worktree / "articles" / "sample-rendered"
        mockup_dir = worktree / "assets" / "mockups"
        article_dir.mkdir(parents=True)
        mockup_dir.mkdir(parents=True)
        (article_dir / "pt-br.md").write_text(pt_body, encoding="utf-8")
        (article_dir / "en.md").write_text(en_body, encoding="utf-8")
        png_pt = mockup_dir / "sample-rendered__screen-a__pt-br__v3.png"
        png_en = mockup_dir / "sample-rendered__screen-a__en__v3.png"
        png_pt.write_bytes(png_1x1)
        png_en.write_bytes(png_1x1)

        summary = {
            "batch_id": "test-real-preview",
            "batch_path": "tests/fixtures/batch-coordinator/batch-1.yml",
            "worktree_base": str(worktree.parent),
            "articles": [
                {
                    "slug": "sample-rendered",
                    "audience": "buyer_br",
                    "intercom_id": 99000,
                    "worktree": str(worktree),
                    "branch": "feat/test-real-preview",
                    "validate_returncode": 0,
                    "validate_output": "Validated 1 article(s): 0 hard fail(s), 0 soft warn(s)\n",
                    "hard_fail_count": 0,
                    "soft_warn_count": 0,
                    "mockups_declared": 2,
                    "mockups_present": 2,
                    "missing_mockups": [],
                    "audit_files_present": 3,
                    "audit_skeleton_unfilled": False,
                    "em_dash_count_pt": 0,
                    "em_dash_count_en": 0,
                    "rdollar_leak_en_count": 0,
                    "pt_br_md_path": "articles/sample-rendered/pt-br.md",
                    "en_md_path": "articles/sample-rendered/en.md",
                    "mockup_pngs": [
                        "assets/mockups/sample-rendered__screen-a__pt-br__v3.png",
                        "assets/mockups/sample-rendered__screen-a__en__v3.png",
                    ],
                    "status": "ready",
                    "blockers": [],
                }
            ],
        }
        json_path = Path(tmp) / "summary.json"
        json_path.write_text(json.dumps(summary), encoding="utf-8")
        html_path = Path(tmp) / "summary.html"

        rc, out, err = _run(
            [sys.executable, str(RENDER_PACK), "--input", str(json_path), "--output", str(html_path)]
        )
        assert rc == 0, f"render failed: rc={rc} err={err}"
        body = html_path.read_text(encoding="utf-8")

        assert "Sua lista de desejos fica na página do seu perfil." in body, (
            "pt-BR body content not rendered into preview"
        )
        assert "Your wishlist sits on your profile page." in body, (
            "EN body content not rendered into preview"
        )
        assert "(pt-br.md not found in worktree)" not in body, "pt-BR fallback shown despite real file"
        assert "(en.md not found in worktree)" not in body, "EN fallback shown despite real file"
        assert "file://" in body, "image src does not use file:// URI"
        import re as _re
        srcs = _re.findall(r'src="(file://[^"]+)"', body)
        assert srcs, "no file:// img src in rendered HTML"
        from urllib.parse import urlparse, unquote
        for src in srcs:
            parsed = urlparse(src)
            disk = Path(unquote(parsed.path))
            assert disk.exists(), f"rendered img points at missing file: {disk}"


def test_decide_status_validator_unparseable_blocks() -> None:
    """If validate exited 0 but the summary line was not parsed (counts
    remain at -1), the article must be marked blocked, not ready. This
    is the fail-closed rule: a regression in the validator's output
    format must never silently mark articles as ready for review."""
    mod = _load_coordinator_module()
    review = mod.ArticleReview(
        slug="x",
        audience="buyer_br",
        intercom_id=None,
        worktree="/tmp/x",
        branch="feat/x",
        validate_returncode=0,
        validate_output="(weird empty validator output)",
        hard_fail_count=-1,
        soft_warn_count=-1,
        mockups_declared=0,
        mockups_present=0,
        missing_mockups=[],
        audit_files_present=3,
        audit_skeleton_unfilled=False,
        em_dash_count_pt=0,
        em_dash_count_en=0,
        rdollar_leak_en_count=0,
        pt_br_md_path=None,
        en_md_path=None,
    )
    mod.decide_review_status(review)
    assert review.status == "blocked", f"expected blocked, got {review.status!r}"
    assert "validator summary not parsed" in review.blockers, (
        f"missing fail-closed blocker: {review.blockers}"
    )


def test_decide_status_clean_review_marks_ready() -> None:
    """Sanity check the inverse: a fully-populated review with zero
    issues should mark ready."""
    mod = _load_coordinator_module()
    review = mod.ArticleReview(
        slug="x",
        audience="buyer_br",
        intercom_id=99,
        worktree="/tmp/x",
        branch="feat/x",
        validate_returncode=0,
        validate_output="Validated 1 article(s): 0 hard fail(s), 1 soft warn(s)\n",
        hard_fail_count=0,
        soft_warn_count=1,
        mockups_declared=2,
        mockups_present=2,
        missing_mockups=[],
        audit_files_present=3,
        audit_skeleton_unfilled=False,
        em_dash_count_pt=0,
        em_dash_count_en=0,
        rdollar_leak_en_count=0,
        pt_br_md_path=None,
        en_md_path=None,
    )
    mod.decide_review_status(review)
    assert review.status == "ready", f"clean review should be ready, got {review.status!r}"
    assert review.blockers == [], f"clean review should have no blockers, got {review.blockers}"


def test_render_path_with_space_uses_url_escape() -> None:
    """Worktrees can live in paths that contain spaces, like
    `/Users/.../Jamble Coworker/help-center`. Manual `f"file://{path}"`
    construction breaks for those paths; Path.as_uri() escapes them
    to `%20`. Confirm the renderer does the right thing."""
    png_1x1 = bytes.fromhex(
        "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
        "0000000d49444154789c6300010000000500010d0a2db40000000049454e44ae426082"
    )
    with tempfile.TemporaryDirectory() as tmp:
        worktree = Path(tmp) / "path with space"
        mockup_dir = worktree / "assets" / "mockups"
        mockup_dir.mkdir(parents=True)
        png = mockup_dir / "x__screen__pt-br__v3.png"
        png.write_bytes(png_1x1)

        summary = {
            "batch_id": "test-space-path",
            "articles": [
                {
                    "slug": "x",
                    "audience": "buyer_br",
                    "intercom_id": 1,
                    "worktree": str(worktree),
                    "branch": "feat/x",
                    "validate_returncode": 0,
                    "validate_output": "Validated 1 article(s): 0 hard fail(s), 0 soft warn(s)\n",
                    "hard_fail_count": 0,
                    "soft_warn_count": 0,
                    "mockups_declared": 1,
                    "mockups_present": 1,
                    "missing_mockups": [],
                    "audit_files_present": 3,
                    "audit_skeleton_unfilled": False,
                    "em_dash_count_pt": 0,
                    "em_dash_count_en": 0,
                    "rdollar_leak_en_count": 0,
                    "pt_br_md_path": None,
                    "en_md_path": None,
                    "mockup_pngs": ["assets/mockups/x__screen__pt-br__v3.png"],
                    "status": "ready",
                    "blockers": [],
                }
            ],
        }
        json_path = Path(tmp) / "summary.json"
        json_path.write_text(json.dumps(summary), encoding="utf-8")
        html_path = Path(tmp) / "summary.html"

        rc, out, err = _run(
            [sys.executable, str(RENDER_PACK), "--input", str(json_path), "--output", str(html_path)]
        )
        assert rc == 0, f"render failed: rc={rc} err={err}"
        body = html_path.read_text(encoding="utf-8")
        # The space in the worktree path must be percent-encoded in
        # the file:// URI. A literal space in href="..." would render
        # an unclickable URL in any browser.
        assert "path%20with%20space" in body, (
            f"file URI did not URL-escape the space in the worktree path:\n{body[:500]}"
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
    test_prepare_existing_worktree_path_returns_exit_3,
    test_prepare_bootstraps_missing_flow_yml,
    test_render_ready_summary_produces_html_with_scorecard_and_questions,
    test_render_hardfail_summary_marks_blocked_in_html,
    test_render_missing_png_summary_lists_missing_pngs,
    test_render_three_articles_all_present_in_scorecard,
    test_render_summary_includes_4_reviewer_questions_in_order,
    test_render_real_md_files_show_in_preview,
    test_decide_status_validator_unparseable_blocks,
    test_decide_status_clean_review_marks_ready,
    test_render_path_with_space_uses_url_escape,
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
