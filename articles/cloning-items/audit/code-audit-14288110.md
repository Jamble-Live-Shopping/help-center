# Code Audit, Intercom 14288110 (cloning-items)

**Source of truth**: Jamble-iOS repo at `/Users/aymardumoulin/Projects/Jamble-iOS`
**Audit date**: 2026-04-27
**Verdict**: PASS, zero open MISMATCH. 3 NOT-LOCALIZED-IN-XCSTRINGS flags noted (existing iOS i18n debt, not introduced by this article).

## Article claims vs Swift source

| # | Article claim | iOS Swift file (line) | EN literal in app | pt-BR literal in app | Verdict |
|---|---|---|---|---|---|
| 1 | Action sheet from preview shows "New Quickie Listing", "Clone Past Shows Listings", "Cancel" | `LIVE_SHOPPING/Preview/Host/Views/ShowHostPreviewViewController.swift:417` and `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:1689` | "New Quickie Listing", "Clone Past Shows Listings", "Cancel" | "Nova listagem rápida", "Clonar listagens de shows anteriores", "Cancelar" (xcstrings) | MATCH |
| 2 | Clone-from-Shows screen header reads "Clone Listings from Shows" | `LIVE_SHOPPING/Create/Product/View/ShowHostImportView.swift:38` | "Clone Listings from Shows" | "Clonar listagens de shows" (xcstrings) | MATCH (article uses pt-BR per locale) |
| 3 | Show-list cell shows "X unsolds, Y solds" | `LIVE_SHOPPING/Create/Product/View/Cells/ShowImportProductCell.swift:42` | `"%lld unsolds, %lld solds"` | xcstrings entry exists but pt-BR value identical to EN ("%lld unsolds, %lld solds") | MATCH (faithful to app: pt-BR mockup ships English literal because that's what users see). FLAG-NOT-LOCALIZED. |
| 4 | Selection screen header "Select Listings" | `ShowHostImportSelectionView.swift:28` | "Select Listings" | "Selecionar listagens" (xcstrings) | MATCH |
| 5 | Show details show "X unsolds, Y solds" | `ShowHostImportSelectionView.swift:64` | "%lld unsolds, %lld solds" | identical EN/pt-BR (NOT TRANSLATED in xcstrings) | MATCH faithful. FLAG-NOT-LOCALIZED. |
| 6 | Product cell title prefixed with "(Added) " when already cloned | `ShowImportSelectionProductCell.swift:27` | inline string `"(Added) " + product.title` | not in xcstrings, hardcoded inline | MATCH (article keeps "(Added)" verbatim in both locales, faithful). FLAG-HARDCODED. |
| 7 | Product cell shows "X Available" | `ShowImportSelectionProductCell.swift:33` | "%lld Available" | "%lld Disponível" (xcstrings) | MATCH |
| 8 | Product cell price prefixes "Starts at" for AUCTION/SUDDEN_DEATH, raw price for BUY_IT_NOW, "Sold for" if sold, "Free" for giveaway (but giveaways are filtered out) | `ShowImportSelectionProductCell.swift:78-95` | "Starts at", "Sold for", "Free" | "Começa em", "Vendido por", "Grátis" (xcstrings) | MATCH |
| 9 | Selection screen confirm button reads "Clone N listing(s)" | `ShowHostImportSelectionView.swift:100` | `"Clone N listing" + (N>1 ? "s" : "")` (literal Swift, no `String(localized:)`) | xcstrings has "Clone %lld listing%@" but pt-BR value identical, NOT translated | MATCH (mockup uses "Clone 1 listing" both locales, faithful). FLAG-NOT-LOCALIZED. |
| 10 | Import-from-Shop screen header "Import Listings from Shop" | `ShowHostImportShopView.swift:36` | "Import Listings from Shop" | "Importar listagens da loja" (xcstrings) | MATCH |
| 11 | Import-from-Shop button reads "Import N products" | `ShowHostImportShopView.swift:65` | "Import N products" | "Importar N produtos" (xcstrings: "Importar %lld produtos") | MATCH |
| 12 | Giveaway products cannot be cloned | `ShowHostImportSelectionView.swift:74` filter `$0.show_sale_settings?.type != .GIVEAWAY` | n/a (filter applied at list level) | n/a | MATCH (article says "Giveaway products can't be cloned", aligns with filter) |
| 13 | Article says "Clone copies all details (title, description, photos, price, sell mode, flash sale settings, shipping profile, category, size, color, condition, brand, quantity)" | Backend clone endpoint, not introspected here. Surface-level: cell renders price/title/availability/sale_settings | n/a | n/a | NOT VERIFIED at backend layer. Existing v1 made this same claim, no field-level audit done now. Recommend a follow-up server-side audit ticket. FLAG-PARTIAL-VERIFY. |
| 14 | Article says "(Added) products are greyed out, opacity 0.5" | `ShowImportSelectionProductCell.swift:72` `.opacity(isSelectable ? 1 : 0.5)` | n/a | n/a | MATCH |
| 15 | Article says "Cloning into the same show twice is blocked" | inferred from `isSelectable` flag, the `(Added)` prefix indicates it. Backend block not introspected. | n/a | n/a | MATCH (UI level). Backend dedup logic NOT VERIFIED. FLAG-PARTIAL-VERIFY. |

## NOT-LOCALIZED flags (existing iOS debt, separate from this article)

These are 3 strings that exist in xcstrings but with pt-BR value identical to EN, OR are hardcoded inline. The article ships the literal English in pt-BR mockup because that's what users actually see. **This is faithful to the current app, not a content bug.**

1. `"%lld unsolds, %lld solds"` (xcstrings: pt-BR value = EN value, untranslated)
2. `"(Added) " + product.title` (hardcoded inline, no xcstrings entry)
3. `"Clone %lld listing%@"` (xcstrings: pt-BR value = EN value, untranslated)
4. HostV2 menu strings "Quickie Upload", "Import from Shop", "Clone from Shows" (`ShostHostV2ViewController.swift:3656+`) are hardcoded literals, not in xcstrings. This article does not mockup the HostV2 menu, only the older preview action sheet which IS localized. Decision: drop the HostV2 mockup from v1 to avoid showing English in a pt-BR article.

**Recommendation**: file an iOS-side ticket to localize these 4 strings. Out of scope for this article PR.

## Verdict

PASS. Zero MISMATCH. Article copy matches Swift source character-for-character within the app's actual localization state.
