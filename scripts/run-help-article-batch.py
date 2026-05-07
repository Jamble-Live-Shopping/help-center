#!/usr/bin/env python3
"""Batch coordinator for the Help Center Article Factory.

Coordinates 1 to 10 article worktrees so that:
  - Claude (or a human worker) writes the article inside each worktree,
    one article per branch, under the writer-packet contract that PR #80
    introduced for single-article runs.
  - A static reviewer pack is produced after the worker has written the
    content, so Aymar can audit the 1 to 10 articles in one review pass from a
    single HTML page.

This script does NOT generate article content. It does NOT call any LLM.
It does NOT auto-publish, auto-merge, or mark a PR ready. It strictly:

  - validates the batch contract,
  - prepares isolated worktrees with writer briefings,
  - collects validate output and mockup status after the worker has
    written content,
  - hands a structured per-article result list to
    `render-reviewer-pack.py` for static HTML aggregation.

Three modes:

    prepare    Validate batch YAML (cap 10 articles), create one isolated
               worktree per article from the fetched base branch, write a
               writer-packet + checklist + CLAUDE_PROMPT.md inside each
               worktree's `_work/` so the worker has everything they need
               to start. Does NOT require validate exit 0; the article is
               by definition still empty at this point.

    review     For each article, run validate inside its worktree, count
               hard fails / soft warns, verify every declared mockup PNG
               exists, check audit-triplet status, and emit a JSON result
               file. Then call `render-reviewer-pack.py` to produce a
               single static HTML at `<out>/summary.html`. Exits non-zero
               if ANY article has a hard fail or a missing PNG.

    cleanup    List the per-article worktrees under `<worktree-base>/`
               and report each one's git status. With `--remove`, removes
               worktrees that are clean (no uncommitted, no untracked).
               Never destructive by default; never removes a worktree
               with pending changes unless `--force-clean` is also set.

Usage:
    scripts/run-help-article-batch.py --mode prepare \\
        --batch process/batches/article-batch.example.yml \\
        --worktree-base /tmp/wt-batch-<batch_id>

    scripts/run-help-article-batch.py --mode review \\
        --batch process/batches/article-batch.example.yml \\
        --worktree-base /tmp/wt-batch-<batch_id> \\
        --out _work/batch-<batch_id>

    scripts/run-help-article-batch.py --mode cleanup \\
        --worktree-base /tmp/wt-batch-<batch_id>
        [--remove [--force-clean]]

Exit codes:
    0  success
    1  validate hard fail or missing PNG (review mode)
    2  contract violation (>10 articles, dup slug, malformed YAML, etc.)
    3  worktree already exists and --force-clean not passed (prepare)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
BATCH_VALIDATOR = SCRIPTS_DIR / "validate-article-batch.py"
RENDER_PACK = SCRIPTS_DIR / "render-reviewer-pack.py"

# Note: there is no module-level RUN_ARTICLE constant. Each per-article
# worktree carries its own copy of `scripts/run-help-article.py`, and
# the runner's `REPO_ROOT` is computed relative to that script. We MUST
# call the worktree-local copy when prepping briefs or collecting review
# data, otherwise the runner rejects the article path with
# "must be inside REPO_ROOT" because the article lives in the per-
# article worktree, not in the coordinator's outer worktree. See
# `_runner_in_worktree` below.


def _runner_in_worktree(worktree_path: Path) -> Path:
    """Return the path to the per-article worktree's
    `scripts/run-help-article.py`. This is what `write_worker_brief`
    and `collect_article_review` must spawn, NOT the coordinator's
    outer-worktree copy.

    If the runner is missing inside the worktree, the caller should
    surface a clear error so the operator updates the base ref.
    """
    return worktree_path / "scripts" / "run-help-article.py"

# Hardcoded cap. Aligned with the upstream `validate-article-batch.py`
# `MAX_BATCH_SIZE = 10` so the coordinator and the upstream lint share
# one ceiling. The PR #84 calibration run validated that the
# coordinator + reviewer pack work end-to-end; the per-screen
# `manual_gates` callout in the reviewer pack lets a reviewer triage
# 10 articles without expanding every detail panel. Above 10 the pack
# format would need a different review pattern (sampled review, or
# split into sub-batches), so the cap stays at 10.
MAX_BATCH_ARTICLES = 10


# --------------------------------------------------------------------------
# Data containers
# --------------------------------------------------------------------------

@dataclass
class ArticleEntry:
    """One article slot from the batch YAML, after preflight."""
    slug: str
    priority: int
    audience: str
    intercom_id: int | None
    job_to_be_done: str
    mode: str  # v2_rewrite / new_article / minor_edit (resolved against batch default)


@dataclass
class ArticleReview:
    """Per-article review-mode result, fed into the reviewer pack."""
    slug: str
    audience: str
    intercom_id: int | None
    worktree: str
    branch: str
    validate_returncode: int
    validate_output: str
    hard_fail_count: int
    soft_warn_count: int
    mockups_declared: int
    mockups_present: int
    missing_mockups: list[str]
    audit_files_present: int  # 0..3
    audit_skeleton_unfilled: bool
    em_dash_count_pt: int
    em_dash_count_en: int
    rdollar_leak_en_count: int
    pt_br_md_path: str | None
    en_md_path: str | None
    mockup_pngs: list[str] = field(default_factory=list)
    # Per-screen manual gates harvested from flow.yml.mockup_plan.screens
    # so the reviewer pack can surface them at the top of each article
    # block. Each entry: {"screen": str, "required_icons": [...],
    # "review_checks": [...], "source": str}. The validator does NOT
    # enforce semantic content; this is purely the manual-review surface.
    manual_gates: list[dict] = field(default_factory=list)
    status: str = "pending"  # ready | blocked | failed
    blockers: list[str] = field(default_factory=list)
    # PR #90 exception-only triage signals. All 5 inputs below feed
    # `exception_free`. The two coverage signals after them are
    # informational only (zero coverage is not a defect).
    unresolved_risk_flags_count: int = 0
    ios_required_screens_without_review_checks: int = 0
    forbidden_html_contract_failures: int = 0
    # Batch real-1 calibration (rule 27 hardening): when JAMBLE_IOS_ROOT
    # is unresolved AND the article declares ios_files / negative_scan,
    # the validator emits a soft warn `source_of_truth_check_skipped`.
    # Counting it here lets `decide_exception_free` exclude such articles
    # from `exception_free=True` so a missing iOS clone never inflates
    # the reviewer pack confidence silently.
    source_of_truth_check_skipped: int = 0
    screens_with_html_contract: int = 0       # informational coverage
    screens_with_required_icons: int = 0      # informational coverage
    exception_free: bool = False
    exception_reasons: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------
# Batch YAML loading + preflight
# --------------------------------------------------------------------------

def _run(args: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(args, capture_output=True, text=True, cwd=str(cwd) if cwd else None)
    return proc.returncode, proc.stdout, proc.stderr


def load_and_validate_batch(batch_path: Path) -> tuple[dict, list[ArticleEntry]]:
    """Load batch YAML and run the existing batch validator. Then enforce
    the coordinator's cap (MAX_BATCH_ARTICLES). Returns (raw_dict, entries).

    Raises SystemExit(2) on any contract violation.
    """
    if not batch_path.exists():
        print(f"ERROR: batch file not found: {batch_path}", file=sys.stderr)
        raise SystemExit(2)

    rc, out, err = _run([sys.executable, str(BATCH_VALIDATOR), str(batch_path)])
    if rc != 0:
        sys.stderr.write(out)
        sys.stderr.write(err)
        print(f"ERROR: batch validator rejected {batch_path}", file=sys.stderr)
        raise SystemExit(2)

    try:
        data = yaml.safe_load(batch_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"ERROR: cannot parse {batch_path}: {exc}", file=sys.stderr)
        raise SystemExit(2)

    if not isinstance(data, dict):
        print(f"ERROR: {batch_path} does not parse to a mapping", file=sys.stderr)
        raise SystemExit(2)

    articles = data.get("articles") or []
    if not isinstance(articles, list) or len(articles) == 0:
        print(f"ERROR: {batch_path} has no articles", file=sys.stderr)
        raise SystemExit(2)
    if len(articles) > MAX_BATCH_ARTICLES:
        print(
            f"ERROR: batch has {len(articles)} articles; coordinator cap is "
            f"{MAX_BATCH_ARTICLES}. The reviewer pack scales to "
            f"{MAX_BATCH_ARTICLES} articles using the manual-gates callout for "
            f"per-screen triage; beyond that the format would need a different "
            f"review pattern (sampled review or sub-batches). Split the batch.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    seen_slugs: set[str] = set()
    entries: list[ArticleEntry] = []
    batch_mode = data.get("mode") or "v2_rewrite"
    for idx, art in enumerate(articles):
        slug = art.get("slug")
        if slug in seen_slugs:
            # Already caught by validate-article-batch.py, defense in depth.
            print(f"ERROR: duplicate slug at articles[{idx}]: {slug}", file=sys.stderr)
            raise SystemExit(2)
        seen_slugs.add(slug)
        entries.append(
            ArticleEntry(
                slug=slug,
                priority=art.get("priority"),
                audience=art.get("audience"),
                intercom_id=art.get("intercom_id"),
                job_to_be_done=art.get("job_to_be_done") or "",
                mode=art.get("mode") or batch_mode,
            )
        )

    return data, entries


# --------------------------------------------------------------------------
# Mode: prepare
# --------------------------------------------------------------------------

def _git(args: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    return _run(["git"] + args, cwd=cwd)


def _local_branch_exists(repo_root: Path, branch: str) -> bool:
    """Return True iff a local branch with that name exists."""
    rc, _, _ = _git(
        ["show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=repo_root,
    )
    return rc == 0


def prepare_worktree(
    repo_root: Path,
    worktree_path: Path,
    branch: str,
    base_ref: str,
    force_clean: bool,
) -> int:
    """Create or re-attach a worktree at `worktree_path` for `branch`.

    Behavior:
      - If `worktree_path` already exists, refuse (return 3) unless
        `force_clean` is set; with --force-clean, drop the existing
        worktree first.
      - If a local branch named `branch` does NOT exist, create one
        from `base_ref` and attach the worktree to it.
      - If a local branch named `branch` DOES exist (typical when a
        previous batch run left the branch behind after the worktree
        was removed), re-attach to it without modifying the branch
        history. This keeps the second `prepare` for the same
        batch_id rerunnable without manual `git branch -D`. Never
        deletes the existing branch silently.

    Returns 0 on success, 1 on git-level failure, 3 on
    existing-path conflict.
    """
    if worktree_path.exists():
        if not force_clean:
            print(
                f"ERROR: worktree path already exists: {worktree_path}\n"
                f"Pass --force-clean to remove it first, or pick a different "
                f"--worktree-base.",
                file=sys.stderr,
            )
            return 3
        # Force-clean: try to remove the worktree cleanly via git first; if
        # git does not know about it (orphaned dir), rmtree as fallback.
        rc, _, _ = _git(["worktree", "remove", "--force", str(worktree_path)], cwd=repo_root)
        if rc != 0 and worktree_path.exists():
            shutil.rmtree(worktree_path)

    worktree_path.parent.mkdir(parents=True, exist_ok=True)

    if _local_branch_exists(repo_root, branch):
        print(
            f"  (reusing existing local branch {branch!r}; --base-ref ignored for re-attach)",
            file=sys.stderr,
        )
        rc, out, err = _git(
            ["worktree", "add", str(worktree_path), branch],
            cwd=repo_root,
        )
    else:
        rc, out, err = _git(
            ["worktree", "add", "-b", branch, str(worktree_path), base_ref],
            cwd=repo_root,
        )
    if rc != 0:
        sys.stderr.write(out)
        sys.stderr.write(err)
        print(f"ERROR: git worktree add failed for {worktree_path}", file=sys.stderr)
        return 1
    return 0


def bootstrap_flow_yml(
    worktree_path: Path,
    slug: str,
    batch_path: Path,
) -> tuple[int, str]:
    """Run init-article-flow.py inside the worktree to create
    articles/<slug>/flow.yml from the batch entry.

    Calls the worktree-local copy of init-article-flow.py so that the
    article folder gets created inside the worktree, not in the script
    author's checkout. Returns (rc, combined_stdout_stderr).
    """
    init_script = worktree_path / "scripts" / "init-article-flow.py"
    if not init_script.exists():
        return (
            1,
            f"ERROR: {init_script} not found in worktree (base ref out of date?)\n",
        )
    rc, out, err = _run(
        [
            sys.executable,
            str(init_script),
            "--slug", slug,
            "--from-batch", str(batch_path.resolve()),
            "--force",
        ],
        cwd=worktree_path,
    )
    return rc, (out or "") + (err or "")


def write_worker_brief(
    worktree_path: Path,
    entry: ArticleEntry,
    batch_id: str,
    batch_path: Path,
) -> int:
    """Inside the worktree, ensure articles/<slug>/flow.yml exists (auto-
    bootstrapping it from the batch entry when missing), then run
    writer-packet + checklist and stash a single-page brief at
    `_work/<slug>__brief.md`.

    Returns 0 on success, non-zero if bootstrap failed. The caller
    propagates the worst exit code so the user sees a clear failure
    instead of a silent "ready" on a half-prepared worktree.
    """
    article_dir = worktree_path / "articles" / entry.slug
    work_dir = worktree_path / "_work"
    work_dir.mkdir(parents=True, exist_ok=True)

    flow_path = article_dir / "flow.yml"
    bootstrap_log = ""
    if not flow_path.exists():
        # Auto-bootstrap. init-article-flow.py creates the article folder
        # if absent, so this works for both v2_rewrite (folder exists,
        # flow.yml accidentally missing) and new_article (greenfield).
        rc, bootstrap_log = bootstrap_flow_yml(worktree_path, entry.slug, batch_path)
        if rc != 0 or not flow_path.exists():
            (work_dir / f"{entry.slug}__brief.md").write_text(
                f"# Worker brief: {entry.slug}\n\n"
                f"ERROR: bootstrap of articles/{entry.slug}/flow.yml failed.\n\n"
                f"Output from init-article-flow.py:\n\n"
                f"```\n{bootstrap_log}\n```\n\n"
                f"Fix the batch entry or the iOS / backend hints and re-run the coordinator.\n",
                encoding="utf-8",
            )
            return rc if rc != 0 else 1

    # Spawn the runner that lives INSIDE the per-article worktree. The
    # runner computes its REPO_ROOT from its own location, so the article
    # path passed via argv must live under the same repo root. Calling
    # the coordinator's outer-worktree runner here makes the runner
    # reject the article path with "must be inside REPO_ROOT", which is
    # what produced the empty briefs that PR #84 hit.
    runner = _runner_in_worktree(worktree_path)
    if not runner.exists():
        (work_dir / f"{entry.slug}__brief.md").write_text(
            f"# Worker brief: {entry.slug}\n\n"
            f"ERROR: {runner} not found in worktree (base ref out of date?).\n",
            encoding="utf-8",
        )
        return 1

    # Capture writer-packet output (read-only on the article).
    rc, out, err = _run(
        [sys.executable, str(runner), str(article_dir), "--phase", "writer-packet"],
        cwd=worktree_path,
    )
    (work_dir / f"{entry.slug}__writer-packet.md").write_text(
        out + (("\n\nSTDERR:\n" + err) if err else ""),
        encoding="utf-8",
    )

    # Capture current checklist (informational). Same runner-in-worktree
    # contract as writer-packet above.
    rc2, out2, err2 = _run(
        [sys.executable, str(runner), str(article_dir), "--phase", "checklist"],
        cwd=worktree_path,
    )
    (work_dir / f"{entry.slug}__checklist.md").write_text(
        out2 + (("\n\nSTDERR:\n" + err2) if err2 else ""),
        encoding="utf-8",
    )

    # Single-page brief that points at everything else.
    brief = (
        f"# Worker brief: {entry.slug}\n\n"
        f"Batch       : `{batch_id}`\n"
        f"Slug        : `{entry.slug}`\n"
        f"Audience    : {entry.audience}\n"
        f"Priority    : {entry.priority}\n"
        f"Mode        : {entry.mode}\n"
        f"Intercom ID : {entry.intercom_id}\n"
        f"\nJob to be done\n\n> {entry.job_to_be_done}\n\n"
        f"## What you have\n\n"
        f"- `articles/{entry.slug}/flow.yml` (the contract)\n"
        f"- `articles/{entry.slug}/metadata.yml` (locales + intercom_id)\n"
        f"- `_work/{entry.slug}__writer-packet.md` (what to read, deliverables, order)\n"
        f"- `_work/{entry.slug}__checklist.md` (current hard fails grouped by RUNBOOK phase)\n\n"
        f"## What to deliver\n\n"
        f"Follow the writer-packet end-to-end. Final gate:\n\n"
        f"```\n"
        f"python3 scripts/run-help-article.py articles/{entry.slug} --phase validate\n"
        f"```\n\n"
        f"Article is shippable iff the gate exits 0. Open a draft PR only after that.\n"
    )
    (work_dir / f"{entry.slug}__brief.md").write_text(brief, encoding="utf-8")
    return 0


def mode_prepare(
    batch_path: Path,
    worktree_base: Path,
    base_ref: str,
    force_clean: bool,
    dry_run: bool = False,
) -> int:
    data, entries = load_and_validate_batch(batch_path)
    batch_id = data.get("batch_id") or batch_path.stem

    if not dry_run:
        # Fetch base ref so worktrees branch from a current snapshot.
        rc, _, err = _git(["fetch", "origin", base_ref.split("/")[-1]], cwd=REPO_ROOT)
        if rc != 0:
            # Not fatal if we are offline; warn and continue with local ref.
            print(f"WARN: git fetch origin {base_ref} failed; using local ref. {err.strip()}", file=sys.stderr)

    print(f"# Prepare batch: {batch_id}")
    print(f"Articles      : {len(entries)} (cap {MAX_BATCH_ARTICLES})")
    print(f"Worktree base : {worktree_base}")
    print(f"Base ref      : {base_ref}")
    print(f"Dry run       : {dry_run}")
    print()

    failures: list[tuple[str, int]] = []
    for entry in entries:
        worktree_path = worktree_base / entry.slug
        branch = f"feat/batch-{batch_id}-{entry.slug}"
        print(f"## {entry.slug}")
        print(f"- worktree : {worktree_path}")
        print(f"- branch   : {branch}")

        if dry_run:
            print(f"- status   : would-create (dry-run)")
            print(f"- brief    : {worktree_path}/_work/{entry.slug}__brief.md")
            print()
            continue

        rc = prepare_worktree(REPO_ROOT, worktree_path, branch, base_ref, force_clean)
        if rc != 0:
            failures.append((entry.slug, rc))
            print(f"- status   : FAILED (worktree, exit {rc})\n")
            continue

        rc_brief = write_worker_brief(worktree_path, entry, batch_id, batch_path)
        if rc_brief != 0:
            failures.append((entry.slug, rc_brief))
            print(f"- status   : FAILED (brief, exit {rc_brief})\n")
            continue

        print(f"- status   : ready")
        print(f"- brief    : {worktree_path}/_work/{entry.slug}__brief.md")
        print()

    if failures:
        names = ", ".join(slug for slug, _ in failures)
        print(f"\nERROR: {len(failures)} worktree(s) failed: {names}", file=sys.stderr)
        # Propagate the most specific exit code seen. Exit 3 (existing
        # worktree path without --force-clean) wins over 1, so the caller
        # can scriptably distinguish "path conflict" from a generic
        # failure.
        worst = max(rc for _, rc in failures)
        return worst

    print("Next steps:")
    print(f"  1. Open each `_work/<slug>__brief.md` to brief Claude or a human worker.")
    print(f"  2. Worker writes the article inside the corresponding worktree.")
    print(f"  3. When all articles are written, run:")
    print(f"     python3 scripts/run-help-article-batch.py --mode review \\")
    print(f"         --batch {batch_path.relative_to(REPO_ROOT) if batch_path.is_relative_to(REPO_ROOT) else batch_path} \\")
    print(f"         --worktree-base {worktree_base} \\")
    print(f"         --out _work/batch-{batch_id}")
    return 0


# --------------------------------------------------------------------------
# Mode: review
# --------------------------------------------------------------------------

VALIDATOR_SUMMARY_RE = re.compile(
    r"Validated\s+\d+\s+article\(s\):\s+(\d+)\s+hard\s+fail\(s\),\s+(\d+)\s+soft\s+warn\(s\)"
)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def collect_article_review(
    repo_root: Path,
    worktree_path: Path,
    entry: ArticleEntry,
) -> ArticleReview:
    """Run validate inside the worktree, then collect mockup + audit + grep stats."""
    branch = ""
    if worktree_path.exists():
        rc_b, out_b, _ = _git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=worktree_path)
        if rc_b == 0:
            branch = out_b.strip()

    article_dir = worktree_path / "articles" / entry.slug
    review = ArticleReview(
        slug=entry.slug,
        audience=entry.audience,
        intercom_id=entry.intercom_id,
        worktree=str(worktree_path),
        branch=branch,
        validate_returncode=-1,
        validate_output="",
        hard_fail_count=-1,
        soft_warn_count=-1,
        mockups_declared=0,
        mockups_present=0,
        missing_mockups=[],
        audit_files_present=0,
        audit_skeleton_unfilled=False,
        em_dash_count_pt=-1,
        em_dash_count_en=-1,
        rdollar_leak_en_count=-1,
        pt_br_md_path=None,
        en_md_path=None,
    )

    if not worktree_path.exists():
        review.status = "failed"
        review.blockers.append("worktree does not exist")
        return review

    if not article_dir.exists():
        review.status = "failed"
        review.blockers.append(f"articles/{entry.slug}/ does not exist in worktree")
        return review

    # Validate via the per-article worktree's own runner so we get the
    # same exit semantics as the canonical gate. The OUTER coordinator's
    # `scripts/run-help-article.py` would reject the article path with
    # "must be inside REPO_ROOT" because it is not under the outer
    # worktree. See `_runner_in_worktree`.
    runner = _runner_in_worktree(worktree_path)
    if not runner.exists():
        review.status = "failed"
        review.blockers.append(f"{runner} not found in worktree (base ref out of date?)")
        return review
    rc, out, err = _run(
        [sys.executable, str(runner), str(article_dir), "--phase", "validate"],
        cwd=worktree_path,
    )
    review.validate_returncode = rc
    review.validate_output = out + (("\n[stderr]\n" + err) if err else "")

    m = VALIDATOR_SUMMARY_RE.search(review.validate_output)
    if m:
        review.hard_fail_count = int(m.group(1))
        review.soft_warn_count = int(m.group(2))

    # Mockup PNG status: read flow.yml.mockup_plan.screens, then check
    # each declared screen has both pt-br + en PNG present in the worktree.
    flow = {}
    flow_path = article_dir / "flow.yml"
    if flow_path.exists():
        try:
            flow = yaml.safe_load(flow_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            flow = {}
    screens = ((flow.get("mockup_plan") or {}).get("screens")) or []
    declared_pairs: list[str] = []
    manual_gates: list[dict] = []
    # PR #90 evidence counters derived from the same screen walk.
    ios_req_no_review_checks = 0
    screens_with_html = 0
    screens_with_icons = 0
    for s in screens:
        if not isinstance(s, dict) or not s.get("name"):
            continue
        declared_pairs.append(f"{s['name']}__pt-br")
        declared_pairs.append(f"{s['name']}__en")
        manual_gates.append({
            "screen": s["name"],
            "source": s.get("source", ""),
            "required_icons": list(s.get("required_icons") or []),
            "review_checks": list(s.get("review_checks") or []),
        })
        # ios_required without review_checks counts as an exception trigger.
        if s.get("source") == "ios_required" and not (s.get("review_checks") or []):
            ios_req_no_review_checks += 1
        # Coverage: html contract declared on this screen?
        html_must = s.get("html_must_contain") or {}
        html_must_not = s.get("html_must_not_contain") or []
        has_html_contract = (
            (isinstance(html_must, dict) and any(html_must.values()))
            or (isinstance(html_must_not, list) and len(html_must_not) > 0)
        )
        if has_html_contract:
            screens_with_html += 1
        # Coverage: required_icons declared non-empty on this screen?
        if list(s.get("required_icons") or []):
            screens_with_icons += 1
    review.mockups_declared = len(declared_pairs)
    review.manual_gates = manual_gates
    review.ios_required_screens_without_review_checks = ios_req_no_review_checks
    review.screens_with_html_contract = screens_with_html
    review.screens_with_required_icons = screens_with_icons

    # Unresolved risk flags: `risk_flags` count minus `resolved_decisions`
    # count, floor at 0. Existing factory practice pairs decisions to
    # risks 1-to-1; a stricter name-match would be a separate scope.
    risk_flags_list = flow.get("risk_flags") or []
    resolved_decisions_list = flow.get("resolved_decisions") or []
    review.unresolved_risk_flags_count = max(
        0, len(risk_flags_list) - len(resolved_decisions_list)
    )

    # PR #89A forbidden HTML contract violation count, parsed from the
    # validator output we already captured. The validator emits one
    # `screen_html_forbidden_text_present` line per (screen, locale,
    # forbidden-token) hit; counting line occurrences is the right granularity.
    review.forbidden_html_contract_failures = (
        review.validate_output.count("screen_html_forbidden_text_present")
    )
    # Batch real-1 calibration (rule 27 hardening): count the visible
    # skip warn so `decide_exception_free` can disqualify articles where
    # the path-existence rule did not actually run.
    review.source_of_truth_check_skipped = (
        review.validate_output.count("source_of_truth_check_skipped")
    )

    mockup_dir = worktree_path / "assets" / "mockups"
    present_pngs: list[str] = []
    missing: list[str] = []
    for pair in declared_pairs:
        candidates = list(mockup_dir.glob(f"{entry.slug}__{pair}__v*.png")) if mockup_dir.exists() else []
        if candidates:
            present_pngs.append(str(candidates[0].relative_to(worktree_path)))
        else:
            missing.append(f"assets/mockups/{entry.slug}__{pair}__v*.png")
    review.mockups_present = len(present_pngs)
    review.missing_mockups = missing
    review.mockup_pngs = present_pngs

    # Audit triplet status. Validator already covers this via audit_missing
    # / audit_skeleton_unfilled hard fails; here we count files for the
    # pack scorecard.
    audit_dir = article_dir / "audit"
    triplet = ["code-audit", "content-audit", "compliance"]
    found = 0
    skeleton_unfilled = False
    if audit_dir.exists():
        for kind in triplet:
            matches = list(audit_dir.glob(f"{kind}-*.md"))
            if matches:
                found += 1
                for mfile in matches:
                    if "SKELETON_TODO" in _read_text(mfile):
                        skeleton_unfilled = True
                        break
    review.audit_files_present = found
    review.audit_skeleton_unfilled = skeleton_unfilled

    # Hygiene grep.
    pt_br_path = article_dir / "pt-br.md"
    en_path = article_dir / "en.md"
    if pt_br_path.exists():
        body = _read_text(pt_br_path)
        review.em_dash_count_pt = body.count("—")
        review.pt_br_md_path = str(pt_br_path.relative_to(worktree_path))
    if en_path.exists():
        body = _read_text(en_path)
        review.em_dash_count_en = body.count("—")
        # R$ leak counted only in EN body; pt-BR is allowed to use R$.
        review.rdollar_leak_en_count = body.count("R$")
        review.en_md_path = str(en_path.relative_to(worktree_path))

    decide_review_status(review)
    return review


def decide_review_status(review: ArticleReview) -> None:
    """Apply the status decision to a populated ArticleReview, in place.

    Extracted from collect_article_review() so the rules are unit-testable
    without spinning up a worktree + validator. The five blocker rules:

      1. validate exited non-zero
      2. validator reported >=1 hard fail
      3. validate exited 0 BUT the summary line did not parse (fail-closed:
         a regression in the validator's output format never bypasses
         review by default)
      4. at least one declared mockup PNG is missing
      5. the audit triplet still contains SKELETON_TODO markers
    """
    blockers: list[str] = []
    if review.validate_returncode != 0:
        blockers.append(f"validate exit {review.validate_returncode}")
    if review.hard_fail_count > 0:
        blockers.append(f"{review.hard_fail_count} validator hard fail(s)")
    if (
        review.validate_returncode == 0
        and (review.hard_fail_count == -1 or review.soft_warn_count == -1)
    ):
        blockers.append("validator summary not parsed")
    if review.missing_mockups:
        blockers.append(f"{len(review.missing_mockups)} mockup PNG(s) missing")
    if review.audit_skeleton_unfilled:
        blockers.append("audit triplet still has SKELETON_TODO markers")

    if not blockers:
        review.status = "ready"
        review.blockers = []
    else:
        review.status = "blocked"
        review.blockers = blockers

    # PR #90: derive the informational `exception_free` signal AFTER the
    # status decision. The status field stays the source of truth for
    # blocked/failed/ready; exception_free is an additional triage layer
    # that only matters for the reviewer pack sort + display.
    decide_exception_free(review)


def decide_exception_free(review: ArticleReview) -> None:
    """Compute the informational `exception_free` signal and the
    human-readable `exception_reasons` list, in place.

    PR #90 triage helper. NOT a publication gate. The reviewer always
    retains final authority over what ships. `exception_free == True`
    means "no exceptions remain for the reviewer to inspect", not
    "ship without review".

    Inputs (all deterministic, no LLM, no vision, no semantic scoring):

    - hard_fail_count          (validator output)
    - audit_skeleton_unfilled  (filesystem grep, already populated)
    - audit_files_present      (filesystem count, already populated)
    - mockups_present vs mockups_declared (already populated)
    - unresolved_risk_flags_count                (PR #90 new)
    - ios_required_screens_without_review_checks (PR #90 new)
    - forbidden_html_contract_failures           (PR #90 new, parsed
      from validator output for `screen_html_forbidden_text_present`)

    Each failed criterion appends a short human-readable string to
    `exception_reasons`. Order is stable so reviewer-pack diffs are
    readable.
    """
    reasons: list[str] = []
    if review.hard_fail_count > 0:
        reasons.append(f"{review.hard_fail_count} validator hard fail(s)")
    if review.audit_skeleton_unfilled:
        reasons.append("audit triplet still has SKELETON_TODO markers")
    if review.audit_files_present < 3:
        reasons.append(
            f"audit triplet incomplete ({review.audit_files_present}/3)"
        )
    if review.mockups_declared > 0 and review.mockups_present < review.mockups_declared:
        missing = review.mockups_declared - review.mockups_present
        reasons.append(f"{missing} mockup PNG(s) missing")
    if review.unresolved_risk_flags_count > 0:
        reasons.append(
            f"{review.unresolved_risk_flags_count} unresolved risk_flag(s)"
        )
    if review.ios_required_screens_without_review_checks > 0:
        n = review.ios_required_screens_without_review_checks
        reasons.append(f"{n} ios_required screen(s) without review_checks")
    if review.forbidden_html_contract_failures > 0:
        reasons.append(
            f"{review.forbidden_html_contract_failures} forbidden HTML "
            "contract violation(s)"
        )
    if review.source_of_truth_check_skipped > 0:
        reasons.append(
            "source_of_truth path-existence rule was skipped "
            "(JAMBLE_IOS_ROOT unresolved); cannot certify ios paths"
        )
    review.exception_reasons = reasons
    review.exception_free = (len(reasons) == 0)


def mode_review(
    batch_path: Path,
    worktree_base: Path,
    out_dir: Path,
) -> int:
    data, entries = load_and_validate_batch(batch_path)
    batch_id = data.get("batch_id") or batch_path.stem

    out_dir.mkdir(parents=True, exist_ok=True)

    reviews: list[ArticleReview] = []
    for entry in entries:
        worktree_path = worktree_base / entry.slug
        review = collect_article_review(REPO_ROOT, worktree_path, entry)
        reviews.append(review)

    # PR #90: sort by exception severity so the reviewer pack opens
    # with the worst-state articles at the top of the scorecard.
    # Sort key: failed -> blocked -> ready+not exception_free -> ready+exception_free.
    def _sort_key(r: ArticleReview) -> int:
        if r.status == "failed":
            return 0
        if r.status == "blocked":
            return 1
        if not r.exception_free:
            return 2
        return 3
    reviews.sort(key=_sort_key)

    # Persist machine-readable result before generating the HTML pack so
    # CI / debugging always has the raw data even if rendering fails.
    summary_json = out_dir / "summary.json"
    summary_json.write_text(
        json.dumps(
            {
                "batch_id": batch_id,
                "batch_path": str(batch_path),
                "worktree_base": str(worktree_base),
                "articles": [asdict(r) for r in reviews],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # Render the static HTML pack.
    summary_html = out_dir / "summary.html"
    rc, out, err = _run(
        [sys.executable, str(RENDER_PACK), "--input", str(summary_json), "--output", str(summary_html)],
    )
    if rc != 0:
        sys.stderr.write(out)
        sys.stderr.write(err)
        print(f"ERROR: render-reviewer-pack.py failed (rc={rc})", file=sys.stderr)
        return 1

    # Print a tight CLI summary so the operator does not need to open the
    # HTML to know whether to proceed.
    print(f"# Review batch: {batch_id}")
    print(f"Reviewer pack : {summary_html}")
    print()
    print(f"{'slug':40s}  {'status':8s}  hard  soft  png  audit  validate")
    print(f"{'-' * 40}  {'-' * 8}  ----  ----  ---  -----  --------")
    any_blocked = False
    for r in reviews:
        png_ratio = f"{r.mockups_present}/{r.mockups_declared}" if r.mockups_declared else "0/0"
        audit_ratio = f"{r.audit_files_present}/3"
        line = (
            f"{r.slug[:40]:40s}  "
            f"{r.status:8s}  "
            f"{r.hard_fail_count:>4d}  "
            f"{r.soft_warn_count:>4d}  "
            f"{png_ratio:>3s}  "
            f"{audit_ratio:>5s}  "
            f"exit {r.validate_returncode}"
        )
        print(line)
        if r.status != "ready":
            any_blocked = True

    print()
    print(f"Open the reviewer pack: open {summary_html}")
    if any_blocked:
        print(f"\nERROR: at least one article is not ready (see scorecard).", file=sys.stderr)
        return 1
    return 0


# --------------------------------------------------------------------------
# Mode: cleanup
# --------------------------------------------------------------------------

def mode_cleanup(
    worktree_base: Path,
    remove: bool,
    force_clean: bool,
) -> int:
    if not worktree_base.exists():
        print(f"# Cleanup: nothing to do, {worktree_base} does not exist")
        return 0

    children = sorted([p for p in worktree_base.iterdir() if p.is_dir()])
    print(f"# Cleanup base: {worktree_base}")
    print(f"Worktrees     : {len(children)}")
    print()
    if not children:
        return 0

    print(f"{'worktree':50s}  status        action")
    print(f"{'-' * 50}  ------------  ------")
    for path in children:
        rc, out, _ = _git(["status", "--porcelain"], cwd=path)
        clean = rc == 0 and out.strip() == ""
        status = "clean" if clean else "has changes"
        action = "skip"
        if remove:
            if clean:
                rc2, _, err2 = _git(["worktree", "remove", str(path)], cwd=REPO_ROOT)
                if rc2 == 0:
                    action = "removed"
                else:
                    action = f"FAILED ({err2.strip()[:30]})"
            elif force_clean:
                rc2, _, err2 = _git(["worktree", "remove", "--force", str(path)], cwd=REPO_ROOT)
                if rc2 == 0:
                    action = "force-removed"
                else:
                    action = f"FAILED ({err2.strip()[:30]})"
            else:
                action = "kept (pass --force-clean to drop)"
        print(f"{str(path)[:50]:50s}  {status:12s}  {action}")
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Batch coordinator (3-article cap) for the Help Center Article Factory"
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["prepare", "review", "cleanup"],
        help="prepare = create worktrees + briefs; review = collect results + reviewer pack; cleanup = list/remove",
    )
    parser.add_argument(
        "--batch",
        type=Path,
        help="path to batch YAML (required for prepare and review)",
    )
    parser.add_argument(
        "--worktree-base",
        type=Path,
        required=True,
        help="directory that holds one subfolder per article worktree",
    )
    parser.add_argument(
        "--base-ref",
        default="origin/main",
        help="git ref to branch worktrees from (prepare only)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="output directory for the reviewer pack (review mode); default _work/batch-<batch_id>/",
    )
    parser.add_argument(
        "--force-clean",
        action="store_true",
        help="(prepare) wipe any existing worktree path before recreating; (cleanup) force-remove worktrees with pending changes",
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="(cleanup only) remove the listed worktrees (clean ones by default; pass --force-clean to also remove dirty)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="(prepare only) skip every git/filesystem mutation; print what would happen and exit 0",
    )
    args = parser.parse_args()

    if args.mode in ("prepare", "review"):
        if not args.batch:
            print(f"ERROR: --batch is required for --mode {args.mode}", file=sys.stderr)
            return 2

    if args.mode == "prepare":
        return mode_prepare(
            args.batch, args.worktree_base, args.base_ref, args.force_clean, dry_run=args.dry_run,
        )
    if args.mode == "review":
        if args.out is None:
            data = yaml.safe_load(args.batch.read_text(encoding="utf-8")) or {}
            batch_id = data.get("batch_id") or args.batch.stem
            out_dir = REPO_ROOT / "_work" / f"batch-{batch_id}"
        else:
            out_dir = args.out
        return mode_review(args.batch, args.worktree_base, out_dir)
    if args.mode == "cleanup":
        return mode_cleanup(args.worktree_base, args.remove, args.force_clean)
    return 2


if __name__ == "__main__":
    sys.exit(main())
