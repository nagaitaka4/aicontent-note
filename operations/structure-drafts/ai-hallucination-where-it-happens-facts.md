# 材料シート：ClaudeやChatGPTの嘘（ハルシネーション）はどこで起きるか（TOP10 #1・D-34・新規no.75）

作成：2026-10-16 18時台（記事セッション）
> **執筆側はこのシートの事実だけを使う。**ここに無い数字・体験は書かない。2節の「13.6%・89%」は**後で原文にあったと分かった**（9/25）ので、「AIが作った数字」の例として使わない。

## 1. 記事の芯

**AIの嘘（ハルシネーション）は、何も無い所から作られるより、調べ物の途中——要約・1ページだけの確認・ニュース記事の写し・条件の読み違え・数え直し——で起きていた。だから確かめる場所も決まる。**半年、AI（Claude Code）に調べ物と記事の下書きをさせて残した訂正の記録で渡す。

- 読者：ChatGPT・Claudeに調べ物や文章を任せていて、「嘘をつかせない方法」「どこを確かめればいいか」を知りたい人（サジェスト`chatgpt 嘘をつかせない`・`ハルシネーション 対策`・`ai ハルシネーション 事例`）
- この記事でしか渡せないもの（④）：半年分の訂正の記録（どこで起き、どう見つけ、外に出たか）。公式の説明（2つ目の節）は「当て推量」「学習データにない最新情報」が中心で、調べ物の途中で起きる型はヘルプの一部にしか無い
- **カニバリ判定（2026-10-16）：新規。**no.13「AIで作ったブログ記事、そのまま公開していいのか？品質チェックの方法」（`ai-article-quality-check`）の読者の問いは「AI記事を公開してよいか・何をチェックするか」。H3「①事実・情報の正確性」で「AIはもっともらしい情報を生成する」「数字・固有名詞・最新情報は確認」を4段落で触れるだけ。この記事の問いは「AIの嘘はどこで起きて、どこを確かめればいいか」で別。no.13はGSCでクリック0（`operations/site-status.md` 795行：0／2表示・1285行：0クリック／5表示）。**この記事からno.13へ「公開前のチェック全体」としてリンクする**

## 2. この環境の実物

### 2-1. `research/`の「訂正」を全行読んで分類（2026-10-16 18時台・別エージェントが全50行を前後の文脈ごと読んだ）

- 「訂正」を含む行は50行（seo-insights 18／ai-tools 14／trends 11／market 5／README 1／ai-tools 2 1）。**TOP10の行の「35行」は古い数**
- うち12行は「訂正が必要な記事：なし」の定型（seo-insights.md 25,39,72,115,129,152,180,206,234,271,300,321）、2行は記録する前に食い違いに気づいて防いだ件（ai-tools.md 796・trends.md 832）
- **残り36行＝誤り17件**。書いたのはすべてAI（Claude Code）の定期リサーチ（ニュース・公式の更新の調べ物）。期間は2026-06-01〜09-17の誤記録

