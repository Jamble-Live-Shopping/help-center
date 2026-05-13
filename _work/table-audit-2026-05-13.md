# Mobile Table Audit — 2026-05-13

Context: `process/07-tables-mobile.md` says Intercom tables are clipped on
mobile and must be converted before publication. PR #123 exposed that the
process existed only as documentation, not as an executable validator rule.

## Source scan, after fixing #123 locally

Remaining source tables: 12 slugs, 29 Markdown tables.

| Slug | Locale | Line | Columns | Rows | Header |
|---|---:|---:|---:|---:|---|
| buy-it-now-sell-at-a-fixed-price | en | 77 | 3 | 5 | Criterion / Buy It Now / Real Time Offer |
| buy-it-now-sell-at-a-fixed-price | pt-br | 77 | 3 | 5 | Critério / Comprar agora / Oferta em tempo real |
| coins-and-currency-listing-requirements | en | 37 | 3 | 5 | Condition / Coins / Banknotes |
| coins-and-currency-listing-requirements | pt-br | 37 | 3 | 5 | Estado / Moedas / Cédulas |
| discounts-during-your-show-flash-sales | en | 26 | 3 | 4 | Feature / Buy It Now / Flash Sale |
| discounts-during-your-show-flash-sales | pt-br | 26 | 3 | 4 | Característica / Compra Direta / Venda Relâmpago |
| make-a-shipping-adjustment | en | 50 | 2 | 4 | Situation / What to ask support |
| make-a-shipping-adjustment | pt-br | 50 | 2 | 4 | Situação / O que pedir ao suporte |
| packaging-guidelines | en | 78 | 3 | 4 | Size / Dimensions (approx.) / Typical use |
| packaging-guidelines | pt-br | 78 | 3 | 4 | Tamanho / Dimensões (aprox.) / Uso típico |
| set-up-shipping-before-you-sell | en | 67 | 3 | 5 | Profile / Best for / Example items |
| set-up-shipping-before-you-sell | pt-br | 67 | 3 | 5 | Perfil / Melhor para / Exemplos |
| shipping-policy-for-sellers | en | 28 | 2 | 4 | Step / Deadline |
| shipping-policy-for-sellers | pt-br | 28 | 2 | 4 | Etapa / Prazo |
| shipping-via-correios-pac-sedex | en | 29 | 4 | 3 | Carrier / Service / Speed / Best for |
| shipping-via-correios-pac-sedex | en | 60 | 2 | 11 | Profile / Weight range |
| shipping-via-correios-pac-sedex | en | 82 | 2 | 3 | Format / Best for |
| shipping-via-correios-pac-sedex | en | 115 | 2 | 4 | Status / What it means |
| shipping-via-correios-pac-sedex | pt-br | 29 | 4 | 3 | Transportadora / Serviço / Velocidade / Melhor para |
| shipping-via-correios-pac-sedex | pt-br | 60 | 2 | 11 | Perfil / Faixa de peso |
| shipping-via-correios-pac-sedex | pt-br | 82 | 2 | 3 | Formato / Melhor para |
| shipping-via-correios-pac-sedex | pt-br | 115 | 2 | 4 | Status / O que significa |
| sneakers-best-practices-for-sellers | en | 34 | 2 | 5 | Condition / What it means for sneakers |
| sneakers-best-practices-for-sellers | pt-br | 34 | 2 | 5 | Estado / O que significa para tênis |
| troubleshoot-shipping-costs-as-a-seller | en | 63 | 2 | 11 | Profile / Relative cost |
| troubleshoot-shipping-costs-as-a-seller | pt-br | 63 | 2 | 11 | Perfil / Custo relativo |
| understand-the-earnings-payout-timeline | en | 57 | 3 | 6 | Status / Color / What it means |
| understand-the-earnings-payout-timeline | pt-br | 57 | 3 | 6 | Status / Cor / O que significa |
| update-default-shipping-label-settings | en | 34 | 3 | 3 | Format / Code / When to use |

## Live Intercom scan, before republishing #123

Live articles with tables: 14. The `how-to-list-products-on-jamble`
source table is fixed in this branch, but the live article still has a
table until a manual Intercom sync is authorized.

| Slug | Intercom ID | Live tables |
|---|---:|---:|
| buy-it-now-sell-at-a-fixed-price | 14288112 | 2 |
| coins-and-currency-listing-requirements | 14288098 | 2 |
| discounts-during-your-show-flash-sales | 14288123 | 2 |
| how-order-cancellations-work | 14288126 | 2 |
| how-to-list-products-on-jamble | 14288093 | 2 |
| make-a-shipping-adjustment | 14288137 | 2 |
| packaging-guidelines | 14288140 | 2 |
| set-up-shipping-before-you-sell | 14288082 | 2 |
| shipping-policy-for-sellers | 14288125 | 2 |
| shipping-via-correios-pac-sedex | 14288134 | 8 |
| sneakers-best-practices-for-sellers | 14288113 | 2 |
| troubleshoot-shipping-costs-as-a-seller | 14288129 | 2 |
| understand-the-earnings-payout-timeline | 14288147 | 2 |
| update-default-shipping-label-settings | 14288142 | 1 |

Live-only/stale relative to local source scan: `how-order-cancellations-work`.
