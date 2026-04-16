# Step 13, Template library

**Goal**: 10 reusable HTML mockup templates that cover ~75% of the ASCII boxes across the seller center. Haiku classifies each ASCII block into one of these, extracts the content fields, and a renderer fills the template deterministically.

**Source**: extracted from the validated pilots 14288093 (How to List Products), 14288094 (Choose Quantities), 14288153 (Seller Statements).

## Template index

| ID | File | When to use | Required content fields | iOS source |
|----|------|-------------|-------------------------|-----------|
| `settings-row-list` | `settings-row-list.html` | A list of settings-style rows with icon + label inside a card, optionally grouped under a section header | `section_title`, `rows: [{icon, icon_bg, label, dimmed?}]` | `SettingCell` |
| `alert-dialog` | `alert-dialog.html` | iOS native UIAlertController (title + message + 2 buttons, one primary purple) | `title`, `message`, `primary_label`, `secondary_label?` | `UIAlertController` |
| `empty-state-cta` | `empty-state-cta.html` | Empty list page with title + subtitle + full-width purple CTA | `title`, `subtitle?`, `cta_label` | `ShowHostProductListViewController` empty state |
| `radio-picker` | `radio-picker.html` | Multi-option picker with radio dots, icon per option, subtitle per option | `title`, `options: [{icon, name, subtitle, selected?}]` | `SellModeDefaultCell` |
| `photo-grid` | `photo-grid.html` | Grid of photo thumbnails with numbered purple badges + add slot | `title?`, `photos: [url or placeholder]`, `max_photos` | `SelectPhotoCell` grid |
| `button-cta` | `button-cta.html` | Standalone primary purple pill button | `label` | `JambleButton` brand |
| `stepper-input` | `stepper-input.html` | Title + horizontal [minus] value [plus] stepper inside a card | `title`, `value`, `min?`, `max?` | `CreateProductQuantityCell` |
| `error-toast` | `error-toast.html` | White toast with red circle+exclamation icon, bold title + subtitle | `title`, `subtitle` | `JambleIndicatorView` state `.error` |
| `wallet-nav` | `wallet-nav.html` | Top nav bar with back chevron + title + 1-2 right icons, balance card below with amount + CTA, optional pending card | `nav_title`, `right_icons: [help?, clock?]`, `balance_label`, `balance_amount`, `cta_label`, `pending?` | `SellerWalletView`, `JambleNavigationBar` |
| `list-with-status` | `list-with-status.html` | Card with section title + list of rows showing ID + amount + status (color-coded) + date | `section_title`, `rows: [{id, amount, status, status_color, date}]` | `PayoutHistoryCellView` |
| `form-layout` | `form-layout.html` | Form screen with title + multiple input fields (text / dropdown / upload / textarea) + submit button | `title`, `fields: [{label, type, placeholder?}]`, `submit_label` | Show creation form, shipping address form |
| `auth-screen` | `auth-screen.html` | Welcome/onboarding with title + 2-3 stacked buttons + optional secondary link | `title`, `buttons: [{label, style}]`, `secondary_link?` | Welcome, Login, Signup |
| `text-with-actions` | `text-with-actions.html` | Title + body paragraph(s) + one or more action buttons | `title`, `body`, `buttons: [{label, style}]` | "Become a Live Seller" CTA, promotional screens |

## Classification hints for Haiku

When classifying an ASCII block, look for these patterns:

- **Rows with `▶` or chevrons + label**, often grouped under "Settings" or a section header → `settings-row-list`
- **Rounded rectangle with centered "OK" button or 2 buttons stacked** → `alert-dialog`
- **Central vertical layout with title + subtitle + single button at bottom** → `empty-state-cta`
- **Options with `○` or `●` circles**, each with a subtitle → `radio-picker`
- **Grid of boxes or thumbnails, often labeled 1/2/3** → `photo-grid`
- **Single button centered (often "Add Listing", "Start", "Continue")** → `button-cta`
- **`[ - ] N [ + ]` horizontal pattern** → `stepper-input`
- **Pill-shaped with icon left + short text right, often with "Oops" or error language** → `error-toast`
- **Top title + balance/amount + "Withdraw" or similar CTA below**, may include clock/help icons → `wallet-nav`
- **List of rows each showing ID + amount on one line and status/date on another** → `list-with-status`

## If nothing matches

Haiku returns `template_id: null` with `unmatched_reason` and the raw ASCII. A human picks up these edge cases manually. Target: <20% of blocks unmatched.

## Adding a new template

1. Find an ASCII pattern that repeats and doesn't fit any of the 10 above.
2. Build the HTML mockup with the same phone frame wrapper as existing templates (see `process/03-html-template.md` for the shared CSS base).
3. Save as `process/templates/<id>.html`.
4. Add a row to the table above with required fields + iOS source reference.
5. Update the classification hints with the pattern to detect.
6. Add a render function in `scripts/render-mockups.py`.

## Rendering contract

Each template file is a complete self-contained HTML document with example content. The `render-mockups.py` script has a matching function per template that takes a `content` dict and returns filled HTML. The file itself acts as the reference for what the filled output should look like.

Filename convention for produced PNGs: `<article-slug>__<screen-name>.png`, written to `assets/mockups/`. See `process/09-screenshot-framing.md` for the full naming rule.
