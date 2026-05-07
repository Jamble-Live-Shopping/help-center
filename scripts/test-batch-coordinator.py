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

What is intentionally fixture-scoped:
- real `git worktree add` is exercised against HEAD for bootstrap/rerun
  safety, but not against a remote branch. That keeps CI deterministic.

Usage:
    scripts/test-batch-coordinator.py             # run all tests
    scripts/test-batch-coordinator.py --quiet     # only print failures + summary
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
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


def _cleanup_worktree_and_branch(worktree: Path | None, branch: str) -> None:
    """Best-effort cleanup for tests that create real git worktrees.

    Git may keep a prunable registration when a tempfile-backed worktree
    disappears before `git worktree remove` can cleanly unregister it. Prune
    explicitly so a green test run does not leave state that affects the next
    run.
    """
    if worktree is not None and worktree.exists():
        rc, _, _ = _run(["git", "worktree", "remove", "--force", str(worktree)], cwd=REPO_ROOT)
        if rc != 0 and worktree.exists():
            shutil.rmtree(worktree)
    _run(["git", "worktree", "prune"], cwd=REPO_ROOT)
    _run(["git", "branch", "-D", branch], cwd=REPO_ROOT)


def _assert_no_git_leak(branch: str) -> None:
    rc_b, out_b, err_b = _run(["git", "branch", "--list", branch], cwd=REPO_ROOT)
    assert rc_b == 0, f"git branch --list failed: {err_b}"
    rc_w, out_w, err_w = _run(["git", "worktree", "list", "--porcelain"], cwd=REPO_ROOT)
    assert rc_w == 0, f"git worktree list failed: {err_w}"
    combined = out_b + "\n" + out_w
    assert branch not in combined, f"fixture branch/worktree leaked after test:\n{combined}"


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


def test_prepare_ten_articles_accepted_at_cap() -> None:
    """Cap raised from 3 to 10 in PR #88. The 10-article fixture must
    be accepted by prepare. Uses --dry-run because the test does not
    need to create real worktrees."""
    rc, out, err = _run(
        [
            sys.executable,
            str(COORDINATOR),
            "--mode", "prepare",
            "--batch", str(FIX / "batch-10.yml"),
            "--worktree-base", "/tmp/wt-batch-fixture-10",
            "--dry-run",
        ]
    )
    assert rc == 0, f"10-article batch should exit 0, got rc={rc}\nout:\n{out}\nerr:\n{err}"
    assert out.count("would-create") == 10, (
        f"expected 10 would-create lines, got:\n{out}"
    )


