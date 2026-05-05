# Content Audit, referral-program-buyer

Date: 2026-05-05

## 6 scans

| Scan | Result |
|---|---|
| PII | PASS, generic mockup names (Camila Alves, João Ferreira) |
| Banned words (auction/leilão) | PASS, 0 occurrences |
| Currency (R$ in pt-BR, $ in EN) | PASS. pt-br 16 R$ refs, en 0 R$ leak |
| Word diet (no jargon, no internal team names) | PASS |
| Tone (humble, conversational) | PASS |
| Alt-text quality | PASS, descriptive 15-150 chars |

## Editorial bloquants

| Rule | pt-br | en |
|---|---|---|
| Zero em-dash | 0 | 0 |
| Zero en-dash | 0 | 0 |
| Zero auction/leilão | 0 | 0 |
| EN body zero R$ | n/a | 0 |
| pt-BR contains R$ | 16 | n/a |
| Description ≤140 chars | 95 | 78 |
| Title sans em-dash | OK | OK |

## Verdict

Zero BLOCKER. Ship-ready.
