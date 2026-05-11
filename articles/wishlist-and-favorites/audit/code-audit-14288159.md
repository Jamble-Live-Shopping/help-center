# Code audit, article 14288159 (wishlist-and-favorites)

Date: 2026-05-08 (rerun-2 patch on the 2026-05-06 audit)
Source iOS: Jamble-iOS develop. Sources cited in flow.yml.
xcstrings: `Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings`
Asset: `Jamble-iOS/Jamble/RESOURCES/Assets.xcassets/bookmark_heart_white_icon.imageset/bookmark_heart_white_icon.svg`

## CRITICAL nuance pinned at the top (post PR #92, rerun-2)

Two facts that the rerun-2 worker MUST keep aligned across mockups, audit, pt-br.md and en.md:

1. **Asset name vs visual: the iOS asset is named `bookmark_heart_white_icon` but renders a HEART, not a flag/bookmark glyph.** The original v1 mockup shipped a flag-shaped SVG path inferred from the asset name. That was the canonical false negative that triggered PR #92 rule 10e. Real shape: see `bookmark_heart_white_icon.svg` (`viewBox="0 0 15 14"`, single closed-curve path with two top lobes, classic two-lobed heart). Mockups now embed the file's `<path d="M7.49651...">` verbatim. Body copy reads "ícone de coração" / "heart icon" so the buyer matches the visual.
2. **xcstrings key `Bids` resolves to "Offers" (en) / "Ofertas" (pt-BR), NOT "Bids".** The iOS source `WishlistPage.swift:16` is `String(localized: "Bids")` but the en localisation in `Localizable.xcstrings` is "Offers". The user-facing tab label is therefore "Bookmarks / Offers" in EN and "Favoritos / Ofertas" in pt-BR. en.md, en mockups, body copy and FAQ all use **Offers**. Treating the source key as the literal label was the rerun-1 mistake; rerun-2 corrects it.

## Claims article vs source code

| Article claim | Source | Verdict |
|---|---|---|
| Wishlist lives on the profile page | PROFILE/View Models/ProfileBottomViewModel.swift (iterates WishlistPage.allCases and instantiates WishlistPageViewController via the profile bottom container) | MATCH |
| Two tabs: Favoritos (key `Bookmarks` -> en `Bookmarks`, pt-BR `Favoritos`) and Ofertas (key `Bids` -> en `Offers`, pt-BR `Ofertas`) | WISHLIST/Models/WishlistPage.swift:15-16 case .favorites: String(localized: "Bookmarks") + case .activeBids: String(localized: "Bids") + xcstrings localizations en `Bids` = "Offers", pt-BR `Bids` = "Ofertas" | MATCH (en label is "Offers", not "Bids") |
| Empty state title "Start Exploring Deals" / "Comece a explorar as ofertas" | WISHLIST/ViewModels/WishlistPageViewModel.swift:50 + xcstrings pt-BR `Start Exploring Deals` = "Comece a explorar as ofertas" | MATCH |
| Empty state subtitle "Discover deals and save your favorite items." / "Descubra ofertas e salve seus itens favoritos." | WISHLIST/ViewModels/WishlistPageViewModel.swift:51 + xcstrings pt-BR | MATCH |
| Heart bookmark icon on a product photo toggles save | PRODUCT/Views/SwiftUI/Components/ProductPhotosSection.swift:51 Image("bookmark_heart_white_icon") inside a `Button(action: viewModel.bookmarkProduct)` + ProductSocialActionsSection.swift:32 same asset under a Bookmark/Bookmarked toggle | MATCH |
| Heart bookmark button on the show preview / sticky CTA | PRODUCT/Views/SwiftUI/Components/ProductStickyActionSection.swift:355 (Save the Show button) + :384 (Bookmark Item button), both Image("bookmark_heart_white_icon") | MATCH |
| `bookmarkProduct` toggles bookmark / unbookmark | PRODUCT/View Models/ProductViewModel.swift bookmarkProduct method | MATCH |
| `bookmarkShow` available on the show preview | PRODUCT/View Models/ProductViewModel.swift bookmarkShow method | MATCH |
| Notification permission requested at first bookmark | WISHLIST/Views/WishlistPageViewController.swift:114 PermissionSettings().requestNotificationAuthorizationIfNeeded(type: .bookmark) | MATCH |
| Bookmarked shows live under Settings > Bookmarked shows (pt-BR Programas marcados) | xcstrings Bookmarked shows -> "Programas marcados" | MATCH |
| Notification "Bookmarked product from show" | iOS notification settings UI Live Shows section (xcstrings) | MATCH |
| Saving a product does not identify the buyer to the seller | Architectural: no seller-side endpoint exposes per-product saver identity in the iOS surface. Article phrased as a privacy assertion ("does not identify you") rather than a quantitative claim about totals | MATCH (negative claim) |

