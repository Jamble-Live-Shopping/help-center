# Code audit, intercom_id=14288101

slug: `understanding-listing-conditions-and-expectations`
audited_at: 2026-05-11
jamble_ios_root: `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble`
jamble_backend_root: `/Users/aymardumoulin/Projects/jamble_backend`

## Source map (iOS + backend)

| File | Lines | Role |
|---|---|---|
| `Jamble-iOS/Jamble/PRODUCT/Models/ProductCondition.swift` | 1-25 | `ProductCondition` model (id, title, description, order). Title and description are server-driven, not localised client-side. |
| `Jamble-iOS/Jamble/PRODUCT/Models/Product.swift` | 319-324 | Only `new_with_tags` and `new_without_tags` IDs are referenced in client code. For other IDs, the title is suffixed with the localised "Condition" string. |
| `Jamble-iOS/Jamble/PRODUCT/Views/Components/ProductConditionCell.swift` | 11-137 | Picker cell layout: title label, description label, radio circle on the right, divider. Title 17pt medium, description 15pt regular blue. |
| `Jamble-iOS/Jamble/PRODUCT/Views/SelectProductAttributeViewController.swift` | 1-300 | Generic picker for product attributes (size, color, condition). Nav title centered, back chevron left, CLEAR button right (when selection exists). |
| `Jamble-iOS/Jamble/PRODUCT/View Models/CreateProductViewModel.swift` | 494-526, 670-680 | Default create-product flow lists Condition as `isOptional: false` (REQUIRED). Section title pulled from `String(localized: "Condition")`. |
| `Jamble-iOS/Jamble/PRODUCT/View Models/CreateProductViewModel.swift` | 528-548 | Quick upload flow lists Condition as `isOptional: true`. |
| `Jamble-iOS/Jamble/PRODUCT/Views/SwiftUI/Components/ProductInfoSection.swift` | 167-176 | Display-side: appends " Condition" to "Very good", "Good", "Satisfactory" titles. |
| `Jamble-iOS/Jamble/PRODUCT/Models/CreateProductSectionType.swift` | 57-58 | Section type `.CONDITION` returns `String(localized: "Condition")` as title. |
| `Jamble-iOS/Jamble/PRODUCT/View Models/CreateProductViewModel.swift` | 175-182 | Description input is capped to 120 characters via `.prefix(120)`. |
| `Jamble-iOS/Jamble/SERVICE/API/Repository/Modules/Product/ProductRepository.swift` | 69, 432-434 | Client calls `get_conditions` to load the picker options. Response is `[ProductCondition]`. |
| `jamble_backend/src/routers/product.py` | 1242-1255 | Backend route `/get_conditions`. `ALLOWED_CONDITIONS = {"NEW_WITH_TAGS", "NEW_WITHOUT_TAGS", "VERY_GOOD", "GOOD", "SATISFACTORY"}`. Only these five are returned to clients today. |
| `jamble_backend/src/product_attributes/configs/attributes/condition.json` | 1-97 | Canonical tier definitions (id, en title, pt title, en description, pt description, order). Source of truth for tier copy. |

## Canonical tier copy (verbatim from `condition.json`)

| ID | order | pt title | pt description |
|---|---|---|---|
| `NEW_WITH_TAGS` | 1 | `Novo com etiquetas` | `Nunca usado e impecável, completo com as etiquetas originais de compra.` |
| `NEW_WITHOUT_TAGS` | 2 | `Novo sem etiquetas` | `Nunca usado, em perfeito estado, mas sem as etiquetas originais.` |
| `VERY_GOOD` | 8 | `Muito Bom` | `Pouco usado, com sinais mínimos de desgaste, bem conservado.` |
| `GOOD` | 9 | `Bom` | `Usado com cuidado e bem conservado, com quaisquer defeitos claramente indicados.` |
| `SATISFACTORY` | 10 | `Satisfatório` | `Usado frequentemente, com desgaste visível e defeitos notados.` |

| ID | en title | en description |
|---|---|---|
| `NEW_WITH_TAGS` | `New with tags` | `Unworn and pristine, complete with original purchase tags.` |
| `NEW_WITHOUT_TAGS` | `New without tags` | `Never worn, in perfect condition, but without the original tags.` |
| `VERY_GOOD` | `Very Good` | `Lightly used with minimal signs of wear, well-maintained.` |
| `GOOD` | `Good` | `Gently worn and well cared for, with any defects clearly noted.` |
| `SATISFACTORY` | `Satisfactory` | `Frequently worn with visible wear and noted defects.` |

(The backend `condition.json` contains 18 tiers total, but only the 5 above are returned by the public `/get_conditions` endpoint per the `ALLOWED_CONDITIONS` allowlist in `product.py:1246`. Other tiers like `MINT`, `NEAR_MINT`, `FAIR`, `POOR`, `DAMAGED`, `UNCIRCULATED`, etc. exist in config but are not exposed to sellers today.)

## Claim verification table

