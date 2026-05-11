# Compliance audit: how-order-cancellations-work (intercom 14288126)

Audience: buyer_br (rerun-2)
Date: 2026-05-08

| # | Check | Status | Notes |
|---|---|---|---|
| 1 | Em-dash count = 0 in both md | PASS | Uses commas / parentheses instead. |
| 2 | En-dash count = 0 in both md | PASS | None. |
| 3 | "Auction" / "leilão" count = 0 | PASS | None. |
| 4 | EN body R$ count = 0 | PASS | No prices quoted. |
| 5 | pt-BR body has R$ if prices quoted | OUT OF SCOPE | Article does not quote prices. |
| 6 | Title sans em-dash, ≤ 60 chars | PASS | "Como funcionam os cancelamentos de pedidos" (43 chars), "How order cancellations work" (28 chars). |
| 7 | Description ≤ 140 chars (both locales) | PASS | pt-br: 123 chars. en: 111 chars. |
| 8 | 1 H1 only per md | PASS | Single `# ...` line at top of each. |
| 9 | All declared screens have HTML pair (pt-br + en) | PASS | order-detail-cancel-button, cancel-order-bulletin-sheet, order-canceled-refund-status: 3 x 2 = 6 HTML files. |
| 10 | All screens have PNG pair DPR3 ≥ 900px | PASS | 6 PNGs rendered via `scripts/shot-retina.mjs`, suffix `__v3`. |
| 11 | Each declared screen referenced in pt-br.md AND en.md | PASS | 3 screens, 6 image refs (3 in each). |
| 12 | No orphan HTML in mockup-sources/ | PASS | rerun-1 orphans deleted (cancel-reason-picker, cancel-sale-confirmation, cancel-sale-dialog, cancellation-reason-picker). Mockup-sources contains only the 6 declared files. |
| 13 | iOS strings used verbatim from xcstrings | PASS | "Cancel Order"/"Cancelar pedido", "Cancel this order"/"Cancelar este pedido", "Yes, I cancel"/"Sim, eu cancelo", "No, back"/"Não, voltar", description text. All match xcstrings. |
| 14 | No invented UI (icons, buttons, surfaces not in iOS) | PASS | Cancel button is text-only per PurchaseViewController.swift:657-672; BLTN sheet is text-only per :1068-1137. No icons added. Status card has only text labels + step bar (drawn as CSS divs to mirror `AWStepBar`). |
| 15 | Code-audit cites file:line | PASS | All claims trace to PurchaseViewController.swift or transaction.py with explicit line ranges. |
| 16 | Audit triplet present (code, content, compliance) | PASS | All 3 files written with intercom suffix `-14288126`. |
| 17 | Risk flags resolved or empty | PASS | Empty. No active risks. |
| 18 | Icon anchor declared per screen (rule 10e) | PASS | All 3 screens use Option B (text-only contract): `html_must_not_contain: ["<img", "<svg", "icon-"]`. iOS source confirms no icons on the buyer cancel surface. |

## Verdict

ALL PASS (17 PASS, 1 OUT OF SCOPE with justification). Article shippable.
