# Compliance audit, article 14288097 (pause-your-shop-with-vacation-mode)

Date: 2026-05-06
Reference: process/12-procedure-compliance.md (17 checks) + scripts/validate-article-flow.py

| # | Check | Result |
|---|---|---|
| 1 | iOS code audit done before drafting | PASS, see code-audit-14288097.md |
| 2 | xcstrings pt-BR pulled, no invented translations | PASS (Modo de férias, Ativar, Desativar, ON/OFF modal copy) |
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
| 15 | DA discipline: no cartoon card/product placeholders, no big-text placeholders, no CSS-drawn icons when an iOS asset exists; mockup pt-br portuguese, en english, mirror layout | PASS, neutral photo-style mockups, locale mirror preserved |
| 16 | Strings from xcstrings or product-stable sources | PASS |
| 17 | metadata.yml syntax + locales lowercase + intercom_id 14288097 matches metadata canonical | PASS |

## Validator notes

- risk_flags empty
- resolved_decisions empty
- No active risk; the compliance verdict can stand without a parallel resolved_decisions entry.

## Verdict

Article meets every procedure-compliance check above. Final gate is `scripts/run-help-article.py articles/pause-your-shop-with-vacation-mode --phase validate` and must exit 0 before the PR is marked ready.
