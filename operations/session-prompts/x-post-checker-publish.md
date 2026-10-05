# 新しいセッション用プロンプト：投稿まえチェック（X投稿チェッカー）をWordPressに載せる

作成：2026-10-05。**Macのセッション（ログイン済みのChromeを操作できる環境）で使う。**クラウドのセッションでは本番サイトに届かないので、できない。
下の枠の中を、新しいセッションの最初のメッセージとして貼る。

```
投稿まえチェック（X投稿チェッカー）を、WordPressに載せる作業をお願いします。ログイン済みのChrome（claude-in-chrome）で作業してください。公開ボタンは押さないでください（公開は私が判断します）。

■ 最初にやること（CLAUDE.mdの作業前ルール）
1. `git pull --rebase origin main`
2. `operations/session-handoff.md` と、`tools/post-mae-check/README.md`（「公開のしかた」「CCにWordPressへ下書きを作らせる」）を読む
3. `rules/article-flow.md` の7.6章を読み直す（記憶で動かない）
4. 作業ブランチ `claude/x-post-checker-v1-dzvj9w` が main に入っているか確認する：
   `git fetch origin claude/x-post-checker-v1-dzvj9w` → `git log origin/main..origin/claude/x-post-checker-v1-dzvj9w --oneline`
   入っていなければ、コミット一覧を私に見せて、mainに取り込んでよいか確認してからマージする（PRは作っていません）。コンフリクトが出たら、CLAUDE.mdのルールどおり自動で解消せず、ファイルごとに「Aの変更／Bの変更」を並べて私に聞いてください

■ クラウドで済んでいること（ファイルで確認して使う）
・ツール本体：`tools/post-mae-check/`（ビルド済み・テスト通過）。固定ページの原稿：`pages/x-post-checker.md`（slug `x-post-checker`・status draft・説明文とCTAつき）
・入稿用の出力：`tools/post-mae-check/dist/page.body.wp.txt`（入稿情報を除いた本文だけ。先頭は段落ブロックのリード）。作り直すときは `python3 tools/post-mae-check/compose-page.py`（CTAが最新の公開記事no.72と同文であることも検査する）
・アイキャッチ：`images/pages/x-post-checker-eyecatch.png`（1200×630）。altは `pages/x-post-checker.md` の `eyecatch_alt`。**保存名について**：固定ページには記事の`no`が無く、`eyecatch_XXXX.png`（`no`で管理）は使えない。`images/pages/service-banner.png` の前例に合わせて `images/pages/<slug>-eyecatch.png` にしてある。私が別の名前を指示したら、それに従う
・プライバシーポリシーの追記：`pages/privacy-policy.md` に新しい節「ブラウザに保存される情報について」（**MDだけ**。WPには未反映）

■ 作業1：固定ページ x-post-checker を下書きで作る
`tools/post-mae-check/README.md` の「CCにWordPressへ下書きを作らせる」の1〜9のとおりに進める（記事の`posts`ではなく**固定ページの`pages`**）。要点：
・先にログイン済みか（`#wpadminbar`）と、同じスラッグが無いこと（`GET /wp-json/wp/v2/pages?slug=x-post-checker&status=any`）を確認する。二重に作らない
・本文は `dist/page.body.wp.txt`。REST nonceは `fetch('/wp-admin/admin-ajax.php?action=rest-nonce')` の応答を使う。本文が大きい（約67KB）ので、7.6章の手順4のとおり分けて `window` 変数に積み、ページ側でSHA-256を突き合わせてから `status:'draft'` でPOSTする
・アイキャッチ：`media-new.php` のfile inputへ画像を流し込む → `POST /wp/v2/media/<id>` でalt → `POST /wp/v2/pages/<id> {featured_media}`
・タイトル「投稿まえチェック（X投稿チェッカー）」・スラッグ `x-post-checker`。SEOタイトルと説明文は `pages/x-post-checker.md` の `seo_title`・`description`（SEO SIMPLE PACKはRESTでは入らない。固定ページの編集画面に `textarea[name="ssp_meta_description"]` があるか確認して、あれば入れる。無ければ私に伝える）
・コメントとピンバックを閉じ、レスポンスで両方 `closed` を確認する
・**RESTで送ったあとに `savePost()` を呼ばない**。開いているエディターは `location.reload()` で読み直してから数える
・数えて合わせる値：**H2 4／表 3／`swl-marker` 1／CTAボタン 1／`<script>` 1**。`GET …/pages/<id>?context=edit` の `content.raw` に、ツールの `<script>` が残っているかを必ず見る（消えていたら、貼り付けでの入稿に切り替える方法を私に相談する）。先頭ブロックが段落であること、MDの記法（`` ` ``・`**`・`==`）が残っていないことも見る

■ 作業2：固定ページを、実際に開いて確認する（Chromeのプレビュー）
・入力欄に文章を打つと、文字数の重みが変わるか（「JavaScriptが必要です」のままなら、スクリプトが除去されている）
・SWELLの固定ページ設定（タイトルの表示・サイドバー・ツールの幅）とアイキャッチの表示を見て、私に報告する（RESTで送れない設定は、私の画面で直す）
・公開サイトのHTMLに、入力内容を録画する計測（Clarity・Hotjar など）が入っていないか調べる。入っていれば、このページだけ除外する方法を相談する
・スマホ実機（iPhoneのSafari）は私が見る。CCは確認できない

■ 作業3：プライバシーポリシーに新しい節を足す（公開済みのページ・慎重に）
・**公開済みのページなので、全文差し替えはしない。**`GET /wp-json/wp/v2/pages?slug=privacy-policy&status=any&context=edit` で今のWPの本文を取り、`pages/privacy-policy.md` と突き合わせる。**差分があればWPが正**（MDを先にWPに合わせる）。差分は私に報告する
・足すのは、MDの新しい節だけ：「## 広告について」の前に、見出し1＋段落3＋区切り線1（計5ブロック）。ブロックの形は、WPにある隣の見出し・段落・区切り線とまったく同じにする（クラスもコピーする）
・書き込む前に、**追加する5ブロックの全文を私に見せて、OKをもらう**（本番に反映される）。反映は、**固定ページ x-post-checker を私が公開したあと**にする（先に出すと、存在しないツールの説明になる）
・反映後に数える：追加した5ブロックだけが増え、ほかのブロック（`is-style-` の出現数など）が変わっていないこと。公開ページで節が出ていること
・最終更新日：WPの末尾の「最終更新日」の行を、**反映した日**に直し、MDの`last_updated`と末尾の行も同じ日に合わせる

■ 作業4：公開後に（私が公開ボタンを押したら）
・`tools/post-mae-check/README.md` の「他の人が使えるか」の「⏳ 未公開」を、公開した日つきの記録に直す
・`operations/seo-index-checklist.md` と `~/Documents/GitHub/tasks/README.md` に、GSCのインデックス登録リクエストと確認の行を足す。GSCのリクエストは私に案内する
・WPを正として、`pages/x-post-checker.md` をWPと同期する（私がWPで直した所があれば）

■ 守ること
・公開ボタンは押さない。下書き保存まではCCが行い、`isEditedPostDirty()` が false であることを確認してから報告する
・ブラウザは**Chrome（claude-in-chrome）**を使う。アプリ内ブラウザはログインしていないので使わない
・「できた」と報告するときは、**数えた値と実測**を書く。未確認のことは未確認と書く（固定ページの`<script>`が残るか・SSPの欄があるか・SWELLの設定・アイキャッチの表示は、固定ページでは前例が無い）
・件数を書いたら全件を示す。修正の報告は「変更前」「変更後」をコードブロックで並べる（差分記号は使わない）
```

## 補足（このファイルを読むCC向け）

- クラウドのセッションでは、`pages/privacy-policy.md`（MD）・`pages/x-post-checker.md`・アイキャッチ・`compose-page.py` までを済ませた。**WordPressには一切触れていない**（本番サイトへの通信が遮断されている）
- 保存名は仮：ユーザーが「記事制作で普段のルールがあるので確認して」と指示した。ルールは`knowledge/eyecatch-rules.md`の「`eyecatch_XXXX.png`（記事のfrontmatter`no`と完全一致・4桁ゼロ埋め）」。**固定ページには`no`が無く、`no`は公開順の記事番号**（`operations/article-md-workflow.md`）。no.73は既に記事（`articles/no73_composition.md`）に使われているので、このページに`eyecatch_0073.png`を付けると上書き事故になる。`images/pages/service-banner.png`の前例に合わせた。**ルールへの追記はユーザーの了承待ち**
