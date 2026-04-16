#!/usr/bin/env bash
# Sync one article from the repo to Intercom.
# Usage: scripts/sync-one.sh articles/<slug>
#
# Reads articles/<slug>/metadata.yml, converts each locale's Markdown body to HTML
# (via scripts/md-to-html.js), and PUTs the result to https://api.intercom.io/articles/:id.
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

# Build the Intercom PUT payload with a single node invocation.
# Writes JSON payload to $PAYLOAD and human-readable summary to $INFO.
node --input-type=module -e "
  import { readFileSync, writeFileSync, existsSync } from 'node:fs';
  import { execSync } from 'node:child_process';
  import yaml from 'js-yaml';

  const articleDir = process.argv[1];
  const payloadPath = process.argv[2];
  const infoPath = process.argv[3];

  const meta = yaml.load(readFileSync(articleDir + '/metadata.yml', 'utf8'));
  if (!meta.intercom_id) {
    console.error('metadata.yml missing intercom_id');
    process.exit(1);
  }
  const defaultLocale = meta.default_locale || 'en';
  const toIntercomLocale = (l) => (l === 'pt-br' ? 'pt-BR' : l);

  const translatedContent = {};
  const synced = [];
  const skipped = [];
  for (const [locale, localeMeta] of Object.entries(meta.locales || {})) {
    const mdFile = \`\${articleDir}/\${locale}.md\`;
    if (!existsSync(mdFile)) {
      skipped.push(locale);
      continue;
    }
    const html = execSync(\`node scripts/md-to-html.js '\${mdFile}'\`, { encoding: 'utf8' });
    translatedContent[toIntercomLocale(locale)] = {
      title: localeMeta.title || '',
      description: localeMeta.description || '',
      body: html,
      state: meta.state || 'published',
    };
    synced.push(locale);
  }

  if (synced.length === 0) {
    console.error('No locale .md files found, nothing to sync.');
    process.exit(1);
  }

  const body = { translated_content: translatedContent };
  const defaultEntry = translatedContent[toIntercomLocale(defaultLocale)];
  if (defaultEntry) {
    body.body = defaultEntry.body;
    body.description = defaultEntry.description;
    body.title = defaultEntry.title;
  }

  writeFileSync(payloadPath, JSON.stringify(body));
  writeFileSync(infoPath, JSON.stringify({
    intercom_id: meta.intercom_id,
    synced,
    skipped,
    default_locale: defaultLocale,
  }));
" "$ARTICLE_DIR" "$PAYLOAD" "$INFO"

INTERCOM_ID=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$INFO')).intercom_id)")
SYNCED=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$INFO')).synced.join(','))")
SKIPPED=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$INFO')).skipped.join(','))")
DEFAULT=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$INFO')).default_locale)")

echo "Article: $INTERCOM_ID"
echo "Default locale: $DEFAULT"
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
