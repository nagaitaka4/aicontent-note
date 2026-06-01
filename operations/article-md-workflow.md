# 記事MDファイル作成ワークフロー

## 概要

公開済み記事をMarkdownファイルとしてリポジトリに保存するための手順。
このファイルに基づいてClaudeが記事MDファイルを作成する。

---

## 保存先

```
articles/
```

---

## ファイル命名規則

- 記事のURLスラッグをそのまま使用する
- 例：`https://aicontent-note.com/ai-content-cost-effectiveness/` → `ai-content-cost-effectiveness.md`

---

## フロントマター構造

```
---
no: [メディア全体での記事番号（公開順）]
series: [シリーズ名。なければ省略]
series_no: [シリーズ内の番号。なければ省略]
title: [記事タイトル]
date: [公開日 YYYY-MM-DD形式]
url: [記事URL]
slug: [URLスラッグ（url末尾のパス部分）]
status: [published / draft]
meta_description: [検索結果に表示されるディスクリプション（120〜140文字、メインキーワード含む）]
eyecatch_alt: [アイキャッチ画像の代替テキスト（画像の内容を説明、キーワードを含む）]
category: [カテゴリー名（日本語）]
tags: [タグ1, タグ2, タグ3]
eyecatch: [eyecatch_XXXX.png]
---
```

### カテゴリー一覧

| カテゴリー名 | スラッグ | 対象記事 |
|---|---|---|
| AIとコンテンツの実務 | `ai-content-practice` | AIツール・実務ノウハウ系 |
| AIコンテンツ運用検証 | `ai-content-verification` | 副業検証シリーズ・検証記事 |
| 継続できる運用設計 | `sustainable-operation` | 運用の仕組み・継続方法系 |
| 費用対効果と現実 | `cost-effectiveness` | コスト・費用対効果系 |

### タグについて
- タグ名（日本語）で記述する
- WordPress投稿時にそのまま使用する
- スラッグはWordPress側で自動生成される（手動設定も可）

### シリーズ一覧

| series値 | 内容 | 設計方針 |
|---|---|---|
| side-business | 副業検証シリーズ | 実況型（計画型ではない） |

※ 新シリーズが追加されたらこの表に追記する。
※ side-businessシリーズは「実況型」で設計。計画の変更・失敗・方針修正もそのまま記録する。

---

## 本文構造

- H1 → `#`
- H2 → `##`
- H3 → `###`
- 記事本文のみ。サイドバー・ナビ・フッターは含めない。

---

## WordPressへの投稿手順

VSCodeのMarkdownファイルをそのままWordPressに貼り付けても見出しや改行が反映されない。以下の手順でコピーする。

```
① VSCodeでmdファイルを開く
② 右上のプレビューアイコンをクリック（または Cmd + Shift + V）
③ プレビュー画面で Cmd + A → Cmd + C
④ WordPressの新規投稿画面にペースト
```

プレビュー画面はMarkdownをHTMLとして表示しているため、H1/H2/H3・改行がそのまま反映される。プラグイン不要。

---

## WordPress入稿時の追加作業

貼り付け後、以下を必ず行う。

### メタディスクリプションの入力
編集画面を下にスクロール →「SEO SIMPLE PACK設定」→「このページのディスクリプション」に入力する。
MDファイルの `meta_description` の内容をそのままコピーして貼り付ける。

- タイトルタグ：空欄でOK（記事タイトルが自動で使われる）
- og:image：空欄でOK（アイキャッチ画像が自動で使われる）

### アイキャッチ画像のalt属性入力
アイキャッチ画像をメディアライブラリから選択する際、「代替テキスト」欄に入力する。
MDファイルの `eyecatch_alt` の内容をそのままコピーして貼り付ける。

### フロントマターへの追記ルール
記事MDファイルには以下を必ず記載する。

