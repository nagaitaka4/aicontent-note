# 材料シート：Claude Codeの定期実行（待機列14・D-15）

作成：2026-09-11 18:40（一次情報を直接確認）。**執筆可能：◯（確認事項なし。ただし7の弱点を本文で正直に書く）**
> **執筆側はこのシートの事実だけを使う。ここに無い数字・仕様は書かない。**足りない数字は「未計測」と書き、推測で埋めない。
> シートの更新：定期リサーチ（月・金）が公式の変更を見つけたら「3. 公式の一次情報」に追記する。X編集部が同じ題材の下書き・投稿を作ったら「4. X編集部の在庫」に追記する。

## 1. 記事の芯

**「Claude Codeに毎朝と週2回のリサーチを2か月任せた。51回の実行で残ったものと、残らなかったもの」。**
主役は実行の記録（回数・稼働条件・見落とし）と、成果の正直な数字（6週間で記事になったのは1本）。「自動で回る」と「役に立つ」は別、を実データで示す。

## 2. この環境の実物（2026-09-11実測）

| 項目 | 値 | 出どころ |
|---|---|---|
| 定期実行の数 | **6本**：`ai-trends-daily`（毎日8:00）／`marketing-research-mon-fri`（月・金12:00）／`biweekly-gsc-x-checkup`（木曜）／`invest-app-session-report`／`invest-app-ai-decision-2026-09-11`／`x-post-cats-20260826`（1回きり） | `~/.claude/scheduled-tasks/` |
| 開始 | 2026-07-06 | `git log --grep=自動実行` |
| 自動実行のコミット | **51回**（2026-07月7回・2026-08月29回・2026-09月15回） | 同上 |
| 中身 | 4領域のリサーチ（Claude Code／競合ツール／SEO・GEO／市場・補助金）→ `research/`に追記 → Xネタ・記事ネタを振り分け | `~/.claude/scheduled-tasks/marketing-research-mon-fri/SKILL.md` |
| 成果（正直な数字） | 8/1以降、リサーチ由来で記事になったのは**no.65の1本**（M-17）。M-16・M-18は落選。Xの下書きへの投入は**9月0本**（キューが37本で満杯のため） | `operations/article-backlog.md`・`knowledge/x/queue.md` |
| 見落としと直し | デイリーが開けなかった面（@ClaudeDevs・OpenAIニュース）をフル版が実Chromeで拾い直す運用／9/5〜9/7のデイリーがキュー在庫を「37本・★17」と誤記→スクリプトで数え直し | `research/trends.md`・`tasks/README.md` 9/7 |
| 記録 | `operations/automation-log.md`（Phase 1〜4の経緯・運用ログ） | リポジトリ |

## 3. 公式の一次情報（[Schedule recurring tasks in Claude Code Desktop](https://code.claude.com/docs/en/desktop-scheduled-tasks)・2026-09-11取得）

- 3種類：**Cloud（Routines・機械が止まっていても動く・最小1時間）／Desktop（自分の機械・アプリが開いていて起きているときだけ・最小1分）／`/loop`（セッション内）**
- verbatim：`Tasks only run while the desktop app is running and your computer is awake. If your computer sleeps through a scheduled time, the run is skipped.` ／ `Desktop checks whether each task missed any runs in the last seven days. If it did, Desktop starts exactly one catch-up run for the most recently missed time`
- 許可：タスクごとに許可モードを持つ。`~/.claude/settings.json`のallowも効く。Manualで止まると承認まで待つ。「Run now」で先に「always allow」を付けておく
- 保存場所：`~/.claude/scheduled-tasks/<task-name>/SKILL.md`（frontmatterに`name`・`description`、本文がプロンプト）。スケジュール・フォルダ・モデルはファイルには無い
- 実行は数分ずらされる（`a small delay of a few minutes ... deterministic`）／worktreeで隔離するトグルあり／Desktop 1.1.5368より前は使えない
- 会話から作れる（「毎朝9時にコードレビュー」）。`update_scheduled_task`で自分の予定を変えられる

## 4. X編集部の在庫（2026-09-11確認）

- 該当する投稿なし。定期実行そのものはXで扱っていない

## 5. 既存記事との重なり

- no.64 ブログ運用はどこまで自動化できたか（判断論）／no.38 構成の運用フロー。**この記事は「定期実行の実物と2か月の成績」に絞る**

## 6. 需要（2026-09-11実測）

`claude code cron`10件（実行／job／jobs／tool）・`claude code スケジュール`4件（実行／管理／タスク／機能）・`claude code 定期実行`2件

## 7. まだ無いもの（本文で正直に書く）

- **スキップされた回数は未集計。**アプリのタスク詳細ページ（Review history）で数えられるが、まだ見ていない → 執筆前に1回数える
- 「役に立った」の実数が薄い（記事1本・X投入0）。**記事の芯はここ**なので、成果を盛らない
