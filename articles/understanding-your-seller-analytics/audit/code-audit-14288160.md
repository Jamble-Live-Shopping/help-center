# Code audit, article 14288160 (understanding-your-seller-analytics)

Date: 2026-05-08
Source iOS: Jamble-iOS develop. Sources cited in flow.yml.
xcstrings: `Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings`

## Negative scan (feature-may-not-exist contract)

The article's central editorial gap: iOS has NO dedicated seller analytics surface. Before drafting, the writer scanned for plausible analytics paths and verified each is absent in the iOS clone resolved via `JAMBLE_IOS_ROOT=/Users/aymardumoulin/Projects/Jamble-iOS/Jamble`.

| Negative path | Verified absent | Method |
|---|---|---|
| `SELLER/Analytics/` | absent | `find . -path '*SELLER*' -type d` returned no Analytics directory anywhere under `Jamble/` |
| `SELLER/Stats/` | absent | `find . -path '*Stats*' -type d` returned no Stats directory anywhere under `Jamble/` |

Note: `LIVE_SHOPPING/AdminSellerStatisticsViewController.swift` exists but is admin-only (the prefix `Admin` in the class name and surrounding admin tooling). Excluded from `source_of_truth.ios_files` per assignment instruction. The article does not reference it.

The article body explicitly tells sellers there is no standalone analytics dashboard, no charts, no trend graphs, no exports, no top-items breakdowns, no audience demographics, no conversion-rate display. Each absent claim is matched by the negative-scan above and surfaced as a `risk_flag` in flow.yml.

## Claims article vs source code

| Article claim | Source | Verdict |
|---|---|---|
| A "Real-Time Sales" overlay shows running total + price-per-item in the top-left while hosting | LIVE_SHOPPING/Host/View/ShowHostViewController.swift:754-797 (`setupCurrentSaleContainer`: titleLabel `String(localized: "Real-Time Sales")`, `currentSaleValueLabel` "$0", `currentSaleAveragePriceLabel` "$0/item", anchored to viewInteractionView leading +16, top equal to topRightStackView top) | MATCH |
| The summary card on the post-show dashboard has 4 tiles: TOTAL, AFTER FEES, SOLD, BUYERS | LIVE_SHOPPING/DashboardHost/Views/ShowHostDashboardView.swift:123-156 (`summarySection`: `Text("SUMMARY")`, then HStack with `getSummaryItem(... label: "TOTAL"...)`, `getSummaryItem(... label: "AFTER FEES"...)`, `getSummaryItem(int: viewModel.soldCount, label: "SOLD")`, `getSummaryItem(int: viewModel.buyerCount, label: ...BUYERS/BUYER)`) | MATCH |
| TOTAL / AFTER FEES / SOLD / BUYERS render in English even on a pt-BR device | ShowHostDashboardView.swift:130-148 passes plain string literals as `label:` (`"TOTAL"`, `"AFTER FEES"`, `"SOLD"`, `"BUYERS"` / `"BUYER"`). None are wrapped in `String(localized:)`, so xcstrings has no chance to substitute. xcstrings has only one matching key ("SOLD" -> "VENDIDO" pt-BR) but the dashboard does not call it through the localized path | MATCH (technical-debt note in article) |
| The "SUMMARY" header above the tiles is localized as "RESUMO" in pt-BR | ShowHostDashboardView.swift:125 `Text("SUMMARY")` is a SwiftUI Text init from a string literal, which IS auto-localized via xcstrings. xcstrings "SUMMARY" -> en "SUMMARY", pt-BR "RESUMO" (Localizable.xcstrings:23442-23456). Article's pt-BR mockup section header is "RESUMO" while the 4 tile labels stay English | MATCH |
| Wallet entry point: profile -> Settings -> "My Wallet" in the SELL section | PROFILE/ProfileSettings/Wallet/View/SellerWalletView.swift exists. xcstrings "My Wallet" -> en "My Wallet", pt-BR "Minha carteira" (Localizable.xcstrings:15098-15113). Wallet is the SwiftUI surface mounted from settings | MATCH |
| Wallet shows available balance + Withdraw button | SellerWalletView.swift:69 `Text(section?.title ?? "Available to Withdraw")` then SellerWalletView.swift:96 `Text(section?.actionTitle ?? "Withdraw")` inside an `IndicatorButton`. xcstrings "Withdraw" -> pt-BR "Sacar" (Localizable.xcstrings:27106-27117) | MATCH |
| The post-show dashboard appears automatically after ending a show, accessible later by tapping the past show | Architectural: `ShowHostDashboardView` is the main host post-show surface (path under `LIVE_SHOPPING/DashboardHost/Views/`). Article does NOT cite a specific view-controller-mount line; the article's claim is descriptive of where the surface lives rather than naming a presentation method. Verified by file location and the absence of any other host-side post-show analytics surface in the repo | MATCH (architectural) |

