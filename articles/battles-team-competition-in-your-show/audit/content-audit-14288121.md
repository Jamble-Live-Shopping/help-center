# Content audit, article 14288121

Date: 2026-04-27

## Scan 1, PII / internal info leaks

| Pattern | Hits | Verdict |
|---|---|---|
| Email addresses other than support@jambleapp.com | 0 | PASS |
| Internal Slack channel names | 0 | PASS |
| Internal employee names | 0 | PASS |
| Linear ticket IDs | 0 | PASS |
| Real seller usernames in screenshots | mockup uses fictional handles `marina_pkmn`, `lucas_tcg`, `rafa.diecast` | PASS (synthetic) |
| Real R$ figures from prod | tier rewards R$25/50/200 are public seller-facing values | PASS |

## Scan 2, banned words

| Pattern | Hits | Verdict |
|---|---|---|
| `auction` / `Auction` | 0 | PASS |
| `leilão` / `leilao` / `Leilão` | 0 | PASS |
| `Hey` / `Yo` opener | 0 | PASS |
| Em-dash `—` | 0 | PASS (Rule 0) |
| En-dash `–` | 0 | PASS (Rule 0) |

## Scan 3, currency localization (Rule 2b)

| File | `R$` count | `$` count (excl R$) | Verdict |
|---|---|---|---|
| pt-br.md | 4 (R$ 25, R$ 50, R$ 200, R$ gasto) | 0 | PASS |
| en.md | 0 | 4 ($25, $50, $200, $ spent) | PASS |

## Scan 4, word diet

Original article: 856 words (pt-br). Updated: 945 words. Net +89 words for +3 mockups, +1 FAQ Q&A, methodology section. Density acceptable, no obvious filler to cut.

Sentences cut from prior version:
- "Os créditos expiram 7 dias depois de concedidos, então os vencedores devem usá-los rapidamente." → trimmed trailing clause "então os vencedores devem usá-los rapidamente" (redundant, the 7-day expiry is the message)

## Scan 5, tone of voice

Reading the article top-to-bottom, target persona = first-time BR seller on phone in PT-BR:
- Verbs are concrete (continue vendendo, escolha, observe)
- Numbers are explicit, no hand-wavy "depends on the tier"
- No corporate filler (no "this guide is your complete reference for...")

PASS.

## Scan 6, image alt-text quality

| Image | Alt text | ≥ 15 chars | Keywords match H2 | Verdict |
|---|---|---|---|---|
| battle-duration-picker (pt-br) | "Alerta Escolha a duração da batalha com botões 30m, 1h, 1h 30, 2h e Cancelar" | 78 | duração / batalha | PASS |
| battle-welcome (pt-br) | "Tela de boas-vindas Bem-vindo à batalha em fundo escuro com avatar do espectador, indicador da equipe Vermelha e botão Exibir regras de batalha" | 145 | batalha / equipe | PASS |
| battle-progress-bar (pt-br) | "Barra de progresso da batalha sobreposta ao show com pontuação Vermelho 1.250 e Azul 980, cronômetro 45:30 e botão Ver classificação" | 134 | progresso / pontuação | PASS |
| battle-ended (pt-br) | "Tela de fim de batalha em fundo escuro com Equipe vermelha venceu, pódio com top 3 jogadores marina_pkmn, lucas_tcg e rafa.diecast e botão Reivindicar R$ 25" | 158 | batalha / vencedor | PASS |

EN alts are 1:1 mirrors with currency localized, same lengths.

## Open BLOCKERS

None.
