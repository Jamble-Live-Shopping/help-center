#!/usr/bin/env node
// Batch screenshot a manifest of { html, png } pairs.
// Usage: node scripts/shot-batch.mjs <manifest.json>
// Reuses 1 browser + N pages, retina deviceScaleFactor 3, inject outer gray frame.

import { readFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import puppeteer from 'puppeteer';

const manifestPath = process.argv[2];
if (!manifestPath) {
  console.error('Usage: shot-batch.mjs <manifest.json>');
  process.exit(2);
}

const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));

let browser = await puppeteer.launch({ headless: true });
let ok = 0, fail = 0;
let iterSinceRestart = 0;
for (const { html, png } of manifest) {
  // Relaunch browser every 50 screenshots to avoid resource exhaustion
  if (iterSinceRestart >= 50) {
    await browser.close();
    browser = await puppeteer.launch({ headless: true });
    iterSinceRestart = 0;
  }
  iterSinceRestart++;
  try {
    mkdirSync(dirname(png), { recursive: true });
    const page = await browser.newPage();
    await page.setViewport({ width: 400, height: 800, deviceScaleFactor: 3 });
    await page.goto(`file://${resolve(html)}`, { waitUntil: 'networkidle0' });
    await page.evaluate(() => {
      const phone = document.querySelector('.phone');
      if (!phone) return;
      const wrap = document.createElement('div');
      wrap.style.cssText = 'background: #F0F1F5; border-radius: 20px; padding: 24px; display: inline-block;';
      phone.parentElement.insertBefore(wrap, phone);
      wrap.appendChild(phone);
    });
    const box = await page.evaluate(() => {
      const p = document.querySelector('.phone');
      if (!p || !p.parentElement) return null;
      const r = p.parentElement.getBoundingClientRect();
      return { x: r.x, y: r.y, width: r.width, height: r.height };
    });
    if (box) {
      await page.screenshot({
        path: png,
        clip: { x: Math.max(0, box.x), y: Math.max(0, box.y), width: box.width, height: box.height },
        omitBackground: true,
      });
    } else {
      await page.screenshot({ path: png, fullPage: false, omitBackground: true });
    }
    ok++;
    if (ok % 10 === 0) console.log(`[${ok + fail}/${manifest.length}] ${png.split('/').pop()}`);
    await page.close();
  } catch (e) {
    console.error(`FAIL ${png}: ${e.message}`);
    fail++;
  }
}
await browser.close();
console.log(`Done: ${ok} ok, ${fail} fail`);
