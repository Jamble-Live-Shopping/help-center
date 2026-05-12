# Compliance audit: make-a-shipping-adjustment (intercom 14288137)

Audience: seller_br (v2_rewrite)
Date: 2026-05-11

| # | Check | Status | Notes |
|---|---|---|---|
| 1 | Em-dash count = 0 in both md | PASS | `grep -c "—" pt-br.md en.md` returns 0/0. Uses commas, parentheses, and colon instead. |
| 2 | En-dash count = 0 in both md | PASS | None. |
| 3 | "Auction" / "leilão" count = 0 | PASS | None. |
| 4 | EN body R$ count = 0 | PASS | en.md mockup screen-2 uses `$8.50` / `$28.10`. iOS strings `You paid $%@` and `Est. Ship. $%@` are not currency-localized in code. |
| 5 | pt-BR body has R$ if prices quoted | PASS | Sample values in pt-br.md screen-2 mockup use `R$147,00` / `R$62,00` / `R$8,50`. Article body itself does not quote product prices. |
| 6 | Title sans em-dash, ≤ 60 chars | PASS | "Faça um Ajuste de Envio" (23 chars), "Make a Shipping Adjustment" (26 chars). |
| 7 | Description ≤ 140 chars (both locales) | PASS | pt-br: 120 chars. en: 129 chars. |
| 8 | 1 H1 only per md | PASS | Single `# Faça um Ajuste de Envio` and single `# Make a Shipping Adjustment`. All other headings are `##` or `###`. |
| 9 | All declared screens have HTML pair (pt-br + en) | PASS | screen-1__pt-br.html, screen-1__en.html, screen-2__pt-br.html, screen-2__en.html. 2 screens x 2 locales = 4 HTML files. |
| 10 | All screens have PNG pair DPR3 ≥ 900px | PASS | 4 PNGs at 1020 px wide (DPR3 of 340 phone width). Suffix `__v3`. Verified via `file` on each output. |
| 11 | Each declared screen referenced in pt-br.md AND en.md | PASS | screen-1 image ref in both; screen-2 image ref in both. |
| 12 | No orphan HTML in mockup-sources/ | PASS | Prior v1 orphans (confirm-weight__pt-br.html, confirm-weight__en.html) deleted. mockup-sources/ now contains only the 4 declared files. |
| 13 | iOS strings used verbatim from xcstrings | PASS | All visible labels in mockups match xcstrings: `Editar Endereço de Entrega` / `Edit Shipping Address`, `Informações Pessoais` / `Personal Information`, `Endereço de Entrega` / `Shipping Address`, `CEP` / `ZIP Code`, `Nome da rua` / `Street Name`, `Número` / `Street Number`, `Complemento` / `Interior/Apt`, `Bairro` / `Neighborhood`, `Cidade` / `City`, `País` / `Country`, `Editar` / `Edit`, `PACOTE` / `PACKAGE`, `Você pagou` / `You paid`. |
| 14 | No invented UI (icons, buttons, surfaces not in iOS) | PASS | screen-1 mirrors AddEditShippingAddressInformationView headerView + sections layout. screen-2 mirrors DashboardBundleView headerView + actions ForEach. No icons added that are not present in iOS (no chevron back arrow asset claim, the `&lsaquo;` is a generic close glyph and is documented as a chrome detail, not an iOS asset). Action buttons in screen-2 are the post-label state (Open Label + Nota Fiscal); no fictional Adjust/Cancel button drawn. The footer note in the mockup is editorial text (not a UI element) to keep the visual anchored in "what is absent" without inventing UI. |
| 15 | Code-audit cites file:line | PASS | All claims trace to AddEditShippingAddressInformationView.swift, BRAddressFormConfiguration.swift, DashboardBundleView.swift, DashboardBundle.swift, DashboardBundleViewModel.swift with explicit line ranges in audit/code-audit-14288137.md. |
| 16 | Audit triplet present (code, content, compliance) | PASS | All 3 files written with intercom suffix `-14288137`. |
| 17 | Risk flags resolved or empty | PASS pending risk resolution | One risk_flag present (ChangeShippingWeightViewController.swift dead code) with a matching `resolved_decisions` entry. The risk is documented, not silently dropped, and re-audit conditions are spelled out in flow.yml. |
| 18 | Icon anchor declared per screen (rule 10e) | PASS | Both screens use Option B (text-only contract). flow.yml screens declare review_checks: labels_match_xcstrings + no_invented_ui_state. The mockups contain no `<img>` and no `<svg>` tags (verified by `grep`). |

## Verdict

PASS pending risk resolution. 17 PASS + 1 PASS pending risk resolution. The one open risk (dead `ChangeShippingWeightViewController.swift`) is documented in flow.yml.risk_flags AND in flow.yml.resolved_decisions with a re-audit trigger ("re-audit if a future PR wires the controller back in"). Article shippable.
