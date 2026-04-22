# Step 6, Replace ASCII blocks with images in Intercom articles

**Goal**: for each `<pre><code>┌─...─┐</code></pre>` block in the article, swap it with `<img src="<github-url>">`. Persist via the Intercom API.

## Intercom API crash course

```bash
# Auth header, same for all calls
AUTH="Authorization: Bearer $(cat ~/.intercom_token)"
ACCEPT="Accept: application/json"
VERSION="Intercom-Version: 2.11"
```

### Author ID, always attribute to Aymar

Every article update via this pipeline must set `author_id: 7980499` (Aymar Dumoulin, aymar@jamble.com). This ensures the help center attributes ownership to the operator running the pipeline, not whoever originally authored the article.

**Admin ID reference**:
- `7980499`, Aymar Dumoulin (aymar@jamble.com), **default for all pipeline updates**
- `7980507`, Mahaut Lacan (mahaut@jamble.com), legacy author on many articles

**How to include in a PUT**: always add `author_id` to the body payload:

```bash
curl -s -X PUT "https://api.intercom.io/articles/<ID>" \
  -H "$AUTH" -H "Content-Type: application/json" -H "$VERSION" \
  -d '{"body": "...", "author_id": 7980499}'
```

Or in Python:
```python
payload = {
    'body': new_body,
    'author_id': 7980499,  # Aymar
}
```

- `GET /articles/<id>`, returns `{body: "<html...>", ...}`
- `PUT /articles/<id>` with `{body: "<new html>"}`, updates the article

**Key quirks** (learned the hard way):
- Intercom **strips inline `style=""` on `<img>`**, border radius, width, etc. must be baked into the PNG
- Intercom **refuses `data:image/...;base64,...` URIs**, images must live at an external URL
- Intercom **auto-copies external images to its own CDN** (`intercom-attachments-1.com`) on first fetch. After copy, the `src` in the stored body points to the Intercom CDN, not GitHub.
- Intercom **keys its CDN cache by the filename in the raw.github URL**. Re-submitting the same URL after updating the PNG on GitHub does NOT force a re-fetch; Intercom keeps serving the old attachment. **Rename with a `__v2.png` (then `__v3.png`, …) suffix and update md refs** to bust the cache. Do this whenever you re-render an existing mockup.
- After a push to `main` that changes PNG bytes but not the filename, `scripts/sync-one.sh` will succeed but the user will still see the old image. If you see pixelation or an outdated mockup, check the filename suffix first.

## The replacement script

```python
import sys, json, re, subprocess

ARTICLE_ID = "14288093"
REPLACEMENTS = [
    # (unique text in the ASCII, GitHub URL, alt text)
    ("Sell Mode",       "https://raw.githubusercontent.com/Jamble-Live-Shopping/help-center/main/assets/mockups/prod-box4.png", "Sell Mode screen"),
    ("Select photos",   "https://raw.githubusercontent.com/Jamble-Live-Shopping/help-center/main/assets/mockups/prod-box5.png", "Select Photos screen"),
    # ... one tuple per ASCII block in this article
]

# Fetch current body
article = json.loads(subprocess.check_output([
    "curl", "-s",
    "-H", f"Authorization: Bearer {open('/Users/aymardumoulin/.intercom_token').read().strip()}",
    "-H", "Accept: application/json",
    "-H", "Intercom-Version: 2.11",
    f"https://api.intercom.io/articles/{ARTICLE_ID}"
]))
body = article['body']

# For each replacement, swap the matching <pre><code> block
for unique_text, url, alt in REPLACEMENTS:
    # Match a <pre><code> that contains the unique text
    pattern = rf'<pre><code>[^<]*{re.escape(unique_text)}[^<]*</code></pre>'
    new_tag = f'<img src="{url}" alt="{alt}">'
    body_new = re.sub(pattern, new_tag, body, flags=re.DOTALL)
    if body_new == body:
        print(f'WARN: "{unique_text}" not found or already replaced')
    body = body_new

# Also handle cases where Intercom already cached the old version
# (on re-runs, the <img> tag is there with intercom-attachments-1.com URL)
# Match by the original github URL or by a distinctive part of the old URL

# Save for PUT
with open('/tmp/intercom-update.json', 'w') as f:
    json.dump({'body': body}, f)
```

