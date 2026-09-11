# 事実シート：Claude Codeの許可設定・auto mode（TOP10 #8・D-16）

作成：2026-09-11 18:10（本セッションで一次情報を直接確認）。**執筆側はこのシートの事実だけを使う。ここに無い数字・仕様は書かない。**

## 1. 記事の芯（9/11 17時台にユーザーの問いで決め直した）

**「auto modeにしても確認は消えない。消えなかった確認の正体と、自分で確認に残した6つ」。**
設定を見せるだけでは薄い（ユーザー指摘）。芯は、ユーザーが体感した「自動にしたのに、また聞かれる回数が増えた」を一次情報で説明すること。

## 2. この環境の実物（2026-09-11実測）

| 項目 | 値 | 出どころ |
|---|---|---|
| 切り替え日 | 2026-08-12 | メモリ`feedback_permission_setup`（8/11 21:45作成）・X `AUTO-気`（8/14投稿） |
| 切り替え前 | 1送信で数十回の確認。操作ミス以外で拒否したことはなく、全部「許可」を押していた | 同メモリ |
| 切り替え前に溜まった許可 | プロジェクト側`.claude/settings.local.json`に**331件**（最終更新2026-08-11 10:53） | 実測 |
| 全体設定 | `~/.claude/settings.json`：`defaultMode: auto`／`allow` **80件**（Bash 22・ブラウザ操作系40・その他18）／`ask` **6件**／`deny` 0件 | 実測 |
| 確認に残した6つ（ask） | `sudo`／`rm -rf`／`git push --force`／`git push -f`／`git reset --hard`／`git clean` | 実測 |
| 手元のClaude Code | CLI `2.1.243`／デスクトップアプリ同梱は`2.1.260`と`2.1.266`（最新は`2.1.268`・9/11公開） | 実測（`claude --version`・`~/Library/Application Support/Claude/claude-code`） |
| X `AUTO-気`（8/14） | 11ビューで止まった（自己最低） | `knowledge/x/published.md` |

## 3. 公式の一次情報

### 3-1. auto modeが既定になった（公式ブログ 2026-08-07）
URL：https://claude.com/blog/auto-mode-default-in-claude-code
- 2026-08-14から**Pro・Max・Teamの新しいセッションはauto modeで始まる**
- verbatim：`users approve 97% of permission prompts in Claude Code`（個別の許可の却下率は3%。プランの承認では39%が却下）
- `49.5% of active CLI users have manually created a Bash allow-rule`／`62% of users have used bypassPermissions or clicked 'don't ask again' on Bash`／`25% of interactive sessions start in bypass permissions mode`
- 統制実験：`human review caught just 13.6% of dangerous commands, while auto mode caught 89%`
- auto modeは`routes each tool call through a classifier targeted at blocking actions that are irreversible, destructive, or aimed outside your environment`。ただし`does not eliminate risk`

### 3-2. auto modeの仕組み（公式ドキュメント permission-modes・2026-09-11取得）
URL：https://code.claude.com/docs/en/permission-modes
- 判定の順番（verbatim要約）：①allow/ask/denyルールに当たるものは即決 ②作業ディレクトリ内の読み取りと編集は自動承認（保護パスへの書き込みと**作業ディレクトリ外の最初の読み取り**は除く） ③それ以外は分類器（classifier）へ ④分類器が止めたらClaudeに理由が渡り、別の方法を試す
- **askルールはauto modeでも必ず聞く**：`If an explicit ask rule matches the command, Claude Code asks you even in auto mode.`
- **auto modeに入ると、広すぎるallowは落とされる**：`Bash(*)`・`Bash(python*)`のようなワイルドカード・パッケージマネージャの実行・`Agent`・`Monitor`。狭いルール（`Bash(npm test)`）は残る
- 分類器はSonnet 5で動く（`The classifier runs on Claude Sonnet 5 by default`）
- **作業ディレクトリ外の最初の読み取り**：blockReadsOutsideWorkingDirectoriesがオフのとき、auto modeでも**最初の1回だけ確認**が出る。選択肢は3つ——`Keep allowing`（記録され、以後出ない）／`Block from now on`（設定がtrueになり以後拒否）／`Ask again next time`（次回また聞く）
  - ⚠️ **このリポジトリは毎セッション`~/Documents/GitHub/tasks/README.md`（作業ディレクトリ外）を読む**＝この確認が当たる位置にいる

### 3-3. 8/29以降、auto modeで確認が増える向きの変更（公式CHANGELOG・2026-09-11に生データで確認）
URL：https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md

