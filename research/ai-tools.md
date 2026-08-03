# 競合AIツール・新興ツール動向

最終更新: 2026-08-03

---

## [2026-08-03] 調査結果

### Gemini（Google）

- **Gemini 3.6 Flash登場**：トークン効率・コード/エージェント計画能力を改善しつつ低価格化。**Gemini 3.5 Flash-Lite**は低遅延・大量自動化向けの低コストオプションとして追加（llm-stats.com, 2026-08時点）

### ChatGPT（OpenAI）

- **ブラウザエージェント「Atlas」を廃止しChatGPT・Codexへ統合する方針**：Atlasは2026-08-09で動作終了予定。ChatGPTが複数タブ・ダウンロード・ナビゲーション改善・アカウントログイン対応を含む、より高機能なブラウザ体験を獲得する見込み。**M-01（ChatGPT Work比較記事・TOP10 1位）の続報素材として使える**：「複数アプリを横断するエージェント」路線をChatGPTがさらに強化している動きの一つ（llm-stats.com, 2026-08時点）
- ChatGPTに新しい音声認識（dictation）モデルが全プランに展開

### AIコーディングエージェント市場

- **選定軸が「どれが一番強いか」から「開発フローにどれだけ自然に統合できるか」へ移行（2026年8月時点）**：Claude Code・GitHub CopilotをTier1の軸に据え、Cursor・Windsurfをプロジェクト単位で併用する組み合わせ運用が実務的という評価が定着しつつある（qiita.com, 2026-08）。**M-04（Claude Code vs OSSエージェント比較）の結論部分に使える視点**：「フロンティアモデルが収束→どれだけ自然に統合できるかで選ぶ」というこのメディアの実況軸とも一致する

### Hermes Agent（Nous Research）

- **GitHubスター21.4万超（2026-07-14時点）**：継続成長中。**v0.18.0「The Judgment Release」（2026-07-01）**でMixture-of-Agents（MoA）が通常のモデル選択と同じ感覚で使える一級機能に。`/learn`のcompletion contracts・検証エビデンス記録機能を追加し、エージェントの「完了しました」を証拠ベースで判断できる方向へ進化。v0.18.2まで7/8に更新確認。**2026年8月時点の新規アップデート情報はまだ確認できず**（labmemo.com, 2026-07）

（定期リサーチで随時追記）

---

## [2026-07-31] 調査結果

### ChatGPT（OpenAI）

- **OpenAIが学術研究者10万人へ無料アクセスプログラムを開始（2026-07-29）**：GPT-5.6 Sol Proを含む最上位モデルに2027年まで無料アクセス可能。1ワークスペースにつき最大5名まで招待可・ChatGPT Pro相当の利用枠。このメディアのターゲット（個人・中小企業）には直接関係しないが、OpenAIの「フロンティアモデルの無料開放で普及を狙う」戦略として記録（axios.com, 2026-07-29）
- 前回記録のGPT-5.6ファミリー正式公開・ChatGPT既定モデル据え置き（GPT-5.5 Instant継続）は変化なし

### AIコーディングエージェント市場

- **前回（7/24）のCursor・Copilotクレジット制移行、Windsurf→Devin Desktopリブランドから大きな新展開なし**：直近90日の主要動向（Cursor Composer 2.5・Claude Code制限倍増・Copilot Max・Antigravity 2.0）を再確認したのみ

（定期リサーチで随時追記）

---

## [2026-07-27] 調査結果

### Gemini（Google）

- **Gemini 3.5 Flashがアプリ全体の新デフォルトモデルに（2026-07-17）**：価格$1.50/$9.00（per 1M tokens）。Gemini 3.1 Proの約4倍速・入力100万トークン超対応・音声動画を直接受付。API単価はGPT-5.6 Sol比で約70%安い（各社ベンチマークサイト, 2026-07）

### ChatGPT（OpenAI）

- **グループチャット機能の新規作成を制限（2026-07-09〜）**：web/iOS/Androidで新規グループチャット作成・既存会話のグループ化・招待リンク経由の参加ができなくなった。用途を絞る方向の仕様変更（releasebot.io, 2026-07）
- 前回記録のGPT-5.6ファミリー（Sol/Terra/Luna）・カスタム指示5,000文字化は継続内容（新展開なし）

