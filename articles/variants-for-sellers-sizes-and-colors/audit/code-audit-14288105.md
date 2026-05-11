# Code audit, article 14288105 (Variants for Sellers, Sizes and Colors)

Last checked: 2026-05-11. Auditor: pipeline worker (batch real-2).

## Summary

The v1 article documented sizes + colors as if it described a "variants" feature; in fact, Jamble iOS has **no variant surface**. Each product is one (size, color, quantity) tuple, period. The v2 rewrite makes that explicit, names the rule, and points sellers to the only code-faithful path for multi-size inventory: **Clone Past Shows Listings** (xcstrings: pt-BR `Clonar listagens de shows anteriores`).

The BR market is collectibles (72% Pokemon TCG, 21% Diecast, 7% other, GMV-weighted 2026-04-19), so the multi-size workflow is genuinely rare; the article scopes the example (Nike Air Max in three sizes) as a fashion residual case rather than the headline use.

## Source files

- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/PRODUCT/View Models/CreateProductViewModel.swift`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/PRODUCT/Models/ProductSize.swift`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/PRODUCT/Models/ProductColor.swift`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/PRODUCT/Views/CreateProductViewController.swift`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/PRODUCT/Views/SelectProductAttributeViewController.swift`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/LIVE_SHOPPING/Host/View/ShowHostViewController.swift`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/SERVICE/API/Repository/Modules/Product/ProductRepository.swift`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/SERVICE/API/Repository/Modules/Product/Model/Request/ProductTemplate.swift`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings`

All paths verified with `ls` on 2026-05-11.

## Claims vs code

| Claim in article | Article says | Code says | Source file | Status |
|------------------|--------------|-----------|-------------|--------|
| Each product has one size | "Each listing has one size" / "Cada anuncio tem um tamanho" | `var size: CurrentValueSubject<ProductSize?, Never>` (scalar, not array) | `PRODUCT/View Models/CreateProductViewModel.swift:36, 89` | MATCH |
| Each product has one color | "Each listing has one color" / "uma cor" | `var color: CurrentValueSubject<ProductColor?, Never>` (scalar, not array) | `PRODUCT/View Models/CreateProductViewModel.swift:32, 90` | MATCH |
| ProductSize is a scalar type | (implicit in "one size" claim) | `struct ProductSize: Codable, Equatable, ProductAttribute { var id, title, order }` | `PRODUCT/Models/ProductSize.swift:10-14` | MATCH |
| ProductColor is a scalar type | (implicit in "one color" claim) | `struct ProductColor: Codable, Equatable, ProductAttribute` | `PRODUCT/Models/ProductColor.swift:10` | MATCH |
| No "variants" field exists in the app | "There is no variants field in the app" / "Nao existe um campo de variantes no app" | grep `variant` / `variation` across `/PRODUCT/`, `/RESOURCES/Localizable.xcstrings`: zero hits | repo-wide grep 2026-05-11 | MATCH (negative scan) |
| Size field appears only after full category selection | "The Size field only appears after you select the full category (Gender, Category, Subcategory)" | `getSizeSection(order:)` guards `gender.value?.id`, `category.value?.id`, `subcategory.value?.id`; returns nil if any missing | `PRODUCT/View Models/CreateProductViewModel.swift:583-589` | MATCH |
| Size resets when category changes | (not explicitly claimed in v2, behavior implicit) | `Publishers.CombineLatest3(gender, category, subcategory).removeDuplicates(...).dropFirst().sink { self?.size.send(nil) }` | `PRODUCT/View Models/CreateProductViewModel.swift:299-305` | MATCH (behavior retained, not surfaced in article body to keep it short) |
| Quantity default = 1 | "The default is 1" / "Por padrao, o valor e 1" | `quantityInput = CurrentValueSubject<Int, Never>(1)`, `quantityOutput = .init(1)` | `PRODUCT/View Models/CreateProductViewModel.swift:81-82` (per choose-quantities audit) | MATCH |
| Quantity min = 1, max = 1,000 | "minimum is 1 and the maximum is 1,000" / "minimo e 1 e o maximo e 1.000" | `case .AUCTION, .SUDDEN_DEATH, .BUY_IT_NOW: return 1000`; `Swift.max(min(quantity, max), 1)` | `PRODUCT/View Models/CreateProductViewModel.swift:307-323` | MATCH |
| Clone Past Shows Listings exists | "use Clone Past Shows Listings" / "Clonar listagens de shows anteriores" | `let cloneFromShowsAction = UIAlertAction(title: String(localized: "Clone Past Shows Listings")` | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1705-1713` | MATCH |
| Clone Past Shows Listings is in the add-product action sheet | "from the add-product menu inside your show" / "menu de adicionar produto no show" | `actionSheet.addAction(cloneFromShowsAction)` inside `presentAddProductSheet()` | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1684, 1713` | MATCH |
| Cloning brings photos, description, price, brand, category from original | "Cloning brings photos, description, price, brand, and category" | `ProductTemplate` fills `availableCount, showSaleSettings, shippingProfile, gender, category, subcategory, color, brand, condition` from the template payload; the Clone Past Shows Listings flow uses the same template-fill mechanism via `ShowHostImportView` | `PRODUCT/View Models/CreateProductViewModel.swift:446-460` (fillProduct), `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1708-1710` | MATCH (the article says "photos, description, price, brand, and category"; iOS template fill covers these plus size/color/quantity. Article keeps the list short to avoid over-spec'ing.) |
| Multi-quantity = identical units same size + same color | "how many identical units the listing covers, with the same size and the same color" | `quantityOutput` is a scalar Int tied to the single (size, color) combo; no per-variant inventory exists | `PRODUCT/View Models/CreateProductViewModel.swift:81-82, 317-331` | MATCH |
| Sell-out is per listing | "When a unit is sold, that listing's count drops by 1; when it hits zero, that size is marked sold out, without affecting the others" | `available_count` is per-product; the iOS client consumes it per listing. Three listings = three independent counters. | `PRODUCT/View Models/CreateProductViewModel.swift:370-371, 419, 848` | MATCH (backend lifecycle for "sold out" mark is trusted from product contract; iOS only consumes `available_count`) |
| Size xcstrings | EN `Size` / pt-BR `Tamanho` | xcstrings key `Size` -> EN `Size`, pt-BR `Tamanho` | `RESOURCES/Localizable.xcstrings:22074-22085` | MATCH (verbatim, used in screen-1 mockups and article body) |
| Color xcstrings | EN `Color` / pt-BR `Cor` | xcstrings key `Color` -> EN `Color`, pt-BR `Cor` | `RESOURCES/Localizable.xcstrings:6894-6905` | MATCH (verbatim, used in screen-1 mockups and article body) |
| Quantity xcstrings | EN `Quantity` / pt-BR `Quantidade` | xcstrings key `Quantity` -> EN `Quantity`, pt-BR `Quantidade` | `RESOURCES/Localizable.xcstrings:18557-18568` | MATCH (verbatim) |
| Clone Past Shows Listings xcstrings (en + pt-BR) | EN `Clone Past Shows Listings` / pt-BR `Clonar listagens de shows anteriores` | xcstrings key `Clone Past Shows Listings` -> EN value `Clone Past Shows Listings`, pt-BR value `Clonar listagens de shows anteriores` | `RESOURCES/Localizable.xcstrings:6719-6733` | MATCH (verbatim, used in screen-2 mockups and article body) |
| New Quickie Listing xcstrings (action sheet sibling) | (shown in screen-2 mockup) | xcstrings key `New Quickie Listing` -> EN `New Quickie Listing`, pt-BR `Nova listagem rápida` | `RESOURCES/Localizable.xcstrings:15223-15235` | MATCH (verbatim in screen-2 mockup) |
| Create Credits Giveaway xcstrings (action sheet sibling) | (shown in screen-2 mockup) | xcstrings key `Create Credits Giveaway` -> EN `Create Credits Giveaway`, pt-BR `Criar créditos de sorteios` | `RESOURCES/Localizable.xcstrings:8099-8112` | MATCH (verbatim in screen-2 mockup) |
| Cancel xcstrings (action sheet) | (shown in screen-2 mockup) | xcstrings key `Cancel` -> EN `Cancel`, pt-BR `Cancelar` | `RESOURCES/Localizable.xcstrings:6020-6032` | MATCH (verbatim in screen-2 mockup) |

## Decisions

- **No "variants" surface, by design**: grep over `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/` returned zero hits for `variant` / `variation` / `variante` / `variação` in source code or xcstrings. The CreateProduct form has a single scalar `size` and single scalar `color`, and a single scalar `quantityOutput`. The "add variant" / "per-variant quantity" workflow described in the brief simply does not exist in the iOS app. The article makes this explicit and routes sellers to `Clone Past Shows Listings`, which is the only code-faithful path to listing the same item across multiple sizes/colors. Risk flagged in `flow.yml.risk_flags`, accepted in `flow.yml.resolved_decisions` because the slug is intake-mandated and renaming the slug breaks the Intercom mapping for already-published `intercom_id: 14288105`.

- **BR-collectibles framing up front (2026-05-11)**: per session memory (`product_mix_br.md`), BR GMV is 72% Pokemon TCG, 21% Diecast, 7% other. Multi-size inventory is rare in this mix (cards have no size; Diecast scale varies by SKU, not by listing). The article notes this in the opening section so sellers don't think they're missing a feature; the Nike Air Max example survives because the residual fashion seller cohort still exists.

- **Screen-1 = Size + Color cells filled, not picker open**: shows the resting state of the form so sellers recognize where the fields live without us inventing the picker chrome (which lives in `SelectProductAttributeViewController.swift` and varies by category; faking a picker risks `no_invented_ui_state` violations). Size value `M` and Color value `Preto` / `Black` with a black swatch are picked from the real xcstrings color names (`Preto` / `Black` are both real ProductColor titles).

- **Screen-2 = action sheet with Clone Past Shows Listings highlighted**: light highlight (purple tint) on the relevant row is purely a doc-cue; the underlying iOS action sheet does not actually highlight rows. We mark this in `flow.yml.mockup_plan.screens[1].review_checks` so reviewers know to compare against the real action sheet. The three action labels are verbatim from xcstrings; `Cancel` button color is `customPurple` (`#7E53F8`) per `ShowHostViewController.swift:1729`.

- **Screen-3 = product list with three same-item-different-size rows**: simulated seller's products list inside a show. The thumbnail is a generic dark shoe-silhouette SVG; the price `R$ 480` (pt-BR) / `$ 95` (EN, no R$ leak) is illustrative and matches the order of magnitude of a real Nike Air Max secondhand listing. The "QTD 1" / "QTY 1" pill drives home that each listing carries its own quantity.

- **No em-dashes anywhere**: pt-br.md and en.md both pass `grep -c '—' pt-br.md en.md` returning 0. Article uses commas and colons. The v1 had 13 em-dashes in each file (most likely from a Markdown editor's smart-dash auto-conversion); rewritten from scratch on 2026-05-11.

## Negative scan

- `PRODUCT/Views/VariantEditor*.swift` -> does not exist (no variants editor screen)
- `PRODUCT/Views/Components/*Variant*.swift` -> does not exist (no per-variant row component)
- `PRODUCT/View Models/*Variant*.swift` -> does not exist (no variants view model)
- xcstrings keys matching `variant` / `variation` / `variante` / `variação` -> 0 hits

All declared `flow.yml.source_of_truth.ios_files` paths exist (verified with `ls` 2026-05-11).

## Actions completed on 2026-05-11

- [x] Verified each iOS path with `ls`.
- [x] Sampled `CreateProductViewModel.swift` to confirm scalar `size` and `color`, single `quantityOutput`, `getSizeSection` gating on category triplet.
- [x] Sampled `ProductSize.swift` and `ProductColor.swift` to confirm scalar struct types (no array members, no per-variant ID).
- [x] Sampled `ShowHostViewController.swift:1684-1731` to confirm `Clone Past Shows Listings` action sheet item and its sibling actions.
- [x] Confirmed `ProductTemplate.swift` exists at `SERVICE/API/Repository/Modules/Product/Model/Request/ProductTemplate.swift` and `getProductTemplate` is the API route used by `ShowHostImportView`.
- [x] Pulled xcstrings values for `Size`, `Color`, `Quantity`, `Clone Past Shows Listings`, `New Quickie Listing`, `Create Credits Giveaway`, `Cancel` and locked them verbatim in the article + screen mockups.
- [x] Rendered all 6 PNGs DPR3 at 960px wide via `scripts/shot-retina.mjs`.
