# 材料シート：非エンジニアがClaude Codeでできること＋最初の1週間で詰まった所（TOP10 #4・T-5・D-20・no.9「claude-code-introduction」の全面改稿・URL維持）

作成：2026-10-02 07時台。**2026-10-20 11時台に3〜6節を今の状態に合わせた**（GSC・カニバリ・X在庫・需要・公式のデスクトップアプリ）。**執筆可能：△（12項目の本人確認＝旧C-3が未回答。最初の1週間の記録が薄い）**
> **執筆側はこのシートの事実だけを使う。**ここに無い数字・体験は書かない。12項目は2026-09-11にCCが記録から作った一覧で、本人の確認はまだ。

## 1. 記事の芯

**「非エンジニアの自分にClaude Codeは扱えるか・何ができるか」を決めたい人に、実際にやっている12項目と、最初の1週間で詰まった所を渡す。**（`tasks/README.md` TOP10 #4の行）
- この記事でしか渡せないもの（④）：12項目＋詰まった所
- カニバリ：no.9と正面で重なる → **新規にせず全面改稿（URL維持）**
- 確認：C-3（＝`operations/editorial-meeting.md`の保留「旧C-3」。12項目に抜け・出したくないもの・やっていないものがあるか）
- `operations/theme-map.md`：「最初の1週間に何をするか」はこの記事に統合
- 注意（`operations/editorial-strategy.md` 3節）：**「とは」で戦わない。**no.9「Claude Codeとは」は内部リンク15本があっても3か月表示0だった

## 2. この環境の実物

### 2-1. できること12項目（2026-09-11版・git `c0a1cea`の`operations/editorial-meeting.md`）

| # | できること | 9/11の記録 | 2026-10-02にCCが数え直した値 |
|---|---|---|---|
| 1 | ブログ記事の構成・執筆・チェック | 64本・`operations/article-precheck.py`ほか | 公開70本（`operations/article-md-workflow.md`の表・no.1〜72・欠番2）。`operations/*.py`は16本 |
| 2 | WordPressへの入稿（下書きまで） | no.63〜66・Chrome拡張 | `operations/md-to-wp.py`あり。本数は数え直していない |
| 3 | アイキャッチのリサイズ・リネーム・色補正 | `images/`のアイキャッチ69枚 | `images/`の`eyecatch_`77ファイル |
| 4 | X投稿の下書き・文字数と1行目の機械チェック | `knowledge/x/queue.md`・`x-count.py`・`x-firstline.py` | 在庫55本（`queue.md` 10/02の更新行）。スクリプト2本あり |
| 5 | 毎朝・週2回の自動リサーチ | 定期実行6本・51回（2026-07-06〜） | 数え直していない（`operations/automation-log.md`は135行） |
| 6 | サーチコンソールの数字を読んで記事を決め直す | `operations/site-status.md` | 1,711行 |
| 7 | 領収書PDFから経費台帳を作る | `business-ops` 70行（⚠️ 進んでいない） | リポジトリはある。行数は数え直していない |
| 8 | 請求書PDFの生成 | `business-ops/invoices/generate_invoice.py` | ファイルあり |
| 9 | 営業リストの抽出とスコアリング | `sales/`（7件・成約なし） | フォルダあり。件数は数え直していない |
| 10 | メルカリ出品の下準備 | no.42 | no.42は公開済み（2026-06-29） |
| 11 | カレンダー登録 | メモリ`feedback_calendar` | メモリの索引に記載あり |
| 12 | ルール・メモリ・引き継ぎで自分の環境を保つ | CLAUDE.md・rules/・メモリ86件・session-handoff 80コミット | CLAUDE.md 139行・`rules/` 2,338行・メモリのファイル119個（索引を含む）・`session-handoff.md` 156コミット |

### 2-2. 最初の1週間の記録

| いつ | 実物 | 出どころ |
|---|---|---|
| 2026-03-27 | 最初のコミット。同じ日に`test.md`（日本語のテスト）・`branch.md`（ブランチの練習）・PR #1（`my-first-branch`）のマージ。**⚠️ 10/20：Claude Codeで作った記録は無い**（コミットにClaudeの共著が無く、GitHub Desktopの練習とも読める。Claudeの共著の初出は2026-04-03の`073e6ce2`）＝「Claude Codeの最初の週」の根拠に使わない | `git log --reverse` |
| 2026-03-30 | 最初の記事と、ルール文書（SEOルール・サービス・ワークフロー・書き方）を追加。READMEを追加 | 同上 |
| 2026-04-01〜04-03 | READMEと方針の文書を更新。略語のルールを追加。4/3に記事#8と運用ルール | 同上（3月は12コミット・4月は21コミット） |
| 2026-04-07 | no.9を公開。入れた道具はVisual Studio Code・GitHub Desktop・Warp・Node.js。YouTubeの解説3本を見て始めた | `articles/claude-code-introduction.md` |
| 同上 | **詰まった所①**：「全部英語で、何が起きているかわからなかった」。エラーなのか正常なのかも判断できない → ClaudeとChatGPTに画面のスクショを見せて進めた | 同 H3「全部英語で、何が起きているかわからなかった」 |
| 同上 | **詰まった所②**：ターミナル（Warp）は「今も慣れているとは言えません」。作業はほぼVisual Studio Codeで完結 | 同 H3「ターミナルとVS Codeの感覚の違い」 |
| Claude Codeの前 | no.5（2026-03-17公開）では、カスタムGPTをやめてClaudeのプロジェクト機能を使っていた | `articles/ai-writing-claude-setup.md` |