### このメディアへの示唆

- Anthropic（Opus 5をMaxのみデフォルト化）・Google（Gemini 3.5 FlashをGemini全体でデフォルト化）ともに「軽量・高速モデルを主役に据え、重い処理は選択制」という設計思想が共通化してきた。trends.mdのOpus 5記事ネタと合わせ、「AI各社が『どのモデルを既定にするか』で見せる思想の違い」という比較軸がさらに厚みを持てる

（定期リサーチで随時追記）

---

## [2026-07-24] 調査結果

### ChatGPT（OpenAI）

- **GPT-5.6ファミリー（Sol・Terra・Luna）が正式公開（2026-07-09）**：米政府の安全性審査を経て一般提供を開始。ただし**ChatGPTの既定モデルは引き続きGPT-5.5 Instant**で、GPT-5.6 Sol は対象有料プランで推論設定から選択する形式（段階的ロールアウトのため未表示のアカウントもあり）。API価格：Sol $5/$30・Terra $2.50/$15・Luna $1/$6（per 1M tokens）。3段階構成でGPT-5.5比約半額のTerraが中間価格帯を担う（CNBC / Wikipedia, 2026-07-09）
- **新モデルが出ても既定は保守的に据え置く設計**：Claude（Sonnet 5が即デフォルト化）とは対照的に、OpenAIは新フラッグシップを既定化する前に有料プラン内の選択制で慎重に展開する方針が明確になった

### Gemini（Google）

- **Gemini アプリに複数の新機能を発表**：「Daily Brief」機能・インターフェース刷新・新動画生成モデル「Gemini Omni」・パーソナルAIエージェント「Gemini Spark」を追加（Google, 2026-07）
- **Google Video Remix（2026-07-08公開）**：Google フォト内でGeminiを使い10秒動画クリップを再照明・背景差し替え・スタイライズ編集できる新機能。AI Plus・Pro・Ultra加入者が対象

### AIコーディングエージェント市場

- **料金体系の「使い放題」時代が終焉**：Cursorがクレジット課金制へ移行（Autoモードのみ無制限）。GitHub Copilotも2026年6月に「AI Credits」制へ移行。無制限プランからクレジット消費制への業界的シフトが進行（各社リリースノート, 2026-06〜07）

### このメディアへの示唆

- OpenAIは新モデルを段階的・選択制で展開する保守設計、AnthropicはSonnet 5を即デフォルト化する積極設計。「新しいモデルが出た＝みんなが使っている」わけではない点はM-04・M-09系記事で使える視点
- Cursor・Copilotのクレジット制移行は「AIツールのコストが実質的に上がっている」文脈。Claude Codeの料金体系の分かりやすさとの対比材料になる

---

## [2026-07-17] 調査結果

### ChatGPT（OpenAI）

- **ChatGPT Work公開（2026-07-09）**：接続済みのアプリ・ファイルを横断してリサーチ・作業し、文書・スプレッドシート・プレゼン・レポートを完成させる汎用エージェント機能（releasebot.io, 2026-07-09）
- **ChatGPTデスクトップアプリがChat／Work／Codexの3モード統合に刷新（2026-07-09）**：CodexアプリとChatGPTデスクトップアプリが1つに統合された（uravation.com, 2026-07-09）
- **ChatGPT Voiceを新モデル「GPT-Live-1」で刷新（2026-07-08）**：聞く・話すを同時処理でき、会話中にWeb検索・メモリを利用可能に（releasebot.io, 2026-07-08）
- **カスタム指示の文字数上限が1,500→5,000文字に拡大**：Plus・Pro・Enterprise・Business・Education対象（releasebot.io, 2026-07）
- **GPT-5.5 Instant Miniがフォールバックモデルに**：GPT-5.5 Instant／Autoのレート制限到達後の代替モデルとしてGPT-5.3 Instant Miniから置き換え。意図追跡・トーン調整・事実精度が向上（releasebot.io, 2026-07）

