# 材料シート：Claude Codeのメモリ機能（TOP10 #7・D-21）

作成：2026-09-11 18:40（一次情報を直接確認）。**執筆可能：◯（確認事項1件、答えが無くても書ける）**
> **執筆側はこのシートの事実だけを使う。ここに無い数字・仕様は書かない。**足りない数字は「未計測」と書き、推測で埋めない。
> シートの更新：定期リサーチ（月・金）が公式の変更を見つけたら「3. 公式の一次情報」に追記する。X編集部が同じ題材の下書き・投稿を作ったら「4. X編集部の在庫」に追記する。

## 1. 記事の芯

**「86件覚えさせても、同じ指摘を3回受けた。Claude Codeのメモリで効くこと・効かないこと」。**
主役は実物（このリポジトリのメモリ86件・5か月）と、メモリがあっても繰り返した失敗の記録。「覚える」と「守る」は別、を実データで示す。

## 2. この環境の実物（2026-09-11実測）

| 項目 | 値 | 出どころ |
|---|---|---|
| メモリの数 | **86件**（feedback 81・project 5）＋索引`MEMORY.md` | `~/.claude/projects/-Users-nagaitakashi-Documents-GitHub-aicontent-note/memory/` |
| 期間 | 2026-04-13（最古`feedback_calendar.md`）〜2026-09-11 | 同ディレクトリの更新日 |
| 索引の長さ | 86行（公式の読み込み上限は200行または25KB） | `MEMORY.md` |
| 他のリポジトリ | invest-app 21件・ok-made 6件・logo-system 4件 | `~/.claude/projects/*/memory/` |
| メモリがあっても繰り返した失敗 | ①相手の投稿を読まずにリプライ（2026-08-17・同種3回目）②「1つの面だけ見て無いと言う」（2026-08-28と09-02・2回）③主語のない文（2026-09-03・同じ指摘の3回目） | `operations/lessons.md` |
| 繰り返しを止めた手段 | 機械チェック（`operations/x-firstline.py` 2026-09-07・`article-self-check.py`）と「測れるルールはスクリプトが正」（2026-08-05） | `operations/lessons.md`・`rules/x-post-flow.md` |

## 3. 公式の一次情報（[How Claude remembers your project](https://code.claude.com/docs/en/memory)・2026-09-11取得）

- 2つの仕組み：**CLAUDE.md（人が書く指示）**と**auto memory（Claudeが自分で書くメモ）**。どちらも毎セッション読み込まれる
- verbatim：`Claude treats them as context, not enforced configuration.` ／ `To block an action regardless of what Claude decides, use a PreToolUse hook instead.`
- auto memoryの種類：`user`／`feedback`／`project`／`reference`。**コードから分かること・CLAUDE.mdに書いてあることは保存しない**
- 保存場所：`~/.claude/projects/<project>/memory/`（リポジトリ単位・worktree共有・機械ローカル）。`MEMORY.md`が索引、1メモリ1ファイル
- **読み込み**：verbatim `The first 200 lines of MEMORY.md, or the first 25KB, whichever comes first, are loaded at the start of every conversation.` ／ `Claude Code doesn't load topic files such as user_role.md or feedback_testing.md at startup. Claude reads them on demand`
- 既定でオン。`/memory`でオン・オフと閲覧、`autoMemoryEnabled: false`で無効化、`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`
- フロントマターに`modified`（v2.1.214以降）
- CLAUDE.mdに足すタイミング（verbatim）：`Claude makes the same mistake a second time`

## 4. X編集部の在庫（2026-09-11確認）

- `rule-file-気`（7/16・38ビュー）「マイGPTの知識ファイル、更新するのが面倒で」——ChatGPT側の話。直接の重なりなし
- 取材待ちリスト「Git・README・ルールがそろって初めてAIが安定した話」「『主語がわからない』を3回言われて、ようやく機械チェックにした」（9/7追加）——**③の材料と同じ**。記事が出たらX側はリンク型に回す

## 5. 既存記事との重なり

- no.55 ルールファイルとは（概念・59表示・3クリック）／no.61 情報整理が9割／no.30 コンテキストとは。**この記事は「Claudeが自分で書くメモ」の実物に絞る。**CLAUDE.md側の話は#5に回す

## 6. 需要（2026-09-11実測）

`claude code memory`10件（memory.md／コマンド／使い方／off／整理）・`claude code メモリ`10件（使用量／不足／機能／削除。⚠️ 半分はPCのメモリの意味）

## 7. まだ無いもの

- **「効いた」側の実例が記録に無い。**言われなくなったことは記録に残らないため。→ 編集会議で1件だけ聞く（例：「WP入稿はCCが実行する」「アイキャッチは1パターン」など、言い直さなくなったもの）。答えが無ければ「効かなかった3件」を主役にして書ける
- メモリを読んだ回数（「Recalled N memories」）は数えていない → 未計測と書く