| フィールド | 内容 |
|---|---|
| `meta_description` | 検索結果に表示されるディスクリプション（120〜140文字） |
| `eyecatch_alt` | アイキャッチ画像の代替テキスト（キーワードを含む説明） |

---

## 作成手順

1. ユーザーから記事URLを受け取る
2. URLから記事全文・公開日を取得する
3. メディア全体の記事番号（`no`）を確認する（直前に作成したファイルの `no` + 1）
4. シリーズに該当する場合は `series` と `series_no` を付与する
5. フロントマターを作成する
6. 本文をMarkdown形式に変換する（H1/H2/H3構造を維持）
7. `articles/` 配下にファイルを保存する

---

## 記事公開時のチェックリスト

記事を公開したら、以下を必ず実行する。

1. **MDファイルのフロントマター更新**：`status: draft` → `status: published`
2. **作成済み記事一覧に追記**：下のテーブルに追加
3. **GitHub issue #2（記事テーマ設計）を更新**：
   - 該当記事のチェックボックスを `[ ]` → `[x]` にする
   - タイトルを正式タイトルに更新する
   - 次の記事に「← **次回確定**」マークをつける
   - 概要の公開済み本数を更新する

---

## 作成済み記事一覧

※ このテーブルは「公開した事実」の記録。未公開・予定は記載しない。

| no | series | series_no | ファイル名 | 公開日 |
|---|---|---|---|---|
| 1 | - | - | ai-content-cost-effectiveness.md | 2026-02-06 |
| 2 | side-business | 1 | ai-webwriting-verification-01.md | 2026-02-17 |
| 3 | side-business | 2 | ai-webwriting-verification-02.md | 2026-03-02 |
| 4 | side-business | 3 | ai-webwriting-verification-03.md | 2026-03-16 |
| 5 | - | - | ai-writing-claude-setup.md | 2026-03-17 |
| 6 | side-business | 4 | ai-webwriting-verification-04.md | 2026-03-22 |
| 7 | - | - | content-operation-system.md | 2026-04-02 |
| 8 | side-business | 5 | ai-webwriting-verification-05.md | 2026-04-03 |
| 9 | - | - | claude-code-introduction.md | 2026-04-07 |
| 10 | - | - | swell-seo-settings.md | 2026-04-09 |
| 11 | - | - | ai-writing-tool-comparison.md | 2026-04-15 |
| 12 | side-business | 6 | ai-webwriting-verification-06.md | 2026-04-16 |
| 13 | - | - | ai-article-quality-check.md | 2026-04-22 |
| 14 | cc-writer | 1 | claude-code-compatible-jobs.md | 2026-04-23 |
| 15 | side-business | 7 | ai-webwriting-verification-07.md | 2026-04-24 |
| 16 | cc-writer | 2 | claude-code-article-structure.md | 2026-04-27 |
| 17 | cc-writer | 3 | claude-code-writing-rewrite.md | 2026-04-27 |
| 18 | cc-writer | 4 | claude-code-entry-publish.md | 2026-04-28 |
| 19 | cc-writer | 5 | claude-code-limitations.md | 2026-05-04 |
| 20 | - | - | blog-update-outsource-timing.md | 2026-05-07 |
| 21 | - | - | claude-code-glossary-beginners.md | 2026-05-11 |
| 22 | - | - | claude-code-rate-limit-update.md | 2026-05-13 |
| 23 | - | - | ai-content-operation-results-timeline.md | 2026-05-14 |
| 24 | - | - | blog-not-needed-message.md | 2026-05-18 |
| 25 | - | - | claude-code-desktop-renewal.md | 2026-05-23 |
| 26 | - | - | content-operation-outsource-what-is.md | 2026-05-27 |
| 27 | - | - | claude-subscription-change-june-2026.md | 2026-05-28 |
| 28 | ai-ops-basics | 1 | prompt-design-basics.md | 2026-05-29 |
| 29 | - | - | claude-opus-4-8-honesty.md | 2026-06-01 |
