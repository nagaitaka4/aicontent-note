# 材料シート：プロンプトはマークダウンで書くべき？（仮題・TOP10 #1・新規・no.87）

> 作成：2026-11-17 15〜16時台。1位の決め方は`operations/theme-candidates-2026-11-17-afternoon-copy-growing.md`。
> ⚠️ no.35（`markdown-basics`「Markdownとは？AI時代に全員が使うべき理由を実務視点で解説」）の改稿ではなく新規。no.35は`series: ai-ops-basics`の4本目なので改稿しない（`rules/task-management.md`「補充の手順」3）。公開したら、no.35の末尾から1行リンクする。

## 1. 記事の芯

プロンプトは基本Markdownで足りる。Markdownは「人が読み返して直す指示書」に向く書き方で、AIもその区切りを読める。ただし、①返事の項目を毎回そろえたい ②ツールが形式を決めている ③守らせたいルールが増えた、の3つの場面では、別の形（JSON・YAML・チェックのプログラム）に分ける。検索の上位は「マークダウン記法◯選で精度が上がる」の一色で、③（Markdownで書いたルールは増えると効かなくなる）を書いている記事は無い。

## 2. 検索の語（2026-11-17 15時台・Googleサジェスト・実Chrome・2語まで）

- `プロンプト マークダウン`6（記法／形式／方式／テンプレート／**なぜ**）
- `マークダウン プロンプト`10（書き方／gemini／例／ai／chatgpt／生成ai／copilot）
- `プロンプト 書き方`10（コツ／生成ai／gemini／記号／**マークダウン**／copilot）
- `プロンプト 構造化`10（**メリット**／記号／ai／生成ai／chatgpt）・`プロンプト xml`10（形式／タグ／claude）・`プロンプト json`10（形式／出力）・`プロンプト 形式`10
- `プロンプト 記号`6（使い方／一覧／意味）・`プロンプト 見出し`6・`マークダウン ai`7（相性／親和性）・`markdown ai`10（**負債**／なぜ）
- 名前入り：`chatgpt マークダウン`5（崩れる／出力／入力）・`claude マークダウン`8
- Googleの「他の人はこちらも検索」：プロンプト マークダウン なぜ／例／書き方／テンプレート／Claude／Gemini／Copilot

→ 題は`プロンプト マークダウン`をそのまま前に（KWの語彙を言い換えない）。「なぜ」「メリット」に答える節が要る。

## 3. 検索の上位（2026-11-17 15時台・実ChromeでGoogle検索）

`プロンプト マークダウン`の上位（AIによる概要あり）：

| 順 | 題 | ドメイン | 型 |
|---|---|---|---|
| 1 | ChatGPTで覚えておくと便利なMarkdown記法5選（2024/3） | qiita.com | 記法◯選 |
| 2 | 【生成AI プロンプト】Markdownを使ってAIの回答精度を上げよう！（2026/2） | qes.co.jp | 記法の説明＋メリット |
| 3 | 生成AIプロンプトにマークダウンを使う方法｜回答精度を上げる書き方（2026/8） | solution.ndisol.jp | 記号5つ＋業務別の例 |
| 4 | プロンプトの書き方に迷ったら、マークダウン記法で整理する（3年前） | note.com | 記法の説明 |
| 5 | マークダウンとは？AIプロンプトでの使い方とテンプレ集10選（2026/4） | kasoudesign.com | テンプレ集。「実務ではほぼ必須レベル」 |
| 6 | プロンプトのマークダウン記述について（2025/6） | softcreate.co.jp | 記法の説明 |
| 7 | 【実例付】生成AIの回答精度が向上！マークダウン活用術（2025/12） | ai.unext-hd.co.jp | 記法＋実例 |

- **読まれている型**：Markdownとは → 記号5つ（# 見出し・- 箇条書き・** 強調・--- 区切り・``` コード）→ テンプレート（# 役割／# 背景／# 依頼事項／# 制約条件）→ メリット（取りこぼしが減る・トークンが少ない・出力が安定）
- **足りない所**：①「精度が上がる」の根拠が公式・研究で示されていない（AIによる概要のメリットも各社ブログの言い分） ②使わなくてよい場面・別の形にする場面が無い ③長い指示書を実際に回している側の話が無い
- 「意味ない」側の検索（`プロンプト マークダウン 意味ない`）にも反対側の記事が数本ある：note 緑どんぐり（下の4節・写す元）／insist.sakura.ne.jp「プロンプトにMarkdownは必要か？」（2026/6・見出しや強調を増やしすぎると読みにくい）／webdesign-code.com「AIプロンプトはMarkdownで書くべきか？」（2026/8・魔法ではない・単発の確認には要らない）／Zenn「なぜAnthropicはプロンプトにXMLタグを推奨するのか」（2026/5）

## 4. 写す元（note 緑どんぐり「プロンプトはMarkdownでいいと思っていた｜使い分けが必要になる3つの場面」・2026/3/8・高評価150件以上・全文を読んだ）

URL：https://note.com/green_donguri/n/nedc603e42a8e

