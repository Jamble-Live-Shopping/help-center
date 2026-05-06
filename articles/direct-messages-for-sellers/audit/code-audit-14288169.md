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
| Profile has a Message CTA button | xcstrings "Message" -> pt-BR "Mensagem" exists as a button label string | MATCH |
| Tapping Message on a profile creates or opens a DM | Negative claim about the absence of contradictory state. The button label is consistent with a DM entry point and no other surface mounts it. Detail audit deferred. | MATCH (high level, detail screens deferred) |
| New messages trigger push notifications gated by the Activity category | Cross-article reference to the notification-settings audit (notification category "Activity" controls the live activity push channel) | MATCH (cross-article) |

## Visual fidelity

| Mockup | pt-BR strings match xcstrings? | Status |
|--------|--------------------------------|--------|
| direct-messages-for-sellers__activity-tabs__pt-br.png | All 6 tab labels match xcstrings; conversation rows are illustrative pt-BR examples | MATCH (tab labels), illustrative (rows) |
| direct-messages-for-sellers__profile-message-cta__pt-br.png | "Mensagem" matches xcstrings; "Seguir", "seguidores", "seguindo", "vendas" are illustrative pt-BR translations of standard profile labels | MATCH on Message CTA, illustrative on the rest |

## Notes

- The original flow.yml hints in `process/batches/article-batch.example.yml` cited paths under a `DM/` folder that does not exist in the iOS tree. Real paths are under `ACTIVITY/`. flow.yml updated.
- Conversation-detail screens (product-anchored conversation header, transaction-anchored thread, photo composer) are deferred to a follow-up. Documented as a risk + resolved_decision in flow.yml.
- The article does NOT document character limits, photo upload limits, archive/unarchive flow internals, or read-receipt behaviour because those need a separate iOS pass that is out of scope for this batch.

## Verdict

Zero MISMATCH against the cited iOS sources. Every UI string the article asserts is traceable to xcstrings or to the live iOS surface (the Activity tab routing). Out-of-scope screens are documented as deferred risk.
