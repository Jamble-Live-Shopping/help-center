# Jamble Design System (extracted from iOS/Android source)

**Source of truth**: Android `Colors.kt` (primitive palette), iOS `Colors.swift` (semantic aliases matched within rounding). Use this file, not Figma, not guesses.

---

## Primitive palette

```css
/* Gray */
--gray-950: #0C131D;    /* darkest / dark theme bg */
--gray-900: #162233;    /* content.primary */
--gray-800: #2E3C52;
--gray-700: #54627A;
--gray-600: #6B7A92;    /* content.secondary */
--gray-500: #828CA2;
--gray-400: #A0A7B7;    /* content.tertiary, borders */
--gray-300: #BDC2CD;    /* content.disabled */
--gray-200: #DADDE3;
--gray-100: #E9EAEF;    /* bg.tertiary */
--gray-50:  #F9FAFC;    /* bg.secondary */

/* Brand (Purple), the Jamble identity */
--brand-500: #7E53F8;   /* PRIMARY BRAND, default purple buttons */
--brand-600: #7337F0;   /* pressed state */

/* Semantic */
--red-600:   #D92C20;   /* negative / error */
--red-500:   #F04437;   /* live indicator */
--green-500: #17B169;   /* positive */
--yellow-400:#FCB022;   /* warning */
--white:     #FFFFFF;
--black:     #000000;
```

---

## Semantic tokens (light theme, what you'll use)

```css
/* Content (text, icons) */
--content-primary:    #162233;  /* main text */
--content-secondary:  #6B7A92;  /* secondary text */
--content-tertiary:   #A0A7B7;  /* labels, subtle text */
--content-disabled:   #BDC2CD;
--content-brand:      #7E53F8;  /* brand accents */

/* Background */
--bg-primary:         #FFFFFF;  /* cards, phone frames */
--bg-secondary:       #F9FAFC;  /* page backgrounds */
--bg-tertiary:        #E9EAEF;  /* secondary buttons, inputs */
--bg-inverse:         #0C131D;  /* dark buttons (deprecated for primary CTA, use brand) */
--bg-brand:           #7E53F8;  /* primary CTA */

/* Border */
--border-primary:     #BDC2CD;
--border-secondary:   #DADDE3;
--border-tertiary:    #E9EAEF;
--border-selected:    #162233;  /* radio/checkbox selected */
```

---

## Typography

```css
/* Font stack, iOS uses SF Pro Display (system), Android uses SF Pro Display */
font-family: -apple-system, "SF Pro Display", BlinkMacSystemFont, system-ui, sans-serif;

/* Title (custom Patron font on iOS, SF Pro Bold on Android, use system for mockups) */
--title-s:    font-size: 24px; line-height: 32px; font-weight: 500; letter-spacing: -0.01em;
--title-xs:   font-size: 20px; line-height: 28px; font-weight: 600; letter-spacing: -0.01em;

/* Body */
--body-l:     font-size: 18px; line-height: 28px; font-weight: 400;
--body-m:     font-size: 16px; line-height: 24px; font-weight: 400;
--body-s:     font-size: 14px; line-height: 20px; font-weight: 400;
--body-xs:    font-size: 12px; line-height: 16px; font-weight: 400;

/* iOS screen titles are typically 17pt semibold (600), subtitles 13pt regular (400) */
```

---

## Buttons

All buttons are pill-shaped (fully rounded, `border-radius = height/2`). Full width is the default for modal / bottom sheet contexts.

```css
/* Sizes */
--btn-s:  height: 32px; border-radius: 16px; font: 12px/16px 600;
--btn-m:  height: 40px; border-radius: 20px; font: 14px/20px 600;
--btn-l:  height: 48px; border-radius: 24px; font: 16px/24px 600;
--btn-xl: height: 56px; border-radius: 28px; font: 18px/28px 600;

/* Android JambleButton default: border-radius: 28px, height: 50px */

/* Variants */
.btn-brand {        /* PRIMARY, use purple */
  background: #7E53F8;
  color: #FFFFFF;
}
.btn-brand:active { background: #7337F0; }

.btn-secondary {    /* light gray */
  background: #E9EAEF;
  color: #162233;
}
.btn-secondary:active { background: #DADDE3; }

.btn-inverse {      /* dark / navy, less common now */
  background: #0C131D;
  color: #FFFFFF;
}
```

