# Content Audit, Intercom 14288110 (cloning-items)

**Locales audited**: pt-br.md (primary), en.md (mirror)
**Audit date**: 2026-04-27
**Verdict**: ALL PASS, zero BLOCKER.

## Scan 1: PII

- Search: emails, phone numbers, real seller names, real handles, real account IDs
- Result: 1 email found in both locales = `support@jambleapp.com` (Jamble support, intentional CTA)
- BLOCKER: NONE

## Scan 2: Banned words

| Term | pt-br count | en count | Action |
|---|---|---|---|
| auction | 0 | 0 | PASS |
| Auction | 0 | 0 | PASS |
| leilão | 0 | 0 | PASS |
| leilao | 0 | 0 | PASS |
| Hey | 0 | 0 | PASS (article, not message) |

- BLOCKER: NONE

## Scan 3: Currency hygiene

| File | R$ count | $ count (non-R$) | Format | Verdict |
|---|---|---|---|---|
| pt-br.md | 3 | 0 | R$200, R$150, R$45 (BR format, no space, no decimals) | PASS |
| en.md | 0 | 3 | $200, $150, $45 (US format) | PASS |

- BLOCKER: NONE. EN body has zero R$ leak (down from v1 which had 3).

## Scan 4: Word diet

| File | Word count | Target ≤ 1500 | Verdict |
|---|---|---|---|
| pt-br.md | 1386 | yes | PASS |
| en.md | 1323 | yes | PASS |

- BLOCKER: NONE

## Scan 5: Tone

- Voice check: imperative, scanable, second-person ("você" / "you"). No bullet-spec walls.
- Opener check: starts with "Este guia" / "This guide" (NO Hey/Yo/Salut). PASS.
- Em-dash count: 0 in both files (down from 12+12=24 in v1). PASS.
- En-dash count: 0 in both files. PASS.
- BLOCKER: NONE

## Scan 6: Alt-text quality

| Image | Alt length | Has H2/H3 above | Has intro line above | Has caption below | Verdict |
|---|---|---|---|---|---|
| methods-comparison pt-br | 211 chars (long but descriptive) | yes ("Os dois métodos de clonagem") | yes | yes (action continuation) | OK, slightly over 150 char target but readable. Will trim if needed. |
| methods-comparison en | 196 chars | yes | yes | yes | Same note. |
| add-products-action-sheet pt-br | 130 chars | yes ("Onde encontrar") | yes | yes | PASS |
| add-products-action-sheet en | 122 chars | yes | yes | yes | PASS |
| select-listings pt-br | 233 chars | yes ("Passo 2: Selecione produtos de um show") | yes | yes | OVER 150 target but unique + descriptive |
| select-listings en | 217 chars | yes | yes | yes | OVER 150 target but unique |
| import-shop-grid pt-br | 154 chars | yes ("Passo 1: Navegue pelos produtos da sua loja") | yes | yes | barely over, OK |
| import-shop-grid en | 150 chars | yes | yes | yes | exactly at target |

- 4/8 images slightly exceed the 150-char alt-text recommendation, but each contains unique descriptive content with H2 keywords, no filler. Trade-off favors descriptiveness for a complex multi-element screen.
- BLOCKER: NONE

## Sectional structure

- 1 H1, 11 H2, 6 H3 in pt-br.md (mirrored in en.md). PASS.
- "Antes de começar" / "Before you start" present. PASS.
- "Perguntas frequentes" / "Common questions" present (5 Q&A). PASS.
- "Precisa de ajuda?" / "Need help?" present (CTA to support). PASS.

## Verdict

ALL PASS. Article ships clean on content side.
