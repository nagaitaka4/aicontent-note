# no.70 執筆プロンプト（ChatGPT Work（GPT-6 Astra）へ渡す本文・Astra実験）

**実験の設計**：構成＝CC → 執筆＝Astra と CC の両方 → `article-self-check.py` のNG件数・事実の誤り件数（下の「書いてはいけないこと」に当たる文の数）・修正回数・所要時間を比べ、良いほうを公開（`operations/measurement-calendar.md`・V-04の再現）。
**実行環境（2択・2026-09-21）**
- **A：Codex（リポジトリ `aicontent-note` を接続）**。新しいスレッドで、次の1行だけを貼る（「執筆してください」だけでは不足。他のルールファイルを読みに行って指示が薄まる）：
  `articles/no70_writing_prompt.md の指示だけを根拠に記事の初稿を書いてください。文体見本は articles/ai-how-to-use-10-questions.md を読んでください。それ以外のファイル（rules/・knowledge/・operations/・他の記事）は読まないでください。出力は articles/no70_astra_draft.md に保存し、コミットはしないでください。`
  **モデル**：Codexの一覧にAstraは無い（2026-09-21実測：5.6 Sol〔既定〕／5.6 Terra／5.6 Luna／5.5）。**既定の 5.6 Sol を使う**。思考量は「高」があればそれを選ぶ。使ったモデル名と思考量をここに記録する：＿＿＿
- **B：ChatGPT Work（GPT-6 Astra）**。新しいスレッド・リポジトリは接続しない（`operations/gpt-writing-prompt.md`）。①下の「---」以降を全部貼る ②文体見本として `articles/ai-how-to-use-10-questions.md`（no.69）をファイル添付する（本文はペーストしない）。
**記録**：Astraの出力は `articles/no70_astra_draft.md` に保存し、CCの初稿 `articles/claude-company-data-training.md` と並べて判定する。開始時刻・終了時刻をここに追記する。

---

あなたはブログメディア「AIコンテンツ運用ノート」の編集ライターです。
確定済みの構成案と、下に書き出した事実だけを根拠に、記事の初稿をMarkdownで書いてください。**ここに無い事実・数字・仕様・条項は書かないでください。**

このメディアは「AIで環境を構築し、AIコンテンツで実際に動かしている」実況メディアです。「AIで稼ぐ方法」を教えるメディアではありません。読者は非エンジニアの個人・中小企業で、コンテンツ運用に課題がある人です。

## 出力の仕様

- Markdown形式。H1が1つ、H2が本文の章、必要に応じてH3
- frontmatterから書き始め、記事の最後（関連記事）まで一度に出力する
- 想定分量は3,400〜3,900字（本文のみ・空白除く）。**文字数のために内容を削らない。**削ってよいのは冗長（言い換え・二重説明・水増し）だけ

## frontmatter（この内容をそのまま使う）

```
---
no: 70
series:
series_no:
title: Claudeに会社の情報を渡して大丈夫か。データが学習に使われる条件
date:
url: https://aicontent-note.com/claude-company-data-training/
slug: claude-company-data-training
status: draft
description: Claudeのデータは学習に使われるのか。Free・Pro・Maxでは「AIモデルの改善にご協力ください」の設定で、通常のチャットやClaude Codeをモデル改善に使うか選べます。私は気づかずオンのまま取引先名や領収書を入れていたので、公式の条件と自分の運用を分けて書きます。
eyecatch_alt: Claudeに会社の情報を渡して大丈夫か、データが学習に使われる条件と自分の設定を確かめた記事のアイキャッチ画像
category: Claude Code活用
tags: Claude,Claude Code,データ学習,プライバシー設定,非エンジニア
eyecatch: eyecatch_0070.png
---
```

## 【最重要】この記事で絶対に外さないこと

