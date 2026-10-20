# 材料シート：Claude Codeの会話履歴は消えるか（TOP10 #1・D-46・no.76）

作成：2026-10-19 07時台（定期リサーチ・月曜のフル版②。記録はCCが`~/.claude/projects/`を数えた実物、公式は英語の原文を取得）
更新：**2026-10-20 17時台（構成案の前に数え直し・4回目の実測。公式5ページを英語の原文で取り直し。デスクトップアプリの一覧と入力履歴を新しく照合）**
> **執筆側はこのシートの事実だけを使う。ここに無い数字・仕様は書かない。**足りない数字は「未計測」と書き、推測で埋めない。
> シートの更新：定期リサーチ（月・金）が公式の変更を見つけたら「3. 公式の一次情報」に追記する。X編集部が同じ題材の下書き・投稿を作ったら「4. X編集部の在庫」に追記する。

## 1. 記事の芯

**「Claude Codeの会話の記録は、デスクトップアプリで始めた（続けた）会話なら何日たっても残る。ターミナルで始めた会話は30日で、知らせなく消える。消えた記録を戻す方法は公式に無いので、残したいなら消える前に設定を変える」を、自分のPCの記録で示す。**
読者が決めたいこと：昔の会話を後から開けるか／消えないようにするには何をするか／消えたら戻せるか。

## 2. この環境の実物（CCが数えた）

### 2-1. 記録の本数（`~/.claude/projects/*/*.jsonl`・件数はファイルの数）

| 日付 | 記録の本数 | 一番古い記録 | 出どころ |
|---|---|---|---|
| 2026-08-28 | 171本 | ちょうど30日前（7/29） | `knowledge/x/queue.md` `KEEP-01`・`research/trends.md` 8/28 |
| 2026-10-05 | 247本 | 8/30 | `operations/article-backlog.md` D-46 |
| 2026-10-19 | 356本 | 8/30（50日前） | 前回の数え直し |
| **2026-10-20** | **397本** | **8/30（51日前）**。8/31が3本・9/1が2本と続く | 本日 `find ~/.claude/projects -maxdepth 2 -name "*.jsonl"`（日付はファイルの更新日） |

- **起動元で分けた（10/20・各記録の先頭200行の`entrypoint`欄）**：デスクトップアプリ（`claude-desktop`）372本／SDK経由（`sdk-cli`＝定期実行や別エージェントなど）25本（10/19は「記載なし8本」があったが、今回の数え方〔先頭200行まで見る〕では0本）
- **30日より古い記録（更新日が9/20以前）は31本＝全部デスクトップアプリ。SDK経由の25本には30日より古いものが1本も無い**＝公式の「デスクトップアプリの会話は年齢に関係なく残す・それ以外は30日」と合っている
- このプロジェクト（aicontent-note）の分だけで173本（10/20）
- 設定：`~/.claude/settings.json`・`settings.local.json`に`cleanupPeriodDays`・`desktopSessionCleanupPeriodDays`の指定は無い（＝既定のまま。**本人は延ばす設定をしていない**）
- 版：ターミナルの`claude`は2.1.283。デスクトップアプリの中のClaude Codeは2.1.295・2.1.299（`~/Library/Application Support/Claude/claude-code/`のフォルダ名）
- ⚠️ 日付はファイルの更新日。会話を始めた日ではない（続きから再開すると新しくなる）

### 2-2. 🆕 デスクトップアプリの一覧には、中身の消えた会話が並んでいる（10/20 照合）

デスクトップアプリは会話の一覧を自分で持っている（`~/Library/Application Support/Claude/claude-code-sessions/`・1会話1ファイル・**中身は題・作った日・やりとりの回数などだけで、会話の本文は入っていない**）。その`cliSessionId`と`~/.claude/projects/`の記録を突き合わせた。

| 一覧の会話 | 本数 | 中身の記録 |
|---|---|---|
| 全部 | 290本 | — |
| **中身の記録が無い** | **67本** | **全部、最後の作業が7/31以前**。このメディアの作業や経理・タスク管理・定期リサーチの会話で、50往復を超えるものもある。アーカイブしていない（一覧に出ている）ものが大半 |
| 中身の記録がある | 223本 | 8月以降に作った会話は全部ある。7月以前に作った会話でも、後から続けたもの（30本）は残っている |

