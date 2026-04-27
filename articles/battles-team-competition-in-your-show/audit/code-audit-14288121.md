# Code audit, article 14288121 (battles-team-competition-in-your-show)

Date: 2026-04-27
Source: `Jamble-iOS` repo, branch `develop` at audit time

## Claims vs source

| Article claim | iOS source | Verdict |
|---|---|---|
| Battle starts via picker on host show controls | `ShowHostViewController.swift` L1265-1295, presents `UIAlertController` with `payload.durations_in_mins` | MATCH |
| Duration options come from server payload (not hardcoded 30/60/90/120) | Same, durations_in_mins iterated dynamically | MATCH (v1 mockup was wrong, fixed in v2 to native alert) |
| Cancel button on duration picker | Same, `String(localized: "Cancel")` action | MATCH |
| Welcome screen shows "Welcome to the Battle!" | `ShowBattleWelcomeView.swift` L20, titleLabel = `String(localized: "Welcome to the Battle!")` | MATCH (pt-BR `Bem-vindo à batalha!` from xcstrings) |
| Welcome eyebrow "Battle starts Now!" | Same, `setTitle(String(localized: "Battle starts Now!"))` on container | MATCH (pt-BR `A batalha começa agora!`) |
| "You've joined the team" + team icon | Same, `teamIndicatorLabel.text = String(localized: "You’ve joined the team")` | MATCH (pt-BR `Você se juntou à equipe`) |
| "Your score: 0" pill | Same, `setTitle(String(localized: "Your score: "))` | MATCH (pt-BR `Sua pontuação:`) |
| "View battle rules" CTA | Same, `setTitle(String(localized: "View battle rules"))` | MATCH (pt-BR `Exibir regras de batalha`) |
| Progress bar component, red/blue split bars | `ShowBattleProgressBar.swift` L18-56, two UIViews with team1/2Color, white labels | MATCH |
| Red team color #FF2867 | `Battle.swift` L70, `case .red: return UIColor.rgba(255, 40, 103, 1)` | MATCH |
| Blue team color #368AFF | `Battle.swift` L71, `case .blue: return UIColor.rgba(54, 138, 255, 1)` | MATCH |
| "See Ranking" button | `ShowBattleViewController.swift` L100, `setTitle(String(localized: "See Ranking"))` | MATCH (pt-BR `Ver classificação`) |
| Timer icon + label | Same L74-87, clock icon with `icon-clock` and timer label, white text | MATCH |
| Battle ended view background #0C131D | `ShowBattleEndedView.swift` L138, `backgroundColor = UIColor(hex: "0C131D")!` | MATCH |
| "Claim Your Rewards!" title | Same L41, `text = "Claim Your Rewards!"` (literal not xcstring) | MATCH (pt-BR `Solicite suas recompensas!` from xcstrings) |
| "Claim" button | Same L72, `text = "Claim"` | MATCH (pt-BR `Reivindicar`) |
| Top 3 winners podium | Same `getWinner(position:)` referenced at end of file, builds vStackView per position | MATCH (visual approximation in mockup) |
| Battle tier system (Bronze R$25 / Silver R$50 / Gold R$200) | Server-driven via `payload.title`/`description` on alert + reward amounts on claim | NOT IN CLIENT (rules live server-side, claims documented from product spec discussed 2026-04-27) |

## Visual fidelity check

Side-by-side vs simulator: not done in this iteration (iOS simulator not booted). Mockups built from code reading + design system (`design-system.md`).

Color tokens used in HTML:
- Brand purple `#7E53F8` (CTA buttons, score pill)
- Red team `#FF2867` (rgba 255,40,103)
- Blue team `#368AFF` (rgba 54,138,255)
- Dark bg `#0C131D` (welcome + ended background)
- Gold accent `#FFD15A` (rewards star, top 1 border)

## Open MISMATCH

None.

## Notes

- Tier system content (Bronze/Silver/Gold thresholds) is product-spec, not extractable from iOS source. Trust source: thread on 2026-04-27 with the agreed thresholds (3 best lives 600/12h, 5 best lives 1400/40h, recalc on best lives 14d, 30+ min only).
- Battle widget mockup is a focused render of the in-show overlay component (progressBar + topInfoStackView from `ShowBattleViewController`). Not a full live-show capture.
- Welcome avatar uses a fallback initial since the iOS view binds a remote profile image; mockup uses a styled circle with letter A.
