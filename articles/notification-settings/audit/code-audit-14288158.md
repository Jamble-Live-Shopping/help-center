# Code audit, article 14288158 (notification-settings)

Date: 2026-05-06
Source iOS: Jamble-iOS develop. Sources cited in flow.yml.
xcstrings: `Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings`

## Claims article vs source code

| Article claim | Source | Verdict |
|---|---|---|
| Notifications screen lives under Settings > Account > Notifications | PROFILE/ProfileSettings/Notifications/NotificationsViewController.swift (mounted from the Account section of ProfileSettingsV2ViewController) | MATCH |
| The screen renders 4 collapsible category sections | PROFILE/ProfileSettings/Notifications/View/NotificationsView.swift:64-86 (`ForEach(notificationsSettings.data.indices)`, sectionHeader + section.settings) | MATCH (count of 4 is the live data shape; the iOS code is data-driven and would render any count the backend returns) |
| Each section has a parent toggle that controls all child toggles | NotificationsView.swift:96-119 sectionHeader uses `viewModel.checkSectionSettingValues` and `viewModel.updateSection(title:isOn:)` to flip every child setting in the section | MATCH |
| Permission sheet appears when iOS push permission is off | PROFILE/ProfileSettings/Notifications/View/NotificationPermissionSheet.swift surfaces the sheet when `requestNotificationAuthorizationIfNeeded` rejects, and copy uses xcstrings entries below | MATCH |
| Permission sheet title pt-BR "Mantenha-se atualizado com as notificações!" | xcstrings "Stay Updated with Notifications!" -> pt-BR | MATCH |
| Permission sheet body pt-BR | xcstrings "90% of top deals, live shows and giveaways are unlocked through notifications" -> pt-BR | MATCH |
| Permission CTA pt-BR "Ativar notificações" | xcstrings "Turn On Notifications" -> pt-BR | MATCH |
| Section titles render in English on pt-BR locale | NotificationsView.swift:104 `Text(section.title)` reads from a `NotificationSettings` payload whose title field is not run through `String(localized:)`. Confirmed by absence of localised category keys in xcstrings (Promotional / Live Shows / Transactions are missing from xcstrings; only Activity has a translation that the dynamic surface does not consume). | MATCH (documented as known limitation in flow.yml.risk_flags + resolved_decisions) |

## Visual fidelity

| Mockup | pt-BR strings match xcstrings? | Status |
|--------|--------------------------------|--------|
| notification-settings__notifications-list__pt-br.png | Section titles in English (matches the live iOS surface). Sub-text under each section is editorial pt-BR description, not pulled from xcstrings | MATCH (English titles intentional, sub-text editorial) |
| notification-settings__permission-sheet__pt-br.png | Title, body and CTA all pulled from xcstrings | MATCH |

## Notes

- iOS does NOT translate the notification section titles. They are rendered raw from a backend payload whose `title` field is not localised. `flow.yml.risk_flags` documents this; `resolved_decisions` records that we ship the article with the live state, and a server-side translation is a separate backend track.
- Notification screen has no static "Account" section title in xcstrings under that exact key; the routing path is documented in the article body and verified in `ProfileSettingsV2ViewController.swift`.
- The article does not document any individual sub-toggle (e.g. "Followers", "Likes", "Bookmarked product from show") because those names are also dynamic backend data and the live label set could shift between releases. Only the 4 stable categories are described.

## Verdict

Zero MISMATCH against the cited iOS sources. Every UI string the article asserts is either pulled from xcstrings or matches the live iOS surface (the English category titles).
