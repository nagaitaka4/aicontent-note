# SEOインデックス登録 設定・対策チェックリスト

最終更新：2026-05-12

---

## 現在の設定状態（正常値）

### SEO SIMPLE PACK（タクソノミーアーカイブ設定）
- カテゴリーアーカイブ → **noindex（インデックスさせない：はい）**
- タグアーカイブ → **noindex（インデックスさせない：はい）**

### XML Sitemap & Google News（タクソノミー設定）
- カテゴリー → **チェックあり（サイトマップに含む）**
- タグ → **チェックなし（除外）**
- フォーマット → **チェックなし（除外）**
- 投稿者 → **そのまま（著者1名のみ・影響軽微）**

### WordPress 表示設定
- 「検索エンジンがサイトをインデックスしないようにする」→ **チェックなし（正常）**

---

## インデックス問題が起きたときの確認順序

1. **WordPress 設定 → 表示設定**
   - 「検索エンジンがサイトをインデックスしないようにする」にチェックが入っていないか確認
   - チェックが入っていたら即外す

2. **robots.txt を確認**
   - `https://aicontent-note.com/robots.txt` を開く
   - `Disallow: /` や意図しないブロックがないか確認

3. **XML Sitemap のタクソノミー設定を確認**
   - タグにチェックが入っていたら外す（タグは除外が正しい）
   - チェックなし＝全部含む になるので注意

4. **SEO SIMPLE PACK のnoindex設定を確認**
   - タグ・カテゴリーが「インデックスさせない：はい」になっているか確認

5. **Search Console でステータス確認**
   - インデックス作成 → ページ → 各カテゴリーの件数を確認
   - 「検出 - インデックス未登録」が多い → サイトマップ再送信 ＋ URLリクエスト
   - 「クロール済み - インデックス未登録」が多い → コンテンツ品質の問題

6. **サイトマップを再送信**
   - Search Console → サイトマップ → `sitemap.xml` を入力して送信

7. **インデックス登録リクエスト（URL検査）**
   - 主力記事から1日5件ずつリクエスト

---

## インデックス登録リクエスト URL一覧（2026-05-11 実施）

| 優先 | URL | ステータス |
|---|---|---|
| 1 | https://aicontent-note.com/ai-content-cost-effectiveness/ | リクエスト済み |
| 2 | https://aicontent-note.com/ai-writing-tool-comparison/ | リクエスト済み |
| 3 | https://aicontent-note.com/claude-code-introduction/ | リクエスト済み |
| 4 | https://aicontent-note.com/claude-code-compatible-jobs/ | リクエスト済み |
| 5 | https://aicontent-note.com/ai-article-quality-check/ | リクエスト済み |
| 6 | https://aicontent-note.com/claude-code-article-structure/ | リクエスト済み |
| 7 | https://aicontent-note.com/claude-code-writing-rewrite/ | リクエスト済み |
| 8 | https://aicontent-note.com/claude-code-entry-publish/ | リクエスト済み |
| 9 | https://aicontent-note.com/ai-writing-claude-setup/ | リクエスト済み |
| 10 | https://aicontent-note.com/swell-seo-settings/ | リクエスト済み |
| 11 | https://aicontent-note.com/ai-webwriting-verification-02/ | リクエスト済み |
| 12 | https://aicontent-note.com/ai-webwriting-verification-03/ | リクエスト済み |
| 13 | https://aicontent-note.com/ai-webwriting-verification-05/ | リクエスト済み |
| 14 | https://aicontent-note.com/ai-webwriting-verification-06/ | リクエスト済み |
| 15 | https://aicontent-note.com/ai-webwriting-verification-07/ | リクエスト済み |
| 16 | https://aicontent-note.com/service/ | リクエスト済み |
| 17 | https://aicontent-note.com/contact/ | リクエスト済み |
| 18 | https://aicontent-note.com/privacy-policy/ | リクエスト済み |
| - | https://aicontent-note.com/claude-code-limitations/ | Googleが発見次第 |
| - | https://aicontent-note.com/blog-update-outsource-timing/ | Googleが発見次第 |

---

## 今回の問題の根本原因（2026-05-11 判明）

XML Sitemap プラグインのタクソノミー設定で「チェックなし＝全部含む」という仕様により、タグページ45件がサイトマップに含まれていた。Googleがタグページへのクロールにリソースを消費し、記事ページへのインデックスが後回しになっていた。

**再発防止：** 新しいタグを大量に追加したときはXML Sitemapの設定を見直す。

---

## 参考：Search Console の状態の見方

| ステータス | 意味 | 対処 |
|---|---|---|
| 検出 - インデックス未登録 | URLは知っているが未訪問 | URLリクエスト・サイトマップ再送信 |
| クロール済み - インデックス未登録 | 訪問したが品質判断で保留 | コンテンツ改善・URLリクエスト |
| インデックス済み | 正常 | 何もしない |
| noindexタグによって除外 | noindex設定あり | 意図的かどうか確認 |
| 見つかりませんでした（404） | ページが存在しない | 削除済みなら放置でOK |
