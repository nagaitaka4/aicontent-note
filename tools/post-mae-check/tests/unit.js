// 画面まわりの細かい機能の単体テスト（node unit.js）
const PMC = require('./load');
let fail = 0, pass = 0;
const eq = (name, got, want) => {
  const a = JSON.stringify(got), b = JSON.stringify(want);
  if (a === b) pass++; else { fail++; console.log(`  [NG] ${name}\n       期待 ${b}\n       実際 ${a}`); }
};

// --- 文字数（手で確かめられる値） ---
eq('日本語10字=20', PMC.weigh('あいうえおかきくけこ').weight, 20);
eq('英数字10字=10', PMC.weigh('abcdefghij').weight, 10);
eq('日本語140字=280・ぴったり投稿できる', [PMC.weigh('あ'.repeat(140)).weight, PMC.weigh('あ'.repeat(140)).over], [280, false]);
eq('日本語141字=282・超過', [PMC.weigh('あ'.repeat(141)).weight, PMC.weigh('あ'.repeat(141)).over], [282, true]);
eq('URLは長さに関係なく23', PMC.weigh('https://example.com/' + 'a'.repeat(200)).weight, 23);
eq('URLが2つなら46', PMC.weigh('https://a.com https://b.com').weight, 23 + 1 + 23);
eq('絵文字1つは2（家族）', PMC.weigh('👨‍👩‍👧‍👦').weight, 2);
eq('空文字は0・残り280', [PMC.weigh('').weight, PMC.weigh('').remaining], [0, 280]);
eq('素の文字数は絵文字を1と数える', PMC.weigh('👨‍👩‍👧‍👦').chars, 7);
eq('README.md はURL扱い', PMC.weigh('README.md').urls.map((u) => u.url), ['README.md']);
eq('投稿できない文字（U+FEFF）', PMC.weigh('a﻿b').invalid, true);

// --- 要注意表現 ---
const ph = (t, en) => PMC.checkPhrases(t, en).items.map((i) => i.kind + ':' + i.match);
eq('前提語：昨日の', ph('昨日の「無料でリセット」も、まだ押してません。'), ['leak:昨日の']);
eq('前提語：複数', ph('前回の続き。例の件。'), ['leak:前回の', 'leak:例の']);
eq('前提語は1行目以外でも拾う', ph('Claudeを試した。\n\n先日の設定のまま。'), ['leak:先日の']);
eq('報告型：1行目が「〜になりました。」', ph('使えるようになりました。無料プランも対象です。'), ['report:になりました']);
eq('報告型：1行目が「〜できました。」', ph('日本語でできました。'), ['report:できました']);
eq('報告型：数字があれば通す', ph('3本書きました。'), []);
eq('報告型：告白なら通す', ph('半年試してませんでした。'), []);
eq('報告型：落差の語があれば通す', ph('作りました。でも動かなかった。'), []);
eq('報告型は2行目以降を見ない', ph('Claudeの話。\n書きました。'), []);
eq('指示語：1行目のこれ', ph('これ、やってませんでした。\n本文'), ['deixis:これ']);
eq('指示語：これから・それぞれ・あれこれ・それでも は除く', ph('これから、それぞれ、あれこれ、それでも。'), []);
eq('指示語は2行目以降を見ない', ph('Claudeの話\nこれは本文'), []);
eq('ON/OFF：前提語だけOFF', ph('昨日の話', { leak: false, report: true, deixis: true }), []);
eq('ON/OFF：指示語だけOFF', ph('これの話', { leak: true, report: true, deixis: false }), []);
eq('1行目は空行を飛ばす', PMC.checkPhrases('\n\n  Claudeの話\n本文').first.trim(), 'Claudeの話');
eq('該当位置（全文の何文字目か）', PMC.checkPhrases('ab\n昨日の話').items[0].index, 3);
eq('空でも落ちない', PMC.checkPhrases('').items, []);

// --- 重なり ---
const P = (id, date, text) => ({ id, date, text });
eq('数字つきの語を共有すると要確認', PMC.findOverlaps('月100ドルのプランを使う', [P('a', '2026-09-29', 'Maxは100ドルです')]).map((h) => h.nums), [['100ドル']]);
eq('目印：よく出る語（Claude）は数えない', PMC.marks('Claudeで書いた', PMC.makeCommonSet()), []);
eq('目印：よく出る語を空にすると Claude も数える', PMC.marks('Claudeで書いた', PMC.makeCommonSet([])), ['Claude']);
eq('目印：数字つきの語と製品名', PMC.marks('月100ドルのSonnet 5.5と8,300字', PMC.makeCommonSet()), ['100ドル', 'Sonnet5.5', '8,300字']);
eq('よく出る語を空にすると Claude も目印になる（2語共有で要確認）', PMC.findOverlaps('Claude と Gemini で書いた', [P('a', '2026-09-29', 'Claude と Gemini を比べた')], { common: [] }).length, 1);
eq('同じ文章は比べない', PMC.findOverlaps('同じ投稿です', [P('a', '2026-09-29', '同じ 投稿です')]).length, 0);
eq('重なりが大きい順', PMC.findOverlaps('今日は朝から記事を書いて公開した', [P('a', '2026-09-29', '全然ちがう話'), P('b', '2026-09-28', '今日は朝から記事を書いて公開した話'), P('c', '2026-09-27', '今日は朝から記事を少し')]).map((h) => h.post.id), ['b', 'c']);
eq('短い文章でも落ちない', PMC.findOverlaps('あ', [P('a', '2026-09-29', 'い')]).length, 0);

// --- 保存した投稿まわり ---
const posts = [P('1', '2026-09-30', 'a'), P('2', '2026-09-16', 'b'), P('3', '2026-09-15', 'c'), P('4', '2026-09-01', 'd'), P('x', 'bad', 'e')];
eq('14日以内（今日から14日前の日を含む）', PMC.recentPosts(posts, 14, '2026-09-30').map((p) => p.id), ['1', '2']);
eq('7日以内', PMC.recentPosts(posts, 7, '2026-09-30').map((p) => p.id), ['1']);
eq('月をまたぐ（9/10の14日前＝8/27を含む）', PMC.recentPosts([P('a', '2026-08-27', 'a'), P('b', '2026-08-26', 'b')], 14, '2026-09-10').map((p) => p.id), ['a']);
eq('まとめて追加：区切りと日付', PMC.parseBulk('2026-09-28\n一つ目\n二行目\n---\n二つ目\n\n---\n日付：2026-09-27\n三つ目\n---\n', '2026-09-30'),
  [{ date: '2026-09-28', text: '一つ目\n二行目' }, { date: '2026-09-30', text: '二つ目' }, { date: '2026-09-27', text: '三つ目' }]);
eq('まとめて追加：空は無視', PMC.parseBulk('  \n---\n---', '2026-09-30'), []);
eq('まとめて追加：存在しない日付は本文に残す', PMC.parseBulk('2026-02-30\n本文', '2026-09-30'), [{ date: '2026-09-30', text: '2026-02-30\n本文' }]);
eq('日付の検証', [PMC.parseDate('2026-02-29'), PMC.parseDate('2026-02-28') !== null], [null, true]);

console.log(`単体テスト: ${pass} 件一致 / ${fail} 件不一致`);
process.exit(fail ? 1 : 0);
