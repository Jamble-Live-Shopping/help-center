# Phase 3a — Layout Proof Table (mandatory before any `source: ios_required` mockup)

## TL;DR

Before writing a single line of HTML for a `source: ios_required` screen, produce a Layout Proof Table that maps every visible UI element to its iOS source file:line + parent container + alignment + size + planned HTML selector. **No proof table → no PNG render → no exception_free.**

This gate exists because of the batch real-2 false negative on `creating-and-managing-real-time-offers` screen-2 (2026-05-11): the writer correctly found the timer icon (`auction_time_icon`) but rendered it as a giant top-centered countdown pill. The iOS source has `saleTimerButton` trailing-aligned BELOW `saleAmountLabel` in the sale-status block. Asset matched ; layout invented. The factory's existing rules (icons_match_ios_source, labels_match_xcstrings) prove **what** is shown, not **where**.

## Why "looks plausible" is the wrong gate

`icons_match_ios_source` proves the asset name. `labels_match_xcstrings` proves the copy. Neither proves placement, parent container, or constraint relationships. A mockup can satisfy both and still invent a layout that doesn't exist in the app. The Layout Proof Table forces the writer to map each element to a real `parent / constraint / size` triple before rendering, so the rendered PNG can be checked deterministically against a written contract instead of "looks roughly right".

## When to produce it

For **every screen with `source: ios_required`**, before writing any HTML for that screen. Concept articles (`source: composite`, editorial illustrations) are exempt — those mockups intentionally do not mirror iOS UI.

## Step 1 — Locate source of truth

Find the EXACT files. Walk the discovery this way:

| iOS surface kind | Files to read |
|---|---|
| UIKit + XIB | `<View>.swift` (IBOutlets, viewDidLoad, config functions like `setTime`) AND `<View>.xib` (frame, constraints, hierarchy) |
| UIKit programmatic | `<View>.swift` + grep for stack views, addArrangedSubview, constraint() calls |
| SwiftUI | `<View>.swift` View body + modifiers + ViewModifier overlays |
| Storyboard | `<flow>.storyboard` for hierarchy + segues |

If you cannot find the source after a reasonable grep (`grep -rln "<ClassName>"` in `LIVE_SHOPPING/` etc.), **STOP this screen**. Either add a `risk_flag` in `flow.yml` and use `source_of_truth.negative_scan`, or reduce `mockup_count_target` and skip the screen. Do not invent a layout.

## Step 2 — Produce the Layout Proof Table

In your `_work/<slug>__layout-proof.md` scratch file (created next to the brief), write one table per `ios_required` screen :

| UI element | iOS source file:line | Parent container | Sibling / order | Alignment / constraints | Size / style | HTML/CSS selector |
|---|---|---|---|---|---|---|

### Rules

- **Parent container** must be a real iOS view, named or with its XIB id (`cp3-Bb-DxC`, `xaP-0h-NcP`, etc.). NOT "the right side of the screen".
- **Alignment** must include left/right/top/bottom/center/trailing/leading where visible in source. If a constraint says `firstAttribute=trailing secondItem=saleAmountLabel secondAttribute=trailing`, write "trailing-aligned with saleAmountLabel".
- **Sibling / order** : if an element is `addArrangedSubview` in a stack, name the stack and the index. If it's between two other elements, name them.
- **Size / style** : font, weight, width/height constants, color tokens. If `titleLabel.widthAnchor = 45`, write "title width 45". If `foregroundColor = .content.warning`, write "amber per .content.warning".
- **HTML/CSS selector** : the planned class name and the parent class. If the iOS source says trailing/right-aligned, the CSS selector must reflect that (parent uses `justify-content: flex-end` or the child has `margin-left: auto` etc.). The pre-write selector commits you to a placement.

### When `mockup-name__<locale>.html` ships

The selectors in the rendered HTML must match column 7 of the Layout Proof Table exactly. If you change a selector during writing, update the table first and re-justify against the iOS source.

