# Step 3, Build the HTML mockup

**Goal**: convert the ASCII + code notes into a self-contained HTML file (`prod-boxN.html`) that renders as a mobile screen mockup, styled to match the real iOS component.

## Architecture of a mockup file

Every mockup file has the same macro structure:

```
<html>
  <head>
    <style>
      [shared reset + body + phone wrapper]
      [component-specific styles]
    </style>
  </head>
  <body>
    <div class="phone">
      [the component, with inline content]
    </div>
  </body>
</html>
```

At screenshot time (Step 4), a gray outer frame is injected programmatically around the phone. Do NOT add it in the HTML, the screenshot script handles it.

## Shared CSS base

Every mockup starts from this base. Copy-paste it verbatim into every `prod-boxN.html`:

```css
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, "SF Pro Display", BlinkMacSystemFont, system-ui, sans-serif;
  background: #F9FAFC;
  display: flex;
  justify-content: center;
  padding: 12px;
}

.phone {
  width: 320px;
  background: #FFFFFF;
  border-radius: 24px;
  padding: 16px 0 12px;
  box-shadow: 0 2px 20px rgba(126,83,248,0.08);
  border: 1px solid #E9EAEF;
  overflow: hidden;
}

/* Standard section header (iOS grouped table section) */
.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #A0A7B7;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 8px 20px 10px;
}
```

## Pattern library

Below are the canonical patterns for the 4 most common screen types. Each matches a real iOS component. Use these as building blocks, do not invent new patterns without checking the code first.

### Pattern A, Settings row (grouped table)

Match: `UICollectionView` with `SettingCell`, "IMPORTANT" / "SELL" sections.

```css
.section-header { font-size: 13px; color: #6D6D80; text-transform: uppercase; padding: 8px 20px 6px; letter-spacing: -0.08px; }
.group { background: #FFFFFF; margin: 0 12px; border-radius: 12px; overflow: hidden; border: 1px solid #E9EAEF; }
.row { display: flex; align-items: center; padding: 12px 16px; min-height: 44px; }
.row-icon { width: 30px; height: 30px; border-radius: 7px; background: #7E53F8; display: flex; align-items: center; justify-content: center; color: white; margin-right: 12px; }
.row-label { font-size: 17px; color: #000; flex: 1; line-height: 22px; }
```

### Pattern B, UIAlertController (native iOS alert)

Match: `.alert` style dialogs. Used for "Pending Application", confirmations, limit warnings.

```css
body { background: rgba(0,0,0,0.08); align-items: center; min-height: 380px; }
.alert { width: 270px; background: rgba(255,255,255,0.97); backdrop-filter: blur(20px); border-radius: 14px; overflow: hidden; text-align: center; }
.alert-body { padding: 20px 16px 0; }
.alert-title { font-size: 17px; font-weight: 600; color: #000; line-height: 22px; }
.alert-msg { font-size: 13px; color: #000; line-height: 18px; margin-top: 8px; }
.alert-btns { margin-top: 20px; border-top: 0.5px solid rgba(60,60,67,0.2); }
.alert-btn { display: block; width: 100%; padding: 11px 8px; font-size: 17px; border: none; background: transparent; border-bottom: 0.5px solid rgba(60,60,67,0.2); }
.alert-btn:last-child { border-bottom: none; }
.alert-btn.purple { color: #7E53F8; }  /* .default with titleTextColor override */
.alert-btn.blue { color: #007AFF; }     /* .default system blue */
```

### Pattern C, Radio cell with icon + subtitle (SellModeDefaultCell)

Match: `UICollectionViewCell` custom selection cells with expand-on-select.

```css
.cell { display: flex; align-items: center; padding: 12px 20px; }
.cell-icon { width: 24px; height: 24px; margin-right: 16px; flex-shrink: 0; }
.cell-icon img { width: 24px; height: 24px; }
.cell-content { flex: 1; }
.cell-title { font-size: 17px; font-weight: 600; color: #000; line-height: 22px; }
.cell-sub { font-size: 13px; color: #A0A7B7; line-height: 18px; margin-top: 1px; }
.radio { width: 18px; height: 18px; border-radius: 50%; border: 1.5px solid #A0A7B7; margin-left: 16px; display: flex; align-items: center; justify-content: center; }
.cell.on .radio { border-color: #162233; }
.radio-dot { width: 10px; height: 10px; border-radius: 50%; background: #162233; display: none; }
.cell.on .radio-dot { display: block; }
.expand { padding: 4px 20px 12px; display: flex; gap: 12px; }
.field { flex: 1; height: 40px; background: #F9FAFC; border: 1px solid #DADDE3; border-radius: 8px; display: flex; align-items: center; padding: 0 12px; font-size: 14px; color: #A0A7B7; }
.divider { height: 0.5px; background: #E9EAEF; margin: 0 20px; }
```

### Pattern D, Photo picker grid

Match: create-product photos section, create-show image upload.

