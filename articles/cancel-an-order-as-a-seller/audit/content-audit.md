# Content audit: cancel-an-order-as-a-seller (14288152)

## Scan 1: User PII

Zero real user names, usernames, emails, or phone numbers. The sample order number `JMB-2A4F91` and product `Charizard Holo 1999` are plausible placeholders, not real records.

## Scan 2: Internal fee / commission leaks

Zero mentions of any take rate or percentage split or any percentage figure in the published body. The previous version leaked "Nenhuma comissão é cobrada" and "You don't pay the Jamble Fees on canceled orders", both removed in the rewrite. Replaced with user-facing neutral copy: "the buyer receives a refund automatically via PIX" and "you lose the sale."

## Scan 3: Forbidden terms

- **auction / leilão / leilao**: 0 occurrences
- **em dashes / en dashes**: 0 occurrences in body
- **Curly quotes in body**: only in iOS label quotes where intentional (none in final body; straight quotes used)
- **Numbered Slack-style lists**: N/A (article format, numbered lists are OK per step-by-step convention)

## Scan 4: Word diet

Original article: 28 lines of pt-BR body. Rewrite: stays in the same density range with richer structure (explicit "Option A" vs "Option B" branches, status-by-status list). No superfluous sentences.

Each heading serves a specific step or decision point:
- "O que você vai aprender" (What you'll learn): scope in one sentence
- "Antes de começar" (Before you start): prerequisite
- "As duas formas de cancelar" (The two ways to cancel): high-level branching
- "Passo 1" + "Passo 2" + "Opção A" + "Opção B" + "Passo 3": the procedure
- "O que acontece depois" (What happens next): outcomes
- "Quando posso cancelar" (When can I cancel): status gating
- "Boas práticas" (Best practices): tone + guardrails
- "Perguntas frequentes" (FAQ): edge cases
- "Precisa de ajuda?" (Need help?): escalation

## Scan 5: Tone of voice test

Readable top to bottom by a first-time BR seller on phone. Short paragraphs, direct instructions ("Toque em ..."), no marketing fluff, no jargon. Sample reader test: a seller in doubt at status Confirmed can reach the action "toque em Cancel Sale" within 3 paragraph jumps.

## Scan 6: Currency localization

- pt-BR body: `R$ 285,00` (comma decimal) in mockup, R$ referenced in prose
- EN body: `R$ 285.00` (dot decimal) in mockup, R$ referenced in prose
- Zero `$` without `R`
- Zero exposed prices in body text outside the mockup illustration

## Scan 7: PIX consistency

PIX mentioned 3 times across the article (pt-BR): reembolso PIX in intro, PIX in Passo 3 outcomes, PIX in FAQ. All refer to the buyer refund mechanism. Source: Pagar.me is the PSP for Jamble BR.

## BLOCKERS

None.
