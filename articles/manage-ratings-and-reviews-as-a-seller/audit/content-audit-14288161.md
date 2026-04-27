# Content audit, article 14288161

Run date: 2026-04-27.
Files: pt-br.md (7509 chars), en.md (7129 chars), metadata.yml.

## 6-scan content review

| # | Scan | pt-BR | EN | Verdict |
|---|------|-------|----|---------|
| 1 | PII (real usernames, emails, phone numbers) | Sample handles `@ana.collector`, `@lucas.tcg` are fictitious | same fictitious handles | PASS |
| 2 | Banned words: em-dash (—), en-dash (–), auction/leilão | 0 / 0 / 0 (verified by python script) | 0 / 0 / 0 | PASS |
| 3 | Currency: pt-BR may carry R$, EN must have 0 R$ | No prices mentioned in this article (rating-only topic). 0 R$ in pt-BR (acceptable, no price needed) | 0 R$, 0 hardcoded "$X" | PASS |
| 4 | Word diet: jargon, internal terms, fee percentages (4%, 10%, 14%) | None. No mention of platform fee, take rate, or PIX percentage | None | PASS |
| 5 | Tone: empathetic, action-oriented, seller-focused | Verbs in second person ("você"), focus on action ("envie rápido", "embale com cuidado", "comunique"), no fluff | mirrors via "you" | PASS |
| 6 | Alt text quality: 15-150 chars, unique per image, contains keywords | image 1 (139 chars), image 2 (146 chars), image 3 (107 chars). All unique, all contain feature keywords | image 1 (123), image 2 (135), image 3 (89). Same | PASS |

## Image framing (Step 9)

| Image | H2 above? | Intro sentence? | Alt 15-150? | Caption with bold UI? | Action continuation? |
|-------|-----------|-----------------|-------------|----------------------|----------------------|
| profile-rating-summary | YES ("Onde sua nota aparece" / "Where your rating shows up") | YES | YES | YES (mentions "a nota média", "o total de Comentários") | YES (paragraph about average stability) |
| rate-transaction-sheet | YES ("Como o comprador te avalia" / "How a buyer rates you") | YES | YES | YES (mentions "Enviar"/"Send") | YES (note about optional comment) |
| report-profile-options | YES ("Como reportar uma avaliação injusta" / "How to report an unfair review") | YES | YES | YES (mentions "Comunicar"/"Report", "Bloquear"/"Block") | YES (paragraph about support outcome) |

All images framed. Zero unframed mockups.

## Structure parity (pt-BR vs EN)

| Section | pt-BR heading | EN heading | Mirror? |
|---------|---------------|------------|---------|
| 1 | O que você vai aprender | What you'll learn | YES |
| 2 | Antes de começar | Before you start | YES |
| 3 | Como funcionam as avaliações | How ratings work | YES |
| 4 | Onde sua nota aparece | Where your rating shows up | YES |
| 5 | Como o comprador te avalia | How a buyer rates you | YES |
| 6 | O que os compradores avaliam | What buyers rate | YES |
| 7 | Como manter uma nota alta | How to keep a high rating | YES |
| 7a | Seja preciso nas suas listagens | Be accurate in your listings | YES |
| 7b | Envie rápido | Ship quickly | YES |
| 7c | Embale com cuidado | Pack with care | YES |
| 7d | Comunique quando precisar | Communicate when needed | YES |
| 8 | Como reportar uma avaliação injusta | How to report an unfair review | YES |
| 9 | Dicas importantes | Important tips | YES |
| 10 | Perguntas frequentes | Common questions | YES |
| 11 | Precisa de ajuda? | Need help? | YES |

Same number of bullets per section. Same number of FAQ items (6). Same image positions.

## Description metadata

| Locale | Title chars | Desc chars | Lead with job-to-do? |
|--------|-------------|------------|----------------------|
| pt-BR | 51 | 129 | YES ("Como funcionam suas avaliações") |
| EN | 38 | 128 | YES ("How your ratings work") |

Both ≤140. Both lead with the user job, not features.

## Verdict

Zero BLOCKER. Content ready for ship.
