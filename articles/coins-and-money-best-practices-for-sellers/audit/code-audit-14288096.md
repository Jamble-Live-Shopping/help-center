# Code audit, article 14288096 (coins-and-money-best-practices-for-sellers)

Date: 2026-05-11
Scope: verify every user-facing string in pt-br.md and en.md against iOS source.

## Article shape

This is a best-practices (editorial) article. It is mostly photo guidance,
condition vocabulary, and authenticity disclosure for a small BR sub-category
(coins, ~7% of BR GMV with diecast and other collectibles per session memory
`product_mix_br.md` 2026-04-19). The article does not describe a specific
iOS screen flow; it does not reproduce iOS UI verbatim.

Consequently:
- `source_of_truth.ios_files` is empty (rule 27 satisfied by explicit empty array)
- Both mockups are `source: composite` (rule 10e does not apply)
- Condition labels match the same Jamble taxonomy used in
  `cards-and-collectibles-best-practices-for-sellers` (server-driven via
  `ProductCondition.swift:10-15`, audited cross-article)

## Claims checked

| Claim | iOS / corpus source | Status |
|-------|---------------------|--------|
| Condition system has 5 levels (Novo com etiquetas, Novo sem etiquetas, Muito bom, Bom, Satisfatório) | `ProductCondition.swift:10-15` (server-driven model) + canonical Jamble taxonomy used in marketplace and in `articles/cards-and-collectibles-best-practices-for-sellers/pt-br.md` (audit 14288099) | MATCH |
| Condition label "Condition" / "Condição" referenced in body | `Localizable.xcstrings` key "Condition" -> en="Condition", pt-BR="Condição" | MATCH |
| Shipping profile names "Carta", "Booster", "Pacotes pequenos" referenced in FAQ | `articles/choose-a-shipping-profile/pt-br.md` (canonical reference, server-driven names; cross-audited per audit 14288099) | MATCH |
| Sell mode "Real-time offers" / "Ofertas em tempo real" | `ShowSaleType.swift` (cross-ref via process/02-code-lookup.md examples, audited in audit 14288099) | MATCH |
| Sell mode "Buy It Now" | `ShowSaleType.swift` (cross-ref) | MATCH |
| BR product mix: article focuses on collectibles only (no fashion / sneaker examples) | session memory `product_mix_br.md` (2026-04-19, 72% Pokemon TCG, 21% Diecast, 7% other) | MATCH (coins examples only, zero fashion mentions) |

## Visual fidelity

| Mockup | source: composite (no iOS UI to mirror) | Status |
|--------|----------------------------------------|--------|
| `coins-and-money-best-practices-for-sellers__screen-1__pt-br__v3.png` | "Fotos: bom vs ruim", FAÇA, EVITE, captions all pt-BR. Editorial illustration of good vs bad coin photography (dark background, focus, flash glare, out of focus, fingers). No iOS UI reproduced. | MATCH (composite) |
| `coins-and-money-best-practices-for-sellers__screen-1__en__v3.png` | "Photos: good vs bad", DO, AVOID, captions all EN. Iso layout to pt-BR. | MATCH (composite) |
| `coins-and-money-best-practices-for-sellers__screen-2__pt-br__v3.png` | "Guia de condição", "Moedas e cédulas", "Novo com etiquetas" through "Satisfatório" all pt-BR (server taxonomy). Editorial swatch progression. | MATCH (composite, pt-BR taxonomy matches server) |
| `coins-and-money-best-practices-for-sellers__screen-2__en__v3.png` | "Condition guide", "Coins and banknotes", "New with Tags" through "Satisfactory" all EN. Iso layout to pt-BR. | MATCH (composite) |

## xcstrings keys consulted

- `Condition` (en="Condition", pt-BR="Condição") - referenced indirectly in the
  condition guide section; no verbatim UI label appears in the article body.

(Article is editorial; no iOS screen is reproduced verbatim, so xcstrings
exposure is minimal by design.)

## Changes from previous version (v1)

- Replaced 24 em-dashes in pt-BR (and 24 in EN) with commas per Rule 0
- Removed the markdown 5-column condition table; condition vocabulary now lives
  in body text + the new condition-guide PNG (screen-2)
- Added 2 composite mockups (4 PNGs): photo good/bad comparison (screen-1) and
  numismatic condition guide (screen-2)
- Title separator changed from colon-only to colon-then-text without em-dash;
  pt-BR title rephrased to "Moedas e Cédulas" (mirrors the listing-requirements
  sibling article 14288164) instead of "Moedas e Dinheiro"
- Description rewritten to ≤140 chars (pt-BR 122, EN 110), leads with job-to-do
  (photos, condition, authenticity, BR market specifics)
- Reorganised photo guidelines around a visual good/bad comparison plus
  separate checklists for coins vs banknotes
- Added explicit Brazilian denomination timeline (Cruzeiro / Cruzado / Cruzado
  Novo / Cruzeiro / Cruzeiro Real / Real) to help sellers identify era on
  listings with unreadable dates
- Replaced "leilão certificado" (forbidden term per Rule 2c) with "casa de
  classificação" / "grading service"

## Open issues

Zero MISMATCH. Zero open issues.