- `theme-map.md`は詰まった所を「許可411件・フォルダ・ターミナル」と書いている。**411件＝全体80件＋このプロジェクト331件**（2026-10-02に設定ファイルで確認）
- **⚠️ 411件は最初の1週間の話ではない。**8/12に手動の許可から自動へ切り替え、8/14に`AUTO-気`「全部『許可』を押してただけでした」を投稿（`operations/article-backlog.md` D-16の行）。たまった件数の話
- **⚠️ 「フォルダ」で詰まった記録は見つからなかった。**no.9の本文では、フォルダが見えるVS Codeは「最初から使いやすかった」側に書かれている

**⚠️ 無いもの**：最初の1週間の日ごとの記録（コミットのメッセージだけ）。詰まった回数・かかった時間の記録なし。メモリは2026-04-13から（D-21の行）で、最初の1週間のぶんは無い。いまの主な入口（デスクトップアプリ）に替えた日の記録は、今回確認していない。

## 3. 公式の一次情報

**新しく調べていない。既にリポジトリに記録してあるものの転記。**

| # | 事実 | 出典 | 取得日・記録の場所 |
|---|---|---|---|
| 1 | Claude CodeはPro・Maxに含まれる | support.claude.com「Use Claude Code with your Pro or Max plan」 | no.72で確認済み（`in-house-vs-outsource-cost-facts.md` 3-3）。**verbatimの記録なし** |
| 2 | 有料プランの既定モデルはOpus 5.5 | [code.claude.com/docs/en/model-config](https://code.claude.com/docs/en/model-config)：`Pro, Max, Team, Enterprise, and Anthropic API: defaults to Opus 5.5` | `knowledge/x/queue.md` `PLAN27-リ`の事実欄（取得日の記載なし） |
| 3 | チャットとCoworkが1つに統合される（入口の前提が変わる） | [claude.com/blog/cowork-is-now-claude](https://claude.com/blog/cowork-is-now-claude)：`Claude Cowork and chat are merging into one Claude.` | 2026-09-18（`claude-entry-points-non-engineer-facts.md` 3節） |
| 4 | 学習に使われる条件・許可のモード | no.70・no.71で公開済み | `claude-company-data-training-facts.md`・`claude-code-permissions-auto-mode-facts.md` |

| 5 | デスクトップアプリの始め方：インストール→サインイン→「Code」タブ | [code.claude.com/docs/en/desktop](https://code.claude.com/docs/en/desktop)：`After installing, launch Claude, sign in, and click the Code tab.` | 2026-10-20（WebFetchの引用。**執筆前にブラウザで原文を開いて確かめる**） |
| 6 | 対応OS：macOS（Intel・Apple Silicon）・Windows（x64・ARM64）・Linux（ベータ） | 同上：`Universal build for Intel and Apple Silicon`／`For x64 processors`／`Get Claude for Linux (beta)` | 同上 |
| 7 | セッションを分けて動かすにはGitが要る。Macは多くが最初から入っている | 同上：`Session isolation requires Git. Most Macs include Git by default.` | 同上 |
| 8 | ローカル＝自分のパソコンでファイルに直接さわる／クラウド＝アプリを閉じても続く | 同上：`Local: runs on your machine with direct access to your files`／`Cloud: ... Sessions continue even if you close the app.` | 同上 |

- 本人の今の入口：**デスクトップアプリで、作業の場所をローカルにして使っている**（no.73 `claude-chat-cowork-code-difference` の最後のH2「私は、手元のフォルダで記事をつくるので、ローカルだけを使っています」）
| 9 | **デスクトップアプリならNode.jsもCLIも入れなくてよい**／ターミナルを使わずに変更を確かめられる | [code.claude.com/docs/en/desktop-quickstart](https://code.claude.com/docs/en/desktop-quickstart)：`The desktop app includes Claude Code, so you don't need to install Node.js or the CLI to use the Code tab.`／`review its changes without using a terminal` | 2026-10-20（WebFetchで本文を取得・原文の文） |
| 10 | 必要なプラン：Pro・Max・Team・Enterprise | 同上：`Claude Code requires a Pro, Max, Team, or Enterprise subscription` | 同上 |
| 11 | 最初は小さく、よく知っているものから | 同上：`Start with a small project you know well. It's the fastest way to see what Claude Code can do.` | 同上 |

- **⚠️ 訂正（10/20）**：上の5〜8を取った /desktop のページだけを見て「Node.jsが要るかは記録なし」としていた。quickstartに答えがあった（9番＝要らない）
- **⚠️ まだ無い記録**：デスクトップアプリに替えた日。1番「Pro・Maxに含まれる（追加料金なし）」の原文

## 4. X編集部の在庫

`python3 operations/x-article-sync-check.py`（2026-10-02・**2026-10-20に再実行**＝この行は今も「X側の材料」を明記していない13件の1つ。10/2の後に同じ題材の新しい下書きは見つからなかった〔`queue.md`を「非エンジニア・詰まっ・ターミナル・英語で」でgrep〕）。同じ題材の下書き・投稿は次のとおり。

| ID | 中身 | 状態 |
|---|---|---|
| `R11-リ` | 非エンジニア向け11本でシリーズ完結 | 在庫7位（★★★★☆） |
| `R10-リ` | AI用語6つを非エンジニア向けに整理 | 在庫13位（★★★★☆） |
| `R11-01` | 任せる環境は結局5つのファイルだった | 在庫14位 |
| `ALLOW71-01` | 「次から聞かなくていい」と許可した操作が331件 | 在庫。盲検未合格 |
| `入稿-気` | 入稿はログインと公開ボタン以外が不要に | 在庫16位 |
| 固定（3代目） | 非エンジニアが、AIでコンテンツ運用を「止めずに回す」実験をしてます | 9/2から固定（46ビュー・9/17） |
| `CLOUD-気` | Claude Codeのクラウド版のお試し250ドル。非エンジニアの自分は使い道がわかっていない | 9/28投稿済み |
| メルカリ出品の投稿 | 写真フォルダ→一言で6処理 | 投稿済み（81ビュー・`published.md` 371行） |
| `士_HR3` | 環境を作るのが難しそうだった。難しかったのは操作ではなく仕事の整理 | `sns/posts-stock.md`。GPT提案の草案で、実体験・数字は未確認 |

## 5. 既存記事との重なり（2026-10-20に見直し）

10/2の後に公開した3本（no.71・no.73・no.74）を、題とH2で読者の問いを比べた。

| 記事 | 読者の問い | 重なる所 | 扱い |
|---|---|---|---|
| no.9 `claude-code-introduction`「Claude Codeとは何か？できること・使い方を実際に使って整理した」 | Claude Codeとは何か／何ができるか | **正面**。H2「Claude Codeでできること」「導入前の正直な状態」「実際に導入した流れ」 | **この記事で全面改稿（URL維持）** |
| no.73 `claude-chat-cowork-code-difference`「Claudeのチャット・Cowork・Claude Codeの違い」 | どれを使えばいいか／どこで開くか | 「チャットと何が違うか」「Web版・デスクトップアプリ・スマホ。どこで開けばいいか」 | **違いと開く場所はno.73に任せる**。この記事は1〜2文でリンク |
| no.74 `claude-code-company-introduction-no-it-staff`「Claude Code導入の手順。IT担当がいない会社が決める4つ」 | 会社に入れるとき何を決めるか（契約・管理する人・渡さない情報・最初の業務） | 「導入」「始め方」の語 | **会社として入れる話はno.74に任せる**。この記事は個人で触り始める人の「何ができるか・どこで詰まるか」 |
| no.71 `claude-code-permission-modes`「Claude Codeの許可、どこまで自動でいいか。モードの選び方」 | 確認をどこまで自動にするか | 許可の確認がたくさん出て詰まる話（411件はたまった件数で、最初の1週間の話ではない＝2-2節） | 詰まった所に許可を入れるなら、1行でno.71へ |
| no.14 `claude-code-compatible-jobs` | 自分の職種に合うか | 職種別の「できること」 | 隣。この記事は職種ではなく「1人が実際に任せている作業」 |
| no.21 `claude-code-glossary-beginners` | 用語が分からない | 初心者・非エンジニア | 隣（英語・用語で詰まった所からリンク） |
| no.62 `ai-work-environment-setup` | 任せる環境をどう作るか | 環境・ルールのファイル | 隣（12番からリンク） |
| no.19 `claude-code-limitations` | できなかったこと | 「できないこと」 | 「できないこと」はリンクで |
| no.42 `mercari-ai-listing` | メルカリ出品 | 12項目の10番 | 子 |

**判定：「非エンジニアに何ができるか・触り始めてどこで詰まるか」に答えているのはno.9だけ。**no.73（どれを・どこで）とno.74（会社で入れる手順）は問いが違う。改稿で1本にするので、2本で答える形にはならない。

## 6. 需要

- サジェスト（`operations/site-status.md` 2026-09-11 12時台取得）：`非エンジニア claude code`10件（本／使い方／できること／始め方／活用事例）・`claude code できること`10件（できないこと／非エンジニア／一覧）・`claude code 事例`9件・`claude code 初心者`7件・`claude code 非エンジニア`5件
- サジェスト（同 2026-09-12 17時取得）：`claude code 始め方`10件（windows／初心者／mac）・`claude code 最初`6件（にやること／の設定／にやるべきこと）・`claude 非エンジニア`10件・`claude できること`10件（一覧／できないこと）・`claude 導入`6件・`claude 使い方 初心者`4件・`claude code 準備`2件・`claude code 何から`1件
- サジェスト（**2026-10-20 11時台に取り直し**・`suggestqueries.google.com`）：`非エンジニア claude code`10件（本／使い方／できること／活用事例／始め方／活用／入門／note）・`claude code できること`10件（非エンジニア／できないこと／一覧／例／初心者）・`claude code 始め方`10件（windows／無料／スマホ／初心者／mac／vscode／ターミナル／非エンジニア／git）・`claude code 初心者`7件・`claude code 非エンジニア`4件・`claude code 最初`4件（にやること／の設定）
- 自サイトのGSC：no.9は**インデックス済みだが表示0**（2026-08-11・被リンク15本）／**表示なし**（2026-09-10）／2026-09-14の直近6か月のページ表にも行が無い
- **2026-10-20 再取得（直近3か月＝2026-07-18〜10-17・実Chrome）**：no.9（`page=!https://aicontent-note.com/claude-code-introduction/`）は**クリック0・表示0**。サイト全体でクエリに「非エンジニア」「できること」「始め方」を含むものは**表示0**。「初心者」は16表示（内部リンクの記事のクエリ1本だけ）。「claude code」を含むクエリは44表示・4クリック（no.56とno.14だけ）
- **リライトの判定（`rules/article-flow.md` 6章）**：11〜20位の滞留ではなく表示0なので、順位を上げる直しではなく**題と中身の立て直し**。URLは維持（被リンクは10/20にgrepで公開記事18本・8/11の15本から増えた）
- 隣の記事（2026-09-14・直近6か月）：用語集 0クリック／10表示／8.1位・no.62 0クリック／19表示／8.1位
- 「非エンジニア」「できること」「始め方」を含むクエリで、自サイトに表示が出た記録：**見つからず（未計測）**

## 7. まだ無いもの（本人にしか答えられないこと・未計測）

1. ✅ **2026-10-20 12:00 回答：7番・9番を外して10の作業にする**（「不必要なものがあって無理がないのなら10にして」）。~~**12項目の本人確認（旧C-3・未回答）。**~~抜け・出したくないもの・やっていないものがあるか。特に7番（経費台帳＝進んでいない）と9番（営業リスト＝成約なし）を出すか
2. ✅ **2026-10-20 13:11 回答**（`operations/interview-notes/claude-code-introduction.md`）：使い始めてから＝①VS Codeで作業していて、コミット・プッシュの意味が分からず変更がよくぶつかって止まった ②どのAI（Claudeのチャット／Claude Code／ChatGPTのWork／ふだんのチャット／Codex）を使えば求める答えが出るか今も分からない。⚠️ 記事の3つ（入れる順番・動画どおりに進まない・英語の表示）は「導入時」のもの（ユーザー指摘）。~~**最初の1週間で実際に詰まった所。**~~記録は「英語で分からない」「ターミナルに慣れない」の2つだけ。ほかに止まった所・解決までにかかった時間は本人の記憶にしか無い
3. **「フォルダ」で詰まった中身。**`theme-map.md`に語だけあり、記録が見つからない
4. ~~**いまも使っている道具はどれか。**~~（10/20：構成案から外した＝H2-2で「デスクトップアプリならターミナルは要らない」と答えるので、詰まった所にターミナルの行を置かない）今の入口がデスクトップアプリ（ローカル）なのはno.73に書いてある（3節）。残りは、no.9のVS Code・GitHub Desktop・Warp・Node.jsのうち今も開いているもの／デスクトップアプリに替えた時期と理由
5. **未計測**：12項目それぞれの頻度（毎日やるもの・1回きりのもの）／2番・5番・7番・9番の今の件数
