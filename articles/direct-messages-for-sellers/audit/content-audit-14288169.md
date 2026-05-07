# Content audit, article 14288169 (direct-messages-for-sellers)

Date: 2026-05-06

## 1. PII / sensitive data
- No real names. Mockup handles (@cardstack_br, @maria_pokemon, @diecast_lover) are synthetic.
- No emails other than support@jambleapp.com.
Verdict: PASS.

## 2. Banned words (auction / leilao)
- 0 occurrences in pt-br.md and en.md.
Verdict: PASS.

## 3. Currency
- Article does not document prices. `flow.yml.currency_required: false`. 0 R$ in en.md, 0 $ in pt-br.md.
Verdict: PASS.

## 4. Word diet
- pt-br.md and en.md follow the same H2 structure (verified by `grep -c "^## "`).
- Sentences are short, action-oriented.
Verdict: PASS.

## 5. Tone
- Direct address to the seller (você / you).
- Action-oriented bullets in the Tips section.
- The "out of scope" surfaces are documented in the audit, not in the body, so the body stays focused.
Verdict: PASS.

## 6. Alt text quality

| Image | Alt text content | Verdict |
|---|---|---|
| activity-tabs pt-br | names the screen, the 6 sub-tab filters, and the conversation list | PASS |
| activity-tabs en | mirror | PASS |
| profile-message-cta pt-br | names the buyer profile and the Follow / Mensagem buttons | PASS |
| profile-message-cta en | mirror | PASS |

Validator confirms all alt strings fall in the 15-150 char band.

Verdict: PASS.

## 7. Stale-feature audit

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Activity tab is the entry point for buyer messages | ACTIVITY/ActivityPage/Views/ActivityViewController.swift | live | 2026-05-06 | Aymar | live_in_ios |
| 6 sub-tabs: All / Messages / Unread / Purchases / Sales / Archived | ACTIVITY/ActivityList/Models/ActivityListTab.swift:12-17 | live | 2026-05-06 | Aymar | live_in_ios |
| pt-BR labels Todos / Mensagens / Não lido / Compras / Vendas / Concluído | xcstrings | live | 2026-05-06 | Aymar | live_in_ios |
| Profile Message CTA button | xcstrings "Message" -> "Mensagem" | live | 2026-05-06 | Aymar | live_in_ios |
| Push notifications via Activity category | cross-article (notification-settings) | confirmed | 2026-05-06 | Aymar | product_confirmed |

Verdict: PASS. 4 of 5 items live_in_ios with verified file paths, 1 product_confirmed.

## 8. Manual visual review (procedure-compliance check #15)

Mockups use neutral avatars with gradient fills, no facial features, no cartoon emoji, no big-text product placeholder.

Verdict: PASS.

## Result

8 SCANS pass. Zero BLOCKER. Article is content-quality ready for review.