| # | 何を誤ったか | 起きた場所 | 見つけたきっかけ | 外に出たか |
|---|---|---|---|---|
| 1 | ChatGPTの広告を「日本は対象外／判断できない」（ai-tools.md 1056〜・1242） | 1ページだけ見た（欧州拡大の発表記事1本） | ユーザーの指摘（構成案の作成中） | **X投稿`ADS-気`（8/24）と構成案M-13まで→8/31に訂正投稿`ADS63-訂`** |
| 2 | 広告は「無料・GoだけでPlus・Proに出ないは公式に記載なし」（1243） | 1ページだけ見た | 1と同時 | 1と同じ出来事 |
| 3 | Geminiの更新履歴を「最新は7/21のまま」（ai-tools.md 1113〜1161） | 公式の日本語版の更新遅れ（「と考えられる」＝推測つき） | 翌日に取り直した | 記録だけ |
| 4 | 「Gemini APIの更新履歴に8/13〜14の新規なし」（1460） | 後から出た分を見ていない（原因の記載なし） | 同日の2回目の調べ物 | 記録だけ |
| 5 | GPT-5.6のリリースを「8/13」（実際は7/09）（1392・1401・1256） | ニュースのまとめ（releasebot経由の要約）を写した | 翌日に調べ直した | 記録だけ |
| 6 | 変更の版を`2.1.268`（実際は`2.1.233`）（trends.md 517〜632） | 版番号の取り違え＋前の調べ物の見落とし | 2日後に更新履歴を全文検索 | 投稿の候補まで→キューに入れず閉じた |
| 7 | Claudeの料金を「Pro月払い$22・Max$110〜」（583・652） | 見ている画面の違い（日本から開くと税込み表示） | 2つの画面で見比べた | 記録だけ |
| 8 | 「最新はv2.1.233」（同日にv2.1.234）（1496） | 後から出た版を見ていない | 翌日 | 記録だけ |
| 9 | 「v2.1.231が最新」（同日にv2.1.232）（1607） | 後から出た版を見ていない | 同日 | 記録だけ |
| 10 | 自動再開のチェックボックスを「未確認の噂」（1546） | 1か所しか見ていない（告知はX投稿だけだった） | 翌日、投稿を開いた | 記録だけ |
| 11 | Sonnet 5の9/1値上げを確定扱い（撤回済みだった）（1644） | 公式が後から変えた（当時は正しかった） | 公式の料金ページの注記 | 記録だけ |
| 12 | 「週複数回利用比率71.6%（サイバーエージェント調べ）」を「利用率」（trends.md 1883・ai-tools.md 1701） | 調査元と、何の割合かの取り違え（実際はICT総研・利用者のうち週に数回以上使う人の割合） | 構成案の作成中に原文を開いた | 構成案の候補まで→使わずに取り消し |
| 13 | 補助金の「6次＝10/30」（market.md 309ほか） | 枠の取り違え（10/30は別の枠の締切） | 4日後に公式の日程を確認 | 記録だけ |
| 14 | 「Ahrefs調査・日本の1位CTRが62.7%低下」（seo-insights.md 614ほか） | 二次情報の誤りを写した（「可能性が高い」＝推測つき） | 次の調べ物で複数の出典が一致 | 投稿の候補まで |
| 15 | GEO論文の施策を、論文に無い組み合わせで記録（662） | **元に無いことを書いた**（どこで生まれたかの記載なし＝推測） | 記事を書く前の事実確認（論文の本文） | 記録だけ（公開記事は訂正後） |
| 16 | 重複率37.9%の出典をllmrefs.comと記録（実際はAhrefs・38%）（678） | 出典の取り違え | 記事を書く前の事実確認 | 記録だけ |
| 17 | 「最大115%向上」を「5施策の平均」（793） | 二次情報の言い方を写した（推測） | 記事を書く前に論文で再確認 | 記録だけ |

**読者向けにまとめた分け方（記事で使う）**

| 起きた場所 | 件数 | 該当 |
|---|---|---|
| 古い情報のまま（後から出た版・公式の変更・日本語版の遅れ） | 5 | #3・#4・#8・#9・#11 |
| 取り違え（出典・調査元・何の割合か・枠・版番号・表示の税込み/税別） | 5 | #6・#7・#12・#13・#16 |
| 1ページ・1か所だけ見て「無い」「対象外」 | 3 | #1・#2・#10 |
| ニュース記事・まとめの写し | 3 | #5・#14・#17 |
| 元のページに無いことを書いた | 1（推測） | #15 |