1. **「設定ひとつで決まる」と言い切らない。**Free・Pro・Maxでは「通常のチャットやClaude Codeの内容が学習に使われるかは、モデル改善の設定で変わる」まで。例外（Incognito・安全性レビュー・フィードバック）がある
2. **「実際に学習に使われた」と書かない。**筆者が確認できたのは「モデル改善を許可する設定がオンだった」まで。「モデル改善の対象になり得る設定のままだった」「オンの状態で送っていた」と書く
3. **「オフにした後、過去のチャットを再開すると学習の対象になる」と書かない。**現行の公式は、オフにすると保存済みの過去のチャットも今後の学習に使わない
4. **「既定でオン」と書かない。**公式に既定の記述は無い。書けるのは「私のアカウントはオンだった。選んだ記憶がない」まで
5. **「仕事に使うことは禁止されていない」という法的結論を書かない。**規約から言えるのは「個人でも法人でもClaude.ai／Proの利用は消費者向け規約の範囲」まで
6. **Teamを勧めない。**「一人ならPro・Max＋オフ、複数人ならTeam」も書かない。条件を並べて読者が選ぶ
7. **「オフにしたから安全」と書かない。**この記事は「学習に使われるか」だけを扱う。情報漏洩・暗号化・端末管理へ広げない
8. **制作の記録を出さない。**日付（2026-09-14 など）・編集会議・ファイル名・行数・前回の記事名は本文に書かない。「気づかずオンだった → オフにした」は事実としてだけ書く
9. **実際の会社名・金額・案件名・ロゴ画像を出さない。**「取引先の会社名」「領収書PDF」「制作中の案件データ（ロゴ案・制作ルール）」の一般名で書く
10. **「顧客の氏名・住所は渡していない」など、下の表に無い項目を「渡していないもの」に足さない**

## 使ってよい事実（この範囲だけ。各項目の札＝〔全体〕〔オン時〕〔オフ時〕〔例外〕〔本人〕）

### 事実1〔全体〕学習に使う条件・保持期間（出典：Claude Code公式「Data usage」 https://code.claude.com/docs/en/data-usage ）

原文：
- 「Consumer users (Free, Pro, and Max plans): We give you the choice to allow your data to be used to improve future Claude models. We will train new models using data from Free, Pro, and Max accounts when this setting is on (including when you use Claude Code from these accounts).」
- 「Commercial users: (Team and Enterprise plans, API, 3rd-party platforms, and Claude Gov) maintain existing policies: Anthropic does not train generative models using code or prompts sent to Claude Code under commercial terms, unless the customer has chosen to provide their data to us for model improvement」
- 「Users who allow data use for model improvement: 5-year retention period」「Users who don't allow data use for model improvement: 30-day retention period」
- 「Privacy settings can be changed at any time at claude.ai/settings/data-privacy-controls.」

### 事実2〔オン時〕5年保持はオンにした後の新規・再開したチャットにだけ適用（出典：プライバシーセンター「How long do you store my data?」 https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data ）

原文：「If you allow us to use your chats or coding sessions to improve Claude, we may retain your data in a de-identified format for up to 5 years in our model training pipelines. This retention period only applies to new or resumed chats after the model training setting has been enabled.」
※この「new or resumed」は**オンにしたときの適用範囲**の話。オフ後の説明に使わない。

### 事実3〔オフ時〕オフにすると何が変わるか（出典：同上、および「How do I change my model improvement privacy settings?」 https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings ）

原文：
- 「If you decide to turn off the model improvement setting, we will not use your previous or new chats or coding sessions for future model training. Additionally, if you delete a chat from your chat history, it will not be used to train future models. Your data will still be included in model training runs that are already in progress, or in models that have been trained.」
- 「If you decide to turn off the model training setting, we will not use any new chats and coding sessions you have with Claude for future model training. Your data will still be included in model training that has already started and in models that have already been trained, but we will stop using your previously stored chats and coding sessions in future model training runs.」
- 対象：「Claude Free, Pro, Max and when accounts from those plans use Claude Code」
- 削除したチャット：「When you delete a conversation it's: Removed from your chat history immediately / Deleted from our back-end storage systems within 30 days」

