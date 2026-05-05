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

Exit code 0 if every replayed article matches its allowlist (or 0 hard
fails when no allowlist is set). Exit 1 if any replay fails its allowlist.

Allowlist convention: each golden flow may declare a top-level
`replay_allowlist:` field with a list of rule names that are tolerated as
hard fails (e.g. ["mockup_referenced_not_declared"] when the historical
article uses v2 mockups that the validator's strict v3 regex misses).
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

RULE_FROM_LINE = re.compile(r"\bFAIL\s+\[([a-z0-9_]+)\]", re.IGNORECASE)


def slug_from_golden_path(path: Path) -> str:
    name = path.name
    # Accept "<slug>.flow.yml" or "<slug>.yml"
    if name.endswith(".flow.yml"):
        return name[: -len(".flow.yml")]
    if name.endswith(".yml"):
        return name[: -len(".yml")]
    return name


def list_golden_flows(filter_slug: str | None = None) -> list[Path]:
    if not GOLDEN_DIR.exists():
        return []
    paths = sorted(GOLDEN_DIR.glob("*.flow.yml")) + sorted(GOLDEN_DIR.glob("*.yml"))
    paths = [p for p in paths if p.name.endswith(".yml") and not p.name.endswith(".flow.yml") or p.name.endswith(".flow.yml")]
    paths = sorted(set(paths))
    if filter_slug:
        paths = [p for p in paths if slug_from_golden_path(p) == filter_slug]
    return paths


def load_allowlist(golden_path: Path) -> list[str]:
    try:
        loaded = yaml.safe_load(golden_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return []
    al = loaded.get("replay_allowlist") or []
    return [str(x) for x in al if isinstance(x, str)]


def run_validator(slug: str) -> tuple[int, str]:
    """Return (returncode, combined_output)."""
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), str(ARTICLES_DIR / slug)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def parse_hard_fails(output: str) -> list[str]:
    return [m.group(1) for m in RULE_FROM_LINE.finditer(output)]


def parse_summary(output: str) -> tuple[int, int]:
    """Extract '<N> hard fail(s), <M> soft warn(s)' from validator summary."""
    m = re.search(r"(\d+)\s+hard fail\(s\),\s+(\d+)\s+soft warn\(s\)", output)
    if not m:
        return (0, 0)
    return (int(m.group(1)), int(m.group(2)))


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
            "allowlist": [],
            "in_allowlist": True,
        }

    backup = None
    article_had_flow = article_flow.exists()
    if article_had_flow:
        backup = article_flow.read_bytes()

    try:
        shutil.copyfile(golden_path, article_flow)
        rc, out = run_validator(slug)
        fail_rules = parse_hard_fails(out)
        hard_count, soft_count = parse_summary(out)
        allowlist = load_allowlist(golden_path)
        # In allowlist when every observed fail rule appears in allowlist,
        # OR when there are 0 fails (allowlist not needed).
        unexpected = [r for r in fail_rules if r not in allowlist]
        in_allowlist = len(unexpected) == 0
        return {
            "slug": slug,
            "status": "ok" if in_allowlist else "fail",
            "hard_fail_count": hard_count,
            "soft_warn_count": soft_count,
            "fail_rules": fail_rules,
            "allowlist": allowlist,
            "unexpected": unexpected,
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

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(render_table(results))
        print()
        for r in results:
            if r["status"] == "fail":
                print(f"FAIL {r['slug']}: unexpected rules outside allowlist: {r.get('unexpected')}")
            elif r["status"] == "skip":
                print(f"SKIP {r['slug']}: {r.get('reason')}")

    any_fail = any(r["status"] == "fail" for r in results)
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
