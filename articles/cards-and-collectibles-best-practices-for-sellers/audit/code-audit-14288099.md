# Code audit, article 14288099 (cards-and-collectibles-best-practices-for-sellers)

Date: 2026-04-27
Scope: verify every user-facing string in pt-br.md and en.md against iOS source.

## Claims checked

| Claim | iOS source | Status |
|-------|-----------|--------|
| Create product field "Title" / "Título" | `CreateProductSectionType.swift:38` + xcstrings | MATCH |
| Create product field "Category" / "Categoria" | `CreateProductSectionType.swift:44` + xcstrings | MATCH |
| Create product field "Condition" / "Condição" | `CreateProductSectionType.swift:58` + xcstrings | MATCH |
| Create product field "Shipping Profile" / "Perfil de remessa" | `CreateProductSectionType.swift:64` + xcstrings | MATCH |
| Create product field "Price" / "Preço" | `CreateProductSectionType.swift:60` + xcstrings | MATCH |
| Pack Opening section title "Pack Opening" / "Abertura do pacote" | `CreateProductSectionType.swift:42` + `PackOpeningToggleCell.swift:66` + xcstrings | MATCH |
| Pack Opening subtitle "Open packs during the Live" / "Abra os pacotes durante a live" | `PackOpeningToggleCell.swift:84` + xcstrings | MATCH |
| Pack Opening description "If you plan to open Pokémon booster packs once they're purchased" / pt-BR equivalent | `PackOpeningToggleCell.swift:93` + xcstrings | MATCH |
| Toggle on tint color customPurple (#7E53F8) | `PackOpeningToggleCell.swift:100` | MATCH |
| Pack Opening cell border 1px, corner radius 8 | `PackOpeningToggleCell.swift:46-49` | MATCH |
| Condition options dynamically loaded from server (id, title, description) | `ProductCondition.swift` | MATCH (5 levels named in pt-br body match Jamble taxonomy used in marketplace) |
| Shipping profile names "Carta", "Booster", "Pacotes pequenos", "Pacotes médios", "Itens volumosos", "Roupas padrão" | `articles/choose-a-shipping-profile/pt-br.md` (canonical reference, sourced from server data) | MATCH |
| Sell mode "Real-time offers" / "Ofertas em tempo real" reference | `ShowSaleType.swift` (cross-ref via process/02-code-lookup.md examples) | MATCH |
| Sell mode "Buy It Now" reference | `ShowSaleType.swift` (cross-ref) | MATCH |

## Visual fidelity

| Mockup | pt-BR strings match xcstrings? | Status |
|--------|--------------------------------|--------|
| `cards-and-collectibles-best-practices-for-sellers__sample-listing__pt-br__v2.png` | TÍTULO, CATEGORIA, CONDIÇÃO, PERFIL DE REMESSA, PREÇO INICIAL, "Novo sem etiquetas", "Carta", "Trading Cards" all pt-BR | MATCH |
| `cards-and-collectibles-best-practices-for-sellers__sample-listing__en__v2.png` | Title, Category, Condition, Shipping Profile, Starting price, "New without Tags", "Card" all EN | MATCH |
| `cards-and-collectibles-best-practices-for-sellers__condition-guide__pt-br__v2.png` | "Guia de condição", "Cards de TCG", "Novo com etiquetas" through "Satisfatório" all pt-BR | MATCH |
| `cards-and-collectibles-best-practices-for-sellers__condition-guide__en__v2.png` | "Condition guide", "TCG Cards", "New with Tags" through "Satisfactory" all EN | MATCH |
| `cards-and-collectibles-best-practices-for-sellers__photo-checklist__pt-br__v2.png` | "Fotos: bom vs ruim", FAÇA, EVITE, captions all pt-BR | MATCH |
| `cards-and-collectibles-best-practices-for-sellers__photo-checklist__en__v2.png` | "Photos: good vs bad", DO, AVOID, captions all EN | MATCH |
| `cards-and-collectibles-best-practices-for-sellers__pack-opening-toggle__pt-br__v2.png` | "Abertura do pacote", "Abra os pacotes durante a live", "Se você planeja abrir boosters de Pokémon assim que comprá-los" exact xcstrings match | MATCH |
| `cards-and-collectibles-best-practices-for-sellers__pack-opening-toggle__en__v2.png` | "Pack Opening", "Open packs during the Live", "If you plan to open Pokémon booster packs once they're purchased" exact xcstrings match | MATCH |

## Changes from previous version (v1)

- Added 4 mockup pairs (pt-BR + EN) where v1 had 0 mockups: sample listing, condition guide, photo checklist, Pack Opening toggle
- Killed all 27 em-dashes in pt-BR (and 27 in EN), replaced with commas per Rule 0
- Restructured photo guidelines around a visual good/bad comparison instead of a wall of bullets
- Added a flagship sample listing section that shows how a complete listing looks for a real Pokémon TCG card (Charizard VMAX, Shining Fates, NM, R$ 450,00 / $90.00)
- Pack Opening toggle now shown with the actual iOS UI, including the exact xcstrings copy ("Abra os pacotes durante a live", "Se você planeja abrir boosters de Pokémon assim que comprá-los")
- Reformatted titles with comma separator instead of em-dash ("Cards e Colecionáveis, Melhores Práticas para Vendedores")
- Description rewritten to ≤140 chars (pt-BR 119, EN 117), leads with job-to-do (condition, photos, shipping, Pack Opening)

## Open issues

Zero MISMATCH. Zero open issues.
