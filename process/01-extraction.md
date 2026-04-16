# Step 1, Extract ASCII from Intercom article

**Goal**: pull each `<pre><code>┌─...─┐</code></pre>` block out of an Intercom article, clean it up to proper multi-line ASCII, save as `ascii-box-N.txt`.

## Why this step exists

Intercom stores article bodies as HTML. The ASCII boxes live inside `<pre><code>` blocks, but Intercom's rich-text editor **collapses newlines**, what looks like a multi-line box in the editor is actually stored as one long string with box-drawing chars acting as implicit line breaks. You must re-split before any downstream tool can parse it.

## Command

Fetch article body:
```bash
curl -s \
  -H "Authorization: Bearer $(cat ~/.intercom_token)" \
  -H "Accept: application/json" \
  -H "Intercom-Version: 2.11" \
  "https://api.intercom.io/articles/<ARTICLE_ID>"
```

Python parser (pipe into this):
```python
import sys, json, re

data = json.load(sys.stdin)
body = data.get('body', '')

# Find all <pre><code>...</code></pre> blocks
blocks = re.findall(r'<pre><code>(.*?)</code></pre>', body, re.DOTALL)

for i, b in enumerate(blocks, start=1):
    # Decode HTML entities
    b = b.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&#x27;', "'")

    # Detect box width (position of ┐ from the top-right corner)
    top_end = b.find('┐')
    if top_end > 0:
        width = top_end + 1  # includes ┐
        lines = [b[j:j+width] for j in range(0, len(b), width)]
        lines = [l for l in lines if l.strip()]
        content = '\n'.join(lines) + '\n'
    else:
        content = b

    with open(f'/tmp/ascii-box-{i}.txt', 'w') as f:
        f.write(content)
    print(f'Box {i}: {len(content.splitlines())} lines, {width}px wide')
```

## Output convention

- Save as `ascii-box-N.txt` in the current working folder (either `_work/wireframe-mockups/` for ad-hoc work, or a per-article folder for batch runs)
- Numbering starts at 1, sequential in article reading order (top → bottom)
- One file per ASCII block; never merge multiple blocks into one file

## Common article IDs (reference)

```
14288077 → Start Selling on Jamble
14288078 → Apply to Sell on Jamble                (2 ASCII boxes)
14288085 → New Seller Guide to Listing Products    (4 ASCII boxes)
14288091 → Account Security                        (2 ASCII boxes)
14288093 → How to List Products on Jamble         (4 ASCII boxes) ← validated
```

To list all articles in a collection:
```bash
python3 _brain/integrations/intercom/j-intercom.py articles --collection <COLLECTION_ID>
```

## Sanity check before moving to Step 2

Open the produced `ascii-box-N.txt` files and verify:
- [ ] Box is multi-line (not one long line)
- [ ] Width is consistent across all lines (typically 35 chars)
- [ ] No leftover HTML entities (`&amp;`, `&lt;`, etc.)
- [ ] Box renders correctly when viewed in a monospace font

If the parser output looks wrong, double-check the width detection, some boxes use different widths (25, 40, 50) and the `┐` detection might grab a nested box's corner instead of the outer one.