- **7月以前に作った会話97本のうち67本（7割近く）は、題だけ残って中身が無い**
- **8/28の修正の前は、デスクトップアプリの会話も30日で消えていた**（`research/trends.md` 8/28：v2.1.248のCHANGELOG `Fixed Claude Desktop and Cowork sessions disappearing after 30 days`）。修正の前に消えた分は、修正のあとも戻っていない
- 消えたのは8/28〜8/30ごろまで（8/28に一番古かった7/29〜7/31の記録も今は無い・今の一番古い記録は8/30）。⚠️ 修正がこのPCのデスクトップアプリに届いた日は記録に無い＝本文で日付を断定しない
- ⚠️ **一覧の会話を開いたとき画面に何が出るか（空になるか・エラーか）は未確認**＝本人の画面で確かめる（7節）

### 2-3. 🆕 ターミナルで始めた会話は、全部消えていた（10/20 照合）

`~/.claude/history.jsonl`（ターミナルで打った指示の一覧・公式では`Kept until you delete them`）に25件。会話の記録と突き合わせた。

| 日付 | ターミナルで打ったもの（要約・文面は写さない） | 会話の記録 |
|---|---|---|
| 3/27・3/30 | 入れたときの操作と、フォルダ構成の相談ほか（13件） | 無い |
| 4/6 | 状態の確認（1件） | 無い |
| 4/16 | 前回の続きと、セッションの引き継ぎ方の相談（VS Codeのターミナル・5件） | 無い |
| 5/1 | 別のプロジェクトの作成の依頼（2件） | 無い |
| 8/25・9/28 | ログインなどの操作だけ（4件） | 無い |

- **ターミナル（VS Codeの中のターミナルを含む）で使ったのは3〜5月の初期と、8/25・9/28のログインだけ**。いまの使い方はデスクトップアプリ（本人の使い方＝ClaudeはClaude Code〔デスクトップアプリ・ローカル〕だけ）と合っている
- **打った指示の一覧は残っているが、答えのほうは残っていない**（例：フォルダ構成を相談した指示は残っているが、何と答えたかはもう見られない）。本文で指示の文面を例に出すかは本人に確認する
- 9/28の分（22日前）も記録が無い：`/login`だけの起動で、会話の記録を作らなかったとみられる（推測）＝本文には使わない

## 3. 公式の一次情報（2026-10-20取得・英語原文）

### [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory)（Application data の節）

- verbatim：`Claude Code deletes the files in the paths below once they're older than cleanupPeriodDays, as long as it can safely determine the retention period. The default is 30 days and the minimum is 1; setting 0 fails with a validation error.`
- 消える対象の1行目：`projects/<project>/<session>.jsonl` ＝ `Full conversation transcript: every message, tool call, and tool result`
- verbatim：`Claude Desktop and Cowork transcripts: Claude Code keeps the transcript of a session you started or most recently continued in Claude Desktop or Cowork at any age. To give these transcripts an age limit, set desktopSessionCleanupPeriodDays. Requires Claude Code v2.1.248 or later; earlier versions delete them after cleanupPeriodDays.`
- 例外（デスクトップアプリの会話も30日で消える）：`Managed settings set cleanupPeriodDays`／`The HIPAA configuration applies to your sessions`（＝会社の管理設定が保持期間を決めているとき）
- 残るもの：`history.jsonl` ＝ `Every prompt you've typed, with timestamp and project path.`（`Kept until you delete them`の表）
- 平文：`Transcripts and history are not encrypted at rest. OS file permissions are the only protection. If a tool reads a .env file or a command prints a credential, that value is written to projects/<project>/<session>.jsonl.`
- 消したら失うもの：`~/.claude/projects/` ＝ `Resume, continue, and rewind for past sessions, and auto memory for every project`

### [Settings reference](https://code.claude.com/docs/en/settings-reference)（`cleanupPeriodDays`・`desktopSessionCleanupPeriodDays`）

- verbatim：`The sweep deletes transcripts without showing a message, so a session you haven't used for longer than the retention period no longer appears in the /resume picker.`（**知らせなく消える**）
- verbatim：`Setting 0 fails validation, so pick a large value such as 3650 for long retention.`
- 例：`{ "cleanupPeriodDays": 20 }`（置き場所は`settings.json`・Scope＝Any file）
- `desktopSessionCleanupPeriodDays`：既定`0`＝期限なし。`cleanupPeriodDays`と両方より古くなったら消す（既定30なら`7`でも30日残る）。Scope＝User or managed（プロジェクトの設定では効かない）

### [Manage sessions](https://code.claude.com/docs/en/sessions)

- 再開：`claude --continue`（今のフォルダの最新）／`claude --resume`（一覧から選ぶ）／`/resume`（会話の中から切り替え）。**このページはターミナルの話**（`This page covers the CLI.`）。デスクトップアプリ・VS Codeの拡張は`each keep their own session list`
- 保持：`Change the 30-day retention｜cleanupPeriodDays｜settings.json`
- 削除：`Transcripts age out under the retention sweep rules. To delete a project's transcripts and related state sooner, run claude purge.`

