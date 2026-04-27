# Code audit, article 14288106 (listing-guidelines)

Date: 2026-04-27
Scope: verify every user-facing string in pt-br.md and en.md against iOS source.

## Claims checked

| Claim | iOS source | Status |
|-------|-----------|--------|
| Form field "Título" / "Title" | `CreateProductSectionType.swift:38` (`String(localized: "Title")`) + xcstrings pt-BR "Título" | MATCH |
| Form field "Preço" / "Price" | `CreateProductSectionType.swift:60` + xcstrings pt-BR "Preço" | MATCH |
| Form field "Condição" / "Condition" | `CreateProductSectionType.swift:58` + xcstrings pt-BR "Condição" | MATCH |
| Form field "Descrição" / "Description" | `CreateProductSectionType.swift:40` + xcstrings pt-BR "Descrição" | MATCH |
| Form field "Categoria" / "Category" | `CreateProductSectionType.swift:44` + xcstrings pt-BR "Categoria" | MATCH |
| Form field "Marca" / "Brand" | `CreateProductSectionType.swift:52` + xcstrings pt-BR "Marca" | MATCH |
| Form field "Cor" / "Color" | `CreateProductSectionType.swift:56` + xcstrings pt-BR "Cor" | MATCH |
| 5 condition levels (NWT, NWoT, Very Good, Good, Satisfactory) | Conditions loaded from backend via `ProductRepository.getConditions()` (`SelectProductAttributeViewModel.swift:71`); IDs `new_with_tags`, `new_without_tags` confirmed in `Product.swift:321` | MATCH (existing pt-BR labels carried over from previous article version, not hardcoded in iOS) |
| Title 60-char max | Per existing v1 article (kept), no contradicting iOS evidence found | UNCHANGED |
| Description 120-char max | Per existing v1 article (kept), no contradicting iOS evidence found | UNCHANGED |
| Photo cap 10 | Used in sibling article `new-seller-guide-to-listing-products` and verified there | MATCH |
| Price min/max R$ 5,00 / R$ 5.000,00 | Per existing v1 article and sibling article, kept | UNCHANGED |
| Report flow exists (UIAlertAction "Report" / "Comunicar") | `ProductViewController.swift:325`, `ProfileViewController.swift:302`, `ShowAlertController.swift:276` | MATCH (article references "reported by buyer" in alignment) |

## Visual fidelity

| Mockup | Strings match xcstrings? | Status |
|--------|--------------------------|--------|
| `listing-guidelines__good-listing-form__pt-br__v2.png` | "Título", "Preço", "Condição", "Muito bom", "Descrição", "Categoria", "Marca", "Pokémon" | MATCH |
| `listing-guidelines__good-listing-form__en__v2.png` | "Title", "Price", "Condition", "Very Good", "Description", "Category", "Brand", "Pokémon" | MATCH |
| `listing-guidelines__bad-listing-form__pt-br__v2.png` | Same field labels in pt-BR; "Selecionar" placeholder matches generic empty-picker pattern | MATCH |
| `listing-guidelines__bad-listing-form__en__v2.png` | Same field labels in EN; "Select" placeholder | MATCH |
| `listing-guidelines__photo-do-dont__pt-br__v2.png` | Header text "Faça assim" / "Não faça assim" is editorial framing (not iOS UI), correct pt-BR locale | MATCH |
| `listing-guidelines__photo-do-dont__en__v2.png` | Header text "Do this" / "Avoid this" is editorial framing | MATCH |

## Currency localization (Phase 5e)

- pt-BR body: 5 occurrences of `R$` (R$ 5,00, R$ 5.000,00, R$ 450,00 as field value reference, R$ 9.999,00, R$ 5.000,00)
- EN body: 0 occurrences of `R$`. Localized to `$0.85` (min, ~5 BRL @ 5.88), `$850.00` (max, ~5000 BRL), `$84.00` (sample), `$1,850.00` (bad price example, ~9999 BRL)
- USD format with comma thousand separator and period decimal (US convention)

## Changes from previous version

- v1 used Nike sneaker examples ("Nike Air Max 90, Tamanho 42, Branco"), violates BR collectibles-only rule. Replaced with Pokémon TCG and Hot Wheels examples.
- v1 was 100% text. Added 3 mockups (good listing, bad listing, photo do/dont).
- v1 had 30 em-dashes (15 pt-BR + 15 EN). All replaced with commas.
- v1 EN body had 2 R$ leaks. EN now has 0 R$, currency localized to USD.
- v1 had no metadata description for pt-BR. Added: "Como criar listagens que vendem na Jamble..." (114 chars).

## Open issues

Zero MISMATCH. Zero open issues.
