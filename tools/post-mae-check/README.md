# 投稿まえチェック（X投稿チェッカー）

X（Twitter）に投稿する前に、**文字数・要注意表現・直近の投稿との重なり**を確認するWebツール。
ブラウザの中だけで動く（AIのAPIなし・外部通信なし・費用ゼロ）。スマホで使える。1ファイル。

元になった相談と回答：`operations/x-checker-gpt-prompt.md`

## 公開のしかた（WordPressに埋め込む）

固定ページの原稿は `pages/x-post-checker.md`（説明文・表・CTA）。スラッグは `x-post-checker`（2026-10-01 ユーザー確定）。**説明文＋ツール＋CTAを1本にした `dist/page.wp.txt` を貼る。**

1. `git pull` して、`tools/post-mae-check/dist/page.wp.txt` を開き、**全文をコピー**する
2. WordPressで**固定ページ**を新規作成 → 右上「⋮」→「コードエディター」に**全文を貼り付ける**（`md-to-wp.py` の出力を貼るときと同じ手順）
3. 先頭の段落ブロック「WPの入力欄に写す情報」を見て、タイトル・SEOタイトル・スラッグ・説明文を各欄に写し、**そのブロックは削除する**
4. 「ビジュアルエディター」に戻す → プレビューで動作確認 → 公開（アイキャッチは未作成。`knowledge/eyecatch-rules.md` の手順で）

作り直すとき：ツール（`src/`）を直したら `node build.js` → 原稿（`pages/x-post-checker.md`）を直したら `python3 tools/post-mae-check/compose-page.py`。後者が、ブロックの対応・CTA文言（最新の公開記事と一致）・ツールが1つだけ・MD記法の残りを検査してから `dist/page.wp.txt` を書く。

### CCにWordPressへ下書きを作らせる（Macのセッション・Chrome。固定ページでは未検証）

記事の入稿（`rules/article-flow.md` 7.6章）と同じく、**ログイン済みのChromeを操作できるMacのClaude Codeセッション**なら、下書き保存まで任せられる。クラウドのセッションでは**できない**（本番サイトへの通信が遮断されていて、ログインもできない）。公開ボタンは押さない（公開は人が判断する）。

固定ページは記事と違い、CCが入稿した前例がない。7.6章の手順を、次のように読み替える（**★は固定ページで未確認**）：

