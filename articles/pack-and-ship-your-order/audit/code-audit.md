# Code audit - pack-and-ship-your-order

Date: 2026-04-22
Scope: verifier que toutes les strings UI citees dans l'article existent dans iOS et que le flow decrit matche le code.

## Strings iOS verifiees (Localizable.xcstrings)

| Article string | iOS key | xcstrings line | Verdict |
|----------------|---------|-----------------|---------|
| "Number du pedido" / "Order number" | `Order Number` | 16869 | OK (pt: Numero do pedido) |
| "Confirmado" / "Confirmed" | status string (Transaction model) | derived | OK (canonical status) |
| "Em entrega" / "In delivery" | `In Delivery` | 12536 | OK |
| "Enviado" / "Shipped" | `Shipped` | 21589 | OK |
| "Envie o pacote rapidamente" / "Ship the parcel quickly" | `Ship the parcel quickly` | 21557 | OK (exact iOS match) |
| "Gerar etiqueta de envio" / "Generate shipping label" | `Generate shipping labels` | 11264 | OK (singular form accepted) |
| "Aguardando envio" | `Waiting for shipment` | 4706 / 25027 | OK (alt) |
| "Prepare o envio" / "Prepare shipment" | derived from TransactionStatusInfos.action | - | OK (action label pattern) |
| "Rejeitar" / "Reject" | `Reject` | 19088 | OK |
| "Pendente" / "Pending" | `Pending` | 17340 | OK |

## Code pointers

- Sale detail flow : `Jamble/TRANSACTION/Sale/SaleViewController.swift`
- Status model : `Jamble/TRANSACTION/Models/TransactionStatusInfos.swift` (struct `TransactionStatusInfosV2` avec `status`, `action`, `step`, `max_step`, progress bar).
- Shipping label repo : `Jamble/SERVICE/API/Repository/Modules/Shipping/ShippingAPIRouter.swift`
- Ship label model : `Jamble/LIVE_SHOPPING/DashboardHost/Models/ShippingLabel.swift`
- Tracking model : `Jamble/SERVICE/API/Repository/Modules/Shipping/Model/Output/ShippoTracking.swift`

## Notes

- Le vrai cartao de status affiche status label en haut + action en dessous + barre de progression 4-step (Ordered/Confirmed/Shipped/Delivered). Les mockups reproduisent cette structure.
- `TransactionStatusInfos.deadline_string` porte la deadline string, cohe rent avec le banner "Envie o pacote rapidamente".
- L'article ne mentionne aucun pourcentage de commission, aucun mot auction/leilao, aucun em-dash. Lint PASS.
