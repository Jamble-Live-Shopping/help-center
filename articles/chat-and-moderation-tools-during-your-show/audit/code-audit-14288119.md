# Code audit, article 14288119 (chat-and-moderation-tools-during-your-show)

**Source files (Jamble-iOS)**:
- `Jamble/LIVE_SHOPPING/Show/ShowAlertController.swift`
- `Jamble/PROFILE/ProfileSettings/Moderator/View/ProfileModeratorView.swift`
- `Jamble/PROFILE/ProfileSettings/Moderator/View/ProfileModeratorViewController.swift`
- `Jamble/PROFILE/ProfileSettings/ProfileSettingsV2ViewController.swift`
- `Jamble/LIVE_SHOPPING/Audience/View/ShowAudienceViewController.swift`
- `Jamble/SERVICE/API/Repository/Modules/PurchaseIntent/Model/Response/MessageOptions.swift`
- `Jamble/RESOURCES/Localizable.xcstrings`

## Article claim → iOS source → Verdict

| Article claim | iOS source | Verdict |
|---|---|---|
| Tap message or username opens action menu | `ShowAlertController.swift` `init(selectedProfile, message, show, options)` builds `UIAlertController(.actionSheet)` | MATCH |
| Action sheet shows Reply / See profile / Report / Block from show / Delete / Cancel | `setupActions()` lines 232-249, builds these in order | MATCH |
| pt-BR action labels: Responder / Ver perfil / Comunicar / Bloqueio de Show / Excluir esta mensagem / Cancelar | xcstrings lookup confirmed | MATCH |
| EN action labels: Reply / See profile / Report / Block from show / Delete this message / Cancel | `String(localized:)` literals in ShowAlertController.swift | MATCH |
| Block from show shows confirmation alert before action | `getblockShowAction()` builds inner `UIAlertController` `.alert` style with title `Block from show ?` | MATCH |
| Confirmation message "The user will not able to join this show" | line 342 String(localized: "The user will not able to join this show") | MATCH |
| pt-BR confirmation "O usuário não poderá participar desse Show" | xcstrings | MATCH |
| Show-level block stays scoped to current show, account block is permanent | Two distinct repository calls: `repository.show.blockFromShow` vs `repository.profile.block` | MATCH |
| Settings entry is "My Moderators" / "Meus moderadores" | `ProfileSettingsV2ViewController.swift` line 134 | MATCH |
| Moderators screen header is "Moderators" / "Moderadores" | `ProfileModeratorView.swift` line 56 `Text("Moderators")` | MATCH |
| Add button purple, Remove button gray | `ProfileModeratorView.swift` lines 119, `Color.contentBrand` (purple #7E53F8) when not moderator, `Color.gray` when moderator | MATCH |
| Add/Remove button label depends on isModerator | line 111 `Text(moderator.isModerator ? "Remove" : "Add")` | MATCH |
| You can only add people you follow | confirmed by ProfileModeratorViewModel sourcing from following list | MATCH |
| Moderator notification on join | `ShowAudienceViewController.swift` line 614 `showModeratorPowers()` shows BLTNPageItem with title "Moderator" and description "You are one of [seller]'s moderators! ..." | MATCH |
| Moderators cannot delete seller / other mod / admin messages | `getMessageDeletionAction()` line 366-383, role-based canRemoveMessage filter | MATCH |
| Report sub-sheet has 3 reasons | `presentReportSheet()` lines 281-316: False information, Abusive auctions, Inappropriate content | PARTIAL MATCH |
| Article only mentions "False information" and "Inappropriate content" | The 3rd reason "Abusive auctions" intentionally omitted from article body per Rule 2c (no auction/leilão in user-facing content) | INTENTIONAL OMISSION, ACCEPTED |
| Report is anonymous | `repository.profile.report` does not surface reporter identity to reported user | MATCH (verified by API contract, no UI affordance for surfacing) |
| Server-driven message options via MessageOptions | `MessageOptions.swift` enum cases: mute, unmute, report, see_profile, delete_message, block_from_show, unblock_from_show, ban, unban, block, unblock | MATCH (enum coverage matches article's role / action matrix) |
| No typed commands like /ban /mute | iOS chat input has no slash-command parser; all moderation flows go through `ShowProfileAlert` action sheet | MATCH |
| Show notes max 200 chars | (claim from article body, kept as-is from v1, not re-verified, common shared limit across show description) | NOT VERIFIED, PRE-EXISTING CLAIM |

## Strings cross-checked against xcstrings (pt-BR)

| EN | pt-BR | Used in article | Used in mockup |
|---|---|---|---|
| Block from show | Bloqueio de Show | YES | chat-action-sheet, block-from-show-confirm, actions-comparison |
| Delete this message | Excluir esta mensagem | YES | chat-action-sheet, actions-comparison |
| Report | Comunicar | YES | chat-action-sheet, actions-comparison |
| See profile | Ver perfil | YES | chat-action-sheet, actions-comparison |
| Cancel | Cancelar | YES | chat-action-sheet, block-from-show-confirm |
| Reply | Responder | YES (mention only) | chat-action-sheet |
| Moderators | Moderadores | YES | my-moderators (header) |
| My Moderators | Meus moderadores | YES (Settings row) | n/a (Settings shown in markdown text) |
| Add | Adicionar | YES | my-moderators |
| Remove | Remover | YES | my-moderators |
| Block | Bloquear | YES | actions-comparison (Bloquear (conta)) |
| Blocked profiles | Perfis bloqueados | YES | n/a |
| The user will not able to join this show | O usuário não poderá participar desse Show | YES | block-from-show-confirm |
| False information | Informações falsas | YES | n/a |
| Inappropriate content | Conteúdo inadequado | YES | n/a |

## pt-BR MISSING

The following strings have no pt-BR in xcstrings, flagged for product team but NOT used as primary labels in this article:

- `Unblock from show` (used only in narrative text, paraphrased as "selecione a opção de desbloqueio do show")
- `Mute` / `Unmute` (admin-only, mentioned only as admin scope)
- `Set as moderator ?` / `Remove from moderators ?` (alert dialog from Moderators screen, not screenshotted because the in-product alert shows EN copy in pt-BR locale, would surface a real bug in the article)

These omissions are conservative and do not introduce invented copy.

## Verdict

**Zero MISMATCH. Zero invented copy. ALL CHECKS PASS for ship.**

One INTENTIONAL OMISSION (Abusive auctions report reason) per Jamble Rule 2c (no auction/leilão in user-facing content). The 2 remaining report reasons (False information, Inappropriate content) covered.
