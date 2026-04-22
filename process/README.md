# Intercom Mockup Production Process

**Purpose**: operational guide for producing Intercom help center articles at scale, with code-faithful mobile mockups replacing ASCII boxes.

**Audience**: AI agents (Claude, Haiku) and any operator running the pipeline.

**Status**: validated on 1 article (Sell Mode, article 14288093). Ready to scale to 67 articles / 228 ASCII boxes.

**IMPORTANT**: **Read [00-HARD-RULES.md](00-HARD-RULES.md) before starting.** It encodes 18 real regressions from 31+ previous worker PRs. Violating any of these rules = PR rejected.

---

## The problem we solved

Intercom articles for the Jamble Seller Center contained 228 ASCII boxes (`┌─┐`) that rendered unreadable on mobile, the box-drawing chars broke, text overflowed, buttons collapsed. Plain text was clearer but killed the visual context sellers needed to "see" the screen.

## The solution

A 3-stage pipeline:

1. **Interpret** the ASCII as a specific iOS screen (which component, which text, which state)
2. **Rebuild** as a code-faithful HTML mobile mockup (components lifted from actual Swift files)
3. **Publish** via `HTML → PNG (Puppeteer) → GitHub repo → Intercom API injection`

The key insight that broke the deadlock: existing ASCII-to-image tools (aasvg, aa2img, wiremd) just redraw the ASCII, they don't make it *pretty* or *mobile-ready*. What works is treating the ASCII as intent, reading the real iOS code for the actual component, and rebuilding it in HTML with the Jamble design system baked in.

---

## Quick start for an AI agent

Given one ASCII box from an Intercom article, produce the final published mockup by running these 6 steps in order. Each step has its own doc in this folder.

| Step | Doc | Deliverable |
|------|-----|-------------|
| 1. Extract ASCII from article | [01-extraction.md](01-extraction.md) | `ascii-box-N.txt` with clean newlines |
| 2. Identify the iOS screen | [02-code-lookup.md](02-code-lookup.md) | File path + component name + styling details |
| 3. Build the HTML mockup | [03-html-template.md](03-html-template.md) | `prod-boxN.html` |
| 4. Screenshot to PNG | [04-screenshot.md](04-screenshot.md) | `prod-boxN.png` (rounded, gray frame) |
| 5. Push to GitHub | [05-hosting.md](05-hosting.md) | Public URL on `help-center` repo |
| 6. Inject in Intercom | [06-intercom-injection.md](06-intercom-injection.md) | Updated article with `<img>` tag |
| 7. Fix mobile-breaking tables | [07-tables-mobile.md](07-tables-mobile.md) | 2-col tables → `<ul>`; 3+ col → PNG |
| 8. Editorial quality (em-dash rule, SEO, tone) | [08-editorial-quality.md](08-editorial-quality.md) | ≤140 char desc, zero em-dashes, job-to-do headings |
| 8b. SEO/GEO fact-check | [08-seo-geo-checklist.md](08-seo-geo-checklist.md) | Score ≥ 14/20 (SEO + GEO) before publish |
| 9. Screenshot framing | [09-screenshot-framing.md](09-screenshot-framing.md) | Every image wrapped in H2 + intro + alt + caption + action |
| 10. Fact-check code | [10-fact-check-code.md](10-fact-check-code.md) | `code-audit-<id>.md` with zero MISMATCH |
| 11. Fact-check content (leaks) | [11-fact-check-content.md](11-fact-check-content.md) | `content-audit-<id>.md` with zero BLOCKERS |
| 12. Procedure compliance (final gate) | [12-procedure-compliance.md](12-procedure-compliance.md) | `compliance-<id>.md` with ALL PASS, restart on FAIL |

The [design-system.md](design-system.md) doc is the reference for all colors, fonts, radii, button styles.

---

## Golden rules (the seven you cannot break)

