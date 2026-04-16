# Code audit, article 14288093 (How to List Products)

Last checked: 2026-04-16. Auditor: Aymar Dumoulin (via pipeline).

## Claims vs code

| Claim in article | Article says | Code says | Source file | Status |
|------------------|--------------|-----------|-------------|--------|
| Title max length | 60 characters | `maxLength = 60` (implied by article, not sampled directly) | `Jamble/PRODUCT/Views/Components/CreateProductTitleCell.swift` | OK (trusted) |
| Min price (BR) | $5.00 (EN) / R$ 5,00 (pt-BR) | `Currency.BRL.minPrice`, enforced via `ShowSaleSettings.startingPrice.minValue` binding in `SellModeDefaultCell.swift` | backend + iOS | OK |
| Max price (BR) | $5,000.00 (EN) / R$ 5.000,00 (pt-BR) | `Currency.BRL.maxPrice`, same binding | backend + iOS | OK |
| Photo limit | "Up to 10 photos" | Not found as a hardcoded string in iOS client (backend-driven or `UICollectionView` dataSource count) | `ProductPhotosSection.swift`, `SelectPhotoCell.swift` | UNVERIFIED in iOS client, trusted from product contract |
| Sell modes count | 3 (Real-time offers, Sudden Death, Buy It Now) | `ShowSaleType` enum has 4 cases: AUCTION, SUDDEN_DEATH, BUY_IT_NOW, GIVEAWAY | `Jamble/LIVE_SHOPPING/Show/Model/ShowSaleType.swift` | MISMATCH (intentional, GIVEAWAY is a separate flow) |
| Sell mode titles | "Real-time offers", "Sudden Death", "Buy It Now" | `.AUCTION.title = "Real-time offers"`, `.SUDDEN_DEATH.title`, `.BUY_IT_NOW.title` | `ShowSaleType.swift` | OK |
| Flash Sale on Buy It Now | "adds a percentage discount and a countdown timer" | `.BUY_IT_NOW` has `toggleView` for flash sale with `percentage` + `durationInSecs` fields | `SellModeDefaultCell.swift`, `SellModeToogleView.swift` | OK |
| Extra time on late bids | "extra time is added so other buyers can respond" | Backend behavior, not present in iOS client code | Server-side | UNVERIFIED in iOS, trusted from product contract |
| Shipping profiles (7) | Card, Booster, Light Accessories, Light Apparel, Standard Apparel, Heavier Apparel, Bulkier Items | `ShippingProfile` enum (not sampled in this pass) | `ShippingProfile.swift` | OK (trusted) |
| Condition grades (5) | New with Tags, New without Tags, Very Good, Good, Satisfactory | `ProductCondition` is a **struct** (not an enum) loaded dynamically from backend. Client has no hardcoded list. | `Jamble/PRODUCT/Models/ProductCondition.swift` | OK in iOS (struct is dynamic). Backend list needs separate verification. |

## Visual fidelity

| Mockup | File | Compared against | Result |
|--------|------|------------------|--------|
| prod-box1.png, Settings Apply to go Live | `help-center/assets/mockups/prod-box1.png` | `ProfileSettingsV2ViewController` settings row with `settings_apply_live` icon | MATCH layout. Icon in mockup is a play-triangle placeholder. Real asset is a PDF in `Assets.xcassets`, not directly embeddable as SVG. DEFERRED, low priority. |
| prod-box2.png, Pending Application | `help-center/assets/mockups/prod-box2.png` | `UIAlertController` native iOS alert, title + message + purple primary + blue secondary | MATCH |
| prod-box3.png, Your Show empty state | `help-center/assets/mockups/prod-box3.png` | `ShowHostProductListViewController` + `ShowHostDashboardViewController.swift`. Empty state: title "There is nothing here yet!", subtitle "Add products to your Show to gain visiblity", button "Add a listing" | MATCH layout and copy |
| prod-box4.png, Sell Mode | `help-center/assets/mockups/prod-box4.png` | `SellModeDefaultCell.swift`: radio 18px navy #162233, icon 24x24 `customBlue500`, title 17pt semibold, subtitle 13pt `customBlue400`, expand with `startingPrice` + `durationInSecs` fields | MATCH |
| prod-box5.png, Select Photos | `help-center/assets/mockups/prod-box5.png` | Photo grid with 4 slots, numbered purple badges | MATCH layout. Simulator side-by-side deferred. |
| prod-box6.png, Add Listing CTA | `help-center/assets/mockups/prod-box6.png` | `JambleButton` brand (pill, #7E53F8). The "Almost done" 3-field summary above the button is pedagogical (no exact equivalent in the listing form). | MATCH for button, summary accepted as pedagogical divergence. |

## Decisions

- **GIVEAWAY omission**: intentional. Giveaways are a separate flow (GiveawaySale module), not listed in the product creation form. Leave article as is.
- **ProductCondition is dynamic**: client has a struct, not an enum. The 5 conditions the article lists must be verified against the backend config or a test account's actual dropdown. Not blocking for this ship.
- **PhotoLimit not found in client**: trust the "10" figure. On a follow-up pass, verify with a test account by adding photos until the UI blocks.
- **Extra-time behavior**: backend-owned. Article's claim is accurate at the product level, but the exact seconds value is not documented in iOS. Safe as written.
- **prod-box1 icon**: play-triangle is placeholder. Real asset is PDF (not SVG), cannot inline-embed. DEFERRED.

## Actions completed on 2026-04-16

- [x] Sampled `ProductCondition.swift`, confirmed struct (not enum), updated status above.
- [x] Searched `PhotoLimit`, not found as hardcoded string in iOS.
- [x] Searched `extraTimeOnBid`, not present in iOS client (backend behavior).
- [x] Verified `settings_apply_live` asset exists as PDF (not directly embeddable as SVG in HTML).
- [x] Confirmed no R$ leaked back into EN body after word-diet edits.

## Actions deferred

- [ ] Verify backend `ProductCondition` list (requires backend repo access or test account).
- [ ] Rasterize real iOS settings icon to PNG/SVG for prod-box1 (low priority, current layout MATCHes).
- [ ] Sample `ShippingProfile` enum exhaustively (currently trusted).
