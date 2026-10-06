// 実ブラウザ（Chromium）での動作確認。
//   NODE_PATH=/opt/node-tools/node_modules node tests/e2e.js      （Playwright が入っている環境）
// 先に node build.js で dist/ を作っておく。スクリーンショットは tests/out/shots/ に出る。
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const dist = path.join(__dirname, '..', 'dist');
const shots = path.join(__dirname, 'out', 'shots');
fs.mkdirSync(shots, { recursive: true });

// WordPress(SWELL)のように、ページ側が強いCSSを持っている状況の再現
const HOSTILE_CSS = `
  *{box-sizing:content-box!important}
  body{font-family:serif;font-size:13px;line-height:1.2;background:#eee;color:#900}
  textarea{display:none!important}
  button{background:#f0f!important;color:#ff0!important;border-radius:0!important;height:10px!important}
  h2,h3{font-size:40px!important;background:#00f!important;color:#fff!important;border-left:20px solid red!important;padding:20px!important}
  p{margin:40px!important;color:#0a0!important}
  table,td,th{border:5px solid #000!important}
  ul,li{list-style:square!important}
  input,select{width:5px!important;display:none!important}
  details,summary{display:none!important}
  mark,code,label{all:unset!important;display:none!important}
`;
function wpPage() {
  const snippet = fs.readFileSync(path.join(dist, 'wp-block.txt'), 'utf8').replace(/<!-- \/?wp:html -->\n?/g, '');
  return `<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>WPふう</title><style>${HOSTILE_CSS}</style></head><body><article class="post_content"><h2>記事の見出し</h2><p>本文です。</p>\n${snippet}\n<p>記事の続き。</p></article></body></html>`;
}

const server = http.createServer((req, res) => {
  if (req.url === '/' || req.url.startsWith('/?')) { res.setHeader('content-type', 'text/html; charset=utf-8'); res.end(fs.readFileSync(path.join(dist, 'post-mae-check.html'))); }
  else if (req.url === '/wp') { res.setHeader('content-type', 'text/html; charset=utf-8'); res.end(wpPage()); }
  else { res.statusCode = 404; res.end('no'); }
});

let pass = 0, fail = 0;
const check = (name, cond, detail) => { if (cond) pass++; else { fail++; console.log('  [NG] ' + name + (detail !== undefined ? '  → ' + JSON.stringify(detail) : '')); } };

