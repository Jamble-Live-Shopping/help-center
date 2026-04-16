#!/usr/bin/env bash
# Sync one article from the repo to Intercom.
# Usage: scripts/sync-one.sh articles/<slug>
#
# Reads articles/<slug>/metadata.yml, converts each locale's Markdown body to HTML
# (via scripts/md-to-html.js), GETs the article to learn Intercom's current default_locale
# (self-healing if someone flips it manually in Intercom admin), then PUTs the payload.
#
# Requires:
#   - $INTERCOM_TOKEN set (local dev: export INTERCOM_TOKEN=...; CI: secret injected)
#   - npm install done (marked, js-yaml)

set -euo pipefail

ARTICLE_DIR="${1:-}"
if [[ -z "$ARTICLE_DIR" ]]; then
  echo "Usage: $0 articles/<slug>" >&2
  exit 2
fi
if [[ ! -d "$ARTICLE_DIR" ]]; then
  echo "Not a directory: $ARTICLE_DIR" >&2
  exit 1
fi
if [[ -z "${INTERCOM_TOKEN:-}" ]]; then
  echo "INTERCOM_TOKEN not set" >&2
  exit 1
fi
if [[ ! -f "$ARTICLE_DIR/metadata.yml" ]]; then
  echo "Missing metadata.yml in $ARTICLE_DIR" >&2
  exit 1
fi

PAYLOAD=$(mktemp)
INFO=$(mktemp)
trap 'rm -f "$PAYLOAD" "$INFO"' EXIT

node scripts/build-sync-payload.mjs "$ARTICLE_DIR" "$PAYLOAD" "$INFO"

INTERCOM_ID=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$INFO')).intercom_id)")
SYNCED=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$INFO')).synced.join(','))")
SKIPPED=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$INFO')).skipped.join(','))")
REPO_DEFAULT=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$INFO')).repo_default_locale)")
INTERCOM_DEFAULT=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$INFO')).intercom_default_locale)")

echo "Article: $INTERCOM_ID"
echo "Repo default_locale: $REPO_DEFAULT"
echo "Intercom default_locale (via GET): $INTERCOM_DEFAULT"
echo "Syncing locales: $SYNCED"
[[ -n "$SKIPPED" ]] && echo "Skipping (no .md): $SKIPPED"

HTTP=$(curl -s -o /tmp/intercom-resp.json -w '%{http_code}' \
  -X PUT \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Intercom-Version: 2.11' \
  -d "@$PAYLOAD" \
  "https://api.intercom.io/articles/$INTERCOM_ID")

if [[ "$HTTP" == "200" ]]; then
  UPDATED_AT=$(node -e "console.log(JSON.parse(require('fs').readFileSync('/tmp/intercom-resp.json')).updated_at)")
  echo "OK: article $INTERCOM_ID updated (updated_at=$UPDATED_AT)"
else
  echo "FAIL: HTTP $HTTP" >&2
  cat /tmp/intercom-resp.json >&2
  exit 1
fi
