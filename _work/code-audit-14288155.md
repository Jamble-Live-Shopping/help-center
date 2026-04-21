# Code Audit: article 14288155 (PIX Payments)

Source files:
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/PROFILE/ProfileSettings/Wallet/View/SellerWalletView.swift`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/PROFILE/ProfileSettings/Wallet/ViewModel/SellerWalletViewModel.swift`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/SERVICE/API/Repository/Modules/Payment/Models/Request/WalletPayload.swift`
- `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings`

## Verified claims (MATCH)

| Claim | iOS Source | Status |
|---|---|---|
| Button label "Sacar" (pt-BR) / "Withdraw" (EN) | xcstrings | MATCH |
| Pending section title "Pendente" (pt-BR) | xcstrings | MATCH |
| Bank details section "Dados Bancários" (pt-BR) | xcstrings | MATCH |
| Update button "Atualizar" (pt-BR) | xcstrings | MATCH |
| My Wallet screen title "Minha carteira" (pt-BR) | xcstrings | MATCH |
| Payouts History "Histórico de pagamentos" (pt-BR) | xcstrings | MATCH |
| Withdrawal fee R$ 3,67 | SellerWalletView.swift:110 | MATCH |
| 1 withdrawal per 24h | SellerWalletView.swift:110 | MATCH |
| Payout takes 2 to 5 business days | SellerWalletViewModel.swift:86 | MATCH (NOT instant as prior version claimed) |
| Action dynamic: withdraw/setup/support | WalletPayload.swift:47-51 | MATCH |

## Corrections applied vs prior version

| Prior claim (WRONG) | Correction (code-faithful) |
|---|---|
| "Saques via PIX são instantâneos, cai em minutos" | "Pode levar de 2 a 5 dias úteis" (iOS success indicator) |
| "Valor mínimo de saque é R$ 100" | Removed, not in iOS code, button enabled flag is server-side |
| No mention of withdrawal fee | Added: "Uma taxa de R$ 3,67 é cobrada por saque" |

## Claims NOT verifiable in iOS (kept cautiously)

- 14% commission rate: shown as dynamic `platform_fee` per transaction, not hardcoded. Kept because it matches Jamble's public take rate policy.
- Auto-confirm delivery after tracking shows delivered: backend behavior, not in iOS.
- Funds move from pending to available upon buyer confirmation: backend, consistent with `PendingSection` + `WithdrawalSection` separation in WalletPayload.

## Mockup assets

- `pix-payments-how-sellers-get-paid__wallet-header__pt-br.png` exists
- `pix-payments-how-sellers-get-paid__wallet-balance__pt-br.png` exists
- `pix-payments-how-sellers-get-paid__wallet-header__en.png` exists
- `pix-payments-how-sellers-get-paid__my-wallet__en.png` exists

Status: zero open MISMATCH.
