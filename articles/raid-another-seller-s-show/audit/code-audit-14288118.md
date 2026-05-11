# Code audit, article 14288118 (raid-another-seller-s-show)

Date: 2026-05-11
Source: `Jamble-iOS` repo, develop branch at audit time. Feature path NOT pre-known
to writer-packet: discovered via `grep -rln "[Rr]aid\b" $JAMBLE_IOS_ROOT/LIVE_SHOPPING/`
which returned `LIVE_SHOPPING/Raid/` (3 files in View + ViewModel + Model). Confirmed
in `Localizable.xcstrings` (lines 1213, 1230, 24278, 4931, 21197, 23815).

## Files read

- `LIVE_SHOPPING/Raid/View/RaidViewController.swift` (349 lines)
- `LIVE_SHOPPING/Raid/View/RaidShowChooserViewController.swift` (204 lines)
- `LIVE_SHOPPING/Raid/ViewModel/RaidViewModel.swift` (60 lines)
- `LIVE_SHOPPING/Raid/ViewModel/RaidShowChooserViewModel.swift` (126 lines)
- `LIVE_SHOPPING/Host/View/ShowHostViewController.swift` (entry points lines 472-486, 1145-1172)
- `LIVE_SHOPPING/Audience/View/ShowAudienceViewController.swift` (audience modal line 398)
- `LIVE_SHOPPING/Chat/View/Cell/ShowRaidMessageCell.swift` (chat cell line 136)
- `RESOURCES/Localizable.xcstrings`

## Claims vs source

