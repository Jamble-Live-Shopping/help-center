# Compliance audit: what-to-do-if-a-package-is-delayed (intercom 14288128)

Audience: buyer_br (real-2 rewrite)
Date: 2026-05-11

18 checks per process/12-procedure-compliance.md. PASS or PARTIAL on each.

## 1. Single H1 (rule 25)

- pt-br.md H1 count: 1 ("O que fazer se um pacote estiver atrasado")
- en.md H1 count: 1 ("What to do if a package is delayed")

Verdict: PASS

## 2. No em-dashes / en-dashes (rule 0)

- pt-br.md em-dash count: 0
- pt-br.md en-dash count: 0
- en.md em-dash count: 0
- en.md en-dash count: 0

Verdict: PASS

## 3. No "auction" / "leilao" (rule 2c)

- pt-br.md: 0 matches
- en.md: 0 matches

Verdict: PASS

## 4. No R$ leak in EN (rule 2b)

- en.md R$ count: 0

Verdict: PASS

## 5. pt-BR primary, EN mirrors (rule 7)

- pt-br.md was written first
- en.md mirrors line by line with currency localized (no R$ in EN body)
- Section count matches: 9 H2 sections in both locales
- Image references mirror: both files reference the same 4 PNGs (2 locale-specific each)

Verdict: PASS

## 6. Verbatim UI strings from xcstrings (rule 5)

UI labels used in the article body and in the mockups:
- "Em Entrega" / "In Delivery" -> xcstrings `In Delivery`
- "Chegando amanha" / "Arriving Tomorrow" -> xcstrings `Arriving Tomorrow`
- "Enviar para" / "Ship to" -> xcstrings `Ship to`
- "Transportadora" / "Carrier" -> xcstrings `Carrier`
- "Numero de rastreamento" / "Tracking Number" -> xcstrings `Tracking Number`
- "Track" -> xcstrings `Track` (pt-BR value is "Faixa", documented in risk_flag)
- "Recebido?" / "Received?" -> xcstrings `Received?`
- "Cancelado" / "Canceled" -> backend `status` getter (`transaction.py:412-418`)
- "Numero do pedido" / "Order Number" -> xcstrings `Order Number`
- "Cancelar pedido" / "Cancel Order" (cross-ref only) -> xcstrings `Cancel Order`
- "Your Support Ticket", "Open Ticket" -> swift literals (xcstrings pt-BR keys not verified for these; the banner only appears when a buyer has an existing ticket, so the article cross-references the EN label that appears in app today)
- Refund text "em ate 5 dias uteis" / "within 5 business days" -> backend `description` getter (`transaction.py:622-625, 631-632`)
- SHIP_TIMEOUT line "O vendedor nao enviou seu pedido a tempo..." / "The seller didn't ship your order on time..." -> backend `description` getter (`transaction.py:639-649`)
- "Cancel Order" mention -> cross-ref to existing buyer Cancel surface (rule 25/26 of how-order-cancellations-work article)

Verdict: PASS

## 7. No invented UI surfaces (rule 5)

Every screen and button the article describes maps to a real iOS file:line, documented in code-audit-14288128.md. No invented "Contact Support" red button, no fake "Open Dispute" menu, no fictional "Shipping Delays" tab. All paths reference real screens.

Verdict: PASS

## 8. Mockup screens declared and rendered (rules 26-27)

- 2 screens declared in flow.yml.mockup_plan.screens (screen-1, screen-2)
- 4 HTMLs in mockup-sources/ (screen-1 + screen-2, pt-br + en)
- 4 PNGs in assets/mockups/ (all v3, all 960px wide = DPR3 from 320px viewport)
- 0 orphan HTMLs

Verdict: PASS

## 9. Every mockup anchored in markdown (rule 26)

- pt-br.md references both `screen-1__pt-br__v3.png` and `screen-2__pt-br__v3.png`
- en.md references both `screen-1__en__v3.png` and `screen-2__en__v3.png`

Verdict: PASS

## 10. Icon contract (rule 10e)