- **17件のうち、元に無いことをAIが書いたと見られるのは1件（それも推測）。**残り16件は、元の情報の選び方・読み方・古さで起きた
- **外に出たのは1件（#1・#2の同じ出来事）**：X投稿と構成案まで広がり、訂正の投稿を出した。ほかは記録・候補の段階で止まった
- ⚠️ #1は、8/15にリポジトリへ正しい情報（公式ページの「日本で提供開始」）を記録していたのに、8/21に「対象外」と書いていた（ai-tools.md 1501）。記事では使わない（内輪の話）
- ⚠️ 日本の広告の開始日は記録が2通り（6/19＝Impress Watch／8/11＝公式ページの更新）。**記事に開始日は書かない**
- ⚠️ `ADS-気`の誤りの説明が記録の間で食い違う（「英語メディア発を公式扱い」／「1ページだけ見た」）。記事では8/28の訂正（1ページだけ）の側だけを使う

### 2-2. 調べ物の外（記事を書く段階）で起きたもの

| 何が起きたか | 起きた場所 | 見つけ方 | 出どころ |
|---|---|---|---|
| 検索結果の要約が「公式のサポート文書にこう書いてある」と言ったが、ページを開くとその記述が無かった（Claude Codeの週次上限+50%） | 要約が出典の所在まで作った | ページを開いた | `research/README.md` 115行（2026-08-17） |
| AIの書いた原稿に「学習に使わない設定でも、昔のチャットを開き直すと使われる」→公式は逆 | 条件（設定オン時／オフ時）の読み違え | 別のAI（ChatGPT）に原稿を読ませた | `knowledge/x/queue.md` 1610行（`REVIEW-70リ`・no.70） |
| 自分のサイトの数字を数え直したら違った：7月以降の公開「41本」→29本・「7日以内に表示32本」→24本・「クリック1以上37本」→33本 | 手元のデータの集計 | 生データから計算し直した | commit 1ec8bc8（2026-10-14・no.23の材料シート） |
| 「4月の記事が5月中旬にそろって出た」を「2〜4月の記事」と広げて書いた | 範囲の言い過ぎ | レビュー役が生データで照合 | `articles/no23_rewrite_composition.md` 11行 |
| 記事のチェック役のChatGPTが「料金は税抜き表示です」→料金ページは税込みだった | チェック役のAIの誤り | 料金ページを開いた | `knowledge/x/queue.md` 1910行（`FACTG-01`） |

### 2-3. 「無い」の判断も外れた例（使うなら1行）

- 2026-08-14：公式ブログの要約に出た「13.6%・89%」を、原文を検索して見つからず「要約が作った数字」として消した。**9/25に開き直すと件数つき（143/1,053・937/1,053）で載っていた**（`operations/lessons.md` 213〜235行）。当時の検索漏れか、後で書き足されたかは分からない
- → 「AIが作った数字」の例には使わない。使うなら「『無い』も、見た日と見た場所つきの事実」の例として

## 3. 公式の一次情報（2026-10-16 18時台にアプリ内ブラウザで原文を開いて取得・英語版を主に）

### 3-1. OpenAI「Why language models hallucinate」（2025-09-05）
https://openai.com/index/why-language-models-hallucinate/ （日本語版 https://openai.com/ja-JP/index/why-language-models-hallucinate/ ）

- `By this we mean instances where a model confidently generates an answer that isn't true.`
- `Hallucinations are plausible but false statements generated by language models.`
- `argues that language models hallucinate because standard training and evaluation procedures reward guessing over acknowledging uncertainty.`
- `ChatGPT also hallucinates.`
- `But arbitrary low-frequency facts, like a pet's birthday, cannot be predicted from patterns alone and hence lead to hallucinations.`
- `Finding: Accuracy will never reach 100% because, regardless of model size, search and reasoning capabilities, some real-world questions are inherently unanswerable.`
- `Finding: They are not, because language models can abstain when uncertain.`（「ハルシネーションは避けられない」という主張への答え）
- 例：論文の著者の博士論文の題を聞くと、自信をもって3つ違う答えを出し、どれも誤り（誕生日も同じ）
- 表（GPT-5 System CardのSimpleQA）：gpt-5-thinking-mini＝答えない52%・正解22%・誤り26%／OpenAI o4-mini＝答えない1%・正解24%・誤り75%

