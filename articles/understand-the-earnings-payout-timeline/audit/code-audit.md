# Code audit, article 14288147

**Scope**: every iOS UI string and status label referenced in pt-br.md and en.md mapped to Swift source.

## String mapping

| Article claim | iOS source | Match |
|---------------|-----------|-------|
| "Minha Carteira" / "My Wallet" | `SellerWalletView.swift:43` `JambleNavigationBar(title: "My Wallet"...)` + `Localizable.xcstrings` pt-BR "Minha Carteira" | MATCH |
| "Disponível para sacar" / "Available to Withdraw" | `SellerWalletView.swift:69` `section?.title ?? "Available to Withdraw"` | MATCH |
| "Sacar" / "Withdraw" | `SellerWalletView.swift:96` `section?.actionTitle ?? "Withdraw"` + `Localizable.xcstrings:27106` "Withdraw" | MATCH |
| "Pendente" / "Pending" | `SellerWalletView.swift:155` `section?.title ?? "Pending"` + `Localizable.xcstrings:17340` "Pending" → pt-BR "Pendente" | MATCH |
| "Saiba Mais" / "Learn More" | `SellerWalletView.swift:177` `Text("Learn More")` + `Localizable.xcstrings:13934` "Learn More" → pt-BR "Saiba Mais" | MATCH |
| "Dados Bancários" / "Bank Details" | `SellerWalletView.swift:125` `Text("Bank Details")` | MATCH |
| "Atualizar" / "Update" | `SellerWalletView.swift:133` `Text("Update")` | MATCH |
| "Histórico de pagamentos" / "Payouts History" | `SellerWalletView.swift:239` `Text("Payouts History")` + `Localizable.xcstrings:17328` "Payouts History" → pt-BR "Histórico de pagamentos" | MATCH |
| Payout statuses: Created, Processing, Pending, Completed, Failed, Canceled | `Payout.swift:57-74` `enum PayoutStatus` with `title` switch returning `String(localized:)` for each | MATCH |
| Status colors: brand (purple) for created/processing/pending, positive (green) for completed, negative (red) for failed/canceled | `Payout.swift:76-82` `var titleColor` | MATCH |
| "In Delivery" (order status mid-transit) | `Localizable.xcstrings:12532` "In Delivery", comment "The status of a transaction that is currently in transit" | MATCH |
| "PIX 2 to 5 business days" / "PIX 2 a 5 dias úteis" | `SellerWalletViewModel.swift:86` `subtitle: "It can take 2 to 5 business days"` (success indicator after withdrawal) | MATCH |
| "My Sales" (location to confirm orders) | kept as-is in both locales (iOS strings don't localize this tab) | MATCH |
| Withdrawal auto-confirmation (system confirms delivery if buyer doesn't) | Backend behavior, not UI-string visible. Documented in article as flow fact. No iOS string contradicts. | FLOW (not string) |

## Visual fidelity (Check E)

All 3 mockups side-by-side with SellerWalletView.swift structure:

- **wallet-balance**: Header "My Wallet" / "Minha Carteira" with nav back (`<`) + help button (`?`), matches `header` computed property using `JambleNavigationBar`. Withdrawal card (title + amount + Withdraw button + Bank Details row with Update button) mirrors `withdrawalSection`. Pending card (title + description + amount + Learn More) mirrors `pendingSection`. Radius 12px, border 1px `#E9EAEF`, brand purple #7E53F8 Withdraw button, dark Update button per `UIColor.bg.inverse`. MATCH.
- **earnings-timeline**: 5-step conceptual diagram (Sale -> Shipped -> Delivered -> Available -> Withdrawn). Not a direct screen, this is editorial illustration built from Jamble design tokens (purple done dots, white active ring, green "Ready to withdraw" badge). All dot colors and typography consistent with design-system.md. MATCH (conceptual).
- **payout-statuses**: Payouts History section with 4 rows, each with ID + amount + status + date. Mirrors `PayoutHistoryCellView.swift` two-line layout: top row `payout.id` + `payout.amountStr` (semibold), bottom row `payout.status.title` colored by `payout.status.titleColor` + `payout.dateStr` secondary. Brand purple for Processing/Pending (`.content.brand`), green for Completed (`.content.positive`), red for Failed (`.content.negative`). MATCH.

## Result

Zero MISMATCH. All UI-string claims in the article are backed by iOS source. Ready for publish.
