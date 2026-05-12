#!/usr/bin/env python3
"""Generate the committed xcstrings snapshot for help-center CI.

Reads every `articles/*/flow.yml`, collects each unique `key` declared
under `visible_text:` entries with `source: xcstrings`, looks them up in
`<JAMBLE_IOS_ROOT>/RESOURCES/Localizable.xcstrings`, and writes the
filtered subset to `scripts/xcstrings-snapshot.json`.

The validator's resolution order is:
  1. JAMBLE_IOS_ROOT Localizable.xcstrings (full source-of-truth)
  2. scripts/xcstrings-snapshot.json  (this file's output, CI fallback)
  3. None (validator emits one soft warn per article, drift NOT enforced)

Refresh this snapshot whenever a `flow.yml` adds, renames, or removes
a `visible_text` xcstrings key.

Usage:
    JAMBLE_IOS_ROOT=/path/to/Jamble-iOS python3 scripts/snapshot-xcstrings.py
    JAMBLE_IOS_ROOT=/path/to/Jamble-iOS python3 scripts/snapshot-xcstrings.py --check
        # --check exits non-zero if the snapshot is stale.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = REPO_ROOT / "articles"
SNAPSHOT_PATH = REPO_ROOT / "scripts" / "xcstrings-snapshot.json"


def _resolve_ios_root() -> Path | None:
    env_val = os.environ.get("JAMBLE_IOS_ROOT", "").strip()
    if env_val:
        candidate = Path(env_val)
        if candidate.is_dir():
            return candidate
    default_root = Path.home() / "Projects" / "Jamble-iOS" / "Jamble"
    if default_root.is_dir():
        return default_root
    return None


def _xcstrings_path(ios_root: Path) -> Path | None:
    p = ios_root / "RESOURCES" / "Localizable.xcstrings"
    if p.exists():
        return p
    p = ios_root / "Jamble" / "RESOURCES" / "Localizable.xcstrings"
    if p.exists():
        return p
    return None


def collect_keys_from_articles() -> set[str]:
    keys: set[str] = set()
    if not ARTICLES_DIR.is_dir():
        return keys
    for flow_path in sorted(ARTICLES_DIR.glob("*/flow.yml")):
        try:
            data = yaml.safe_load(flow_path.read_text(encoding="utf-8")) or {}
        except (yaml.YAMLError, OSError):
            continue
        mockup_plan = data.get("mockup_plan") or {}
        if not isinstance(mockup_plan, dict):
            continue
        screens = mockup_plan.get("screens") or []
        if not isinstance(screens, list):
            continue
        for screen in screens:
            if not isinstance(screen, dict):
                continue
            for entry in screen.get("visible_text") or []:
                if not isinstance(entry, dict):
                    continue
                if entry.get("source") != "xcstrings":
                    continue
                key = entry.get("key")
                if isinstance(key, str) and key:
                    keys.add(key)
    return keys


def load_full_xcstrings(xc_path: Path) -> dict[str, dict[str, str]]:
    data = json.loads(xc_path.read_text(encoding="utf-8"))
    strings = data.get("strings", {})
    out: dict[str, dict[str, str]] = {}
    for key, entry in strings.items():
        if not isinstance(entry, dict):
            continue
        localizations = entry.get("localizations", {}) or {}
        bucket: dict[str, str] = {}
        for loc_key, loc_val in localizations.items():
            if not isinstance(loc_val, dict):
                continue
            string_unit = loc_val.get("stringUnit", {}) or {}
            v = string_unit.get("value")
            if isinstance(v, str):
                bucket[loc_key] = v
        out[key] = bucket
    return out


def build_snapshot(declared_keys: set[str], full_xc: dict) -> tuple[dict, list[str]]:
    filtered: dict[str, dict[str, str]] = {}
    missing: list[str] = []
    for key in sorted(declared_keys):
        if key in full_xc:
            filtered[key] = full_xc[key]
        else:
            missing.append(key)
    snapshot = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "source": "Localizable.xcstrings",
        "key_count": len(filtered),
        "strings": filtered,
    }
    return snapshot, missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Snapshot xcstrings for CI fallback")
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if the committed snapshot is stale",
    )
    args = parser.parse_args()

    declared = collect_keys_from_articles()
    print(f"declared visible_text xcstrings keys: {len(declared)}")

    ios_root = _resolve_ios_root()
    if ios_root is None:
        print("ERROR: cannot resolve iOS root. Set JAMBLE_IOS_ROOT=/path/to/Jamble-iOS", file=sys.stderr)
        return 2
    xc_path = _xcstrings_path(ios_root)
    if xc_path is None:
        print(f"ERROR: Localizable.xcstrings not found under {ios_root}", file=sys.stderr)
        return 2

    full_xc = load_full_xcstrings(xc_path)
    snapshot, missing = build_snapshot(declared, full_xc)

    if missing:
        print(f"WARN: {len(missing)} declared key(s) not in Localizable.xcstrings:", file=sys.stderr)
        for m in missing[:10]:
            print(f"  - '{m}'", file=sys.stderr)
        if len(missing) > 10:
            print(f"  ... +{len(missing) - 10} more", file=sys.stderr)

    if args.check:
        if not SNAPSHOT_PATH.exists():
            print(f"FAIL: --check mode but {SNAPSHOT_PATH.relative_to(REPO_ROOT)} does not exist.", file=sys.stderr)
            return 1
        existing = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
        existing.pop("generated_at", None)
        proposed_copy = json.loads(json.dumps(snapshot))
        proposed_copy.pop("generated_at", None)
        if existing != proposed_copy:
            print(
                f"FAIL: {SNAPSHOT_PATH.relative_to(REPO_ROOT)} is STALE. "
                f"Run `python3 scripts/snapshot-xcstrings.py` to refresh.",
                file=sys.stderr,
            )
            return 1
        print(f"OK: snapshot fresh ({snapshot['key_count']} keys).")
        return 0

    new_text = json.dumps(snapshot, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    SNAPSHOT_PATH.write_text(new_text, encoding="utf-8")
    print(f"OK: wrote {SNAPSHOT_PATH.relative_to(REPO_ROOT)} ({snapshot['key_count']} keys, {len(missing)} missing)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