| 元の並び | このメディアの実物 |
|---|---|
| ①結論：基本はMarkdownで合っている。苦しくなる瞬間が3つあり、そこだけ切り替える | 同じ結論を、長い指示書を回している側から言える（下の行） |
| ②基本はMarkdownでいい：プロンプトは人が書いて、人が読み返して、人が直す文書。書くのが速い・読み返しやすい・ツールを選ばない | **Claude Codeへの指示書（`CLAUDE.md`と`rules/`の4本）が計1,775行（11/17）、GPTへのレビュー依頼文が42本（`operations/review-requests/`）、構成案もすべてMarkdown**。毎回ユーザーとCCが読み返して直している（ルールの見直しのコミットが日々ある） |
| ③場面1 必須の枠を落としたくないとき → JSONで項目を明示 | **X投稿の読者役チェック（`operations/x-review-pack.py`・2026-09-25〜）**：読者役のAIへの依頼は箇条書き（意味が分からない言葉・止まるか1〜5・面白いか・フォローしたくなるか…）で、**返事は「JSONだけを1つ返してください。前後に文章を書かないでください」と形を指定**。返ってきたJSONを`x-review-judge.py`が読んで合否を出す（人が読む文章で返させると、合否を機械で出せない） |
| ④場面2 大量のデータを渡したいとき → 指示はMarkdown、データはCSV | **実物なし**。このメディアはGPTへの依頼文でもデータをMarkdownの表で渡している（例：`operations/editorial-meeting-gpt-prompt-2026-10-29.md`に表の行が24行）。CSVに分けて比べた記録は無い → **構成では作らない**（7節） |
| ⑤場面3 使うツールが形式を決めているとき → そのツールの形式（YAMLなど）に従う | **記事のMDの冒頭（frontmatter）はYAMLの形**（`title:`・`slug:`・`description:`・`eyecatch:`…）で、WPに入れる変換スクリプト`operations/md-to-wp.py`がそこを読む。Claude Codeの設定ファイル（`.claude/settings.local.json`・337行）はJSON。どちらも自分で選んだ形ではない |
| ⑥まとめ：形式を増やすのではなく、用途を分けるだけ | 同じ |
| （元に無い一手）**守らせたいルールが増えたとき** | **Markdownの指示書は、増えると1つずつが効かなくなった**：2026-08-05に`rules/article-flow.md`が357行・42,726字、「省略禁止」が33行に達し、同じ指摘を何度もされた（`operations/lessons.md` 2026-08-05「ルールは多いほど1つあたりの効きが薄まる」）。→ **測れるルール（一文60字・リードの字数・表の強調など）は、Markdownの文章ではなくPythonのチェック（`operations/constraints.py`・2026-08-18〜）に移し、`article-self-check.py`がNGを出す形にした**。Markdownの指示書に残すのは原則だけ（`CLAUDE.md`「測れるルールはスクリプトが正・プロースは原則のみ」）。あわせて、`>`（Markdownの引用）を使ってよいかが3つのファイルで食い違い、修正が連鎖した（`constraints.py`冒頭・8/18） |

- 元の整理（3つの場面）をほぼそのまま使うので、**本文で元の記事を紹介してリンクする**（`rules/task-management.md` 0番）。文章・表は写さない
- 元の場面2（CSV）は実物が無いので、本文では元の記事の紹介の中で1行触れるか、触れない。こちらの3つ目は「守らせたいルールが増えたとき」に入れ替える

## 5. 公式の一次情報（2026-11-17 15時台・実Chromeで原文を開いた）

