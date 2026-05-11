# Compliance audit, intercom_id=14288117 (invite-a-co-host-live-duo)

Scope: process/12-procedure-compliance.md, 18 checks. PR #91 + PR #92 hard contracts also verified below.

| # | Check | Status | Notes |
|---|---|---|---|
| 1 | pt-br.md present, single H1, valid headings | PASS | 1 H1 "Convidar um co-host (Live Duo)" + H2 sections |
| 2 | en.md present, 1:1 mirror, single H1 | PASS | 1 H1 "Invite a co-host (Live Duo)" + H2 sections |
| 3 | metadata.yml: intercom_id, slug, locales, default_locale=pt-br | PASS | All present, default_locale lowercase |
| 4 | metadata description <= 140 chars per locale | PASS | pt-br: 124 chars, en: 130 chars |
| 5 | Em-dashes / en-dashes = 0 in both md | PASS | grep verified |
| 6 | R$ leak in en body = 0 | PASS | en.md does not mention prices |
| 7 | currency_required gate | PASS | flow.yml currency_required=false (article is not transactional) |
| 8 | Auction / leilao banned word | PASS | 0 occurrences |
| 9 | Mockups: 3 screens declared, all required PNG pairs at v3 + DPR3 | PASS | 6 PNGs at 960x1560 |
| 10 | Mockup HTML pair (pt-br + en) per screen | PASS | 6 HTMLs total |
| 10b | Screen-scoped required_icons present in HTML | PASS | invite-bottom-sheet -> icon-camera-add (alt + comment), guest-invite-modal -> image_video (alt + comment) |
| 10c | review_checks declared per ios_required screen | PASS | All 3 screens declare 3 review_checks |
| 10d | Screen-scoped html_must_contain / html_must_not_contain | PASS | All 3 screens declare html_must_contain; remove-guest-alert declares the full text-only blocker set |
| 10e (PR #92) | icons_match_ios_source anchored per screen | PASS | invite-bottom-sheet anchor A (required_icons icon-camera-add), guest-invite-modal anchor A (required_icons image_video), remove-guest-alert anchor B (html_must_not_contain `<img`, `<svg`, `icon-`) |
| 11 | Audit triplet present: code-audit, content-audit, compliance | PASS | 3 audit files |
| 12 | icons_required entries used in HTML AND have iOS source proof | PASS | icon-camera-add: alt + comment + assets/icons-ios/icon-camera-add.svg; image_video: alt + comment + assets/icons-ios/image_video.png |
| 13 | forbidden_terms grep | PASS | "5 minutes", "5-minute", "five-minute", "expires after", "expira apos", "five minute" all return 0 hits in body |
| 14 | must_answer keywords | PASS | invite, duo, guest, accept, remove all present in pt-br + en |
| 15 | risk_flags non-empty -> resolved_decisions required | PASS | risk_flags is empty |
| 16 | TOC | PASS | Article has 8 H2; default workflow toc_policy=warn (not strict). No TOC needed by per-article override; soft warn acceptable |
| 17 | Heading hierarchy: exactly 1 H1 per locale | PASS | verified |
| 18 | Mockup orphans / source_of_truth path existence | PASS | All 3 ios_files paths verified with `ls`; 0 orphan HTMLs |
| 27 | source_of_truth.ios_files actually exist on disk | PASS | All 7 paths under JAMBLE_IOS_ROOT exist |
| Stale-feature audit | Structured table with required cols | PASS | content-audit-14288117.md has the table with all required columns |

Verdict: PASS pending no risk resolution. No active risk_flags, no resolved_decisions required.

## PR #92 anchor matrix (per-screen)

| Screen | Anchor | Mechanism | Verified |
|---|---|---|---|
| invite-bottom-sheet | A (real-icon) | `required_icons: [icon-camera-add]` + `alt="icon-camera-add"` and `<!-- icon: icon-camera-add from Assets.xcassets/icon-camera-add.imageset -->` in both pt-br and en HTML | YES |
| guest-invite-modal | A (real-icon) | `required_icons: [image_video]` + `alt="image_video"` and `<!-- icon: image_video from Assets.xcassets/image_video.imageset -->` in both pt-br and en HTML | YES |
| remove-guest-alert | B (text-only) | `html_must_not_contain: ["<img", "<svg", "icon-"]` (all three blockers); HTML grep shows 0 occurrences of each | YES |

No `screen_icon_review_check_unanchored` warns expected.
