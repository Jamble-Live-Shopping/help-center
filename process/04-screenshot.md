# Step 4, Render HTML to PNG

**Goal**: convert each `<mockup>__<locale>.html` into `<slug>__<mockup>__<locale>.png` at retina resolution (DPR 3), with the outer gray rounded frame injected automatically.

## Prerequisites

- Node.js 18+
- Puppeteer (already a repo dep): `npm ci` at the repo root installs it via `package.json`
- Chrome binary auto-installed under `~/.cache/puppeteer/chrome/`

## The canonical script: `scripts/shot-retina.mjs`

Use **only** this script, sequentially, one PNG per invocation:

```bash
node scripts/shot-retina.mjs \
  "/absolute/path/to/articles/<slug>/mockup-sources/<mockup>__<locale>.html" \
  "/absolute/path/to/assets/mockups/<slug>__<mockup>__<locale>.png"
```

It launches Puppeteer with `deviceScaleFactor: 3`, renders the HTML, crops to `.phone`, injects the outer gray frame, writes the PNG, and closes the browser. One process per PNG avoids the Chrome zombie leaks we hit earlier.

## What NOT to use

- **Never `j-playwright.py shot`**: defaults to `device_scale_factor: 1`. PNGs look pixelated when scaled up on the help center page. We re-rendered 40+ PNGs (PR #42, #44) because of this.
- **Never the old `scripts/shot-batch.mjs`**: leaves dozens of orphan Chrome processes on fail, saturates the machine, future renders time out.

## Batch for many mockups

Run the canonical script in a shell loop, sequential (not parallel, not via shot-batch):

```bash
for html in articles/<slug>/mockup-sources/*.html; do
  base=$(basename "$html" .html)
  node scripts/shot-retina.mjs "$(pwd)/$html" "$(pwd)/assets/mockups/<slug>__${base}.png"
done
```

One PNG per second is plenty fast for a 6-mockup article.

## Design rationale for the outer frame

The phone card alone looks abrupt when embedded in an Intercom article body, it floats on the white article background with no visual anchor. The gray rounded frame (`#F0F1F5`, `border-radius: 20px`, `padding: 24px`) gives the mockup a clear "screenshot boundary" and matches the help center article's light-gray feel.

The frame is injected at screenshot time (not in the HTML) because:
- The phone card HTML stays reusable for other contexts (internal docs, design reviews) where no frame is needed
- The frame styling is centralized in one place (the script), so a change propagates to all future mockups

## Quality checklist (mandatory visual QA on EACH PNG before Step 5)

Open each PNG (or use the Read tool) and verify:

- [ ] Retina (width >= 900 px for a 320-340 px phone frame = DPR 3 confirmed)
- [ ] Outer gray frame present, rounded corners visible
- [ ] Phone card has its purple-tinted shadow
- [ ] No scrollbar visible (page content fits in viewport)
- [ ] No overflow / cut-off text
- [ ] Cards have **substantive content** (labels, amounts, rows, buttons), not empty bodies with just a title
- [ ] Q/A and list items use structured divs (row, separator), NOT a single fluid paragraph
- [ ] Icons render as SVGs, no broken-image placeholders, no emoji for UI chrome
- [ ] For `__pt-br.png`: all visible UI text is in Portuguese (no "My Wallet", "Withdraw", "Completed" leaking through)
- [ ] `__pt-br.png` and `__en.png` are visually iso (same layout, same spacing, same components)

A failure on any line here means rebuild the HTML + re-render. Shipping a PNG that fails a check is the single largest source of rework in this pipeline.

If an icon is broken, the base64 SVG embed in the HTML is corrupted or the MIME type is wrong. Re-encode and retry.
