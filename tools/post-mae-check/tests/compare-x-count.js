// operations/x-count.py が、公式の数え方とどこで食い違うかを一覧にする（node tests/compare-x-count.js）。
// x-count.py は直さない。この一覧は、直すときの材料。
// 比べる文章：fixtures/weight-cases.json（公式の適合テスト＋手書きの代表例）。公式の値は fixtures の正解を使う。
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const script = path.join(__dirname, '..', '..', '..', 'operations', 'x-count.py');
const cases = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', 'weight-cases.json'), 'utf8'));
const rows = [];
for (const c of cases) {
  if (c.text.trim() === '') continue;                      // x-count.py は空入力を受け付けない
  const r = spawnSync('python3', [script, c.text], { encoding: 'utf8' });
  const m = /X重み\s*:\s*(\d+)/.exec(r.stdout);
  if (!m) continue;
  rows.push({ d: c.description, text: c.text, official: c.weight, mine: +m[1], src: c.source });
}
const diff = rows.filter((r) => r.official !== r.mine);
const esc = (s) => s.replace(/\n/g, '⏎').replace(/\|/g, '\\|');
const cut = (s) => (Array.from(s).length > 40 ? Array.from(s).slice(0, 40).join('') + '…' : s);
const out = [];
out.push('# x-count.py と公式の数え方の食い違い（自動生成）');
out.push('');
out.push('`node tests/compare-x-count.js` で作り直せる。公式＝X公式ライブラリ twitter-text 3.1.0（設定v3）。');
out.push('');
out.push(`比べた文章 ${rows.length} 本のうち、重みが食い違ったのは **${diff.length} 本**（全件を下に載せる）。`);
out.push(`x-count.py が少なく数える（280を超えているのに[OK]と出うる）のは ${diff.filter((r) => r.mine < r.official).length} 本、多く数えるのは ${diff.filter((r) => r.mine > r.official).length} 本。`);
out.push('');
out.push('| 文章（先頭40字） | 公式 | x-count.py | 差 | 出どころ |');
out.push('|---|---|---|---|---|');
for (const r of diff) out.push(`| ${esc(cut(r.text))} | ${r.official} | ${r.mine} | ${r.mine - r.official > 0 ? '+' : ''}${r.mine - r.official} | ${r.src === 'official-conformance' ? '公式の適合テスト' : '手書きの代表例'}：${esc(cut(r.d))} |`);
out.push('');
out.push('## 原因（x-count.py 側・いずれも実際に動かして確かめた）');
out.push('');
out.push('1. **`LIGHT_RANGES`（重み1の範囲）が公式より広い** → 少なく数える。公式は `0–4351`・`8192–8205`・`8208–8223`・`8242–8247` の4つだけ。x-count.py は矢印（→）・三点リーダ（…）・米印（※）・丸数字（①）・★・♪・✅ なども重み1にしている');
out.push('2. **絵文字を1つの塊として数えていない** → 多く数える。ZWJつなぎ（👨‍👩‍👧‍👦）・肌色・国旗・キーキャップは、公式では1つで2。x-count.py は部品ごとに足す');
out.push('3. **URLの直後の文字まで URL に含めてしまう** → 少なく数える。`https?://\\S+` は空白まで続くので、`https://example.com。次の文` の「。次の文」まで23に吸われる（公式は `https://example.com` だけが23）。`(https://…/a_(b))` の末尾の `)` も同じ');
out.push('4. **ドメインの前の日本語を URL に巻き込む** → 少なく数える。`[\\w-]+` が日本語にも当たるので、`サイトはexample.com` 全体が23になる（公式は「サイトは」8＋URL23＝31）');
out.push('5. **TLD（.com など）の一覧が短く、前方一致する** → 少なくも多くも数える。一覧は `com・net・org・jp・io・ai・co・dev・app・me・to・so・tv・info・biz` だけで、`README.md`・`main.py` を拾わない。`foo.tokyo` は `.to` に前方一致して「foo.to（23）＋kyo（3）」＝26になる（公式は23）');
out.push('6. **日本語を含むURLの扱い** → 少なく数える。公式ライブラリは、パスに日本語が来るとその手前でURLが終わると数える（`https://example.com/日本語/パス` は URL23 ＋ 残りの文字）。x-count.py は全体を23にする。※実際のXがどちらで数えるかは確認できていない。公式ライブラリのとおりに数えると画面の重みは大きく出る（安全側）');
out.push('7. **ドメインの妥当性を見ていない** → 少なく数える。63字を超えるドメインのラベルなど、公式がURLと認めない文字列も、x-count.py は URL（23）にしてしまう');
out.push('8. **NFC正規化をしていない** → 多く数える。濁点が分解された「が」などは、公式は正規化してから数える');
out.push('');
fs.writeFileSync(path.join(__dirname, '..', 'x-count-diff.md'), out.join('\n'));
console.log(`比べた ${rows.length} 本 / 食い違い ${diff.length} 本（少なく数える ${diff.filter((r) => r.mine < r.official).length}・多く数える ${diff.filter((r) => r.mine > r.official).length}） → x-count-diff.md`);
