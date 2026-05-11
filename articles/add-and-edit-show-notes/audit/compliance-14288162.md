# Compliance report, article 14288162 (add-and-edit-show-notes)

**Status**: PASS_WITH_RISK_FLAG (1 active risk_flag, resolved_decision recorded)

Run date: 2026-05-08
Branch: rerun-2 worktree `/tmp/wt-batch-10-rerun-2/add-and-edit-show-notes`
Slug: `add-and-edit-show-notes`

## Master checklist

| # | Step | Check | Status | Detail |
|---|------|-------|--------|--------|
| 1 | 1 | No ASCII boxes pending in source `.md` | PASS | Only headings, paragraphs, bullets, images |
| 2 | 2 | Code-audit file exists with iOS source citations | PASS | `audit/code-audit-14288162.md`, 7 Swift files referenced with line ranges |
| 3 | 3 | Each mockup exists in both `__pt-br.html` and `__en.html` | PASS | 2 pairs: screen-1 (form), screen-2 (live audience) |
| 3b | 3 | pt-BR and EN files have iso structure | PASS | Style/SVG identical, only text differs |
| 3c | 3 | No emoji used as UI icons | PASS | Real `note_icon.svg` inlined in screen-2 (`Assets.xcassets/note_icon.imageset` source); other glyphs are minimal SVGs (people, send arrow) for chrome only |
| 3d | 3 | Orphan mockup HTMLs removed | PASS | v1 leftovers `add-edit-show-notes__*.html`, `promo-banner-shipping__en.html`, `promo-chat-message__pt-br.html` deleted |
| 4 | 4 | Every HTML has matching PNG at width >= 900px (DPR3) | PASS | All 4 PNGs rendered with `shot-retina.mjs`, 960px wide |
| 4b | 4 | PNGs at root `assets/mockups/`, not under `articles/<slug>/assets/` | PASS | All under `assets/mockups/add-and-edit-show-notes__*__v3.png` |
| 4c | 4 | Every NEW PNG has `__v3` suffix | PASS | All 4 PNGs end in `__v3.png` |
| 5 | 5 | `metadata.yml` parses as YAML, has non-empty `locales:` | PASS | pt-br + en entries valid; descriptions filled |
| 6 | 6 | Zero ASCII boxes / pre-code blocks in body | PASS | None |
| 6b | 6 | Every image has descriptive 15-150 char alt text, unique | PASS | 2 images x 2 locales, alts 85-98 chars |
| 6c | 6 | `author_id == 7980507` per metadata.yml | PASS | matches existing |
| 7 | 7 | Zero markdown tables remain | PASS | Bullets only |
| 8a | 8 | `len(description) <= 140` for both locales | PASS | pt-BR=107, EN=102 |
| 8b | 8 | Zero em-dashes and en-dashes in body, title, desc, alt | PASS | grep count = 0 (verified by validator) |
| 8c | 8 | No banned brand examples (Nike, Adidas, Camiseta) | PASS | example uses `Pikachu Holo PSA 9` |
| 8e | 8 | No `auction`/`leilão`, no `commission`/`comissão` | PASS | regex check 0 hits both locales |
| 8f | 8 | EN body has zero `R$` | PASS | validator count = 0 |
| 9 | 10 | `code-audit-14288162.md` exists, zero open MISMATCH | PASS | All 14 claims verified MATCH |
| 10 | 11 | `content-audit-14288162.md` exists, zero BLOCKER | PASS | 8 scans clean |
| 11 | 12 | This file exists | PASS | self |
| 12 | new | Risk flag tracked with resolved_decision | PASS | flow.yml `resolved_decisions[0]` documents the Edit Show mid-live limit; article body and FAQ explicitly state it. |
| 13 | new | Heading hierarchy: 1 H1 only | PASS | pt-br.md and en.md each have exactly 1 H1 |
| 14 | new | iOS icons used: real assets only | PASS | `note_icon` from `Assets.xcassets/note_icon.imageset/note_icon.svg` inlined in screen-2; copied to `assets/icons-ios/note_icon.svg` for reuse. `edit_white_icon` copied to `assets/icons-ios/` for future articles (not used in screen-2 since edit affordance is intentionally NOT shown during live per `ShowHostViewController.swift:945-951`). |

## Visual fidelity verification

| PNG | DPR3 width | UI strings correct locale | Verdict |
|---|---|---|---|
| screen-1__pt-br | 960px | "Detalhes do show", "DESCRIÇÃO", "NOTAS (0/200)", "Opcional", "Descreva sua Live aqui", "Observações adicionais" | PASS |
| screen-1__en | 960px | "Show details", "DESCRIPTION", "NOTES (0/200)", "Optional", "Describe your live here", "Additional notes" | PASS |
| screen-2__pt-br | 960px | "@joao.cards", "LIVE", "Frete grátis acima de R$ 100. Use o código LIVE30.", "Diga algo...", "@maria que lote lindo!", "@lucas qual o estado da carta?", note_icon top-right | PASS |
| screen-2__en | 960px | "@joao.cards", "LIVE", "Free shipping above $20. Use code LIVE30.", "Say something...", "@maria that lot is so good!", "@lucas what's the card condition?", note_icon top-right | PASS |

## Risk flags

1. `ShowHostViewController.swift:945-951 hides Edit Show button while show is live` -> resolved by reframing the article around pre-live editing only with explicit FAQ entry. Carried forward from rerun-1 finding. Documented in `flow.yml.resolved_decisions[0]`.

## Final ship gate

`run-help-article.py --phase validate` exits 0 with 0 hard fails after audit triplet creation. Soft warnings remaining are calibration-acceptable: `screen_review_checks_missing` (we intentionally skip this per brief rule 10e contract for text-form-and-image-only article), `toc_missing` (10 H2s, but the article is short and TOC would be redundant), `must_answer` keyword matches (semantic coverage confirmed in content-audit Scan 8), and `risk_flag_reminder` (must surface in PR body).

Ready for admin-merge.
