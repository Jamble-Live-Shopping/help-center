# Code audit, article 14288120 (use-two-devices-while-hosting)

Date: 2026-05-08
Source iOS: Jamble-iOS develop. Sources cited in flow.yml.
xcstrings: `Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings`

## Claims article vs source code

| Article claim | Source | Verdict |
|---|---|---|
| Joining the same live show on a second device opens a *Remote Control* card with two buttons | LIVE_SHOPPING/Audience/View/ShowAudienceViewController.swift:570-612 (showDeviceMenu builds a BLTNPageItem with title `String(localized: "Remote Control")`, actionButtonTitle `String(localized: "Use as a remote")`, alternativeButtonTitle `String(localized: "Livestream from this device")`) | MATCH |
| Same Remote Control bulletin also appears on the host side when another device of the same account joins | LIVE_SHOPPING/Host/View/ShowHostViewController.swift:580-623 (presentDeviceMenu mirrors the same BLTN with identical xcstrings keys) | MATCH |
| Action button label is `Use como um controle remoto` (pt-BR) / `Use as a remote` (EN) | xcstrings key `Use as a remote` -> pt-BR `Use como um controle remoto` | MATCH |
| Alternative button label is `Transmissao ao vivo a partir deste dispositivo` (pt-BR) / `Livestream from this device` (EN) | xcstrings key `Livestream from this device` -> pt-BR `Transmissão ao vivo a partir deste dispositivo` | MATCH |
| Bulletin description text is `Selecione a primeira opcao se quiser usar este dispositivo como um controle remoto / Caso voce queira fazer uma transmissao ao vivo a partir desse dispositivo, use a segunda opcao` | xcstrings key `Select the first option if you want to use this device as a remote\n\nIn case you want to livestream from this device, use the second option` -> pt-BR `Selecione a primeira opção se quiser usar este dispositivo como um controle remoto\n\nCaso você queira fazer uma transmissão ao vivo a partir desse dispositivo, use a segunda opção` | MATCH (verbatim in pt-BR mockup; description trimmed for editorial flow in body text) |
| Tapping *Livestream from this device* swaps the broadcaster (the new device transmits, the previous one becomes remote) | ShowAudienceViewController.swift:601-606 alternativeHandler -> `viewModel.setAudienceAsBroadcaster(...)` + symmetric ShowHostViewController.swift:613-618 | MATCH |
| The Close Remote control is icon-only (no text label) | UTILS/COMPONENTS/Buttons/CloseRemoteButton.swift:10-93 (UIControl subclass; only UIImageViews in stackViewContainer; no UILabel anywhere) | MATCH (article does not invent a "Close Remote" / "Fechar Controle Remoto" text label) |
| The Close Remote control uses SF Symbol `av.remote.fill` with white tint | CloseRemoteButton.swift:14 `UIImageView(image: .init(systemName: "av.remote.fill"))` + line 16 `tintColor = .white` | MATCH |
| The Close Remote control has a red close badge stacked under the SF Symbol | CloseRemoteButton.swift:25-34 (iconView with `backgroundColor = .customError500` + `UIImage(named: "icon-close")`) + lines 73-89 (rounded iconContainer 20x20, cornerRadius 10, customError500 background, asset is `Assets.xcassets/Search/icon-close.imageset/icon-close.svg`) | MATCH |
| The Close Remote control sits on the host video frame and lets you exit remote mode | ShowHostViewController.swift:57 declares `private var stopRemoteButton: CloseRemoteButton!` + line 926 instantiates it in the host video VC layer | MATCH |
| When the broadcasting device drops, the remote device shows a dark rounded overlay with `Aguarde` + `Seu dispositivo principal parece estar off-line` + a loading indicator | LIVE_SHOPPING/HostV2/ShostHostV2ViewController.swift:5732-5783 (setHostOfflineView: blackNavy alpha 0.8, cornerRadius 17, two-line attributedText `Hold on\n` + `Your main device seems offline`, plus a `QBIndicatorButton` with `loaderButton.start()`) | MATCH |
| `Aguarde` is the pt-BR string for `Hold on` | xcstrings key `Hold on` -> pt-BR `Aguarde` | MATCH |
| `Seu dispositivo principal parece estar off-line` is the pt-BR string for `Your main device seems offline` | xcstrings key `Your main device seems offline` -> pt-BR `Seu dispositivo principal parece estar off-line` | MATCH |

## Visual fidelity

