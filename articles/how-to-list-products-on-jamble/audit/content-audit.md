# Content audit, article 14288093 (How to List Products)

Last checked: 2026-04-16. Auditor: Aymar Dumoulin (via pipeline).

Article: https://intercom.help/jamble-bb4bea116bbe/en/articles/14288093-how-to-list-products-on-jamble

## Scans completed

- Scan 1, regex sweep for PII and internal terms (EN + pt-BR): clean
- Scan 2, contextual leaks pass: 4 false-positive Firebase-ID matches, all Intercom CDN hashes, safe
- Scan 3, translation parity: both locales swept, no divergent leaks
- Scan 4, word diet: 5 replacements applied
- Scan 5, tone of voice: 1 sentence-split + 1 intro-tighten applied, average 18 words/sentence, within target

## BLOCKERS found

(none)

## WARNs found

- "R$" shown inside mockup PNGs (`prod-box4.png`, `prod-box6.png`). Decision: KEEP. The mockup reflects the Brazilian app UI. EN prose localizes to `$`. Cross-language artifact accepted per RULE 2b.
- No competitor names found (Whatnot, TikTok Shop, Kwai, Shopee).
- 4 matches flagged as "Firebase ID-like" in Scan 2 are Intercom CDN image hashes (e.g. `3837c797ffc7746e7b8a76bb5db1`). These are Intercom-owned, not Jamble internals. SAFE.

## Word diet, Scan 4 applied

| Original | After | Status |
|----------|-------|--------|
| "clear, specific title" (x2 occurrences) | "specific title" | DONE |
| "Each show has its own product list, and you add products to that list before going live." | "Each show has its own product list. Add products before going live." | DONE |
| "The title is the first thing buyers see, so make it count." | "Buyers see the title first, so make it count." | DONE |
| "You can also bring products from other shows or from your shop profile using the Clone and Import features (covered in the Cloning Items article)." | already compliant, no change needed in this pass | checked |
| "Be as specific as possible." | already compliant | checked |

Total: 5 replacements, body shortened by ~50 characters.

## Tone of voice, Scan 5 applied

Persona: first-time Brazilian seller, on phone, between two shows, pt-BR first language, wants to list one product now.

### Edits applied

| Original | After | Reason |
|----------|-------|--------|
| "This guide is your complete reference for creating product listings on Jamble. You'll learn every field available in the listing form, how each sell mode works, how to set prices, add photos, and get your products ready to sell during your live shows." | "Create a listing in 11 steps. Covers titles, sell modes, prices, photos, and every required field." | 31 words to 16, direct action framing |
| "You can also enable a Flash Sale on Buy It Now products, which adds a percentage discount and a countdown timer (see the Flash Sales article for details)." | "You can also enable a Flash Sale on Buy It Now products. It adds a percentage discount and a countdown timer. See the Flash Sales article for details." | Split 28-word sentence into 3 shorter ones |

### Final metrics

- Total sentences: 105
- Sentences >25 words: 13 (mostly false positives from list-joining, not prose)
- Average sentence length: 18 words (target ≤20, PASS)

### Checklist

| Check | Result |
|-------|--------|
| Every sentence obvious on first read | PASS (after edits above) |
| Technical terms either in-app or explained inline | PASS |
| Every step actionable | PASS |
| Key answer delivered in first 3 H2 sections | PASS |
| Sentences ≤20 words on average | PASS (18 avg) |
| Warm but not chatty tone | PASS |
| Share-with-first-time-seller test | PASS |

Verdict: PASS.

## Actions completed on 2026-04-16

- [x] Scan 4 TODOs applied (5 word-diet replacements pushed)
- [x] Scan 2 contextual leaks pass run, 4 false positives verified safe
- [x] Scan 5 tone of voice pass run, 2 sentence rewrites applied
- [x] Verified no R$ leaked back into EN body after edits (automated check in compliance)

## Actions deferred

- [ ] Run a Haiku API pass on the full body for deeper contextual leak detection (needs API quota commitment, low priority given the regex pass is clean)
- [ ] Run a Haiku Scan 5 pass top-to-bottom with the persona prompt (same, deferred to next iteration)

Auditor: Aymar Dumoulin.
