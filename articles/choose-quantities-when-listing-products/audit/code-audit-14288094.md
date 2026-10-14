# Code audit, article 14288094 (Choose Quantities When Listing Products)

## 2026-10-14 wave 2 rewrite (supersedes the tables below)

Sources: iOS tag `5.10.1`, Android tag `v5.10.0`, `jamble_backend` origin/main (291e133b5), Jamble-Website origin/main. The product form is now server-driven on all clients (`get_product_edition_fields`), so the old `CreateProductQuantityCell` / pre-bid error toast rows below are historical.

| Claim in article | Code says | Source file | Status |
|---|---|---|---|
| Field **Quantidade**, starts at 1, min 1, a max exists and disables **+** | `key="available_count"`, `title=Localized(en="Quantity", pt="Quantidade")`, `min_value=1`, `max_value=1000`; `+` button `.disabled(quantity >= range.upperBound)`; no text shows the max | jamble_backend `src/services/product_service.py` (get_product_edition_fields, available_count field); iOS `PRODUCT/Views/SwiftUI/Components/CreateProductQuantitySectionView.swift` | MATCH (number kept out of the article, code-only value) |
| **Lote** toggle with description "Várias unidades idênticas vendidas como um único anúncio" | `key="is_bundle"`, `title=Localized(en="Bundle", pt="Lote")`, description pt as quoted | `src/services/product_service.py` | MATCH |
| **Unidades do lote** appears when Lote is on, starts at 2 | `bundle_count` field only if `selection.get("is_bundle")`, default 2, `min_value=2` | `src/services/product_service.py` | MATCH |
| Shipping counts every bundle unit | comment + `resolve_item_units` unfolds bundle_count x quantity | `src/entities/item_spec.py` (resolve_item_units) | MATCH (stated generally) |
| **Ativar pré-ofertas** only for live products, Ofertas em Tempo Real / Morte Súbita, quantity 1; disappears when quantity > 1 | `is_prebid_enabled` only kept when `show` and type in `[auction, sudden_death]` and `available_count <= 1`, else popped; title `pt="Ativar pré-ofertas"` | `src/services/product_service.py` | MATCH |
| Multi-unit purchase only for live Comprar Agora and Loja | `quantity_count > 1 and not (product.is_show_buy_it_now or (not product.is_show))` raises | `src/utils/purchase_intent_manager.py` (perform_product_availability_checks) | MATCH |
| Buyer picks quantity at checkout / in cart, up to a limit shown | `quantity_rule` (min/max/is_editable); iOS stepper when `rule.max > rule.min`; cart row stepper | `src/schemas/cart.py`, `src/entities/purchase_intent.py`; iOS `LIVE_SHOPPING/Checkout/View/ShowCheckoutView.swift`, `CART/Views/CartItemRow.swift` | MATCH (limit value not stated) |
| Timed sales: one unit per sale, seller starts the next one | no auto restart found; stock decremented per purchase (`product.available_count -= item.quantity`) | `src/services/purchase_intent_service.py` | MATCH (old "next unit starts automatically" claim removed) |
| "3 restantes" | xcstrings `%lld left` -> pt-BR `%lld restantes` | iOS `RESOURCES/Localizable.xcstrings` | MATCH |

Mockups removed: screen-1 (old stepper layout), screen-2/3 (pre-offer conflict + error toast that the server-driven form no longer shows).

Last checked: 2026-05-11. Auditor: pipeline worker (batch real-1-rerun-2).

## 2026-05-11 patch summary (PR #96 review correction)

The 2026-05-08 audit recorded a confused interpretation of the xcstrings
contract: the section/toggle titles were declared "kept verbatim" as the
iOS source key (`Pre-Bid`, `Enable Pre-Bid?`), and the sell-mode label
`Morte súbita` was written without its accent. The 2026-05-11 PR review
verified the xcstrings ground truth at
`/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings`
and corrected the article + mockups:

- key `Pre-Bid` → user-facing pt-BR `Pré-oferta`, EN `Pre-Offer`
- key `Sudden Death` → user-facing pt-BR `Morte súbita` (accented), EN `Sudden Death`
- key `Auction` → user-facing pt-BR `Oferta em tempo real`, EN `Real Time Offer`

