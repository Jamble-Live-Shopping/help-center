# Step 9, Screenshot framing convention

**Why this step is non-negotiable**: the screenshots/mockups are where the article's value concentrates. A seller who lands on an article from a Google result or from Fin's answer will decide in 2 seconds if the article matches their screen, and they decide by looking at the image, not by reading the paragraph above it. An image without proper framing (heading, alt text, descriptive filename, intro sentence) is an image that:

- Google and Fin can't index → the article doesn't rank on the query the image would answer
- LLMs can't extract in context → the image gets lost when the body is chunked for retrieval
- Sellers can't connect to the paragraph → they scroll past, the article scores low CSAT

The mockup pipeline (Steps 3-5) produces beautiful PNGs. This step ensures each PNG is **referenced** so its value is accessible.

---

## The 5-part frame around every screenshot

Every image embedded in an Intercom article must be surrounded by these 5 elements:

```
┌──────────────────────────────────────────────┐
│  1. H2 heading, the feature name            │
│  2. Intro sentence (1 line)                  │
│                                              │
│  3. <img src=... alt=...> ← the mockup       │
│                                              │
│  4. Caption paragraph (optional, 1-2 lines)  │
│  5. Action continuation (what to do next)    │
└──────────────────────────────────────────────┘
```

### 1. H2 heading (mandatory)

Every mockup is introduced by an H2 that names the feature or the step. The heading is the primary index signal for Google / Fin.

**Format**: verb + object, or pure concept name. Short (≤ 40 chars).

- Good: `<h2>Sell Mode</h2>`, `<h2>Set your price</h2>`, `<h2>Step 3: Choose a sell mode</h2>`
- Bad: `<h2>How it works</h2>`, `<h2>Image</h2>`, no heading at all

**Anti-pattern**: placing two mockups under a single H2. Each mockup gets its own H2 or H2+step (e.g. "Step 3", "Step 4", each with its own image).

### 2. Intro sentence (mandatory)

One short sentence directly before the image that **tells the reader what the screenshot shows and why**. Not a definition of the feature, a signpost.

**Format**: "Here's [what you'll see]." or "You'll see [this screen] when [trigger]." or "The [feature] screen looks like this:"

- Good: "You'll see three options when you tap Sell Mode:"
- Good: "Here's the product list for your show, tap **+ Add a listing** to create your first product."
- Bad: "See screenshot below." (zero info, adds noise to extraction)
- Bad: Jumping from heading to image with no connecting text.

### 3. `<img>` with alt text (mandatory)

Alt text is the *only* text index signal for the image itself. It gets indexed by Google, read by screen readers, and used by Fin/LLMs when extracting what the image contains.

**Format**: `<img src="<URL>" alt="<15-150 chars descriptive>">`

Alt text must:
- Describe the **screen** shown, not just its name ("Sell Mode screen with three radio options: Real-time offers, Sudden Death, Buy It Now")
- Use **the same keywords** as the H2 and intro sentence (reinforces the triad)
- Be **unique per image in the article** (never reuse the same alt across multiple images)
- Avoid filler ("Image showing...", "Screenshot of...", start with the content directly)

**Good examples**:
- `alt="Sell Mode screen with three options: Real-time offers selected, Sudden Death, Buy It Now"`
- `alt="Select Photos grid with three product images and Add slot, up to 10 photos"`
- `alt="Pending Application dialog with Ok I will wait! and Reach out buttons"`

**Bad examples**:
- `alt="image1"`, zero info
- `alt="Sell Mode"`, just the H2, no new info
- `alt="Screenshot of the app"`, no keywords, no indexing value

### 4. Caption paragraph (recommended, not mandatory)

A short `<p>` after the image that labels the key elements the seller should notice. Optional for obvious mockups, useful for complex ones.

**Format**: 1-2 sentences, calls out 2-3 specific UI elements by name (in **bold**).

- "The **Real-time offers** option is selected by default. You can change it by tapping **Sudden Death** or **Buy It Now**."
- "The **+** slot at the end lets you add more photos, up to **10 total**."

Skip the caption when:
- The mockup is self-explanatory (one button, one screen title)
- The H2 + intro already described what to look at

### 5. Action continuation (mandatory)

The paragraph after the image tells the reader what to **do next** or what the screen enables. This closes the loop from "you see this" to "now you can act".

- "Once your sell mode is selected, move on to **Step 4: Set your price**."
- "Tap any thumbnail to set it as the cover photo."

---

## Filename convention (GitHub repo)

The PNGs in `Jamble-Live-Shopping/help-center/assets/mockups/` follow a descriptive naming convention. The filename itself is a weak SEO signal (some crawlers index image URLs), but more importantly it's how we locate files when scaling to 228+ mockups.

