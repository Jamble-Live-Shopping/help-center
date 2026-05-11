# Code audit: how-order-cancellations-work (intercom 14288126)

Audience: buyer_br (rerun-2)
Date: 2026-05-08

## Article claim -> iOS / backend source -> verdict

| Claim in article | Source file:line | Verdict |
|---|---|---|
| Buyers see a "Cancel Order" button on order detail when status = Created | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:657-672 | MATCH (button text "Cancel Order", red color, only when `transaction.status == .created`) |
| Tapping Cancel Order opens a confirmation sheet titled "Cancel this order" | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:1068-1071 | MATCH (`BLTNPageItem(title: String(localized: "Cancel this order"))`) |
| Confirmation sheet explains "Upon cancelation, This order will be closed and you will be refunded." | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:1090 | MATCH (verbatim string) |
| Confirmation sheet has buttons "Yes, I cancel" (red) and "No, back" | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:1077-1079 | MATCH (action red `.liveRed`, alternative purple `.customPurple`) |
| Cancel Order is only available before seller confirms (status = Created) | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:657, 1069 | MATCH (button shown only when `.created`; sheet handler guards `status == .created`) |
| Buyer cannot cancel after seller confirms | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:673-705 | MATCH (other status branches show different actions: "Received?", "Issue Solved?", or none) |
| Auto-cancel deadline if seller does not confirm = 3 days | jamble_backend/src/entities/transaction.py:62-63 | MATCH (`case TransactionStatus.confirm_timeout: return 3`) |
| Auto-cancel deadline if seller does not ship = 10 days | jamble_backend/src/entities/transaction.py:64-65 | MATCH (`case TransactionStatus.ship_timeout: return 10`) |
| Refund timing is "5 business days" / "5 dias úteis" | jamble_backend/src/entities/transaction.py:604-605, 614-615, 622-625, 631-632 | MATCH (verbatim "5 business days" / "em até 5 dias úteis") |
| After cancellation the order detail shows status "Canceled" / "Cancelado" | jamble_backend/src/entities/transaction.py:412-418 | MATCH (`refunded`/`confirm_timeout`/`not_confirmed`/`delivery_returned` all map to "Canceled"/"Cancelado") |
| After cancellation the description label says order canceled + refund within 5 business days | jamble_backend/src/entities/transaction.py:622-625 | MATCH (refunded buyer description) |
| Created status description says "We'll notify you upon seller confirmation" | jamble_backend/src/entities/transaction.py:516-520 | MATCH (verbatim) |
| Created status action label = "Awaiting Seller Confirmation" / "Aguardando Confirmação do Vendedor" | jamble_backend/src/entities/transaction.py:438-439 | MATCH |

## xcstrings keys pulled (verbatim values)

| Key | EN | pt-BR |
|---|---|---|
| `Cancel Order` | "Cancel Order" | "Cancelar pedido" |
| `Cancel this order` | "Cancel this order" | "Cancelar este pedido" |
| `Yes, I cancel` | "Yes, I cancel" | "Sim, eu cancelo" |
| `No, back` | "No, back" | "Não, voltar" |
| `Upon cancelation, This order will be closed and you will be refunded.` | "Upon cancelation, This order will be closed and you will be refunded." | "Após o cancelamento, esse pedido será fechado e você será reembolsado." |
| `Ship to` | "Ship to" | "Enviar para" |
| `Order Number` | "Order Number" | "Número do pedido" |

Verified via `RESOURCES/Localizable.xcstrings` (Jamble-iOS).

## iOS files - lines used

- `TRANSACTION/Purchase/View/PurchaseViewController.swift`
  - 657-672: Cancel Order button construction (text-only, no UIImage; red text + border, transparent background; gated to `transaction.status == .created`)
  - 1068-1137: `cancelBuyerOrder` BLTNBoard sheet (title "Cancel this order", description, two text buttons "Yes, I cancel" red and "No, back" purple, dispatches `TransactionStatusInput(status: .refunded)`)

## Backend files - lines used

- `jamble_backend/src/entities/transaction.py`
  - 60-72: `get_pending_status_in_days`: confirm_timeout=3, ship_timeout=10, refunded=5
  - 412-418: `status` getter (refunded -> "Canceled"/"Cancelado")
  - 438-439, 516-520: created-status buyer texts
  - 604-605, 614-615, 622-625, 631-632: refund timing strings ("5 business days" / "em até 5 dias úteis") for not_confirmed, confirm_timeout, refunded, delivery_returned (buyer)

## Icon contract (rule 10e)

All three screens use the **text-only anchor** (Option B): `html_must_not_contain: ["<img", "<svg", "icon-"]`.

Justification: the buyer cancel surface in iOS is text-only.
- The Cancel Order button (`PurchaseViewController.swift:657-672`) is a `QBIndicatorButton` constructed with `text:` only; no `setImage(...)` call.
- The BLTNBoard sheet (`PurchaseViewController.swift:1068-1137`) uses `BLTNPageItem` with title + description + two text buttons; no image asset attached (contrast with other BLTN sheets in the app that set `page.image = UIImage(named: ...)`).
- The status banner (rendered by `transaction.buyerStatusInfos` via `infos.status` text label, `infos.description` text label, plus a step bar) carries no glyph icon at the buyer's status-text position, only the text labels.

Search for icon usage in the file confirmed UIImage assets only appear in unrelated header/seller-info/share rows (`spotlight_help_button`, `valid_username`, `share_link_icon`, `link_purple_icon`, `left_arrow_icon`), none of which sit on the cancel surface.

## Verdict

ALL CLAIMS MATCH. Zero MISMATCH. Article shippable on the code-audit gate.
