# Content audit, article 14288157 (livestream-tools-everything-you-can-do-while-hosting)

6 scans across pt-br.md and en.md.

## 1. PII / sensitive data

- No real seller usernames in body or mockups (sample chat usernames `maria_collects` and `tcg_fan` are illustrative)
- No emails other than `support@jambleapp.com` (allowed)
- No phone numbers, no addresses, no tokens, no IDs

Verdict: PASS

## 2. Banned words

- `auction` count = 0 in both locales
- `leilão` / `leilao` count = 0 in both locales
- `Hey` / `Yo` / `Salut` opener: not applicable (article body, not message)
- No tirets longs (em-dashes): 0 in both locales (was 30 + 30 = 60 before this revamp)
- No tirets demi-cadratin (en-dashes): 0 in both locales

Verdict: PASS

## 3. Currency

- pt-br.md: `R$` count = 1 (in mockup caption referencing `R$ 250` price). EN body has 0 `R$`.
- en.md: dollar `$` shows `$50` in screen overview caption (illustrative price for Charizard sample). Format uses point-as-decimal, period-grouping, matching US convention.
- Currency-only divergence between locales. No prose divergence.

Verdict: PASS

## 4. Word diet

- pt-br.md: 1118 words. Length is justified (article describes 6 distinct screen areas, each with its own H2 + procedure). No filler paragraphs.
- en.md: 1098 words, 1:1 mirror of pt-BR.
- Sentences are short (most under 25 words). No buildup paragraphs before sections.
- Tips section uses 5 bullets, each one line.

Verdict: PASS

## 5. Tone (against Jamble voice guidelines)

- Imperative for procedures (`Toque no...`, `Tap the...`), declarative for explanations.
- No buzzword padding (no "robust", "leverage", "seamless", "powerful").
- No "we" condescension. Direct address to the seller (`você` / `you`).
- Brand voice principle "actionable over poetic" maintained throughout.

Verdict: PASS

## 6. Alt text quality

| Image | Alt text length | Verdict |
|---|---|---|
| screen-overview pt-br | 116 chars, descriptive of 6 areas | PASS |
| screen-overview en | 110 chars, mirror | PASS |
| product-list-tabs pt-br | 99 chars, names tabs and buttons | PASS |
| product-list-tabs en | 88 chars, mirror | PASS |
| add-products-sheet pt-br | 78 chars, names both options | PASS |
| add-products-sheet en | 73 chars, mirror | PASS |
| show-settings-menu pt-br | 124 chars, lists key options | PASS |
| show-settings-menu en | 113 chars, mirror | PASS |

All alt texts are 15-150 chars, descriptive (no `screenshot of`, no `image of`), unique per image, contain feature keywords from the H2.

Verdict: PASS

## Result

ALL 6 SCANS PASS. Zero BLOCKER. Article ready for ship from a content-quality standpoint.
