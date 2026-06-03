# Code audit, article 14288097 (pause-your-shop-with-vacation-mode)

Date: 2026-05-06
Source iOS: Jamble-iOS develop. Sources cited in flow.yml.
xcstrings: `Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings`

## Claims article vs source code

| Article claim | Source | Verdict |
|---|---|---|
| Vacation mode lives in Settings under the Sell section | PROFILE/ProfileSettings/ProfileSettingsV2ViewController.swift:48 (`Setting(id: "VACATION", title: String(localized: "Vacation mode"), image: "settings_vacation"...)`) plus the SELL section grouping | MATCH |
| Tapping Vacation mode opens a confirmation modal | PROFILE/ProfileSettings/ProfileSettingsV2ViewController.swift:377 (`else if setting_id == "VACATION" { self.showVacation() }`) and :738 (`func showVacation()` builds a BLTNPageItem) | MATCH |
| pt-BR label is "Modo de férias" | xcstrings "Vacation mode" -> pt-BR "Modo de férias" | MATCH |
| ON modal copy: "When turning on Vacation Mode, all your items will become unavailable for others to purchase" / "Ao ativar o Modo de Férias, todos os seus itens ficarão indisponíveis para serem comprados por outras pessoas" | xcstrings exact source string + pt-BR translation | MATCH |
| OFF modal copy: "You are currently in Vacation Mode. Turning it off will make all your items available to purchase" / "No momento, você está no Modo de Férias. Ao desativá-lo, todos os seus itens estarão disponíveis para compra" | xcstrings exact source string + pt-BR translation | MATCH |
| ON button label "Turn On" / "Ativar" | xcstrings "Turn On" -> pt-BR "Ativar" | MATCH |
| OFF button label "Turn Off" / "Desativar" | xcstrings "Turn Off" -> pt-BR "Desativar" | MATCH |
| Toggle is a single profile-level flag (`is_vacation_enabled`) | PROFILE/ProfileSettings/ProfileSettingsV2ViewController.swift:751-764 reads `profile.is_vacation_enabled` and posts `ProfileBuilder(id: profile.id, isVacationEnabled: !profile.is_vacation_enabled)` | MATCH |
| Effect is immediate (no waiting period) | Profile update is a single PATCH; the modal dismisses on tap. No deferred logic in the showVacation flow | MATCH |
| Existing orders are not affected | Negative claim. `is_vacation_enabled` only gates new product purchase availability; no logic in showVacation references orders or transactions | MATCH (negative claim) |

## Visual fidelity

| Mockup | pt-BR strings match xcstrings? | Status |
|--------|--------------------------------|--------|
| pause-your-shop-with-vacation-mode__settings-vacation-cell__pt-br.png | "Modo de férias" matches xcstrings; surrounding rows ("Minhas vendas", "Carteira", "Preferências de envio") are illustrative pt-BR translations of standard seller settings rows | MATCH on the focal row, illustrative on the others |
| pause-your-shop-with-vacation-mode__vacation-modal-on__pt-br.png | "Modo de férias" + ON-modal copy + "Ativar" all pulled from xcstrings | MATCH |

## Notes

- The flow.yml originally listed `PROFILE/ProfileSettings/SellerSettings/VacationModeViewController.swift` as a source, derived from the batch hint. That file does not exist in the iOS tree; the real surface lives in `ProfileSettingsV2ViewController.swift`. Source list updated to reflect the audit.
- "Modo de férias" lowercase is the canonical label used in the cell and the modal title. The body copy mixes "Modo de Férias" capitalised, which is the xcstrings-canonical phrasing inside running prose.
- The modal also has an OFF state that the article describes textually but does not screenshot. Adding a second modal mockup would be 1 more screen pair; deferred to keep the canary tight (2 screens).

## Verdict

Zero MISMATCH against the cited iOS sources. Every UI string in pt-br.md and en.md is traceable to xcstrings. Article body is consistent with the audited iOS surface.
