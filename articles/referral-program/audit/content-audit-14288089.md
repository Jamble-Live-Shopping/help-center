# Content Audit, referral-program (seller, intercom 14288089)

Date: 2026-05-05

## 6 scans

| Scan | Result |
|---|---|
| PII (no real names, emails, phones) | PASS. Mockup names (Lucas Rocha, Bruno Silva) are generic illustrative, no real users |
| Banned words (auction/leilão) | PASS. 0 occurrences in pt-br.md and en.md |
| Currency (R$ in pt-BR, $ in EN) | PASS. pt-br has 17 R$ refs, en has 0 R$ leak, EN uses $500/$498.10/$75 with US format |
| Word diet (no jargon, no internal team names) | PASS. No "Wise" mention, no internal speak. "International financial institution" used per Aymar instruction |
| Tone (humble, conversational, action-oriented) | PASS. "Você", direct CTAs, no corporate fluff |
| Alt-text quality (15-150 chars, descriptive, mots-clés du H2) | PASS. Both alt texts 80-100 chars, describe screen and reward visible |

## Editorial bloquants

| Rule | pt-br | en |
|---|---|---|
| Zero em-dash (—) | 0 | 0 |
| Zero en-dash (–) | 0 | 0 |
| Zero auction/leilão | 0 | 0 |
| EN body zero R$ | n/a | 0 |
| pt-BR contains R$ (article parle de prix) | 17 | n/a |
| Description ≤140 chars | 96 | 96 |
| Title sans em-dash | OK | OK |

## Verdict

Zero BLOCKER. Ship-ready.