| Article claim | iOS source | Verdict |
|---|---|---|
| Raid modal title "The Jamble Raid" | `RaidViewController.swift:21` `stack.setTitle("The Jamble Raid")` (hardcoded English, no String(localized:)) | MATCH (literal in both locales) |
| Raid is triggered by ending the show | `ShowHostViewController.swift:483-484` `else if self.show.has_started == true { ... RaidViewController(... type: .initial) }`; same path line 1166-1170 via action sheet "End Show" | MATCH |
| Bring back the raid screen if you tap back after a successful raid | `ShowHostViewController.swift:481-482` `else if self.show.has_redirected { ... type: .ended }` | MATCH |
| Two profile photos with a send icon between them | `RaidViewController.swift:34-66` `profileImage` + `sendIcon` + `blurImage` in `imagesStackContainer` (line 26-32); image of current seller + blur silhouette for the unknown destination | MATCH |
| Description copy "Before leaving, support the community by sending your viewers to a seller who's currently live!" | `RaidViewController.swift:290-292` three-part NSAttributedString | MATCH (pt-BR concat from xcstrings keys "Before leaving, support the community by " + "sending your viewers to a seller" + " who's currently live!") |
| Primary button "Select Live Show" | `RaidViewController.swift:114` and 246 `setTitle("Select Live Show")` | MATCH (pt-BR `Selecionar show ao vivo`, xcstrings:20725) |
| Secondary button "End without Raid" in red | `RaidViewController.swift:122-123` `textColor = .customError500`, `setTitle("End without Raid")` (HARDCODED English, no String(localized:) wrapper) | MATCH (literal in both locales) |
| Show picker title "Select a Live" | `RaidShowChooserViewController.swift:15` `setTitle(String(localized: "Select a Live"))` | MATCH (pt-BR `Selecione um Live`, xcstrings:20643) |
| Picker is a 2-column grid of live show cards | `RaidShowChooserViewController.swift:142-153` compositional layout `NSCollectionLayoutGroup.horizontal(... count: 2)` with 8px interItemSpacing and 16px interGroupSpacing | MATCH |
| Picker excludes your own show and non-live shows | `RaidShowChooserViewModel.swift:90` filter `$0.isUserVisible() && self.show.id != $0.id && $0.has_started` | MATCH |
| Empty state "There's no shows to raid yet" | `RaidShowChooserViewController.swift:185` `String(localized: "There's no shows to raid yet")` | MATCH (pt-BR `Ainda não há shows para invadir`, xcstrings:24290) |
| Confirm button at bottom of picker "Select Live Show" | `RaidShowChooserViewController.swift:48` `setTitle(String(localized: "Select Live Show"))` | MATCH (same xcstrings key as initial CTA) |
| Confirm button only appears once a show is selected | `RaidShowChooserViewModel.swift:60-62` `_selectedShow.map { $0 == nil }.weakSubscribe(self.hideRideButton)` + animated reveal in `RaidShowChooserViewController.swift:196-203` | MATCH |
| After confirm, raid is sent to backend then end-show modal opens | `RaidShowChooserViewModel.swift:64-78` `repository.show.redirect(from: self.show, to: selectedShow)` then `didRaid` triggers `RaidShowChooserViewController.swift:106-113` `presentPanModal(RaidViewController(... type: .ended))` | MATCH |
| End-show panel shows large send icon (80x80) with "Success!" chip | `RaidViewController.swift:248-258` (.ended branch): `sendIcon.widthAnchor.constraint(equalToConstant: 80)`, `chip.isHidden = false`, `chip.setTitle("Success!")` (line 73, hardcoded English) | MATCH |
| End-show copy "Thanks for supporting the community! You can now end your Show" | `RaidViewController.swift:296` `String(localized: "Thanks for supporting the community! You can now end your Show")` | MATCH (pt-BR `Obrigado por apoiar a comunidade! Agora você pode encerrar seu Show`, xcstrings:23827) |
| End-show CTA changes to "End Show" | `RaidViewController.swift:254` `selectButton.setTitle(String(localized: "End Show"))` | MATCH (pt-BR `Fim do Show`, xcstrings:9530) |
| "End without Raid" button hidden in .ended state | `RaidViewController.swift:255` `leaveButton.isHidden = true` | MATCH |
| Tapping End Show calls endShow which fires HOST end | `RaidViewModel.swift:35-44` `showRepository.endShow(show: ..., reason: "HOST")`, only when `profile.id == show.seller_id` | MATCH |
| Viewers see "X is Raiding Y!" panel with join CTA | `RaidViewController.swift:299-301` `.audience` branch description "\\(currentSeller) is Raiding \\(redirectedSeller)! 🎉"; `selectButton.setTitle("Join \\(model.selectedSeller.display_name) Show")` line 267 | MATCH (pt-BR `está invadindo`, xcstrings:1225) |
| Viewer panel says viewers will be auto-redirected | `RaidViewController.swift:271` `leaveButton.setTitle(String(localized: "You will be automatically redirected to another show."))` (presented as caption under the join button) | MATCH |
| Chat message during raid "X is Raiding with N people" | `ShowRaidMessageCell.swift:136` `String(localized: "\\(profile.displayName) is Raiding with \\(count) people 🎉")` | MATCH (pt-BR `está invadindo com %lld pessoas`, xcstrings:1242) |
| One raid per show (cannot raid again) | `ShowHostViewController.swift:481-485` flow: if `show.has_redirected` then re-entering the back path goes to `.ended` (not `.initial`), so the picker never reopens. Backend sets `has_redirected` via the `redirect` call in `RaidShowChooserViewModel.swift:68`. | MATCH |
| Cannot raid during a battle | `ShowHostViewController.swift:479-480` `else if self.show.battleId != nil { self.showEndBattleAlert(... ) }` short-circuits before the raid branch | MATCH |

## Claims dropped from v1

