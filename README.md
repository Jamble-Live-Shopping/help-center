# Jamble Help Center

Source of truth for the Jamble Help Center on Intercom. Every article lives here as Markdown. Every change goes through a PR. On merge to `main`, the GitHub Action `sync-intercom.yml` pushes the updated articles to Intercom.

> Intercom is a mirror. GitHub is the source of truth. Never edit articles directly in Intercom UI, the next PR will overwrite your changes.

## Repo layout

```
help-center/
├── articles/<slug>/              One folder per article
│   ├── metadata.yml              Intercom ID, locale titles + descriptions
│   ├── pt-br.md                  Body in Brazilian Portuguese (primary source)
│   ├── en.md                     Body in English (mirror of pt-br)
│   ├── mockup-sources/           HTML sources of the PNGs, for traceability
│   └── audit/                    Per-article code-audit / content-audit / compliance reports
├── assets/
│   ├── mockups/                  PNG mockups, served to Intercom via raw.githubusercontent.com
│   └── icons/                    Shared icon pool
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
npm ci
# Edit articles/<slug>/pt-br.md or en.md
git checkout -b fix/<slug>-<what>
git commit -am 'Fix typo in <slug>'
gh pr create
# On merge, the GitHub Action syncs to Intercom in under a minute.
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
- Injection into Intercom via `sync-one.sh` or the Action
- Editorial rules (zero em-dashes, description ≤ 140 chars, currency localization, banned words)
- Fact-check gates (code audit, content audit, compliance)

## Local sync (debug only)

```bash
export INTERCOM_TOKEN="$(cat ~/.intercom_token)"
bash scripts/sync-one.sh articles/choose-quantities-when-listing-products
```

The CI does the same thing on merge, just with the secret injected.