## Visual fidelity

| Mockup | iOS-source anchor | pt-BR strings | Saved-state colour | Verdict |
|---|---|---|---|---|
| product-bookmark-cta__pt-br.png | `bookmark_heart_white_icon` SVG verbatim from xcassets, embedded with xcassets comment + role=img + alt + aria-label; pill background `#F14A22` mirrors `UIColor.liveRed` (rgb 241,74,34) per EXTENSIONS/Colors.swift:252-256 | "R$ 1.450,00", body callout "ícone de coração" / "Favoritos" | liveRed pill, white heart fill | MATCH |
| product-bookmark-cta__en.png | same, alt + aria reads "heart icon" | "$1,450.00", body callout "heart icon" / "Bookmarks" | liveRed pill, white heart fill | MATCH |
| wishlist-tabs__pt-br.png | tabs "Favoritos" + "Ofertas" + filled heart pills on every saved card | xcstrings pt-BR keys above | liveRed circles | MATCH |
| wishlist-tabs__en.png | tabs "Bookmarks" + "Offers" + filled heart pills | xcstrings en localisations | liveRed circles | MATCH (en uses Offers, NOT Bids) |
| wishlist-empty-state__pt-br.png | empty illustration uses the same heart SVG, scaled, with `liveRed` fill on a tinted halo | "Comece a explorar as ofertas" / "Descubra ofertas e salve seus itens favoritos." | liveRed heart on cream halo | MATCH |
| wishlist-empty-state__en.png | mirror | "Start Exploring Deals" / "Discover deals and save your favorite items." | liveRed heart on cream halo | MATCH |

## Notes

- "Wishlist" itself has no xcstrings key. The article uses "Lista de desejos" as a descriptive pt-BR heading; the in-app surface is reached by tapping the Favoritos / Ofertas tabs from the profile.
- The product-bookmark-cta mockup was re-rendered on 2026-05-08 to drop the previously illustrative flag/bookmark glyph (path `M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z`, a Feather-style flag shape) and replace it with the verbatim heart path from `bookmark_heart_white_icon.svg`.
- The wishlist-tabs and wishlist-empty-state mockups received the same heart-SVG correction in the same pass.
- The body copy was patched in lockstep: "ícone de marcador" / "bookmark icon" -> "ícone de coração" / "heart icon", both pt-BR and EN, plus FAQ entries that referenced the old label.
- en.md tab labels and FAQ entries were patched from "Bids" to "Offers" to match the xcstrings en value of the `Bids` key. The pt-BR side already used "Ofertas".
- flow.yml mockup_plan now anchors each screen with `required_icons: [bookmark_heart_white_icon]` + `review_checks: [icons_match_ios_source, labels_match_xcstrings, no_invented_ui_state]` + screen-scoped `html_must_contain` lists per locale, satisfying PR #92 rule 10e (Option A: real-icon anchor).

## Verdict

Zero MISMATCH against the cited iOS sources. Article is grounded in real xcstrings, the real `bookmark_heart_white_icon` asset, and the real `WishlistPage` model. The Bids->Offers nuance and the heart-not-flag visual nuance are now both pinned in this audit and reflected in pt-br.md, en.md, flow.yml, and all six mockup HTML/PNG files.
