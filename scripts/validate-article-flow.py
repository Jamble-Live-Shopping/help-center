#!/usr/bin/env python3
"""Validate article flow contract.

Reads articles/<slug>/flow.yml + metadata.yml + content files + mockups +
audit triplet. Enforces 13 hard fails and 2 soft warns per process/ doctrine.

Usage:
    scripts/validate-article-flow.py articles/<slug>           # validate one
    scripts/validate-article-flow.py --all                     # validate all articles/*/flow.yml
    scripts/validate-article-flow.py --changed <base_ref>      # validate articles changed vs base ref

Exit code 0 if all hard fails pass. Exit 1 with structured error report
otherwise. Soft warns echo to stderr regardless.

Source of truth: process/00-RUNBOOK.md and process/templates/article-flow.yml.
"""
from __future__ import annotations

import argparse
import os
import re
import struct
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
ICONS_POOL_DIR = REPO_ROOT / "assets" / "icons-ios"
MOCKUPS_DIR = REPO_ROOT / "assets" / "mockups"

EM_DASH = "—"
EN_DASH = "–"
AUCTION_PATTERN = re.compile(r"\b(auction|leil[aã]o)\b", re.IGNORECASE)
RDOLLAR_PATTERN = re.compile(r"R\$")


@dataclass
class Report:
    article: str
    hard_fails: list[str] = field(default_factory=list)
    soft_warns: list[str] = field(default_factory=list)

    def fail(self, rule: str, msg: str) -> None:
        self.hard_fails.append(f"[{rule}] {msg}")

    def warn(self, rule: str, msg: str) -> None:
        self.soft_warns.append(f"[{rule}] {msg}")


