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

Ship-ready. The article is source-backed and avoids stale imagery.
