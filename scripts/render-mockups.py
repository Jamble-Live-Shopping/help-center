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

ICON_SVGS = {
    # Feather-style inline icons, keyed by common names Haiku returns
    "play": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="6 3 20 12 6 21 6 3" fill="#FFFFFF"/></svg>',
    "wallet": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h15a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h12"/><circle cx="17" cy="14" r="1.5" fill="#FFFFFF"/></svg>',
    "box": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="12" width="3" height="8"/><rect x="10.5" y="6" width="3" height="14"/><rect x="17" y="9" width="3" height="11"/></svg>',
    "bell": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
    "user": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "settings": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    "cart": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>',
    "shop": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l1-6h16l1 6"/><path d="M3 9v11a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V9"/><path d="M8 9a4 4 0 1 1 8 0"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
    "edit": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>',
    "credit-card": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>',
    "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "plus": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "dot": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3" fill="#FFFFFF"/></svg>',
}

# Fuzzy name mapping: many words → one icon
ICON_ALIASES = {
    "live": "play", "arrow": "play", "▶": "play",
    "money": "wallet", "bank": "wallet", "payout": "wallet", "carteira": "wallet",
    "package": "box", "product": "box", "listing": "box", "item": "box", "pacote": "box",
    "analytics": "chart", "stats": "chart", "sales": "chart", "bar": "chart", "bar-chart": "chart", "graph": "chart",
    "notification": "bell", "alert": "bell", "notificações": "bell",
    "profile": "user", "person": "user", "account": "user", "perfil": "user", "person.badge.plus": "user", "👤": "user",
    "config": "settings", "preferences": "settings", "preferência": "settings",
    "favorite": "heart", "wishlist": "heart", "favorito": "heart",
    "order": "cart", "buy": "cart", "pedido": "cart",
    "store": "shop", "shop": "shop", "storefront": "shop",
    "security": "shield", "privacy": "shield", "block": "shield", "segurança": "shield",
    "message": "mail", "email": "mail", "dm": "mail",
    "shipping": "truck", "envio": "truck", "correios": "truck", "delivery": "truck",
    "payment": "credit-card", "card": "credit-card", "pagar.me": "credit-card", "pagamento": "credit-card",
    "sale": "tag", "discount": "tag", "offer": "tag",
    "history": "clock", "time": "clock", "schedule": "clock",
    "add": "plus", "create": "plus", "new": "plus", "➕": "plus",
    "verified": "check", "complete": "check", "done": "check", "ellipsis": "dot",
    "exclamation": "bell",
    "chevron-right": "", "chevron": "", ">": "",
}


def resolve_icon(name: str) -> str:
    """Return inline SVG for an icon name, or empty string for generic blank."""
    if not name:
        return ""
    key = name.lower().strip()
    if key in ICON_SVGS:
        return ICON_SVGS[key]
    if key in ICON_ALIASES:
        target = ICON_ALIASES[key]
        return ICON_SVGS.get(target, "") if target else ""
    # Fuzzy contains match
    for alias, target in ICON_ALIASES.items():
        if alias in key:
            return ICON_SVGS.get(target, "") if target else ""
    for known in ICON_SVGS:
        if known in key:
            return ICON_SVGS[known]
    # Unknown icon name: return a generic dot
    return ICON_SVGS["dot"]


