// 公式の twitter-text 3.1.0 が実際に使っている正規表現を、そのまま書き出す（手で写さない）。
//   node tests/gen-vendor.js
// 出力: src/vendor/twitter-text-regex.js           （AIっぽさチェック用・JS）
//       ../../operations/x-count-data.json         （operations/x-count.py 用・Python用に変換済み）
const fs = require('fs');
const path = require('path');
const tt = require('twitter-text');
const twemojiPath = require.resolve('twemoji-parser/dist/lib/regex.js', {
  paths: [path.dirname(require.resolve('twitter-text'))],
});
const twemojiRe = require(twemojiPath).default;
const twemojiVersion = require(path.join(path.dirname(twemojiPath), '..', '..', 'package.json')).version;
const ttVersion = require('twitter-text/package.json').version;
const r = tt.regexen;

const need = { extractUrl: 'gi', validAsciiDomain: 'gi', validTcoUrl: 'i', invalidUrlWithoutProtocolPrecedingChars: '', invalidChars: '' };
for (const [k, f] of Object.entries(need)) {
  if (r[k].flags !== f) throw new Error(k + ' のフラグが想定と違う: ' + r[k].flags);
  if (/\(\?<[=!]/.test(r[k].source)) throw new Error(k + ' に先読み(後ろ向き)がある。古いiPhoneで動かない');
}
if (/\(\?<[=!]/.test(twemojiRe.source)) throw new Error('絵文字の正規表現に後ろ向き先読みがある');
if (twemojiRe.flags !== 'g') throw new Error('絵文字の正規表現のフラグが想定と違う: ' + twemojiRe.flags);

// ライセンス文面は、パッケージ同梱のファイルからそのまま引き写す（要約や言い換えをしない）
const ttLicense = fs.readFileSync(require.resolve('twitter-text/LICENSE'), 'utf8');
const twemojiLicense = fs.readFileSync(path.join(path.dirname(twemojiPath), '..', '..', 'LICENSE.md'), 'utf8').trim();
const apacheNotice = ttLicense.split('\n').slice(0, 13).join('\n').trim();      // 「Copyright 2011 Twitter, Inc. ... limitations under the License.」まで
if (!/limitations under the License\.$/.test(apacheNotice)) throw new Error('Apacheの告知文の範囲が想定と違う');
const comment = (txt) => txt.split('\n').map((l) => (' * ' + l).replace(/\s+$/, '')).join('\n');
if (/\*\//.test(apacheNotice + twemojiLicense + ttLicense)) throw new Error('ライセンス文面に */ が含まれている');

const out = `/*!
 * AIっぽさチェック（旧 投稿まえチェック）が使っている第三者の成果物。tests/gen-vendor.js が自動生成（手で直さない）。全文は THIRD-PARTY-NOTICES.md。
 *
 * ■ twitter-text ${ttVersion}  https://github.com/twitter/twitter-text
 *   URLの見つけ方の正規表現（公式がそのまま使っているもの）を取り出して使っている。
 *   数え方の手順（parseTweet・extractUrlsWithIndices）は、公式の実装を見て JavaScript で書き直したもの（変更あり）。
 *
${comment(apacheNotice)}
 *
 * ■ twemoji-parser ${twemojiVersion}  https://github.com/twitter/twemoji-parser
 *   絵文字の見つけ方の正規表現（twitter-text ${ttVersion} が依存している版）を取り出して使っている。
 *
${comment(twemojiLicense)}
 */
var TT = {
  extractUrl: ${JSON.stringify(r.extractUrl.source)},
  validAsciiDomain: ${JSON.stringify(r.validAsciiDomain.source)},
  validTcoUrl: ${JSON.stringify(r.validTcoUrl.source)},
  invalidUrlWithoutProtocolPrecedingChars: ${JSON.stringify(r.invalidUrlWithoutProtocolPrecedingChars.source)},
  invalidChars: ${JSON.stringify(r.invalidChars.source)},
  emoji: ${JSON.stringify(twemojiRe.source)},
  versions: { twitterText: ${JSON.stringify(ttVersion)}, twemojiParser: ${JSON.stringify(twemojiVersion)} }
};
`;
// 配布物に同梱する第三者ライセンスの全文（Apache License 2.0 は全文の写しを渡すことが条件）
fs.writeFileSync(path.join(__dirname, '..', 'THIRD-PARTY-NOTICES.md'),
  '# 第三者のライセンス\n\n自動生成（tests/gen-vendor.js）。パッケージ同梱の文面をそのまま写している。\n\n' +
  'AIっぽさチェック（旧 投稿まえチェック）と operations/x-count.py は、X公式の次の成果物から、正規表現（URLと絵文字の見つけ方）を取り出して使っている。' +
  '数え方の手順は公式の実装を見て書き直したもの（変更あり）。\n\n' +
  '---\n\n## twitter-text ' + ttVersion + '（Apache License 2.0）\nhttps://github.com/twitter/twitter-text\n\n```\n' + ttLicense.trim() + '\n```\n\n' +
  '---\n\n## twemoji-parser ' + twemojiVersion + '（MIT License）\nhttps://github.com/twitter/twemoji-parser\n\n```\n' + twemojiLicense + '\n```\n');
const dest = path.join(__dirname, '..', 'src', 'vendor', 'twitter-text-regex.js');
fs.writeFileSync(dest, out);
console.log('書き出し:', dest, out.length, 'bytes / twitter-text', ttVersion, '/ twemoji-parser', twemojiVersion);

// ---------- Python 用（operations/x-count.py が読む） ----------
// Python の正規表現はコードポイント単位で、JS のようなサロゲートペア表記（👨）は使えない。
// 絵文字の正規表現だけ、サロゲートペアをコードポイントに直す。変換が正しいかは tests/xcount.py が公式との一致で確かめる。
function surrogatesToCodePoints(src) {
  const hiRe = /^\\u(d[89ab][0-9a-f]{2})/i;
  const loRe = /^\\u(d[c-f][0-9a-f]{2})/i;
  const cp = (hi, lo) => 0x10000 + ((parseInt(hi, 16) - 0xd800) << 10) + (parseInt(lo, 16) - 0xdc00);
  const esc = (n) => '\\U' + n.toString(16).padStart(8, '0');
  let out = '';
  for (let i = 0; i < src.length;) {
    const rest = src.slice(i);
    const h = hiRe.exec(rest);
    if (h) {
      const after = rest.slice(6);
      const l = loRe.exec(after);
      if (l) { out += esc(cp(h[1], l[1])); i += 12; continue; }
      if (after[0] === '[') {
        const end = after.indexOf(']');
        const body = after.slice(1, end);
        let conv = '';
        for (const m of body.matchAll(/\\u(d[c-f][0-9a-f]{2})(?:-\\u(d[c-f][0-9a-f]{2}))?/gi)) {
          conv += esc(cp(h[1], m[1])) + (m[2] ? '-' + esc(cp(h[1], m[2])) : '');
        }
        // クラスの中身が低位サロゲートだけであること（それ以外が混ざっていたら変換できない）
        if (body.replace(/\\u(d[c-f][0-9a-f]{2})(?:-\\u(d[c-f][0-9a-f]{2}))?/gi, '') !== '') throw new Error('サロゲートのクラスに別の文字が混ざっている: ' + body);
        out += '[' + conv + ']';
        i += 6 + end + 1;
        continue;
      }
      throw new Error('高位サロゲートの後ろが想定外: ' + rest.slice(0, 20));
    }
    out += src[i];
    i++;
  }
  if (/\\u(d[89a-f][0-9a-f]{2})/i.test(out)) throw new Error('サロゲートが残っている');
  return out;
}
// JS の $（文字列の終わり）は、Python では「末尾の改行の手前」にも当たるので \Z にする
const toPy = (s) => s.replace(/\|\$\)/g, '|\\Z)');

// Extended_Pictographic（絵柄）の範囲。Python の re には \p{...} が無いので、範囲の表を渡す（x-count.py の「絵文字注意」用）
const pict = [];
{
  const re = /\p{Extended_Pictographic}/u;
  let start = -1;
  for (let c = 0; c <= 0x10ffff; c++) {
    const hit = !(c >= 0xd800 && c <= 0xdfff) && re.test(String.fromCodePoint(c));
    if (hit && start < 0) start = c;
    if (!hit && start >= 0) { pict.push([start, c - 1]); start = -1; }
  }
  if (start >= 0) pict.push([start, 0x10ffff]);
}

const pyData = {
  _comment: '自動生成（tools/post-mae-check/tests/gen-vendor.js）。手で直さない。operations/x-count.py が読む。' +
    'twitter-text ' + ttVersion + ' (c) Twitter, Inc. Apache License 2.0 の正規表現／twemoji-parser ' + twemojiVersion + ' (c) Twitter, Inc. MIT License の絵文字表。ライセンス全文：tools/post-mae-check/THIRD-PARTY-NOTICES.md',
  versions: { twitterText: ttVersion, twemojiParser: twemojiVersion },
  extractUrl: toPy(r.extractUrl.source),
  validAsciiDomain: toPy(r.validAsciiDomain.source),
  validTcoUrl: toPy(r.validTcoUrl.source),
  invalidUrlWithoutProtocolPrecedingChars: r.invalidUrlWithoutProtocolPrecedingChars.source,
  invalidChars: r.invalidChars.source,
  emoji: surrogatesToCodePoints(twemojiRe.source),
  pictographic: pict,
  pictographicNote: 'Extended_Pictographic の範囲（Node ' + process.versions.node + ' / Unicode ' + process.versions.unicode + '）',
};
const pyDest = path.join(__dirname, '..', '..', '..', 'operations', 'x-count-data.json');
fs.writeFileSync(pyDest, JSON.stringify(pyData, null, 1) + '\n');
console.log('書き出し:', pyDest, fs.statSync(pyDest).size, 'bytes');
