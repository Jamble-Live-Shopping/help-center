# Jamble Help Center

Source of truth for the Jamble Help Center on Intercom. Every article lives here as Markdown and every change goes through a pull request.

> Intercom is a mirror. GitHub is the source of truth. Never edit articles directly in Intercom UI, the next PR will overwrite your changes.

> **Merging does not publish.** Intercom publication is a separate, manual action for one approved article. See [process/15-intercom-sync.md](./process/15-intercom-sync.md).

## Start here

- Human handover and current status: [HANDOVER.md](./HANDOVER.md)
- AI agent rules: [AGENTS.md](./AGENTS.md)
- Contribution workflow: [CONTRIBUTING.md](./CONTRIBUTING.md)
- Article production entry point: [process/00-RUNBOOK.md](./process/00-RUNBOOK.md)

## Repo layout

```
help-center/
├── AGENTS.md                     Canonical rules for AI coding agents
├── HANDOVER.md                   Dated operational handover and known gaps
├── articles/<slug>/              One folder per article
│   ├── metadata.yml              Intercom ID, locale titles + descriptions
│   ├── flow.yml                  Source, risks, mockup, and validation contract
│   ├── pt-br.md                  Body in Brazilian Portuguese (primary source)
│   ├── en.md                     Body in English (mirror of pt-br)
│   ├── mockup-sources/           HTML sources of the PNGs, for traceability
│   └── audit/                    Per-article code-audit / content-audit / compliance reports
├── assets/
│   ├── mockups/                  PNG mockups, served to Intercom via raw.githubusercontent.com
│   └── icons-ios/                Real shared assets extracted from the iOS app
├── process/                      The 12-step production pipeline (see process/README.md)
├── scripts/
│   ├── md-to-html.js             Markdown → Intercom-ready HTML
│   └── sync-one.sh               Manual sync for a single article
└── .github/
    ├── workflows/sync-intercom.yml
    └── PULL_REQUEST_TEMPLATE.md
```

## Quick start for contributors

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full walkthrough. In short:

```bash
git clone https://github.com/Jamble-Live-Shopping/help-center.git
cd help-center
git switch -c content/<short-topic> origin/main

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
npm ci
# Edit articles/<slug>/pt-br.md or en.md
python scripts/run-help-article.py articles/<slug> --phase validate
git add <files-you-changed>
git commit -m 'Fix typo in <slug>'
git push -u origin HEAD
gh pr create --fill
# On merge, stop. Publishing is a separate approved manual action.
```

## Language priority (policy, see process/)

Jamble is Brazil-only. **pt-BR is the source language**, English is the mirror. Every article is first written in pt-BR with the full production pipeline, then translated to English. This keeps native quality for the primary audience and avoids the "translated from English" feel that hurts sad-reaction rates.

## Pipeline

The full production pipeline (12 steps from ASCII extraction to compliance gate) is in [process/README.md](./process/README.md). It covers:

- Extraction from Intercom article HTML
- iOS code lookup (terminology and visuals = source of truth)
- HTML mobile mockups
- Screenshot to PNG (Puppeteer, retina)
- Hosting in this repo
- Manual, article-scoped publication to Intercom after merge and explicit approval
- Editorial rules (zero em-dashes, description ≤ 140 chars, currency localization, banned words)
- Fact-check gates (code audit, content audit, compliance)

## Local sync (release debugging only)

This writes to production Intercom. Do not run it unless the release owner explicitly authorizes one exact article slug.

```bash
export INTERCOM_TOKEN="$(cat ~/.intercom_token)"
bash scripts/sync-one.sh articles/choose-quantities-when-listing-products
```

Normal pull request CI validates content and does not publish. The canonical production path is the manual GitHub Action documented in [process/15-intercom-sync.md](./process/15-intercom-sync.md).
