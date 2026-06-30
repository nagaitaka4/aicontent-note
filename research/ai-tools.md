# 競合AIツール・新興ツール動向

最終更新: 2026-06-08

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

## このメディアへの示唆

- Hermes Agentは「Claude Codeの比較対象」として記事に使える。差別化ポイントが明確（コーディング特化 vs 汎用常時稼働）
- 「AIツール乱立時代にどれを選ぶか」系の記事はターゲット読者（中小企業・コンテンツ運用者）に刺さりやすい
- GPT-5.5・Gemini急成長はClaude Codeユーザーへの「比較検討層」が増えることを意味し、差別化コンテンツの需要が上がる

---

## 記事ネタ候補（ai-tools由来）

（随時追記）
