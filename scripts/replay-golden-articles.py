#!/usr/bin/env python3
"""Golden replay harness for the article-flow validator.

Reads each `process/golden-flows/<slug>.flow.yml`, swaps it temporarily into
`articles/<slug>/flow.yml`, runs `scripts/validate-article-flow.py
articles/<slug>`, captures the report, then restores the original
`articles/<slug>/flow.yml` (or removes it if the article had none).

Goal: calibrate the validator against historical v2 articles. The script
does NOT modify the article body, mockups, audits, or any other file.

Usage:
    scripts/replay-golden-articles.py             # run all golden flows
    scripts/replay-golden-articles.py <slug>      # run one
    scripts/replay-golden-articles.py --json      # machine-readable output

Exit code 0 if every replayed article matches its expected_fails. Exit 1
if any replay deviates (unexpected rule, count mismatch, missing
`contains` substring). Exit 2 on script error.

Expected fails format (preferred, structured):

    expected_fails:
      - rule: content_audit_scan6_not_stale
        count: 1
        contains: "Scan 6"
        reason: "legacy audit used Scan 6 for alt-text, not stale-feature"
        removal_path: "Add real stale-feature subsection"

Each expected_fail must match at least `count` occurrences of `rule` in
the validator output. The combined output of those occurrences must
contain the `contains` substring.

Backward compat: legacy `replay_allowlist: [rule_names]` is still parsed
but emits a stderr DEPRECATION warning. New golden flows must use
`expected_fails`.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_DIR = REPO_ROOT / "process" / "golden-flows"
ARTICLES_DIR = REPO_ROOT / "articles"
VALIDATOR = REPO_ROOT / "scripts" / "validate-article-flow.py"

FAIL_LINE_PATTERN = re.compile(r"\bFAIL\s+\[([a-z0-9_]+)\]\s*(.*)$", re.IGNORECASE)


def slug_from_golden_path(path: Path) -> str:
    name = path.name
    if name.endswith(".flow.yml"):
        return name[: -len(".flow.yml")]
    if name.endswith(".yml"):
        return name[: -len(".yml")]
    return name


def list_golden_flows(filter_slug: str | None = None) -> list[Path]:
    if not GOLDEN_DIR.exists():
        return []
    paths = sorted(GOLDEN_DIR.glob("*.flow.yml"))
    if filter_slug:
        paths = [p for p in paths if slug_from_golden_path(p) == filter_slug]
    return paths


def load_expectations(golden_path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Return (expected_fails, deprecation_warnings).

    expected_fails is a list of dicts {rule, count, contains, reason,
    removal_path}. Legacy replay_allowlist entries are converted to
    expected_fails with count=1 and an empty contains string.
    """
    warnings: list[str] = []
    try:
        loaded = yaml.safe_load(golden_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return [], [f"could not parse {golden_path.name}"]

    expected: list[dict[str, Any]] = []

    raw_expected = loaded.get("expected_fails") or []
    for entry in raw_expected:
        if not isinstance(entry, dict):
            continue
        rule = entry.get("rule")
        if not isinstance(rule, str) or not rule:
            continue
        expected.append({
            "rule": rule,
            "count": int(entry.get("count", 1)),
            "contains": str(entry.get("contains", "")),
            "reason": str(entry.get("reason", "")),
            "removal_path": str(entry.get("removal_path", "")),
        })

    legacy = loaded.get("replay_allowlist") or []
    if legacy:
        warnings.append(
            f"DEPRECATION: {golden_path.name} uses legacy `replay_allowlist`. "
            f"Migrate to `expected_fails: [{{rule, count, contains, reason, "
            f"removal_path}}]` (see process/golden-flows/README.md)."
        )
        for rule_name in legacy:
            if not isinstance(rule_name, str) or not rule_name:
                continue
            expected.append({
                "rule": rule_name,
                "count": 1,
                "contains": "",
                "reason": "legacy replay_allowlist (no structured reason)",
                "removal_path": "migrate to expected_fails",
            })

    return expected, warnings


def run_validator(slug: str) -> tuple[int, str]:
    """Return (returncode, combined_output)."""
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), str(ARTICLES_DIR / slug)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def parse_fail_lines(output: str) -> list[tuple[str, str]]:
    """Return list of (rule_name, full_message) for every FAIL line."""
    out: list[tuple[str, str]] = []
    for line in output.splitlines():
        m = FAIL_LINE_PATTERN.search(line)
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def parse_summary(output: str) -> tuple[int, int]:
    """Extract '<N> hard fail(s), <M> soft warn(s)' from validator summary."""
    m = re.search(r"(\d+)\s+hard fail\(s\),\s+(\d+)\s+soft warn\(s\)", output)
    if not m:
        return (0, 0)
    return (int(m.group(1)), int(m.group(2)))


