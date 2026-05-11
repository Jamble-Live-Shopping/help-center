# Content audit: how-order-cancellations-work (intercom 14288126)

Audience: buyer_br (rerun-2)
Date: 2026-05-08

## 7-scan content review

| Scan | Result | Notes |
|---|---|---|
| 1. PII | PASS | No emails, phone numbers, real user names. Support email `support@jambleapp.com` is the canonical Jamble support address. |
| 2. Banned words (auction / leilão) | PASS | Zero matches in pt-br.md and en.md. |
| 3. Currency leak (R$ in EN) | PASS | No `R$` in en.md. Article does not quote prices, so no currency mention required. |
| 4. Word diet | PASS | Article condensed from prior seller-focused rerun-1; redundant tips section removed. Section count = 6 (overview, when buyer can cancel, how to cancel, after cancel, automatic cancellations, FAQ). |
| 5. Tone | PASS | Direct, "you" address, no jargon, no CSAT-poison phrases. Refund timing stated factually. |
| 6. Alt-text quality | PASS | All 3 image alts: 50-110 chars, descriptive, mention concrete UI elements, no "Screenshot of" / "Image of". |
| 7. Stale-feature audit | PASS | See structured table below. |

## Stale-feature audit (structured)

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Cancel Order button on order detail (status=Created) | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:657-672 | active | 2026-05-08 | Aymar | live_in_ios |
| BLTNBoard cancel-confirmation sheet (Cancel this order) | Jamble-iOS/Jamble/TRANSACTION/Purchase/View/PurchaseViewController.swift:1068-1137 | active | 2026-05-08 | Aymar | live_in_ios |
| Canceled status banner with refund-timing description | jamble_backend/src/entities/transaction.py:418, 622-625 | active | 2026-05-08 | Aymar | live_in_backend |
| Auto-cancel deadline if seller does not confirm = 3 days | jamble_backend/src/entities/transaction.py:62-63 | active | 2026-05-08 | Aymar | live_in_backend |
| Auto-cancel deadline if seller does not ship = 10 days | jamble_backend/src/entities/transaction.py:64-65 | active | 2026-05-08 | Aymar | live_in_backend |
| Refund timing 5 business days | jamble_backend/src/entities/transaction.py:604, 614, 624, 632 | active | 2026-05-08 | Aymar | live_in_backend |

No deprecated features mentioned. No Auction/Leilão wording. No Jamble Prime references. No verified-badge references.

## Audience pivot rationale (buyer_br)

The rerun-1 article wrote this as a seller-focused doc (how a seller cancels). That misaligned with the assigned audience and with the published Intercom title, which is buyer-facing. Rerun-2 rewrites for `buyer_br`:
- removes the seller cancel-reason picker flow (5-radio screen) - that surface only exists for sellers and is out of scope
- adds the buyer Cancel Order button, the BLTN confirm sheet, and the post-cancel refund-status card
- drops the "2-hour Jamble review" wording (that is a seller-side moderation step, not visible to buyers)

## Numbers cited (traceability)

| Number | Source | Verbatim? |
|---|---|---|
| 3 days (auto-cancel if seller does not confirm) | `jamble_backend/src/entities/transaction.py:62-63` | yes (`return 3`) |
| 10 days (auto-cancel if seller does not ship) | `jamble_backend/src/entities/transaction.py:64-65` | yes (`return 10`) |
| 5 business days (refund timing) | `jamble_backend/src/entities/transaction.py:604, 614, 624, 632` | yes ("5 business days" / "5 dias úteis") |

No invented numbers. No marketing-rounded values.

## Verdict

Zero BLOCKER. Article shippable on the content-audit gate.
