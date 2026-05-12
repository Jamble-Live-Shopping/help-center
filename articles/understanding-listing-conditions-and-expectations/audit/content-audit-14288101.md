# Content audit, intercom_id=14288101

slug: `understanding-listing-conditions-and-expectations`
audited_at: 2026-05-11

## 7-scan content audit

| Scan | Status | Notes |
|---|---|---|
| 1. PII | PASS | No emails, phone numbers, CPF, or personal data. Only the `support@jambleapp.com` mailbox is present in pt-br.md and en.md. |
| 2. Banned terms (auction / leilão / leilao) | PASS | `grep -ic "auction\|leil" pt-br.md en.md` = 0. Forbidden_terms enforced by the validator. |
| 3. Currency leak (R$ in en.md) | PASS | en.md uses `$90.00` only. pt-br.md uses `R$ 450,00` only. No leak in either direction. |
| 4. Word diet (no padding, no marketing) | PASS | Each paragraph carries a verifiable fact tied to the condition flow. Removed v1 marketing claims ("sell better", "number one cause of returns"). |
| 5. Tone (operational, sober, BR seller voice) | PASS | Imperative + practical. No hype, no emojis. Mirrors the verified UI literally. |
| 6. Alt text quality (15-150 chars, no "Screenshot of") | PASS | Both alt texts describe the screen content + key labels. See below. |
| 7. Stale-feature audit | PASS | All 5 tier IDs are in the backend `ALLOWED_CONDITIONS` allowlist (`product.py:1246`). All pt/en tier titles come verbatim from `condition.json` (currently in main). No reference to deprecated features (no badges, no Jamble Prime, no auction wording). |

## Alt text inventory

| File | Image | Alt text | Length | Verdict |
|---|---|---|---|---|
| pt-br.md | section-row | "Linha Condição no fluxo de criação de anúncio, posicionada entre Cor e Preço" | 75 | PASS |
| pt-br.md | condition-picker | "Tela de seleção de condição com cinco opções: Novo com etiquetas, Novo sem etiquetas, Muito Bom, Bom, Satisfatório" | 116 | PASS |
| en.md | section-row | "Condition row inside the create-listing flow, sitting between Color and Price" | 78 | PASS |
| en.md | condition-picker | "Condition picker screen with five options: New with tags, New without tags, Very Good, Good, Satisfactory" | 103 | PASS |

## Tier copy verification (verbatim grep)

| Tier | pt-br.md contains | en.md contains | Source |
|---|---|---|---|
| `NEW_WITH_TAGS` | `Novo com etiquetas` + verbatim pt description | `New with tags` + verbatim en description | `condition.json` |
| `NEW_WITHOUT_TAGS` | `Novo sem etiquetas` + verbatim pt description | `New without tags` + verbatim en description | `condition.json` |
| `VERY_GOOD` | `Muito Bom` + verbatim pt description | `Very Good` + verbatim en description | `condition.json` |
| `GOOD` | `Bom` + verbatim pt description | `Good` + verbatim en description | `condition.json` |
| `SATISFACTORY` | `Satisfatório` + verbatim pt description | `Satisfatory` + verbatim en description | `condition.json` |

(Spot-check: `grep -c "Pouco usado, com sinais mínimos de desgaste, bem conservado" pt-br.md` returns 1. Same pattern for the four other pt descriptions and the five en descriptions.)

## Stale-feature audit

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| 5-tier condition list (NEW_WITH_TAGS, NEW_WITHOUT_TAGS, VERY_GOOD, GOOD, SATISFACTORY) | `jamble_backend/src/routers/product.py:1246` | live | 2026-05-11 | backend | live_in_backend |
| Tier titles + descriptions verbatim pt + en | `jamble_backend/src/product_attributes/configs/attributes/condition.json:11-60` | live | 2026-05-11 | backend | live_in_backend |
| Picker layout (radio rows, "Condição" / "Condition" title) | `Jamble-iOS/Jamble/PRODUCT/Views/Components/ProductConditionCell.swift:11-137`, `Jamble-iOS/Jamble/PRODUCT/Views/SelectProductAttributeViewController.swift:1-300` | live | 2026-05-11 | iOS | live_in_ios |
| Section row layout (label + value + chevron) | `Jamble-iOS/Jamble/PRODUCT/Views/Components/ProductAttributeCell.swift:11-80` | live | 2026-05-11 | iOS | live_in_ios |
| Listing description 120-char cap | `Jamble-iOS/Jamble/PRODUCT/View Models/CreateProductViewModel.swift:177` | live | 2026-05-11 | iOS | live_in_ios |
| Edit listing flow | `Jamble-iOS/Jamble/PRODUCT/View Models/ProductViewModel.swift:458`, `Jamble-iOS/Jamble/PRODUCT/Views/ProductViewController.swift:147` | live | 2026-05-11 | iOS | live_in_ios |
| `support@jambleapp.com` mailbox | jamble.com infra | live | 2026-05-11 | platform | product_confirmed |

No deprecated features referenced. Article ships clean.

## What was tightened vs v1

1. Dropped invented per-tier buyer-expectation bullet lists; kept only the verified description from `condition.json`.
2. Replaced "Condition is optional but strongly recommended" with the verified fact that condition is part of the standard listing flow.
3. Replaced refund mechanics with a neutral "reach out to support" pointer (no code source for a condition-based refund pathway).
4. Removed performance claims ("sell better") and "number one cause of returns" ranking with no source.
5. Removed the v1 "decision guide" mockup (invented UI: a custom decision tree the app does not show) and replaced it with two faithful renderings of real iOS screens (the picker and the section row).

## Verdict

ALL PASS. Ship.
