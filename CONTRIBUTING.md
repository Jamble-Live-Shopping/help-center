# Contributing to the Jamble Help Center

Every change goes through a pull request. No direct pushes to `main`. Intercom is a downstream mirror and does not accept direct edits from the UI anymore.

## Prerequisites

```bash
git clone https://github.com/Jamble-Live-Shopping/help-center.git
cd help-center
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
npm ci
```

You do not need an Intercom token to edit or validate content. Production publication is a separate maintainer action.

## Edit an existing article

1. Create a branch from current `origin/main` before editing: `git switch -c content/<short-topic> origin/main`.
2. Find the article in `articles/<slug>/`. Slug matches the Intercom URL slug.
3. Edit `pt-br.md` (primary source) first. Then mirror changes to `en.md`.
4. Update `metadata.yml`, `flow.yml`, mockups, and audits when the change affects them.
5. Run `python scripts/run-help-article.py articles/<slug> --phase validate` when the article has a flow contract.
6. Open a PR, fill the template, and request review from a maintainer.
7. Merge after approval. This does **not** publish to Intercom.

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

If a bad change was merged but not manually published, revert it through a pull request; Intercom is unchanged.

If the change was published, create a revert on a new branch:

```bash
git switch -c revert/<short-topic> origin/main
git revert <commit-sha>
git push -u origin HEAD
gh pr create --fill
```

After the revert PR is reviewed and merged, obtain explicit release approval and manually sync the affected slug again. A revert does not publish automatically.

## Publication

Merging and publishing are intentionally separate. Only a release owner may run the manual workflow, one approved slug at a time with `confirm=yes`. See [process/15-intercom-sync.md](./process/15-intercom-sync.md).

## Questions

Open an issue in this repository or ask a current maintainer.
