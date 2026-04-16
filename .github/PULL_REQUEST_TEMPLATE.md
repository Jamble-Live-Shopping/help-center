# Pull Request

## What changed

<!-- One line summary. Example: "Fix typo in 'choose-quantities' FAQ" or "Add new article 'Referral Program'" -->

## Articles affected

<!-- List the article slugs touched by this PR -->
- [ ] articles/<slug>

## Type

- [ ] Typo / copy edit
- [ ] Content update (new info, corrected info)
- [ ] New article
- [ ] Structural change (metadata, slug, collection)
- [ ] Infra (process/, scripts/, workflows/)

## Editorial checks (author fills before requesting review)

- [ ] pt-BR edited first, EN mirrored
- [ ] Zero em-dashes / en-dashes
- [ ] Description ≤ 140 characters per locale
- [ ] Currency correct (`R$` in pt-BR, `$` in EN)
- [ ] No "auction" / "leilão"
- [ ] Every image has alt text
- [ ] `metadata.yml` valid (CI will re-check)

## Code fidelity (for claims about app behavior)

- [ ] Claims verified against iOS / Android source (see `process/10-fact-check-code.md`)
- [ ] Audit report updated at `articles/<slug>/audit/code-audit.md`

## Content safety

- [ ] No PII, no internal system names, no competitor names (see `process/11-fact-check-content.md`)
- [ ] Audit report updated at `articles/<slug>/audit/content-audit.md`

## Compliance gate

- [ ] `articles/<slug>/audit/compliance.md` exists and shows ALL PASS

## Preview

<!-- Paste a screenshot of the key change, especially if visual. Helps reviewers. -->
