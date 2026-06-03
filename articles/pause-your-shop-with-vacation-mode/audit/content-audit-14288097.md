# Content audit, article 14288097 (pause-your-shop-with-vacation-mode)

Date: 2026-05-06

## 1. PII / sensitive data

- No real user names. No emails other than support@jambleapp.com.
- No phone numbers, no tokens, no IDs.

Verdict: PASS.

## 2. Banned words (auction / leilao)

- 0 occurrences in pt-br.md and en.md.

Verdict: PASS.

## 3. Currency

- Article does not document prices. `flow.yml.currency_required: false`.
- 0 R$ in en.md, 0 $ in pt-br.md.

Verdict: PASS.

## 4. Word diet

- pt-br.md and en.md follow the same H2 structure (verified by `grep -c "^## "`).
- Sentences are short and action-oriented; no filler paragraphs.
- Tips section uses single-line bullets.

Verdict: PASS.

## 5. Tone

- Direct address to the seller (você / you).
- No condescension, no buildup before sections.
- Action-oriented (matches Jamble voice).

Verdict: PASS.

## 6. Alt text quality

| Image | Alt text content | Verdict |
|---|---|---|
| settings-vacation-cell pt-br | names the Sell section and the Vacation mode row | PASS |
| settings-vacation-cell en | mirror | PASS |
| vacation-modal-on pt-br | names the confirmation sheet, the warning copy, and the Ativar button | PASS |
| vacation-modal-on en | mirror with Turn On button | PASS |

Validator (`alt_text_too_short` / `alt_text_too_long`) confirms all alt strings fall in the 15-150 char band.

Verdict: PASS.

## 7. Stale-feature audit

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Vacation mode cell in Sell section | PROFILE/ProfileSettings/ProfileSettingsV2ViewController.swift:48 | live | 2026-05-06 | Aymar | live_in_ios |
| Confirmation modal opens on tap | PROFILE/ProfileSettings/ProfileSettingsV2ViewController.swift:738 | live | 2026-05-06 | Aymar | live_in_ios |
| pt-BR label "Modo de férias" | xcstrings | live | 2026-05-06 | Aymar | live_in_ios |
| ON modal copy | xcstrings | live | 2026-05-06 | Aymar | live_in_ios |
| OFF modal copy | xcstrings | live | 2026-05-06 | Aymar | live_in_ios |
| Ativar / Desativar buttons | xcstrings | live | 2026-05-06 | Aymar | live_in_ios |
| Effect is immediate, no delay | ProfileBuilder PATCH at :764, no deferred logic | confirmed | 2026-05-06 | Aymar | product_confirmed |

Verdict: PASS. 6 of 7 items live_in_ios with verified file paths, 1 product_confirmed (negative claim about absence of deferred logic).

## 8. Manual visual review (procedure-compliance check #15)

Mockups use neutral photo-style backgrounds with abstract icons and meta lines. No cartoon emoji, no big-text product placeholders, no facial features. Aligned with `process/12-procedure-compliance.md` check #15.

Verdict: PASS.

## Result

8 SCANS pass. Zero BLOCKER. Article is content-quality ready for review.
