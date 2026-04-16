#!/usr/bin/env python3
"""
Rewrite articles/<slug>/{en,pt-br}.md to replace ASCII blocks with <img> markdown
pointing to assets/mockups/<slug>__<screen>.png, and convert 2-col tables to <ul>.

Reads _work/ascii-extracted.json (from extract-ascii.py).
Idempotent: running twice has no effect after first pass.

Usage:
    python3 scripts/rewrite-mds.py                # apply to all articles in JSON
    python3 scripts/rewrite-mds.py --dry-run      # show diffs without writing
    python3 scripts/rewrite-mds.py <slug>         # one article only
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXTRACTIONS = REPO / "_work" / "ascii-extracted.json"
ARTICLES = REPO / "articles"


def table_to_ul(match):
    """Convert a 2-column markdown table into a <ul> bullet list.
    If 3+ cols, return the match unchanged (flag for manual PNG treatment).
    """
    table = match.group(0)
    lines = [ln for ln in table.strip().split("\n") if ln.strip()]
    if len(lines) < 3:
        return table
    # Parse cells per row
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if cells and all(c for c in cells):
            rows.append(cells)
    if len(rows) < 2:
        return table
    ncols = len(rows[0])
    if ncols != 2:
        return table  # 3+ cols: leave for manual treatment
    # Skip header (row 0) + separator (row 1, all dashes)
    header = rows[0]
    data = [r for r in rows[1:] if not all(re.match(r'^[-:]+$', c) for c in r)]
    # Output as `- **Label** — value` bullets
    out = []
    for r in data:
        out.append(f"- **{r[0]}** — {r[1]}")
    return "\n".join(out) + "\n"


TABLE_RE = re.compile(r"(?:^\|[^\n]*\|\s*$\n){3,}", re.MULTILINE)


def main():
    extractions = json.loads(EXTRACTIONS.read_text())
    dry = "--dry-run" in sys.argv
    filter_slug = None
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            filter_slug = arg

    # Group by (slug, locale)
    per_file = {}
    for e in extractions:
        ext = e["extraction"]
        if ext["template_id"] == "unmatched":
            continue
        key = (e["slug"], e["locale"])
        per_file.setdefault(key, []).append(e)

    if filter_slug:
        per_file = {k: v for k, v in per_file.items() if k[0] == filter_slug}

    total_ascii = 0
    total_tables = 0
    total_files = 0

    for (slug, locale), blocks in sorted(per_file.items()):
        md_path = ARTICLES / slug / f"{locale}.md"
        if not md_path.exists():
            continue
        text = md_path.read_text()
        original = text

        # Replace ASCII blocks in reverse source_offset order so offsets stay valid
        for e in sorted(blocks, key=lambda x: -x["source_offset"]):
            ascii_raw = e["ascii_raw"]
            # Find the full fenced code block containing this raw content
            fenced_pattern = re.compile(r"```[a-z]*\n" + re.escape(ascii_raw) + r"\n```", re.DOTALL)
            m = fenced_pattern.search(text)
            if not m:
                print(f"  WARN: can't find ASCII block in {slug}/{locale}", file=sys.stderr)
                continue
            ext = e["extraction"]
            alt_key = "alt_text_pt" if locale == "pt-br" else "alt_text_en"
            alt = ext.get(alt_key, ext.get("screen_name", "mockup")).replace("]", ")").replace("[", "(")
            png_name = f"{slug}__{ext['screen_name']}__{locale}.png"
            img_md = f"![{alt}](./assets/mockups/{png_name})"
            text = text[:m.start()] + img_md + text[m.end():]
            total_ascii += 1

        # Convert 2-col tables to bullets (in place, forward order is safe with single-sub)
        table_count_before = len(TABLE_RE.findall(text))
        text = TABLE_RE.sub(table_to_ul, text)
        # Re-count: tables remaining are 3+ col (leave them)
        table_count_after = len(TABLE_RE.findall(text))
        total_tables += (table_count_before - table_count_after)

        if text != original:
            total_files += 1
            if dry:
                print(f"  [DRY] {slug}/{locale}.md: {len(blocks)} ASCII + {table_count_before - table_count_after} tables → diff ready")
            else:
                md_path.write_text(text)
                print(f"  [OK ] {slug}/{locale}.md")

    print(f"\nRewrote {total_files} files, {total_ascii} ASCII → img, {total_tables} tables → bullets")


if __name__ == "__main__":
    main()
