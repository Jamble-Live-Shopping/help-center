# Step 5, Host PNGs on GitHub

**Goal**: push the produced PNGs to `Jamble-Live-Shopping/help-center` so they're served from a permanent, public URL that Intercom can fetch.

## Why GitHub (not S3, not a personal gist, not a CDN)

- **Source of truth + versioning for free**, every change is a commit, easy to diff and roll back
- **Org-owned**, assets survive any individual leaving the team
- **Public URLs out of the box**, `raw.githubusercontent.com/<org>/<repo>/main/<path>` is stable and CDN-cached
- **Intercom fetches once, caches on its own CDN**, GitHub is only hit at upload time

Trade-off accepted: the repo is public, so anyone can see the mockups. This is fine because the mockups are already public (they're in published help articles).

## Repo layout

```
Jamble-Live-Shopping/help-center/
├── README.md                           # what this repo is for
├── assets/
│   ├── mockups/                        # the PNGs we screenshot
│   │   ├── prod-box1.png
│   │   ├── prod-box2.png
│   │   └── ...
│   └── icons/                          # (future) shared icon pool
├── articles/                           # (future) article-by-article HTML source
│   └── <article-slug>/
│       ├── body.html
│       ├── mockup-sources/
│       └── metadata.json
└── scripts/                            # (future) batch tools
```

For the current phase, only `assets/mockups/` is populated.

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
