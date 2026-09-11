# 材料シート：CLAUDE.mdとルールファイルの実物（TOP10 #5・D-05）

作成：2026-09-11 18:40（一次情報を直接確認）。**執筆可能：◯（確認事項なし）**
> **執筆側はこのシートの事実だけを使う。ここに無い数字・仕様は書かない。**足りない数字は「未計測」と書き、推測で埋めない。
> シートの更新：定期リサーチ（月・金）が公式の変更を見つけたら「3. 公式の一次情報」に追記する。X編集部が同じ題材の下書き・投稿を作ったら「4. X編集部の在庫」に追記する。

## 1. 記事の芯

**「CLAUDE.mdに書いても守られない。5か月で、ルールを『書く』から『測る』に変えた実物」。**
サジェスト`claude code ルール`の候補に「忘れる」がある。答えは公式にも書いてある（context, not enforced configuration）。このリポジトリは、守られなかったルールをスクリプト・フック・メモリに移してきた。その経緯と現物を見せる。

## 2. この環境の実物（2026-09-11実測）

| 項目 | 値 | 出どころ |
|---|---|---|
| `CLAUDE.md` | **122行**・初コミット2026-03-30・45回改訂 | `git log -- CLAUDE.md` |
| 分割したルール | 1917行（4ファイル。**毎回は読み込まず、作業の直前に読み直す設計**） | 下の表 |
| ルールの肥大化（2026-08-05） | `rules/article-flow.md`が357行・42,726字、「省略禁止」が33行 → いまはCLAUDE.md 3か所・article-flow 3か所 | `operations/lessons.md` 2026-08-05 |
| 測れるルールの移し先 | `operations/constraints.py`（`CONSTRAINTS` 39項目）＋スクリプト6本（article-precheck.py・article-self-check.py・constraints.py・md-to-wp.py・x-count.py・x-firstline.py） | `operations/` |
| フック | 3本（`UserPromptSubmit`で現在日時を差し込む／`PermissionRequest`・`PermissionDenied`で確認を記録・9/11追加） | `~/.claude/settings.json` |
| スキル | 1本（`.claude/commands/eyecatch-ref.md`） | リポジトリ |
| メモリ | 86件（#7のシート） | `~/.claude/projects/.../memory/` |
| 「読み直す」ルールの日付 | 2026-07-16確定（一度読んだ記憶で動かない） | `CLAUDE.md` |

| ファイル | 行数 |
|---|---|
| `rules/article-flow.md` | 311行 |
| `rules/session-handoff.md` | 33行 |
| `rules/task-management.md` | 179行 |
| `rules/x-post-flow.md` | 1394行 |


## 3. 公式の一次情報（[How Claude remembers your project](https://code.claude.com/docs/en/memory)・2026-09-11取得）

- verbatim：`Claude treats them as context, not enforced configuration.` ／ `CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself.`
- **推奨サイズ**：verbatim `target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence.`
- 置き場所：`~/.claude/CLAUDE.md`（個人・全プロジェクト）／`./CLAUDE.md`（プロジェクト）／`./CLAUDE.local.md`（個人・gitignore）／管理ポリシー
- **`.claude/rules/`**：トピック別に分けられる。`paths:`フロントマターで対象ファイルを限定すると、そのファイルを触るときだけ読み込まれる。⚠️ **このリポジトリの`rules/`は`.claude/rules/`ではなく、CLAUDE.mdの索引から人（CC）が読みに行く運用**。違いを記事で明記する
- 足すタイミング（verbatim）：`Claude makes the same mistake a second time` ／ `You type the same correction or clarification into chat that you typed last session`
- 守られないときの対処：`If the instruction is something that must run at a specific point ... write it as a hook instead.` ／ `/context`で読み込みを確認／`/doctor`が不要な記述の削減を提案（v2.1.206以降）
- HTMLコメントは読み込み時に除かれる（人向けのメモに使える）／`@path`で他ファイルを取り込める（最大4段）

## 4. X編集部の在庫（2026-09-11確認）

- `rule-file-気`（7/16・38ビュー）／取材待ちリスト「Git・README・ルールがそろって初めてAIが安定した話」「X素材の供給ルールを数日で2回作り変えた」——記事が出たらリンク型に回す

## 5. 既存記事との重なり

- no.55 ルールファイルとは（概念）／no.62 土台を作る5ステップ／no.38 構成を毎回安定させる運用フロー／no.64 自動化の限界。**この記事はClaude Codeの実物ファイルと「守られない→測る」の経緯に絞る。**概念はno.55へリンク

## 6. 需要（2026-09-11実測）

`claude.md`9件（とは／ベストプラクティス／場所／書き方）・`claude code ルール`10件（設定／ファイル／**忘れる**／追加）・`claude code 指示`5件（の出し方／書／ファイル）／no.55が59表示の隣

## 7. まだ無いもの

- ルールを守った・守らなかった回数の実測は無い（未計測）。代わりに「同じ指摘が3回来た」記録（lessons）と「省略禁止が33→3か所」の前後を使う
