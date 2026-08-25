# AI・Claude Code 最新情報・トレンド

最終更新: 2026-08-26

---

## [2026-08-26] 調査結果（デイリー・8:00の回）

**本日の主収穫は1件。Claude Code v2.1.246で、`/permissions`に「Auto mode」タブが増え、autoモードが自動承認するときの分類ルールを画面で見て編集できるようになった。**本日04:17（JST）公開で、旬としてはいちばん新しい。**自分の設定は`defaultMode: auto`＋許可リスト411件（グローバル80／プロジェクト331）で、まさに使っている機能そのもの**のため、実務に落として語れる。**本日この素材を下書き化してキューへ入れた**（消化先＝`queue.md`の`AUTOTAB-01`）。

### Claude Code / Anthropic

- **【本日の主収穫・使う側の何かが変わる】Claude Code v2.1.246 で `/permissions` に「Auto mode」タブが追加された**（一次情報＝[anthropics/claude-code CHANGELOG.md](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md)を**本日CCが直接取得して確認**）
  - **原文（verbatim）**：`Added Auto mode tab to /permissions for viewing and editing auto mode classifier rules`
  - **公開時刻**：npmレジストリの`time`フィールドで確認。`2.1.246` は **2026-08-25T19:17:34Z＝日本時間 2026-08-26 04:17**（`curl https://registry.npmjs.org/@anthropic-ai/claude-code`で本日取得）
  - **使う側の何が変わるか**：autoモードは「安全そうな操作は聞かずに進める」モード。**これまでその判断（分類）ルールは画面から見えなかった。**今回のタブで**見る・編集するの両方ができる**ようになった。自分で書く許可リスト（`settings.json`の`permissions.allow`）とは別レイヤーの話
  - ⚠️ **CHANGELOGの記述は上の1行だけ。**タブの中身（ルールの粒度・書式・既定でいくつ入っているか）は書かれていない。**「◯種類のルールが見える」等は書かない**（実機で開くまで不明）
  - ⚠️ **公式ドキュメント側の追記は未確認。**一次情報はCHANGELOGの1行
- **v2.1.243（日本時間 2026-08-25 08:10 公開）も未記録だった**（前回のデイリー回が8:00に走った10分後の公開）。使う側に効くものだけ抜き出す
  - `Improved native install download size: binary now zstd-compressed (~75 MB vs 340 MB)`＝**ネイティブ版の配布サイズが340MB→約75MB**
  - `Fixed /resume only listing 50 most recent sessions`＝**`/resume`が直近50件しか出ない不具合の修正**
  - `Added promptCacheTtl and subagentPromptCacheTtl settings for cache management`＝プロンプトキャッシュのTTLを設定で持てるようになった
  - `Added keyless sign-in under /login via Anthropic Console account`＝Consoleアカウントでのキーなしサインイン
  - `Updated /model picker and claude-api skill showing Sonnet 5's $2/$10 list price`＝**8/21のフル版が記録済みのSonnet 5価格が、`/model`の表示側にも反映された**（新しい値下げではない）
- **バージョンの公開時刻（本日npmレジストリで実測）**：`2.1.242`＝8/25 04:16／`2.1.243`＝8/25 08:10／`2.1.245`＝8/25 13:45／`2.1.246`＝**8/26 04:17**（JST）。**`2.1.244`は存在しない**
  - ⚠️ **npmの`dist-tags`は`latest: 2.1.246`／`stable: 2.1.231`。**`stable`タグは15バージョン分遅れている。**「最新版」と「安定版」は別物**で、記事・投稿で「最新版が◯◯になった」と書くときは`latest`の話だと明示する