→ 読者向けの言い方：**AIは「分からない」と言うより推測で答えるほうに寄りやすい。とくに数の少ない細かい事実（誕生日・論文名など）で起きる**

### 3-2. OpenAIヘルプ「Does ChatGPT tell the truth?」（Updated: 2 months ago＝取得日10/16から見て2026-08ごろ）
https://help.openai.com/en/articles/8313428-does-chatgpt-tell-the-truth

- 例として：`Incorrect definitions, dates, or facts`／`Fabricated quotes, studies, citations or references to non-existent sources`／`Overconfident answers to ambiguous or complex questions`
- `Confidence isn't reliability: The model may express high confidence even in incorrect answers.`
- `Lack of access: The model may not be able to obtain relevant information from a given website due to technical issues, paywalls or preferences set via robots.txt.`
- `Use ChatGPT as a first draft, not a final source.`／`Always verify quotes, data, technical information or references to external documents.`／`check sources when accuracy matters by visiting links directly.`

### 3-3. Claudeヘルプ「Claude is providing incorrect or misleading responses. What's going on?」（March 17, 2026）
https://support.claude.com/en/articles/8525154-claude-is-providing-incorrect-or-misleading-responses-what-s-going-on

- `Claude might not have been trained on the most-up-to-date information and may get confused when prompted about current events.`
- `Claude can display quotes that may look authoritative or sound convincing, but are not grounded in fact.`
- `When working with web search results, users should review Claude's cited sources. Original websites may contain important context or details not included in Claude's synthesis.`
- `the quality of Claude's responses depends on the underlying sources it references, so checking original content helps you identify any information that might be misinterpreted without the full context.`
- 関連記事の題（開いていない）：`Claude is producing links that don't work and falsely claiming that it has sent emails or produced external documents. What's going on?`

→ **この記事の芯にいちばん近い公式の一文**：回答の質は、参照した元の情報で決まる＝元のページを開いて確かめる

### 3-4. Claude開発者向けドキュメント「Reduce hallucinations」
https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations

- `Allow Claude to say "I don't know": Explicitly give Claude permission to admit uncertainty.`
- `Use direct quotes for factual grounding: ... ask Claude to extract word-for-word quotes first before performing its task.`
- `Verify with citations: ... If it can't find a quote, it must retract the claim.`
- `Best-of-N verification: Run Claude through the same prompt multiple times and compare the outputs.`
- `External knowledge restriction: Explicitly instruct Claude to only use information from provided documents and not its general knowledge.`
- `while these techniques significantly reduce hallucinations, they don't eliminate them entirely. Always validate critical information`

→ 読者が使えるのは①「分からないと言っていい」と書く ②根拠の一文をそのまま引用させる ③引用が無い主張は消させる。**「無くならない」と公式が書いている**

### 3-5. Google検索セントラル「生成AIコンテンツ」（Last updated 2026-10-01 UTC・2026-10-16 18時台に原文で確認）
https://developers.google.com/search/docs/fundamentals/using-gen-ai-content?hl=en
- `It is critical to manually factcheck and review all AI-generated content for accuracy and trustworthiness before publishing.`

## 4. X編集部の在庫

| ID | 状態 | 中身 | 記事で使えるか |
|---|---|---|---|
| `FACTG-01` | 10/4 09:28投稿済み（9ビュー） | 記事のチェックをChatGPTに任せたら「料金は税抜き表示です」→料金ページは税込みだった。合っている所を間違いに直すところだった（`knowledge/x/queue.md` 1910行） | **使える：チェック役のAIも間違える例** |
| `REVIEW-70リ` | 9/25投稿済み | AI（Claude Code）が書いた原稿に「学習に使わない設定でも、昔のチャットを開き直すと使われる」→公式は逆。ChatGPTに読ませて見つかった（`queue.md` 1610行） | **使える：条件（オン時／オフ時）の読み違え。別のAIに読ませて見つけた例** |
| `ideas.md` 463行 | ⚠️ 前提が崩れた | 「WebFetchが作った13.6%・89%」→9/25・9/30に公式ブログの原文にあったと判明 | **「AIが作った数字」としては使わない。**使うなら「AIが作ったと思って消した数字が、あとで原文にあった＝『無い』も時点つき」の例として |
| `ADS63-訂` | 投稿済み（別エージェントで確認中） | ChatGPT広告「日本は対象外」の訂正投稿 | 使える：1ページだけ見た結論が外に出た例 |

