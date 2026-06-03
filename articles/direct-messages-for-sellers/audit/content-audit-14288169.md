# Content audit, direct-messages-for-sellers (intercom 14288169)

Date: 2026-05-05

## 6 scans

| Scan | Result |
|---|---|
| PII (no real names, emails, phones) | PASS. Sample buyer/seller usernames (@camila_alves) and names (Camila, Bruno, Lucas, Charizard PSA 9) are generic illustrative |
| Banned words (auction/leilao) | PASS. 0 occurrences in pt-br.md and en.md |
| Currency (R$ in pt-BR mockups, $ in EN) | PASS. pt-br body has 0 R$ (article does not document prices); pt-BR mockups use R$ correctly for the sample product price; EN mockups use $ |
| Word diet (no jargon, no internal team names) | PASS. No backend service names, no Wise, no admin tools |
| Tone (humble, conversational, action-oriented) | PASS. "Você", direct CTAs, no corporate fluff |
| Alt-text quality (15-150 chars, descriptive) | PASS. Alt texts 80-120 chars per image, describe screen and key UI elements |

## Editorial bloquants

| Rule | pt-br | en |
|---|---|---|
| Zero em-dash (chr 0x2014) | 0 | 0 |
| Zero en-dash (chr 0x2013) | 0 | 0 |
| Zero auction/leilao | 0 | 0 |
| EN body zero R$ | n/a | 0 |
| pt-BR R$ count (article does not document prices) | 0 | n/a |
| Description <= 140 chars | 112 | 106 |
| Title sans em-dash | OK | OK |

## Verdict

Zero BLOCKER. Ship-ready.
