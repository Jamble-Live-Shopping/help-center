# Compliance, article 14288078 (apply-to-sell-on-jamble)

Date: 2026-04-21
Gate: final 12-step procedure compliance.

| Check | Status | Notes |
|-------|--------|-------|
| 01. Extraction | N/A | No ASCII boxes to extract, article already in markdown |
| 02. Code lookup | PASS | iOS strings sourced from xcstrings + Swift VCs, see code-audit-14288078.md |
| 03. HTML template | PASS | Two pt-BR mockups rebuilt with correct xcstrings |
| 04. Screenshot | PASS | Puppeteer render at deviceScaleFactor 3, two PNGs regenerated |
| 05. Hosting | PASS | PNGs at assets/mockups/ in help-center repo (public raw URL) |
| 06. Intercom injection | DEFERRED | sync-intercom.yml handles this on merge |
| 07. Tables mobile | N/A | No multi-column tables in body |
| 08. Editorial quality | PASS | Job-to-do H2s, ≤140 char desc (pt-BR 105 / EN 91), BR examples added |
| 08b. SEO/GEO | PASS | Keywords: "vender na Jamble", "inscrição vendedor", "apply to sell", clear question-answer FAQ section |
| 09. Screenshot framing | PASS | Each image has H2 above + intro + alt + caption/context below |
| 10. Fact-check code | PASS | code-audit-14288078.md = zero MISMATCH |
| 11. Fact-check content | PASS | content-audit-14288078.md = zero BLOCKERS |
| 12. Procedure compliance | PASS | All gates green |

Lints:
- em-dashes pt-BR: 0
- en-dashes pt-BR: 0
- em-dashes EN: 0
- en-dashes EN: 0
- "auction"/"leilão": 0 in both
- "R$" in EN: 0
- No currency in article, so no `$` check needed

Status: ALL PASS. Ready to ship.
