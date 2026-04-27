# Code audit, article 14288161

**Scope**: every iOS UI string and rating mechanic referenced in pt-br.md and en.md mapped to Swift source.

## String mapping

| Article claim (EN / pt-BR) | iOS source | Match |
|---|---|---|
| "Ratings & Reviews" / "Classificações e Avaliações" (profile tab title + section header) | `Jamble/PROFILE/Views/ProfileRatingViewController.swift:33` `String(localized: "Ratings & Reviews")` and `Jamble/PROFILE/Views/Components/ProfileRatingsHeaderView.swift:26` same key. Localizable.xcstrings pt-BR = "Classificações e Avaliações" | MATCH |
| "Reviews" / "Comentários" (count label under the big number) | `Jamble/PROFILE/Views/Components/ProfileRatingsHeaderView.swift:47` `descriptionLabel.text = String(localized: "Reviews")`. xcstrings pt-BR = "Comentários" | MATCH |
| "out of 5" / "de 5" (label under the average grade) | `Jamble/PROFILE/Views/Components/ProfileRatingsHeaderView.swift:77` `descriptionLabel.text = String(localized: "out of 5")`. xcstrings pt-BR = "de 5" | MATCH |
| "Rate" button on completed transaction (buyer side) | `Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:309` `rateButton.setTitle("Rate")`, surfaces when `transaction.status in {.completed,.productConfirmed,.productConfirmTimeout} && seller_rating_id == nil` | MATCH |
| "Write a feedback" / "Escreva um feedback" (rating sheet nav title) | `Jamble/RATING/Model/RatingType.swift:31` `var navigationTitle: String { return String(localized: "Write a feedback") }`. xcstrings pt-BR = "Escreva um feedback" | MATCH |
| "Tap a Star to Rate" / "Toque em uma estrela para avaliar" (under stars) | `Jamble/RATING/Views/CustomRatingViewController.swift:78` `label.text = String(localized: "Tap a Star to Rate")`. xcstrings pt-BR = "Toque em uma estrela para avaliar" | MATCH |
| "How was your product?" / "Como foi seu produto?" (review text placeholder, transaction case) | `Jamble/RATING/Model/RatingType.swift:43` `case .transaction: return String(localized: "How was your product?")`. xcstrings pt-BR = "Como foi seu produto?" | MATCH |
| "Cancel" / "Cancelar" (rating sheet left nav button) | `Jamble/RATING/Views/CustomRatingViewController.swift:39` `button.setTitle(String(localized: "Cancel"), for: .normal)` + `setTitleColor(.customPurple, for: .normal)`. xcstrings pt-BR = "Cancelar" | MATCH |
| "Send" / "Enviar" (rating sheet right nav button) | `Jamble/RATING/Views/CustomRatingViewController.swift:56` `button.setTitle(String(localized: "Send"), for: .normal)` + `.customPurple` + weight semibold. xcstrings pt-BR = "Enviar" | MATCH |
| Star color = Jamble purple #7E53F8 on rating sheet | `Jamble/RATING/Views/CustomRatingViewController.swift:273` `button.tintColor = .customPurple`. design-system.md customPurple = #7E53F8 | MATCH |
| Star color = orange/amber on profile review cell | `Jamble/PROFILE/Views/Components/ProfileRatingCell.swift:181` `starImageView.tintColor = (i <= Int(grade - 1)) ? UIColor(hex: "F59E0B") : UIColor(hex: "56636F")` | MATCH (#F59E0B filled, #56636F empty) |
| 5-star rating system | `Jamble/RATING/Views/CustomRatingViewController.swift:68-72` `for index in 1...5 { ... starsStackView.addArrangedSubview(starButton) }` and ProfileRatingCell `for i in 0...4` | MATCH |
| "Report" / "Comunicar" (action sheet on other-user profile) | `Jamble/PROFILE/Views/ProfileViewController.swift:302` `UIAlertAction(title: String(localized: "Report"), style: .default)`. xcstrings pt-BR = "Comunicar" | MATCH |
| "Block" / "Bloquear" (destructive action sheet item) | `Jamble/PROFILE/Views/ProfileViewController.swift:309` `let blockedString = isBlocked ? String(localized: "Unblock") : String(localized: "Block")`, style `.destructive`. xcstrings pt-BR = "Bloquear" | MATCH |
| Action sheet style is iOS native UIAlertController .actionSheet | `Jamble/PROFILE/Views/ProfileViewController.swift:276` `UIAlertController(title: nil, message: nil, preferredStyle: .actionSheet)` | MATCH |
| Report opens a webview via `AskJamble.shared.getReportLink` | `Jamble/PROFILE/Views/ProfileViewController.swift:303-305` `getReportLink(source: "profile", reported_profile: self.profile)` then `WebEmbeddedViewController` | MATCH (article describes a "form" generically, no string claim) |
| Rating tied to transaction (not show) | `Jamble/RATING/Model/RatingType.swift:11` `case transaction(Transaction)` and `seller_rating_id` field on transaction (`PurchaseViewController.swift:245`) | MATCH |
| Rating prompted only after confirmed delivery | `Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:297` `[.completed, .productConfirmed, .productConfirmTimeout].contains(self.transaction.status) && self.transaction.seller_rating_id == nil` | MATCH |
| Comment is optional for transaction rating | `Jamble/RATING/Model/RatingType.swift:48-53` `var isFeedbackRequired { case .transaction: return false }` | MATCH |
| "Rate" button color = customPurple, white text, semibold 16, corner radius 25 (pill) | `Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:299` `QBIndicatorButton(... textColor: UIColor.white, font: ...semibold, backgroundColor: .customPurple, cornerRadius: 25)` | MATCH |
| Profile rating header: 40pt rounded semibold for big number, 16pt medium for label | `Jamble/PROFILE/Views/Components/ProfileRatingsHeaderView.swift:41,51,71,81` `UIFont.rounded(ofSize: 40, weight: .semibold)` (number) + `systemFont(ofSize: 16, weight: .medium)` (label) | MATCH |
| Profile review cell card: corner 16, bg #FAFAFC | `Jamble/PROFILE/Views/Components/ProfileRatingCell.swift:87-88` `contentView.backgroundColor = UIColor(hex: "FAFAFC")` + `cornerRadius = 16` | MATCH |
| Profile review cell name 14 medium #162131 | `ProfileRatingCell.swift:54-55` `textColor = UIColor(hex: "162131")` + `systemFont(ofSize: 14, weight: .medium)` | MATCH |
| Profile review cell time label 12 medium #78828C | `ProfileRatingCell.swift:70-71` `textColor = UIColor(hex: "78828C")` + `systemFont(ofSize: 12, weight: .medium)` | MATCH |
| Profile review cell comment 14 regular #56636F | `ProfileRatingCell.swift:79-80` `textColor = UIColor(hex: "56636F")` + `systemFont(ofSize: 14, weight: .regular)` | MATCH |

## Mechanic claims (no string, but flow logic)

| Claim | Source | Verdict |
|---|---|---|
| "Buyer can also rate later from order history" | Inferred from `seller_rating_id == nil` gate on `.completed/.productConfirmed/.productConfirmTimeout` statuses, the Rate button surfaces every time the buyer reopens the purchase as long as the rating hasn't been submitted | MATCH |
| "Rating becomes permanent once Send is tapped" | `CustomRatingViewModel.save()` mutates `seller_rating_id`, no edit/delete API surfaced in `ProfileRatingsViewModel` or `RatingProfile` model | MATCH (no edit path in iOS code) |
| "Sellers cannot delete reviews themselves" | No deletion UI exists in `ProfileRatingViewController` or related cells | MATCH |
| "Report goes through support, only policy-violating reviews are removed" | Report link is a webview to AskJamble (`AskJamble.shared.getReportLink`), backend / support handles outcome. Article describes outcome generically without claiming specific policies | MATCH (flow correct, no fabricated guarantees) |

## Visual fidelity

All 3 mockups side-by-side with Swift structure:

- **profile-rating-summary**: title "Classificações e Avaliações" matches `ProfileRatingsHeaderView` titleLabel. Two big numbers in rounded 40pt match the layout (left = grade with "de 5" subtitle, right = count with "Comentários" subtitle). Below, two `ProfileRatingCell` cards with bg #FAFAFC, radius 16, profile name 14pt, time 12pt, stars 14px (slightly smaller than 18px iOS for visual fit), comment 14pt regular. MATCH.
- **rate-transaction-sheet**: Cancel left (#7E53F8 regular), title "Escreva um feedback" centered semibold black, Send right (#7E53F8 semibold). 5 purple stars (21x21) horizontally with spacing 16. "Toque em uma estrela para avaliar" 12pt #8B8A8F centered. Divider then placeholder "Como foi seu produto?" 16pt #C5C5C7. Mirrors `CustomRatingViewController` pixel-for-pixel. MATCH.
- **report-profile-options**: iOS-native UIAlertController.actionSheet with two grouped actions ("Comunicar" default + "Bloquear" destructive red) and separated "Cancelar" cancel button below. Mirrors `ProfileViewController.openOptions` for non-admin viewer-of-other-profile path. MATCH.

## Verdict

Zero MISMATCH. All UI strings, layout, colors, and mechanics confirmed against `/Users/aymardumoulin/Projects/Jamble-iOS`.
