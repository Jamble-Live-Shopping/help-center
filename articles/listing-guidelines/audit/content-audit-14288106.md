# Content audit, article 14288106 (listing-guidelines)

Date: 2026-04-27
Scope: PII scan, internal leak scan, banned words, currency, word diet, tone, alt-text quality.

## Scan 1, PII

- No real user names, emails, phone numbers, CPFs, or addresses in body
- `support@jambleapp.com` is a public support address, not PII
- Example product names (Charizard VMAX, Hot Wheels Super Treasure Hunt, booster Escarlate e Violeta) are public catalog items, not SKUs tied to real listings

Status: CLEAR

## Scan 2, internal leaks

- No internal tool names (Metabase, BigQuery, Mixpanel) exposed
- No admin-only flags or feature toggles referenced
- No engineer names, no Slack channel names
- No revenue numbers, no take-rate percentages
- "equipe da Jamble" and "equipe de operações" are generic, not internal team-specific names

Status: CLEAR

## Scan 3, banned terms / dashes / currency

- pt-BR em-dashes (U+2014): 0
- pt-BR en-dashes (U+2013): 0
- EN em-dashes (U+2014): 0
- EN en-dashes (U+2013): 0
- "auction" / "leilão" occurrences: 0 in both locales
- "R$" in EN body: 0 (currency localized to USD)
- "R$" in pt-BR body: 5 (correct, prices are part of the article)
- Nike / Adidas / sneaker / fashion examples: 0 in both locales
- "Sell your item" / inventive copy not present in iOS: none

Status: CLEAR

## Scan 4, word diet

Changes made:
- v1 H2 "Diretrizes de título" / "Title guidelines" kept (editorial fit), but the body now leads with BR collectibles examples (Charizard VMAX, Hot Wheels Super Treasure Hunt, sealed booster) instead of Nike sneakers
- New H2 "Como é uma boa listagem" / "What a good listing looks like" added with mockup, illustrates the abstract guidelines concretely
- New H2 "O que evitar" / "What to avoid" added with mockup, makes "don't" rules visible
- New H2 "Fotos: faça e não faça" / "Photos: do and don't" added with side-by-side comparison
- "What you cannot list" section trimmed: removed the redundant "Jamble is a fashion and lifestyle marketplace" line, replaced with "Jamble Brasil is focused on collectibles"
- FAQ "Are there specific rules for collectibles" answer expanded to mention Hot Wheels diecast (was only trading cards)
- "Important tips" reduced from 5 verbose bullets to 5 tighter one-line bullets

Total length: pt-BR 5,540 chars (vs v1 5,460), EN 5,280 chars (vs v1 5,200). Net +1.5%, with 3 mockups added that compensate dense text.

## Scan 5, tone-of-voice (BR seller, mostly first-time)

Read aloud test:
- Opens with "O que você vai aprender", direct
- "Por que isto importa" frames the stakes for the seller (trust, sales, account safety) without being preachy
- Examples are recognizable to a BR collector (Charizard, Hot Wheels Super Treasure Hunt, Escarlate e Violeta)
- "Faça / Não faça" cadence is concrete and scannable
- "Na dúvida, avalie um nível abaixo" is encouraging, not gatekeeping
- FAQ answers are short, lead with the answer

No passage requires re-reading. Reader reaches the end without friction.

Status: PASS

## Scan 6, alt-text quality

| Image | Alt length | Has H2 keywords | Unique | Verdict |
|-------|-----------|-----------------|--------|---------|
| good-listing-form__pt-br | 100 chars | "boa listagem", "Charizard", "PSA 10" | yes | PASS |
| good-listing-form__en | 99 chars | "good listing", "Charizard", "Very Good" | yes | PASS |
| bad-listing-form__pt-br | 134 chars | "ruim", "CARTA RARA PROMOÇÃO", "limite" | yes | PASS |
| bad-listing-form__en | 110 chars | "Bad listing", "RARE CARD", "above limit" | yes | PASS |
| photo-do-dont__pt-br | 144 chars | "boas fotos", "Pokémon", "Hot Wheels", "STOCK" | yes | PASS |
| photo-do-dont__en | 144 chars | "good photos", "Pokémon cards", "Hot Wheels", "STOCK" | yes | PASS |

All alt strings are 15-150 chars, descriptive, contain H2 keywords, unique within the article.

## Open blockers

Zero BLOCKERS.
