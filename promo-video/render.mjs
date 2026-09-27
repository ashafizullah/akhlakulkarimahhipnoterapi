// Render promo.html frame-by-frame with Playwright, pipe to ffmpeg.
// Usage: node render.mjs [out.mp4] [--stills t1,t2,...]
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright'); // honours NODE_PATH for a global install
import { spawn } from 'node:child_process';
import path from 'node:path';
import fs from 'node:fs';

const FPS = 30;
const dir = path.dirname(new URL(import.meta.url).pathname);
const args = process.argv.slice(2);
const stillsIdx = args.indexOf('--stills');
const ffmpeg = process.env.FFMPEG || 'ffmpeg';

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto('file://' + path.join(dir, 'promo.html') + '?render=1');
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(300);

if (stillsIdx >= 0) {
  fs.mkdirSync(path.join(dir, 'stills'), { recursive: true });
  for (const t of args[stillsIdx + 1].split(',').map(Number)) {
    await page.evaluate(t => render(t), t);
    await page.screenshot({ path: path.join(dir, 'stills', `t${t}.jpg`), type: 'jpeg', quality: 85 });
  }
  await browser.close();
  process.exit(0);
}

const out = args[0] || path.join(dir, 'promo-akh-vertical.mp4');
const audio = path.join(dir, 'music.wav');
const duration = await page.evaluate(() => window.DURATION);
const ff = spawn(ffmpeg, [
  '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
  ...(fs.existsSync(audio) ? ['-i', audio, '-c:a', 'aac', '-b:a', '192k', '-shortest'] : []),
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '23', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out,
], { stdio: ['pipe', 'inherit', 'inherit'] });

const total = Math.round(duration * FPS);
for (let f = 0; f < total; f++) {
  await page.evaluate(t => render(t), f / FPS);
  const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (f % 90 === 0) console.log(`frame ${f}/${total}`);
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
await browser.close();
console.log('wrote', out);
