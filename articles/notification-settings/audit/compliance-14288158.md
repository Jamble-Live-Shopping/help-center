# Compliance audit, article 14288158 (notification-settings)

Date: 2026-05-06
Reference: process/12-procedure-compliance.md (17 checks) + scripts/validate-article-flow.py

| # | Check | Result |
|---|---|---|
| 1 | iOS code audit done before drafting | PASS, see code-audit-14288158.md |
| 2 | xcstrings pt-BR pulled, no invented translations | PASS (permission sheet title, body, CTA) |
| 3 | pt-BR primary, EN strict 1:1 mirror | PASS |
| 4 | Currency localization (no R$ leak in EN body) | PASS, currency_required: false, body has no prices |
| 5 | Zero em-dash and en-dash | PASS |
| 6 | Zero auction/leilao | PASS |
| 7 | Description <= 140 chars per locale | PASS |
| 8 | Title sans em-dash | PASS |
| 9 | Mockup framing (H2 + intro + alt + caption + action) | PASS for the 2 inline images |
| 10 | Alt-text descriptive 15-150 chars | PASS |
| 11 | Tables 3+ cols converted to PNG | n/a |
| 12 | Zero ASCII box | PASS |
| 13 | PNG suffix __v3 cache-bust | PASS |
| 14 | PNG DPR 3 (>=900px wide) | PASS, all 4 PNGs are 1020px wide |
| 15 | DA discipline: no cartoon card/product placeholders, mockup pt-br/en mirror layout | PASS, neutral mockups, locale mirror preserved |
| 16 | Strings from xcstrings or product-stable sources | PASS, with risk_flag documenting English category titles |
| 17 | metadata.yml syntax + locales lowercase + intercom_id 14288158 matches metadata canonical | PASS |

## Validator notes

- 1 active risk_flag: "English section titles on pt-BR locale".
- 1 corresponding `resolved_decisions` entry by Aymar (2026-05-06).
- `published` state is allowed because every active risk has a resolved_decisions entry. The validator's `published_with_unresolved_risks` rule does not fire.

## Verdict

Article meets every procedure-compliance check above. Final gate is `scripts/run-help-article.py articles/notification-settings --phase validate` and must exit 0 before the PR is marked ready.