The pt-br.md, en.md, metadata.yml, screen-2 HTMLs, and screen-2 PNGs now
use the localized values. `flow.yml.content_contract.forbidden_terms`
was inverted-fix: previously banned `pre-offer` / `pre-offers` (the
CORRECT EN labels); now bans `regex:\bPre-Bid\b` to lock the source-key
leak. The verbatim iOS error toast text (`prebid` one-word lowercase /
`pre-oferta` no accent in pt-BR) is preserved because it IS the literal
iOS error message string, not the section title.

The table rows below were rewritten on 2026-05-11 to reflect the
corrected article state. Source files cited are unchanged.

## Claims vs code

| Claim in article | Article says | Code says | Source file | Status |
|------------------|--------------|-----------|-------------|--------|
| Default quantity = 1 | "The default value is 1" / "Por padrao, o valor e 1" | `quantityInput = CurrentValueSubject<Int, Never>(1)`, `quantityOutput = CurrentValueSubject<Int, Never>(1)` | `PRODUCT/View Models/CreateProductViewModel.swift:81-82` | MATCH |
| Min quantity = 1 | "The minimum is 1" / "O minimo e 1" | `correctedValue = max(1, value)` in `textFieldDidEndEditing` | `PRODUCT/Views/Components/CreateProductQuantityCell.swift:218-219` | MATCH |
| Max quantity = 1,000 (all sell modes) | "the maximum is 1,000 per listing, across all sell modes (Real Time Offer, Sudden Death, Buy It Now)" / pt-BR "(Oferta em tempo real, Morte súbita, Comprar agora)" | `case .AUCTION, .SUDDEN_DEATH, .BUY_IT_NOW: return 1000` | `PRODUCT/View Models/CreateProductViewModel.swift:307-315` | MATCH |
| Pre-Offer disabled when quantity > 1 | EN: "If you enable Pre-Offer, the quantity must be 1" / pt-BR: "Se voce ativar Pré-oferta, a quantidade precisa ser 1" | `isPreBidEnabled.filter { $0 && quantityOutput.value > 1 }.sink { isPreBidEnabled.send(false) }` | `PRODUCT/View Models/CreateProductViewModel.swift:347-354` | MATCH (article uses xcstrings-localized user-facing label `Pre-Offer` / `Pré-oferta`; iOS source-key remains `Pre-Bid` in code only) |
| Quantity > 1 also disables Pre-Offer in real time | "The toggle snaps back to off" / "O toggle volta para desligado" | `quantityOutput.filter { $0 > 1 }.sink { isPreBidEnabled.send(false) }` | `PRODUCT/View Models/CreateProductViewModel.swift:317-319` | MATCH |
| Error toast subtitle (en) | "You can not use prebid if you have more than one quantity" | `String(localized: "You can not use prebid if you have more than one quantity")` | `PRODUCT/View Models/CreateProductViewModel.swift:351` | MATCH (verbatim) |
| Error toast subtitle (pt-BR) | "Voce nao pode usar o servico de pre-oferta se tiver mais de uma unidade." | `Localizable.xcstrings` pt-BR value: "Voce nao pode usar o servico de pre-oferta se tiver mais de uma unidade.\n" | `RESOURCES/Localizable.xcstrings` (key: "You can not use prebid if you have more than one quantity") | MATCH (whitespace trimmed) |
| Error toast title (en) | "Oops, something happened!" | xcstrings en value of key "Oops, something happened!" | `RESOURCES/Localizable.xcstrings` | MATCH |
| Error toast title (pt-BR) | "Opa, aconteceu alguma coisa!" | xcstrings pt-BR value of key "Oops, something happened!" | `RESOURCES/Localizable.xcstrings` | MATCH |
| Pre-Offer section title (en, user-facing) | "Pre-Offer" | iOS source key `Pre-Bid` in `getBidSection` -> `String(localized: "Pre-Bid")`; xcstrings EN value = "Pre-Offer" (user-facing) | `PRODUCT/View Models/CreateProductViewModel.swift:596,708` + `RESOURCES/Localizable.xcstrings` | MATCH (article + mockup use the xcstrings-resolved user-facing label `Pre-Offer`, not the source key) |
| Pré-oferta section title (pt-BR, user-facing) | "Pré-oferta" | iOS source key `Pre-Bid` in code resolves to xcstrings pt-BR value `Pré-oferta` (accented) | `PRODUCT/View Models/CreateProductViewModel.swift:596,708` + `RESOURCES/Localizable.xcstrings` | MATCH (screen-2 header + pt-br body use `Pré-oferta`) |
| Pre-Offer toggle title (en) | "Enable Pre-Offer?" | iOS source key `String(localized: "Enable Pre-Bid?")` resolves through xcstrings to EN value `Enable Pre-Offer?` | `PRODUCT/Views/Components/PreBidToggleCell.swift:33` + xcstrings | MATCH |
| Pré-oferta toggle title (pt-BR) | "Ativar Pré-oferta?" | xcstrings pt-BR value of "Enable Pre-Bid?" key = "Ativar Pré-oferta?" | `RESOURCES/Localizable.xcstrings` | MATCH (screen-2 mockup uses pt-BR user-facing value verbatim with accent) |
| Pre-Bid toggle subtitle (en) | "Bids can be placed before the show starts" | `String(localized: "Bids can be placed before the show starts")` | `PRODUCT/Views/Components/PreBidToggleCell.swift:44` | MATCH |
| Pre-Bid toggle subtitle (pt-BR) | "As ofertas podem ser feitos antes do inicio do show" | xcstrings pt-BR value | `RESOURCES/Localizable.xcstrings` | MATCH |
| Quantity section title (en) | "Quantity" | `getQuantitySection` -> `String(localized: "Quantity")` | `PRODUCT/View Models/CreateProductViewModel.swift:592,713` | MATCH |
| Quantity section title (pt-BR) | "Quantidade" | xcstrings pt-BR | `RESOURCES/Localizable.xcstrings` | MATCH |
| Pre-Offer available modes | "Real Time Offer and Sudden Death" / "Oferta em tempo real e Morte súbita" | `canPrebid = true` for `.AUCTION`, `.SUDDEN_DEATH`; false for `.BUY_IT_NOW`, `.GIVEAWAY`, `.unknown` | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:73-80` | MATCH (article uses xcstrings-localized user-facing labels) |
| Sell mode names | EN: "Real Time Offer", "Sudden Death", "Buy It Now" / pt-BR: "Oferta em tempo real", "Morte súbita", "Comprar agora" | `.AUCTION.title = "Real Time Offer"` (pt-BR "Oferta em tempo real"), `.SUDDEN_DEATH.title = "Sudden Death"` (pt-BR "Morte súbita"), `.BUY_IT_NOW.title = "Buy It Now"` (pt-BR "Comprar agora") | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:18-30` + xcstrings | MATCH. The xcstrings ground truth for `Auction` key maps to user-facing `Real Time Offer` (EN, singular, no hyphen) and `Oferta em tempo real` (pt-BR); the article body uses those values verbatim. `auction` / `leilao` stay in `forbidden_terms` policy. |
| Buy It Now banner shows items left | banner shows "3 left", "2 left" | `setItemsLeft` -> `itemsLeftLabel.text = String(localized: "\(itemsLeft ?? 0) left")` | `LIVE_SHOPPING/SaleView/View/Components/ShowBuyItNowBannerView.swift:111-115` | MATCH (string template "\(n) left", pt-BR "restantes" via xcstrings " left") |
| Sold-out marking when last unit sells | "When the last unit is sold, the product is marked sold out" | Backend-owned (transaction lifecycle), iOS only consumes `available_count` | n/a | TRUSTED from product contract; not directly verified in iOS client |
| Auto-start next unit (Real-time / Sudden Death) | "The next unit starts automatically" | Backend-owned show lifecycle | n/a | TRUSTED from product contract; not directly verified in iOS client |
| Buyer purchase limit per round | "each purchase covers one unit" | Backend-owned | n/a | TRUSTED from product contract; not directly verified in iOS client |
| Quantity disappears for GIVEAWAY | Article omits Giveaway | `getQuantitySection(order:)` -> `guard self.product?.showSaleType != .GIVEAWAY` returns nil | `PRODUCT/View Models/CreateProductViewModel.swift:711-713` | MATCH (intentional omission, Giveaway is a separate flow) |

