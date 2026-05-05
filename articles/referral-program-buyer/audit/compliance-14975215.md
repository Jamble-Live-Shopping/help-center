# Compliance Audit, referral-program-buyer

Date: 2026-05-05
Reference: process/12-procedure-compliance.md (17 checks)

| # | Check | Result |
|---|---|---|
| 1 | iOS code audit done before drafting | PASS |
| 2 | xcstrings pt-BR pulled, no invented translations | PASS |
| 3 | pt-BR primary, EN strict mirror | PASS |
| 4 | Currency localization (R$ 100 → $100) | PASS |
| 5 | Zero em-dash/en-dash | PASS |
| 6 | Zero auction/leilão | PASS |
| 7 | Description ≤140 chars per locale | PASS, 95/78 |
| 8 | Title sans em-dash | PASS |
| 9 | Mockup framing (H2 + intro + alt + caption + action) | PASS, 2 mockups |
| 10 | Alt-text descriptive | PASS |
| 11 | Tables 3+ cols converted to PNG | n/a |
| 12 | Zero ASCII box | PASS |
| 13 | PNG suffix __v3 cache-bust | PASS |
| 14 | PNG DPR 3 (≥900px wide) | TO VERIFY post-render Phase 4 |
| 15 | Mockup pt-br portuguese, en english | PASS |
| 16 | Strings from xcstrings | PASS |
| 17 | metadata.yml syntax + locales + intercom_id present | PASS (intercom_id null, sera populated au sync) |

## Notes

- Article nouveau: intercom_id sera assigné par l'API Intercom au premier sync (POST → response includes id → writeback to metadata.yml). Si workflow de sync ne supporte pas writeback, créer manuellement via `j-intercom.py articles create --collection 11348923 --state draft` puis coller l'id avant le sync.
- Pas de risk flag legal (ToU 25.A pas en tension avec le code).

## Verdict

ALL PASS pour drafting. Check #14 post-render.
