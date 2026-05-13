# Code Audit — how-to-list-products-on-jamble

Date: 2026-05-12
Intercom ID: 14288093

## Source Review

| Source | Evidence | Article impact |
| --- | --- | --- |
| `CreateProductViewModel.swift:167-180` | Title is capped at 60 characters and description at 120 characters. | Article states the exact limits. |
| `CreateProductViewModel.swift:528-545` | Quick upload sections include photos, title, description, sell mode, quantity, pre-bid toggle, shipping profile, category, size, color, brand, condition, retail price. | Article separates required and optional fields without inventing a full screen. |
| `CreateProductViewModel.swift:780-804,836-858` | Required-field check includes title, quantity, price, shipping profile, category where present, and save assigns product fields. | Article says the app blocks saving when required fields are missing. |
| `CreateProductViewModel.swift:307-323,591-596,706-713,873-878` | Quantity clamps to 1..1000 for sell modes; quantity greater than 1 disables pre-offers; pre-offer is only added when eligible. | Article documents quantity/pre-offer interaction. |
| `CreateProductViewModel.swift:892-938` | Auction/Sudden Death/Buy It Now validate starting price against `currency.minPrice`; flash sale fields have separate validations. | Article describes price/start price safely. |
| `SellModeDefaultCell.swift:181-227` | Real-time offer, Sudden Death, and Buy It Now fields are configured with Start at/Price and timers. | Article summarizes mode differences without duplicating UI. |
| `CreateProductViewController.swift:323-412,740-888` | Quick listing sections route photos, title, description, sell mode, quantity, pre-offer toggle, shipping profile, and category cells. | Three mockups now show the central form areas instead of leaving the article text-only. |
| `SelectPhotoHeaderView.swift:19-57,79-104` + `SelectPhotoFirstCell.swift:18-31,61-87` | Photo header label, 3 recommended helper, and add-photo tile placement. | Listing-basics mockup uses the actual photo row shape and localized labels. |
| `ProductAttributeCell.swift:64-70,82-101,116-124` | Attribute rows use a vertical small label plus selected value and trailing chevron. | Category and shipping profile rows avoid the horizontal label/value false-negative class from batch real-2. |
| `CreateProductQuantityCell.swift:26-39,80-127` + `PreBidToggleCell.swift:31-58,67-99` | Quantity has a centered minus/value/plus control; pre-offer toggle has title/subtitle leading and switch trailing. | Quantity-shipping mockup mirrors the iOS parent layout and visible copy. |
| `ProductShippingProfile.swift:10-18,24-43` | Shipping profile carries title, description, and min/max weight display. | Article says profile should match the packaged item. |
| `Price.swift:194-222` | BRL symbol is R$, min price is 5.0, max price is 5000.0. | Article uses R$ and states R$ 5,00 minimum. |

## Negative Scan

| Removed claim | Reason |
| --- | --- |
| Cross-slug mockup images | Existing images referenced `new-seller-guide-to-listing-products`, not this article. |
| USD price examples | Brazil help center must use R$. |
| Product list/store absolute claim | The code supports multiple product upload modes; the article now focuses on show listing without saying every product is always listed only in a show. |
| Flash Sale as universal Buy It Now behavior | Flash sale validation exists, but this central listing article now points to the dedicated Buy It Now article instead of over-documenting. |

## Verdict

Ship-ready. The article is source-backed, replaces stale imagery with three iOS-anchored mockups, and uses visible_text contracts for localized labels.
