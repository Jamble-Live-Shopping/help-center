#!/usr/bin/env python3
"""
Extract every ASCII block from every articles/<slug>/{en,pt-br}.md, classify it
into one of the 10 templates, and extract structured content via Haiku 4.5.

Output: _work/ascii-extracted.json with one entry per block.

Usage:
    python3 scripts/extract-ascii.py              # run on all articles
    python3 scripts/extract-ascii.py <slug>       # run on a single article (debug)
    python3 scripts/extract-ascii.py --limit 5    # run on first N articles (pilot)

Requires:
    - ANTHROPIC_API_KEY in env
    - pip install instructor anthropic pydantic
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Literal, Optional

import instructor
from anthropic import Anthropic
from pydantic import BaseModel, Field

REPO = Path(__file__).resolve().parent.parent
ARTICLES = REPO / "articles"
OUT = REPO / "_work" / "ascii-extracted.json"
OUT.parent.mkdir(exist_ok=True)
BOX_CHARS = set("┌┐└┘│─├┤┬┴┼╔╗╚╝║═╠╣╦╩╬")

TemplateId = Literal[
    "settings-row-list",
    "alert-dialog",
    "empty-state-cta",
    "radio-picker",
    "photo-grid",
    "button-cta",
    "stepper-input",
    "error-toast",
    "wallet-nav",
    "list-with-status",
    "form-layout",
    "auth-screen",
    "text-with-actions",
    "tab-bar",
    "product-card",
    "unmatched",
]


class Extraction(BaseModel):
    template_id: TemplateId = Field(description="Which of the 10 templates matches this ASCII pattern. Use 'unmatched' if no template fits well.")
    confidence: float = Field(ge=0, le=1, description="0-1, how sure are you")
    screen_name: str = Field(description="Short kebab-case name for this screen (used in PNG filename). Example: 'sell-mode-picker', 'wallet-header', 'payout-list'")
    alt_text_en: str = Field(description="Descriptive alt text (EN) for the image, 15-150 chars, starts with the screen name")
    alt_text_pt: str = Field(description="Descriptive alt text (pt-BR) for the image, same format")
    content: dict = Field(description="Structured content for the template, as key-value JSON. Fields depend on template_id (see docs).")
    unmatched_reason: Optional[str] = Field(default=None, description="If template_id=unmatched, explain why")


SYSTEM_PROMPT = """You are a UI pattern classifier for the Jamble help center.

You receive an ASCII-art UI mockup from a help article. Classify it into ONE of these 10 templates:

1. settings-row-list: list of settings rows with icon+label inside a card. Required content: {section_title, rows: [{icon: string (emoji or name), icon_bg: "brand"|"gray", label, dimmed?: bool}]}
2. alert-dialog: iOS UIAlertController with title+message+buttons. Required: {title, message, primary_label, secondary_label?}
3. empty-state-cta: empty list with title+subtitle+CTA. Required: {title, subtitle, cta_label}
4. radio-picker: options with radio dots. Required: {title?, options: [{icon?, name, subtitle?, selected?: bool}]}
5. photo-grid: grid of photo slots with numbered badges. Required: {title?, photos: int (count shown), max_photos: int (total allowed)}
6. button-cta: single primary button. Required: {label}
7. stepper-input: title + [-] N [+] stepper. Required: {title, value: int}
8. error-toast: toast with red icon + title + subtitle. Required: {title, subtitle}
9. wallet-nav: nav bar with title + right icons + balance card. Required: {nav_title, right_icons: ["help"?, "clock"?, "bell"?], balance_label, balance_amount, cta_label, pending?: {label, amount}}
10. list-with-status: section title + list of rows with id+amount+status+date. Required: {section_title, rows: [{id, amount, status, status_color: "green"|"red"|"yellow", date}]}
11. form-layout: form screen with title + multiple input fields (text / dropdown / upload) + submit button. Required: {title, fields: [{label, type: "text"|"dropdown"|"upload"|"textarea", placeholder?}], submit_label}
12. auth-screen: welcome/onboarding screen with title + 2-3 stacked action buttons + optional secondary link. Required: {title, buttons: [{label, style: "primary"|"secondary"}], secondary_link?: {label}}
13. text-with-actions: screen with main title + 1-2 paragraphs of body text + one or more buttons. Required: {title, body: string, buttons: [{label, style: "primary"|"secondary"}]}
14. tab-bar: horizontal row of 2-5 tabs (e.g. Deals / Explore / Follow, Activity / Messages / Requests) with a content area placeholder below. Required: {tabs: [string], content_placeholder?: string, active_tab_index?: int}
15. product-card: card with product icon/thumbnail + title + subtitle + price or stock indicator + optional action button. Required: {title, subtitle?, price?, stock?, icon?, cta_label?}