### Gemini（Google）

- **Nano Banana 2 Lite**：最速・低コストのGemini画像生成モデルとして追加
- **Gemini Omni Flash**：ネイティブマルチモーダルAPIをパブリックプレビューで公開
- **外部アプリ連携拡大**：OpenTable・Canva・Instacart等への接続に対応

### 国産AIライティングツール

- **Value AI Writer byGMO**：リサーチ〜構成案〜本文〜アイキャッチ〜リライトまで全工程を自動化するSEO記事生成AIとして継続展開（GMOデジロック）
- **ミエルカGEO（2026年1月リリース）**：AI経由流入の分析に特化した国産ツールとして定着しつつある

### このメディアへの示唆

- OpenAIが「ChatGPT Work」で複数アプリを横断して作業を完成させるエージェントを投入。「AIで環境を構築し、AIコンテンツで実際に動かす」というこのメディアの実況軸との対比記事が書ける（M-04の続報候補）
- 国産AIライティングツールがSEO記事の全自動生成を訴求する中、「AI設計＋人間監修」という代行の差別化軸がより明確になる

---

## [2026-06-08] 調査結果

### Hermes Agent（Nous Research）

- **概要**：オープンソースの自己進化型AIエージェント。2026年2月リリース。GitHubスター15.4万超（急成長）
- **最大の特徴**：「使えば使うほど賢くなる」。ユーザーの操作・好みを永続記憶し、タスク完了手順を「スキル」として自動保存・再利用。Claude Codeと異なりサーバーで24時間常時稼働
- **対応プラットフォーム**：Slack・Discord・Telegram・WhatsApp・Signal・CLIなど22種
- **Hermes Desktop（2026-06-03リリース）**：GUI版デスクトップアプリ。Windows/Mac/Linux対応。ターミナル不要・初回オンボーディング付きで非エンジニアも導入しやすい
- **日本展開**：GMOペパボが「ロリポップ！AIエージェントクラウド」で提供開始（月1,200円・サーバー費用込み）（impress PC Watch, 2026-06-03）
- **NVIDIA連携**：NVIDIA RTX PC・DGX Sparkを活用した自己改善型エージェント実装を発表（NVIDIA Japan Blog, 2026）

**Claude Codeとの比較**

| 軸 | Claude Code | Hermes Agent |
|---|---|---|
| 得意領域 | コーディング・ファイル操作・ライティング | 汎用タスク・マルチプラットフォーム自動化 |
| 実行モデル | セッションベース（手動起動） | 24時間常時稼働（サーバー常駐） |
| メモリ | CLAUDE.md等ファイルで手動管理 | 自動学習・永続記憶（操作から自動生成） |
| 非エンジニア向け | デスクトップGUIあり（ターミナル可） | Hermes Desktopでターミナル不要 |
| 日本での価格 | Claude Pro月約3,200円〜 | 月1,200円（GMOペパボ経由） |

**記事・Xポストへの活用可能性**
- 「Claude CodeとHermes Agent、何が違うのか」比較記事（M-04候補）
- 「使うほど賢くなるAIエージェントが来た」X速報ポスト

---

### ChatGPT / OpenAI

- **GPT-5.5（2026-04-23リリース）**：コーディング・データ分析・マルチツール横断タスクに強化。幻覚60%減・SWEベンチマーク88.7%。Pro・Business・Enterpriseユーザー向け。GPT-5.5 Instantも並行提供（正確性と簡潔さ重視）（OpenAI, gihyo.jp, 2026-04）
- **ChatGPT「Go」プラン（月約1,500円）**：無料〜Plus（月約3,200円）の中間帯。AI課金の裾野が拡大中

---

### Gemini / Google

- **AI Mode（月間10億ユーザー突破・Google I/O 2026）**：Gemini 3.5 Flashがデフォルトモデルとしてグローバル展開。クエリ数は四半期ごとに倍増
- **日本での利用率急成長**：週複数回利用比率71.6%（Claude 70.4%・Perplexity 69.2%）。ChatGPT一強から多様化フェーズへ（サイバーエージェント調べ, 2026）

---

