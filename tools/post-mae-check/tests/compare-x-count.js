// operations/x-count.py が、公式の数え方と食い違っていないかを、fixtures（公式の適合テスト＋手書きの代表例）で見る（node tests/compare-x-count.js）。
// 2026-10-01に x-count.py を公式準拠に直したので、食い違いは 0 本のはず。修正前の一覧は x-count-diff.md に記録として残してある。
// 約84万本の突き合わせは tests/xcount.py。
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
console.log(`比べた ${rows.length} 本 / 食い違い ${diff.length} 本`);
for (const r of diff) console.log(`  [NG] 公式 ${r.official} / x-count.py ${r.mine}  ${JSON.stringify(r.text.slice(0, 40))}  （${r.d}）`);
process.exit(diff.length ? 1 : 0);
