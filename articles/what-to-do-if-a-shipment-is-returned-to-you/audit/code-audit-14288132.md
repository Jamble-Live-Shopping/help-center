# Code audit: what-to-do-if-a-shipment-is-returned-to-you (intercom 14288132)

Audience: seller_br (batch-real-2)
Date: 2026-05-11

## Article claim -> iOS / backend source -> verdict

| Claim in article | Source file:line | Verdict |
|---|---|---|
| The seller has a "Returned" / "Devolvido" filter tab in the Sales list | Jamble-iOS/Jamble/TRANSACTION/Models/TransactionFilter.swift:34-44 (sale ordered cases include `.returned`), :64-65 (`String(localized: "Returned")`) | MATCH |
| The "Returned" filter tab uses a red alert icon (red circle with `!`) | Jamble-iOS/Jamble/TRANSACTION/Models/TransactionFilter.swift:160 (`return "transaction_alert_red"`), :142-148 (`.alwaysOriginal`, `tintColor: .clear`) | MATCH (asset Vector.svg in `Assets.xcassets/transaction_alert_red.imageset/`) |
| The Sales-list filter tabs include "Returned" alongside "Completed" and "Canceled" for sellers | Jamble-iOS/Jamble/TRANSACTION/Models/TransactionFilter.swift:34-44 | MATCH (case .sale: [.all, .toBeShipped, .shipped, .toBeConfirmed, .completed, .investigation, .returned, .cancelled]) |
| When the parcel reaches the seller back, the transaction status becomes DELIVERY_RETURNED | jamble_backend/src/services/shipping_service.py:3080-3100 (sets pending_status=delivery_returned when label not is_return + tracking RETURNED) | MATCH (lifecycle confirmed: confirmed/in_delivery -> pending delivery_returned, then DELIVERY_RETURNED on receipt) |
| The status label shown in the order detail is "Canceled" / "Cancelado" for DELIVERY_RETURNED | jamble_backend/src/entities/transaction.py:412-418 (case `delivery_returned -> Localized(en="Canceled", pt="Cancelado")`) | MATCH |
| The seller's description on the order detail says the item could not be delivered and was returned | jamble_backend/src/entities/transaction.py:634-638 (`case (TransactionStatus.delivery_returned, False)` -> "Your item could not be delivered and was returned to you" / "Seu item não pôde ser entregue e foi devolvido a você") | MATCH (verbatim) |
| The step bar shows the order at the last (maximum) step in red | jamble_backend/src/entities/transaction.py:698-706 (case `delivery_returned -> self.max_step`), :750-756 (case `delivery_returned -> FEColorEnum.order_red.hex`) | MATCH |
| The buyer's description says the order will be refunded within 5 business days | jamble_backend/src/entities/transaction.py:629-633 (`case (TransactionStatus.delivery_returned, True)` -> "Your order could not be delivered and was returned to the seller. You'll receive a refund on your payment method within 5 business days" / "Seu pedido não pôde ser entregue e foi devolvido ao vendedor. Você receberá um reembolso no método de pagamento em até 5 dias úteis") | MATCH (verbatim, traceable to backend) |
| Refund is automatic on DELIVERY_RETURNED (no buyer action required) | jamble_backend/src/schemas/transaction.py:184 (`delivery_returned: [TransactionStatusRequirements.refund]`) | MATCH (refund is a status requirement, not a buyer-triggered action) |
| Seller has no "Cancel Sale" button at DELIVERY_RETURNED | Jamble-iOS/Jamble/TRANSACTION/Sale/SaleViewController.swift:921-923 (button only when `transaction.seller_transfer_id == nil && (status == .confirmed || ((status == .inDelivery || .delivered || .investigation) && sale_count >= 50))`) | MATCH (status `.deliveryReturned` not in the gating set) |
| The order-detail screen shows the Order Number row beneath the status banner | Jamble-iOS/Jamble/TRANSACTION/Sale/SaleViewController.swift:903-998 (setupTransactionStatusView), reference real-1 article order-canceled-refund-status mockup | MATCH (label uses xcstring "Order Number" / "Número do pedido") |
| The tracking section (Carrier + Tracking number + Track button) is rendered when a Tracking exists | Jamble-iOS/Jamble/TRANSACTION/Sale/SaleViewController.swift:1076-1170 (`if let tracking = tracking`, builds carrier row, tracking-number row, Track button) | MATCH |
| There is no in-app self-service "reship after return" flow | Jamble-iOS grep: 0 hits for `Reship`/`Repackage`/`Reenviar` outside the dashboard "Resend Shipping Labels" action which is for pre-shipment label regeneration (jamble_backend/src/schemas/sale_actions.py:414-418) | MATCH (negative finding documented) |
| There is no separate Devolvido status label distinct from Cancelado on the order banner | jamble_backend/src/entities/transaction.py:412-418 (delivery_returned collapses into "Canceled"/"Cancelado") | MATCH (the "Devolvido" xcstring at Localizable.xcstrings:19629-19643 is used ONLY in the filter tab, not the status banner) |

