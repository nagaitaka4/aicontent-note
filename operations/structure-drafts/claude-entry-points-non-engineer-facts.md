# 材料シート：Claude.ai・デスクトップ・Cowork・Claude Code。非エンジニアはどれを使えばいいか（TOP10 #5・T-2・D-28）

作成：2026-09-21 06時台（月曜のフル版②）。**執筆可能：△（前提が動いている最中。3節の⚠️を読んでから構成に入る）**
> **⚠️ 入口は「4つ」ではなくなる。**2026-09-16の公式発表で**チャットとCoworkが1つに統合**され、順次展開中。**「4つから選ぶ」を骨組みにすると、公開時点で古くなる。**

## 1. 記事の芯

**「Claudeを使いたいが、どの画面を開けばいいのか分からない」人に、いまの入口と選び方を渡す。**
読者が決めたいのは「自分の仕事なら、どれを開くか」。機能の一覧ではない。**4つ全部を実際に使い分けている実物があることが、この記事の主役**（④）。
**統合で何が変わるかまで書く**——切り替えて選ぶ形から、Claudeが道具を選ぶ形へ。**選び方の軸が「どの入口か」から「どこで動かすか（手元かクラウドか）」へ移る**というのが、いまの一次情報から言える範囲。

## 2. この環境の実物

| 入口 | この環境での実物 | 何に使っているか |
|---|---|---|
| Claude Code（デスクトップアプリ） | このリポジトリの記事制作の主戦場。記事**69本**（`articles/`）・構成案・アイキャッチ・入稿 | 構成→執筆→チェック→入稿 |
| Claude Code（CLI／スクリプト） | `operations/*.py` 8本（`x-count.py`・`pipeline-status.py`・`article-precheck.py`等）／スケジュールタスク（朝ブリーフ） | 測る・回す |
| Cowork | no.58（`claude-cowork-usage-data`）の検証で使用。**公式の利用データ記事**。枠の消費が速い点は`ideas.md` `daily-20260819-01`が「要実測」のまま | 一度使って記事にした |
| Claude in Chrome（拡張） | WordPress入稿・GSCの取得（本日のGSC 100クエリもこれ）。`feedback_wp_entry_by_cc` | ログインの要る画面 |
| Claude.ai（ブラウザのチャット） | 記録上の使用は少ない。**ユーザーの普段のチャットはGPT**（TOP10 #7の材料シート1節・2026-09-14の本人回答） | ほぼ使っていない |

**⚠️ 無いもの**：Claude.ai（素のチャット）を仕事で使った実測。統合後の画面を見た記録（**ユーザーのMaxにはまだ来ていない**＝X `CWMERGE-01` 9/19投稿の最終行）。Coworkの枠の消費倍率（未実測）。

## 3. 公式の一次情報

