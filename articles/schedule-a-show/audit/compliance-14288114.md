# Compliance Audit, schedule-a-show (seller, intercom 14288114)

Date: 2026-05-08
Reference: process/12-procedure-compliance.md (17 checks) + scripts/validate-article-flow.py + PR #92 rule 10e

| # | Check | Result |
|---|---|---|
| 1 | iOS code audit done before drafting | PASS, see code-audit-14288114.md |
| 2 | xcstrings pt-BR pulled, no invented translations | PASS, 28 keys verified verbatim from Localizable.xcstrings |
| 3 | pt-BR primary, EN strict 1:1 mirror | PASS, pt-br written first, en mirrored line by line |
| 4 | Currency localization (no R$ leak in EN body, US format $20) | PASS |
| 5 | Zero em-dash and en-dash | PASS, 0 in both md |
| 6 | Zero auction/leilao | PASS, 0 in both md |
| 7 | Description <= 140 chars per locale | PASS, pt-BR 113, en 112 |
| 8 | Title sans em-dash | PASS |
| 9 | Mockup framing (H2 above, intro phrase, alt, caption, action) | PASS for all 4 inline images on pt-br + en |
| 10 | Alt-text descriptive 15-150 chars | PASS |
| 11 | Tables 3+ cols converted to PNG | n/a, no tables in body |
| 12 | Zero ASCII box | PASS |
| 13 | PNG suffix __v3 cache-bust | PASS, all 8 PNGs use __v3 |
| 14 | PNG DPR 3 (>=900px wide) | PASS, all 8 PNGs are 960px wide (DPR3 from 320px phone) |
| 15 | DA discipline (no cartoon placeholders, no CSS-drawn icons when iOS asset exists) | PASS, the only embedded iOS icon (icon-calendar) renders the real SVG verbatim; the other three screens are text-only at the surfaces under audit and the html_must_not_contain anchor enforces that the mockup cannot smuggle invented icon markup back in |
| 16 | Strings strictly from xcstrings or product-stable sources | PASS |
| 17 | metadata.yml syntax + locales lowercase + intercom_id 14288114 matches | PASS |

## PR #92 rule 10e (icon anchor per screen)

| Screen | review_checks | Anchor | Status |
|---|---|---|---|
| show-title-input | icons_match_ios_source, labels_match_xcstrings, no_invented_ui_state | text-only: html_must_not_contain ['<img', '<svg', 'icon-'] (all three blockers) | ANCHORED |
| show-tags-grid | icons_match_ios_source, labels_match_xcstrings, no_invented_ui_state | text-only: html_must_not_contain ['<img', '<svg', 'icon-'] (all three blockers) | ANCHORED |
| show-cover-options | icons_match_ios_source, labels_match_xcstrings, no_invented_ui_state | text-only: html_must_not_contain ['<img', '<svg', 'icon-'] (all three blockers) | ANCHORED |
| show-details-form | icons_match_ios_source, labels_match_xcstrings, no_invented_ui_state | real-icon: required_icons [icon-calendar] + verbatim SVG embed + Assets.xcassets/icon-calendar.imageset comment + aria-label | ANCHORED |

## Validator notes

- risk_flags empty
- resolved_decisions empty
- No active risk
- icons_required: [icon-calendar] satisfied by assets/icons-ios/icon-calendar.svg + inline SVG embed in show-details-form HTML pair (with xcassets comment)

## Verdict

ALL PASS. Ship-ready. Final gate is `scripts/run-help-article.py articles/schedule-a-show --phase validate` and must exit 0.
