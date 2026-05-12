# Content Audit, referral-program-buyer

Date: 2026-05-11

## 7 scans

| Scan | Result |
|---|---|
| PII | PASS. Mock names only (Camila A., João F., Luiza M.) |
| Banned words (auction/leilão) | PASS, 0 occurrences |
| Currency (R$ in pt-BR, $ in EN) | PASS. pt-br has zero R$ amount tokens (intentional: amounts are API-driven and not in xcstrings, see code-audit). EN body has zero R$ leak. |
| Word diet (no jargon, no internal team names) | PASS |
| Tone (humble, conversational, buyer audience) | PASS |
| Alt-text quality | PASS. Three images, alt 15-150 chars, mentions screen name and main UI elements |
| Stale-feature audit | PASS, see below |

## Stale-feature audit

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Invite Friends entry in Profile | xcstrings line 12961-12975, ReferralView.swift in develop | active | 2026-05-11 | iOS | live_in_ios |
| Share Friends button | xcstrings line 21476-21490, ReferralView.swift:289-301 | active | 2026-05-11 | iOS | live_in_ios |
| I have a referral code link | xcstrings line 12294-12309, ReferralView.swift:303-313 | active | 2026-05-11 | iOS | live_in_ios |
| Redeem a code modal | DiscountCodeInputViewController.swift in develop, xcstrings line 18942-18957 | active | 2026-05-11 | iOS | live_in_ios |
| Phone verification gate before sharing | ReferralViewController.swift:93-117 | active | 2026-05-11 | iOS | live_in_ios |
| Ongoing / Past Referrals tabs | xcstrings line 16372-16387 and 17123-17138, ReferralInviteListView.swift | active | 2026-05-11 | iOS | live_in_ios |
| dias restantes countdown | xcstrings line 1459-1475 (`%lld dias restantes`) | active | 2026-05-11 | iOS | live_in_ios |
| Concluído / Prazo perdido statuses | xcstrings line 7204 and 8350-8367, ReferralInviteListView.swift:181-187 | active | 2026-05-11 | iOS | live_in_ios |
| Welcome credit on redemption | session memory (referral rules since 2026-03-04), product status | active | 2026-05-11 | product (Aymar) | product_confirmed |
| Reward on first friend purchase at a Show | session memory (referral rules since 2026-03-04), product status | active | 2026-05-11 | product (Aymar) | product_confirmed |
| Seller-side referral cross-link | articles/referral-program/ exists and is v2-merged | active | 2026-05-11 | help-center | live_in_backend |
| No verified badges (deprecated 2026-04-28) | grep `Rising|Elite|Ultra|Parceiro|Partner` in pt-br.md and en.md returns 0 | not referenced | 2026-05-11 | product | deprecated |
| No auction/leilão wording | grep `auction|leil[aã]o` returns 0 | not referenced | 2026-05-11 | legal | deprecated |
| No Jamble Prime mention | grep `Prime|prime` returns 0 (only legitimate words like "primeira") | not referenced | 2026-05-11 | product | deprecated |

No deprecated UI surfaces referenced. The article does NOT mention:
- Verified badges (deprecated 2026-04-28)
- Auction / Leilão wording
- Jamble Prime (stopped Jan 2026)

## Editorial bloquants

| Rule | pt-br | en |
|---|---|---|
| Zero em-dash (U+2014) | 0 | 0 |
| Zero en-dash (U+2013) | 0 | 0 |
| Zero auction/leilão | 0 | 0 |
| EN body zero R$ | n/a | 0 |
| pt-BR R$ token count | 0 (intentional, see currency_required: false in flow.yml) | n/a |
| Description ≤140 chars | 109 | 99 |
| Title sans em-dash | OK | OK |
| H1 count | 1 | 1 |

## Verdict

Zero BLOCKER. Ship-ready. The intentional zero-R$ choice is documented
in the code-audit and the flow.yml header, and `currency_required` is
explicitly set to false for this article.
