# Compliance audit, article 14288094 (Choose Quantities When Listing Products)

Last checked: 2026-05-08. Auditor: pipeline worker (batch real-1-rerun-2).

Reference: `process/12-procedure-compliance.md` (18 checks).

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | pt-BR primary, en mirror 1:1 | PASS | Title and section structure mirrored line-by-line. Currency localisation N/A (no prices). |
| 2 | Em-dash count = 0 in both files | PASS | grep returns 0 occurrences of U+2014. |
| 3 | En-dash count = 0 in both files | PASS | grep returns 0 occurrences of U+2013. |
| 4 | Auction/Leilao count = 0 (user-facing) | PASS | flow.yml.forbidden_terms hard-fail grep clean. Article uses "Real-time offers" / "Oferta em tempo real". |
| 5 | EN body: zero `R$` | PASS | Article does not document price mechanics. |
| 6 | Description <= 140 chars | PASS | pt-BR description: 114 chars; EN: under 140. |
| 7 | Title without em-dash | PASS | Both titles: comma-only. |
| 8 | Single H1 per file | PASS | pt-br.md: 1 H1; en.md: 1 H1. |
| 9 | Image framing (Step 9): H2/H3 above, intro sentence, alt 15-150 chars, caption follows, action continuation | PASS | All 3 images framed correctly. |
| 10 | Tables 3+col -> PNG; tables 2-col -> bullet list | PASS | No markdown tables in article body. Sell-mode-specific behaviors rendered as bold-label bullets. |
| 11 | ASCII art / box-drawing | PASS | Zero box-drawing characters in body. |
| 12 | Mockup pair per declared screen (HTML pt-br + en, PNG pt-br + en) | PASS | 3 screens, 6 HTMLs, 6 PNGs DPR3 at 960px wide. |
| 13 | Mockup PNG suffix `__v3` | PASS | All 6 files use `__v3.png` suffix. |
| 14 | xcstrings verbatim (no invented copy) | PASS | Quantity, Pre-Bid, Pre-oferta, Quantidade, Auction -> Oferta em tempo real, Sudden Death -> Morte subita, Buy It Now -> Comprar agora, error toast title (Oops, something happened! / Opa, aconteceu alguma coisa!), error toast subtitle (You can not use prebid if you have more than one quantity / Voce nao pode usar o servico de pre-oferta se tiver mais de uma unidade.) all sourced from `Localizable.xcstrings`. |
| 15 | Code audit triplet present | PASS | code-audit-14288094.md, content-audit-14288094.md, compliance-14288094.md all present. |
| 16 | Risk flags resolved or documented | PASS | flow.yml.risk_flags = []; no active risks. |
| 17 | Stale-feature audit | PASS | All cited features confirmed in iOS code as of 2026-05-08. |
| 18 | metadata.yml state matches publication intent | PASS | state: published; reviewers: aymar; locales pt-br + en filled. |

## Verdict

ALL PASS. Article is shippable.

## Active risks

None.

## Resolved decisions

None required.
