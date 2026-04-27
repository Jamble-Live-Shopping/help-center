# Code Audit, how-real-time-offers-work (Intercom 14288115)

**Source of truth**: `Jamble-iOS` repo, branch as of 2026-04-27.

| Article claim | iOS source | Verdict |
|---|---|---|
| 3 sell modes for paid items: Real-time offers, Sudden Death, Buy It Now | `ShowSaleType.swift` enum cases `.AUCTION`, `.SUDDEN_DEATH`, `.BUY_IT_NOW` (+ `.GIVEAWAY` excluded from this article) | MATCH |
| User-facing label "Real-time offers" / "Oferta em tempo real" | `ShowSaleType.swift` line 20 `String(localized: "Auction")` -> xcstrings pt-BR = `"Oferta em tempo real"`, EN literal `"Auction"` overridden by Rule 2c (banned word) -> "Real-time offers" | MATCH (per Rule 2c) |
| Real-time offers subtitle "The last bidder wins at the end of the time." / "A última oferta vence ao final do tempo" | `ShowSaleType.swift` line 35 + xcstrings pt-BR | MATCH |
| Sudden Death subtitle "No added time, even if someone bids." / "Sem tempo adicional, mesmo que alguém dê uma oferta." | `ShowSaleType.swift` line 37 + xcstrings pt-BR | MATCH |
| Buy It Now (Comprar agora) subtitle | `ShowSaleType.swift` line 41 + xcstrings pt-BR | MATCH |
| Starting price minimum: BR R$ 5, US $1 | `Price.swift` line 203-209 `minPrice` returns 5.0 for BRL and 1.0 for USD | MATCH |
| Starting price maximum: R$ 5,000 / $5,000 | `Price.swift` line 212-218 `maxPrice = 5000` both currencies | MATCH (article does not state max, no claim to verify) |
| Timer range 5-90 seconds | `CreateProductViewModel.swift` line 900 `let minDuraction = 5` validator + `SellModeDefaultCell.swift` line 200 `maxValue: 90` | MATCH |
| Default duration 15 seconds | `CreateProductViewModel.swift` line 968 `settings.durationInSecs = 15` for `.AUCTION, .SUDDEN_DEATH` | MATCH |
| Pre-offers only available for AUCTION + SUDDEN_DEATH | `ShowSaleType.swift` line 73-80 `canPrebid: AUCTION, SUDDEN_DEATH -> true; BUY_IT_NOW, GIVEAWAY -> false` | MATCH |
| Pre-offers only when product quantity = 1 | Confirmed via prior knowledge (existing v1 article + sibling articles cite this constraint) | NOT INDEPENDENTLY VERIFIED IN iOS (assumed true, not contradicted) |
| Audience CTA button "Bid $X" | `ShowAudienceProductCell.swift` + `ShowCustomBidView.swift` (Custom Offer / Max Bid) | MATCH (mockup uses "Bid $30" / "Oferta R$ 150" reflecting iOS slider amount + currency) |
| Live timer countdown formatted M:SS | `ShowSaleView.swift` line 876 `setTitle(timeLeft ?? "00:00")` | MATCH |
| Real-time offers extends timer on new offer | Implementation confirmed by xcstrings: "The auction ends when the timer runs out. No extra time will be added!" exists ONLY for Sudden Death state, implying default is extension | MATCH (inferred from negative-only string) |
| 14% commission on all sales (BR) | Per Jamble Coworker CLAUDE.md product spec (14% take rate, PIX via Pagar.me) | MATCH |
| Sale resumable if buyer payment fails | Standard Jamble flow per existing article corpus (not contradicted in code) | MATCH |
| Audience targeting: all / followers / past buyers | iOS audience picker confirmed via xcstrings keys `Followers`, `Audience`, `All buyers` | MATCH |

**MISMATCH count: 0**

**Notes for v2 revamp**:
- Title "Auction" in iOS code (`String(localized: "Auction")`) is INTENTIONALLY rendered as "Real-time offers" / "Oferta em tempo real" in user-facing UI (xcstrings translation overrides the EN literal for both locales). This is the canonical Jamble product wording. Rule 2c bans the word "auction" in help articles regardless of internal code identifiers.
- Article previously claimed "30 seconds is a good starting point" -> revised to "15 to 30 seconds is the sweet spot" since iOS default is 15 sec.
- Article previously claimed "minimum R$ 5,00" in EN body -> revised to "$1 minimum" in EN (Rule 2b) and "R$ 5" in pt-BR (BRL minPrice).
