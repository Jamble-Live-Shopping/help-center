# Content audit, article 14288105 (Variants for Sellers, Sizes and Colors)

Last checked: 2026-05-11. Auditor: pipeline worker (batch real-2).

## 7 scans

| Scan | Method | Result |
|------|--------|--------|
| PII | grep email/phone/CPF in pt-br.md and en.md | OK (only generic `support@jambleapp.com` per process template) |
| Banned words | grep `auction`, `leilao` (regex case-insensitive) per `flow.yml.forbidden_terms` | OK. No "auction" or "leilao" in either file. |
| Currency (EN) | EN body must not contain `R$` | OK. The illustrative price in screen-3 EN mockup is `$ 95`; the article body in en.md mentions no currency. |
| Currency (pt-BR) | `currency_required: false` (article does not document price mechanics, mockup shows `R$ 480` as a contextual price tag only) | N/A |
| Word diet | sentences <= 25 words avg, no jargon | OK. Verb-led headings, short bullets, plain pt-BR. |
| Tone | no opener "Hey/Yo/Salut", no second-person hard-sell | OK. Article opens with "O que voce vai aprender" / "What you'll learn" per process template. |
| Alt-text quality | each `![...]()` has 15-150 chars descriptive alt, no "screenshot of" | OK. 3 alt texts, each 60-100 chars, describes the UI content with code-faithful labels. |
| Stale-feature audit | each feature mentioned still in prod | OK. All three referenced flows (`Size`/`Color` cells, `Clone Past Shows Listings`, per-listing `Quantity`) are live in iOS 2026-05-11. |

## Stale-feature audit (detail)

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|-----------------|----------------|--------|------------|-------|---------|
| Size cell (CreateProduct form) | `PRODUCT/View Models/CreateProductViewModel.swift:583-589` (getSizeSection) | mounted via `getUpdatedSectionsWithSize` when category triplet is complete | 2026-05-11 | iOS | live_in_ios |
| Color cell (CreateProduct form) | `PRODUCT/View Models/CreateProductViewModel.swift:682-692` (getColorsSection) | mounted in base sections list, isOptional | 2026-05-11 | iOS | live_in_ios |
| Quantity cell (CreateProduct form) | `PRODUCT/View Models/CreateProductViewModel.swift:591-593` (getQuantitySection) | mounted in base sections (non-Giveaway sell modes) | 2026-05-11 | iOS | live_in_ios |
| Clone Past Shows Listings action | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1705-1713` | action sheet item in `presentAddProductSheet`, opens `ShowHostImportView` | 2026-05-11 | iOS | live_in_ios |
| ProductTemplate auto-fill | `PRODUCT/View Models/CreateProductViewModel.swift:439-460` + `SERVICE/API/Repository/Modules/Product/ProductRepository.swift:73, 466-468` | fetchProductTemplate + fillProduct, called per show | 2026-05-11 | iOS | live_in_ios |
| One Size / Multi / Others color options | xcstrings + `ProductColor` server-driven catalog (`getProductAttributes` at `CreateProductViewModel.swift:1016`) | catalog served by `repository.product.getProductAttributes()`, includes "Multi" entry per v1 audit | 2026-05-11 | Backend (catalog) | live_via_api |
| Auction / Leilao wording (NOT used) | flow.yml.forbidden_terms regex | hard-fail grep enforces deprecated user-facing wording stays out | 2026-05-11 | Doc | deprecated |
| "Variant" / "Variantes" / "Variation" surface (NOT used in body claims, only in slug-mandated title) | code grep returned 0 hits in iOS source and xcstrings | NO matching surface in iOS | 2026-05-11 | iOS | does_not_exist |

## Heading hierarchy

- pt-br.md: 1 H1 (`# Variantes para Vendedores, Tamanhos e Cores`), 9 H2.
- en.md: 1 H1 (`# Variants for Sellers, Sizes and Colors`), 9 H2.

## Em-dash / en-dash

- pt-br.md: 0 em-dash (U+2014), 0 en-dash (U+2013). Verified with `grep -c $'\\u2014'`.
- en.md: 0 em-dash, 0 en-dash.

## Image refs

- pt-br.md references all 3 v3 PNGs (screen-1, screen-2, screen-3) at the canonical raw.githubusercontent.com URL.
- en.md mirrors the same 3 image refs, EN-locale variants.

## Title / description budget (metadata.yml)

- pt-BR title: `Variantes para Vendedores, Tamanhos e Cores` (45 chars, comma-only, no em-dash).
- EN title: `Variants for Sellers, Sizes and Colors` (39 chars, comma-only).
- pt-BR description: 136 chars (<=140).
- EN description: 134 chars (<=140).

## Verdict

ALL PASS on the content side, but the article carries an explicit `risk_flag` on the slug-mandated `Variantes` wording vs the iOS reality. See compliance audit for the risk + resolved_decision summary.
