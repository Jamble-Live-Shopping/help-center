# Phase 3a — Layout Proof Table (mandatory before any `source: ios_required` mockup)

## TL;DR

Before writing a single line of HTML for a `source: ios_required` screen, produce a Layout Proof Table that maps every visible UI element to its iOS source file:line + parent container + alignment + size + planned HTML selector. **No proof table → no PNG render → no exception_free.**

This gate exists because of two false negatives on `creating-and-managing-real-time-offers` screen-2 (2026-05-11) :

1. **AM pass** : the writer correctly found the timer icon (`auction_time_icon`) but rendered it as a giant top-centered countdown pill. The iOS source has `saleTimerButton` trailing-aligned BELOW `saleAmountLabel` in the sale-status block. Asset matched ; layout invented.
2. **PM pass** : after the AM fix, the patched HTML placed the timer inside `.price-wrap` — but `.price-wrap` was the LEFT column of a `justify-content: space-between` row, with `.action-btn` to its right. The Layout Proof Table correctly DESCRIBED the placement as "trailing-aligned in cp3-Bb-DxC (right column)" ; the CSS selector implemented "left column under price". The table and the CSS contradicted each other. The selector name (`.price-wrap`) sounded like a sale-status column, but its visible parent rendered it on the left.

Both passes failed the same gap : the factory's existing rules (icons_match_ios_source, labels_match_xcstrings) prove **what** is shown, not **where**.

## Why "looks plausible" is the wrong gate

`icons_match_ios_source` proves the asset name. `labels_match_xcstrings` proves the copy. Neither proves placement, parent container, or constraint relationships. A mockup can satisfy both and still invent a layout that doesn't exist in the app — or contradict its own proof. The Layout Proof Table forces the writer to map each element to a real `parent / constraint / size` triple AND prove the rendered CSS container actually places it where the table says.

## When to produce it

For **every screen with `source: ios_required`**, before writing any HTML for that screen. Concept articles (`source: composite`, editorial illustrations) are exempt — those mockups intentionally do not mirror iOS UI.

## Step 1 — Locate source of truth

Find the EXACT files. Walk the discovery this way :

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
- **HTML/CSS selector** : the planned class name AND its rendered parent. See Step 2.5 below.

### When `mockup-name__<locale>.html` ships

The selectors in the rendered HTML must match column 7 of the Layout Proof Table exactly. If you change a selector during writing, update the table first and re-justify against the iOS source.

## Step 2.5 — Hard wording rule on column 7 (post 2026-05-11 PM false negative)

**A selector name is not proof of placement. The rendered CSS container must visibly enforce the alignment.**

If column 5 (Alignment / constraints) says "right" or "trailing" or "trailing-aligned" :

- ✅ The element MUST be a descendant of a CSS container that visibly enforces right/trailing alignment via ONE of :
  - parent has `align-items: flex-end` (the element is in a column flex with right alignment)
  - parent has `justify-content: flex-end` (the element is in a row flex pushed right)
  - parent has `justify-content: space-between` AND the element is the RIGHT-side (last) flex child
  - element has `margin-left: auto` (pushes itself to the right in a row flex)
  - element has `align-self: flex-end` (right-aligns itself in a column flex)
  - element has `text-align: right` AND its parent has the same flex placement guarantees
- ❌ A selector name like `.sale-status`, `.right-column`, `.price-trailing`, `.timer-right` is NOT proof. The reviewer cannot see CSS guarantees from the class name alone.

If column 5 says "left" or "leading" :

- ✅ The element must be a descendant of a CSS container that visibly enforces left placement (first child of `justify-content: space-between`, parent `align-items: flex-start`, no `margin-left: auto`, etc.).

If column 5 says "centered" :

- ✅ The element must be in a `justify-content: center` row flex OR `align-self: center` OR `margin: 0 auto` etc.

### Symmetry check before claiming exception_free

Re-read column 5 and column 7 for every row in the table. Ask : "if I deleted the class name and replaced it with `<div>`, would a reviewer who only sees the parent CSS still know this element renders where column 5 says?" If the answer is no, the selector is named after intent, not enforced by structure, and the table is unfinished.

Confidence check on a real case (the PM 2026-05-11 false negative) :