**Rule**: primary CTA = purple (`#7E53F8`). Navy `#0C131D` is legacy / used sparingly. When in doubt, purple.

---

## Radio buttons (from `SellModeDefaultCell.swift`)

```css
.radio-outer {
  width: 18px; height: 18px;
  border-radius: 50%;
  border: 1.5px solid #A0A7B7;  /* customBlue400, unselected */
}
.radio-outer.selected {
  border-color: #162233;         /* customBlue900, selected */
}
.radio-inner {
  width: 10px; height: 10px;
  border-radius: 50%;
  background: #162233;           /* customBlue900 fill */
}
```

**Note**: radio selection uses **navy**, not brand purple. This is the iOS convention. Only primary CTAs use brand purple.

---

## Spacing scale

```css
--space-xs:  4px;
--space-s:   8px;
--space-m:   12px;
--space-l:   16px;
--space-xl:  24px;
--space-2xl: 28px;
--space-3xl: 32px;
```

## Border radius

```css
--radius-card:    12px;  /* content cards, grouped cells */
--radius-dialog:  16px;  /* bottom sheets, alerts */
--radius-phone:   24px;  /* phone frame wrapper */
--radius-frame:   20px;  /* outer gray frame wrapper for Intercom */
--radius-btn:     height/2 (pill);
```

## Shadow (phone frame)

```css
box-shadow: 0 2px 20px rgba(126,83,248,0.08);  /* subtle purple tint */
```

---

## Special components

**UIAlertController (iOS native)**, used for dialogs like "Pending Application":
- Width: 270px
- Background: `rgba(255,255,255,0.95)` with backdrop blur
- Border radius: 14px
- Title: 17px semibold
- Message: 13px regular
- Buttons: separated by 0.5px hairline, centered
- Button text color: `.default` = system blue `#007AFF`, unless overridden via `setValue(UIColor.customPurple, forKey: "titleTextColor")` → `#7E53F8`

**Photo selector (`ShowFormScreen.kt`, `CreateProductViewModel.swift`)**:
- Upload box: aspect ratio 9:16, max height 220px, `background: #F9FAFC`, `border: 1px solid #BDC2CD`, `border-radius: 12px`
- Thumbnail slots: square, `border-radius: 8px`, numbered badge top-left (purple circle 16px, white 9px bold text)
- Add slot: 1.5px dashed `#C7C7CC`, transparent bg, `+` sign 22px

---

## Real icon assets (download from iOS repo)

Path prefix: `Jamble-Live-Shopping/Jamble-iOS/contents/Jamble/RESOURCES/Assets.xcassets/icon/`

Common seller-center icons:
- `icon-real-time-offer.svg` (Real-time offers / Auction)
- `sell-mode-sudden-death.svg`
- `sell-mode-buy_it_now.svg`
- `sell-mode-giveaway.svg`
- `settings_apply_live` (Apply to go Live row icon)
- `icon-flash.svg` (flash sale)
- `icon-people.svg`, `icon-badge.svg`, `icon-arrow-down.svg`

**How to download**:
```bash
gh api repos/Jamble-Live-Shopping/Jamble-iOS/contents/Jamble/RESOURCES/Assets.xcassets/icon/<name>.imageset/<name>.svg --jq '.content' | base64 -d > icon.svg
```

**How to embed in HTML**: inline as `<img src="data:image/svg+xml;base64,...">`, this way the mockup is self-contained and the screenshot bakes in the icon without external fetches.

**Tinting**: icons ship with fill `#828DA2` or `#6C7B93` (gray). Do NOT retint, match the source.
