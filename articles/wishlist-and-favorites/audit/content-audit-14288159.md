# Content audit, article 14288159 (wishlist-and-favorites)

Date: 2026-05-08 (rerun-2 patch on the 2026-05-06 audit)

## 1. PII / sensitive data

- No real user names. Mockup product names ("Charizard PSA 9", "Pikachu Holo") are public Pokemon TCG cards.
- No emails other than support@jambleapp.com.
- No phone numbers, no tokens, no IDs.

Verdict: PASS.

## 2. Banned words (auction / leilao)

- auction count = 0 in pt-br.md and en.md
- leilao / leilão count = 0 in pt-br.md and en.md

Verdict: PASS.

## 3. Currency

- pt-br.md body has 0 R$. The article does not document price mechanics; mockups carry price labels visually.
- en.md has 0 R$ leak. Mockup captions use US format ($1,450.00) only.
- flow.yml.currency_required is false to match this scope.

Verdict: PASS.

## 4. Word diet

- pt-br.md and en.md follow the same 1:1 H2 structure (verified by `grep -c "^## "`).
- Sentences are short and action-oriented; no filler paragraphs spotted on read-through.
- Tips section uses single-line bullets, no nested bullets, no walls of text.

Exact word and bullet counts are not asserted here, since they drift with copy edits and the validator does not enforce a specific count. Structural balance is what matters and is preserved.

Verdict: PASS.

## 5. Tone

- Direct address to the buyer (você / you).
- No condescension, no buildup before sections.
- Action-oriented (matches Jamble voice "actionable over poetic").

Verdict: PASS.

## 6. Alt text quality

| Image | Alt text content | Verdict |
|---|---|---|
| wishlist-tabs pt-br | names the screen, both tabs (Favoritos / Ofertas), and the heart icon visible on the cards | PASS |
| wishlist-tabs en | mirror with Bookmarks / Offers labels (NOT Bids) | PASS |
| product-bookmark-cta pt-br | names the heart icon, the saved state, and the red fill | PASS |
| product-bookmark-cta en | mirror, "heart icon" + "filled in red" | PASS |
| wishlist-empty-state pt-br | names the heart icon and the title "Comece a explorar as ofertas" | PASS |
| wishlist-empty-state en | mirror, "Start Exploring Deals" | PASS |

The validator (`alt_text_too_short` / `alt_text_too_long`) confirms all alt strings fall in the 15-150 char band. Each alt text is distinct from the others.

Verdict: PASS.

## 7. Stale-feature audit

Confirms every feature, button, and label described in the article still exists in production. Verdicts: live_in_ios | live_in_backend | product_confirmed | deprecated | unknown_blocker.

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Wishlist lives on the profile page | PROFILE/View Models/ProfileBottomViewModel.swift | live | 2026-05-08 | Aymar | live_in_ios |
| Tabs Favoritos / Ofertas (xcstrings: en `Bookmarks`->Bookmarks, en `Bids`->Offers; pt-BR identical) | WISHLIST/Models/WishlistPage.swift + Localizable.xcstrings | live | 2026-05-08 | Aymar | live_in_ios |
| Empty-state copy "Start Exploring Deals" / "Comece a explorar as ofertas" | WISHLIST/ViewModels/WishlistPageViewModel.swift | live | 2026-05-08 | Aymar | live_in_ios |
| Heart bookmark toggle on a product photo | PRODUCT/Views/SwiftUI/Components/ProductPhotosSection.swift:51 (Image("bookmark_heart_white_icon")) | live | 2026-05-08 | Aymar | live_in_ios |
| Heart bookmark button on the sticky CTA (Save the Show / Bookmark Item) | PRODUCT/Views/SwiftUI/Components/ProductStickyActionSection.swift:355 + :384 | live | 2026-05-08 | Aymar | live_in_ios |
| Notification permission requested at bookmark | WISHLIST/Views/WishlistPageViewController.swift:114 | live | 2026-05-08 | Aymar | live_in_ios |
| Bookmarked shows menu under Settings | xcstrings Bookmarked shows -> Programas marcados | confirmed | 2026-05-08 | Aymar | product_confirmed |

Verdict: PASS. 6 of 7 items live_in_ios with verified file paths, 1 product_confirmed (settings menu entry exists per xcstrings, no dedicated controller file to cite).

## 8. Manual visual review (procedure-compliance check #15)

Re-rendered all 6 mockups (product-bookmark-cta, wishlist-tabs, wishlist-empty-state in pt-BR + EN) on 2026-05-08 to:

1. Drop the previously inline flag/bookmark glyph (Feather-style flag SVG path) on every screen and replace with the verbatim heart `<path>` from `Assets.xcassets/bookmark_heart_white_icon.imageset/bookmark_heart_white_icon.svg`. Each instance carries an xcassets comment, an `alt="bookmark_heart_white_icon"`, an `aria-label` naming the icon and the human-readable visual cue ("ícone de coração" / "heart icon"), and `aria-hidden="true"` on the inner `<svg>` to keep screen readers from announcing it twice.
2. Recolour the saved-state pill / circle backgrounds with `#F14A22` (UIColor.liveRed = rgb 241,74,34, sourced from EXTENSIONS/Colors.swift:252-256), matching what the buyer actually sees in the iOS app when a bookmark is set.
3. Patch the en mockups so the second tab reads **Offers**, not Bids, in line with the xcstrings localisation of the `Bids` key.
4. Keep the existing neutral photo-style thumbnails (no cartoon emoji card placeholders, no big-text product placeholders), per process/12-procedure-compliance.md check #15.

Verdict: PASS (manual visual review post re-render on 2026-05-08).

## Result

8 SCANS pass. Zero BLOCKER. Article is content-quality ready for review.
