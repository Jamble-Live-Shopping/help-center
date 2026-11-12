# Content Audit — how-to-list-products-on-jamble

Date: 2026-11-13 (5.11 fidelity pass; previous audit 2026-05-12)
Intercom ID: 14288093

## Editorial Checks

| Check | Result |
| --- | --- |
| Heading hierarchy | Pass. One H1, H2 sections unchanged from the previous version. |
| Source-backed labels | Pass. Mockup and body labels match 5.11 (xcstrings or prod backend builder). |
| Banned words / dashes | Pass. No leilão/auction, no em or en dashes, no " - " mid-sentence. |
| Currency | Pass. PT-BR uses R$ 5; EN body uses $5. Mockups show R$ because the app shows the show currency (BRL) in both languages. |
| Internal info | Pass. No code paths, flags, ticket numbers or code-only caps in the body. Title/description character caps and the quantity range were removed because the UI never shows them. |
| Alt text | Pass. Three unique descriptive alt texts per locale naming the visible labels. |
| PII | Pass. Sample product title is a public card name. |

## Stale-feature audit

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
| --- | --- | --- | --- | --- | --- |
| Nova listagem rápida header | iOS 5.11 CreateProductView.swift | Replaced by Criar Novo Anúncio | 2026-11-13 | content | live_in_ios |
| Selecione uma foto / Descrição (opcional) helper | iOS 5.11 + jamble_backend product_service.py | Replaced by Selecionar uma Foto / Descrição | 2026-11-13 | content | live_in_backend |
| Duração (segundos) timer field | iOS 5.11 SaleTypeSectionView.swift | Replaced by Temporizador (seg) | 2026-11-13 | content | live_in_ios |
| Ativar Pré-oferta? toggle copy | jamble_backend product_service.py | Replaced by Ativar pré-ofertas | 2026-11-13 | content | live_in_backend |
| Perfil de remessa with weight-range value | jamble_backend product_service.py, shipping_infos.py | Replaced by Perfil de envio with Automático | 2026-11-13 | content | live_in_backend |
| Lote / Unidades do lote | jamble_backend product_service.py | Current | 2026-11-13 | content | live_in_backend |
| R$ 5 minimum price | iOS Price.swift + validation message | Current, visible to users | 2026-11-13 | content | live_in_ios |
| Title 40 / description 120 / quantity 1 to 1.000 | jamble_backend product_service.py | Enforced but not shown in UI | 2026-11-13 | content | removed from body |
| Abrir em Live radio | jamble_backend product_service.py | 5.11.1+ only | 2026-11-13 | content | not mentioned |

## Verdict

Fidelity fix only; structure kept. Body sentences that described pre-5.11 UI were updated.
