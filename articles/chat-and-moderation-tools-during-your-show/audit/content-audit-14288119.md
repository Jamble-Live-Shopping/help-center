# Content audit, article 14288119

## Scan 1, PII (personally identifiable info)

- Sample names in moderators mockup: Marina Silva, Bruno Souza, Larissa Mendes, with handles @marina.collects, @bruno.cards, @larissa.tcg
- These are **fictional** sample profiles for illustration, not real Jamble users
- No real email, phone, address, transaction ID, profile ID anywhere
- Verdict: **PASS**

## Scan 2, Banned words

| Word | pt-br count | en count | Status |
|---|---|---|---|
| em-dash `—` (U+2014) | 0 | 0 | PASS |
| en-dash `–` (U+2013) | 0 | 0 | PASS |
| auction | 0 | 0 | PASS |
| leilão | 0 | 0 | PASS |
| leilao | 0 | 0 | PASS |
| Hey / Yo / Salut (opener) | n/a (article, not message) | n/a | PASS |

Verdict: **PASS**

## Scan 3, Currency

- pt-BR body: contains `R$ 100` once (in the show notes example "Frete grátis acima de R$ 100"). Format is BR-correct (R$ space-separated, integer).
- en body: contains `$20` once (localized from R$ to $ in the matching show notes example). Zero `R$` leak.
- No prices in body other than illustrative show note examples
- Verdict: **PASS**

## Scan 4, Word diet (verbosity)

- pt-br.md: 8421 chars, ~1300 words, 11 sections
- en.md: 7770 chars, ~1240 words, 11 sections
- No filler ("As you may know", "It's worth noting"), no redundant intros
- Each section is action-oriented (verb + object headers)
- Verdict: **PASS**

## Scan 5, Tone

- pt-BR: tu/você consistent (você used throughout, no mix with tu), informal-but-clear (matches Jamble seller voice for help center)
- EN: second-person consistent, contracted forms (you'll, don't) where natural
- No corporate jargon ("synergize", "leverage")
- Imperative mood for procedures ("Toque em", "Tap")
- Verdict: **PASS**

## Scan 6, Alt-text quality

| Image | Alt text | Length | H2 keyword present | Verdict |
|---|---|---|---|---|
| chat-action-sheet pt-br | "Menu de ações iOS no chat com opções Responder, Ver perfil, Comunicar, Bloqueio de Show, Excluir esta mensagem, Cancelar" | 137 | YES (menu de ações) | PASS |
| chat-action-sheet en | "iOS chat actions menu with options Reply, See profile, Report, Block from show, Delete this message, Cancel" | 109 | YES (actions menu) | PASS |
| block-from-show-confirm pt-br | "Diálogo de confirmação iOS Bloqueio de Show com mensagem O usuário não poderá participar desse Show e botões Cancelar e Bloqueio de Show" | 142 | YES (Bloqueio de Show) | PASS |
| block-from-show-confirm en | "iOS Block from show confirmation dialog with message The user will not able to join this show and Cancel and Block from show buttons" | 134 | YES (Block from show) | PASS |
| my-moderators pt-br | "Tela Moderadores listando três perfis com avatares, nome de exibição, handle e botões Adicionar em roxo e Remover em cinza" | 122 | YES (Moderadores, Adicionar, Remover) | PASS |
| my-moderators en | "Moderators screen listing three profiles with avatars, display name, handle, and Add buttons in purple and Remove buttons in gray" | 130 | YES (Moderators, Add, Remove) | PASS |
| actions-comparison pt-br | "Cartões mostrando cinco ações de moderação Excluir esta mensagem, Bloqueio de Show, Bloquear conta, Comunicar, Ver perfil com tags de papel Vendedor, Moderador ou Qualquer pessoa" | 178 | YES, but **OVER 150 chars limit** | NEEDS TRIM |
| actions-comparison en | "Cards showing five moderation actions Delete this message, Block from show, Block account, Report, See profile with role tags Seller, Moderator, or Anyone" | 152 | YES, **borderline over 150** | NEEDS TRIM |

**Action**: trim alt text on actions-comparison images (see fix below)

## Fix applied

Alt text for actions-comparison shortened to fit 15-150 char window. Verified post-fix.

## Final verdict

After alt-text trim: **ZERO BLOCKER**. Article is content-audit clean for ship.