| # | 事実 | 出典（verbatim） | 取得日 |
|---|---|---|---|
| 1 | **チャットとCoworkが1つに統合される。**Pro・Maxから数週間かけて展開。**一度移ると戻せない** | [claude.com/blog/cowork-is-now-claude](https://claude.com/blog/cowork-is-now-claude)：`Claude Cowork and chat are merging into one Claude.` ／ `Ask Claude for what you need, and it can decide which tool to use.` ／ `Once your account has the new experience, you can't switch back to separate "Chat" and "Cowork" options.` | 2026-09-18 |
| 2 | **Claude Docs・Claude Slidesがベータで開始。**Freeは対象外 | [ヘルプ Get started with Claude Docs](https://support.claude.com/en/articles/16923645-get-started-with-claude-docs)：`available in beta on Pro, Max, Team, and Enterprise plans. It isn't available on the Free plan.` | 2026-09-18 |
| 3 | **Claude Codeに「Projects」（ベータ）。**Claudeが仕事を分けて並列に走らせる。**いまはクラウドで動く。手元で動かせるのは「もうすぐ」** | [claude.com/blog/projects-redesigned](https://claude.com/blog/projects-redesigned)：`Claude scopes the request, delegates the work, coordinates parallel threads, reviews the outputs, and assembles the finished result.` ／ `Starting today, updated projects are available in beta to select Claude Pro and Max subscribers who use cloud sessions in Claude Code.` ／ `Threads run in the cloud today; running on your machine alongside your local tools and code and behind your network is coming very soon.` | 2026-09-21 |
| 4 | Claude in Chrome が一般提供 | [claude.com/blog/claude-in-chrome-generally-available](https://claude.com/blog/claude-in-chrome-generally-available)（`datePublished` **2026-08-26**・本日CCが確認） | 2026-09-21（**本文は未読**） |
| 5 | Artifacts in Claude Code | [claude.com/blog/artifacts-in-claude-code](https://claude.com/blog/artifacts-in-claude-code)（`datePublished` **2026-06-18**） | 2026-09-21（**本文は未読**） |

**⚠️ 執筆前に取り直すもの**：統合の展開状況（「順次」がどこまで進んだか）／Projectsの提供範囲（ベータの対象が広がる予定）／#4・#5の本文。

## 4. X編集部の在庫

| ID | 中身 | 状態 |
|---|---|---|
| `CWMERGE-01` | チャットとCoworkが1つに（**2026-09-19 08:54に投稿済み**・重み278） | 投稿済み。**本文の最終行「自分のMaxには、まだ来てません。」＝この記事の入口にそのまま使える** |
| `CW58-02` | Coworkの9割が開発以外だと公式が公開 | 在庫。⚠️ **統合で「Cowork」という呼び名の前提が動いている**（9/20の注記） |
| `CW-02` | ChatGPT WorkとClaude Codeを比べた | 在庫（★★★★☆） |
| `CW-03` | スケジュール実行の同時数がプランで決まる | 在庫（★★★★☆） |
| `research-20260918-03` | Claude Docs・Slides（`ideas.md`・未下書き） | 期限9/20超過・閉じていない |
| `research-20260918-04` | Claude CodeのProjects（`ideas.md`・未下書き） | 期限9/21＝本日 |

## 5. 既存記事との重なり

| 記事 | 重なる所 | 扱い |
|---|---|---|
| no.58 `claude-cowork-usage-data` | H2①「Claude Coworkとは？Claude Codeとの違いと、どこから使えるか」が**正面で重なる** | **この記事は「選び方」で立てる。**no.58は「Coworkの使われ方のデータ」。⚠️ **統合でno.58のH2①は前提が変わる＝リライト候補**（バックログへ） |
| no.56 `chatgpt-work-claude-code-comparison` | ChatGPT Work と Claude Code の選び方 | **別社の比較**。こちらはClaude内の入口。隣 |
| `claude-code-desktop-renewal` | デスクトップアプリの刷新 | 隣（機能の話） |
| `claude-code-introduction` | Claude Codeとは | 隣（入口1つの説明） |

## 6. 需要

- サジェスト（TOP10 #5の行・2026-09-12〜19に取得）：`claude cowork`10件（何ができる／claude code 違い）・`claude cowork code`10件（違い／使い分け）・`claude code desktop cli`10件・`claude アプリ 違い`10件・`claude デスクトップ`10件
- 自サイトのGSC（直近3か月・2026-09-21）：`claude cowork 使い方`3表示／33.7位・`cowork 使い方`2表示／28.5位・`claude コワーク 使い方`1表示／37.0位・`claude codeとの違いは？`2表示／4.0位・`クロードコードとの違いは？`1表示／2.0位
- 受け皿の`claude-cowork-usage-data`は**2クリック／48表示／11.4位**
- **クラスタとしては小さい（合計9表示）。**ただし**「違いは？」系で2位・4位に入っている**＝答えとして評価されている芽がある

## 7. まだ無いもの（本人にしか答えられないこと・未計測）

1. **統合後の画面が来たか。**来たら、入力欄がどう変わったかを1枚見せたい（X `CWMERGE-01`の続き）
2. **Claude.ai（素のチャット）を仕事で使っているか。**「普段のチャットはGPT」なら、この記事では「Claudeのチャットは使っていない」と書けるか
3. **Coworkをもう一度使うか。**統合後に「Coworkの枠の消費が速い」がどうなったかは実測の価値がある（`daily-20260819-01`が1か月「要実測」のまま）
4. **Projectsが手元に来たか／待機リストに登録するか**（来れば③の実測が書ける）
