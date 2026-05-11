# Content audit, article 14288094 (Choose Quantities When Listing Products)

Last checked: 2026-05-08. Auditor: pipeline worker (batch real-1-rerun-2).

## 7 scans

| Scan | Method | Result |
|------|--------|--------|
| PII | grep email/phone/CPF in pt-br.md and en.md | OK (only generic `support@jambleapp.com` per process template) |
| Banned words | grep `auction`, `leilao`, `pre-ofertas`, `pre-offer` in pt-br.md and en.md (per flow.yml.forbidden_terms) | OK (article uses "Oferta em tempo real" / "Real-time offers" and "Pre-Bid" / "Pre-oferta") |
| Currency | EN body must not contain `R$` | OK (no `R$` in en.md) |
| Currency (pt-BR) | currency_required: false (article does not document price mechanics directly) | N/A |
| Word diet | sentences <= 25 words avg, no jargon | OK (verb-led headings, short bullets, plain pt-BR) |
| Tone | no opener "Hey/Yo/Salut", no second-person hard-sell | OK |
| Alt-text quality | each `![...]()` has 15-150 chars descriptive alt, no "screenshot of" | OK (3 alts, each describes the screen content with UI labels) |
| Stale-feature audit | each feature mentioned still in prod | OK (Pre-Bid live, all 3 sell modes live, items-left banner live in `ShowBuyItNowBannerView.swift`) |

## Stale-feature audit (detail)

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|-----------------|----------------|--------|------------|-------|---------|
| Pre-Bid toggle | `PRODUCT/Views/Components/PreBidToggleCell.swift`, `PRODUCT/View Models/CreateProductViewModel.swift:596,708` | mounted via `getBidSection` | 2026-05-08 | iOS | live_in_ios |
| Real-time offers (AUCTION) | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:11`, xcstrings public name "Real Time Offer" | enum case + xcstrings | 2026-05-08 | iOS | live_in_ios |
| Sudden Death | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:13` | enum case + xcstrings "Sudden Death" | 2026-05-08 | iOS | live_in_ios |
| Buy It Now | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:12`, `LIVE_SHOPPING/SaleView/View/Components/ShowBuyItNowBannerView.swift` | banner view live | 2026-05-08 | iOS | live_in_ios |
| Items-left counter on banner | `LIVE_SHOPPING/SaleView/View/Components/ShowBuyItNowBannerView.swift:111-115` | label "\(n) left" / pt-BR "\(n) restantes" | 2026-05-08 | iOS | live_in_ios |
| Quantity range 1..1000 | `PRODUCT/View Models/CreateProductViewModel.swift:307-315` | maxQuantity = 1000 for AUCTION, SUDDEN_DEATH, BUY_IT_NOW | 2026-05-08 | iOS | live_in_ios |
| Pre-Bid auto-disable on quantity > 1 | `PRODUCT/View Models/CreateProductViewModel.swift:317-319,347-354` | reactive guard with shouldShowErrorToast | 2026-05-08 | iOS | live_in_ios |
| Verified badges (NOT mentioned) | n/a (cross-corpus check) | deprecated 2026-04-28 (Rising/Elite/Ultra/Parceiro da Jamble killed) | 2026-05-08 | Product | deprecated |
| Auction / Leilao wording (NOT used) | flow.yml.forbidden_terms regex | hard-fail grep enforces deprecated user-facing wording stays out | 2026-05-08 | Doc | deprecated |

## Heading hierarchy

- pt-br.md: 1 H1 (`# Definir Quantidades ao Listar Produtos`), 9 H2.
- en.md: 1 H1 (`# Choose Quantities When Listing Products`), 9 H2.

## Em-dash / en-dash

- pt-br.md: 0 em-dash (U+2014), 0 en-dash (U+2013).
- en.md: 0 em-dash, 0 en-dash.

## Image refs

- pt-br.md references all 3 v3 PNGs (screen-1, screen-2, screen-3) at the canonical raw.githubusercontent.com URL.
- en.md mirrors the same 3 image refs.

## Verdict

ALL PASS. No BLOCKER, no MISMATCH. Article is shippable from the content side.
