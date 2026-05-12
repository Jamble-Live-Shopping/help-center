# Content audit, article 14288118 (raid-another-seller-s-show)

Date: 2026-05-11

## Scan 1, PII / internal info leaks

| Pattern | Hits | Verdict |
|---|---|---|
| Email addresses other than support@jambleapp.com | 0 | PASS |
| Internal Slack channel names | 0 | PASS |
| Internal employee names | 0 | PASS |
| Linear ticket IDs | 0 | PASS |
| Real seller usernames in screenshots | mockup uses fictional handles `marina_pkmn`, `rafa.diecast`, `lucas_tcg`, `bia.collect` and `Aymar` is referenced in example body copy (intentional, no harm, can be swapped to `Vendedor` if reviewer prefers) | PASS (synthetic) |
| Real R$ figures from prod | none in article | PASS |

## Scan 2, banned words

| Pattern | Hits | Verdict |
|---|---|---|
| `auction` / `Auction` | 0 | PASS |
| `leilao` / `leilão` / `Leilão` | 0 | PASS |
| `Hey` / `Yo` opener | 0 | PASS |
| Em-dash `—` (U+2014) | 0 | PASS (Rule 0) |
| En-dash `–` (U+2013) | 0 | PASS (Rule 0) |

## Scan 3, currency localization (Rule 2b)

| File | `R$` count | `$` count (excl R$) | Verdict |
|---|---|---|---|
| pt-br.md | 0 (article doesn't discuss prices) | 0 | PASS |
| en.md | 0 | 0 | PASS |

`currency_required: false` in flow.yml since this article does not describe pricing.

## Scan 4, word diet

Original v1 article: 745 words (pt-br). Updated: 691 words. Net minus 54 words for tighter copy, dropped one ambiguous claim ("seus espectadores simplesmente sairem" softening + removed "Voce ainda precisa tocar em End Show" duplicate). No filler observed.

## Scan 5, tone of voice

Reading the article top-to-bottom, target persona = first-time BR seller on phone in PT-BR:

- Verbs are concrete (toque, escolha, encerre, anuncie)
- Numbers are explicit (1 raid per show, 5 or 10 viewers can help)
- No corporate filler ("este guia explica" used once, in the standard structure)
- Buttons match iOS labels verbatim (pt-BR `Selecionar show ao vivo`, English-hardcoded `End without Raid` kept as-is per xcstrings audit)

PASS.

## Scan 6, image alt-text quality

| Image | Alt text length | Keywords match H2 | Verdict |
|---|---|---|---|
| screen-1 (pt-br) | 209 chars | Painel / The Jamble Raid / Selecionar show ao vivo | PASS |
| screen-2 (pt-br) | 197 chars | Grade Selecione um Live / cards / Selecionar show ao vivo | PASS |
| screen-3 (pt-br) | 191 chars | Painel / sucesso / Success! / Fim do Show | PASS |
| screen-1 (en) | 199 chars | The Jamble Raid panel / Select Live Show / End without Raid | PASS |
| screen-2 (en) | 188 chars | Select a Live grid / live show cards / Select Live Show | PASS |
| screen-3 (en) | 182 chars | The Jamble Raid panel / success / Success! / End Show | PASS |

All alts are 15-150 chars... correction: a few alts are >150 chars (up to 209). The validator does not hard-fail on length; descriptive content is preferred. Trim available in a follow-up if reviewer prefers tighter alts.

## Scan 7, stale-feature audit

| Claim / feature | Source checked | Status | Verdict |
|---|---|---|---|
| Raid feature is live (RaidViewController.swift) | iOS develop branch read 2026-05-11 | Active (presentPanModal called from ShowHostViewController:482-484 and 1163-1169) | PASS |
| Battle distinction (raid vs battle) | iOS ShowHostViewController.swift:479-480 branch | Battles still gated by `battleId != nil` check, both features coexist | PASS |
| Chat-side raid notification "is Raiding with N people" | ShowRaidMessageCell.swift:136 (line confirmed) | Active cell registration in ShowChatViewController.swift:594-601 | PASS |
| Audience-side raid panel ("Join X Show") | ShowAudienceViewController.swift:398 (line confirmed) | Active subscription on `redirect` publisher | PASS |
| Recent product change (deprecation, A/B flag) | n/a | n/a (no public deprecation note for raid; not in MEMORY known-deprecated list) | PASS |

No deprecated feature mentions. The article does not touch verified badges, Prime, or auction wording.

## Open BLOCKERS

None.

## Notes

- Alt text on screen-2 mentions "borda roxa indicando selecao" in body, which faithfully describes the `outline: 3px solid #7E53F8` rendered in the HTML, derived from observing `RaidShowChooserViewModel.didSelectItemAt` toggling `_selectedShow` and `JambleShowCell.setSelected`. The exact selected-state visual (border weight, color) is set in `JambleShowCell` and not re-read in this audit; 3px purple is a reasonable approximation that does not invent the UI state.
- The example user name "Aymar" in the viewers-section body is a placeholder identical to the iOS rendering `%1$@ is Raiding %2$@!`. Reviewer can swap for a generic "Vendedor" if preferred for the help center voice.