| Mockup | iOS source mapping | Status |
|--------|--------------------|--------|
| use-two-devices-while-hosting__remote-control-picker__pt-br.png | BLTNPageItem rendered by ShowAudienceViewController.showDeviceMenu (and the symmetric host VC). Title = `Controle remoto`, primary CTA `Use como um controle remoto` purple, alternative `Transmissão ao vivo a partir deste dispositivo` purple text-only. xcstrings verbatim. No icons in the bulletin. | MATCH (text-only screen anchored via `html_must_not_contain: ['<img', '<svg', 'icon-']`) |
| use-two-devices-while-hosting__close-remote-button__pt-br.png | CloseRemoteButton component. SF Symbol `av.remote.fill` (white tint, 24x24) stacked above a 20x20 red rounded badge (corner radius 10, `customError500` red) containing the verbatim Jamble asset `Assets.xcassets/Search/icon-close.imageset/icon-close.svg`. Side helper card is editorial copy, not a UI string. | MATCH (icon-only screen anchored via `required_icons: [av.remote.fill, icon-close]`. The icon-close SVG path in the mockup is the verbatim file content from the iOS asset.) |
| use-two-devices-while-hosting__host-offline-overlay__pt-br.png | setHostOfflineView builds a UIView with `.blackNavy.withAlphaComponent(0.8)` background and `cornerRadius = 17`. Inner UILabel uses two attributed runs: `Hold on\n` (16pt medium) + `Your main device seems offline` (28pt rounded semibold), centered. Below: a QBIndicatorButton (50pt height, transparent, white indicator, started). | MATCH (text-only screen anchored via `html_must_not_contain: ['<img', '<svg', 'icon-']`. Spinner is CSS-only animation, no SVG/IMG/icon- markup.) |

## Anchor decisions (rule 10e compliance)

| Screen | Anchor type | Why |
|--------|-------------|-----|
| remote-control-picker | text-only (`html_must_not_contain: ['<img', '<svg', 'icon-']`) | The BLTNPageItem in iOS code has zero icons inside the dialog body. Anchoring as text-only blocks any future regression that smuggles invented glyphs back in. |
| close-remote-button | real-icon (`required_icons: [av.remote.fill, icon-close]`) | The component is icon-only by definition. Both glyphs are anchored explicitly: the SF Symbol via `<!-- icon: av.remote.fill -->` comment, and the Jamble asset via `<!-- icon: icon-close -->` comment + the verbatim SVG path embedded inline. |
| host-offline-overlay | text-only (`html_must_not_contain: ['<img', '<svg', 'icon-']`) | The native overlay has only text + a UIKit indicator (no asset-backed icon). Anchoring as text-only forces the spinner to stay CSS-only. |

## Stale-feature audit

| Stale claim removed in this rewrite | Evidence | Action |
|---|---|---|
| Article previously documented an Android dual-device prompt with bespoke labels | No Android source files were audited for this article. The two iOS VCs above are the only audited surfaces. | Removed from body. Added `must_not_say: "Android-specific UI states"` to flow.yml. Article now scopes to iOS. |
| Article previously called the icon-only control `Close Remote` / `Fechar Controle Remoto` | CloseRemoteButton.swift has no UILabel. The component is icon-only. | Removed text labels from the body. Added `Close Remote` and `Fechar Controle Remoto` to forbidden_terms in flow.yml so the regression is caught by the validator. |
| Article previously claimed the Android takeover dialog uses the words `Stay as remote control` / `Take over` | No Android source audited; the previous mockup was invented. | Mockup deleted. Body switches to neutral copy that maps to the audited iOS bulletin. |

## Notes

- The pt-BR description text in the body uses ASCII transliteration (no diacritics) to match the editorial baseline of other v2 rewrites in main today. The mockup screen renders the verbatim diacritic text from xcstrings (`Selecione a primeira opção…`) so the screenshot matches what the user actually sees.
- The Close Remote button has no xcstrings key because it is icon-only. The body intentionally describes it as `o indicador no canto superior direito` (pt-BR) / `the indicator in the top right corner` (EN) to avoid inventing a label.
- The offline overlay attributedText concatenates two runs in code; the mockup mirrors that structure with `.hold-on` (16pt) above `.offline-headline` (26-28pt) on a single dark card.

## Verdict

Zero MISMATCH against the cited iOS sources. Article is grounded in CloseRemoteButton.swift, ShowAudienceViewController.swift, ShowHostViewController.swift, ShostHostV2ViewController.swift, and Localizable.xcstrings. All pt-BR strings are xcstrings verbatim or labelled as editorial copy. No invented UI.
