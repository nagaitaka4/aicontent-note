// operations/x-count.py を検証するための「公式の答え」を作る（node gen-xcount-expected.js）。
// 公式ライブラリ twitter-text 3.1.0 に、次の文章を数えさせて tests/out/xcount-cases.json に書く。Python側（xcount.py）が同じ文章を数えて比べる。
//   1. fixtures（公式の適合テスト＋手書きの代表例）
//   2. 乱数の文章（seed 2本）
//   3. Unicodeの全絵文字
//   4. 1文字ずつ全コードポイントを、URLの前後・ドメイン・TLD・パスに置いた文章（文字の種類ごとの食い違いを網羅する）
const fs = require('fs');
const path = require('path');
const tt = require('twitter-text');
const PMC = require('./load');
const { makeRandText } = require('./fuzz');

const out = { fixtures: [], fuzz: [], emoji: [], cp: {} };
const entry = (t) => {
  const n = t.normalize();
  return { t, w: tt.parseTweet(t).weightedLength, u: tt.extractUrlsWithIndices(n).map((x) => x.url), un: PMC.weigh(t).uncertain.map((x) => x.text) };
};

for (const c of JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'weight-cases.json'), 'utf8'))) {
  out.fixtures.push({ t: c.text, w: c.weight, source: c.source });     // 重みは公式の適合テストの値／手書き例は公式ライブラリの値
}
for (const seed of [20260930, 20261001]) {
  const rnd = makeRandText(seed);
  for (let i = 0; i < 30000; i++) out.fuzz.push(entry(rnd()));
}
const data = require('emojibase-data/en/data.json');
const emojis = [];
for (const d of data) { emojis.push(d.emoji); for (const s of d.skins || []) emojis.push(s.emoji); }
for (const e of emojis) {
  const t = 'あ' + e + 'い';
  out.emoji.push({ t, w: tt.parseTweet(t).weightedLength, uncertain: PMC.weigh(e).uncertain.length > 0, e });
}

// 全コードポイント（サロゲートを除く）：BMP全部＋0x10000–0x1FFFF＋0xE0000–0xE01FF（タグ・異体字セレクタ補助）
const templates = [
  (c) => 'x' + c + '.com', (c) => c + 'a.com', (c) => 'http://a.com/' + c + 'x', (c) => 'a.com/' + c, (c) => 'a.' + c + 'om', (c) => 'a.co' + c,
];
const ranges = [[0, 0xd7ff], [0xe000, 0xffff], [0x10000, 0x1ffff], [0xe0000, 0xe01ff]];
out.cpRanges = ranges;
out.cp.w = templates.map(() => []);
out.cp.u = templates.map(() => []);
for (const [a, b] of ranges) {
  for (let c = a; c <= b; c++) {
    const ch = String.fromCodePoint(c);
    templates.forEach((f, k) => {
      const t = f(ch);
      out.cp.w[k].push(tt.parseTweet(t).weightedLength);
      out.cp.u[k].push(tt.extractUrlsWithIndices(t.normalize()).length);
    });
  }
}
fs.mkdirSync(path.join(__dirname, 'out'), { recursive: true });
fs.writeFileSync(path.join(__dirname, 'out', 'xcount-cases.json'), JSON.stringify(out));
const n = out.fixtures.length + out.fuzz.length + out.emoji.length + out.cp.w[0].length * templates.length;
console.log('書き出し: tests/out/xcount-cases.json  文章', n, '本（fixtures', out.fixtures.length, '／乱数', out.fuzz.length, '／絵文字', out.emoji.length, '／1文字×', templates.length, '型', out.cp.w[0].length * templates.length, '）');
