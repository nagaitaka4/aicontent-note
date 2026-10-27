---
no: 77
series:
series_no:
title: Claude CodeにWordPress入稿は任せられる？失敗と対策
url: https://aicontent-note.com/claude-code-wordpress-posting/
slug: claude-code-wordpress-posting
status: draft
date:
description: Claude CodeにWordPressの入稿は、下書き保存までなら任せられます。20本近くを任せて、いちばん危なかったのは人がWordPressで直した所を送り直しで消すことでした。起きた失敗を種類ごとに並べ、任せるときの3つの確認をまとめます。
eyecatch: eyecatch_0077.png
eyecatch_alt: Claude CodeにWordPress入稿は任せられる？と書いた題の横に、ブログの編集画面を開いたノートPCと、オレンジのペンで直した跡のある紙と鉛筆を描いたアイキャッチ画像
category: Claude Code活用
tags: Claude Code,WordPress,入稿,Claude in Chrome,自動化
---

# Claude CodeにWordPress入稿は任せられる？失敗と対策

==Claude CodeにWordPressの入稿は、下書き保存まで任せられます。==
20本近くを任せて、いちばん危なかったのは、人がWordPressで直した所を送り直しで消すことでした。
今は、公開ボタンを人に残し、送る前にWordPressの今の本文と比べてもらっています。

---

## Claude CodeにWordPress入稿は、下書き保存まで任せられる

==本文から画像、説明文まで、Claude Codeが下書きに入れます。==
公開ボタンも押せますが、私は人に残しています。
太字やマーカーなど、見た目の仕上げも人がしています。

| やること | 誰が |
|---|---|
| **本文**を入れる（SWELLの装飾ブロック・表・区切り線も） | Claude Code |
| **題・スラッグ・カテゴリー・タグ** | Claude Code |
| **アイキャッチと本文の画像**のアップロード、**検索向けの説明文** | Claude Code |
| **ログイン** | 人 |
| **太字・マーカー・表の幅**などの仕上げ | 人（下書きの画面で） |
| ==**公開ボタン**== | ==人== |

記事づくりの中で、いちばん手間が減ったのが入稿でした。

### 私が使っている環境

・**Claude Code**：デスクトップアプリで使う<br>
・**Claude in Chrome**：いつものChromeを、Claude Codeが操作できるようにする拡張機能。[有料プラン（Pro・Max・Team・Enterprise）で使える](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome)<br>
・**変換スクリプト**：Markdownの原稿を、SWELLの装飾ブロックに変える自作のもの。SWELLは私が使っているWordPressのテーマ

Claude Codeは、ログインしたままのChromeを拡張ごしに操作して入れます。
ログイン画面やCAPTCHAに当たると、[止まって人に頼みます](https://code.claude.com/docs/en/chrome)。
公式の言葉では「it pauses and asks you to handle it manually」です。

【アラート】<br>
**公式がいちばんのリスクとするのは、ページに隠された指示です。**<br>
そのため、大事なアカウントの無い[別のブラウザプロファイル](https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely)を勧めています。

---

## Claude CodeにWordPress入稿を任せて起きた失敗

==特に気をつけたいのは、人が下書きの画面で直した所の上書きです。==
起きた失敗は、大きく4種類でした。

| 失敗の種類 | 実際に起きたこと | 今の止め方 |
|---|---|---|
| ==**人の直しを消す**== | 下書きで直した6か所を、本文の送り直しで**2回消した**。気づいたのは私で、リビジョンから戻せた | 送る前に**WordPressの今の本文を読み**、原稿と比べる。違う所があれば送らずに聞く |
| **見た目が崩れる** | リンクの中で改行され、記事タイトルが途中で切れた。コード欄や番号付きの手順が、改行の無い1段落になった | **変換のしかたを直す**。公開したら実物の画面を開く |
| **確認漏れ** | コメント欄を閉じ忘れた。試しに入れた文字が、抜粋に残ったまま公開された | **手順に入れて**毎回確かめる |
| **送る・保存で壊れる** | 本文が1回で送りきれず、分けて送ると文字が化けた。送った直後の保存で、古い自動保存の本文に戻った。Claude Codeの安全チェックが送り方を止めたこともある | 保存したあとに、**WordPressの本文が送ったものと同じか**確かめる。止まったら人に返す |

人の直しを消すのは、Claude Codeが手元の原稿を正しいものとして送るからです。
人が下書きの画面で直した所は、手元の原稿には入っていません。

---

## Claude CodeにWordPress入稿を任せるときの3つの確認

【チェック】<br>
**公開ボタンは人が押す**<br>
**送る前にWordPressの今の本文と比べ、保存したあとにも確かめてもらう**<br>
**公開したら、実物の画面を開く**

公開すると、誰でも読める状態になります。
だから最後は、自分で画面を確かめてから押しています。

Claudeが代わりに公開した記事でも、責任は使う人が負います。
[公式](https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely)にも「You remain responsible for all browser actions」とあります。

---

＼　ブログ更新が止まっている・記事運用を任せたい方へ　／
企画から執筆・公開まで、まるごとお任せください。お気軽にご相談を。

[お問い合わせフォームはこちら](https://aicontent-note.com/contact/)

---

**関連記事**
・[ブログ運用はどこまで自動化できたか。人に残った2つの判断](https://aicontent-note.com/blog-operation-automation-limit/)<br>
・[入稿・整形・公開はどこまで効率化できるか【Claude Code実践】](https://aicontent-note.com/claude-code-entry-publish/)<br>
・[Claudeに会社の情報を渡して大丈夫か。データが学習に使われる条件](https://aicontent-note.com/claude-company-data-training/)
