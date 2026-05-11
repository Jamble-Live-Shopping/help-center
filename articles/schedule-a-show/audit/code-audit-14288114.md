# Code Audit, schedule-a-show (seller, intercom 14288114)

Date: 2026-05-08
Source iOS: Jamble-iOS develop, paths cited in flow.yml
xcstrings: `Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings`

## Source files actually used

- `LIVE_SHOPPING/Create/Show/Model/CreateShowStep.swift` (lines 10-16)
- `LIVE_SHOPPING/Create/Show/Views/CreateShowV2ViewController.swift`
- `LIVE_SHOPPING/Create/Show/Views/CreateShowTextFieldViewController.swift` (lines 24-38, 96-107)
- `LIVE_SHOPPING/Create/Show/Views/CreateShowTagsV2ViewController.swift` (lines 22-37, 93-113)
- `LIVE_SHOPPING/Create/Show/Views/CreateShowCoverPhotoViewController.swift` (lines 19-49, 105-115, 145-150)
- `LIVE_SHOPPING/Create/Show/Views/CreateShowDetailsViewController.swift` (lines 39-124, 295-353)
- `LIVE_SHOPPING/Create/Show/Views/Components/RepeatContainerView.swift` (lines 41, 69, 124, 128)
- `LIVE_SHOPPING/Create/Show/ViewModel/CreateShowViewModel.swift` (lines 460-490)
- `LIVE_SHOPPING/Show/Model/Show.swift` (lines 92-93)
- `PROFILE/Views/ProfileViewController.swift` (lines 196-217, 248-252)
- `TABBAR/View/JambleTabBarController.swift` (lines 356-436)
- `RESOURCES/Localizable.xcstrings`
- `RESOURCES/Assets.xcassets/icon-calendar.imageset/icon-calendar.svg`

## xcstrings keys pulled (verbatim)

| Key | en | pt-BR |
|---|---|---|
| `Schedule a Show` | Schedule a Show | Agendar um show |
| `Type your show title` | Type your show title | Digite o título de seu show |
| `No title` | No title | Sem título |
| `Please type a title for your show` | Please type a title for your show | Digite um título para seu show |
| `Next` | Next | Seguinte |
| `Import from library` | Import from library | Importar da biblioteca |
| `Select your date` | Select your date | Selecione sua data |
| `Select Date` | Select Date | Selecione a data |
| `Invalid date` | Invalid date | Data inválida |
| `DESCRIPTION` | DESCRIPTION | DESCRIÇÃO |
| `NOTES` | NOTES | NOTAS |
| `DATE` | DATE | DATA |
| `Describe your live here` | Describe your live here | Descreva sua Live aqui |
| `Additional notes` | Additional notes | Observações adicionais |
| `Repeats` | Repeats | Repetições |
| `Every` | Every | A cada |
| `Ends` | Ends | Finais |
| `Day` | Day | Dia |
| `Week` | Week | Semana |
| `Month` | Month | Mês |
| `On Date` | On Date | Na Data |
| `After 1 Show` | After 1 Show | Após 1 Show |
| `After 3 Shows` | After 3 Shows | Após 3 Shows |
| `After 5 Shows` | After 5 Shows | Após 5 Shows |
| `After 10 Shows` | After 10 Shows | Após 10 Shows |
| `Postpone Limit` | Postpone Limit | Limite de adiamento |
| `This Show was already postponed too many times. You cannot postpone it.` | (en verbatim) | Este Show já foi adiado muitas vezes. Você não pode mais adiá-lo. |
| `Got it` | Got it | Entendi |

## Claims article vs source code

