# Code audit: cancel-an-order-as-a-seller (14288152)

Every UI string in the article is traced back to iOS source. Zero MISMATCH.

## Strings verified in iOS

| Article label | iOS source | File | Line |
|---|---|---|---|
| My Sales | `String(localized: "My Sales")` | `PROFILE/ProfileSettings/ProfileSettingsV2ViewController.swift` | 45 |
| My Wallet | `String(localized: "My Wallet")` | same | 46 |
| Shipping Preferences | `String(localized: "Shipping Preferences")` | same | 47 |
| Vacation mode | `String(localized: "Vacation mode")` | same | 48 |
| Reject | `firstButton.setTitle("Reject")` | `TRANSACTION/Sale/SaleViewController.swift` | 361 |
| Confirm | `secondButton.setTitle("Confirm")` | same | 376 |
| Cancel Sale (red button on status card) | `QBIndicatorButton(... text: String(localized: "Cancel Sale"), textColor: UIColor.liveRed ...)` | same | 925 |
| Order Number | `String(localized: "Order Number")` | same | 43 |
| What's making you cancel? | `JambleNavigationBar(title: "What's making you cancel?", isModal: true)` | `TRANSACTION/Sale/CancelSaleReasonView.swift` | 18 |
| Our team will review your request within 2 hours. | `Text("Our team will review your request whitin 2 hours.")` (iOS typo "whitin"; article corrects to "within") | same | 19 |
| Unable to ship the item | `case unableToShip = "Unable to ship the item"` | same | 99 |
| Item lost | `case itemLost = "Item lost"` | same | 100 |
| Item damaged | `case itemDamaged = "Item damaged"` | same | 101 |
| Buyer requested cancellation | `case buyerRequested = "Buyer requested cancellation"` | same | 102 |
| Other reasons | `case otherReasons = "Other reasons"` | same | 103 |
| Submit | `Text("Submit")` | same | 78 |
| Cancel this sale | `.alert("Cancel this sale", isPresented: self.$showConfirmationAlert)` | same | 29 |
| Don't Cancel | `Button("Don't Cancel", role: .cancel)` | same | 30 |
| Cancel Sale (destructive alert button) | `Button(role: .destructive) { ... } label: { Text("Cancel Sale") }` | same | 33-38 |
| Abusive or repeated cancellations may lead to temporary restrictions or account suspension. | `Text("Abusive or repeated cancellations may lead to temporary restrictions or account suspension.")` | same | 42 |
| Cancel Order (buyer-side) | `QBIndicatorButton(... text: String(localized: "Cancel Order"), textColor: UIColor.liveRed ...)` | `TRANSACTION/Purchase/View/PurchaseViewController.swift` | 658 |
| Cancel this order | `let page = BLTNPageItem(title: String(localized: "Cancel this order"))` | same | 1071 |
| Yes, I cancel | `page.actionButtonTitle = String(localized: "Yes, I cancel")` | same | 1077 |
| No, back | `page.alternativeButtonTitle = String(localized: "No, back")` | same | 1078 |

## pt-BR translations verified in Localizable.xcstrings

| EN key | pt-BR value |
|---|---|
| Cancel Sale | Cancelar venda |
| Cancel Order | Cancelar pedido |
| Cancel this sale | Cancelar esta venda |
| Cancel this order | Cancelar este pedido |
| Don't Cancel | Não cancele |
| Reject | Rejeitar |
| Submit | Enviar |
| What's making you cancel? | O que te levou a cancelar? |
| Unable to ship the item | Não foi possível enviar o item |
| Item lost | Item perdido |
| Item damaged | Item danificado |
| Buyer requested cancellation | O comprador solicitou o cancelamento |
| Other reasons | Outras razões |
| Yes, I cancel | Sim, eu cancelo |
| No, back | Não, voltar |
| Abusive or repeated cancellations ... | Cancelamentos abusivos ou repetidos podem levar a restrições temporárias ou à suspensão da conta. |

## Behavioral claims traced to code

| Claim | Source |
|---|---|
| Cancel Sale visible on status card for confirmed/inDelivery/delivered status | `SaleViewController.swift:921-939`, condition `transaction.status == .confirmed || ((transaction.status == .inDelivery || transaction.status == .delivered || transaction.status == .investigation) && seller_profile.sale_count >= 50)` |
| Post-confirmation cancel on inDelivery/delivered requires 50 completed sales | same condition |
| Reject + Confirm buttons shown only on `.created` status | `SaleViewController.swift:349-378` |
| Buyer Cancel Order button visible only while status = created | `PurchaseViewController.swift:657` |
| Refund triggers status update to `.refunded` | `PurchaseViewController.swift:1106` |
| Cancellation reasons tracked as event `product_cancel` with reason rawValue | `CancelSaleReasonView.swift:88-94` |

## Visual fidelity (Check E)

4 mockups, 2 locales. Every PNG visually inspected after render.

- `settings-seller-menu`: matches Settings screen > SELL section. iOS uses colored square icons (yellow for sales, gray for wallet, blue for shipping, purple for vacation). MATCH within mockup abstraction.
- `sale-detail-cancel-button`: composite screen showing order header (Order Number + copy button), product row (image + name + price in R$), status card (green label + action + progress bar + Cancel Sale button in red with liveRed `#F04437` border). MATCH code-only for layout assembly.
- `cancellation-reason-picker`: matches `CancelSaleReasonView.swift`. 5 radio options in SwiftUI list, Submit button at bottom. MATCH.
- `cancel-sale-confirmation`: matches native iOS `.alert` modifier. 2 buttons (destructive red + cancel blue). Title `Cancel this sale` + detail message. MATCH.

## Open mismatches

None.