### 事実4〔例外〕オフでも使われるもの・オンでも使われないもの

- 安全性の分類器に引っかかった会話（出典：事実3の12109829）：「If our safety classifiers flag your conversations, they may still be used to improve our internal trust and safety models, detect harmful content, enforce our policies, or advance our safety research.」
- フィードバック（出典：Consumer Terms）：「Even if you opt out, we will use Materials for model training when: (1) you provide Feedback to us regarding any Materials, or (2) your Materials are flagged for safety review to improve our ability to detect harmful content, enforce our policies, or advance our safety research.」
- Incognitoチャット（出典：プライバシーセンター「Is my data used for model training?」 https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training ）：「Your Incognito chats are not used to improve Claude, even if you have enabled Model Improvement in your Privacy Settings.」**Incognitoの保持日数は書かない（消費者向けページに記述が無い）。脚注1行で触れるだけ。主役にしない**
- 「ロケーションメタデータ」は同じ画面にある別の設定。モデル改善の設定と連動しない（筆者の画面で確認）

### 事実5〔全体〕設定の場所と名前（出典：事実3の12109829 ＋ 筆者の画面）

- 英語UI：「Under Help Improve our AI models, click the button to toggle it off/on」。手順：Select your name from your settings menu → Settings → Privacy
- 日本語UI：設定 → プライバシー →「AIモデルの改善にご協力ください」。説明文「チャットやコーディングセッションのデータをAnthropic AIモデルの訓練と改善に使用することを許可します。」
- URL：claude.ai/settings/data-privacy-controls
- 同じ画面にあるもの：「ロケーションメタデータ」「データをエクスポート」「アップロード済みファイル」「記憶設定」

### 事実6〔全体〕誰がいつ選ぶか（出典：Anthropic発表「Updates to Consumer Terms and Privacy Policy」2025-08-28 https://www.anthropic.com/news/updates-to-our-consumer-terms ）

原文：
- 「If you're a new user, you can pick your setting for model training during the signup process.」
- 「Existing users will see the choice in a pop-up window」「You can make your selection right away, or select "not now" and decide later. You have until October 8, 2025 to make your choice.」
- 「After October 8, you'll need to make your selection on the model training setting in order to continue using Claude.」
- 「These updates do not apply to services under our Commercial Terms, including: Claude for Work, which includes our Team and Enterprise plans / Our API, Amazon Bedrock, or Google Cloud's Vertex API / Claude Gov and Claude for Education」
- **既定がオンかオフかは、この記事にもプライバシーセンターにも規約にも書かれていない**

### 事実7〔全体〕消費者向け規約（出典：Consumer Terms of Service「Effective October 8, 2025」 https://www.anthropic.com/legal/consumer-terms ）

原文：
- 範囲：「Our Commercial Terms of Service govern your use of any Anthropic API key, the Anthropic Console, or any other Anthropic offerings that reference the Commercial Terms of Service. For clarity, this does not include Claude.ai or Claude Pro use for individuals or entities.」→ 言えるのは「個人でも法人でもClaude.ai／Proの利用はCommercial Termsの対象に含まれない（＝消費者向け規約の範囲）」まで
- 会社のメール：「Business Domains. If you use an email address owned by your employer or another organization, your Account may be linked to the organization's Anthropic enterprise account, and the organization's administrator may be able to monitor and control the Account, including having access to Materials (defined below). We will provide notice to you before linking your Account to an organization's enterprise account.」
- 入力する情報の権利：「Rights and Responsibilities. You are responsible for all Inputs you submit to our Services and all Actions. By submitting Inputs to our Services, you represent and warrant that you have all rights, licenses, and permissions that are necessary for us to process the Inputs under our Terms and to provide the Services to you」
- 学習利用：「Our use of Materials. We may use Materials to provide, maintain, and improve the Services and to develop other products and services, including training our models, unless you opt out of training through your account settings.」

