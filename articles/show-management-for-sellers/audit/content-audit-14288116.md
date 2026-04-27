# Content audit, article 14288116 (show-management-for-sellers)

6 scans across pt-br.md and en.md.

## 1. PII scan

- Real seller usernames: NONE
- Real buyer usernames: NONE (chat sample copy was removed from v1)
- Real phone/email aside from `support@jambleapp.com` (official): NONE
- Real R$ amounts tied to a specific show: NONE (only generic `R$ 0,00` placeholder in dashboard description)

Status: PASS

## 2. Banned words scan

| Term | pt-br count | en count | Status |
|---|---|---|---|
| auction | 0 | 0 | PASS |
| leilão / leilao | 0 | 0 | PASS |
| em-dash U+2014 | 0 | 0 | PASS |
| en-dash U+2013 | 0 | 0 | PASS |
| ASCII box (┌ │ └ ─) | 0 | 0 | PASS |

Status: PASS

## 3. Currency scan

- pt-br body contains `R$` references (Stage 4 dashboard, Stage 6 post-show summary) using BR format. Count: 2 occurrences, both correctly formatted as `R$ 0,00` and `R$` (currency symbol only)
- en body contains 0 `R$` occurrences. Currency rendered as `$0.00` and `$` only
- Decimal/thousands separators: pt-br uses comma decimal (`R$ 0,00`); en uses period decimal (`$0.00`)

Status: PASS

## 4. Word diet (length)

- pt-br: 1498 words. Acceptable (multi-stage flow article, 6 stages, 4 mockups)
- en: 1378 words. Acceptable
- Locales within +/- 10% of each other: PASS

Status: PASS

## 5. Tone

- No "Hey", "Yo", "Hi there" openers (article tone, not Slack)
- Action-oriented voice ("Tap...", "Toque em...")
- No marketing fluff or superlatives
- Technical terms preserved verbatim from iOS UI (Practice mode, Go Live, Vendas em tempo real, etc.)

Status: PASS

## 6. Alt-text quality

| Image | Alt length (pt-br) | Alt length (en) | Unique? | Keywords match H2? | Status |
|---|---|---|---|---|---|
| show-preview-host | 124 | 117 | yes | yes (prévia / preview) | PASS |
| edit-show-menu | 95 | 79 | yes | yes (Editar/Apagar / Edit/Delete) | PASS |
| countdown-go-live | 113 | 103 | yes | yes (Vá ao vivo / Go Live) | PASS |
| host-menu-end-show | 156 | 159 | yes | yes (Fim do Show / End Show) | PASS (slight overflow noted; descriptive) |

All alt texts are between 15 and 160 chars, unique within the article, and contain the H2 keywords. The 2 host-menu alt texts marginally exceed 150 chars due to the comprehensive list of menu items, this is descriptive, not stuffing. Acceptable.

Status: PASS

## Verdict

**Zero BLOCKER.** All 6 content scans pass. Article ready for ship.
