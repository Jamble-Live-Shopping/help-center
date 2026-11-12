# Code Audit — how-to-list-products-on-jamble

Date: 2026-11-13 (5.11 fidelity pass; previous audit 2026-05-12)
Intercom ID: 14288093

Sources (released only): iOS tag `5.11` (`Jamble/`), Android tag `v5.11.0`, `jamble_backend` `origin/main` (prod).

## What changed in 5.11

The iOS listing form is now SwiftUI and server-driven (`PRODUCT/Views/SwiftUI/CreateProductView.swift`). Field titles, placeholders, toggle copy and attribute values come from `jamble_backend/src/services/product_service.py` `get_product_edition_fields`; Android v5.11.0 consumes the same endpoint. Only the nav title, Save button, photo helper and sale-type rows are localized in iOS `Localizable.xcstrings`. The old UIKit cells (`SelectPhotoHeaderView`, `CreateProductDescriptionCell`, `PreBidToggleCell`, `ProductShippingProfile`) no longer exist in 5.11.

## Label map (old -> 5.11)

| Mockup | Old label | 5.11 label (pt-BR / EN) | Source |
| --- | --- | --- | --- |
| all | Nova listagem rápida / New Quickie Listing | Criar Novo Anúncio / Create New Listing | iOS `CreateProductView.swift` navigationTitle, xcstrings (pt-BR only, EN = key) |
| all | Adicionar produto / Add Listing | Salvar / Save | iOS `CreateProductView.swift` saveButtonTitle, xcstrings `Save` |
| listing-basics | Selecione uma foto / Select a Photo | Selecionar uma Foto / Choose a picture | jamble_backend `product_service.py:2931` |
| listing-basics | 3 recomendado / 3 recommended | 3 recomendadas / 3 recommended | iOS `CreateProductPhotosSectionView.swift:24`, xcstrings plural `%lld recommended` |
| listing-basics | Título (label) | Detalhes do Produto (header) + Título* (placeholder) / Product Details + Title* | jamble_backend `product_service.py:2942-2943` |
| listing-basics | Descrição (opcional) + helper line | Descrição / Description (placeholder, no helper) | jamble_backend `product_service.py:2955` |
| listing-basics | Categoria row | moved to quantity-shipping mockup (server order puts it after pre-offers) | jamble_backend `product_service.py:3124` |
| selling-mode-price | Comece em | Começar em / Start at | xcstrings `Start at` (`SaleTypeSectionView.swift:152`) |
| selling-mode-price | Duração (segundos) / Timer (Seconds) | Temporizador + unit seg / Timer + sec | xcstrings `Timer`, `sec` (`SaleTypeSectionView.swift:155`) |
| selling-mode-price | A última oferta vence ao final do tempo (no period) / The last offerer wins... | A última oferta vence ao final do tempo. / The last offer wins when the time runs out. | xcstrings key `The last bidder wins at the end of the time.` |
| selling-mode-price | ...even if someone make an offer. | Sem tempo adicional, mesmo que alguém dê uma oferta. / No added time, even if someone makes an offer. | xcstrings key `No added time, even if someone bids. ` |
| selling-mode-price | Radio dark, start R$ 75,00 | Radio brand purple, default start R$ 5 (currency minimum) | `SaleTypeSectionView.swift:136-147,228-256` |
| quantity-shipping | Quantidade with centered round buttons | Quantidade title left, bordered minus/value/plus right | `CreateProductQuantitySectionView.swift`; title jamble_backend `product_service.py:2980` |
| quantity-shipping | (absent) | Lote / Bundle + description toggle | jamble_backend `product_service.py:2998-3002` |
| quantity-shipping | Ativar Pré-oferta? / Enable Pre-Bid? + As ofertas podem ser feitas antes do início da live | Ativar pré-ofertas / Enable offers + Permitir que usuários façam ofertas antes do início da live | jamble_backend `product_service.py:3059-3063` |
| quantity-shipping | Perfil de remessa / Shipping Profile, value "0.18 kg - 0.32 kg (Small Box)" | Perfil de envio* / Shipping profile*, value Automático (2 g · 8,8 × 6,3 × 0,05 cm) | jamble_backend `product_service.py:3340`, `src/entities/shipping_infos.py:47-56`, `src/entities/item_spec.py:68` |
| quantity-shipping | (absent) | Categoria* Cartas de Pokémon, Condição* Quase Mint, Tipo* Carta Individual | jamble_backend `configs/attributes/category.json`, `condition.json`, `item_type.json`, `configs/categories/pokemon_cards.json` |

## Article claims

| Claim | Source | Verdict |
| --- | --- | --- |
| Required fields carry a red asterisk | `CreateProductFieldTitleView.swift:15-18`, `FloatingLabelTextField.swift` placeholder + `*` | MATCH |
| Title required, under Detalhes do Produto | `product_service.py:2939-2949` (required=True) | MATCH |
| Description optional | `product_service.py:2951-2961` (required=False) | MATCH |
| Three sale types in a live: Oferta em tempo real, Comprar agora, Morte súbita | `product_service.py` allowed_sale_types; `ShowSaleType.swift` | MATCH |
| Começar em + Temporizador for offers modes, Preço for Comprar agora | `SaleTypeSectionView.swift:149-170` | MATCH |
| Minimum price R$ 5 | `Price.swift` BRL minPrice 5; shown to users as "Valor mínimo: R$ 5" (`CreateProductViewModel.swift:256-268`) and as the default start value | MATCH |
| Store listings use a fixed price | `product_service.py` non-show branch serves a single `price` field | MATCH |
| Preço de Varejo optional | `product_service.py:3090-3104` | MATCH |
| Lote + Unidades do lote | `product_service.py:2994-3031` | MATCH |
| Ativar pré-ofertas only for Oferta em tempo real / Morte súbita with quantity 1 | `product_service.py:2886-2906` | MATCH |
| Perfil de envio options Automático / Informar peso e tamanho / custom profiles; Automático shows weight and size in parentheses | `product_service.py:3128-3210`, `shipping_infos.py:47-56` | MATCH |
| Criar anúncio na Loja entry | xcstrings `Create a Store listing` = Criar anúncio na Loja | MATCH |

## Removed code-only numbers

Title 40 and description 120 character caps and the quantity range 1 to 1.000 are enforced in code (`max_length`, `max_value`) but never displayed in the 5.11 UI, so they were removed from the article per content rules.

## Not verified

- Seller Hub labels (Criar Novo Produto, Importar CSV, Clonar anúncios) were not re-checked in this pass (web, out of scope of the 5.11 app sources).
- The 2:3 product photo recommendation is an editorial decision from an earlier commit, not re-verified against app code.
- Visual fidelity is code-only (no simulator capture in this pass).
- 5.11 apps get the legacy "Abertura ao Vivo" toggle for openable items; the "Abrir em Live" radio is 5.11.1+ only. Neither is shown or described in this article.

## Verdict

Labels in all three mockups trace to iOS 5.11 xcstrings or the prod backend builder; no open MISMATCH.
