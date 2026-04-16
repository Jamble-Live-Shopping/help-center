# Step 10, Fact-check against code

**Goal**: verify every factual claim in the article is backed by actual iOS/Android source code. If an article says "the minimum price is R$ 5.00" or "titles can be up to 60 characters", that number must exist in the repo. Otherwise it is a hallucination, outdated, or misremembered, and will confuse or mislead sellers.

**Runs after Step 8 (editorial quality) and before Step 11 (content safety).**

## What counts as a fact worth checking

Any **numeric value**, **range**, **limit**, **rule**, **UI behavior claim**, **list of options**, or **feature capability** that a reader could verify or rely on for a real action. Examples from article 14288093:

- "The minimum price is R$ 5.00 and the maximum is R$ 5,000.00"
- "You have a maximum of 60 characters" (title length)
- "Up to 10 photos"
- "Three sell modes: Real-time offers, Sudden Death, Buy It Now"
- "Card, Booster, Light Accessories, Light Apparel, Standard Apparel, Heavier Apparel, Bulkier Items" (shipping profiles)
- "New with Tags, New without Tags, Very Good, Good, Satisfactory" (condition grades)
- "When a new offer comes in near the end of the timer, extra time is added"

NOT checkable (ignore):
- Marketing fluff ("sell your items fast")
- Subjective advice ("titles that get clicks")
- Pure instructions ("Tap Save")

## Procedure

For each claim, run one or more of these checks:

### Check A, Constants and limits

```bash
# Example: verify min/max price
gh search code "minPrice" --repo Jamble-Live-Shopping/Jamble-iOS --limit 5
gh search code "maxPrice" --repo Jamble-Live-Shopping/Jamble-iOS --limit 5
gh search code "MIN_PRICE\|MAX_PRICE" --repo Jamble-Live-Shopping/Jamble-iOS --limit 5

# Example: verify title character limit
gh search code "title.count\|titleLimit\|60" --repo Jamble-Live-Shopping/Jamble-iOS --filename "*Product*" --limit 5

# Example: verify photo limit
gh search code "maxPhotos\|photo.count" --repo Jamble-Live-Shopping/Jamble-iOS --limit 5
```

Open the matching file, read the actual value, compare to the article. If mismatch: the article is wrong, fix the article (or escalate if the article is right and the code changed without docs update).

### Check B, Enum cases (sell modes, categories, conditions)

For any article claim of the form "there are X options: A, B, C", find the Swift enum:

```bash
gh search code "enum ShowSaleType\|enum ShippingProfile\|enum Condition" --repo Jamble-Live-Shopping/Jamble-iOS --limit 5
```

Read the enum. Verify:
- Count matches (if article says "three", enum has three non-`.unknown` cases)
- Names match (case order, spelling, pt-BR localization strings)
- No hidden / deprecated cases are leaked to users (some enums have `.unknown`, `.legacy`, etc. that should NOT appear in help docs)

### Check C, UI behavior claims

For claims about what happens in the UI ("extra time is added", "the app remembers your previous selection", "buyers see a countdown"):

```bash
# Find the controller or view model that handles the behavior
gh search code "addExtraTime\|extraSeconds\|remainingTime" --repo Jamble-Live-Shopping/Jamble-iOS --limit 5

# Find "remembers your last" / persistence claims
gh search code "UserDefaults\|persisted\|lastUsed" --repo Jamble-Live-Shopping/Jamble-iOS --filename "*Product*" --limit 5
```

Read the code. If the code says extra time is 15 seconds and the article says 30, fix the article. If the article claims a persistence feature the code doesn't implement, drop the claim.

### Check D, Text strings

Article button labels, screen titles, and alert messages must match what the code renders. Already covered by Step 2 (code-lookup) for each mockup, but run one more sweep across non-mockup prose:

```bash
# Find a specific claimed label
gh search code "\"Add a listing\"\|\"Sell Mode\"" --repo Jamble-Live-Shopping/Jamble-iOS --limit 3
```

## Audit template

After running the checks, produce a short audit file per article. Save as `code-audit-<article-id>.md` in the project `_work/` folder.

