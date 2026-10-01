# 材料シート：IT担当がいない会社がClaude Codeを入れる手順。契約・プラン・情報の扱い・最初の業務（TOP10 #3・D-番号とT-番号は未採番・スラッグは題から仮に付けた `claude-code-company-introduction-no-it-staff`）

作成：2026-10-02 07時台。**執筆可能：△（会社＝複数人に入れた実体験の記録が無い。Team／Enterpriseの契約・管理の公式条件は執筆前に取り直す）**
> **執筆側はこのシートの事実だけを使う。**ここに無い数字・体験は書かない。あるのは「一人で入れた実物」と「既に記録してある公式条件」まで。

## 1. 記事の芯

**会社にClaude Codeを入れたい担当者（IT担当がいない会社）に、契約 → プラン → 情報の扱い → 最初の業務、の順で決めることを渡す。**（`tasks/README.md` TOP10 #3の行・種類＝仕事）
- この記事でしか渡せないもの（④）：**一人で入れた実物（このリポジトリ）**＋**Team／Enterpriseの契約・管理の公式条件（執筆前に公式で確認）**
- 分け方：T-1（情報の扱い＝no.70で公開済み）・T-5（できること＝TOP10 #4）とは**「会社の契約と管理」**で分ける
- 注意：行にも`operations/theme-map.md`（20本の一覧 #9）にも、これ以上の主張は書かれていない。**「会社に入れた」実績を前提にした題ではない**（材料は「一人で入れた実物」）

## 2. この環境の実物

| 項目 | 実物 | 出どころ |
|---|---|---|
| 使っている人数 | **1人**（コミットの作者は`nagaitaka4` 1,197件と`Claude` 27件）。`research/trends.md`にも「このアカウント（Max・1人運用）」 | `git shortlog -sn`（2026-10-02）／`research/trends.md` 487行 |
| 始めた日 | リポジトリの最初のコミットは**2026-03-27**。最初の5件はテスト用ファイルとブランチの練習（`test.md`・`branch.md`・PR #1） | `git log --reverse` |
| 入れた道具（4月時点） | Visual Studio Code・GitHub Desktop・Warp・Node.js。YouTubeの解説3本を見て始めた。「全部英語で、何が起きているかわからなかった」→ ClaudeとChatGPTに画面のスクショを見せて進めた | no.9 `articles/claude-code-introduction.md`（2026-04-07公開）H2「導入前の正直な状態」「実際に導入した流れ」 |
| 契約（プラン） | **Pro → Max 5x（2026-08-04に切り替え）**。Max 5xは月110ドル（消費税込み・月払いのみ）。ChatGPT Plus 月20ドルと合わせて月130ドル | `claude-subscription-pro-vs-max-facts.md` 2節／`in-house-vs-outsource-cost-facts.md` 2節（2026-10-01に実Chromeで確認）／X `Max-気`（8/5投稿） |
| 情報の扱い | 「AIモデルの改善に協力する」の設定は**2026-09-14 14:30時点でオン → 14:53にオフ**。渡しているもの6項目・渡していないもの（パスワード・認証情報・カード等）は決めてある。案内どおりに進めてAPIキーを渡してしまい、作り直した（9/22の本人申告） | `claude-company-data-training-facts.md` 1〜2節／no.70 |
| 許可の設定 | 全体（`~/.claude/settings.json`）：`defaultMode` auto・許可80件・確認5件・拒否6件／このプロジェクト（`.claude/settings.local.json`）：許可331件。**2026-09-11の記録は「許可80・確認6・拒否0」で、今日数えた値と違う** | 2026-10-02にCCが設定ファイルを数えた／no.71 |
| 最初に任せた業務（記録で分かる範囲） | 3/30のコミットが「記事の追加」と「SEOルール・サービス・ワークフロー・書き方の文書の追加」。4/3に記事#8と運用ルール | `git log --reverse`（3/27〜4/3） |
| いまの環境の大きさ | CLAUDE.md 139行／`rules/` 4ファイル2,338行／メモリのファイル119個（索引を含む）／`operations/*.py` 16本／コミット1,223件（3月12・4月21・5月126・6月90・7月136・8月313・9月498） | 2026-10-02にCCが数えた |

