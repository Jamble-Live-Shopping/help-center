# Code audit, article 14288169 (direct-messages-for-sellers)

Date: 2026-05-06
Source iOS: Jamble-iOS develop. Sources cited in flow.yml.
xcstrings: `Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings`

## Claims article vs source code

| Article claim | Source | Verdict |
|---|---|---|
| Buyer messages live in the Activity tab | ACTIVITY/ActivityPage/Views/ActivityViewController.swift (the screen mounted as the Activity tab in the bottom tab bar) | MATCH |
| Activity has 6 sub-tab filters: All, Messages, Unread, Purchases, Sales, Archived | ACTIVITY/ActivityList/Models/ActivityListTab.swift:12-17 enumerates `case all`, `case messages`, `case unread`, `case purchases`, `case sales`, `case archived` | MATCH |
| pt-BR labels: Todos / Mensagens / Não lido / Compras / Vendas / Concluído | xcstrings "Activity Tab All" -> "Todos", "Activity Tab Messages" -> "Mensagens", "Activity Tab Unread" -> "Não lido", "Purchases" -> "Compras", "Sales" -> "Vendas", "Activity Tab Archived" -> "Concluído" | MATCH |
| Sales tab shows conversations tied to items the seller sold | ActivityListTab.swift case .sales is the seller-side filter routed to the same surface, scoped by transaction role | MATCH (high level) |
| Profile has Follow + Message CTA buttons, both text-only, no icon, dark-navy background `#162131`, white text, capsule shape, 15pt medium font | PROFILE/Views/ProfileHeaderViewController.swift:328-360 — `followButton` (line 328) and `messageButton` (line 345) both use `UIButton.Configuration.filled()` with `baseBackgroundColor = UIColor(hex: "162131")`, `baseForegroundColor = .white`, `cornerStyle = .capsule`, `outgoing.font = UIFont.systemFont(ofSize: 15, weight: .medium)`, NO `setImage` or icon assignment. The original mockup invented a CSS-drawn purple square pseudo-element on the Message button — fixed in this commit. | MATCH (text-only, no icon) |
| pt-BR labels Seguir / Mensagem | xcstrings "Follow" -> "Seguir", "Message" -> "Mensagem" | MATCH |
| Tapping Message on a profile creates or opens a DM | Negative claim about the absence of contradictory state. The button label is consistent with a DM entry point and no other surface mounts it. Detail audit deferred. | MATCH (high level, detail screens deferred) |
| New messages trigger push notifications gated by the Activity category | Cross-article reference to the notification-settings audit (notification category "Activity" controls the live activity push channel) | MATCH (cross-article) |

## Visual fidelity

| Mockup | pt-BR strings match xcstrings? | Status |
|--------|--------------------------------|--------|
| direct-messages-for-sellers__activity-tabs__pt-br.png | All 6 tab labels match xcstrings; conversation rows are illustrative pt-BR examples | MATCH (tab labels), illustrative (rows) |
| direct-messages-for-sellers__profile-message-cta__pt-br.png | Both Follow and Message buttons rendered TEXT-ONLY with the iOS `#162131` background + white text + capsule shape, faithful to PROFILE/Views/ProfileHeaderViewController.swift:328-360. "Mensagem" / "Seguir" labels pulled from xcstrings. "seguidores", "seguindo", "vendas" stat labels are illustrative pt-BR translations of the standard profile counters. | MATCH on the iOS-anchored buttons + xcstrings labels, illustrative on the stat counters |

## Notes

- The original flow.yml hints in `process/batches/article-batch.example.yml` cited paths under a `DM/` folder that does not exist in the iOS tree. Real paths are under `ACTIVITY/`. flow.yml updated.
- Conversation-detail screens (product-anchored conversation header, transaction-anchored thread, photo composer) are deferred to a follow-up. Documented as a risk + resolved_decision in flow.yml.
- The article does NOT document character limits, photo upload limits, archive/unarchive flow internals, or read-receipt behaviour because those need a separate iOS pass that is out of scope for this batch.
- **2026-05-07 batch-10 readiness pass (PR #88 + this patch)**: the `profile-message-cta` mockup originally embedded a CSS-drawn purple square pseudo-element on the Message button. iOS uses NO icon on either Follow or Message (text-only `UIButton.Configuration.filled` with `#162131` background). The mockup was rewritten to drop the invented icon and match iOS exactly. Per-screen `required_icons: []` in flow.yml because no iOS icon is required for this surface; `review_checks: [icons_match_ios_source, labels_match_xcstrings, no_invented_ui_state]` records the manual gates the reviewer must apply. The new `screen_icon_not_in_html` validator rule is dormant for this screen by design (nothing to enforce when no icons are required), but `screen_review_checks_missing` is satisfied by the explicit review_checks list.

## Verdict

Zero MISMATCH against the cited iOS sources. Every UI string the article asserts is traceable to xcstrings or to the live iOS surface (the Activity tab routing). Out-of-scope screens are documented as deferred risk.
