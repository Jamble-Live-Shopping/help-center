# Compliance audit, article 14288159 (wishlist-and-favorites)

Date: 2026-05-08 (rerun-2 patch on the 2026-05-06 audit)
Reference: process/12-procedure-compliance.md (17 checks) + scripts/validate-article-flow.py + PR #91 + PR #92 contracts

| # | Check | Result |
|---|---|---|
| 1 | iOS code audit done before drafting | PASS, see code-audit-14288159.md (2026-05-08 rerun-2 entry pins Bids->Offers + heart-not-flag nuance) |
| 2 | xcstrings pt-BR pulled, no invented translations | PASS (Bookmarks->Favoritos, Bids->Offers/Ofertas, Start Exploring Deals->Comece a explorar as ofertas, Discover deals and save your favorite items.->Descubra ofertas e salve seus itens favoritos.) |
| 3 | pt-BR primary, EN strict 1:1 mirror with xcstrings-correct labels (en uses "Offers", not "Bids") | PASS |
| 4 | Currency localization (no R$ leak in EN body) | PASS |
| 5 | Zero em-dash and en-dash | PASS, 0 in both md |
| 6 | Zero auction/leilao | PASS, 0 in both md |
| 7 | Description <= 140 chars per locale | PASS, pt-BR 135, en 132 |
| 8 | Title sans em-dash | PASS |
| 9 | Mockup framing (H2 + intro + alt + caption + action) | PASS for the 3 inline images |
| 10 | Alt-text descriptive 15-150 chars, "heart icon" vocabulary | PASS |
| 11 | Tables 3+ cols converted to PNG | n/a (no body tables) |
| 12 | Zero ASCII box | PASS |
| 13 | PNG suffix __v3 cache-bust | PASS |
| 14 | PNG DPR 3 (>=900px wide) | PASS, all 6 PNGs are 1020px wide |
| 15 | DA discipline: no cartoon card/product placeholders, no big-text placeholders, no CSS-drawn icons when an iOS asset exists; mockup pt-br portuguese, en english, mirror layout | PASS after manual visual review on 2026-05-08: all 6 mockups now embed the verbatim `bookmark_heart_white_icon` SVG from xcassets, with xcassets comment + alt + aria-label, and use the iOS `liveRed` (#F14A22) saved-state colour. Locale mirror preserved (en uses Offers, not Bids) |
| 16 | Strings from xcstrings or product-stable sources | PASS |
| 17 | metadata.yml syntax + locales lowercase + intercom_id 14288159 matches metadata canonical | PASS |
| 10e (PR #92, NEW) | Each mockup screen anchored: real-icon Option A (`required_icons: [bookmark_heart_white_icon]`) on all 3 screens + `review_checks` triplet + `html_must_contain` per locale | PASS |
| 91/heading_hierarchy | exactly 1 H1 in pt-br.md and en.md | PASS |
| 91/mockup_orphan_html | every HTML in mockup-sources/ matches a declared screen + locale | PASS, 6 HTMLs <-> 3 screens x 2 locales |
| 91/source_of_truth_path_missing | every ios_files entry resolves under JAMBLE_IOS_ROOT | PASS, 10 entries resolved (verified 2026-05-08) |

## Validator notes

- risk_flags empty
- resolved_decisions empty
- No active risk. The compliance verdict can stand without a parallel resolved_decisions entry.
- toc_required=false in flow.yml: the article reads top-down, a TOC would not help the buyer find a deeper section.

## Verdict

Article meets every procedure-compliance check above. Final gate is `scripts/run-help-article.py articles/wishlist-and-favorites --phase validate` and exits 0 with 0 hard fails and 0 soft warns on 2026-05-08.
