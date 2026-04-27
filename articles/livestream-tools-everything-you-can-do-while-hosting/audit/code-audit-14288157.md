# Code audit, article 14288157 (livestream-tools-everything-you-can-do-while-hosting)

**Source of truth**: `Jamble-iOS` repo at `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble`. pt-BR strings pulled from `Jamble/RESOURCES/Localizable.xcstrings`.

## Article claim, iOS source, verdict

| Article claim (string seen in body) | iOS file | Swift / xcstrings value | Verdict |
|---|---|---|---|
| Tabs: Upcoming / Unsold / Sold | `Jamble/PRODUCT/Models/Product.swift` line 401-410 | `enum ShowSection { upcoming, unsold, sold }` with `displayName` returning `String(localized: "Upcoming")`, `"Unsold"`, `"Sold"`. xcstrings pt-BR: `Próximos`, `Não vendido`, `Vendido` | MATCH |
| Listings title | `Jamble/LIVE_SHOPPING/Host/View/ShowHostProductsViewController.swift` line 50 | `String(localized: "Listings")`, pt-BR `Listagens` | MATCH |
| Search placeholder | same file, line 62 | `String(localized: "Search for a listing")`, pt-BR `Pesquisar uma listagem` | MATCH |
| Pin / Unpin button | `Jamble/LIVE_SHOPPING/Host/View/Cell/ShowHostProductCell.swift` line 463/480 | `String(localized: "Pin")` / `"Unpin"`, pt-BR `Fixar` / `Desafixar` | MATCH |
| Start / Started button | same file, line 554/560/596 | `String(localized: "Start")` / `"Started"`, pt-BR `Iniciar` / `Iniciado` | MATCH |
| Rerun / Free / Paid / Waiting button | same file, line 409/429/432/440/447 | `String(localized: "Rerun" / "Free" / "Paid" / "Waiting")`, pt-BR `Rerun` / `Grátis` / `Pago` / `Aguardando` | MATCH |
| Edit / Delete context menu | same file, line 528/535 | `String(localized: "Edit")` / `"Delete"`, pt-BR `Editar` / `Apagar` | MATCH |
| Real-Time Sales label | `Jamble/LIVE_SHOPPING/Host/View/ShowHostViewController.swift` line 772 | `String(localized: "Real-Time Sales")`, pt-BR `Vendas em tempo real` | MATCH |
| Settings menu, End Show | same file, line 1154/1161/1167 | `String(localized: "End Show")`, pt-BR `Fim do Show` | MATCH |
| Settings menu, Start Battle / End Battle | same file, line 1180/1187 | `String(localized: "Start Battle!")` / `"End Battle"`, pt-BR `Comece a batalha!` / `Fim da batalha` | MATCH |
| Settings menu, How will I get paid? | same file, line 1196 | `String(localized: "How will I get paid?")`, pt-BR `Como serei pago?` | MATCH |
| Settings menu, Audio Settings | same file, line 1211 | `String(localized: "Audio Settings")`, pt-BR `Configurações de áudio` | MATCH |
| Settings menu, Stuck? Unlock! | same file, line 1222 | `String(localized: "Stuck? Unlock!")`, pt-BR `Está preso? Desbloqueie!` | MATCH |
| Settings menu, Any question, Bug or Feedback? | same file, line 1230 | `String(localized: "Any question, Bug or Feedback?")`, pt-BR `Alguma dúvida, bug ou feedback?` | MATCH |
| Settings menu, Help Center | same file, line 1236 | `String(localized: "Help Center")`, pt-BR `Central de ajuda` | MATCH |
| Add-products sheet, New Quickie Listing | same file, line 1689 | `String(localized: "New Quickie Listing")`, pt-BR `Nova listagem rápida` | MATCH |
| Add-products sheet, Clone Past Shows Listings | same file, line 1705 | `String(localized: "Clone Past Shows Listings")`, pt-BR `Clonar listagens de shows anteriores` | MATCH |
| Remote Control prompt, two options | same file, line 582/589/591 | title `String(localized: "Remote Control")`, pt-BR `Controle remoto`. Buttons `Use as a remote` / `Livestream from this device`, pt-BR `Use como um controle remoto` / `Transmissão ao vivo a partir deste dispositivo` | MATCH |
| Live Duo, Remove confirmation | same file, line 1125-1127 | `String(localized: "Remove \(guest.username) From Live Duo?")` (kept literal in body since it's the confirm dialog) | MATCH |
| Late? Revive this Show | same file, line 1579 | `String(localized: "Late? Revive this Show")`, pt-BR `Atrasado? Reviva este Show` | MATCH |
| Sale action button states (Finishing.../Run Again/Next item) | xcstrings | pt-BR `Acabamento...` / `Reiniciar` / `Próximo item` | MATCH |
| Cancel button on action sheets | iOS UIAlertAction style `.cancel` | xcstrings `Cancel` -> pt-BR `Cancelar` | MATCH |

## Mismatches found

None.

## Notes

- "Rerun" has no pt-BR translation in xcstrings (literal `Rerun` is used in the iOS UI for pt-BR locale). The article body uses the same literal, matching what the seller actually sees.
- "Live Duo" is a brand term, kept identical in pt-BR (xcstrings confirms).
- The mockup in `screen-overview` includes a sample product `Charizard Holo PSA 9` at `R$ 250` / `$50` to anchor the BR collectibles use case (72% Pokemon TCG GMV per product mix). The number is illustrative, not pulled from a fixture.
- The iOS host UI uses native `UIAlertController .actionSheet` style for the "+" add-products button and the "..." settings menu. Mockups render the iOS native sheet visual (white cards with hairline separators, system blue text, destructive red for `End Show`, bold `Cancel` card at the bottom) per design-system.md guidance.

## Result

ALL CLAIMS MATCH. Zero MISMATCH. Article ready for ship from a code-fidelity standpoint.