## Step 3 — Encode the layout anchor in `flow.yml`

For every `ios_required` screen, add a short layout-anchor comment block above the screen entry :

```yaml
- name: <screen-name>
  # Layout anchor (source of truth):
  #   files: <list of swift / xib paths and key line ranges>
  #   parents: <top-level container hierarchy, eg cp3-Bb-DxC under productView Ogx-lZ-qCX>
  #   key placements: <2-4 critical placement relationships, eg "saleTimerButton sits BELOW saleAmountLabel, trailing-aligned via constraint vAm-e3-sKd + Sjh-oJ-6bY">
  #   forbidden layouts: <2-3 wrong layouts the writer must NOT produce, eg "NOT a top-centered countdown pill, NOT under the left price column, NOT a floating overlay">
  purpose: "<one-line purpose>"
  source: ios_required
  review_checks:
    - icons_match_ios_source       # only if you ALSO declare required_icons
    - labels_match_xcstrings       # always for ios_required
    - no_invented_ui_state         # always
    - layout_matches_ios_source    # add this once the Layout Proof Table is complete
  required_icons: [<asset-name>]   # OR html_must_not_contain for text-only screens
  html_must_contain:
    pt-br: [<exact xcstrings tokens>]
    en:    [<exact xcstrings tokens>]
```

The `layout_matches_ios_source` review_check is **descriptive only** at the moment — same shape as `icons_match_ios_source` before PR #92's rule 10e existed. It signals to the reviewer that a Layout Proof Table was produced and that the writer commits to the layout. If the same false-negative class repeats across multiple slugs in a future batch, that's the trigger to encode a deterministic validator rule.

## Step 4 — Visual QA after rendering

After `node scripts/shot-retina.mjs <html> <png>` :

```bash
# Quick stale-language sweep across the article folder
rg -n "center|central|ao centro|centered|floating|chrono|placeholder|TODO|SKELETON" articles/<slug>
```

Then **open each PNG visually** and verify :

| Check | What you confirm |
|---|---|
| No overlapping text | No text bleeding into another text block ; no Z-index collision |
| No ghost / bleed-through text behind cards | All cards opaque ; no leftover dimmer or absolute-positioned label peeking through |
| No stale hidden elements visible | If your CSS hides an element with `display:none`, confirm the rendered PNG matches |
| No invented overlay / pill / card | Every visible element traces to a row in the Layout Proof Table |
| No contradiction between alt text and PNG | The article's `![alt](png)` alt text describes what the PNG actually shows |
| Visible hierarchy matches the table | Parent / sibling / order in the PNG matches column 3 + 4 of the table |

If the `rg` sweep surfaces any of the listed stale phrases AND those phrases describe an outdated layout, **patch body / alt / audit before reporting**. Words like `chrono`, `centered`, `floating` are tells from earlier drafts.

## Step 5 — Stop conditions

STOP and report instead of claiming `exception_free` if any of these fire :

- iOS source is ambiguous or missing for an element.
- Layout Proof Table has any blank row.
- CSS selector placement (column 7) does not match iOS parent/alignment (column 3-5).
- A rendered PNG has overlap, ghost text, or visible stale state.
- The article body or alt text describes a layout different from the rendered PNG.
- A manual layout check fails on any row of the table.

Raise a `risk_flag` (and matching `resolved_decision` if you ship despite it). Document the gap in `audit/code-audit-<intercom_id>.md` under a "Layout gap" section so the reviewer can spot-check.

## Deliverable format (reporter back to caller)

Every writer agent for an `ios_required` mockup MUST report :

```
Layout Proof Table   : <path to _work/<slug>__layout-proof.md>
Before/after PNG paths : <if patching after a false negative>
Validate result      : <exit code, hard/soft>
Batch summary        : <if applicable>
Explicit visual verdict:
  layout_matches_ios_source : yes / no
  overlap_or_bleed          : yes / no
  stale_alt_text            : yes / no
```

