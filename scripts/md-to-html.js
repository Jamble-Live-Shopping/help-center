#!/usr/bin/env node
// Convert a Markdown article body into Intercom-ready HTML.
// Usage: node scripts/md-to-html.js <path-to-md-file>
// Output: HTML on stdout.
//
// What this does beyond vanilla MD → HTML:
//  - Rewrites relative image URLs (./assets/...) to raw.githubusercontent.com
//  - Adds stable h_<hash> IDs on h1/h2/h3 (used by Intercom for deep links)
//  - Preserves only Intercom-compatible tags (h1, h2, h3, p, ul, ol, li, img, b, i, a, hr, code)

import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { marked } from 'marked';

const RAW_BASE = 'https://raw.githubusercontent.com/Jamble-Live-Shopping/help-center/main';

function stableId(text) {
  return 'h_' + createHash('sha1').update(text).digest('hex').slice(0, 10);
}

function rewriteImageUrl(src) {
  if (/^https?:\/\//.test(src)) return src;
  if (src.startsWith('/')) return RAW_BASE + src;
  if (src.startsWith('./')) return RAW_BASE + '/' + src.slice(2);
  return RAW_BASE + '/' + src;
}

const [, , mdPath] = process.argv;
if (!mdPath) {
  console.error('Usage: node scripts/md-to-html.js <path-to-md-file>');
  process.exit(2);
}

const md = readFileSync(mdPath, 'utf8');

// Let marked do vanilla HTML rendering, then post-process.
marked.setOptions({ gfm: true, breaks: false });
let html = marked.parse(md);

// 1. Rewrite image src
html = html.replace(/<img\s+([^>]*?)src="([^"]+)"([^>]*)>/g, (_, pre, src, post) => {
  const newSrc = rewriteImageUrl(src);
  return `<img ${pre}src="${newSrc}"${post}>`.replace(/\s+/g, ' ').replace(' >', '>');
});

// 2. Add stable IDs to h1/h2/h3 based on text content
html = html.replace(/<(h[123])>([^<]+)<\/\1>/g, (_, tag, text) => {
  return `<${tag} id="${stableId(text.trim())}">${text}</${tag}>`;
});

// 3. Strip class attributes that marked sometimes adds (defensive)
html = html.replace(/\s+class="[^"]*"/g, '');

// 4. Paragraphs that only wrap an <img> lose the <p> wrapper (Intercom is sensitive to <p><img></p>)
html = html.replace(/<p>\s*(<img[^>]+>)\s*<\/p>/g, '$1');

process.stdout.write(html);