def render_settings_row_list(c):
    rows_html = ""
    for r in c.get("rows", []):
        dim = " dimmed" if r.get("dimmed") else ""
        icon_bg = "gray" if r.get("icon_bg") == "gray" else "brand"
        icon_svg = resolve_icon(r.get("icon", ""))
        rows_html += f'<div class="row{dim}"><div class="row-icon {icon_bg}">{icon_svg}</div><div class="row-label">{esc(r.get("label", ""))}</div></div>'
    header = f'<div class="section-header">{esc(c.get("section_title", ""))}</div>' if c.get("section_title") else ""
    css = """
.section-header { font-size: 13px; font-weight: 400; color: #6D6D80; text-transform: uppercase; padding: 14px 20px 6px; letter-spacing: -0.08px; }
.group { background: #FFFFFF; margin: 0 12px 10px; border-radius: 12px; overflow: hidden; border: 1px solid #E9EAEF; }
.row { display: flex; align-items: center; padding: 12px 16px; min-height: 44px; }
.row-icon { width: 30px; height: 30px; border-radius: 7px; display: flex; align-items: center; justify-content: center; color: white; font-size: 14px; margin-right: 12px; flex-shrink: 0; padding: 6px; }
.row-icon svg { width: 100%; height: 100%; }
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


def render_tab_bar(c):
    tabs = c.get("tabs", [])
    active = c.get("active_tab_index", 0)
    tabs_html = ""
    for i, t in enumerate(tabs):
        cls = "tab active" if i == active else "tab"
        tabs_html += f'<div class="{cls}">{esc(t)}</div>'
    placeholder = c.get("content_placeholder", "")
    css = """
.phone { padding: 20px 0 28px; }
.tab-row { display: flex; gap: 10px; padding: 8px 16px 18px; }
.tab { flex: 1; padding: 10px 12px; text-align: center; border-radius: 20px; background: #F3F4F8; color: #6B7A92; font-size: 14px; font-weight: 600; }
.tab.active { background: #162233; color: #FFFFFF; }
.tab-content { margin: 0 16px; padding: 40px 16px; text-align: center; background: #F9FAFC; border: 1px dashed #DADDE3; border-radius: 12px; color: #A0A7B7; font-size: 13px; line-height: 18px; }
"""
    placeholder_html = f'<div class="tab-content">{esc(placeholder or "Content appears here")}</div>' if placeholder or True else ""
    return wrap(f'<div class="tab-row">{tabs_html}</div>{placeholder_html}', css)


def render_product_card(c):
    price = ""
    if c.get("price"):
        price = f'<div class="prod-price">{esc(c["price"])}</div>'
    stock = ""
    if c.get("stock"):
        stock = f'<div class="prod-stock">{esc(c["stock"])}</div>'
    subtitle = ""
    if c.get("subtitle"):
        subtitle = f'<div class="prod-sub">{esc(c["subtitle"])}</div>'
    cta = ""
    if c.get("cta_label"):
        cta = f'<div class="prod-cta">{esc(c["cta_label"])}</div>'
    icon = resolve_icon(c.get("icon", "box")) or ICON_SVGS["box"]
    css = """
.phone { padding: 20px 0; }
.prod-card { margin: 0 12px; border: 1px solid #E9EAEF; border-radius: 12px; overflow: hidden; }
.prod-row { display: flex; align-items: center; padding: 16px; gap: 14px; }
.prod-thumb { width: 64px; height: 64px; border-radius: 10px; background: #7E53F8; display: flex; align-items: center; justify-content: center; padding: 14px; flex-shrink: 0; }
.prod-thumb svg { width: 100%; height: 100%; }
.prod-info { flex: 1; min-width: 0; }
.prod-title { font-size: 16px; font-weight: 600; color: #162233; line-height: 21px; }
.prod-sub { font-size: 13px; color: #6B7A92; margin-top: 2px; }
.prod-price { font-family: -apple-system-round, "SF Pro Rounded", system-ui, sans-serif; font-size: 18px; font-weight: 600; color: #162233; margin-top: 6px; }
.prod-stock { font-size: 12px; color: #A0A7B7; margin-top: 2px; }
.prod-cta { margin: 0 16px 16px; background: #7E53F8; color: white; height: 40px; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600; }
"""
    body = f'<div class="prod-card"><div class="prod-row"><div class="prod-thumb">{icon}</div><div class="prod-info"><div class="prod-title">{esc(c.get("title",""))}</div>{subtitle}{price}{stock}</div></div>{cta}</div>'
    return wrap(body, css)


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
    "tab-bar": render_tab_bar,
    "product-card": render_product_card,
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
