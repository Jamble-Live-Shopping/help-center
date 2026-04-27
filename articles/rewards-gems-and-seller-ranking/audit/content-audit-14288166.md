# Content audit, article 14288166 (rewards-gems-and-seller-ranking)

**Date**: 2026-04-27
**Auditor**: Help Center v2 worker
**Scope**: 6 scans, pt-br.md and en.md.

## 1. PII scan

| Risk | Result |
|---|---|
| Real seller usernames | Mockups use stylized samples (lucas_tcg, marina_pkmn, rafa.diecast, bianca.cards, diego.diecast). All fictitious, not on the platform. |
| Real customer names in body text | None |
| Email addresses | Only `support@jambleapp.com` (canonical support address) |
| Phone numbers | None |

PASS

## 2. Banned words scan

| Term | pt-br.md | en.md |
|---|---|---|
| `auction` | 0 | 0 |
| `leilão` / `leilao` | 0 | 0 |
| em-dash `—` (U+2014) | 0 | 0 |
| en-dash `–` (U+2013) | 0 | 0 |
| Hey/Yo/Salut openers | n/a (article, not message) | n/a |

PASS

## 3. Currency scan

The article does not reference monetary amounts. Sellers earn ranking points and badges, not money tied to Gems. No R$ or $ tokens needed.

| Locale | R$ count | $ count | Verdict |
|---|---|---|---|
| pt-br.md | 0 | 0 | PASS |
| en.md | 0 | 0 | PASS |

## 4. Word diet scan

| Locale | Word count | Reading time | Verdict |
|---|---|---|---|
| pt-br.md | ~720 words | ~4 min | OK (in target range for explainer) |
| en.md | ~700 words | ~4 min | OK |

Body kept tight, no waffle, no marketing copy. Each section answers one explicit question.

## 5. Tone scan

- Conversational, second-person ("você"/"you")
- Verbs front-loaded in CTAs ("Faça shows", "Engaje", "Host shows", "Engage")
- No corporate jargon ("monetize", "leverage", "ecosystem")
- Brand vocabulary aligned with iOS strings (Gems, Watch & Earn, Seller Ranking, badge tiers)

PASS

## 6. Alt-text quality

| Image | Alt text (length) | Verdict |
|---|---|---|
| gems-watch-earn pt-BR | "Tela de Recompensas com Assista e ganhe e botão Obter gemas grátis" (66c) | PASS, 15-150 |
| gems-watch-earn EN | "Rewards screen with Watch and Earn and Get Free Gems button" (60c) | PASS |
| seller-ranking pt-BR | "Classificação de Vendedores com regras de pontos e leaderboard" (62c) | PASS |
| seller-ranking EN | "Seller Ranking with point rules and a leaderboard list" (54c) | PASS |
| badge-gallery pt-BR | "Galeria com os 4 niveis de badges verificados Rising Elite Ultra e Parceiro da Jamble" (84c) | PASS |
| badge-gallery EN | "Gallery of the 4 verified badge tiers Rising Elite Ultra and Jamble Partner" (76c) | PASS |

All alt texts unique per article, contain feature keywords, no "Image of..." filler.

## BLOCKER count: 0

Ready to ship from a content quality standpoint.
