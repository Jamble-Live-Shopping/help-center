# Content audit, intercom_id=14288169 (direct-messages-for-sellers)

Checked on 2026-11-13 on `pt-br.md`, `en.md`, `metadata.yml` and the `activity-tabs` mockup pair.

## Scan 1, PII

No user names, emails, phone numbers or IDs. Mockup names (Lucas Cards, Marina TCG, Rafa Colecionáveis) are invented samples on neutral avatar swatches. The only email is the public support address. PASS.

## Scan 2, banned words and internal info

- `auction` / `leilão`: 0 in both locales
- No code paths, flags, ticket numbers, team names, thresholds, rate limits or moderation criteria in the body. The old FAQ describing a per-conversation message rate was removed (it was wrong for DMs and exposed an internal limit). Internal sending limits are not mentioned.
- No rule that applies only to some sellers.

PASS.

## Scan 3, currency

The article quotes no prices. `R$` count 0 in both locales, `$` count 0. `currency_required: false`. PASS.

## Scan 4, word diet and dashes

- Em dashes: 0 in pt-br.md, 0 in en.md (13 and 14 before)
- En dashes: 0
- Mid-sentence " - ": 0
- Descriptions: pt-BR 133 chars (was empty), EN 122 chars (was 250)
- pt-BR rewritten with correct accents (the old body had none: "voce", "nao", "transacao")

PASS.

## Scan 5, tone

Plain pt-BR, second person, short sentences, no jargon. EN mirrors pt-BR section by section; the only intentional divergence is the note that the iPhone archived filter reads "Concluído" in Portuguese, kept in EN because the label differs by app language. PASS.

## Scan 6, alt-text quality

| Image | Alt (pt-BR) | Length | Verdict |
|---|---|---|---|
| activity-tabs pt-BR | Tela Atividade com os filtros Todos, Mensagens e Não lido e a lista de conversas com uma conversa não lida destacada | 116 | PASS |
| activity-tabs EN | Activity screen with the All, Messages and Unread filters and the conversation list with one unread conversation highlighted | 124 | PASS |

Each image sits under the H2 "Onde encontrar suas mensagens", with an intro sentence, a caption with bold UI elements and a follow-up list.

## Scan 7, stale-feature audit

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Activity tab with six filters (incl. Mensagens) | iOS 5.11 `ActivityType.swift`, Android v5.11.0 `ActivityType.kt` | live | 2026-11-13 | Claude for Vaimiti | live_in_ios |
| Search in Activity | iOS 5.11 `ActivityListViewController.swift`, Android `MessageSearchScreen`, backend main `search_group_messages_route` | live | 2026-11-13 | Claude for Vaimiti | live_in_ios |
| Message button on profiles | iOS `ProfileHeaderViewController.swift`, Android `ProfileActions.kt` | live | 2026-11-13 | Claude for Vaimiti | live_in_ios |
| Message the seller from a shop product | backend main `product_options.py`, iOS `ProductProfileSection.swift`, Android `ProductSellerSection.kt` | live | 2026-11-13 | Claude for Vaimiti | live_in_backend |
| Offer creates or reuses the product thread | backend main `purchase_intent_service.py` | live | 2026-11-13 | Claude for Vaimiti | live_in_backend |
| Order thread after every sale | backend main `transaction.py`, `message_service.py` | live | 2026-11-13 | Claude for Vaimiti | live_in_backend |
| 500 characters, 6 / 10 photos | iOS `MessageViewModel.swift`, `MessageViewController.swift`; Android `MessageInput.kt` | live | 2026-11-13 | Claude for Vaimiti | live_in_ios |
| Archive / unarchive | iOS context menu, Android swipe row | live | 2026-11-13 | Claude for Vaimiti | live_in_ios |
| Delete own message (removed from thread) | iOS `MessageViewModel.swift`, Android `MessageScreen.kt` | live | 2026-11-13 | Claude for Vaimiti | live_in_ios |
| Read icon | iOS `MessageStatusRowView.swift`, Android `MessageBubbles.kt` | live | 2026-11-13 | Claude for Vaimiti | live_in_ios |
| Push per message, "Te enviou uma foto" | backend main `send_new_message_notification` | live | 2026-11-13 | Claude for Vaimiti | live_in_backend |
| Mensagens notification toggle | backend main `get_notification_settings` | live | 2026-11-13 | Claude for Vaimiti | live_in_backend |
| Personal data / off-platform / offensive messages blocked | backend main `send_message` moderation + `error_codes.py` public messages | live | 2026-11-13 | Claude for Vaimiti | live_in_backend |
| Block from profile | backend main `user_options.py` | live | 2026-11-13 | Claude for Vaimiti | live_in_backend |
| "Mensagem cancelada" placeholder after delete | iOS 5.11 removes the message; no such label | removed from article | 2026-11-13 | Claude for Vaimiti | deprecated |
| Per-conversation DM rate limit FAQ | limit does not apply to DMs | removed from article | 2026-11-13 | Claude for Vaimiti | deprecated |

No deprecated feature remains in the body (no verified badges, no Jamble Prime, no auction wording).

## BLOCKERS found
- (none)
