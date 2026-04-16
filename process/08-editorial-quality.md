# Step 8, Editorial quality (SEO, tone, localization)

**Goal**: apply Intercom's editorial best practices on every article before considering it shipped. Pipeline covers layout (Steps 1-7); this step covers the writing itself.

**Source**: [Intercom, How to write great help articles](https://www.intercom.com/help/en/articles/56645-how-to-write-great-help-articles), [7 steps to creating better help content](https://www.intercom.com/blog/creating-better-help-content/).

---

## RULE 0, Never use em-dashes, use commas

Mandatory style rule across every article, H1, H2, body paragraph, bullet, and alt text.

**Replace** every em-dash character (U+2014, the long dash) with a comma. Also replace the en-dash (U+2013) with a comma. Only use hyphens `-` for compound words (`real-time`, `pt-BR`, `self-hosted`).

### Examples

| Bad (uses em-dash)                              | Good (uses comma)                                |
|-------------------------------------------------|--------------------------------------------------|
| `Real-time offers [EMDASH] The starting price.` | `Real-time offers, The starting price.`          |
| `Too vague [EMDASH] which cards?`               | `Too vague, which cards?`                        |
| `Similar to Real-time offers [EMDASH] buyers compete.` | `Similar to Real-time offers, buyers compete.`   |

*(`[EMDASH]` shown as a placeholder to keep this doc comma-only. In the article body, it is the actual long-dash character.)*

### Automated check

```python
EMDASH = chr(0x2014)
ENDASH = chr(0x2013)
count = body.count(EMDASH) + body.count(ENDASH)
assert count == 0, f'{count} em/en-dashes found, replace with commas'
```

### Why

Consistent house style. Em-dashes render inconsistently in some Intercom renderers (they can be stripped, doubled, or turned into `--`). Commas are safer across every channel.

Three rules are ENFORCED (run the checklist before any publish). Three are RECOMMENDED (apply when the ROI is obvious). Split, empathy phrasing, visual density per step are in TESTING, not yet enforced, see the testing track at the bottom.

---

## RULE 1, Description must be ≤140 characters

Intercom's own docs: "Keep this short and to the point (aim for no more than 140 characters)."

Why: the description shows in search engine snippets, in the help center article list, and in Messenger previews. Longer descriptions get truncated mid-sentence and lose keywords.

**How to check**: `len(article['description'])` ≤ 140.

**How to rewrite**: lead with the job-to-do, cut the "complete reference" / "this guide" filler, drop everything after the first keyword-dense sentence.

### Example

Before (262 chars):
> "This guide is your complete reference for creating product listings on Jamble. You'll learn every field available in the listing form, how each sell mode works, how to set prices, add photos, and get your products ready to sell during your live shows"

After (118 chars):
> "Create product listings for your live shows - titles, sell modes, prices, photos, and all required fields explained."

### How to update via API

```bash
curl -s -X PUT "https://api.intercom.io/articles/<ID>" \
  -H "Authorization: Bearer $(cat ~/.intercom_token)" \
  -H "Content-Type: application/json" \
  -H "Intercom-Version: 2.11" \
  -d '{"description": "<≤140 char description>", "author_id": 7980499}'
```

Note: `description` is a top-level article field, NOT inside `body`. Don't confuse with the `<p>` under "What you'll learn".

---

## RULE 2, Examples must reflect Brazilian market reality

Jamble market reality (`product_mix_br.md`): **~90% collectibles** in Brazil (50% Pokémon TCG, 40% diecast/Hot Wheels, 10% other). Fashion/sneakers are NOT the primary category on Jamble BR. The English version of each article is the translation of the Brazilian version, both must feature BR-appropriate examples.

Rule: **every example item, image, or placeholder must be a collectible** (trading card, diecast, sealed pack), not fashion/sneakers.

### Examples (drop-in library)

Use these verbatim or adapt with the same vocabulary:

**Pokémon TCG**
- "Charizard VMAX PSA 9 - Scarlet & Violet"
- "Pokémon Booster Pack - Paldea Evolved"
- "Mew ex Special Collection Box"
- "Pikachu Illustrator Graded PSA 10"

**Hot Wheels / Diecast**
- "Hot Wheels 2024 Super Treasure Hunt - C-10"
- "Hot Wheels RLC Datsun 510 - Spectraflame Blue"
- "Mini GT Nissan Skyline GT-R - 1/64"
- "Matchbox Premium 1969 Dodge Charger"

**Other collectibles (sparingly)**
- "One Piece TCG - Romance Dawn Booster Box"
- "Magic: The Gathering Commander Masters Bundle"

### Banned examples in any article

- Nike / Adidas / sneakers (`"Nike Air Max 90 - Size 42"`), not BR market
- Fashion / apparel in isolation (`"Camiseta Vintage Band - M - Preta"`), secondary category at best
- Generic goods without brand/condition detail (`"T-shirt"`, `"Watch"`)

### Localization rule

- Write examples in English (primary source), then translate to pt-BR in the same article (locale: `pt-BR`)
- Product names can stay in English when they're the canonical collector name (e.g. "Charizard VMAX PSA 9" is a product SKU, not a translation)
- Condition grades (PSA 10, Mint, CIB) stay in English, universal collector vocabulary

---

## RULE 2b, Currency localization

The EN article and the pt-BR article use different currency formats. Do not mirror them.

| Locale | Currency symbol | Format | Example |
|--------|-----------------|--------|---------|
| EN     | `$` (dollar)    | `$5.00`, `$5,000.00` (no space) | "The minimum price is $5.00 and the maximum is $5,000.00" |
| pt-BR  | `R$` (BRL)      | `R$ 5,00`, `R$ 5.000,00` (space after R$, BR-style decimal) | "O preço mínimo é R$ 5,00 e o máximo é R$ 5.000,00" |

**Why**: English-language readers expect `$`. Brazilian Portuguese readers expect `R$` with BR number formatting (comma as decimal separator, dot as thousands separator).

**Application**:
- Replace every `R$` in the EN body with `$`.
- Keep `R$` in the pt-BR body.
- If a mockup PNG shows `R$` (which reflects the actual Brazilian app UI), that is fine, the PNG stays the same in both locales. The surrounding prose localizes.

**Automated check**:
```python
import re
en_has_rs = len(re.findall(r'R\$', en_body)) > 0
pt_has_rs = len(re.findall(r'R\$', pt_body)) > 0
assert not en_has_rs, 'EN body must use $, not R$'
assert pt_has_rs, 'pt-BR body must use R$, not $'
```

---

## RULE 2c, Never use "auction" or "leilão"

In Jamble's product language, the auction-style sell mode is called **"Real-time offers"** (EN) / **"Ofertas em tempo real"** (pt-BR). The word "auction" exists in the code as the internal enum `ShowSaleType.AUCTION`, but it is never surfaced to users.

**Banned words across every article, EN and pt-BR**:
- `Auction`, `auction`
- `Leilão`, `leilao`, `Leilao`

**Replace with**:
- EN: "Real-time offers"
- pt-BR: "Ofertas em tempo real"

**Why**: In Brazil, "leilão" carries regulatory and cultural connotations (government property auctions, distressed goods) that don't match Jamble's product experience. We deliberately chose "Real-time offers" / "Ofertas em tempo real" to frame the feature as a modern competitive bidding experience, not an auction.

**Automated check**:
```python
import re
banned = re.findall(r'\b[Aa]uction\b|\b[Ll]eil[aã]o\b', body + pt_body)
assert not banned, f'Banned auction wording found: {set(banned)}'
```

This rule also aligns with the long-standing internal feedback (`feedback_no_auction_word.md`).

---

## RULE 3, Lead with the job, not the feature

Intercom's #1 writing principle: reframe every heading to describe what the user achieves, not what they interact with.

### Reframing cheat-sheet (apply on every H1 and H2)

| Feature-framed (avoid) | Job-framed (use) |
|------------------------|------------------|
| "Step by step" | "Create a product listing that sells" |
| "Choose a sell mode" | "Pick how buyers will compete for your item" |
| "Add a title" | "Write a title that gets clicks" |
| "Add photos" | "Add photos that sell" |
| "Add a description" | "Describe details buyers care about" |
| "Save your listing" | "Save and get ready to sell" |
| "How this feature works" | "What happens when buyers see your listing" |

Pattern recognition: if a heading starts with a verb that describes the UI action (`Choose`, `Select`, `Add`, `Enter`), reframe to start with a verb that describes the user's outcome (`Pick how...`, `Write a title that...`, `Help buyers find...`).

The body can still describe the UI. The heading must describe the destination.

---

## RULE 4, Table of contents for articles with 6+ H2 sections

Articles with many sub-steps need navigation. Intercom supports anchor links to auto-generated heading IDs.

Every `<h2>` in Intercom has a generated `id="h_XXXXXXXX"`. Find them in the current body and build a linked TOC at the top of the article (right after "What you'll learn" or as its own intro block).

### Template (insert right after the "What you'll learn" section)

```html
<h2 id="h_toc">Jump to a step</h2>
<ul>
  <li><p><a href="#h_774ba3c97e">Step 1: Open your show and add a product</a></p></li>
  <li><p><a href="#h_e97f0af6cd">Step 2: Write a title that gets clicks</a></p></li>
  <li><p><a href="#h_XXXXXXXXXX">Step 3: Pick how buyers will compete</a></p></li>
  <!-- ... one per step -->
</ul>
```

### How to build it automatically

```python
import re
# Pull all <h2 id="..."> and their text
h2s = re.findall(r'<h2[^>]*id="([^"]+)"[^>]*>(.*?)</h2>', body)
toc_items = ''.join(f'<li><p><a href="#{id}">{text}</a></p></li>' for id, text in h2s)
toc = f'<h2 id="h_toc">Jump to a step</h2><ul>{toc_items}</ul>'
```

**Threshold**: apply TOC when an article has **6 or more H2 sections**. Shorter articles don't need it.

---

## RECOMMENDATION 1, Screenshot/mockup convention per step

For "how-to" articles with multi-step workflows, every MAJOR step deserves a visual anchor (either real screenshot or code-faithful mockup). Rule of thumb: if a step references a specific screen, button, or input field, show it.

### Convention

| Step type | Visual required? | Visual style |
|-----------|------------------|--------------|
| User taps a button | YES | Mockup of the screen with the button highlighted |
| User fills a field | YES | Mockup of the field with a realistic sample value (from the BR examples library above) |
| User selects from a list | YES | Mockup showing 1 option selected with brand purple |
| User reads confirmation | YES | Alert/toast mockup |
| User waits (passive) | NO | Skip, use text |
| "Important tips" / general commentary | NO | Skip |

For each visual, follow the Step 3-6 pipeline: HTML mockup → Puppeteer PNG → GitHub upload → Intercom injection.

### Naming convention

Under `assets/mockups/` in the help-center repo, use `{article-id}-step{N}.png` when the mockup is specific to a step, or `{component-name}.png` when it's a generic component used across articles.

Example for article 14288093:
- `14288093-step2-title-field.png`
- `14288093-step5-shipping-profiles.png`
- `sell-mode-selector.png` (reusable across multiple articles)

### Batching images in alt text

For every `<img>`, include descriptive `alt` text that describes the UI for screen readers AND for AI indexing:

```html
<img src="..." alt="Product listing form showing title field with 60-character counter and placeholder text">
```

Never leave `alt=""`. Never use generic alt like `alt="image"` or `alt="screenshot"`.

---

## RECOMMENDATION 2, Apply on articles with known visibility

Don't batch-apply these rules to the entire 67-article corpus blindly. Apply on:
1. High-traffic articles first (pull view count from `article['statistics']['views']`)
2. Articles with support conversations attached (the ones users actually read when confused)
3. Articles in the Getting Started collection (first touch for new sellers)

For lower-traffic articles, Rule 1 and Rule 2 are still cheap and worth applying; Rules 3 and 4 can wait.

---

## IN TESTING, not yet process

These experiments need a validation round before being codified.

### Split long articles (11+ steps) into 2-3 focused articles

**Hypothesis**: a 19k-char article with 11 steps + pre-offers + tips + FAQ is trying to be a reference. Readers would be better served by 3 focused articles:
- "How to list a product" (Steps 1-11)
- "Understanding sell modes" (sell mode deep-dive)
- "Listing FAQ & tips" (pre-offers, app memory, common questions)

**Validation needed**: A/B the 1-article vs 3-article version on view count, sad/happy ratio, and internal linking. If the split articles individually outperform, codify the split.

### Empathy phrasing

**Hypothesis**: adding phrases like "We understand it's hard to...", "Don't worry...", "A great workaround is..." warms the tone and increases article satisfaction.

**Validation needed**: test 2-3 empathy phrases per article on a sample of 5 articles, measure happy rate delta. If significant (>5pp), add to the editorial checklist.

### Where to track the testing

Create a row in `4-TODO.md` of the parent project with:
- Article ID being tested
- Hypothesis
- Metric + baseline
- Target delta
- Decision deadline (typically 2 weeks of views)

---

## Checklist (run before shipping any article)

- [ ] Description ≤ 140 chars (Rule 1)
- [ ] Zero non-BR examples (Nike, fashion-only, generic goods) (Rule 2)
- [ ] All H1/H2 reframed to jobs-to-do, not UI actions (Rule 3)
- [ ] TOC at top if ≥6 H2 sections (Rule 4)
- [ ] `author_id: 7980499` on every PUT
- [ ] Every `<img>` has meaningful `alt` text
- [ ] Tested on mobile via the intercom.help public URL (or Firecrawl screenshot)
