# Content audit, article 14288161

Run date: 2026-04-27.

## 6-scan content review

| # | Scan | pt-BR | EN | Verdict |
|---|------|-------|----|---------|
| 1 | PII (real users/emails/phones) | Sample handles `@ana.collector`, `@lucas.tcg` fictitious | same | PASS |
| 2 | Banned: em-dash, en-dash, auction/leilão | 0 / 0 / 0 | 0 / 0 / 0 | PASS |
| 3 | Currency leak (R$ in EN) | n/a, no prices in this article | 0 R$ | PASS |
| 4 | Word diet (jargon, fee %) | None | None | PASS |
| 5 | Tone: empathetic, action-oriented | Verbs in 2nd person, action-led | Mirrors via "you" | PASS |
| 6 | Alt text 15-150 chars unique with keywords | 3 imgs, 139/146/107 chars, unique | 3 imgs, 123/135/89 chars, unique | PASS |

## Image framing (Step 9)

| Image | H2 above? | Intro sentence? | Alt 15-150? | Caption with bold UI? | Action continuation? |
|-------|-----------|-----------------|-------------|-----------------------|----------------------|
| profile-rating-summary | YES | YES | YES | YES (a nota média / Comentários) | YES |
| rate-transaction-sheet | YES | YES | YES | YES (Enviar/Send) | YES |
| report-profile-options | YES | YES | YES | YES (Comunicar/Report, Bloquear/Block) | YES |

All 3 images framed. Zero unframed.

## Structure parity

15 sections mirror 1:1. 6 FAQ items mirror 1:1. 5 tips mirror. 4 sub-sections under "Como manter uma nota alta" mirror. 3 images at same positions in both files.

## Description metadata

| Locale | Title chars | Desc chars | Lead with job-to-do? |
|--------|-------------|------------|----------------------|
| pt-BR | 51 | 129 | YES |
| EN | 38 | 128 | YES |

Both ≤140.

## Verdict

Zero BLOCKER. Content ready for ship.
