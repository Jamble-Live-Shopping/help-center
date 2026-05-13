#!/usr/bin/env python3
"""Regression tests for the Help Center Article Factory.

Encapsulates the negative tests proven by hand in PR #77 so they survive
in the repo and run on every factory PR. NOT a full unit suite: it
covers behavior the validator team must not regress (priority handling,
source_hints checks, mode propagation, expected_fails strict semantics).

Usage:
    scripts/test-article-factory.py              # run all tests
    scripts/test-article-factory.py --quiet      # only print failures + summary

Exit 0 if all tests pass. Exit 1 with a clear summary if any fails.
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
BATCH_VALIDATOR = SCRIPTS_DIR / "validate-article-batch.py"
INIT_FLOW = SCRIPTS_DIR / "init-article-flow.py"
REPLAY = SCRIPTS_DIR / "replay-golden-articles.py"


def _run(args: list[str], input_text: str | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(
        args,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        input=input_text,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _write_temp_yaml(content: str) -> Path:
    tmp = Path(tempfile.NamedTemporaryFile(suffix=".yml", delete=False).name)
    tmp.write_text(content, encoding="utf-8")
    return tmp


# ---------------------------------------------------------------
# Tests for validate-article-batch.py
# ---------------------------------------------------------------

def test_duplicate_priority_fails() -> None:
    yml = """\
batch_id: test-dup-priority
workflow: article-v2
mode: v2_rewrite
articles:
  - slug: direct-messages-for-sellers
    priority: 1
    audience: seller_br
    job_to_be_done: "A"
    source_hints:
      ios_files: []
      backend_files: []
      justification: "test"
  - slug: wishlist-and-favorites
    priority: 1
    audience: buyer_br
    job_to_be_done: "B"
    source_hints:
      ios_files: []
      backend_files: []
      justification: "test"
"""
    p = _write_temp_yaml(yml)
    try:
        rc, _, err = _run([sys.executable, str(BATCH_VALIDATOR), str(p)])
        assert rc == 1, f"expected exit 1, got {rc}"
        assert "duplicate priorities" in err, f"missing 'duplicate priorities' in stderr: {err!r}"
    finally:
        p.unlink(missing_ok=True)


def test_missing_source_arrays_fails() -> None:
    yml = """\
batch_id: test-missing-source
workflow: article-v2
mode: v2_rewrite
articles:
  - slug: direct-messages-for-sellers
    priority: 1
    audience: seller_br
    job_to_be_done: "A"
    source_hints: {}
"""
    p = _write_temp_yaml(yml)
    try:
        rc, _, err = _run([sys.executable, str(BATCH_VALIDATOR), str(p)])
        assert rc == 1, f"expected exit 1, got {rc}"
        assert "ios_files is required" in err, f"missing ios_files msg: {err!r}"
        assert "backend_files is required" in err, f"missing backend_files msg: {err!r}"
    finally:
        p.unlink(missing_ok=True)


def test_empty_sources_with_justification_passes() -> None:
    yml = """\
batch_id: test-empty-source-justified
workflow: article-v2
mode: v2_rewrite
articles:
  - slug: direct-messages-for-sellers
    priority: 1
    audience: seller_br
    job_to_be_done: "A"
    source_hints:
      ios_files: []
      backend_files: []
      justification: "copy-only metadata test"
"""
    p = _write_temp_yaml(yml)
    try:
        rc, out, err = _run([sys.executable, str(BATCH_VALIDATOR), str(p)])
        assert rc == 0, f"expected exit 0, got {rc} (stderr={err!r})"
    finally:
        p.unlink(missing_ok=True)


def test_priorities_unsorted_fails() -> None:
    yml = """\
batch_id: test-unsorted
workflow: article-v2
mode: v2_rewrite
articles:
  - slug: direct-messages-for-sellers
    priority: 2
    audience: seller_br
    job_to_be_done: "A"
    source_hints:
      ios_files: []
      backend_files: []
      justification: "test"
  - slug: wishlist-and-favorites
    priority: 1
    audience: buyer_br
    job_to_be_done: "B"
    source_hints:
      ios_files: []
      backend_files: []
      justification: "test"
"""
    p = _write_temp_yaml(yml)
    try:
        rc, _, err = _run([sys.executable, str(BATCH_VALIDATOR), str(p)])
        assert rc == 1, f"expected exit 1, got {rc}"
        assert "ascending order" in err, f"missing 'ascending order' in stderr: {err!r}"
    finally:
        p.unlink(missing_ok=True)


# ---------------------------------------------------------------
# Tests for init-article-flow.py mode propagation
# ---------------------------------------------------------------

def test_init_propagates_new_article_mode() -> None:
    yml = """\
batch_id: test-new-mode
workflow: article-v2
mode: new_article
articles:
  - slug: brand-new-help-article
    priority: 1
    audience: seller_br
    job_to_be_done: "Greenfield"
    source_hints:
      ios_files: []
      backend_files: []
      justification: "greenfield"
    mockup_count_target: 0
"""
    p = _write_temp_yaml(yml)
    try:
        rc, out, err = _run([
            sys.executable, str(INIT_FLOW),
            "--slug", "brand-new-help-article",
            "--from-batch", str(p),
            "--dry-run",
        ])
        assert rc == 0, f"init exit {rc}: {err!r}"
        # Parse the YAML output (skip provenance comments at top)
        import yaml
        data = yaml.safe_load(out)
        assert data["mode"] == "new_article", f"expected mode=new_article, got {data.get('mode')!r}"
        assert data["audience"] == "seller_br"
        assert data["workflow"] == "article-v2"
    finally:
        p.unlink(missing_ok=True)


def test_init_per_article_mode_overrides_batch() -> None:
    yml = """\
batch_id: test-override
workflow: article-v2
mode: v2_rewrite
articles:
  - slug: brand-new-help-article
    priority: 1
    mode: new_article
    audience: seller_br
    job_to_be_done: "Override"
    source_hints:
      ios_files: []
      backend_files: []
      justification: "test"
    mockup_count_target: 0
"""
    p = _write_temp_yaml(yml)
    try:
        # batch validator will fail because mode=v2_rewrite at batch level expects
        # the article folder to exist; here we only test init's behavior. Bypass
        # the batch validator and call init directly.
        rc, out, _ = _run([
            sys.executable, str(INIT_FLOW),
            "--slug", "brand-new-help-article",
            "--from-batch", str(p),
            "--dry-run",
        ])
        assert rc == 0, f"init exit {rc}"
        import yaml
        data = yaml.safe_load(out)
        assert data["mode"] == "new_article", f"per-article override should win, got {data.get('mode')!r}"
    finally:
        p.unlink(missing_ok=True)


# ---------------------------------------------------------------
# Tests for replay-golden-articles.py expected_fails strict
# ---------------------------------------------------------------

def _load_replay_module():
    spec = importlib.util.spec_from_file_location("replay", str(REPLAY))
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_expected_fails_strict_one_match_fails() -> None:
    mod = _load_replay_module()
    fails = [
        ("mockup_png_missing", "missing settings-menu pt"),
        ("mockup_png_missing", "missing totally-other en"),
    ]
    expected = [{"rule": "mockup_png_missing", "count": 2, "contains": "settings-menu"}]
    ok, deviations = mod.evaluate_expectations(fails, expected)
    assert not ok, f"expected fail when one occurrence misses, got ok=True"
    assert any("does not contain" in d for d in deviations), deviations


def test_expected_fails_strict_all_match_passes() -> None:
    mod = _load_replay_module()
    fails = [
        ("mockup_png_missing", "missing settings-menu pt-br v3"),
        ("mockup_png_missing", "missing settings-menu en v3"),
    ]
    expected = [{"rule": "mockup_png_missing", "count": 2, "contains": "settings-menu"}]
    ok, deviations = mod.evaluate_expectations(fails, expected)
    assert ok, f"expected pass when both contain, got deviations={deviations}"


def test_expected_fails_list_positional_passes() -> None:
    mod = _load_replay_module()
    fails = [
        ("mockup_referenced_not_declared", "screen 'configuracoes-menu' is referenced..."),
        ("mockup_referenced_not_declared", "screen 'settings-apply-to-sell' is referenced..."),
    ]
    expected = [{
        "rule": "mockup_referenced_not_declared",
        "count": 2,
        "contains": ["configuracoes-menu", "settings-apply-to-sell"],
    }]
    ok, deviations = mod.evaluate_expectations(fails, expected)
    assert ok, f"expected list positional to pass, got deviations={deviations}"


def test_expected_fails_list_length_mismatch_fails() -> None:
    mod = _load_replay_module()
    fails = [
        ("mockup_png_missing", "msg-1"),
        ("mockup_png_missing", "msg-2"),
    ]
    expected = [{
        "rule": "mockup_png_missing",
        "count": 2,
        "contains": ["only-one"],  # length 1, count 2 -> mismatch
    }]
    ok, deviations = mod.evaluate_expectations(fails, expected)
    assert not ok, f"expected list length mismatch to fail"
    assert any("contains list length" in d for d in deviations), deviations


# ---------------------------------------------------------------
# Tests for run-help-article.py preflight (PR #79 false-green class)
# ---------------------------------------------------------------

RUN_HELP = SCRIPTS_DIR / "run-help-article.py"


def _make_articleless_fixture() -> Path:
    """Create a temp article dir without flow.yml (mirrors apply-to-sell repro)."""
    tmp = Path(tempfile.mkdtemp(prefix="article-no-flow-", dir=str(REPO_ROOT / "articles")))
    return tmp


def test_runner_validate_no_flow_returns_nonzero() -> None:
    art = _make_articleless_fixture()
    try:
        rc, out, err = _run([sys.executable, str(RUN_HELP), str(art), "--phase", "validate"])
        assert rc != 0, f"validate without flow.yml must NOT exit 0; got rc={rc}, out={out!r}"
        assert "flow_missing" in err or "flow_missing" in out, (
            f"expected 'flow_missing' marker in output; got out={out!r} err={err!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_runner_checklist_no_flow_does_not_print_ready() -> None:
    art = _make_articleless_fixture()
    try:
        rc, out, err = _run([sys.executable, str(RUN_HELP), str(art), "--phase", "checklist"])
        assert rc != 0, f"checklist without flow.yml must NOT exit 0; got rc={rc}"
        assert "ready" not in out.lower(), (
            f"checklist must not print 'ready' on a flow_missing article; got out={out!r}"
        )
        assert "flow_missing" in err or "flow_missing" in out, (
            f"expected 'flow_missing' marker; got out={out!r} err={err!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_runner_checklist_metadata_missing_is_phase6() -> None:
    """When metadata.yml is absent, the validator emits metadata_missing.
    The runner checklist must NOT bucket it under 'Unmapped'."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("run_help_article", str(RUN_HELP))
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    mapping = mod.RULE_TO_PHASE
    assert "metadata_missing" in mapping, "metadata_missing must be mapped"
    assert mapping["metadata_missing"][0] == 6, mapping["metadata_missing"]
    assert "metadata_yaml_parse" in mapping, "metadata_yaml_parse must be mapped"
    assert mapping["metadata_yaml_parse"][0] == 6, mapping["metadata_yaml_parse"]
    assert "flow_missing" in mapping
    assert "flow_yaml_parse" in mapping
    assert mapping["flow_missing"][0] == 0
    assert mapping["flow_yaml_parse"][0] == 0


