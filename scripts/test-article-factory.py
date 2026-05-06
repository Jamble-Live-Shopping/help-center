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


def test_runner_validate_dm_preserves_validator_nonzero() -> None:
    """run-help-article --phase validate must forward the validator's
    non-zero exit code on an article with real defects."""
    # Build a minimal article fixture that triggers at least one validator hard fail
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
    test_runner_validate_dm_preserves_validator_nonzero,
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
