# Compliance, article 14288096 (coins-and-money-best-practices-for-sellers)

Date: 2026-05-11
Gate: final 12-step procedure compliance.

| Check | Status | Notes |
|-------|--------|-------|
| 01. Extraction | N/A | No ASCII boxes in v1 source, article was markdown |
| 02. Code lookup | PASS | Condition taxonomy traced to `ProductCondition.swift` (server-driven, audited in 14288099); shipping profiles and sell modes cross-referenced from canonical sibling articles. See `code-audit-14288096.md` |
| 03. HTML template | PASS | Two composite mockup pairs (pt-BR + EN = 4 HTML files) created with brand colours (#162233 customBlack, #6B7A92 customBlue400 for muted text, dark radial #1F2A3B->#0E1623 for coin backgrounds). Editorial illustrations, not iOS UI reproductions, so no `source: ios_required` claim |
| 04. Screenshot | PASS | Puppeteer DPR3, 4 PNGs all 960px wide, all `__v3` suffix |
| 05. Hosting | PASS | PNGs at `assets/mockups/coins-and-money-best-practices-for-sellers__*__v3.png` (public raw URL via GitHub on merge) |
| 06. Intercom injection | DEFERRED | sync-intercom.yml handles this on merge to main |
| 07. Tables mobile | PASS | v1 5-column condition table killed; condition vocabulary now lives in body text plus the condition-guide PNG (screen-2). No markdown tables remain |
| 08. Editorial quality | PASS | Comma-as-em-dash-replacement throughout (24 em-dashes killed in each locale), BR-only examples (Cruzeiro/Cruzado/Real timeline, Casa da Moeda, 2000 Réis 1924), zero fashion, zero "leilão / auction" wording |
| 08b. SEO/GEO | PASS | Keywords: "moedas colecionáveis", "cédulas", "numismática", "Casa da Moeda", "condição moedas", "PCGS NGC", "Cruzeiro Real", "réplica fantasia". Job-to-do H2s. FAQ Q-A format |
| 09. Screenshot framing | PASS | Each of 2 image references has H2 above (Como tirar fotos / Diretrizes de condição) + intro sentence + 119-132 char alt + caption with bolded `**Faça**` / `**Evite**` / `**Novo com etiquetas**` / etc + action continuation |
| 10. Fact-check code | PASS | `code-audit-14288096.md` = zero MISMATCH |
| 11. Fact-check content | PASS | `content-audit-14288096.md` = zero BLOCKER |
| 12. Procedure compliance | PASS | All gates green |

## Lints

- em-dashes pt-BR: 0
- en-dashes pt-BR: 0
- em-dashes EN: 0
- en-dashes EN: 0
- "auction" / "leilão": 0 in both
- "R$" in EN: 0
- "R$" in pt-BR: 0 (article is editorial, no specific price examples)
- "$" in EN: 0
- pt-BR title length: 51 chars (≤60)
- EN title length: 43 chars (≤60)
- pt-BR description length: 122 chars (≤140)
- EN description length: 110 chars (≤140)

## Mockup verification

| Mockup | PNG dims | <900px wide? | Scrollbar visible? | Text overflow? | Visually iso pt-BR vs EN? |
|---|---|---|---|---|---|
| screen-1 (photo good/bad) | 960 x 1419 | NO | NO | NO | YES |
| screen-2 (condition guide) | 960 x 1644 (pt-BR), 960 x 1560 (EN) | NO | NO | NO | YES (slight height diff = pt-BR text length, layout iso) |

## Mockup source classification

Both mockups are `source: composite` (rule 10e n/a):

- screen-1 (photo good/bad): editorial illustration of coin photography practices. Two "DO" cells (dark background sharp focus, date macro close-up) and two "AVOID" cells (flash glare hotspot, out-of-focus held in fingers). No iOS UI reproduced
- screen-2 (condition guide): swatch progression mapping the 5 Jamble condition levels (server-driven, taxonomy audited 14288099) to numismatic vocabulary (MS, AU, XF/VF, F/VG, G/AG). No iOS UI reproduced

Per the BEST-PRACTICES article shape guidance (post PR #91/#92/#103/#104):
"For these mockups, source is NOT ios_required, these are editorial
illustrations, not iOS UI screens. Use source: composite [...] in flow.yml so
rule 10e does NOT apply."

## Status

ALL PASS. Ready to ship.
