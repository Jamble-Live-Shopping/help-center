#!/usr/bin/env python3
"""Validate article flow contract.

Reads articles/<slug>/flow.yml + metadata.yml + content files + mockups +
audit triplet. Enforces 21 hard fails and 2 soft warns per process/ doctrine.

Usage:
    scripts/validate-article-flow.py articles/<slug>           # validate one
    scripts/validate-article-flow.py --all                     # validate all articles/*/flow.yml
    scripts/validate-article-flow.py --changed <base_ref>      # validate articles changed vs base ref

Exit code 0 if all hard fails pass. Exit 1 with structured error report
otherwise. Soft warns echo to stderr regardless.

Source of truth: process/00-RUNBOOK.md, process/templates/article-flow.yml,
process/workflows/article-v2.yml.
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
WORKFLOW_FILE = REPO_ROOT / "process" / "workflows" / "article-v2.yml"

EM_DASH = "—"
EN_DASH = "–"
AUCTION_PATTERN = re.compile(r"\b(auction|leil[aã]o)\b", re.IGNORECASE)
RDOLLAR_PATTERN = re.compile(r"R\$")
H2_PATTERN = re.compile(r"^##\s+\S", re.MULTILINE)
PNG_REF_PATTERN = re.compile(r"!\[[^\]]*\]\([^)]*?/([a-z0-9-]+)__([a-z0-9-]+)__(pt-br|en)__v\d+\.png", re.IGNORECASE)


# Workflow config defaults; overridden by process/workflows/article-v2.yml when present.
DEFAULT_WORKFLOW = {
    "thresholds": {
        "toc_required_h2_count": 6,
        "mockup_png_min_width": 900,
        "description_max_chars": 140,
        "max_hard_fails": 0,
    },
    "toc_markers": {
        "pt_br": [
            "## Conteudo",
            "## Conteúdo",
            "## Sumario",
            "## Sumário",
            "## Neste guia",
            "[[toc]]",
        ],
        "en": [
            "## Contents",
            "## On this page",
            "## In this guide",
            "## Table of contents",
            "[[toc]]",
        ],
    },
    "audit_markers": {
        "code_audit_ship_ready_blockers": [
            "PARTIAL",
            "not re-audited",
            "not reaudited",
            "requires cross-check",
            "requires crosscheck",
            "to be verified",
            "TBD",
        ],
        # Tightened in v1.1.1: explicit stale-feature markers only. Bare
        # "Scan 6" is no longer accepted because audits like "Scan 6,
        # alt-text quality" passed the v1.1 check without doing the actual
        # stale-feature audit.
        "content_audit_stale_feature_markers": [
            "stale-feature",
            "stale feature",
            "Stale-feature audit",
            "Stale feature audit",
        ],
    },
    "toc_policy": "warn",
    "mockup_filename": {
        "current_suffix": "v3",
        "fallback_suffix": "v2",
    },
}


def load_workflow_config() -> dict[str, Any]:
    """Load process/workflows/article-v2.yml if present, fall back to defaults."""
    if not WORKFLOW_FILE.exists():
        return DEFAULT_WORKFLOW
    try:
        loaded = yaml.safe_load(WORKFLOW_FILE.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return DEFAULT_WORKFLOW
    # Shallow merge: per-key fallback to defaults if missing.
    cfg = {**DEFAULT_WORKFLOW}
    for k, v in loaded.items():
        if k in cfg and isinstance(cfg[k], dict) and isinstance(v, dict):
            merged = {**cfg[k]}
            merged.update(v)
            cfg[k] = merged
        else:
            cfg[k] = v
    return cfg


WORKFLOW = load_workflow_config()


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

    # ---- rule 0: metadata.slug matches folder slug (if metadata.slug declared)
    meta_slug = metadata.get("slug")
    if meta_slug is not None and meta_slug != slug:
        rep.fail(
            "slug_mismatch",
            f"metadata.yml slug='{meta_slug}' does not match folder name '{slug}'",
        )

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

    # ---- rule 9b: mockup_plan.required=true must declare at least one screen
    if mockup_required and not screens:
        rep.fail(
            "mockup_screens_empty",
            "flow.yml mockup_plan.required=true but screens list is empty (declare each screen with name + purpose + source)",
        )

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

    # ---- rule 10b (NEW, batch-10 gate): screen-scoped required_icons
    # check. Only fires when the field is declared and non-empty, so
    # historical flow.yml files without the field stay green.
    if mockup_required and screens and mockup_dir.exists():
        for screen in screens:
            if not isinstance(screen, dict):
                continue
            name = screen.get("name", "")
            req_icons = screen.get("required_icons") or []
            if not name or not req_icons:
                continue
            pt_html = mockup_dir / f"{name}__pt-br.html"
            en_html = mockup_dir / f"{name}__en.html"
            for lang_label, html_path in (("pt-br", pt_html), ("en", en_html)):
                if not html_path.exists():
                    # The HTML pair check above already failed; do not
                    # cascade a redundant icon error.
                    continue
                try:
                    blob = html_path.read_text(encoding="utf-8")
                except OSError:
                    continue
                for icon_name in req_icons:
                    if not isinstance(icon_name, str) or not icon_name:
                        continue
                    has_alt = f'alt="{icon_name}"' in blob
                    has_icon_comment = f"<!-- icon: {icon_name}" in blob
                    has_xcassets_comment = f"Assets.xcassets/{icon_name}.imageset" in blob
                    if not (has_alt or has_icon_comment or has_xcassets_comment):
                        rep.fail(
                            "screen_icon_not_in_html",
                            f"screen '{name}' declares required_icons "
                            f"['{icon_name}'] but it is not referenced in "
                            f"{html_path.relative_to(REPO_ROOT)}. Use "
                            f'alt="{icon_name}", `<!-- icon: {icon_name} -->`, '
                            f"or `Assets.xcassets/{icon_name}.imageset` "
                            f"comment in the HTML.",
                        )

    # ---- rule 10c (NEW, batch-10 gate): manual review_checks nudge.
    # Soft warn when a screen is sourced from iOS but no review_checks
    # are declared. Encourages explicit reviewer guidance before
    # scaling the batch. Soft only (backward-compatible).
    if mockup_required and screens:
        for screen in screens:
            if not isinstance(screen, dict):
                continue
            name = screen.get("name", "")
            source = screen.get("source", "")
            review_checks = screen.get("review_checks") or []
            if not name:
                continue
            if source == "ios_required" and not review_checks:
                rep.warn(
                    "screen_review_checks_missing",
                    f"screen '{name}' has source: ios_required but no "
                    f"review_checks declared. Add at least one of "
                    f"icons_match_ios_source, labels_match_xcstrings, "
                    f"no_invented_ui_state so the reviewer pack lists "
                    f"the manual gates explicitly.",
                )

    # ---- rule 10d (NEW, PR #89A, screen-scoped HTML text contract).
    #
    # Two HARD-FAIL rules for catching invented or missing UI text in
    # mockup HTMLs. Calibrated from the PR #87 DM bug: iOS Follow +
    # Message buttons are text-only (no icon), but the original mockup
    # invented a CSS-drawn purple-square pseudo-element on the Message
    # button. The required_icons rule (10b) is dormant when no icons
    # are required, so it could not catch this class of regression.
    # html_must_not_contain plugs that gap with deterministic grep:
    # if a screen's iOS source says "no icon", declare ["::before",
    # "<img", "<svg", "icon-"] in html_must_not_contain and the
    # validator hard-fails the moment any of those reappears.
    #
    # screen_html_required_text_missing (HARD FAIL):
    #   When `screen.html_must_contain.<lang>` is non-empty for `pt-br`
    #   or `en`, every string in that list must appear (case-sensitive
    #   substring) in the corresponding `<screen>__<lang>.html`.
    #
    # screen_html_forbidden_text_present (HARD FAIL):
    #   When `screen.html_must_not_contain` is non-empty (a flat list
    #   that applies to BOTH locales), no string in the list may
    #   appear in either `<screen>__pt-br.html` or `<screen>__en.html`.
    #
    # Pure substring grep. NO regex, NO LLM, NO semantic scoring.
    # Backward-compat: if both fields are absent or empty, the rules
    # are no-ops on that screen, so historical articles keep their
    # current validate output.
    if mockup_required and screens and mockup_dir.exists():
        for screen in screens:
            if not isinstance(screen, dict):
                continue
            name = screen.get("name", "")
            if not name:
                continue
            must_contain = screen.get("html_must_contain")
            must_not_contain_list = screen.get("html_must_not_contain") or []
            if not must_contain and not must_not_contain_list:
                continue  # backward-compat: no contract declared
            for lang_label in ("pt-br", "en"):
                html_path = mockup_dir / f"{name}__{lang_label}.html"
                if not html_path.exists():
                    continue
                try:
                    blob = html_path.read_text(encoding="utf-8")
                except OSError:
                    continue
                # Locale-specific required strings.
                required_for_lang: list[str] = []
                if isinstance(must_contain, dict):
                    raw = must_contain.get(lang_label)
                    if isinstance(raw, list):
                        required_for_lang = [
                            s for s in raw if isinstance(s, str) and s
                        ]
                for needle in required_for_lang:
                    if needle not in blob:
                        rep.fail(
                            "screen_html_required_text_missing",
                            f"screen '{name}' declares html_must_contain."
                            f"{lang_label} ['{needle}'] but it is not "
                            f"present in {html_path.relative_to(REPO_ROOT)}.",
                        )
                # Forbidden strings (apply to BOTH locales).
                forbidden = [
                    s for s in must_not_contain_list
                    if isinstance(s, str) and s
                ]
                for needle in forbidden:
                    if needle in blob:
                        rep.fail(
                            "screen_html_forbidden_text_present",
                            f"screen '{name}' declares html_must_not_contain "
                            f"['{needle}'] but it IS present in "
                            f"{html_path.relative_to(REPO_ROOT)}.",
                        )

    # ---- rule 11: audit triplet present
    intercom_id = meta_id or flow_id
    if intercom_id is None:
        rep.warn("audit_id_unknown", "no intercom_id in metadata.yml or flow.yml; cannot check audit triplet")
    else:
        for kind in ("code-audit", "content-audit", "compliance"):
            audit_path = audit_dir / f"{kind}-{intercom_id}.md"
            if not audit_path.exists():
                rep.fail("audit_missing", f"missing {audit_path.relative_to(REPO_ROOT)}")

    # ---- rule 11b: audit skeletons must be filled before ship.
    # `scripts/run-help-article.py --write-skeletons` stamps each section
    # with a `SKELETON_TODO` marker. Any audit file that still contains
    # the marker is unfilled work, regardless of whether the rest of the
    # validator passes. Hard fail. Catches the "I generated a skeleton
    # and ran the validator before actually auditing" path.
    if intercom_id is not None and audit_dir.exists():
        for kind in ("code-audit", "content-audit", "compliance"):
            audit_path = audit_dir / f"{kind}-{intercom_id}.md"
            if not audit_path.exists():
                continue
            try:
                body = audit_path.read_text(encoding="utf-8")
            except OSError:
                continue
            if "SKELETON_TODO" in body:
                count = body.count("SKELETON_TODO")
                rep.fail(
                    "audit_skeleton_unfilled",
                    f"{audit_path.relative_to(REPO_ROOT)} still contains "
                    f"{count} SKELETON_TODO marker(s). Replace each one with the "
                    f"actual audit content before declaring the article ready.",
                )

    # ---- rule 12: icons_required must be USED in HTML mockup AND have source proof
    #
    # Two separate checks:
    #   12a (icon_not_in_mockup): the icon name must appear in at least one
    #       HTML mockup-source as alt="<name>", "<!-- icon: <name> ... -->",
    #       or "Assets.xcassets/<name>.imageset". Without this, an icon can
    #       sit unused in the pool and still pass validation -- exactly the
    #       PR #69 bug we want to prevent.
    #   12b (icon_no_source_proof): the icon must also be traceable to an
    #       iOS source. Either it lives in the assets/icons-ios/ pool (any
    #       of svg/png/webp), OR the HTML mockup-source explicitly cites
    #       the iOS asset path via "Assets.xcassets/<name>.imageset" comment.
    #       Otherwise the worker may have used a Feather lookalike under
    #       the icon name, or a different image entirely.
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
            has_xcassets_comment = f"Assets.xcassets/{icon_name}.imageset" in html_blob
            has_alt = f'alt="{icon_name}"' in html_blob
            has_icon_comment = f"<!-- icon: {icon_name}" in html_blob
            in_html = has_xcassets_comment or has_alt or has_icon_comment

            if not in_html:
                pool_hint = (
                    " (icon is in assets/icons-ios/ pool but never used in any mockup; "
                    "either remove from icons_required or reference it in a mockup HTML)"
                    if in_pool
                    else ""
                )
                rep.fail(
                    "icon_not_in_mockup",
                    f"icon '{icon_name}' declared in flow.yml.icons_required but not "
                    f"referenced in any HTML mockup-source{pool_hint}. "
                    f"Use alt=\"{icon_name}\", '<!-- icon: {icon_name} -->', or "
                    f"'Assets.xcassets/{icon_name}.imageset' comment in the HTML.",
                )
                continue

            if not in_pool and not has_xcassets_comment:
                rep.fail(
                    "icon_no_source_proof",
                    f"icon '{icon_name}' is referenced in HTML but has no source proof: "
                    f"add the asset to assets/icons-ios/ (svg/png/webp) OR add "
                    f"'<!-- icon: {icon_name} from Assets.xcassets/{icon_name}.imageset -->' "
                    f"comment in the HTML mockup-source.",
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

    # =====================================================================
    # v1.1 hard fails: tightenings driven by Codex review of DM rewrite.
    # =====================================================================

    th = WORKFLOW.get("thresholds", {})
    toc_markers = WORKFLOW.get("toc_markers", {})
    audit_markers = WORKFLOW.get("audit_markers", {})

    # ---- rule 17: TOC policy.
    # Calibration after golden replay (2026-05-05): TOC is WARN by default
    # because 67/67 v2 articles in main today have no TOC. Per-article
    # override available via flow.yml.toc_required: true|false.
    #   flow.toc_required == True  -> hard fail when missing
    #   flow.toc_required == False -> skip the check entirely
    #   flow.toc_required unset    -> use workflow toc_policy (warn|strict|off)
    toc_threshold = int(th.get("toc_required_h2_count", 6))
    pt_h2_count = len(H2_PATTERN.findall(pt_body))
    en_h2_count = len(H2_PATTERN.findall(en_body))

    flow_toc_required = flow.get("toc_required")  # True | False | None
    workflow_toc_policy = (WORKFLOW.get("toc_policy") or "warn").lower()

    if flow_toc_required is True:
        toc_mode = "strict"
    elif flow_toc_required is False:
        toc_mode = "off"
    elif workflow_toc_policy in ("strict", "warn", "off"):
        toc_mode = workflow_toc_policy
    else:
        toc_mode = "warn"

    if toc_mode != "off":
        report_method = rep.fail if toc_mode == "strict" else rep.warn
        if pt_h2_count >= toc_threshold:
            pt_toc_markers = toc_markers.get("pt_br", []) or toc_markers.get("pt-br", [])
            if not any(m in pt_body for m in pt_toc_markers):
                report_method(
                    "toc_missing_pt",
                    f"pt-br.md has {pt_h2_count} H2 sections (>={toc_threshold}) but no TOC. "
                    f"Add a section like '## Conteúdo' or '## Neste guia' listing the article sections. "
                    f"(toc_policy={toc_mode}, override per-article via flow.yml.toc_required: true)",
                )
        if en_h2_count >= toc_threshold:
            en_toc_markers = toc_markers.get("en", [])
            if not any(m in en_body for m in en_toc_markers):
                report_method(
                    "toc_missing_en",
                    f"en.md has {en_h2_count} H2 sections (>={toc_threshold}) but no TOC. "
                    f"Add a section like '## Contents' or '## In this guide'. "
                    f"(toc_policy={toc_mode}, override per-article via flow.yml.toc_required: true)",
                )

    # ---- rule 18+19: bidirectional mockup-screen check
    # 18 (declared_but_not_referenced): every flow.yml screen must appear at
    #     least once in pt-br.md AND en.md as a markdown image reference.
    # 19 (referenced_but_not_declared): every PNG referenced via
    #     ![...](url with __<screen>__<lang>__vN.png) must correspond to a
    #     screen in flow.yml.mockup_plan.screens.
    if mockup_required:
        declared_screens = {s.get("name") for s in (screens or []) if isinstance(s, dict) and s.get("name")}

        # Extract referenced screens from each markdown (looking for slug__screen__lang__v3.png pattern)
        def extract_screen_refs(md_body: str) -> set[str]:
            return {m.group(2) for m in PNG_REF_PATTERN.finditer(md_body)}

        pt_refs = extract_screen_refs(pt_body)
        en_refs = extract_screen_refs(en_body)

        # 18: declared but not referenced
        for screen_name in sorted(declared_screens):
            if screen_name not in pt_refs:
                rep.fail(
                    "mockup_declared_not_in_pt",
                    f"screen '{screen_name}' is declared in flow.yml.mockup_plan.screens "
                    f"but no markdown image reference to '{slug}__{screen_name}__pt-br__v3.png' "
                    f"(or v2 fallback) found in pt-br.md. Either reference it or remove from flow.yml.",
                )
            if screen_name not in en_refs:
                rep.fail(
                    "mockup_declared_not_in_en",
                    f"screen '{screen_name}' is declared in flow.yml.mockup_plan.screens "
                    f"but no markdown image reference to '{slug}__{screen_name}__en__v3.png' "
                    f"(or v2 fallback) found in en.md.",
                )

        # 19: referenced but not declared
        for screen_name in sorted(pt_refs | en_refs):
            if screen_name not in declared_screens:
                rep.fail(
                    "mockup_referenced_not_declared",
                    f"screen '{screen_name}' is referenced in markdown but not declared in "
                    f"flow.yml.mockup_plan.screens. Add it (with name, purpose, source) or "
                    f"remove the image reference.",
                )

    # ---- rule 20: state:published + active risk_flags require resolved_decisions
    risk_flags_list = flow.get("risk_flags") or []
    resolved_decisions = flow.get("resolved_decisions") or []
    meta_state = (metadata.get("state") or "").lower()
    if meta_state == "published" and risk_flags_list and not resolved_decisions:
        rep.fail(
            "published_with_unresolved_risks",
            f"metadata.state='published' but flow.yml has {len(risk_flags_list)} active "
            f"risk_flag(s) and no resolved_decisions entries. Either set state='draft', "
            f"resolve the risks (remove from risk_flags), or document each accepted risk "
            f"in resolved_decisions with decided_by, decided_at, rationale.",
        )

    # ---- rule 21: code-audit cannot say ship-ready if it contains blocker fragments
    if intercom_id is not None and audit_dir.exists():
        code_audit_path = audit_dir / f"code-audit-{intercom_id}.md"
        if code_audit_path.exists():
            try:
                code_audit_body = code_audit_path.read_text(encoding="utf-8")
            except OSError:
                code_audit_body = ""
            ship_ready_markers = ["ship-ready", "ship ready", "shipready"]
            blockers = audit_markers.get("code_audit_ship_ready_blockers", [])
            says_ship_ready = any(m.lower() in code_audit_body.lower() for m in ship_ready_markers)
            blocker_hits = [b for b in blockers if b.lower() in code_audit_body.lower()]
            if says_ship_ready and blocker_hits:
                rep.fail(
                    "code_audit_inconsistent",
                    f"code-audit-{intercom_id}.md claims 'ship-ready' but contains uncertain "
                    f"language: {blocker_hits}. Either resolve the uncertainty (re-audit) or "
                    f"remove the ship-ready claim from the verdict.",
                )

    # ---- rule 22: content-audit must include an explicit stale-feature audit.
    # v1.1.1 tightening: bare "Scan 6" is no longer accepted because audits
    # mentioning "Scan 6, alt-text quality" passed the v1.1 check without
    # actually performing the stale-feature audit. The audit now requires an
    # explicit stale-feature marker. If "Scan 6" is mentioned but the explicit
    # marker is missing, a clearer failure surfaces the misleading section.
    if intercom_id is not None and audit_dir.exists():
        content_audit_path = audit_dir / f"content-audit-{intercom_id}.md"
        if content_audit_path.exists():
            try:
                content_audit_body = content_audit_path.read_text(encoding="utf-8")
            except OSError:
                content_audit_body = ""
            # Backward compat: workflow yaml may still ship the v1.1 key
            # `content_audit_scan6_required`. Prefer the new explicit key.
            stale_markers = (
                audit_markers.get("content_audit_stale_feature_markers")
                or audit_markers.get("content_audit_scan6_required")
                or []
            )
            has_stale_marker = any(
                m.lower() in content_audit_body.lower() for m in stale_markers
            )
            mentions_scan6 = "scan 6" in content_audit_body.lower()
            if not has_stale_marker:
                if mentions_scan6:
                    rep.fail(
                        "content_audit_scan6_not_stale",
                        f"content-audit-{intercom_id}.md mentions 'Scan 6' but does not contain "
                        f"an explicit stale-feature marker (one of: 'stale-feature', 'stale feature', "
                        f"'Stale-feature audit'). The 'Scan 6' label alone is not enough; rename "
                        f"or split the subsection so the stale-feature audit is unambiguous.",
                    )
                else:
                    rep.fail(
                        "content_audit_missing_stale_feature",
                        f"content-audit-{intercom_id}.md has no stale-feature audit. "
                        f"Add a 'Stale-feature audit' subsection (or include 'stale-feature' / "
                        f"'stale feature') that confirms every feature, button, and label "
                        f"described in the article still exists in production.",
                    )
            else:
                # ---- rule 22b: stale-feature subsection must use the structured table.
                # Once the audit declares a stale-feature subsection, the validator
                # checks the entries are auditable. The required columns are:
                # "Claim / feature", "Source checked", "Status", "Verdict".
                # Without the structure, "stale-feature: PASS" is unverifiable
                # narrative text.
                required_cols = ("Claim / feature", "Source checked", "Status", "Verdict")
                table_lines = [
                    ln for ln in content_audit_body.splitlines()
                    if ln.lstrip().startswith("|")
                ]
                has_required_header = any(
                    all(col.lower() in ln.lower() for col in required_cols)
                    for ln in table_lines
                )
                if not has_required_header:
                    rep.fail(
                        "content_audit_stale_table_missing",
                        f"content-audit-{intercom_id}.md has a stale-feature marker but no "
                        f"structured audit table. Add a markdown table with columns: "
                        f"| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |. "
                        f"Verdicts: live_in_ios | live_in_backend | product_confirmed | "
                        f"deprecated | unknown_blocker.",
                    )

    # ---- rule 23: compliance cannot say ALL PASS if active risk_flags remain
    if intercom_id is not None and audit_dir.exists():
        compliance_path = audit_dir / f"compliance-{intercom_id}.md"
        if compliance_path.exists():
            try:
                compliance_body = compliance_path.read_text(encoding="utf-8")
            except OSError:
                compliance_body = ""
            says_all_pass = "ALL PASS" in compliance_body
            if says_all_pass and risk_flags_list and not resolved_decisions:
                rep.fail(
                    "compliance_all_pass_with_risks",
                    f"compliance-{intercom_id}.md says 'ALL PASS' but flow.yml has "
                    f"{len(risk_flags_list)} active risk_flag(s) without resolved_decisions. "
                    f"Either resolve the risks or downgrade the verdict from 'ALL PASS' to "
                    f"'PASS pending risk resolution'.",
                )

    # ---- rule 24: backend_files declared require evidence in code-audit
    backend_files = (flow.get("source_of_truth") or {}).get("backend_files") or []
    if backend_files and intercom_id is not None and audit_dir.exists():
        code_audit_path = audit_dir / f"code-audit-{intercom_id}.md"
        if code_audit_path.exists():
            try:
                code_audit_body = code_audit_path.read_text(encoding="utf-8")
            except OSError:
                code_audit_body = ""
            # Evidence = any of the declared backend file paths or the substring "jamble_backend"
            backend_referenced = "jamble_backend" in code_audit_body or any(
                bf in code_audit_body for bf in backend_files if isinstance(bf, str)
            )
            if not backend_referenced:
                rep.fail(
                    "backend_files_not_audited",
                    f"flow.yml declares {len(backend_files)} backend_file(s) in source_of_truth "
                    f"but code-audit-{intercom_id}.md never mentions 'jamble_backend' or any "
                    f"of the declared paths. Either add the evidence (cite at least one backend "
                    f"file:line in the audit table) or remove from source_of_truth.",
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