```markdown
# Code audit, article 14288093 (How to List Products)

Checked on 2026-04-16.

| Claim | Claimed | Code says | Status |
|-------|---------|-----------|--------|
| Min price | R$ 5.00 | `Currency.BRL.minPrice = 5.0` in `Currency.swift` | OK |
| Max price | R$ 5,000.00 | `Currency.BRL.maxPrice = 5000.0` | OK |
| Title max chars | 60 | `CreateProductTitleCell.maxLength = 60` | OK |
| Photo max count | 10 | NOT FOUND, `photoLimit` returns 10 in `ProductPhotoViewModel.swift` | OK |
| Sell modes (3) | Real-time offers, Sudden Death, Buy It Now | `ShowSaleType` has 4: AUCTION (→ Real-time offers), SUDDEN_DEATH, BUY_IT_NOW, GIVEAWAY | MISMATCH, article excludes GIVEAWAY, is that intentional? |
| "Extra time added on late offers" | Yes | `BidsCoordinator.extraTimeOnBid = 5` seconds | OK (article does not specify the duration, so not lying) |
| Shipping profiles | 7 (Card, Booster, Light Accessories, Light Apparel, Standard Apparel, Heavier Apparel, Bulkier Items) | ShippingProfile enum has exactly those 7 | OK |
| Condition grades | 5 (New with Tags, ...) | `ProductCondition` enum: 6 cases incl. `POOR` | MISMATCH, article missing "Poor" |

## Decisions
- GIVEAWAY omission is intentional (giveaways are a separate product creation flow, not a sell mode in the listing form). Leave article as is.
- POOR condition exists in code but is discouraged by support policy. Escalate to @mahaut to confirm whether to add to article or keep hidden.

## Actions before ship
- [ ] Clarify with @mahaut whether POOR should be in article
```

## Check E, Visual fidelity (does the mockup look like the actual app?)

The mockup pipeline produces a PNG meant to resemble the real app. This check verifies that resemblance. Not just that the code references are correct in text, but that the final rendered image looks like the screen a seller would see if they opened the app right now.

### Procedure

For every mockup `<img>` in the article:

1. **Capture the real screen**. Open the Jamble app in an iOS simulator (or on a TestFlight device), navigate to the exact state depicted, take a screenshot.
2. **Side-by-side compare** with the mockup PNG. Use any image diff tool, or simply open both in a split window.
3. **Walk through this 6-point check**:
   - Layout: order of elements, spacing, alignment
   - Colors: eyeball or sample hex with a color picker tool
   - Text: word for word, including punctuation and capitalization
   - Icons: same symbol, same size, same tint, same SVG source
   - State: the correct radio selected, the correct toggle position, the correct badge count
   - Typography: weight, size, letter spacing
4. **Record every divergence** in the audit file, even sub-pixel.

### Acceptable vs unacceptable divergences

| Divergence | Acceptable? |
|------------|-------------|
| Platform chrome (status bar, home indicator) missing from mockup | Yes |
| Placeholder sample content (e.g. product title) differs from the code default | Yes, use a BR collectible from RULE 2 |
| Font rendering sub-pixel differences | Yes |
| Phone-frame white card vs full-bleed screen | Yes, the phone frame is a documentation convention |
| Outer gray frame vs no frame in the app | Yes, same reason |
| Color off by 1 hex value | No, fix it |
| Missing or extra button, field, or section | No, fix it |
| Wrong selection state | No, fix it |
| Paraphrased text instead of the exact code string | No, fix it |
| Icon that is "close" but not the real SVG from `Assets.xcassets` | No, download the real SVG and embed it |

### When you cannot reproduce the state in a simulator

Some mockups show rare states (empty accounts, specific server errors, paid-only features a test account cannot reach). When reproduction is impossible:

- Read the view controller code end to end, verify the mockup matches the layout described by constraints and subview hierarchies.
- Add a note to the audit file, for example: `Visual fidelity deferred, state cannot be reproduced. Verified against code only.`
- Tag the mockup row with `audit: code-only` so a future reviewer knows to spot-check on a real device when a qualifying account is available.

### Audit template addition

Extend `code-audit-<article-id>.md` with a second table:

```markdown
## Visual fidelity

| Mockup | Compared against | Result |
|--------|------------------|--------|
| prod-box4.png (Sell Mode) | iOS simulator, CreateProductViewController, section SELL_MODE | MATCH |
| prod-box5.png (Select Photos) | iOS simulator, same VC, section PHOTOS | MATCH |
| prod-box3.png (Your Show, empty state) | iOS simulator, ShowHostProductListViewController with an empty list | MATCH |
| prod-box2.png (Pending Application alert) | Not reproduced, no account in pending state | code-only |
```

## Fail policy

If the audit surfaces 1+ MISMATCH, the article is not ready for ship. Either:
- Fix the article to match the code, or
- Escalate the mismatch to the relevant engineer / PM to decide (code change vs doc change)

Do not silently keep a mismatch in a published article. It erodes trust and creates support tickets.

## When the code has moved since the article was written

Articles can legitimately drift from code. When you find a mismatch, check `git log` on the relevant file:

```bash
gh api repos/Jamble-Live-Shopping/Jamble-iOS/commits?path=Jamble/PRODUCT/Views/CreateProductViewController.swift --jq '.[0:5] | .[] | {sha: .sha[:8], date: .commit.author.date, msg: .commit.message[:80]}'
```

If the code changed recently (last 30 days) and the article was written before, the article needs an update. If the code changed long ago and the article was never right, flag as tech debt.
