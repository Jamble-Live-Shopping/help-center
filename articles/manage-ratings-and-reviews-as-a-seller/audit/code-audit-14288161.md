# Code audit, article 14288161

**Scope**: every iOS UI string and rating mechanic referenced in pt-br.md and en.md mapped to Swift source.

## String mapping

| Article claim (EN / pt-BR) | iOS source | Match |
|---|---|---|
| "Ratings & Reviews" / "Classificações e Avaliações" (profile tab title + section header) | `Jamble/PROFILE/Views/ProfileRatingViewController.swift:33` `String(localized: "Ratings & Reviews")` and `Jamble/PROFILE/Views/Components/ProfileRatingsHeaderView.swift:26` same key. Localizable.xcstrings pt-BR = "Classificações e Avaliações" | MATCH |
| "Reviews" / "Comentários" (count label under big number) | `ProfileRatingsHeaderView.swift:47` `String(localized: "Reviews")`. xcstrings pt-BR = "Comentários" | MATCH |
| "out of 5" / "de 5" (label under average grade) | `ProfileRatingsHeaderView.swift:77` `String(localized: "out of 5")`. xcstrings pt-BR = "de 5" | MATCH |
| "Rate" button on completed transaction (buyer side) | `Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:309` `rateButton.setTitle("Rate")`, surfaces when status in {completed, productConfirmed, productConfirmTimeout} && seller_rating_id == nil | MATCH |
| "Write a feedback" / "Escreva um feedback" (rating sheet nav title) | `Jamble/RATING/Model/RatingType.swift:31` `String(localized: "Write a feedback")`. xcstrings pt-BR = "Escreva um feedback" | MATCH |
| "Tap a Star to Rate" / "Toque em uma estrela para avaliar" | `Jamble/RATING/Views/CustomRatingViewController.swift:78` `String(localized: "Tap a Star to Rate")`. xcstrings pt-BR = "Toque em uma estrela para avaliar" | MATCH |
| "How was your product?" / "Como foi seu produto?" (transaction case placeholder) | `RatingType.swift:43` `case .transaction: return String(localized: "How was your product?")`. xcstrings pt-BR = "Como foi seu produto?" | MATCH |
| "Cancel" / "Cancelar" + "Send" / "Enviar" (sheet nav buttons) | `CustomRatingViewController.swift:39,56` both with `.customPurple` color. xcstrings pt-BR = "Cancelar" / "Enviar" | MATCH |
| Star color = customPurple #7E53F8 on rating sheet | `CustomRatingViewController.swift:273` `button.tintColor = .customPurple` | MATCH |
| Star color = #F59E0B filled / #56636F empty on profile review cell | `ProfileRatingCell.swift:181` `tintColor = (i <= Int(grade-1)) ? UIColor(hex: "F59E0B") : UIColor(hex: "56636F")` | MATCH |
| 5-star scale | `CustomRatingViewController.swift:68-72` `for index in 1...5` and `ProfileRatingCell.swift:178` `for i in 0...4` | MATCH |
| "Report" / "Comunicar" (action sheet on viewer profile) | `Jamble/PROFILE/Views/ProfileViewController.swift:302` `UIAlertAction(title: String(localized: "Report"), style: .default)`. xcstrings pt-BR = "Comunicar" | MATCH |
| "Block" / "Bloquear" (destructive item) | `ProfileViewController.swift:309` `String(localized: "Block")` style `.destructive`. xcstrings pt-BR = "Bloquear" | MATCH |
| Action sheet = native UIAlertController.actionSheet | `ProfileViewController.swift:276` `UIAlertController(title: nil, message: nil, preferredStyle: .actionSheet)` | MATCH |
| Report opens webview via AskJamble | `ProfileViewController.swift:303-305` `AskJamble.shared.getReportLink(...)` then `WebEmbeddedViewController` | MATCH |
| Rating tied to transaction not show | `RatingType.swift:11` `case transaction(Transaction)` + `seller_rating_id` field on Transaction | MATCH |
| Rating prompted only after delivery confirmed | `PurchaseViewController.swift:297` status in {completed, productConfirmed, productConfirmTimeout} | MATCH |
| Comment optional for transaction | `RatingType.swift:48-53` `var isFeedbackRequired { case .transaction: return false }` | MATCH |
| Profile rating header big number 40pt rounded semibold; label 16pt medium | `ProfileRatingsHeaderView.swift:41,51,71,81` `UIFont.rounded(ofSize: 40, weight: .semibold)` + `systemFont(ofSize: 16, weight: .medium)` | MATCH |
| Profile review cell card bg #FAFAFC radius 16 | `ProfileRatingCell.swift:87-88` `backgroundColor = UIColor(hex: "FAFAFC")` + `cornerRadius = 16` | MATCH |
| Profile review cell name 14 medium #162131; time 12 medium #78828C; comment 14 regular #56636F | `ProfileRatingCell.swift:54-55,70-71,79-80` | MATCH |

## Mechanic claims

| Claim | Source | Verdict |
|---|---|---|
| "Buyer can rate later from order history" | `seller_rating_id == nil` gate, Rate button surfaces on every reopen until rated | MATCH |
| "Rating becomes permanent once Send is tapped" | `CustomRatingViewModel.save()` mutates `seller_rating_id`, no edit UI | MATCH |
| "Sellers can't delete reviews" | No deletion path in ProfileRatingViewController | MATCH |
| "Report goes through support" | Report = AskJamble webview, support handles outcome | MATCH |

## Visual fidelity

- **profile-rating-summary**: title + dual rounded big-number layout + ProfileRatingCell stack matches `ProfileRatingsHeaderView` + `ProfileRatingCell`. MATCH
- **rate-transaction-sheet**: nav (Cancel/Title/Send), 5 purple stars 21px gap 16, hint, divider, placeholder. Mirrors `CustomRatingViewController` 1:1. MATCH
- **report-profile-options**: native UIAlertController.actionSheet with grouped actions + destructive Block + separated Cancel. Mirrors `ProfileViewController.openOptions`. MATCH

## Verdict

Zero MISMATCH. All UI strings, layout, colors, mechanics confirmed against `/Users/aymardumoulin/Projects/Jamble-iOS`.
