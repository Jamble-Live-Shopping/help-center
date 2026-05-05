# Code Audit, referral-program (seller, intercom 14288089)

Date: 2026-05-05
Source backend: jamble_backend origin/main (`bb83f191 cash amount`)
Source iOS: Jamble-iOS develop (ReferralView.swift, ReferralInviteListView.swift, Localizable.xcstrings)

## Claims article vs source code

| Article claim | Source | Verdict |
|---|---|---|
| Active seller, complete registration required | `ProfileSettingsV2ViewController.swift` shows SELLER_REFERRAL only if `profile.isLiver == True` | MATCH |
| Referrer earns R$ 500 cash on completed referral | `referral.py:209` (R$ 500 for seller flow) + `referral.py:251-272` swap to `cash_specification` when `is_liver==True` | MATCH |
| Referee earns R$ 75 starter bonus | `referral.py:198` (`credit=75 if currency==brl`) | MATCH |
| Referred seller has 30 days to make first sale | `referral.py:189` `should_complete_in_days=30` | MATCH |
| Trigger = first sale (1 buyer) | `referral.py:219` `step_unit="buyers"`, step_count=1 | MATCH |
| Up to 200 referrals limit | `referral.py:190` `max_referral_count=200` | MATCH |
| Payment via international financial institution within 14 business days | ToU 25.B.2.d, PR #593 description | MATCH |
| IOF 0.38% withheld at settlement | ToU 25.B.2.e | MATCH |
| Bank account must match same CPF/CNPJ | ToU 25.B.2.d | MATCH |
| pt-BR string "Compartilhar amigos" | Localizable.xcstrings (verified by Explore agent audit) | MATCH |
| pt-BR string "Tenho um código de convite" | Localizable.xcstrings (verified) | MATCH |
| pt-BR string "Referências contínuas" / "Referências anteriores" | ReferralView.swift:220, 262 + xcstrings | MATCH |
| pt-BR status "Concluído" / "Prazo perdido" | ReferralInviteListView.swift mappings | MATCH |
| pt-BR status "X dias restantes" | GetReferralsResponse.swift:51-55 deadline_remaining_days | MATCH |
| Article describes new seller account requirement | Backend `referral_type=seller` is gated by referee creation flow + `referrer.is_liver==True` | MATCH |

## Risk flag (non-blocking for draft)

**ToU 25.B.2.d caps gross commission at "up to R$ 100"**, but backend code sets R$ 500 in `referral.py:209`. Article documents code value (R$ 500) per Aymar's plan-mode decision. Pending Yamila reconciliation before merging `state: published`. Until reconciled, ship PR as draft.

## Verdict

Zero MISMATCH. Ship-ready pending Yamila signoff on R$ 500 vs ToU R$ 100.
