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
    scripts/run-help-article.py articles/<slug> --phase writer-packet [--write-skeletons [--force]]

Note: `checklist` is informational, NOT a gate. The final gate is
`--phase validate`, which forwards the validator's exit code.
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
    # Phase 0: contract setup (article does not even have a parseable flow.yml)
    "flow_missing": (0, "Phase 0, Contract setup"),
    "flow_yaml_parse": (0, "Phase 0, Contract setup"),
    # Phase 1: code audit
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
    "metadata_missing": (6, "Phase 6, metadata.yml"),
    "metadata_yaml_parse": (6, "Phase 6, metadata.yml"),
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


def preflight(article_dir: Path) -> int:
    """Common contract preflight for every phase.

    Returns 0 if the article is well-formed enough to be processed, or 2
    with a clear stderr message if not. The runner must NEVER print
    "ready" or report 0 fails when these checks do not pass: the
    underlying validator silently skips paths without a flow.yml, so
    every phase has to fail loud here instead.
    """
    if not article_dir.exists():
        print(f"ERROR: {article_dir} does not exist", file=sys.stderr)
        return 2
    if not article_dir.is_dir():
        print(f"ERROR: {article_dir} is not a directory", file=sys.stderr)
        return 2

    flow_path = article_dir / "flow.yml"
    if not flow_path.exists():
        rel = article_dir.relative_to(REPO_ROOT) if article_dir.is_relative_to(REPO_ROOT) else article_dir
        print(
            f"ERROR [flow_missing]: {rel}/flow.yml is missing. "
            f"This is a Phase 0 (contract setup) error: bootstrap the flow with "
            f"scripts/init-article-flow.py --slug {article_dir.name} or copy "
            f"process/templates/article-flow.yml.",
            file=sys.stderr,
        )
        return 2
    try:
        parsed = yaml.safe_load(flow_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(
            f"ERROR [flow_yaml_parse]: cannot parse {flow_path.relative_to(REPO_ROOT)}: {exc}",
            file=sys.stderr,
        )
        return 2
    if not isinstance(parsed, dict):
        print(
            f"ERROR [flow_yaml_parse]: {flow_path.relative_to(REPO_ROOT)} does not parse to a mapping",
            file=sys.stderr,
        )
        return 2

    metadata_path = article_dir / "metadata.yml"
    if metadata_path.exists():
        try:
            meta_parsed = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            print(
                f"ERROR [metadata_yaml_parse]: cannot parse "
                f"{metadata_path.relative_to(REPO_ROOT)}: {exc}",
                file=sys.stderr,
            )
            return 2
        if not isinstance(meta_parsed, dict):
            print(
                f"ERROR [metadata_yaml_parse]: "
                f"{metadata_path.relative_to(REPO_ROOT)} does not parse to a mapping",
                file=sys.stderr,
            )
            return 2

    return 0


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
        print("0 hard fails. Article looks ready against the validator.")
        print()
        print("This phase is informational, NOT a gate. The final gate is:")
        print(f"    python3 scripts/run-help-article.py {article_dir.relative_to(REPO_ROOT)} --phase validate")
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
    print("This phase is informational, NOT a gate. Use --phase validate as the final gate.")
    return 0


# ---------------------------- phase: writer-packet ----------------------------

def phase_writer_packet(article_dir: Path) -> int:
    """Print a structured Markdown packet that briefs Claude (or any human
    worker) on what the article needs, in the order the worker should
    produce it. Read-only: this phase does NOT modify any file.
    """
    slug = article_dir.name
    flow = load_yaml(article_dir / "flow.yml")
    meta = load_yaml(article_dir / "metadata.yml")
    intercom_id = meta.get("intercom_id") or flow.get("intercom_id") or "<intercom_id>"

    print(f"# Writer packet: {slug}")
    print()

    # ---- Identity
    print("## Article identity")
    print()
    print(f"- slug         : `{slug}`")
    print(f"- mode         : {flow.get('mode') or '(unset)'}")
    print(f"- audience     : {flow.get('audience') or '(unset)'}")
    print(f"- workflow     : {flow.get('workflow') or '(unset)'}")
    print(f"- intercom_id  : {intercom_id}")
    print(f"- state        : {meta.get('state') or '(unset)'}")
    print(f"- collection_id: {meta.get('collection_id') or '(unset)'}")
    print()

    # ---- Job to be done
    print("## Job to be done")
    print()
    print(f"> {flow.get('job_to_be_done') or '(empty, fill in flow.yml)'}")
    print()

    # ---- Source-of-truth reading checklist
    print("## Source of truth (read before writing)")
    print()
    sot = flow.get("source_of_truth") or {}
    ios_files = sot.get("ios_files") or []
    backend_files = sot.get("backend_files") or []
    legal = sot.get("legal") or []
    support = sot.get("support_context") or []
    print(f"- iOS files ({len(ios_files)}):")
    for f in ios_files:
        print(f"  - [ ] {f}")
    print(f"- Backend files ({len(backend_files)}):")
    for f in backend_files:
        print(f"  - [ ] {f}")
    if legal:
        print(f"- Legal references ({len(legal)}):")
        for l in legal:
            print(f"  - [ ] {l}")
    if support:
        print(f"- Support context ({len(support)}):")
        for s in support:
            print(f"  - [ ] {s}")
    print()

    # ---- Content contract
    print("## Content contract")
    print()
    cc = flow.get("content_contract") or {}
    must_answer = cc.get("must_answer") or []
    forbidden = cc.get("forbidden_terms") or []
    must_not_say = cc.get("must_not_say") or []
    print(f"### must_answer ({len(must_answer)})")
    for q in must_answer:
        print(f"- [ ] {q}")
    print()
    print(f"### forbidden_terms ({len(forbidden)})  -- HARD FAIL on grep, both md files")
    for t in forbidden:
        print(f"- {t}")
    print()
    print(f"### must_not_say ({len(must_not_say)})  -- soft warn, reviewer judgment")
    for t in must_not_say:
        print(f"- {t}")
    print()

    # ---- Mockup plan
    print("## Mockup plan")
    print()
    mp = flow.get("mockup_plan") or {}
    required = bool(mp.get("required", False))
    screens = mp.get("screens") or []
    print(f"- required : {required}")
    print(f"- screens  : {len(screens)} declared")
    print()
    if screens:
        print("| screen name | source | expected HTML pair | expected PNG pair |")
        print("|---|---|---|---|")
        for s in screens:
            if not isinstance(s, dict):
                continue
            name = s.get("name", "")
            source = s.get("source", "")
            html = f"mockup-sources/{name}__pt-br.html + __en.html"
            png = f"assets/mockups/{slug}__{name}__{{pt-br,en}}__v3.png"
            print(f"| {name} | {source} | {html} | {png} |")
        print()
        print("Each screen produces two HTML files and two PNGs DPR3 (>=900px wide).")
        print()

    # ---- Icons
    print("## Icons required")
    print()
    icons = flow.get("icons_required") or []
    print(f"- declared: {len(icons)}")
    for icon in icons:
        print(f"  - [ ] {icon} (must appear in HTML alt or comment as `Assets.xcassets/{icon}.imageset` or `<!-- icon: {icon} -->`)")
    print()
    print(f"- icons_fallback_feather: {flow.get('icons_fallback_feather', False)}")
    print()

    # ---- Risks
    print("## Risks")
    print()
    risks = flow.get("risk_flags") or []
    resolved = flow.get("resolved_decisions") or []
    if not risks and not resolved:
        print("- (none)")
    else:
        if risks:
            print(f"### Active risk_flags ({len(risks)})")
            for r in risks:
                print(f"- {r}")
            print()
        if resolved:
            print(f"### resolved_decisions ({len(resolved)})")
            for r in resolved:
                if isinstance(r, dict):
                    risk = r.get("risk", "?")
                    by = r.get("decided_by", "?")
                    when = r.get("decided_at", "?")
                    why = r.get("rationale", "?")
                    print(f"- {risk}  (decided by {by} on {when}: {why})")
            print()
    if risks and not resolved and (meta.get("state") or "").lower() == "published":
        print("> WARN: state=published with active risk_flags and no resolved_decisions.")
        print("> Validator will block the merge until risks are resolved or documented.")
        print()

    # ---- Deliverables in order
    print("## Deliverables (produce in this order)")
    print()
    print(f"1. `articles/{slug}/audit/code-audit-{intercom_id}.md` (cite iOS file:line per claim)")
    print(f"2. `articles/{slug}/pt-br.md` (PRIMARY, writer's first focus)")
    print(f"3. `articles/{slug}/en.md` (1:1 mirror, currency localised, no R$ in EN body)")
    if screens:
        print(f"4. mockup HTMLs in `articles/{slug}/mockup-sources/` (one pair per screen above)")
        png_cmd_lines = []
        for s in screens:
            if not isinstance(s, dict) or not s.get("name"):
                continue
            name = s["name"]
            png_cmd_lines.append(f"   node scripts/shot-retina.mjs articles/{slug}/mockup-sources/{name}__pt-br.html assets/mockups/{slug}__{name}__pt-br__v3.png")
            png_cmd_lines.append(f"   node scripts/shot-retina.mjs articles/{slug}/mockup-sources/{name}__en.html assets/mockups/{slug}__{name}__en__v3.png")
        print(f"5. render PNGs DPR3 (commands):")
        print("   ```bash")
        for l in png_cmd_lines:
            print(l)
        print("   ```")
    else:
        print(f"4. (no mockups declared; skip)")
        print(f"5. (no mockups declared; skip)")
    print(f"6. `articles/{slug}/audit/content-audit-{intercom_id}.md` (with explicit Stale-feature audit table)")
    print(f"   `articles/{slug}/audit/compliance-{intercom_id}.md`     (no 'ALL PASS' if active risk_flags remain)")
    print(f"7. final gate (article is shippable iff this exits 0):")
    print()
    print("   ```bash")
    print(f"   python3 scripts/run-help-article.py articles/{slug} --phase validate")
    print("   ```")
    print()
    print("Open a draft PR only after the final gate exits 0.")
    return 0


# ---------------------------- write skeletons (audit triplet only) ----------------------------

AUDIT_SKELETONS = {
    "code-audit": """\
# Code audit, article {intercom_id} ({slug})

Date: {date}
Source iOS: Jamble-iOS develop. Sources cited in flow.yml.
xcstrings: `Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings`

## Claims article vs source code

| Article claim | Source | Verdict |
|---|---|---|
| (fill: claim 1) | (file:line) | MATCH / MISMATCH |

## Verdict

(Resolve uncertainty before declaring ship-ready. The validator rejects
"ship-ready" when the body still contains 'PARTIAL', 'not re-audited',
'requires cross-check', 'to be verified', or 'TBD'.)
""",
    "content-audit": """\
# Content audit, article {intercom_id} ({slug})

Date: {date}

## 1. PII / sensitive data
Verdict: (PASS / BLOCKER + detail)

## 2. Banned words (auction / leilao)
Verdict: PASS

## 3. Currency
Verdict: PASS

## 4. Word diet
Verdict: PASS

## 5. Tone (against Jamble voice guidelines)
Verdict: PASS

## 6. Alt text quality
Verdict: PASS

## 7. Stale-feature audit

Confirms every feature, button, and label described in the article still
exists in production. Verdicts: `live_in_ios` | `live_in_backend` |
`product_confirmed` | `deprecated` | `unknown_blocker`.

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| (fill: feature 1) | (file path) | live | {date} | (name) | live_in_ios |

Verdict: (PASS / BLOCKER + detail)

## Result

ALL N SCANS PASS. Zero BLOCKER.
""",
    "compliance": """\
# Compliance audit, article {intercom_id} ({slug})

Date: {date}
Reference: process/12-procedure-compliance.md (17 checks)

| # | Check | Result |
|---|---|---|
| 1 | iOS code audit done before drafting | (PASS / BLOCKER) |

## Verdict

(Do NOT write 'ALL PASS' if the article still has active risk_flags
without a corresponding resolved_decisions entry; the validator will
fail.)
""",
}


def write_skeletons(article_dir: Path, intercom_id: Any, force: bool) -> int:
    """Create the 3 audit triplet skeleton files. Surgical: only touches
    `articles/<slug>/audit/`, never modifies article body, mockups, or
    flow.yml. Skips files that already exist unless --force is set."""
    if intercom_id in (None, "", "<intercom_id>"):
        print(
            "ERROR: --write-skeletons requires an intercom_id in metadata.yml or flow.yml",
            file=sys.stderr,
        )
        return 2

    audit_dir = article_dir / "audit"
    audit_dir.mkdir(exist_ok=True)
    slug = article_dir.name
    today = "2026-05-06"  # stamp the day the skeletons are produced; worker updates as they audit

    written: list[str] = []
    skipped: list[str] = []
    for kind, template in AUDIT_SKELETONS.items():
        target = audit_dir / f"{kind}-{intercom_id}.md"
        if target.exists() and not force:
            skipped.append(target.name)
            continue
        body = template.format(intercom_id=intercom_id, slug=slug, date=today)
        target.write_text(body, encoding="utf-8")
        written.append(target.name)

    if written:
        print("Wrote audit skeleton(s):")
        for n in written:
            print(f"  - {audit_dir.relative_to(REPO_ROOT)}/{n}")
    if skipped:
        print("Skipped (already exists; pass --force to overwrite):")
        for n in skipped:
            print(f"  - {audit_dir.relative_to(REPO_ROOT)}/{n}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Single-article runner for the Help Center factory")
    parser.add_argument("article_dir", help="path to articles/<slug>")
    parser.add_argument(
        "--phase",
        choices=["plan", "validate", "checklist", "writer-packet"],
        required=True,
        help="which phase to run",
    )
    parser.add_argument(
        "--write-skeletons",
        action="store_true",
        help="(writer-packet only) also create empty audit triplet skeletons in articles/<slug>/audit/",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="(--write-skeletons only) overwrite existing audit files",
    )
    args = parser.parse_args()

    article_dir = Path(args.article_dir).resolve()

    try:
        article_dir.relative_to(REPO_ROOT)
    except ValueError:
        print(f"ERROR: {args.article_dir} must be inside {REPO_ROOT}", file=sys.stderr)
        return 2

    # Common preflight: fail loud on contract setup errors. The validator
    # silently skips paths without a flow.yml; without this preflight,
    # `validate` and `checklist` would mistakenly print "ready" on an
    # article that has no contract yet.
    rc = preflight(article_dir)
    if rc != 0:
        return rc

    if args.phase == "plan":
        return phase_plan(article_dir)
    if args.phase == "validate":
        return phase_validate(article_dir)
    if args.phase == "checklist":
        return phase_checklist(article_dir)
    if args.phase == "writer-packet":
        rc = phase_writer_packet(article_dir)
        if rc == 0 and args.write_skeletons:
            meta = load_yaml(article_dir / "metadata.yml")
            flow = load_yaml(article_dir / "flow.yml")
            intercom_id = meta.get("intercom_id") or flow.get("intercom_id")
            return write_skeletons(article_dir, intercom_id, args.force)
        return rc
    return 2


if __name__ == "__main__":
    sys.exit(main())