### 事実8〔全体〕Teamの条件（出典：料金ページ https://claude.com/pricing ・日本語 https://claude.com/ja/pricing ）

- Team：「2〜150名のチーム向け」「スタンダードシート $20 年払い時のシートあたり月額。月払いの場合は $25」
- 比較表「モデルのトレーニング」：Free／Pro／Max＝「オプトアウト」、Team／Enterprise＝「No model training on your content by default」
- 料金は米ドル表記。日本語ページも円の表示なし
- **Enterpriseの料金・Teamのプレミアムシートは書かない**

### 事実9〔全体〕PC側に残る記録（出典：事実1のData usage）

原文：「Local caching: Claude Code clients store session transcripts locally in plaintext under `~/.claude/projects/` for 30 days by default to enable session resumption. Adjust the period with `cleanupPeriodDays`.」
→ 【メモ】2〜3文だけ。学習設定とは別に、Claude CodeではPC側にもセッション記録が残る、という位置づけ

### 事実10〔本人〕筆者の実物

- 使っているプラン：Max。Claude Codeを毎日使い、Claude.aiのチャットも使う
- 設定「AIモデルの改善にご協力ください」は**オンだった**。選んだ記憶がない（「後で」を押したか、読まずに通したかは分からない。分からないと書く）
- 確認した後、**オフに切り替えた**。切り替え時に確認ダイアログは出なかった。使える機能は変わらなかった。「ロケーションメタデータ」はオンのまま
- オフにした理由：取引先の会社名・領収書・案件のデータなど、自分以外の情報を日常的に入れているから。オフにしても、すでに始まっている学習からは外れないと分かったうえで決めた
- 渡しているもの・渡していないもの（この6項目だけ。足さない）：

| 種類 | 実物の例 | 渡している？ | 決めた理由 |
|---|---|---|---|
| 取引先の会社名 | 営業リスト・求人情報から抽出した会社名 | 渡している | 分類・優先づけをAIに任せるため |
| 領収書・経費台帳 | 領収書PDF（取引先名・金額）・経費台帳 | 渡している | 仕訳と集計を任せるため |
| 制作中の案件データ | ロゴ案・制作ルール | 渡している | 制作の下書きを任せるため |
| 自分のメディアのデータ | 記事本文・検索の数字・X投稿 | 渡している | 自分の情報なので迷わない |
| パスワード・ログイン情報 | WordPress等の認証情報 | 渡していない | AIはログインしない・入力しないと決めている |
| クレジットカード・口座の情報 | カード番号・口座番号 | 渡していない | 財務情報は入れない |

- 渡しているものの半分以上（6項目のうち3項目）が「自分以外の情報」
- **無いもの（書かない）**：オンにした日／渡した情報の件数／データの保管場所・国／Incognitoの保持日数／既定の値

## 絶対に守るルール（機械チェック項目＋事実の扱い）

**事実の扱い（最優先・機械では検出できない）**
- **体験していないことを「試した」「やってみた」と書かない。**構成案に体験として書かれている内容だけが実体験
- **引用は原文どおりに書く。**要約や言い換えを、引用符や `【本】` ブロックに入れない。長くて入らない場合は「〜」の部分引用にして、残りは地の文で説明する
- 構成案にない数値・事実を書くときは、**一次情報を原文で開いて確認し、URLを本文に貼る**。確認できないものは書かない（WebFetchや検索結果の要約だけで書かない）
- **推測を断定しない。**公式が理由を説明していない事象は「背景として考えられるのは〜」と、推測であることを明示する
- 数字・事実・比較を述べるときは、根拠（出典URL・ファイル名）を併記する。数値には調査時期を添え、公開日と更新日を区別する
- **「証拠にならない」と「効果がない」を混同しない。**確かめた範囲を越えて書かない
- 業界の一般論を、自社サービスの強みのように書かない
- 「AIはこういうものだ」という断定を避ける。AIと人は対等な目線で書く