## 5. 既存記事との重なり

| 記事 | 重なり | 扱い |
|---|---|---|
| no.13 AIで作ったブログ記事、そのまま公開していいのか？品質チェックの方法（`ai-article-quality-check`） | H3①事実の正確性（4段落） | 公開前チェック全体はno.13へリンク |
| no.70 Claudeに会社の情報を渡して大丈夫か。データが学習に使われる条件（`claude-company-data-training`） | 規約の読み違えが起きた記事 | 例として触れるならリンク（本文に記事名・制作の記録は出さない） |
| `geo-ng-practices` GEO対策でやってはいけないこと（precheck②） | Googleのガイド | 3-5を使うならリンク候補 |
| no.72 ChatGPTとClaudeの使い分け（`chatgpt-claude-division-of-work`） | ChatGPTをレビューに使っている | 「別のAIに読ませる」の節からリンク候補 |

## 6. 需要（2026-10-16 18時台・Googleサジェスト `client=firefox&hl=ja`）

| 語 | 件数 | 主な候補 |
|---|---|---|
| `claude ハルシネーション` | 10 | 対策／少ない／ひどい／多い／対策 プロンプト／claude code ハルシネーション／claude chatgpt ハルシネーション |
| `chatgpt 嘘` | 10 | 嘘をつかせない／嘘つく／嘘ばかり／嘘をつかせない プロンプト／方法／設定 |
| `ai ハルシネーション` | 10 | とは／対策／対策 プロンプト／事例／なぜ／原因／比較／確率 |
| `ハルシネーション 対策` | 10 | プロンプト／カスタム指示／論文／chatgpt／gemini／rag |
| `ハルシネーション 例` | 10 | 例文／chatgpt／gemini／copilot |
| `ai 嘘` | 10 | 嘘をつく／嘘ばかり／嘘をつかせない／例 |
| `chatgpt 信用` | 10 | 信用性／信用できる／できない／していい |
| `生成ai 間違い` | 9 | 例／間違いだらけ／間違いを認めない／計算 間違い |
| `ai ファクトチェック` | 6 | やり方／方法／プロンプト／ツール |
| `chatgpt 出典` | 5 | 書き方／出典元／出典 嘘 |

- 自サイトの隣のクラスタ：ChatGPTとClaudeの比較（no.56 `chatgpt-work-claude-code-comparison`・`tasks/README.md` TOP10 #1の行）
- 読者の動き：「嘘をつかせない（プロンプト・設定）」が最多＝**対策を知りたい**。「事例」「なぜ」「原因」も並ぶ

## 7. まだ無いもの

1. **本人がふだんのチャット（ChatGPT）で嘘に当たった場面**（ユーザーのチャットはChatGPT・メモリ`feedback_author_usage_not_overridden`）。2節の記録はすべてClaude Codeの調べ物と記事づくりの中のもの → 構成案の確認事項で聞く
2. AI全体で「どこで嘘が多いか」の統計：無い。**記事では「私の記録では」の範囲で書く**
3. #15（元に無いことを書いた）が、要約のせいか、写した元の記事のせいかは記録に無い＝推測のまま
4. ChatGPTとClaudeのどちらが嘘が少ないか（サジェスト`claude ハルシネーション 少ない`）：比べた実測は無い＝**書かない**（公式の数字も別々の評価なので並べない）
