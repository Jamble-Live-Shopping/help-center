# Code audit: what-to-do-if-a-package-is-delayed (intercom 14288128)

Audience: buyer_br (real-2 rewrite)
Date: 2026-05-11

## Article claim -> iOS / backend source -> Verdict

| Claim in article | Source file:line | Verdict |
|---|---|---|
| Buyers open an order from Purchases and see a status card with status text, action text, step bar, and description | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:644-761 | MATCH (status card construction: status label, action label, step bar, status description) |
| Once a tracking record exists, the card adds Carrier, Tracking Number with copy button, and a Track button | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:798-913 | MATCH (carrier row, tracking number row, Track button, Copy button via `copyTrackingNumber` selector) |
| Estimated delivery banner reads "Arriving Today", "Arriving Tomorrow", or "Estimated for {date}" | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:916-930 | MATCH (gated to `.confirmed`, `.inDelivery`, `.delivered`; pulled from `tracking.estimatedDeliveryDate`) |
| Tracking section shows a reverse-chronological list of carrier events (title + description) | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:931-1003 | MATCH (`for (i,event) in tracking.events.reversed()`, sets `event.title` and `event.description`) |
| Status text reads "In Delivery" / "Em Entrega" while the package is in transit | jamble_backend/src/entities/transaction.py:421-422 | MATCH (`Localized(en="In Delivery", pt="Em Entrega")`) |
| The status description for the IN_DELIVERY state is empty by design (no extra paragraph below the step bar) | jamble_backend/src/entities/transaction.py:510-680 | MATCH (no `case TransactionStatus.in_delivery` in the description match block) |
| If the seller misses the shipping deadline, status flips to "Confirmed" with a SHIP_TIMEOUT description telling the buyer they will be refunded automatically | jamble_backend/src/entities/transaction.py:419-420, 639-649 | MATCH (status label stays "Confirmed"/"Confirmado"; description: "The seller didn't ship your order on time. They have {deadline} to send it, or you'll be refunded automatically.") |
| Seller has up to 10 days from confirmation to ship before the SHIP_TIMEOUT state triggers | jamble_backend/src/entities/transaction.py:64-65 | MATCH (`case TransactionStatus.ship_timeout: return 10`) |
| If the package returns to sender, status flips to "Canceled" with a refund-within-5-business-days message | jamble_backend/src/entities/transaction.py:412-418, 629-632 | MATCH (`delivery_returned` maps to "Canceled"/"Cancelado"; description: "Your order could not be delivered and was returned to the seller. You'll receive a refund on your payment method within 5 business days") |
| Automatic refund timing is "within 5 business days" / "em ate 5 dias uteis" | jamble_backend/src/entities/transaction.py:604-605, 614-615, 622-625, 631-632 | MATCH (verbatim string in not_confirmed, confirm_timeout, refunded, delivery_returned buyer descriptions) |
| When a support ticket exists for the order, a "Your Support Ticket" banner with an "Open Ticket" button appears above the order content | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:108-167 | MATCH (gated to `transaction.buyer_intercom_conversation_id != nil`; title "Your Support Ticket", button "Open Ticket" routes to `openIntercomTicket` -> `IntercomHandler().openIntercomTransactionTicket`) |
| The "Received?" button appears on the status card while the order is `inDelivery` (or `confirmed` with `show_id`) | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:673-688 | MATCH (text "Received?", green border, hooked to `confirmDeliveryBuyerOrder`) |
| The seller block on the order is tappable and opens the seller profile (buyer can DM from there) | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:318-385 | MATCH (`sellerView.addGestureRecognizer(...)` -> `showProfile` -> `presentProfile(seller_profile, ...)`) |

## xcstrings keys pulled (verbatim values)

| Key | EN | pt-BR |
|---|---|---|
| `In Delivery` | "In Delivery" | "Em Entrega" |
| `Tracking Number` | "Tracking Number" | "Numero de rastreamento" |
| `Carrier` | "Carrier" | "Transportadora" |
| `Track` | "Track" | "Faixa" (xcstrings pt-BR is "Faixa" but iOS displays in pt-BR context; see risk_flag note) |
| `Arriving Today` | "Arriving Today" | "Chegando hoje" |
| `Arriving Tomorrow` | "Arriving Tomorrow" | "Chegando amanha" |
| `Estimated for %@` | "Estimated for %@" | "Estimado para %@" |
| `Ship to` | "Ship to" | "Enviar para" |
| `Order Number` | "Order Number" | "Numero do pedido" |
| `Your Support Ticket` | "Your Support Ticket" | (xcstrings pt-BR unverified; banner only shown when buyer already has a ticket) |
| `Open Ticket` | "Open Ticket" | (xcstrings pt-BR unverified; banner only shown when buyer already has a ticket) |

