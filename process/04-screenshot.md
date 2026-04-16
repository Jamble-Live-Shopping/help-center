# Step 4, Render HTML to PNG

**Goal**: convert `prod-boxN.html` into `prod-boxN.png` at retina resolution, with the outer gray rounded frame injected automatically.

## Prerequisites

- Node.js 18+
- Puppeteer (auto-installed by `npx`): `npx puppeteer browsers install chrome`
  - Chrome binary cached at `~/.cache/puppeteer/chrome/`

## The script

Save as `/tmp/screenshot-mockups.mjs`:

```javascript
import puppeteer from 'puppeteer';
import { resolve } from 'path';

const dir = process.argv[2];
const files = process.argv.slice(3); // ['prod-box1', 'prod-box2', ...]

const browser = await puppeteer.launch({ headless: true });

for (const f of files) {
  const page = await browser.newPage();
  await page.setViewport({ width: 400, height: 800, deviceScaleFactor: 3 });
  await page.goto(`file://${resolve(dir, f + '.html')}`, { waitUntil: 'networkidle0' });

  // Inject the outer gray rounded frame around the phone card
  await page.evaluate(() => {
    const phone = document.querySelector('.phone') || document.querySelector('.alert');
    if (!phone) return;
    const wrapper = document.createElement('div');
    wrapper.style.cssText = 'background: #F0F1F5; border-radius: 20px; padding: 24px; display: inline-block;';
    const parent = phone.parentElement;
    parent.insertBefore(wrapper, phone);
    wrapper.appendChild(phone);
  });

  // Get wrapper bounding box for tight crop
  const wrapperBox = await page.evaluate(() => {
    const phone = document.querySelector('.phone') || document.querySelector('.alert');
    const wrapper = phone?.parentElement;
    if (!wrapper) return null;
    const r = wrapper.getBoundingClientRect();
    return { x: r.x, y: r.y, width: r.width, height: r.height };
  });

  if (wrapperBox) {
    await page.screenshot({
      path: resolve(dir, f + '.png'),
      clip: {
        x: Math.max(0, wrapperBox.x),
        y: Math.max(0, wrapperBox.y),
        width: wrapperBox.width,
        height: wrapperBox.height
      },
      omitBackground: true
    });
  } else {
    await page.screenshot({ path: resolve(dir, f + '.png'), omitBackground: true });
  }

  console.log(`${f}.png saved`);
  await page.close();
}

await browser.close();
```

## Run it

```bash
MOCKUP_DIR="<path to folder with prod-*.html>"
node /tmp/screenshot-mockups.mjs "$MOCKUP_DIR" prod-box1 prod-box2 prod-box4 prod-box5
```

## Design rationale for the outer frame

The phone card alone looks abrupt when embedded in an Intercom article body, it floats on the white article background with no visual anchor. The gray rounded frame (`#F0F1F5`, `border-radius: 20px`, `padding: 24px`) gives the mockup a clear "screenshot boundary" and matches the help center article's light-gray feel.

The frame is injected at screenshot time (not in the HTML) because:
- The phone card HTML stays reusable for other contexts (internal docs, design reviews) where no frame is needed
- The frame styling is centralized in one place (the script), so a change propagates to all future mockups

## Quality checklist (inspect the PNG before Step 5)

- [ ] Retina quality (no blurry text), `deviceScaleFactor: 3` gives ~900px for a 320px phone frame
- [ ] Outer gray frame present, rounded corners visible
- [ ] Phone card has its purple-tinted shadow
- [ ] No scrollbar visible (page content fits in viewport)
- [ ] No overflow / cut-off text
- [ ] Icons render as actual SVGs (not broken image placeholders)

If an icon is broken, the base64 SVG embed in the HTML is corrupted or the MIME type is wrong. Re-encode and retry.

## Batch runs

For 228 boxes across 100 articles, this script is trivial to parallelize, just pass all file basenames:

```bash
ls "$MOCKUP_DIR"/prod-box*.html | sed 's/.*prod-/prod-/;s/.html//' | xargs node /tmp/screenshot-mockups.mjs "$MOCKUP_DIR"
```

On a 2023 MacBook, single-threaded Puppeteer does ~1 screenshot/second. 228 boxes ≈ 4 minutes.