## xcstrings keys pulled (verbatim values)

| Key | EN | pt-BR | xcstrings line |
|---|---|---|---|
| `Returned` | "Returned" | "Devolvido" | 19629-19643 |
| `Canceled` | "Canceled" | "Cancelado" | 6123-6138 |
| `Completed` | "Completed" | "Concluído" | confirmed via lookup |
| `All` | "All" | "Todos" | confirmed via lookup |
| `In Delivery` | "In Delivery" | "Em Entrega" | confirmed via lookup |
| `Order Number` | "Order Number" | "Número do pedido" | confirmed via lookup |
| `Carrier` | "Carrier" | "Transportadora" | confirmed via lookup |
| `Track` | "Track" | "Faixa" | confirmed via lookup (Note: pt-BR value is a translation defect in xcstrings; we use it verbatim per rule 5. Article body does not surface this string outside the mockup.) |
| `Ship to` | "Ship to" | "Enviar para" | confirmed via lookup |

Backend-rendered labels (NOT xcstrings - server-side `Localized(en=..., pt=...)`):

| String | EN | pt-BR | backend line |
|---|---|---|---|
| Status when delivery_returned | "Canceled" | "Cancelado" | transaction.py:412-418 |
| Seller description when delivery_returned | "Your item could not be delivered and was returned to you" | "Seu item não pôde ser entregue e foi devolvido a você" | transaction.py:634-638 |
| Buyer description when delivery_returned | "Your order could not be delivered and was returned to the seller. You'll receive a refund on your payment method within 5 business days" | "Seu pedido não pôde ser entregue e foi devolvido ao vendedor. Você receberá um reembolso no método de pagamento em até 5 dias úteis" | transaction.py:629-633 |

## iOS files - lines used

- `TRANSACTION/Models/Transaction.swift`
  - 37-58: `TransactionStatus` enum (raw `DELIVERY_RETURNED`)
- `TRANSACTION/Models/TransactionFilter.swift`
  - 10-19: `TransactionFilter` enum cases (`returned`, `cancelled`, etc.)
  - 34-44: Sale-side filter order
  - 48-73: `title(for:)` mapping `.returned` -> "Returned", `.cancelled` -> "Canceled"
  - 142-148: Filter icon state (rendering mode `.alwaysOriginal`, no tint for `.returned`)
  - 151-164: `iconAssetName` mapping `.returned` -> `"transaction_alert_red"`
- `TRANSACTION/Sale/SaleViewController.swift`
  - 903-998: `setupTransactionStatusView` (status label, action label, step bar, description label rendering `sellerStatusInfos`)
  - 921-939: Cancel Sale button gating (NOT shown for `.deliveryReturned`)
  - 1076-1170: Tracking section (carrier, tracking number, Track button)
- `RESOURCES/Assets.xcassets/transaction_alert_red.imageset/Vector.svg`
  - Real iOS asset embedded inline in mockup #2 (red circle, "!" inside, fill #FD6642)

## Backend files - lines used

- `jamble_backend/src/entities/transaction.py`
  - 30-41: `TransactionStatus` enum (`delivery_returned`, `delivery_return_started`)
  - 60-72: `get_pending_status_in_days` (delivery_returned = 7 days)
  - 402-432: `status` (computed): delivery_returned -> "Canceled"/"Cancelado"
  - 601-680: `description` (computed): seller and buyer texts for delivery_returned
  - 682-706: `step` (delivery_returned -> max_step, terminal)
  - 708-756: `status_color` / `step_color` (delivery_returned -> order_red)
- `jamble_backend/src/services/shipping_service.py`
  - 3080-3100: Tracking event RETURNED with non-return label transitions transaction.pending_status to delivery_returned

## Icon contract (rule 10e)

Three screens declare review_checks per rule 10c:

- **Screen 1 (sale-detail-returned-status)** - text-only anchor (Option B): `html_must_not_contain: ["<img", "<svg", "icon-"]`. Justification: the seller status banner at `SaleViewController.swift:903-998` is plain UILabels (status, action, description) plus `AWStepBar` (drawn as CSS bars), no icon attached. Mockup mirrors the banner only; tracking row showing the icon-bearing `share_link_icon` is intentionally omitted to keep the surface scoped.
- **Screen 2 (sales-list-returned-tab)** - icon anchor (Option A): `required_icons: [transaction_alert_red]`, asset embedded inline as `<svg>`. Justification: the filter tab at `TransactionFilter.swift:160` declares `transaction_alert_red` with rendering mode `.alwaysOriginal` (line 145), which means the original color is preserved. Asset is the only icon on the surface; other tabs in the same strip use neutral text pills per the screenshot real-1 article style.
- **Screen 3 (buyer-refund-status-after-return)** - text-only anchor (Option B): same justification as Screen 1. Buyer banner uses `buyerStatusInfos`, same `setupTransactionStatusView` pattern, no icon attached to the banner itself.

## Verdict

ALL CLAIMS MATCH. Zero MISMATCH. Article shippable on the code-audit gate.
