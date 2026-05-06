# Compliance audit, article 14288159 (wishlist-and-favorites)

Date: 2026-05-06
Reference: process/12-procedure-compliance.md (17 checks) + scripts/validate-article-flow.py

| # | Check | Result |
|---|---|---|
| 1 | iOS code audit done before drafting | PASS, see code-audit-14288159.md |
| 2 | xcstrings pt-BR pulled, no invented translations | PASS (Bookmarks, Bids, Start Exploring Deals, Bookmarked shows) |
| 3 | pt-BR primary, EN strict 1:1 mirror | PASS |
| 4 | Currency localization (no R$ leak in EN body) | PASS |
| 5 | Zero em-dash and en-dash | PASS, 0 in both md |
| 6 | Zero auction/leilao | PASS, 0 in both md |
| 7 | Description <= 140 chars per locale | PASS, pt-BR 135, en 132 |
| 8 | Title sans em-dash | PASS |
| 9 | Mockup framing (H2 + intro + alt + caption + action) | PASS for the 3 inline images |
| 10 | Alt-text descriptive 15-150 chars | PASS |
| 11 | Tables 3+ cols converted to PNG | n/a (no body tables) |
| 12 | Zero ASCII box | PASS |
| 13 | PNG suffix __v3 cache-bust | PASS |
| 14 | PNG DPR 3 (>=900px wide) | PASS, all 6 PNGs are 1020px wide |
| 15 | Mockup pt-br portuguese, en english, mirror layout | PASS, generated from a shared template with locale params |
| 16 | Strings from xcstrings or product-stable sources | PASS |
| 17 | metadata.yml syntax + locales lowercase + intercom_id 14288159 matches metadata canonical | PASS |

## Validator notes

- risk_flags empty
- resolved_decisions empty
- No active risk. The compliance verdict can stand without a parallel resolved_decisions entry.

## Verdict

Article meets every procedure-compliance check above. Final gate is `scripts/run-help-article.py articles/wishlist-and-favorites --phase validate` and must exit 0 before the PR is marked ready.
