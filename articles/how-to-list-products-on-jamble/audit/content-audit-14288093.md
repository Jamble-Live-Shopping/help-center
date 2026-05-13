# Content Audit — how-to-list-products-on-jamble

Date: 2026-05-12
Intercom ID: 14288093

## Editorial Checks

| Check | Result |
| --- | --- |
| Heading hierarchy | Pass — one H1 and H2 sections only. |
| Source-backed labels | Pass — sale-mode terms follow batch real-2 decisions. |
| No stale images | Pass — all cross-slug image references were removed and replaced with three iOS-anchored listing-flow mockups. |
| Brazil currency | Pass — PT-BR uses R$; EN follows the validator convention and says local currency / $5. |
| User value | Pass — seller gets a compact listing checklist plus screenshots of the high-salience form areas. |

## Stale-feature Audit

| Claim / feature | Source checked | Status | Verdict |
| --- | --- | --- | --- |
| Title 60 characters | CreateProductViewModel | Current | Keep |
| Description 120 characters | CreateProductViewModel | Current | Keep |
| R$ minimum price | Price.swift + CreateProductViewModel | Current | Keep |
| Quantity up to 1,000 | CreateProductViewModel | Current | Keep |
| Pre-offer disabled above quantity 1 | CreateProductViewModel | Current | Keep |
| Old images from `new-seller-guide-to-listing-products` | Existing markdown | Stale | Removed |
| USD pricing | Existing EN article | Stale for BR | Removed |
| Listing form mockups | CreateProductViewController + component cells | Current | Added |

## Verdict

Factory-grade central seller guide. The added mockups are limited to the areas where they reduce seller ambiguity: required details, selling mode/price, and quantity/pre-offer/shipping.
