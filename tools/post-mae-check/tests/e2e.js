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

    // 保存 → 重なり
    await page.fill('#pmc-t', '月100ドルのMaxプランに課金して、Sonnet 5.5で記事を10本書いた話です。');
    await page.click('#pmc-save');
    check('保存できた', (await page.textContent('#pmc-toast')).includes('保存しました'), await page.textContent('#pmc-toast'));
    check('保存した直後は同じ文章なので重なりなし', (await page.textContent('#pmc-chip3')).includes('重なりなし'), await page.textContent('#pmc-chip3'));
    await page.click('#pmc-save');
    check('同じ文章は二重に保存しない', (await page.textContent('#pmc-toast')).includes('すでに保存'), await page.textContent('#pmc-toast'));

    await page.fill('#pmc-t', '今日は月100ドルのプランの話をもう一度。別の角度から書いてみました。');
    check('数字つきの語（100ドル）が同じなら重なり', (await page.textContent('#pmc-chip3')).includes('重なり 1件'), await page.textContent('#pmc-chip3'));
    check('理由に「100ドル」が出る', (await page.textContent('#pmc-hits')).includes('100ドル'), await page.textContent('#pmc-hits'));
    await page.screenshot({ path: path.join(shots, '03-phone-findings.png'), fullPage: true });

    await page.fill('#pmc-t', '全然ちがう話です。今日は散歩をしました。');
    check('関係ない文章は重なりなし', (await page.textContent('#pmc-chip3')).includes('重なりなし'), await page.textContent('#pmc-chip3'));

    // 再読み込みしても残る
    await page.reload();
    await page.waitForSelector('#pmc-t');
    check('再読み込み後も保存が残る', (await page.textContent('#pmc-saved-sum')).includes('1件'), await page.textContent('#pmc-saved-sum'));
    await page.fill('#pmc-t', '今日は月100ドルのプランの話をもう一度。');
    check('再読み込み後も重なりを見つける', (await page.textContent('#pmc-chip3')).includes('重なり'), await page.textContent('#pmc-chip3'));

    // まとめて追加
    await page.click('summary:has-text("まとめて追加")');
    await page.fill('#pmc-bulk', '2026-09-20\nAAA\n---\n2026-09-21\nBBB\n---\nCCC');
    await page.click('#pmc-bulk-add');
    check('まとめて追加（3件）', (await page.textContent('#pmc-toast')).includes('3件を追加'), await page.textContent('#pmc-toast'));
    check('保存数が4件になる', (await page.textContent('#pmc-saved-sum')).includes('4件'), await page.textContent('#pmc-saved-sum'));

    // 個別削除・全削除
    await page.click('summary:has-text("保存した投稿")');
    await page.locator('#pmc-saved button:has-text("削除")').first().click();
    check('1件削除で3件', (await page.textContent('#pmc-saved-sum')).includes('3件'), await page.textContent('#pmc-saved-sum'));
    page.once('dialog', (d) => d.accept());
    await page.click('#pmc-del-all');
    check('全削除で0件', (await page.textContent('#pmc-saved-sum')).includes('0件'), await page.textContent('#pmc-saved-sum'));

    // 項目のOFF
    await page.fill('#pmc-t', '昨日の話');
    check('前提語を拾う', (await page.textContent('#pmc-chip2')).includes('確認'));
    await page.click('summary:has-text("見る項目を選ぶ")');
    await page.uncheck('#pmc-on-leak');
    check('前提語をOFFにすると拾わない', (await page.textContent('#pmc-chip2')).includes('拾えた所なし'), await page.textContent('#pmc-chip2'));

    // はみ出し（横スクロール）が無いこと
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    check('スマホ幅で横スクロールが出ない', overflow <= 0, overflow);
    const geo = await page.evaluate(() => {
      const r = document.querySelector('#pmc-host').shadowRoot;
      const t = r.querySelector('#pmc-t').getBoundingClientRect();
      const card = r.querySelector('.card').getBoundingClientRect();
      const btn = getComputedStyle(r.querySelector('#pmc-save'));
      const sub = getComputedStyle(r.querySelector('#pmc-bulk-add'));
      return { textareaW: t.width, cardW: card.width, btnColor: btn.color, btnBg: btn.backgroundColor, subColor: sub.color };
    });
    check('入力欄がカードと同じ幅まで広がる', Math.abs(geo.textareaW - geo.cardW) < 2, geo);
    check('主ボタンの文字が白（読める）', geo.btnColor === 'rgb(255, 255, 255)' && geo.btnBg === 'rgb(11, 107, 99)', geo);
    check('副ボタンの文字がアクセント色', geo.subColor === 'rgb(11, 107, 99)', geo);
    check('前の操作のメッセージは、入力し直すと消える', (await page.textContent('#pmc-toast')) === '', await page.textContent('#pmc-toast'));
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
      const b = r.querySelector('#pmc-save');
      const h = r.querySelector('h2.title');
      const cs = (e) => getComputedStyle(e);
      return {
        textareaShown: cs(t).display !== 'none' && t.getBoundingClientRect().height > 100,
        btnBg: cs(b).backgroundColor, btnHeight: b.getBoundingClientRect().height,
        titleSize: cs(h).fontSize, titleBg: cs(h).backgroundColor,
      };
    });
    check('ページ側のCSSがあっても入力欄が見える', vis.textareaShown, vis);
    check('ボタンの色がページ側のCSSに上書きされない', vis.btnBg === 'rgb(11, 107, 99)', vis.btnBg);
    check('ボタンの高さが44px以上', vis.btnHeight >= 44, vis.btnHeight);
    check('見出しがページ側のCSSに上書きされない', vis.titleSize === '20px' && vis.titleBg === 'rgba(0, 0, 0, 0)', vis);
    await page.fill('#pmc-t', '先日の話。');
    check('ページに埋め込んでも動く', (await page.textContent('#pmc-chip2')).includes('確認'), await page.textContent('#pmc-chip2'));
    await page.screenshot({ path: path.join(shots, '05-wp-embed-hostile-css.png'), fullPage: true });
    check('埋め込み：外部通信なし', blocked.length === 0, blocked);
    check('埋め込み：エラーなし', errors.length === 0, errors);
    await ctx.close();
  }

  // ===== 4. ブラウザに保存できない環境（プライベートブラウズなど） =====
  {
    const { ctx, page, errors } = await newPage(PHONE, () => {
      Storage.prototype.setItem = function () { throw new Error('QuotaExceededError'); };
    });
    await page.goto(base + '/');
    await page.waitForSelector('#pmc-t');
    check('保存できない環境では注意書きが出る', (await page.textContent('#pmc-store-note')).includes('保存できません'), await page.textContent('#pmc-store-note'));
    await page.fill('#pmc-t', '保存できない環境のテスト。月100ドル');
    await page.click('#pmc-save');
    await page.fill('#pmc-t', '月100ドルの話をもう一度');
    check('保存できなくても、開いている間は重なりを見つける', (await page.textContent('#pmc-chip3')).includes('重なり'), await page.textContent('#pmc-chip3'));
    check('保存できない環境でもエラーなし', errors.length === 0, errors);
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
