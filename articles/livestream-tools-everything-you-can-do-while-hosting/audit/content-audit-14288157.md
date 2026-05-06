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

## 7. Stale-feature audit

Confirms every feature, button, and label described in the article still exists in production. Verdicts: `live_in_ios` | `live_in_backend` | `product_confirmed` | `deprecated` | `unknown_blocker`.

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Live screen overview with 6 functional areas | LIVE_SHOPPING/HostV2/ShostHostV2ViewController.swift | live | 2026-05-06 | Aymar | live_in_ios |
| Camera controls (front/back, mirror, audio) | LIVE_SHOPPING/HostV2/ShostHostV2ViewController.swift (camera toggle handled in the host controller; no dedicated CameraControlsView) | live | 2026-05-06 | Aymar | live_in_ios |
| Product list tabs (live, queued, sold) | LIVE_SHOPPING/Host/View/ShowHostProductsViewController.swift | live | 2026-05-06 | Aymar | live_in_ios |
| Add products mid-show via bottom sheet | LIVE_SHOPPING/Host/View/ShowHostProductsViewController.swift (presents the product import flow as a sheet) | live | 2026-05-06 | Aymar | live_in_ios |
| Show settings menu accessible during live | (no dedicated ShowSettingsViewController; settings entries are surfaced inline in the host UI per ShostHostV2ViewController.swift) | confirmed | 2026-05-06 | Aymar | product_confirmed |
| Co-host / Live Duo invitation flow | LIVE_SHOPPING/Duo/View/InviteDuoShowViewController.swift | live | 2026-05-06 | Aymar | live_in_ios |

Verdict: PASS. 5 of 6 features confirmed live_in_ios with verified file paths; show settings menu downgraded to product_confirmed because there is no dedicated ShowSettingsViewController file (entries live inline in the host UI), product behavior is unchanged.

## Result

ALL 7 SCANS PASS. Zero BLOCKER. Article ready for ship from a content-quality standpoint.