| 版（日本時間の公開） | 変更（verbatim） | この環境に当たるか |
|---|---|---|
| 2.1.251（8/29） | `Fixed Bash permission checks auto-approving commands that assign an arithmetic expression to an integer shell variable ...; these now prompt for approval` | 当たらない（そういうコマンドを使っていない） |
| 2.1.257（9/2 02:15） | `Added a one-time prompt in auto mode before the first file read outside the working directories, with the option to block such reads` | **当たる**（tasks/README.mdを毎回読む） |
| 2.1.257 | `Added a Containment Escape rule to auto mode so cloud metadata-credential fetches, egress evasion, and cross-tenant reach are no longer auto-approved` | 当たらない |
| 2.1.257 | `Fixed a permissions.ask rule being skipped in auto mode when the matching command ran inside a compound command or subshell` | **当たり得る**（askの6件が`cd … && …`の中でも確認になる） |
| 2.1.257 | `Fixed Bash permission checks auto-approving certain [[ ]] conditionals ...; these commands now prompt for approval` | 当たり得る（シェルの条件式を使うことがある） |
| 2.1.260（9/4） | zshの`REPORTTIME`等への代入に隠したコマンド置換が確認に | 当たらない |
| 2.1.261（9/5 02:49） | `Changed auto mode to treat a link that packs content into a public diagram renderer's URL as an upload to that site: no longer auto-approved unless you asked for it` | 当たらない |
| 2.1.268（9/11） | `Improved auto mode denials: the message Claude receives now names the rule that blocked the action and asks Claude to try a safer method and finish unrelated work before stopping to ask you` | **逆向き**（止まって聞く回数を減らす） |

**⚠️ 書き方の注意**：「auto modeが使いにくくなった」と一般化しない。増えたのは自動承認しない操作の種類で、通常のファイル編集・コマンド実行の扱いは変わっていない（`research/trends.md` 9/2・9/5の注記と同じ）。

## 4. まだ無いもの（記事の弱点）

- **切り替え前後の確認回数の実測が無い。**「1送信で数十回」はユーザーの申告。切り替え後に何回聞かれたかの記録も無い
- **「増えた」の原因を1つに特定できていない。**候補は3-3の「当たる／当たり得る」の3件。実機で確認の中身を記録するまで断定しない
- 対処：`PermissionRequest`フックで確認のたびにツール名を記録する（設定変更なのでユーザーの承認が要る）。数日ぶんの記録が入れば「auto modeが実際に何を聞いてくるか」を実数で書ける

## 4-2. X編集部の在庫（2026-09-11 17時台に確認。**記事側が読んでいなかった材料**）

| ID | 状態 | 使える材料 |
|---|---|---|
| `AUTO-気`（8/14投稿） | 11ビュー（自己最低・伸びが止まった） | 「安全のための確認のはずが、全部『許可』を押してただけ」「今日からデフォルトで自動になるようです。公式によると承認率97%」 |
| `PERM-01`（キュー2位・★★★★★・未投稿・期限超過7日） | 下書き | 「許可80件・確認6件・拒否0件」「8/29の更新でBashの一部が自動から確認に」「9/2の更新では作業フォルダの外を読むときも確認」「確認を減らすための設定のはずが、1週間で2回増えてます」「Macをまだ更新してないので、気づいてませんでした」 |
| `AUTOTAB-01`（キュー3位・★★★★★・未投稿） | 下書き | 「『これは毎回聞かなくていい』にした設定、数えたら**411件**」（＝プロジェクト側331＋全体80）「自動で承認されている分の判断ルールは、一度も見たことがなかった」「8/26のアップデートで見られるようになりました」（CHANGELOG `2.1.246`：`Added an Auto mode tab to /permissions for viewing and editing auto mode classifier rules`） |

**記事とXの分担**：記事が出たら、`PERM-01`をリンク型に組み替えて出す（`rules/x-post-flow.md`「記事を公開したら、その週にリンク型を1本入れる」）。**記事の公開前に`PERM-01`を単独で出さない**（同じ材料を2回使うことになる）。判断はX編集部。

## 5. 既存記事との重なり

- 許可・パーミッションを扱った記事は0本（`grep -l "許可\|permission" articles/*.md`はno.57だけで、意味が違う）
- 近い記事：no.55 ルールファイルとは（概念）・no.64 自動化の限界（人に残す判断）。**この記事は「Claude Codeの設定の実物」に絞り、判断論はno.64へリンクで逃がす**

## 6. 需要（2026-09-11 サジェスト実測）

`claude code 許可`10件（めんどくさい／許可不要／バイパス／設定／自動／コマンド／許可リスト）・`claude code auto`10件（auto mode／auto mode 設定／auto モード／使い方）・`claude code 権限`5件（権限設定／権限モード／権限確認をスキップ）。GSCの自サイトには該当クエリ0件（まだ記事が無いため）。
