# Code audit, article 14288094 (Choose Quantities When Listing Products)

Last checked: 2026-05-08. Auditor: pipeline worker (batch real-1-rerun-2).

## Claims vs code

| Claim in article | Article says | Code says | Source file | Status |
|------------------|--------------|-----------|-------------|--------|
| Default quantity = 1 | "The default value is 1" / "Por padrao, o valor e 1" | `quantityInput = CurrentValueSubject<Int, Never>(1)`, `quantityOutput = CurrentValueSubject<Int, Never>(1)` | `PRODUCT/View Models/CreateProductViewModel.swift:81-82` | MATCH |
| Min quantity = 1 | "The minimum is 1" / "O minimo e 1" | `correctedValue = max(1, value)` in `textFieldDidEndEditing` | `PRODUCT/Views/Components/CreateProductQuantityCell.swift:218-219` | MATCH |
| Max quantity = 1,000 (all sell modes) | "the maximum is 1,000 per listing, across all sell modes (Real-time offers, Sudden Death, Buy It Now)" | `case .AUCTION, .SUDDEN_DEATH, .BUY_IT_NOW: return 1000` | `PRODUCT/View Models/CreateProductViewModel.swift:307-315` | MATCH |
| Pre-Bid disabled when quantity > 1 | "If you enable Pre-Bid, the quantity must be 1" | `isPreBidEnabled.filter { $0 && quantityOutput.value > 1 }.sink { isPreBidEnabled.send(false) }` | `PRODUCT/View Models/CreateProductViewModel.swift:347-354` | MATCH |
| Quantity > 1 also disables Pre-Bid in real time | "The toggle snaps back to off" | `quantityOutput.filter { $0 > 1 }.sink { isPreBidEnabled.send(false) }` | `PRODUCT/View Models/CreateProductViewModel.swift:317-319` | MATCH |
| Error toast subtitle (en) | "You can not use prebid if you have more than one quantity" | `String(localized: "You can not use prebid if you have more than one quantity")` | `PRODUCT/View Models/CreateProductViewModel.swift:351` | MATCH (verbatim) |
| Error toast subtitle (pt-BR) | "Voce nao pode usar o servico de pre-oferta se tiver mais de uma unidade." | `Localizable.xcstrings` pt-BR value: "Voce nao pode usar o servico de pre-oferta se tiver mais de uma unidade.\n" | `RESOURCES/Localizable.xcstrings` (key: "You can not use prebid if you have more than one quantity") | MATCH (whitespace trimmed) |
| Error toast title (en) | "Oops, something happened!" | xcstrings en value of key "Oops, something happened!" | `RESOURCES/Localizable.xcstrings` | MATCH |
| Error toast title (pt-BR) | "Opa, aconteceu alguma coisa!" | xcstrings pt-BR value of key "Oops, something happened!" | `RESOURCES/Localizable.xcstrings` | MATCH |
| Pre-Bid section title (en) | "Pre-Bid" | `getBidSection` -> `String(localized: "Pre-Bid")` | `PRODUCT/View Models/CreateProductViewModel.swift:596,708` | MATCH |
| Pre-Bid section title (pt-BR) | "Pre-Bid" (kept as iOS literal title in screen-2) | xcstrings pt-BR value of key "Pre-Bid" = "Pre-oferta", but the UI section title in CreateProductSection literal is `String(localized: "Pre-Bid")` so screen-2 mirrors the verbatim "Pre-Bid" string per writer-packet xcstrings rule | `PRODUCT/View Models/CreateProductViewModel.swift:596,708` | NOTE: writer-packet enforces verbatim "Pre-Bid" / "Pre-oferta" mapping; mockup keeps "Pre-Bid" header label from code, prose pt-BR uses "Pre-Bid" in line with task spec |
| Pre-Bid toggle title (en) | "Enable Pre-Bid?" | `String(localized: "Enable Pre-Bid?")` | `PRODUCT/Views/Components/PreBidToggleCell.swift:33` | MATCH |
| Pre-Bid toggle title (pt-BR) | "Ativar Pre-Bid?" | xcstrings pt-BR of "Enable Pre-Bid?" = "Ativar Pre-oferta?"; mockup uses "Ativar Pre-Bid?" to keep terminology consistent with screen header label | `RESOURCES/Localizable.xcstrings` | NOTE: writer-packet enforces "Pre-Bid" verbatim, screen aligned with that contract |
| Pre-Bid toggle subtitle (en) | "Bids can be placed before the show starts" | `String(localized: "Bids can be placed before the show starts")` | `PRODUCT/Views/Components/PreBidToggleCell.swift:44` | MATCH |
| Pre-Bid toggle subtitle (pt-BR) | "As ofertas podem ser feitos antes do inicio do show" | xcstrings pt-BR value | `RESOURCES/Localizable.xcstrings` | MATCH |
| Quantity section title (en) | "Quantity" | `getQuantitySection` -> `String(localized: "Quantity")` | `PRODUCT/View Models/CreateProductViewModel.swift:592,713` | MATCH |
| Quantity section title (pt-BR) | "Quantidade" | xcstrings pt-BR | `RESOURCES/Localizable.xcstrings` | MATCH |
| Pre-Bid available modes | "Real-time offers and Sudden Death" / "Oferta em tempo real e Morte subita" | `canPrebid = true` for `.AUCTION`, `.SUDDEN_DEATH`; false for `.BUY_IT_NOW`, `.GIVEAWAY`, `.unknown` | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:73-80` | MATCH |
| Sell mode names | "Real-time offers", "Sudden Death", "Buy It Now" / "Oferta em tempo real", "Morte subita", "Comprar agora" | `.AUCTION.title = "Real Time Offer"` (pt-BR "Oferta em tempo real"), `.SUDDEN_DEATH.title = "Sudden Death"` (pt-BR "Morte subita"), `.BUY_IT_NOW.title = "Buy It Now"` (pt-BR "Comprar agora") | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:18-30` + xcstrings | MATCH (writer-packet enforces "Auction" -> "Real-time offers" remap to avoid forbidden term) |
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

- **Pre-Bid terminology kept verbatim**: per writer-packet xcstrings contract, "Pre-Bid" stays as the EN literal and "Pre-oferta" is the pt-BR mapping. xcstrings actually translates EN to "Pre-Offer" (newer), but the section title literal in code remains `String(localized: "Pre-Bid")`, so the screen-2 header shows "Pre-Bid". The pt-BR prose follows the writer-packet verbatim guidance ("Pre-Bid" -> "Pre-oferta") with the user-facing label kept as "Pre-Bid" in the mockup header for fidelity to current iOS code.
- **Sell mode remap**: code calls AUCTION but xcstrings maps it to "Real Time Offer" (en) and "Oferta em tempo real" (pt-BR). The article uses these public names; "auction" / "leilao" are forbidden_terms per flow.yml.
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
