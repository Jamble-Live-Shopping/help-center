# Content audit: make-a-shipping-adjustment (intercom 14288137)

Audience: seller_br (v2_rewrite)
Date: 2026-05-11

## 7-scan content review

| Scan | Result | Notes |
|---|---|---|
| 1. PII | PASS | No emails, phone numbers, real user names. Support email `support@jambleapp.com` is the canonical Jamble support address. Sample buyer handle `@marina_cards` and address `Avenida Paulista, 1578` are illustrative. |
| 2. Banned words (auction / leilão) | PASS | Zero matches in pt-br.md and en.md. |
| 3. Currency leak (R$ in EN) | PASS | en.md has zero `R$`. Sample monetary values in en.md mockup screen-2 use `$8.50` / `$28.10` (the iOS strings `You paid $%@` and `Est. Ship. $%@` are not currency-localized in code, see code-audit). |
| 4. Word diet | PASS | Article has 7 H2 sections plus 4 H3 subsections in pt-br.md (mirror in en.md). Sections: O que você vai aprender / Antes de começar / Caso 1: antes de gerar a etiqueta / Caso 2: depois que a etiqueta já foi gerada / Quem paga o quê / Boas práticas / Perguntas frequentes / Precisa de ajuda. Each FAQ answer is 1-3 sentences. |
| 5. Tone | PASS | Direct, "você" address in pt-br, "you" in en. No jargon, no internal terminology. Explicit rule "antes da etiqueta = no app, depois da etiqueta = suporte" appears early to set expectations. |
| 6. Alt-text quality | PASS | Both image alts are descriptive (1 line each, ~150-180 chars), mention the screen name, the visible sections, the key fields, and the CTA button. No "Screenshot of" / "Image of". |
| 7. Stale-feature audit | PASS | See structured table below. |

## Stale-feature audit (structured)

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Edit Shipping Address screen, edit mode, with Personal Information + Shipping Address sections | Jamble-iOS/Jamble/SHIPPING/Add Edit Shipping Address/Views/AddEditShippingAddressInformationView.swift:256-292 | active | 2026-05-11 | Aymar | live_in_ios |
| BR field order (CEP, Street Name, Street Number, Interior/Apt, Neighborhood, City, State, Country) | Jamble-iOS/Jamble/SHIPPING/Add Edit Shipping Address/Configuration/BRAddressFormConfiguration.swift:21-32 | active | 2026-05-11 | Aymar | live_in_ios |
| CEP format XXXXX-XXX (8 digits) | Jamble-iOS/Jamble/SHIPPING/Add Edit Shipping Address/Configuration/BRAddressFormConfiguration.swift:62-70 | active | 2026-05-11 | Aymar | live_in_ios |
| State = 2-letter UF code | Jamble-iOS/Jamble/SHIPPING/Add Edit Shipping Address/Configuration/BRAddressFormConfiguration.swift:76-84 | active | 2026-05-11 | Aymar | live_in_ios |
| Post-show bundle row exposes Open Label + Nota Fiscal after label purchase | Jamble-iOS/Jamble/LIVE_SHOPPING/DashboardHost/Views/DashboardBundleView.swift:89-117 + Models/DashboardBundle.swift:28-34 | active | 2026-05-11 | Aymar | live_in_ios |
| No self-service Edit Label / Cancel Label action exists in the bundle row | Jamble-iOS/Jamble/LIVE_SHOPPING/DashboardHost/Models/DashboardBundle.swift:28-34 (ActionType enum has only purchaseLabel / openLabel / addNotaFiscal / openNotaFiscal / examptNotaFiscal / unknown) | active | 2026-05-11 | Aymar | live_in_ios |
| "You paid $X" appears once label is purchased | Jamble-iOS/Jamble/LIVE_SHOPPING/DashboardHost/Views/DashboardBundleView.swift:72-78 + xcstrings "You paid $%@" | active | 2026-05-11 | Aymar | live_in_ios |
| Self-service Confirm Weight modal exists in app for the seller to adjust weight | Jamble-iOS/Jamble/TRANSACTION/Sale/ChangeShippingWeightViewController.swift (file exists, zero call sites; xcstrings keys CONFIRM WEIGHT / Current weight only referenced from this file) | deprecated | 2026-05-11 | Aymar | deprecated |

The dead Confirm Weight controller is the single stale-feature finding. It is the central reason v2 dropped the v1 "Step 1: Confirm the shipping weight" walkthrough. The article body now explicitly tells the seller that pre-label weight is locked to the product's shipping profile and that adjustments go through support.

No Auction/Leilão wording. No Jamble Prime references. No verified-badge references.

## Numbers cited (traceability)

| Number | Source | Verbatim? |
|---|---|---|
| CEP format = 8 digits, XXXXX-XXX | `BRAddressFormConfiguration.swift:62-70` | yes (regex `^[0-9]{5}-[0-9]{3}$`) |
| Sample shipping price `$8.50` / `R$8,50` in mockups | Illustrative, mirrors the bundled-shipments mockup convention | not a product claim (sample value) |
| Sample buyer total `R$147,00` / `$28.10` | Illustrative, sum of the 3 sample items | not a product claim (sample value) |

No invented numbers, no marketing-rounded values.

## Forbidden-term compliance

- `auction` / `leilão`: 0 matches
- em-dash `—`: 0 matches in pt-br.md and en.md (verified by `grep -c "—"`)
- en-dash `–`: 0 matches
- `R$` in en.md body: 0 matches

## Audience and scope rationale

The Intercom title "Faça um Ajuste de Envio" is broad enough that the v1 rewrite tried to cover everything from weight to address to label fix. v2 narrows the scope to two surfaces sellers actually interact with:

1. Pre-label sender-address edit, the only adjustment the seller can self-serve.
2. Post-label fallback to support, with a per-case decision table.

The sibling article `change-or-fix-your-shipping-label` covers the printing/regeneration/external tracking flow in more depth; this article links to it instead of duplicating.

## Verdict

Zero BLOCKER. Article shippable on the content-audit gate. One risk flag carried in flow.yml.risk_flags + a resolved_decisions entry to surface the dead `ChangeShippingWeightViewController.swift` in the PR body.
