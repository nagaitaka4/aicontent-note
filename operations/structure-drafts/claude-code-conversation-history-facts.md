# 材料シート：Claude Codeの会話履歴は消えるか（TOP10 #9・D-46）

作成：2026-10-19 07時台（定期リサーチ・月曜のフル版②。記録はCCが`~/.claude/projects/`を数えた実物、公式は英語の原文を取得）
> **執筆側はこのシートの事実だけを使う。ここに無い数字・仕様は書かない。**足りない数字は「未計測」と書き、推測で埋めない。
> シートの更新：定期リサーチ（月・金）が公式の変更を見つけたら「3. 公式の一次情報」に追記する。X編集部が同じ題材の下書き・投稿を作ったら「4. X編集部の在庫」に追記する。

## 1. 記事の芯

**「Claude Codeの会話の記録は、何もしなければ30日で消える。ただしデスクトップアプリで始めた会話は残る」を、自分のPCの記録を3回数えた実物で示す。**
読者が決めたいこと：昔の会話を後から開けるか／消えないようにするには何をするか。

## 2. この環境の実物（CCが数えた・件数はファイルの数）

| 日付 | 記録の本数（`~/.claude/projects/*/*.jsonl`） | 一番古い記録 | 出どころ |
|---|---|---|---|
| 2026-08-28 | 171本 | ちょうど30日前（7/29） | `knowledge/x/queue.md` `KEEP-01`・`operations/article-backlog.md` D-46 |
| 2026-10-05 | 247本 | 8/30 | `operations/article-backlog.md` D-46 |
| **2026-10-19** | **356本** | **8/30（50日前）**。8/31が3本・9/1が3本・9/2が4本と続く | 本日 `find ~/.claude/projects -maxdepth 2 -name "*.jsonl"`（日付はファイルの更新日） |

- **8/28の時点では30日より古い記録が無かった → 10/19は50日前の記録が残っている。**8/28の修正（デスクトップアプリで作った会話は年齢に関係なく残す）のあと、消えなくなった
- このプロジェクト（aicontent-note）の分だけで168本（10/19）
- **起動元で分けた（10/19・各記録の`entrypoint`欄）**：デスクトップアプリ（`claude-desktop`）326本／SDK経由（`sdk-cli`＝定期実行や別エージェントなど）23本／記載なし8本（計357本・数えている間にこのセッションの分が1本増えた）
- **30日より古い記録（更新日が9/18以前）は31本＝デスクトップアプリ30本・記載なし1本。SDK経由の23本には30日より古いものが1本も無い**＝公式の「デスクトップアプリの会話は年齢に関係なく残す・それ以外は30日」と合っている
- 設定：`~/.claude/settings.json`に`cleanupPeriodDays`の指定は無い（＝既定のまま）
- ⚠️ 日付はファイルの更新日。会話を始めた日ではない（続きから再開すると新しくなる）

## 3. 公式の一次情報（[Explore the .claude directory](https://code.claude.com/docs/en/claude-directory)・2026-10-19取得・英語原文）

- verbatim：`Claude Code deletes the files in the paths below once they're older than cleanupPeriodDays, as long as it can safely determine the retention period. The default is 30 days and the minimum is 1; setting 0 fails with a validation error.`
- verbatim：`Claude Desktop and Cowork transcripts: Claude Code keeps the transcript of a session you started or most recently continued in Claude Desktop or Cowork at any age.`
- verbatim：`To give these transcripts an age limit, set desktopSessionCleanupPeriodDays.`
- 再開の方法（`claude --continue`／`--resume`／`/resume`）は`claude-code-session-handoff-facts.md` 3節（[Manage sessions](https://code.claude.com/docs/en/sessions)・9/11取得）にある。執筆の直前に取り直す

## 4. X編集部の在庫

- `KEEP-01`「会話記録はPCに30日しか残っていない」（`knowledge/x/queue.md`・★★★★☆・未投稿）。**8/28時点の内容で、今は「デスクトップアプリの分は残る」に変わった。記事が出たらリンク型に組み替える**（公開前に単独で出さない）
- 10/5の@tokkyo宛リプライ案（`operations/article-backlog.md` D-46）

## 5. 既存記事との重なり

- TOP10 #6「翌日も続きから任せられるか」＝**続きから再開できるか**の問い。こちらは**記録が残るか**の問い。再開の手順は#6へリンクで逃がす
- no.25（Claude Code Desktopのセッション管理・機能紹介・GSC 9表示）＝保持期間は扱っていない
- no.30 コンテキストとは（概念）

## 6. 需要

- サジェスト（10/5）：`claude code 履歴`8（**消えた／消える**／保存／削除）・`claude code 会話`10（会話履歴 保存／再開／引き継ぎ）・`claude 履歴`10（消えた／復元）
- GSC（直近3か月・10/19）：履歴の語の表示は0件。隣のClaude系の束＝`claude 担当職種`20表示・`chatgpt work claude code`16表示

## 7. まだ無いもの

- **ターミナル（CLI）で直接始めた会話は、記録の上では見当たらない**（起動元はデスクトップアプリ326・SDK経由23・記載なし8）。本人がターミナルで`claude`を打って使っているかは本人の確認が要る
- **消えて困ったことがあったか**（本人にしか答えられない）。無ければ「困る前に知っておく」の書き方にする
- 消えた記録を戻せるか（復元）は未確認。公式に戻す方法の記載は見つけていない＝執筆の直前に確かめる
