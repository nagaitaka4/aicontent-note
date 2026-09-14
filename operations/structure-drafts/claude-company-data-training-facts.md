# 材料シート：Claudeに会社の情報を渡して大丈夫か。学習に使われる条件と、自分が渡しているもの・渡さないもの（TOP10 #4・D-27・T-1）

作成：2026-09-14 14:35（編集会議C-3の途中で、CCが公式ページと実際の設定画面を確認して作成）。**執筆可能：△（7節の①②が埋まれば◯。4・5節は埋めた）**
> **執筆側はこのシートの事実だけを使う。ここに無い数字・仕様は書かない。**法律・規約の話は「一次情報が言っていること」と「自分が決めたこと」を分ける。

## 1. 記事の芯（2026-09-14・仮置き。C-3の回答で確定する）

**Claudeに入れたチャットとClaude Codeの作業が「AIの学習に使われるか」は、設定ひとつで決まる。**Free／Pro／Maxは「AIモデルの改善にご協力ください」がオンだと学習に使われ、データは5年保持。オフだと新しいチャット・セッションは学習に使われず、30日保持。

**本人の実物**：2026-09-14 14:30時点で、このアカウント（Max）の設定は**オン**だった（CCが実際の設定画面を読んで確認）。「会社の情報を渡して大丈夫か」を書く本人が、オンのまま仕事の情報を入れていた——**C-3の回答（2026-09-14 14:36）：「デフォルトでオンになったままだから、気づかずにオンにしたままだった」**。本人の理解：Anthropicが自社のAIモデルの開発に使うことに、ユーザーが協力するかどうかの設定（合っている）。⚠️ 「既定でオン」は本人の認識。公式の一次情報は3-4で執筆前に確かめる。

読者＝会社の情報（取引先名・経費・顧客の資料）をClaudeに入れてよいか迷っている非エンジニア・個人事業主。渡すのは「学習に使われる条件」「どこで確かめるか」「自分は何を渡して何を渡していないか」「変えるなら何が変わるか」。

## 2. この環境の実物（2026-09-14）

| 項目 | 実物 | 使い方 |
|---|---|---|
| 設定の状態 | `claude.ai/settings/data-privacy-controls`（設定 → プライバシー）の「AIモデルの改善にご協力ください」＝**オン**（2026-09-14 14:30・実Chromeで`aria-checked="true"`を読んだ）。同じ画面の「ロケーションメタデータ」もオン | 記事の芯。⚠️ 既定がオンなのか本人がオンにしたのかは未確認（7節） |
| Claudeに渡しているもの（リポジトリの記録から） | `business-ops`：領収書PDF（取引先名・金額・2025/06〜12）と経費台帳70行／`sales/leads-raw.md`・`leads-scored.md`：ハローワーク求人から抽出した会社名（スコア済み7件）／`logo-system`：案件の参考ロゴ・制作ルール／このリポジトリ：記事本文・GSCの数字・X投稿 | 「自分が渡しているもの」の実物。**一覧は本人確認が要る（7節②）** |
| 渡していないもの（ルールで決めている） | パスワード・認証情報（CCはログインしない・入力しない：`rules/article-flow.md` 7.6・メモリ`feedback_wp_entry_by_cc`）／クレジットカード等の財務情報 | 「渡さないもの」の実物 |
| ローカルに残るもの | Claude Codeのセッション記録は`~/.claude/projects/`に平文で30日保存（公式・3-1）。この環境では`ai-trends-daily`など定期実行の記録も同じ場所 | 「Anthropicに渡す」以外に「自分のPCに残る」も書く |

**⚠️ 無いもの**：オンにした日（記録なし）。渡した情報の件数（数えていない）。

## 3. 公式の一次情報（2026-09-14 14:30取得。verbatimは原文どおり）

