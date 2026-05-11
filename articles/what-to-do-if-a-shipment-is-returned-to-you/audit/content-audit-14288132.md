# Content audit: what-to-do-if-a-shipment-is-returned-to-you (intercom 14288132)

Audience: seller_br (batch-real-2)
Date: 2026-05-11

## 7-scan content review

| Scan | Result | Notes |
|---|---|---|
| 1. PII | PASS | No emails, phone numbers, real user names. Support email `support@jambleapp.com` is the canonical Jamble support address. |
| 2. Banned words (auction / leilão) | PASS | Zero matches in pt-br.md and en.md. Forbidden_terms list applied. |
| 3. Currency leak (R$ in EN) | PASS | No `R$` anywhere in en.md. Article does not quote prices, so no currency mention is required in pt-br.md either. |
| 4. Word diet | PASS | 7 H2 sections (overview, how to know, why returns happen, what the app shows, what happens to buyer, reship outside app, prevention, FAQ, need help). The pre-existing v1 had a vague Step-1/Step-2/Step-3 / "contact support" flow that did not match the iOS reality (no support escalation needed because the refund is automatic). Replaced by a lifecycle-grounded narrative. |
| 5. Tone | PASS | Direct, "você" / "you" address, no jargon. Frank about what the app does NOT do (no reship button, no manual refund). No CSAT-poison phrasing. |
| 6. Alt-text quality | PASS | All 3 image alts: 50-90 chars, descriptive, mention concrete UI elements ("Cancelado", "aba Devolvido", "ícone vermelho de alerta"), no "Screenshot of" / "Image of". |
| 7. Stale-feature audit | PASS | See structured table below. |

## Stale-feature audit (structured)

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| "Returned" / "Devolvido" filter tab in seller's Sales list | Jamble-iOS/Jamble/TRANSACTION/Models/TransactionFilter.swift:34-44, :64-65, :151-164 | active | 2026-05-11 | Aymar | live_in_ios |
| `transaction_alert_red` red-circle alert icon for the Returned tab | Jamble-iOS/Jamble/RESOURCES/Assets.xcassets/transaction_alert_red.imageset/Vector.svg | active | 2026-05-11 | Aymar | live_in_ios |
| `DELIVERY_RETURNED` status renders "Canceled"/"Cancelado" in order banner | jamble_backend/src/entities/transaction.py:412-418 | active | 2026-05-11 | Aymar | live_in_backend |
| Seller description "Your item could not be delivered and was returned to you" | jamble_backend/src/entities/transaction.py:634-638 | active | 2026-05-11 | Aymar | live_in_backend |
| Buyer description with 5 business days refund timing | jamble_backend/src/entities/transaction.py:629-633 | active | 2026-05-11 | Aymar | live_in_backend |
| Refund is automatic upon `DELIVERY_RETURNED` (no buyer cancel required) | jamble_backend/src/schemas/transaction.py:184 (`delivery_returned: [refund]`) | active | 2026-05-11 | Aymar | live_in_backend |
| Backend transitions confirmed/in_delivery -> pending DELIVERY_RETURNED on Correios RETURNED tracking event | jamble_backend/src/services/shipping_service.py:3080-3100 | active | 2026-05-11 | Aymar | live_in_backend |
| Order Number row visible on sale detail | Jamble-iOS/Jamble/TRANSACTION/Sale/SaleViewController.swift:903-998 + xcstrings "Order Number"/"Número do pedido" | active | 2026-05-11 | Aymar | live_in_ios |

No deprecated features mentioned. No Auction/Leilão wording. No Jamble Prime references. No verified-badge references.

## Anti-patterns avoided (vs v1)

- v1 said "Contact support to arrange a new shipment. A new label may need to be generated" - **removed**. No such in-app flow exists; the order is closed at `DELIVERY_RETURNED`.
- v1 said "Contact support to initiate a cancellation and refund" - **removed**. Refund is automatic per backend schema (`status_change_requirements.delivery_returned: [refund]`).
- v1 described a Step 4 "Contact support" as the default conclusion - **removed**. Replaced by accurate description of the automatic system behavior and a "reship outside app" section that is explicit about the constraint.
- v1 implied the seller might be liable for return shipping ("buyer is generally responsible") - **removed**. The article now states the system handles the financial outcome (refund automatic, seller keeps the item) without inventing liability rules.

## Numbers cited (traceability)

| Number | Source | Verbatim? |
|---|---|---|
| 5 business days (refund timing) | `jamble_backend/src/entities/transaction.py:629-633` | yes ("5 business days" / "em até 5 dias úteis") |

No invented numbers. No marketing-rounded values. No SLAs guessed.

## Verdict

Zero BLOCKER. Article shippable on the content-audit gate.
