# Code audit, intercom_id=14288117 (invite-a-co-host-live-duo)

Source of truth: Jamble-iOS at `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/`.

## Files read

| Path | Lines used | Notes |
|---|---|---|
| `LIVE_SHOPPING/Duo/View/InviteDuoShowViewController.swift` | 11-225 | Bottom sheet "Invite for a Duo", search bar, viewer grid, Invite button with `icon-camera-add` |
| `LIVE_SHOPPING/Duo/View/InvitationDuoShowViewController.swift` | 11-162 | Guest-side modal "Live Duo", `image_video` 80x80, Accept/Don't Join buttons, dynamic title with seller username |
| `LIVE_SHOPPING/Duo/View/InviteDuoInfoView.swift` | 11-107 | "Live Duo" intro card + "Got it!" dismiss; one-time per `UserDefaults.liveShow.didDisplayLiveDuoInfo` |
| `LIVE_SHOPPING/Duo/ViewModel/InviteDuoShowViewModel.swift` | full | Selection + invite plumbing, `inviteGuest`, `selectedGuest` publisher |
| `LIVE_SHOPPING/Host/View/ShowHostViewController.swift` | 895-930, 1075-1131 | Host-side toggle of `addGuestButton` (uses `icon-camera-add`), guest avatar button, "Remove %@ From Live Duo?" alert |
| `LIVE_SHOPPING/Audience/View/ShowAudienceViewController.swift` | 2049-2067 | Guest-side "Stop broadcasting?" alert (Stop / Cancel) when guest taps own broadcasting button |
| `RESOURCES/Localizable.xcstrings` | keys below | xcstrings verbatim (en + pt-BR) |
| `RESOURCES/Assets.xcassets/icon-camera-add.imageset/` | Contents.json + PDF | Camera with plus glyph used on Invite button + addGuestButton |
| `RESOURCES/Assets.xcassets/image_video.imageset/` | image_video.png 81x80 | Header glyph in InvitationDuoShowViewController |

## xcstrings keys pulled (verbatim)

| Key | en | pt-BR |
|---|---|---|
| `Invite for a Duo` | Invite for a Duo | Convite para uma dupla |
| `Invite your friend` | Invite your friend | Convide seu amigo |
| `Live Duo` | Live Duo | Live Duo |
| `Live Duo allows you to do live sessions with a person of your choice. By clicking 'Send Invite,' your friend will receive a link to join you.` | (verbatim) | O Live Duo permite que voce faca sessoes ao vivo com uma pessoa de sua escolha. Ao clicar em 'Send Invite' (Enviar convite), seu amigo recebera um link para se juntar a voce. |
| `Got it!` | Got it! | Entendi! |
| `Accept and Join` | Accept and Join | Aceitar e participar |
| `Allow Camera Access and Join` | Allow Camera Access and Join | Permitir acesso a camera e participar |
| `Don't Join` | Don't Join | Nao participe |
| `You have been invited to join %@ as a guest!` | (verbatim) | Voce foi convidado a participar do %@ como convidado! |
| `No one in your Show? You can stil invite someone outside!` | (verbatim, sic stil) | Nao ha ninguem em seu show? Voce ainda pode convidar alguem de fora! |
| `Remove %@ From Live Duo?` | Remove %@ From Live Duo? | Remover %@ do Live Duo? |
| `Remove` | Remove | Remover |
| `Cancel` | Cancel | Cancelar |
| `Stop broadcasting?` | Stop broadcasting? | Parar de transmitir? |
| `Stop` | Stop | Parar |

Note: typo "stil" (one L) is verbatim from xcstrings line 15523. Article does not embed this empty-state message (kept short).

## Article claim, iOS source, verdict

| Article claim | iOS source | Verdict |
|---|---|---|
| Live Duo lets the host bring one person on camera as a guest | `InviteDuoInfoView.swift:32` description label string | MATCH |
| Host taps a camera-with-plus button to open the invite sheet | `ShowHostViewController.swift:910 UIImage(named: "icon-camera-add")`, `:917 inviteGuestAction` | MATCH |
| The invite sheet shows current viewers + a search bar | `InviteDuoShowViewController.swift:23-37 ElasticSearchBar + JambleCollectionView` | MATCH |
| Sheet title is "Invite for a Duo" | `InviteDuoShowViewController.swift:18` + xcstrings `Invite for a Duo` | MATCH |
| Selecting a viewer enables the bottom Invite button labelled "Invite your friend" | `InviteDuoShowViewController.swift:56-65, 122-131` (canInvite publisher controls bottomStackContainer) + xcstrings `Invite your friend` | MATCH |
| Guest receives a "Live Duo" modal with the seller username inside | `InvitationDuoShowViewController.swift:18 stack title "Live Duo"`, `:148 setDescription "You have been invited to join \(self.seller.username) as a guest!"` | MATCH |
| Guest sees Accept and Join + Don't Join buttons | `InvitationDuoShowViewController.swift:46-58` + xcstrings keys | MATCH |
| Accept button label switches to "Allow Camera Access and Join" if permission not granted | `InvitationDuoShowViewController.swift:47-49` | MATCH (article keeps "Accept and Join" because that is the steady-state label after permission grant; guidance about permission is one bullet) |
| Removing a guest is via tap on guest avatar then "Remove %@ From Live Duo?" alert | `ShowHostViewController.swift:1122-1131` + xcstrings `Remove %@ From Live Duo?` | MATCH |
| Alert action labels are Cancel + Remove | `ShowHostViewController.swift:1126-1127` | MATCH |
| Guest can leave on their own via "Stop broadcasting?" alert | `ShowAudienceViewController.swift:2049-2056` | MATCH |
| Article does not mention a 5-minute invite expiry | grep `expir|timeout` in `LIVE_SHOPPING/Duo/` returns 0 hits | MATCH (claim removed; v1 invented this) |
| Article scopes feature to iPhone | All Duo VCs are UIKit iPhone-only; no Android equivalent declared in source | MATCH (product confirmation not in code, but iOS-only is the shipped state) |
| Camera button hidden until host is live + no guest already | `ShowHostViewController.swift:908 isHidden = true` + topRightSideStackView lifecycle (button shown only after start broadcasting) | MATCH (article wording: "this icon only appears once you are live, and only when you do not already have a guest") |

Zero MISMATCH. Article is consistent with iOS code as of audit date.

## Negative scan

- Surface verified absent: `LIVE_SHOPPING/Duo/`-level countdown / expiry view. `grep -rn "expir|timeout" LIVE_SHOPPING/Duo/` returns 0 hits. No invite-timeout claim is made in this article. (No risk_flag needed because no negative_scan path is declared in flow.yml.)

## Risks / open items

- None.