1. `git pull` して `python3 tools/post-mae-check/compose-page.py` を実行する。入稿に使うのは **`dist/page.body.wp.txt`**（入稿情報を除いた本文だけ。先頭は `core/paragraph` のリード）
2. Chromeで wp-admin を開き、ログイン済みか確認する。同じスラッグが無いことを確認する：`GET /wp-json/wp/v2/pages?slug=x-post-checker&status=any`
3. `POST /wp-json/wp/v2/pages` に `status:'draft'`・`title`・`slug`・`content`（page.body.wp.txt）を送る。**記事の `posts` ではなく `pages`**。カテゴリー・タグ・アイキャッチは無し
4. ★ツール本体の `<script>` が残っているか確認する（`GET …/pages/<id>?context=edit` の `content.raw`）。管理者アカウントなら残る。消えていたら、貼り付けでの入稿に切り替える
5. ★説明文（SEO SIMPLE PACK）はRESTでは入らない。エディターで `textarea[name="ssp_meta_description"]` に入れて保存する。**固定ページの編集画面にこの欄があるか未確認**
6. コメント・ピンバックを閉じる：`POST …/pages/<id> {comment_status:'closed', ping_status:'closed'}`（レスポンスで両方 `closed` を確認）
7. 数えて確認する。`compose-page.py` が出す値と合わせる：H2 4／表 3／`swl-marker` 1／CTAボタン 1／script 1。公開ページ（プレビュー）にMDの記法（`` ` ``・`**`・`==`）が残っていないかも見る
8. 開いているエディターは `location.reload()` で読み直す。**RESTで送ったあとに `savePost()` を呼ばない**（古い自動保存で上書きされる）

★SWELLの固定ページ設定（タイトルの表示・サイドバー・ツールを幅広に見せるテンプレート）はRESTで送れない可能性が高い。入稿後にあなたの画面で見る。

CTAは**最新の公開記事（2026-10-01時点はno.71 `claude-code-permission-modes`）の末尾からそのままコピー**してある（直近4本の公開記事で同一・`article-self-check.py` の標準文言とも一致）。新しい記事が公開されたら、`compose-page.py` の `LATEST_ARTICLE` と原稿のCTAを合わせ直す。

公開前の確認（この環境からは本番サイトに触れないため、**あなたの画面で1回**確かめる）：

- プレビューで、入力欄に文章を打つと重みが変わる（「JavaScriptが必要です」のままなら、スクリプトが除去されている。管理者アカウントで貼っているか確認）
- スマホ実機で入力できる・横スクロールが出ない
- サイトに入力内容を録画するタイプの計測（Clarity・Hotjar など）が入っていないか。入っていると、「送らない」と書いた文章が録画され得る。入っているなら、このページだけ除外する
- このツールには問い合わせへの導線（CTA）を入れていない。ページの前後に置くなら、`CLAUDE.md` のルールどおり、最新の公開記事からCTA文言をコピーして書く

単独ページとして出すなら `dist/post-mae-check.html`（同じ中身をHTML1枚にしたもの）。

## 他の人が使えるか（公開の状態・2026-10-01）

**他の人が使うことを前提に作ってある。** アカウント登録なし・サーバーなし・AIのAPIなし・費用ゼロで、URLを開けば誰でも使える。入力した文章は端末の外に出ない。

| 状態 | 内容 |
|---|---|
| ✅ できている | スマホ幅で使える（Chromiumのスマホ設定で確認）／サイトのCSSと混ざらない（Shadow DOM）／保存はその人のブラウザだけ／文字数は公式ライブラリと一致／「採点しない・添削しない」「運営者の見ている項目」と画面に明記／第三者ライセンス（Apache 2.0・MIT）の表記を配布物に同梱（THIRD-PARTY-NOTICES.md） |
| ⏳ 未公開 | まだWordPressに貼っていない。貼る作業と、本番サイトでの動作確認（上の「公開のしかた」）は運営者の作業 |
| ⚠️ 確認できていない | iPhone実機のSafari（確認はChromiumのスマホ設定だけ）／Xの現在の数え方（新しい絵文字・ファイル名風のURL・日本語を含むURL）／サイトに入力を録画する計測が入っていないか |
| 他の人には合わない所 | 要注意表現は**日本語の投稿向け**（文字数は言語を問わない）／直近の重なりは、**使う人が自分の投稿を自分で保存する**必要がある（Xのアカウントとは連携しない）／「よく出る語」の初期値は運営者の題材（Claude など）なので、画面で変えてもらう前提／Premiumの長文ポストは対象外 |
| ✅ 説明文とCTA | `pages/x-post-checker.md` に作成済み（CTAは最新の公開記事からコピー）。**関連記事カードは入れていない**（記事IDを本番サイトの公開APIから取る必要があり、クラウド環境から届かないため。入れるならMacで `md-to-wp.py` を実行する） |

## 機能（初版）

| # | 機能 | 基準 |
|---|---|---|
| ① | 文字数 | Xの公式ライブラリ **twitter-text 3.1.0（設定v3）** と同じ数え方。上限280。重み1は `0–4351`・`8192–8205`・`8208–8223`・`8242–8247`、それ以外は2。URLは一律23（スキームなし・ファイル名風の `README.md` も）。絵文字は1つ（ZWJ・肌色・国旗・キーキャップ含む）で2。数える前にNFC正規化 |
| ② | 要注意表現 | `operations/x-hook.py` のA（1行目が報告型の語尾）とC（前提を知らないと通じない言い回し：昨日の・前回の・この前の・例の…）をそのまま移植。加えて1行目の「これ・それ・あれ」。**NGとは言わず「確認」と出す**。1行目だけを別枠で見せる（「何の話か」は機械で判定しない）。項目ごとにON/OFF |
| ③ | 直近の重なり | `operations/x-cannibal.py` の基準をそのまま移植（3文字の重なり0.18以上／数字つきの語を共有／目印の語を2つ以上共有）。比べる相手は、ブラウザに保存した直近7・14・30日の投稿。「投稿した → 保存」と「まとめて追加」で入れる。よく出る語（Claude など）は画面で変えられる |

保存するのは「投稿した文章」と設定だけ。この端末のブラウザ（localStorage）の中にしか置かず、スマホとパソコンでは共有されない。保存が使えない環境（プライベートブラウズなど）でも、開いている間は動く。

**入れなかったもの**：`x-hook.py` のB（自分の話が真ん中にあるか）、`x-firstline.py`（1行目の固有名詞）、AIによる判定、Premiumの長文ポスト、端末間の同期・書き出し。

## 分からないこと・限界（画面にも書いてある）

- **公式ドキュメント本体（docs.x.com）は、作った環境から読めなかった。** 内容の元である公式OSS（twitter-text。npm最新は2020年3月の3.1.0）で確認した。**「X仕様確認日」は 2026-09-30**（`src/app.js` の `SPEC_CHECKED`）。Xの最新の数え方と違っていたら、ここが古い
- 公式ライブラリの絵文字表は古く、Emoji 11（2018年）までのもの。いまのUnicodeの絵文字3,979個のうち**1,077個（新しい並び・余計な異体字セレクタつき）は、公式ライブラリでは部品ごとに数えられ、2を超える**（例：❤️‍🔥＝5、😐️＝4）。実際のXが2で数えるかは**確認できていない**。画面は公式どおりに数え、該当の絵文字に「重めの見積もり」と注意書きを出す
- 日本語を含むURLは、公式ライブラリでは日本語の手前でURLが終わると数える。実際のXが全体を23で数えるかは確認できていない（そうなら画面の重みは実際より大きく出る＝安全側）
- 「1行目だけで何の話か分かるか」「おもしろいか」は、AIなしでは判定できない。見せるだけ

## テスト（`tests/`）

`npm install` のあと（`node_modules/` は git に入れない）：

| 何を | 件数（2026-09-30 実測） | コマンド |
|---|---|---|
| 公式の適合テスト＋手書きの代表例（日本語のみ・英数のみ・URL・絵文字）との一致 | 190件 | `node tests/run.js` |
| 公式ライブラリと、乱数で作った文章の重み・URLの一致 | 30,000件 | 同上 |
| Unicodeの全絵文字との一致、注意書きの過不足 | 3,979個 | 同上 |
| 要注意表現が `x-hook.py` と同じ判定か（リポジトリの実際の投稿・下書き＋手書き） | 175本 | `python3 tests/parity.py && node tests/parity.js` |
| 重なりが `x-cannibal.py` と同じ判定か（総当たり） | 174本（該当1,110組） | 同上 |
| 画面まわり（日付の範囲・まとめて追加・指示語・絵文字注意など） | 48件 | `node tests/unit.js` |
| **`operations/x-count.py` が公式と同じか**（適合テスト・手書き例53、乱数60,000、全絵文字3,979、全コードポイント×6型777,216。重み・URL・絵文字注意）＋CLIの出力4行・終了コード。約1分 | 841,248本 | `npm run test:xcount`（= `node tests/gen-xcount-expected.js && python3 tests/xcount.py`） |
| 組み立てた固定ページ（`dist/page.wp.txt`）を実ブラウザで表示：構造・CTAの文言とリンク・ページに組み込んでもツールが動く・スマホ幅・外部通信なし | 24件 | `NODE_PATH=/opt/node-tools/node_modules node tests/e2e-page.js` |
| 実ブラウザ（Chromium）：スマホ幅・外部通信ゼロ・WPふうの強いCSSの中・保存不可の環境・Shadow DOMなし | 48件 | `NODE_PATH=/opt/node-tools/node_modules node tests/e2e.js` |

まとめて：`npm test`（e2e以外）。わざとcoreを壊して、テストが落ちることも確認済み（重みの範囲・URLの重み・要注意語・重なりの基準）。

`tests/fixtures/` は「保存した正解」。**Xの仕様が変わったら、ここを更新して再テストする**。作り直すときは、公式の適合テストを取得してから：

```
mkdir -p tests/out
curl -o tests/out/validate.yml https://raw.githubusercontent.com/twitter/twitter-text/master/conformance/validate.yml
curl -o tests/out/extract.yml  https://raw.githubusercontent.com/twitter/twitter-text/master/conformance/extract.yml
node tests/gen-fixtures.js
```

## 作り直し・更新

- 画面や判定を直したら：`node build.js`（`dist/` が更新される）→ テスト → WPの固定ページを貼り直す
- 公式の正規表現を取り込み直す：`node tests/gen-vendor.js`（`src/vendor/twitter-text-regex.js` を上書き。手で直さない）
- 要注意表現の語を変えるとき：`src/core.js` と `operations/x-hook.py` を**両方**直す（`parity` テストが食い違いを見つける）
- 通信・外部読み込みにつながる書き方と、古いiPhoneで止まる書き方（後ろ向き先読みなど）は、`build.js` が検査して止める

## ファイル

```
src/core.js          計算の中核（文字数・要注意表現・重なり）
src/app.js           画面の動き
src/style.css        スタイル（Shadow DOMの中だけで効く＝SWELLのCSSと混ざらない）
src/vendor/          公式の正規表現（twitter-text 3.1.0 Apache-2.0／twemoji-parser 11.0.2 MIT）。自動生成
THIRD-PARTY-NOTICES.md  上のライセンス全文（自動生成）。dist/ のHTMLにも告知文を同梱している
build.js             1つのHTMLに束ねる
compose-page.py      固定ページ（説明文＋ツール＋CTA）を1本に組み立てる。検査つき
../../pages/x-post-checker.md   固定ページの原稿（説明文・CTA）
dist/                出力（page.wp.txt＝固定ページ丸ごと／page.body.wp.txt＝入稿情報を除いた本文だけ（REST用）／wp-block.txt＝ツールだけ／post-mae-check.html＝単独版）
tests/               テストと「保存した正解」（xcount.py＝operations/x-count.py の検証／fuzz.js＝乱数の文章／gen-*.js＝正解や正規表現の生成）
../../operations/x-count-data.json   x-count.py が読む公式の正規表現（tests/gen-vendor.js が自動生成。手で直さない）
x-count-diff.md      operations/x-count.py が公式とどこで食い違っていたかの一覧（修正前の記録）
```

## 関連：`operations/x-count.py`（2026-10-01に公式準拠へ修正済み）

毎日の文字数判定に使っている `x-count.py` は、修正前は公式の数え方と食い違っていた（矢印・三点リーダ・✅を1と数える／絵文字を部品で足す／URLの直後の「。」まで吸う／`.md`・`.py`・`.tokyo` など。280を超えているのに[OK]と出るケースがあった）。修正前の一覧と原因は `x-count-diff.md`（記録）。

- いまの `x-count.py` は、公式の正規表現を `operations/x-count-data.json`（`node tests/gen-vendor.js` が自動生成）から読み込み、公式と同じ手順で数える。`weight(text)`・`MAX_WEIGHT`・CLIの出力4行と終了コードは変えていない（`x-gate.py` はそのまま動く）
- CLIの出力に、URLとして23で数えたもの（`URL換算`）と、公式の表にない絵文字（`絵文字注意`）の行を足した
- 検証は上の表の `test:xcount`。数え方を直したら必ず通す
- 実データでの確認（2026-10-01）：投稿済み85本は新しい数え方でもすべて280以下。全154本（投稿済み85・キュー69）のうち22本の重みが変わり、キューの `閾値-気` だけが280→282で超過になる（→を2回使っているため）
- 「絵文字注意」の判定は、投稿まえチェック（`src/core.js`）と同じ。両方を `tests/xcount.py` が突き合わせている
