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
| **デスクトップアプリ・Cowork**（最後にそこで使った会話） | ==何日たっても残る== | 8月末に最後に使った会話も、**50日以上たって残っている** |
| **ターミナル・VS Code**など、デスクトップアプリ以外 | **最後に使ってから30日**（既定） | 平日にコマンドで自動で動かしている会話は、**30日より前のものが1つも残っていない** |

会社の管理設定で日数が決まっているときは、どこで使った会話もその日数で消えます。
自分の設定では延ばせません。
Claude Codeは起動したあと、裏で古い記録を消します。[知らせは出ません](https://code.claude.com/docs/en/settings-reference#cleanupperioddays)。

---

## 消えた会話は戻せる？

まず、その会話を使った場所の一覧で探します。
==そこにも無ければ、戻す方法は公式には書かれていません。==

・**デスクトップアプリ**：アーカイブした会話まで見る<br>
・**ターミナル / VS Code**：それぞれの[一覧](https://code.claude.com/docs/en/sessions)で探す。ターミナルは `claude --resume` のあと Ctrl＋A で、ほかのフォルダの会話も出る

8月末の更新より前は、デスクトップアプリの会話も30日で消えていました。
私のPCでは、7月以前に始めた会話の多くが、一覧に題だけ残っています。
開くと「ディスク上にセッションが見つかりません」と表示され、中身は読めませんでした。

---

## 会話履歴を長く残す設定と、残す前に知っておくこと

==デスクトップアプリだけで使うなら、設定は要りません。==
ターミナルなどの会話は、`cleanupPeriodDays`を大きな数にすると長く残せます。
[公式](https://code.claude.com/docs/en/settings-reference#cleanupperioddays)が挙げる例は3650日（約10年）です。

1. MacのFinderで command＋shift＋G を押し、~/.claude を開く（隠しフォルダ）
2. settings.json があれば、右クリックの「このアプリケーションで開く」からテキストエディットで開く。下の真ん中の行を、最初の { のすぐ下に貼り、行の終わりにカンマを付けて保存する（同じ項目があれば数字だけ書き換える）
3. 無いときは、テキストエディットの新規書類で「フォーマット」→「標準テキストにする」を選ぶ。下の3行をコピーして貼る。保存の画面でも同じキーで ~/.claude を選び、settings.json の名前で保存する。拡張子を聞かれたら「“.json”を使用」を選ぶ

```
{
  "cleanupPeriodDays": 3650
}
```

【アラート】<br>
**会話の記録は[暗号化されていません](https://code.claude.com/docs/en/claude-directory#plaintext-storage)。**<br>
読ませたファイルの内容も、記録に残ります。<br>
長く残すほど、その内容も長く手元に残ります。

---

＼　ブログ更新が止まっている・記事運用を任せたい方へ　／
企画から執筆・公開まで、まるごとお任せください。お気軽にご相談を。

[お問い合わせフォームはこちら](https://aicontent-note.com/contact/)

---

**関連記事**
・[Claudeに会社の情報を渡して大丈夫か。データが学習に使われる条件](https://aicontent-note.com/claude-company-data-training/)<br>
・[非エンジニアがClaude Codeでできること。始め方と詰まった所](https://aicontent-note.com/claude-code-introduction/)<br>
・[Claude Code導入の手順。IT担当がいない会社が決める4つ](https://aicontent-note.com/claude-code-company-introduction-no-it-staff/)
