# 材料シート：GPT-6 AstraがChatGPT Plusでも使える。ChatGPTとClaude、両方課金の分担はこう変わる（TOP10 #7・T-4・no.11「ai-writing-tool-comparison」の全面改稿・URL維持）

作成：2026-09-14 15:05（編集会議C-5の回答から）。**執筆可能：△（Astraを使った実測が無い。7節①の実験が先）**
> **執筆側はこのシートの事実だけを使う。**「Astraで分担が変わった」は、使って比べるまで書かない。

## 1. 記事の芯（2026-09-14・C-5の回答）

**ChatGPT PlusとClaude Maxの両方に課金している人の、いまの分担。**画像生成はGPT一択。記事制作はClaude Codeで、レビューはGPT。企画・設計・方向性の相談はGPTのほうが向いている（本人の実感）。普段のチャットはGPT。画面を開いている比率は**1日でClaude Code 9割・GPT 1割**（本人の体感・計測なし）。**サイト制作はGPTとClaude Codeのどちらがいいか、まだ結論が出ていない。**

ユーザーの回答（2026-09-14 15:03・そのまま使ってよい体験）：
- 「画像生成はGPT一択、記事制作はCCでやって、レビューをGPT、という使い方が基本」
- 「企画や設計、方向性の相談はGPTのほうが向いている気がしている」
- 「普段のチャット使いはGPT」
- 「サイト制作はGPTのほうがいいのか、CCのほうがいいのか、まだ結論が出ていない」
- 「Astraは使ったことがない」
- 「何をするかにもよるが、1日の割合で言うと、CCを9割、GPTは1割くらいの比率で画面を開いている」

**⚠️ 題との食い違い**：題は「Astraで分担はこう変わる」だが、**Astraは未使用**。①Astraを使って比べる（7節①の実験）か、②題を「両方課金の分担はこうなっている。Astraで何が変わるかは試してから」に置き直すか、構成案で決める。**CCの推奨は①（実験してから書く）**。

## 2. この環境の実物

| 項目 | 実物 | 使い方 |
|---|---|---|
| 分担の表 | 画像＝GPT／記事の構成・執筆・入稿・チェック＝Claude Code（**2026-09-14：「今は全部CC」。入稿はどちらにしてもCC——安定しているのでGPTでやる必要がない**）／レビュー＝GPT／企画・設計・方向性の相談＝GPT／普段のチャット＝GPT／サイト制作＝未決 | 記事の骨組み |
| 開いている比率 | Claude Code 9：GPT 1（本人の体感。計測なし） | 数字として書くなら「体感」と明記 |
| 記事制作の分担の実験 | V-04（2026-08-13・no.57）：構成をClaude Code、執筆をGPT Workに渡した実測（`operations/article-backlog.md` V-04） | Astra再実験の比較対象（同じ設計で再現できる） |
| レビューをGPTに | `operations/gpt-workflow-review-prompt.md`（2026-08-17・工程の見直し）／no.66の「人の指摘」はGPTレビューだった（2026-09-14判明・X `DW66-リ`保留） | 「レビューはGPT」の実物 |
| 画像はGPT | アイキャッチ69枚（`images/`・`knowledge/eyecatch-rules.md`・`eyecatch-ref`スキル） | 「画像はGPT一択」の実物 |
| 契約 | ChatGPT Plus（X `Plus3-気` 8/21）＋Claude Max 5x $110（#5の材料シート） | 「両方課金」の実物 |
| モデルの乗り換え | X `R10-02`（新しいモデルが出るたび乗り換えている）・`SL-気`（開発Fable／記事Opus） | 使い分けの変遷 |

**⚠️ 無いもの**：Astraの実測（未使用）。9:1の計測。サイト制作のGPT vs Claude Codeの比較（未決＝実験候補）。

## 3. 公式の一次情報

| # | 確かめること | 取れたもの | 状態 |
|---|---|---|---|
| 3-1 | AstraがPlusのWork・Codexで使える（`research/ai-tools.md` 2026-09-11に記録・**執筆前に原文を開き直す**） | OpenAI 9/9「GPT-6 Astra: The next generation in intelligence for work」verbatim：`Last week we introduced GPT‑6 Astra, the world's most intelligent and aligned model, now available in ChatGPT Work, Codex, and the API.`／ヘルプ「Managing usage with GPT-6 Astra in Work and Codex」verbatim：`Plus includes Astra in Work and Codex, but not GPT-6 Pro in Chat.`／⚠️ ChatGPTのリリースノートは9/3付「not yet generally available」のまま（面によって記載が違う） | ◯（記録済み） |
| 3-2 | ChatGPT Plusの料金（日本）・Workの公式定義 | 未取得（no.56の材料と重なる。原文で） | 未 |
| 3-3 | Claude Max 5xの料金 | #5の材料シート（$110税込・月払い・画面） | ◯ |

## 4. X編集部の在庫（2026-09-14）

- `ASTRA-気`（9/14投稿・`knowledge/x/queue.md`）／`R10-02`（新しいモデルが出るたび乗り換え）／`CW-02`（ChatGPT WorkとClaude Codeを比べた）／`SL-気`（8/12）／`Plus3-気`（8/21・353ビュー）／`DW66-リ`（保留：no.66の答え合わせはGPTレビュー）

## 5. 既存記事との重なり

- **no.11（この記事の改稿・URL維持）**：`ai-writing-tool-comparison`「AIライティングツール比較｜ChatGPTとClaudeを両方使って気づいたこと」（4月・18表示・8.1位・0クリック）
- **no.56**（`chatgpt-work-claude-code-comparison`・26クリック・6.7位）は「どっちを選ぶか」に答える記事。**この記事は「両方持っている人の分担」に絞る**（同じ読者の問いに2本で答えない）。no.59（ChatGPTの無料と有料）はリンクで逃がす

## 6. 需要

`gpt-6 astra`10・`claude 使い分け`10（chatgpt claude 使い分け／codex claude 使い分け）・`chatgpt plus work`10（制限／上限／違い）・`claude opus sonnet`10（違い／使い分け）／GSC：`chatgpt work claude code`10表示・3.5位（no.56）

## 7. まだ無いもの（執筆で埋めない）

1. **Astraの実測**：**実験は承認済み（9/14 15:09・次に着手する記事で実施）**。設計＝Claude Codeの構成案を、GPT Work（Astra）とClaude Codeの両方に執筆させ、`article-self-check.py`のNG件数・修正回数・所要時間を並べる（8/13のV-04も参照）。入稿はCC・レビューはGPT。**Workの操作は本人**。結果はこの2節へ
2. サイト制作のGPT vs Claude Code（未決）：別の実験候補（OK MADEの自社サイト工程・待機17と接続）
3. 9:1の計測（体感のまま書くなら「体感」と明記）
4. 3-2の一次情報