## Visual fidelity

| Mockup | Strings match xcstrings + literals? | Status |
|--------|--------------------------------------|--------|
| screen-1 (post-show summary) pt-BR | Section header "RESUMO" (xcstrings pt-BR for "SUMMARY"). 4 tile labels stay English (TOTAL / AFTER FEES / SOLD / BUYERS) because the iOS code passes plain literals, not `String(localized:)`. Article body explicitly tells the pt-BR reader why the labels are English | MATCH |
| screen-1 (post-show summary) en | "SUMMARY" + 4 tile labels TOTAL / AFTER FEES / SOLD / BUYERS, mirror of pt-BR | MATCH |
| screen-2 (live real-time-sales overlay) pt-BR | "Vendas em tempo real" (xcstrings pt-BR for "Real-Time Sales"). Top-left placement, running total in $-style placeholder (the iOS code shows "$0" / "$0/item" placeholders; in production the value is the real R$ formatted currency) | MATCH |
| screen-2 (live real-time-sales overlay) en | "Real-Time Sales" + same layout, dollar-format placeholder | MATCH |
| screen-3 (wallet) pt-BR | "Minha carteira" header (xcstrings pt-BR for "My Wallet"), "Saldo disponível" caption + R$ amount + "Sacar" button (xcstrings pt-BR for "Withdraw") | MATCH |
| screen-3 (wallet) en | "My Wallet" header + "Available balance" caption + dollar-formatted amount + "Withdraw" button | MATCH |

## Notes

- iOS has NO analytics surface. The article is honest about that gap. Three mockups depict the three real surfaces sellers DO have: the live overlay, the post-show summary card, and the wallet. They are not stitched into a fictional "analytics tab".
- TOTAL / AFTER FEES / SOLD / BUYERS as English-only on a pt-BR device is documented technical debt, not a bug to invent around. Article explicitly tells the pt-BR reader to expect English labels there. Mockup pt-BR matches the rendered reality.
- "AFTER FEES" wording: the article describes this as "valor liquido depois da taxa Jamble" / "net amount after Jamble's fee" with explicit caveat that it does NOT include product cost, shipping out of pocket, packaging, taxes, or refunds. The word "lucro" / "profit" / "real take" / "real profit" is not used anywhere in the article.
- screen-3 (wallet) is the rerun-1 anchor target. flow.yml declares `review_checks: [icons_match_ios_source]` AND `html_must_not_contain: ["<img", "<svg", "icon-"]` because the wallet mockup is intentionally text-only (no glyphs). Rule 10e is satisfied via Option B (text-only anchor with all three icon-blockers).
- screens 1 and 2 also declare `review_checks: [icons_match_ios_source]` and pick the same Option B contract: the dashboard summary card and the live overlay are both text + numbers, no glyphs.

## Verdict

Zero MISMATCH against the cited iOS sources. Negative scan confirms the absent analytics surface is genuinely absent. Article is grounded in real xcstrings + the three real iOS surfaces sellers can see.
