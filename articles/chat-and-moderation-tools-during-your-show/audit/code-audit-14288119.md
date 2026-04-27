# Code audit, article 14288119

**iOS sources**: ShowAlertController.swift, ProfileModeratorView.swift, ProfileSettingsV2ViewController.swift, ShowAudienceViewController.swift, MessageOptions.swift, Localizable.xcstrings.

## Article claim, iOS source, Verdict

| Article claim | iOS source | Verdict |
|---|---|---|
| Tap message/username opens action sheet | ShowAlertController.swift init builds UIAlertController(.actionSheet) | MATCH |
| Action sheet has Reply / See profile / Report / Block from show / Delete / Cancel | setupActions() lines 232-249 | MATCH |
| pt-BR labels (Responder, Ver perfil, Comunicar, Bloqueio de Show, Excluir esta mensagem, Cancelar) | xcstrings | MATCH |
| EN labels (Reply, See profile, Report, Block from show, Delete this message, Cancel) | String(localized:) literals | MATCH |
| Block from show shows confirm dialog "Block from show ?" | getblockShowAction() builds inner UIAlertController .alert | MATCH |
| Confirm message "The user will not able to join this show" | ShowAlertController.swift line 342 | MATCH |
| pt-BR confirm "O usuário não poderá participar desse Show" | xcstrings | MATCH |
| Show-level vs account-level block are separate flows | repository.show.blockFromShow vs repository.profile.block | MATCH |
| Settings row "My Moderators" / "Meus moderadores" | ProfileSettingsV2ViewController.swift line 134 | MATCH |
| Inside-screen header "Moderators" / "Moderadores" | ProfileModeratorView.swift line 56 | MATCH |
| Add btn purple, Remove btn gray | ProfileModeratorView.swift line 119 (Color.contentBrand vs Color.gray) | MATCH |
| You can only add people you follow | ProfileModeratorViewModel sources from following | MATCH |
| Moderator notification on join | ShowAudienceViewController.swift line 614 BLTNPageItem | MATCH |
| Moderators cannot delete seller/admin/other-mod messages | getMessageDeletionAction() role filter line 366-383 | MATCH |
| Report sub-sheet has 3 reasons (False info, Abusive auctions, Inappropriate content) | presentReportSheet() lines 281-316 | PARTIAL MATCH |
| Article omits "Abusive auctions" | per Rule 2c (no auction/leilão in user-facing) | INTENTIONAL OMISSION |
| Reports anonymous | repository.profile.report API | MATCH |
| No typed commands /ban /mute | iOS chat input has no slash-command parser | MATCH |

## pt-BR MISSING (flagged, not used as primary copy)

- Unblock from show, Mute, Unmute, Set as moderator ?, Remove from moderators ?

## Verdict

**Zero MISMATCH. Zero invented copy. ALL CHECKS PASS for ship.**
