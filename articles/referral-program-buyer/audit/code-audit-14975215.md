# Code Audit, referral-program-buyer (intercom_id 14975215)

Date: 2026-05-11
Source iOS: Jamble-iOS develop, verified at `/Users/aymardumoulin/Projects/Jamble-iOS/Jamble`
Source backend: not accessed in this v2 rerun (negative-scan applied to amounts).

## Negative scan, money amounts

The brief and session memory cite R$30/R$30 (sender/receiver) for the
buyer referral. xcstrings is the v2 source of truth for any user-facing
string and number. Direct grep:

```bash
grep -E "R\\\$|R\$\\s*[0-9]+|\$[0-9]+" \\
  /Users/aymardumoulin/Projects/Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings
```

returns no R$ amount key tied to the referral flow. The only $-prefixed
string is `⬆️ Get $10 to spend when signing in with this invite code`,
which is a marketing teaser, not the canonical amount.

iOS surface for the referral (`DISCOUNT/Views/ReferralView.swift:233,
267`) renders amounts dynamically with `Text("$\(amount) pending")` and
`Text("$\(amount) earned")`, where `amount` comes from
`repository.profile.getReferralSetting(type:)`. The values are therefore
controlled by the backend at runtime.

Verdict: amount is NOT in xcstrings. Per the brief (rule 6: "Do not
invent amounts"), the body of pt-br.md and en.md does NOT quote a fixed
R$ value. Mockups show illustrative `$` totals consistent with the iOS
UI source. If the team later decides to lock the R$ figure into the
article, the path is to ship the figure through xcstrings (so it shows
on the user's screen and can be cited by the article) or to update this
audit with the explicit decision and the source.

## Article claim vs source code

| Article claim | Source | Verdict |
|---|---|---|
| Profile has an Invite Friends entry | xcstrings `Invite Friends` -> `Convidar amigos` (translated, line 12961-12975) | MATCH |
| Invite Friends screen shows program steps | `ReferralView.swift:86-127` stepsSection | MATCH |
| Screen has a reward section | `ReferralView.swift:129-163` rewardSection | MATCH |
| Primary CTA labelled Share Friends / Compartilhar amigos | xcstrings `Share Friends` -> `Compartilhar amigos` (line 21476-21490), `ReferralView.swift:289-301` inviteButton | MATCH |
| Secondary link labelled I have a referral code / Tenho um código de convite | xcstrings `I have a referral code` -> `Tenho um código de convite` (line 12294-12309), `ReferralView.swift:303-313` redeemCodeButton | MATCH |
| Ongoing Referrals tile / Referências contínuas | xcstrings `Ongoing Referrals` -> `Referências contínuas` (line 16372-16387), `ReferralView.swift:214-254` | MATCH |
| Past Referrals tile / Referências anteriores | xcstrings `Past Referrals` -> `Referências anteriores` (line 17123-17138), `ReferralView.swift:256-286` | MATCH |
| Past Referrals shows totals with $ symbol | `ReferralView.swift:233` `$\(amount) pending`, `:267` `$\(amount) earned` | MATCH |
| `dias restantes` countdown for ongoing referrals | xcstrings `%lld days Left` -> `%lld dias restantes` (line 1459-1475) | MATCH |
| Completed status / Concluído | xcstrings `Completed` -> `Concluído` (line 7204), `ReferralInviteListView.swift:181-183` | MATCH |
| Deadline Missed / Prazo perdido | xcstrings `Deadline Missed` -> `Prazo perdido` (line 8350-8367), `ReferralInviteListView.swift:184-187` | MATCH |
| Redemption surface titled Redeem a code / Resgatar um código | xcstrings `Redeem a code` -> `Resgatar um código` (line 18942-18957), `DiscountCodeInputViewController.swift:47` `navigationLabel.text = "Redeem a code"` | MATCH |
| Redemption field placeholder Enter your code.... / Digite seu código.... | xcstrings `Enter your code....` -> `Digite seu código....` (line 9900-9914), `DiscountCodeInputViewController.swift:70` | MATCH |
| Redemption CTA labelled Redeem / Resgatar | xcstrings `Redeem` -> `Resgatar` (line 18926-18941), `DiscountCodeInputViewController.swift:77` | MATCH |
| Code Redeemed confirmation / Código Resgatado | xcstrings `Code Redeemed` -> `Código Resgatado` (line 6843-6859) | MATCH |
| Phone verification gate before sharing | `ReferralViewController.swift:93-117` `openRedeemCode()` branches on `PhoneVerificationViewController(context: .redeemCode)` and xcstrings `Before you invite friends, we need to verify your phone number for security.` | MATCH |
| Trigger = friend completes 1 item purchase at a Show | session memory + product status (Aymar) | UNVERIFIABLE in iOS code (backend-controlled), kept as documented program rule, not a strict UI claim |
| New accounts only / no limit on referrals | session memory + product status (Aymar) | UNVERIFIABLE in iOS code (backend-controlled). Kept as documented program rule. |
| Credits scoped to Shows | session memory + product status (Aymar) | UNVERIFIABLE in iOS code (backend-controlled). Kept as documented program rule. |
| Seller does not see the referral attribution | session memory + product privacy stance | NO contradicting iOS string. Treated as privacy stance, audit flag for review. |

## Verdict

Zero MISMATCH against iOS code. Three buyer-program rules (trigger,
eligibility, scope) live backend-side and could not be re-verified in
this v2 rerun without backend access. They are documented as rules, not
as UI claims, and match the existing program operation since 2026-03-04.

If those rules change before this article ships, the body sections
"How the program works" and "How credits work" must be re-audited.
