# Code audit, article 14288107 (flash-sales)

Source of truth: `Jamble-iOS` repo. Strings cross-referenced with `Jamble/RESOURCES/Localizable.xcstrings`.

## iOS source files referenced

| File | Purpose |
|---|---|
| `Jamble/PRODUCT/Views/Components/SellModeToogleView.swift` | Flash sale toggle row + icon |
| `Jamble/PRODUCT/Views/Components/SellModeDefaultCell.swift` | Buy It Now sell mode cell, reveals Discount + Timer fields when toggle on |
| `Jamble/PRODUCT/Views/Components/SellModeTextFieldView.swift` | Renders Price / Discount (%) / Timer (Seconds) text fields |
| `Jamble/PRODUCT/View Models/CreateProductViewModel.swift` | Validation: min 30 sec duration, error toasts |
| `Jamble/LIVE_SHOPPING/Host/ViewModel/ShowHostProductListViewModel.swift` | UIAlertController "Start as a Flash Sale or Buy It Now?" |
| `Jamble/LIVE_SHOPPING/SaleView/View/Components/ShowBuyItNowBannerView.swift` | Live banner "Flash Sale • X% OFF" + items left chip |
| `Jamble/LIVE_SHOPPING/Audience/View/Components/ShowSlideControl.swift` | Slide-to-buy button label "Buy Now: $X" |
| `Jamble/EXTENSIONS/Colors.swift` | `flashSaleGreen = rgb(0.79, 0.94, 0.04)` = `#C9F00A` (lime) |

## Claim, source, verdict

| Article claim (EN) | iOS source | Verdict |
|---|---|---|
| Flash sale toggle label is "Flash sale" | `SellModeToogleView.swift:51` `String(localized: "Flash sale")` | MATCH |
| Toggle pt-BR is "Venda relâmpago" | xcstrings: "Flash sale" -> "Venda relâmpago" | MATCH |
| Discount field placeholder is "Discount (%)" | `SellModeDefaultCell.swift:224` `String(localized: "Discount (%)")` | MATCH |
| Discount placeholder pt-BR is "Desconto (%)" | xcstrings: "Discount (%)" -> "Desconto (%)" | MATCH |
| Timer field placeholder is "Timer (Seconds)" | `SellModeDefaultCell.swift:227` | MATCH |
| Timer pt-BR is "Duração (segundos)" | xcstrings: "Timer (Seconds)" -> "Duração (segundos)" | MATCH |
| Discount range 10 to 90 percent | `SellModeDefaultCell.swift:224` `minValue: 10, maxValue: 90` | MATCH |
| Timer minimum 30 seconds | `CreateProductViewModel.swift:923` validator rejects `< 30` with toast "Flash Sale duration be at least 30 seconds." | MATCH |
| Timer maximum 5 minutes (300 seconds) | `SellModeDefaultCell.swift:227` `maxValue: 300` | MATCH (v1 article said "10 minutes / 600 seconds", FIXED in v2) |
| Default duration 60 seconds | `SellModeDefaultCell.swift:220` `?? 60` | MATCH |
| Picker title "Start as a Flash Sale or Buy It Now?" | `ShowHostProductListViewModel.swift:190` | MATCH |
| Picker pt-BR "Começar como uma venda rápida ou comprar agora?" | xcstrings | MATCH |
| Picker buttons: Flash Sale / Buy It Now / Later | `ShowHostProductListViewModel.swift:192-194` | MATCH |
| Picker pt-BR buttons: Venda relâmpago / Comprar agora / Mais tarde | xcstrings | MATCH |
| Picker is a native UIAlertController, not a custom radio list | `.showAlertConfirmation(in: vc, ...)` => UIAlertController | MATCH (v1 mockup invented a custom radio picker, FIXED in v2) |
| Live banner reads "Flash Sale • X% OFF" with bullet | `ShowBuyItNowBannerView.swift:106` `" • \(Int(discount))% OFF"` | MATCH (v1 article used hyphen "Flash Sale - X% OFF", FIXED in v2) |
| Banner color is `flashSaleGreen` lime | `Colors.swift:364-367` rgb(0.79, 0.94, 0.04) = #C9F00A | MATCH (v1 mockup used "bright green", actual color is lime) |
| "X left" pill | `ShowBuyItNowBannerView.swift:114` `String(localized: "\(itemsLeft ?? 0) left")` | MATCH |
| pt-BR "X restantes" | xcstrings: "%lld left" plural -> "%lld restantes" | MATCH |
| Slide button label "Buy Now: $price" | `ShowSlideControl.swift:228` `"Buy Now: \(numberFormatter.string(...))"` | MATCH |
| Buy It Now sell mode subtitle | xcstrings: "Offer a discount on an item during a limited time." -> "Ofereça um desconto em um item durante um período limitado." | MATCH |
| Flash Sale only available on Buy It Now products | `ShowHostProductListViewModel.swift:173-205` (switch on .BUY_IT_NOW only) | MATCH |
| Pinned product behavior | `ShowHostViewModel.swift:244` `pinProduct(_, isFlashSale, ...)` | MATCH |

## v1 -> v2 changes (mismatches FIXED)

1. Timer maximum was claimed "10 minutes / 600 seconds" in v1 body. iOS code says max 300 (5 min). Fixed.
2. Live banner used hyphen "Flash Sale - X% OFF" in v1 alt text. iOS uses bullet "Flash Sale • X% OFF". Fixed.
3. v1 mockup of mode picker rendered as custom radio list. iOS uses native UIAlertController. Rebuilt as iOS-faithful UIAlertController in v2.
4. v1 example used "Nike Air Max 90" (fashion). BR market is collectibles only. Switched to "Pikachu Holo, PSA 9".
5. v1 banner color was generic green. iOS `flashSaleGreen` is `#C9F00A` (lime). Fixed in v2 mockup.
6. v1 4-column markdown pricing table broke on mobile. Replaced with `pricing-chart` PNG mockup.

## Open MISMATCH count: 0

All article claims verified against Swift source. Ship-ready.