**⚠️ 無いもの**：会社（複数人）に入れた実体験の記録なし。Team／Enterpriseを契約・試用した記録なし。入れるのにかかった時間の記録なし（3/27の最初のコミットからno.9公開の4/7まで11日、とまでしか言えない）。契約の名義・支払い方法の記録なし。

## 3. 公式の一次情報

**新しく調べていない。既にリポジトリに記録してあるものの転記。**

| # | 事実 | 出典（verbatim） | 取得日・記録の場所 |
|---|---|---|---|
| 1 | Team・Enterprise・APIは、送った内容を学習に使わない（客が提供を選んだ場合を除く）。Free・Pro・Maxは設定がオンなら学習に使う | [code.claude.com/docs/en/data-usage](https://code.claude.com/docs/en/data-usage)：`Commercial users: (Team and Enterprise plans, API, 3rd-party platforms, and Claude Gov) maintain existing policies: Anthropic does not train generative models using code or prompts sent to Claude Code under commercial terms, unless the customer has chosen to provide their data to us for model improvement` | 2026-09-14（`claude-company-data-training-facts.md` 3-1） |
| 2 | Teamは2〜150名向け。席は2種類 | [claude.com/ja/pricing](https://claude.com/ja/pricing)：「2〜150名のチーム向け」「スタンダードシート $20 年払い時のシートあたり月額。月払いの場合は $25」「プレミアムシート スタンダードシートの5倍の使用量 $100」／比較表の英語ページ `No model training on your content by default` | 2026-09-20（同 3-6）。**日本語ページも米ドル表記** |
| 3 | 日本から開いたときの料金表示（税込みと見られる額） | [claude.com/pricing](https://claude.com/pricing)：Team標準 `$22`（`$27.50 if billed monthly.`）／Teamプレミアム `$110`（`$137.50 if billed monthly.`） | 2026-08-27（`research/trends.md` 1044行）。**9/12の記録は税抜表示で標準$20／$25・上位$100／$125・Enterprise $20/席＋API課金**（427行） |
| 4 | Enterpriseの料金 | `$20/seat/month, billed annually. Usage cost scales with model and task` | 2026-09-20（同 3-6）。**WebFetchの要約。原文を開いて確認してから使う** |
| 5 | Pro・Maxを仕事に使うこと自体を禁じる条項は無い。会社のメールアドレスで作ったアカウントは、会社の管理下に入ることがある | [Consumer Terms](https://www.anthropic.com/legal/consumer-terms)（Effective October 8, 2025）：`For clarity, this does not include Claude.ai or Claude Pro use for individuals or entities.` ／ `Business Domains. If you use an email address owned by your employer or another organization, your Account may be linked to the organization's Anthropic enterprise account, and the organization's administrator may be able to monitor and control the Account, including having access to Materials` | 2026-09-20（同 3-5） |
| 6 | 保持期間：Team・Enterprise・APIは標準30日 | `Commercial users (Team, Enterprise, and API): Standard: 30-day retention period` | 2026-09-22（同 3-1の追記） |
| 7 | メモリの初期値はプランで違う | [Claude Apps リリースノート](https://support.claude.com/en/articles/12138966-release-notes) August 25, 2026：`Memory is on by default for Free, Pro, and Max plans and off by default for Team and Enterprise organizations.` | 2026-08-28（`research/trends.md` 1025行） |
| 8 | コネクタの認証を管理者がまとめて管理できる | [@ClaudeDevs 2026-08-25](https://x.com/ClaudeDevs/status/2091953609185657251)：`Enterprise-managed auth for MCP connectors is now generally available.` | 2026-08-25（`research/trends.md` 1090行） |
| 9 | Claude CodeはPro・Maxに含まれる | support.claude.com「Use Claude Code with your Pro or Max plan」 | no.72で確認済み（`in-house-vs-outsource-cost-facts.md` 3-3）。**verbatimの記録なし** |

**⚠️ 該当の記録なし（執筆前に取り直す）**：Teamの管理画面でできること（メンバーの追加・請求・権限）／TeamのどちらのシートでClaude Codeが使えるか／Enterpriseの契約条件（最少人数・SSOなど）／支払い方法（請求書払いの可否）。

## 4. X編集部の在庫

`python3 operations/x-article-sync-check.py`（2026-10-02）：**この行は「X側の材料」を明記していない16件の1つ**。`knowledge/x/queue.md`・`sns/posts-stock.md`・`knowledge/x/published.md`を「導入」「会社」「Team」「契約」でgrepした結果、**会社にClaude Codeを入れる話の下書き・投稿は0本**。近い題材は次のとおり。

| ID | 中身 | 状態 |
|---|---|---|
| `Max-気` | 昨日、ClaudeをProからMaxにしました | 8/5投稿済み（27ビュー） |
| `PLAN27-リ` | Claude CodeはProでも既定がOpus 5.5。Max 5xは料金も量も5倍 | 在庫。9/26に盲検3回不合格 |
| `TRAIN-気` | 「モデル改善に協力する」、自分はオンのままでした | 9/22投稿済み |
| `PASS70-01` | 「渡す」の範囲。コネクタでつないだ中身は学習の対象外 | 在庫（出せる） |
| `ALLOW71-01` | 「次から聞かなくていい」と許可した操作が331件 | 在庫。盲検未合格 |
| `士_HR3` | 環境を作るのが難しそうだった。難しかったのは操作ではなく仕事の整理（導入ハードル） | `sns/posts-stock.md`。GPT提案の草案で、実体験・数字は未確認 |

リプライの記録：8/17に`@ai_moshimur`の記事「個人でAIを使うのと、会社にAIが入るのは、別物だった。」（29,265ビュー）へ返信している（`knowledge/x/published.md` 157行）。

## 5. 既存記事との重なり

| 記事 | 重なる所 | 扱い |
|---|---|---|
| no.70 `claude-company-data-training` | H2「会社で使うと、Claude Pro・MaxとTeamは何が違うか」が**プランと情報の扱いで重なる** | 情報の扱いはno.70へリンク。この記事は契約と管理の手順 |
| no.9 `claude-code-introduction` | H2「実際に導入した流れ」（個人の導入体験）。**TOP10 #4で全面改稿の予定** | 導入の流れを#3と#4で2回書かない |
| no.27 `claude-subscription-change-june-2026` | 個人のプラン選び（Pro／Max 5x） | 隣。個人のプランはno.27へ |
| no.71 `claude-code-permission-modes` | 許可のモード | 隣 |
| no.62 `ai-work-environment-setup` | 環境を作る5ステップ | 隣（概念） |

**判定：題名に「導入」「会社」を含む記事は0本で、「会社としてどう契約して入れるか」に答える記事はまだ無い。同じ問いに2本で答える形にはならない。**ただしno.70のH2と1節ぶん重なるので、そこはリンクで分ける。

## 6. 需要

- サジェスト（`operations/site-status.md` 2026-09-11 12時台取得）：`claude code 導入`10件（方法／windows／支援／手順／企業）・`claude code 事例`9件（活用 事例／導入 事例／活用 事例 非エンジニア）・`claude code 一人`5件（会社／社長／起業）
- サジェスト（同 2026-09-12 17時取得）：`claude 導入`6件（方法／企業／事例）。**0件：`claude 導入 中小企業`**
- `operations/theme-map.md`（2026-09-12）：`claude 業務利用`6・`claude 社内`5・`claude 中小企業`5
- 自サイトのGSC：**未計測**（`site-status.md`に「導入」を含むクエリの記録なし。受け皿の記事が無い）

## 7. まだ無いもの（本人にしか答えられないこと・未計測）

1. **会社（複数人）にClaude Codeを入れた経験があるか。**リポジトリにあるのは1人運用の記録だけ。無ければ「一人で入れた実物＋公式条件」で書く
2. **Team／Enterpriseを契約・試用したことがあるか。**記録なし。無ければ公式条件だけを書き、体験として書かない
3. **契約の名義と支払い。**個人名義か屋号か・経費にしているか・領収書をどう受け取っているか（記録なし）
4. **最初に任せた業務と、その理由。**記録では3/30に記事とルール文書を追加している。本人の記憶と合うか
5. **未計測**：入れるのにかかった時間／自サイトのGSC（受け皿なし）／3節末尾の公式条件4点
