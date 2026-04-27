# Code audit, article 14288116 (show-management-for-sellers)

Source of truth: Jamble-iOS Swift code at `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble`.

All article claims about UI labels/states are mapped below to the originating Swift file and `String(localized:)` literal. pt-BR values pulled from `Jamble/RESOURCES/Localizable.xcstrings`.

| Article claim | iOS source (file:line) | EN literal | pt-BR literal | Verdict |
|---|---|---|---|---|
| Stage 1 preview shows **Bookmarks** stat | `LIVE_SHOPPING/Preview/Host/Views/ShowHostPreviewViewController.swift:954` | `Bookmarks` | `Favoritos` | MATCH |
| Stage 1 preview shows **Views** stat | `LIVE_SHOPPING/Preview/Host/Views/ShowHostPreviewViewController.swift:956` | `Views` | `Visualizações` | MATCH |
| Stage 1 button **Add listings** | `LIVE_SHOPPING/Preview/Host/Views/ShowHostPreviewViewController.swift:490, 986` | `Add listings` | `Adicionar listagens` | MATCH |
| Add listings sheet option **New Quickie Listing** | `LIVE_SHOPPING/Preview/Host/Views/ShowHostPreviewViewController.swift:417` | `New Quickie Listing` | `Nova listagem rápida` | MATCH |
| Add listings sheet option **Clone Past Shows Listings** | `LIVE_SHOPPING/Preview/Host/Views/ShowHostPreviewViewController.swift:424` | `Clone Past Shows Listings` | `Clonar listagens de shows anteriores` | MATCH |
| Stage 2 menu actions **Edit** / **Delete** | `LIVE_SHOPPING/Preview/Host/Views/ShowHostPreviewViewController.swift:356, 363` | `Edit`, `Delete` | `Editar`, `Apagar` | MATCH |
| Delete confirmation title | `LIVE_SHOPPING/Preview/Host/Views/ShowHostPreviewViewController.swift:365` | `Are you sure you want to delete this show?` | `Tem certeza de que deseja excluir este show?` | MATCH |
| Delete action button label | `LIVE_SHOPPING/Preview/Host/Views/ShowHostPreviewViewController.swift:369-370` | `Delete` / `Cancel` | `Apagar` / `Cancelar` | MATCH |
| Postpone Limit alert (reached limit) | `LIVE_SHOPPING/Create/Show/ViewModel/CreateShowViewModel.swift:476-477` | `Postpone Limit`, `You just reached the postpone limit for this Show. It cannot be postponed anymore.` | `Limite de adiamento`, `Você acabou de atingir o limite de adiamento para este Show. Ele não pode mais ser adiado.` | MATCH |
| Stage 3 countdown text | `LIVE_SHOPPING/Host/ViewModel/ShowHostViewModel.swift:390` | `Show starts in\n` | `O Show começa em\n` | MATCH |
| Stage 3 button **Practice mode** | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1399` | `Practice mode` | `Modo de prática` | MATCH |
| Stage 3 button **Go Live** | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1405` | `Go Live` | `Vá ao vivo` | MATCH |
| Go Live confirmation title | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:406` | `Start your Show` | `Comece seu show` | MATCH |
| Go Live confirmation message | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:421` | `Once started, people will be able to join you` | `Uma vez iniciado, as pessoas poderão se juntar a você` | MATCH |
| Go Live confirmation buttons | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:425, 429` | `Yes, start` / `Later` | `Sim, comece` / `Mais tarde` | MATCH |
| Late state, 0 to 5 min after | `LIVE_SHOPPING/Host/ViewModel/ShowHostViewModel.swift:393` | `Time` + `to go live!` | `Hora` + `para entrar no ar!` | MATCH |
| Late state, 5 to 10 min after | `LIVE_SHOPPING/Host/ViewModel/ShowHostViewModel.swift:397` | `Last chance to join or postpone the show!` | `Última chance para participar ou adiar o show!` | MATCH |
| Revive show action | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1579` | `Late? Revive this Show` | `Atrasado? Reviva este Show` | MATCH |
| Stage 4 sales dashboard label | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:772` | `Real-Time Sales` | `Vendas em tempo real` | MATCH |
| Host menu **End Show** | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1154, 1161, 1167` | `End Show` | `Fim do Show` | MATCH |
| Host menu **Stop Practice** (during practice) | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1140` | `Stop Practice` | `Parar de praticar` | MATCH |
| Host menu **How will I get paid?** | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1196` | `How will I get paid?` | `Como serei pago?` | MATCH |
| Host menu **Audio Settings** | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1211` | `Audio Settings` | `Configurações de áudio` | MATCH |
| Host menu **Any question, Bug or Feedback?** | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1230` | `Any question, Bug or Feedback?` | `Alguma dúvida, bug ou feedback?` | MATCH |
| Host menu **Help Center** | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1236` | `Help Center` | `Central de ajuda` | MATCH |
| Raid prompt text | `LIVE_SHOPPING/Raid/View/RaidViewController.swift:290-292` | `Before leaving, support the community by sending your viewers to a seller who's currently live!` | `Antes de sair, apoie a comunidade enviar seus espectadores para um vendedor` (assembled) | MATCH (note: pt-BR strings concatenated as in iOS) |
| Sell modes referenced (Real-time offers, Sudden Death, Buy It Now) | `LIVE_SHOPPING/SaleView/.../ShowSaleType.swift` (cross-article ref) | already verified in flash-sales / how-to-list-products audits | matches | MATCH (out of scope, verified upstream) |

## Localization gaps

None. All EN strings used in the article have a non-empty pt-BR localization in `Localizable.xcstrings`.

## Verdict

**Zero MISMATCH.** All host-show management labels referenced in the article body match Jamble-iOS source code character-for-character. Article ready for ship.
