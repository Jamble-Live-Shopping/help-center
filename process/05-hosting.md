# Step 5, Host PNGs on GitHub

**Goal**: push the produced PNGs to `Jamble-Live-Shopping/help-center` so they're served from a permanent, public URL that Intercom can fetch.

## Why GitHub (not S3, not a personal gist, not a CDN)

- **Source of truth + versioning for free**, every change is a commit, easy to diff and roll back
- **Org-owned**, assets survive any individual leaving the team
- **Public URLs out of the box**, `raw.githubusercontent.com/<org>/<repo>/main/<path>` is stable and CDN-cached
- **Intercom fetches once, caches on its own CDN**, GitHub is only hit at upload time

Trade-off accepted: the repo is public, so anyone can see the mockups. This is fine because the mockups are already public (they're in published help articles).

## Repo layout (current)

```
Jamble-Live-Shopping/help-center/
├── README.md
├── assets/
│   └── mockups/                        # ALL PNGs live HERE, flat, at ROOT
│       ├── <slug>__<mockup>__pt-br.png
│       ├── <slug>__<mockup>__en.png
│       └── ...
├── articles/
│   └── <slug>/
│       ├── pt-br.md
│       ├── en.md
│       ├── metadata.yml
│       ├── mockup-sources/             # HTML sources only (no PNGs here)
│       │   ├── <mockup>__pt-br.html
│       │   └── <mockup>__en.html
│       └── audit/
├── process/                            # this folder
├── scripts/
│   ├── shot-retina.mjs                 # canonical render (see Step 4)
│   ├── md-to-html.js                   # md -> Intercom HTML
│   ├── build-sync-payload.mjs
│   └── sync-one.sh
└── .github/workflows/sync-intercom.yml
```

**Critical**: PNGs go at `assets/mockups/` (repo root), never under `articles/<slug>/assets/mockups/`. `scripts/md-to-html.js` rewrites `./assets/mockups/foo.png` in the md → `https://raw.githubusercontent.com/.../main/assets/mockups/foo.png`. A PNG nested under an article folder will 404 on sync.

## PNG filename convention

```
<slug>__<mockup-name>__<locale>[__v<N>].png
```

- `<slug>` matches the article folder name exactly
- `<locale>` is `pt-br` or `en`
- `__v2` / `__v3` suffix is the cache-bust convention (see Step 6)

## Upload command

For each PNG produced in Step 4:

```bash
MOCKUP_DIR="<path to PNGs>"
BOX="prod-box4"  # without .png extension

B64=$(base64 -i "$MOCKUP_DIR/$BOX.png")

# Check if file exists (need SHA for update)
SHA=$(gh api repos/Jamble-Live-Shopping/help-center/contents/assets/mockups/$BOX.png --jq '.sha' 2>/dev/null)

if [ -n "$SHA" ]; then
    # Update existing file
    gh api repos/Jamble-Live-Shopping/help-center/contents/assets/mockups/$BOX.png \
      --method PUT \
      -f message="Update $BOX" \
      -f content="$B64" \
      -f sha="$SHA" \
      --jq '.content.download_url'
else
    # Create new file
    gh api repos/Jamble-Live-Shopping/help-center/contents/assets/mockups/$BOX.png \
      --method PUT \
      -f message="Add $BOX" \
      -f content="$B64" \
      --jq '.content.download_url'
fi
```

The command returns the public URL, e.g.:
```
https://raw.githubusercontent.com/Jamble-Live-Shopping/help-center/main/assets/mockups/prod-box4.png
```

## URL convention (remember this)

```
https://raw.githubusercontent.com/Jamble-Live-Shopping/help-center/main/assets/mockups/<filename>.png
```

Never use `github.com/...` (that's the HTML page, not the file). Never use `githubusercontent.com` without the `raw.` prefix.

## Batch upload

```bash
MOCKUP_DIR="<path>"
for box in prod-box1 prod-box2 prod-box4 prod-box5; do
  B64=$(base64 -i "$MOCKUP_DIR/$box.png")
  SHA=$(gh api repos/Jamble-Live-Shopping/help-center/contents/assets/mockups/$box.png --jq '.sha' 2>/dev/null)

  if [ -n "$SHA" ]; then
    gh api repos/Jamble-Live-Shopping/help-center/contents/assets/mockups/$box.png \
      --method PUT -f message="Update $box" -f content="$B64" -f sha="$SHA" \
      --jq '.content.download_url'
  else
    gh api repos/Jamble-Live-Shopping/help-center/contents/assets/mockups/$box.png \
      --method PUT -f message="Add $box" -f content="$B64" \
      --jq '.content.download_url'
  fi
done
```

## Verify

After upload, open the URL in a browser (or `curl -I <url>`). Expect:
- `HTTP/2 200`
- `content-type: image/png`
- Visible image in browser

If you get a 404: check the org name, repo name, branch (`main`, not `master`), and path match exactly. GitHub is case-sensitive.

## Permissions setup (one-time)

The `gh` CLI needs org repo write permission on `Jamble-Live-Shopping`. If you get `403 Must have admin rights`, run:

```bash
gh auth refresh -h github.com -s delete_repo,write:org,repo
```

And confirm the org admin has granted your PAT repo access on the org settings page.

## `metadata.yml` schema (mandatory)

Each article folder has a `metadata.yml`. `scripts/build-sync-payload.mjs` iterates over **`meta.locales`** to decide which `.md` files to sync. An article with only the flat `titles:` / `descriptions:` keys and no `locales:` block fails sync with "No locale .md files found". This hit us on PR #21 and PR #24.

Full required shape:

```yaml
intercom_id: 14288124
slug: pack-and-ship-your-order
collection_id: 19177937
default_locale: pt-BR
state: published
author_id: 7980507

# Top-level (used for the article's primary language body)
titles:
  pt-BR: Embale e Envie Seu Pedido
  en: Pack and Ship Your Order
descriptions:
  pt-BR: <= 140 chars
  en: <= 140 chars

# Per-locale (used by build-sync-payload.mjs to find .md files, REQUIRED)
locales:
  pt-BR:
    title: 'Embale e Envie Seu Pedido'
    description: '<same <=140>'
  en:
    title: 'Pack and Ship Your Order'
    description: '<same <=140>'
```

Both `titles:`/`descriptions:` AND `locales:` must be present. `yaml.safe_load` on the file should succeed, and the result must contain the key `locales` with entries for every `.md` in the folder.

## Branch hygiene (when working in parallel worktrees)

- Work inside your worktree (`.claude/worktrees/agent-<id>/`), never in the main repo directory
- Confirm `git branch --show-current` returns your `rewrite-<slug>-<id>` branch before every commit
- Never commit to `main` directly. PRs are the only route in.