### Apple Intelligence

- **次世代AI基盤にGemini採用**：SiriなどApple Intelligenceで活用へ。Apple独自AIとGeminiの併用モデルに移行する見通し（Ledge.ai, 2026）

---

---

## [2026-06-19] 調査結果

### OpenCode（最注目・OSSコーディングエージェント）

- **OpenCode が 160K+ GitHub スター・7.5M MAU を記録**（developersdigest.tech / abhs.in, 2026-06）：2026年6月時点で最多採用のオープンソースコーディングエージェント。6月時点では176,017 スター。Cursor を抜いて最初の大きな disruption を起こした
- **特徴**：75+ AIプロバイダーに対応（Claude・GPT・Gemini・DeepSeek・Ollama等）。LSP統合でコンパイラのリアルタイム診断をモデルへフィードバック（他ツールにはない機能）。SQLiteで会話を保存し、MITライセンスでフルOSS。エアギャップ展開（regulated industries向け）対応（developersdigest.tech, 2026-06）
- **Claude Code との差別化**：OpenCode はモデル非依存で切り替えが自由。Claude Code は Anthropic エコシステムとの深い統合・Claude 特有の安全制限対応・企業向けツールが強み。「どちらが正解か」ではなく「何を優先するか」の選択軸になってきた

### Gemini CLI / Google

- **Gemini CLI が 2026-06-18 でサービス終了**（morphllm.com / lushbinary.com, 2026-06）：後継は **Antigravity CLI**（Go 製・非同期ワークフロー・統一アーキテクチャ）。Antigravity 2.0（5/19リリース）では動的サブエージェント・スケジュールバックグラウンドタスク・公開 SDK・Gemini 3.5 Flash 対応

### OpenAI / GPT

- **GPT-5.5 の市場評価が固まってきた**（morphllm.com, 2026-06）：Terminal-Bench 2.0 でスコア 82.7%。GPT-4.5比でハルシネーション 52.5% 減。OpenAI 初の完全再訓練ベースモデルとして評価が定まりつつある

### Cursor

- **Cursor が並列エージェント対応に UI を刷新（6/9確認）**（lushbinary.com, 2026-06）：Claude Fable 5 / Opus 4.8 / GPT-5.5 / Gemini 3.1 Pro 等のマルチモデル選択が可能に。「どのモデルでも動くエディタ」として再ポジション

---

---

## [2026-06-26] 調査結果

### Cursor

- **Cursor が SpaceX（xAI 子会社）に $600 億で買収**（buildfastwithai.com, 2026-06-24）：300名・年間収益 $4M→$2B を 18 ヶ月で達成した最速成長SaaS企業の一つ。xAI 傘下に入ることで Grok モデルとの統合強化が予想される。Claude Code との競合関係が資本レベルでより複雑化

### Anthropic / Claude Code

- **Anthropic が $965B 評価で資金調達・IPO 機密申請**（cnbc.com, 2026-06）：OpenAI を抜いて AI 企業時価総額首位に。Claude Code が成長を牽引していると報道

### OpenAI

- **Codex でエンタープライズ注力にシフト**：Claude Code と正面からぶつかる形。GitHub Copilot の失速が鮮明に（morphllm.com, 2026-06）
- **LLM 最適化推論チップを Broadcom と共同開発**：独自ハードウェアへの投資を加速

### Google

- **AI 開発者向けサブスクリプション $100/月 を発表**：Antigravity（旧 Gemini CLI 後継）等の開発者向けツールをバンドル。開発者取り込みを強化

---

---

## [2026-07-03] 調査結果

### OpenAI

- **GPT-5.6 ファミリーをプレビュー発表**：Sol（旗艦）・Terra（バランス・GPT-5.5 相当を約半額）・Luna（高速・低コスト）の 3 モデル構成。ただし米政府要請により約 20 の承認パートナー組織への API 限定プレビューのみ。一般向けリリース時期は未定（llm-stats.com, 2026-07）

### Google

