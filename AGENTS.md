# AI agent instructions

This file is the canonical entry point for any AI agent working in this repository. Read it before making changes.

## Project purpose

This public repository is the source of truth for Jamble Help Center articles. Intercom is only the publication surface. Article content, translations, mockup sources, rendered assets, and audit evidence belong in GitHub.

## Required reading order

1. `AGENTS.md` (this file): non-negotiable safety and content rules.
2. `HANDOVER.md`: dated operational status, known gaps, and ownership checklist.
3. `CONTRIBUTING.md`: branch, pull request, and review workflow.
4. `process/00-RUNBOOK.md`: canonical article-production workflow.
5. The numbered `process/` document for the phase you are changing.
6. `process/15-intercom-sync.md` only when a human explicitly asks about publication.

If two process documents disagree, the more specific numbered document wins. Nothing overrides the manual publication gate below.

## Non-negotiable safety rules

- This is a public repository. Never commit tokens, `.env` files, user data, private screenshots, internal system names, or non-public product details.
- Never edit an article independently in both GitHub and Intercom. GitHub is canonical.
- Never push directly to `main`, bypass branch protection, force-push shared branches, or merge without the required human review.
- Merging to `main` does **not** publish to Intercom.
- Never add an `on: push` trigger to `.github/workflows/sync-intercom.yml`.
- Never run `scripts/sync-one.sh`, call the Intercom write API, or dispatch the sync workflow unless the human release owner explicitly authorizes publication of one exact article slug in the current task.
- An authorized publication is one slug per workflow run, from `main`, with `confirm=yes`. A broad instruction such as “ship everything” is not sufficiently scoped.
- Until ownership is explicitly updated, Aymar is the release authorizer. A handover of repository maintenance does not silently transfer production-publish authority.
- If code evidence contradicts an article, a feature appears missing, a localized label cannot be verified, or an active risk has no recorded decision, stop and report the evidence. Do not invent a fallback.

## Content contract

- Public articles always have both `pt-br.md` and `en.md`.
- pt-BR is the primary source. EN mirrors the same meaning; currency formatting is the only routine divergence.
- Live iOS code and `Localizable.xcstrings` are the source of truth for behavior, labels, and UI. Do not rely on memory, Figma, or old article copy when code can be checked.
- Use `R$` in pt-BR and `$` in EN. Never leak `R$` into EN or `$` into pt-BR.
- Use “Real-time offers” in EN and “Ofertas em tempo real” in pt-BR. Never use “auction” or “leilão” in public copy.
- Descriptions are at most 140 characters per locale.
- Do not use em dashes (`—`) or en dashes (`–`).
- Every image needs descriptive alt text.
- User-facing Markdown or HTML tables are forbidden because Intercom clips them on mobile. Convert two-column content to a list and three-or-more-column comparisons to a PNG mockup.
- Never invent UI copy, icons, states, product behavior, fee logic, or eligibility rules.
- If an iOS icon exists, use the real asset from `assets/icons-ios/`; do not substitute emoji or a CSS approximation.
- Render mockups at device scale factor 3 and store final PNGs in root `assets/mockups/` using a cache-busting versioned filename.
- Never print base64 or raw image bytes to terminal output. Write binary data to a file and inspect it with `file`, `ls -lh`, or `wc -c`.

## Local setup

A Python virtual environment is an isolated folder for this repository's Python packages.

```bash
git clone https://github.com/Jamble-Live-Shopping/help-center.git
cd help-center
git switch -c codex/<short-topic> origin/main

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
npm ci
```

Create the branch before editing so work cannot accidentally land on `main`.

For product-behavior or UI work, clone `Jamble-Live-Shopping/Jamble-iOS` and export `JAMBLE_IOS_ROOT` to its `Jamble/` directory. If that source is unavailable, report the verification limitation instead of claiming code fidelity.

## Validation commands

For an article with a `flow.yml` contract:

```bash
python scripts/run-help-article.py articles/<slug> --phase plan
python scripts/run-help-article.py articles/<slug> --phase validate
```

The `validate` phase is the gate. `plan`, `checklist`, and `writer-packet` are informational and cannot prove readiness.

When changing factory scripts, validators, templates, or workflow rules, also run:

```bash
python scripts/test-article-factory.py
python scripts/test-batch-coordinator.py
python scripts/replay-golden-articles.py
```

Do not claim the entire repository is green based on a changed-article check. The dated full-repository baseline and known red articles are recorded in `HANDOVER.md`.

## Expected article change

An article rewrite normally contains:

- `articles/<slug>/flow.yml`
- `articles/<slug>/metadata.yml`
- `articles/<slug>/pt-br.md` followed by the mirrored `en.md`
- paired `mockup-sources/*__pt-br.html` and `*__en.html` files when UI visuals are required
- matching versioned PNGs in `assets/mockups/`
- the code, content, and compliance audit triplet under `articles/<slug>/audit/`

Before requesting review, inspect `git diff`, run the relevant validator, and fill the pull request template with risks and evidence. A green validator does not authorize a production publish.
