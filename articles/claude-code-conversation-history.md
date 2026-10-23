---
no: 76
series:
series_no:
title: Claude Codeの会話履歴は消える？残る期間と残す設定
url: https://aicontent-note.com/claude-code-conversation-history/
slug: claude-code-conversation-history
status: draft
date: 2026-10-22
description: Claude Codeの会話履歴は、ターミナルなどで使った会話なら、最後に使ってから30日を超えると知らせなしに自動で消えます。最後にデスクトップアプリで使った会話は、今は期限なしで残ります。消えた会話を戻す方法は公式に書かれていないため、長く残す設定と注意点をまとめました。
eyecatch: eyecatch_0076.png
eyecatch_alt: Claude Codeの会話履歴は消える？と書いた題の横に、四角い置き時計、上のほうが紙片になって消えていく書類の山、30と書いた卓上カレンダーを描いたアイキャッチ画像
category: Claude Code活用
tags: Claude Code,設定,プライバシー設定
---

# Claude Codeの会話履歴は消える？残る期間と残す設定

==Claude Codeの会話履歴は、ターミナルなら30日使わないと消えます。==
最後にデスクトップアプリで使った会話は、今は何日たっても残ります。
消えた会話を戻す方法は公式に書かれていないので、残したいなら消える前に設定で期間を延ばします。

---

## Claude Codeの会話履歴は、どこで使ったかで残る期間が変わる

[公式の説明](https://code.claude.com/docs/en/claude-directory)と私のPCの記録を並べると、こうなります。

| 使った場所 | 残る期間 | 私のPCでは |
|---|---|---|
| **デスクトップアプリ・Cowork**（そこで始めた・最後にそこで使った会話） | ==何日たっても残る== | 8月末に最後に使った会話も、**50日以上たって残っている** |
| **ターミナル・VS Code**など、デスクトップアプリ以外 | **最後に使ってから30日**（初期設定） | ターミナルから自動で動かしている会話は、**約1か月より前のものが残っていない** |

会社の管理設定で日数が決まっているときは、どこで使った会話もその日数で消えます。
自分の設定では延ばせません。

Claude Codeは起動したあと、裏で古い記録を消します。[知らせは出ません](https://code.claude.com/docs/en/settings-reference#cleanupperioddays)。

---

## 消えた会話は戻せる？

==消えた会話を戻す方法は、公式には書かれていません。==
ただ、一覧に見当たらないだけなら、消えたとは限りません。
まず、その会話を使った場所の一覧で探します。

・**デスクトップアプリ**：アーカイブした会話まで見る<br>
・**ターミナル / VS Code**：それぞれの[一覧](https://code.claude.com/docs/en/sessions)で探す。ターミナルは `claude --resume` のあと Ctrl＋A で、ほかのフォルダの会話も出る<br>
・**PCの中**：[記録のファイル](https://code.claude.com/docs/en/sessions#where-transcripts-are-stored)は ~/.claude/projects に、作業フォルダごとに入っている

8月末の更新より前は、デスクトップアプリの会話も30日で消えていました。
私のPCでは、7月以前に始めた会話の多くが、一覧に題だけ残っています。
開くと「ディスク上にセッションが見つかりません」と表示され、中身は読めませんでした。

---

## 会話履歴を長く残す設定と、残す前に知っておくこと

==デスクトップアプリだけで使うなら、設定は要りません。==
ターミナルやVS Codeの会話は、設定ファイルに1行足すと長く残せます。

### 手順1：設定ファイルのあるフォルダを開く（Mac）

1. Finderを開き、command＋shift＋G を押す
2. 「~/.claude」と入れる
3. 候補に出たフォルダ「.claude」を開く

【ポイント】<br>
**.claude はふだん隠れているフォルダです。**<br>
似た名前の「.claude.json」は別のファイルなので開きません。

### 手順2：settings.json があるとき、1行足す

1. settings.json を右クリックし、「このアプリケーションで開く」からテキストエディットを選ぶ
2. 下の真ん中の行と同じ項目がすでにあれば、数字だけ下と同じに変える
3. 中身が {} だけなら、全部消して下の3行を貼る
4. ほかの設定が書いてあれば、最初の { のすぐ下に下の真ん中の1行を貼り、行の終わりにカンマ（,）を付ける
5. command＋S で保存する

```
{
  "cleanupPeriodDays": 3650
}
```

3650日は約10年で、[公式](https://code.claude.com/docs/en/settings-reference#cleanupperioddays)が長く残す例に挙げている数です。

### 手順2：settings.json が無いとき、新しく作る

1. テキストエディットで新規書類を作る
2. メニューの「フォーマット」→「標準テキストにする」を選ぶ
3. 上の3行をコピーして貼る
4. command＋S を押し、保存の画面で command＋shift＋G を押し、~/.claude と入れる
5. 名前を settings.json にして保存する。拡張子を聞かれたら「“.json”を使用」を選ぶ

【アラート】<br>
**3行は、手で打たずにコピーして貼ります。**<br>
テキストエディットで打つと、" が別の記号に変わることがあります。

### 手順3：設定が入ったか確かめる

・**再起動は要らない**：保存すると、Claude Codeが[その場で読み込みます](https://code.claude.com/docs/en/settings#when-edits-take-effect)<br>
・**読み込まれたか**：Claude Codeの会話の中で `/status` と打つ。「Setting sources」に「User settings」と出ていれば入っている<br>
・**書き間違えたとき**：次に起動したとき「Settings Error」と出る。その画面から直せる

### 大事な会話だけ残すなら /export

ターミナルなら、会話の中で `/export` と打つと、[今の会話を文字のファイルに保存できます](https://code.claude.com/docs/en/sessions#export-and-locate-session-data)。
保存したファイルは自動では消えないので、期限を気にせず残せます。

【アラート】<br>
**会話の記録は[暗号化されていません](https://code.claude.com/docs/en/claude-directory#plaintext-storage)。**<br>
読ませたファイルの内容も、記録に残ります。

---

＼　ブログ更新が止まっている・記事運用を任せたい方へ　／
企画から執筆・公開まで、まるごとお任せください。お気軽にご相談を。

[お問い合わせフォームはこちら](https://aicontent-note.com/contact/)

---

**関連記事**
・[Claudeに会社の情報を渡して大丈夫か。データが学習に使われる条件](https://aicontent-note.com/claude-company-data-training/)<br>
・[非エンジニアがClaude Codeでできること。始め方と詰まった所](https://aicontent-note.com/claude-code-introduction/)<br>
・[Claude Code導入の手順。IT担当がいない会社が決める4つ](https://aicontent-note.com/claude-code-company-introduction-no-it-staff/)
