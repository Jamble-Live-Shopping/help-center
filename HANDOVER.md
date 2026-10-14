# Help Center handover for Vaimiti

Operational snapshot: **25 August 2026**

## The short version

Repository: <https://github.com/Jamble-Live-Shopping/help-center>

This public repository is the source of truth for Jamble Help Center content. Intercom is a downstream publication surface. Contributors edit pt-BR and EN article files here, prove claims against the live app code, open a pull request, and obtain one human approval.

**A merge does not publish.** Production publication is a separate manual GitHub Actions run for one named article. This separation exists because the previous automatic-on-merge workflow caused an accidental publish on 11 May 2026.

## Ten-minute onboarding

1. Open the repository link and confirm that your GitHub account can create a branch and pull request. Reading is public; contributing requires write access or a fork.
2. Read [`AGENTS.md`](./AGENTS.md), then [`CONTRIBUTING.md`](./CONTRIBUTING.md).
3. For article work, read [`process/00-RUNBOOK.md`](./process/00-RUNBOOK.md). For publication, read [`process/15-intercom-sync.md`](./process/15-intercom-sync.md).
4. Clone and install the local tools:

   ```bash
   git clone https://github.com/Jamble-Live-Shopping/help-center.git
   cd help-center
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements-dev.txt
   npm ci
   ```

   For product-behavior or UI work, also clone the private iOS source and set the validator path:

   ```bash
   git clone https://github.com/Jamble-Live-Shopping/Jamble-iOS.git ../Jamble-iOS
   export JAMBLE_IOS_ROOT="$(cd ../Jamble-iOS/Jamble && pwd)"
   ```

5. Make the first contribution on a branch, never directly on `main`:

   ```bash
   git fetch origin
   git switch -c content/<short-topic> origin/main
   # Edit files, then validate the affected article.
   python scripts/run-help-article.py articles/<slug> --phase validate
   git add <files-you-changed>
   git commit -m "docs: describe the change"
   git push -u origin HEAD
   gh pr create --fill
   ```

## How the system fits together

```text
pt-BR article + EN mirror + flow contract + audit evidence
                         |
                         v
                 Pull request review
                         |
                         v
                  Merge to main
                  (no publication)
                         |
              explicit human release approval
                         |
                         v
       manual GitHub Action, one slug, confirm=yes
                         |
                         v
                  Intercom production
```

Key folders:

| Path | Purpose |
|---|---|
| `articles/<slug>/` | Article bodies, metadata, flow contract, mockup HTML, and audit evidence |
| `assets/mockups/` | Public PNGs loaded by Intercom |
| `assets/icons-ios/` | Real UI assets extracted from the iOS app |
| `process/` | Production rules, design system, validators, and publication runbook |
| `scripts/` | Conversion, rendering, validation, factory, and sync tools |
| `.github/workflows/` | Pull request validation and manual Intercom publication |

## Current repository state

This is a dated baseline, not a promise that the numbers will stay current.

- `main` is protected and requires one approving review.
- 68 article folders are present.
- 22 articles currently have Article Factory `flow.yml` contracts and are covered by the v2 validator.
- Three workflows are active: Article Factory validation, changed-article validation, and manual Intercom sync.
- The `INTERCOM_TOKEN` GitHub Actions secret exists. Its value is intentionally not visible and must never be copied into the repository.
- `npm ci` succeeds, but `npm audit` currently reports eight high-severity advisories. The direct affected packages are `js-yaml` and `puppeteer`; the Puppeteer remediation requires a major-version upgrade. Handle this in a separate dependency PR with rendering and factory regression tests, not as an unreviewed `--force` fix.
- The latest `main` commit at handover is `1fefb0d` from 13 May 2026.
- Eight pull requests are open: four non-draft batch 3A PRs (`#119` to `#122`) and four older drafts (`#73`, `#85`, `#86`, `#87`). Treat them as stale until rebased and revalidated against current app behavior.

The full local validator is **not green**. On 25 August 2026, after running:

```bash
python scripts/validate-article-flow.py --all
```

it reported 103 hard failures and 37 warnings across the 22 contracted articles. This does not mean 103 production incidents; it means the repository cannot honestly claim an all-articles green baseline. The main categories are:

- the unfinished `direct-messages-for-sellers` pilot;
- iOS source paths that moved or became stale compared with the current local iOS checkout;
- mobile-breaking tables in `buy-it-now-sell-at-a-fixed-price` and `make-a-shipping-adjustment`;
- older contracts that predate newer validator gates.

Pull request CI intentionally checks changed articles rather than running `--all`. Therefore, always make the article you touch pass its current contract; do not use unrelated legacy failures to waive a new failure.

## The rules that matter most

- GitHub is canonical; do not independently edit the same article in Intercom.
- Every public article has pt-BR first and an EN mirror with the same meaning.
- App behavior, labels, icons, and layout must be backed by current iOS code and localized strings.
- No private data, secrets, internal system names, or unsupported product promises in this public repository.
- No em/en dashes, no mobile tables, no invented UI copy, and no “auction/leilão” terminology.
- A visual needs real iOS assets when available, paired locale HTML, a DPR 3 PNG, and human visual review.
- Article changes go through a pull request and one approval.
- Publishing is manual, one article at a time, after explicit release approval.

The complete timeless version is in [`AGENTS.md`](./AGENTS.md); detailed rules are indexed by [`process/README.md`](./process/README.md).

## Normal article workflow

1. Start from current `origin/main` on a new branch.
2. Read the article's `flow.yml`, `metadata.yml`, both language files, and existing audits.
3. Verify product claims and visible UI labels against current app code.
4. Edit pt-BR first, then mirror the meaning in EN.
5. Update mockup HTML, PNGs, metadata, flow contract, and audits when affected.
6. Run `python scripts/run-help-article.py articles/<slug> --phase validate`.
7. Open a pull request, describe risks and evidence, and obtain one approval.
8. Merge. Stop here unless a release owner separately approves publication.
9. If publication is approved, use the manual workflow and spot-check both locales live.

## Publishing one approved article

Publication changes production content. The repository maintainer and release authorizer may be different people. Until Aymar explicitly changes this policy, publication requires his approval for the exact slug.

In GitHub:

1. Open **Actions**.
2. Select **Sync articles to Intercom**.
3. Click **Run workflow**.
4. Select branch `main`.
5. Enter one exact article slug.
6. Enter `yes` in the confirmation field.
7. Run the workflow and wait for a green result.
8. Open the live Help Center article and spot-check EN and pt-BR.

Never add an automatic push trigger and never use a batch wildcard. The detailed safety checks are in [`process/15-intercom-sync.md`](./process/15-intercom-sync.md).

## Rollback

If a bad change was merged but not published, revert it through a new pull request; Intercom is unchanged.

If it was published:

1. Create a revert commit on a new branch with `git revert <commit-sha>`.
2. Open and merge the revert pull request after review.
3. Obtain explicit approval to publish the corrected slug.
4. Run the manual sync for that slug again and verify both locales live.

Do not direct-push a revert to protected `main`, and do not assume the revert publishes automatically.

## Access and ownership checklist for the handover

- [ ] Confirm Vaimiti's exact GitHub username before changing permissions.
- [ ] Grant repository write access through the appropriate organization team or collaborator role.
- [ ] Confirm Vaimiti can create branches, open pull requests, and view Actions.
- [ ] Confirm Vaimiti can read and clone `Jamble-Live-Shopping/Jamble-iOS`, which is required to verify live UI behavior.
- [ ] Decide and record who may approve content pull requests.
- [ ] Decide whether production-publish authorization remains with Aymar or transfers to Vaimiti.
- [ ] Confirm who performs the post-publish EN + pt-BR live check.
- [ ] Do not send the Intercom token in Slack, email, a document, or a local `.env` file. Keep it only as a GitHub Actions secret.

## Recommended first maintenance session

1. Review this handover pull request together.
2. Confirm access and release authority.
3. Triage PRs `#119` to `#122` and drafts `#73`, `#85`, `#86`, `#87`: rebase and revalidate, or close with a reason.
4. Create a separate cleanup plan for the full-validator baseline. Start with the mobile tables and the unfinished direct-messages pilot; do not mix that cleanup into an unrelated content PR.
5. Create a separate dependency-upgrade PR for the npm advisories and run mockup rendering plus both factory test suites before merging it.
6. Make one small, non-production copy change end to end so Vaimiti practices the branch, validation, PR, and review flow without publishing.
