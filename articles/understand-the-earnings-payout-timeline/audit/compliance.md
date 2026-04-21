# Compliance gate, article 14288147

Run date: 2026-04-21.
Procedure: 12-step v2 with iOS-faithful mockups and Haiku EN translation.

## 17-check compliance matrix

| # | Check | Result |
|---|-------|--------|
| 1 | Every UI string matches iOS source exactly (see code-audit) | PASS |
| 2 | Colors match design-system.md (#7E53F8, #162233, #17B169, #D92C20, #E9EAEF) | PASS |
| 3 | Phone frame + outer gray frame present (via shot-batch.mjs wrapper) | PASS |
| 4 | PNG rendered at deviceScaleFactor 3 (retina) | PASS |
| 5 | Hosted on Jamble-Live-Shopping/help-center, raw.githubusercontent.com URLs | PASS |
| 6 | Zero em-dashes (U+2014) or en-dashes (U+2013) in body / description | PASS (grep -P "[–—]" empty) |
| 7 | Zero "auction" / "leilão" | PASS (grep empty) |
| 8 | No fee percentages (4%, 10%, 14%, commission) in body | PASS (grep empty) |
| 9 | Currency: R$ in both locales (Jamble BR-only) | PASS |
| 10 | Description ≤140 chars | PASS (pt-BR 110, EN 107) |
| 11 | Headings are job-to-do, not feature-listings | PASS |
| 12 | Tables mobile-safe (3 columns max, no complex tables) | PASS (status table 3 cols) |
| 13 | Every image has H2 + intro + alt + caption/action context | PASS |
| 14 | code-audit.md with zero MISMATCH | PASS |
| 15 | content-audit.md with zero BLOCKERS | PASS |
| 16 | Visual fidelity check: read each PNG, real content present | PASS (6/6 mockups inspected, status badges visible, timeline renders, wallet layout correct) |
| 17 | Strict pt-BR ↔ EN parity (same structure, same bullets, same tables, only UI-strings translated) | PASS |

## Verdict

ALL PASS. Article 14288147 is ready for commit + PR.

## Mockups produced

1. `understand-the-earnings-payout-timeline__wallet-balance__pt-br.png` (101K)
2. `understand-the-earnings-payout-timeline__wallet-balance__en.png` (94K)
3. `understand-the-earnings-payout-timeline__earnings-timeline__pt-br.png` (111K)
4. `understand-the-earnings-payout-timeline__earnings-timeline__en.png` (115K)
5. `understand-the-earnings-payout-timeline__payout-statuses__pt-br.png` (105K)
6. `understand-the-earnings-payout-timeline__payout-statuses__en.png` (100K)

Old mockup (`earnings-payout-timeline__*.png`) superseded, file left on main branch to avoid breaking Intercom CDN references until article is re-injected.
