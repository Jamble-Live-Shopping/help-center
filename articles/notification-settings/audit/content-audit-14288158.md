# Content audit, article 14288158 (notification-settings)

Date: 2026-05-06

## 1. PII / sensitive data
- No real names, emails (other than support@jambleapp.com), phone numbers, tokens, IDs.
Verdict: PASS.

## 2. Banned words (auction / leilao)
- 0 occurrences in pt-br.md and en.md.
Verdict: PASS.

## 3. Currency
- Article does not document prices. `flow.yml.currency_required: false`. 0 R$ in en.md, 0 $ in pt-br.md.
Verdict: PASS.

## 4. Word diet
- pt-br.md and en.md follow the same H2 structure (verified by `grep -c "^## "`).
- Sentences are short and action-oriented.
Verdict: PASS.

## 5. Tone
- Direct address (você / you), action-oriented.
- The known English-section-titles limitation is surfaced upfront in the body, not buried.
Verdict: PASS.

## 6. Alt text quality

| Image | Alt text content | Verdict |
|---|---|---|
| notifications-list pt-br | names the screen and the 4 section titles + parent toggles | PASS |
| notifications-list en | mirror | PASS |
| permission-sheet pt-br | names the iOS push permission prompt and the call to action | PASS |
| permission-sheet en | mirror | PASS |

Validator confirms all alt strings fall in the 15-150 char band.

Verdict: PASS.

## 7. Stale-feature audit

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Notifications screen under Settings > Account | PROFILE/ProfileSettings/Notifications/NotificationsViewController.swift | live | 2026-05-06 | Aymar | live_in_ios |
| 4 collapsible category sections with parent toggle | PROFILE/ProfileSettings/Notifications/View/NotificationsView.swift:64-86 | live | 2026-05-06 | Aymar | live_in_ios |
| iOS push-permission prompt sheet | PROFILE/ProfileSettings/Notifications/View/NotificationPermissionSheet.swift | live | 2026-05-06 | Aymar | live_in_ios |
| Permission-sheet copy (title, body, CTA) | xcstrings | live | 2026-05-06 | Aymar | live_in_ios |
| Section titles render English on pt-BR | NotificationsView.swift:104, xcstrings absence | live (known limitation) | 2026-05-06 | Aymar | live_in_ios |
| Push only (no email / banner) | flow.yml.must_not_say documents this; iOS surface confirms | confirmed | 2026-05-06 | Aymar | product_confirmed |

Verdict: PASS. 5 of 6 items live_in_ios with verified file paths, 1 product_confirmed.

## 8. Manual visual review (procedure-compliance check #15)

Mockups use neutral backgrounds and the iOS-style toggle component from the design system. No cartoon emoji, no big-text product placeholder, no facial features.

Verdict: PASS.

## Result

8 SCANS pass. Zero BLOCKER. Article is content-quality ready for review.
