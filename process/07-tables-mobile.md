# Step 7, Fix tables that break on mobile

**Problem**: Intercom's table renderer doesn't add horizontal scroll on mobile. A 2+ column table with any content wider than ~150px per column gets cut off at the right edge, hiding content entirely from readers.

**Real example**: article 14288093 had a "Sell mode / What the price means" table where the second column was clipped on iPhone 13 width (390px), users saw "The sta..." with no way to scroll.

## What Intercom allows (and doesn't)

Source: [Intercom Developers, Allowed HTML for Articles](https://developers.intercom.com/docs/guides/help-center/supported-html)

Key constraints:
- **`<div>` and `<span>` are replaced with `<p>`** → you cannot wrap a table in `<div style="overflow-x:auto">`. The wrapper is stripped.
- **Only 2 CSS classes supported**: `intercom-align-center`, `intercom-h2b-button`. No custom styles at all.
- **Nested `<ul>`/`<ol>` causes `400 Bad Request`** → definition list-style nesting is out.
- **`<dl>` is not supported** (hard fail).
- **`<table>` is supported**, but rendered natively without mobile responsive treatment.

Conclusion: there is no CSS-only fix. Tables must be restructured at the HTML level.

## Decision tree

```
Is the table 2 columns (label → value)?
├── YES → Convert to <ul><li><b>Label</b>, Value</li></ul>
└── NO  → Is the content simple text?
         ├── YES → Split into multiple 2-column tables (one per logical group), each converted to a list
         └── NO  → Render as a PNG mockup (use the Step 3,6 pipeline)
```

The vast majority of Jamble help center tables are 2-column "header → explanation" tables (sell modes, shipping profiles, condition grades). These all go to lists.

## Pattern: 2-column table → bulleted list

**Before** (Intercom table HTML):
```html
<div class="intercom-interblocks-table-container">
  <table role="presentation"><tbody>
    <tr><td><p class="no-margin">Sell mode</p></td><td><p class="no-margin">What the price means</p></td></tr>
    <tr><td><p class="no-margin">Real-time offers</p></td><td><p class="no-margin">The <b>starting price</b>. Buyers will place offers above this amount</p></td></tr>
    <tr><td><p class="no-margin">Sudden Death</p></td><td><p class="no-margin">The <b>starting price</b>. Same as Real-time offers</p></td></tr>
    <tr><td><p class="no-margin">Buy It Now</p></td><td><p class="no-margin">The <b>fixed price</b> the buyer pays to purchase immediately</p></td></tr>
  </tbody></table>
</div>
```

**After**:
```html
<ul>
  <li><p><b>Real-time offers</b>, The <b>starting price</b>. Buyers will place offers above this amount</p></li>
  <li><p><b>Sudden Death</b>, The <b>starting price</b>. Same as Real-time offers</p></li>
  <li><p><b>Buy It Now</b>, The <b>fixed price</b> the buyer pays to purchase immediately</p></li>
</ul>
```

Rules for the conversion:
- Drop the header row (column names, those become the intro sentence in the paragraph above the list)
- The first cell becomes `<b>...</b>` followed by a comma and then the second cell's content
- Preserve inner `<b>` tags in the value cell
- Wrap the `<li>` body in `<p>` (Intercom prefers paragraph wrappers inside `<li>`)
- Never nest another `<ul>` inside `<li>` (Intercom hard-fails on nested lists)

## Automated script

```python
import json, re, subprocess

ARTICLE_ID = "14288093"

# Fetch
raw = subprocess.check_output([
    "curl", "-s",
    "-H", f"Authorization: Bearer {open('/Users/aymardumoulin/.intercom_token').read().strip()}",
    "-H", "Accept: application/json",
    "-H", "Intercom-Version: 2.11",
    f"https://api.intercom.io/articles/{ARTICLE_ID}"
])
data = json.loads(raw)
body = data['body']

def table_to_list(match):
    table_html = match.group(0)
    rows = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
    if not rows:
        return table_html  # leave unchanged if parse fails
    items = []
    header_done = False
    for row in rows:
        cells = re.findall(r'<td[^>]*><p[^>]*>(.*?)</p></td>', row, re.DOTALL)
        if len(cells) != 2:
            continue  # skip rows that aren't 2-column
        if not header_done:
            header_done = True
            continue  # drop header row
        label, value = cells
        label_clean = re.sub(r'</?[^>]+>', '', label).strip()  # strip inner tags from label
        items.append(f'<li><p><b>{label_clean}</b>, {value.strip()}</p></li>')
    if not items:
        return table_html
    return '<ul>' + ''.join(items) + '</ul>'

new_body = re.sub(
    r'<div class="intercom-interblocks-table-container">.*?</div>',
    table_to_list,
    body,
    flags=re.DOTALL
)

with open('/tmp/intercom-tables.json', 'w') as f:
    json.dump({'body': new_body}, f)

# Push
subprocess.run([
    "curl", "-s", "-X", "PUT",
    f"https://api.intercom.io/articles/{ARTICLE_ID}",
    "-H", f"Authorization: Bearer {open('/Users/aymardumoulin/.intercom_token').read().strip()}",
    "-H", "Content-Type: application/json",
    "-H", "Intercom-Version: 2.11",
    "-d", "@/tmp/intercom-tables.json"
])
```

## When to fall back to a PNG mockup

If the table has:
- 3+ columns
- Rich embedded content (images, buttons, complex formatting)
- Visual semantics that matter (e.g. a price grid, a comparison matrix with checkmarks)

Then the list conversion loses information. Use the standard Step 3,6 pipeline:
- Build the table as a styled HTML mockup (mobile-friendly width 320px, possibly with a horizontal scroll hint)
- Screenshot to PNG
- Upload to `Jamble-Live-Shopping/help-center/assets/mockups/`
- Replace the `<table>` (or its surrounding `<div class="intercom-interblocks-table-container">`) with an `<img>` tag

For this, add a new HTML pattern to [03-html-template.md](03-html-template.md):

```html
<!-- PATTERN E: Table (3+ columns, PNG fallback) -->
<div class="phone" style="width: 320px;">
  <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
    <thead>
      <tr>
        <th style="text-align: left; padding: 8px; background: #F9FAFC; color: #6B7A92; font-weight: 600; border-bottom: 1px solid #E9EAEF;">Col 1</th>
        <th style="text-align: left; padding: 8px; background: #F9FAFC; color: #6B7A92; font-weight: 600; border-bottom: 1px solid #E9EAEF;">Col 2</th>
        <th style="text-align: left; padding: 8px; background: #F9FAFC; color: #6B7A92; font-weight: 600; border-bottom: 1px solid #E9EAEF;">Col 3</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px; border-bottom: 1px solid #E9EAEF; color: #162233;">Row data</td>
        <td style="padding: 8px; border-bottom: 1px solid #E9EAEF; color: #162233;">Row data</td>
        <td style="padding: 8px; border-bottom: 1px solid #E9EAEF; color: #162233;">Row data</td>
      </tr>
    </tbody>
  </table>
</div>
```

## Audit script: find all table-breaking articles

Run this once over the 67-article corpus to produce a list of articles to fix:

```bash
for ID in $(python3 _brain/integrations/intercom/j-intercom.py articles --collection 19177935 2>/dev/null | awk 'NR>2 && /published/ {print $1}'); do
  BODY=$(curl -s -H "Authorization: Bearer $(cat ~/.intercom_token)" -H "Accept: application/json" -H "Intercom-Version: 2.11" "https://api.intercom.io/articles/$ID" | python3 -c "import sys,json; print(json.load(sys.stdin).get('body',''))")
  TABLES=$(echo "$BODY" | grep -c "intercom-interblocks-table-container" || echo 0)
  if [ "$TABLES" -gt 0 ]; then
    echo "$ID has $TABLES table(s)"
  fi
done
```

## Add this step to the checklist in README

After the 6 original steps, every article should pass:

- [ ] 7. No `<table>` remains that would break on mobile, either converted to `<ul>` or rendered as PNG mockup

## Why not just use `<ul>` from the start?

Users (and writers) perceive tables as "more official", they signal structured data. But the 2-column label/value case is inherently just a list, and lists render correctly on every viewport size. The table was a formatting preference, not a semantic requirement. The list conversion loses no information and gains universal readability.

For genuinely tabular data (3+ columns that only make sense in relation, like a comparison matrix), the PNG fallback preserves semantics at the cost of not being selectable/searchable text, an acceptable trade-off for edge cases.