1. **iOS code is the source of truth, not Figma, not memory.** Every styling decision (radio color, icon, subtitle wording, border radius) must be traceable to a Swift file. If the code says navy `#162233`, the mockup uses navy, even if the brand color would look nicer.
2. **Intercom strips inline styles on `<img>`.** Rounded corners, shadows, borders must be baked into the PNG via the HTML template, not added as `style=""` attributes.
3. **Intercom refuses `data:` URIs.** Images must live at a public URL (`raw.githubusercontent.com`). Intercom will auto-cache them on its CDN.
4. **One phone frame, one gray outer frame, one style.** All mockups share the same phone card wrapper + outer gray rounded frame. Consistency beats per-article creativity.
5. **Never invent copy.** Titles, subtitles, button labels come from the Swift source (enum cases, `String(localized:...)`), not from the ASCII, not from the article text, not from intuition.
6. **Never echo base64 or image bytes to stdout.** Claude Code auto-attaches data-URIs and binary blobs from command output. A bad blob returns `400 Could not process image` and poisons the session history permanently, every turn after fails the same way. Always redirect to a file, inspect via `wc -c` / `ls -la` / `file`, never `echo`, `cat`, or `head` the content. Full rationale and safe patterns in [03-html-template.md](03-html-template.md#binary-data-hygiene-never-echo-base64-to-stdout).
7. **pt-BR is the primary source language, EN is a 1:1 mirror.** Jamble is Brazil-only, sellers are native Portuguese speakers. Every article is written in pt-BR first with the full pipeline, then translated to EN as a 1:1 mirror. The only allowed divergence is currency localization (`R$` → `$`, BR-style decimals → US-style). Drift between pt-BR and EN is a bug. Detail in [08-editorial-quality.md](08-editorial-quality.md#localization-rule).

---

## Quality bar

Before pushing a mockup to Intercom, verify:

- [ ] Every text string matches the iOS source exactly (title, subtitle, button label)
- [ ] Colors match the design system (check against [design-system.md](design-system.md))
- [ ] Icons are the real iOS SVG assets (from `Jamble/RESOURCES/Assets.xcassets/`), not emoji
- [ ] Phone frame + outer gray frame are present (use shared CSS from template)
- [ ] PNG rendered at `deviceScaleFactor: 3` (retina)
- [ ] Hosted on `Jamble-Live-Shopping/help-center` repo (not a personal repo, not a temp host)
- [ ] Published article verified on mobile (TestFlight or real device) before batch continues
- [ ] No `<table>` remains that would break on mobile, either converted to `<ul>` (2-col label/value) or rendered as PNG mockup (3+ col complex data). See [07-tables-mobile.md](07-tables-mobile.md).
- [ ] Zero em-dashes (U+2014) or en-dashes (U+2013) anywhere in body, description, or pt-BR. Commas only. See [08-editorial-quality.md](08-editorial-quality.md).
- [ ] Currency localized: `$` in EN body, `R$` in pt-BR body. Never `R$` in EN, never `$` in pt-BR. See RULE 2b in [08-editorial-quality.md](08-editorial-quality.md).
- [ ] Zero "auction" / "leilão" anywhere. Only "Real-time offers" / "Ofertas em tempo real". See RULE 2c.
- [ ] Visual fidelity check done on every mockup (Check E in [10-fact-check-code.md](10-fact-check-code.md)): side-by-side vs simulator, MATCH or code-only noted.
- [ ] Word-diet pass run (Scan 4 in [11-fact-check-content.md](11-fact-check-content.md)): every superfluous sentence cut or shortened.
- [ ] Tone-of-voice test PASS (Scan 5): a first-time BR seller on phone reads top to bottom without pausing.
- [ ] `code-audit-<id>.md` exists in `_work/` with zero open MISMATCH. See [10-fact-check-code.md](10-fact-check-code.md).
- [ ] `content-audit-<id>.md` exists in `_work/` with zero BLOCKERS. See [11-fact-check-content.md](11-fact-check-content.md).
- [ ] `compliance-<id>.md` shows ALL PASS, final gate. See [12-procedure-compliance.md](12-procedure-compliance.md).

---

## File map of this process

```
_work/process/
├── README.md                   # This file
├── design-system.md            # Jamble colors, fonts, buttons (from iOS code)
├── 01-extraction.md            # Get ASCII out of Intercom article HTML
├── 02-code-lookup.md           # Find the iOS component that matches the ASCII
├── 03-html-template.md         # The reusable HTML template + how to adapt it
├── 04-screenshot.md            # Puppeteer script to render HTML → PNG
├── 05-hosting.md               # GitHub repo setup + upload command
├── 06-intercom-injection.md    # API call to replace ASCII with <img>
├── 07-tables-mobile.md         # Convert tables that break on mobile
├── 08-editorial-quality.md     # SEO, tone, em-dash rule, job-to-do headings
├── 08-seo-geo-checklist.md     # SEO/GEO scoring (parallel track)
├── 09-screenshot-framing.md    # How to wrap screenshots in articles
├── 10-fact-check-code.md       # Verify claims against iOS/Android source
├── 11-fact-check-content.md    # Scan for user PII and internal info leaks
├── 12-procedure-compliance.md  # Final gate, restart on any failing check
├── template.html               # The canonical HTML template (copy-paste starting point)
└── logs/                       # Per-article audit logs + compliance reports
    ├── code-audit-<id>.md      # Step 10 output: claims vs code + visual fidelity
    ├── content-audit-<id>.md   # Step 11 output: PII scans + word diet + tone
    └── compliance-<id>.md      # Step 12 output: final 17-check PASS/FAIL report
```

## Lineage

Process built during session 2026-04-15 to 2026-04-16 on project `2l-help-center` (formerly `2m-seller-center-refonte`). Validated on articles `14288093` (How to List Products on Jamble) and `14288094` (Choose Quantities When Listing Products). First production runs: 4 mockups on 14288093 (Settings, Pending Application, Sell Mode, Select Photos), 2 mockups on 14288094 (Quantity stepper, Pre-Bid error toast).

Target migration: this `process/` folder moves to the root of `Jamble-Live-Shopping/help-center/process/` as part of the GitHub-as-source-of-truth pivot (see project ARCHITECTURE.md).
