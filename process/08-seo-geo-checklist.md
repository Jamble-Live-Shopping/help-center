# Step 8, SEO / GEO fact-checking checklist for help articles

**Goal**: ensure every published help article is findable (SEO) and AI-readable (GEO - Generative Engine Optimization) without degrading the help center UX.

**Source**: adapted from the Press Article Scorecard at `jamble-projects/1-upcoming/1l-seo-geo-visibility/deliverables/press-article-scorecard.md`. Key differences vs press:
- Help articles are **inbound** (user has a problem, searches for the answer) → findability matters more than entity moat
- No "moat claim" or "About Jamble" boilerplate needed → adapted to "concept statement" + "facts density"
- **pt-BR is the primary locale** (Jamble BR = main market). EN is the translation, not the other way around.
- Purpose: answer the user's question, enable Fin (Intercom AI) + Google + in-app search to surface the right article

**Threshold**: 7/10 SEO + 7/10 GEO minimum to publish. UX bonus is nice-to-have.

---

## SECTION A, SEO / Findability (10 points)

| # | Criterion | Weight | Check | Detail |
|---|-----------|--------|-------|--------|
| A1 | **Action-based title, ≤ 60 chars, contains primary keyword** | 1 | [ ] | Starts with a verb ("How to...", "Set up...", "Understand..."). Contains the exact search term users would type. Example: "How to List Products on Jamble" ✓ vs "Product listing guide" ✗ |
| A2 | **Description ≤ 140 chars, contains primary query** | 1 | [ ] | Intercom best practice = max 140. Description = what the article covers + for whom. Example: "Create product listings for your live shows - titles, sell modes, prices, photos explained." (113 chars) |
| A3 | **Primary query appears verbatim in H1 or first paragraph** | 1 | [ ] | The exact question users ask ("how to list a product", "how to set price") appears word-for-word in the intro. Signals relevance to search engines and LLMs. |
| A4 | **Keywords in H2 headings or `<b>` bold** | 1 | [ ] | Domain terms (sell mode, shipping profile, flash sale, Pokemon TCG, PIX) appear in subheadings or bold text, not buried in paragraphs |
| A5 | **3+ internal links to related help articles** | 1 | [ ] | Links to 3+ other help center articles with descriptive anchor text (not "click here"). Builds article graph, helps Fin recommend follow-ups |
| A6 | **Structured content: lists / bullets / mockups** | 1 | [ ] | No walls of text. Content is broken into scannable blocks. Tables are either 2-col lists or PNG mockups (see Step 7) |
| A7 | **pt-BR is primary, EN is translation** | 1 | [ ] | pt-BR version is the authoritative one (market = Brazil). EN is a faithful translation of pt-BR, not an independent write-up. Both locales carry the same facts, examples, and screenshots |
| A8 | **App concepts named explicitly** | 1 | [ ] | Jamble-specific terms are named and linked/defined on first use: show, sell mode, shipping profile, flash sale, pre-offer, battle, giveaway. Lets users form a mental model |
| A9 | **Concrete values present** | 1 | [ ] | At least 3 concrete numbers that answer common questions: price range (R$5,R$5,000), character limits (60 chars title), timers (15s default), photo count (max 10), delays (14 days review). No vague "some", "a few", "shortly" |
| A10 | **No dead-ends: every article has a "next step"** | 1 | [ ] | Last section links to the next logical article in the user journey (e.g. "Once your product is listed → How to start your show") |

**SEO score: ___/10** (minimum: 7)

---

## SECTION B, GEO / AI-readability (10 points)

**Why this matters**: Fin (Intercom AI) + ChatGPT + Google's AI overviews are increasingly the first touchpoint before users even open the article. These criteria ensure the article is correctly extracted and cited.

| # | Criterion | Weight | Check | Detail |
|---|-----------|--------|-------|--------|
| B1 | **Concept statement in the first sentence** | 2 | [ ] | The article opens with a definition-style sentence: "A show is [X]", "Sell mode determines [Y]", "Shipping profile is used to [Z]". LLMs extract the first 200 words as the entity definition |
| B2 | **Front-loaded answer** | 1 | [ ] | The direct answer to the article's question appears in the first 200 words. LLMs extract ~25-30 KB max, lead with the answer, back-fill with detail |
| B3 | **Quote-ready sentences** | 1 | [ ] | At least 3 sentences that stand alone when extracted: complete subject, no orphan pronouns, no dependencies on previous context. "You can add up to 10 photos to a listing." ✓ vs "There are 10 of them." ✗ |
| B4 | **Facts density: 3+ concrete values per 1000 words** | 1 | [ ] | Limits, prices, durations, counts explicitly stated. LLMs cite pages with high facts density 5× more often. Avoid vague descriptors when a number exists |
| B5 | **Q→A structure at H2 level** | 1 | [ ] | Each H2 is either a question users would ask OR an action verb ("Set your price", "Add photos"). Body directly answers the H2 in the first paragraph |
| B6 | **Entity graph: link concepts explicitly** | 1 | [ ] | Relationships between Jamble concepts are stated: "A product belongs to a show", "A sell mode sets the price logic", "Shipping profile determines the box weight". LLMs build accurate mental models from explicit relations |
| B7 | **No ambiguous pronouns at section boundaries** | 1 | [ ] | First sentence of each H2 does not start with "It", "This", "They" referring to the previous section. Each section must be self-contained for partial extraction |
| B8 | **At least 1 visual (screenshot or code-faithful mockup)** | 1 | [ ] | Long articles get a mockup per major step. Short articles get at least 1. Visual context helps Fin confirm the article matches the user's screen (see Step 3,4 pipeline) |
| B9 | **Human-reviewed, not AI-generated** | 1 | [ ] | Final pass by a human editor. LLMs detect and deprioritize content that reads as AI-generated (repetitive sentence structure, generic filler, "Indeed, it is important to note that...") |
| B10 | **Examples use BR-realistic products** | 1 | [ ] | Examples match the actual BR market: 90% collectibles (Pokemon TCG, diecast/Hot Wheels, retro gaming), not fashion US-style (Nike, Adidas, generic apparel). "Charizard VMAX PSA 9" ✓ vs "Nike Air Max 90" ✗. In EN, keep the same BR examples for consistency across locales |

