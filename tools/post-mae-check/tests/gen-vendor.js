// 公式の twitter-text 3.1.0 が実際に使っている正規表現を、そのまま書き出す（手で写さない）。
//   node gen-vendor.js
// 出力: ../src/vendor/twitter-text-regex.js
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

const out = `/* 自動生成（tests/gen-vendor.js）。手で直さない。
 *
 * twitter-text ${ttVersion}  (c) Twitter, Inc.  Apache License 2.0  http://www.apache.org/licenses/LICENSE-2.0
 *   URLの見つけ方の正規表現（公式がそのまま使っているもの）
 * twemoji-parser ${twemojiVersion}  (c) Twitter, Inc.  MIT License  https://github.com/twitter/twemoji-parser/blob/master/LICENSE.md
 *   絵文字の見つけ方の正規表現（twitter-text ${ttVersion} が依存している版）
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
const dest = path.join(__dirname, '..', 'src', 'vendor', 'twitter-text-regex.js');
fs.writeFileSync(dest, out);
console.log('書き出し:', dest, out.length, 'bytes / twitter-text', ttVersion, '/ twemoji-parser', twemojiVersion);
