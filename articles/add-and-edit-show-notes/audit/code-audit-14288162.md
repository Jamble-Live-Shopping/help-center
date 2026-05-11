# Code audit, article 14288162 (add-and-edit-show-notes)

Source of truth: `Jamble-iOS` repo at `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble`. Strings cross-referenced with `Jamble/RESOURCES/Localizable.xcstrings`. iOS assets live under `Jamble/RESOURCES/Assets.xcassets/<name>.imageset/`.

## iOS source files referenced

| File | Lines used | Purpose |
|---|---|---|
| `Jamble/LIVE_SHOPPING/Create/Show/Views/CreateShowDetailsViewController.swift` | 12-37, 58-74, 361-374 | Show details form: stack of `descriptionHeader / descriptionTextView / notesHeader / notesTextView`. NOTES header constructed with `charactersLimit: 200`. UITextViewDelegate trims to 200 on `textViewDidChange`. |
| `Jamble/LIVE_SHOPPING/Create/Show/Views/Components/CreateShowDetailsHeader.swift` | 14-54, 85-90 | Header layout: title + counter `(0/<limit>)` + optional `Optional` label. Title uses `Patron-Medium 13` white. Counter `rounded medium 13` white. Optional label `rounded medium 13`, hex `#787878`. |
| `Jamble/LIVE_SHOPPING/Chat/View/ShowPinnedMessageView.swift` | 12-23, 25-39, 41-49, 84-96 | Pinned message: stackView with white-20% alpha background, layoutMargins(8,8,8,8), corner radius 3, 28x28 round avatar, `messageLabel.numberOfLines=5`. `configure(_ note)` applies attributes: `rounded semibold 15`, `kern -0.15`, white. |
| `Jamble/LIVE_SHOPPING/Chat/View/ShowChatViewController.swift` | 38, 201-206, 280-283, 746-764 | `pinnedMessage` is `ShowPinnedMessageView`, hidden by default. `viewModel.showPinnedMessage` sink calls `pinnedMessage.configure(note)` then `showPinnedMessage()`. `showPinnedMessage()` fades in 0.3s, then fades out after `viewModel.estimatedReadingTime()` (auto-dismiss). |
| `Jamble/LIVE_SHOPPING/Audience/View/ShowAudienceViewController.swift` | 47, 281, 1259-1268, 2085-2088 | `notesButton: JambleButton` with `image: UIImage(named: "note_icon")`, hidden when `viewModel.shouldShowNoteButton == false`, action `showNotes` calls `chatViewProvider?.showNote()` (re-opens pinned message). |
| `Jamble/LIVE_SHOPPING/Host/View/ShowHostViewController.swift` | 51, 642-655, 934-951, 1521-1528 | `editShowButton` setImage `edit_white_icon`. Visibility rule: `if show.has_started == true && show.is_over == false { editShowButton.isEnabled = false; editShowButton.isHidden = true }` else visible. `didJoinAsAudience()` also forces `isHidden = true`. |
| `Jamble/EXTENSIONS/Colors.swift` | 64 | `customGrey900 = rgb(0.1,0.1,0.1) == #1A1A1A`. Used as background of NOTES text view. |

## xcstrings keys pulled (verbatim)

| Key | EN value | pt-BR value |
|---|---|---|
| `NOTES` | `NOTES` | `NOTAS` |
| `DESCRIPTION` | `DESCRIPTION` | `DESCRIÇÃO` |
| `Optional` | `Optional` | `Opcional` |
| `Additional notes` | `Additional notes` | `Observações adicionais` |
| `Describe your live here` | `Describe your live here` | `Descreva sua Live aqui` |

## Claim, source, verdict