**GEO score: ___/10** (minimum: 7)

---

## SECTION C, Help Center UX (5 points bonus)

| # | Criterion | Weight | Check | Detail |
|---|-----------|--------|-------|--------|
| C1 | **Empathy sentence early** | 1 | [ ] | An acknowledgment of the user's context in the first 2 paragraphs: "We know starting your first show can feel overwhelming", "Don't worry, you can edit this later", "A common workaround is...". Optional but highly recommended |
| C2 | **Good / Bad examples pattern** | 1 | [ ] | Where relevant (titles, pricing, photos), show 2-3 good examples AND 2-3 bad examples with reasons. Teaches pattern recognition faster than abstract rules |
| C3 | **Clear "See also" / related articles section** | 1 | [ ] | End of article has a dedicated section with 2-4 related article links (not just inline mentions). Helps users complete the job |
| C4 | **Scannable: no paragraph > 4 lines** | 1 | [ ] | Long paragraphs get broken up or converted to lists. Subheadings every 100-200 words. Mobile-first density |
| C5 | **Mobile-tested before publication** | 1 | [ ] | Open the published article on a real mobile device (or Firecrawl mobile viewport screenshot). Confirm images, tables, and layout render correctly. See [04-screenshot.md](04-screenshot.md) for the Firecrawl command |

**UX score: ___/5** (bonus, no threshold)

---

## Total score

| Section | Score | Threshold |
|---------|-------|-----------|
| SEO | ___/10 | 7 minimum |
| GEO | ___/10 | 7 minimum |
| UX | ___/5 | Bonus |
| **TOTAL** | **___/25** | **14 minimum (SEO+GEO)** |

Articles that score below 14/20 should be flagged and rewritten before publication. Articles between 14 and 17 should be shipped but logged for a second-pass review.

---

## Feedback template

```
Article : [ID + title]
Locales reviewed : [pt-BR / EN]
Date review : YYYY-MM-DD
Score : SEO [X]/10 | GEO [X]/10 | UX [X]/5

Must fix before publication :
- [A/B/C][num] : [problem] → [concrete action]

Should improve (next iteration) :
- [A/B/C][num] : [opportunity] → [suggested rewrite]

Passing items :
- [list of items that pass]
```

---

## Concept statements (Jamble help center)

When writing B1 concept statements, use these canonical definitions:

- **Show**, "A show is a live session where you present and sell products to viewers in real time."
- **Sell mode**, "Sell mode determines how buyers purchase a product: through real-time offers, sudden death, or a fixed price."
- **Shipping profile**, "A shipping profile groups products by size and weight so Jamble can calculate the right shipping fee automatically."
- **Flash sale**, "A flash sale is a time-limited discount applied to a Buy It Now product during a live show."
- **Pre-offer**, "A pre-offer is a bid placed on a product before the show starts."
- **Battle**, "A battle is a live competition between two buyers bidding on the same product."

---

## BR-realistic product examples (replace fashion US examples)

Use these when writing listing examples. All examples are adapted from real Jamble BR catalog categories.

**Pokemon TCG (50% of BR GMV)**
- "Charizard VMAX Rainbow Rare - PSA 9 - Champion's Path"
- "Pokemon Booster Pack - Scarlet & Violet 151"
- "Pikachu Illustrator Holo - BGS 8.5"

**Diecast / Hot Wheels (40% of BR GMV)**
- "Hot Wheels 2024 Super Treasure Hunt - '70 Pontiac Firebird"
- "Mini GT Porsche 911 GT3 RS - Limited Edition"
- "Hot Wheels RLC Exclusive - Nissan Skyline GT-R"

**Retro gaming / collectibles (10%)**
- "Nintendo 64 Console - Complete in Box"
- "Magic: The Gathering Black Lotus - LP"
- "Funko Pop Limited Edition - Exclusive SDCC 2023"

**Never use in examples** (inconsistent with BR market):
- Nike/Adidas sneakers (not the dominant category, triggers wrong search intent)
- Generic "camiseta vintage" (too vague, not the BR Jamble customer)
- Fashion brands without specific SKU context

---

## Audit checklist (before committing a new article)

Run this 2-minute mental check before pushing a new article via the pipeline:

```
[ ] Title ≤ 60 chars, action-based, contains primary keyword
[ ] Description ≤ 140 chars
[ ] Primary query appears in H1 or first paragraph (verbatim)
[ ] First 200 words contain the direct answer
[ ] H2 headings are questions or action verbs
[ ] At least 3 concrete values (numbers, limits, timers)
[ ] Examples use BR collectibles (not fashion US)
[ ] pt-BR version is primary, EN is translation
[ ] 3+ internal links to related articles
[ ] At least 1 mockup/screenshot (Step 3-4 pipeline)
[ ] No tables that break on mobile (Step 7)
[ ] Author ID = 7980499 (Aymar)
[ ] Mobile-tested on real device or Firecrawl
```

If any checkbox fails, fix before pushing to Intercom.
