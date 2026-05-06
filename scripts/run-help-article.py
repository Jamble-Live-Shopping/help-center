#!/usr/bin/env python3
"""Single-article runner for the Help Center Article Factory.

Reads `articles/<slug>/flow.yml` + `metadata.yml` and helps the worker
(human or LLM) produce a v2 article. Three phases, each callable
independently:

    plan        Print an ordered checklist of artefacts the article needs
                (pt-br.md, en.md, mockup HTMLs + PNGs, audit triplet)
                derived from flow.yml.mockup_plan.screens, metadata.yml,
                and the RUNBOOK 8-phase contract.

    validate    Run scripts/validate-article-flow.py on the article and
                forward its exit code. Mirrors what CI runs on PRs.

    checklist   Run validator, parse hard fails, and group them by
                RUNBOOK phase (Phase 1 audit, Phase 5 body, Phase 6
                metadata, Phase 7 audits, Phase 8 PR & sync, etc.).
                Output is a human-readable list of what to fix next,
                ordered by phase.

This runner does NOT generate content (pt-br.md / en.md / mockup HTMLs /
PNGs / audit MDs). It structures the work and turns validator hard fails
into an actionable plan. PR #79 will add an "article writer" mode for
one article; PR #80 will add the batch runner.

Usage:
    scripts/run-help-article.py articles/<slug> --phase plan
    scripts/run-help-article.py articles/<slug> --phase validate
    scripts/run-help-article.py articles/<slug> --phase checklist
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = REPO_ROOT / "scripts" / "validate-article-flow.py"

# Mapping from validator hard-fail rule -> RUNBOOK phase that owns the fix.
RULE_TO_PHASE: dict[str, tuple[int, str]] = {
    "backend_files_not_audited": (1, "Phase 1, Code audit"),
    "em_dash": (5, "Phase 5, Article body"),
    "en_dash": (5, "Phase 5, Article body"),
    "rdollar_leak_en": (5, "Phase 5, Article body"),
    "currency_required": (5, "Phase 5, Article body"),
    "auction_word": (5, "Phase 5, Article body"),
    "forbidden_term": (5, "Phase 5, Article body"),
    "content_missing": (5, "Phase 5, Article body"),
    "toc_missing_pt": (5, "Phase 5, Article body"),
    "toc_missing_en": (5, "Phase 5, Article body"),
    "locale_lowercase": (6, "Phase 6, metadata.yml"),
    "intercom_id_mismatch": (6, "Phase 6, metadata.yml"),
    "description_too_long": (6, "Phase 6, metadata.yml"),
    "description_empty": (6, "Phase 6, metadata.yml"),
    "slug_mismatch": (6, "Phase 6, metadata.yml"),
    "mockup_png_missing": (4, "Phase 4, Render PNGs"),
    "mockup_png_unreadable": (4, "Phase 4, Render PNGs"),
    "mockup_png_too_narrow": (4, "Phase 4, Render PNGs"),
    "mockup_html_missing": (3, "Phase 3, HTML mockups"),
    "mockup_screens_empty": (3, "Phase 3, HTML mockups"),
    "mockup_screen_no_name": (3, "Phase 3, HTML mockups"),
    "mockup_declared_not_in_pt": (5, "Phase 5, Article body (image refs)"),
    "mockup_declared_not_in_en": (5, "Phase 5, Article body (image refs)"),
    "mockup_referenced_not_declared": (5, "Phase 5, Article body (image refs)"),
    "icon_not_in_mockup": (3, "Phase 3, HTML mockups (icons)"),
    "icon_no_source_proof": (3, "Phase 3, HTML mockups (icons)"),
    "feather_fallback_enabled": (3, "Phase 3, HTML mockups (icons)"),
    "audit_missing": (7, "Phase 7, Audit triplet"),
    "code_audit_inconsistent": (7, "Phase 7, Audit triplet"),
    "content_audit_missing_stale_feature": (7, "Phase 7, Audit triplet"),
    "content_audit_scan6_not_stale": (7, "Phase 7, Audit triplet"),
    "content_audit_stale_table_missing": (7, "Phase 7, Audit triplet"),
    "compliance_all_pass_with_risks": (7, "Phase 7, Audit triplet"),
    "published_with_unresolved_risks": (8, "Phase 8, PR and sync"),
}

FAIL_LINE = re.compile(r"\bFAIL\s+\[([a-z0-9_]+)\]\s*(.*)$", re.IGNORECASE)


def run_validator(article_dir: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), str(article_dir)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def parse_fails(output: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for line in output.splitlines():
        m = FAIL_LINE.search(line)
        if m:
            out.append((m.group(1), m.group(2).strip()))
    return out


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}


def phase_plan(article_dir: Path) -> int:
    slug = article_dir.name
    flow = load_yaml(article_dir / "flow.yml")
    meta = load_yaml(article_dir / "metadata.yml")

    if not flow:
        print(f"ERROR: {article_dir.relative_to(REPO_ROOT)}/flow.yml is missing or empty", file=sys.stderr)
        return 2

    print(f"# Article plan: {slug}")
    print()
    job = flow.get("job_to_be_done") or "(empty, fill in flow.yml)"
    audience = flow.get("audience") or "(unset)"
    mode = flow.get("mode") or "(unset)"
    intercom_id = meta.get("intercom_id") or flow.get("intercom_id") or "(none)"
    print(f"Job to be done : {job}")
    print(f"Audience       : {audience}")
    print(f"Mode           : {mode}")
    print(f"Intercom ID    : {intercom_id}")
    print()

    screens = []
    plan = flow.get("mockup_plan") or {}
    if plan.get("required"):
        for s in plan.get("screens") or []:
            if isinstance(s, dict) and s.get("name"):
                screens.append(s["name"])

    print("Required artefacts (RUNBOOK Phases 1 to 8):")
    print()
    print("  Phase 1: code audit")
    ios_files = (flow.get("source_of_truth") or {}).get("ios_files") or []
    backend_files = (flow.get("source_of_truth") or {}).get("backend_files") or []
    print(f"    - Read iOS sources: {len(ios_files)} file(s)")
    for f in ios_files:
        print(f"        * {f}")
    print(f"    - Read backend sources: {len(backend_files)} file(s)")
    for f in backend_files:
        print(f"        * {f}")
    print()
    print("  Phase 3: HTML mockups (per locale)")
    if not screens:
        print("    - (no screens declared in flow.yml.mockup_plan)")
    else:
        for s in screens:
            print(f"    - mockup-sources/{s}__pt-br.html")
            print(f"    - mockup-sources/{s}__en.html")
    print()
    print("  Phase 4: render PNGs DPR3 (>=900px wide)")
    if not screens:
        print("    - (no screens; nothing to render)")
    else:
        for s in screens:
            print(f"    - assets/mockups/{slug}__{s}__pt-br__v3.png")
            print(f"    - assets/mockups/{slug}__{s}__en__v3.png")
    print()
    print("  Phase 5: article body")
    print(f"    - articles/{slug}/pt-br.md (primary)")
    print(f"    - articles/{slug}/en.md   (1:1 mirror, currency localised)")
    print()
    print("  Phase 6: metadata.yml")
    print(f"    - locales.pt-br.{{title, description<=140}}")
    print(f"    - locales.en.{{title, description<=140}}")
    print()
    print("  Phase 7: audit triplet")
    if intercom_id and intercom_id != "(none)":
        print(f"    - audit/code-audit-{intercom_id}.md (cite iOS file:line)")
        print(f"    - audit/content-audit-{intercom_id}.md (with explicit Stale-feature audit table)")
        print(f"    - audit/compliance-{intercom_id}.md  (no 'ALL PASS' if active risk_flags)")
    else:
        print(f"    - audit triplet keyed by intercom_id (currently unknown)")
    print()
    print("  Phase 8: PR + sync")
    print(f"    - draft PR with risk_flags surfaced in body")
    print(f"    - state=published only after risk_flags resolved or documented in resolved_decisions")
    print()

    risk_flags = flow.get("risk_flags") or []
    resolved = flow.get("resolved_decisions") or []
    if risk_flags:
        print(f"Risk flags ({len(risk_flags)}):")
        for r in risk_flags:
            print(f"    - {r}")
    if resolved:
        print(f"Resolved decisions ({len(resolved)}):")
        for r in resolved:
            if isinstance(r, dict):
                who = r.get("decided_by", "?")
                when = r.get("decided_at", "?")
                why = r.get("rationale", "?")
                print(f"    - {r.get('risk', '?')} (by {who} on {when}): {why}")
    print()
    print(f"Next: scripts/run-help-article.py articles/{slug} --phase validate")
    return 0


def phase_validate(article_dir: Path) -> int:
    rc, out = run_validator(article_dir)
    print(out, end="" if out.endswith("\n") else "\n")
    return rc


def phase_checklist(article_dir: Path) -> int:
    rc, out = run_validator(article_dir)
    fails = parse_fails(out)
    print(f"# Checklist: {article_dir.relative_to(REPO_ROOT)}")
    print()
    if not fails:
        print("0 hard fails. Article is ready for review and PR.")
        print()
        print(f"Next: open a draft PR. The CI workflow validate-article-flow")
        print(f"      will re-run the validator on the changed paths.")
        return 0

    by_phase: dict[tuple[int, str], list[tuple[str, str]]] = defaultdict(list)
    for rule, msg in fails:
        phase = RULE_TO_PHASE.get(rule, (99, "Unmapped (check process/00-RUNBOOK.md)"))
        by_phase[phase].append((rule, msg))

    for (phase_num, phase_name), entries in sorted(by_phase.items()):
        suffix = "s" if len(entries) != 1 else ""
        print(f"## {phase_name}  ({len(entries)} fail{suffix})")
        for rule, msg in entries:
            print(f"  - [{rule}] {msg}")
        print()

    print(f"Total hard fails: {len(fails)}")
    print()
    print(f"Next: address phase by phase, starting with the lowest phase number.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Single-article runner for the Help Center factory")
    parser.add_argument("article_dir", help="path to articles/<slug>")
    parser.add_argument(
        "--phase",
        choices=["plan", "validate", "checklist"],
        required=True,
        help="which phase to run",
    )
    args = parser.parse_args()

    article_dir = Path(args.article_dir).resolve()
    if not article_dir.is_dir():
        print(f"ERROR: {args.article_dir} is not a directory", file=sys.stderr)
        return 2

    try:
        article_dir.relative_to(REPO_ROOT)
    except ValueError:
        print(f"ERROR: {args.article_dir} must be inside {REPO_ROOT}", file=sys.stderr)
        return 2

    if args.phase == "plan":
        return phase_plan(article_dir)
    if args.phase == "validate":
        return phase_validate(article_dir)
    if args.phase == "checklist":
        return phase_checklist(article_dir)
    return 2


if __name__ == "__main__":
    sys.exit(main())
