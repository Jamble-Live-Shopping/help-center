# Code Audit, make-a-shipping-adjustment (seller, intercom 14288137)

Date: 2026-05-11
Source iOS: Jamble-iOS develop (`/Users/aymardumoulin/Projects/Jamble-iOS/Jamble`)
Strings cross-referenced with `Jamble/RESOURCES/Localizable.xcstrings`.

## iOS source files referenced

| File | Lines used | Purpose |
|---|---|---|
| `Jamble/SHIPPING/Add Edit Shipping Address/Views/AddEditShippingAddressInformationView.swift` | 22-65, 68-82, 84-124, 256-292, 294-313 | The seller-facing Edit Shipping Address form. Two sections: Personal Information (firstName, lastName, phoneNumber) and Shipping Address (dynamic fields driven by `formConfiguration`). Header uses `\(viewModel.editingMode ? String(localized: "Edit") : String(localized: "Add")) Shipping Address`. CTA label `viewModel.editingMode ? "Edit" : "Add"`. |
| `Jamble/SHIPPING/Add Edit Shipping Address/Configuration/BRAddressFormConfiguration.swift` | 12-32, 34-89 | BR field order: postalCode, streetName, streetNumber (half), apartment (half), neighborhood, city, state (half-width effectively), country (isEditable=false). Placeholders are passed through `String(localized:)`. CEP regex `^[0-9]{5}-[0-9]{3}$`, 8-digit format. State validated against 27 UF codes. |
| `Jamble/LIVE_SHOPPING/DashboardHost/Views/DashboardBundleView.swift` | 25-46, 48-88, 89-117 | Renders one row per bundle on the host post-show dashboard. Title `"PACKAGE \(index + 1)"` resolves via xcstrings to `"PACKAGE %lld"` / `"PACOTE %lld"`. Right side shows `"You paid $%@"` after label purchase OR `"Est. Ship. $%@"` before. `actions` ForEach iterates `viewModel.bundle.actions` and renders one `IndicatorButton` per action with `Text(action.title)` (server-provided title). |
| `Jamble/LIVE_SHOPPING/DashboardHost/Models/DashboardBundle.swift` | 19-71, 24-71 | `DashboardBundle.actions: [Action]?` with `actionId` enum `purchaseLabel`/`openLabel`/`addNotaFiscal`/`openNotaFiscal`/`examptNotaFiscal`/`unknown`. NO action exists for "adjust", "edit weight", "change address", or "cancel label". Visual styling: `purchaseLabel` is dark/inverse, `openLabel` is tertiary background. |
| `Jamble/LIVE_SHOPPING/DashboardHost/ViewModels/DashboardBundleViewModel.swift` | 49 ; 58-59 | `handleAction(.purchaseLabel)` calls `repository.shipping.purchaseLabel(bundleId:)`. `handleAction(.openLabel)` reads `self.bundle.label` and routes to `coordinator.send(.openShippingLabel(...))`. No code path edits an already-purchased label. |
| `Jamble/RESOURCES/Localizable.xcstrings` | 2997-3010, 7242-7271, 8183-8197, 9176-9189, 10132-10146, 10588, 12764-12774, 13750, 15177-15187, 16992-17003, 17422-17436, 17454-17460, 21622-21636, 22979-22994, 23181-23215, 28068-28082, 29015-29030 | Verbatim labels used in mockups. See xcstrings table below. |

## xcstrings keys pulled (verbatim)

| Key | EN value | pt-BR value |
|---|---|---|
| `Edit` | `Edit` | `Editar` |
| `Add` | `Add` | `Adicionar` |
| `%@ Shipping Address` | `%@ Shipping Address` | (locale-formatted via `"Edit"` prefix and `Shipping Address` key) |
| `Shipping Address` | `Shipping Address` | `Endereço de Entrega` |
| `Personal Information` | `Personal Information` | `Informações Pessoais` |
| `First Name` | `First Name` | (placeholder text, pt-BR fallback to en) |
| `Last Name` | `Last Name` | (placeholder text) |
| `Phone Number` | `Phone Number` | (placeholder text) |
| `ZIP Code` | `ZIP Code` | `CEP` |
| `Street Name` | `Street Name` | `Nome da rua` |
| `Street Number` | `Street Number` | `Número` |
| `Interior/Apt` | `Interior/Apt` | `Complemento` |
| `Neighborhood` | `Neighborhood` | `Bairro` |
| `City` | `City` | `Cidade` |
| `State Code e.g SP` | `State Code e.g SP` | (BR config uses this same key) |
| `Country` | `Country` | `País` |
| `PACKAGE %lld` | `PACKAGE %lld` | `PACOTE %lld` |
| `Est. Ship. $%@` | `Est. Ship. $%@` | `Est. Ship. $%@` |
| `You paid $%@` | `You paid $%@` | `Você pagou $%@` |
| `CONFIRM WEIGHT` | `CONFIRM WEIGHT` | `CONFIRMAR PESO` (key exists but the surface that displays it is unreachable in production, see Stale-surface section) |
| `Current weight:  %f lbs` | `Current weight:  %f lbs` | `Peso atual: %f lbs` (same: unreachable) |
| `Confirm` | `Confirm` | `Confirmar` |

## Claim, source, verdict

