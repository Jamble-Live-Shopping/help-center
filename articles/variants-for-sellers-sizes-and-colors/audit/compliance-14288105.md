# Compliance audit, article 14288105 (Variants for Sellers, Sizes and Colors)

Last checked: 2026-05-11. Auditor: pipeline worker (batch real-2).

Reference: `process/12-procedure-compliance.md` (18 checks).

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | pt-BR primary, en mirror 1:1 | PASS | Section structure and order mirrored line-by-line. Currency localisation N/A (article body has no prices; mockup shows R$ in pt-BR screen-3 and $ in EN screen-3, with no R$ leak in en.md body). |
| 2 | Em-dash count = 0 in both files | PASS | grep returns 0 occurrences of U+2014. |
| 3 | En-dash count = 0 in both files | PASS | grep returns 0 occurrences of U+2013. |
| 4 | Auction/Leilao count = 0 (user-facing) | PASS | `flow.yml.forbidden_terms` hard-fail grep clean. |
| 5 | EN body: zero `R$` | PASS | Article body in en.md does not use R$. The illustrative pricing in screen-3 EN mockup uses `$` only. |
| 6 | Description <= 140 chars | PASS | pt-BR description: 136 chars; EN: 134 chars. |
| 7 | Title without em-dash | PASS | Both titles: comma-only. |
| 8 | Single H1 per file | PASS | pt-br.md: 1 H1; en.md: 1 H1. |
| 9 | Image framing (Step 9): H2/H3 above, intro sentence, alt 15-150 chars, caption follows, action continuation | PASS | All 3 images framed correctly. |
| 10 | Tables 3+col -> PNG; tables 2-col -> bullet list | PASS | No markdown tables in article body. (v1 had a 4-col color table; rewritten as a bullet on "Multi/One Size/Others" and a reference to the color grid which lives in app, not in the help center body.) |
| 10e | Every `icons_match_ios_source` screen anchored (Option A real-icon OR Option B text-only) | PASS | Screens 1, 2, 3 all anchor as text-only (`no_invented_ui_state` + `labels_match_xcstrings`); no `icons_match_ios_source` declared on any screen, so 10e is N/A per the anchor matrix. |
| 11 | ASCII art / box-drawing | PASS | Zero box-drawing characters in body. |
| 12 | Mockup pair per declared screen (HTML pt-br + en, PNG pt-br + en) | PASS | 3 screens, 6 HTMLs, 6 PNGs DPR3 at 960px wide. |
| 13 | Mockup PNG suffix `__v3` | PASS | All 6 files use `__v3.png` suffix. |
| 14 | xcstrings verbatim (no invented copy) | PASS | EN labels in mockups + body: `Size`, `Color`, `Quantity`, `Clone Past Shows Listings`, `New Quickie Listing`, `Create Credits Giveaway`, `Cancel`. pt-BR labels: `Tamanho`, `Cor`, `Quantidade`, `Clonar listagens de shows anteriores`, `Nova listagem rápida` (accented), `Criar créditos de sorteios` (accented), `Cancelar`. All sourced from `Localizable.xcstrings` and locked verbatim. |
| 15 | Code audit triplet present | PASS | code-audit-14288105.md, content-audit-14288105.md, compliance-14288105.md all present. |
| 16 | Risk flags resolved or documented | PASS | `flow.yml.risk_flags` has 1 active entry (slug-mandated `Variantes` title vs iOS reality), matched by 1 entry in `flow.yml.resolved_decisions` (decided 2026-05-11). Article body explicitly clarifies the no-variants reality in the opening section. |
| 17 | Stale-feature audit | PASS | All cited features (Size/Color cells, Quantity, Clone Past Shows Listings, ProductTemplate auto-fill) confirmed live in iOS 2026-05-11. |
| 18 | metadata.yml state matches publication intent | PASS | `state: published`, locales pt-br + en filled with title + description. |

## Verdict

PASS with one documented risk. Article is shippable. The `Variantes` wording in the title is preserved due to intake / Intercom mapping constraints (intercom_id 14288105); the article body explicitly corrects the expectation and routes sellers to the only code-faithful path.

## Active risks

1. **Slug + title wording**: `Variantes para Vendedores, Tamanhos e Cores` / `Variants for Sellers, Sizes and Colors`. Jamble iOS has no variant surface; each product = 1 size + 1 color + 1 quantity. Article body explicitly clarifies this in the opening section. Slug rename would break Intercom mapping (`intercom_id: 14288105`) and is out of scope for batch real-2. Reviewers may queue a follow-up to retitle the article + re-key Intercom in a separate batch.

## Resolved decisions

1. Risk: "Article title contains 'Variantes' but iOS has no variant surface". Decided by: Aymar (worker batch real-2). Decided at: 2026-05-11. Rationale: slug mandated by intake. Article rescopes the body to be code-faithful: one-size-one-color reality, the Clone Past Shows Listings workaround, and the BR collectibles context where variants are rare. Remaining risk is the lingering title wording; can be re-keyed in a follow-up if Intercom mapping is renegotiated.
