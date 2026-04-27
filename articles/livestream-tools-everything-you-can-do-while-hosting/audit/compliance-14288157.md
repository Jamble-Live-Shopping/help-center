# Compliance report, article 14288157 (livestream-tools-everything-you-can-do-while-hosting)

**Run date**: 2026-04-27
**Branch**: update/livestream-tools-v2-revamp
**Status**: ALL PASS

| # | Step | Check | Status | Detail |
|---|------|-------|--------|--------|
| 1 | Step 1 | Source extraction (legacy `_work/wireframe-mockups/ascii-box-N.txt`) | OUT OF SCOPE | v2 pipeline writes mockup-sources directly under `articles/<slug>/mockup-sources/`, no `_work/` artifacts |
| 2 | Step 2 | Code-notes per ASCII box | OUT OF SCOPE | Replaced by single `code-audit-14288157.md` with 22 claim rows, all MATCH |
| 3 | Step 3 | HTML mockup per ASCII box | PASS | 4 mockups x 2 locales = 8 HTML files in `mockup-sources/` |
| 3b | Step 3 | pt-BR pair per `__en.html`, iso structure | PASS | 4 pairs, identical CSS/structure, only text content differs |
| 3c | Step 3 | No emoji UI icons in HTML | PASS | Only product thumbnails use gradient placeholders, no emoji-as-icon. Camera/refresh icons use Unicode symbols, acceptable per design-system since iOS uses SF Symbols rendered identically |
| 4 | Step 4 | PNG width >= 900px (DPR 3) | PASS | All 8 PNGs are 960px wide |
| 4a | Step 4 | New PNGs use `__v2` suffix | PASS | All 8 PNGs end in `__v2.png` |
| 4b | Step 4 | PNGs at root `assets/mockups/` | PASS | All 8 PNGs at `assets/mockups/livestream-tools-everything-you-can-do-while-hosting__*__v2.png` |
| 5 | Step 5 | metadata.yml parses, has locales | PASS | YAML parses, both `pt-br` and `en` locales present with non-empty title and description |
| 6 | Step 6 | Zero ASCII boxes in body | PASS | 2 ASCII boxes removed (was in `## Visão geral` and `## Screen layout overview` sections) |
| 6b | Step 6 | Every img has alt 15-150 chars | PASS | 4 imgs in pt-BR + 4 in EN, all with descriptive alt 73-124 chars |
| 6c | Step 6 | author_id correct | PASS | metadata.yml `author_id: 7980507` (matches existing convention used across help-center repo) |
| 7 | Step 7 | Zero breaking 3+col tables | PASS | No markdown tables in body, sale-action-button states list converted from table to bullet list |
| 8a | Step 8 | description <= 140 chars | PASS | pt-br: 116 chars, en: 105 chars |
| 8b | Step 8 | Zero em/en-dashes (both locales) | PASS | pt-br em=0 en=0, en em=0 en=0 (was 30+30=60 em-dashes) |
| 8b-title | Step 8 | Zero em-dashes in metadata titles | PASS | pt-br title `, ` separator, en title `, ` separator |
| 8c | Step 8 | No banned brand examples | PASS | Sample products are `Charizard Holo PSA 9`, `Hot Wheels Treasure Hunt`, `Pikachu VMAX`, all collectibles aligned with BR product mix |
| 8e | Step 8 | No fee decomposition, no auction/leilão | PASS | 0 occurrences of `auction`, `leilão`, `4%`, `10%`, `commission`, `comissão`, `taxa de saque` in either locale |
| 8e-currency | Step 8 | EN body has zero `R$`, pt-BR has `R$` | PASS | EN: 0 occurrences. pt-BR: 1 occurrence (in `R$ 250` price reference) |
| 9 | Step 9 | Image framing (H2 + intro + alt + caption + action) | PASS | 4 images, each preceded by H2/H3 + 1-line intro, followed by caption and action continuation |
| 10 | Step 10 | code-audit exists, zero MISMATCH | PASS | `audit/code-audit-14288157.md` with 22 claim rows, all MATCH |
| 11 | Step 11 | content-audit exists, zero BLOCKER | PASS | `audit/content-audit-14288157.md` 6 scans, all PASS |
| 12 | Step 12 | This compliance report exists | PASS | This file |

## Summary

- 4 new mockups (was 0 usable, 2 placeholder broken HTML files removed)
- 8 new PNGs at DPR3 (`__v2` suffix)
- 60 em-dashes killed (30 pt-BR + 30 EN)
- 2 ASCII boxes removed and replaced with `screen-overview` mockup
- 1 R$ leak fixed in EN (now currency-localized as `$50`)
- 0 auction/leilão occurrences (was already 0, kept clean)

## Verdict

ALL PASS. Article ready for PR + merge + sync.