def test_prepare_eleven_articles_rejected_with_cap_message() -> None:
    """11 articles must reject. Either layer can do the rejecting:
    `validate-article-batch.py` (MAX_BATCH_SIZE=10) runs first as a
    preflight, and if it accepted (e.g. cap raised), the coordinator's
    own MAX_BATCH_ARTICLES=10 check would catch it. Both layers share
    the same ceiling, so 11 articles always rejects with rc=2 and the
    user sees a clear "exceeds max 10" / "cap is 10" message."""
    rc, out, err = _run(
        [
            sys.executable,
            str(COORDINATOR),
            "--mode", "prepare",
            "--batch", str(FIX / "batch-11-rejects.yml"),
            "--worktree-base", "/tmp/wt-batch-fixture-11",
            "--dry-run",
        ]
    )
    assert rc == 2, f"11-article batch should exit 2, got rc={rc}\nout:\n{out}\nerr:\n{err}"
    combined = (out + err).lower()
    assert (
        "cap is 10" in combined
        or "coordinator cap is 10" in combined
        or "exceeds max 10" in combined
    ), (
        f"11-article batch rejected without a clear cap rationale "
        f"(expected 'cap is 10' or 'exceeds max 10'):\n{out}\n{err}"
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


def test_prepare_rerun_with_same_batch_id_reuses_branch() -> None:
    """Operational regression for the friction Aymar flagged: after a
    full prepare + worktree removal, the branch feat/batch-<id>-<slug>
    survives. A second prepare with the same batch_id was failing on
    `git worktree add -b` ("a branch named ... already exists"). The
    coordinator must detect the existing branch and re-attach instead
    of trying to recreate it. Never deletes the branch automatically."""
    branch = "feat/batch-fixture-batch-rerun-fixture-bootstrap-article"
    # Pre-clean any leftover state from prior runs so this test is
    # reentrant. `git worktree prune` drops registrations whose
    # working trees were rm'd outside git (the tempfile case).
    _cleanup_worktree_and_branch(None, branch)

    # Use a dedicated batch_id so this test does not collide with
    # other tests' branches in a parallel run.
    rerun_batch = REPO_ROOT / "tests" / "fixtures" / "batch-coordinator" / "batch-1-rerun.yml"
    rerun_yaml = (FIX / "batch-1-new-article.yml").read_text(encoding="utf-8").replace(
        "batch_id: fixture-batch-bootstrap",
        "batch_id: fixture-batch-rerun",
    )
    rerun_batch.write_text(rerun_yaml, encoding="utf-8")
    wt: Path | None = None

    try:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "wt-rerun"

            def run_prepare() -> tuple[int, str, str]:
                return _run(
                    [
                        sys.executable,
                        str(COORDINATOR),
                        "--mode", "prepare",
                        "--batch", str(rerun_batch),
                        "--worktree-base", str(base),
                        "--base-ref", "HEAD",
                    ]
                )

            rc1, out1, err1 = run_prepare()
            assert rc1 == 0, f"first prepare failed: rc={rc1}\nout:\n{out1}\nerr:\n{err1}"
            wt = base / "fixture-bootstrap-article"
            assert wt.exists(), "first prepare did not create worktree"

            # Tear down the worktree but leave the branch intact, mimicking
            # the post-cleanup state we hit in the smoke test.
            _run(["git", "worktree", "remove", "--force", str(wt)], cwd=REPO_ROOT)
            assert not wt.exists(), "first worktree was not torn down"

            rc2, out2, err2 = run_prepare()
            assert rc2 == 0, (
                f"second prepare with same batch_id failed: rc={rc2}\n"
                f"This is the rerun-safety regression. The coordinator must "
                f"detect an existing local branch and re-attach instead of "
                f"trying to recreate it.\nout:\n{out2}\nerr:\n{err2}"
            )
            assert "reusing existing local branch" in (out2 + err2), (
                f"second prepare did not signal branch reuse:\n{out2}\n{err2}"
            )
            assert wt.exists(), "second prepare did not create worktree"
    finally:
        rerun_batch.unlink(missing_ok=True)
        # Always drop the test branch so we do not leak it into the
        # developer's repo (even though the test does not delete it
        # automatically inside its own steps).
        _cleanup_worktree_and_branch(wt, branch)
    _assert_no_git_leak(branch)


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


def test_validator_screen_required_icons_missing_fails() -> None:
    """When `screen.required_icons` declares an icon name that is NOT
    referenced in the screen's pt-br/en HTML, the validator must hard
    fail with `screen_icon_not_in_html`. Defends against the bug PR #87
    surfaced: invented icons inside a mockup that the global
    `flow.icons_required` rule cannot catch."""
    fixture = REPO_ROOT / "tests" / "fixtures" / "batch-10-gates" / "article-icon-missing"
    rc, out, err = _run([sys.executable, str(SCRIPTS_DIR / "validate-article-flow.py"), str(fixture)])
    combined = out + err
    assert "screen_icon_not_in_html" in combined, (
        f"missing required-icon should trigger `screen_icon_not_in_html`:\n{combined[:600]}"
    )
    # Both locales should fail (one entry per HTML).
    assert combined.count("screen_icon_not_in_html") >= 2, (
        f"expected >=2 hits (pt-br + en), got:\n{combined[:600]}"
    )


def test_validator_screen_required_icons_present_passes() -> None:
    """Counterpart: when the icon IS referenced in BOTH HTMLs (via
    alt, `<!-- icon: -->`, or xcassets comment), the rule does NOT
    fail. Other validator rules may still flag the fixture for
    unrelated reasons, but `screen_icon_not_in_html` must not appear."""
    fixture = REPO_ROOT / "tests" / "fixtures" / "batch-10-gates" / "article-icon-present"
    rc, out, err = _run([sys.executable, str(SCRIPTS_DIR / "validate-article-flow.py"), str(fixture)])
    combined = out + err
    assert "screen_icon_not_in_html" not in combined, (
        f"icon IS in HTML but rule still fired:\n{combined[:600]}"
    )


def test_validator_review_checks_missing_softwarns_for_ios_required() -> None:
    """When a screen is `source: ios_required` but `review_checks` is
    empty/missing, the validator emits a SOFT warn (not a hard fail).
    Backward compatibility: existing articles that pre-date this contract
    must keep validating exit 0; the warn is just a process nudge."""
    # The wishlist-and-favorites article on main has 3 screens with
    # source: ios_required and no review_checks declared, so it is the
    # ideal natural-history fixture.
    article = REPO_ROOT / "articles" / "wishlist-and-favorites"
    if not article.exists():
        # Skip cleanly when running on a checkout that doesn't have it.
        return
    rc, out, err = _run([sys.executable, str(SCRIPTS_DIR / "validate-article-flow.py"), str(article)])
    combined = out + err
    assert "screen_review_checks_missing" in combined, (
        f"`screen_review_checks_missing` should fire on wishlist-and-favorites:\n{combined[:600]}"
    )
    # Soft warn must NOT promote to hard fail; rc must stay 0.
    assert rc == 0, f"backward-compat broken: review_checks soft warn promoted to hard fail (rc={rc})"


def test_reviewer_pack_renders_manual_gates_when_present() -> None:
    """When summary.json carries `manual_gates` per article, the renderer
    must surface them in a Manual gates table at the top of the article
    block, visible without expanding any details panel."""
    summary = {
        "batch_id": "test-gates",
        "articles": [
            {
                "slug": "x",
                "audience": "buyer_br",
                "intercom_id": 1,
                "worktree": "/tmp/x",
                "branch": "feat/x",
                "validate_returncode": 0,
                "validate_output": "Validated 1 article(s): 0 hard fail(s), 0 soft warn(s)\n",
                "hard_fail_count": 0,
                "soft_warn_count": 0,
                "mockups_declared": 0,
                "mockups_present": 0,
                "missing_mockups": [],
                "audit_files_present": 3,
                "audit_skeleton_unfilled": False,
                "em_dash_count_pt": 0,
                "em_dash_count_en": 0,
                "rdollar_leak_en_count": 0,
                "pt_br_md_path": None,
                "en_md_path": None,
                "mockup_pngs": [],
                "manual_gates": [
                    {
                        "screen": "composer",
                        "source": "ios_required",
                        "required_icons": ["icon-send", "icon-camera"],
                        "review_checks": ["icons_match_ios_source", "labels_match_xcstrings"],
                    }
                ],
                "status": "ready",
                "blockers": [],
            }
        ],
    }
    with tempfile.TemporaryDirectory() as tmp:
        json_path = Path(tmp) / "summary.json"
        json_path.write_text(json.dumps(summary), encoding="utf-8")
        html_path = Path(tmp) / "summary.html"
        rc, out, err = _run([
            sys.executable, str(RENDER_PACK),
            "--input", str(json_path), "--output", str(html_path),
        ])
        assert rc == 0, f"render failed: {err}"
        body = html_path.read_text(encoding="utf-8")
        # Section header
        assert "Manual gates per screen" in body, "manual gates section missing"
        # Required icons rendered as code spans
        assert "icon-send" in body and "icon-camera" in body, "required_icons not rendered"
        # Review checks rendered as code spans
        assert "icons_match_ios_source" in body, "review_checks not rendered"
        # Section is visible without <details> (no <details> wrapping it)
        gates_idx = body.find("Manual gates per screen")
        validate_idx = body.find("Validate output")
        # Gates must appear ABOVE the Validate output details panel.
        assert 0 < gates_idx < validate_idx, (
            f"gates should appear above validate output: gates={gates_idx} validate={validate_idx}"
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


def test_render_sample_summary_json_resolves_repo_root_marker() -> None:
    """The committed sample summary.json uses `{REPO_ROOT}` markers instead
    of developer-local paths. The renderer must still resolve those markers
    and show the real fixture article bodies."""
    with tempfile.TemporaryDirectory() as tmp:
        rc, html, stdout, stderr = _render(REPO_ROOT / "_work" / "sample-batch" / "summary.json", Path(tmp))
        assert rc == 0, f"render failed: rc={rc} stderr={stderr}"
        body = html.read_text(encoding="utf-8")
        assert "Este artigo e um exemplo sintetico" in body, (
            "pt-BR fixture body did not render from {REPO_ROOT} marker"
        )
        assert "This article is a synthetic example" in body, (
            "EN fixture body did not render from {REPO_ROOT} marker"
        )
        assert "(pt-br.md not found in worktree)" not in body
        assert "file://" in body, "runtime-rendered sample should point images at local files"


def test_generate_sample_pack_is_idempotent_and_has_no_local_paths() -> None:
    """The checked-in sample is reviewer-facing documentation. Regenerating
    it must be byte-for-byte stable and must not leak the path of whoever
    last ran the generator."""
    sample_dir = REPO_ROOT / "_work" / "sample-batch"
    html_path = sample_dir / "summary.html"
    json_path = sample_dir / "summary.json"
    before_html = html_path.read_text(encoding="utf-8")
    before_json = json_path.read_text(encoding="utf-8")

    try:
        rc, out, err = _run([sys.executable, str(SCRIPTS_DIR / "generate-sample-reviewer-pack.py")])
        assert rc == 0, f"sample generator failed: rc={rc}\nout:\n{out}\nerr:\n{err}"

        after_html = html_path.read_text(encoding="utf-8")
        after_json = json_path.read_text(encoding="utf-8")
        assert after_html == before_html, "sample summary.html is not idempotent"
        assert after_json == before_json, "sample summary.json is not idempotent"

        combined = after_html + "\n" + after_json
        for forbidden in ("/private/tmp", "/tmp/help-center", "/Users/", "file://"):
            assert forbidden not in combined, (
                f"committed sample leaks local-only token {forbidden!r}"
            )
        assert "../../tests/fixtures/batch-coordinator/sample-worktree/assets/mockups" in after_html, (
            "sample HTML should use repo-relative fixture mockup paths"
        )
    finally:
        html_path.write_text(before_html, encoding="utf-8")
        json_path.write_text(before_json, encoding="utf-8")


def test_prepare_and_review_use_worktree_local_runner_end_to_end() -> None:
    """End-to-end integration: prove the coordinator spawns the runner
    that lives INSIDE each per-article worktree, not the outer-worktree
    copy, AND that prepare's writer-packet + checklist contain real
    RUNBOOK output, AND that review parses the validate summary line.

    Regression for the bug PR #84's first batch surfaced:
      - write_worker_brief and collect_article_review used a module
        constant `RUN_ARTICLE = SCRIPTS_DIR / "run-help-article.py"`
        pointing at the OUTER worktree.
      - run-help-article.py validates `article_dir.relative_to(REPO_ROOT)`
        against its OWN `__file__` parent.parent. With the outer runner,
        that check rejects every per-article worktree path with
        "must be inside REPO_ROOT".
      - Briefs and review pack ended up empty (every writer-packet held
        only the rejection STDERR; review summaries had hard/soft = -1
        with exit 2).

    This test sets up a real worktree from HEAD, runs prepare on a
    bootstrap fixture (so the path goes through both the bootstrap and
    the writer-packet branch), reads the produced files, and runs review
    to assert hard/soft >= 0.
    """
    branch = "feat/batch-fixture-batch-runner-path-fixture-bootstrap-article"
    _run(["git", "worktree", "prune"], cwd=REPO_ROOT)
    _run(["git", "branch", "-D", branch], cwd=REPO_ROOT)

    custom_batch = REPO_ROOT / "tests" / "fixtures" / "batch-coordinator" / "batch-1-runner-path.yml"
    custom_yaml = (FIX / "batch-1-new-article.yml").read_text(encoding="utf-8").replace(
        "batch_id: fixture-batch-bootstrap",
        "batch_id: fixture-batch-runner-path",
    )
    custom_batch.write_text(custom_yaml, encoding="utf-8")

    try:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "wt-runner-path"
            review_out = Path(tmp) / "review"

            rc, out, err = _run(
                [
                    sys.executable,
                    str(COORDINATOR),
                    "--mode", "prepare",
                    "--batch", str(custom_batch),
                    "--worktree-base", str(base),
                    "--base-ref", "HEAD",
                ]
            )
            assert rc == 0, f"prepare failed: rc={rc}\nout:\n{out}\nerr:\n{err}"

            wt = base / "fixture-bootstrap-article"
            wp_path = wt / "_work" / "fixture-bootstrap-article__writer-packet.md"
            cl_path = wt / "_work" / "fixture-bootstrap-article__checklist.md"
            assert wp_path.exists(), "writer-packet file not written"
            assert cl_path.exists(), "checklist file not written"

            wp_text = wp_path.read_text(encoding="utf-8")
            cl_text = cl_path.read_text(encoding="utf-8")

            assert "must be inside" not in wp_text, (
                "writer-packet contains the runner's REPO_ROOT rejection. "
                "The coordinator is calling the OUTER worktree's runner instead "
                "of the per-article worktree's runner.\n"
                f"writer-packet head:\n{wp_text[:300]}"
            )
            assert "must be inside" not in cl_text, (
                "checklist contains the runner's REPO_ROOT rejection - same root cause."
            )
            assert wp_text.lstrip().startswith("# Writer packet"), (
                f"writer-packet does not look like real RUNBOOK output:\n{wp_text[:300]}"
            )
            assert "## Article identity" in wp_text or "## Job to be done" in wp_text, (
                "writer-packet missing expected RUNBOOK headings"
            )
            assert cl_text.lstrip().startswith("# Checklist"), (
                f"checklist does not look like real RUNBOOK output:\n{cl_text[:300]}"
            )

            # Review must also parse the validate summary, proving the
            # runner-in-worktree fix applies to collect_article_review too.
            rc_rev, out_rev, err_rev = _run(
                [
                    sys.executable,
                    str(COORDINATOR),
                    "--mode", "review",
                    "--batch", str(custom_batch),
                    "--worktree-base", str(base),
                    "--out", str(review_out),
                ]
            )
            # rc_rev != 0 expected: the bootstrapped article has no body,
            # mockups, or audit triplet. We only check that review
            # collected real data, not that the article passed.
            summary_json = review_out / "summary.json"
            assert summary_json.exists(), "review did not produce summary.json"
            payload = json.loads(summary_json.read_text(encoding="utf-8"))
            assert len(payload["articles"]) == 1
            article = payload["articles"][0]
            assert article["hard_fail_count"] >= 0, (
                f"review failed to parse the validate summary line "
                f"(hard_fail_count={article['hard_fail_count']!r}, soft_warn_count={article['soft_warn_count']!r}). "
                f"validate_output:\n{article['validate_output'][:600]}"
            )
            assert article["soft_warn_count"] >= 0, (
                f"review failed to parse the validate summary line "
                f"(soft_warn_count={article['soft_warn_count']!r})"
            )
    finally:
        custom_batch.unlink(missing_ok=True)
        _run(["git", "worktree", "prune"], cwd=REPO_ROOT)
        _run(["git", "branch", "-D", branch], cwd=REPO_ROOT)


# ---------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------

TESTS = [
    test_prepare_one_article_dry_run_succeeds,
    test_prepare_three_articles_dry_run_succeeds,
    test_prepare_ten_articles_accepted_at_cap,
    test_prepare_eleven_articles_rejected_with_cap_message,
    test_prepare_duplicate_slug_rejected,
    test_prepare_existing_worktree_path_returns_exit_3,
    test_prepare_bootstraps_missing_flow_yml,
    test_prepare_rerun_with_same_batch_id_reuses_branch,
    test_prepare_and_review_use_worktree_local_runner_end_to_end,
    test_render_ready_summary_produces_html_with_scorecard_and_questions,
    test_render_hardfail_summary_marks_blocked_in_html,
    test_render_missing_png_summary_lists_missing_pngs,
    test_render_three_articles_all_present_in_scorecard,
    test_render_summary_includes_4_reviewer_questions_in_order,
    test_render_real_md_files_show_in_preview,
    test_decide_status_validator_unparseable_blocks,
    test_decide_status_clean_review_marks_ready,
    test_render_path_with_space_uses_url_escape,
    test_validator_screen_required_icons_missing_fails,
    test_validator_screen_required_icons_present_passes,
    test_validator_review_checks_missing_softwarns_for_ios_required,
    test_reviewer_pack_renders_manual_gates_when_present,
    test_render_html_is_self_contained_no_external_js,
    test_render_sample_summary_json_resolves_repo_root_marker,
    test_generate_sample_pack_is_idempotent_and_has_no_local_paths,
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