| Article claim | iOS source | Verdict |
|---|---|---|
| Seller can edit sender address before generating the label | `AddEditShippingAddressInformationView.swift:256-292` Edit-mode header `"Edit Shipping Address"`; `Views/AddShippingAddressViewController.swift:15` controller is the entry from `PaymentMethodManagementCoordinator.swift:75` and `ShippingAddressSelectionCoordinator.swift:41` | MATCH |
| BR form has 8-digit CEP in XXXXX-XXX format | `BRAddressFormConfiguration.swift:62-70` regex `^[0-9]{5}-[0-9]{3}$` and 8-char validation | MATCH |
| State is the 2-letter UF code | `BRAddressFormConfiguration.swift:76-84` valid list of 27 UF codes, `String(localized: "State Code e.g SP")` placeholder | MATCH |
| BR address fields include Street Name, Street Number, Interior/Apt, Neighborhood, City, State, Country | `BRAddressFormConfiguration.swift:21-32` exact field order and placeholder keys | MATCH |
| After label purchase, only Open Label and Nota Fiscal buttons are exposed in the bundle row | `DashboardBundle.swift:28-34` action enum cases; `DashboardBundleView.swift:91-117` renders one button per action; there is no `editLabel` or `cancelLabel` case in `ActionType` | MATCH |
| Seller paid shipping price appears once label is purchased | `DashboardBundleView.swift:72-78` `if let _ = viewModel.bundle.label { if let paid = viewModel.bundle.sellerPaidShippingPrice { Text("You paid $\(...)") } }` | MATCH |
| Buyer's address cannot be edited from the seller side | No seller-side surface in `SHIPPING/` exposes buyer address mutation. `AddEditShippingAddressInformationView.swift` is bound to `viewModel` which is the seller's profile (called from `PaymentMethodManagementCoordinator` etc.), not from any post-show bundle action | MATCH (negative claim verified by absence) |
| Label is purchased through Melhor Envio | `ShippingRepository.swift` (purchaseLabel route) per prior change-or-fix-your-shipping-label code-audit; carrier text `Melhor Envio` cited in that article's audit set | MATCH (consistent with sibling article) |
| There is no in-app self-service for label weight or address adjustment after purchase | `DashboardBundle.Action.ActionType` enum has no edit case; `DashboardBundleViewModel.swift:43-65` `handleAction` only handles `purchaseLabel`, `openLabel`, NF-e variants | MATCH |

## Stale-surface audit (rule 27 negative_scan)

| Surface declared absent | iOS path | Verdict |
|---|---|---|
| Self-service confirm weight modal | `TRANSACTION/Sale/ChangeShippingWeightViewController.swift` | File EXISTS in the repo and in the xcode project (`project.pbxproj:43, 1518, 3056`) but has ZERO call sites: `grep -r "ChangeShippingWeightViewController" Jamble/` returns only the file's own declaration. `String(localized: "CONFIRM WEIGHT")` and `String(localized: "Current weight:  %f lbs")` are referenced ONLY from this file. The screen is unreachable from any presentation/coordinator code, so the prior v1 article's "CONFIRM WEIGHT" walkthrough described a surface no seller could open. Recorded under `flow.yml.source_of_truth.negative_scan` (file path) with a matching `risk_flags` entry. |

## v1 to v2 changes (mismatches FIXED)

1. v1 article centerpiece was the `CONFIRM WEIGHT` modal with a `Current weight: X lbs` label and a `Confirm` button. The Swift file (`ChangeShippingWeightViewController.swift`) exists but is never instantiated. The previous article documented a feature sellers cannot reach. v2 drops that walkthrough entirely and reframes around the two surfaces that ARE reachable: Edit Shipping Address (pre-label) and the bundle action row (post-label).
2. v1 told sellers they could "tap to edit the product" and change shipping profile of an already-sold item. The shipping profile is locked once the product is sold (the listing edit flow does not expose profile change for sold items). v2 explicitly states profile is editable BEFORE the sale and locked AFTER.
3. v1 said "the buyer's address is set at the time of purchase. If the address is wrong, the buyer needs to contact support". Kept in v2 because it matches the absence of any seller-side buyer-address mutation in `SHIPPING/`.
4. v1 mockup `confirm-weight__pt-br.html` rendered a screen with the dead `CONFIRM WEIGHT` flow. v2 deletes both confirm-weight HTMLs and renders:
   - screen-1: the actual `AddEditShippingAddressInformationView` in edit mode with BR field order (CEP, Street Name, Street Number + Interior/Apt half-row, Neighborhood, City, State + Country half-row), CTA = `Editar` / `Edit`.
   - screen-2: the actual bundle row from `DashboardBundleView` after label purchase, with `PACOTE 1` / `PACKAGE 1`, `Você pagou $8,50` / `You paid $8.50`, and the two visible action buttons (`Abrir etiqueta` / `Open Label` + `Nota Fiscal`).
5. v1 used a `lbs` weight unit consistent with the dead Confirm Weight modal (US convention). v2 removes weight UI entirely from the article body since no seller-facing weight input is reachable in BR.

## Open MISMATCH count: 0

All article claims verified against Swift source. One risk flag carried as `resolved_decision` in flow.yml (the dead `ChangeShippingWeightViewController.swift` must trigger a re-audit if any future PR wires it back into a coordinator).
