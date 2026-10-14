# Code Audit: article 14288159 (Wishlist and Favorites)

Wave 2 rewrite, 2026-10-14. Sources: Jamble-iOS tag 5.10.1, Jamble-Android tag v5.10.0, jamble_backend origin/main (291e133b5). Paths are repo-relative.

## Verified claims

- Own-profile tabs on iOS: `WISHLIST/Models/WishlistPage.swift` (Bookmarks, Bids) shown only on your own profile (`PROFILE/View Models/ProfileBottomViewModel.swift:97-101`). xcstrings pt-BR: Bookmarks = Favoritos, Bids = Ofertas. MATCH
- Favoritos lists bookmarked products, Ofertas lists active pre-offer products: `WISHLIST/ViewModels/WishlistPageViewModel.swift:34-36` (getBookmarkedProducts / myActivePrebidProducts). MATCH
- iOS saved lives: settings entry "Bookmarked shows" (pt Lives salvas) `PROFILE/ProfileSettings/ProfileSettingsV2ViewController.swift:36`, screen `BOOKMARKS/Views/BookmarkShowsViewController.swift`. MATCH
- Android saved lives: profile tab Salvos (`features/profile/.../ProfileTabSection.kt:177` renders BookmarkedShowsScreen); Ofertas tab renders MyOffersScreen (prebids). MATCH
- Save buttons: live card Salvar / Salvo (iOS xcstrings Save/Saved, Android bookmark_show_save_cta); product save icon on photo `PRODUCT/Views/SwiftUI/Components/ProductPhotosSection.swift:52-56` (icon-bookmark, not a heart); Android product_detail_action_bookmark = Salvar Item. MATCH
- Pre-offers placed again when the sale starts: xcstrings "Any Pre bids placed before the sale will be placed again" (pt "Todas as ofertas prévias feitas antes da venda serão feitas novamente"). MATCH
- Saved searches on the Products search tab: jamble_backend `src/routers/product.py:721,782`; iOS `SEARCH/Main/Views/SearchView.swift:72`; Android `search_strings.xml` Buscas salvas. MATCH
- Notification toggle "Lives salvas" in section "Lives": jamble_backend `src/services/notification_service.py:3967-3976`. Note: both the bookmarked-show and bookmarked-product toggles carry the pt title "Lives salvas". MATCH

## Gaps found (not claimed in the article)

- Android v5.10.0 can save a product (Salvar Item) but no saved-products list was found on the profile (`getBookmarkedProducts` is unused outside the bookmark module). The article states the saved-products location for iPhone only.

## Verdict

All claims trace to the production sources above.