| Article claim | Source | Verdict |
|---|---|---|
| Schedule a Show is opened from the seller profile menu | ProfileViewController.swift:196-217, openCreateShow() at 248-252 calls JambleTabBarController.openCreateShowVC | MATCH |
| Profile must have email/phone/address/payment before creating | JambleTabBarController.swift:371-376 InfoManager.checkInfosAreNeeded with .email, .phone_number, .shipping_address, .payment_method | MATCH |
| Four-step flow: title, tag, cover, details | CreateShowStep.swift:10-16 enum cases showTitle=0, showTags=1, showCover=2, showDetails=3 | MATCH |
| Step 1 is one centered text field with placeholder Type your show title / Digite o título de seu show | CreateShowTextFieldViewController.swift:24-38 textField with attributedPlaceholder String(localized: "Type your show title"), centered alignment, dark background | MATCH |
| Empty title alert: No title / Sem título | CreateShowTextFieldViewController.swift:101-104 UIAlertController(title: String(localized: "No title"), message: String(localized: "Please type a title for your show")) | MATCH |
| Step 2 only allows one tag | CreateShowTagsV2ViewController.swift:163-172 didSelectItemAt selects single tag, unselects on second tap | MATCH |
| Step 2 Next button | CreateShowTagsV2ViewController.swift:30 setTitle String(localized: "Next") | MATCH |
| Step 3 has Import from library button + Unsplash picker | CreateShowCoverPhotoViewController.swift:19-33 importButton with String(localized: "Import from library") + setupPhotoPicker UnsplashPhotoPicker | MATCH |
| Cover image cropped 1:1 after import | CreateShowCoverPhotoViewController.swift:152-160 openImageCropper aspectRatioPreset CGSize(width:1, height:1) | MATCH |
| Step 4 sections: DESCRIPTION, NOTES, DATE, Repeats | CreateShowDetailsViewController.swift:39 descriptionHeader, 58 notesHeader, 89-96 showDateLabel "DATE", 118-124 repeatContainer | MATCH |
| Notes 200 char limit | CreateShowDetailsViewController.swift:58 charactersLimit: 200 + 366-368 prefix(200) clamp | MATCH |
| Date row uses icon-calendar asset | CreateShowDetailsViewController.swift:106 UIImageView(image: UIImage(named: "icon-calendar")), asset at RESOURCES/Assets.xcassets/icon-calendar.imageset/icon-calendar.svg | MATCH |
| Repeats card disabled until date is set | CreateShowDetailsViewController.swift:118-124 repeatContainer.alpha = 0.6, isUserInteractionEnabled = false; 180-181 alpha goes back to 1.0 once showDate fires | MATCH |
| Repeat unit options Day, Week, Month | CreateShowDetailsViewController.swift:319-330 getRepeatUnitActions [day, week, month] | MATCH |
| Repeat end options On Date, After 1, 3, 5, 10 Shows | CreateShowDetailsViewController.swift:336-353 getRepeatDateActions [dateAction, after1Action, after3Action, after5Action, after10Action] | MATCH |
| Repeats can only be set at creation, not on edit | RepeatContainerView only embedded in CreateShowDetailsViewController, no editable RepeatContainerView path on edit; CreateShowViewModel.swift:455-491 edit branch has no repeat write | MATCH |
| Cannot pick a date in the past | CreateShowDetailsViewController.swift:297, 302 RPicker.selectDate minDate: Date() | MATCH |
| Postpone limit 3, blocks further moves to later time | Show.swift:92-93 max_postpone_count: Int = 3; CreateShowViewModel.swift:461-470 indicator state .error if postpone_count == max_postpone_count, error string from xcstrings "This Show was already postponed too many times. You cannot postpone it." | MATCH |
| Postpone counter increments only on later moves | CreateShowViewModel.swift:458-459 only enters postpone branch when new_starting_at > show.starting_at | MATCH |
| Pre-warning at penultimate move | CreateShowViewModel.swift:472-487 warning indicators at postpone_count + 1 == max_postpone_count and == max_postpone_count - 1 | MATCH |

## Claims dropped (no iOS source)

| Prior claim | Reason for drop |
|---|---|
| "Must be at least 1 hour between your shows" | Not in iOS code. No grep hit for hour gap rule in LIVE_SHOPPING/Create/. Likely backend rule but no backend source cited in flow.yml. Article rewrites this as "leave a reasonable gap so they don't overlap" without committing to a specific number. |
| "Up to 10 shows in a single batch" | Not directly enforced in iOS code as a hard cap. The end-condition pickers stop at After 10 Shows, but this is a label, not a backend cap. Article describes the four explicit options (1, 3, 5, 10) and lets the reader infer scope. |
| "Default tag Collectibles when skipped" | Tag selection requires picking one tag before Next becomes enabled (CreateShowTagsV2ViewController.swift:60 nextButton.isUserInteractionEnabled = false; bindView toggles to true only when selectedTag is set). No skip path. Article rewrites as "you can only pick one tag". |
| "Android title 60 char limit" | Article scope is iOS-only per RUNBOOK and seller_br targeting. Android caveat removed from FAQ. |

## Visual fidelity (per screen)

| Screen | iOS source contract | Anchor | Status |
|---|---|---|---|
| show-title-input | CreateShowTextFieldViewController, dark bg, centered text field, no icon assets | text-only contract via html_must_not_contain ['<img', '<svg', 'icon-'] | MATCH (HTML uses no img/svg/icon classes) |
| show-tags-grid | CreateShowTagsV2ViewController, 2-col grid, selected white / unselected #1A1A1A, Next pill (chevron is system SF symbol) | text-only contract | MATCH |
| show-cover-options | CreateShowCoverPhotoViewController, Import button uses SF symbol "photo" (system, not Jamble Assets), Unsplash picker | text-only contract; "photo" is a system SF Symbol with no Jamble Assets.xcassets imageset | MATCH |
| show-details-form | CreateShowDetailsViewController, date row literally embeds icon-calendar via UIImage(named: "icon-calendar") | real-icon anchor: required_icons: [icon-calendar] + render the verbatim SVG from RESOURCES/Assets.xcassets/icon-calendar.imageset/icon-calendar.svg + xcassets comment | MATCH |

## Verdict

Zero MISMATCH. The four screens map 1:1 to the iOS CreateShowStep enum cases. The icon-calendar SVG is rendered verbatim from the iOS asset; no other Jamble assets are referenced because the other three screens are text-only at the surfaces under audit. Article is shippable.
