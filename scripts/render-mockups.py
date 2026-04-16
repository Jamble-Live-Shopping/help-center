#!/usr/bin/env python3
"""
Render HTML mockups from _work/ascii-extracted.json using the 10 templates.

Writes articles/<slug>/mockup-sources/<screen>.html per extraction.
Then calls Puppeteer (scripts/shot-batch.mjs) to produce PNGs.
Finally copies PNGs to assets/mockups/<slug>__<screen>.png.

Usage:
    python3 scripts/render-mockups.py                # render all from JSON
    python3 scripts/render-mockups.py --dry-run      # print what would be rendered
    python3 scripts/render-mockups.py --html-only    # skip Puppeteer
"""

import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXTRACTIONS = REPO / "_work" / "ascii-extracted.json"
ARTICLES = REPO / "articles"
MOCKUPS = REPO / "assets" / "mockups"
TEMPLATES = REPO / "process" / "templates"

BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, "SF Pro Display", BlinkMacSystemFont, system-ui, sans-serif; background: #F9FAFC; display: flex; justify-content: center; padding: 12px; }
.phone { width: 320px; background: #FFFFFF; border-radius: 24px; box-shadow: 0 2px 20px rgba(126,83,248,0.08); border: 1px solid #E9EAEF; overflow: hidden; }
"""


def esc(s):
    return html.escape(str(s or ""))


def wrap(body_html, extra_css=""):
    return f"""<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>{BASE_CSS}{extra_css}</style></head><body><div class="phone">{body_html}</div></body></html>"""


# --- Renderers per template ---

def render_settings_row_list(c):
    rows_html = ""
    for r in c.get("rows", []):
        dim = " dimmed" if r.get("dimmed") else ""
        icon_bg = "gray" if r.get("icon_bg") == "gray" else "brand"
        rows_html += f'<div class="row{dim}"><div class="row-icon {icon_bg}">{esc(r.get("icon", ""))}</div><div class="row-label">{esc(r.get("label", ""))}</div></div>'
    header = f'<div class="section-header">{esc(c.get("section_title", ""))}</div>' if c.get("section_title") else ""
    css = """
.section-header { font-size: 13px; font-weight: 400; color: #6D6D80; text-transform: uppercase; padding: 14px 20px 6px; letter-spacing: -0.08px; }
.group { background: #FFFFFF; margin: 0 12px 10px; border-radius: 12px; overflow: hidden; border: 1px solid #E9EAEF; }
.row { display: flex; align-items: center; padding: 12px 16px; min-height: 44px; }
.row-icon { width: 30px; height: 30px; border-radius: 7px; display: flex; align-items: center; justify-content: center; color: white; font-size: 14px; margin-right: 12px; flex-shrink: 0; }
.row-icon.brand { background: #7E53F8; }
.row-icon.gray { background: #8E8E93; }
.row-label { font-size: 17px; color: #162233; flex: 1; line-height: 22px; }
.row.dimmed .row-label { color: #C7C7CC; }
"""
    return wrap(header + f'<div class="group">{rows_html}</div><div style="height:16px"></div>', css)


def render_alert_dialog(c):
    secondary = ""
    if c.get("secondary_label"):
        secondary = f'<div class="alert-btn secondary">{esc(c["secondary_label"])}</div>'
    css = """
body { background: rgba(0,0,0,0.35); }
.phone { background: transparent; border: none; box-shadow: none; width: 270px; }
.alert { background: rgba(255,255,255,0.96); border-radius: 14px; backdrop-filter: blur(20px); }
.alert-body { padding: 19px 16px 17px; text-align: center; }
.alert-title { font-size: 17px; font-weight: 600; color: #000; margin-bottom: 4px; }
.alert-msg { font-size: 13px; color: #000; line-height: 18px; }
.alert-btns { border-top: 0.5px solid #C6C6C8; display: flex; }
.alert-btn { flex: 1; padding: 11px; text-align: center; font-size: 17px; }
.alert-btn.primary { color: #7E53F8; font-weight: 600; border-right: 0.5px solid #C6C6C8; }
.alert-btn.secondary { color: #007AFF; }
"""
    body = f'''<div class="alert"><div class="alert-body"><div class="alert-title">{esc(c.get("title",""))}</div><div class="alert-msg">{esc(c.get("message",""))}</div></div><div class="alert-btns">{secondary}<div class="alert-btn primary">{esc(c.get("primary_label","OK"))}</div></div></div>'''
    return wrap(body, css).replace('<div class="phone">', '<div class="phone"><div class="alert-wrap">').replace('</div></body>', '</div></div></body>')


def render_empty_state_cta(c):
    css = """
.phone { padding: 40px 24px 24px; text-align: center; }
.empty-title { font-size: 22px; font-weight: 600; color: #162233; margin-bottom: 8px; line-height: 28px; }
.empty-sub { font-size: 15px; color: #6B7A92; line-height: 21px; margin-bottom: 24px; }
.empty-cta { background: #7E53F8; color: white; height: 48px; border-radius: 24px; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 600; }
"""
    sub = f'<div class="empty-sub">{esc(c.get("subtitle",""))}</div>' if c.get("subtitle") else ""
    body = f'<div class="empty-title">{esc(c.get("title",""))}</div>{sub}<div class="empty-cta">{esc(c.get("cta_label","Continue"))}</div>'
    return wrap(body, css)


def render_radio_picker(c):
    options_html = ""
    for opt in c.get("options", []):
        selected = "selected" if opt.get("selected") else ""
        icon = f'<div class="opt-icon"></div>'
        subtitle = f'<div class="opt-sub">{esc(opt.get("subtitle",""))}</div>' if opt.get("subtitle") else ""
        options_html += f'''<div class="opt {selected}">{icon}<div class="opt-text"><div class="opt-name">{esc(opt.get("name",""))}</div>{subtitle}</div><div class="radio {selected}"></div></div>'''
    title = f'<div class="picker-title">{esc(c.get("title",""))}</div>' if c.get("title") else ""
    css = """
.picker-title { font-size: 15px; font-weight: 600; color: #A0A7B7; text-transform: uppercase; padding: 14px 20px 8px; letter-spacing: 0.5px; }
.group { margin: 0 12px 14px; border: 1px solid #E9EAEF; border-radius: 12px; overflow: hidden; }
.opt { display: flex; align-items: center; padding: 14px 16px; border-bottom: 1px solid #F0F1F5; }
.opt:last-child { border-bottom: none; }
.opt.selected { background: #F9F8FF; }
.opt-icon { width: 24px; height: 24px; background: #E9EAEF; border-radius: 6px; margin-right: 12px; flex-shrink: 0; }
.opt-text { flex: 1; }
.opt-name { font-size: 17px; font-weight: 600; color: #162233; line-height: 22px; }
.opt-sub { font-size: 13px; color: #A0A7B7; line-height: 18px; margin-top: 2px; }
.radio { width: 18px; height: 18px; border-radius: 50%; border: 1.5px solid #A0A7B7; flex-shrink: 0; margin-left: 12px; }
.radio.selected { border-color: #162233; position: relative; }
.radio.selected::after { content: ""; position: absolute; top: 3px; left: 3px; width: 10px; height: 10px; border-radius: 50%; background: #162233; }
"""
    return wrap(title + f'<div class="group">{options_html}</div>', css)


def render_photo_grid(c):
    n = c.get("photos", 0)
    max_n = c.get("max_photos", 10)
    slots = ""
    for i in range(max_n):
        if i < n:
            slots += f'<div class="slot filled"><div class="badge">{i+1}</div></div>'
        else:
            slots += '<div class="slot add"><div class="plus">+</div></div>'
    title = f'<div class="grid-title">{esc(c.get("title","Photos"))}</div>'
    css = """
.grid-title { font-size: 15px; font-weight: 600; color: #A0A7B7; text-transform: uppercase; padding: 14px 20px 8px; letter-spacing: 0.5px; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; padding: 0 16px 20px; }
.slot { aspect-ratio: 1; border-radius: 8px; position: relative; }
.slot.filled { background: #DADDE3; }
.slot.add { background: transparent; border: 1.5px dashed #C7C7CC; display: flex; align-items: center; justify-content: center; }
.slot .plus { font-size: 22px; color: #C7C7CC; font-weight: 300; }
.badge { position: absolute; top: 3px; left: 3px; width: 16px; height: 16px; border-radius: 50%; background: #7E53F8; color: white; font-size: 9px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
"""
    return wrap(title + f'<div class="grid">{slots}</div>', css)


def render_button_cta(c):
    css = """
.phone { padding: 40px 24px; }
.cta { background: #7E53F8; color: white; height: 56px; border-radius: 28px; display: flex; align-items: center; justify-content: center; font-size: 17px; font-weight: 600; }
"""
    return wrap(f'<div class="cta">{esc(c.get("label","Continue"))}</div>', css)


def render_stepper_input(c):
    css = """
.phone { padding: 20px 0; }
.group { background: #FFFFFF; margin: 0 12px; border-radius: 12px; overflow: hidden; border: 1px solid #E9EAEF; padding: 16px 16px 14px; }
.title { font-family: -apple-system-round, "SF Pro Rounded", system-ui, sans-serif; font-size: 17px; font-weight: 600; color: #162233; line-height: 22px; margin-bottom: 10px; }
.stepper { display: flex; align-items: center; justify-content: center; gap: 12px; }
.step-btn { width: 32px; height: 32px; border-radius: 50%; background: #E9EAEF; color: #162233; display: flex; align-items: center; justify-content: center; font-size: 15px; font-weight: 500; }
.step-value { min-width: 32px; text-align: center; font-family: -apple-system-round, "SF Pro Rounded", system-ui, sans-serif; font-size: 17px; font-weight: 600; color: #162233; }
"""
    body = f'<div class="group"><div class="title">{esc(c.get("title","Quantity"))}</div><div class="stepper"><div class="step-btn">&minus;</div><div class="step-value">{esc(c.get("value",1))}</div><div class="step-btn">+</div></div></div>'
    return wrap(body, css)


def render_error_toast(c):
    css = """
body { padding: 16px 12px; }
.phone { background: #F9FAFC; padding: 12px 0; border: none; box-shadow: none; }
.toast { background: #FFFFFF; border-radius: 12px; margin: 0 12px; padding: 12px 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.18), 0 0 1px rgba(0,0,0,0.1); display: flex; align-items: center; gap: 8px; }
.toast-icon { width: 32px; height: 32px; flex-shrink: 0; }
.toast-text { display: flex; flex-direction: column; align-items: flex-start; flex: 1; min-width: 0; }
.toast-title { font-size: 16px; font-weight: 600; color: #162233; line-height: 22px; letter-spacing: -0.01em; }
.toast-subtitle { font-size: 14px; font-weight: 400; color: #162233; line-height: 20px; margin-top: 2px; }
"""
    svg_icon = '<svg class="toast-icon" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><circle cx="16" cy="16" r="14" fill="#D92C20"/><rect x="14.5" y="7.5" width="3" height="11" rx="1.5" fill="#FFFFFF"/><circle cx="16" cy="22.5" r="1.75" fill="#FFFFFF"/></svg>'
    body = f'<div class="toast">{svg_icon}<div class="toast-text"><div class="toast-title">{esc(c.get("title",""))}</div><div class="toast-subtitle">{esc(c.get("subtitle",""))}</div></div></div>'
    return wrap(body, css)


def render_wallet_nav(c):
    right = ""
    for icon in c.get("right_icons") or []:
        if icon == "help":
            right += '<div class="nav-icon">?</div>'
        elif icon == "clock":
            right += '<div class="nav-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#162233" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"></circle><polyline points="12 7 12 12 15 14"></polyline></svg></div>'
        elif icon == "bell":
            right += '<div class="nav-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#162233" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg></div>'
    pending = ""
    if c.get("pending"):
        p = c["pending"]
        pending = f'<div class="pending"><div class="pending-label">{esc(p.get("label","Pending"))}</div><div class="pending-amount">{esc(p.get("amount",""))}</div></div>'
    css = """
.nav { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px 10px; border-bottom: 1px solid #F0F1F5; }
.nav-back { width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; color: #162233; font-size: 20px; }
.nav-title { font-size: 17px; font-weight: 600; color: #162233; }
.nav-right { display: flex; gap: 4px; }
.nav-icon { width: 36px; height: 36px; border-radius: 50%; background: #F3F4F8; color: #162233; display: flex; align-items: center; justify-content: center; font-size: 15px; }
.card { margin: 16px 12px 12px; padding: 18px 16px 16px; border: 1px solid #E9EAEF; border-radius: 12px; }
.card-label { font-size: 15px; font-weight: 600; color: #162233; }
.card-amount { font-family: -apple-system-round, "SF Pro Rounded", system-ui, sans-serif; font-size: 32px; font-weight: 500; color: #162233; letter-spacing: -0.02em; margin: 10px 0 14px; }
.withdraw { height: 40px; border-radius: 20px; background: #7E53F8; color: #FFFFFF; font-size: 15px; font-weight: 600; display: flex; align-items: center; justify-content: center; }
.pending { margin: 0 12px 14px; padding: 14px 16px; border: 1px solid #E9EAEF; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; }
.pending-label { font-size: 14px; color: #6B7A92; }
.pending-amount { font-size: 16px; font-weight: 600; color: #162233; }
"""
    body = f'<div class="nav"><div class="nav-back">&lsaquo;</div><div class="nav-title">{esc(c.get("nav_title","My Wallet"))}</div><div class="nav-right">{right}</div></div><div class="card"><div class="card-label">{esc(c.get("balance_label","Available to Withdraw"))}</div><div class="card-amount">{esc(c.get("balance_amount","R$ 0,00"))}</div><div class="withdraw">{esc(c.get("cta_label","Withdraw"))}</div></div>{pending}<div style="height:8px"></div>'
    return wrap(body, css)


def render_list_with_status(c):
    rows = ""
    for r in c.get("rows", []):
        color_map = {"green": "#17B169", "red": "#D92C20", "yellow": "#FCB022"}
        color = color_map.get(r.get("status_color"), "#6B7A92")
        rows += f'<div class="row"><div class="row-top"><div class="row-id">{esc(r.get("id",""))}</div><div class="row-amount">{esc(r.get("amount",""))}</div></div><div class="row-bottom"><div class="status" style="color:{color}">{esc(r.get("status",""))}</div><div class="row-date">{esc(r.get("date",""))}</div></div></div>'
    css = """
.phone { padding-bottom: 8px; }
.section-header { padding: 16px 20px 8px; font-size: 17px; font-weight: 600; color: #162233; }
.list { margin: 0 12px; border: 1px solid #E9EAEF; border-radius: 12px; overflow: hidden; }
.row { padding: 12px 16px; display: flex; flex-direction: column; gap: 4px; border-bottom: 1px solid #F0F1F5; }
.row:last-child { border-bottom: none; }
.row-top, .row-bottom { display: flex; justify-content: space-between; align-items: center; }
.row-id { font-size: 15px; font-weight: 600; color: #162233; }
.row-amount { font-family: -apple-system-round, "SF Pro Rounded", system-ui, sans-serif; font-size: 15px; font-weight: 600; color: #162233; }
.status { font-size: 13px; font-weight: 600; }
.row-date { font-size: 13px; color: #6B7A92; }
"""
    body = f'<div class="section-header">{esc(c.get("section_title","History"))}</div><div class="list">{rows}</div>'
    return wrap(body, css)


def render_form_layout(c):
    fields = ""
    for f in c.get("fields", []):
        label = esc(f.get("label", ""))
        t = f.get("type", "text")
        placeholder = esc(f.get("placeholder", ""))
        if t == "dropdown":
            fields += f'<div class="field"><div class="fl">{label}</div><div class="fd">{placeholder or "Select"} &#9662;</div></div>'
        elif t == "upload":
            fields += f'<div class="field"><div class="fl">{label}</div><div class="fu"><span>+</span><span>{placeholder or "Add"}</span></div></div>'
        elif t == "textarea":
            fields += f'<div class="field"><div class="fl">{label}</div><div class="ft">{placeholder}</div></div>'
        else:
            fields += f'<div class="field"><div class="fl">{label}</div><div class="fi">{placeholder or "Enter " + label.lower()}</div></div>'
    css = """
.form-title { font-size: 20px; font-weight: 700; color: #162233; padding: 20px 20px 12px; }
.form-body { padding: 0 20px 20px; }
.field { margin-bottom: 14px; }
.fl { font-size: 13px; font-weight: 600; color: #6B7A92; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.4px; }
.fi { font-size: 15px; color: #A0A7B7; background: #F9FAFC; border: 1px solid #E9EAEF; border-radius: 8px; padding: 10px 12px; }
.fd { font-size: 15px; color: #162233; background: #F9FAFC; border: 1px solid #E9EAEF; border-radius: 8px; padding: 10px 12px; display: flex; justify-content: space-between; align-items: center; }
.fu { font-size: 14px; color: #6B7A92; border: 1.5px dashed #C7C7CC; border-radius: 8px; padding: 22px 12px; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.fu span:first-child { font-size: 24px; font-weight: 300; color: #C7C7CC; }
.ft { font-size: 15px; color: #A0A7B7; background: #F9FAFC; border: 1px solid #E9EAEF; border-radius: 8px; padding: 10px 12px; min-height: 60px; }
.form-submit { background: #7E53F8; color: white; height: 48px; border-radius: 24px; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 600; margin: 4px 20px 20px; }
"""
    body = f'<div class="form-title">{esc(c.get("title", ""))}</div><div class="form-body">{fields}</div><div class="form-submit">{esc(c.get("submit_label", "Continue"))}</div>'
    return wrap(body, css)


def render_auth_screen(c):
    btns = ""
    for b in c.get("buttons", []):
        style = b.get("style", "primary")
        btns += f'<div class="auth-btn {style}">{esc(b.get("label", ""))}</div>'
    link = ""
    if c.get("secondary_link"):
        link = f'<div class="auth-link">{esc(c["secondary_link"].get("label", ""))}</div>'
    css = """
.phone { padding: 40px 24px 28px; text-align: center; }
.auth-title { font-family: -apple-system-round, "SF Pro Rounded", system-ui, sans-serif; font-size: 24px; font-weight: 600; color: #162233; margin-bottom: 28px; line-height: 30px; }
.auth-btn { height: 48px; border-radius: 24px; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 600; margin-bottom: 10px; }
.auth-btn.primary { background: #7E53F8; color: white; }
.auth-btn.secondary { background: #F3F4F8; color: #162233; }
.auth-link { font-size: 14px; color: #7E53F8; font-weight: 600; margin-top: 18px; }
"""
    return wrap(f'<div class="auth-title">{esc(c.get("title", ""))}</div>{btns}{link}', css)


def render_text_with_actions(c):
    btns = ""
    for b in c.get("buttons", []):
        style = b.get("style", "primary")
        btns += f'<div class="twa-btn {style}">{esc(b.get("label", ""))}</div>'
    css = """
.phone { padding: 28px 24px 24px; }
.twa-title { font-size: 20px; font-weight: 700; color: #162233; margin-bottom: 12px; line-height: 26px; }
.twa-body { font-size: 15px; color: #162233; line-height: 22px; margin-bottom: 22px; }
.twa-btn { height: 44px; border-radius: 22px; display: flex; align-items: center; justify-content: center; font-size: 15px; font-weight: 600; margin-bottom: 10px; }
.twa-btn.primary { background: #7E53F8; color: white; }
.twa-btn.secondary { background: #F3F4F8; color: #162233; }
"""
    return wrap(f'<div class="twa-title">{esc(c.get("title", ""))}</div><div class="twa-body">{esc(c.get("body", ""))}</div>{btns}', css)


RENDERERS = {
    "settings-row-list": render_settings_row_list,
    "alert-dialog": render_alert_dialog,
    "empty-state-cta": render_empty_state_cta,
    "radio-picker": render_radio_picker,
    "photo-grid": render_photo_grid,
    "button-cta": render_button_cta,
    "stepper-input": render_stepper_input,
    "error-toast": render_error_toast,
    "wallet-nav": render_wallet_nav,
    "list-with-status": render_list_with_status,
    "form-layout": render_form_layout,
    "auth-screen": render_auth_screen,
    "text-with-actions": render_text_with_actions,
}


def main():
    extractions = json.loads(EXTRACTIONS.read_text())
    dry = "--dry-run" in sys.argv
    html_only = "--html-only" in sys.argv

    # One PNG per (slug, screen_name, locale) — content differs per locale
    per_screen = {}
    for e in extractions:
        ext = e["extraction"]
        if ext["template_id"] == "unmatched":
            continue
        key = f'{e["slug"]}/{ext["screen_name"]}/{e["locale"]}'
        per_screen[key] = e

    print(f"Will render {len(per_screen)} mockups (one per locale) from {len(extractions)} extractions")
    if dry:
        for key in sorted(per_screen):
            e = per_screen[key]
            print(f"  {key:<60} template={e['extraction']['template_id']}")
        return

    rendered = 0
    for key, e in sorted(per_screen.items()):
        ext = e["extraction"]
        tid = ext["template_id"]
        if tid not in RENDERERS:
            continue
        renderer = RENDERERS[tid]
        html_str = renderer(ext["content"])
        article_dir = ARTICLES / e["slug"]
        out_dir = article_dir / "mockup-sources"
        out_dir.mkdir(exist_ok=True)
        # Include locale in HTML filename so both EN and pt-br sources coexist
        html_path = out_dir / f"{ext['screen_name']}__{e['locale']}.html"
        html_path.write_text(html_str)
        rendered += 1

    print(f"Rendered {rendered} HTML files")

    if html_only:
        return

    # Batch screenshot via Puppeteer
    # Build a single manifest file the script will read
    manifest = []
    for key, e in sorted(per_screen.items()):
        ext = e["extraction"]
        if ext["template_id"] == "unmatched":
            continue
        slug = e["slug"]
        screen = ext["screen_name"]
        locale = e["locale"]
        html_path = ARTICLES / slug / "mockup-sources" / f"{screen}__{locale}.html"
        png_path = MOCKUPS / f"{slug}__{screen}__{locale}.png"
        if html_path.exists():
            manifest.append({"html": str(html_path), "png": str(png_path)})

    manifest_path = REPO / "_work" / "shot-manifest.json"
    manifest_path.write_text(json.dumps(manifest))
    print(f"Manifest: {len(manifest)} entries")

    # Run puppeteer batch
    subprocess.run(["node", "scripts/shot-batch.mjs", str(manifest_path)], check=True)


if __name__ == "__main__":
    main()