Then push:

```bash
curl -s -X PUT "https://api.intercom.io/articles/<ID>" \
  -H "Authorization: Bearer $(cat ~/.intercom_token)" \
  -H "Content-Type: application/json" \
  -H "Intercom-Version: 2.11" \
  -d @/tmp/intercom-update.json | python3 -c "
import sys, json
data = json.load(sys.stdin)
errors = data.get('errors', [])
print('ERRORS:' if errors else 'OK', errors if errors else data.get('title',''))
"
```

## Handling updates (not just first-time replacements)

After the first replacement, Intercom has cached the image on its own CDN. The stored body now contains something like:

```html
<img src="https://jamble-bdca2cf2859f.intercom-attachments-1.com/i/o/oenjhaid/.../prod-box4.png?...">
```

To update the image (new version pushed to GitHub), you can't rely on matching the original ASCII anymore, that's gone. Instead, target the `intercom-attachments-1.com` URL OR keep a mapping of `article_id → box_number → alt_text` and match by `alt="..."`:

```python
# Re-run pattern, target the cached img by alt text
body_new = re.sub(
    r'<img[^>]*alt="Sell Mode screen"[^>]*>',
    f'<img src="{NEW_GITHUB_URL}" alt="Sell Mode screen">',
    body
)
```

Keep the `alt` text stable across runs. It's your anchor.

## Multilingual articles (EN + pt-BR)

Each article has two locales. Use the `--locale` flag if going through `j-intercom.py`, or pass `?locale=pt-BR` on the API, or, simpler, run the replacement twice, once per locale. The article IDs are the same; only the `body` differs.

For the current Seller Center corpus: 67 articles × 2 locales = 134 article bodies to update.

## Safety checks (do these BEFORE hitting PUT on a batch)

- [ ] Dry-run: run the script in read-only mode, print `len(body_old)` vs `len(body_new)` for each article
- [ ] Spot-check: pick 3 articles at random, diff the old and new body manually, confirm only the intended blocks changed
- [ ] Stage: apply to 1 article, open the live URL on mobile (TestFlight or real device), eyeball the result
- [ ] Rollback plan: save the pre-update body to a backup file (`/tmp/article-<id>-before.json`) so you can restore with a second PUT

**Never bulk-update without the 3-article preview step**. A bad regex could blow away content across 134 article bodies in under a minute.

## Verify zero ASCII blocks remain (MANDATORY before marking article done)

After every PUT, re-fetch the article and scan for any remaining `<pre><code>` blocks containing box-drawing characters. Easy to miss a block that wasn't matched by your regex (e.g. a lonely button box like "Add Listing" with no distinctive title, or a box that the extraction step renumbered between runs).

```bash
curl -s -H "Authorization: Bearer $(cat ~/.intercom_token)" -H "Accept: application/json" -H "Intercom-Version: 2.11" \
  "https://api.intercom.io/articles/<ID>" | python3 -c "
import sys, json, re
body = json.load(sys.stdin).get('body','')
blocks = re.findall(r'<pre><code>(.*?)</code></pre>', body, re.DOTALL)
box_blocks = [b for b in blocks if any(c in b for c in '┌┐└┘│─')]
print(f'ASCII boxes remaining: {len(box_blocks)}')
for i, b in enumerate(box_blocks):
    print(f'  Block {i+1}: {b[:120]}')
"
```

Expected output: `ASCII boxes remaining: 0`. If >0, identify each remaining block, extract it, run the full Step 3-6 pipeline, and re-inject. **Do not ship an article with any remaining `<pre><code>┌─...─┐</code></pre>` block**, it will render broken on mobile.

## Verification

After update, the article live URL shows the new image:
```
https://intercom.help/jamble-bb4bea116bbe/<locale>/articles/<id>-<slug>
```

Check both desktop and mobile rendering. On mobile, the PNG should:
- Fill the content width (up to ~300px phone card inside the ~360px article width)
- Show the gray outer frame clearly
- Have the phone card shadow visible
- Remain readable without zoom