## Visual fidelity

| Mockup | Source HTML | Compared against | Result |
|--------|-------------|------------------|--------|
| screen-1 (Quantity stepper) | `mockup-sources/screen-1__pt-br.html`, `mockup-sources/screen-1__en.html` | `CreateProductQuantityCell`: titleLabel rounded 17pt semibold, hStackView center spacing 12, two 32x32 `JambleButton(.secondary)` circles (SF Symbol minus/plus), centered textfield with "1" | MATCH layout: 320px phone, 12px margins, rounded label, two 32x32 circle buttons with Unicode minus/plus, centered "1" |
| screen-2 (Pre-Bid toggle on with Quantity 2) | `mockup-sources/screen-2__pt-br.html`, `mockup-sources/screen-2__en.html` | `PreBidToggleCell`: titleLabel 17pt semibold, subtitleLabel 15pt regular customBlue400, UISwitch with onTintColor `.customPurple` (#7E53F8). `CreateProductQuantityCell` stepper at value 2 | MATCH composed view: Quantity cell stepper at 2, Pre-Bid section header, toggle cell with title + subtitle + switch in ON state |
| screen-3 (error toast) | `mockup-sources/screen-3__pt-br.html`, `mockup-sources/screen-3__en.html` | `JambleIndicatorView` error state, light theme: white bg, corner 12, shadow, h-stack spacing 8, 32x32 icon, title body.L semibold, subtitle body.M regular, both content.primary (#162233) | MATCH layout. Error icon recreated as inline SVG (red circle #D92C20 + white exclamation) to avoid base64 PNG handling per Golden Rule #6 |

## Decisions

- **Pre-Offer terminology, xcstrings-localized (2026-05-11 correction)**: the iOS code uses `String(localized: "Pre-Bid")` as the source-key call site (`PRODUCT/View Models/CreateProductViewModel.swift:596,708` for the section title, `PRODUCT/Views/Components/PreBidToggleCell.swift:33` for the toggle title). The user does NOT see the source key; xcstrings resolves `Pre-Bid` to user-facing **`Pre-Offer`** (EN) and **`Pré-oferta`** (pt-BR, accented). The 2026-05-08 audit confused the source key with the user-facing label, and the article shipped with `Pre-Bid` in the body and mockups. Patched 2026-05-11: pt-br.md uses `Pré-oferta`, en.md uses `Pre-Offer`, screen-2 mockup headers + toggle titles updated to localized values, screen-2 PNGs re-rendered DPR3. `flow.yml.content_contract.forbidden_terms` adds `regex:\bPre-Bid\b` to lock the source-key leak; the verbatim iOS error toast text (`prebid` one-word lowercase + `pre-oferta` pt-BR no accent) is preserved because it is the literal iOS error string, not a section title.
- **Sell mode remap**: code calls AUCTION but xcstrings maps it to **`Real Time Offer`** (EN, singular, no hyphen) and **`Oferta em tempo real`** (pt-BR). The article uses these public names verbatim (en.md: `Real Time Offer`; pt-br.md: `Oferta em tempo real`). The 2026-05-08 audit + body had `Real-time offers` (plural, hyphenated) which drifted from xcstrings; patched 2026-05-11. `auction` / `leilao` stay as `forbidden_terms` per flow.yml policy.
- **Error icon recreated in SVG**: real `icon_error_status.png` asset is a raster. Inline SVG (red circle + white exclamation) is design-token equivalent and avoids base64 binary handling.

## Negative scan

None declared. All claims trace to one of the 6 ios_files entries.

## Actions completed on 2026-05-08

- [x] Verified existence of all 5 Swift files cited (path verification per task spec).
- [x] Sampled `CreateProductQuantityCell.swift` -> stepper UI, default = 1, min clamp = max(1, value).
- [x] Sampled `CreateProductViewModel.swift` -> `quantityInput/Output = 1`, max = 1000 for AUCTION/SUDDEN_DEATH/BUY_IT_NOW, Pre-Bid auto-disable on quantity > 1, error string verbatim.
- [x] Sampled `PreBidToggleCell.swift` -> "Enable Pre-Bid?" title, "Bids can be placed before the show starts" subtitle, switch onTintColor customPurple.
- [x] Sampled `ShowSaleType.swift` -> canPrebid truth table.
- [x] Sampled `ShowBuyItNowBannerView.swift` -> items-left label "\(itemsLeft) left".
- [x] Pulled pt-BR for all 9 xcstrings keys via Localizable.xcstrings.
- [x] Rendered 6 PNGs DPR3 at 960px wide.