(async () => {
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const base = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });

  async function newPage(opts, init) {
    const ctx = await browser.newContext(opts);
    const requests = [];
    const blocked = [];
    await ctx.route('**/*', (route) => {
      const u = route.request().url();
      requests.push(u);
      if (!u.startsWith(base)) { blocked.push(u); return route.abort(); }
      return route.continue();
    });
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
    page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
    if (init) await page.addInitScript(init);
    return { ctx, page, requests, blocked, errors };
  }

  const PHONE = { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' };
  const DESKTOP = { viewport: { width: 1100, height: 900 } };

  // ===== 1. スマホ：基本の流れ =====
  {
    const { ctx, page, requests, blocked, errors } = await newPage(PHONE);
    await page.goto(base + '/');
    await page.waitForSelector('#pmc-t');
    await page.screenshot({ path: path.join(shots, '01-phone-empty.png'), fullPage: true });

    check('空のときの重みは0', (await page.textContent('#pmc-w')) === '0');
    check('空のとき、空メッセージが出る', (await page.textContent('#pmc-msg')).includes('入力すると'));

    await page.fill('#pmc-t', 'Claude Codeで作りました');
    check('重み23（日本語6字×2＋英数11字）', (await page.textContent('#pmc-w')) === '23', await page.textContent('#pmc-w'));
    check('あと257', (await page.textContent('#pmc-msg')).includes('257'), await page.textContent('#pmc-msg'));

    const sample = '昨日の「無料でリセット」も、まだ押してません。\n\nこれ、試した話です。詳しくは https://example.com/abc を見てください。👨‍👩‍👧‍👦';
    await page.fill('#pmc-t', sample);
    const w = await page.textContent('#pmc-w');
    const expected = require('twitter-text').parseTweet(sample).weightedLength;   // 公式ライブラリの値
    check('画面の重みが公式ライブラリと一致（URL・絵文字入り）', w === String(expected), { 画面: w, 公式: expected });
    const finds = await page.locator('.find').allTextContents();
    check('前提語「昨日の」を拾う', finds.some((t) => t.includes('昨日の')), finds);
    check('1行目の「これ」は2行目なので拾わない（1行目は「昨日の〜」）', !finds.some((t) => t.includes('「これ」')), finds);
    check('1行目をそのまま見せる', (await page.textContent('#pmc-first')).includes('昨日の「無料でリセット」'));
    check('要注意表現のチップ', (await page.textContent('#pmc-chip2')).includes('確認'), await page.textContent('#pmc-chip2'));
    check('URLの一覧に出る', (await page.textContent('#pmc-count-notes')).includes('https://example.com/abc'));

    // 超過
    await page.fill('#pmc-t', 'あ'.repeat(141));
    check('141字で超過表示', (await page.textContent('#pmc-msg')).includes('2 超過'), await page.textContent('#pmc-msg'));
    check('超過のチップ', (await page.textContent('#pmc-chip1')).includes('超過'));
    await page.screenshot({ path: path.join(shots, '02-phone-over.png'), fullPage: true });

    // ③（直近の投稿との重なり）と保存の仕組みは公開版から外した（2026-10-05）
    check('③の欄が無い', (await page.locator('#pmc-h3, #pmc-save, #pmc-bulk, #pmc-saved').count()) === 0);
    check('画面に「重なり」「保存した投稿」の文言が無い', !/重なり|保存した投稿|まとめて追加/.test(await page.evaluate(() => document.querySelector('#pmc-host').shadowRoot.textContent)));

    // 何も保存しない：入力して再読み込みすると消え、ブラウザの保存領域に何も無い
    await page.fill('#pmc-t', '月100ドルのMaxプランに課金して、記事を10本書いた話です。');
    await page.click('summary:has-text("見る項目を選ぶ")');
    await page.uncheck('#pmc-on-report');
    const stored = await page.evaluate(() => ({ local: localStorage.length, session: sessionStorage.length, cookie: document.cookie }));
    check('localStorage・sessionStorage・Cookieに何も入らない', stored.local === 0 && stored.session === 0 && stored.cookie === '', stored);
    await page.reload();
    await page.waitForSelector('#pmc-t');
    check('再読み込みすると入力は消える', (await page.inputValue('#pmc-t')) === '');
    check('再読み込みすると見る項目は全部ONに戻る', await page.evaluate(() => document.querySelector('#pmc-host').shadowRoot.querySelector('#pmc-on-report').checked));

    // クリア
    await page.fill('#pmc-t', 'あいう');
    await page.click('#pmc-clear');
    check('クリアで入力が空になり、重みが0', (await page.inputValue('#pmc-t')) === '' && (await page.textContent('#pmc-w')) === '0');

    // 項目のOFF
    await page.fill('#pmc-t', '昨日の話');
    check('前提語を拾う', (await page.textContent('#pmc-chip2')).includes('確認'));
    await page.click('summary:has-text("見る項目を選ぶ")');
    await page.uncheck('#pmc-on-leak');
    check('前提語をOFFにすると拾わない', (await page.textContent('#pmc-chip2')).includes('問題なし'), await page.textContent('#pmc-chip2'));

    // はみ出し（横スクロール）が無いこと
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    check('スマホ幅で横スクロールが出ない', overflow <= 0, overflow);
    const geo = await page.evaluate(() => {
      const r = document.querySelector('#pmc-host').shadowRoot;
      const t = r.querySelector('#pmc-t').getBoundingClientRect();
      const card = r.querySelector('.card').getBoundingClientRect();
      const link = getComputedStyle(r.querySelector('#pmc-clear'));
      return { textareaW: t.width, cardW: card.width, linkColor: link.color };
    });
    check('入力欄がカードと同じ幅まで広がる', Math.abs(geo.textareaW - geo.cardW) < 2, geo);
    check('「クリア」の文字がアクセント色', geo.linkColor === 'rgb(11, 107, 99)', geo);
    check('スマホ幅のtextareaが16px以上（iPhoneで拡大されない）', (await page.evaluate(() => parseFloat(getComputedStyle(document.querySelector('#pmc-host').shadowRoot.querySelector('#pmc-t')).fontSize))) >= 16);

    check('通信：自分のページ以外へのリクエストなし', blocked.length === 0, blocked);
    check('通信：リクエストは本体のHTMLとfaviconだけ', requests.every((u) => u === base + '/' || u.endsWith('/favicon.ico')), requests);
    check('エラーなし', errors.length === 0, errors);
    await ctx.close();
  }

  // ===== 2. デスクトップ：見た目 =====
  {
    const { ctx, page, errors } = await newPage(DESKTOP);
    await page.goto(base + '/');
    await page.fill('#pmc-t', 'Claude Codeを半年使って分かったこと。\n\n前回の記事で「これ」と書いた設定を、実際に試してみました。');
    await page.screenshot({ path: path.join(shots, '04-desktop.png'), fullPage: true });
    check('デスクトップでエラーなし', errors.length === 0, errors);
    await ctx.close();
  }

  // ===== 3. WordPress(SWELL)ふうの強いCSSの中に貼っても崩れない =====
  {
    const { ctx, page, blocked, errors } = await newPage(PHONE);
    await page.goto(base + '/wp');
    await page.waitForSelector('#pmc-t');
    const vis = await page.evaluate(() => {
      const r = document.querySelector('#pmc-host').shadowRoot;
      const t = r.querySelector('#pmc-t');
      const b = r.querySelector('#pmc-clear');
      const h = r.querySelector('h2.title');
      const cs = (e) => getComputedStyle(e);
      return {
        textareaShown: cs(t).display !== 'none' && t.getBoundingClientRect().height > 100,
        btnColor: cs(b).color, btnBg: cs(b).backgroundColor, btnHeight: b.getBoundingClientRect().height,
        titleSize: cs(h).fontSize, titleBg: cs(h).backgroundColor,
      };
    });
    check('ページ側のCSSがあっても入力欄が見える', vis.textareaShown, vis);
    check('ボタンの色がページ側のCSSに上書きされない', vis.btnColor === 'rgb(11, 107, 99)' && vis.btnBg === 'rgba(0, 0, 0, 0)', vis);
    check('ボタンの高さが36px以上（ページ側の height:10px に負けない）', vis.btnHeight >= 36, vis.btnHeight);
    check('見出しがページ側のCSSに上書きされない', vis.titleSize === '20px' && vis.titleBg === 'rgba(0, 0, 0, 0)', vis);
    await page.fill('#pmc-t', '先日の話。');
    check('ページに埋め込んでも動く', (await page.textContent('#pmc-chip2')).includes('確認'), await page.textContent('#pmc-chip2'));
    await page.screenshot({ path: path.join(shots, '05-wp-embed-hostile-css.png'), fullPage: true });
    check('埋め込み：外部通信なし', blocked.length === 0, blocked);
    check('埋め込み：エラーなし', errors.length === 0, errors);
    await ctx.close();
  }

  // ===== 4. ブラウザの保存領域に一度も触らない（プライベートブラウズなどでも同じに動く） =====
  {
    const { ctx, page, errors } = await newPage(PHONE, () => {
      window.__touched = 0;
      ['getItem', 'setItem', 'removeItem', 'clear', 'key'].forEach((m) => {
        Storage.prototype[m] = function () { window.__touched++; throw new Error('blocked'); };
      });
    });
    await page.goto(base + '/');
    await page.waitForSelector('#pmc-t');
    await page.fill('#pmc-t', '保存できない環境のテスト。昨日の話');
    check('保存領域が使えない環境でも動く', (await page.textContent('#pmc-chip2')).includes('確認'), await page.textContent('#pmc-chip2'));
    check('localStorage・sessionStorageを一度も呼ばない', (await page.evaluate(() => window.__touched)) === 0, await page.evaluate(() => window.__touched));
    check('保存領域が使えない環境でもエラーなし', errors.length === 0, errors);
    await ctx.close();
  }

  // ===== 5. Shadow DOM が無い古い端末 =====
  {
    const { ctx, page, errors } = await newPage(PHONE, () => { delete Element.prototype.attachShadow; });
    await page.goto(base + '/');
    await page.waitForSelector('#pmc-t');
    await page.fill('#pmc-t', 'あ'.repeat(10));
    check('attachShadow が無くても動く（重み20）', (await page.textContent('#pmc-w')) === '20', await page.textContent('#pmc-w'));
    check('attachShadow が無くてもエラーなし', errors.length === 0, errors);
    await ctx.close();
  }

  await browser.close();
  server.close();
  console.log(`\nブラウザ確認: ${pass} 件OK / ${fail} 件NG（スクリーンショット: tests/out/shots/）`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); server.close(); process.exit(1); });
