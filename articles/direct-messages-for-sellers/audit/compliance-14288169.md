# Compliance audit, direct-messages-for-sellers (intercom 14288169)

Date: 2026-05-05
Reference: process/12-procedure-compliance.md (17 checks) + scripts/validate-article-flow.py (13 hard fails)

| # | Check | Result |
|---|---|---|
| 1 | iOS code audit done before drafting | PASS, see code-audit-14288169.md |
| 2 | xcstrings pt-BR pulled for tab labels and CTAs, no invented translations | PASS |
| 3 | pt-BR primary, EN strict 1:1 mirror | PASS |
| 4 | Currency localization (no R$ leak in EN mockups) | PASS |
| 5 | Zero em-dash and en-dash | PASS |
| 6 | Zero auction/leilao | PASS |
| 7 | Description <= 140 chars per locale | PASS, 112 / 106 |
| 8 | Title sans em-dash | PASS |
| 9 | Mockup framing (H2 + intro + alt + caption + action continuation) | PASS for all 3 inline images |
| 10 | Alt-text descriptive 15-150 chars | PASS |
| 11 | Tables 3+ cols converted to PNG (n/a, no tables in article) | n/a |
| 12 | Zero ASCII box | PASS, none used |
| 13 | PNG suffix __v3 cache-bust | PASS |
| 14 | PNG DPR 3 (>=900px wide) | PASS, all 8 PNGs are 1020px wide |
| 15 | Mockup pt-br portuguese, en english, mirror layout | PASS, generated from same Python templates with locale params |
| 16 | Strings from xcstrings or product-stable sources | PASS, tab labels and CTAs from xcstrings |
| 17 | metadata.yml syntax + locales lowercase + intercom_id | PASS |

## Validator (scripts/validate-article-flow.py) results

Hard fails: 0
Soft warns: see local run output (must_answer keyword false positives expected per cross-locale naive check; risk_flags reminders for product-team confirmations)

## Specific risks flagged in flow.yml

- **R1 (active)**: confirm with Aymar which buyer-to-seller DM rules are live versus planned. Article reflects current iOS behavior.
- **R2 (active)**: confirm with support team whether product-conversation auto-creation behavior changed in any recent release.

## Verdict

ALL PASS. Ready for human review on draft PR.