def test_runner_checklist_count_matches_validator() -> None:
    """The number of FAIL lines printed by the runner checklist must equal
    the FAIL line count of the underlying validator on the same article.

    Uses a synthetic fixture with a flow.yml + an empty metadata.yml so
    the validator emits a deterministic, small set of fails.
    """
    art = Path(tempfile.mkdtemp(prefix="article-counter-", dir=str(REPO_ROOT / "articles")))
    try:
        flow_yaml = """\
workflow: article-v2
mode: v2_rewrite
audience: seller_br
job_to_be_done: ""
source_of_truth:
  ios_files: []
  backend_files: []
  legal: []
  support_context: []
content_contract:
  must_answer: []
  forbidden_terms: []
  must_not_say: []
mockup_plan:
  required: false
  screens: []
icons_required: []
icons_fallback_feather: false
currency_required: false
risk_flags: []
resolved_decisions: []
"""
        (art / "flow.yml").write_text(flow_yaml, encoding="utf-8")
        # Minimal but parseable metadata so preflight passes; the validator
        # will still flag content_missing for pt-br/en + description_empty etc.
        (art / "metadata.yml").write_text(
            "intercom_id: 999999\n"
            f"slug: {art.name}\n"
            "default_locale: pt-br\n"
            "state: draft\n"
            "locales:\n"
            "  pt-br:\n"
            "    title: 'X'\n"
            "    description: 'Y'\n"
            "  en:\n"
            "    title: 'X'\n"
            "    description: 'Y'\n",
            encoding="utf-8",
        )
        # Compare validator vs runner checklist on the same fixture
        rc_v, out_v, err_v = _run([
            sys.executable, str(SCRIPTS_DIR / "validate-article-flow.py"), str(art),
        ])
        validator_fail_lines = sum(
            1 for ln in (out_v + err_v).splitlines() if "FAIL  [" in ln or " FAIL [" in ln
        )

        rc_r, out_r, err_r = _run([sys.executable, str(RUN_HELP), str(art), "--phase", "checklist"])
        # Runner formats fails as "  - [rule] ..."
        runner_fail_lines = sum(
            1 for ln in (out_r + err_r).splitlines() if ln.lstrip().startswith("- [")
        )
        assert validator_fail_lines == runner_fail_lines, (
            f"runner counted {runner_fail_lines} fails, validator {validator_fail_lines}; "
            f"validator out={out_v!r}; runner out={out_r!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_runner_validate_forwards_validator_nonzero() -> None:
    """run-help-article --phase validate must forward the validator's
    non-zero exit code on an article with real defects.

    Uses a synthetic fixture (not DM, despite earlier naming) so the
    test stays deterministic and self-contained.
    """
    art = Path(tempfile.mkdtemp(prefix="article-redfix-", dir=str(REPO_ROOT / "articles")))
    try:
        flow_yaml = """\
workflow: article-v2
mode: v2_rewrite
audience: seller_br
job_to_be_done: ""
source_of_truth:
  ios_files: []
  backend_files: []
  legal: []
  support_context: []
content_contract:
  must_answer: []
  forbidden_terms: []
  must_not_say: []
mockup_plan:
  required: false
  screens: []
icons_required: []
icons_fallback_feather: false
currency_required: false
risk_flags: []
resolved_decisions: []
"""
        (art / "flow.yml").write_text(flow_yaml, encoding="utf-8")
        # No metadata.yml -> validator emits metadata_missing -> rc 1
        rc, out, err = _run([sys.executable, str(RUN_HELP), str(art), "--phase", "validate"])
        assert rc == 1, f"expected rc=1 (validator non-zero forwarded), got rc={rc}; out={out!r}"
    finally:
        shutil.rmtree(art, ignore_errors=True)


# ---------------------------------------------------------------
# Tests for --phase writer-packet (PR #80)
# ---------------------------------------------------------------

def _writer_fixture(slug_prefix: str, *, with_metadata: bool = True, intercom_id: int = 9999001) -> Path:
    art = Path(tempfile.mkdtemp(prefix=slug_prefix, dir=str(REPO_ROOT / "articles")))
    flow_yaml = f"""\
workflow: article-v2
mode: v2_rewrite
audience: seller_br
job_to_be_done: "Help sellers learn the writer packet feature"
source_of_truth:
  ios_files:
    - DISCOUNT/Views/SomeView.swift
  backend_files:
    - jamble_backend/src/services/some_service.py
  legal: []
  support_context: []
content_contract:
  must_answer:
    - "what the writer packet shows"
  forbidden_terms:
    - "regex:\\\\bauction\\\\b"
  must_not_say:
    - "Internal moderation tooling"
mockup_plan:
  required: true
  screens:
    - name: example-screen
      purpose: "demo"
      source: ios_required
icons_required:
  - icon-clock
icons_fallback_feather: false
currency_required: false
risk_flags:
  - "needs PM review"
resolved_decisions: []
"""
    (art / "flow.yml").write_text(flow_yaml, encoding="utf-8")
    if with_metadata:
        (art / "metadata.yml").write_text(
            f"intercom_id: {intercom_id}\n"
            f"slug: {art.name}\n"
            "default_locale: pt-br\n"
            "state: draft\n"
            "locales:\n"
            "  pt-br: { title: 'X', description: 'Y' }\n"
            "  en:    { title: 'X', description: 'Y' }\n",
            encoding="utf-8",
        )
    return art


def test_writer_packet_contains_all_sections() -> None:
    art = _writer_fixture("writer-packet-")
    try:
        rc, out, err = _run([sys.executable, str(RUN_HELP), str(art), "--phase", "writer-packet"])
        assert rc == 0, f"writer-packet exit {rc}; err={err!r}"
        for required in [
            "## Article identity",
            "## Job to be done",
            "## Source of truth",
            "## Content contract",
            "### must_answer",
            "### forbidden_terms",
            "### must_not_say",
            "## Mockup plan",
            "## Icons required",
            "## Risks",
            "## Deliverables",
            "icon-clock",
            "example-screen",
            "--phase validate",
        ]:
            assert required in out, f"writer-packet missing section/marker: {required!r}"
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_writer_packet_exits_2_on_missing_flow() -> None:
    art = Path(tempfile.mkdtemp(prefix="writer-no-flow-", dir=str(REPO_ROOT / "articles")))
    try:
        rc, out, err = _run([sys.executable, str(RUN_HELP), str(art), "--phase", "writer-packet"])
        assert rc == 2, f"writer-packet on no-flow must exit 2; got {rc}"
        assert "flow_missing" in (out + err), f"expected flow_missing marker, got out={out!r} err={err!r}"
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_writer_packet_does_not_modify_files() -> None:
    art = _writer_fixture("writer-packet-noop-")
    try:
        before = sorted((p.relative_to(art), p.stat().st_mtime_ns) for p in art.rglob("*") if p.is_file())
        rc, _, _ = _run([sys.executable, str(RUN_HELP), str(art), "--phase", "writer-packet"])
        assert rc == 0
        after = sorted((p.relative_to(art), p.stat().st_mtime_ns) for p in art.rglob("*") if p.is_file())
        assert before == after, f"writer-packet must not modify files; before={before}; after={after}"
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_write_skeletons_creates_audit_triplet() -> None:
    art = _writer_fixture("writer-skel-", intercom_id=9999002)
    try:
        rc, out, _ = _run([
            sys.executable, str(RUN_HELP), str(art), "--phase", "writer-packet", "--write-skeletons",
        ])
        assert rc == 0
        for kind in ("code-audit", "content-audit", "compliance"):
            target = art / "audit" / f"{kind}-9999002.md"
            assert target.exists(), f"missing skeleton: {target}"
        # The article body and mockups must NOT be touched
        for body_file in ("pt-br.md", "en.md"):
            assert not (art / body_file).exists(), f"writer must NOT create {body_file}"
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_write_skeletons_does_not_overwrite_without_force() -> None:
    art = _writer_fixture("writer-skel-noforce-", intercom_id=9999003)
    try:
        # First run creates the triplet
        rc1, _, _ = _run([
            sys.executable, str(RUN_HELP), str(art), "--phase", "writer-packet", "--write-skeletons",
        ])
        assert rc1 == 0
        # Mutate one of the audits to detect overwrite
        target = art / "audit" / "code-audit-9999003.md"
        target.write_text("USER MUTATION\n", encoding="utf-8")
        # Second run without --force must skip
        rc2, out2, _ = _run([
            sys.executable, str(RUN_HELP), str(art), "--phase", "writer-packet", "--write-skeletons",
        ])
        assert rc2 == 0
        assert "USER MUTATION" in target.read_text(encoding="utf-8"), (
            "without --force, existing audit must be preserved"
        )
        assert "Skipped" in out2 or "skipped" in out2, f"expected 'Skipped' message; got {out2!r}"
        # Third run with --force must overwrite
        rc3, out3, _ = _run([
            sys.executable, str(RUN_HELP), str(art), "--phase", "writer-packet", "--write-skeletons", "--force",
        ])
        assert rc3 == 0
        assert "USER MUTATION" not in target.read_text(encoding="utf-8"), (
            "--force must overwrite existing audit"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


# ---------------------------------------------------------------
# Tests for skeleton hardening (PR #81)
# ---------------------------------------------------------------

VALIDATOR = SCRIPTS_DIR / "validate-article-flow.py"


def test_skeletons_contain_skeleton_todo_marker() -> None:
    """Every audit skeleton produced by --write-skeletons must contain the
    SKELETON_TODO marker so the validator catches unfilled audits."""
    art = _writer_fixture("skel-marker-", intercom_id=8881001)
    try:
        rc, _, _ = _run([
            sys.executable, str(RUN_HELP), str(art), "--phase", "writer-packet", "--write-skeletons",
        ])
        assert rc == 0
        for kind in ("code-audit", "content-audit", "compliance"):
            target = art / "audit" / f"{kind}-8881001.md"
            body = target.read_text(encoding="utf-8")
            assert "SKELETON_TODO" in body, f"{kind} skeleton missing SKELETON_TODO marker"
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_skeletons_use_dynamic_date() -> None:
    """Skeletons must stamp `date.today().isoformat()`, not a hardcoded
    date that would silently lie about when the audit happened."""
    import datetime
    art = _writer_fixture("skel-date-", intercom_id=8881002)
    try:
        rc, _, _ = _run([
            sys.executable, str(RUN_HELP), str(art), "--phase", "writer-packet", "--write-skeletons",
        ])
        assert rc == 0
        today = datetime.date.today().isoformat()
        # Hardcoded date from the previous PR that should not appear anymore
        forbidden_hardcoded = "2026-05-06"
        for kind in ("code-audit", "content-audit", "compliance"):
            target = art / "audit" / f"{kind}-8881002.md"
            body = target.read_text(encoding="utf-8")
            assert today in body, f"{kind} skeleton missing today's date {today}"
            # If today happens to equal the legacy hardcoded date, skip
            # the regression check (only meaningful when they differ).
            if today != forbidden_hardcoded:
                assert forbidden_hardcoded not in body, (
                    f"{kind} skeleton still contains hardcoded date {forbidden_hardcoded}"
                )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_validator_fails_on_audit_skeleton_unfilled() -> None:
    """Validator hard fail `audit_skeleton_unfilled` fires whenever any
    audit file contains the SKELETON_TODO marker."""
    art = _writer_fixture("validate-unfilled-", intercom_id=8881003)
    try:
        rc, _, _ = _run([
            sys.executable, str(RUN_HELP), str(art), "--phase", "writer-packet", "--write-skeletons",
        ])
        assert rc == 0
        rc_v, out_v, err_v = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out_v + err_v
        assert rc_v == 1, f"validator must exit 1 with unfilled skeletons; got {rc_v}"
        assert "audit_skeleton_unfilled" in combined, (
            f"expected audit_skeleton_unfilled rule; got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_validator_passes_audit_skeleton_after_markers_removed() -> None:
    """Once a worker fills every SKELETON_TODO marker, the
    `audit_skeleton_unfilled` rule disappears from the validator output.
    Other unrelated rules may still fire, but not this one."""
    art = _writer_fixture("validate-filled-", intercom_id=8881004)
    try:
        rc, _, _ = _run([
            sys.executable, str(RUN_HELP), str(art), "--phase", "writer-packet", "--write-skeletons",
        ])
        assert rc == 0
        for kind in ("code-audit", "content-audit", "compliance"):
            target = art / "audit" / f"{kind}-8881004.md"
            body = target.read_text(encoding="utf-8")
            target.write_text(body.replace("SKELETON_TODO", "(filled-stub)"), encoding="utf-8")
        rc_v, out_v, err_v = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out_v + err_v
        assert "audit_skeleton_unfilled" not in combined, (
            f"audit_skeleton_unfilled must disappear after markers removed; got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_skeletons_drop_pass_like_defaults() -> None:
    """Pre-PR-#81 skeletons shipped with `ALL N SCANS PASS. Zero
    BLOCKER` and `Verdict: PASS` lines that would let an unfilled audit
    look green at a glance. Post-#81, those defaults must not appear."""
    art = _writer_fixture("skel-no-pass-", intercom_id=8881005)
    try:
        rc, _, _ = _run([
            sys.executable, str(RUN_HELP), str(art), "--phase", "writer-packet", "--write-skeletons",
        ])
        assert rc == 0
        forbidden_phrases = [
            "ALL N SCANS PASS",
            "Zero BLOCKER",
        ]
        for kind in ("code-audit", "content-audit", "compliance"):
            target = art / "audit" / f"{kind}-8881005.md"
            body = target.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                assert phrase not in body, (
                    f"{kind} skeleton still contains pre-#81 default {phrase!r}"
                )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_runner_maps_audit_skeleton_unfilled_to_phase7() -> None:
    """run-help-article.py's RULE_TO_PHASE must include audit_skeleton_unfilled
    so the checklist phase groups it cleanly under Phase 7 instead of Unmapped."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("run_help_article", str(RUN_HELP))
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    mapping = mod.RULE_TO_PHASE
    assert "audit_skeleton_unfilled" in mapping
    assert mapping["audit_skeleton_unfilled"][0] == 7


# ---------------------------------------------------------------
# Tests for batch real-1 calibration: 3 false-negative rules
# ---------------------------------------------------------------
# Calibrated from the 4-sample human review of batch real-1 (2026-05-07).
# Each false-negative discovered by Aymar on an exception_free article gets
# a deterministic rule + regression test below before any volume scale.

def _calibration_fixture(slug_prefix: str, *, intercom_id: int) -> Path:
    """Minimal article that passes the validator (used as a clean baseline
    for the calibration tests; each test mutates ONE field to provoke its
    target rule)."""
    art = Path(tempfile.mkdtemp(prefix=slug_prefix, dir=str(REPO_ROOT / "articles")))
    flow_yaml = f"""\
workflow: article-v2
mode: v2_rewrite
audience: seller_br
job_to_be_done: "Help sellers learn the calibration tests"
intercom_id: {intercom_id}
source_of_truth:
  ios_files: []
  backend_files: []
  legal: []
  support_context: []
content_contract:
  must_answer: []
  forbidden_terms: []
  must_not_say: []
mockup_plan:
  required: false
  screens: []
icons_required: []
icons_fallback_feather: false
currency_required: false
risk_flags: []
resolved_decisions: []
"""
    (art / "flow.yml").write_text(flow_yaml, encoding="utf-8")
    (art / "metadata.yml").write_text(
        f"intercom_id: {intercom_id}\n"
        f"slug: {art.name}\n"
        "default_locale: pt-br\n"
        "state: draft\n"
        "locales:\n"
        "  pt-br: { title: 'Calibracao', description: 'Teste de calibracao deterministica' }\n"
        "  en:    { title: 'Calibration', description: 'Deterministic calibration test' }\n",
        encoding="utf-8",
    )
    (art / "pt-br.md").write_text(
        "# Titulo unico\n\n"
        "## Secao 1\n\nConteudo de teste em portugues sem caracteres proibidos.\n\n"
        "## Secao 2\n\nMais conteudo.\n",
        encoding="utf-8",
    )
    (art / "en.md").write_text(
        "# Single title\n\n"
        "## Section 1\n\nTest content in english without forbidden characters.\n\n"
        "## Section 2\n\nMore content.\n",
        encoding="utf-8",
    )
    audit = art / "audit"
    audit.mkdir(exist_ok=True)
    for kind in ("code-audit", "content-audit", "compliance"):
        (audit / f"{kind}-{intercom_id}.md").write_text(
            f"# {kind}-{intercom_id}\n\n"
            "## Stale-feature audit\n\n"
            "| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |\n"
            "|---|---|---|---|---|---|\n"
            "| baseline | none | n/a | 2026-05-07 | aymar | live_in_ios |\n",
            encoding="utf-8",
        )
    return art


def test_validator_fails_on_multiple_h1_headings() -> None:
    """Calibration false-negative #1: choose-quantities shipped with 8 H1
    headings instead of 1 H1 + N H2. Rule heading_hierarchy must hard-fail
    when count != 1."""
    art = _calibration_fixture("calib-h1-many-", intercom_id=8881101)
    try:
        # mutate pt-br.md to have 3 H1 instead of 1
        (art / "pt-br.md").write_text(
            "# Primeiro titulo\n\n# Segundo titulo\n\n# Terceiro titulo\n",
            encoding="utf-8",
        )
        rc, out, err = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out + err
        assert rc == 1, f"validator must exit 1 with multiple H1s; got {rc}"
        assert "heading_hierarchy" in combined, (
            f"expected heading_hierarchy rule; got {combined!r}"
        )
        assert "3 top-level H1" in combined or "has 3" in combined, (
            f"rule message should report the count; got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_validator_passes_with_single_h1_heading() -> None:
    """Single H1 + multiple H2 is the canonical structure; rule must not fire."""
    art = _calibration_fixture("calib-h1-one-", intercom_id=8881102)
    try:
        rc, out, err = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out + err
        assert "heading_hierarchy" not in combined, (
            f"heading_hierarchy must not fire on canonical structure; got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_validator_fails_on_markdown_table_2col() -> None:
    """Intercom clips article tables on mobile. 2-column label/value tables
    must become bullet lists, not Markdown tables."""
    art = _calibration_fixture("calib-table-2col-", intercom_id=8881128)
    try:
        (art / "en.md").write_text(
            "# Single title\n\n"
            "## Section\n\n"
            "| Mode | Use it when |\n"
            "| --- | --- |\n"
            "| Buy It Now | You want a fixed price. |\n",
            encoding="utf-8",
        )
        rc, out, err = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out + err
        assert rc == 1, f"validator must exit 1 with mobile table; got {rc}"
        assert "mobile_table_forbidden" in combined, (
            f"expected mobile_table_forbidden rule; got {combined!r}"
        )
        assert "2-col" in combined or "2 columns" in combined, (
            f"rule message should guide list conversion; got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_validator_fails_on_markdown_table_3col() -> None:
    """3+ column tables are also forbidden in article markdown; process says
    to render real matrices as PNG/mockups instead."""
    art = _calibration_fixture("calib-table-3col-", intercom_id=8881129)
    try:
        (art / "en.md").write_text(
            "# Single title\n\n"
            "## Section\n\n"
            "| Status | Color | Meaning |\n"
            "| --- | --- | --- |\n"
            "| Paid | Green | Buyer paid. |\n",
            encoding="utf-8",
        )
        rc, out, err = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out + err
        assert rc == 1, f"validator must exit 1 with 3-col table; got {rc}"
        assert "mobile_table_forbidden" in combined, (
            f"expected mobile_table_forbidden rule; got {combined!r}"
        )
        assert "PNG" in combined or "mockup" in combined, (
            f"rule message should guide PNG/mockup conversion; got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_validator_fails_on_raw_html_table() -> None:
    """Raw HTML tables reach Intercom as mobile-breaking tables too."""
    art = _calibration_fixture("calib-table-html-", intercom_id=8881130)
    try:
        (art / "en.md").write_text(
            "# Single title\n\n"
            "## Section\n\n"
            "<table><tr><td>Mode</td><td>Use it when</td></tr></table>\n",
            encoding="utf-8",
        )
        rc, out, err = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out + err
        assert rc == 1, f"validator must exit 1 with raw HTML table; got {rc}"
        assert "mobile_table_forbidden" in combined, (
            f"expected mobile_table_forbidden rule; got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_validator_passes_on_bullet_list_table_replacement() -> None:
    """The canonical replacement for 2-column tables is a flat bullet list."""
    art = _calibration_fixture("calib-table-list-", intercom_id=8881131)
    try:
        (art / "en.md").write_text(
            "# Single title\n\n"
            "## Section\n\n"
            "- **Buy It Now**, use it when you want a fixed price.\n"
            "- **Real Time Offer**, use it when buyers should compete.\n",
            encoding="utf-8",
        )
        rc, out, err = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out + err
        assert "mobile_table_forbidden" not in combined, (
            f"bullet list must not trigger table gate; got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_validator_ignores_audit_markdown_tables() -> None:
    """Audit files intentionally use markdown tables; the mobile gate is
    scoped to user-facing en.md / pt-br.md only."""
    art = _calibration_fixture("calib-table-audit-", intercom_id=8881132)
    try:
        rc, out, err = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out + err
        assert "mobile_table_forbidden" not in combined, (
            f"audit markdown tables must be ignored by mobile gate; got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_validator_fails_on_orphan_mockup_html() -> None:
    """Calibration false-negative #2: choose-quantities shipped with 3 orphan
    HTMLs in mockup-sources/ that no longer mapped to any declared screen.
    Rule mockup_orphan_html must hard-fail any HTML not matching a declared
    screen pair."""
    art = _calibration_fixture("calib-orphan-", intercom_id=8881103)
    try:
        # declare ONE screen (screen-1) and add the matching HTML pair
        flow_yaml = (art / "flow.yml").read_text(encoding="utf-8")
        flow_yaml = flow_yaml.replace(
            "mockup_plan:\n  required: false\n  screens: []",
            "mockup_plan:\n  required: true\n  screens:\n    - name: screen-1\n      purpose: demo\n      source: ios_required\n      review_checks: [labels_match_xcstrings]\n",
        )
        (art / "flow.yml").write_text(flow_yaml, encoding="utf-8")
        mockup_dir = art / "mockup-sources"
        mockup_dir.mkdir(exist_ok=True)
        for fname in ("screen-1__pt-br.html", "screen-1__en.html"):
            (mockup_dir / fname).write_text("<div class='phone'>ok</div>", encoding="utf-8")
        # add an ORPHAN file
        (mockup_dir / "stale-toast.html").write_text("<div class='phone'>orphan</div>", encoding="utf-8")
        rc, out, err = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out + err
        assert "mockup_orphan_html" in combined, (
            f"expected mockup_orphan_html rule; got {combined!r}"
        )
        assert "stale-toast.html" in combined, (
            f"rule message should name the orphan file; got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_validator_passes_when_orphan_in_allowlist() -> None:
    """Allowlist escape hatch: orphan files explicitly listed in
    mockup_plan.allowlist_orphans don't fire the rule (rare, but supported
    for legacy artifacts that can't be deleted yet)."""
    art = _calibration_fixture("calib-allow-", intercom_id=8881104)
    try:
        flow_yaml = (art / "flow.yml").read_text(encoding="utf-8")
        flow_yaml = flow_yaml.replace(
            "mockup_plan:\n  required: false\n  screens: []",
            "mockup_plan:\n  required: true\n  allowlist_orphans:\n    - legacy-stale.html\n  screens:\n    - name: screen-1\n      purpose: demo\n      source: ios_required\n      review_checks: [labels_match_xcstrings]\n",
        )
        (art / "flow.yml").write_text(flow_yaml, encoding="utf-8")
        mockup_dir = art / "mockup-sources"
        mockup_dir.mkdir(exist_ok=True)
        for fname in ("screen-1__pt-br.html", "screen-1__en.html"):
            (mockup_dir / fname).write_text("<div class='phone'>ok</div>", encoding="utf-8")
        (mockup_dir / "legacy-stale.html").write_text(
            "<div class='phone'>allowlisted</div>", encoding="utf-8",
        )
        rc, out, err = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out + err
        assert "mockup_orphan_html" not in combined, (
            f"allowlisted orphan must not fire rule; got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_validator_fails_on_nonexistent_ios_path() -> None:
    """Calibration false-negative #3: seller-analytics shipped with
    `SELLER/Analytics/` and `SELLER/Stats/` in source_of_truth.ios_files even
    though the article's central claim is those surfaces don't exist. Rule
    source_of_truth_path_missing must hard-fail when JAMBLE_IOS_ROOT is set
    AND the path doesn't exist there."""
    # Create a fake iOS root with one valid file
    fake_root = Path(tempfile.mkdtemp(prefix="fake-ios-", dir="/tmp"))
    try:
        (fake_root / "REAL").mkdir()
        (fake_root / "REAL" / "Existing.swift").write_text("// real", encoding="utf-8")
        art = _calibration_fixture("calib-iospath-", intercom_id=8881105)
        try:
            flow_yaml = (art / "flow.yml").read_text(encoding="utf-8")
            flow_yaml = flow_yaml.replace(
                "  ios_files: []",
                "  ios_files:\n    - REAL/Existing.swift\n    - PHANTOM/DoesNotExist.swift",
            )
            (art / "flow.yml").write_text(flow_yaml, encoding="utf-8")
            env = {**os.environ, "JAMBLE_IOS_ROOT": str(fake_root)}
            proc = subprocess.run(
                [sys.executable, str(VALIDATOR), str(art)],
                capture_output=True, text=True, cwd=REPO_ROOT, env=env,
            )
            combined = proc.stdout + proc.stderr
            assert proc.returncode == 1, (
                f"validator must exit 1 when ios_files entry is missing; "
                f"got {proc.returncode}; combined={combined!r}"
            )
            assert "source_of_truth_path_missing" in combined, (
                f"expected source_of_truth_path_missing rule; got {combined!r}"
            )
            assert "PHANTOM/DoesNotExist.swift" in combined, (
                f"rule message should name the missing path; got {combined!r}"
            )
            # The valid path must NOT trigger the rule
            assert "REAL/Existing.swift" not in combined.split("source_of_truth_path_missing")[1] if "source_of_truth_path_missing" in combined else True
        finally:
            shutil.rmtree(art, ignore_errors=True)
    finally:
        shutil.rmtree(fake_root, ignore_errors=True)


def test_orphan_rule_displays_safe_path_outside_repo_root() -> None:
    """Hardening (P1): mockup_orphan_html previously called
    `html_file.relative_to(REPO_ROOT)` and raised ValueError when the
    article was outside REPO_ROOT (multi-worktree calibration runs,
    external fixtures). The rule must instead emit a normal FAIL with
    the absolute path string. Calibration: this test creates the
    article OUTSIDE REPO_ROOT/articles to provoke the original crash."""
    art = Path(tempfile.mkdtemp(prefix="calib-orphan-extern-", dir="/tmp"))
    try:
        flow_yaml = """\
workflow: article-v2
mode: v2_rewrite
audience: seller_br
job_to_be_done: "Validate orphan rule outside REPO_ROOT"
intercom_id: 8881107
source_of_truth: { ios_files: [], backend_files: [], legal: [], support_context: [] }
content_contract: { must_answer: [], forbidden_terms: [], must_not_say: [] }
mockup_plan:
  required: true
  screens:
    - name: screen-1
      purpose: demo
      source: ios_required
      review_checks: [labels_match_xcstrings]
icons_required: []
icons_fallback_feather: false
currency_required: false
risk_flags: []
resolved_decisions: []
"""
        (art / "flow.yml").write_text(flow_yaml, encoding="utf-8")
        (art / "metadata.yml").write_text(
            "intercom_id: 8881107\n"
            f"slug: {art.name}\n"
            "default_locale: pt-br\n"
            "state: draft\n"
            "locales:\n"
            "  pt-br: { title: 'X', description: 'X' }\n"
            "  en:    { title: 'X', description: 'X' }\n",
            encoding="utf-8",
        )
        (art / "pt-br.md").write_text("# X\n\n## S1\n\nbody\n", encoding="utf-8")
        (art / "en.md").write_text("# X\n\n## S1\n\nbody\n", encoding="utf-8")
        (art / "audit").mkdir()
        for kind in ("code-audit", "content-audit", "compliance"):
            (art / "audit" / f"{kind}-8881107.md").write_text(
                f"# {kind}-8881107\n\n## Stale-feature audit\n\n"
                "| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |\n"
                "|---|---|---|---|---|---|\n"
                "| baseline | none | n/a | 2026-05-07 | aymar | live_in_ios |\n",
                encoding="utf-8",
            )
        mockup_dir = art / "mockup-sources"
        mockup_dir.mkdir()
        for fname in ("screen-1__pt-br.html", "screen-1__en.html"):
            (mockup_dir / fname).write_text("<div class='phone'>ok</div>", encoding="utf-8")
        # ORPHAN — outside REPO_ROOT this used to crash with ValueError
        (mockup_dir / "stale-extern.html").write_text(
            "<div class='phone'>orphan</div>", encoding="utf-8",
        )
        rc, out, err = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out + err
        # Robustness: never traceback, even outside REPO_ROOT
        assert "Traceback" not in combined, (
            f"validator crashed instead of emitting normal FAIL; got {combined!r}"
        )
        assert "ValueError" not in combined, (
            f"validator raised ValueError instead of safe display path; got {combined!r}"
        )
        # Behavior: the rule still fires, with absolute path in message
        assert "mockup_orphan_html" in combined, (
            f"expected mockup_orphan_html rule; got {combined!r}"
        )
        assert "stale-extern.html" in combined, (
            f"expected the orphan filename in error message; got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_orphan_rule_skips_when_mockup_not_required() -> None:
    """Hardening (P2 scope): mockup_orphan_html is a v2_rewrite product
    invariant. When `mockup_plan.required=false`, the article opts out
    of the mockup contract entirely — orphan files in mockup-sources/
    must not fire the rule. Smallest gate that matches the observed
    defect (which was on a required:true article)."""
    art = _calibration_fixture("calib-orphan-skip-", intercom_id=8881108)
    try:
        # default fixture has mockup_plan.required=false and screens=[]
        mockup_dir = art / "mockup-sources"
        mockup_dir.mkdir(exist_ok=True)
        (mockup_dir / "anything-goes.html").write_text(
            "<div class='phone'>orphan</div>", encoding="utf-8",
        )
        rc, out, err = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out + err
        assert "mockup_orphan_html" not in combined, (
            f"orphan rule must NOT fire when mockup_plan.required=false; "
            f"got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_source_of_truth_warns_when_env_unset_with_ios_paths() -> None:
    """Hardening (P2 silent skip): when the article declares
    source_of_truth.ios_files (or negative_scan) but no iOS clone is
    resolved (env unset AND default location absent), the validator
    must emit a visible soft warn `source_of_truth_check_skipped`.
    The previous version silently skipped the check, which let
    exception_free stay True even though path-existence had not been
    enforced — false confidence."""
    art = _calibration_fixture("calib-skipwarn-", intercom_id=8881109)
    try:
        # add an ios_files entry so the rule activation logic kicks in
        flow_yaml = (art / "flow.yml").read_text(encoding="utf-8")
        flow_yaml = flow_yaml.replace(
            "  ios_files: []",
            "  ios_files:\n    - ANY/Path/Will/Do.swift",
        )
        (art / "flow.yml").write_text(flow_yaml, encoding="utf-8")
        # Suppress both env and default resolution. The escape hatch
        # JAMBLE_IOS_NO_DEFAULT_FALLBACK=1 prevents the default location
        # from resolving without having to override HOME (which would
        # break PyYAML import in the validator subprocess).
        env = {**os.environ, "JAMBLE_IOS_NO_DEFAULT_FALLBACK": "1"}
        env.pop("JAMBLE_IOS_ROOT", None)
        proc = subprocess.run(
            [sys.executable, str(VALIDATOR), str(art)],
            capture_output=True, text=True, cwd=REPO_ROOT, env=env,
        )
        combined = proc.stdout + proc.stderr
        assert "source_of_truth_check_skipped" in combined, (
            f"expected visible skip warn when no iOS clone resolves; "
            f"got {combined!r}"
        )
        # Confirm rule 27 itself did NOT silently fire on a phantom path
        assert "source_of_truth_path_missing" not in combined, (
            f"rule 27 must not fire when iOS root unresolved; got {combined!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_unanchored_icon_review_check_warns_and_disqualifies() -> None:
    """Hardening (Aymar sample-review false-negative, 2026-05-07): if a
    screen declares review_checks=[icons_match_ios_source] but has
    neither required_icons (real-icon anchor) nor html_must_not_contain
    icon-blockers (text-only anchor), the validator must emit the soft
    warn `screen_icon_review_check_unanchored` AND the coordinator's
    `decide_exception_free` must disqualify the article. Calibrated from
    the wishlist product-bookmark-cta bug where exception_free=true on a
    mockup that rendered an invented flag glyph instead of the real iOS
    heart asset, slipping past existing rules because the icon-match
    claim was descriptive rather than enforced.

    Three sub-assertions: (1) warn fires when neither anchor present;
    (2) warn does NOT fire when required_icons is non-empty (real-icon
    opt-in); (3) warn does NOT fire when html_must_not_contain blocks
    icon markup (text-only opt-in). Plus coordinator-level proof that
    decide_exception_free disqualifies on the warn."""
    art = _calibration_fixture("calib-icon-anchor-", intercom_id=8881110)
    try:
        # (1) UNANCHORED — warn must fire
        flow_yaml = (art / "flow.yml").read_text(encoding="utf-8")
        flow_yaml = flow_yaml.replace(
            "mockup_plan:\n  required: false\n  screens: []",
            "mockup_plan:\n  required: true\n  screens:\n"
            "    - name: screen-1\n"
            "      purpose: demo\n"
            "      source: ios_required\n"
            "      review_checks: [icons_match_ios_source, labels_match_xcstrings]\n",
        )
        (art / "flow.yml").write_text(flow_yaml, encoding="utf-8")
        mockup_dir = art / "mockup-sources"
        mockup_dir.mkdir(exist_ok=True)
        for fname in ("screen-1__pt-br.html", "screen-1__en.html"):
            (mockup_dir / fname).write_text("<div class='phone'>ok</div>", encoding="utf-8")
        rc, out, err = _run([sys.executable, str(VALIDATOR), str(art)])
        combined = out + err
        assert "screen_icon_review_check_unanchored" in combined, (
            f"warn must fire when icons_match_ios_source has no anchor; "
            f"got {combined!r}"
        )

        # (1b) coordinator-level: decide_exception_free disqualifies
        import importlib.util
        coord_path = SCRIPTS_DIR / "run-help-article-batch.py"
        spec = importlib.util.spec_from_file_location("batch_coord_anchor", str(coord_path))
        mod = importlib.util.module_from_spec(spec)
        sys.modules["batch_coord_anchor"] = mod
        assert spec.loader is not None
        spec.loader.exec_module(mod)
        review = mod.ArticleReview(
            slug="x", worktree=Path("/tmp/x"), branch="x", intercom_id=1,
            audience="seller_br",
            validate_returncode=0,
            validate_output="WARN [screen_icon_review_check_unanchored] screen 'screen-1' ...",
            hard_fail_count=0, soft_warn_count=1,
            mockups_present=2, mockups_declared=2, missing_mockups=[],
            mockup_pngs=["a", "b"],
            em_dash_count_pt=0, em_dash_count_en=0, rdollar_leak_en_count=0,
            pt_br_md_path="pt-br.md", en_md_path="en.md",
            audit_files_present=3, audit_skeleton_unfilled=False,
        )
        review.screens_with_unanchored_icon_check = 1
        mod.decide_exception_free(review)
        assert review.exception_free is False, (
            f"unanchored icon check must disqualify exception_free; "
            f"got exception_free={review.exception_free}, "
            f"reasons={review.exception_reasons}"
        )
        assert any("icons_match_ios_source" in r for r in review.exception_reasons), (
            f"expected explicit unanchored-icon reason; "
            f"got {review.exception_reasons}"
        )

        # (2) ANCHORED via required_icons — warn must NOT fire
        flow_yaml_anchored = (art / "flow.yml").read_text(encoding="utf-8")
        flow_yaml_anchored = flow_yaml_anchored.replace(
            "      review_checks: [icons_match_ios_source, labels_match_xcstrings]\n",
            "      review_checks: [icons_match_ios_source, labels_match_xcstrings]\n"
            "      required_icons: [real_asset_name]\n",
        )
        (art / "flow.yml").write_text(flow_yaml_anchored, encoding="utf-8")
        for fname in ("screen-1__pt-br.html", "screen-1__en.html"):
            (mockup_dir / fname).write_text(
                "<div class='phone'><!-- icon: real_asset_name from "
                "Assets.xcassets/real_asset_name.imageset --></div>",
                encoding="utf-8",
            )
        rc2, out2, err2 = _run([sys.executable, str(VALIDATOR), str(art)])
        combined2 = out2 + err2
        assert "screen_icon_review_check_unanchored" not in combined2, (
            f"warn must NOT fire when required_icons is non-empty; "
            f"got {combined2!r}"
        )

        # (3a) PARTIAL anchor via html_must_not_contain (only "<img") —
        # warn STILL fires because each of the three icon-blockers
        # covers a distinct regression vector (bitmap, inline SVG, CSS
        # icon class). A partial subset would let the other vectors
        # slip past unanchored. Aymar 2026-05-07 hardening.
        flow_yaml_partial = (art / "flow.yml").read_text(encoding="utf-8")
        flow_yaml_partial = flow_yaml_partial.replace(
            "      review_checks: [icons_match_ios_source, labels_match_xcstrings]\n"
            "      required_icons: [real_asset_name]\n",
            "      review_checks: [icons_match_ios_source, labels_match_xcstrings]\n"
            "      html_must_not_contain: ['<img']\n",
        )
        (art / "flow.yml").write_text(flow_yaml_partial, encoding="utf-8")
        for fname in ("screen-1__pt-br.html", "screen-1__en.html"):
            (mockup_dir / fname).write_text(
                "<div class='phone'>text-only with partial anchor</div>",
                encoding="utf-8",
            )
        rc3a, out3a, err3a = _run([sys.executable, str(VALIDATOR), str(art)])
        combined3a = out3a + err3a
        assert "screen_icon_review_check_unanchored" in combined3a, (
            f"warn MUST still fire when html_must_not_contain has only "
            f"a partial blocker subset (text-only anchor must declare "
            f"all three: '<img', '<svg', 'icon-'); got {combined3a!r}"
        )

        # (3b) FULL anchor via html_must_not_contain — warn must NOT fire
        flow_yaml_textonly = (art / "flow.yml").read_text(encoding="utf-8")
        flow_yaml_textonly = flow_yaml_textonly.replace(
            "      review_checks: [icons_match_ios_source, labels_match_xcstrings]\n"
            "      html_must_not_contain: ['<img']\n",
            "      review_checks: [icons_match_ios_source, labels_match_xcstrings]\n"
            "      html_must_not_contain: ['<img', '<svg', 'icon-']\n",
        )
        (art / "flow.yml").write_text(flow_yaml_textonly, encoding="utf-8")
        rc3, out3, err3 = _run([sys.executable, str(VALIDATOR), str(art)])
        combined3 = out3 + err3
        assert "screen_icon_review_check_unanchored" not in combined3, (
            f"warn must NOT fire when html_must_not_contain has the "
            f"complete icon-blocker set ['<img', '<svg', 'icon-']; "
            f"got {combined3!r}"
        )
    finally:
        shutil.rmtree(art, ignore_errors=True)


def test_source_of_truth_check_skipped_disqualifies_exception_free() -> None:
    """Hardening (P2 silent skip, coordinator side): when the validator
    emits `source_of_truth_check_skipped`, the coordinator's
    `decide_exception_free` must add an exception_reason and set
    `exception_free=False`. Otherwise the reviewer pack would still
    show EXCEPTION-FREE on an article whose ios paths were never
    actually checked."""
    import importlib.util
    coord_path = SCRIPTS_DIR / "run-help-article-batch.py"
    spec = importlib.util.spec_from_file_location("batch_coord", str(coord_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["batch_coord"] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    review = mod.ArticleReview(
        slug="x",
        worktree=Path("/tmp/x"),
        branch="x",
        intercom_id=1,
        audience="seller_br",
        validate_returncode=0,
        validate_output="some text",
        hard_fail_count=0,
        soft_warn_count=1,
        mockups_present=2,
        mockups_declared=2,
        missing_mockups=[],
        mockup_pngs=["a", "b"],
        em_dash_count_pt=0,
        em_dash_count_en=0,
        rdollar_leak_en_count=0,
        pt_br_md_path="pt-br.md",
        en_md_path="en.md",
        audit_files_present=3,
        audit_skeleton_unfilled=False,
    )
    # Manually set the new field, mirroring what collect_article_review
    # does when validate_output contains the warn.
    review.source_of_truth_check_skipped = 1
    mod.decide_exception_free(review)
    assert review.exception_free is False, (
        f"source_of_truth_check_skipped > 0 must disqualify exception_free; "
        f"got exception_free={review.exception_free}, reasons={review.exception_reasons}"
    )
    assert any("path-existence rule was skipped" in r for r in review.exception_reasons), (
        f"expected explicit skipped-rule reason; got {review.exception_reasons}"
    )


# --- visible_text / xcstrings_locale_drift gate ---
#
# Five tests anchored to the 2026-05-11 batch real-2 back-sweep that
# triggered the rule. Each test loads the validator module directly and
# calls `_validate_visible_text` with synthetic fixtures so we don't have
# to spin up a full article dir + iOS clone.

_VALIDATOR_FLOW = SCRIPTS_DIR / "validate-article-flow.py"


def _load_validator_module():
    """Load validate-article-flow.py as an importable module.

    Must register the module in sys.modules BEFORE exec_module so the
    @dataclass decorator on Report can resolve its own module via
    sys.modules.get(cls.__module__).
    """
    name = "validate_article_flow_under_test"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, str(_VALIDATOR_FLOW))
    assert spec is not None and spec.loader is not None, f"could not load spec for {_VALIDATOR_FLOW}"
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _build_visible_text_fixture(html_pt: str, html_en: str | None = None) -> tuple[Path, Path]:
    """Build a synthetic article dir with screen-1__pt-br.html (and optionally en).

    Returns (article_dir, mockup_dir).
    """
    article = Path(tempfile.mkdtemp(prefix="visible-text-fixture-"))
    mockup_dir = article / "mockup-sources"
    mockup_dir.mkdir(parents=True)
    (mockup_dir / "screen-1__pt-br.html").write_text(html_pt, encoding="utf-8")
    if html_en is not None:
        (mockup_dir / "screen-1__en.html").write_text(html_en, encoding="utf-8")
    return article, mockup_dir


def test_visible_text_track_faixa_drift() -> None:
    """PT-BR mockup shows 'Track' but xcstrings PT-BR for key 'Track' is 'Faixa'."""
    mod = _load_validator_module()
    article, mockup_dir = _build_visible_text_fixture(
        html_pt="<html><body><div class='track-btn'>Track</div></body></html>",
    )
    try:
        flow = {
            "mockup_plan": {
                "screens": [{
                    "name": "screen-1",
                    "source": "ios_required",
                    "visible_text": [
                        {"selector": ".track-btn", "source": "xcstrings", "key": "Track"},
                    ],
                }],
            },
        }
        xc_data = {"Track": {"en": "Track", "pt-BR": "Faixa"}}
        rep = mod.Report(article=str(article))
        mod._validate_visible_text(rep, article, flow, mockup_dir, xc_data)
        drifts = [f for f in rep.hard_fails if "xcstrings_locale_drift" in f]
        assert len(drifts) == 1, f"expected 1 xcstrings_locale_drift; got {rep.hard_fails!r}"
        msg = drifts[0]
        assert "expected 'Faixa'" in msg, f"expected diagnostic to cite 'Faixa'; got {msg!r}"
        assert "observed 'Track'" in msg, f"expected diagnostic to cite observed 'Track'; got {msg!r}"
    finally:
        shutil.rmtree(article, ignore_errors=True)


def test_visible_text_pre_bid_source_key_leak() -> None:
    """Mockup uses xcstrings SOURCE KEY 'Pre-Bid?' instead of localized value.

    Source key 'Enable Pre-Bid?' resolves to 'Enable Pre-Offer?' (en) / 'Ativar Pré-oferta?' (pt-BR).
    If the writer typed the SOURCE key 'Enable Pre-Bid?' into the PT-BR mockup, the validator
    must catch that as a drift even though the en VALUE happens to match the key.
    """
    mod = _load_validator_module()
    article, mockup_dir = _build_visible_text_fixture(
        html_pt="<html><body><div class='toggle-title'>Enable Pre-Bid?</div></body></html>",
        html_en="<html><body><div class='toggle-title'>Enable Pre-Offer?</div></body></html>",
    )
    try:
        flow = {
            "mockup_plan": {
                "screens": [{
                    "name": "screen-1",
                    "source": "ios_required",
                    "visible_text": [
                        {"selector": ".toggle-title", "source": "xcstrings", "key": "Enable Pre-Bid?"},
                    ],
                }],
            },
        }
        xc_data = {
            "Enable Pre-Bid?": {"en": "Enable Pre-Offer?", "pt-BR": "Ativar Pré-oferta?"},
        }
        rep = mod.Report(article=str(article))
        mod._validate_visible_text(rep, article, flow, mockup_dir, xc_data)
        drifts = [f for f in rep.hard_fails if "xcstrings_locale_drift" in f]
        # PT-BR drifted (source key leak), EN matched.
        assert len(drifts) == 1, f"expected 1 drift on PT-BR; got {rep.hard_fails!r}"
        assert "pt-br" in drifts[0], f"drift must be on pt-br locale; got {drifts[0]!r}"
        assert "'Ativar Pré-oferta?'" in drifts[0]
    finally:
        shutil.rmtree(article, ignore_errors=True)


def test_visible_text_invented_string_uncovered() -> None:
    """Mockup contains visible text not declared in visible_text or allowlist.

    Triggers visible_text_uncovered hard fail (this is the 'Selling now' / 'Your sales'
    class from PR #109 and PR #115).
    """
    mod = _load_validator_module()
    article, mockup_dir = _build_visible_text_fixture(
        html_pt="""<html><body>
            <div class='title'>Listings</div>
            <div class='invented-banner'>Selling now</div>
        </body></html>""",
    )
    try:
        flow = {
            "mockup_plan": {
                "screens": [{
                    "name": "screen-1",
                    "source": "ios_required",
                    "visible_text": [
                        {"selector": ".title", "source": "xcstrings", "key": "Listings"},
                    ],
                }],
            },
        }
        xc_data = {"Listings": {"en": "Listings", "pt-BR": "Listings"}}
        rep = mod.Report(article=str(article))
        mod._validate_visible_text(rep, article, flow, mockup_dir, xc_data)
        uncovered = [f for f in rep.hard_fails if "visible_text_uncovered" in f]
        assert len(uncovered) == 1, f"expected 1 uncovered fail; got {rep.hard_fails!r}"
        assert "Selling now" in uncovered[0], f"expected 'Selling now' diagnostic; got {uncovered[0]!r}"
    finally:
        shutil.rmtree(article, ignore_errors=True)


def test_visible_text_user_content_and_numeric_pass() -> None:
    """Numeric placeholders + user_content selectors pass without text comparison.

    Currency, time, and counts are already filtered by the noise regex. User-supplied
    content (product names, usernames) is exempt when declared with source=user_content.
    """
    mod = _load_validator_module()
    article, mockup_dir = _build_visible_text_fixture(
        html_pt="""<html><body>
            <div class='pname'>Charizard holo PSA 9</div>
            <div class='price-val'>R$ 75,00</div>
            <div class='timer'>0:18</div>
        </body></html>""",
    )
    try:
        flow = {
            "mockup_plan": {
                "screens": [{
                    "name": "screen-1",
                    "source": "ios_required",
                    "visible_text": [
                        {"selector": ".pname", "source": "user_content"},
                    ],
                    # .price-val + .timer have only numerics/currency, auto-filtered.
                }],
            },
        }
        rep = mod.Report(article=str(article))
        mod._validate_visible_text(rep, article, flow, mockup_dir, None)
        assert not rep.hard_fails, f"expected no fails; got {rep.hard_fails!r}"
    finally:
        shutil.rmtree(article, ignore_errors=True)


def test_visible_text_backend_locale_values_pass() -> None:
    """Backend-sourced text matches when locale_values are provided per locale."""
    mod = _load_validator_module()
    backend_pt = "Seu pedido não pôde ser entregue e foi devolvido ao vendedor"
    backend_en = "Your order could not be delivered and was returned to the seller"
    article, mockup_dir = _build_visible_text_fixture(
        html_pt=f"<html><body><div class='banner'>{backend_pt}</div></body></html>",
        html_en=f"<html><body><div class='banner'>{backend_en}</div></body></html>",
    )
    try:
        flow = {
            "mockup_plan": {
                "screens": [{
                    "name": "screen-1",
                    "source": "ios_required",
                    "visible_text": [
                        {
                            "selector": ".banner",
                            "source": "backend",
                            "path": "src/entities/transaction.py:631",
                            "locale_values": {"en": backend_en, "pt-br": backend_pt},
                        },
                    ],
                }],
            },
        }
        rep = mod.Report(article=str(article))
        mod._validate_visible_text(rep, article, flow, mockup_dir, None)
        assert not rep.hard_fails, f"expected no fails for backend match; got {rep.hard_fails!r}"

        # Negative case: PT-BR drift -> the validator must catch a backend drift too.
        (mockup_dir / "screen-1__pt-br.html").write_text(
            "<html><body><div class='banner'>Was returned</div></body></html>",
            encoding="utf-8",
        )
        rep2 = mod.Report(article=str(article))
        mod._validate_visible_text(rep2, article, flow, mockup_dir, None)
        drifts = [f for f in rep2.hard_fails if "xcstrings_locale_drift" in f]
        assert len(drifts) == 1, f"expected 1 backend drift; got {rep2.hard_fails!r}"
        assert "source=backend" in drifts[0]
    finally:
        shutil.rmtree(article, ignore_errors=True)


# --- xcstrings snapshot fallback + soft-degrade (post-#117 hybrid F+G-lite) ---


def _write_snapshot_at(repo_root: Path, mapping: dict[str, dict[str, str]]) -> Path:
    snap_dir = repo_root / "scripts"
    snap_dir.mkdir(parents=True, exist_ok=True)
    snap_path = snap_dir / "xcstrings-snapshot.json"
    payload = {
        "generated_at": "2026-05-12T10:00:00+00:00",
        "source": "Localizable.xcstrings",
        "key_count": len(mapping),
        "strings": mapping,
    }
    snap_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    return snap_path


def test_visible_text_snapshot_fallback_resolves_track_faixa() -> None:
    """JAMBLE_IOS_ROOT unset BUT scripts/xcstrings-snapshot.json exists:
    validator resolves via snapshot and still HARD-fails drifts."""
    mod = _load_validator_module()
    article, mockup_dir = _build_visible_text_fixture(
        html_pt="<html><body><div class='track-btn'>Track</div></body></html>",
    )
    try:
        real_repo = Path(mod.REPO_ROOT)
        snap_path = real_repo / "scripts" / "xcstrings-snapshot.json"
        backup = snap_path.read_text(encoding="utf-8") if snap_path.exists() else None
        try:
            _write_snapshot_at(real_repo, {"Track": {"en": "Track", "pt-BR": "Faixa"}})
            xc_data, xc_source = mod._resolve_xcstrings_data(None, real_repo)
            assert xc_source == "snapshot", f"expected snapshot fallback; got {xc_source!r}"
            assert xc_data is not None and "Track" in xc_data
            flow = {
                "mockup_plan": {"screens": [{"name": "screen-1", "source": "ios_required",
                    "visible_text": [{"selector": ".track-btn", "source": "xcstrings", "key": "Track"}]}]},
            }
            rep = mod.Report(article=str(article))
            mod._validate_visible_text(rep, article, flow, mockup_dir, xc_data, xc_source)
            drifts = [f for f in rep.hard_fails if "xcstrings_locale_drift" in f]
            assert len(drifts) == 1, f"snapshot must hard-fail Track→Faixa drift; got {rep.hard_fails!r}"
            assert "'Faixa'" in drifts[0]
            skipped = [w for w in rep.soft_warns if "xcstrings_resolution_skipped" in w]
            assert not skipped, f"snapshot resolved; no skipped-warn expected; got {rep.soft_warns!r}"
        finally:
            if backup is None:
                snap_path.unlink(missing_ok=True)
            else:
                snap_path.write_text(backup, encoding="utf-8")
    finally:
        shutil.rmtree(article, ignore_errors=True)


def test_visible_text_missing_root_and_missing_snapshot_emits_one_warn() -> None:
    """No root, no snapshot -> ONE soft warn per article, no cascade."""
    mod = _load_validator_module()
    article, mockup_dir = _build_visible_text_fixture(
        html_pt="""<html><body>
            <div class='title'>Sell mode</div>
            <div class='opt-name'>Real Time Offer</div>
            <div class='opt-sub'>The last offerer wins at the end of the time.</div>
        </body></html>""",
    )
    try:
        flow = {
            "mockup_plan": {"screens": [{"name": "screen-1", "source": "ios_required",
                "visible_text": [
                    {"selector": ".title", "source": "xcstrings", "key": "Sell mode"},
                    {"selector": ".opt-name", "source": "xcstrings", "key": "Auction"},
                    {"selector": ".opt-sub", "source": "xcstrings", "key": "The last bidder wins at the end of the time."},
                ]}]},
        }
        rep = mod.Report(article=str(article))
        mod._validate_visible_text(rep, article, flow, mockup_dir, None, "")
        skipped = [w for w in rep.soft_warns if "xcstrings_resolution_skipped" in w]
        assert len(skipped) == 1, f"expected exactly 1 summary soft warn; got {rep.soft_warns!r}"
        assert not rep.hard_fails, f"no hard fails expected; got {rep.hard_fails!r}"
        assert "3" in skipped[0], f"summary must cite skip count; got {skipped[0]!r}"
    finally:
        shutil.rmtree(article, ignore_errors=True)


def test_visible_text_declared_selectors_covered_when_xcstrings_skipped() -> None:
    """Declared selectors mark elements covered even when xcstrings can't resolve;
    prevents visible_text_uncovered cascade."""
    mod = _load_validator_module()
    article, mockup_dir = _build_visible_text_fixture(
        html_pt="""<html><body>
            <div class='title'>Sell mode</div>
            <div class='extra'>SOMETHING_NOT_DECLARED</div>
        </body></html>""",
    )
    try:
        flow = {
            "mockup_plan": {"screens": [{"name": "screen-1", "source": "ios_required",
                "visible_text": [{"selector": ".title", "source": "xcstrings", "key": "Sell mode"}]}]},
        }
        rep = mod.Report(article=str(article))
        mod._validate_visible_text(rep, article, flow, mockup_dir, None, "")
        uncovered = [f for f in rep.hard_fails if "visible_text_uncovered" in f]
        assert len(uncovered) == 1, f"expected uncovered ONLY on .extra; got {rep.hard_fails!r}"
        assert "SOMETHING_NOT_DECLARED" in uncovered[0]
        assert "Sell mode" not in uncovered[0], f".title was declared; got {uncovered[0]!r}"
    finally:
        shutil.rmtree(article, ignore_errors=True)


def test_visible_text_drift_hard_fails_with_snapshot_available() -> None:
    """Snapshot path catches drifts as HARD fails (full enforcement in CI)."""
    mod = _load_validator_module()
    article, mockup_dir = _build_visible_text_fixture(
        html_pt="<html><body><div class='nav'>Cancelado</div></body></html>",
    )
    try:
        xc_data = {"Returned": {"en": "Returned", "pt-BR": "Devolvido"}}
        flow = {
            "mockup_plan": {"screens": [{"name": "screen-1", "source": "ios_required",
                "visible_text": [{"selector": ".nav", "source": "xcstrings", "key": "Returned"}]}]},
        }
        rep = mod.Report(article=str(article))
        mod._validate_visible_text(rep, article, flow, mockup_dir, xc_data, "snapshot")
        drifts = [f for f in rep.hard_fails if "xcstrings_locale_drift" in f]
        assert len(drifts) == 1, f"snapshot must hard-fail drift; got {rep.hard_fails!r}"
        assert "'Devolvido'" in drifts[0]
        assert "'Cancelado'" in drifts[0]
        skipped = [w for w in rep.soft_warns if "xcstrings_resolution_skipped" in w]
        assert not skipped, f"snapshot resolved; no skipped-warn; got {rep.soft_warns!r}"
    finally:
        shutil.rmtree(article, ignore_errors=True)


def test_validator_passes_when_path_in_negative_scan_with_risk_flag() -> None:
    """Correct encoding for "I checked this surface and it's absent": move
    the path to source_of_truth.negative_scan AND raise a matching
    risk_flag. The rule must not fire on negative_scan paths, but must fire
    if negative_scan is non-empty AND risk_flags is empty."""
    fake_root = Path(tempfile.mkdtemp(prefix="fake-ios-neg-", dir="/tmp"))
    try:
        # No PHANTOM dir created; paths in negative_scan are intentionally absent
        art = _calibration_fixture("calib-iosneg-", intercom_id=8881106)
        try:
            flow_yaml = (art / "flow.yml").read_text(encoding="utf-8")
            flow_yaml = flow_yaml.replace(
                "  ios_files: []",
                "  ios_files: []\n  negative_scan:\n    - PHANTOM/Analytics/\n    - PHANTOM/Stats/",
            )
            flow_yaml = flow_yaml.replace(
                "risk_flags: []",
                'risk_flags:\n  - "feature-may-not-exist: PHANTOM analytics surface absent"',
            )
            (art / "flow.yml").write_text(flow_yaml, encoding="utf-8")
            env = {**os.environ, "JAMBLE_IOS_ROOT": str(fake_root)}
            proc = subprocess.run(
                [sys.executable, str(VALIDATOR), str(art)],
                capture_output=True, text=True, cwd=REPO_ROOT, env=env,
            )
            combined = proc.stdout + proc.stderr
            assert "source_of_truth_path_missing" not in combined, (
                f"negative_scan paths must not fire source_of_truth_path_missing; "
                f"got {combined!r}"
            )
            assert "negative_scan_without_risk" not in combined, (
                f"risk_flags is non-empty so negative_scan_without_risk must not fire; "
                f"got {combined!r}"
            )

            # Now drop the risk_flag and confirm negative_scan_without_risk fires
            flow_no_risk = flow_yaml.replace(
                'risk_flags:\n  - "feature-may-not-exist: PHANTOM analytics surface absent"',
                "risk_flags: []",
            )
            (art / "flow.yml").write_text(flow_no_risk, encoding="utf-8")
            proc2 = subprocess.run(
                [sys.executable, str(VALIDATOR), str(art)],
                capture_output=True, text=True, cwd=REPO_ROOT, env=env,
            )
            combined2 = proc2.stdout + proc2.stderr
            assert "negative_scan_without_risk" in combined2, (
                f"empty risk_flags + non-empty negative_scan must fire "
                f"negative_scan_without_risk; got {combined2!r}"
            )
        finally:
            shutil.rmtree(art, ignore_errors=True)
    finally:
        shutil.rmtree(fake_root, ignore_errors=True)


# ---------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------

TESTS = [
    test_duplicate_priority_fails,
    test_missing_source_arrays_fails,
    test_empty_sources_with_justification_passes,
    test_priorities_unsorted_fails,
    test_init_propagates_new_article_mode,
    test_init_per_article_mode_overrides_batch,
    test_expected_fails_strict_one_match_fails,
    test_expected_fails_strict_all_match_passes,
    test_expected_fails_list_positional_passes,
    test_expected_fails_list_length_mismatch_fails,
    test_runner_validate_no_flow_returns_nonzero,
    test_runner_checklist_no_flow_does_not_print_ready,
    test_runner_checklist_metadata_missing_is_phase6,
    test_runner_checklist_count_matches_validator,
    test_runner_validate_forwards_validator_nonzero,
    test_writer_packet_contains_all_sections,
    test_writer_packet_exits_2_on_missing_flow,
    test_writer_packet_does_not_modify_files,
    test_write_skeletons_creates_audit_triplet,
    test_write_skeletons_does_not_overwrite_without_force,
    test_skeletons_contain_skeleton_todo_marker,
    test_skeletons_use_dynamic_date,
    test_validator_fails_on_audit_skeleton_unfilled,
    test_validator_passes_audit_skeleton_after_markers_removed,
    test_skeletons_drop_pass_like_defaults,
    test_runner_maps_audit_skeleton_unfilled_to_phase7,
    test_validator_fails_on_multiple_h1_headings,
    test_validator_passes_with_single_h1_heading,
    test_validator_fails_on_markdown_table_2col,
    test_validator_fails_on_markdown_table_3col,
    test_validator_fails_on_raw_html_table,
    test_validator_passes_on_bullet_list_table_replacement,
    test_validator_ignores_audit_markdown_tables,
    test_validator_fails_on_orphan_mockup_html,
    test_validator_passes_when_orphan_in_allowlist,
    test_validator_fails_on_nonexistent_ios_path,
    test_orphan_rule_displays_safe_path_outside_repo_root,
    test_orphan_rule_skips_when_mockup_not_required,
    test_source_of_truth_warns_when_env_unset_with_ios_paths,
    test_source_of_truth_check_skipped_disqualifies_exception_free,
    test_unanchored_icon_review_check_warns_and_disqualifies,
    test_visible_text_track_faixa_drift,
    test_visible_text_pre_bid_source_key_leak,
    test_visible_text_invented_string_uncovered,
    test_visible_text_user_content_and_numeric_pass,
    test_visible_text_backend_locale_values_pass,
    test_visible_text_snapshot_fallback_resolves_track_faixa,
    test_visible_text_missing_root_and_missing_snapshot_emits_one_warn,
    test_visible_text_declared_selectors_covered_when_xcstrings_skipped,
    test_visible_text_drift_hard_fails_with_snapshot_available,
    test_validator_passes_when_path_in_negative_scan_with_risk_flag,
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Regression tests for the article factory")
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
