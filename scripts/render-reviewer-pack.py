#!/usr/bin/env python3
"""Static reviewer pack generator for the batch coordinator.

Reads the JSON dump produced by `run-help-article-batch.py --mode review`
and writes a single self-contained HTML page that lets the reviewer
audit 1 to 3 articles in 15 minutes.

The output is intentionally:
  - static HTML (no JS, no forms, no server, no React, no fetch)
  - readable side-by-side with a browser open
  - safe to share as a PR comment attachment
  - reproducible: same JSON in -> same HTML out

The page has two parts:

    1. A top scorecard (one row per article).
    2. One detail block per article with:
        - validate output verbatim
        - pt-BR + EN rendered preview (markdown to HTML, image URLs
          rewritten to point at the worktree's local PNGs so the page
          works offline)
        - inline mockup grid (every PNG declared in flow.yml)
        - the four reviewer questions (a, b, c, d) the reviewer must
          answer in their own notes / PR comment.

NO external Python deps beyond stdlib (and PyYAML used elsewhere in the
repo). NO Jinja. The HTML template is built with f-strings and small
helper functions.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

GITHUB_RAW_PREFIX = "https://raw.githubusercontent.com/Jamble-Live-Shopping/help-center/main/"


# --------------------------------------------------------------------------
# Tiny markdown -> HTML renderer (preview-grade, not Intercom-grade).
# --------------------------------------------------------------------------

def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _render_inline(line: str) -> str:
    """Inline markdown: bold, italic, inline code, links, images."""
    # Images first (before links).
    def repl_img(m: re.Match[str]) -> str:
        alt = _esc(m.group(1))
        url = m.group(2)
        return f'<img alt="{alt}" src="{_esc(url)}">'

    line = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl_img, line)
    # Links.
    line = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{_esc(m.group(2))}" target="_blank" rel="noopener">{_esc(m.group(1))}</a>',
        line,
    )
    # Bold then italic. Order matters so ** is not eaten by *.
    line = re.sub(r"\*\*([^*]+)\*\*", lambda m: f"<b>{_esc(m.group(1))}</b>", line)
    line = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", lambda m: f"<i>{_esc(m.group(1))}</i>", line)
    # Inline code.
    line = re.sub(r"`([^`]+)`", lambda m: f"<code>{_esc(m.group(1))}</code>", line)
    return line


def md_to_html(md: str, image_rewriter: Any = None) -> str:
    """Render a small Markdown subset (heading 1-3, paragraph, ul, ol,
    inline code/bold/italic/links/images) to HTML.

    `image_rewriter` is an optional callable str -> str applied to image
    URLs before HTML escaping (used to swap GitHub raw URLs for local
    file:// paths that work in the reviewer pack).
    """
    if image_rewriter is None:
        rewriter = lambda u: u
    else:
        rewriter = image_rewriter

    # Preprocess image URLs so the inline pass sees the rewritten string.
    def repl_img_pre(m: re.Match[str]) -> str:
        alt = m.group(1)
        url = rewriter(m.group(2))
        return f"![{alt}]({url})"

    md = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl_img_pre, md)

    out: list[str] = []
    lines = md.splitlines()
    i = 0
    in_ul = False
    in_ol = False
    para: list[str] = []

    def close_para() -> None:
        nonlocal para
        if para:
            text = " ".join(para)
            out.append(f"<p>{_render_inline(text)}</p>")
            para = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            close_para()
            close_lists()
            i += 1
            continue

        # Headings.
        m = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if m:
            close_para()
            close_lists()
            level = len(m.group(1))
            out.append(f"<h{level}>{_render_inline(m.group(2))}</h{level}>")
            i += 1
            continue

        # Unordered list.
        m = re.match(r"^[-*]\s+(.+)$", stripped)
        if m:
            close_para()
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{_render_inline(m.group(1))}</li>")
            i += 1
            continue

        # Ordered list.
        m = re.match(r"^\d+\.\s+(.+)$", stripped)
        if m:
            close_para()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{_render_inline(m.group(1))}</li>")
            i += 1
            continue

        # Default: paragraph buffer (preserves line wraps).
        para.append(stripped)
        i += 1

    close_para()
    close_lists()
    return "\n".join(out)


# --------------------------------------------------------------------------
# Scorecard + article block builders
# --------------------------------------------------------------------------

STATUS_BADGE = {
    "ready":   ('#0F8A3C', '#E8F5E9', 'READY'),
    "blocked": ('#B45309', '#FEF3C7', 'BLOCKED'),
    "failed":  ('#B42318', '#FEE4E2', 'FAILED'),
    "pending": ('#475467', '#F2F4F7', 'PENDING'),
}


def _badge_html(status: str) -> str:
    fg, bg, label = STATUS_BADGE.get(status, STATUS_BADGE["pending"])
    return f'<span class="badge" style="color:{fg};background:{bg};">{label}</span>'


def render_scorecard(reviews: list[dict]) -> str:
    rows: list[str] = []
    for r in reviews:
        png_ratio = (
            f"{r['mockups_present']}/{r['mockups_declared']}"
            if r["mockups_declared"] else "0/0"
        )
        png_class = "ok" if r["mockups_present"] == r["mockups_declared"] and r["mockups_declared"] > 0 else "warn"
        if r["mockups_declared"] == 0:
            png_class = "muted"
        if r["mockups_present"] < r["mockups_declared"]:
            png_class = "fail"

        hard = r["hard_fail_count"]
        hard_class = "ok" if hard == 0 else "fail"
        soft = r["soft_warn_count"]

        em_pt = r.get("em_dash_count_pt", -1)
        em_en = r.get("em_dash_count_en", -1)
        em_str = (
            f"{em_pt}/{em_en}"
            if em_pt >= 0 and em_en >= 0 else "-"
        )
        em_class = "ok" if em_pt == 0 and em_en == 0 else "fail" if em_pt > 0 or em_en > 0 else "muted"

        rdollar = r.get("rdollar_leak_en_count", -1)
        rd_class = "ok" if rdollar == 0 else "fail" if rdollar > 0 else "muted"
        rd_str = str(rdollar) if rdollar >= 0 else "-"

        audit_str = f"{r['audit_files_present']}/3"
        audit_class = "ok" if r["audit_files_present"] == 3 and not r["audit_skeleton_unfilled"] else "fail"

        blockers_html = ""
        if r.get("blockers"):
            blockers_html = (
                '<div class="blockers">'
                + "<br>".join(_esc(b) for b in r["blockers"])
                + "</div>"
            )

        rows.append(
            f'<tr>'
            f'<td><a href="#article-{_esc(r["slug"])}"><b>{_esc(r["slug"])}</b></a>'
            f'<div class="muted small">audience: {_esc(r["audience"])}</div></td>'
            f'<td>{_badge_html(r["status"])}{blockers_html}</td>'
            f'<td class="num {hard_class}">{hard if hard >= 0 else "-"}</td>'
            f'<td class="num">{soft if soft >= 0 else "-"}</td>'
            f'<td class="num {em_class}">{em_str}</td>'
            f'<td class="num {rd_class}">{rd_str}</td>'
            f'<td class="num {png_class}">{png_ratio}</td>'
            f'<td class="num {audit_class}">{audit_str}</td>'
            f'<td class="num">exit {r["validate_returncode"]}</td>'
            f'</tr>'
        )

    return (
        '<table class="scorecard">'
        '<thead><tr>'
        '<th>article</th><th>status</th>'
        '<th>hard</th><th>soft</th>'
        '<th>em-dash<br><span class="muted small">pt/en</span></th>'
        '<th>R$ leak<br><span class="muted small">en body</span></th>'
        '<th>mockups<br><span class="muted small">present/declared</span></th>'
        '<th>audit<br><span class="muted small">files/3</span></th>'
        '<th>validate</th>'
        '</tr></thead>'
        '<tbody>' + "".join(rows) + '</tbody>'
        '</table>'
    )


def _make_image_rewriter(worktree: str) -> Any:
    """Return a function that rewrites GitHub raw URLs to file:// URLs
    that point at the worktree's local PNGs, so the reviewer pack works
    when opened locally without a network round-trip.

    Uses Path.as_uri() so worktree paths containing spaces or unicode
    characters get URL-escaped correctly (a manual `f"file://{path}"`
    would break on "/Users/.../Jamble Coworker/..." for example).
    """
    abs_root = _resolve_worktree(worktree).resolve()

    def rewrite(url: str) -> str:
        if url.startswith(GITHUB_RAW_PREFIX):
            relative = url[len(GITHUB_RAW_PREFIX):]
            target = abs_root / relative
            return target.as_uri()
        return url

    return rewrite


def _resolve_worktree(worktree: str) -> Path:
    """Resolve a worktree field from summary.json.

    Real review packs carry absolute worktree paths. The committed sample
    uses a stable `{REPO_ROOT}/...` marker so it can live in git without
    leaking a developer path, while still being renderable by this script.
    """
    marker = "{REPO_ROOT}"
    if worktree == marker:
        return REPO_ROOT
    if worktree.startswith(marker + "/"):
        return REPO_ROOT / worktree[len(marker) + 1:]
    return Path(worktree)


def _read_md(worktree: str, rel: str | None) -> str:
    if not rel:
        return ""
    path = _resolve_worktree(worktree) / rel
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def render_article(r: dict) -> str:
    rewriter = _make_image_rewriter(r["worktree"])
    pt_md = _read_md(r["worktree"], r.get("pt_br_md_path"))
    en_md = _read_md(r["worktree"], r.get("en_md_path"))
    pt_html = md_to_html(pt_md, image_rewriter=rewriter) if pt_md else "<i class='muted'>(pt-br.md not found in worktree)</i>"
    en_html = md_to_html(en_md, image_rewriter=rewriter) if en_md else "<i class='muted'>(en.md not found in worktree)</i>"

    # Mockup grid (independent of inline images in the body).
    mockups_html = ""
    if r.get("mockup_pngs"):
        cards = []
        worktree_root = _resolve_worktree(r["worktree"]).resolve()
        for rel in r["mockup_pngs"]:
            abs_url = (worktree_root / rel).as_uri()
            label = Path(rel).name
            cards.append(
                f'<figure class="mock"><a href="{_esc(abs_url)}" target="_blank">'
                f'<img src="{_esc(abs_url)}" alt="{_esc(label)}"></a>'
                f'<figcaption>{_esc(label)}</figcaption></figure>'
            )
        mockups_html = '<div class="mockup-grid">' + "".join(cards) + "</div>"

    missing_html = ""
    if r.get("missing_mockups"):
        missing_html = (
            '<div class="alert"><b>Missing mockup PNGs:</b><ul>'
            + "".join(f"<li><code>{_esc(p)}</code></li>" for p in r["missing_mockups"])
            + "</ul></div>"
        )

    # Validate output kept verbatim in a <pre> so the reviewer can see
    # exactly what the gate produced.
    validate_pre = (
        f'<pre class="validate">{_esc(r["validate_output"] or "(no output)")}</pre>'
    )

    questions_html = (
        '<div class="questions">'
        '<h3>Reviewer questions</h3>'
        '<ol>'
        '<li><b>Tone, pt-BR.</b> Does the pt-br body sound like a Brazilian buyer or seller would write it? Any words that still sound translated rather than native?</li>'
        '<li><b>Mockups.</b> Do the rendered PNGs look professional and not placeholder-ish? Any cartoon emoji, big-text placeholder, missing icon?</li>'
        '<li><b>Factual claims.</b> Are all factual claims grounded in the cited iOS or backend file:line in the code-audit? Any claim that feels invented or unsupported?</li>'
        '<li><b>Publishable in Intercom today?</b> If yes, leave a GO comment on the PR. If no, list the blockers and stop the batch.</li>'
        '</ol>'
        '</div>'
    )

    blockers_html = ""
    if r.get("blockers"):
        blockers_html = (
            '<div class="alert"><b>Blockers:</b><ul>'
            + "".join(f"<li>{_esc(b)}</li>" for b in r["blockers"])
            + "</ul></div>"
        )

    branch_link = ""
    if r.get("branch"):
        branch_link = f'<span class="muted small"> · branch: <code>{_esc(r["branch"])}</code></span>'

    no_mockups_html = '<p class="muted">No mockup PNGs.</p>'

    return (
        f'<section id="article-{_esc(r["slug"])}" class="article">'
        f'<header><h2>{_esc(r["slug"])} {_badge_html(r["status"])}</h2>'
        f'<div class="muted">audience: {_esc(r["audience"])} · '
        f'intercom_id: {r.get("intercom_id") or "-"} · '
        f'worktree: <code>{_esc(r["worktree"])}</code>{branch_link}</div></header>'
        f'{blockers_html}'
        f'{missing_html}'
        f'<details open><summary>Validate output</summary>{validate_pre}</details>'
        f'<details><summary>pt-BR body (rendered preview)</summary>'
        f'<div class="md-preview">{pt_html}</div></details>'
        f'<details><summary>EN body (rendered preview)</summary>'
        f'<div class="md-preview">{en_html}</div></details>'
        f'<h3>Mockups</h3>'
        f'{mockups_html or no_mockups_html}'
        f'{questions_html}'
        f'</section>'
    )


CSS = """
:root {
  --fg: #162233;
  --muted: #6D6D80;
  --bg: #F9FAFC;
  --card: #FFFFFF;
  --border: #E9EAEF;
  --brand: #7E53F8;
  --ok: #0F8A3C;
  --fail: #B42318;
  --warn: #B45309;
}
* { box-sizing: border-box; }
body {
  font-family: -apple-system, "SF Pro Display", BlinkMacSystemFont, system-ui, sans-serif;
  background: var(--bg); color: var(--fg);
  margin: 0; padding: 24px;
  font-size: 14px; line-height: 1.5;
}
h1, h2, h3 { color: var(--fg); }
h1 { font-size: 24px; margin: 0 0 6px; }
h2 { font-size: 20px; margin: 18px 0 8px; }
h3 { font-size: 15px; margin: 14px 0 6px; }
.subtitle { color: var(--muted); margin-bottom: 20px; }
.muted { color: var(--muted); }
.small { font-size: 12px; }
table.scorecard {
  width: 100%; border-collapse: collapse;
  background: var(--card); border: 1px solid var(--border); border-radius: 12px; overflow: hidden;
  margin-bottom: 28px;
}
.scorecard th, .scorecard td { padding: 10px 12px; text-align: left; border-bottom: 1px solid var(--border); vertical-align: top; }
.scorecard th { background: #F4F4F8; font-size: 12px; text-transform: uppercase; letter-spacing: 0.4px; color: var(--muted); }
.scorecard td.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
.scorecard td.num.ok { color: var(--ok); }
.scorecard td.num.fail { color: var(--fail); font-weight: 600; }
.scorecard td.num.warn { color: var(--warn); }
.scorecard td.num.muted { color: var(--muted); }
.badge { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 700; letter-spacing: 0.3px; }
.blockers { font-size: 12px; color: var(--fail); margin-top: 4px; }
.article {
  background: var(--card); border: 1px solid var(--border); border-radius: 12px;
  padding: 20px; margin-bottom: 24px;
}
.article header h2 { display: flex; align-items: center; gap: 10px; margin-top: 0; }
.alert {
  background: #FEF3C7; border: 1px solid #FDE68A; color: #B45309;
  padding: 10px 14px; border-radius: 8px; margin: 10px 0;
}
.alert ul { margin: 6px 0 0 18px; }
details { margin: 12px 0; border: 1px solid var(--border); border-radius: 8px; padding: 0 12px; }
details > summary { padding: 10px 0; font-weight: 600; cursor: pointer; }
details[open] > summary { border-bottom: 1px solid var(--border); }
pre.validate {
  background: #1B1530; color: #E9E5FB;
  padding: 12px 14px; border-radius: 8px;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 12px; overflow-x: auto; white-space: pre-wrap;
  margin: 12px 0;
}
.md-preview { padding: 4px 0 12px; max-width: 720px; }
.md-preview h1 { font-size: 22px; margin-top: 16px; }
.md-preview h2 { font-size: 17px; margin-top: 18px; padding-top: 8px; border-top: 1px solid var(--border); }
.md-preview h3 { font-size: 14px; }
.md-preview p { margin: 6px 0; }
.md-preview img { max-width: 100%; border-radius: 6px; border: 1px solid var(--border); margin: 8px 0; }
.md-preview ul, .md-preview ol { padding-left: 22px; }
.mockup-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 8px 0 16px; }
.mock { margin: 0; }
.mock img { width: 100%; border-radius: 8px; border: 1px solid var(--border); background: #FFF; }
.mock figcaption { font-size: 11px; color: var(--muted); padding: 4px 2px; word-break: break-all; }
.questions { background: #F4EFFF; border: 1px solid #DCC9FF; border-radius: 10px; padding: 14px 18px; margin-top: 16px; }
.questions h3 { margin-top: 0; color: var(--brand); }
.questions ol { margin: 6px 0 0 22px; }
.questions li { margin: 6px 0; }
"""


def render_pack(payload: dict) -> str:
    reviews = payload.get("articles", [])
    batch_id = payload.get("batch_id", "(unknown)")

    summary_line = (
        f"{len(reviews)} article(s) reviewed. "
        f"{sum(1 for r in reviews if r['status'] == 'ready')} ready, "
        f"{sum(1 for r in reviews if r['status'] == 'blocked')} blocked, "
        f"{sum(1 for r in reviews if r['status'] == 'failed')} failed."
    )
    body = (
        '<header>'
        f'<h1>Reviewer pack — batch <code>{_esc(batch_id)}</code></h1>'
        f'<div class="subtitle">{_esc(summary_line)}</div>'
        '</header>'
        + render_scorecard(reviews)
        + "".join(render_article(r) for r in reviews)
        + (
            '<footer class="muted small" style="margin-top:32px;">'
            'Generated by <code>scripts/render-reviewer-pack.py</code>. '
            'Static HTML, no scripts. Open in any browser; image links work locally.'
            '</footer>'
        )
    )

    return (
        '<!DOCTYPE html>'
        '<html lang="en">'
        '<head>'
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>Reviewer pack — {_esc(batch_id)}</title>'
        f'<style>{CSS}</style>'
        '</head>'
        f'<body>{body}</body>'
        '</html>'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the static reviewer pack from a batch review JSON")
    parser.add_argument("--input", type=Path, required=True, help="path to summary.json (from --mode review)")
    parser.add_argument("--output", type=Path, required=True, help="path to write summary.html")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        return 2

    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: cannot parse {args.input}: {exc}", file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_pack(payload), encoding="utf-8")
    print(f"OK wrote {args.output} ({args.output.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
