# Compliance, article 14288106 (listing-guidelines)

Date: 2026-04-27
Gate: final 12-step procedure compliance.

| Check | Status | Notes |
|-------|--------|-------|
| 01. Extraction | N/A | No ASCII boxes in v1, article was 100% prose |
| 02. Code lookup | PASS | iOS form labels sourced from `CreateProductSectionType.swift` + xcstrings pt-BR; report flow confirmed in `ProductViewController.swift` |
| 03. HTML template | PASS | 3 mockups x 2 locales = 6 HTML files; phone width 340px, system fonts, no external assets |
| 04. Screenshot | PASS | Puppeteer DPR3 render; 6 PNGs at 1020px wide (good listing 1608h, bad listing 1518h, photo do/dont 921h) |
| 05. Hosting | PASS | PNGs at `assets/mockups/listing-guidelines__*__v2.png`, served via raw.githubusercontent.com |
| 06. Intercom injection | DEFERRED | sync-intercom.yml handles this on merge to main |
| 07. Tables mobile | N/A | No multi-column data tables in body |
| 08. Editorial quality | PASS | Job-to-do H2s, BR collectibles examples (Pokémon TCG, Hot Wheels), zero fashion references |
| 08b. SEO/GEO | PASS | Keywords: "diretrizes listagem", "listing guidelines", "boa listagem", "fotos colecionáveis"; clear FAQ section answers buyer questions |
| 09. Screenshot framing | PASS | Each image has H2 above + intro sentence + alt text 15-150 chars + caption with bolded UI elements + action continuation |
| 10. Fact-check code | PASS | code-audit-14288106.md = zero MISMATCH |
| 11. Fact-check content | PASS | content-audit-14288106.md = zero BLOCKERS |
| 12. Procedure compliance | PASS | All gates green |

Lints:
- em-dashes pt-BR: 0 (was 15 in v1)
- en-dashes pt-BR: 0
- em-dashes EN: 0 (was 15 in v1)
- en-dashes EN: 0
- "auction" / "leilão": 0 in both
- "R$" in EN: 0 (was 2 in v1)
- "R$" in pt-BR: 5 (correct, pricing references)
- Fashion examples (Nike/Adidas/sneaker/tênis): 0 in both
- Metadata description: pt-BR 114 chars, EN 113 chars (both ≤140)
- Title em-dashes: 0 in both
- Mockups: 3 (good listing form, bad listing form, photo do/dont) with `__v2` suffix

Status: ALL PASS. Ready to ship.
