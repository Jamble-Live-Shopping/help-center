# Compliance, article 14288099 (cards-and-collectibles-best-practices-for-sellers)

Date: 2026-04-27
Gate: final 12-step procedure compliance.

| Check | Status | Notes |
|-------|--------|-------|
| 01. Extraction | N/A | No ASCII boxes in v1 source, article was markdown |
| 02. Code lookup | PASS | iOS strings sourced from `CreateProductSectionType.swift`, `PackOpeningToggleCell.swift`, `xcstrings`, see `code-audit-14288099.md` |
| 03. HTML template | PASS | Four mockup pairs (pt-BR + EN = 8 files) created with brand colors (#7E53F8 customPurple, #162233 customBlack, #6B7A92 customBlue400) |
| 04. Screenshot | PASS | Puppeteer DPR3, 8 PNGs all 960px wide, all `__v2` suffix |
| 05. Hosting | PASS | PNGs at `assets/mockups/cards-and-collectibles-best-practices-for-sellers__*__v2.png` (public raw URL via GitHub) |
| 06. Intercom injection | DEFERRED | sync-intercom.yml handles this on merge to main |
| 07. Tables mobile | PASS | All v1 multi-column tables converted to bullet lists or PNG (condition guide is now a PNG, not a markdown table) |
| 08. Editorial quality | PASS | Comma-as-em-dash-replacement throughout, BR-only examples (Pokémon TCG, Hot Wheels, Funko Pop), zero fashion |
| 08b. SEO/GEO | PASS | Keywords: "trading cards", "Pokémon TCG", "condição cards", "Pack Opening", "perfil de envio Carta", "booster packs". Job-to-do H2s. FAQ Q-A format. |
| 09. Screenshot framing | PASS | Each of 4 images has H2 above + intro sentence + 15-150 char alt + caption with bolded UI elements + action continuation |
| 10. Fact-check code | PASS | `code-audit-14288099.md` = zero MISMATCH |
| 11. Fact-check content | PASS | `content-audit-14288099.md` = zero BLOCKER |
| 12. Procedure compliance | PASS | All gates green |

## Lints

- em-dashes pt-BR: 0
- en-dashes pt-BR: 0
- em-dashes EN: 0
- en-dashes EN: 0
- "auction" / "leilão": 0 in both
- "R$" in EN: 0
- "R$" in pt-BR: 2 (R$ 450,00, BR format)
- "$" in EN: 1 ($90.00, US format)
- pt-BR title length: 56 chars (≤60)
- EN title length: 50 chars (≤60)
- pt-BR description length: 119 chars (≤140)
- EN description length: 117 chars (≤140)

## Mockup verification

| Mockup | PNG dims | <900px wide? | Scrollbar visible? | Text overflow? | Visually iso pt-BR vs EN? |
|---|---|---|---|---|---|
| sample-listing | 960 x 1659 | NO | NO | NO | YES |
| condition-guide | 960 x 1644 (pt-BR), 960 x 1602 (EN) | NO | NO | NO | YES (slight height diff = pt-BR text length, layout iso) |
| photo-checklist | 960 x 1419 | NO | NO | NO | YES |
| pack-opening-toggle | 960 x 822 (pt-BR), 960 x 765 (EN) | NO | NO | NO | YES (slight height diff = pt-BR text length, layout iso) |

## Status

ALL PASS. Ready to ship.