- **Gemini 3.5 Flash が一般提供開始**：エージェント・コーディング作業向けにチューニング。サブエージェント展開・マルチステップツール使用に対応（llm-stats.com, 2026-07）
- **Google 検索ボックスを 25 年ぶりに刷新**（Google I/O 2026）：AI Mode に Gemini 3.5 Flash を搭載。トピックをバックグラウンドで監視する「検索エージェント」を発表（blog.google, 2026）

### セキュリティ・規制

- **Five Eyes（英米豪加NZ）が AI サイバーリスクに関する共同声明を発表（2026-06-22）**：「The AI Shift in Cyber Risk: Why Leaders Must Act Now」。フロンティア AI モデルを巡る安全保障上の懸念が国家レベルで顕在化

---

---

## [2026-07-10] 調査結果

### ZCode（Z.ai・新規参入）

- **Z.ai が ZCode を発表、Claude Code・Cursor・GitHub Copilot に真っ向対抗**（VentureBeat, 2026-07）：Z.aiが自社開発モデルを搭載したコーディングエージェント ZCode をリリース。Claude Code・Cursor・Copilotを競合として明示的に対抗ポジションを取る。AIコーディングエージェント市場への参入プレイヤーが一段と増加した
- **AI コーディングエージェントの競合構図（2026-07-04時点）**（lushbinary.com, morphllm.com）：Claude Code・OpenCode・Antigravity（旧Gemini CLI）・Codex・Cursor・Windsurf・GitHub Copilot・ZCode。「フロンティアモデルが収束しているため、エージェントラッパーが体験を決める」局面に移行

### Cursor

- **Cursor が iOS 版をパブリックベータ公開（全有料プラン対象）**（releasebot.io, 2026-07）：7/5までComposer 2.5ランを75%割引で提供するキャンペーンを実施。AIコーディングツールのモバイル展開が本格化
- **Cursor が Continue（オープンソースのGitHub Copilot代替）を買収**（thenewstack.io, 2026-07）：ContinueはGitHub CopilotのOSS代替として開発者コミュニティで普及していたツール。CursorがOSSエコシステムの取り込みに動き、Claude Code・Copilotとの差別化を強化
- **Cursor が Automations（常時オンエージェント）を追加**：反復タスクを処理する常時稼働エージェント機能と、GitHub・Slackトリガーの拡充、クラウドエージェントでコンピュータ使用に対応

### Windsurf → Devin Desktop にリブランディング

- **Windsurf がブランド名を Devin Desktop に変更**（lushbinary.com, 2026-07）：AIコーディングエージェント市場で「Devin」ブランドへの統合が進行。ツール名の変遷が加速しており、市場の再編・統合フェーズに入っている

### OpenAI

- **GPT-5.6 ファミリー（Sol・Terra・Luna）限定プレビュー**（llm-stats.com, 2026-07）：Sol（旗艦）・Terra（バランス型・GPT-5.5の約半額相当）・Luna（高速・低コスト）の3モデル構成でプレビュー発表。米政府要請により約20の承認パートナーへのAPI限定プレビュー段階。一般向け時期は未定
- **Codex がエンタープライズ注力にシフト**：Claude Code と正面衝突の構図は継続。GPT-5.6ファミリーがCodexに統合されれば競合強化が予想される

### Google / Gemini

- **Gemini 3.5 Flash が一般提供開始**（llm-stats.com, 2026-07）：エージェント・コーディング向けにチューニング。サブエージェント展開・マルチステップツール使用に最適化。Google AI Mode のデフォルトモデルとしてグローバル展開中

---

## このメディアへの示唆

- Hermes Agentは「Claude Codeの比較対象」として記事に使える。差別化ポイントが明確（コーディング特化 vs 汎用常時稼働）
- 「AIツール乱立時代にどれを選ぶか」系の記事はターゲット読者（中小企業・コンテンツ運用者）に刺さりやすい
- GPT-5.5・Gemini急成長はClaude Codeユーザーへの「比較検討層」が増えることを意味し、差別化コンテンツの需要が上がる
- ZCode参入で比較候補がさらに増加。「2026年AIコーディングエージェント全比較」系の記事需要が高まっている

---

## 記事ネタ候補（ai-tools由来）

（随時追記）
