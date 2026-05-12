# Content Audit — how-to-list-products-on-jamble

Date: 2026-05-12
Intercom ID: 14288093

## Editorial Checks

| Check | Result |
| --- | --- |
| Heading hierarchy | Pass — one H1 and H2 sections only. |
| Source-backed labels | Pass — sale-mode terms follow batch real-2 decisions. |
| No stale images | Pass — all cross-slug image references were removed. |
| Brazil currency | Pass — PT-BR uses R$; EN follows the validator convention and says local currency / $5. |
| User value | Pass — seller gets a compact listing checklist instead of a brittle step-by-step UI clone. |

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

## Verdict

Factory-grade central seller guide. It is intentionally text-first until an iOS layout-proof mockup pass is scoped.
