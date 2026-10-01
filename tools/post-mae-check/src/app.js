/* 投稿まえチェック：画面の動き
 *
 * 外部と通信しない（fetch・XMLHttpRequest・外部スクリプト・画像・フォントを使わない）。
 * 保存するのは「投稿した文章」と設定だけで、この端末のブラウザ（localStorage）の中にしか置かない。
 * PMC（core.js）と PMC_CSS（style.css）は、ビルド時に同じスコープへ並べて入れる。
 */

var SPEC_CHECKED = '2026-09-30';     // Xの仕様（文字数の数え方）を確かめた日。確かめ直したら更新する
var KEY_POSTS = 'pmc:v1:posts';
var KEY_SETTINGS = 'pmc:v1:settings';
var MAX_POSTS = 200;

/* ---------- 保存（localStorage。使えない環境ではページを開いている間だけメモリに持つ） ---------- */

function makeStore() {
  var mem = {};
  var ok = true;
  try {
    window.localStorage.setItem('pmc:probe', '1');
    window.localStorage.removeItem('pmc:probe');
  } catch (e) { ok = false; }
  return {
    get ok() { return ok; },
    get: function (key) {
      if (ok) {
        try {
          var v = window.localStorage.getItem(key);
          return v === null ? null : JSON.parse(v);
        } catch (e) { /* 壊れた値は無かったことにする */ }
      }
      return mem[key] === undefined ? null : mem[key];
    },
    set: function (key, val) {
      mem[key] = val;
      if (ok) {
        try { window.localStorage.setItem(key, JSON.stringify(val)); } catch (e) { ok = false; }
      }
    }
  };
}

function defaultSettings() {
  return { days: 14, common: PMC.DEFAULT_COMMON.slice(), enabled: { leak: true, report: true, deixis: true } };
}

function loadSettings(store) {
  var d = defaultSettings();
  var s = store.get(KEY_SETTINGS);
  if (!s || typeof s !== 'object') return d;
  if (s.days === 7 || s.days === 14 || s.days === 30) d.days = s.days;
  if (Array.isArray(s.common)) d.common = s.common.filter(function (w) { return typeof w === 'string' && w.trim(); }).slice(0, 60);
  if (s.enabled && typeof s.enabled === 'object') {
    ['leak', 'report', 'deixis'].forEach(function (k) { if (typeof s.enabled[k] === 'boolean') d.enabled[k] = s.enabled[k]; });
  }
  return d;
}

function loadPosts(store) {
  var p = store.get(KEY_POSTS);
  if (!Array.isArray(p)) return [];
  return p.filter(function (x) {
    return x && typeof x.id === 'string' && typeof x.text === 'string' && x.text.trim() && PMC.parseDate(x.date);
  });
}

/* ---------- 小さな道具 ---------- */

function el(tag, cls, text) {
  var e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined && text !== null) e.textContent = text;
  return e;
}
function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }
function oneLine(s) { return String(s).replace(/\s*\n\s*/g, ' ↵ '); }
function mmdd(date) { return date.slice(5).replace('-', '/'); }
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

function head(text) {
  var chars = Array.from(oneLine(text.trim()));
  return chars.length > 40 ? chars.slice(0, 40).join('') + '…' : chars.join('');
}

function newId() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 6); }

/* ---------- 画面の骨組み（ユーザーの文章は入れない静的な部分だけ） ---------- */

