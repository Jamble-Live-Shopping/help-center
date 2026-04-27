# Compliance Checklist, how-real-time-offers-work (Intercom 14288115)

| # | Check | Status | Notes |
|---|---|---|---|
| 1 | Title without em-dash, ≤60 chars (both locales) | PASS | pt-BR "Como Funcionam as Ofertas em Tempo Real" (39 ch), EN "How Real-time Offers Work" (25 ch) |
| 2 | Description ≤140 chars (both locales) | PASS | pt-BR 134 ch, EN 132 ch |
| 3 | Body em-dash count = 0 (both locales) | PASS | pt-BR 0, EN 0 |
| 4 | Body en-dash count = 0 (both locales) | PASS | pt-BR 0, EN 0 |
| 5 | Body `auction` / `leilão` count = 0 (Rule 2c) | PASS | both locales 0 |
| 6 | EN body `R$` count = 0 (Rule 2b) | PASS | EN 0 |
| 7 | pt-BR body `R$` present (article cites prices) | PASS | pt-BR 7 occurrences, BR-formatted |
| 8 | All mockups use `__v2` PNG suffix | PASS | 4 mockups x 2 locales = 8 PNGs, all `__v2` |
| 9 | All PNGs DPR3 (≥900 px wide) | PASS | sell-mode 960px, real-time-offer-card 960px, sudden-death-card 960px, comparison-chart 1068px |
| 10 | Step 9 framing on every image (H2 + intro + alt + caption + action) | PASS | 4/4 images on each locale |
| 11 | Alt text 15-150 chars, descriptive, keyword-aligned | PASS | range 99-142 chars |
| 12 | Source = iOS Swift code (per Rule 1) | PASS | code-audit-14288115.md, 0 MISMATCH |
| 13 | Strings match xcstrings pt-BR | PASS | "Oferta em tempo real", "Sudden Death", "Comprar agora", "Modo de venda", subtitles all confirmed |
| 14 | 3+ column tables converted to PNG (Rule 7d) | PASS | comparison-chart PNG replaces the 5-row 3-col markdown table |
| 15 | No nested `<ul>` / `<dl>` / Intercom-incompatible HTML | PASS | markdown only, simple paragraphs + bullets |
| 16 | Both locales 1:1 mirror (only currency divergence) | PASS | section count match, paragraph count match, only `R$ 5 / $1`, `R$ 145 / $29`, `R$ 150 / $30`, `R$ 30 / $6`, `R$ 85 / $17`, `R$ 90 / $18` divergences (currency localisation) |
| 17 | metadata.yml `last_sync` updated to today | PASS | 2026-04-27T00:00:00Z |

**Summary: 17/17 PASS**

**Ready to merge.**
