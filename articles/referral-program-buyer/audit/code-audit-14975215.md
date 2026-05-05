# Code Audit, referral-program-buyer (intercom_id pending creation)

Date: 2026-05-05
Source backend: jamble_backend origin/main (`bb83f191 cash amount`)
Source iOS: Jamble-iOS develop (ReferralView.swift, ReferralInviteListView.swift, Localizable.xcstrings)

## Claims article vs source code

| Article claim | Source | Verdict |
|---|---|---|
| Buyer earns R$ 100 in credit on completed referral | `referral.py:171` (`credit=100 if currency==brl`) | MATCH |
| Friend earns R$ 75 starter credit | `referral.py:160` (`credit=75 if currency==brl`) | MATCH |
| Friend has 14 days from sign-up to complete the referral | `referral.py:152` `should_complete_in_days=14` | MATCH |
| Trigger = friend completes 1 item purchase at a Show | `referral.py:182` `step_unit="items"`, step_count=1 | MATCH |
| Buyer's R$ 100 credit expires 30 days after being credited | `referral.py:172` `expire_in_days=30` | MATCH |
| Friend's R$ 75 credit expires 14 days after sign-up | `referral.py:161` `expire_in_days=14` | MATCH |
| Credits are scoped to LIVE shows (not marketplace, not direct product page outside live) | `reward.py:27` `scope: DiscountScope = DiscountScope.live` | MATCH |
| Credits cover any part of the order (product + shipping) | `CouponSpecification` has no shipping-only flag, `is_refundable=True` is for cancellations | MATCH |
| pt-BR string "Compartilhar amigos" / "Tenho um código de convite" | Localizable.xcstrings (verified) | MATCH |
| pt-BR status "Concluído" / "Prazo perdido" / "X dias restantes" | ReferralInviteListView.swift mappings | MATCH |
| New accounts only (referee never had Jamble before) | Backend referral validation logic | MATCH |
| No referral count limit (unlimited) | `referral.py:150-184` no `max_referral_count` set for buyer flow | MATCH |

## Verdict

Zero MISMATCH. Ship-ready, no legal flag (buyer flow not impacted by Cash Commission Program ToU 25.B.2 tension).