var SKELETON = [
  '<h2 class="title">投稿まえチェック</h2>',
  '<p class="lead">X投稿の文字数・前提語・直近の重なりを、投稿する前に確認します。</p>',
  '<p class="privacy">入力した文章はどこにも送りません。この端末のブラウザの中だけで処理します（AIも使っていません）。</p>',

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
  '<label><input type="checkbox" id="pmc-on-leak">前提を知らないと通じない言い回し（昨日の・前回の・例の など）</label>',
  '<label><input type="checkbox" id="pmc-on-report">1行目が「〜しました」の報告で終わっている</label>',
  '<label><input type="checkbox" id="pmc-on-deixis">1行目の「これ・それ・あれ」</label>',
  '</div></details>',
  '</section>',

  // ③ 直近の重なり
  '<section class="card" aria-labelledby="pmc-h3">',
  '<div class="card-head"><h3 class="card-title" id="pmc-h3">③ 直近の投稿との重なり</h3><span class="chip" id="pmc-chip3"></span></div>',
  '<p class="sub" id="pmc-ov-sum"></p>',
  '<div id="pmc-hits"></div>',
  '<div class="actions"><button type="button" class="btn" id="pmc-save">投稿した → 保存</button>',
  '<span class="row"><label for="pmc-date">日付</label><input type="date" id="pmc-date"></span></div>',
  '<div class="toast" id="pmc-toast" role="status" aria-live="polite"></div>',
  '<p class="small" id="pmc-store-note"></p>',
  '<details><summary>まとめて追加</summary>',
  '<p class="small">1件ずつ「---」だけの行で区切って貼り付けます。各件の最初の行が「2026-09-28」のような日付なら、その日付で保存します（なければ上の日付）。</p>',
  '<textarea class="bulk" id="pmc-bulk" rows="5" spellcheck="false" placeholder="2026-09-28&#10;1件目の文章&#10;---&#10;2026-09-29&#10;2件目の文章"></textarea>',
  '<div class="actions"><button type="button" class="btn sub-btn" id="pmc-bulk-add">まとめて追加</button></div>',
  '</details>',
  '<details><summary id="pmc-saved-sum">保存した投稿</summary>',
  '<div id="pmc-saved"></div>',
  '<div class="actions"><button type="button" class="btn danger" id="pmc-del-all">すべて削除</button></div>',
  '</details>',
  '<details><summary>比べ方の設定</summary>',
  '<div class="row" style="margin-top:8px"><label for="pmc-days">比べる期間</label><select id="pmc-days"><option value="7">直近7日</option><option value="14">直近14日</option><option value="30">直近30日</option></select></div>',
  '<p class="small" style="margin-top:10px">よく出る語（「Claude」のように、どの投稿にも出る名前は重なりの目印に数えません。読点「、」かカンマで区切ります）</p>',
  '<input type="text" class="txt" id="pmc-common" autocomplete="off" spellcheck="false">',
  '<div class="actions"><button type="button" class="btn sub-btn" id="pmc-common-reset">初期値に戻す</button></div>',
  '</details>',
  '<p class="small" style="margin-top:10px">「重なり」は、同じ数字・同じ目印の語・似た文章が続いていないかの目安です。禁止ではありません。続き物として出すか、題材や数字を替えるかを決めるための確認です。保存先はこの端末のこのブラウザだけで、スマホとパソコンでは共有されません。ブラウザのサイトデータを消すと消えます。</p>',
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
  var store = makeStore();
  var settings = loadSettings(store);
  var posts = loadPosts(store);

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

  var today = function () { return PMC.dateToString(new Date()); };
  $('date').value = today();

  function setChip(node, cls, text) { node.className = 'chip' + (cls ? ' ' + cls : ''); node.textContent = text; }

  /* --- ① 文字数 --- */
  function renderCount(r, hasText) {
    $('w').textContent = r.weight;
    var meter = $('meter');
    var pct = Math.min(100, r.weight / r.max * 100);
    $('fill').style.width = pct + '%';
    meter.className = 'meter' + (r.over ? ' over' : (r.remaining <= 28 && hasText ? ' near' : ''));
    if (!hasText) $('msg').textContent = '入力すると、ここに重みが出ます';
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
    sum.appendChild(el('td', null, '合計（重み）'));
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
      var box = el('div', 'sub', 'URLとして23で数えたもの（スキームなしの example.com やファイル名の README.md も、Xは URL と見なします）');
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
    leak: { tag: '前提語', what: '前を知らないと通じないかもしれない言い回し', msg: '書き手は前の出来事を知っていても、初めて読む人は知りません。その場で一言説明するか、消すかを確認してください。' },
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

  /* --- ③ 直近の重なり --- */
  function renderOverlap(text, hasText) {
    var recent = PMC.recentPosts(posts, settings.days, today());
    $('ov-sum').textContent = '比べる投稿：直近' + settings.days + '日の' + recent.length + '件（保存してあるのは' + posts.length + '件）';
    var hitsBox = $('hits');
    clear(hitsBox);
    var hits = hasText ? PMC.findOverlaps(text, recent, { common: settings.common }) : [];
    hits.slice(0, 6).forEach(function (h) {
      var box = el('div', 'hit');
      box.appendChild(el('div', 'what', mmdd(h.post.date) + ' の投稿と重なっています'));
      var why = [];
      why.push('文章の重なり ' + h.jaccard.toFixed(2) + (h.jaccard >= PMC.JACCARD ? '（' + PMC.JACCARD + ' 以上）' : ''));
      if (h.nums.length) why.push('数字つきの語が同じ：' + h.nums.join('・'));
      var others = h.shared.filter(function (s) { return h.nums.indexOf(s) < 0; });
      if (others.length) why.push('目印の語が同じ：' + others.join('・'));
      box.appendChild(el('div', 'why', why.join(' ／ ')));
      box.appendChild(el('div', 'ctx', '「' + head(h.post.text) + '」'));
      hitsBox.appendChild(box);
    });
    if (hits.length > 6) hitsBox.appendChild(el('p', 'small', 'ほか ' + (hits.length - 6) + ' 件'));
    if (hits.length) hitsBox.appendChild(el('p', 'sub', '禁止ではありません。続き物として出すか、題材・数字を替えるかを決めてください。'));

    if (!posts.length) setChip($('chip3'), '', '比べる投稿なし');
    else if (!hasText) setChip($('chip3'), '', '入力待ち');
    else if (hits.length) setChip($('chip3'), 'warn', '重なり ' + hits.length + '件');
    else setChip($('chip3'), 'ok', '重なりなし');

    if (!posts.length) hitsBox.appendChild(el('p', 'sub', 'まだ比べる投稿がありません。投稿したら「投稿した → 保存」を押すと、次の下書きから比べられます。'));
  }

  function renderSaved() {
    var box = $('saved');
    clear(box);
    var sorted = posts.slice().sort(function (a, b) { return a.date < b.date ? 1 : (a.date > b.date ? -1 : 0); });
    $('saved-sum').textContent = '保存した投稿（' + posts.length + '件）';
    sorted.forEach(function (p) {
      var row = el('div', 'saved-row');
      row.appendChild(el('span', 'd', mmdd(p.date)));
      row.appendChild(el('span', 't', head(p.text)));
      var del = el('button', 'link', '削除');
      del.type = 'button';
      del.setAttribute('data-id', p.id);
      del.setAttribute('aria-label', mmdd(p.date) + ' の投稿を削除');
      row.appendChild(del);
      box.appendChild(row);
    });
    if (!posts.length) box.appendChild(el('p', 'small', '保存した投稿はありません。'));
    $('del-all').disabled = !posts.length;
    $('store-note').textContent = store.ok ? '' : 'この環境ではブラウザに保存できません（プライベートブラウズなど）。保存した投稿は、このページを開いている間だけ使えます。';
  }

  function renderSettings() {
    $('days').value = String(settings.days);
    $('common').value = settings.common.join('、');
    $('on-leak').checked = settings.enabled.leak;
    $('on-report').checked = settings.enabled.report;
    $('on-deixis').checked = settings.enabled.deixis;
  }

  function render() {
    var text = ta.value.replace(/\r\n?/g, '\n');
    var hasText = text.trim() !== '';
    renderCount(PMC.weigh(text), hasText);
    renderPhrases(text, hasText);
    renderOverlap(text, hasText);
  }

  function toast(msg, isErr) {
    var t = $('toast');
    t.textContent = msg;
    t.className = 'toast' + (isErr ? ' err' : '');
  }

  function persistPosts() {
    posts.sort(function (a, b) { return a.date < b.date ? 1 : (a.date > b.date ? -1 : 0); });
    if (posts.length > MAX_POSTS) posts = posts.slice(0, MAX_POSTS);
    store.set(KEY_POSTS, posts);
  }

  function addPosts(list) {
    var added = 0, skipped = 0;
    list.forEach(function (x) {
      var key = x.text.replace(/\s+/g, '');
      var dup = posts.some(function (p) { return p.text.replace(/\s+/g, '') === key; });
      if (dup) { skipped++; return; }
      posts.push({ id: newId(), date: x.date, text: x.text });
      added++;
    });
    if (added) persistPosts();
    return { added: added, skipped: skipped };
  }

  /* --- 操作 --- */
  ta.addEventListener('input', function () { toast(''); render(); });
  $('clear').addEventListener('click', function () { ta.value = ''; toast(''); render(); ta.focus(); });

  $('save').addEventListener('click', function () {
    var t = ta.value.replace(/\r\n?/g, '\n').replace(/^\s+|\s+$/g, '');
    if (!t) { toast('下書きが空です。', true); return; }
    var date = $('date').value || today();
    if (!PMC.parseDate(date)) { toast('日付を選んでください。', true); return; }
    var r = addPosts([{ date: date, text: t }]);
    if (r.added) { toast('保存しました（' + mmdd(date) + '）。次の下書きから比べます。'); } else { toast('同じ文章がすでに保存されています。', true); }
    renderSaved();
    render();
  });

  $('bulk-add').addEventListener('click', function () {
    var list = PMC.parseBulk($('bulk').value, $('date').value || today());
    if (!list.length) { toast('追加する文章がありません。', true); return; }
    var r = addPosts(list);
    toast(r.added + '件を追加しました' + (r.skipped ? '（' + r.skipped + '件は同じ文章があるため追加しませんでした）' : '。'), r.added === 0);
    if (r.added) $('bulk').value = '';
    renderSaved();
    render();
  });

  $('saved').addEventListener('click', function (ev) {
    var id = ev.target && ev.target.getAttribute && ev.target.getAttribute('data-id');
    if (!id) return;
    posts = posts.filter(function (p) { return p.id !== id; });
    store.set(KEY_POSTS, posts);
    renderSaved();
    render();
  });

  $('del-all').addEventListener('click', function () {
    if (!posts.length) return;
    if (!window.confirm('保存した投稿をすべて削除します。よろしいですか？')) return;
    posts = [];
    store.set(KEY_POSTS, posts);
    toast('すべて削除しました。');
    renderSaved();
    render();
  });

  $('days').addEventListener('change', function () { settings.days = +$('days').value; store.set(KEY_SETTINGS, settings); render(); });
  $('common').addEventListener('change', function () {
    settings.common = $('common').value.split(/[,，、\n]+/).map(function (s) { return s.trim(); }).filter(Boolean).slice(0, 60);
    store.set(KEY_SETTINGS, settings);
    render();
  });
  $('common-reset').addEventListener('click', function () {
    settings.common = PMC.DEFAULT_COMMON.slice();
    store.set(KEY_SETTINGS, settings);
    renderSettings();
    render();
  });
  ['leak', 'report', 'deixis'].forEach(function (k) {
    $('on-' + k).addEventListener('change', function () {
      settings.enabled[k] = $('on-' + k).checked;
      store.set(KEY_SETTINGS, settings);
      render();
    });
  });

  renderSettings();
  renderSaved();
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