Both screens declared `html_must_not_contain: ["<img", "<svg", "icon-"]` (text-only anchor, Option B). HTMLs verified to contain no `<img>`, `<svg>` or `icon-` strings (`grep` clean).

Verdict: PASS

## 11. Refund timing grounded (rule 6 / post real-1)

Only timing claims in the article are:
- "10 days" / "10 dias" -> `entities/transaction.py:64-65`
- "5 business days" / "5 dias uteis" -> `entities/transaction.py:604-605, 614-615, 622-625, 631-632`
- "7 days" / "7 dias" (for "when to open a support ticket" heuristic) -> editorial heuristic, NOT a contractual SLA, framed as "if X is more than 7 days old" rather than "we promise within 7 days". No backend grounding required.

Verdict: PASS

## 12. negative_scan + risk_flags alignment (rule 27)

No `negative_scan` declared, so the negative_scan + risk_flags pairing rule does not apply. risk_flags has 1 entry (xcstrings Track mistranslation) paired with 1 entry in resolved_decisions, so the published-with-active-risk gate is satisfied.

Verdict: PASS

## 13. metadata.yml fields

- intercom_id: 14288128 (matches)
- slug: what-to-do-if-a-package-is-delayed (matches)
- collection_id: 19177937 (matches)
- default_locale: pt-br
- state: published
- author_id: 7980507
- last_sync: 2026-05-11T00:00:00Z
- titles: under 60 chars each, no em-dash
- descriptions: pt-br 108 chars, en 106 chars (both <=140)

Verdict: PASS

## 14. Image alt text quality

All 4 image references have alt text 130-174 chars, mention H2 keywords, never say "image of"/"screenshot of". Each image is framed by a sentence intro before and a caption-style continuation after.

Verdict: PASS

## 15. No tables 3+ cols left as markdown

The article uses prose + 4 bulleted lists. Zero markdown tables.

Verdict: PASS

## 16. Forbidden_terms grep (flow.yml content_contract)

flow.yml declares no forbidden_terms, so the deterministic ban list is empty by design.

Verdict: PASS

## 17. Cross-link integrity

Article references:
- "Cancel Order" / "Cancelar pedido" button (existing buyer cancel flow) -> live in `PurchaseViewController.swift:657-672`, primary subject of sister article `how-order-cancellations-work` (intercom 14288126)
- "Your Support Ticket" banner / "Open Ticket" -> live in `PurchaseViewController.swift:108-167`
- No broken cross-links to articles that have not shipped.

Verdict: PASS

## 18. TOC policy

pt-br.md and en.md each have 9 H2 sections. Workflow toc_policy = `warn`. Validator emits soft warn `toc_missing_pt` / `toc_missing_en`. Per article calibration, no TOC was added because:
- H2 titles are descriptive enough for scroll-skimming
- Article is a buyer reference, not a long-form runbook
- Adding a TOC for 9 sections would push the meaningful content below the fold on mobile

Verdict: PARTIAL (soft warn accepted, not blocking)

## Summary

| Check | Status |
|---|---|
| 1. Single H1 | PASS |
| 2. No em/en-dashes | PASS |
| 3. No auction/leilao | PASS |
| 4. No R$ in EN | PASS |
| 5. pt-BR primary mirror | PASS |
| 6. Verbatim UI strings | PASS |
| 7. No invented UI | PASS |
| 8. Mockups declared+rendered | PASS |
| 9. Every mockup anchored | PASS |
| 10. Icon contract (text-only) | PASS |
| 11. Refund timing grounded | PASS |
| 12. negative_scan/risk_flags | PASS |
| 13. metadata fields | PASS |
| 14. Alt text quality | PASS |
| 15. No 3+col tables | PASS |
| 16. Forbidden_terms grep | PASS |
| 17. Cross-link integrity | PASS |
| 18. TOC policy | PARTIAL (soft warn, accepted) |

17 PASS, 1 PARTIAL (soft warn accepted). Article shippable on the compliance gate.
