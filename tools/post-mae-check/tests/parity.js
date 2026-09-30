// 要注意表現・重なりを、既存の x-hook.py / x-cannibal.py と突き合わせる（後半）。先に python3 parity.py を実行しておく。
const fs = require('fs');
const path = require('path');
const PMC = require('./load');

const exp = JSON.parse(fs.readFileSync(path.join(__dirname, 'out', 'parity-expected.json'), 'utf8'));
let fail = 0;
const ng = (m) => { fail++; if (fail <= 25) console.log('  [NG] ' + m); };

// 要注意表現：A（1行目の報告型）と C（前提語）が Python 版と同じか
let hookOk = 0;
for (const t of exp.texts) {
  const r = PMC.checkPhrases(t.text, { leak: true, report: true, deixis: false });
  const report = r.items.find((i) => i.kind === 'report');
  const leaks = [...new Set(r.items.filter((i) => i.kind === 'leak').map((i) => i.match))].sort();
  const same = !!report === t.report && (report ? report.match : null) === t.tail && JSON.stringify(leaks) === JSON.stringify(t.leaks.slice().sort());
  if (same) hookOk++;
  else ng(`[要注意] ${t.label}: Python 報告型=${t.report}(${t.tail}) 前提語=${JSON.stringify(t.leaks)} / JS 報告型=${!!report}(${report && report.match}) 前提語=${JSON.stringify(leaks)}`);
}
console.log(`要注意表現（A・C）: ${hookOk} / ${exp.texts.length} 件、x-hook.py と一致`);

// 重なり：総当たりの結果が x-cannibal.py と同じか
const posts = exp.texts.filter((t) => t.text.trim()).map((t) => ({ id: t.label, date: '2026-01-01', text: t.text }));
let ovOk = 0, ovN = 0, pairs = 0;
for (const t of exp.texts) {
  if (!t.text.trim()) continue;
  ovN++;
  const py = exp.overlaps[t.label] || [];
  const js = PMC.findOverlaps(t.text, posts).map((h) => ({ other: h.post.id, jac: h.jaccard, shared: h.shared }));
  pairs += py.length;
  const pyMap = Object.fromEntries(py.map((h) => [h.other, h]));
  const jsMap = Object.fromEntries(js.map((h) => [h.other, h]));
  let same = Object.keys(pyMap).sort().join('|') === Object.keys(jsMap).sort().join('|');
  if (same) {
    for (const k of Object.keys(pyMap)) {
      if (Math.abs(pyMap[k].jac - jsMap[k].jac) > 1e-9 || JSON.stringify(pyMap[k].shared) !== JSON.stringify(jsMap[k].shared)) same = false;
    }
  }
  if (same) ovOk++;
  else ng(`[重なり] ${t.label}: Python ${py.length}件 / JS ${js.length}件（差：${Object.keys(pyMap).filter((k) => !jsMap[k]).concat(Object.keys(jsMap).filter((k) => !pyMap[k])).slice(0, 4).join(',')}）`);
}
console.log(`重なり: ${ovOk} / ${ovN} 本で、x-cannibal.py と同じ結果（該当の組 ${pairs} 件を含む）`);
console.log(fail === 0 ? '\n全部一致' : `\n不一致 ${fail} 件`);
process.exit(fail === 0 ? 0 : 1);
