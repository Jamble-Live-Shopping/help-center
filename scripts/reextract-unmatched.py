#!/usr/bin/env python3
"""Re-extract only the blocks currently classified as 'unmatched' in _work/ascii-extracted.json.
Uses the updated template list (includes tab-bar, product-card)."""

import json
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# Import the same Extraction model + SYSTEM_PROMPT from the main extractor
from importlib import util
spec = util.spec_from_file_location("extract_ascii", Path(__file__).parent / "extract-ascii.py")
ea = util.module_from_spec(spec)
spec.loader.exec_module(ea)

import instructor
from anthropic import Anthropic

EXTRACTIONS = Path(__file__).resolve().parent.parent / "_work" / "ascii-extracted.json"
data = json.loads(EXTRACTIONS.read_text())

client = instructor.from_anthropic(Anthropic())
changed = 0
for i, e in enumerate(data):
    if e["extraction"]["template_id"] != "unmatched":
        continue
    try:
        new_ext = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=ea.SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Article slug: {e['slug']}\nLocale: {e['locale']}\nASCII block #{e['block_index']}:\n\n{e['ascii_raw']}"
            }],
            response_model=ea.Extraction,
        )
    except Exception as ex:
        print(f"FAIL {e['slug']}/{e['locale']}#{e['block_index']}: {ex}", file=sys.stderr)
        continue
    print(f"[{i+1}/{len(data)}] {e['slug']}/{e['locale']}#{e['block_index']} → {new_ext.template_id} ({new_ext.confidence:.2f}) {new_ext.screen_name}")
    e["extraction"] = new_ext.model_dump()
    if new_ext.template_id != "unmatched":
        changed += 1

EXTRACTIONS.write_text(json.dumps(data, indent=2, ensure_ascii=False))
print(f"\nReclassified {changed} previously-unmatched blocks")
