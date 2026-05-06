# Content audit, article 14288159 (wishlist-and-favorites)

Date: 2026-05-06

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
| wishlist-tabs pt-br | names the screen, both tabs (Favoritos / Ofertas), and the product cards | PASS |
| wishlist-tabs en | mirror with Bookmarks / Bids labels | PASS |
| product-bookmark-cta pt-br | names the filled bookmark icon and the saved state | PASS |
| product-bookmark-cta en | mirror | PASS |
| wishlist-empty-state pt-br | names the empty-state title "Comece a explorar as ofertas" | PASS |
| wishlist-empty-state en | mirror | PASS |

The validator (`alt_text_too_short` / `alt_text_too_long`) confirms all alt strings fall in the 15-150 char band. Each alt text is distinct from the others.

Verdict: PASS.

## 7. Stale-feature audit

Confirms every feature, button, and label described in the article still exists in production. Verdicts: live_in_ios | live_in_backend | product_confirmed | deprecated | unknown_blocker.

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Wishlist lives on the profile page | PROFILE/View Models/ProfileBottomViewModel.swift | live | 2026-05-06 | Aymar | live_in_ios |
| Tabs Favoritos / Ofertas | WISHLIST/Models/WishlistPage.swift | live | 2026-05-06 | Aymar | live_in_ios |
| Empty-state copy "Start Exploring Deals" / "Comece a explorar as ofertas" | WISHLIST/ViewModels/WishlistPageViewModel.swift | live | 2026-05-06 | Aymar | live_in_ios |
| Bookmark toggle on a product card | PRODUCT/View Models/ProductViewModel.swift | live | 2026-05-06 | Aymar | live_in_ios |
| Bookmark a show from preview | PRODUCT/View Models/ProductViewModel.swift | live | 2026-05-06 | Aymar | live_in_ios |
| Notification permission requested at bookmark | WISHLIST/Views/WishlistPageViewController.swift | live | 2026-05-06 | Aymar | live_in_ios |
| Bookmarked shows menu under Settings | xcstrings Bookmarked shows -> Programas marcados | confirmed | 2026-05-06 | Aymar | product_confirmed |

Verdict: PASS. 6 of 7 items live_in_ios with verified file paths, 1 product_confirmed (settings menu entry exists per xcstrings, no dedicated controller file to cite).

## 8. Manual visual review (procedure-compliance check #15)

Re-rendered all 4 product-bearing mockups (product-bookmark-cta pt-br + en, wishlist-tabs pt-br + en) on 2026-05-06 to drop the `🎴` and `🃏` cartoon emoji placeholders and the orange-saturation cartoon thumbnails. The new mockups show a neutral dark photo-style background with a small white card silhouette inside (rounded corners, subtle shadow, abstract gradient art block, two thin meta lines). No facial features, no big-text product placeholder, no playing-card emoji. The empty-state mockups did not contain a card placeholder and were left untouched.

Aligned with `process/12-procedure-compliance.md` check #15: "No cartoon illustrations of cards/products, no big-text product placeholders, no CSS-drawn icons quand un asset iOS existe".

Verdict: PASS (manual visual review post re-render).

## Result

8 SCANS pass. Zero BLOCKER. Article is content-quality ready for review.