- **料金の差分なし**（[claude.com/pricing](https://claude.com/pricing)を本日確認）。Free $0／Pro **$17（年払い）・$20（月払い）**／Max $100〜（5x・20x）／Team $20・$25（標準）＋$100・$125（プレミアム）／Enterprise カスタム。**8/24に常設化した料金ページ巡回の2日目。変更なし**

---

## [2026-08-25] 調査結果（デイリー・8:00の回）

**本日の収穫は1件。Claudeのウェブ版とデスクトップアプリで、長い回答の表示（ストリーミング描画）が作り直された。**モデルの賢さではなく画面の描き方の改善で、**長文を出させる人ほど体感が変わる**。公式が数字（詰まる回数9分の1・最長の固まり4.5分の1・120Hzで120fps維持）を出しているため、実務に落として語れる。**本日この素材を下書き化してキューへ入れた**（消化先＝`queue.md`の`STREAM-01`）。

### Claude Code / Anthropic

- **【本日の主収穫・使う側の体感が変わる】Claudeのウェブ版とデスクトップアプリで、長い回答の表示が作り直された**（一次情報＝[@ClaudeDevs・日本時間 2026-08-25 6:51](https://x.com/ClaudeDevs/status/2092006814804214163)を**本日CCがブラウザで直接開いて本文を確認**）
  - **原文（verbatim）**：`Long answers on Claude on web and desktop now stream ~4x smoother.` ／ `We rebuilt the streaming renderer to only touch what's still changing, so a long reply stalls 9x less on a slower laptop, its worst freeze is 4.5x shorter, and on a 120Hz MacBook it holds 120fps start to finish.`
  - **数字の読み方**：`~4x smoother`＝**滑らかさが約4倍であって、速度が4倍ではない**。`stalls 9x less`＝途中で詰まる回数が9分の1、`worst freeze is 4.5x shorter`＝いちばん長い固まりの時間が4.5分の1。いずれも`on a slower laptop`（遅いノートPC）の条件付き
  - ⚠️ **対象は`Claude on web and desktop`＝Claudeアプリ（チャット）のウェブ版とデスクトップアプリ。Claude Codeとは書かれていない。**「Claude Codeが速くなった」と書いたら誤り
  - ⚠️ **公式のリリースノートには載っていない。**[Claude Apps リリースノート](https://support.claude.com/en/articles/12138966-release-notes)は**2026-08-06のまま**（本日確認）で、この改善のエントリは無い。**一次情報は@ClaudeDevsの投稿そのもの**として扱う
  - **使う側の何が変わるか**：記事1本分のような長い回答を出させたとき、途中で表示が固まる・カクつくのが減る。**中身の進化ではなく表示側の改善**で、長文を書かせる人ほど効く
  - **本日この素材を下書き化してキューへ入れた**（消化先＝`queue.md`の`STREAM-01`）
- **MCPコネクタの企業管理認証が一般提供に**（[@ClaudeDevs・日本時間 2026-08-25 3時台](https://x.com/ClaudeDevs/status/2091953609185657251)）。原文（verbatim）：`Enterprise-managed auth for MCP connectors is now generally available.` Team・Enterpriseの管理者がIdPで認可を一元化し、利用者は個別のOAuthなしでツールに繋がる
  - ⚠️ **X投稿には採らない**：対象がTeam・Enterpriseの管理者で、このメディアの読者（個人・中小企業のコンテンツ運用者）の手元では何も変わらない
- **公式changelogは v2.1.241（2026-08-23）が最新のまま**（[公式changelog](https://code.claude.com/docs/en/changelog)を本日確認）。本文は`Bug fixes and reliability improvements`の1行のみで、**4日連続で中身が公表されていない**
- **Anthropic Newsroom は 2026-08-14（透かしの記事）から新規なし**（[anthropic.com/news](https://www.anthropic.com/news)を本日確認・**11日連続**）
- **Claude Platform リリースノートは 2026-08-20（Python SDK v1.0）が最新のまま**（[platform.claude.com](https://platform.claude.com/docs/en/release-notes/overview)を本日確認）
- **Claude Apps リリースノートは 2026-08-06 のまま**（[support.claude.com](https://support.claude.com/en/articles/12138966-release-notes)・**19日連続で動きなし**）
- **Claude Academy（8/24からデイリーの巡回先に追加）は数字に変化なし**（[academy.claude.com/products/code](https://academy.claude.com/products/code)を本日確認）。`Claude Code 101`は**12 lessons · 1 quiz · 1 hr**のままで、8/24のフル版の記録どおり
  - ⚠️ **8/24の記録「日本語で表示される」は環境によって変わる。**本日この環境で開いたときはコース本文が英語表示だった（日付表記だけ`9月1日`のように日本語）。**「日本語のコースがある」と断定して書かない**

### 障害（記録のみ・X投稿には採らない）

- **2026-08-24〜25に障害が3件あった**（[status.claude.com](https://status.claude.com/)を本日確認）
  - **モデルのエラー増加**：`From 9:50pm PT / 04:50 UTC through 00:36am PT / 07:36 UTC, users saw elevated errors`＝**日本時間 8/24 13:50〜16:36**。Claude Opus 5・Fable 5ほかが対象（[ITmedia AI+ 2026-08-24](https://www.itmedia.co.jp/aiplus/article/2608/24/2000000719/)も同じ時間帯で報道）
  - **claude.aiのログインエラー**：日本時間 **8/25 01:02〜01:08** と **8/25 05:00〜05:08** の2回。どちらもClaude Codeのサブスク接続にも影響
  - **手元の事実**：8/24の障害時間帯（13:50〜16:36）の中で、**14:00にこのリポジトリへコミットが通っている**（`docs: 3点セットの提示は3点だけに絞るルールを追記`）。ただし**この日エラーに当たったかどうかはユーザーに確認していない**
  - ⚠️ **X投稿には採らない。**理由は日付ではなく**角度の重複**：2026-06-08の43番「6/2のClaude障害、実は全く気が付きませんでした」が**63ビュー**で、同じ枠組みの再演になる（`knowledge/x/published.md`）。出すとしたら別の角度が要る

---

## [2026-08-24] 調査結果（定期リサーチ・12:00のフル版）

**本日の最重要は、Anthropicが公式の学習サイト「Claude Academy」を出していたこと（2026-08-20公開）。日本語で、無料で、Claude Code・Coworkの入門コースがある。**
**⚠️ この発見は「フル版はデイリーが見ていないチャネルを開く」というルール（`research/README.md` 2026-08-21）がそのまま効いた事例。**本日朝までのデイリー回は①側を6チャネル（changelog・@ClaudeDevs・Newsroom・Apps／Platformリリースノート・料金ページ）巡回して「4日間新しい発表なし」と閉じているが、**Claude Academyはそのどれにも載っていない**。Newsroomにも、Apps／Platformのリリースノートにも出ていない。**製品の変更でも事業のリリースでもない「学習リソースの公開」は、既存の巡回先の外に出る。**

### Claude Academy（本日の主収穫・デイリーの巡回先の外にあった）

- **【最重要】Anthropicの公式学習サイト「Claude Academy」が 2026-08-20 に公開された**（**本日CCがブラウザで [academy.claude.com](https://academy.claude.com/) を直接開いて確認**。公開日の出典は[gihyo.jp「Anthropic、AIの活用方法を学べる「Claude Academy」を公開」2026-08-20](https://gihyo.jp/article/2026/08/claude-academy)）
  - **日本語で表示される。**トップの見出し（verbatim）：`Claude Academy へようこそ` ／ `AIを探求している方、Claude を使い始めたばかりの方、チームへの導入を検討している方など、すべての方のためのリソースです。`
  - **製品別に5トラック**：Claude.ai ／ **Claude Cowork** ／ **Claude Code** ／ Claude Tag ／ Claude Platform。加えて **AI Fluency**（4Dフレームワーク：委任力・記述力・評価力・倫理的責任）
  - **Claude Codeトラックの中身**（[academy.claude.com/products/code](https://academy.claude.com/products/code)を直接確認）：入口は **「Claude Code 101」＝12レッスン＋クイズ1・所要1時間**。ほかに**チュートリアル11件・コース6件**。ドキュメントへの導線（CLAUDE.mdファイル／MCPサーバー／フック／サブエージェント／.claudeディレクトリ／コンテキストウィンドウの仕組み）も同じページに並ぶ
  - **サインインは任意**（ヘッダーに`サインイン`リンクはあるが、コース一覧・製品トラックは未ログインで閲覧できた）。gihyoは「コースやチュートリアルは無料で誰にでも公開」と記載
  - ⚠️ **コース総数は二次情報で割れている**（gihyo 22件／英語メディアは20件・26件）。**総数は書かない。**書くなら本日確認できた「Claude Code 101＝12レッスン・1時間」のような**トラック単位の実数**を使う
  - ⚠️ **Anthropic公式のアナウンス記事（Newsroom／ブログ）は本日時点で見つけられていない。**Newsroomは8/14の透かし記事から動いていない。**一次情報はサイト本体そのもの**として扱う
  - **使う側の何が変わるか**：これまで非エンジニアがClaude Codeを覚える経路は、公式ドキュメントか有志の記事しかなかった。**そこに、公式・無料・日本語・1時間の入門コースができた。**「Claude Codeは難しそう」という手前で止まっている人の入口が1段下がる
  - **このメディアへの意味**：no.14（Claude Codeとは何か・417表示でサイト1位）・no.24（初心者が最初に理解すべき用語）と**同じ読者層が行く先が公式にできた**。競合ではなく、**「公式講座を1時間受けたあと、実際に業務で回すとどうなるか」がこのメディアの持ち場**という線引きがはっきりする

- **【TOP10 #10に直結】Coworkトラックに「ユースケース72件」が部署別で公開されている**（[academy.claude.com/products/cowork](https://academy.claude.com/products/cowork)を本日直接確認）
  - **部署タブ**（verbatim）：`一般 / マーケティング / 製品 / エンジニアリング / 人事 / 財務 / オペレーション / データ / デザイン / 法務 / 営業 / リサーチ / 教育 / 個人`
  - 入口コースは**「Claude Cowork入門」＝14レッスン＋クイズ1・所要2.5時間**。ほかに**ユースケース72件・チュートリアル17件・コース1件**
  - マーケティング枠の具体例（verbatim）：`キャンペーンブリーフを作成する`（10分）／`ガイドラインに対してビジュアルアセットのフォルダを監査する`（15分・Opus 4.7が画像を**フル解像度で読み**、ブランドに合わない色・古いロゴ・不足している法的文言を見つける）
  - **no.58「Claude Coworkの使い方｜実際の9割は開発以外だった」の裏付けが、提供元の実データ（9割が開発以外）から公式の実例72件に増えた。**no.58は公開データの読み方で体験ゼロ、TOP10 #10は「実際に動かした記録」。**その間を埋める材料として、公式が想定している使い道の一覧が使える**
  - ⚠️ **72件は「Anthropicが想定している用途」であって、実測でも実績でもない。**記事に書くなら「公式が挙げている用途」と明示する

### Claude Code本体（デイリーの記録の再確認）

- **公式changelogは v2.1.241（2026-08-23）が最新のまま**（[公式changelog](https://code.claude.com/docs/en/changelog)を本日フル版でも確認）。本文は`Bug fixes and reliability improvements`の1行のみで、**3日連続で中身が公表されていない**。デイリー回の判断（X投稿に採らない）を維持する
- **Claude Platform リリースノートは 2026-08-20（Python SDK v1.0）が最新のまま**（[platform.claude.com](https://platform.claude.com/docs/en/release-notes/overview)を本日フル版で直接確認）。**8/19のGA8項目以降、新規なし**
- **Claude Apps リリースノートは 2026-08-06 のまま**（[support.claude.com](https://support.claude.com/en/articles/12138966-release-notes)・**18日連続で動きなし**）
- **Anthropic Newsroom は 2026-08-14（透かしの記事）から新規なし**（[anthropic.com/news](https://www.anthropic.com/news)を本日確認・**10日連続**）
  - ⚠️ **にもかかわらずClaude Academyは8/20に出ている。**「Newsroomが止まっている＝Anthropicが何も出していない」ではない。**巡回先の穴として記録する**
- **Mythos 5 が Claude Security の脆弱性スキャンに開放された（2026-08-21・Enterpriseプラン向け）**（[ITmedia AI+ 2026-08-22](https://www.itmedia.co.jp/aiplus/article/2608/22/2000000697/)）。⚠️ **X投稿には採らない**：Enterprise限定でこのメディアの読者の手元では何も変わらない

### 運用上の学び（`research/README.md`へ反映する）

**①の巡回先に「Claude Academy（academy.claude.com）」を足す。**理由は上記のとおり、**学習リソースの公開はリリースノートにもNewsroomにも載らない**ため。8/21のフル版が②について出した結論（「リリースノートは製品の変更しか載せない」）が、**①でも同じ形で起きた**。

---

## [2026-08-21] 調査結果（定期リサーチ・12:00の回）

**本日朝のデイリー回が拾った内容（Concise出力スタイル・v2.1.238・Platform GA）は一次情報で再確認し、重複しない差分だけを以下に足す。**
**フル版の役目どおり、デイリーが見ていないチャネル（Claude Platform リリースノート本体・Claude Apps リリースノート）を自分で開いた。結果、GAの中身がXの1文よりかなり広いことが分かった。**

### Claude Code本体

- **公式changelogに v2.1.238（2026-08-20）より新しい版はない**（[公式changelog](https://code.claude.com/docs/en/changelog)を12:00の回で直接確認）。本日朝のデイリー回の記録から進んでいない
- **朝の回が拾っていない、実務に効く1件（v2.1.236・2026-08-19）**（verbatim）：`Improved auto mode: the git status check can no longer be fooled by a repo's status.showUntrackedFiles=no setting into reporting a clean tree`。**auto modeが「作業ツリーはきれい」と誤認する経路が塞がれた**。auto modeを常用しているこのリポジトリには直接効く

### Claude Platform（デイリー回が見ていないチャネル・本日の主な収穫）

- **8/21早朝のGA告知（@ClaudeDevsの1文）の実体は、[Claude Platform リリースノート 2026-08-19](https://platform.claude.com/docs/en/release-notes/overview)の8項目だった。**朝の回はXの1文だけを見ていたため、以下は未記録だった（verbatim・要旨）
  - **Computer use tool がGA**：`computer_toolset_20260801`。**betaヘッダ不要・batch actions（1ターンで複数操作）・`zoom`が既定で有効・`configs`によるメンバー単位の設定**。旧beta版も引き続き利用可。既存実装の移行はリクエスト形状が変わる
  - **Browser use tool を新規ローンチ**：`browser_toolset_20260801`。**デスクトップ全体ではなくブラウザのビューポート内で動き、ページのアクセシビリティツリー・要素・フォーム・タブを読む**。要素参照・フォーム入力・タブ管理・ダウンロード報告・オプトインのファイルアップロードが、スクリーンショット＋クリック操作の上に乗る
  - 両toolsetの対象モデル：**Fable 5・Mythos 5・Opus 5・Sonnet 5・Opus 4.8**
  - **Files API がGA**：`files-api-2025-04-14`ヘッダ不要。**アップロード時に`expires_in_seconds`で有効期限を指定でき、fileオブジェクトが`expires_at`を返す**。一覧はページネーションと`ids[]`フィルタに対応
  - **Agent Skills と Skills API（`/v1/skills`）がGA**：`skills-2025-10-02`ヘッダ不要
  - **Admin API のユーザー管理エンドポイントが Claude Enterprise 向けにGA**（メンバー・招待・グループ・カスタムロール）
  - **Claude Managed Agents の`web_search`／`web_fetch`が到達できるサイトを制限できるようになった**：`agent_toolset_20260401`の`configs`に`allowed_domains`／`blocked_domains`を設定。`web_fetch`は`max_content_tokens`、`web_search`は`user_location`も受け付ける
  - **Console のセッションビューアが刷新**：タイムラインのミニマップ、モデルリクエスト単位のトランスクリプト、セッション詳細とコストのInspectorパネル
- **8/18：Console の「Workbench」が「Playground」に改称**（[同リリースノート](https://platform.claude.com/docs/en/release-notes/overview)・[platform.claude.com/playground](https://platform.claude.com/playground)）。Messages APIの全パラメータに対応し、コード実行・Web検索などのテンプレートを同梱。**実行ごとにSDKリクエストとAPIレスポンスの全文を表示する**
  - ⚠️ **このリポジトリには「レガシーWorkbenchは2026-08-17でアクセス終了」とだけ記録があった**（`research/trends.md`の7/27の回）。**終了と改称は別の出来事。混同して「Workbenchが終わった」とだけ書くと誤り**
- ⚠️ **X投稿には採らない（朝の回の判断を維持）**：対象がAPIを直接叩く開発者で、このメディアの読者（コンテンツ運用者・中小企業）の手元では何も変わらない

### Claude Apps（consumer側・本日確認）

- **[Claude Apps リリースノート](https://support.claude.com/en/articles/12138966-release-notes)の最新エントリは 2026-08-06 のまま**（Enterprise向けのskill・pluginセキュリティスキャンβ）。**8月に入ってから15日間、消費者向けアプリ側の公表更新は1件も出ていない**。Claude Code側の更新頻度との差が開いている

### Sonnet 5の価格

- **変化なし。**$2/$10が標準のまま（`research-20260813-01`／8/21朝のデイリー回から変化なし）

---

#### 【デイリー】2026-08-24

**差分なし（X投稿に採れる新情報はゼロ）。**巡回した6チャネルすべての確認結果を下に残す。**①側は8/21のRemote Controlスレッド以降、4日間新しい発表がない。**

- **Claude Code公式changelogに v2.1.241（2026-08-23）が出た**（[公式changelog](https://code.claude.com/docs/en/changelog)を本日確認）。前回記録の v2.1.240 から1つ進んだ
  - **本文は1行のみ**（verbatim）：`Bug fixes and reliability improvements`
  - ⚠️ **X投稿には採らない**：8/22の v2.1.240 と同じで中身が公表されておらず、使う側の何が変わったかを書けない。**2日連続で「Bug fixes」1行のみ**
- **「Claude Codeにセルフホスト環境が追加された」という検索要約を一次情報で否定した**（本日実際に起きた取り違え）。検索結果は8/22前後の新機能のように伝えていたが、公式changelogを開くと **v2.1.224（2026-08-07）** の項目だった（verbatim）：`Added self-hosted environments: claude self-hosted-runner turns your own machines or containers into a place Claude Code web, mobile, and desktop sessions can run, on Team and Enterprise plans`
  - **8/23に続いて2日連続で、二次情報の日付が公式とずれていた。**検索要約の日付は毎回changelog本体で突き合わせる
- **@ClaudeDevsのXに8/22〜8/24の投稿なし**（[x.com/ClaudeDevs](https://x.com/ClaudeDevs)を本日CCがブラウザで直接確認。WebFetchはx.comに402を返すため）。最新は8/21付のRemote Controlスレッド（消化先＝`queue.md`の`RC-01`・**本日8/24が鮮度期限の最終日**）
- **Anthropic Newsroom は 2026-08-14（透かしの記事）から新規なし**（[anthropic.com/news](https://www.anthropic.com/news)を本日確認。**10日連続で動きなし**）
- **Claude Apps リリースノートは 2026-08-06 のまま**（[support.claude.com](https://support.claude.com/en/articles/12138966-release-notes)・**18日連続で動きなし**）
- **Claude Platform リリースノートは 2026-08-20（Python SDK v1.0）が最新のまま**（[platform.claude.com](https://platform.claude.com/docs/en/release-notes/overview)を本日確認）。差分なし
- **Sonnet 5の価格は変化なし**（[公式Pricing docs](https://platform.claude.com/docs/en/about-claude/pricing)を本日確認）。表は`$2 / MTok`・`$10 / MTok`のまま。注記も残っている（verbatim）：`The $2/$10 per million input/output token pricing for Claude Sonnet 5, announced at launch as introductory pricing through August 31, 2026, is now the standard price. The previously scheduled increase to $3/$15 per million input/output tokens on September 1, 2026 will not occur.`
  - **9/1の値上げが撤回されたままであることを、本日も一次情報で確認した**（`research-20260813-01`の「9/1前後に『値上げされなかった日』として再利用可」の前提が生きている）
  - **本日、OpenAIがGPT-5.6 Solの従量課金を2割以上下げたことを確認した**（`research/ai-tools.md`の本日エントリ）。**同じ月に、Anthropicは値上げを撤回し、OpenAIは値下げした。**フロンティアモデルの単価が下がる方向で揃っている点は、9月以降の料金ネタの背景として使える

---

#### 【デイリー】2026-08-23

**差分なし（X投稿に採れる新情報はゼロ）。**日曜のため各チャネルとも動きが止まっている。巡回した5チャネルすべての確認結果を下に残す。

- **Claude Code公式changelogに v2.1.240（2026-08-22）が出た**（[公式changelog](https://code.claude.com/docs/en/changelog)を本日確認）。前回記録の v2.1.239 から1つ進んだ
  - **本文は1行のみ**（verbatim）：`Bug fixes and reliability improvements`
  - ⚠️ **X投稿には採らない**：中身が公表されておらず、使う側の何が変わったかを書けない
  - ⚠️ **二次情報の取り違えに注意（本日実際に起きた）**：検索結果の要約が「8/22に`ANTHROPIC_DEFAULT_MODEL`と`notify_when_idle`が追加された」と伝えていたが、[Releasebot](https://releasebot.io/updates/anthropic/claude-code)を直接開くと**この2件は8/18の v2.1.236 の項目**で、同サイトは版の日付を公式changelogより1日ずれた形で並べている。**公式changelogを開いて確認しなければ、この誤りをそのまま記録していた**
- **@ClaudeDevsのXに8/22・8/23の投稿なし**（[x.com/ClaudeDevs](https://x.com/ClaudeDevs)を本日CCがブラウザで直接確認。WebFetchはx.comに402を返すため）。最新は8/21付のRemote Controlスレッド（`research-20260822`で記録済み・**8/22の消化先＝`queue.md`の`RC-01`**）
- **Anthropic Newsroom は 2026-08-14（透かしの記事）から新規なし**（[anthropic.com/news](https://www.anthropic.com/news)を本日確認。**9日連続で動きなし**）
- **Claude Apps リリースノートは 2026-08-06 のまま**（[support.claude.com](https://support.claude.com/en/articles/12138966-release-notes)・**17日連続で動きなし**）
- **Claude Platform リリースノートは 2026-08-20（Python SDK v1.0）が最新のまま**（[platform.claude.com](https://platform.claude.com/docs/en/release-notes/overview)を本日確認）。差分なし
- **Sonnet 5の価格は変化なし**（[公式Pricing docs](https://platform.claude.com/docs/en/about-claude/pricing)を本日確認）。表は`$2 / MTok`・`$10 / MTok`のまま。注記も残っている（verbatim）：`The $2/$10 per million input/output token pricing for Claude Sonnet 5, announced at launch as introductory pricing through August 31, 2026, is now the standard price. The previously scheduled increase to $3/$15 per million input/output tokens on September 1, 2026 will not occur.`
  - **9/1の値上げが撤回されたままであることを、本日も一次情報で確認した**（`research-20260813-01`の「9/1前後に『値上げされなかった日』として再利用可」の前提が生きている）

---

#### 【デイリー】2026-08-22

**本日の最重要は、Remote Controlのアップデート。スマホから「続ける」だけだったのが、スマホから「新しく始める」ができるようになった。**@ClaudeDevsが日本時間7:44に出したスレッドで、本デイリー実行の約20分前。**8/21から追加した「@ClaudeDevsのXをブラウザで直接見る」手順が2日連続で効いている。**

- **【最重要】スマホからClaude Codeのセッションを新規に開始できるようになった**
  - **一次情報（公式X・[@ClaudeDevs 2026-08-22 7:44 JST](https://x.com/ClaudeDevs/status/2090933155847143498)のスレッド・本日CCがブラウザで原文を直接確認**。WebFetchはx.comに402を返すため）
  - スレッド冒頭（verbatim）：`Last month you told us Remote Control was the thing you'd most like us to fix, so we've been working hard on reliability.`
  - **新規開始（verbatim）**：`You can now start a Claude Code session directly from your phone.` ／ `Any machine running claude remote-control shows up as a device card at the top of the Code tab. Tap it, pick a directory, and it starts on that machine.`
  - **同期（verbatim）**：`Resuming a session on your laptop keeps the phone on the live session instead of archiving it. When Claude Code exits, your phone shows it offline within seconds instead of leaving a stale session hanging around`
  - **自動再接続（verbatim）**：`Dropped connections now recover on their own, so if you briefly close your laptop or switch wifi, it'll automatically reconnect.`
  - **モデル・effortの同期とスラッシュコマンド（verbatim）**：`Your phone and CLI sessions also stay in sync on model and effort level, and heavy sessions open much faster on iOS.` ／ `/clear resets the phone view` ／ `/compact shows a compaction marker` ／ `/diff opens the native diff sheet`
  - ⚠️ **公式ドキュメント側はまだ追いついていない。**[Remote Controlのdocs](https://code.claude.com/docs/en/remote-control)を本日確認したが、`device card`・`Code tab`から新規開始する記述は**まだ載っていない**（ページのタイトルは`Continue local sessions from any device with Remote Control`のまま＝「続ける」前提の記述）。**現時点の一次情報は公式Xのみ。**docsに反映されたら差し替える
  - **docsで確認できる前提条件（verbatim）**：`Subscription: available on Pro, Max, Team, and Enterprise plans. API keys are not supported. On Team and Enterprise, an Owner must first enable the Remote Control toggle`／PC側で`claude remote-control`を起動しておく必要がある（`The process stays running in your terminal in server mode, waiting for remote connections.`）
  - **使う側の何が変わるか**：これまでは「机で始めた作業をスマホで続ける」だけだった。**始める側がスマホに来た。**外出先で思いついた記事の直しに、机に戻らず着手できる。⚠️ ただしPCが起動していて`claude remote-control`が動いていることが条件なので、「スマホだけで完結する」ではない

- **Claude Code公式changelogに v2.1.239（2026-08-21）が出ていた**（[公式changelog](https://code.claude.com/docs/en/changelog)を本日確認）。前回記録の v2.1.238 から1つ進んだ。**中身はほぼ不具合修正で、X採用基準（使う側の何かが変わる）を満たす項目は少ない。**実務に関係しうるものだけ抜き出す（verbatim）
  - `The usage-limit message shown when your monthly spend limit is already used up now also says when your session or weekly limit resets`（上限で止まったときのメッセージに、次のリセット時刻が出るようになった）
  - `Fixed a race where pressing Esc with a prompt queued could let the next turn finish early, leaving the session idle while Claude was still working and letting a later resubmit repeat actions`（Escを押したのに裏で動き続け、後から同じ操作が繰り返される不具合）
  - `Improved the reminder shown after compaction so a skill's original arguments are not re-run as a new request`（圧縮後にスキルの引数が新しい依頼として再実行される問題）
  - `Windows: cross-session messaging is now available`（Windowsでもセッション間メッセージが使えるようになった。macOS・Linuxに追いついた）
  - ⚠️ **X投稿には採らない**：どれも「壊れていたものが直った」で、読者の仕事のやり方は変わらない

- **Anthropic Newsroom は 2026-08-14（透かしの記事）から新規なし**（[anthropic.com/news](https://www.anthropic.com/news)を本日ブラウザで確認）
- **Claude Apps リリースノートは 2026-08-06 のまま**（[support.claude.com](https://support.claude.com/en/articles/12138966-release-notes)・**16日連続で動きなし**。前回8/21の記録から1日伸びた）
- **Claude Platform リリースノートは 2026-08-20（Python SDK v1.0）が最新のまま**（[platform.claude.com](https://platform.claude.com/docs/en/release-notes/overview)を本日確認）。差分なし
- **Sonnet 5の価格は変化なし。**$2/$10が標準のまま（`research-20260813-01`から変化なし）
- **参考（新情報ではない・8/6発表の再確認）**：セルフホスト環境（[Self-hosted environments for Claude Code](https://claude.com/blog/run-claude-code-sessions-on-your-own-compute)）は**Team・Enterpriseプラン限定のpublic beta**。このメディアの読者（個人・中小企業）の手元では何も変わらないため**X投稿には採らない**

---

#### 【デイリー】2026-08-21

**本日の最重要は、Claude Codeに「Concise（簡潔）」という出力スタイルが標準搭載されたこと。設定ひとつでClaudeの答え方が結論先出しに変わる。同じ日に「指定した出力スタイルがセッション途中で既定の声に戻る」不具合も修正されている。**
**あわせて巡回手順を1つ変えた：8/20の自戒（巡回先が公式changelog・公式ヘルプ中心でXを見ておらず、公式Xだけの告知を2日連続で取りこぼした）を受け、本日から`@ClaudeDevs`のXをブラウザで直接見る手順を追加した。**その初日に、本日の最重要ネタがそのXで245万再生を集めていた。**巡回先を変えたその日に効いている。**

- **【最重要】Claude Codeに「Concise」出力スタイルが標準で入った。設定ひとつで、前置きと実況をやめて結論から書く答え方に変わる**
  - **一次情報①（公式X・verbatim）**：[@ClaudeDevs](https://x.com/ClaudeDevs/status/2090245922685063634) — `You can now set Claude Code's output style to Concise.` ／ `Claude leads with the result, keeps responses short, and still gives full detail when you ask.` ／ `Turn it on in /config → Output style, or set "outputStyle": "Concise" in settings.json.`
  - **一次情報②（公式changelog v2.1.237・2026-08-20・verbatim）**：`Added a built-in "Concise" output style: Claude leads with results and skips preamble and narration, while doing the work just as thoroughly. Select it under Output style in /config.`
  - **本日CCがブラウザでX上の原文を直接確認済み**（WebFetchはx.comに402を返すため）。表示は**245万再生・846リプライ・1.8万いいね**。投稿の表示は8/21 8:10 JST時点で「21h」＝**日本時間8/20の昼ごろ**
  - **使う側の何が変わるか**：`/config`の Output style で選ぶか、`settings.json`に`"outputStyle": "Concise"`と書くだけで、**Claude Codeの答え方そのものが変わる**。長い前置き・作業の実況に付き合わされていた人は、その画面が変わる。**プロンプトで毎回「短く」と頼む必要がなくなる**
  - ⚠️ **「短くなる＝手を抜く」と読ませない。**公式Xは`still gives full detail when you ask`、changelogは`while doing the work just as thoroughly`と、**作業量は落とさないことを両方で明記している**。変わるのは報告の仕方であって仕事の中身ではない
  - ⚠️ **245万再生・846リプライという反応の大きさは「長さに困っていた人が多かった」の裏付けに使えるが、他人の不満をなぞる形にしない**（`research-20260817-01`と同じ注意）
  - ⚠️ **手元はv2.1.233でこの機能自体がまだ入っていない**（8/21朝に`claude --version`で確認）。`~/.claude/output-styles/`も`.claude/output-styles/`も存在せず、settings.jsonに`outputStyle`の指定も無い。**実機で選んで挙動を見てから書く**

- **同じ日に、出力スタイルが途中で外れる不具合も直っている**（[公式changelog](https://code.claude.com/docs/en/changelog) v2.1.238・2026-08-20・verbatim）：`Fixed custom, project, and plugin output styles drifting back to the default voice mid-session`
  - **つまり、出力スタイルを指定していても、セッションの途中で既定の声に戻ることが実際に起きていた。**「最初は言うとおりに書いていたのに、途中から元に戻る」を経験していた人には、原因が公式に名指しされた形になる
  - ⚠️ **この`output styles`は`/config`の出力スタイル機能のことで、CLAUDE.mdに書いた文体ルールとは別物。**混同して「CLAUDE.mdの指示が途中で外れる不具合が直った」と書いたら誤り

- **v2.1.238（2026-08-20）のその他**（[公式changelog](https://code.claude.com/docs/en/changelog)・verbatim）
  - `Fixed unbounded memory growth in long interactive sessions: subagent tool results are now released once they leave the recent display window` — **長時間セッションのメモリが際限なく増えていた**。サブエージェントを多用する運用（このリポジトリの自動リサーチが該当）には効く
  - `Changed Ctrl+L and Cmd+K in fullscreen to always just repaint — the double-press /clear shortcut was removed` — **Ctrl+L・Cmd+Kの2回押しで`/clear`が走る挙動が廃止**。画面を消すつもりが会話ごと消える事故が減る
  - `Added a keybindingFlavor setting: set it to "readline" to make Ctrl+W in the prompt delete back to the previous whitespace, as in Bash; the default ("classic") is unchanged`
  - `Improved startup: bare claude starts sooner on macOS` ／ `Improved startup responsiveness: the automatic update check now runs about 10 seconds after launch instead of competing with startup for CPU`
  - ⚠️ **X投稿には採らない**：残りはプラグインの`headersHelper`・self-hosted runner・Remote Control・MCPの修正が大半で、効く層がこのメディアの読者とずれる

- **Claude PlatformでComputer use・browser tool・Skills API・Files APIが一般提供（GA）に**（[@ClaudeDevs](https://x.com/ClaudeDevs/status/2090540270219567575)・8/21 8:10 JST時点でX表示「2h」＝**本日8/21の早朝**・verbatim）：`Computer use, the browser tool, the Skills API, and the Files API are now generally available on the Claude Platform.` ／ `Automate work in applications that have no API with fewer round trips per task, and build Claude Managed Agents on versioned skills and reusable files.`
  - ⚠️ **X投稿には採らない**：対象がAPIを直接叩く開発者で、このメディアの読者（コンテンツ運用者・中小企業）の手元では何も変わらない。**「新機能が出た報告だけ」に該当する**

- **Sonnet 5の価格：本日も公式は「$2/$10が標準」のまま**（[公式Pricing docs](https://platform.claude.com/docs/en/about-claude/pricing)）。9/1の$3/$15への値上げは撤回済みの状態が継続（`research-20260813-01`・8/20の記録から変化なし）

---

#### 【デイリー】2026-08-20

**本日の収穫は1件で、しかもこのリポジトリが6日間追いかけていた件の決着。週次上限+50%は4回目の延長に入り、8/31まで続く。加えてAnthropicが初めて「恒久化したい」と書いた。**
**あわせて自戒：この告知は昨日8/19の4:35（X表示・JST）に出ている。昨日のデイリー実行（8:00）の3時間半前だったのに拾えなかった。8/19の透かし1週間遅れに続いて2日連続の取りこぼし。原因は巡回先が公式changelog・公式ヘルプ中心で、Xを見ていないこと。この件の告知チャネルは公式Xだけだった。**

- **【最重要】Claude Codeの週次使用上限+50%が4回目の延長。8/31まで。初めて「恒久化したい」と明言された**
  - **一次情報（公式X・verbatim）**：[@ClaudeDevs, 2026-08-19 4:35（X表示・JST）](https://x.com/ClaudeDevs/status/2089798442306711646) — `We're extending the 50% increase to weekly Claude Code limits through August 31. We hope to make this a permanent change to our plans, but strong demand for our models means that capacity may be tight over the coming weeks. We'll keep you posted as things develop.`
  - **本日CCがブラウザでX上の原文を直接確認済み**（WebFetchはx.comに402を返すため。表示は317.6万再生・1,333リプライ）。この投稿は7/18の投稿（`We're also keeping Claude Code weekly limits 50% higher, now through August 19, for all Pro, Max, Team, and seat-based Enterprise users.`）の引用ポストになっている
  - ⚠️ **JSTとPTの差に注意**：X表示は2026-08-19 4:35（JST）で、これは**2026-08-18 12:35 PT**にあたる。リプライに8月18日付が並んでいるのはこのため。「8/19に発表」と書くと現地時間では前日になる。**日付を書くなら『日本時間8/19未明』と書く**
  - **使う側の何が変わるか**：8/19の23:59 PTで標準に戻る前提で1週間の作業量を組んでいた人は、**8/31まで1.5倍のまま**。かつ「一時的な施策」から「恒久化の候補」に格が上がった
  - ⚠️ **同時に釘も刺されている**：`capacity may be tight over the coming weeks`。恒久化は希望であって確定ではない。**「恒久化された」と書いたら誤り**
  - ⚠️ **[公式ヘルプ](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)には本日も週次上限の期間・+50%施策・8/19・8/31のいずれも記載が無い**（8/14・8/18・8/19に続き4回目の確認・結果は同じ）。**告知チャネルは公式Xのみという状態が続いている**
  - **このリポジトリにとっての意味**：`research-20260814-02`で「4回目の延長もありうるため8/19に戻ると断定して書かない」「期限前・確認前には出さない」と3回にわたって判断を据え置いた。**その翌日に4回目の延長が来た。**期限当日の8/19に「今日で戻ります」と投稿していたら、翌日には外れていた。**予告を事実として書かなかったから助かった、という実話が日付つきで手元に残っている**（前例：`research-20260813-01`のSonnet 5値上げ予告の撤回）

- **Claude Code v2.1.236（2026-08-19）が出ている**（[公式changelog](https://code.claude.com/docs/en/changelog)）。**既定の挙動が変わる項目は無いが、auto mode関連の変更が3件入っている**
  - **`ANTHROPIC_DEFAULT_MODEL`環境変数の追加**（verbatim）：`sets the model new sessions start on, while a /model pick still overrides it and persists across restarts (unlike ANTHROPIC_MODEL)`。新規セッションの開始モデルを指定できる。`ANTHROPIC_MODEL`と違い`/model`での選択が優先される
  - **auto modeの変更3件**（verbatim）：`Monitor allow rules are now set aside while auto mode is active, so Monitor commands are reviewed the same way Bash commands are` ／ `Improved auto mode on Bedrock, Vertex AI, and Foundry, and when telemetry is disabled: the classifier now uses the same defaults as on the Claude API, including severity-scored classification` ／ `the git status check can no longer be fooled by a repo's status.showUntrackedFiles=no setting into reporting a clean tree`
  - **サンドボックスの穴が塞がれた（macOS・verbatim）**：`wildcard read-deny rules (e.g. **/.env) now take precedence inside allowed read regions, cover matched directories' contents, and can't be bypassed by renaming the denied file`。**`.env`をdenyしていても、ファイル名を変えれば読めていた**。⚠️ **X投稿には採らない**：効くのはサンドボックスのdenyルールを自分で書いている層に限られ、このメディアの読者層とずれる
  - その他：`/usage`にTeam・Enterpriseの使用クレジット消費行を追加／`/goal`が長時間のバックグラウンド作業待ちで30分後（次に1h・2h）に自動チェックイン／`SendMessage`に`notify_when_idle`（同一マシンの他セッションがidleになったとき1回だけ通知・macOSとLinux）／スラッシュコマンドの打ち間違いで一番近い候補を勝手に実行せずエラーを返すように変更

- **Sonnet 5の価格：検索要約がいまだに撤回前の情報を流している。公式は本日も「$2/$10が標準」のまま**
  - 本日の検索要約は`Claude Sonnet 5's promotional pricing of $2/$10 per million tokens ends August 31, 2026, with standard pricing of $3/$15 taking effect September 1`と出してきたが、**[公式Pricing docs](https://platform.claude.com/docs/en/about-claude/pricing)を本日取得すると本文は逆**（verbatim）：`The $2/$10 per million input/output token pricing for Claude Sonnet 5, announced at launch as introductory pricing through August 31, 2026, is now the standard price. The previously scheduled increase to $3/$15 per million input/output tokens on September 1, 2026 will not occur.`
  - 表の実値も **Claude Sonnet 5：入力$2/MTok・出力$10/MTok** のまま
  - **`research-20260813-01`の補強材料**：撤回から1週間が経っても、検索要約は撤回前の予告を現在形で返してくる。**「二次情報は撤回に追いつかない」の実例が、今日また1つ増えた**

---

#### 【デイリー】2026-08-19

**本日の収穫は1件で、しかも大きい。Claudeが出力した文章そのものに、目に見えない透かしが入る。Claude Codeも対象に明記されている。このメディアはClaude Codeで記事を書いているので、直撃する側の変更。**
**あわせて自戒：この発表は8/11に報道が出て、8/14に公式ブログが出ている。デイリーを毎日回していながら1週間拾えていなかった。**

- **【最重要】Claudeの出力テキストに機械可読な透かし（watermark）が入る。対象にClaude Codeが明記されている**
  - **対象サーフェス（公式ヘルプ・verbatim）**：[How Claude marks AI-generated content, support.claude.com](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content) — `Claude markings cover output from supported models everywhere you use Claude, including Claude Platform (API), Claude, Claude Code, Claude Cowork, and Claude Tag.`
  - **対象モデルと時期（公式ヘルプ・verbatim）**：`Claude models launched in the EU on or after August 2, 2026 will support machine-readable marking at launch.` ／ 旧モデルについては `We're also working to add marking support to Claude models released before that date`
  - **仕組み（公式ブログ 2026-08-14）**：[How Claude's text watermarking works, anthropic.com](https://www.anthropic.com/news/claude-text-watermark) — `Future Claude models will generate text that contains a watermark.` 文中に何かを埋め込むのではなく、**次の単語を選ぶときの乱数の出どころを変える**方式（Google DeepMindがNature論文で公開したSynthID-Textの応用）
  - **編集しても消えない（公式ブログ・verbatim）**：`Light editing probably won't remove the watermark completely; a complete rewrite where every word is replaced will.` **軽く直したくらいでは残る。全単語を書き換える全面リライトで消える**
  - **コードは扱いが違う（公式ブログ・verbatim）**：`code—which in very many cases has to be exact—has generally less watermarking than some other forms of text`。正確さが要るコードは透かしが薄い
  - **検出は未提供**：公式ブログは `We will soon be offering a watermark detection API. We're in the process of working out the details of its implementation.`、公式ヘルプは `We'll share details on detection mechanisms in forthcoming technical documentation.`。**検出APIも検出ツールもまだ出ていない**
  - **背景**：EU AI Act第50条の透明性義務。ただし**適用はEU限定ではなく、Claudeが提供されている全世界**（公式ヘルプの記載どおり、EUで8/2以降にローンチするモデルが起点）
  - ⚠️ **「supported models」の具体的なモデル名一覧は公式に出ていない。**手元で使っているOpus 5・Sonnet 5・Fable 5のどれが対象かは公式に確認できない。**「いま自分が書いた文章に透かしが入っている」と断定して書かない**
  - ⚠️ **オプトアウトの記載は公式2ページのいずれにも無い。**ただし「オプトアウトできない」と公式が明言しているわけでもない。**「拒否できない」と断定しない**
  - ⚠️ **煽らない。**検出APIが出ていない以上、いま「AIで書いたことがバレる」と書くのは実態より先走り。**書くとしたら「消しても消えない前提で、AIで書くことをどう扱うか」まで**
  - ⚠️ 二次情報には「8/2から適用」「C2PAでファイルにも署名」といった書き方が混ざるが、**公式ヘルプが日付を紐づけているのは『EUで8/2以降にローンチするモデル』であって『8/2から全出力に適用』ではない**。ここを混ぜない

- **Claude Code v2.1.235（2026-08-18）が出ている**（[公式changelog](https://code.claude.com/docs/en/changelog)）。**使う側の既定が変わる項目は無い。**追加は`spellcheck`設定（プロンプト入力の誤字にアンダーラインを引く／ローカルのaspell・hunspell・ispellを使う・任意）1件のみで、残りは不具合修正と改善。**X投稿には採らない**
  - 記録のみ：`/ultrareview`等のクラウドセッション実行中のメモリ・CPU改善、権限ダイアログの表示範囲と「don't ask again」の一致、`ctrl+t`のタスク一覧が再開時に畳まれる不具合の修正

- **週次使用上限+50%の延長は、本日8/19（23:59 PT）で切れる予定のまま動いていない**
  - **本日あらためて[公式ヘルプ](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)を取得したが、週次上限の期間・+50%施策・8/19という日付のいずれも本文に無い**（8/14・8/18に続き3回目の確認・結果は同じ）
  - **4回目の延長のアナウンスも、終了のアナウンスも公式チャネルに出ていない**。二次情報（[aicatchup.com](https://aicatchup.com/news/claude-code-weekly-limits-50-percent-promo)等）は「サポート記事に8/19 23:59 PTまでと書かれている」としているが、**本日時点の公式ヘルプ本文では確認できない**
  - **判断：`research-20260814-02`の方針どおり、実機で自分のアカウントの週次上限がどうなったかを見てから出す。**期限前・確認前には出さない

---

#### 【デイリー】2026-08-18

**8/17の回・同日12:00のフル回はどちらも「最新版はv2.1.233のまま」と記録したが、それは誤り。v2.1.234が8/17付で出ている。しかも中身に、使う側の既定の挙動が変わる項目が入っていた。**

- **【8/17の記録を訂正】Claude Code v2.1.234（2026-08-17）が出ている**（[公式changelog, code.claude.com](https://code.claude.com/docs/en/changelog)）。8/17は8:00のデイリー回・12:00のフル回の両方で「最新5バージョンを読み直してv2.1.233が最新」と記録したが、**同日中にv2.1.234が公開されている**。**日中に出たリリースを翌日拾う運びになっており、8/13のv2.1.232を8/14に拾ったときと同じ取りこぼし方をしている**
- **【本日の収穫・使う側の既定が変わる】上限で止まったセッションの自動再開が、Claude Code本体に入った。しかも「オフにする」側の書き方になっている**
  - 原文（verbatim・v2.1.234）：`Claude Code now continues your session automatically when a claude.ai usage limit resets; turn it off in /config ("Continue automatically at usage limit")`
  - **8/17の記録（`research-20260817-01`）からの変化が2点ある**
    1. **対象**：8/14の[@ClaudeDevsのX投稿](https://x.com/ClaudeDevs/status/2088014831605702937)は`Claude Code desktop`限定の書き方だったが、**changelogの本文にdesktopという限定が無い**。Claude Code本体の変更として書かれている
    2. **既定**：X投稿は`Turn it on`（自分でオンにするチェックボックス）だったが、**changelogは`turn it off in /config`**。**オフにする手順しか書かれていない＝既定でオンと読める**
  - ⚠️ **「既定でオン」は文面からの読み取りであって、実機で確認できていない。**手元のClaude Codeは**v2.1.233**（本日確認）で、この項目自体がまだ入っていない。**投稿する前に更新して`/config`の「Continue automatically at usage limit」の初期値を自分の目で見る**
  - ⚠️ **上限そのものは1ミリも増えていない。**リセットを待つ時間は変わらない。変わるのは「リセット後に人が打ち直すかどうか」だけ
- **v2.1.234のその他（記録のみ・X投稿には採らない）**
  - `/permissions`が作業中でも開けるようになり、ルール変更がそのターンの残りから効く
  - 組み込みskill`claude-api`の読み込みコストが**約200k+トークン→約25k**に（参照ドキュメントを必要時ロードに変更）
  - auto modeが全Agentツール呼び出しの下に出していた`Allowed by auto mode classifier`の行を削除
  - `/config`から「Default teammate model」を削除。エージェントチームのteammateはリーダーのモデルを使う
  - セキュリティ：リモートのファイル読み込み・セッション復元・CLAUDE.mdのinclude・ワークフロースクリプト・ファイルアップロードがWindows NT名前空間（`\??\`）のパスを拒否するようになった（NTLM資格情報リークの残り経路を塞ぐ）
- **Anthropic本体：新しい料金・モデル・提供範囲の変更なし**（[公式リリースノート, support.claude.com](https://support.claude.com/en/articles/12138966-release-notes)を確認。**最新エントリは8/6の「スキル・プラグインのセキュリティスキャン（β・Enterprise向け）」のままで、12日間エントリが増えていない**）

### 週次使用制限+50%の8/19期限（本日が予告どおりの再確認日・結論：新情報なし）

- **8/14・8/15・8/17の記録どおり、公式チャネルには本日時点でも一切の記載がない。**[Pro/Maxプランでのclaude code利用の公式ヘルプ](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)を本日あらためて取得したが、**週次上限の期間・+50%施策・8/19という日付のいずれも本文に無い**
- **4回目の延長のアナウンスも、終了のアナウンスも出ていない。**検索で出てくるのは依然として[@ClaudeDevs（2026-07-18）](https://x.com/ClaudeDevs/status/2078511173759324328)の`We're also keeping Claude Code weekly limits 50% higher, now through August 19, for all Pro, Max, Team, and seat-based Enterprise users.`と、それを引用した二次情報（[@TestingCatalog](https://x.com/testingcatalog/status/2078529470894330026)／[note.com/zephel01](https://note.com/zephel01/n/nb7d668ade5b5)／[explainx.ai](https://www.explainx.ai/blog/claude-usage-limits-2026-timeline-explained)等）のみ
- **判断**：**期限は明日（8/19）。「8/19で戻る」と断定して書ける材料は最後まで揃わなかった。**5月13日開始・3回延長という経緯があるため4回目もありうる。**投稿するなら、8/19以降に自分のアカウントの週次上限が実際にどうなったかを見てから出す。**予告を事実として書いて撤回された前例が、このリポジトリには既に1件ある（`research-20260813-01`のSonnet 5値上げ予告）

---

## [2026-08-17] 調査結果（定期リサーチ・12:00の回）

**本日8:00のデイリー回の結論（差分なし）を、一次ソースを自分で開いて再確認した。結果は一致。この領域に新しい差分はない。**

### Claude Code本体

- **最新版はv2.1.233（2026-08-14）のまま。8/15〜8/17に新しいリリースは出ていない**（[公式changelog, code.claude.com](https://code.claude.com/docs/en/changelog)の**最新5バージョン分の全項目を読み直して確認**。最新から順にv2.1.233・v2.1.232・v2.1.231・v2.1.229・v2.1.228で、8/14以降のエントリはゼロ）
  - v2.1.233の全項目を読み直したが、**既に記録済みの4点（Taskツールの既定オフ／Windowsのauto modeリグレッション修正／デスクトップの通知フック修正／Bashパーミッションの一部差し戻し）以外に、使う側の挙動が変わる項目はなかった**。残りはGitLab MR対応・apps gateway・self-hosted runner・スクリーンリーダー対応など、対象が限られる改善
- **Week 33（8/10〜8/14）のダイジェストは本日も404**：`/docs/en/whats-new/2026-w33`はHTTP 404。8/15・8/17（デイリー）に続き**3回連続で404**。この週のダイジェストは存在しないと見てよい

### Anthropic本体

- **新しい料金・モデル・提供範囲の変更なし**（[公式リリースノート, support.claude.com](https://support.claude.com/en/articles/12138966-release-notes)を確認）。**最新エントリは8/6の「スキル・プラグインのセキュリティスキャン（β・Enterprise向け）」のままで、11日間エントリが増えていない**

### 週次使用制限+50%の8/19期限（残り2日・要再確認）

- **公式サポート記事には、本日時点でも+50%施策そのものの記載がない**（[Pro/Maxプランでのclaude code利用, support.claude.com](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)を直接取得して本文を確認。**週次上限に関する記述も、8/19という日付も無い**）
- ⚠️ **検索結果には「サポート文書が8/19 23:59 PT までと記載している」とする要約が出てくるが、実際にそのページを開いても該当記述は無かった。**この要約を根拠にしない
- 裏付けは依然として**@ClaudeDevsのX投稿**（[2026-07-18, x.com](https://x.com/ClaudeDevs/status/2078511173759324328)・原文`We're also keeping Claude Code weekly limits 50% higher, now through August 19, for all Pro, Max, Team, and seat-based Enterprise users.`）と、それを引用した二次情報（[note.com/zephel01](https://note.com/zephel01/n/nb7d668ade5b5)等）のみ
- **対象範囲（二次情報の整理・投稿時は要注意）**：Pro／Max／Team／シート課金のEnterpriseが対象で、**Freeと従量課金のEnterpriseシートは対象外**。上がるのは**週次上限だけで、5時間の短期上限は変わらない**。適用は自動
- **再確認は予定どおり8/18（明日）に行う。**4回目の延長もありうるため「8/19に戻る」と断定して書かない

---

#### 【デイリー】2026-08-17

**Claude Code本体・Anthropic本体ともに新しいリリースはなし。ただし8/16の回で「未確認の噂」として保留した1件が、一次情報で確認できたので訂正する。**

- **【8/16の記録を訂正／一次確認済み】「上限で止まったセッションを、枠のリセット後に自動で再開するチェックボックス」は実在した**
  - 出典：**Anthropic公式の開発者向けアカウント[@ClaudeDevs のX投稿（2026-08-14 6:28）](https://x.com/ClaudeDevs/status/2088014831605702937)**。8/16の回はWebFetchが読めず二次情報しか取れなかったが、本日**ブラウザで投稿本文を直接開いて確認した**
  - 原文（verbatim）：`Hit your usage limit in Claude Code desktop? There's now an auto-continue checkbox. Turn it on, and it'll automatically continue where you left off once your limit resets.`
  - **条件・除外まで確認した点**：原文が指しているのは **Claude Code の「desktop」** で、CLIについては言及がない。**オプトイン**（チェックボックスを自分でオンにする）。**上限そのものは増えていない**——リセットを待つ時間は変わらず、リセット後に自分で打ち直す手間だけが消える
  - ⚠️ **公式changelog・公式リリースノートのどちらにも記載がない**（本日あらためて両方を確認）。**告知チャネルはこのX投稿だけ**。「changelogに載った」「正式リリースされた」と書かない
  - 参考：この投稿は**132.8万再生・1,013リプライ**まで伸びており、リプライの上位は「そもそも上限を上げてほしい」という反応で占められている。**ただし他人の不満をなぞる形で使うと煽りになるので、投稿に使うなら自分の運用にどう効くかまで書く**
- **Claude Codeの最新版はv2.1.233（2026-08-14）のまま**。8/15〜8/17に新しいリリースは出ていない（[公式changelog, code.claude.com](https://code.claude.com/docs/en/changelog)で最新5バージョンの本文を確認）
- **Anthropic本体：新しい料金・モデル・提供範囲の変更なし**（[公式リリースノート, support.claude.com](https://support.claude.com/en/articles/12138966-release-notes)を確認。最新エントリは**8/6の「スキル・プラグインのセキュリティスキャン（β・Enterprise向け）」のまま**で、11日間エントリが増えていない）
- **Week 33（8/10〜8/14）のダイジェストは本日も404**：`/docs/en/whats-new/2026-w33`はHTTP 404。8/15は404、8/16はタイムアウトで判定不能だったが、**本日は明確に404を返した**。この週のダイジェストは現時点で存在しない
- **週次使用制限+50%の8/19期限：本日も公式記載なし**。あらためて[Pro/Maxプランでのclaude code利用の公式ヘルプ](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)を確認したが、**+50%施策そのものへの言及が無い**状態が続いている。裏付けは依然として@ClaudeDevs・@TestingCatalogのX投稿を引用した二次情報のみ。**再確認は予定どおり8/18に行う**

---

#### 【デイリー】2026-08-16

**Claude Code・Anthropic本体ともに、使う側の挙動が変わる新しい差分はなし（日曜）。**

- **Claude Codeの最新版は依然としてv2.1.233（2026-08-14）**。8/15〜8/16に新しいリリースは出ていない（[公式changelog, code.claude.com](https://code.claude.com/docs/en/changelog)を**ブラウザで直接開いて本文検索し確認**）
- **Anthropic本体：新しい料金・モデル・提供範囲の変更なし**（[公式リリースノート, support.claude.com](https://support.claude.com/en/articles/12138966-release-notes)を確認。最新エントリは**8/6の「スキル・プラグインのセキュリティスキャン（β・Enterprise向け）」のまま**で、8/14以降のエントリはゼロ）
- **⚠️【未確認の噂・投稿に使わない】「8/14にClaude Codeデスクトップへ、使用量上限で止まったセッションを枠のリセット後に自動再開するチェックボックスが入った」という記述が、検索結果の二次情報（releasebot系のまとめ）に出てくる**
  - **一次確認を試みた結果、裏が取れなかった**：公式changelogの本文を全文検索したところ、`auto-continue`のヒットは**2026-07-03のv2.1.200にある`AskUserQuestion`ダイアログの自動継続を既定オフにした、という別項目1件のみ**。v2.1.233・v2.1.232の項目にも該当する記述はない。Anthropic公式リリースノートにも記載なし
  - 内容としては「上限で止まった作業が自動で再開する」＝使う側に効く変更なので、**事実なら軸②になりうる**。ただし**現時点では出典が二次情報のみ**。ideas.mdには入れない。デスクトップアプリ側の別チャネルで告知された可能性があるため、次回以降に再確認する
- **⚠️同じ検索結果に出てきた以下は、いずれも日付が特定できず、かつ対象がEnterprise／Team向けで、このメディアの読者（個人・中小企業）の使い方は変わらない。記録のみで投稿候補にしない**
  - Compliance APIのCowork・Claude Codeへの拡張（Enterprise β）
  - Claude Codeのセルフホスト環境（公開β・Team／Enterprise）
  - Claude for Government（β）
- **週次使用制限+50%の8/19期限：本日も新情報なし**（公式サポート記事に+50%施策そのものの記載がない状態が続いている）。**再確認は予定どおり8/18に行う**
- **Week 33（8/10〜8/14）のダイジェストは本日確認できず**：`/docs/en/whats-new/2026-w33`はWebFetchがタイムアウトした。8/15時点では404だった。**「公開された」とも「まだ無い」とも書けない状態**なので、次回に持ち越す

---

#### 【デイリー】2026-08-15

- **【重要・既定変更】Claude Code v2.1.233（2026-08-14）で、Task／Todo系ツールが新しめのモデルでは既定で使えなくなった**（[公式changelog, code.claude.com](https://code.claude.com/docs/en/changelog)）
  - 原文（verbatim）：`Todo/task-tracking tools (TaskCreate/Get/Update/List, TodoWrite) are no longer available on Opus 4.8, Sonnet 5, Fable 5, Mythos 5, and newer models; set CLAUDE_CODE_ENABLE_TODO_TOOLS=1 to bring them back`
  - **条件・除外まで確認した点**：対象は**Opus 4.8・Sonnet 5・Fable 5・Mythos 5、およびそれ以降のモデル**。古いモデルでは従来どおり使える。戻す手段は環境変数`CLAUDE_CODE_ENABLE_TODO_TOOLS=1`
  - 経緯：TodoWriteは2026-05に`TaskCreate`／`TaskUpdate`／`TaskGet`／`TaskList`の4ツールへ分割済み。今回は**その後継のTaskツールごと既定から外れた**形
  - ⚠️ **自分の環境ではまだ消えていない（2026-08-15 08時・実機確認）**：手元の`claude --version`は**2.1.233**、`~/.claude/settings.json`・プロジェクト設定・環境変数のいずれにも`CLAUDE_CODE_ENABLE_TODO_TOOLS`／`CLAUDE_CODE_ENABLE_TASKS`は入っていない。それでも**本日のOpus 5セッションではTaskCreate等が提示された**。changelogの記述とローカルの挙動が一致していない。**「タスクリストが消えた」と断定して書かない**
  - ⚠️ `CLAUDE_CODE_ENABLE_TODO_TOOLS`は**settingsドキュメント（[code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings)）には未掲載**（8/15確認）。出典はchangelogの1行のみ
  - **軸②のX投稿ネタとして採用（→ ideas.md）**。8/13のサブエージェントfork既定オン・8/14のauto mode既定化と合わせて、**2日で「何も設定していない人の画面」が3回変わっている**という角度で書ける
- **v2.1.233のその他の変更**（同changelog）
  - **Windows：auto modeが`cd <dir> && <command> > file`のような普通のBashコマンドで繰り返し手動承認を求めるv2.1.232のリグレッションを修正**。auto mode既定化の当日にauto mode側の不具合が直っている
  - **Claude DesktopまたはVS Code配下で、許可プロンプト時にNotificationフックが発火しない不具合を修正**
  - v2.1.232で入れたBashパーミッション変更のうち、**Windowsのcygwin形式シンボリックリンクと入力リダイレクト（`< file`）の扱いは差し戻し**。「より狭い版を後のリリースで再投入する」と明記
  - `CLAUDE_CODE_WEBFETCH_CACHE_TTL_MS`追加（WebFetchのURLキャッシュTTL設定・既定15分は据え置き）／Linuxで`CLAUDE_CODE_TOOL_MEMORY_LIMIT`によるBashコマンドのメモリcgroup上限／`--worktree`と`claude agents`ビューがGitLabのマージリクエストURLに対応
  - 使う側の挙動が変わるのは上のWindows auto modeとデスクトップの通知フックの2点。**単独ではX投稿ネタにならない。記録のみ**
- **Week 33（8/10〜8/14）のダイジェストは8/15時点でも未公開**（`/docs/en/whats-new/2026-w33`は404のまま）。最新は**Week 32**
- **Anthropic本体：8/14〜8/15に新しい料金・モデル・提供範囲の変更はなし**（[公式リリースノート, support.claude.com](https://support.claude.com/en/articles/12138966-release-notes)を確認。最新エントリは8/6の「スキル・プラグインのセキュリティスキャン（β・Enterprise向け）」のまま）
  - ⚠️ **検索結果には「Sonnet 5の$2/$10は8/31まで、9/1から$3/$15」と書く二次情報がまだ複数残っている**（releasebot等）。これは**8/11に撤回済みで誤り**（8/13記録・公式Pricing docsで確認済み）。今後もこの誤情報を拾わない
- **週次使用制限+50%の8/19期限は本日も新情報なし**。再確認は予定どおり**8/18**に行う

---

## [2026-08-14] 調査結果（定期リサーチ・12:00の回）

### Claude Code / Anthropic

同日8:00のデイリー回（下記）で①②は調査済みのため、**8:00以降に確認できた差分と、デイリー回で拾えていなかった項目のみ**を記録する。

- **【デイリー回の記録漏れ・訂正】Claude Code v2.1.232（2026-08-13）が出ている**（[公式changelog, code.claude.com](https://code.claude.com/docs/en/changelog)）。本日8:00の回は「v2.1.231（8/13）が最新」と記録したが、**同じ8/13付でv2.1.232が出ており、こちらには挙動が変わる変更が複数含まれている**。v2.1.231はMCPのOAuth修正1件だけの小さいリリースで、実質的な中身はv2.1.232のほうにあった
  - **サブエージェントのforkが既定でオンになった**：`subagent_type: "fork"`のサブエージェントが会話全体とプロンプトキャッシュを引き継ぐようになり、**対話セッションでのエージェント起動が既定でバックグラウンド実行になった**（teammate以外）
  - **プロンプトで`@`を打つと他のClaude Codeセッションを名前で呼べる**：指定するとClaudeが`SendMessage`でそのセッションに直接届ける。あわせて、同じマシン上の対話セッションは名前が重複しないよう自動で`name-word-word`の変種が割り当てられる
  - **`/config`に行が2つ増えた**：「Dialog expiry」と「Messages from your other sessions」（他セッションからの受信をaccept／hold／refuseで選ぶ）
  - GitLab関連の強化（トークン7種以上の秘匿化・`glab` CLIの認証情報保護・プラグインマーケットプレイスがGitLabのURLに対応）、設定エイリアス`additionalMarketplaces`／`allowedMarketplaces`の追加
  - **このメディアへの示唆**：8/14のauto mode既定化と同じく「既定の挙動が変わる」型の変更が連続している。ただし対象がサブエージェント・複数セッション運用と、**Claude Codeをかなり作り込んで使っている層に限られる**。X投稿ネタとしては軸②で拾えるが、auto modeほど広くは効かない（→ ideas.md に低めの評価付きで記録）
- **料金・モデル・提供範囲の新しい変更は8:00以降なし**。Sonnet 5の$2/$10標準価格化（8/11・8/13記録）が直近のまま
- **週次使用制限+50%の8/19期限は本日も新情報なし**（8/14デイリー回の記録どおり。公式サポート記事に記載がない状態が続いている）。**8/18に再確認する**という方針は変更なし

（定期リサーチで随時追記）

---

#### 【デイリー】2026-08-14

- **【本日発動】auto modeの既定化が本日8/14から適用される**（既報。8/12・8/13の記録どおり実施）
- **【新規・数値】auto mode既定化の根拠データを公式ブログで確認した**（[Anthropic公式ブログ「Auto mode is now the default in Claude Code for Pro, Max, and Team plans」2026-08-07](https://claude.com/blog/auto-mode-default-in-claude-code)）
  - **ユーザーはClaude Codeの許可プロンプトの97%を承認している**（比較対象として、plan reviewなど他の承認では39%が却下されるとしている）
  - **1,053人の有料テスターを使った対照実験**：セッション途中で許可プロンプトを1つだけ明確に危険なコマンドに差し替えたところ、**人間のレビューが止められたのは13.6%、auto modeの分類器は89%**を検知した
  - **条件・除外まで確認した点**：既定が変わるのは**Pro・Max・Teamの新規セッション**のみ。**Enterprise・Claude API・AWS上のClaude Platform・Amazon Bedrock・Google CloudのAgent Platform・Microsoft Foundryではauto modeはopt-inのまま**。既定を自分で設定済みの人には一度だけ切り替えプロンプトが出る（pin済みなら変化なし）。元の挙動に戻すのはCLIのShift+Tabまたはデスクトップのモードドロップダウン、組織はmanaged settingsの`defaultMode`で固定できる
  - ⚠️ **二次情報の誤りを1件排除**：8/14の検索で「承認率93%」と書く記事があったが、**公式は97%**。数字を使うときは必ず上記ブログを参照する
  - **軸②のX投稿ネタとして採用（→ ideas.md）**。「使う側の何が変わるか」に加えて「自分がどう振る舞っていたか（＝ほぼ全部Yesしていた）」まで書ける数字
- **Claude Code v2.1.229（8/12）・v2.1.231（8/13）**（[公式changelog, code.claude.com](https://code.claude.com/docs/en/changelog)）：**読者の使い方が変わる変更はなし。記録のみ**
  - v2.1.231：Slackなど事前登録型OAuthクライアントを使うMCPサーバーでサインインがredirect URI不一致で失敗する不具合を修正
  - v2.1.229：`claude remote-control --continue`をドキュメント化／プラグインマーケットプレイスに`command`ソース追加／`ListAgents`が切断済みRemote Controlセッションを`offline`、クラウドセッションを`cloud`と表示／ストリーミング中に長い応答が消える・二重出力される不具合など多数修正
- **Week 33（8/10〜8/14）のダイジェストは本日時点で未公開**（`/docs/en/whats-new/2026-w33`は404）。最新は**Week 32**のまま
- **【期限接近・既知／未確認】Claude Codeの週次使用制限+50%の延長期間が2026-08-19で切れる予定**
  - 7/18に「8/19まで延長」とアナウンスされた件（`research/trends.md` 8/3記録）。**本日、公式サポート記事（[Using Claude Code with your Pro or Max plan](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)）を確認したが、この+50%施策と期限の記載はない。**出典は@ClaudeDevsのX投稿を引用した二次情報のみ
  - **5月以降3回延長されており、4回目の延長もありうる。「8/19に戻る」と断定して書かない。**8/18に再確認する
- **Anthropic本体：8/13〜8/14に新規の料金・モデル・提供範囲の変更は確認できず**（8/11のSonnet 5価格据え置きが直近）

---

#### 【デイリー】2026-08-13

- **【重要・料金】Claude Sonnet 5の$2/$10が正式に標準価格になった。9/1に予定されていた$3/$15への値上げは実施されない**（[Anthropic公式・Pricing, platform.claude.com](https://platform.claude.com/docs/en/about-claude/pricing)）
  - 公式ドキュメントの原文注記で確認済み：「導入価格として2026-08-31までとされていた$2/$10は現在の標準価格であり、2026-09-01に予定されていた$3/$15への引き上げは発生しない」
  - **⚠️ このリポジトリの記録を訂正する必要がある。**`research/trends.md`の2026-07-31・08-03・08-11の3エントリすべてで「9/1から$3/$15」を確定事項として記録していた。当時は正しかったが、**8/11のアナウンスで撤回された**。今後この数字を記事・投稿に使わない
  - **条件・除外まで確認した点**：これは**API（従量課金）の価格**。Pro・Maxなどのサブスクは元々トークン単価で請求されないため、月額が下がるわけではない。影響を受けるのは**APIを直接叩く人・メータリングクレジットで使っている人**。投稿・記事で「安くなった」と書くとサブスク利用者には誤りになる
  - **予告どおりの値上げが撤回された**という形の変更で、「新モデルが出た」型の発表とは種類が違う。**軸②のX投稿ネタとして採用（→ ideas.md）**
- **Claude Code v2.1.228（2026-08-11）**（[公式changelog, code.claude.com](https://code.claude.com/docs/en/changelog)）：バグ修正中心。描画停止・Windowsでのgit検出・`/tui`のモデル巻き戻り・セッション間メッセージングのinbox不在・Remote Controlの`/resume`が履歴を漏らす問題などを修正。**使う側の挙動が変わる変更はなく、X投稿ネタとしては採らない**
  - 1点だけ挙動変更あり：**Writeツールが、新しめのモデルなら未読ファイルを上書きできるようになった**（Editツールと同じ規則に統一）。古いモデルは従来どおり事前のReadが必要。開発寄りの話のため記録のみ
  - あわせて「auto modeのセッションは費用がやや高くなる」という初回通知の注記が削除された。8/12記録の「分類器の消費が使用量上限にカウントされなくなった」と整合する
- **8/14のauto mode既定化は変更なし**（8/12記録どおり）。`queue.md`のAUTO-01は**本日8/13の投稿を推奨**したまま
- **Anthropic IPO関連の記事が複数ヒットしたが日次の新情報ではない**：S-1の秘密提出は2026-06-01、主幹事選定は6/03で、いずれも約2ヶ月半前の出来事。8/11のSonnet 5価格据え置きを「IPO前の動き」と関連付けた解説記事が出ているだけ。**新着として記録しない**

---

#### 【デイリー】2026-08-12

出典はすべて公式ドキュメント（code.claude.com）で確認済み。

- **【重要・2日後に発動】auto modeが既定のパーミッションモードになる（2026-08-14〜）**（[Week 32ダイジェスト, code.claude.com](https://code.claude.com/docs/en/whats-new/2026-w32)）
  - 対象は**Pro・Max・Teamプランの新規セッション**。8/14以降に開始するセッションが、これまでの都度確認ではなく auto mode（分類器が安全な操作を通し、危険な操作をブロックする）で始まる
  - **条件・除外まで確認した点**：①自分で`defaultMode`を設定している人はその設定が維持される（一度だけ出る切り替えプロンプトを承認した場合のみ変わる）②組織が管理している既定値は変更されない ③切り替えは従来どおりいつでも可能
  - **併せて既に反映済み**：auto modeが呼ぶ分類器の消費が**使用量上限にカウントされなくなった**。「安全確認のために上限を食う」状態が解消されている
  - **このメディアへの示唆**：料金でも新モデルでもなく「既定の動作」が変わる変更。Claude Codeを業務で回している読者は、8/14以降に何も設定しなければ挙動が変わる側にいる。**軸②のX投稿ネタとして採用（→ ideas.md）**
- **Ultraplanリサーチプレビューが終了**：`/ultraplan`コマンドと`ultraplan`キーワードが削除された。代替はplan modeまたはClaude Code on the web（同ダイジェスト）。提供終了だが利用者が限られるプレビュー機能のため、記録のみ
- **1セッションあたりのサブエージェント上限200が撤廃**：長時間セッションで新規サブエージェントが拒否される問題が解消。同時実行数と深度の制限は従来どおり残る（8/11記録の「同時実行20・深度3」は現行仕様のまま）
- **セッション間メッセージング（v2.1.224）**：複数のClaude Codeセッションが`ListAgents`／`SendMessage`で互いに連絡できる。送るのはClaudeが書いたテキストのみで、会話履歴やファイルは渡らない。**macOS・Linuxのみ**
- **セルフホスト環境（Team・Enterpriseのパブリックβ）**：`claude self-hosted-runner`で自社マシンをランナー化し、クラウドセッションを自社ネットワーク内で実行できる。管理者が admin settings で許可する必要がある
- **`/review`が`/code-review`のエイリアスに統合**。`/fork`でコピーしたセッションは元のチェックアウトではなく専用ワークツリーで変更を行うようになった

（定期リサーチで随時追記）

---

## [2026-08-11] 調査結果

### Claude Code / Anthropic

- **【重要】Claude Cowork の利用実態データが公開**：Anthropic自身の利用分析で、Coworkのアクティビティの**9割以上がソフトウェア開発以外のタスク**だと判明。最多カテゴリは**業務オペレーションとコンテンツ制作**で、具体例として「四半期の支出を照合して差異メモを作成」「通話の書き起こしとパイプラインデータから翌日の顧客向け資料を作成」が挙げられている。Anthropicはこれらを「仕事の周りにある仕事（職務内容には明記されにくいが、実際には多くの人の仕事時間の大きな割合を占めている業務）」と位置付けた（ITmedia AI+, 2026-07-08／Web・モバイル展開発表は現地時間2026-07-07・Maxプランからβ提供）。**このメディアの軸に直結する一次情報**：「AIエージェントは開発者のものではなく、コンテンツ制作・業務オペレーションの現場で使われている」という主張を、Anthropic自身のデータで裏付けられる
- **Claude Code v2.1.213〜v2.1.220（2026-08-02〜08-03）の週次まとめで新事実を確認**（qiita.com/saitoko, 2026-08-02週）
  - **Opus 5は1Mトークンコンテキストに対応**（前回8/3記録では価格面のみだったため追記）。価格は入力$5／出力$25 per 1M tokensでOpus 4.8と同額。**fast mode の対象からOpus 4.7が除外された**
  - v2.1.214：`dir/**`形式の許可ルールが過度にマッチしていたセキュリティバグを修正
  - v2.1.216：AskUserQuestionがユーザーの待機指示を無視するバグを修正
  - v2.1.217：サブエージェントの無制限分岐を防ぐため同時実行数の上限20を追加（7/31記録のネスト深度3と併せて現行仕様）
  - v2.1.218：編集直後に左矢印キーを押すと会話が破棄されるデータロスバグを修正／`/deep-research`の自動起動を廃止（`/verify`・`/code-review`はv2.1.215で廃止済み。**スキルの自律実行廃止がこれで3つとも完了**）
- **Claude Enterprise：inference hooks をベータ提供**：チャット・Claude Code・Coworkを横断して、プロンプトとツール呼び出しがモデルに届く前に検査するリアルタイムDLP（情報漏えい防止）機能。コンプライアンス部門向け。併せて管理者分析の詳細化・モデル単位の利用権限・支出アラートも提供（releasebot.io, 2026-08時点）
- Sonnet 5のプロモ価格（$2/$10）が2026-08-31終了・9/1から$3/$15になる件は今回も変更なし（再確認のみ）

#### 【10:15 補足回】同日2回目の自動実行による差分追記

同日07:43に本日分のリサーチが完了済みのため、07:43以降・および朝の回で拾えていなかった項目のみ追記する。

- **Anthropicが英Voltaと6年10億ドルのクラウド契約（2026-08-04）**（[techcrunch.com, 2026-08-04](https://techcrunch.com/2026/08/04/anthropic-signs-10-billion-deal-with-ai-cloud-startup-volta/)）：Voltaは2026年初頭設立の英AIクラウド新興企業でNvidiaのクラウドパートナープログラム参加企業。Bitdeerと組みノルウェーに133MWのデータセンターを建設し、Nvidia Vera Rubinチップで稼働予定。**朝の回で未記録だった項目**。計算資源の確保競争という文脈で、料金・使用制限の見通しを語る際の背景材料になる
- **Anthropicが Mariano-Florentino (Tino) Cuéllar 氏を Chief Global Affairs Officer に迎える（2026-08-04）**：規制・政策対応の体制強化。記事ネタとしての優先度は低いが、企業動向として記録
- **Claude CLI v2.1.226（2026-08-10）**：バグ修正・安定性改善が中心。併せてゲートウェイの支出上限（spend-limit）に対応した使用量警告、`claude agents`のワークスペース信頼プロンプトを追加。OAuth・セッション・履歴・UIのバグ修正、科学的記数法の環境変数値の不具合、巨大なMarkdown表のレンダリング遅延も修正（[releasebot.io](https://releasebot.io/updates/anthropic/claude-code) / [gradually.ai](https://www.gradually.ai/en/changelogs/claude-code/), 2026-08-10）。**記事化に足る新機能はなし**

（定期リサーチで随時追記）

---

## [2026-08-03] 調査結果

### Claude Code / Anthropic

- **Claude Code v2.1.217（2026-07-22）**：サブエージェントの実行制御を強化（起動数・予算・バックグラウンドセッションへのより厳格な制御）。emoji shortcode自動補完・トランスクリプト書き込み警告の明確化を追加。`/fork`のバックグラウンドセッション対応、より賢い`/resume`・`/background`フロー、WebSearch・サブエージェント起動・Bash実行への安全策強化も含む（dev.classmethod.jp, 2026-07-22）
- **Claude Code v2.1.219（2026-07-25）**：Claude Opus 5をデフォルト選択肢として導入。**Opus 4.8と同価格帯**でFast Modeが2.5倍速に（前回7/27記録の「Opus 4.8比約半額」という表現は誤りだった可能性が高く、一次情報に近いdev.classmethod.jp記事では「同価格帯」と明記。使用時は「同価格・体感速度2.5倍」の表現を採用する）
- **Dynamic Workflowsのデフォルトが「medium」基準に変更**：目安15エージェント未満に設定。`/config`の「Dynamic workflow size」から他サイズ・無制限も選択可能（releasebot.io, 2026-07）
- **Claude Code週次使用制限50%増枠が2026-08-19まで再延長**：前回記録の7/19までの延長からさらに延長された（explainx.ai, 2026-08時点）
- **Claude Fable 5のサブスク取り扱いが確定（2026-07-20）**：Max・Team Premiumプランは週次使用制限の最大50%まで引き続き含まれる。Pro・Team Standardはメータリングクレジット（従量課金）へ移行。7/20〜8/2の期間限定で$100分のプロモクレジットを請求可能だった（9/17失効・**期間終了済み**）
- **Claude Developer Platform：レガシーWorkbench・実験的prompt tools APIが2026-08-17でアクセス終了**（開発者向け技術情報として記録）
- **Anthropicが「Claude for Open Source」を開始**：OSSメンテナー・コントリビューター向けにClaude Max 20x（約$1,200相当）を6ヶ月無料提供する取り組み（explainx.ai, 2026-08時点）
- Sonnet 5のプロモ価格（$2/$10）が8/31終了・9/1から$3/$15に変更される件は既存記録どおり変更なし（再確認のみ）

（定期リサーチで随時追記）

---

## [2026-07-31] 調査結果

### Claude Code / Anthropic

- **MCP 2026-07-28スペック公開・Claudeが対応拡大**：Model Context Protocolの最新仕様がステートレスコア化（双方向ステートフル通信からリクエスト/レスポンス型へ）。OAuth・OIDC認証の強化、Apps・Tasksのバージョン管理付き拡張機能が追加された。Claudeのコネクターディレクトリには950以上のMCPサーバーが掲載され毎日数百万人が利用。MCP自体は月間4億SDKダウンロード超（年初来4倍）に成長（claude.com/blog, 2026-07-28）
- **Claude Code：サブエージェントのネスト深度が3階層に再設定**：7/21〜7/24にかけて同時実行数を20に制限→ネスト完全無効化→デフォルト深度3で再有効化、という調整を経て現行仕様に確定。`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`で無効化も可能（digitalapplied.com, 2026-07）
- **Sonnet 5の導入価格（$2/$10）は2026-08-31までで、9/1以降$3/$15に上昇予定**（既存記録どおり変更なし。再確認のみ）

（定期リサーチで随時追記）

---

## [2026-07-27] 調査結果

### Claude Code / Anthropic

- **Claude Opus 5 リリース（2026-07-24）**：Opus 4.8比で約半額の価格帯（$5/$25 per 1M tokens・Opus 4.8と同水準）ながら、Frontier-Bench・GDPval-AAでAnthropicモデル中最高性能を記録。「最も安全性が高くmisuseに強いOpusモデル」と位置付け。**low/medium/highの3段階effort toggle**を新搭載し、簡単なタスクは低effortで高速・低コスト化できる（Axios / VentureBeat / Fortune, 2026-07-24）
- **Opus 5がClaude Maxの新デフォルトモデルに**：Sonnet 5が全プラン共通デフォルトだった構図から、Maxプランのみ最上位Opus 5がデフォルト化。Proプランでは引き続き選択可能な最強モデルという位置付け（コスト効率重視の設計思想が継続）。**M-09（Sonnet 5の体感変化）記事の続報ネタとして使える**：デフォルトモデルがわずか1ヶ月弱でSonnet 5→Opus 5（Maxのみ）と変わった事実は「モデル切り替えの体感」を再検証する材料になる（各社レビューサイト, 2026-07）
- 業界レビューでは「日常利用はSonnet 5をデフォルトにし、複雑なコーディング・エージェント用途でOpus 5にエスカレーションする」使い分けが推奨パターンとして定着しつつある

（定期リサーチで随時追記）

---

## [2026-07-24] 調査結果

### Claude Code / Anthropic

- **Claude Voice Mode 刷新（2026-07-23）**：音声モードで応答生成モデルをOpus・Sonnet・Haikuから選択可能に。従来は常にHaikuが担当し即答重視だったが、複雑な作業には不向きだった。新設計ではテキストチャットで直近使用したモデルの最速版がデフォルトになる（TechCrunch, 2026-07-23）
- **Claude Developer Platform：Managed Agents機能拡張**：モデルのeffort設定・environment/memory storeイベントを含むwebhookカバレッジ拡大・初期イベント付きセッションシーディング・更新時のバージョンチェック任意化・スレッドストリームのイベントデルタを追加（releasebot.io, 2026-07）
- **Claude Code Week 29（v2.1.207〜v2.1.212・7/13〜17）**：`/code-review`がバックグラウンドサブエージェントとして実行されるように変更。**`/deep-research`も手動起動専用に変更**（Claudeが自動でスキルを起動しなくなった。7/20記録済みの`/verify`・`/code-review`の手動化方針が`/deep-research`にも拡大）。スクリーンリーダーモードに削除テキストの読み上げ通知を追加。Windowsパスの特殊プレフィックス破損バグ修正。plan modeのauto設定がBashコマンドの確認プロンプトではなくauto-modeクラシファイアに依存するよう変更（code.claude.com / releasebot.io, 2026-07）
- **Claude Code Artifacts：公開共有リンク・エディターロールを追加（Team/Enterprise）**：7/20記録済みのライブMCPコネクター対応に加え、閲覧者への公開共有リンクと共同編集用エディターロールが正式に追加されたことを確認（releasebot.io, 2026-07）

（定期リサーチで随時追記）

---

## [2026-07-17] 調査結果

### Claude Code / Anthropic

- **Claude Code 安定性・ワークフロー刷新アップデート**：サブエージェントのテキストストリーミング対応、`--forward-subagent-text` フラグ／`CLAUDE_CODE_FORWARD_SUBAGENT_TEXT` 環境変数を追加（サブエージェントのテキスト・思考過程をstream-json出力に含められるように）。パーミッション・アップロード処理改善、バックグラウンドエージェントのレポート改善、ターミナル描画高速化。Chrome・Windows・Bedrock・Vertex・hooks・セッション復旧まわりの修正多数（releasebot.io, 2026-07）
- **Auto modeにセッショントランスクリプト改ざん防止ルールを追加**：セッション記録ファイルの改ざんをブロックする新ルールがauto modeのセーフティに追加。`/doctor` によるフルセットアップチェック機能・より賢いPRリンク付け・バックグラウンドタスク処理の改善・Windows向け低メモリ自動更新ダウンロードも追加（releasebot.io / code.claude.com, 2026-07）
- **Claude Artifacts（ベータ）**：セッションの成果物をclaude.ai上でライブ共有ページ化できる機能。セッション実行中も内容がその場で更新される。Team・Enterprise プランでベータ提供開始（releasebot.io, 2026-07）

---

## [2026-07-15] 調査結果

### Claude Code / Anthropic

- **Claude Reflect（リフレクトダッシュボード）ベータ公開（2026-07-09）**：Claudeの利用状況を可視化するダッシュボード機能。月次のトピック・最も活発な曜日/時間・作業パターンを振り返れる仕組み。「何をAIに頼っているか・自分でやり続けたいことは何か」を問いかける設計思想が特徴的。ウェブ・Claude Desktop対応。Free/Pro/Max利用可（メモリ有効化が必要）。クワイエットアワー設定・休憩リマインダーも搭載（Anthropic, 2026-07-09）
- **Claude for Teachers 開始（2026-07-14）**：米国K-12教員向けに、認証済み教師へ1年間無料でプレミアムClaudeを提供するプログラム。Claude Code・Coworkへのアクセス含む。Learning Commons全米50州カリキュラム標準に対応。FERPA準拠プライバシー設計。授業データを分析して学級全体の傾向把握にも活用可（9to5Mac / Anthropic, 2026-07-14）
- **Claude Cowork がWebとモバイルに展開**：デスクトップ限定だったClaude CoworkがWebおよびモバイルでも利用可能に。Maxプランから先行展開（Anthropic, 2026-07）
- **Claude Code：サブエージェントがデフォルトでバックグラウンドRunに変更**：新たな設計でサブエージェントが自動的にバックグラウンドで起動・実行される挙動がデフォルト化（releasebot.io, 2026-07）
- **Claude in Chrome が GA（一般公開）に**：Chrome拡張としてのClaude統合がリサーチプレビューを終え正式リリース（releasebot.io, 2026-07）
- **スクリーンリーダーモード追加**：アクセシビリティ強化として、スクリーンリーダー利用者向けのオプトイン型プレーンテキストレンダリングを追加（code.claude.com, 2026-07）
- **Vim Insert Modeカスタムキーマッピング追加**：`vimInsertModeRemaps` 設定で `jj` → Escape など2キーシーケンスのカスタムマッピングが可能に（code.claude.com, 2026-07）
- **Ben Bernanke氏がAnthropic Long-Term Benefit Trust（LTBT）に参加（2026-07-09）**：元FRB議長・ノーベル経済学賞受賞者。Anthropicのガバナンス体制強化に向けた人事（Anthropic, 2026-07-09）
- **AnthropicがカナダのAI研究に$10M投資（2026-07-09）**（Anthropic, 2026-07-09）

### AIコンテンツ・業務効率化トレンド

- **AIエージェントの実用化が2026年の最大トレンドに確定**：「答えるだけ」から「仕事をする」AIへの移行が完成。「プロンプトを送る」から「目的を渡してプロセスを任せる」設計が業務標準に。Claude Code・自律型エージェントの台頭が代表例（sotatek.com / relipasoft.com, 2026-07）
- **動画生成AIが実用レベルに到達**：1080p解像度・数分長尺・一貫したキャラクター表現が標準的なAI動画ツールで実現可能に。SNS広告・商品紹介・社内教育用途での実用活用が本格化。テキスト→画像→動画という制作パイプラインが1ツール完結する環境が整った（genai-ai.co.jp, 2026-07）
- **生成AI活用が「実験フェーズ」から「収益化フェーズ」へ完全移行**：ROI（投資対効果）が企業内AI活用の主要論点に変化。「使う」ではなく「成果を出す仕組みで使う」が共通課題に。業界特化型AIの台頭も加速（sotatek.com, 2026-07）

---

## [2026-07-13] 調査結果

### Claude Code / Anthropic

- **Claude Code Desktop にブラウザ内蔵（v2.1.206）**：Claude Code Desktop に組み込みブラウザが追加。ドキュメント・デザインファイル・任意の Web ページを直接開き、読み取り・クリック・操作が可能。ショートカット：macOS = Cmd+Shift+B、Windows = Ctrl+Shift+B（Views メニューからも起動可）（jls42.org / dev.classmethod.jp, 2026-07）
- **Sonnet 5 が Pro・Team Standard・Enterprise のデフォルトモデルとして確定**：Sonnet 価格で Opus クラスに近いコーディング性能を提供。適応思考（Adaptive Thinking）がデフォルトオン。アクティブセッションが PR を編集・マージ・コメント・プッシュした場合に `claude agents` へリンクが表示されるようになった（releasebot.io, 2026-07）
- **Auto Mode が Bedrock・Vertex AI・Foundry でオプトイン不要に**：これまで `CLAUDE_CODE_ENABLE_AUTO_MODE` 環境変数が必要だったが、3プラットフォームでデフォルト有効化。`disableAutoMode` 設定で無効化可能（code.claude.com, 2026-07）
- **バックグラウンドエージェントの自動更新が静音化**：Claude Code アップデート直後にバックグラウンドエージェントが静かに更新されるようになり、ユーザーがアタッチした瞬間に更新待ちが発生しなくなった（code.claude.com, 2026-07）
- **`/doctor` が対話型セットアップ診断に機能拡張**：CLAUDE.md ファイルのうちリポジトリを探索すれば推定可能なコンテンツを削ぎ落とす提案機能を追加（code.claude.com / gradually.ai, 2026-07）
- **自動更新バイナリのピークメモリ使用量を約 400 MB 削減**：ディスクへのストリーミング書き込みへの切り替えによる改善（code.claude.com, 2026-07）

### AIコンテンツ・業務効率化トレンド

- **AIライティングツール世界市場が 2026 年に $4.2B 規模**：2030 年に $12B 規模へ成長予測（CAGR 約 30%）。AIコンテンツ生成市場全体（$28.75B）とは別にライティングツールカテゴリが独立成長（TextShift / Siege Media, 2026）
- **AIを「編集・校閲」に使うコンテンツマーケターが前年比 2 倍に拡大**：2025 年 19% → 2026 年 38%。生成だけでなく品質チェック・リライト工程へのAI活用が本格化（Siege Media, 2026）
- **AIライティングの使われ方が「単発プロンプト」から「チームワークフロー組み込み」に転換**：反復タスクをエージェントが担い、人間が判断・レビュー・アカウンタビリティを担う役割分担が標準化。AI単体ではなく「AI+人間の設計力」が競争力の軸に（FutureTechnologyHub, 2026）

---

## [2026-07-10] 調査結果

### Claude Code / Anthropic

- **サブエージェントとコンテキスト圧縮が拡張思考設定を継承**：`claude agents` で起動したサブエージェントと自動コンテキスト圧縮が、セッションの拡張思考（extended thinking）設定を引き継ぐようになった。委任タスクの出力品質が向上し、複雑な推論が必要なコーディングタスクでも一貫した思考深度を維持できる（releasebot.io, 2026-07）
- **Claude Design が Claude Code と統合**：Claude Designがプロジェクトをまたいでデザインシステムを引き継ぐようになり、Claude Code とフルイドに連携。デザインキャンバス上で直接編集でき、既存ツールとの接続も拡充（releasebot.io, 2026-07）
- **Claude Fable 5：7/8以降はメータリングクレジット（API課金）のみに移行確認**：Anthropicが予告した通り7/8をもってPro/Max/Teamサブスクリプションからのアクセスは終了。利用継続にはAPI経由のメータリングクレジット（$10/$50/Mtok）が必要な状態となった（Anthropic, 2026-07-08）
- **Claude Opus 4.7 Fast Mode 廃止（2026-07-24予定）確認**：7/24以降は `claude-opus-4-7` に `speed: "fast"` を指定するとエラー返却になるため、Opus 4.8 Fast Modeへの移行が必要（releasebot.io, 2026-07）

---

## [2026-07-06] 調査結果

### Claude Code / Anthropic

- **Claude Sonnet 5 リリース（2026-06-30）**：Opus 4.8に近い性能を中間価格帯で提供するAnthropicの最新Sonnetモデル。1Mトークンコンテキスト・128k最大出力・適応思考対応。API価格は$2/M入力・$10/M出力（8/31まで）、9/1以降は$3/$15/Mに変更。Free・Proプランのデフォルトモデルとして搭載。Claude Code の新デフォルトモデルとしても採用（Anthropic, 2026-06-30）
- **Claude Fable 5 輸出規制解除・7/1から再公開**：6/12から米政府輸出規制指令により停止されていたFable 5が7/1に再一般公開。ただし7/7まではPro/Max/Team/Enterpriseの週使用枠の最大50%まで利用可能という制限付き。7/8以降はサブスクリプションから外れ、メータリングクレジット（API料金 $10/$50/M）のみでの利用に移行。Anthropicはキャパシティ確保次第でサブスクへの復帰を公式に表明（MacRumors / BleepingComputer, 2026-07-01）
- **Claude Code バックグラウンドエージェントが自動PR作成に対応**：`claude agents` で起動したバックグラウンドエージェントがWorktreeでのコード作業完了時に自動的にコミット・プッシュ・ドラフトPRを作成するようになった（以前は入力待ちで停止）。作業完了後の確認ステップが不要になり自律作業フローが完結（releasebot.io, 2026-07）
- **Claude Code デフォルト権限モードが「Manual」に変更**：CLIの既定権限モードが「Default」から「Manual」に変更。AskUserQuestionダイアログも自動継続しなくなった（`/config` でアイドルタイムアウト設定可能）。より慎重な操作承認が標準設計に（releasebot.io, 2026-07）
- **Claude Code エンタープライズ管理機能強化**：管理者向け詳細分析・モデルレベルの利用権限設定・支出アラート機能を追加。Claude Enterprise利用者の使用量・コスト・生産性の可視性が向上（support.claude.com, 2026-07）
- **Claude Apps Gateway（Amazon Bedrock・Google Cloud向け）**：企業のClaude Code利用向けにセルフホスト型コントロールプレーンが提供開始。SSO・集中ポリシー管理・ロールベースアクセス・ユーザー別コスト帰属に対応（Anthropic, 2026-07）

### AIコンテンツ・業務効率化トレンド

- **94%のマーケターが2026年にAIをコンテンツ制作プロセスに活用予定**（Averi AI調査2026）：73%が「AIと人間の共同執筆」アプローチを採用。AI単独より人間監修ありの組み合わせが最も高い成果を出す傾向が複数の調査で確認

---

## [2026-07-01] 調査結果

### Claude Code / Anthropic

- **Claude Opus 4.7 Fast Mode 廃止予告（2026-07-24）**：7/24をもってFast Mode for Opus 4.7が削除予定。`claude-opus-4-7` に `speed: "fast"` を指定するとエラー返却になるため、Opus 4.8 Fast Modeへの移行が必要（Releasebot, 2026-07）
- **Claude Code Week 26（6/22〜6/26）主要アップデート**：
  - `claude mcp login / logout` コマンド追加。シェルからMCPサーバーの認証・クリアが可能に
  - シェルモードがコマンド出力に自動応答するようになった（セカンドプロンプト不要）
  - `/rewind` が `/clear` 前の状態への巻き戻しに対応
  - バックグラウンドサブエージェントがメインセッションに権限プロンプトを表示するように（以前は自動拒否）
- **Claude Code 追加改善**：組織デフォルトモデルの設定・読みやすいセッション名・クリッカブルなファイル添付・エージェントビュー改善。バックグラウンドセッションの安定性向上（Releasebot, 2026-07）
- **Trusted Devices 機能（Team・Enterprise）**：管理者がリモートClaude Codeセッションの閲覧・操作前にデバイス認証を必須にできるセキュリティ機能を追加
- **Anthropic IPO 2026報道**：複数メディアが2026年中のIPO検討を報道。バリュエーション・資金調達の最新状況が注目されている（Zacks, FutureSearch, 2026）

### AIコンテンツ・業務効率化トレンド

- **コンテンツマーケティング実務者の約6割がAI検索の影響を実感・8割が対策意向**（日本SPセンター 2026調査）：GEO対応が「検討課題」から「実務課題」に移行していることを示す数値
- **記事制作代行の単価二極化が進行**：AI汎用文章生成の普及で「単純な文章作成のみ」の文字単価は低下傾向（0.5〜3円が主流）。一方、独自調査データ・ブランド戦略理解・AI設計・編集監修特化型代行の価値は上昇。「何をしている代行業者か」が問われる局面に（bakuyasu.techsuite.co.jp, stock-sun.com, 2026）
- **AIの業務組み込みフェーズへ完全移行**：「試す年」から「組み込む年」へ。Gartner「2026年末までに80%以上の企業がGenAI対応を本格展開」が現実に近づいている

---

## [2026-06-12] 調査結果

### Claude Code / Anthropic

- **Claude Fable 5 リリース（2026-06-09）**：Mythosクラスモデルの一般公開版。ブランド名は「Mythos」ではなく「Fable 5」として公開。全ベンチマーク（コーディング・知識・ビジョン・科学研究）でSOTA性能。価格$10/M入力・$50/M出力（TechCrunch, CNBC, Anthropic, 2026-06-09）
  - Pro/Max/Team/Enterprise：**6/9〜6/22は無料**。6/23以降はクレジット必要
  - セーフガード付き（約5%未満のセッションで一部制限発動・Opus 4.8が代替応答）
  - **Claude Mythos 5**：同一基盤モデルだが一部セーフガード緩和版。米政府「Project Glasswing」で展開（一般向けでない）
- **Claude Code v2.1.170 主要アップデート**：ネスト型サブエージェント（最大5階層）・`/cd`コマンド・ポストセッションフック・セーフモード・プラグイン検索追加。Fast modeがOpus 4.8デフォルトに（Releasebot, 2026-06）
- **Claude Sonnet 4・Opus 4（旧API）廃止（2026-06-15）**：本日（6/12）から3日後。API利用者は移行が必要

### AIコンテンツ・業務効率化トレンド

- **2026年は「試す年」から「業務・ツールに組み込む年」への転換点**：Gartner「2026年末までに企業の80%以上がGenAI対応アプリを本格展開」と予測（usknet.com, 2026）

---

## [2026-06-08] 調査結果

### Claude Code / Anthropic

- **Claude Mythos クラスモデルが一般公開間近**：Opus ラインの上位に位置する新モデル。Anthropicが「coming weeks」でリリース予定と確認済み。セキュリティベンチマークで約90倍の能力向上（オフェンシブセキュリティで181 vs 2 Firefox exploits）。価格帯は$25+/M入力・$125+/M出力のプレミアム想定。当初はAWS Bedrock経由で先行提供の可能性（BleepingComputer, TokenMix, AndroidHeadlines, 2026-05-28〜）
- **6月15日 課金構造変更（本日施行10日前）**：Agent SDK・`claude -p`（非インタラクティブ）・Claude Code GitHub Actions・サードパーティエージェントアプリが既存サブスク枠から切り出され、独立した「Agent SDK クレジットプール」へ移行。付与額はPro=$20 / Max5x=$100 / Max20x=$200。月末未使用分は失効・非繰り越し。**インタラクティブ利用（端末でのClaude Code・Claude Cowork・チャット）は影響なし**（devtoolpicks.com, codersera.com, 2026-06）
- **Claude 障害（2026-06-02）**：サブエージェントシステムのバグにより無限ループ・指数的トークン消費が発生。数時間分の使用枠が数分で消滅するケースあり。Web・API・Claude Code が影響を受け、6/3に主要インシデント解決（一部継続）（TechRadar, SQMagazine, 2026-06-02〜03）

### AIコンテンツ・業務効率化トレンド

- **AI検索利用率が8ヶ月で3.5倍増**（AI検索白書2026・日本）：検索行動の変化が数値として確認。「AI検索を使っている」層が急拡大中（webtan.impress.co.jp, 2026-04）
- **日本の生成AI勢力図が変化**：Geminiの利用率が1.5倍に急成長し、ChatGPT一強から多様化フェーズへ。週複数回利用比率はGemini 71.6%・Claude 70.4%・Perplexity 69.2%（サイバーエージェント調べ, 2026）
- **AIコンテンツマーケティング市場：2026年に50億ドル規模**（2025年40億ドルからCAGR 25.4%増）。代行市場への需要も継続拡大（gii.co.jp, 2026）

---

## [2026-06-01] 調査結果

### Claude Code / Anthropic

- **Claude Opus 4.8 リリース（2026-05-28）**：Claude Codeにデフォルト統合。エージェントコーディングスコア 64.3% → 69.2%、ツール使用を伴う多分野推論 54.7% → 57.9%に向上。「判断の鋭さ・進捗の誠実な報告・長時間の自律作業」が強化（MacRumors, 9to5Mac, 2026-05-28）
- **Dynamic Workflows（Research Preview）**：1セッション内で数十〜数百のサブエージェントをバックグラウンドで並列オーケストレーション。コードベース全体のバグハント・セキュリティ監査・大規模リファクタリング（数千ファイル規模）に対応（ghacks.net, 2026-05-30）
- **Ultracode Mode / Effort Controls**：effort levelをxhigh（Ultracode）に設定しDynamic Workflowsを自動使用するClaude Code専用設定。high/extra/maxの3段階調整が可能。highは前モデル同等トークンで性能向上を実現
- **Fast Modeが前モデル比3倍安価に**：Opus 4.8のFast Modeは2.5倍速で動作。価格自体はOpus 4.7と同一
- **Security Guidance Plugin**：コード編集・diff・コミットをリアルタイム監視。SQLインジェクション・XSS・ハードコードAPIキーなど約25種の脆弱性クラスをregexベースで自動検出
- **Claude Managed Agents 強化（6月）**：セルフホストサンドボックス対応・アクティブセッション中のMCPサーバー設定更新が可能に・100Kトークン超の大出力を自動ファイルスピル
- **Claude Platform on AWS 開始**：IAM認証・AWSビリングでMessages API・Files API・Managed Agentsなどを利用可能。AWSユーザーへのエンタープライズ展開が加速
- **Anthropicが65億ドルの資金調達発表**（2026-05-28）：Opus 4.8発表と同日。コンピュート・インフラ拡張の資金とみられる（SiliconANGLE, 2026-05-28）
- **Mythosクラスモデルを近日予告**：「coming weeks」内に全ユーザー向けリリースと予告。Opus 4.8と別ラインの高性能モデルとして位置づけ（MacRumors, 2026-05-28）
- **モデル廃止予定**：Claude Sonnet 4・Opus 4はAPI上で2026年6月15日に廃止予定

### AIコンテンツ・業務効率化トレンド

- **マーケターの85%が2026年にコンテンツ制作へAIを活用**（2023年61%から増加）。AIを使ったコンテンツ制作が標準化しつつある（affinco.com / CleverType, 2026）
- **生成AIグローバル市場規模が2026年に914億ドル見通し**（2025年630億ドルから約45%増）（businessresearchinsights.com, 2026）
- AIコンテンツツール投資企業で「420% ROI・62%の制作速度向上・32%のエンゲージメント増加」が報告されている（Siege Media, 2026）
- **少人数体制でのコンテンツ運用が標準化**：専任2〜5名が最多・約3割が専任なしで運営。増員よりツール活用で成果を出すモデルが普及
- **AI活用による外注費ゼロ化事例が増加**：LP制作内製化で月額10万円の外注費ゼロ・制作時間3営業日→2時間という事例あり（AIアナリスト, 2026）

---

## [2026-05-25] 調査結果

### Claude Code / Anthropic

- **Dreaming詳細**：エージェントが直前セッションの行動パターンを分析し、次セッション用メモリエントリを自動生成する自己改善プロセス。法律AIスタートアップHarveyのパイロットでタスク完了率が**約6倍**に向上（Anthropic, 2026-05-06）
- **Outcomes詳細**：別の評価モデルがエージェント出力をルーブリックで採点し修正指示を与える自己採点ループ。Anthropic社内ベンチマークで「.docxタスク+8.4%・.pptxタスク+10.1%のタスク成功率向上」を記録
- **Claude Finance**：金融業務向け10種のエージェントテンプレートを公開。ピッチ資料作成・決算レビュー・財務モデル構築・KYCスクリーナーなどを含む参照アーキテクチャ（Code with Claude 2026, 2026-05-06）
- **Code Review機能とCI auto-fix**：チームのコードレビュー工数削減に特化した新機能。**CI auto-fix**はPRに対して自動修正を適用する（Code with Claude 2026）
- **リモートコントロール**：あるデバイスで開始したセッションを別デバイス（スマートフォン等）から引き継ぎ継続可能に。背景エージェントとの組み合わせで移動中の監視・操作が現実的に

### AIコンテンツ・業務効率化トレンド

- **2026年5月の主要AI料金が横並びに**：Claude Pro・ChatGPT Plus・Perplexity Proが月額約20ドル（日本円換算約3,200円前後）。Google AI Plusが年初に日本円建て月額1,200円のプランを新設し、コスパ重視層を取り込む動き（Business Insider Japan, 2026-05）
- ChatGPTに中価格帯「Go」プラン（月額約1,500円）が新設。AI課金の裾野が広がっている

---

## [2026-05-22] 調査結果

### Claude Code / Anthropic

- **Claude Code Desktopアプリ大幅リニューアル**：セッションサイドバー・ドラッグ＆ドロップワークスペース・統合ターミナル・ファイルエディタ・SSH対応（Mac）・高速diff・拡張プレビュー。複数タスクの並列実行が容易に
- **Managed Agents強化**：dreaming・マルチエージェント連携・outcomes・webhooks追加。長時間エージェント作業の制御が向上
- **Claude Code週次使用制限を7/13まで50%増**（5/13発表）：Pro・Max・Team・Enterprise対象。Codexへの対抗措置とも言われる
- **Claude Opus 4.7**：コーディング強化・長時間タスク改善・高解像度ビジョン対応。Opus 4.6を上回る
- **agents --jsonコマンド追加**：ライブセッションをJSON一覧で取得しスクリプト連携可能に

### AIコンテンツ・業務効率化トレンド

- Claude Code Desktopリニューアルで非エンジニアでもマルチタスク並列運用が現実的に
- 「プロンプトを書く」から「エージェントを設計・監督する」段階への移行が加速（継続トレンド）

---

## [2026-05-15] 調査結果

### Claude Code / Anthropic

- **Agent View**：複数のClause Codeセッションを一画面から管理する新機能。バックグラウンドエージェントを起動し、ステータス・最終応答を確認しつつ、入力が必要な時だけセッションに戻れる設計
- **/goal コマンド**：成果ベースの自律タスク実行機能。ユーザーが目標を宣言するだけでClaude Codeが最小介入で達成に向けて動作。ワークフロー自動化に直結
- **System Prompt Compaction**：長時間セッションでコンテキストとユーザーの意図を保持する機能。長期・複雑なワークフローの中断を大幅に削減
- **--plugin-url フラグ**：URLからプラグインアーカイブを取得してセッションに適用。プラグイン管理がより柔軟に
- **Claude for Excel・PowerPoint・Word が正式GA**：Claude for Outlookもパブリックベータ開始。ビジネスツール統合が本格化
- **Claude for Small Business**：QuickBooks・PayPal・HubSpot・Canva・Docusign・Google Workspace・Microsoft 365 と連携した業務フロー自動化サービスをローンチ
- **Claude Cowork 法律領域への展開**（2026-05-12）：BigLaw向けに法律MCP connectorを20以上、業務分野別プラグインを12種追加。リサーチ・契約・ディスカバリー・マター管理・法律支援に対応
- **Claude Platform on AWS**：AWS経由でClaude APIにアクセスできるAnthropicマネージドインフラ。AWSの請求・IAM認証と統合

### AIコンテンツ・業務効率化トレンド

- **テキスト生成AIツールがB2Bマーケターの利用ツールで2位浮上**：「アクセス解析ツール」（1位）に次ぐ29.2%のシェアを獲得（1年で主要ツール群に食い込んだ形）
- **コンテンツマーケティング実務者の約6割がAI検索の影響を実感**。対策意向は8割（日本SPセンター 2026年調査）
- **「プロンプトを工夫する」から「エージェントを設計・監督する」段階へ移行**。AI活用の巧拙が業務効率に直結する時代に入った
- **マルチモーダルAIが事実上の標準仕様に**：テキスト・画像・音声・動画を一つのモデルで横断処理できる環境が整備完了。音声生成は感情指示（怒り・囁きなど）にも対応
- 少人数体制での安易な増員より効率化・ツール活用で成果を出すスタイルが定着。「使う人」と「使えない人」の生産性格差が顕在化

---

## [2026-05-01] 調査結果

### Claude Code / Anthropic

- **Claude Code v2.1.114〜v2.1.119**（Week 17: 2026-04-20〜24）が順次リリース
- **Computer Use**：3月にPro・Maxユーザー向けに追加。Claudeがファイルを開いたり開発ツールを操作したりをセットアップ不要で実行できる
- **Auto Mode**：通常の承認フローと `--dangerously-skip-permissions` の中間。繰り返しの承認を削減する2段階チェック方式
- **Scheduled Tasks**：Anthropicのクラウドインフラ上で定期ジョブを実行できるように。PCを開いていなくても動く
- **/powerup**：新規ユーザー向けインタラクティブオンボーディングシステムとして4月に追加
- **MCP 500K アップグレード**：ツールの出力文字数上限が50万文字に拡張
- **Claude Opus 4.7**：2026-04-16リリース。エージェント型コーディング・マルチステップ推論・大規模ツール使用でOpus 4.6を上回るとされる
- **Claude Design**：プロトタイプ・スライド・ワンページャーなどのビジュアルを作成できる新しい実験的プロダクト（4月発表）
- **Managed Agents**：長時間エージェント作業向けのホスト型Claudeプラットフォームサービス。セッション・ハーネス・サンドボックスの安定したインターフェースを提供
- **Claude Cowork**：2026年1月末にリサーチプレビューとして静かに開始。反復的な作業をAIが担い、人間が重要な判断に集中できる環境を目指す

### AIコンテンツ・業務効率化トレンド

- コンテンツ制作における生成AI市場規模：2026年予測 **287億5,000万ドル**（CAGR 33.5%、2025年215億3,000万ドルから）
- コンテンツマーケターの **97%** が2026年にAI活用を計画（2025年90%、2024年83.2%から増加）
- AI執筆ツール活用による生産性向上：チームあたり **44%の生産性向上**、月間コンテンツ公開数 **42%増加**
- 従業員1人あたり週約2.2時間の節約効果が報告されている
- 最も信頼されるAIツールはChatGPT（選択率80%）、次点はClaude（55%）
- 新規Webページの74%がすでにAI生成テキストを含む状況。「AIを使う」から「AIを使いこなす」へ競争軸がシフト
- AIを業務活用する目的として「効率・生産性向上」（56%）が「イノベーション・成長」（29%）を大きく上回る

---

## [2026-05-08] 調査結果

### Claude Code / Anthropic

- **「Code with Claude」開発者カンファレンス**（2026-05-06 サンフランシスコ）にて複数の重要アップデートを発表
- **SpaceX Colossus 1 コンピュートパートナーシップ締結**：300MW超の追加キャパシティ・GPU22万台超を「月内に」提供開始予定。これを背景にレート制限を大幅引き上げ
- **Claude Code レート制限を倍増**：Pro・Max・Team・Enterpriseの5時間レート制限を2倍に。Pro・MaxはピークアワーのCode利用制限も撤廃
- **Claude Opus APIレート制限を大幅引き上げ**：Tier-I の入力トークン上限が30,000→500,000トークン/分、出力が8,000→80,000トークン/分。Tier-IIは入力200万→Tier-IIIは入力500万トークン/分まで拡大
- **Claude Code v2.1（2026-05-04 更新）主要変更点**：
  - `/color`（引数なし）でセッションカラーをランダム設定
  - `/mcp` が接続サーバーのツール数を表示（ツール0件のサーバーをフラグ付き表示）
  - `--plugin-dir` がディレクトリに加えて `.zip` アーカイブを受け入れ可能に
  - `/model` ピッカーでOpus 4.7の重複エントリを折りたたみ表示、現行Opusは"Opus"と表示
  - `--channels` がコンソール（APIキー）認証でも動作するように
- **Claude Code v2.1（2026-05-01 更新）主要変更点**：
  - `/model` ピッカーが `ANTHROPIC_BASE_URL` にゲートウェイを指定した場合 `/v1/models` 一覧を表示
  - `claude project purge [path]` コマンドを追加（プロジェクトの履歴・設定・タスクを一括削除）

### AIコンテンツ・業務効率化トレンド

- （今回は2026-05-01分と重複なし・特記事項なし）

---

## [2026-05-15] 調査結果

### Claude Code / Anthropic

- **Claudeサブスクリプション構造変更（2026-06-15施行）**：Agent SDK・`claude -p`等の自動化・プログラム利用が「別枠クレジット」として切り出される
  - 付与額：Pro=$20 / Max 5x=$100 / Max 20x=$200
  - 自動化をヘビーに使うユーザーにとっては実質値上げ。手動利用メインのユーザーは影響軽微
- SpaceX提携・レート制限倍増・API上限引き上げは2026-05-08エントリに記録済み（no.22として公開）

---

## [2026-05-18] 調査結果

### Claude Code / Anthropic

- **Claude Code v2.1.139（2026-05-11 リリース）** でAgent ViewとGOALコマンドが正式にResearch Previewとして公開
  - Agent View：全Claudeセッション（実行中・入力待ち・完了）を1画面のCLIダッシュボードで管理。バックグラウンドエージェントのステータスと最新応答を確認し、必要なときだけセッションに戻れる設計
  - /goal コマンド：Claudeが定義された完了状態に達するまで自律的に目標を追求する命令駆動型の実行機能
- **/feedback の機能拡張**：直近24時間または7日間のセッションを含められるよう拡張（複数セッションにまたがる問題の報告が可能に）
- **Rewind メニューに「Summarize up to here」追加**：古いコンテキストを圧縮しつつ直近ターンを保持する操作が可能に
- **terminalSequence フィールド追加**：フックの JSON 出力にデスクトップ通知・ウィンドウタイトル・ベルを制御端末なしで送出できる
- **ANTHROPIC_WORKSPACE_ID 環境変数追加**：ワークロードアイデンティティフェデレーション用スコープ設定
- **claude agents --cwd \<path\>**：指定ディレクトリにスコープしたセッション一覧の取得が可能に
- **サブスクリプション変更の経緯補足**：Anthropicは2月に第三者エージェント利用を禁止→4月に禁止を強化→5月に「分割課金」方式として再開。Agent SDK枠は非繰り越し（月末に未使用分失効）

---

## [2026-06-08] 調査結果

### Claude Code / Anthropic

- **Claude Code v2.1.166（2026-06-06 リリース）**：`fallbackModel` 設定を追加。プライマリモデルが過負荷・利用不可時に最大3つのフォールバックモデルを順番に試みる構成が可能に。`--fallback-model` フラグがインタラクティブセッションにも適用される（releasebot.io, 2026-06-06）
- **`/plugin list` コマンド追加**：インストール済みプラグインを `--enabled`/`--disabled` フィルタ付きで一覧表示。`/btw` コマンドに「c to copy」ショートカットを追加（rawマークダウン回答をクリップボードにコピー）
- **Claude Mythos：Project Glasswingとして15カ国150組織へ拡大（2026-06-02）**：電力・水道・医療・通信・ハードウェアの重要インフラ組織向けに展開。セキュリティタスクに特化した能力を持つ汎用モデルとして位置づけ。一般公開は安全性・悪用懸念を理由に引き続き未実施（TechCrunch / 9to5Mac, 2026-06-02）

### AIコンテンツ・業務効率化トレンド

- **AI Overview表示率：複数社の推計で30〜40%に更新**：2026年6月時点の複数リサーチ会社の推計値。従前の47%（別調査手法）との差は集計対象クエリの定義の違いによるもの。インフォメーショナル検索では引き続き高水準で表示

---

## [2026-06-15] 調査結果

### Claude Code / Anthropic

- **Claude Fable 5 リリース（2026-06-09）**：Mythosクラスモデルの一般公開版として初リリース。コンテキストウィンドウ1Mトークン・最大出力128kトークン。API価格は入力$10/M・出力$50/M（Opus 4.8の2倍）。ハイリスク領域（サイバーセキュリティ・生物化学・蒸留など）ではOpus 4.8にフォールバックする安全制限付き（Anthropic / TechCrunch, 2026-06-09）
- **Fable 5のサブスクリプション取り扱い**：Pro/Max/Team/Enterpriseプランでは6月22日まで無料で利用可能（使用量2倍カウント）。6月23日以降はこれらのプランから削除され、利用には使用クレジットが必要。Anthropicは容量確保次第でサブスクプランへの再統合を予定（Anthropic公式, 2026-06）
- **Claude Mythos 5**：Project Glasswing参加の限定ユーザーのみ提供継続。一般公開の予定は現時点で未定（Anthropic, 2026-06-09）
- **Claude Code v2.1.170（2026-06-09）**：Fable 5アクセスを追加。プラグイン検索機能追加。Chrome・VSCode・ターミナルワークフロー改善。VSCode統合ターミナルからのセッション起動時にトランスクリプトが保存されないバグを修正（releasebot.io, 2026-06）
- **Claude Code v2.1.172（2026-06）**：ネストされたサブエージェントが最大5階層まで可能に。エージェントが自分自身のサブエージェントを起動でき、各フレームが独自のシステムプロンプト・モデルを持つ構造。「コンテキスト管理のためのエージェント起動」がユースケース（claudefa.st, 2026-06）

---

## [2026-06-22] 調査結果

### Claude Code / Anthropic

- **Claude Code Artifacts（2026-06-18 リリース）**：Team・Enterpriseプラン向け。セッションの成果物をライブインタラクティブなHTML共有ページとして公開できる新機能。複数データソース・コードをリアルタイム連携し、チームメンバーはURLを開くだけで更新内容を即時確認可能。セキュリティ設計：デフォルトでプライベート・CSPにより外部スクリプト/フォント/スタイルシートの読み込みをブロック。fetch/XHR/WebSocketも完全ブロック（Stripe社の事例：5,000万行Rubyコードベースの全体マイグレーションを1日で完了。通常チーム全体で2ヶ月超かかる作業）（VentureBeat / claude.com/blog, 2026-06-18）
- **Claude Code Auto Modeの安全性強化**：破壊的gitコマンド（git reset --hard・git checkout -- .・git clean -fd・git stash drop）を明示的指示なしに自動ブロック。エージェントが同セッション内で作成していないコミットへのgit commit --amendも自動ブロック。terraform destroy/pulumi destroy/cdk destroyもスタック指定なしでブロック（releasebot.io, 2026-06）
- **Fable 5の無料サブスク期間終了（2026-06-22）**：本日をもってPro/Max/Team/Enterpriseプランでの無料利用終了。6/23以降は使用クレジット（APIレートと同一：$10/M入力・$50/M出力）が必要。なお無料期間中もFable 5は通常モデルの約2倍の使用量をカウントしていた。容量確保次第でプランへの復帰を予定しているが日程は未定（claudefa.st / developersdigest.tech, 2026-06）
- **Claude Design：Brand Controls・Code Sync追加**：エンタープライズチーム向けにブランドコントロール機能とコード同期機能を追加（TechRepublic / Anthropic, 2026-06）

---

## [2026-06-19] 調査結果

### Claude Code / Anthropic

- **Claude Code 最新アップデート（6月中旬〜後半）**：言語認識セッションタイトルが追加（日本語入力時に適切なタイトルを生成）。フッターリンクのバッジ表示が改善。Bedrock認証情報キャッシュが最適化（releasebot.io, 2026-06）
- **Bedrock / Vertex / Foundry での auto mode**：Opus 4.7 / Opus 4.8 向けに auto mode が有効化。パーミッションプロンプトをバックグラウンド安全チェックに置き換える設計（サードパーティプロバイダー向け）（releasebot.io, 2026-06）
- **/plugin list コマンド追加**：インストール済みプラグインの一覧表示が可能に。managed deployment 向けバージョン管理機能も追加（mexc.com / releasebot.io, 2026-06）
- **接続切断時の部分レスポンス保存**：mid-stream での接続断発生時に、それまでの部分レスポンスが raw エラーではなく保存されるよう改善（releasebot.io, 2026-06）
- **WSL2 マウスホイール修正**：WSL2 環境でのスクロール問題を修正。サンドボックス動作・ウェルカムバナー・プラグイン読み込みパフォーマンスも改善（releasebot.io, 2026-06）

---

## [2026-06-29] 調査結果

### Claude Code / Anthropic

- **Claude Code v2.1.195（2026-06-26 リリース）**：複数のバグ修正とパフォーマンス改善（github.com/anthropics/claude-code, 2026-06-26）
  - **日本語・中国語・タイ語等の語間スペースがない言語で音声入力の自動送信が動作しないバグを修正**：日本語ユーザーに影響していた問題が解消
  - macOS でデフォルト音声入力デバイス変更後に無音をキャプチャし続けるバグを修正
  - フック識別子のハイフン名（`code-reviewer`・`mcp__brave-search` 等）が部分一致していたバグ→完全一致に変更
  - JetBrains IDE ターミナル（IntelliJ / PyCharm / WebStorm 等）のちらつきを修正
  - `CLAUDE_CODE_DISABLE_MOUSE_CLICKS` 環境変数を追加：フルスクリーンモードでマウスクリック/ドラッグ/ホバーを無効化しながらホイールスクロールは維持できる設定
- **ストリーミング中の CPU 使用量を約 37% 削減**：MCP 信頼性と OAuth 再試行ロジックも強化（releasebot.io, 2026-06）
- **Trusted Devices for Remote Control（Team・Enterprise 向け）**：管理者がメンバーのローカル Claude Code セッションをリモート閲覧・操作する前にデバイス認証を必須化できる新機能（support.claude.com, 2026-06）
- **JetBrains IDE：Claude をエージェントプロバイダーとして使用するプレビュー開始**（GitHub Changelog, 2026-06-22）：IntelliJ / PyCharm / WebStorm 等で Claude をネイティブエージェントとして使用できる環境が整備

### AIコンテンツ・業務効率化トレンド

- **LLM 由来のトラフィックが前年比 527% 増加**（Evolv Agency, 2026）：ただし米国デスクトップ検索全体に占める LLM 経由の割合は約 5.6%（WSJ, 2025年6月時点）。絶対量はまだ小さいが成長速度は急加速
- **LLM 引用の 44.2% がページ冒頭 30% のコンテンツから発生**（position.digital / omnibound.ai, 2026-06）：「冒頭200語」という既存データをより広い定義（冒頭 30% ≒ 約 600〜800語）で補強する新データ。冒頭セクション全体の質が引用確率を大きく左右する
- **コンテンツ形式別の LLM 引用率**（AI Mode・ChatGPT・Perplexity 共通・omnibound.ai, 2026-06）：リスト記事 21.9%・一般記事 16.7%・製品ページ 13.7%。リスト形式が LLM に引用されやすい傾向を複数エンジンで確認

---
---

## [2026-06-26] 調査結果

### Claude Code / Anthropic

- **Claude Code `/rewind` サポート追加**：エージェント・パーミッション動作改善、MCP耐障害性・OAuth処理改善、CPU・メモリ使用量低下。長時間セッション・ストリーミング中のリソース消費が改善（releasebot.io, 2026-06）
- **Claude Tag on Slack（ベータ開始）**：Slackチャンネルで `@Claude` タグ付けでタスク委任・文脈蓄積・非同期作業が可能に。ツール・データへのアクセスは制御付き。Claude Enterprise/Team向けベータ（technobezz.com, 2026-06）
- **Anthropic が $965B 評価で資金調達・IPO 機密申請**：OpenAI を抜いて時価総額首位に。Claude Code が Anthropic の急成長を牽引していると CNBC が報道（cnbc.com, 2026-06）

---

---

## [2026-07-03] 調査結果

### Claude / Anthropic

- **Claude Sonnet 5 リリース（2026-06-30）**：Anthropic の新デフォルトモデル。1M トークンのコンテキストウィンドウ。プロモーション価格 $2/$10 per MTok（〜2026-08-31）。「最もエージェント的な Sonnet モデル」と位置づけ。TechRadar は「AI の戦いはチャットからエージェントへ」と報道（techradar.com, 2026-06-30）
- **Claude Fable 5 が 2026-07-01 にグローバル再デプロイ**：米国輸出規制解除を受けて世界向けに復帰。新しいサイバーセキュリティ分類器を追加（marktechpost.com, 2026-07-01）
- **Claude Code v2.1.197**：Claude Sonnet 5 がデフォルトモデルに変更。組織単位のデフォルトモデル設定が可能に。読みやすいセッション名・クリック可能なファイル添付・スムーズなエージェントビューを追加（releasebot.io, 2026-07）
- **ストリーミングアイドルウォッチドッグがデフォルト有効化**：5分間無応答で自動中断・リトライ。全プロバイダー向け（releasebot.io, 2026-07）
- **マウスクリックでメニュー選択が可能に**：フルスクリーンモードでパーミッションプロンプト・/model・/config 等をマウスで操作できるように（releasebot.io, 2026-07）

---

## Claude Code / Anthropic アップデート

## [2026-07-20] 調査結果

### Claude Code / Anthropic
- **Claude Code 広範囲安定性・安全性アップデート（7月後半）**：パーミッションチェックの厳格化・Bash/PowerShellの安全な実行処理改善・バックグラウンドセッションのクリーンアップ強化・テレメトリ強化・リモート・プラグイン信頼性改善。`EndConversation`ツール追加（エージェントがセッション終了を明示的に宣言可能に）・長時間タスク向けプログレスハートビートを追加（releasebot.io, 2026-07）
- **`/verify` と `/code-review` が手動専用に変更**：Claudeが自動でスキルを起動しなくなり、ユーザーが明示的にコマンド入力した場合のみ実行（releasebot.io, 2026-07）
- **ArtifactにライブMCPコネクターデータ対応・公開共有リンク・編集者ロール追加（Team/Enterprise）**：公開済みArtifactが各閲覧者のMCP接続を通じてリアルタイムデータを取得・操作可能に。閲覧者は初回アクセス時にアクセスを承認する設計。公開共有リンクと共同編集用エディターロールもTeam/Enterpriseで追加（releasebot.io, 2026-07）
- **Claude Tag（Slack）セッションからのArtifact作成に対応**（releasebot.io, 2026-07）
- **`/login` コマンドがAnthropicパブリックゲートウェイエンドポイントに対応**（code.claude.com, 2026-07）
- **`/cd` コマンドにディレクトリパス候補サジェスト機能を追加**（code.claude.com, 2026-07）
- **`dir/**` 単一セグメント権限ルールのスコープバグ修正**：`Edit(src/**)` のような許可ルールがcwd配下ではなくツリー全体の同名ネストディレクトリへの書き込みを承認していたバグを修正（releasebot.io, 2026-07）
- **Claude Code週次使用制限の50%増枠が2026-07-19まで延長**：5月から継続中の50%増プロモーション上限が7/19まで延長された（helpnetsecurity.com, 2026-07-13）

（定期リサーチで随時追記）

---

## AI全般トレンド（コンテンツ・業務効率化領域）

### [2026-07-20] AIコンテンツ・業務効率化トレンド
- **Claude Sonnet 5が「長文品質」評価でAIライティングモデルのデフォルト推奨に**：2026年7月時点の複数独立レビューで「自然な長文執筆の最良デフォルト」として評価。精度・校閲重視の用途ではOpus 4.8が推奨される二層構成が定着（buildmvpfast.com / eesel.ai, 2026-07）
- **AIライティング市場が2層化**：高品質出力を目的とした「最上位モデル層」（Claude Sonnet 5・GPT-5.5等）と、SEO・ブランド施行・キャンペーン量産向け「ワークフローツール層」（Jasper・Writer等）への分離が鮮明（buildmvpfast.com / digitalmarketinginstitute.com, 2026-07）

（定期リサーチで随時追記）

---

## 記事ネタ候補（ここから article-backlog.md に移す）

（随時追記）
