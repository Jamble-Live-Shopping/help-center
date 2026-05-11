# Content Audit, schedule-a-show (seller, intercom 14288114)

Date: 2026-05-08

## 7 scans

| Scan | Result |
|---|---|
| PII (no real names, emails, phones) | PASS, only generic example titles |
| Banned words (auction/leilao) | PASS, 0 occurrences in pt-br.md and en.md |
| Currency (R$ in pt-BR if prices, $ in EN, no R$ leak) | PASS, pt-BR has 1 R$ illustrative example ("Frete grátis acima de R$ 100"), EN body has 0 R$, EN uses "$20" with US format |
| Word diet (no jargon, no internal team names, no internal codenames) | PASS, no Wise / no internal names; uses plain seller language |
| Tone (humble, conversational, action-oriented, "você") | PASS, second-person throughout, direct CTAs, no corporate filler |
| Alt-text quality (15-150 chars, descriptive, mots-clés du H2) | PASS, all four alt texts 70-110 chars, describe the screen and selected state |
| Stale-feature audit | PASS, no deprecated features mentioned (no Verified badges, no Auction/Leilão wording, no Jamble Prime). Postpone limit (3, max_postpone_count) is current per Show.swift:92-93. icon-calendar asset is current per Assets.xcassets. |

## Editorial blockers

| Rule | pt-br | en |
|---|---|---|
| Zero em-dash (U+2014) | 0 | 0 |
| Zero en-dash (U+2013) | 0 | 0 |
| Zero auction / leilao | 0 | 0 |
| EN body zero R$ | n/a | 0 |
| pt-BR illustrative R$ allowed (one example in Notes/tips) | 2 (R$ 100 example x2 in tip + Notes section) | n/a |
| Description <= 140 chars | 113 | 112 |
| Title sans em-dash | OK ("Agendar um Show") | OK ("Schedule a Show") |

## Stale-feature audit table

| Claim / feature | Source checked | Status | Checked at | Owner | Verdict |
|---|---|---|---|---|---|
| Postpone Limit, max 3 | Show.swift:92-93 max_postpone_count: Int = 3 + xcstrings "Postpone Limit" present | active in code, asset present | 2026-05-08 | iOS | live_in_ios |
| Repeats: Day, Week, Month + After 1, 3, 5, 10 Shows, On Date | CreateShowDetailsViewController.swift:319-353 getRepeatUnitActions + getRepeatDateActions; RepeatContainerView wired | active in code | 2026-05-08 | iOS | live_in_ios |
| icon-calendar SVG asset | RESOURCES/Assets.xcassets/icon-calendar.imageset/icon-calendar.svg present | asset present | 2026-05-08 | iOS | live_in_ios |
| Schedule a Show entry from profile menu | ProfileViewController.swift:196-217 + JambleTabBarController.swift:356-436 openCreateShowVC | active in code | 2026-05-08 | iOS | live_in_ios |
| Profile gating: email, phone, address, payment | JambleTabBarController.swift:371-376 InfoManager.checkInfosAreNeeded | active in code | 2026-05-08 | iOS | live_in_ios |
| Unsplash photo picker | CreateShowCoverPhotoViewController.swift:50-53, 105-115 UnsplashPhotoPicker embedded | active in code | 2026-05-08 | iOS | live_in_ios |

## Verdict

Zero BLOCKER. Ship-ready.
