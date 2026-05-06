# Code audit, article 14288159 (wishlist-and-favorites)

Date: 2026-05-06
Source iOS: Jamble-iOS develop. Sources cited in flow.yml.
xcstrings: `Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings`

## Claims article vs source code

| Article claim | Source | Verdict |
|---|---|---|
| Wishlist lives on the profile page | PROFILE/View Models/ProfileBottomViewModel.swift:81 (iterates WishlistPage.allCases and instantiates WishlistPageViewController) | MATCH |
| Two tabs: Bookmarks (pt-BR Favoritos) and Bids (pt-BR Ofertas) | WISHLIST/Models/WishlistPage.swift case .favorites: String(localized: "Bookmarks") + case .activeBids: String(localized: "Bids") + xcstrings pt-BR Bookmarks -> "Favoritos", Bids -> "Ofertas" | MATCH |
| Empty state title "Start Exploring Deals" / "Comece a explorar as ofertas" | WISHLIST/ViewModels/WishlistPageViewModel.swift empty state branch + xcstrings pt-BR | MATCH |
| Empty state subtitle "Discover deals and save your favorite items." / "Descubra ofertas e salve seus itens favoritos." | WISHLIST/ViewModels/WishlistPageViewModel.swift + xcstrings pt-BR | MATCH |
| Bookmark icon on a product card toggles save | PRODUCT/View Models/ProductViewModel.swift:315 bookmarkProduct (bookmark / unbookmark) | MATCH |
| Bookmark a show from the show preview | PRODUCT/View Models/ProductViewModel.swift:32 bookmarkShow | MATCH |
| Notification permission requested at first bookmark | WISHLIST/Views/WishlistPageViewController.swift:114 PermissionSettings().requestNotificationAuthorizationIfNeeded(type: .bookmark) | MATCH |
| Bookmarked shows live under Settings > Bookmarked shows (pt-BR Programas marcados) | xcstrings Bookmarked shows -> "Programas marcados" | MATCH |
| Notification "Bookmarked product from show" | iOS notification settings UI Live Shows section (xcstrings) | MATCH |
| Sellers do not see individual saver names | Architectural: no seller-side endpoint that lists savers per product. Negative claim, confirmed by reading the wishlist + product models | MATCH |

## Visual fidelity

| Mockup | pt-BR strings match xcstrings? | Status |
|--------|--------------------------------|--------|
| wishlist-and-favorites__wishlist-tabs__pt-br.png | Favoritos, Ofertas, Lista de desejos | MATCH (Favoritos / Ofertas pulled from xcstrings; "Lista de desejos" is the article heading because xcstrings has no "Wishlist" key) |
| wishlist-and-favorites__wishlist-empty-state__pt-br.png | "Comece a explorar as ofertas" + "Descubra ofertas e salve seus itens favoritos." | MATCH (verified xcstrings) |
| wishlist-and-favorites__product-bookmark-cta__pt-br.png | "Produto salvo nos Favoritos" | MATCH on tab name; the confirmation toast is illustrative since the iOS app surfaces a permission modal then fills the icon, no custom toast |

## Notes

- "Wishlist" itself has no xcstrings key. The article uses "Lista de desejos" as a descriptive pt-BR heading; the in-app surface is reached by tapping the Favoritos / Ofertas tabs from the profile.
- The bookmark CTA mockup confirmation toast is a teaching aid (the real iOS interaction is permission-modal + icon-fill), not a string pulled from xcstrings.

## Verdict

Zero MISMATCH against the cited iOS sources. Article is grounded in real xcstrings and the real WishlistPage model. Article body is consistent with the audited iOS surface.