Classification hints:
- Rows with ▶ or chevrons + label = settings-row-list
- Rounded dialog with OK button = alert-dialog
- Title+subtitle+single centered button = empty-state-cta or button-cta (use button-cta if no title)
- ○ ● circles with text = radio-picker
- Grid of rectangles numbered 1/2/3 = photo-grid
- [-] N [+] pattern = stepper-input
- Pill with "Oops" or error message = error-toast
- "My Wallet" + balance + "Withdraw" = wallet-nav
- List with PAY- or #ID + R$ amount = list-with-status
- Form with labeled input fields (text boxes, dropdowns, upload zones) + submit = form-layout
- Welcome/login with title and 2-3 stacked buttons = auth-screen
- Simple screen with title + body text + action button(s) = text-with-actions
- Mix of text and a final button = text-with-actions (not button-cta)
- Horizontal row of 2-5 labeled rectangles/pills/boxes (Deals, Explore, Follow) with area below = tab-bar
- Card with product name + subtitle + price/stock + optional CTA = product-card
- Promotional banner with icon + label = product-card (use title for the main label)

Rules:
- Extract content VERBATIM from the ASCII. Do not paraphrase user-visible strings.
- For pt-BR blocks, preserve Portuguese strings as-is.
- Write alt_text to be useful for screen readers AND SEO. Include the screen name + key UI elements.
- If the ASCII is too unusual to fit any template, set template_id=unmatched and explain in unmatched_reason.
- screen_name must be short, kebab-case, and descriptive. Reuse the same screen_name if the same screen appears in both EN and pt-BR.
"""


def find_ascii_blocks(md_text: str):
    """Yield (start_offset, end_offset, content) for each ASCII code-fenced block."""
    for m in re.finditer(r"```[a-z]*\n(.*?)\n```", md_text, re.DOTALL):
        content = m.group(1)
        if any(c in BOX_CHARS for c in content):
            yield m.start(), m.end(), content


def main():
    client = instructor.from_anthropic(Anthropic())

    article_dirs = sorted(ARTICLES.iterdir())
    filter_slug = None
    limit = None
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--limit" and i < len(sys.argv) - 1:
            limit = int(sys.argv[i + 1])
        elif not arg.startswith("--"):
            filter_slug = arg

    if filter_slug:
        article_dirs = [d for d in article_dirs if d.name == filter_slug]
    elif limit:
        article_dirs = [d for d in article_dirs if d.is_dir()][:limit]

    results = []
    total = 0
    for article_dir in article_dirs:
        if not article_dir.is_dir():
            continue
        slug = article_dir.name
        for locale in ("en", "pt-br"):
            md_path = article_dir / f"{locale}.md"
            if not md_path.exists():
                continue
            text = md_path.read_text()
            for block_idx, (start, end, content) in enumerate(find_ascii_blocks(text), 1):
                total += 1
                try:
                    extraction = client.messages.create(
                        model="claude-haiku-4-5-20251001",
                        max_tokens=1024,
                        system=SYSTEM_PROMPT,
                        messages=[{
                            "role": "user",
                            "content": f"Article slug: {slug}\nLocale: {locale}\nASCII block #{block_idx}:\n\n{content}"
                        }],
                        response_model=Extraction,
                    )
                except Exception as e:
                    print(f"FAIL {slug}/{locale}#{block_idx}: {e}", file=sys.stderr)
                    continue
                print(f"[{total}] {slug}/{locale}#{block_idx} → {extraction.template_id} ({extraction.confidence:.2f}) {extraction.screen_name}")
                results.append({
                    "slug": slug,
                    "locale": locale,
                    "block_index": block_idx,
                    "source_offset": start,
                    "source_end": end,
                    "ascii_raw": content,
                    "extraction": extraction.model_dump(),
                })

    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nWrote {len(results)} extractions to {OUT}")

    # Summary
    by_template = {}
    for r in results:
        t = r["extraction"]["template_id"]
        by_template[t] = by_template.get(t, 0) + 1
    print("\nBy template:")
    for t, n in sorted(by_template.items(), key=lambda kv: -kv[1]):
        print(f"  {t:<24} {n}")


if __name__ == "__main__":
    main()