**文の長さ**
- 一文は60字以内。超えたら削るのではなく句点で切る（連用中止「〜が効き、」「〜であり、」が分割点になりやすい）
- 1つの段落は160字以内
- 1文に主題を複数入れない。対比は「AはX。逆に、BはY。」と文を分ける

**主語**
- タイトル・説明文・リード1文目・見出しで「明確なライン」のように書かない。何の線・何の基準かを付ける（例：どこまで似たらパクリかの線）

**リード**
- H1直下のリードは3文・150字以内、1文目は40字以内。1文目で検索意図に直接答える
- 各H2の直下のリードは3文・100字以内

**視覚のリズム**
- 文字だけの段落を5つ以上続けない。H3・表・箇条書き・ブロック要素が区切りになる
- 表やブロックに書いた内容を、直後の地の文で言い直さない。表の後に書くのは「そこから何が言えるか」だけ
- 同じ趣旨の但し書きを3文並べない

**記法**
- 箇条書きは `・`（`-` は使わない）。複数項目は各行末に `<br>`（空行で区切らない）
- `・` をネストしない。項目内の列挙は `A / B` と書く

**読み手**
- 「◯◯は〜としている」で行を終えない。資料が何と言ったかではなく、読み手にとって何が起きるかまで書く
- 一般的な問いに答える記事では、制作の記録（日付・会議名・ファイル名・行数・前回の記事名）を本文に出さない。経験は「たとえば〜なら〜」の一般的な答えに直して書く

**記法**
- ブロック要素は `【ブロック名】<br>` ＋内容。**`>`（Markdown引用）とHTMLコメントは使わない**
- ブロック要素は80字以内。一言で伝わる長さにする
- 使えるブロック名：ポイント／チェック／バツ印／アラート／はてな／メモ／グッド／バッド／インフォ／アナウンス／ペン／本
- 句読点の直後に半角スペースを入れない
- リンクは `[テキスト](URL)` で書く。frontmatterの `url` は生のURL文字列にする（Markdownリンクにしない）

**読点**
- 文頭の接続語（ただし・しかし・また・なお・さらに・一方・逆に・つまり・そのため・例えば）の後には読点を打つ
- 主題を示す「〜は」（当サービスは、このメディアは 等）の後にも読点を打つ。目的語（〜を）や短い副詞の直後には打たない

**禁止表現**
- 「〜しましょう」の指示形
- 「ぜひ」「▶」「お気軽にご相談ください。」
- 「ここまで説明してきました」「〜について整理すると、大きく」「〜という点が重要です」「〜ということが言えます」
- H2見出しに「まとめ」「結論」「導入」を使わない
- 一人称は「私」で統一する（「僕」「自分」を混ぜない）
- 同じ言い回し・同じ結論パターンをセクション間で繰り返さない

**frontmatter**
- タイトルは35字以内（理想30〜33字）。KWの語彙をそのまま前方に置く
- description は120〜140字。記事の結論を含める

**CTA・関連記事**
- CTA文言は最新published記事からそのままコピーする。途中1回・末尾1回で、間にH2を3つ以上入れる
- 記事末尾の関連記事は3本

## 文体

- 丁寧体が基本。ところどころ常体が混ざってよい
- 現実ベース・実体験重視。誇張しない・煽らない。ただしワクワク感は残す
- 断定を避ける（「〜気がしています」）。本音を出す（「正直に言うと」）
- 軽い自虐は1〜2箇所まで、短文で落とす。ネガティブの後には前を向く一文を置く
- 小難しい言い回し・論文調の抽象表現を使わない。読者が自分の状況をそのまま想像できる具体形で書く
- 「AIはこういうものだ」という断定を避ける。AIと人は対等な目線で書く
- 引用は原文（英語）どおりに書く。日本語に訳して引用符に入れない。訳は地の文で「〜という意味です」と添える
- 締めに筆者の感覚を一般ルールとして載せない。「私はこう決めた」に留める

