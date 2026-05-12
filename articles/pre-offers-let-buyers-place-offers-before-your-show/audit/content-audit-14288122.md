# Content Audit, pre-offers-let-buyers-place-offers-before-your-show (Intercom 14288122)

## Scan 1: PII (personally identifiable information)

- pt-br.md: NO emails (besides public `support@jambleapp.com`), NO phone numbers, NO names of real users (sample seller `lucas.tcg` is illustrative)
- en.md: same
- mockups: same illustrative seller `lucas.tcg`, no real user data
- PASS

## Scan 2: Banned words (Rule 2c)

```
$ rg -i 'auction|leil[aã]o' articles/pre-offers-let-buyers-place-offers-before-your-show/{pt-br,en}.md
(no matches)
$ rg -i '\bPre-Bid\b' articles/pre-offers-let-buyers-place-offers-before-your-show/{pt-br,en}.md
(no matches)
```

- 0 occurrences of `auction` / `Auction` / `AUCTION` in either body
- 0 occurrences of `leilão` / `leilao` / `Leilão` in either body
- 0 occurrences of `Pre-Bid` (hyphenated source key) in either body
- All references use **Real Time Offer** (EN) / **Oferta em tempo real** (pt-BR), and **Pre-Offer** (EN) / **Pré-oferta** (pt-BR)
- PASS

## Scan 3: Currency localisation (Rule 2b)

- pt-br.md: 10 occurrences of `R$`, all BR-formatted (`R$ 1`, `R$ 5`, `R$ 26`, `R$ 30`, `R$ 50`, `R$ 75`)
- en.md: 0 occurrences of `R$`. 7 occurrences of `$N` (`$1`, `$6`, `$9`, `$11`, `$13`, `$15`, `$26`)
- PASS

## Scan 4: Word diet & em-dashes (Rule 0)

- pt-br.md: 0 em-dashes (U+2014), 0 en-dashes (U+2013)
- en.md: 0 em-dashes, 0 en-dashes
- PASS

## Scan 5: Tone & voice

- Both locales: informational + actionable, second-person, no jargon. Buyer + seller perspectives clearly separated by H2 sections.
- Brazilian collectibles examples (Charizard Holo PSA 9, Hot Wheels Redline 71, Pikachu Holo) per product mix BR
- 0 fake numbers (R$ 5 platform minimum verified in `how-real-time-offers-work` code audit; all UI strings verified in `code-audit-14288122.md`)
- PASS

## Scan 6: Alt-text quality (Step 9)

- pt-br.md image 1 alt: 78 chars, names UI elements ("Card de produto em show agendado", "botão Enviar oferta"). PASS
- pt-br.md image 2 alt: 121 chars, names UI elements ("aviso de oferta final", "valor atual da Pré-oferta", "campo de oferta máxima", "botão para enviar"). PASS
- pt-br.md image 3 alt: 110 chars, names UI elements ("Lista de produtos do vendedor", "começa em valor inicial", "três ofertas em destaque"). PASS
- en.md mirror: equivalent 70-120 char range, keyword overlap with H2. PASS
- All images framed by H2 above + intro sentence + caption with bolded UI + action continuation. PASS

## Scan 7: Stale-feature audit

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Pre-Offer (Pré-oferta) is a live, supported feature | iOS code `PRE-BID/` module fully present, `ShowSaleType.canPrebid` truth table active, xcstrings shipping for en + pt-BR | LIVE | 2026-05-11 | Code | KEEP |
| Sell modes Real Time Offer + Sudden Death support Pre-Offer | `ShowSaleType.swift:73-80` `canPrebid` returns true only for `.AUCTION` and `.SUDDEN_DEATH` | LIVE | 2026-05-11 | Code | KEEP |
| Pre-Offer requires product quantity = 1 | `CreateProductViewModel.swift:347-354` actively disables `isPreBidEnabled` and toasts when quantity > 1 | LIVE | 2026-05-11 | Code | KEEP |
| `Submit Offer` CTA on upcoming-show product cards | `CalendarProductCell.swift:207-225` `preBidButton` actively wired in `setupViews` line 246 and tapped via `openPreBid` line 532-535 | LIVE | 2026-05-11 | Code | KEEP |
| Pre-Offer modal (PreBidViewController) with slide-to-confirm | Active VC, presented from `ProductsCalendarDayViewController.swift:224-231` and `UTILS/COMPONENTS/Cells/JambleProductCellView.swift:63` | LIVE | 2026-05-11 | Code | KEEP |
| Buyer's dedicated Offers screen with Active + Closed tabs | `PreBidListViewController.swift` + `PreBidSectionType.swift` actively shipped | LIVE | 2026-05-11 | Code | KEEP |
| Seller's host product cell shows `Starts at $X · N Offers` when Pre-Offers placed | `ShowHostProductCell.swift:190-198,254-278` actively renders pre-offer state | LIVE | 2026-05-11 | Code | KEEP |
| Verified badges (Rising / Elite / Ultra) | Cross-corpus grep | DEPRECATED 2026-04-28 per CLAUDE.md/process/00-RUNBOOK.md anti-pattern table | n/a | Product | NOT MENTIONED (article does not reference badges) |
| Jamble Prime | Cross-corpus grep | KILLED jan 2026 per CLAUDE.md anti-pattern table | n/a | Product | NOT MENTIONED |
| Auction / Leilão user-facing wording | xcstrings translation of `Auction` key is `Real Time Offer` / `Oferta em tempo real`; ban enforced via Rule 2c | LIVE FEATURE, RENAMED COPY | 2026-05-11 | Code+CLAUDE.md | USED USER-FACING NAME ONLY |

No deprecated features mentioned. All listed claims have a current, non-stale iOS source.

## Verdict

**Zero BLOCKER issues. Article is publication-ready.**