- `.product-card .price-wrap .sale-timer-btn` → parent `.price-wrap` is in `.pbottom-row { display: flex; justify-content: space-between; }` as the FIRST flex child. CSS guarantees `.price-wrap` is the LEFT child. So `.sale-timer-btn` is left-aligned, regardless of the class name. **Fails column 5 ("trailing-aligned via Sjh-oJ-6bY")**.
- `.product-card .product-row .sale-status .sale-timer-btn` → parent `.sale-status { display: flex; flex-direction: column; align-items: flex-end; }` and `.sale-status` is the THIRD flex child of `.product-row` (after `.thumb` and `.pinfo { flex: 1 }`). CSS guarantees `.sale-status` is pushed to the right by `.pinfo` flex-grow, and `align-items: flex-end` forces every child to be trailing-aligned. **Passes column 5**.

The first one says "right" but renders left. The second one's CSS structure visibly enforces "right". That is the difference between proof and intent.

## Step 3 — Encode the layout anchor in `flow.yml`

For every `ios_required` screen, add a short layout-anchor comment block above the screen entry :

```yaml
- name: <screen-name>
  # Layout anchor (source of truth):
  #   files: <list of swift / xib paths and key line ranges>
  #   parents: <top-level container hierarchy, eg cp3-Bb-DxC under productView Ogx-lZ-qCX>
  #   key placements: <2-4 critical placement relationships, eg "saleTimerButton sits BELOW saleAmountLabel, trailing-aligned via constraint vAm-e3-sKd + Sjh-oJ-6bY">
  #   forbidden layouts: <2-3 wrong layouts the writer must NOT produce, eg "NOT a top-centered countdown pill, NOT inside a class whose parent flex container is left-aligned, NOT a floating overlay">
  purpose: "<one-line purpose>"
  source: ios_required
  review_checks:
    - icons_match_ios_source       # only if you ALSO declare required_icons
    - labels_match_xcstrings       # always for ios_required
    - no_invented_ui_state         # always
    - layout_matches_ios_source    # add this once the Layout Proof Table is complete AND Step 2.5 passed
  required_icons: [<asset-name>]   # OR html_must_not_contain for text-only screens
  html_must_contain:
    pt-br: [<exact xcstrings tokens>]
    en:    [<exact xcstrings tokens>]
```

The `layout_matches_ios_source` review_check is **descriptive only** at the moment — same shape as `icons_match_ios_source` before PR #92's rule 10e existed. It signals to the reviewer that a Layout Proof Table was produced, Step 2.5 passed, and the writer commits to the rendered CSS structure. If the same false-negative class repeats across multiple slugs in a future batch, that's the trigger to encode a deterministic validator rule.

## Step 4 — Visual QA after rendering

After `node scripts/shot-retina.mjs <html> <png>` :

