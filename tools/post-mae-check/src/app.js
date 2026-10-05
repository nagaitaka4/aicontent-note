/* 投稿まえチェック：画面の動き
 *
 * 外部と通信しない（fetch・XMLHttpRequest・外部スクリプト・画像・フォントを使わない）。
 * 何も保存しない（localStorage・Cookie などを使わない）。入力した文章は、ページを閉じれば消える。
 * 2026-10-05：③直近の投稿との重なり（と投稿の保存）は公開版から外した。判定の中身は core.js に残してある（x-cannibal.py との突き合わせテスト用）。
 * PMC（core.js）と PMC_CSS（style.css）は、ビルド時に同じスコープへ並べて入れる。
 */

var SPEC_CHECKED = '2026-09-30';     // Xの仕様（文字数の数え方）を確かめた日。確かめ直したら更新する

/* ---------- 小さな道具 ---------- */

function el(tag, cls, text) {
  var e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined && text !== null) e.textContent = text;
  return e;
}
function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }
function oneLine(s) { return String(s).replace(/\s*\n\s*/g, ' ↵ '); }
function isLow(code) { return code >= 0xdc00 && code <= 0xdfff; }

// 該当箇所を前後の文脈つきで切り出し、該当部分に <mark> をつける
function context(text, index, length) {
  var start = Math.max(0, index - 14);
  var end = Math.min(text.length, index + length + 14);
  if (start > 0 && isLow(text.charCodeAt(start))) start--;
  if (end < text.length && isLow(text.charCodeAt(end))) end++;
  var frag = document.createDocumentFragment();
  frag.appendChild(document.createTextNode((start > 0 ? '…' : '') + oneLine(text.slice(start, index))));
  var m = el('mark', null, oneLine(text.slice(index, index + length)));
  frag.appendChild(m);
  frag.appendChild(document.createTextNode(oneLine(text.slice(index + length, end)) + (end < text.length ? '…' : '')));
  return frag;
}

/* ---------- 画面の骨組み（ユーザーの文章は入れない静的な部分だけ） ---------- */

var SKELETON = [
  '<h2 class="title">投稿まえチェック</h2>',
  '<p class="lead">X投稿の文字数と、伝わりにくい言い回しを、投稿する前に確認します。</p>',
  '<p class="privacy">入力した文章は、外部に送らず、保存もしません。ブラウザの中だけで処理し、ページを閉じれば消えます（AIも使っていません）。</p>',

  '<div class="field">',
  '<div class="field-top"><label for="pmc-t">投稿の下書き</label><button type="button" class="link" id="pmc-clear">クリア</button></div>',
  '<textarea id="pmc-t" rows="7" placeholder="ここに投稿前の文章を貼り付け（または入力）してください" spellcheck="false" autocomplete="off" autocapitalize="off" autocorrect="off"></textarea>',
  '</div>',

  '<div class="meter" id="pmc-meter">',
  '<div class="m-row"><span class="m-num"><b id="pmc-w">0</b> / 280</span><span class="m-msg" id="pmc-msg"></span></div>',
  '<div class="bar" aria-hidden="true"><div class="fill" id="pmc-fill"></div></div>',
  '</div>',

  // ① 文字数
  '<section class="card" aria-labelledby="pmc-h1">',
  '<div class="card-head"><h3 class="card-title" id="pmc-h1">① 文字数</h3><span class="chip" id="pmc-chip1"></span></div>',
  '<table class="tbl" id="pmc-tbl"></table>',
  '<p class="small" id="pmc-chars" style="margin-top:6px"></p>',
  '<div id="pmc-count-notes"></div>',
  '<p class="sub">通常のポスト用（上限280）です。Premiumの長文ポストは対象外です。数え方はXの公式ライブラリ twitter-text（設定 v3）に合わせています。確認日：<span id="pmc-spec"></span></p>',
  '</section>',

  // ② 要注意表現
  '<section class="card" aria-labelledby="pmc-h2">',
  '<div class="card-head"><h3 class="card-title" id="pmc-h2">② 要注意表現</h3><span class="chip" id="pmc-chip2"></span></div>',
  '<div class="first"><div class="lbl">1行目（初めて読む人が最初に目にする所）</div><div class="line" id="pmc-first"></div><div class="ask">この1行だけで、何の話か分かりますか？</div></div>',
  '<div id="pmc-finds"></div>',
  '<p class="sub" id="pmc-find-foot"></p>',
  '<details><summary>見る項目を選ぶ</summary>',
  '<div class="toggles">',
  '<label><input type="checkbox" id="pmc-on-leak">前の投稿を知らないと伝わりにくい言い回し（昨日の・前回の・例の など）</label>',
  '<label><input type="checkbox" id="pmc-on-report">1行目が「〜しました」の報告で終わっている</label>',
  '<label><input type="checkbox" id="pmc-on-deixis">1行目の「これ・それ・あれ」</label>',
  '</div></details>',
  '</section>',

'<div class="foot">',
  '<p class="small">このツールは、運営者が毎日の投稿前に見ている項目を、そのまま機械にしたものです。採点も添削もしません。引っかかった所を示すだけで、直すかどうかは自分で決めてください。</p>',
  '<p class="small">機械では見られないこと：内容がおもしろいか、刺さるか、1行目だけで話が通じるか。</p>',
  '<p class="small">Xの仕様が変わった場合は、追従できていないことがあります。</p>',
  '<p class="small">文字数の数え方・URLと絵文字の見つけ方は、Twitter, Inc. の twitter-text（Apache License 2.0）と twemoji-parser（MIT License）を元にしています。</p>',
  '</div>'
].join('');

