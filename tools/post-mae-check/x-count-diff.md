# x-count.py と公式の数え方の食い違い（自動生成）

`node tests/compare-x-count.js` で作り直せる。公式＝X公式ライブラリ twitter-text 3.1.0（設定v3）。

比べた文章 51 本のうち、重みが食い違ったのは **26 本**（全件を下に載せる）。
x-count.py が少なく数える（280を超えているのに[OK]と出うる）のは 12 本、多く数えるのは 14 本。

| 文章（先頭40字） | 公式 | x-count.py | 差 | 出どころ |
|---|---|---|---|---|
| 282 chars-xxxxxxxxxx-xxxxxxxxxx-xxxxxxxx… | 281 | 282 | +1 | 公式の適合テスト：282 chars with a normalized character wi… |
| H🐱☺👨‍👩‍👧‍👦 | 7 | 15 | +8 | 公式の適合テスト：Count a mix of single byte single word, … |
| 🙋🏽👨‍🎤 | 4 | 9 | +5 | 公式の適合テスト：Count unicode emoji chars outside the ba… |
| This is a tweet with general punctuation… | 110 | 113 | +3 | 公式の適合テスト：Handle General Punctuation Characters wi… |
| Long url with invalid domain labels and … | 12079 | 148 | -11931 | 公式の適合テスト：Handle long url with invalid domain labe… |
| randomurlrandomurlrandomurlrandomurlrand… | 68 | 23 | -45 | 公式の適合テスト：Handle a 64 character domain without pro… |
| あいうえおかきくけこあいうえおかきくけこあいうえおかきくけこあいうえおかきくけこ… | 358 | 264 | -94 | 公式の適合テスト：Do not allow > 140 CJK characters by vir… |
| 👨‍👩‍👧‍👦👨‍👩‍👧‍👦👨‍👩‍👧‍👦👨‍👩‍👧‍👦👨‍👩‍👧‍👦👨‍👩‍👧… | 280 | 1540 | +1260 | 公式の適合テスト：140 family emoji |
| Unicode 10.0 emoji: 🤪; 🧕; 🧕🏾; 🏴󠁧󠁢󠁥󠁮󠁧󠁿 | 34 | 48 | +14 | 公式の適合テスト：Unicode 10.0 emoji |
| Unicode 9.0 emoji: 🤠; 💃; 💃🏾 | 29 | 31 | +2 | 公式の適合テスト：Unicode 9.0 emoji |
| ⁦‪http://foobar.پاکستان/‬⁩ | 31 | 26 | -5 | 公式の適合テスト：Tweet text containing directional charac… |
| 矢印→と…と※と• | 18 | 14 | -4 | 手書きの代表例：矢印・三点リーダ・米印（重み2） |
| ①②③★☆♪ | 12 | 6 | -6 | 手書きの代表例：丸数字・星・音符（重み2） |
| 完了✅ | 6 | 5 | -1 | 手書きの代表例：チェックマーク |
| “quote” ‘s’ — – ― | 17 | 20 | +3 | 手書きの代表例：引用符・ダッシュ（重み1） |
| 家族👨‍👩‍👧‍👦です | 10 | 19 | +9 | 手書きの代表例：絵文字：家族（ZWJ） |
| 肌色🙋🏽です | 10 | 12 | +2 | 手書きの代表例：絵文字：肌色 |
| 国旗🇯🇵です | 10 | 12 | +2 | 手書きの代表例：絵文字：国旗 |
| キーキャップ1️⃣です | 18 | 20 | +2 | 手書きの代表例：絵文字：キーキャップ |
| foo.tokyo と bar.dev/x と baz.app | 77 | 80 | +3 | 手書きの代表例：URL：新しめのTLD |
| README.md と main.py と index.js | 62 | 32 | -30 | 手書きの代表例：URL：ファイル名っぽいもの（.md .py はURL扱い） |
| https://example.com/日本語/パス?q=1#frag | 43 | 23 | -20 | 手書きの代表例：URL：日本語パス |
| サイトはexample.comです | 35 | 27 | -8 | 手書きの代表例：URL：ドメインの前に日本語 |
| (https://example.com/a_(b)) です | 30 | 29 | -1 | 手書きの代表例：URL：括弧つき |
| https://example.com。次の文 | 31 | 23 | -8 | 手書きの代表例：URL：末尾の句点 |
| が | 2 | 4 | +2 | 手書きの代表例：NFC：分解された濁点 |

## 原因（x-count.py 側・いずれも実際に動かして確かめた）

1. **`LIGHT_RANGES`（重み1の範囲）が公式より広い** → 少なく数える。公式は `0–4351`・`8192–8205`・`8208–8223`・`8242–8247` の4つだけ。x-count.py は矢印（→）・三点リーダ（…）・米印（※）・丸数字（①）・★・♪・✅ なども重み1にしている
2. **絵文字を1つの塊として数えていない** → 多く数える。ZWJつなぎ（👨‍👩‍👧‍👦）・肌色・国旗・キーキャップは、公式では1つで2。x-count.py は部品ごとに足す
3. **URLの直後の文字まで URL に含めてしまう** → 少なく数える。`https?://\S+` は空白まで続くので、`https://example.com。次の文` の「。次の文」まで23に吸われる（公式は `https://example.com` だけが23）。`(https://…/a_(b))` の末尾の `)` も同じ
4. **ドメインの前の日本語を URL に巻き込む** → 少なく数える。`[\w-]+` が日本語にも当たるので、`サイトはexample.com` 全体が23になる（公式は「サイトは」8＋URL23＝31）
5. **TLD（.com など）の一覧が短く、前方一致する** → 少なくも多くも数える。一覧は `com・net・org・jp・io・ai・co・dev・app・me・to・so・tv・info・biz` だけで、`README.md`・`main.py` を拾わない。`foo.tokyo` は `.to` に前方一致して「foo.to（23）＋kyo（3）」＝26になる（公式は23）
6. **日本語を含むURLの扱い** → 少なく数える。公式ライブラリは、パスに日本語が来るとその手前でURLが終わると数える（`https://example.com/日本語/パス` は URL23 ＋ 残りの文字）。x-count.py は全体を23にする。※実際のXがどちらで数えるかは確認できていない。公式ライブラリのとおりに数えると画面の重みは大きく出る（安全側）
7. **ドメインの妥当性を見ていない** → 少なく数える。63字を超えるドメインのラベルなど、公式がURLと認めない文字列も、x-count.py は URL（23）にしてしまう
8. **NFC正規化をしていない** → 多く数える。濁点が分解された「が」などは、公式は正規化してから数える
