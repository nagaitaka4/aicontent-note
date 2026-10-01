// 組み立てた固定ページ（dist/page.wp.txt）を実ブラウザで表示して確認する。
//   NODE_PATH=/opt/node-tools/node_modules node tests/e2e-page.js   （先に python3 compose-page.py）
// SWELLのCSSは無いので、見た目の細部ではなく「構造・ツールが動く・CTAが出る・通信しない」を見る。
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const wp = fs.readFileSync(path.join(__dirname, '..', 'dist', 'page.wp.txt'), 'utf8');
// WPのブロックコメントを外してHTMLにする（WPが表示するのと同じ中身）。入稿情報の段落（削除する前提のもの）は除く
const bodyHtml = wp.replace(/<!-- wp:paragraph -->\n<p>【WPの入力欄に写す情報】.*?<\/p>\n<!-- \/wp:paragraph -->/s, '').replace(/<!-- \/?wp:[^>]*-->\n?/g, '');
const page = `<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>page</title>
<style>body{margin:0;padding:16px;font:16px/1.8 sans-serif;color:#222;background:#fff}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:6px}.swl-marker{background:linear-gradient(transparent 60%,#ff6 0)}.swell-block-button__link{display:inline-block;padding:10px 20px;background:#2a8;color:#fff}</style></head><body><article>${bodyHtml}</article></body></html>`;

const server = http.createServer((req, res) => { res.setHeader('content-type', 'text/html; charset=utf-8'); res.end(page); });
let pass = 0, fail = 0;
const check = (name, cond, detail) => { if (cond) pass++; else { fail++; console.log('  [NG] ' + name + (detail !== undefined ? ' → ' + JSON.stringify(detail) : '')); } };

(async () => {
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const base = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch();
  const shots = path.join(__dirname, 'out', 'shots');
  fs.mkdirSync(shots, { recursive: true });
  for (const [name, opts] of [['phone', { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true }], ['desktop', { viewport: { width: 1000, height: 900 } }]]) {
    const ctx = await browser.newContext(opts);
    const blocked = [];
    await ctx.route('**/*', (route) => { const u = route.request().url(); if (!u.startsWith(base)) { blocked.push(u); return route.abort(); } return route.continue(); });
    const p = await ctx.newPage();
    const errors = [];
    p.on('pageerror', (e) => errors.push(e.message));
    await p.goto(base + '/');
    await p.waitForSelector('#pmc-t');
    const order = await p.evaluate(() => {
      const art = document.querySelector('article');
      const kids = [...art.children].map((e) => e.tagName + ':' + (e.id || '') + ':' + (e.textContent || '').slice(0, 14));
      return kids;
    });
    check(`[${name}] 先頭はリード文・次がツール`, order[0].startsWith('P') && order[1].includes('pmc-host'), order.slice(0, 3));
    check(`[${name}] H2が5つ（ツール内部は別）`, (await p.locator('article > h2').count()) === 5, await p.locator('article > h2').allTextContents());
    check(`[${name}] 表が5つ（ページ本体の表。ツール内部の表は別）`, (await p.locator('article > figure table').count()) === 5, await p.locator('article > figure table').count());
    check(`[${name}] CTAのリンクがお問い合わせフォーム`, (await p.locator('a.swell-block-button__link').getAttribute('href')) === 'https://aicontent-note.com/contact/');
    const cta = await p.locator('article > p', { hasText: 'ブログ更新が止まっている' }).textContent();
    check(`[${name}] CTA文言`, cta.includes('企画から執筆・公開まで、まるごとお任せください。お気軽にご相談を。'), cta);
    check(`[${name}] プライバシーポリシーへのリンク`, (await p.locator('a[href="https://aicontent-note.com/privacy-policy/"]').count()) === 1);
    check(`[${name}] 外部一次情報のリンク（twitter-text）`, (await p.locator('a[href^="https://github.com/twitter/twitter-text"]').count()) === 1);
    await p.fill('#pmc-t', '昨日の話。Claude Codeで作りました');
    check(`[${name}] ページに組み込んでもツールが動く（重み）`, (await p.textContent('#pmc-w')) === String(require('twitter-text').parseTweet('昨日の話。Claude Codeで作りました').weightedLength), await p.textContent('#pmc-w'));
    check(`[${name}] 前提語を拾う`, (await p.textContent('#pmc-chip2')).includes('確認'));
    check(`[${name}] 横スクロールなし`, (await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth)) <= 0);
    check(`[${name}] 外部通信なし`, blocked.length === 0, blocked);
    check(`[${name}] エラーなし`, errors.length === 0, errors);
    await p.screenshot({ path: path.join(shots, `06-page-${name}.png`), fullPage: true });
    await ctx.close();
  }
  await browser.close();
  server.close();
  console.log(`\n固定ページの確認: ${pass} 件OK / ${fail} 件NG（スクリーンショット: tests/out/shots/06-page-*.png）`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); server.close(); process.exit(1); });
