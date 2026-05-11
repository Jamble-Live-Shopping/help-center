# Compliance Audit, referral-program-buyer

Date: 2026-05-11
Reference: process/12-procedure-compliance.md (18 checks, post PR #91/#92/#103/#104)

| # | Check | Result |
|---|---|---|
| 1 | iOS code audit done before drafting | PASS, see code-audit-14975215.md |
| 2 | xcstrings pt-BR pulled, no invented translations | PASS. All UI labels traced to xcstrings line numbers |
| 3 | pt-BR primary, EN strict mirror | PASS, written pt-BR first, EN mirror line-by-line |
| 4 | Currency localization (R$ only in pt-BR if any) | PASS, no R$ amounts in either body (see code-audit) |
| 5 | Zero em-dash/en-dash | PASS |
| 6 | Zero auction/leilão | PASS |
| 7 | Description ≤140 chars per locale | PASS, 109/99 |
| 8 | Title sans em-dash | PASS |
| 9 | Mockup framing (H2 + intro + alt + caption + action) | PASS, three mockups each anchored under their H2 |
| 10 | Alt-text descriptive (15-150 chars, no "image of", no "screenshot of") | PASS |
| 10e | Every `icons_match_ios_source` screen anchored | PASS. Each of the 3 screens declares its `required_icons` and `html_must_contain` (text-anchor option B for `redeem-code` which has no iOS icon asset; option A for the other two which inline real `icon-clock` SVG and document `icon-send` provenance) |
| 11 | Tables 3+ cols converted to PNG | n/a |
| 12 | Zero ASCII box | PASS |
| 13 | PNG suffix __v3 cache-bust | PASS, six PNGs ending in __v3.png |
| 14 | PNG DPR 3 (≥900px wide) | PASS, six PNGs all 1020px wide |
| 15 | Mockup pt-br portuguese, en english | PASS, locale strings come directly from xcstrings |
| 16 | Strings from xcstrings | PASS, no invented strings |
| 17 | metadata.yml syntax + locales + intercom_id present | PASS, intercom_id 14975215, both locales populated |
| 18 | flow.yml v2 schema (PR #91/#92/#103/#104) | PASS. ios_files exist (verified by ls), 3 screens declared, no orphan HTMLs, no negative_scan needed beyond money-amount note (documented in code-audit) |

## Notes

- Money amounts: explicitly omitted from the body, per the brief and
  because xcstrings has no R$ amount keys for the referral. The iOS UI
  uses dynamic API values. The article points users to the screen for
  the exact figure, so the article ages without churn when the campaign
  is re-tuned. See code-audit-14975215.md.
- The article complements the seller-side article `referral-program`
  (already v2-merged) by covering the buyer flow only. The cross-link
  in the last FAQ ("I want to refer friends as sellers") routes the
  seller-intent reader to the seller article without duplicating its
  content.
- No legal flag: buyer referral payout is in-app credit, not cash. The
  ToU 25 cash-payout tension only applies to the seller referral flow.

## Verdict

ALL PASS. Ship-ready for v2 merge.
