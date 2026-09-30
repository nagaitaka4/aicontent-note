// 文字数・URLの「保存した正解」を作る。
//   node gen-fixtures.js
// ・公式の適合テスト（conformance/*.yml）の期待値はそのまま使う
// ・手書きの代表例の期待値は、公式ライブラリ twitter-text 3.1.0 に出してもらう
// 出力: fixtures/weight-cases.json, fixtures/url-cases.json
// 公式の適合テストは tests/out/ に置いたものを読む（取得方法は README）
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const tt = require('twitter-text');

const out = path.join(__dirname, 'out');
const readYaml = (f) => {
  const p = path.join(out, f);
  if (!fs.existsSync(p)) throw new Error(f + ' が tests/out/ にありません（README の「公式テストの取得」を参照）');
  return yaml.load(fs.readFileSync(p, 'utf8')).tests;
};
const validate = readYaml('validate.yml');
const extract = readYaml('extract.yml');

const weight = [];
for (const k of ['WeightedTweetsWithDiscountedEmojiCounterTest', 'UnicodeDirectionalMarkerCounterTest']) {
  for (const t of validate[k]) {
    // 公式の期待値と、いま入っている公式ライブラリの結果が食い違っていないかも確かめる
    const lib = tt.parseTweet(t.text).weightedLength;
    if (lib !== t.expected.weightedLength) throw new Error('公式テストとライブラリが不一致: ' + t.description);
    weight.push({ source: 'official-conformance', description: t.description, text: t.text, weight: t.expected.weightedLength, valid: t.expected.valid });
  }
}

// 手書きの代表例（GPTの助言：日本語だけ・英数字だけ・URL・絵文字のテスト例を保存して再テスト）
const hand = [
  ['日本語だけ', '今日は記事を書きました。'],
  ['日本語の句読点と括弧', '「かぎ括弧」と（全角括弧）、そして『二重』。'],
  ['英数字だけ', 'Claude Code 2.1.283 is out'],
  ['日本語と英数字', 'Claude Codeで作りました'],
  ['半角カナ', 'ｱｲｳｴｵ ｶﾞ'],
  ['矢印・三点リーダ・米印（重み2）', '矢印→と…と※と•'],
  ['丸数字・星・音符（重み2）', '①②③★☆♪'],
  ['チェックマーク', '完了✅'],
  ['引用符・ダッシュ（重み1）', '“quote” ‘s’ — – ―'],
  ['絵文字1つ', '絵文字😀だけ'],
  ['絵文字：家族（ZWJ）', '家族👨‍👩‍👧‍👦です'],
  ['絵文字：肌色', '肌色🙋🏽です'],
  ['絵文字：国旗', '国旗🇯🇵です'],
  ['絵文字：ハート（異体字セレクタあり・なし）', 'ハート❤️と❤'],
  ['絵文字：キーキャップ', 'キーキャップ1️⃣です'],
  ['URL：https', 'URLは https://example.com/very/long/path?x=1&y=2 です'],
  ['URL：スキームなし', '裸ドメイン example.com と google.com/goto です'],
  ['URL：t.co', '短縮 https://t.co/abc123 です'],
  ['URL：新しめのTLD', 'foo.tokyo と bar.dev/x と baz.app'],
  ['URL：ファイル名っぽいもの（.md .py はURL扱い）', 'README.md と main.py と index.js'],
  ['URL：バージョン番号', 'v2.1.283 と 1.5.0 と Claude.ai'],
  ['URL：メールアドレス', 'メール a@example.com です'],
  ['URL：日本語パス', 'https://example.com/日本語/パス?q=1#frag'],
  ['URL：ドメインの前に日本語', 'サイトはexample.comです'],
  ['URL：括弧つき', '(https://example.com/a_(b)) です'],
  ['URL：末尾の句点', 'https://example.com。次の文'],
  ['NFC：分解された濁点', 'が'],
  ['空文字', ''],
  ['改行だけ', '\n\n'],
];
for (const [d, t] of hand) {
  weight.push({ source: 'library-3.1.0', description: d, text: t, weight: tt.parseTweet(t).weightedLength, valid: tt.parseTweet(t).valid });
}

const urls = [];
for (const k of ['urls', 'urls_with_directional_markers', 'tco_urls_with_params']) {
  for (const t of extract[k]) urls.push({ source: 'official-conformance', description: t.description, text: t.text, urls: t.expected.map((e) => (typeof e === 'string' ? e : e.url)) });
}
for (const t of extract.urls_with_indices) {
  urls.push({ source: 'official-conformance', description: t.description, text: t.text, urls: t.expected.map((e) => e.url) });
}
for (const [d, t] of hand) {
  const n = t.normalize();
  urls.push({ source: 'library-3.1.0', description: d, text: t, urls: tt.extractUrlsWithIndices(n).map((u) => u.url) });
}

fs.mkdirSync(path.join(__dirname, 'fixtures'), { recursive: true });
fs.writeFileSync(path.join(__dirname, 'fixtures', 'weight-cases.json'), JSON.stringify(weight, null, 1) + '\n');
fs.writeFileSync(path.join(__dirname, 'fixtures', 'url-cases.json'), JSON.stringify(urls, null, 1) + '\n');
console.log('weight-cases:', weight.length, '件 / url-cases:', urls.length, '件');