| Claim in article | Source | Verdict |
|---|---|---|
| 5 condition tiers on Jamble | `product.py:1246` `ALLOWED_CONDITIONS = {NEW_WITH_TAGS, NEW_WITHOUT_TAGS, VERY_GOOD, GOOD, SATISFACTORY}` | MATCH |
| Tier names "Novo com etiquetas", "Novo sem etiquetas", "Muito Bom", "Bom", "Satisfatório" (pt-BR) | `condition.json` title.pt | MATCH (verbatim) |
| Tier names "New with tags", "New without tags", "Very Good", "Good", "Satisfactory" (en) | `condition.json` title.en | MATCH (verbatim) |
| Tier descriptions verbatim | `condition.json` description.pt and description.en | MATCH (verbatim) |
| Section/screen title "Condição" / "Condition" | `Localizable.xcstrings` `"Condition"` -> pt `Condição`; `CreateProductSectionType.swift:57-58` | MATCH |
| Condition row sits between Color and Price in the listing flow | `CreateProductViewModel.swift:503-505` (orders 9, 10, 11) | MATCH |
| Picker layout: title 17pt medium black, description 15pt regular blue, radio circle right | `ProductConditionCell.swift:15-49` | MATCH |
| Picker top bar: back chevron, "Condition" centred, optional CLEAR | `SelectProductAttributeViewController.swift:58-95` | MATCH |
| Sellers can edit a listing after publishing | `ProductViewModel.swift:458` `editProduct()` + `ProductViewController.swift:92,147` | MATCH |
| Sellers have 120 characters for the listing description | `CreateProductViewModel.swift:177` `$0?.prefix(120)` | MATCH (note: this is the listing description, not a condition-specific limit) |

## Claims dropped (post CONCEPT doctrine)

These were present in v1 and removed because they could not be cited from iOS code, xcstrings, or backend:

| v1 claim | Why dropped |
|---|---|
| "Condition is optional but strongly recommended." | Wrong for the default create-product flow. `CreateProductViewModel.swift:504` sets `isOptional: false`. Replaced with "Condition is part of the standard listing flow." |
| "If the condition was misrepresented, the buyer may get a full refund." | No code or backend reference found for a condition-based refund pathway. Refund/dispute UX is owned by the support team, not by the listing flow. Replaced with a neutral pointer to support, without naming a specific remedy. |
| "Tap the listing, update the condition, and save." | The actual edit entry-point (`editProduct()` in `ProductViewModel.swift:458`) is reached from the listing's own action sheet, not by tapping the listing card. Replaced with the verified flow (open the listing, then choose Edit). |
| "You can edit the condition of any listing before it sells." | Code does not gate condition edits on sold-state in the picker layer; the gate lives elsewhere. Softened to "before the listing is sold". |
| "Products with a condition rating sell better because buyers know what to expect." | No backend or analytics tie in code to back this performance claim. Dropped. |
| "Buyers naturally expect lower prices for lower conditions." | Behavioural assumption, no code source. Kept the practical advice ("describe and photograph every defect") and dropped the price claim. |
| "Over-rating condition is the number one cause of returns on Jamble." | No source for "number one cause" claim. Dropped the ranking; kept the underlying tip about being accurate. |
| Standalone tier sub-headings with explicit "What buyers expect" / "When to use it" bullet lists per tier | The picker shows ONE short description per tier (from `condition.json`), not multi-bullet expectations. The v1 bullets were largely invented elaboration. Kept the verified pt/en description verbatim and added a short framing line that does not invent new expectations. |
| "(maybe you planned to wear it and changed your mind)" hypothetical examples | Invented narrative not in code. Dropped. |
| "Quantity stepper / 120 characters" specifically attached to condition description | The 120 cap is on the listing description as a whole, not on a per-condition note. Kept the 120-char fact tied to the listing description in the writing-tips section, not to condition. |

## pt-BR xcstrings spot-check

```
"Condition" -> "Condição"  (Localizable.xcstrings:7226-7237)
```

No other condition-specific UI strings exist in `Localizable.xcstrings`. All tier titles and descriptions are server-driven via `/get_conditions`.

## Negative scan

- No per-tier explanatory copy ("What buyers expect" lists) exists in `Localizable.xcstrings` or in iOS Swift sources. The picker shows ONLY the title and the single-line description from the backend.
- No "dispute resolution" UI tied to condition exists in the listing flow. Dispute UX lives outside the create-product code path.
- No "condition affects price" logic exists in the create-product flow. Price is a free-text input independent of condition (`CreateProductViewModel.swift:505`).

## Verdict

Article is safe to ship if it:
1. Names exactly the 5 verified tiers using the pt/en titles from `condition.json`,
2. Quotes the verified pt/en description per tier verbatim,
3. Describes the section title as "Condition / Condição" and the picker layout as documented in `ProductConditionCell.swift`,
4. Does not invent per-tier buyer-expectation lists, refund mechanics, or performance claims.