```css
.grid-wrap { padding: 0 20px; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; background: #F9FAFC; border: 1px solid #E9EAEF; border-radius: 12px; padding: 12px; }
.slot { aspect-ratio: 1; border-radius: 8px; background: #F2F2F7; display: flex; align-items: center; justify-content: center; position: relative; }
.slot.add { border: 1.5px dashed #C7C7CC; background: transparent; }
.slot.add .plus { font-size: 22px; color: #C7C7CC; font-weight: 300; }
.badge { position: absolute; top: 3px; left: 3px; width: 16px; height: 16px; border-radius: 50%; background: #7E53F8; color: white; font-size: 9px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.hint { font-size: 13px; color: #8E8E93; padding: 8px 0 0; text-align: center; }
```

## Embedding real iOS icons

For any mockup that includes an icon referenced in the code, download it as SVG and embed inline as a base64 data URI:

```bash
# Download
gh api repos/Jamble-Live-Shopping/Jamble-iOS/contents/Jamble/RESOURCES/Assets.xcassets/icon/<name>.imageset/<name>.svg \
  --jq '.content' | base64 -d > <name>.svg

# Embed in HTML
SVG_B64=$(base64 -i <name>.svg | tr -d '\n')
# Then in HTML: <img src="data:image/svg+xml;base64,$SVG_B64" />
```

**Why inline, not external URL**: at screenshot time Puppeteer loads the HTML via `file://`, external fetches can fail. Inline data URIs are self-contained and deterministic.

**Don't retint**: icons ship with their designed colors (`#828DA2`, `#6C7B93`). Changing them breaks visual parity with the app. If the icon looks too dark/light in the mockup, the source icon is wrong and needs a design fix, not a CSS hack.

### Binary data hygiene, NEVER echo base64 to stdout

Claude Code auto-detects data-URIs and raw image bytes in command output and tries to attach them to the conversation. A malformed or truncated blob is rejected by the API with `400 Could not process image`, and that error payload is then frozen into the session history, poisoning every subsequent turn. The session becomes unrecoverable. Real incident, 2026-04-16.

Safe patterns:

```bash
# OK, redirect to file
gh api repos/.../icon.svg --jq '.content' | base64 -d > /tmp/icon.svg
base64 -i /tmp/icon.svg | tr -d '\n' > /tmp/icon.b64

# OK, size check on the file, not on contents
wc -c /tmp/icon.b64

# OK, use the variable inside a heredoc that writes to a file
cat > prod-box1.html <<EOF
<img src="data:image/svg+xml;base64,$(cat /tmp/icon.b64)" />
EOF
```

Forbidden patterns:

```bash
# NEVER, leaks base64 blob to stdout
echo "data:image/svg+xml;base64,${SVG_B64}"
cat /tmp/icon.b64
echo $SVG_B64 | head -c 60

# NEVER, pipes decoded bytes to stdout
gh api repos/.../icon.png --jq '.content' | base64 -d
```

Rule: any blob >500 chars that could be image data goes to a FILE, never to stdout. Applies to PNG, SVG, JPG, WebP, and any base64 of those. If you need to inspect, inspect the file (`wc -c`, `file <path>`, `ls -la`), never the content.

If a session does get poisoned: it is lost. Start a new session, the file artifacts on disk survive.

## Multilingual mockups: write EN first, then copy to pt-BR

For articles with both locales, produce `<mockup>__en.html` and `<mockup>__pt-br.html`. They MUST be byte-identical except for user-visible text (between tags, in `alt`, in `aria-label`). Same CSS, same DOM, same SVGs, same spacing.

**Workflow**:
1. Write `<mockup>__en.html` fully, render and QA it
2. `cp <mockup>__en.html <mockup>__pt-br.html`
3. Translate ONLY the text content. Do not touch class names, styles, SVG paths, structure, class modifiers
4. Verify via `diff` that only text-bearing lines changed

**Why**: previous batches shipped structurally-different HTMLs (different paddings, missing sections, icons renamed per locale) which look inconsistent side-by-side on the help center.

## Naming and placement

- HTML files: `<mockup>__<locale>.html` in `articles/<slug>/mockup-sources/` (locales `pt-br` and `en`)
- PNG files: `<slug>__<mockup>__<locale>.png` in ROOT `assets/mockups/` — **never** under `articles/<slug>/assets/` (md-to-html resolves `./assets/` against repo root; nested PNGs won't reach raw.githubusercontent)
- One mockup per HTML file
- Always open locally in a browser once before moving to Step 4, the final PNG is deterministic but a bad HTML won't error, it'll just render wrong

## Anti-patterns to avoid

- Do NOT use emoji as UI icons (🚚 truck, ⧉ copy, 🔨, ⚡, 💀, ℹ, 🔍, ←). Always use inline SVG stroke icons, Feather-style, colored with design-system tokens. Emoji are OK **only** for product-image placeholders inside a gradient container (they simulate an uploaded product photo), never for UI chrome.
- Do NOT add `box-shadow`, rounded corners via JS/dynamic CSS. Bake them into the static HTML.
- Do NOT reference external fonts or stylesheets (`@import`, `<link rel=stylesheet>`). Everything inline.
- Do NOT invent subtitles like "Buyers bid against each other" if the code says "The last bidder wins at the end of the time.", copy the code verbatim.
- Do NOT add the outer gray frame in the HTML. The screenshot step injects it.
- Do NOT put EN literals in a `__pt-br.html` file (see "Multilingual mockups" above).
- Do NOT let the pt-BR HTML diverge structurally from the EN HTML (only text should differ).
