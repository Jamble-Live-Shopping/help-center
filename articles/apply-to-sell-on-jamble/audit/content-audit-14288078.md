# Content audit, article 14288078 (apply-to-sell-on-jamble)

Date: 2026-04-21
Scope: PII scan, internal leak scan, word diet, tone-of-voice.

## Scan 1, PII

- No real user names, emails, phone numbers, CPFs, or addresses in body
- `support@jambleapp.com` is a public support address, not PII
- Example product names (Pokémon TCG graduadas PSA, Hot Wheels Treasure Hunt) are categories, not SKUs tied to real listings

Status: CLEAR

## Scan 2, internal leaks

- No internal tool names (Metabase, BigQuery, Mixpanel) exposed
- No admin-only flags or feature toggles referenced
- No engineer names, no Slack channel names
- No revenue numbers, no approval rate percentages
- Mention of "equipe da Jamble" is generic, not internal team-specific

Status: CLEAR

## Scan 3, banned terms

- Zero em-dashes (U+2014)
- Zero en-dashes (U+2013)
- Zero "auction" / "leilão" (not relevant in this article anyway)
- Zero Nike / Adidas / fashion-only examples

Status: CLEAR

## Scan 4, word diet

Changes made:
- H2 "O que você vai aprender" kept (scannable intro pattern)
- H2 "Passo a passo" removed (was nested over individual H3 steps, redundant)
- H3 "Passo 1/2/3/4" flattened to job-to-do H2s: "Encontre a inscrição", "Preencha o formulário", "Aguarde a análise", "Seja aprovado e comece a vender"
- "Enquanto sua inscrição está em análise, nos 15 dias seguintes por favor não se inscreva novamente" → cut "nos 15 dias seguintes" (redundant with "enquanto está em análise", and "até 14 dias" already stated above)
- FAQ answers shortened (one-liner where possible)
- Tip "O erro mais comum..." kept (concrete, high-signal)

## Scan 5, tone-of-voice (first-time BR seller on mobile)

Read aloud test:
- Opens with "O que você vai aprender", direct
- "Antes de começar" lists requirements in bullet, no jargon
- Three entry paths are labeled clearly (perfil / configurações / assistindo um show)
- Form explanation uses examples a BR collector recognizes (cartas Pokémon, Hot Wheels)
- "Seja o mais específico possível" is encouraging, not preachy
- "Dicas para aumentar a chance de aprovação" frames tips as helpful, not gatekeeping
- FAQ is short, answers first

No passage requires re-reading. Reader reaches the end without friction.

Status: PASS

## Open blockers

Zero BLOCKERS.
