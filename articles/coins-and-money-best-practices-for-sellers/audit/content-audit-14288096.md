# Content audit, article 14288096 (coins-and-money-best-practices-for-sellers)

Date: 2026-05-11
Scope: 7-scan content quality check on pt-br.md and en.md.

## Scan 1, PII

| Item | Status |
|------|--------|
| Email addresses (only support@jambleapp.com is allowed) | PASS, only support@jambleapp.com cited |
| Phone numbers | PASS, none |
| Real seller names or handles | PASS, none |
| Internal IDs (Intercom, Firestore, etc.) | PASS, none |

## Scan 2, banned words

| Banned token | pt-BR count | EN count | Status |
|---|---|---|---|
| em-dash U+2014 | 0 | 0 | PASS |
| en-dash U+2013 | 0 | 0 | PASS |
| auction (EN) | 0 | 0 | PASS |
| leilão (pt-BR) | 0 | 0 | PASS |
| Hey / Yo / Salut openers | n/a (article) | n/a | N/A |

## Scan 3, currency

| Locale | R$ count | $ count | Notes |
|---|---|---|---|
| pt-br.md | 0 | 0 | PASS, no currency literals (article is editorial, prices discussed in abstract) |
| en.md | 0 | 0 | PASS, no currency literals |

`currency_required: false` in flow.yml. Article does not assert any specific
price points, so no R$ exposure in either locale. No `R$` leak risk in EN.

## Scan 4, word diet

| Section | pt-BR length | EN length | Match |
|---|---|---|---|
| Total | ~8,600 chars | ~7,900 chars | OK (lexical divergence, no factual divergence) |
| What you'll learn | 384 chars | 360 chars | OK |
| Photo guidelines section | flagship section, mirrors 1:1 | flagship section, mirrors 1:1 | MATCH |
| Condition guidelines section | flagship section, mirrors 1:1 | flagship section, mirrors 1:1 | MATCH |

No filler ("this article will explain"), no marketing fluff, every paragraph
carries a fact or instruction.

## Scan 5, tone

- pt-BR uses informal direct address ("você"), consistent with Jamble brand voice
- EN uses informal direct address ("you"), 1:1 mirror tone
- Bullets opened with bold lead-in label, no preamble
- FAQ uses question / direct answer pattern
- Zero apology language, zero hedging ("kind of", "sort of")

## Scan 6, alt text quality

| Image | Alt length | H2 keyword overlap | Unique? | Status |
|---|---|---|---|---|
| screen-1 pt-BR | 132 chars | YES (fotos, fundo escuro, foco, reflexo de flash) | unique | PASS |
| screen-1 EN | 132 chars | YES (photos, dark background, focus, flash glare, out of focus) | unique | PASS |
| screen-2 pt-BR | 132 chars | YES (condição, Novo com etiquetas, Satisfatório, desgaste) | unique | PASS |
| screen-2 EN | 119 chars | YES (condition, New with Tags, Satisfactory, wear) | unique | PASS |

All alt texts: 15-150 char range, descriptive (not "image of"), keyword-overlap
with H2, unique per article.

## Scan 7, Stale-feature audit

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Real-time offers / Ofertas em tempo real (sell mode) | `ShowSaleType.swift` (cross-ref via audit 14288099) | active in iOS today | 2026-05-11 | Aymar | live_in_ios |
| Buy It Now (sell mode) | `ShowSaleType.swift` (cross-ref via audit 14288099) | active in iOS today | 2026-05-11 | Aymar | live_in_ios |
| Shipping profile name "Carta" | `articles/choose-a-shipping-profile/pt-br.md` (canonical, server-driven names) | active server-driven profile | 2026-05-11 | Aymar | live_in_backend |
| Shipping profile name "Booster" | `articles/choose-a-shipping-profile/pt-br.md` | active server-driven profile | 2026-05-11 | Aymar | live_in_backend |
| Shipping profile name "Pacotes pequenos" | `articles/choose-a-shipping-profile/pt-br.md` | active server-driven profile | 2026-05-11 | Aymar | live_in_backend |
| Condition system 5 levels (Novo com etiquetas through Satisfatório) | `ProductCondition.swift:10-15` + server taxonomy, audited 14288099 | active, server-driven taxonomy | 2026-05-11 | Aymar | live_in_ios |
| Condition label "Condition" / "Condição" | `Localizable.xcstrings` key "Condition" | active xcstrings key | 2026-05-11 | Aymar | live_in_ios |
| Casa da Moeda do Brasil (mint reference) | Real-world entity, not a Jamble feature; legitimate numismatic context | not a Jamble surface | 2026-05-11 | Aymar | product_confirmed |
| Numismatic grading services PCGS / NGC | Real-world entities, not Jamble features; used as slab grading vocabulary examples | not a Jamble surface | 2026-05-11 | Aymar | product_confirmed |

No deprecated features mentioned. No verified-badge references (Rising / Elite
/ Ultra / Jamble Partner deprecated 2026-04-28). No Jamble Prime references
(IAP stopped Jan 2026). No "leilão / auction" user-facing wording. No
reference to surfaces that have been removed.

## Scan 8, BR-relevance (per session memory `product_mix_br.md`)

| Example used | Category | OK? |
|---|---|---|
| 1 Real, 500 Cruzeiros, 1 Dollar (denomination examples) | Brazilian and international coins | YES |
| Cruzeiro, Cruzado, Cruzeiro Novo, Cruzado Novo, Cruzeiro Real, Real (denomination timeline) | Brazilian numismatic history | YES |
| Casa da Moeda do Brasil | Brazilian mint, real-world | YES |
| Período Imperial, Década de 1970 (era examples) | Brazilian historical periods | YES |
| 2000 Réis de 1924 (silver coin example) | Brazilian historical coinage | YES |
| Prata, Cobre-Níquel, Ouro, Bronze (material examples) | Numismatic materials | YES |
| PCGS MS-65, NGC AU-58 (grading examples) | Numismatic grading vocabulary | YES |
| PSA grading | NOT referenced (PSA is TCG grading, not coins) | N/A |

Zero fashion / sneaker / Nike examples. Zero non-collectible examples. Article
is fully aligned with `product_mix_br.md` (coins fit in the 7% "other"
collectibles bucket alongside diecast, figures, and other numismatic
sub-categories). Article respects BR-only market positioning.

## Open BLOCKERS

Zero BLOCKERS. Article is content-clean.