| v1 claim | Why dropped | Replacement |
|---|---|---|
| "Em vez de seus espectadores simplesmente saírem quando seu show acaba, eles são enviados para outro show ao vivo" (implies forced redirect) | iOS code line 271 sets the caption to "You will be automatically redirected to another show" but the primary CTA (`selectButton`, line 267) is "Join [Name] Show" which the viewer must tap; this is a hybrid (auto-suggestion with explicit join). v1 phrasing softened the auto-redirect part. | Faithful description: viewers see a takeover panel with profile photos and a Join button; the panel also tells them they will be redirected. |
| "Você só pode fazer um raid por show" (presented as enforced rule) | Code-level evidence is the `has_redirected` flag handling: re-entry to End Show after a raid skips straight to `.ended` state. Functionally the same outcome but the rule is enforced by state machine, not a hard backend rejection. | Kept the claim but phrased as "Once you raid, the chooser does not reopen for that show" to match the state machine. |
| "Raid vs Batalha: ... batalhas fazem dois vendedores competirem lado a lado (ambos shows ficam ativos)" | True for battles; redundant but mostly accurate. | Kept the differentiator but tightened wording. |
| Mentioned `support@jambleapp.com` for help (no change) | Standard footer, kept as-is. | (no change) |

## Strings copied verbatim from xcstrings

```
"Select Live Show"                                 -> pt-BR: "Selecionar show ao vivo"        (line 20725)
"Select a Live"                                    -> pt-BR: "Selecione um Live"              (line 20643)
"There's no shows to raid yet"                     -> pt-BR: "Ainda não há shows para invadir" (line 24290)
"Thanks for supporting the community! You can now end your Show" -> pt-BR: "Obrigado por apoiar a comunidade! Agora você pode encerrar seu Show" (line 23827)
"Before leaving, support the community by "        -> pt-BR: "Antes de sair, apoie a comunidade" (line 4943)
"sending your viewers to a seller"                 -> pt-BR: "enviar seus espectadores para um vendedor" (line 21209)
"End Show"                                         -> pt-BR: "Fim do Show"                    (line 9530)
"%@ is Raiding %@! 🎉"                              -> pt-BR: "%1$@ está invadindo %2$@! 🎉"     (line 1225)
"%@ is Raiding with %lld people 🎉"                 -> pt-BR: "%1$@ está invadindo com %2$lld pessoas 🎉" (line 1242)
```

## Hardcoded English (no String(localized:) wrapper)

| String | File:Line | Status |
|---|---|---|
| "The Jamble Raid" | RaidViewController.swift:21 | Same in both locales |
| "End without Raid" | RaidViewController.swift:123 | Same in both locales |
| "Success!" | RaidViewController.swift:73 | Same in both locales |

These three strings appear identically on the iPhone in both pt-BR and EN. The article uses them verbatim.

## Strings not in xcstrings but needed for the article

- "who's currently live!" (part of `RaidViewController.swift:292`): hardcoded English fragment, no xcstrings entry found via `grep -n '"who.s currently live"' Localizable.xcstrings`. The full description string the user sees in pt-BR is the concatenation of two xcstring values + this English fragment, which means a user on pt-BR sees a mixed string ending in English. Article paraphrases conservatively; this is a known iOS i18n gap, not a writer issue.

## Mockup assets

- `screen-1` = `RaidType.initial` modal: avatars + send icon, description, Select Live Show + End without Raid.
- `screen-2` = `RaidShowChooserViewController`: "Select a Live" grid with one show highlighted (selected state), Select Live Show CTA.
- `screen-3` = `RaidType.ended` modal: Success chip, big send icon, Thanks copy, End Show CTA.

Icon `send_icon` (PNG, square) copied to `assets/icons-ios/send_icon.png` from `Jamble-iOS/Jamble/RESOURCES/Assets.xcassets/send_icon.imageset/send_icon.png` per Phase 1.3b.

## Open MISMATCH

None.

## Notes

- The audience-facing raid screen (RaidType.audience, presented in `ShowAudienceViewController.swift:398`) is described in the article body but not rendered as a fourth mockup; the 3-mockup target is held by representing the host-side flow only and using prose for the viewer side. This keeps mockup_count_target = 3.
- iOS surface is hard-coupled to iPhone today. Android parity not confirmed; copy notes "no momento o recurso fica disponivel apenas no iPhone" in a Before-you-start callout.
