# Content Audit, buy-it-now-sell-at-a-fixed-price (seller, intercom 14288112)

Date: 2026-05-08

## Job-to-be-done coverage

The article is contracted to help sellers (1) list items at a fixed buy-it-now price, (2) understand when to use Buy It Now versus the timed sell mode, and (3) set the price. The body covers the three explicitly:

| JTBD beat | Where it lives in pt-br.md | Where it lives in en.md |
|---|---|---|
| List at a fixed BIN price | "Como funciona o modo Comprar agora" + Steps 1-4 | "How Buy It Now works" + Steps 1-4 |
| When to use BIN vs Real Time Offer | "Quando usar Comprar agora" comparison table | "When to use Buy It Now" comparison table |
| How to set the price | Step 2 (R$ 5 to R$ 5.000 range, pricing dica) + "Dicas para o preço" | Step 2 ($5 to $5,000 range, pricing tip) + "Pricing tips" |

## Stale-feature audit

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| BUY_IT_NOW sale type | `ShowSaleType.swift:11` | Active in develop | 2026-05-08 | aymar | live_in_ios |
| Real Time Offer label (xcstrings rename of "Auction") | `Localizable.xcstrings` "Auction" entry, en="Real Time Offer", pt-BR="Oferta em tempo real" | Active in develop | 2026-05-08 | aymar | live_in_ios |
| Sudden Death sale type | `ShowSaleType.swift:13` + xcstrings "Sudden Death" pt-BR="Morte súbita" | Active in develop | 2026-05-08 | aymar | live_in_ios |
| Flash Sale toggle on BIN only | `SellModeDefaultCell.swift:206-233` (BIN branch) + `SellModeToogleView.swift` | Active in develop | 2026-05-08 | aymar | live_in_ios |
| Flash Sale 10-90% discount range | `SellModeDefaultCell.swift:224` minValue 10, maxValue 90 | Active in develop | 2026-05-08 | aymar | live_in_ios |
| Flash Sale 5-300s duration range | `SellModeDefaultCell.swift:227` minValue 5, maxValue 300 | Active in develop | 2026-05-08 | aymar | live_in_ios |
| Pre-offers blocked on BIN | `ShowSaleType.swift:73-80` `canPrebid` excludes BUY_IT_NOW | Active in develop | 2026-05-08 | aymar | live_in_ios |
| ShowBuyItNowBannerView purple normal variant | `ShowBuyItNowBannerView.swift:90-91` bg.brand 16% alpha | Active in develop | 2026-05-08 | aymar | live_in_ios |
| ShowBuyItNowBannerView green flash variant | `ShowBuyItNowBannerView.swift:90-91` flashSaleGreen 16% alpha | Active in develop | 2026-05-08 | aymar | live_in_ios |
| BRL price floor R$ 5 / ceiling R$ 5.000 | `Price.swift:206-219` BRL minPrice=5.0, maxPrice=5000.0 | Active in develop | 2026-05-08 | aymar | live_in_ios |
| Giveaway sale type (out of scope here) | `ShowSaleType.swift:14` | Active in develop | 2026-05-08 | aymar | live_in_ios |
| Marketplace post-show label (not surfaced) | `ProductType.swift:17` `buyItNow.title = "Marketplace"` | Active in develop | 2026-05-08 | aymar | live_in_ios |

## Forbidden terms scan (deterministic)

- `auction` (regex `\bauction\b`): 0 hits in pt-br.md, 0 hits in en.md
- `leilão` / `leilao` (regex `\bleil[aã]o\b`): 0 hits in pt-br.md, 0 hits in en.md
- `Compra Direta` (legacy Help Center title, banned because xcstrings now uses "Comprar agora"): 0 hits in pt-br.md, 0 hits in en.md

## Soft warns reviewer should still eyeball

- The article keeps the USD floor at $5 in en.md for parity with the BR storyline, even though `Price.swift:206` puts USD min at $1. Reasoned in code-audit-14288112.md.
- Step 3 mentions Flash Sale numeric ranges (10-90%, 5-300s) directly inline. Confirm these are not yet in any active product gate or experiment that could change them mid-quarter.

## Verdict

Article matches the iOS source surface and the JTBD. No active risk_flags. Ready to ship.
