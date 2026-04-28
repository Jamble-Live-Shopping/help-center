# Compliance gate, article 14288166

Last updated: 2026-04-28

## Update history
- 2026-04-27: v2 revamp shipped (PR #52)
- 2026-04-27: real iOS PNG assets used for badges + gems (PR #63)
- **2026-04-28: Verified badges deprecated** (Aymar feedback). Removed all badge content from body, deleted `badge-gallery` mockup (HTML + PNGs). Article now scoped to Gems + Seller Ranking only.

## Checklist

| # | Check | Status |
|---|---|---|
| 1 | Description ≤ 140 chars (Rule 1) | PASS |
| 2 | Zero non-BR examples (Rule 2) | PASS |
| 3 | Currency localized (Rule 2b) | N/A (no R$ amounts in body) |
| 4 | Zero auction/leilão (Rule 2c) | PASS |
| 5 | Zero em-dashes / en-dashes (Rule 0) | PASS |
| 6 | pt-BR primary, EN 1:1 mirror (Rule 7) | PASS |
| 7 | Every image has descriptive alt text | PASS (2 images: gems-watch-earn + seller-ranking) |
| 8 | Every image wrapped in H2 + intro + caption (Step 9) | PASS |
| 9 | PNGs at retina DPR 3 | PASS (all 4 PNGs are 960px wide) |
| 10 | PNGs hosted on `Jamble-Live-Shopping/help-center` raw URL | PASS |
| 11 | `__v2` suffix on all PNGs | PASS |
| 12 | iOS code is the source of truth | PASS (gems + ranking from `RewardDashboardView.swift`, `SellerRankingView.swift`) |
| 13 | xcstrings pt-BR pulled for every EN string | PASS |
| 14 | No deprecated features mentioned | **PASS as of 2026-04-28** (badges removed) |
| 15 | TOC if ≥ 6 H2 sections (Rule 4) | OUT OF SCOPE (corpus-wide pass deferred) |
| 16 | code-audit present, zero MISMATCH | PASS |
| 17 | content-audit present, zero BLOCKERS | PASS |

## Mockups (post-deprecation)

| Mockup | Purpose |
|---|---|
| gems-watch-earn | Rewards screen showing Watch & Earn pedagogy |
| seller-ranking | Monthly leaderboard with point rules + Você highlight |
| ~~badge-gallery~~ | **DELETED 2026-04-28** (badges deprecated) |

## Verdict

**SHIP**, all enforced checks PASS.
