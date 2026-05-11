# Compliance audit, article 14288160 (understanding-your-seller-analytics)

Date: 2026-05-08
Reference: process/12-procedure-compliance.md (17 checks) + scripts/validate-article-flow.py

| # | Check | Result |
|---|---|---|
| 1 | iOS code audit done before drafting | PASS, see code-audit-14288160.md |
| 2 | xcstrings pt-BR pulled, no invented translations | PASS (RESUMO, Vendas em tempo real, Minha carteira, Sacar). The 4 dashboard tile labels (TOTAL / AFTER FEES / SOLD / BUYERS) are documented as English-only because the iOS code passes plain literals, not String(localized:) |
| 3 | pt-BR primary, EN strict 1:1 mirror | PASS |
| 4 | Currency localization (no R$ leak in EN body) | PASS, EN uses $1,250.00 in the wallet example |
| 5 | Zero em-dash and en-dash | PASS, 0 in both md |
| 6 | Zero auction/leilao | PASS, 0 in both md |
| 7 | Description <= 140 chars per locale | PASS |
| 8 | Title sans em-dash | PASS |
| 9 | Mockup framing (H2 + intro + alt + caption + action) | PASS for the 3 inline images |
| 10 | Alt-text descriptive 15-150 chars | PASS |
| 11 | Tables 3+ cols converted to PNG | n/a (no body tables) |
| 12 | Zero ASCII box | PASS |
| 13 | PNG suffix __v3 cache-bust | PASS |
| 14 | PNG DPR 3 (>=900px wide) | PASS, all 6 PNGs are >= 900px wide |
| 15 | DA discipline (no cartoon placeholders, no big-text placeholders, no CSS-drawn icons) | PASS, all 3 mockups show real iOS strings only, no glyphs |
| 16 | Strings from xcstrings or product-stable sources | PASS |
| 17 | metadata.yml syntax + locales lowercase + intercom_id 14288160 matches | PASS |

## Validator notes

- risk_flags has one entry: `feature-may-not-exist: no dedicated seller analytics surface`. This is the documented gap that the article exists to address; resolved_decisions has a matching entry green-lighting publication because the article's whole job is to be honest about the gap.
- negative_scan declares two paths (SELLER/Analytics/, SELLER/Stats/) verified absent in the iOS clone resolved via JAMBLE_IOS_ROOT.
- Each `screen` with `review_checks: [icons_match_ios_source]` is anchored via Option B (`html_must_not_contain: ["<img", "<svg", "icon-"]`). The mockups are intentionally text-only.

## Verdict

Article meets every procedure-compliance check above. Final gate is `scripts/run-help-article.py articles/understanding-your-seller-analytics --phase validate` and must exit 0 with zero `screen_icon_review_check_unanchored` warnings before the PR is marked ready.
