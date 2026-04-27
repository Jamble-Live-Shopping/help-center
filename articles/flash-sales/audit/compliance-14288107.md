# Compliance report, article 14288107 (flash-sales)

**Status**: PASS

Run date: 2026-04-27
Branch: `update/flash-sales-v2-revamp`
Slug: `flash-sales`

## Master checklist (17 checks)

| # | Step | Check | Status | Detail |
|---|------|-------|--------|--------|
| 1 | 1 | No ASCII boxes pending in source `.md` | PASS | All v1 markdown table content converted to PNG mockup |
| 2 | 2 | Code-audit file exists with iOS source citations | PASS | `audit/code-audit-14288107.md`, 8 Swift files referenced |
| 3 | 3 | Each mockup exists in both `__pt-br.html` and `__en.html` | PASS | 4 pairs: flash-sales-config, flash-sale-mode-picker, flash-sale-product-card, pricing-chart |
| 3b | 3 | pt-BR and EN files have iso structure | PASS | Style/SVG identical, only text differs |
| 3c | 3 | No emoji used as UI icons | PASS | All icons inline SVG |
| 4 | 4 | Every HTML has matching PNG at width >= 900px (DPR3) | PASS | All 8 PNGs rendered with `shot-retina.mjs`, 960px wide |
| 4b | 4 | PNGs at root `assets/mockups/`, not under `articles/<slug>/assets/` | PASS | All under `assets/mockups/flash-sales__*__v2.png` |
| 4c | 4 | Every NEW PNG has `__v2` suffix | PASS | All 8 PNGs end in `__v2.png` |
| 5 | 5 | `metadata.yml` parses as YAML, has non-empty `locales:` | PASS | pt-br + en entries valid |
| 6 | 6 | Zero ASCII boxes / pre-code blocks in body | PASS | Only headings, paragraphs, bullets, images |
| 6b | 6 | Every image has descriptive 15-150 char alt text, unique | PASS | 4 images x 2 locales, alts 92-148 chars |
| 6c | 6 | `author_id == 7980507` per metadata.yml | PASS | matches existing |
| 7 | 7 | Zero markdown tables remain (was 4-col pricing table) | PASS | Replaced by `pricing-chart` PNG mockup |
| 8a | 8 | `len(description) <= 140` for both locales | PASS | pt-BR=131, EN=129 |
| 8b | 8 | Zero em-dashes and en-dashes in body, title, desc, alt | PASS | grep count = 0 |
| 8c | 8 | No banned brand examples (Nike, Adidas, Camiseta) | PASS | v1 Nike replaced by Pikachu Holo PSA 9 |
| 8e | 8 | No `auction`/`leilão`, no `commission`/`comissão`, no `4%`/`10%` exact, no `taxa de saque` | PASS | regex check 0 hits both locales |
| 9 | 10 | `code-audit-14288107.md` exists, zero open MISMATCH | PASS | All 23 claims verified MATCH |
| 10 | 11 | `content-audit-14288107.md` exists, zero BLOCKER | PASS | 6 scans clean |
| 11 | 12 | This file exists with ALL PASS | PASS | Self-referential, ALL checks PASS |

## Visual fidelity verification (manual via Read tool)

| PNG | DPR3 width | UI strings correct locale | Verdict |
|---|---|---|---|
| flash-sales-config__pt-br | 960px | "Modo de venda", "Compre agora", "Venda relâmpago", "Desconto (%)", "Duração (segundos)", "R$ 200,00" | PASS |
| flash-sales-config__en | 960px | "Sell mode", "Buy It Now", "Flash sale", "Discount (%)", "Timer (Seconds)", "$200.00" | PASS |
| flash-sale-mode-picker__pt-br | 960px | "Começar como uma venda rápida ou comprar agora?", "Venda relâmpago", "Comprar agora", "Mais tarde" | PASS |
| flash-sale-mode-picker__en | 960px | "Start as a Flash Sale or Buy It Now?", "Flash Sale", "Buy It Now", "Later" | PASS |
| flash-sale-product-card__pt-br | 960px | "Venda relâmpago • 30% OFF", "3 restantes", "R$ 200,00" struck, "R$ 140,00" lime, "0:42", "Compre agora: R$ 140,00" | PASS |
| flash-sale-product-card__en | 960px | "Flash Sale • 30% OFF", "3 left", "$200.00" struck, "$140.00" lime, "0:42", "Buy Now: $140.00" | PASS |
| pricing-chart__pt-br | 960px | "Quanto você ganha", "ORIGINAL / DESC. / COMPRADOR PAGA / VOCÊ RECEBE", BR-format prices | PASS |
| pricing-chart__en | 960px | "How much you earn", "ORIGINAL / OFF / BUYER PAYS / YOU EARN", US-format prices | PASS |

## Final ship gate

ALL 17 checks PASS. Visual fidelity confirmed on all 8 PNGs.

Ready for admin-merge.