## 構成（この見出しと順序で書く。→ は構成意図。見出しには「①②」「→」を入れない）

```
# Claudeに会社の情報を渡して大丈夫か。データが学習に使われる条件
（34字・案A）

（リード3文・116字。1文目41字＝40字以内。「設定ひとつで決まる」と言い切らない＝例外〔Incognito・安全性レビュー・フィードバック〕と矛盾させない）
Free・Pro・Maxでは、通常のチャットが学習に使われるかは設定で変わります。
Claude Codeも対象で、設定名は「AIモデルの改善にご協力ください」です。
私はこの設定が気づかずオンのまま、取引先名や領収書を入れていました。

## 通常のチャットが学習に使われるかは、プランと設定で決まる
→ 答えを最初の1行に置く（マーカー候補：==通常のチャットが学習に使われるかは、プランと「AIモデルの改善にご協力ください」の設定で決まる==）
→ 表1：プラン ／ 学習に使われるか ／ 保持期間 ／ 根拠（公式リンク）
   ・Free・Pro・Max（Claude Codeをこのアカウントで使う場合も含む）＋設定オン → 使われる ／ 5年
   ・Free・Pro・Max＋設定オフ → 新しいチャット・セッションは使われない ／ 30日
   ・Team・Enterprise・API → 既定で使わない（Commercial Termsの範囲）／ 別の規定
   （根拠：Claude Code公式「Data usage」・プライバシーセンター「How long do you store my data?」・料金ページ）
→ 表の脚注1行：※Claude.aiのIncognitoチャットは例外で、モデル改善の設定がオンでも学習には使われない（プライバシーセンターverbatim）。Incognitoは主役にしない（Claude Codeの話ではない）
→ 表の後に言えることだけ2文：「Claudeだから危ない／安全」ではなく、どのプランをどの設定で使っているかで答えが変わる。有料（Pro・Max）でもオンなら使われる
→ 権利の2文（オフ＝何でも入れてよい、の誤読を防ぐ）：ただし、学習に使われない設定なら何でも入力してよい、という意味ではありません。AnthropicのConsumer Termsでは、入力する情報について必要な権利や許可を持つことを利用者側に求めています。（verbatim「you represent and warrant that you have all rights, licenses, and permissions that are necessary for us to process the Inputs」＝シート3-8。**ここから先のセキュリティ全般へは広げない**）
→ 【ポイント】プランの名前ではなく、設定の状態で決まる（80字以内）
→ ⚠️ ここで公式の条件を全部出し切る。後の見出しで公式の条件を言い直さない

## オンかオフか、どこで確かめるか
→ リード（3文・100字以内）：設定の場所と名前。1分で確かめられる
→ 手順（1. 2. 3.）：右上の自分の名前 → 設定 → プライバシー →「AIモデルの改善にご協力ください」（英語UIは Help Improve our AI models）。URL直接 claude.ai/settings/data-privacy-controls
→ 画像1枚：設定画面（ユーザーが撮る）。キャプションに「オフの状態」
→ 「既定でオンか」への答え（読者の次の疑問）：公式は「既定はオン」とは書いていない。新規ユーザーはサインアップ時に選ぶ。既存ユーザーは2025年10月8日までにポップアップで選び、以後は選ばないと使い続けられない（発表記事のverbatim）。**私は選んだ記憶がないままオンになっていた**（「後で」を押したか、読まずに通したかは分からない。分からないと書く）
→ 【チェック】自分のアカウントの設定を、今この場で見る（80字以内）

## 私が渡しているもの・渡さないもの
→ リード：「会社の情報を入れていいか」を書いている本人が、オンのまま何を入れていたか。体験は圧縮（この記事の3割以内）
→ 表2：種類 ／ 実物の例 ／ 渡している？ ／ 決めた理由
   ・取引先の会社名（営業リスト・求人から抽出した会社名） ／ 渡している ／ 分類・優先づけをAIに任せるため
   ・領収書PDF・経費台帳（取引先名・金額） ／ 渡している ／ 仕訳と集計を任せるため
   ・制作中の案件データ（ロゴ案・制作ルール） ／ 渡している ／ 制作の下書きを任せるため
   ・自分の記事本文・検索の数字・X投稿 ／ 渡している ／ 自分の情報なので迷わない
   ・パスワード・ログイン情報 ／ 渡していない ／ CCはログインしない・入力しないと決めている
   ・クレジットカード・口座の情報 ／ 渡していない ／ 財務情報は入れない
   （✅ 9/21本人確認済み：この6項目で確定・追加しない。実際の会社名・金額・案件名・ロゴ画像は出さない。**「顧客の氏名・住所は渡していない」など確認していない項目を「渡していないもの」に足さない**）
→ 表の後に言えることだけ：渡しているものの半分以上が「自分以外の情報」だった。それを、モデル改善を許可する設定がオンの状態で送っていた（⚠️ **「実際に学習に使われた」と断定しない**。確認できるのは「設定がオンだった」まで）
→ 「Anthropicに渡る」以外に「自分のPCに残る」を【メモ】2〜3文だけ：学習設定とは別に、Claude CodeではPC側にもセッション記録が残る。~/.claude/projects/ に平文で標準30日（cleanupPeriodDays で変更）。**暗号化・情報漏洩・端末管理へ広げない**
→ 内部リンク：士業の読者向けに no.49 弁護士・no.53 社労士へ（「顧客の情報を預けて安全か」はこの2本で職種ごとに書いている）

---（途中CTA：no.69からコピー）---

## オフにして、何が変わったか
→ リード：オンだった設定をオフにした。変わること・変わらないことを分ける
→ 表3：項目 ／ オフにすると
   ・これから始めるチャット・コーディングセッション ／ 今後のモデル学習には使われない
   ・保持期間 ／ 5年 → 30日
   ・すでに始まっている学習・作られたモデル ／ 外れない（公式verbatim）
   ・保存済みの過去のチャット・セッション ／ 今後のモデル学習には使われない（プライバシーセンターverbatim「we will not use your previous or new chats or coding sessions for future model training」。⚠️ 2025年発表記事の「new or resumed」は**オンにしたときにどの会話から適用されるか**の話。オフ後の説明に使わない）
   ・安全性の分類器に引っかかった会話・自分から送ったフィードバック ／ オフでも使われる（例外）
   ・「ロケーションメタデータ」 ／ 別の設定。連動しない
→ 【アラート】オフにしても、すでに始まった学習からは外れない（80字以内）
→ 私の決定と理由を2〜3文：自分以外の情報を日常的に入れているのでオフにした。オフにしても使える機能は変わらなかった（確認ダイアログも出なかった）
→ ⚠️ 「オフにしたから安全」と書かない。学習に使われるかと、情報が漏れるかは別の話（この記事は前者だけを扱うと明示）

## 会社で使うと、Pro・MaxとTeamは何が違うか
→ リード（読者の次の疑問「会社契約は何が違うか」に答える。**確認できた事実だけ**を並べる）
→ 4点を箇条書き（各1〜2文・一次情報のverbatimを添える）：
   ・Pro・Max：Consumer Termsの範囲（verbatim「this does not include Claude.ai or Claude Pro use for individuals or entities」＝個人でも法人でもClaude.ai／Proの利用はCommercial Termsの対象に含まれない、**までしか言えない**。「仕事に使うことは禁止されていない」という法的結論は書かない）。モデル改善はオプトアウト方式
   ・Team：Commercial側の契約。既定でコンテンツをモデル学習に使わない
   ・Team：2〜150名向け。標準席は1席あたり月$20（年払い）／$25（月払い）。料金ページは米ドル表記（日本語ページも同じ）
   ・会社ドメインのメールで登録している人：規約の「Business Domains」条項。勤め先のEnterpriseアカウントへ紐づく可能性があり、管理者がMaterialsへアクセスできる場合がある（verbatim）
→ 表4（必要なら）：Pro・Max ／ Team の2列：規約 ／ モデル学習 ／ 席数 ／ 月額。**全セルが一次情報で埋まる列だけ**
→ 【インフォ】Pro・MaxはConsumer Terms＋オプトアウト方式。TeamはCommercial側の契約で、既定ではコンテンツをモデル学習に使用しない（80字以内）
→ ⚠️ 「一人ならPro・Max＋オフ、複数人ならTeam」のような勧めは書かない（実質「Teamにすべき」になる）。条件を並べて、読者が選ぶ

## 渡す前に決めておく3つ
→ 読者の判断で終わる（「安全です／危険です」で終わらない）
→ 1. 2. 3. で：
   1. 自分の設定を見る（オンなら、通常のチャットやセッションをモデル改善に使う設定になっている）
   2. 入れているものを一度書き出す（自分の情報か、自分以外の情報か）
   3. 自分以外の情報を日常的に入れるなら、オフにするかTeamにするかを決める
→ 締め2〜3文：私はオフにした。理由は自分以外の情報を日常的に入れているから。使い勝手は変わらなかったので、迷っている人は先に設定だけ見るのがいい（「〜しましょう」は使わない）
→ ⚠️ 締めに「私の感覚」を一般ルールとして載せない。「私はこう決めた」に留める

---（末尾CTA：no.69からコピー）---

**関連記事**（3本）
・弁護士業務の案件管理と書類作成に、Claude Codeを当てはめた（no.49）
・社労士業務の就業規則・36協定に、Claude Codeを当てはめた（no.53）
・Claude Codeとは何か？できること・使い方を実際に使って整理した（no.9）
```

