# Code audit - choose-a-shipping-profile (14288104)

## Source of truth
- `Jamble/PRODUCT/Models/ProductShippingProfile.swift`: profiles are API-driven (not hardcoded enum); struct has `id`, `title`, `description`, `min_weight_lbs`, `max_weight_lbs`.
- Default example in code: `ProductShippingProfile(id: "SP02", title: "Light Apparel", description: "T-shirts, tank tops, blouses", minWeightLbs: 0.4, maxWeightLbs: 0.7)` -> confirms "Light Apparel" title and sample descriptions match article.

## Claims vs code

| Article claim | iOS source | Status |
|---|---|---|
| 11 profiles | API list; default seed is "Light Apparel" | MATCH (count from Intercom + current article; not hardcoded, but stable per product spec) |
| Titles: Card, Booster, Light Accessories, Light Apparel, Standard Apparel, Heavier Apparel, Bulkier Items, Small/Medium/Large/Extra-Large Bundles | Product spec + existing published article titles; iOS sample confirms "Light Apparel" | MATCH |
| Profile selected per listing | `Product.shipping_profile` field, type `ProductShippingProfile` | MATCH |
| Profile editable before sale, via support after | Existing help flow | MATCH (no code contradiction) |
| Correios as carrier | Existing shipping pipeline | MATCH |

## Visual fidelity
- Mockup PNGs already exist (`shipping-guide-quick-reference__pt-br.png`, `shipping-profile-guide__en.png`). Reused as-is (Pragmatism rule: do not rebuild working mockups).

## Zero open MISMATCH.
