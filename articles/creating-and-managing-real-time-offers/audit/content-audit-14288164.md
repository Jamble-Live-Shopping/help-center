# Content audit, creating-and-managing-real-time-offers (intercom 14288164)

Audit run on 2026-05-11.

Scope: pt-br.md (PRIMARY) + en.md (mirror) + metadata.yml descriptions.

## 7 scans

### 1. PII scan

| Check | Result |
|---|---|
| Personal email addresses | NONE (only `support@jambleapp.com`) |
| Phone numbers | NONE |
| Buyer or seller usernames | NONE (only a generic example `@maria_cards` inside the screen-2 mockup) |
| Order ids, payment ids | NONE |
| Internal Jamble employee names | NONE |

Verdict: PASS.

### 2. Banned words and deprecated features

| Term | Found in pt-br.md | Found in en.md | Verdict |
|---|---|---|---|
| `auction` (regex `\bauction\b`) | 0 | 0 | PASS |
| `leilão` / `leilao` (regex `\bleil[aã]o\b`) | 0 | 0 | PASS |
| `Compra Direta` (legacy BIN wording) | 0 | 0 | PASS |
| `Morte subita` (unaccented) | 0 | 0 | PASS |
| `Pre-Bid` (source key, must surface as Pre-Offer / Pré-oferta) | 0 | 0 | PASS |
| `Pré-lance` (legacy pt-BR wording) | 0 | 0 | PASS |
| `Rising` / `Elite` / `Ultra` (deprecated badges, 2026-04-28) | 0 | 0 | PASS |
| `Jamble Prime` (IAP stopped Jan 2026) | 0 | 0 | PASS |

Verdict: PASS. `forbidden_terms` are locked in `flow.yml`.

### 3. Currency scan

| Check | Result |
|---|---|
| `R$` in pt-br.md (article documents BRL price floor) | PRESENT, format `R$ 5,00` / `R$ 5.000,00` / `R$ 75,00` |
| `R$` leak in en.md | 0 (verified by validator `rdollar_leak_en`) |
| `$` in en.md mirror | PRESENT, format `$5` / `$5,000` / `$75.00` |
| Separator convention (pt-BR: vírgula = decimal, ponto = milhar; EN: inverse) | OK |

Verdict: PASS.

### 4. Word diet

| Section | pt-br words | en words | Comment |
|---|---|---|---|
| Header H1 + lead paragraph | ~52 | ~55 | Single sentence + intro paragraph, no padding |
| Step-by-step (steps 1 to 6) | ~480 | ~510 | Each step under 100 words, screen anchors break the flow |
| Timer mechanics | ~110 | ~115 | One short paragraph + rationale, no jargon |
| FAQs | ~210 | ~220 | 6 Q&A, each answer 1 to 2 sentences |

Verdict: PASS. No filler paragraphs, no walls of bullets.

### 5. Tone

- pt-BR primary, BR Portuguese throughout (e.g. `Comece em`, `Duração (segundos)`, `Próximo item`)
- Sentences in 2nd person singular (`você`), consistent with the rest of the seller corpus
- No outbound voice openers, no English source keys
- Screen captions use **bold** on UI labels
- No imperative-only `Faça X` walls; instructions are framed by the screen they map to

Verdict: PASS.

### 6. Alt-text quality

| Image | Alt text length | Mentions key UI elements |
|---|---|---|
| screen-1 pt-br | 137 chars | "Modo de venda", "Oferta em tempo real selecionado", "Comece em", "Duração (segundos)" |
| screen-1 en | 138 chars | "Sell mode", "Real Time Offer selected", "Start at", "Timer (Seconds)" |
| screen-2 pt-br | 196 chars | "Vendas em tempo real", "0:18", "3 ofertas" |
| screen-2 en | 196 chars | "Real-Time Sales", "0:18", "3 offers" |
| screen-3 pt-br | 137 chars | "Ativar Pré-oferta?", "As ofertas podem ser feitos antes do início do show" |
| screen-3 en | 134 chars | "Enable Pre-Offer?", "Offers can be placed before the show starts" |

All within 15 to 200 chars, all descriptive, no `Image of...` / `Screenshot of...`. Verdict: PASS.

### 7. Stale-feature audit

