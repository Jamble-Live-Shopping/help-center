# Content audit, article 14288160 (understanding-your-seller-analytics)

Date: 2026-05-08

## 1. PII / sensitive data

- No real user names. Mockup uses `@seunomeusuario` (pt-BR) / `@yourusername` (en) placeholders.
- No emails other than support@jambleapp.com.
- No phone numbers, no tokens, no IDs.

Verdict: PASS.

## 2. Banned words (auction / leilao)

- auction count = 0 in pt-br.md and en.md
- leilao / leilão count = 0 in pt-br.md and en.md

Verdict: PASS.

## 3. Currency

- pt-br.md body uses R$ in the wallet section caption only (e.g. "R$ 1.250,00") because the article references monetary amounts visible to the seller in the wallet. flow.yml.currency_required is set to true to enforce the R$ presence in pt-br.md.
- en.md uses $ for the same example (e.g. "$1,250.00"). en body grep for `R$` returns 0 occurrences.

Verdict: PASS.

## 4. Word diet

- pt-br.md and en.md follow the same H2 structure (1:1 mirror).
- Sentences are short. The "AFTER FEES" caveat paragraph is the longest single bullet and stays under 3 lines on mobile width.
- Tips section uses single-line bullets, no nested bullets, no walls of text.

Verdict: PASS.

## 5. Tone

- Direct address to the seller (você / you).
- The article is honest about the analytics gap (no charts, no exports, no top-items breakdown). It does not pretend a feature exists. It tells the seller exactly what is and is not available, so the reader walks away with a working mental model instead of false hope.
- No condescension, no buildup before sections.

Verdict: PASS.

## 6. Alt text quality

| Image | Alt text content | Verdict |
|---|---|---|
| screen-1 pt-br | names the post-show RESUMO header and the 4 English tile labels (TOTAL, AFTER FEES, SOLD, BUYERS) so the reader is primed for the bilingual reality | PASS |
| screen-1 en | mirror with SUMMARY header | PASS |
| screen-2 pt-br | names the live overlay "Vendas em tempo real" + running total + price-per-item caption | PASS |
| screen-2 en | mirror with "Real-Time Sales" | PASS |
| screen-3 pt-br | names the Minha carteira header, the Saldo disponível caption, the R$ amount, the Sacar button | PASS |
| screen-3 en | mirror with My Wallet / Available balance / Withdraw | PASS |

All alt strings fall in the 15-150 char band. Each alt text is distinct from the others.

Verdict: PASS.

## 7. Stale-feature audit

Confirms every feature, button, and label described in the article still exists in production. Verdicts: live_in_ios | live_in_backend | product_confirmed | deprecated | unknown_blocker.

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Real-Time Sales overlay top-left during host live | LIVE_SHOPPING/Host/View/ShowHostViewController.swift:754-797 | live | 2026-05-08 | Aymar | live_in_ios |
| Post-show summary card with TOTAL / AFTER FEES / SOLD / BUYERS tiles | LIVE_SHOPPING/DashboardHost/Views/ShowHostDashboardView.swift:123-156 | live | 2026-05-08 | Aymar | live_in_ios |
| RESUMO section header in pt-BR | xcstrings SUMMARY -> RESUMO (Localizable.xcstrings:23442-23456) | live | 2026-05-08 | Aymar | live_in_ios |
| TOTAL / AFTER FEES / SOLD / BUYERS render in English on pt-BR device (technical debt) | ShowHostDashboardView.swift:130-148 plain string literals | live | 2026-05-08 | Aymar | live_in_ios |
| Wallet entry point profile -> Settings -> Minha carteira / My Wallet | xcstrings My Wallet (Localizable.xcstrings:15098-15113) + SellerWalletView.swift | live | 2026-05-08 | Aymar | live_in_ios |
| Sacar / Withdraw button on wallet | xcstrings Withdraw -> Sacar (Localizable.xcstrings:27106-27117) + SellerWalletView.swift:96 | live | 2026-05-08 | Aymar | live_in_ios |
| No standalone analytics surface (no charts, no exports, no top-items, no audience breakdown, no conversion-rate display) | Negative scan: SELLER/Analytics/, SELLER/Stats/ both absent under Jamble/ root | absent | 2026-05-08 | Aymar | product_confirmed |
| AdminSellerStatisticsViewController is admin-only (excluded from article) | LIVE_SHOPPING/AdminSellerStatisticsViewController.swift class name + container path | admin-only | 2026-05-08 | Aymar | product_confirmed |

Verdict: PASS. Six items live_in_ios with verified file paths, two product_confirmed (the absent analytics surface and the admin-only stats controller).

## 8. Manual visual review (procedure-compliance check #15)

All 3 mockups were rendered in the v3 framing. None contain cartoon illustrations, big-text product placeholders, or CSS-drawn icons. Each mockup is a tight cropped surface (summary card, live overlay corner, wallet card) so the reader sees exactly what the iOS surface shows.

The wallet mockup is intentionally icon-free: no clock, no chevron, no decorative SVG. This matches the article's editorial focus (numbers + button label, not chrome) and satisfies rule 10e via Option B (text-only contract with all three icon-blockers in flow.yml).

Verdict: PASS (manual visual review).

## Result

8 SCANS pass. Zero BLOCKER. Article is content-quality ready for review. Stale-feature audit confirmed the absent analytics surface is genuinely absent and the article tells the reader so.
