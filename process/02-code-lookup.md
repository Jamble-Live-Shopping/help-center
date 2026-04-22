# Step 2, Identify the iOS screen behind the ASCII

**Goal**: find the exact Swift file that renders the screen the ASCII represents. Read it. Extract the exact text strings, colors, icons, layout logic.

**Why this matters more than anything**: the ASCII is a rough sketch by a writer. The iOS code is ground truth. The writer may have written "Real-time offers" but the code may say "Auction", the code wins. Same for button labels, subtitles, icons, copy.

## Search strategy

Given an ASCII box, identify distinctive text strings (a title, a button label, a unique phrase) and grep the iOS repo for them.

```bash
# Primary: full-text search via GitHub
gh search code "<distinctive text>" --repo Jamble-Live-Shopping/Jamble-iOS --limit 5

# Secondary: search by section/type name if you see one in the ASCII
gh search code "SELL_MODE" --repo Jamble-Live-Shopping/Jamble-iOS --limit 10
gh search code "SELECT_PHOTOS" --repo Jamble-Live-Shopping/Jamble-iOS --limit 10
gh search code "pendingApplication" --repo Jamble-Live-Shopping/Jamble-iOS --limit 10

# Tertiary: search by screen name (VC suffix)
gh search code "CreateProductViewController" --repo Jamble-Live-Shopping/Jamble-iOS --limit 5
```

Example queries that worked during the first session:
- `"Pending Application"` → found 5 files all using `UIAlertController` (copy-pasted, we took the first)
- `"Apply to go Live"` → `ProfileSettingsV2ViewController.swift`
- `"Real-time offers"` → `ShowSaleType.swift` (the enum with all sale types)
- `"SELL_MODE"` → `CreateProductViewController.swift` + `SellModeDefaultCell.swift` (the cell renderer)

## Read the file

```bash
gh api repos/Jamble-Live-Shopping/Jamble-iOS/contents/<path> --jq '.content' | base64 -d
```

## What to extract, the mandatory checklist

From each Swift file you open, pull:

### Text strings (via `String(localized: "...")`)
- Screen title
- Section headers
- Row titles, subtitles
- Button labels
- Placeholder text
- Alert titles and messages

**For every EN string, also extract its pt-BR value from `Jamble/RESOURCES/Localizable.xcstrings`.** Workers have repeatedly shipped pt-BR mockups with EN literals ("My Wallet" in pt-BR mockup instead of "Minha carteira"). This is auto-reject at Step 10 visual fidelity.

```bash
python3 -c "
import json
d=json.load(open('/Users/aymardumoulin/Projects/Jamble-iOS/Jamble/RESOURCES/Localizable.xcstrings'))
for k in ['My Wallet','Withdraw','Bank Details','Payouts History','Update','Pending','Completed','Processing','Failed']:
    loc=d['strings'].get(k,{}).get('localizations',{})
    pt=loc.get('pt-BR',{}).get('stringUnit',{}).get('value')
    print(f'{k!r:25} -> pt-BR={pt!r}')
"
```

Record both locales in `code-notes-boxN.md` (see example below).

### Styling
- Font sizes and weights (look for `.systemFont(ofSize: X, weight: .semibold)`)
- Colors (look for `UIColor.customPurple`, `UIColor.customBlue900`, etc., cross-reference with [design-system.md](design-system.md))
- Corner radius
- Padding / constraints (`.topAnchor.constraint(..., constant: 12)`)
- Border width/color

### Structural pieces
- Component type (`UICollectionViewCell`, `UIAlertController`, `UIStackView`, custom view)
- Subviews and their layout relationship
- Conditional states (selected / unselected / pending / error)

### Icons (`UIImage(named: "...")`)
- Note every icon name; you'll download the SVG in Step 3
- Path convention: `Jamble/RESOURCES/Assets.xcassets/icon/<name>.imageset/<name>.svg`

## Document your findings

In the working folder, create `code-notes-boxN.md` with the extraction:

```markdown
# Box 4, Sell Mode

**File**: Jamble/PRODUCT/Views/Components/SellModeDefaultCell.swift
**Component type**: UICollectionViewCell (custom)
**Triggered in**: CreateProductViewController.swift, section `.SELL_MODE`

## Text (from ShowSaleType.swift, pt-BR from xcstrings)
- Title "Real-time offers" / "Ofertas em tempo real" (case `.AUCTION`), subtitle "The last bidder wins at the end of the time." / "O último a ofertar ganha no fim do tempo."
- Title "Sudden Death" / "Morte súbita", subtitle "No added time, even if someone bids." / "Sem tempo adicional, mesmo se alguém ofertar."
- Title "Buy It Now" / "Compre agora", subtitle "Offer a discount on an item during a limited time." / "Ofereça um desconto em um item por tempo limitado."

## Layout
- Icon 24x24, tinted `customBlue500` (#828CA2), leading 16
- Title: `.systemFont(ofSize: 17, weight: .semibold)`, color `customBlack`
- Subtitle: `.systemFont(ofSize: 13, weight: .regular)`, color `customBlue400` (#A0A7B7)
- Radio: 18x18 circle, border 1.5px
  - Unselected: `customBlue400` border, no fill
  - Selected: `customBlue900` (#162233) border + 10x10 `customBlue900` filled inner dot
- Top padding 12, horizontal padding 16

## Conditional state (selected)
- Expands to show text fields (UIStackView, axis .horizontal, spacing 16)
  - Auction: Start price, Timer (seconds)
  - Buy It Now: Price, Flash sale toggle (optionally: Discount, Timer)

## Icons to download
- icon-real-time-offer.svg
- sell-mode-sudden-death.svg
- sell-mode-buy_it_now.svg
- sell-mode-giveaway.svg
```

These notes become the contract for Step 3 (HTML building).

## When there's no iOS code (webview, Android-only)

Some screens, notably the "Apply to Go Live" form, are rendered as an embedded WebView loading a URL (`AppLinks.applyToGoLive()`). In that case:

- Skip iOS code lookup
- Open the webview URL in a browser, screenshot the real page
- Use the screenshot directly OR rebuild a simplified mockup based on what the webview shows

Note these cases clearly in `code-notes-boxN.md` so the batch pipeline doesn't waste time searching.

## Golden rule

**Never invent copy.** If the ASCII writer put "Sell your item!" but the code says "List Product", use "List Product". The help article should match what sellers actually see in the app, character-for-character.
