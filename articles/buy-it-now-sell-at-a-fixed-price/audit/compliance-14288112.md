# Compliance Audit, buy-it-now-sell-at-a-fixed-price (seller, intercom 14288112)

Date: 2026-05-08

## Style

| Check | Result |
|---|---|
| Em-dashes in pt-br.md / en.md | 0 / 0 |
| En-dashes in pt-br.md / en.md | 0 / 0 |
| Single H1 per file | Yes (one `# ...` line each) |
| R$ leakage in en.md | 0 (BR pricing localized to $) |
| Currency present in pt-br.md (`R$`) | Yes (R$ 5,00 and R$ 5.000,00) |
| Banned phrases (auction / leilão / Compra Direta) | 0 hits |
| Numbered ordered lists in body | Used only for the "How it works" 4-step list and the picker walkthrough; readable |

## Source-of-truth coverage

Every quoted UI label in the article corresponds to a verbatim xcstrings value:

- "Comprar agora" (PT-BR) and "Buy It Now" (EN): Localizable.xcstrings "Buy It Now" entry
- "Oferta em tempo real" (PT-BR) and "Real Time Offer" (EN): Localizable.xcstrings "Auction" entry
- "Morte súbita" (PT-BR) and "Sudden Death" (EN): Localizable.xcstrings "Sudden Death" entry
- "Venda relâmpago" (PT-BR) and "Flash sale" (EN, lowercase per code): Localizable.xcstrings "Flash sale" entry
- "Modo de venda" (PT-BR) and "Sell mode" (EN): Localizable.xcstrings "Sell mode" entry
- "X restantes" / "X left": Localizable.xcstrings "%lld left" plural variation

## Mockup integrity

| Screen | Real iOS asset anchored | Variant |
|---|---|---|
| screen-1 (sell-mode-picker) | icon-real-time-offer.svg, sell-mode-sudden-death.svg, sell-mode-buy_it_now.svg copied verbatim from Assets.xcassets/icon/ | Static UI |
| screen-2 (buy-it-now-banner) | icon_cart inlined, anchored to Assets.xcassets/icon_cart.imageset comment + alt | Purple normal banner (#7E53F8 16% alpha) |
| screen-3 (flash-sale-banner) | icon-flash inlined, anchored to Assets.xcassets/icon-flash.imageset comment + alt | Green flash banner (#CAF00A 16% alpha) |

Each screen declares both `required_icons` and `review_checks: [icons_match_ios_source, labels_match_xcstrings, no_invented_ui_state]` in flow.yml so the validator hard-anchors the visual contract.

`html_must_contain` locks the verbatim xcstrings labels in every HTML pair.

## Risk flags

None. State = published, risk_flags = [], resolved_decisions = [].

## Verdict

PASS. No "ALL PASS" wording reused; the article ships with zero open risk and a complete deterministic anchor on every screen.