Every feature, button, and label described in the article was checked against the iOS source on 2026-05-11.

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Real Time Offer sale mode (AUCTION enum) | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:11` + xcstrings `Auction` -> EN `Real Time Offer`, pt-BR `Oferta em tempo real` | active | 2026-05-11 | iOS | live_in_ios |
| Pre-Offer toggle (PreBidToggleCell) | `PRODUCT/Views/Components/PreBidToggleCell.swift:33-44` + xcstrings `Enable Pre-Bid?` -> EN `Enable Pre-Offer?`, pt-BR `Ativar Pré-oferta?` | active | 2026-05-11 | iOS | live_in_ios |
| Sudden Death sale mode | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:13` + xcstrings `Sudden Death` -> pt-BR `Morte súbita` | active | 2026-05-11 | iOS | live_in_ios |
| Buy It Now sale mode | `LIVE_SHOPPING/Show/Model/ShowSaleType.swift:12` + xcstrings `Buy It Now` -> pt-BR `Comprar agora` | active | 2026-05-11 | iOS | live_in_ios |
| Live host overlay label `Real-Time Sales` / `Vendas em tempo real` | `LIVE_SHOPPING/Host/View/ShowHostViewController.swift:755-797` (setupCurrentSaleContainer, line 772) + xcstrings `Real-Time Sales` | active | 2026-05-11 | iOS | live_in_ios |
| Host action button title `Start Real Time Offer` / `%lld offers` / `Offer ended` | `LIVE_SHOPPING/Show/Model/ShowSale.swift:115-141` + xcstrings keys `Start Auction`, `%lld bids`, `Auction ended` | active | 2026-05-11 | iOS | live_in_ios |
| Run Again and Next item host follow-up actions | `LIVE_SHOPPING/SaleView/ViewModel/ShowSaleViewModel.swift:664-674` + xcstrings `Run Again` -> pt-BR `Reiniciar`, `Next item` -> pt-BR `Próximo item` | active | 2026-05-11 | iOS | live_in_ios |
| `Start at` and `Timer (Seconds)` textfields under the Real Time Offer picker | `PRODUCT/Views/Components/SellModeDefaultCell.swift:181-193` (AUCTION branch, min 10 / max 90 seconds) + xcstrings `Start at`, `Timer (Seconds)` | active | 2026-05-11 | iOS | live_in_ios |
| Pin / Unpin host actions | `LIVE_SHOPPING/SaleView/View/ShowSaleView.swift:435` + xcstrings `Pin`, `Unpin` | active | 2026-05-11 | iOS | live_in_ios |
| Sale-targeting picker (All / Followers / Buyers) per product | `LIVE_SHOPPING/Show/Model/ShowSaleTarget.swift` (enum exists), grep across `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble` returns only model + decode paths, no UI references | model-only, no UI | 2026-05-11 | iOS | deprecated |
| Cancel-sale reason picker (v1 claim) | `LIVE_SHOPPING/Host/View/ShowHostProductListViewController.swift:257-282` (only cancel-unpaid alert exists, offers `Rerun` and `Cancel` buttons only) | not implemented | 2026-05-11 | iOS | deprecated |
| `Auction` / `Leilão` user-facing wording (v1 claim) | xcstrings always localize `Auction` source key to `Real Time Offer` / `Oferta em tempo real`. Jamble policy bans the term in user-facing copy. | banned | 2026-05-11 | Product policy | deprecated |
| `Pre-Bid` user-facing wording (v1 claim) | xcstrings localize `Pre-Bid` source key to `Pre-Offer` / `Pré-oferta`. Source key must not leak. | banned | 2026-05-11 | iOS | deprecated |
| `Morte subita` (unaccented, v1 claim) | xcstrings value is the accented `Morte súbita`. Same drift class as the choose-quantities post-mortem (PR #96 commits 22a020f + d1f920b). | banned | 2026-05-11 | iOS | deprecated |
| Verified badges (Rising / Elite / Ultra) | Out of scope. Not mentioned in this article. Deprecated 2026-04-28 product-wide. | banned | 2026-05-11 | Product policy | deprecated |
| Jamble Prime references | Out of scope. Not mentioned in this article. IAP stopped Jan 2026. | banned | 2026-05-11 | Product policy | deprecated |

Verdict: PASS. All `live_in_ios` claims trace to a live file:line in the iOS repo. All `deprecated` claims are excluded from the article body (verified by `forbidden_terms` regex and grep).

## Open BLOCKERS

None.