### [Data usage](https://code.claude.com/docs/en/data-usage)

- verbatim：`Local caching: Claude Code clients store session transcripts locally in plaintext under ~/.claude/projects/ for 30 days by default to enable session resumption. Adjust the period with cleanupPeriodDays.`／`Transcripts of sessions started or most recently continued in Claude Desktop or Cowork are exempt from that limit by default.`
- ⚠️ 同じページのサーバー側の保持（学習を許可＝5年・許可しない＝30日）は、手元の記録とは別の話。本文に混ぜない

### [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop)

- ターミナルの会話をデスクトップアプリへ移す：`To move a CLI session into Desktop, run /desktop in the terminal.`（macOSとx64のWindows・Claudeのサブスクでログインしているとき）
- アーカイブ：一覧からアーカイブすると「Archived」タブへ移る。**アーカイブで会話の記録が消えるかは書かれていない**（作業用のworktreeの変更は約30日で消える、とだけある）＝本文で触れない

### 復元（消えた記録を戻せるか）

- **上の5ページに、消えた会話の記録を戻す方法は書かれていない**（claude-directory・settings-reference・sessions・data-usage・desktop を10/20に確認）。checkpointingの`checkpoint restore`は会話の中でファイルを前の状態に戻す機能で、消えた会話を戻すものではない
- 本文では「公式に戻す方法は書かれていない」と書く。Macのバックアップ等の一般論は、試していないので書かない

## 4. X編集部の在庫

- `x-article-sync-check.py`（10/20）：この題材の未接続の下書きは出ていない
- `KEEP-01`「会話記録はPCに30日しか残っていない」（`knowledge/x/queue.md`・★★★★☆・未投稿）。**8/28時点の内容で、今は「デスクトップアプリの分は残る」に変わった。記事が出たらリンク型に組み替える**（公開前に単独で出さない）
- `RESUME-01`（10/20 08:25投稿）＝「同じ会話を続けるより、前提・決めたことだけメモで渡す」。**こちらは「記録が残るか」の問い**で重ならない。ただし記事の締めで「決めたことはファイルに残す」と書くなら、同じ趣旨になる＝記事の公開後にリンク型を作るときは`RESUME-01`の言い回しを使い回さない
- 10/5の@tokkyo宛リプライ案（`operations/article-backlog.md` D-46）

## 5. 既存記事との重なり（10/20 判定＝新規 no.76）

- TOP10 #5「翌日も続きから任せられるか」＝**続きから再開できるか**の問い（未公開）。こちらは**記録が残るか**の問い。再開の手順は書かない（公式へのリンク1行）
- no.25（Claude Code Desktopが大幅刷新。新機能と実務への影響を整理）＝機能紹介。H2に保持期間は無い
- no.70（Claudeに会社の情報を渡して大丈夫か）＝表の1行に「~/.claude/projects/ に平文で標準30日」。**8/28以降の「デスクトップアプリの分は残る」は反映されていない**＝公開後にno.70の1行を直す（リライトのメモ）
- no.30 コンテキストとは（概念）

## 6. 需要

- サジェスト（**10/20取り直し**）：`claude code 履歴`8（確認／コマンド／削除／**消えた**／保存／共有／**消える**）・`claude code 会話`10（会話履歴／引き継ぎ／戻る／分岐／保存／会話ログ／会話履歴 保存／再開）・`claude 履歴`10（削除／**消えた**／一括削除／確認／検索／**復元**／エクスポート）・`claude code 会話履歴`5（保存／削除／**復元**／出力）・`claude code 保存期間`2（セッション 保存期間）
- GSC（直近3か月・10/19）：履歴の語の表示は0件。隣のClaude系の束＝`claude 担当職種`20表示・`chatgpt work claude code`16表示（10/20は取り直していない＝1日前の値）

## 7. まだ無いもの

- **消えて困ったことがあったか**（C-18・本人にしか答えられない）。無ければ「困る前に知っておく」の書き方にする
- **デスクトップアプリの一覧で、中身の消えた古い会話を開くと何が出るか**（本人の画面で確認）
- ~~ターミナル（CLI）で直接`claude`を打って使っているか~~ → **10/20 ファイルで解決**：`history.jsonl`で3〜5月の初期と8/25・9/28のログインだけ（2-3節）。本人に聞かない
- ~~消えた記録を戻せるか~~ → **10/20：公式5ページに戻す方法は書かれていない**（3節）