**Format**: `<article-slug>__<screen-name>.png`

- `how-to-list-products__sell-mode.png`
- `how-to-list-products__select-photos.png`
- `how-to-list-products__pending-application.png`
- `apply-to-sell-live__settings-row.png`

**Rules**:
- Lowercase only, hyphens (no underscores within words, no camelCase)
- `__` (double underscore) separates the article slug from the screen name
- Article slug matches the Intercom URL slug
- Screen name is the feature as known in the iOS codebase (e.g. `sell-mode`, `pending-application`)
- No box numbers (`prod-box1`, `prod-box4`) in final filenames, those were scratch names during development

**Rename the existing files** (one-time migration):
```bash
# In the help-center repo
# prod-box1 → apply-to-sell-live__settings-row
# prod-box2 → apply-to-sell-live__pending-application
# prod-box3 → how-to-list-products__your-show-empty
# prod-box4 → how-to-list-products__sell-mode
# prod-box5 → how-to-list-products__select-photos
```

(Do this migration when touching the files next time, not retroactively, Intercom has already cached the old URLs on its CDN.)

---

## Full example (complete frame applied)

Below is what a properly framed screenshot block looks like in the Intercom article body:

```html
<h2 id="h_dbaecacc40">Step 3: Choose a sell mode</h2>

<p>Sell mode controls how buyers purchase your item during the show. You'll see three options:</p>

<img src="https://raw.githubusercontent.com/Jamble-Live-Shopping/help-center/main/assets/mockups/how-to-list-products__sell-mode.png"
     alt="Sell Mode screen with three options: Real-time offers selected, Sudden Death, Buy It Now">

<p>The <b>Real-time offers</b> option is selected by default. You can change it by tapping <b>Sudden Death</b> or <b>Buy It Now</b>.</p>

<p>Once your sell mode is selected, move on to <a href="#h_price">Step 4: Set your price</a>.</p>
```

This 5-element frame hits every SEO/GEO signal:
- H2 with feature name → indexed
- Intro sentence with keyword "sell mode" → reinforces the triad
- Image with rich alt text → indexed + accessible
- Caption with bolded element names → extractable facts
- Action continuation with internal link → entity graph

---

## Updated B8 criterion in the checklist

Replace B8 in [08-seo-geo-checklist.md](08-seo-geo-checklist.md) with:

> **B8. Every screenshot is framed (H2 + intro + alt + action)** (1 pt)
> Each mockup sits inside the 5-part frame: H2 heading naming the feature, 1-line intro sentence, `<img>` with descriptive alt text (15-150 chars, unique per article, contains keywords), optional caption with bolded UI elements, action continuation paragraph. Unframed mockups are invisible to search, skipping this criterion auto-fails the article.

---

## Audit: find unframed screenshots in existing articles

Run this over a published article to spot unframed images:

```python
import re, json, subprocess

article_id = "14288093"
body = json.loads(subprocess.check_output([
    "curl", "-s",
    "-H", f"Authorization: Bearer {open('/Users/aymardumoulin/.intercom_token').read().strip()}",
    "-H", "Accept: application/json",
    "-H", "Intercom-Version: 2.11",
    f"https://api.intercom.io/articles/{article_id}",
]))['body']

imgs = list(re.finditer(r'<img[^>]+>', body))
for idx, m in enumerate(imgs, 1):
    tag = m.group(0)
    alt_match = re.search(r'alt="([^"]*)"', tag)
    alt = alt_match.group(1) if alt_match else ''

    # Look 500 chars before for an H2
    before = body[max(0, m.start()-500):m.start()]
    has_h2 = bool(re.search(r'<h2[^>]*>[^<]+</h2>', before))

    # Look 300 chars before for an intro <p>
    has_intro = bool(re.search(r'<p[^>]*>[^<]{20,}</p>\s*(?!<h)', before))

    fail = []
    if not alt or len(alt) < 15: fail.append('alt<15')
    if len(alt) > 150: fail.append('alt>150')
    if not has_h2: fail.append('no_h2_nearby')
    if not has_intro: fail.append('no_intro_nearby')

    status = 'FAIL: ' + ','.join(fail) if fail else 'OK'
    print(f'Image {idx}: {status} | alt="{alt[:80]}"')
```

This catches the 3 most common failures:
- alt text missing, too short, or too long
- no H2 within 500 chars before the image
- no intro `<p>` directly preceding the image

---

## Summary: why every screenshot matters more than every paragraph

Sellers skim articles. Fin extracts chunks. Google indexes visible content. In all 3 cases, **images carry disproportionate weight**, a well-framed image moves the needle 5-10× more than an extra paragraph of prose. This step is not optional polish; it's the single highest-leverage content investment in the pipeline.
