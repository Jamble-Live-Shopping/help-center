# Contributing to the Jamble Help Center

Every change goes through a pull request. No direct pushes to `main`. Intercom is a downstream mirror and does not accept direct edits from the UI anymore.

## Prerequisites

```bash
git clone https://github.com/Jamble-Live-Shopping/help-center.git
cd help-center
npm ci
```

For local sync testing (optional):
```bash
export INTERCOM_TOKEN="<your Intercom Personal Access Token>"
```

## Edit an existing article

1. Find the article in `articles/<slug>/`. Slug matches the Intercom URL slug.
2. Edit `pt-br.md` (primary source) first. Then mirror changes to `en.md`.
3. Update `metadata.yml` if the title or description changed.
4. Open a PR. Fill the PR template. Request review from a teammate (or Aymar by default).
5. On merge, the GitHub Action syncs the changes to Intercom in under a minute.

## Add a new article

1. Create `articles/<slug>/` with `metadata.yml`, `pt-br.md`, and `en.md`.
2. Follow the 12-step pipeline in `process/README.md`.
3. Upload mockup PNGs to `assets/mockups/<slug>__<screen>.png` if the article has UI screenshots.
4. Reference images from markdown as `![alt](./assets/mockups/<slug>__<screen>.png)`. The `md-to-html.js` script rewrites relative paths to absolute `raw.githubusercontent.com` URLs.
5. Run the full audit (code, content, compliance). Commit the audit reports under `articles/<slug>/audit/`.
6. Open a PR.

## Metadata format

```yaml
intercom_id: 14288094
slug: choose-quantities-when-listing-products
collection_id: 19177935
default_locale: pt-br
locales:
  pt-br:
    title: Escolha as Quantidades ao Listar Produtos
    description: ...
  en:
    title: Choose Quantities When Listing Products
    description: Set how many units you have per listing...
state: published
author_id: 7980507
reviewers:
  - aymar
last_sync: 2026-04-16T10:47:45Z
```

Rules:
- `intercom_id` never changes once the article is published
- `slug` must match the Intercom URL slug exactly, it is how the Intercom link survives renames
- `default_locale` is `pt-br` per the language priority policy
- `state` is `published` or `draft`

## Editorial rules (enforced by CI)

- Zero em-dashes (U+2014) or en-dashes (U+2013). Use commas
- Description ≤ 140 characters per locale
- Currency: `R$` in pt-BR, `$` in EN. Never `R$` in an EN body, never `$` in a pt-BR body
- Never "auction" (EN) or "leilão" (pt-BR). Use "Real-time offers" (EN) / "Ofertas em tempo real" (pt-BR)
- Every image has a descriptive `alt`
- No `<table>` that breaks on mobile. 2-column becomes a bullet list. 3+ columns becomes a PNG mockup

Full editorial doc: [process/08-editorial-quality.md](./process/08-editorial-quality.md).

## Review checklist

The PR author runs the compliance gate before requesting review. Reviewers check:

- [ ] Code claims verified against iOS or Android source (`process/10-fact-check-code.md`)
- [ ] No PII / internal system names leaked (`process/11-fact-check-content.md`)
- [ ] Compliance gate at `articles/<slug>/audit/compliance.md` shows all PASS
- [ ] pt-BR and EN say the same thing, no drift
- [ ] Images exist and load (CI validates this)
- [ ] `metadata.yml` is valid (CI validates this)

## Emergency rollback

If a merge pushes a bad article to Intercom:

```bash
git revert <commit-sha>
git push origin main
```

The Action re-runs on the revert commit and restores the previous body. No manual Intercom edit needed.

## Questions

Ping Aymar on Slack, or open an issue in this repo.
