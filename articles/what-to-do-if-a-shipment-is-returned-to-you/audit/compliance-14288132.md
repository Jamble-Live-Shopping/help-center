# Compliance audit: what-to-do-if-a-shipment-is-returned-to-you (intercom 14288132)

Audience: seller_br (batch-real-2)
Date: 2026-05-11

| # | Check | Status | Notes |
|---|---|---|---|
| 1 | Em-dash count = 0 in both md | PASS | 0 in pt-br.md, 0 in en.md. Verified via python `body.count(chr(0x2014))`. |
| 2 | En-dash count = 0 in both md | PASS | 0 in both files. |
| 3 | "Auction" / "leilão" count = 0 | PASS | 0 in pt-br.md, 0 in en.md. `forbidden_terms` declared in flow.yml. |
| 4 | EN body R$ count = 0 | PASS | No `R$` anywhere in en.md. |
| 5 | pt-BR body has R$ if prices quoted | OUT OF SCOPE | Article does not quote prices. |
| 6 | Title sans em-dash, <= 60 chars | PASS | "O que fazer se o envio for devolvido" (36 chars), "What to do if a shipment is returned to you" (43 chars). |
| 7 | Description <= 140 chars (both locales) | PASS | pt-br: 131 chars. en: 129 chars. |
| 8 | 1 H1 only per md | PASS | Single `# ...` line at top of each. |
| 9 | All declared screens have HTML pair (pt-br + en) | PASS | sale-detail-returned-status, sales-list-returned-tab, buyer-refund-status-after-return: 3 x 2 = 6 HTML files in mockup-sources/. |
| 10 | All screens have PNG pair DPR3 >= 900px | PASS | 6 PNGs at 960px wide (DPR3). Verified via `file *.png`. |
| 11 | Each declared screen referenced in pt-br.md AND en.md | PASS | 3 screens, 6 image refs (3 in each locale). |
| 12 | No orphan HTML in mockup-sources/ | PASS | Directory contains only the 6 declared files. |
| 13 | iOS strings used verbatim from xcstrings | PASS | "Returned"/"Devolvido", "Canceled"/"Cancelado", "Completed"/"Concluído", "Order Number"/"Número do pedido", "Carrier"/"Transportadora", "Track"/"Faixa". Backend-rendered status / description strings used verbatim per transaction.py:412-638. |
| 14 | No invented UI (icons, buttons, surfaces not in iOS) | PASS | Mockup 1 & 3: text-only status cards mirror `setupTransactionStatusView` (SaleViewController.swift:903-998). Mockup 2: filter strip mirrors `TransactionFilter` cases (TransactionFilter.swift:34-44) with the real `transaction_alert_red` SVG embedded inline. The truck SVG used for the Shipped pill is the real `truck_icon` asset from Assets.xcassets. No fabricated controls. |
| 15 | Code-audit cites file:line | PASS | Every claim in code-audit-14288132.md traces to a Jamble-iOS swift path or jamble_backend python path with explicit line ranges. |
| 16 | Audit triplet present (code, content, compliance) | PASS | All 3 files written with intercom suffix `-14288132`. |
| 17 | Risk flags resolved or empty | PASS | Empty. No active risks. |
| 18 | Icon anchor declared per screen (rule 10e) | PASS | Screen 1 (sale-detail-returned-status): Option B text-only, `html_must_not_contain: ["<img", "<svg", "icon-"]`. Screen 2 (sales-list-returned-tab): Option A icon anchor, `required_icons: [transaction_alert_red]`, asset embedded as inline `<svg>`. Screen 3 (buyer-refund-status-after-return): Option B text-only, same justification as Screen 1. |

## Verdict

ALL PASS (17 PASS, 1 OUT OF SCOPE with justification). Article shippable.