| Article claim (EN) | iOS source | Verdict |
|---|---|---|
| NOTES field has a 200-character limit | `CreateShowDetailsViewController.swift:58` `charactersLimit: 200`; `CreateShowDetailsViewController.swift:366-368` truncates to first 200 chars | MATCH |
| NOTES character counter format `(0/200)` | `CreateShowDetailsHeader.swift:52` `charactersLimitLabel.text = "(0/\(charactersLimit))"` | MATCH |
| NOTES field is labelled `NOTES` (EN) and `NOTAS` (pt-BR) | xcstrings: `NOTES` -> `NOTAS` | MATCH |
| DESCRIPTION field is labelled `DESCRIPTION` (EN) and `DESCRIÇÃO` (pt-BR) | xcstrings: `DESCRIPTION` -> `DESCRIÇÃO` | MATCH |
| Both fields show `Optional` (EN) / `Opcional` (pt-BR) on the right | `CreateShowDetailsHeader.swift:35` `String(localized: "Optional")` + xcstrings | MATCH |
| Placeholders: NOTES -> `Additional notes` / `Observações adicionais`, DESCRIPTION -> `Describe your live here` / `Descreva sua Live aqui` | `CreateShowDetailsViewController.swift:44, 63` + xcstrings | MATCH |
| NOTES textview background is dark (`customGrey900` == `#1A1A1A`) | `CreateShowDetailsViewController.swift:66` `backgroundColor = UIColor.customGrey900`; `Colors.swift:64` | MATCH |
| Notes appear as a pinned message in chat for viewers | `ShowChatViewController.swift:201-206` `viewModel.showPinnedMessage` sink calls `pinnedMessage.configure(note)` + `showPinnedMessage()` | MATCH |
| Pinned message shows seller profile picture next to text | `ShowPinnedMessageView.swift:25-39` 28x28 round `pinIcon` from `sellerProfile.getProfileImage`; layout in `setup()` with avatar and label side-by-side | MATCH |
| Pinned message text style: white semibold rounded | `ShowPinnedMessageView.swift:84-92` `rounded(ofSize: 15, weight: .semibold)`, `kern: -0.15`, `foregroundColor: .white` | MATCH |
| Pinned message auto-dismisses after a few seconds | `ShowChatViewController.swift:756-764` second UIView.animate with `delay: estimatedReadingTime()` then `isHidden = true` | MATCH |
| Notes button (note_icon) appears top-right of audience view to re-open pinned message | `ShowAudienceViewController.swift:1259-1268` `notesButton.setImage(UIImage(named: "note_icon"))`, action `showNotes`, added to `topRightSideStackView`. `showNotes` calls `chatViewProvider?.showNote()` | MATCH |
| Edit Show button is HIDDEN when the show is live | `ShowHostViewController.swift:945-951` `if self.show.has_started == true && self.show.is_over == false { editShowButton.isEnabled = false; editShowButton.isHidden = true }` | MATCH (article scoped to pre-live editing) |
| Edit Show button uses pencil icon (`edit_white_icon`) | `ShowHostViewController.swift:941` `setImage(UIImage(named: "edit_white_icon"))` | MATCH |

## v1 -> v2 changes (mismatches FIXED)

1. v1 article body claimed sellers can edit notes "during the live, tap the edit button (pencil icon) and update your notes in the show editor." iOS code `ShowHostViewController.swift:945-951` hides the edit button while live. v2 reframes the article around pre-live editing with an explicit limit ("Important, once the show starts, the edit button is no longer available on the host screen"). Carried forward from rerun-1 finding.
2. v1 mockup `add-edit-show-notes__pt-br.html` rendered the form on light background with `Show Notes` form title. iOS form is rendered on dark background (`customGrey900` text view) inside the standard create-show wizard. v2 rebuilt with dark background, real `(0/200)` counter, real `Optional` label, real placeholder strings.
3. v1 mockup `promo-chat-message__pt-br.html` and `promo-banner-shipping__en.html` rendered the chat message as a card with `Frete grátis em 3+ itens!` / `LIVE30` and a `Continue` button. The actual iOS render is a `ShowPinnedMessageView` overlaid on the live video, with white-20% alpha background, 28x28 avatar, no buttons, auto-dismiss timer. v2 rebuilt the audience screen with the real overlay style and added the top-right `note_icon` to surface the re-open affordance.
4. v1 article example used "edição tênis" (sneakers). BR market is collectibles only (Pokemon TCG 72%, Diecast 21%). Switched to `Pikachu Holo PSA 9` lot example.
5. v1 mockups had no real icons. v2 inlines the actual `Assets.xcassets/note_icon.imageset/note_icon.svg` in the audience screen-2 mockup (also copied to `assets/icons-ios/note_icon.svg` for reuse).

## Open MISMATCH count: 0

All article claims verified against Swift source. Risk flag (Edit Show button hidden mid-live) carried as resolved_decision in flow.yml.
