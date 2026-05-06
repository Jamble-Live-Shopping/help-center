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

- pt-br.md: 565 words across 11 H2 sections. Sentences mostly under 25 words.
- en.md: 580 words, 1:1 mirror with pt-BR. No filler paragraphs.
- Tips section is 4 single-line bullets.

Verdict: PASS.

## 5. Tone

- Direct address to the buyer (você / you).
- No condescension, no buildup before sections.
- Action-oriented (matches Jamble voice "actionable over poetic").

Verdict: PASS.

## 6. Alt text quality

| Image | Alt text length | Verdict |
|---|---|---|
| wishlist-tabs pt-br | 88 chars, names tabs and content | PASS |
| wishlist-tabs en | 80 chars, mirror | PASS |
| product-bookmark-cta pt-br | 96 chars, names icon and toast | PASS |
| product-bookmark-cta en | 90 chars, mirror | PASS |
| wishlist-empty-state pt-br | 89 chars, includes empty-state title | PASS |
| wishlist-empty-state en | 79 chars, mirror | PASS |

All alt texts are 15-150 chars, descriptive, unique per image.

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

## Result

7 SCANS pass. Zero BLOCKER. Article is content-quality ready for review.
