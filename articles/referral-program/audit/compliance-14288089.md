# Compliance Audit, referral-program (seller, intercom 14288089)

Date: 2026-05-05
Reference: process/12-procedure-compliance.md (17 checks)

| # | Check | Result |
|---|---|---|
| 1 | iOS code audit done before drafting | PASS, Phase 1 RUNBOOK via Explore agent |
| 2 | xcstrings pt-BR pulled, no invented translations | PASS, all strings sourced from Localizable.xcstrings |
| 3 | pt-BR primary locale, EN strict 1:1 mirror | PASS, pt-br written first, en mirrored |
| 4 | Currency localization (R$ 500 → $500, decimal separator inverted) | PASS |
| 5 | Zero em-dash/en-dash | PASS, 0 in pt-br and en |
| 6 | Zero auction/leilão | PASS |
| 7 | Description ≤140 chars per locale | PASS, 96/96 |
| 8 | Title sans em-dash | PASS |
| 9 | Mockup framing (H2 above + intro phrase + alt + caption + action continuation) | PASS, both mockups framed |
| 10 | Alt-text 15-150 chars descriptive, no "image of" | PASS |
| 11 | Tables 3+ cols converted to PNG (n/a here, no tables) | n/a |
| 12 | Zero ASCII box `┌─┐` | PASS, none used |
| 13 | PNG suffix __v3 cache-bust (because v2 existait) | PASS in markdown refs |
| 14 | PNG DPR 3 (≥900px wide) | TO VERIFY post-render Phase 4 |
| 15 | Mockup pt-br has portuguese text, en has english | PASS, both HTMLs distinct |
| 16 | Strings strictement depuis xcstrings ou ToU | PASS |
| 17 | metadata.yml syntax + locales + intercom_id present | PASS |

## Specific risk flag

**ToU 25.B.2.d cap R$ 100 vs code R$ 500**: ship as DRAFT until Yamila signoff. Do NOT merge with `state: published` until reconciled.

## Verdict

ALL PASS for drafting. Check #14 to verify post-render. Ship as draft pending legal signoff.