| # | 確かめること | 取れたもの（verbatim） | 状態 |
|---|---|---|---|
| 3-1 | 学習に使う条件・保持期間（Claude Code公式「Data usage」・[code.claude.com/docs/en/data-usage](https://code.claude.com/docs/en/data-usage)） | 「**Consumer users (Free, Pro, and Max plans)**: We give you the choice to allow your data to be used to improve future Claude models. We will train new models using data from Free, Pro, and Max accounts when this setting is on (including when you use Claude Code from these accounts).」／「**Commercial users**: (Team and Enterprise plans, API, 3rd-party platforms, and Claude Gov) maintain existing policies: Anthropic does not train generative models using code or prompts sent to Claude Code under commercial terms, unless the customer has chosen to provide their data to us for model improvement」／「Users who allow data use for model improvement: 5-year retention period」「Users who don't allow data use for model improvement: 30-day retention period」「Privacy settings can be changed at any time at claude.ai/settings/data-privacy-controls.」／「Local caching: Claude Code clients store session transcripts locally in plaintext under `~/.claude/projects/` for 30 days by default to enable session resumption. Adjust the period with `cleanupPeriodDays`.」 | ◯ |
| 3-2 | 設定の名前と、オン／オフで何が変わるか（プライバシーセンター「How do I change my model improvement privacy settings?」・[privacy.claude.com/en/articles/12109829](https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings)） | 設定名「Help Improve our AI models」／場所「Settings > Privacy」／オン「we will use your data to improve Claude」／オフ「we will not use any new chats and coding sessions you have with Claude for future model training」／**「Your data will still be included in model training that has already started and in models that have already been trained」**／対象「Claude Free, Pro, Max and when accounts from those plans use Claude Code」 | ◯（WebFetchの要約。**執筆前に原文ページを開いて読み直す**） |
| 3-3 | 画面の実物（日本語UI・2026-09-14 14:30） | 設定 → プライバシー →「AIモデルの改善にご協力ください」。説明文「チャットやコーディングセッションのデータをAnthropic AIモデルの訓練と改善に使用することを許可します。」（「詳細はこちら」→3-2の記事）。同じ画面に「ロケーションメタデータ」「データをエクスポート」「アップロード済みファイル」「記憶設定」 | ◯ |
| 3-4 | 既定がオンかオフか（新規アカウントの初期値） | 未取得。3-2の記事か消費者向け利用規約で確かめる。**取れなければ「自分のアカウントはオンだった」とだけ書く** | 未 |
| 3-5 | Pro／Maxを仕事（商用）に使ってよいか（Consumer Termsの該当条項） | 未取得。[Consumer Terms](https://www.anthropic.com/legal/consumer-terms)を原文で | 未 |
| 3-6 | 会社で使うならTeam／Enterprise（学習に使わない）の条件・料金 | 未取得。公式の料金ページを執筆前に | 未 |

## 4. X編集部の在庫

- 該当なし（2026-09-14 14:40：`knowledge/x/queue.md`・`ideas.md`を「学習」「セキュリティ」「機密」「情報漏洩」でgrep → 下書き・取材待ちとも0本。`x-article-sync-check.py`にもこの題材の未連携なし）

## 5. 既存記事との重なり

- 題名に「学習」「セキュリティ」「機密」「安全」を含む記事：0本（2026-09-14 14:40 grep）
- H2で触れている記事：no.49 弁護士編「案件情報を預けても安全なのか」／no.53 社労士編「顧客の労務情報を、安全に運用するには」（士業の文脈で1節ずつ）。**この記事は一般の答え＋自分の設定の実物。士業2本へはリンクで逃がす**（同じ読者の問いに2本で答える形にしない）

## 6. 需要（2026-09-12実測・テーママップ段階1）

`claude セキュリティ`10・`claude 商用利用`10・`claude データ 学習`10（させない／オフ）・`claude 安全性`10・`claude 情報漏洩`6・`claude 機密`6・`claude 業務利用`6・`claude 社内`5・`claude 個人情報`5・`claude code セキュリティ`10・`claude code 機密`5／GSC：`claude security 費用`1表示（2026-09-14）

## 7. まだ無いもの（執筆で埋めない）

1. ~~本人の理由~~ → 回答済み（気づかずにオンのまま）。**残り：このまま（オン）にするか、オフにするか、その理由**（1行でよい）
2. **渡しているものの一覧の本人確認**（2節の表に抜け・出したくないものがあるか）
3. 3-4（既定の値）・3-5（商用利用の条項）・3-6（Team／Enterprise）の一次情報
