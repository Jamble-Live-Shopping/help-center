# Content audit, article 14288094 (Choose Quantities When Listing Products)

Last checked: 2026-05-11. Auditor: pipeline worker (batch real-1-rerun-2 + PR #96 review).

## 2026-05-11 patch summary

PR review surfaced xcstrings source-key drift on `Pre-Bid` (kept as
source key) and `Morte subita` (unaccented). Patched article + screen-2
mockups to use xcstrings-localized user-facing values: pt-BR `Pré-oferta`
and `Morte súbita`, EN `Pre-Offer`. Sell-mode label `Real Time Offer`
also corrected from drifted `Real-time offers`. `flow.yml.forbidden_terms`
inverted-fix: removed wrongly-banned `pre-offer` / `pre-offers`, added
`regex:\bPre-Bid\b` to lock source-key leak. See code-audit for detail.

## 7 scans

| Scan | Method | Result |
|------|--------|--------|
| PII | grep email/phone/CPF in pt-br.md and en.md | OK (only generic `support@jambleapp.com` per process template) |
| Banned words | grep `auction`, `leilao`, `pre-ofertas`, `Pre-Bid` (with hyphen) in pt-br.md and en.md per flow.yml.forbidden_terms (post 2026-05-11 fix) | OK. Article uses xcstrings-localized user-facing labels: pt-BR `Oferta em tempo real` / `Pré-oferta` / `Morte súbita` / `Comprar agora`; EN `Real Time Offer` / `Pre-Offer` / `Sudden Death` / `Buy It Now`. Verbatim iOS error toast strings preserved (`prebid` one-word lowercase + `pre-oferta` pt-BR no accent are literal iOS error strings, not section titles, so they survive the hyphenated `Pre-Bid` regex ban). |
| Currency | EN body must not contain `R$` | OK (no `R$` in en.md) |
| Currency (pt-BR) | currency_required: false (article does not document price mechanics directly) | N/A |
| Word diet | sentences <= 25 words avg, no jargon | OK (verb-led headings, short bullets, plain pt-BR) |
| Tone | no opener "Hey/Yo/Salut", no second-person hard-sell | OK |
| Alt-text quality | each `![...]()` has 15-150 chars descriptive alt, no "screenshot of" | OK (3 alts, each describes the screen content with UI labels) |
| Stale-feature audit | each feature mentioned still in prod | OK (Pre-Offer / Pré-oferta toggle live, all 3 sell modes live with xcstrings-localized labels, items-left banner live in `ShowBuyItNowBannerView.swift`) |

## Stale-feature audit (detail)

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|-----------------|----------------|--------|------------|-------|---------|
| Pre-Offer / Pré-oferta toggle | `PRODUCT/Views/Components/PreBidToggleCell.swift`, `PRODUCT/View Models/CreateProductViewModel.swift:596,708` | mounted via `getBidSection`; iOS source key `Pre-Bid` resolves to xcstrings EN `Pre-Offer` / pt-BR `Pré-oferta` (user-facing) | 2026-05-11 | iOS | live_in_ios |
| Real Time Offer (AUCTION) | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:11`, xcstrings public name `Real Time Offer` (EN) / `Oferta em tempo real` (pt-BR) | enum case + xcstrings | 2026-05-11 | iOS | live_in_ios |
| Sudden Death / Morte súbita | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:13` | enum case + xcstrings EN `Sudden Death` / pt-BR `Morte súbita` (accented) | 2026-05-11 | iOS | live_in_ios |
| Buy It Now / Comprar agora | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:12`, `LIVE_SHOPPING/SaleView/View/Components/ShowBuyItNowBannerView.swift` | banner view live; xcstrings pt-BR `Comprar agora` | 2026-05-11 | iOS | live_in_ios |
| Items-left counter on banner | `LIVE_SHOPPING/SaleView/View/Components/ShowBuyItNowBannerView.swift:111-115` | label "\(n) left" / pt-BR "\(n) restantes" | 2026-05-11 | iOS | live_in_ios |
| Quantity range 1..1000 | `PRODUCT/View Models/CreateProductViewModel.swift:307-315` | maxQuantity = 1000 for AUCTION, SUDDEN_DEATH, BUY_IT_NOW | 2026-05-11 | iOS | live_in_ios |
| Pre-Offer auto-disable on quantity > 1 | `PRODUCT/View Models/CreateProductViewModel.swift:317-319,347-354` | reactive guard with shouldShowErrorToast | 2026-05-11 | iOS | live_in_ios |
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
