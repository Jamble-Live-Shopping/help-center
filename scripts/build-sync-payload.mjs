#!/usr/bin/env node
// Build the Intercom PUT payload for one article.
//
// Usage: node scripts/build-sync-payload.mjs <article-dir> <payload-out> <info-out>
//
// Reads:    <article-dir>/metadata.yml + each <locale>.md
// Writes:   <payload-out> (JSON, the PUT body)
//           <info-out>    (JSON, { intercom_id, synced, skipped, intercom_default_locale })
//
// Requires INTERCOM_TOKEN in env (for the pre-flight GET).

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { execSync } from 'node:child_process';
import yaml from 'js-yaml';

const [, , articleDir, payloadPath, infoPath] = process.argv;
if (!articleDir || !payloadPath || !infoPath) {
  console.error('Usage: build-sync-payload.mjs <article-dir> <payload-out> <info-out>');
  process.exit(2);
}

const token = process.env.INTERCOM_TOKEN;
if (!token) {
  console.error('INTERCOM_TOKEN not set');
  process.exit(1);
}

const meta = yaml.load(readFileSync(articleDir + '/metadata.yml', 'utf8'));
if (!meta.intercom_id) {
  console.error('metadata.yml missing intercom_id');
  process.exit(1);
}

const toIntercomLocale = (l) => (l === 'pt-br' ? 'pt-BR' : l);

// Convert each locale's MD → HTML
const translatedContent = {};
const synced = [];
const skipped = [];
for (const [locale, localeMeta] of Object.entries(meta.locales || {})) {
  const mdFile = `${articleDir}/${locale}.md`;
  if (!existsSync(mdFile)) {
    skipped.push(locale);
    continue;
  }
  const html = execSync(`node scripts/md-to-html.js '${mdFile}'`, { encoding: 'utf8' });
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

// GET the article to learn Intercom's current default_locale (self-healing: if someone flips
// it manually on the Intercom admin side, the sync adapts next run).
let intercomDefaultLocale = 'en';
try {
  const curlOut = execSync(
    `curl -s -H "Authorization: Bearer ${token}" -H "Intercom-Version: 2.11" "https://api.intercom.io/articles/${meta.intercom_id}"`,
    { encoding: 'utf8' }
  );
  const parsed = JSON.parse(curlOut);
  if (parsed.default_locale) intercomDefaultLocale = parsed.default_locale;
} catch (e) {
  console.error('Warning: failed to GET article for default_locale, falling back to en:', e.message);
}

const body = { translated_content: translatedContent };
const defaultEntry = translatedContent[intercomDefaultLocale];
if (defaultEntry) {
  body.body = defaultEntry.body;
  body.description = defaultEntry.description;
  body.title = defaultEntry.title;
} else {
  console.error(`Warning: Intercom default_locale is '${intercomDefaultLocale}' but no matching .md, top-level body left untouched`);
}

writeFileSync(payloadPath, JSON.stringify(body));
writeFileSync(infoPath, JSON.stringify({
  intercom_id: meta.intercom_id,
  synced,
  skipped,
  repo_default_locale: meta.default_locale || 'en',
  intercom_default_locale: intercomDefaultLocale,
}));