def evaluate_expectations(
    fails: list[tuple[str, str]],
    expected: list[dict[str, Any]],
) -> tuple[bool, list[str]]:
    """Return (in_allowlist, deviation_messages)."""
    deviations: list[str] = []
    actual_by_rule: dict[str, list[str]] = {}
    for rule, msg in fails:
        actual_by_rule.setdefault(rule, []).append(msg)

    expected_rules = {e["rule"] for e in expected}

    # Check each expected_fail
    for entry in expected:
        rule = entry["rule"]
        want_count = int(entry["count"])
        contains = entry.get("contains", "")
        actual_msgs = actual_by_rule.get(rule, [])
        if len(actual_msgs) != want_count:
            deviations.append(
                f"rule '{rule}': expected count={want_count}, got {len(actual_msgs)}"
            )
            continue
        if contains and not any(contains in m for m in actual_msgs):
            deviations.append(
                f"rule '{rule}': none of the {len(actual_msgs)} fail message(s) "
                f"contain expected substring {contains!r}"
            )

    # Any rule fired but not declared = unexpected
    for rule in actual_by_rule:
        if rule not in expected_rules:
            deviations.append(f"unexpected rule '{rule}' (not in expected_fails)")

    return (len(deviations) == 0), deviations


def replay_one(golden_path: Path) -> dict[str, Any]:
    slug = slug_from_golden_path(golden_path)
    article_dir = ARTICLES_DIR / slug
    article_flow = article_dir / "flow.yml"

    if not article_dir.exists():
        return {
            "slug": slug,
            "status": "skip",
            "reason": f"articles/{slug} does not exist",
            "hard_fail_count": 0,
            "soft_warn_count": 0,
            "fail_rules": [],
            "expected": [],
            "deviations": [],
            "warnings": [],
            "in_allowlist": True,
        }

    backup = None
    article_had_flow = article_flow.exists()
    if article_had_flow:
        backup = article_flow.read_bytes()

    expected, warnings = load_expectations(golden_path)

    try:
        shutil.copyfile(golden_path, article_flow)
        rc, out = run_validator(slug)
        fails = parse_fail_lines(out)
        hard_count, soft_count = parse_summary(out)
        in_allowlist, deviations = evaluate_expectations(fails, expected)
        return {
            "slug": slug,
            "status": "ok" if in_allowlist else "fail",
            "hard_fail_count": hard_count,
            "soft_warn_count": soft_count,
            "fail_rules": [r for r, _ in fails],
            "expected": [e["rule"] for e in expected],
            "deviations": deviations,
            "warnings": warnings,
            "in_allowlist": in_allowlist,
            "validator_exit": rc,
        }
    finally:
        if article_had_flow:
            article_flow.write_bytes(backup or b"")
        else:
            try:
                article_flow.unlink()
            except FileNotFoundError:
                pass


def render_table(results: list[dict[str, Any]]) -> str:
    headers = ["article", "hard", "warn", "rules", "status"]
    rows = []
    for r in results:
        rules = ", ".join(r.get("fail_rules") or []) or "-"
        rows.append([
            r["slug"],
            str(r.get("hard_fail_count", 0)),
            str(r.get("soft_warn_count", 0)),
            rules if len(rules) <= 64 else rules[:61] + "...",
            r["status"],
        ])
    widths = [max(len(h), max((len(r[i]) for r in rows), default=0)) for i, h in enumerate(headers)]
    lines = []
    lines.append("  ".join(h.ljust(w) for h, w in zip(headers, widths)))
    lines.append("  ".join("-" * w for w in widths))
    for r in rows:
        lines.append("  ".join(c.ljust(w) for c, w in zip(r, widths)))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Replay validator against golden flows")
    parser.add_argument("slug", nargs="?", help="run only the named golden flow")
    parser.add_argument("--json", action="store_true", help="machine-readable JSON output")
    args = parser.parse_args()

    golden_paths = list_golden_flows(args.slug)
    if not golden_paths:
        msg = f"No golden flows found in {GOLDEN_DIR}"
        if args.slug:
            msg = f"No golden flow named {args.slug!r} in {GOLDEN_DIR}"
        print(msg, file=sys.stderr)
        return 2

    results = [replay_one(p) for p in golden_paths]

    # Emit warnings (deprecations) on stderr regardless of output mode.
    for r in results:
        for w in r.get("warnings", []):
            print(w, file=sys.stderr)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(render_table(results))
        print()
        for r in results:
            if r["status"] == "fail":
                for d in r.get("deviations", []):
                    print(f"FAIL {r['slug']}: {d}")
            elif r["status"] == "skip":
                print(f"SKIP {r['slug']}: {r.get('reason')}")

    any_fail = any(r["status"] == "fail" for r in results)
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