**Anthropic（日本語版あり）**：[プロンプティングのベストプラクティス](https://platform.claude.com/docs/ja/build-with-claude/prompt-engineering/claude-prompting-best-practices)（`use-xml-tags`はこのページの`#structure-prompts-with-xml-tags`へ転送）

- 「XMLタグは、特にプロンプトに指示、コンテキスト、例、可変入力が混在している場合に、Claudeが複雑なプロンプトを曖昧さなく解析するのに役立ちます。」
- 「手順の順序や完全性が重要な場合は、番号付きリストや箇条書きを使って指示を順序立てたステップとして提供してください。」
- 「プロンプトで使用されるフォーマットスタイルは、Claudeの応答スタイルに影響を与える可能性があります。」「たとえば、プロンプトからmarkdownを削除すると、出力に含まれるmarkdownの量を減らせます。」
- 「重要なテスト： タスクについての文脈をほとんど持たない同僚にプロンプトを見せ、それに従うよう頼んでみてください。その同僚が混乱するなら、Claudeも混乱します。」
- → **Markdownで書けとは言っていない。**区切るならXMLタグ、順番があるなら番号付き・箇条書き。書式は返事の書式にうつる

**OpenAI（英語のみ）**：[Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)（`platform.openai.com/docs/guides/prompt-engineering`から転送）

- 原文：`Markdown headers and lists can be helpful to mark distinct sections of a prompt, and to communicate hierarchy to the model. They can also potentially make your prompts more readable during development. XML tags can help delineate where one piece of content (like a supporting document used for reference) begins and ends.`
- → Markdownの見出しと箇条書きは区切りと階層を伝えるのに「役立つことがある」・開発中に人が読みやすくなる。資料の始まりと終わりはXMLタグ

**OpenAI（英語のみ・アーカイブ）**：[GPT-4.1 Prompting Guide](https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide)（2025/4/14・「This recipe is archived and may reference outdated models or APIs.」）

- `Markdown: We recommend starting here, and using markdown titles for major sections and subsections`／`XML: These also perform well`／`JSON is highly structured and well understood by the model particularly in coding contexts. However it can be more verbose`
- 長い資料を渡すとき：`XML performed well in our long context testing.`／`JSON performed particularly poorly.`
- `The model is trained to robustly understand structure in a variety of formats. Generally, use your judgement and think about what will provide clear information and "stand out" to the model.`
- → 古いモデル向けのガイド。使うなら「OpenAIは以前のガイドでMarkdownから始めるのを勧めていた」と時点つきで

**Google（`?hl=ja`でも本文は英語）**：[Prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies?hl=ja)（aistudio.google.com/docs/へ転送）Gemini 3の項

- `Use consistent structure: Employ clear delimiters to separate different parts of your prompt. XML-style tags (e.g., <context>, <task>) or Markdown headings are effective. Choose one format and use it consistently within a single prompt.`
- → XML風のタグでもMarkdownの見出しでもよい。1つのプロンプトの中ではどちらかにそろえる

**研究（英語）**：[Does Prompt Formatting Have Any Impact on LLM Performance?](https://arxiv.org/abs/2411.10541)（2024/11/15・He ほか）

- 同じ中身をプレーンテキスト・Markdown・JSON・YAMLで渡して比べた。`GPT-3.5-turbo's performance varies by up to 40% in a code translation task depending on the prompt template, while larger models like GPT-4 are more robust to these variations.`
- → 形式で結果が変わることはある。ただし大きいモデルほど影響は小さい。**「Markdownが一番」とは言っていない**（どの形が勝つかはタスクとモデルで変わる）。2024年の古いモデルの話

⚠️ 英語のリンク（OpenAI・Google・arXiv）を本文に入れるときは`operations/en-link-allow.tsv`に登録し、本文でリンク先の中身を日本語で説明する（メモリ`feedback_reader_links_japanese`）。Anthropicは日本語版にリンクする。

## 6. 既存記事との重なり

| 記事 | 重なり | 扱い |
|---|---|---|
| no.35 Markdownとは？AI時代に全員が使うべき理由を実務視点で解説（`markdown-basics`・シリーズ4本目） | Markdownとは・記号・AIが好む理由。**GSCで3か月50〜96表示・9.5位前後でクリック1（site-status 9〜11月）** | 記法の説明はno.35へリンクで逃がす。題は`プロンプト マークダウン`（no.35は`markdown とは`寄り）で問いを分ける。公開後にno.35の末尾から1行リンク。⚠️ no.35が今どのクエリで出ているかはGSCで確かめてから題を決める（7節） |
| no.28 プロンプトとは？AIに仕事を依頼する設計書の考え方（`prompt-design-basics`） | プロンプトの4要素 | リンク |
| ルールファイルとは？AIを安定運用する指示書の考え方（`rule-file-basics`） | 指示書の分類・階層 | 3つ目の場面（ルールが増えたとき）からリンク |
| no.82 ブログのアイキャッチをAIで作る方法。80枚作って決めた頼み方の型（`blog-eyecatch-ai-how-to`） | プロンプトの型を載せた | 必要ならリンク |
| no.85 AIに記事をレビューさせても良くならない？指摘を重ねて分かった頼み方（`ai-article-review-how-to`） | レビューの依頼文 | 必要ならリンク |

- 一般的な問いの記事＝制作の記録（日付・ファイル名・行数・記事番号）を本文に出さない（メモリ`feedback_general_question_no_media_story`）。実物は「指示書が1,800行近くになったら〜」のように、読者の判断の根拠になる形にして出す

## 7. まだ無いもの・確認事項

1. **CSVでデータを渡した実物は無い** → 場面2は作らない（元の記事の紹介の中で触れるだけ）。推奨どおりなら聞かなくてよい
2. **普段ChatGPTに手で打つ短い頼みごとをMarkdownで書いているか**は記録に無い → 推奨は「書かない」（記事の主張は長い指示書と返事の形の話で、短い頼みごとの書き方に本人の事実は要らない。一般論として「短い頼みごとには要らない」は公式の書き方〔役立つことがある〕と上位の反対側の記事で言える）
3. ✅ **no.35がどのクエリで表示されているか**（2026-11-17 16時台・実ChromeのGSC・3か月＝8/16〜11/15）：60表示・1クリック・平均8.7位。**クエリの内訳は「データがありません」＝すべて開示されない少数の語**。`プロンプト マークダウン`で食い合っている証拠は無い → 題は`プロンプト マークダウン`を前に置き、記法の説明はno.35へリンクで逃がす
4. 「Markdownで書くとAIの精度が上がる」を確かめた実験はこのメディアに無い → 「精度が上がる」とは書かない。公式（役立つことがある）と研究（形式で変わることはあるが大きいモデルほど影響は小さい）の範囲で書く