If any of the three booleans is `no` / `yes` (whichever is bad), DO NOT claim `exception_free` and DO NOT recommend mark-ready. Stop and report.

## Canonical example — real-time-offers screen-2 (2026-05-11 retro)

This is the false negative that triggered this gate. The patched Layout Proof Table for the corrected screen-2 :

| UI element | iOS source file:line | Parent container | Sibling / order | Alignment / constraints | Size / style | HTML/CSS selector |
|---|---|---|---|---|---|---|
| Sale area row | `LIVE_SHOPPING/SaleView/View/ShowSaleView.xib:179-217` | `T4f-up-gzW` (product card root) | right of `productView` (`Ogx-lZ-qCX`, gT3-yr-nqV: leading=productView.trailing+8) | row, vertical-axis stack | n/a | `.product-card .pbottom-row` |
| `saleAmountLabel` (current price) | `ShowSaleView.swift:43` + XIB id `JST-50-JEJ` | sale area row `cp3-Bb-DxC` | top of row | trailing-aligned (rAq-QJ-REu) ; top=row.top (yFg-WR-wxX) | bold price font | `.product-card .price-wrap .price-val` |
| `saleTimerAddedLabel` (15-wide "+Ns" indicator, hidden in steady state) | XIB id `q69-Ei-iJL` at line 180 | sale area row `cp3-Bb-DxC` | between saleAmount and saleTimer, leading of saleTimer | height 20 (CZA-36-Jau) ; trailing=saleTimer.leading-4 (yzq-0a-1wd) | tail-truncation | not rendered (hidden state) — note in flow.yml |
| `saleTimerButton` (compact countdown) | `ShowSaleView.swift:43` IBOutlet ; `:330-340` config ; `:858-871` setTime ; XIB id `mFP-1R-Tk3` :199-217 | sale area row `cp3-Bb-DxC` | bottom of row, right of saleTimerAddedLabel | trailing-aligned via Sjh-oJ-6bY ; below saleAmount via vAm-e3-sKd ; centerY w/ saleTimerAddedLabel via Ju0-vY-SSu | height 20 ; bg/border clear ; icon-leading ; titleLabel widthAnchor 45 ; text right-aligned ; spacing 4 ; `.body(.S(.semibold))` ; `.content.warning` amber | `.product-card .price-wrap .sale-timer-btn` (inline-flex, height 20, color #F2A900, gap 4, child `.timer-text` min-width 45 right-aligned) |
| `auction_time_icon` glyph | `ShowSaleView.swift:861` `UIImage(named: "auction_time_icon").withRenderingMode(.alwaysTemplate)` ; asset path `Assets.xcassets/auction_time_icon.imageset/auction_time_icon.pdf` | inside saleTimerButton | leading (image first per `imagePlacement = .leading`) | template render, foregroundColor = .content.warning | 16x16 | inline SVG in `.sale-timer-btn` (hand-traced from PDF, currentColor tint) |

### Stale-language sweep (post-patch)
```
$ rg -n "center|central|ao centro|centered|floating|chrono|placeholder|TODO|SKELETON" articles/creating-and-managing-real-time-offers
# (only matches : code-audit references to "centered chrono" in the patch-history section explaining the false negative — acceptable historical context)
```

### Visual verdict
```
layout_matches_ios_source : yes
overlap_or_bleed          : no
stale_alt_text            : no  (article body + alt text reference the timer-below-price layout, NOT a centered countdown)
```

### Forbidden layouts (encoded in flow.yml screen-2 comment)
- NOT a giant top-centered countdown pill
- NOT placed under the left price column
- NOT a floating overlay outside the product card
- NOT a separate row between the product info and the action button (the timer is INSIDE the price column, below the price)

This is the level of source-grounded specificity the gate requires for every `ios_required` screen going forward.
