import { readFileSync } from 'node:fs';
import puppeteer from 'puppeteer';

const [, , htmlPath, pngPath] = process.argv;
if (!htmlPath || !pngPath) {
  console.error('Usage: shot-retina.mjs <html> <png>');
  process.exit(2);
}

const browser = await puppeteer.launch({ headless: true });
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 380, height: 2000, deviceScaleFactor: 3 });
  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle0' });
  const el = await page.$('.phone');
  if (!el) throw new Error('.phone selector not found');
  await el.screenshot({ path: pngPath, omitBackground: false });
  console.log(`Saved: ${pngPath}`);
} finally {
  await browser.close();
}
