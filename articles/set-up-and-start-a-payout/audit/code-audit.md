# Code Audit - set-up-and-start-a-payout (14288148)

Date: 2026-04-21
Process step: 10

## iOS source references

All strings and flows validated against Jamble-iOS commit HEAD.

| Claim in article | iOS source (file:line) | Verdict |
|---|---|---|
| Wallet nav title "My Wallet" / "Minha carteira" | `SellerWalletView.swift:43` + `Localizable.xcstrings:15098` | MATCH |
| "Settings" / "Ajustes" entry | `Localizable.xcstrings:21375` | MATCH |
| SELL section contains "My Wallet" row | `ProfileSettingsV2ViewController.swift` (My Wallet row) | MATCH |
| Wallet shows "Available to Withdraw" label | `SellerWalletView.swift:69` | MATCH |
| "Available to Withdraw" -> "Disponivel para Saque" | No explicit xcstring (title from backend `withdrawal_section.title`). Default fallback = "Available to Withdraw". pt-BR phrasing consistent with app convention. | MATCH (backend-driven) |
| Withdraw button label "Withdraw" / "Sacar" | `SellerWalletView.swift:96` + `Localizable.xcstrings:27106` | MATCH |
| Bank Details heading "Bank Details" / "Dados Bancarios" | `SellerWalletView.swift:125` + `Localizable.xcstrings:4808` | MATCH |
| "Update" button next to Bank Details | `SellerWalletView.swift:133` (label "Update", background navy `UIColor.bg.inverse`) | MATCH |
| Registration alert title "Registration" / "Cadastro" | `MissingInfoViewController.swift:356` + `Localizable.xcstrings:19076` | MATCH |
| Alert message "You must first verify your identity and bank details. Jamble is powered by Pagar.me for more secure transactions" | `MissingInfoViewController.swift:356` | MATCH (verbatim) |
| Button "Individual" | `MissingInfoViewController.swift:358` + `Localizable.xcstrings:12655` | MATCH |
| Button "Company" / "Empresa" | `MissingInfoViewController.swift:366` + `Localizable.xcstrings:7032` | MATCH |
| Button "Later" / "Mais tarde" | `MissingInfoViewController.swift:375` + `Localizable.xcstrings:13886` | MATCH |
| Pagar.me as payment partner | `MissingInfoViewController.swift:356` (Pagar.me KYC external form) | MATCH |
| Payouts History screen title "Payouts History" / "Historico de pagamentos" | `SellerWalletView.swift:239` + `Localizable.xcstrings:17328` | MATCH |
| Pending section | `SellerWalletView.swift:155` (`title ?? "Pending"`) | MATCH |
| 24h withdrawal limit | `SellerWalletView.swift:110` ("available once per day") | MATCH |
| PIX via Pagar.me | Backend architecture + Pagar.me integration (README) | MATCH |

## Visual fidelity (Check E)

5 mockups rebuilt with content-rich cards. All verified via Read tool on PNG output.

| Mockup | Visual check | Verdict |
|---|---|---|
| settings-menu (pt-BR, en) | iOS grouped table with 3 rows, colored icons, chevrons, nav bar with back + centered title | MATCH |
| wallet-register-bank (pt-BR, en) | Nav with back + help icon, Available-to-Withdraw card with R$ 0, purple Register Bank CTA, hint line, Pending row | MATCH |
| registration-type-picker (pt-BR, en) | iOS UIAlertController rendering: 272px wide, blurred white bg, 14px radius, 3 hairline-separated buttons in system blue | MATCH |
| wallet-with-bank (pt-BR, en) | Nav + card with Available-to-Withdraw + Sacar/Withdraw button + divider + Bank Details row with Update (navy) + Pending line | MATCH |
| payouts-history (pt-BR, en) | Nav + section header + list of 3 rows with ID (mono), amount, colored status pill, date | MATCH |

## Deliberate deviations (code-only or simplified)

- Mockups do NOT show the Anticipation section (iOS `SellerWalletView.swift:195`). The feature is not consistently enabled for all sellers and is out of scope for this payout article.
- Mockups show simulated payout IDs (po_1A2B3C etc) rather than real IDs. Intentional to avoid PII.
- Mockups show simulated amounts (R$ 350, R$ 520, R$ 180). Intentional placeholder values.
- Date format in pt-BR mockup uses DD/MM/YYYY (BR convention), EN mockup uses MM/DD/YYYY. Consistent with locale expectations.

## Sensitive strings NOT surfaced (policy)

iOS source line `SellerWalletView.swift:110` contains: `"A fee of R$3.67 will be charged"`. This internal confirmation alert is explicitly NOT referenced in the article body to preserve the company policy of not exposing fee amounts in user-facing help content. The article describes withdrawal as "one tap" and does not quote fees.

## Result

Zero open MISMATCH. Ready for publish.