/* ---------- 本体 ---------- */

function mount(host) {
  var settings = { enabled: { leak: true, report: true, deixis: true } };   // 見る項目のON/OFF。保存しない（開き直すと全部ON）

  var root = host.attachShadow ? host.attachShadow({ mode: 'open' }) : host;   // attachShadow が無い古い端末ではそのまま入れる
  if (root === host) host.textContent = '';
  var style = document.createElement('style');
  style.textContent = PMC_CSS;
  root.appendChild(style);
  var app = el('div', 'pmc');
  app.setAttribute('lang', 'ja');
  app.innerHTML = SKELETON;
  root.appendChild(app);
  var $ = function (id) { return app.querySelector('#pmc-' + id); };

  var ta = $('t');
  $('spec').textContent = SPEC_CHECKED;

  function setChip(node, cls, text) { node.className = 'chip' + (cls ? ' ' + cls : ''); node.textContent = text; }

  /* --- ① 文字数 --- */
  function renderCount(r, hasText) {
    $('w').textContent = r.weight;
    var meter = $('meter');
    var pct = Math.min(100, r.weight / r.max * 100);
    $('fill').style.width = pct + '%';
    meter.className = 'meter' + (r.over ? ' over' : (r.remaining <= 28 && hasText ? ' near' : ''));
    if (!hasText) $('msg').textContent = '入力すると、ここに文字数（Xの数え方）が出ます';
    else if (r.over) $('msg').textContent = (r.weight - r.max) + ' 超過（削る必要があります）';
    else $('msg').textContent = 'あと ' + r.remaining;

    if (!hasText) setChip($('chip1'), '', '入力待ち');
    else if (r.over) setChip($('chip1'), 'over', (r.weight - r.max) + ' 超過');
    else setChip($('chip1'), 'ok', '投稿できます（あと ' + r.remaining + '）');

    var tbl = $('tbl');
    clear(tbl);
    var rows = [
      ['日本語など（1字＝2）', r.heavy + '字', r.heavy * 2],
      ['半角英数・記号（1字＝1）', r.light + '字', r.light],
      ['URL（1件＝23）', r.urls.length + '件', r.urls.length * 23],
      ['絵文字（1個＝2）', r.emojis.length + '個', r.emojis.length * 2]
    ];
    rows.forEach(function (row) {
      var tr = el('tr');
      tr.appendChild(el('td', null, row[0]));
      tr.appendChild(el('td', null, row[1]));
      tr.appendChild(el('td', null, String(row[2])));
      tbl.appendChild(tr);
    });
    var sum = el('tr', 'sum');
    sum.appendChild(el('td', null, '合計（Xの数え方）'));
    sum.appendChild(el('td', null, ''));
    sum.appendChild(el('td', null, String(r.weight)));
    tbl.appendChild(sum);
    $('chars').textContent = '素の文字数（見た目の文字数）：' + r.chars + '字';

    var notes = $('count-notes');
    clear(notes);
    if (r.invalid) {
      notes.appendChild(el('div', 'note over', '投稿できない文字（U+FEFF など）が含まれています。貼り付け元から混ざった見えない文字の可能性があります。'));
    }
    if (r.urls.length) {
      var box = el('div', 'sub', 'URLとして23で数えたもの（スキームなしの example.com や、README.md のようなファイル名も、公式ライブラリは URL と見なします）');
      var ul = el('ul', 'list');
      r.urls.slice(0, 8).forEach(function (u) {
        var li = el('li');
        li.appendChild(el('code', null, u.url.length > 70 ? u.url.slice(0, 70) + '…' : u.url));
        li.appendChild(document.createTextNode(' → 23'));
        ul.appendChild(li);
      });
      notes.appendChild(box);
      notes.appendChild(ul);
      if (r.urls.length > 8) notes.appendChild(el('p', 'small', 'ほか ' + (r.urls.length - 8) + ' 件'));
    }
    if (r.uncertain.length) {
      var msg = el('div', 'note');
      msg.appendChild(document.createTextNode('次の絵文字は、公式ライブラリの表にない組み合わせなので部品ごとに数えています：'));
      r.uncertain.slice(0, 6).forEach(function (u, i) {
        msg.appendChild(document.createTextNode((i ? '、' : '') + u.text + ' → ' + u.weight));
      });
      msg.appendChild(document.createTextNode('。実際のXが2で数えるかは確認できていません。公式の数え方のままなので、重めの見積もりです。'));
      notes.appendChild(msg);
    }
  }

  /* --- ② 要注意表現 --- */
  var LABELS = {
    leak: { tag: '言い回し', what: '前の投稿を知らないと伝わりにくいかもしれない言い回し', msg: '書き手は前の出来事を知っていても、初めて読む人は知りません。その場で一言説明するか、消すかを確認してください。' },
    report: { tag: '1行目', what: '1行目が「〜しました」の報告で終わっています', msg: '何をしたかの報告で始まると、読む理由が見えにくくなります。数字・意外な点・「実は〜してませんでした」のような一言が1行目にあれば、この表示は出ません。' },
    deixis: { tag: '1行目', what: '1行目に「これ・それ・あれ」があります', msg: '1行目は前後の文脈なしで読まれます。何を指すか、初めて読む人にも通じるか確認してください。' }
  };

  function renderPhrases(text, hasText) {
    var res = PMC.checkPhrases(text, settings.enabled);
    var first = res.first.trim();
    $('first').textContent = first || '（下書きを入力すると、ここに1行目が出ます）';

    var finds = $('finds');
    clear(finds);
    var any = settings.enabled.leak || settings.enabled.report || settings.enabled.deixis;
    var shown = res.items.slice(0, 8);
    shown.forEach(function (it) {
      var lab = LABELS[it.kind];
      var box = el('div', 'find');
      var top = el('div');
      top.appendChild(el('span', 'tag', lab.tag));
      top.appendChild(el('span', 'what', it.kind === 'leak' ? '「' + it.match + '」があります' : lab.what));
      box.appendChild(top);
      box.appendChild(el('div', 'msg', lab.msg));
      var ctx = el('div', 'ctx');
      ctx.appendChild(context(text, it.index, it.length));
      box.appendChild(ctx);
      finds.appendChild(box);
    });
    if (res.items.length > shown.length) finds.appendChild(el('p', 'small', 'ほか ' + (res.items.length - shown.length) + ' 件'));

    if (!hasText) setChip($('chip2'), '', '入力待ち');
    else if (!any) setChip($('chip2'), '', 'すべてOFF');
    else if (res.items.length) setChip($('chip2'), 'warn', '確認 ' + res.items.length + '件');
    else setChip($('chip2'), 'ok', '拾えた所なし');

    $('find-foot').textContent = hasText && any && !res.items.length
      ? '拾えた所はありませんでした。機械で見られるのは言い回しの形だけです。内容が伝わるかは、1行目を読み返して確認してください。'
      : '';
  }

  function renderSettings() {
    $('on-leak').checked = settings.enabled.leak;
    $('on-report').checked = settings.enabled.report;
    $('on-deixis').checked = settings.enabled.deixis;
  }

  function render() {
    var text = ta.value.replace(/\r\n?/g, '\n');
    var hasText = text.trim() !== '';
    renderCount(PMC.weigh(text), hasText);
    renderPhrases(text, hasText);
  }

  /* --- 操作 --- */
  ta.addEventListener('input', render);
  $('clear').addEventListener('click', function () { ta.value = ''; render(); ta.focus(); });

  ['leak', 'report', 'deixis'].forEach(function (k) {
    $('on-' + k).addEventListener('change', function () {
      settings.enabled[k] = $('on-' + k).checked;
      render();
    });
  });

  renderSettings();
  render();
}

function start() {
  var host = document.getElementById('pmc-host');
  if (host && !host.getAttribute('data-pmc-mounted')) {
    host.setAttribute('data-pmc-mounted', '1');
    mount(host);
  }
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
