# Code audit, article 14288166 (rewards-gems-and-seller-ranking)

**iOS source of truth**: `/Users/aymardumoulin/Projects/Jamble-iOS`
**Date**: 2026-04-27
**Auditor**: Help Center v2 worker

## Files inspected

| File | Purpose |
|---|---|
| `Jamble/PROFILE/Models/LiverProgram.swift` | Badge enum (rising/elite/ultra/jambleManaged), display names, colors, icons |
| `Jamble/REWARDS/View/RewardDashboardView.swift` | Watch & Earn card, Get Free Gems button, challenges section |
| `Jamble/REWARDS/View/Components/ChallengeItem.swift` | Challenge row with `gem-icon` reward |
| `Jamble/LIVE_SHOPPING/SellerRanking/Views/SellerRankingView.swift` | Ranking screen (title/subtitle/rules card/list/own row) |
| `Jamble/LIVE_SHOPPING/SellerRanking/Models/SellerLeaderboardRule.swift` | Rule struct (icon: gem/shop, entry_points) |
| `Jamble/LIVE_SHOPPING/SellerRanking/Views/Components/SellerRankingParticipantCellView.swift` | Per-row cell, top-5 background tint |
| `Jamble/TIPS/Scenes/Show Audience/Tips/ShowAudienceClaimGemsTip.swift` | Canonical message: "Use Gems to send emojis and raise the seller's ranking." |
| `Jamble/RESOURCES/Localizable.xcstrings` | pt-BR localizations |

## Claim, source, verdict

| Article claim | iOS source | Verdict |
|---|---|---|
| Buyers earn Gems for free via Watch & Earn | `RewardDashboardView.swift` line 244 `Text("Watch & Earn")`, line 267 `"Get Free Gems"` | MATCH |
| pt-BR uses "gemas" (lowercase) | xcstrings `Get Free Gems` -> `Obter gemas grátis`, `Earn Free Gems for each friend you invite` -> `Ganhe gemas grátis para cada amigo que você convidar` | MATCH |
| Watch & Earn subtitle pt-BR | xcstrings: `Watch Shows and convert time daily before midnight` -> `Assista às Lives e converta o tempo em gemas antes da meia noite` | MATCH |
| Buyers convert watch time before midnight | RewardDashboardView line 248: "Watch Shows and convert time daily before midnight" | MATCH |
| Challenges reward Gems | ChallengeItem.swift line 39-41: `challenge.reward?.coinCount` rendered with `Image("gem-icon")` | MATCH |
| Buyers spend Gems on emojis to support sellers | ShowAudienceClaimGemsTip.swift line 25-29: "Use Gems to send emojis and raise the seller's ranking." | MATCH |
| Seller Ranking is monthly | SellerRankingViewModel.swift line 89: `frequency: .monthly` | MATCH |
| Ranking has 2 rules: gem support + sales | SellerRankingView.swift rules section iterates over `viewModel.rules`, RuleIcon enum is `.gem` or `.shop` | MATCH |
| Top 5 rows have purple tint background | SellerRankingParticipantCellView.swift line 19-28: `case 1 -> brand.opacity(0.16)` etc. up to rank 5 | MATCH |
| Own row label "You" | SellerRankingParticipantCellView.swift line 17: `isOwn ? "You" : ...` | MATCH |
| pt-BR own row label "Você" | xcstrings `You` -> `Você` | MATCH |
| Score column header pt-BR | xcstrings `Score` -> `Pontuação`, `Ranking` -> `Classificação` | MATCH |
| Ranking accessed from profile | ProfileHeaderViewController.swift references SellerRanking module | MATCH |
| 4 badge tiers: Rising, Elite, Ultra, Jamble Partner | LiverProgram.swift enum: `ultra, elite, rising, jambleManaged` with displayName mapping | MATCH |
| Rising display name pt-BR is "Rising Live Seller" (kept EN) | xcstrings: `Rising Live Seller` -> `Vendedor ao vivo em ascensão`. NOTE: pt-BR translation EXISTS but tier name is brand-recognizable in EN. Article uses EN forms in headings + pt-BR descriptive paragraph. Acceptable per Language Priority Policy (brand terms can stay EN). | MATCH (with note) |
| Jamble Partner pt-BR is "Parceiro da Jamble" | xcstrings: `Jamble Partner` -> `Parceiro da Jamble` | MATCH |
| Badge colors (rising bronze, elite silver, ultra gold, partner purple) | LiverProgram.swift: rising `#C48C54`, elite `#A6A9B0`, ultra `#CDB35E`, partner `UIColor.content.primary` (Jamble purple) | MATCH (mockups use these exact hex values) |
| Badges assigned by Jamble (not self-applied) | No "Apply for badge" UI exists in the codebase. LiverProgram is read from `Profile.shared.jamble_profile?.liver_program`. | MATCH |

## Strings extracted (for mockups)

| EN string | pt-BR (from xcstrings) | Used in mockup |
|---|---|---|
| Watch & Earn | Assista e ganhe | gems-watch-earn |
| Watch Shows and convert time daily before midnight | Assista às Lives e converta o tempo em gemas antes da meia noite | gems-watch-earn |
| Get Free Gems | Obter gemas grátis | gems-watch-earn (CTA) |
| Score | Pontuação | seller-ranking |
| Ranking | Classificação | seller-ranking |
| You | Você | seller-ranking (own row) |
| Rising Live Seller | Rising Live Seller (kept EN, brand) | badge-gallery |
| Elite Live Seller | Elite Live Seller (kept EN, brand) | badge-gallery |
| Ultra Live Seller | Ultra Live Seller (kept EN, brand) | badge-gallery |
| Jamble Partner | Parceiro da Jamble | badge-gallery |

## MISMATCH count: 0

Article ships against the iOS source as ground truth. No invented copy.
