# Compliance Checklist, pre-offers-let-buyers-place-offers-before-your-show (Intercom 14288122)

| # | Check | Status | Notes |
|---|---|---|---|
| 1 | Title without em-dash, ≤60 chars (both locales) | PASS | pt-BR "Pré-ofertas, compradores ofertam antes do show começar" (54 ch), EN "Pre-Offers, let buyers offer before your show" (45 ch) |
| 2 | Description ≤140 chars (both locales) | PASS | pt-BR 130 ch, EN 118 ch |
| 3 | Body em-dash count = 0 (both locales) | PASS | pt-BR 0, EN 0 |
| 4 | Body en-dash count = 0 (both locales) | PASS | pt-BR 0, EN 0 |
| 5 | Body `auction` / `leilão` count = 0 (Rule 2c) | PASS | both locales 0 |
| 6 | Body `Pre-Bid` (source key) count = 0 (post-mortem rule) | PASS | both locales 0 |
| 7 | EN body `R$` count = 0 (Rule 2b) | PASS | EN 0 |
| 8 | pt-BR body `R$` present (article cites prices) | PASS | pt-BR 10 occurrences, BR-formatted |
| 9 | All mockups use `__v3` PNG suffix | PASS | 3 screens x 2 locales = 6 PNGs, all `__v3` |
| 10 | All PNGs DPR3 (≥900 px wide) | PASS | screen-1 960px, screen-2 960px, screen-3 960px |
| 11 | Step 9 framing on every image (H2 + intro + alt + caption + action) | PASS | 3/3 images on each locale |
| 12 | Alt text 15-150 chars, descriptive, keyword-aligned | PASS | range 78-121 chars |
| 13 | Source = iOS Swift code (per Rule 1) | PASS | code-audit-14288122.md, 0 MISMATCH |
| 14 | Strings match xcstrings pt-BR + EN (verbatim from source values) | PASS | Pré-oferta, Sua oferta máxima, Enviar oferta, Morte súbita, Oferta em tempo real, Ofertas ativos, Ofertas fechadas, Pre-Offer, Your max offer, Submit Offer, Sudden Death, Real Time Offer, Active Offers, Closed Offers, Minimum: %@ all confirmed |
| 15 | screen-1 has real iOS icon via `required_icons: [pre_bid_icon]` and inline SVG verbatim from `Assets.xcassets/icon/pre_bid_icon.imageset/pre_bid_icon.svg` (rule 10e Option A) | PASS | screen-1 HTMLs embed the gavel path verbatim, only fill color overridden to white per iOS `tintColor = .white` runtime |
| 16 | screen-2 and screen-3 are text-only screens with full `html_must_not_contain: ["<img", "<svg", "icon-"]` anchor (rule 10e Option B) | PASS | both screens contain 0 occurrences of `<img`, `<svg`, `icon-` (verified via grep on HTML files) |
| 17 | 3+ column tables converted to PNG (Rule 7d) | PASS | no markdown tables in body; visual comparisons rendered as mockups |
| 18 | No nested `<ul>` / `<dl>` / Intercom-incompatible HTML | PASS | markdown only, simple paragraphs + bullets |
| 19 | Both locales 1:1 mirror (only currency divergence) | PASS | section count match, paragraph count match. Currency divergences: R$ 1 / $1, R$ 5 / $1 (platform minimum), R$ 26 / $13 (mockup minimum), R$ 30 / $6, R$ 50 / $11, R$ 75 / $15 |
| 20 | metadata.yml `last_sync` updated to today | PASS | 2026-05-11T00:00:00Z |
| 21 | flow.yml source_of_truth.ios_files all exist (rule 27) | PASS | 13 paths verified with `ls $JAMBLE_IOS_ROOT/<path>` |
| 22 | flow.yml `risk_flags: []` matches metadata `state: published` (no unresolved tensions) | PASS | 0 risk flags, 0 resolved_decisions |
| 23 | No deprecated features mentioned (Verified badges, Jamble Prime, Auction wording) | PASS | none referenced in body |
| 24 | Mockups consistent with iOS source (no invented UI state) | PASS | every mockup element traces back to a CalendarProductCell / PreBidViewController / ShowHostProductCell line cited in code-audit |

**Summary: 24/24 PASS**

**Ready to merge.**