## CTA（この文言をそのままコピーする。1文字も変えない）

```
---

＼　ブログ更新が止まっている・記事運用を任せたい方へ　／
企画から執筆・公開まで、まるごとお任せください。お気軽にご相談を。

[お問い合わせフォームはこちら](https://aicontent-note.com/contact/)

---
```

配置は構成の指定どおり、**H2「私が渡しているもの・渡さないもの」の直後に1回・末尾に1回**。間にH2が3つ入る。

## 記事の末尾に置く関連記事（この3本をこの形式で）

```
**関連記事**
・[弁護士業務の案件管理と書類作成に、Claude Codeを当てはめた](https://aicontent-note.com/claude-code-lawyer-case-management/)
・[社労士業務の就業規則・36協定に、Claude Codeを当てはめた](https://aicontent-note.com/claude-code-labor-consultant-rules-agreement/)
・[Claude Codeとは何か？できること・使い方を実際に使って整理した](https://aicontent-note.com/claude-code-introduction/)
```

本文中の内部リンクは、H2「私が渡しているもの・渡さないもの」の末尾に、上の弁護士・社労士の2本をこのタイトルのまま置く。

## 添付ファイルの扱い

添付した記事（no.69）は**文体見本**です。構成や内容は真似せず、**文の長さ・語尾・段落の切り方・ブロック要素の使い方**だけを参考にしてください。

## 出力前の自己チェック

1. 60字を超える一文がないか
2. 文字だけの段落が5つ以上続いていないか
3. 表やブロックの内容を、直後の地の文で言い直していないか
4. 「この記事で絶対に外さないこと」10項目に違反する文がないか（特に2・3・4・5・6）
5. 「使ってよい事実」に無い数値・事実・条項を書いていないか
6. 引用が原文どおりか（要約・和訳を引用符に入れていないか）

以上を確認したうえで、記事の初稿を出力してください。