```bash
# Quick stale-language sweep across the article folder
rg -n "center|central|ao centro|centered|floating|chrono|placeholder|TODO|SKELETON" articles/<slug>
# Also grep for any old class names that should have been replaced
rg -n "price-wrap|pbottom-row|chrono-wrap" articles/<slug>/mockup-sources
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
| Symmetry of column 5 vs column 7 | For every row : the rendered element is actually where column 5 says, enforced by the CSS parent of column 7 (Step 2.5 check) |

If the `rg` sweep surfaces any of the listed stale phrases AND those phrases describe an outdated layout, **patch body / alt / audit before reporting**. Words like `chrono`, `centered`, `floating` are tells from earlier drafts. Old class names (`price-wrap`, `pbottom-row`) in current screen-2 files are direct PM-2026-05-11 false-negative signatures.

## Step 5 — Stop conditions

STOP and report instead of claiming `exception_free` if any of these fire :

- iOS source is ambiguous or missing for an element.
- Layout Proof Table has any blank row.
- CSS selector placement (column 7) does not match iOS parent/alignment (column 3-5), per Step 2.5 symmetry check.
- The rendered CSS parent of column 7 does NOT visibly enforce the alignment stated in column 5 (e.g. column 5 says "right" but the selector's parent is the first child of `justify-content: space-between`).
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

## Canonical example — real-time-offers screen-2 (2026-05-11 retro, both passes)

This is the false-negative chain that triggered this gate (AM pass) and its hard wording rule (PM pass). The patched Layout Proof Table for the corrected screen-2 :

| UI element | iOS source file:line | Parent container | Sibling / order | Alignment / constraints | Size / style | HTML/CSS selector |
|---|---|---|---|---|---|---|
| `productView` (left column) | `ShowSaleView.swift:33` + XIB `Ogx-lZ-qCX` | `T4f-up-gzW` (product card root) | left of sale-status (gT3-yr-nqV) | leading=card.leading ; top/bottom=card | thumb 54×54 + title M semibold | `.product-card .product-row .thumb` + `.product-card .product-row .pinfo` (FIRST + SECOND flex children of `.product-row`, with `.pinfo` having `flex: 1` to push `.sale-status` right) |
| `saleAmountLabel` (highest offer price) | `ShowSaleView.swift:42` + XIB `JST-50-JEJ` | sale-area `cp3-Bb-DxC` (RIGHT column) | top of right column | **trailing-aligned via rAq-QJ-REu** ; top=row.top (yFg-WR-wxX) | white attributedText, bold body | `.product-card .product-row .sale-status .price-val` (parent `.sale-status` has `display: flex; flex-direction: column; align-items: flex-end` AND is the THIRD flex child of `.product-row` ; CSS structure visibly enforces RIGHT placement) |
| `saleTimerButton` (compact countdown) | `ShowSaleView.swift:43` + `:330-340` + `:858-871` + XIB `mFP-1R-Tk3` :199-217 | sale-area `cp3-Bb-DxC` (RIGHT column) | bottom of right column, BELOW saleAmount | **trailing-aligned via Sjh-oJ-6bY** ; top >= saleAmount.bottom via vAm-e3-sKd | height 20, bg clear, icon-leading, title widthAnchor 45 right, `.body(.S(.semibold))`, `.content.warning` amber | `.product-card .product-row .sale-status .sale-timer-btn` (same `.sale-status` parent, child of the column-flex with `align-items: flex-end` → visibly right-aligned) |
| `auction_time_icon` glyph | `ShowSaleView.swift:861` ; asset `Assets.xcassets/auction_time_icon.imageset` | inside saleTimerButton | leading (`imagePlacement = .leading`) | template render, currentColor | 16×16 | inline `<svg>` in `.sale-timer-btn` |
| Host action button "3 ofertas" / "3 offers" | `ShowSaleView.swift:53` programmatic `hostActionButtons: UIStackView` | **NOT inside T4f-up-gzW** — separate area below product card | separate row below product-row | row center-aligned, full-width-ish capsule | 44pt height, capsule, purple `#7E53F8` | `.product-card .action-row .action-btn` (SEPARATE `.action-row` div BELOW `.product-row` ; `.action-row` has `justify-content: center` ; the action button is NOT a sibling of `.sale-status`) |

### Symmetry sanity check (Step 2.5 applied row-by-row)

| Row | Column 5 says | Column 7 parent CSS guarantees |
|---|---|---|
| saleAmount | trailing | `.sale-status { align-items: flex-end }`, `.sale-status` is right flex child of `.product-row` ✅ |
| saleTimer | trailing | same parent, same guarantee ✅ |
| auction_time_icon | leading inside saleTimerButton | `.sale-timer-btn` is inline-flex with image first, no margin-left auto — leading inside an already-trailing parent ✅ |
| hostActionButtons | separate row below | `.action-row` is a sibling of `.product-row`, not a child ; `justify-content: center` puts the button visibly below, not inline ✅ |

### Stale-language sweep (post pass-2 patch)
```
$ rg -n "center|central|ao centro|centered|floating|chrono|placeholder|TODO|SKELETON|price-wrap|pbottom-row" articles/creating-and-managing-real-time-offers
# (only matches : code-audit + _work/layout-proof references to "centered chrono" / "price-wrap" in the patch-history sections explaining the two false negatives — acceptable historical context)
```

### Visual verdict
```
layout_matches_ios_source : yes
overlap_or_bleed          : no
stale_alt_text            : no  (article body + alt text reference the right-column sale-status with timer-below-price layout, and the separate-row action button)
```

### Forbidden layouts (encoded in flow.yml screen-2 comment)
- NOT a giant top-centered countdown pill (AM false negative)
- NOT inside a class whose parent flex container is visibly left-aligned (PM false negative)
- NOT a floating overlay outside the product card
- NOT a separate row between the product info and the action button (the timer is INSIDE the right column with the price, NOT a sibling row of `.product-row`)
- NOT inline with the action button as siblings of `justify-content: space-between` (the timer is in the right column ; the action button is a separate row below)

This is the level of source-grounded specificity the gate requires for every `ios_required` screen going forward, plus the Step 2.5 symmetry check between column 5 (intended placement) and column 7 (rendered CSS structure).
