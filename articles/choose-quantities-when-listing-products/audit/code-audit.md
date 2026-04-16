# Code audit, article 14288094 (Choose Quantities When Listing Products)

Last checked: 2026-04-16. Auditor: Aymar Dumoulin (via pipeline).

## Claims vs code

| Claim in article | Article says | Code says | Source file | Status |
|------------------|--------------|-----------|-------------|--------|
| Default quantity | "set to 1" (implied by stepper at 1) | `quantityInput = CurrentValueSubject<Int, Never>(1)`, `quantityOutput = CurrentValueSubject<Int, Never>(1)` | `CreateProductViewModel.swift:81-82` | OK |
| Min quantity | "minimum is 1" | `textFieldDidEndEditing: correctedValue = max(1, value)` | `CreateProductQuantityCell.swift:219` | OK |
| Max quantity, all modes | "maximum is 1,000 per listing, across all sell modes" | `case .AUCTION, .SUDDEN_DEATH, .BUY_IT_NOW: return 1000` | `CreateProductViewModel.swift:307-311` | OK |
| Pre-Bid disabled on quantity > 1 | "If you enable Pre-Bid, the quantity must be 1" | `filter { $0 && quantityOutput.value > 1 }` then `isPreBidEnabled.send(false)` | `CreateProductViewModel.swift:347-352` | OK |
| Error toast string | "You can not use prebid if you have more than one quantity" | `String(localized: "You can not use prebid if you have more than one quantity")` | `CreateProductViewModel.swift:351` | OK (character-for-character) |
| Toast title | "Oops, something happened!" | `title: String(localized: "Oops, something happened!")` | `CreateProductViewController.swift:586` | OK |
| Pre-Bid available modes | "Real-time offers and Sudden Death" (FAQ) | `canPrebid = true` for `.AUCTION, .SUDDEN_DEATH` only | `ShowSaleType.swift:73-78` | OK |
| Pre-Bid NOT available modes | Implicit: not on Buy It Now | `canPrebid = false` for `.BUY_IT_NOW, .GIVEAWAY, .unknown` | `ShowSaleType.swift:77-78` | OK (implicit but consistent) |
| Feature name in prose | "Pre-Bid" (hyphen, capital) | Section title `String(localized: "Pre-Bid")`, toggle title `"Enable Pre-Bid?"` | `CreateProductViewModel.swift:596`, `PreBidToggleCell.swift:33` | OK |
| Sell modes mentioned | "Real-time offers, Sudden Death, Buy It Now" | `.AUCTION.title = "Real-time offers"`, `.SUDDEN_DEATH.title = "Sudden Death"`, `.BUY_IT_NOW.title = "Buy It Now"` | `ShowSaleType.swift:18-26` | OK |
| Giveaway omission | Not mentioned | `.GIVEAWAY` removes the Quantity section entirely (`updatedSections.removeAll...`) | `CreateProductViewModel.swift:605-616` | OK (intentional, GIVEAWAY is separate flow) |
| Buyer purchase limit | "each purchase covers one unit" | Backend-owned transaction flow | n/a | UNVERIFIED in iOS client, trusted from product contract |
| Auto-start next unit (Real-time / Sudden Death) | "The next unit starts automatically" | Backend-owned show lifecycle | n/a | UNVERIFIED in iOS client, trusted from product contract |
| Sold out marking | "product is automatically marked sold out" | Backend sets `sold_out` status | n/a | UNVERIFIED in iOS client, trusted from product contract |

## Visual fidelity

| Mockup | File | Compared against | Result |
|--------|------|------------------|--------|
| `choose-quantities-when-listing-products__quantity-stepper.png` | `help-center/assets/mockups/` | `CreateProductQuantityCell.swift`: title 17pt rounded semibold, HStack spacing 12 centered, two 32x32 `JambleButton(.secondary)` circles with SF Symbol minus/plus, center textfield with "1" | MATCH layout and content. Buttons rendered as light-gray circles with Unicode minus (U+2212) and plus; visually equivalent to SF Symbol render. |
| `choose-quantities-when-listing-products__prebid-error-toast.png` | `help-center/assets/mockups/` | `JambleIndicatorView` with state `.error`, light theme: white bg, corner 12, shadow, horizontal stack spacing 8, 32x32 icon, title `body.L.semibold`, subtitle `body.M.regular`, both `content.primary` (#162233) | MATCH layout and text. Error icon recreated in SVG (red circle #D92C20 per design system, white exclamation) rather than embedding the real `icon_error_status.png` asset. Visual equivalent. Avoids base64 handling (see Golden Rule #6). |

## Decisions

- **Icon recreated in SVG, not embedded**: the real `icon_error_status` asset is a PNG. Inline base64 PNG embedding in HTML was the root cause of the session crash on 2026-04-16 (data-URI auto-attach). For this and future mockups, recreate simple status icons (error, success, warning) as inline SVG using design-system tokens instead of embedding the raster asset. Cleaner, crisper, no binary handling risk. Already documented as Golden Rule #6 in `process/README.md`.
- **Stepper buttons rendered as circles**: iOS `JambleButton(.secondary)` with `width=height=32` is effectively a circle (pill `border-radius: 50%`). Match confirmed.
- **Article terminology fix**: article formerly used "pre-offer" / "pre-offers" (invented copy). Per "never invent copy" rule, rewritten to use "Pre-Bid" (matches UI section title + toggle label). The error toast quote preserves the exact lowercase code string "prebid".

## Actions completed on 2026-04-16

- [x] Sampled `CreateProductQuantityCell.swift`, confirmed default/min/stepper layout.
- [x] Sampled `CreateProductViewModel.swift`, confirmed max = 1000 for all non-GIVEAWAY sale types.
- [x] Sampled `PreBidToggleCell.swift`, confirmed UI label "Enable Pre-Bid?" and section title "Pre-Bid".
- [x] Sampled `ShowSaleType.swift`, confirmed `canPrebid` truth table.
- [x] Sampled `JambleIndicatorView.swift`, confirmed toast structure (state, title, subtitle, icon, layout).
- [x] Sampled `CreateProductViewController.swift:584-588`, confirmed toast title "Oops, something happened!" and subtitle = the error message.
- [x] Verified both PNGs render at retina (1104x558 and 1104x480, deviceScaleFactor: 3).
- [x] Verified both URLs return HTTP 200 on `raw.githubusercontent.com`.
- [x] Verified Intercom response post-PUT shows both img tags mirrored to intercom-attachments-1.com.

## Actions deferred

- [ ] Verify backend-owned claims (buyer purchase limit, next-unit auto-start, sold-out marking) against the backend repo. Trusted from product contract for now.
- [ ] Rasterize real `icon_error_status.png` to PDF or embed as `<img>` URL for stricter visual parity. Current SVG recreation is a design-token-accurate equivalent, DEFERRED.
