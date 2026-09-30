// 文字数・URL・絵文字の計算テスト（node run.js）
//   1. 保存した正解（fixtures/）と一致するか
//   2. 公式ライブラリ twitter-text 3.1.0 と、乱数で作った大量の文章で一致するか（--fuzz N、既定 30000）
const fs = require('fs');
const path = require('path');
const PMC = require('./load');
const tt = require('twitter-text');

let fail = 0, pass = 0;
const ng = (msg) => { fail++; if (fail <= 25) console.log('  [NG] ' + msg); };
const ok = () => { pass++; };

// 1-a. 文字数の保存した正解
for (const c of JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'weight-cases.json'), 'utf8'))) {
  const r = PMC.weigh(c.text);
  const valid = !r.invalid && r.weight > 0 && r.weight <= PMC.SPEC.maxWeight;
  if (r.weight === c.weight && valid === c.valid) ok();
  else ng(`[文字数/${c.source}] ${c.description}: 期待 ${c.weight}(valid=${c.valid}) 実際 ${r.weight}(valid=${valid})`);
}
// 1-b. URLの保存した正解
for (const c of JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'url-cases.json'), 'utf8'))) {
  const got = PMC.extractUrls(c.text.normalize()).map((u) => u.url);
  if (JSON.stringify(got) === JSON.stringify(c.urls)) ok();
  else ng(`[URL/${c.source}] ${c.description}: 期待 ${JSON.stringify(c.urls)} 実際 ${JSON.stringify(got)}`);
}
console.log(`保存した正解: ${pass} 件一致 / ${fail} 件不一致`);

// 2. 乱数での突き合わせ
const argN = process.argv.indexOf('--fuzz');
const N = argN >= 0 ? +process.argv[argN + 1] : 30000;
function rng(seed) { return () => { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const rand = rng(20260930);
const pick = (a) => a[Math.floor(rand() * a.length)];
const chars = (s) => Array.from(s);
const pools = [
  chars('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞっゃゅょー'),
  chars('日本語文字数検証投稿記事運用実測確認公式仕様読者前提昨日今日'),
  chars('アイウエオカキクケコサシスセソタチツテトナニヌネノ'),
  chars('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'),
  chars(' .,:;!?-_/()@#$%&*+=~|\'"<>[]{}'),
  chars('→←↑↓…・※①②③★☆♪♫✅❤❗‼⁉™©®℃°±×÷—–―‐“”‘’「」『』（）【】〜～、。，．'),
  ['😀', '😷', '👾', '🔥', '💩', '🙋🏽', '👨‍🎤', '👨‍👩‍👧‍👦', '🇯🇵', '🇺🇸', '🏴󠁧󠁢󠁥󠁮󠁧󠁿', '❤️', '❤', '✅', '1️⃣', '#️⃣', '*️⃣', '0️⃣', '©️', '®️', '™️', '☺️', '☺', '🧑‍🦰', '🫶', '🐦‍🔥', '🤝🏻', '👍', '👍🏿', '🎉', '⭐', '✨', '⚠️', '⚠', '▶️', '▶', '🅰️', '🈁', '🧑‍💻', '👩‍🔬', '🏃‍♀️', '🤷‍♂️'],
  ['https://example.com', 'http://t.co/abc123', 'https://t.co/abc123?x=1', 'example.com/path', 'foo.tokyo', 'README.md', 'index.js', 'main.py', 'a.b', 'v2.1.283', '1.5.0', 'x.com/aicontent_note', 'claude.ai', 'user@example.com', 'https://example.com/日本語/パス?q=1#frag', 'www.google.co.jp', 'github.com/nagaitaka4/aicontent-note', 'bit.ly/3xYz', 'localhost:3000', '192.168.0.1', 'ftp://x.com', 'https://例え.jp/テスト', 'foo.bar.baz.com', 'Node.js', 'pages.dev', 'example.com:8080/a', '(https://example.com/a_(b))', 'https://example.com/a.', 'xn--eckwd4c7c.jp', 'test.co.jp。', 'ABC.COM', 'ai.tools'],
  [' ', ' ', '\n', '\n\n', '　', '‍', '️', '​', ' ', '\t', '﻿', '‪'],
  ['が', 'é', 'ｱｲｳ', 'ｶﾞ', '㌔', 'ﬁ', 'Ⅳ', '①', ' '],
];
function rndText() {
  const n = 1 + Math.floor(rand() * 14);
  let s = '';
  for (let i = 0; i < n; i++) {
    const p = pick(pools);
    s += pick(p);
    if (rand() < 0.15) s += ' ';
  }
  return s;
}
let fz = 0, fzNg = 0;
for (let i = 0; i < N; i++) {
  const t = rndText();
  const o = tt.parseTweet(t);
  const r = PMC.weigh(t);
  const valid = !r.invalid && r.weight > 0 && r.weight <= PMC.SPEC.maxWeight;
  const norm = t.normalize();
  const ou = tt.extractUrlsWithIndices(norm).map((u) => [u.url, u.indices[0], u.indices[1]]);
  const ru = PMC.extractUrls(norm).map((u) => [u.url, u.start, u.end]);
  fz++;
  if (o.weightedLength !== r.weight || o.valid !== valid || JSON.stringify(ou) !== JSON.stringify(ru)) {
    fzNg++; ng(`[乱数] ${JSON.stringify(t)}: 公式 ${o.weightedLength}(valid=${o.valid}) 自作 ${r.weight}(valid=${valid}) URL公式 ${JSON.stringify(ou)} 自作 ${JSON.stringify(ru)}`);
  }
}
console.log(`乱数の突き合わせ: ${fz - fzNg} / ${fz} 件一致`);

// 3. 絵文字の全一覧（emojibase-data：Unicodeの全絵文字、肌色違いを含む）
{
  const data = require('emojibase-data/en/data.json');
  const all = [];
  for (const d of data) {
    all.push({ e: d.emoji, name: d.label, ver: d.version });
    for (const s of d.skins || []) all.push({ e: s.emoji, name: s.label, ver: s.version });
  }
  let n = 0, nNg = 0;
  const notOne = [];
  for (const x of all) {
    const text = 'あ' + x.e + 'い';
    n++;
    if (tt.parseTweet(text).weightedLength !== PMC.weigh(text).weight) { nNg++; ng('[絵文字] ' + x.name); }
    const w = PMC.weigh(x.e);
    if (w.weight !== 2) notOne.push({ emoji: x.e, name: x.name, emojiVersion: x.ver, weight: w.weight });
    // 「重めに数えた絵文字」の注意書きが、2にならない絵文字と過不足なく一致するか
    if ((w.weight !== 2) !== (w.uncertain.length > 0)) ng(`[絵文字の注意書き] ${x.e} ${x.name}: 重み${w.weight} 注意書き${w.uncertain.length > 0 ? 'あり' : 'なし'}`);
  }
  console.log(`絵文字一覧（Unicode全件・${n}個）: ${n - nNg} / ${n} 件、公式と一致`);
  fs.writeFileSync(path.join(__dirname, 'out', 'emoji-not-two.json'), JSON.stringify(notOne, null, 1));
  console.log(`  うち「1つで2」にならない絵文字（公式ライブラリの表に無い並び）: ${notOne.length} 個 → tests/out/emoji-not-two.json`);
}

console.log(fail === 0 ? '\n全部一致' : `\n不一致 ${fail} 件`);
process.exit(fail === 0 ? 0 : 1);
