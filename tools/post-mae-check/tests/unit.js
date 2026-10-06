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
const cps = (...a) => String.fromCodePoint(...a);
const heartOnFire = cps(0x2764, 0xfe0f, 0x200d, 0x1f525);   // ❤️‍🔥（公式の表に無い並び）
eq('絵文字注意：新しい絵文字（❤️‍🔥）は部品ごとに数えるので注意', PMC.weigh(heartOnFire).uncertain.map((u) => u.text), [heartOnFire]);
eq('絵文字注意：❤️‍🔥は重み5', PMC.weigh(heartOnFire).weight, 5);
eq('絵文字注意：家族の絵文字は1つで2なので注意しない', PMC.weigh(cps(0x1f468, 0x200d, 0x1f469, 0x200d, 0x1f467, 0x200d, 0x1f466)).uncertain, []);
eq('絵文字注意：ヒンディー語のZWJだけの並びは絵文字ではない', PMC.weigh(cps(0x915, 0x94d, 0x200d, 0x937)).uncertain, []);
eq('絵文字注意：数字の後ろのFE0Fだけは絵文字ではない', PMC.weigh('1' + cps(0xfe0f)).uncertain, []);
eq('素の文字数は絵文字を1と数える', PMC.weigh('👨‍👩‍👧‍👦').chars, 7);
eq('README.md はURL扱い', PMC.weigh('README.md').urls.map((u) => u.url), ['README.md']);
eq('投稿できない文字（U+FEFF）', PMC.weigh('a\ufeffb').invalid, true);

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

// --- AIっぽく読まれやすい形（v2・2026-10-06） ---
const ai = (t, en) => PMC.checkAiLike(t, en).map((i) => i.kind + ':' + i.match + (i.count ? 'x' + i.count : '') + (i.sub ? '/' + i.sub : ''));
eq('名詞に押し込めた言い回し（課金の要否）', ai('課金の要否は、使い方で決まります。'), ['noun:の要否']);
eq('名詞に押し込めた言い回し（取れる手・余儀なく・他なりません・言えるでしょう）', ai('取れる手が変わる。変更を余儀なくされた。偶然に他なりません。成功と言えるでしょう。').length, 4);
eq('決まり文句（ここまで〜してきました・という点が重要です）', ai('ここまで3つの方法を説明してきました。続けるという点が重要です。'), ['stock:ここまで3つの方法を説明してきました', 'stock:という点が重要です']);
eq('決まり文句は行をまたがない', ai('ここまで\n説明してきました'), []);
eq('抽象名詞は1行目だけ（明確なライン）', ai('明確なラインはありません。\n大きな差もありません。'), ['vague:なライン']);
eq('資料の紹介で終わる文（句点つきでも）', ai('公式は30日保存としています。'), ['source:としています']);
eq('資料の紹介：文の途中なら出さない', ai('としている人もいますが、私は違います。'), []);
eq('同じ締めが2回で出す（2回目の位置）', ai('今振り返ると楽しかった。今振り返ると長かった。'), ['repeat:今振り返るとx2']);
eq('同じ締めが1回なら出さない', ai('今振り返ると楽しかった。'), []);
eq('文の始めのつなぎが3回で出す', ai('また、Aです。さらに、Bです。次に、Cです。'), ['conj:次にx3']);
eq('文の始めのつなぎが2回なら出さない', ai('また、Aです。さらに、Bです。'), []);
eq('文の途中の「また」は数えない', ai('私もまた、そう思う。彼もまた、そう思う。君もまた、そう思う。'), []);
eq('同じ文末が4文続くと出す', ai('Aを使っています。Bを使っています。Cを使っています。Dを使っています。'), ['ending:ています。x4']);
eq('同じ文末が3文なら出さない', ai('Aを使っています。Bを使っています。Cを使っています。'), []);
eq('同じ文末が5文なら回数が5', ai('Aを使っています。Bを使っています。Cを使っています。Dを使っています。Eを使っています。'), ['ending:ています。x5']);
eq('使役の重ね', ai('資料を集めさせて、要点をまとめさせた。'), ['causative:させて、要点をまとめさせ']);
eq('使役の重ね：「任せて」「合わせて」は拾わない', ai('作業を任せて、予定を合わせて、結果を見せてもらった。'), []);
eq('X投稿の形：自分の話が最後の段落だけ', ai('新機能が出ました。\n\n料金は据え置きです。\n\n自分はまだ試していません。'), ['shape:自分/last']);
eq('X投稿の形：最後が問いかけ', ai('新機能が出ました。\n\n料金は据え置きです。\n\n自分の場合はどうしますか？'), ['shape:自分/reader']);
eq('X投稿の形：自分の話が真ん中なら出さない', ai('新機能が出ました。\n\n自分は試しました。\n\n料金は据え置きです。'), []);
eq('X投稿の形：1段落なら出さない', ai('新機能が出ました。自分はまだです。'), []);
eq('ON/OFF：言い回しをOFF', ai('課金の要否', { phrase: false, rhythm: true, shape: true }), []);
eq('ON/OFF：リズムをOFF', ai('また、A。さらに、B。次に、C。', { phrase: true, rhythm: false, shape: true }), []);
eq('ふつうの文には出ない', ai('Claude Codeで記事を書いています。昨日は3本書けました。正直、かなり楽になりました。'), []);
eq('空でも落ちない', PMC.checkAiLike(''), []);
eq('位置：該当箇所の全文中の位置', PMC.checkAiLike('ab\n課金の要否').map((i) => i.index), [5]);

console.log(`単体テスト: ${pass} 件一致 / ${fail} 件不一致`);
process.exit(fail ? 1 : 0);