def png_dimensions(path: Path) -> tuple[int, int] | None:
    """Read PNG width and height from header without external deps."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    try:
        width, height = struct.unpack(">II", data[16:24])
    except struct.error:
        return None
    return width, height


def load_yaml(path: Path) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None
    try:
        return yaml.safe_load(text) or {}
    except yaml.YAMLError as exc:
        return None


def validate_article(article_dir: Path) -> Report:
    slug = article_dir.name
    rep = Report(article=slug)

    # ---- existence preflight
    flow_path = article_dir / "flow.yml"
    metadata_path = article_dir / "metadata.yml"
    pt_path = article_dir / "pt-br.md"
    en_path = article_dir / "en.md"
    mockup_dir = article_dir / "mockup-sources"
    audit_dir = article_dir / "audit"

    if not flow_path.exists():
        rep.fail("flow_missing", f"{flow_path.relative_to(REPO_ROOT)} not found")
        return rep
    if not metadata_path.exists():
        rep.fail("metadata_missing", f"{metadata_path.relative_to(REPO_ROOT)} not found")
        return rep

    flow = load_yaml(flow_path)
    metadata = load_yaml(metadata_path)
    if flow is None:
        rep.fail("flow_yaml_parse", f"could not parse {flow_path.relative_to(REPO_ROOT)}")
        return rep
    if metadata is None:
        rep.fail("metadata_yaml_parse", f"could not parse {metadata_path.relative_to(REPO_ROOT)}")
        return rep

    # ---- rule 1: metadata.yml locales lowercase
    locales_section = metadata.get("locales") or {}
    for key in locales_section.keys():
        if key != key.lower():
            rep.fail(
                "locale_lowercase",
                f"metadata.yml locales.{key} must be lowercase (use {key.lower()})",
            )
    default_locale = metadata.get("default_locale", "")
    if default_locale and default_locale != default_locale.lower():
        rep.fail(
            "locale_lowercase",
            f"metadata.yml default_locale '{default_locale}' must be lowercase",
        )

    # ---- rule 2: flow.intercom_id matches metadata.intercom_id (if both present)
    flow_id = flow.get("intercom_id")
    meta_id = metadata.get("intercom_id")
    if flow_id is not None and meta_id is not None and flow_id != meta_id:
        rep.fail(
            "intercom_id_mismatch",
            f"flow.yml intercom_id={flow_id} does not match metadata.yml intercom_id={meta_id}",
        )

    # ---- rule 3: pt-br.md and en.md exist
    if not pt_path.exists():
        rep.fail("content_missing", "pt-br.md not found")
    if not en_path.exists():
        rep.fail("content_missing", "en.md not found")

    pt_body = pt_path.read_text(encoding="utf-8") if pt_path.exists() else ""
    en_body = en_path.read_text(encoding="utf-8") if en_path.exists() else ""

    # ---- rule 4: descriptions <= 140 chars per locale in metadata
    for lang, locale_meta in locales_section.items():
        if not isinstance(locale_meta, dict):
            continue
        desc = (locale_meta.get("description") or "").strip()
        if len(desc) > 140:
            rep.fail(
                "description_too_long",
                f"metadata.yml locales.{lang}.description has {len(desc)} chars (max 140)",
            )
        if not desc:
            rep.fail(
                "description_empty",
                f"metadata.yml locales.{lang}.description is empty",
            )

    # ---- rule 5: zero em-dash and en-dash in both md
    if EM_DASH in pt_body:
        rep.fail("em_dash", f"pt-br.md contains {pt_body.count(EM_DASH)} em-dash(es)")
    if EN_DASH in pt_body:
        rep.fail("en_dash", f"pt-br.md contains {pt_body.count(EN_DASH)} en-dash(es)")
    if EM_DASH in en_body:
        rep.fail("em_dash", f"en.md contains {en_body.count(EM_DASH)} em-dash(es)")
    if EN_DASH in en_body:
        rep.fail("en_dash", f"en.md contains {en_body.count(EN_DASH)} en-dash(es)")

    # ---- rule 6: zero R$ in en.md body
    en_rdollar_count = len(RDOLLAR_PATTERN.findall(en_body))
    if en_rdollar_count > 0:
        rep.fail(
            "rdollar_leak_en",
            f"en.md contains {en_rdollar_count} R$ occurrence(s) (use $ in EN body)",
        )

    # ---- rule 7: currency_required gate (R$ in pt-br.md if true)
    currency_required = bool(flow.get("currency_required", False))
    if currency_required:
        pt_rdollar_count = len(RDOLLAR_PATTERN.findall(pt_body))
        if pt_rdollar_count == 0:
            rep.fail(
                "currency_required",
                "flow.yml declares currency_required=true but pt-br.md contains no R$",
            )

    # ---- rule 8: zero auction/leilao in both md
    pt_auction = AUCTION_PATTERN.findall(pt_body)
    if pt_auction:
        rep.fail(
            "auction_word",
            f"pt-br.md contains banned word(s): {pt_auction[:3]}",
        )
    en_auction = AUCTION_PATTERN.findall(en_body)
    if en_auction:
        rep.fail(
            "auction_word",
            f"en.md contains banned word(s): {en_auction[:3]}",
        )

    # ---- rule 9: mockup PNG width >= 900 (DPR3)
    mockup_plan = flow.get("mockup_plan") or {}
    mockup_required = bool(mockup_plan.get("required", False))
    screens = mockup_plan.get("screens") or []

    if mockup_required and screens:
        for screen in screens:
            if not isinstance(screen, dict):
                continue
            name = screen.get("name", "")
            if not name:
                rep.fail("mockup_screen_no_name", f"screen missing name in mockup_plan")
                continue
            for lang in ("pt-br", "en"):
                png_name = f"{slug}__{name}__{lang}__v3.png"
                png_path = MOCKUPS_DIR / png_name
                # Try v2 fallback if v3 missing (some legacy articles)
                if not png_path.exists():
                    png_path_v2 = MOCKUPS_DIR / f"{slug}__{name}__{lang}__v2.png"
                    if png_path_v2.exists():
                        png_path = png_path_v2
                    else:
                        rep.fail(
                            "mockup_png_missing",
                            f"missing PNG for {slug}__{name}__{lang}__v3 (or v2 fallback)",
                        )
                        continue
                dims = png_dimensions(png_path)
                if dims is None:
                    rep.fail("mockup_png_unreadable", f"could not read PNG dimensions: {png_path.name}")
                    continue
                width, _ = dims
                if width < 900:
                    rep.fail(
                        "mockup_png_too_narrow",
                        f"{png_path.name} width={width}px (min 900 for DPR3)",
                    )

    # ---- rule 10: mockup HTML pair pt-br + en for each screen name
    if mockup_required and screens and mockup_dir.exists():
        for screen in screens:
            if not isinstance(screen, dict):
                continue
            name = screen.get("name", "")
            if not name:
                continue
            pt_html = mockup_dir / f"{name}__pt-br.html"
            en_html = mockup_dir / f"{name}__en.html"
            if not pt_html.exists():
                rep.fail("mockup_html_missing", f"missing {pt_html.relative_to(REPO_ROOT)}")
            if not en_html.exists():
                rep.fail("mockup_html_missing", f"missing {en_html.relative_to(REPO_ROOT)}")

    # ---- rule 11: audit triplet present
    intercom_id = meta_id or flow_id
    if intercom_id is None:
        rep.warn("audit_id_unknown", "no intercom_id in metadata.yml or flow.yml; cannot check audit triplet")
    else:
        for kind in ("code-audit", "content-audit", "compliance"):
            audit_path = audit_dir / f"{kind}-{intercom_id}.md"
            if not audit_path.exists():
                rep.fail("audit_missing", f"missing {audit_path.relative_to(REPO_ROOT)}")

    # ---- rule 12: icons_required in pool OR HTML comment
    icons_required = flow.get("icons_required") or []
    if icons_required:
        # collect HTML mockup-source content for grep
        html_blob = ""
        if mockup_dir.exists():
            for html_file in mockup_dir.glob("*.html"):
                try:
                    html_blob += html_file.read_text(encoding="utf-8") + "\n"
                except OSError:
                    continue

        for icon_name in icons_required:
            in_pool = any(
                (ICONS_POOL_DIR / f"{icon_name}.{ext}").exists()
                for ext in ("svg", "png", "webp")
            )
            in_html = (
                f"Assets.xcassets/{icon_name}.imageset" in html_blob
                or f'alt="{icon_name}"' in html_blob
                or f"<!-- icon: {icon_name}" in html_blob
            )
            if not in_pool and not in_html:
                rep.fail(
                    "icon_missing",
                    f"icon '{icon_name}' not found in assets/icons-ios/ pool nor referenced in HTML mockup-sources",
                )

    # ---- rule 13: forbidden_terms grep (hard fail on match)
    cc = flow.get("content_contract") or {}
    forbidden_terms = cc.get("forbidden_terms") or []
    for term in forbidden_terms:
        if not isinstance(term, str) or not term:
            continue
        if term.startswith("regex:"):
            pattern = re.compile(term[len("regex:"):], re.IGNORECASE)
        else:
            pattern = re.compile(re.escape(term), re.IGNORECASE)
        if pattern.search(pt_body):
            rep.fail("forbidden_term", f"pt-br.md contains banned term '{term}'")
        if pattern.search(en_body):
            rep.fail("forbidden_term", f"en.md contains banned term '{term}'")

    # ---- icons_fallback_feather: hard ban for UI chrome
    if flow.get("icons_fallback_feather", False):
        rep.fail(
            "feather_fallback_enabled",
            "icons_fallback_feather=true requires explicit reviewer override and risk_flag entry",
        )

    # ---- rule 14: must_answer keywords (soft warn)
    must_answer = cc.get("must_answer") or []
    for topic in must_answer:
        if not isinstance(topic, str) or not topic:
            continue
        # Soft check: at least one significant word from the topic appears
        # in pt-br.md and en.md. Use stems > 4 chars to avoid false positives.
        words = [w for w in re.findall(r"\w+", topic.lower()) if len(w) >= 5]
        if not words:
            continue
        pt_lower = pt_body.lower()
        en_lower = en_body.lower()
        for word in words:
            if word not in pt_lower:
                rep.warn(
                    "must_answer_pt",
                    f"keyword '{word}' (from must_answer: '{topic}') not found in pt-br.md",
                )
                break
        for word in words:
            if word not in en_lower:
                rep.warn(
                    "must_answer_en",
                    f"keyword '{word}' (from must_answer: '{topic}') not found in en.md",
                )
                break

    # ---- rule 15: risk_flags non-empty (soft warn reminder)
    risk_flags = flow.get("risk_flags") or []
    if risk_flags:
        for flag in risk_flags:
            rep.warn("risk_flag_reminder", f"surface in PR body: {flag}")

    return rep


def find_articles(args: argparse.Namespace) -> list[Path]:
    if args.all:
        return sorted(p.parent for p in (REPO_ROOT / "articles").glob("*/flow.yml"))
    if args.changed:
        try:
            out = subprocess.check_output(
                ["git", "diff", "--name-only", args.changed, "HEAD", "--", "articles/"],
                cwd=REPO_ROOT,
                text=True,
            )
        except subprocess.CalledProcessError:
            return []
        article_dirs: set[Path] = set()
        for line in out.splitlines():
            parts = line.split("/")
            if len(parts) >= 2 and parts[0] == "articles":
                cand = REPO_ROOT / "articles" / parts[1]
                if (cand / "flow.yml").exists():
                    article_dirs.add(cand)
        return sorted(article_dirs)
    if args.paths:
        out: list[Path] = []
        for raw in args.paths:
            p = (REPO_ROOT / raw).resolve()
            if (p / "flow.yml").exists():
                out.append(p)
            elif p.name == "flow.yml":
                out.append(p.parent)
            else:
                print(f"WARN: {raw} has no flow.yml, skipping", file=sys.stderr)
        return out
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate article flow contracts")
    parser.add_argument("paths", nargs="*", help="article dirs (e.g. articles/<slug>)")
    parser.add_argument("--all", action="store_true", help="validate all articles/*/flow.yml")
    parser.add_argument("--changed", metavar="REF", help="validate articles changed vs git ref")
    args = parser.parse_args()

    articles = find_articles(args)
    if not articles:
        print("No articles to validate (use --all, --changed <ref>, or pass article dirs)")
        return 0

    reports = [validate_article(d) for d in articles]
    total_fails = sum(len(r.hard_fails) for r in reports)
    total_warns = sum(len(r.soft_warns) for r in reports)

    for r in reports:
        if r.hard_fails or r.soft_warns:
            print(f"\n=== {r.article} ===")
            for line in r.hard_fails:
                print(f"  FAIL  {line}")
            for line in r.soft_warns:
                print(f"  warn  {line}", file=sys.stderr)
        else:
            print(f"\n=== {r.article} === OK")

    print(f"\nValidated {len(reports)} article(s): {total_fails} hard fail(s), {total_warns} soft warn(s)")
    return 1 if total_fails else 0


if __name__ == "__main__":
    sys.exit(main())