Verbatim from `RESOURCES/Localizable.xcstrings` (Jamble-iOS).

Note on `Track`: the xcstrings pt-BR value is "Faixa" (literal "Stripe / Band"), which appears to be a mistranslation in the iOS catalog. Buyer-facing usage on the order detail Tracking row is for opening the carrier tracking webpage. Article body and mockups use neutral wording ("acompanhar / track") in surrounding prose and reference the button label verbatim. Flagging as risk for translators (`risk_flags`).

## Refund timing grounded

Per real-1 rule 6 (Refund timing grounded): the article quotes "5 business days" / "5 dias uteis" only because the backend renders that exact string in buyer descriptions for the four refunded/canceled buyer states. Sources:

- `jamble_backend/src/entities/transaction.py:604-605` (not_confirmed buyer)
- `jamble_backend/src/entities/transaction.py:614-615` (confirm_timeout buyer)
- `jamble_backend/src/entities/transaction.py:622-625` (refunded buyer)
- `jamble_backend/src/entities/transaction.py:631-632` (delivery_returned buyer)

The 10-day shipping deadline is quoted only because it is the literal value returned by `get_pending_status_in_days(ship_timeout)`:
- `jamble_backend/src/entities/transaction.py:64-65`

No other SLAs are invented.

## iOS files - lines used

- `TRANSACTION/Purchase/View/PurchaseViewController.swift`
  - 108-167: Support ticket banner ("Your Support Ticket" + "Open Ticket" button), gated to `transaction.buyer_intercom_conversation_id`
  - 318-385: `setupSellerView` - tappable seller row that opens the seller profile (buyer can DM from there)
  - 639-1010: `setupTransactionStatusView` - status card (status label, action label, step bar, status description, Ship to address, optional Tracking section with Carrier/Tracking Number/Track button and a reverse-chronological list of carrier events)
  - 673-688: "Received?" button shown on the status card during `.inDelivery` (or `.confirmed` + `show_id`)
  - 916-930: Estimated-delivery banner ("Arriving Today" / "Arriving Tomorrow" / "Estimated for {date}") rendered above the carrier-event list

## Backend files - lines used

- `jamble_backend/src/entities/transaction.py`
  - 27-41: `TransactionStatus` enum (incl. `in_delivery`, `ship_timeout`, `delivery_returned`, `refunded`)
  - 60-72: `get_pending_status_in_days` (ship_timeout = 10, refunded = 5)
  - 412-422: `status` getter ("In Delivery"/"Em Entrega", SHIP_TIMEOUT collapsed back to "Confirmed"/"Confirmado")
  - 510-680: `description` getter (no `in_delivery` case = empty by design; `ship_timeout` buyer line; `delivery_returned` buyer line with "within 5 business days" / "em ate 5 dias uteis")

## negative_scan

No paths were declared in `source_of_truth.negative_scan`. The article does not claim that any non-existent screen exists. The article does not mention any feature we know to be deprecated (no badges Rising/Elite/Ultra; no auction/leilao wording; no Jamble Prime).

## Icon contract (rule 10e)

Two screens use the **text-only anchor** (Option B): `html_must_not_contain: ["<img", "<svg", "icon-"]`.

Justification: both mockups render parts of the status card surface, which is text + step-bar + carrier-event list. The actual iOS implementation uses small grey circle dots for the carrier-event timeline (background-colored UIView, no UIImage asset) and a `share_link_icon` for the copy-tracking-number button. The copy button is purely chrome and not load-bearing for the article's claims, so the mockup omits it; the timeline dots are reproduced as CSS background-colored circles (matching the iOS implementation which is also CSS-equivalent - background color on a sized view, no image asset).

No real iOS image asset is on the surfaces depicted (status text, step bar, event list, "In Delivery" status label, "Track" button text).

## Verdict

ALL CLAIMS MATCH. Zero MISMATCH. Article shippable on the code-audit gate.
