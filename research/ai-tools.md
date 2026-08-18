# 競合AIツール・新興ツール動向

最終更新: 2026-08-19

---

#### 【デイリー】2026-08-19

**差分なし。ChatGPT・Geminiとも公式チャネルに新規エントリが無いことを一次情報で確認した（8/17・8/18に続き3日連続）。**

- **ChatGPT（OpenAI）：新規エントリなし**。[ChatGPT — Release Notes, help.openai.com](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)を**ブラウザで直接開いて本文を確認**（WebFetchは403のまま）。ページの表示は`Updated: 3 日前`で、**最新エントリは8/14付のまま**（対話型クイズ／プロジェクトのメモリ設定変更／Web版の無料・GoでThink／Androidの音声入力／Linuxデスクトップ公開プレビュー）。いずれも8/16の回で記録済み
  - ⚠️ 検索要約には「Health experience」「Computer History（macOS）」が新着のように出てくるが、**本文で日付を取り直すとComputer HistoryとGoogle DriveのLibrary対応は8/13付**。8/18の回と同じ誤認パターンなので、**検索要約の並びを新着と読まない**
- **Gemini（Google）：新規エントリなし**（[ai.google.dev/gemini-api/docs/changelog](https://ai.google.dev/gemini-api/docs/changelog)を確認。ページの`Last updated`は**2026-08-13 UTC**のまま）。最新は8/13の`Gemini 3.7 Flash generally available (GA)`で記録済み
- **国産AIライティングツール：新機能・料金変更は確認できず**。検索でヒットするのは日付のない比較記事・ランキング記事のみで、**6日連続で同じ状態**

> **本日の収穫は`research/trends.md`側にある**（Claudeの出力テキストへの透かし導入。Claude Codeも対象）。競合ツール側は静かな日が続いている。

---

#### 【デイリー】2026-08-18

**差分なし。3社とも公式チャネルに8/15以降の新規エントリが無いことを一次情報で確認した（8/17の回と同じ状態）。**

- **ChatGPT（OpenAI）：8/15〜8/18の新規エントリなし**。[ChatGPT — Release Notes, help.openai.com](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)を**ブラウザで直接開いて本文を確認**（WebFetchは403が続いている）。**最新エントリは8/14のまま**で、内容は8/16の回で記録済み（Web版の無料・GoでThinkが選べる／プロジェクトのメモリ設定変更／対話型クイズ／Linuxデスクトップ公開プレビュー）
  - ⚠️ **検索結果の要約に「Health experience（米国18歳以上）」「OpenTableとResy・Yelpのレストラン予約」が新着のように混ざるが、いずれも新情報ではない。**本文で日付を確認したところ**レストラン予約は8/10付**、Computer History（macOS）とGoogle DriveのLibrary対応は**8/13付**。**検索要約は日付を落として並べるので、本文で日付を取り直さないと新着と誤認する**
- **Gemini（Google）：8/14以降の新規エントリなし**（[ai.google.dev/gemini-api/docs/changelog](https://ai.google.dev/gemini-api/docs/changelog)を確認。ページの`Last updated`も**2026-08-13 UTC**のまま）。最新は8/13の`Gemini 3.7 Flash generally available (GA)`で記録済み
- **国産AIライティングツール：8/15〜8/18の新機能・料金変更は確認できず**。検索でヒットするのは日付のない比較記事・ランキング記事のみで、**5日連続で同じ状態**。差分なし

---

## [2026-08-17] 調査結果（定期リサーチ・12:00の回）

**本日8:00のデイリー回は「差分なし」で閉じたが、フル版で掘り直したところ2件見つかった。1件は期限付きの提供終了（＝使う側が動く必要がある）、1件は8/16の記録の訂正。**

### ChatGPT（OpenAI）

- **【今回の収穫・期限あり】ChatGPT内の公式「DALL·E GPT」が2026-08-30で提供終了する。残しておきたい画像は、それまでにダウンロードが必要**
  - 出典：[ChatGPT — Release Notes, help.openai.com](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)（**このページはWebFetchが403で読めないため、本日確認できたのは検索結果の要約と複数の英語メディア（[Tom's Guide](https://www.tomsguide.com/ai/chatgpt/you-have-until-august-30-to-save-your-chatgpt-dall-e-images-heres-how-to-avoid-losing-them-forever) ／ [Notebookcheck](https://www.notebookcheck.net/DALL-E-leaves-ChatGPT-on-August-30-download-your-images-first.1360522.0.html) ／ [Windows Report](https://windowsreport.com/openai-will-retire-the-official-dalle-gpt-on-august-30/) 等）まで。日付と主旨は各社で一致している**
  - **⚠️ここを間違えると誤報になる**：終わるのは**ChatGPT内にプリセットされた公式の「DALL·E」GPTという入口だけ**で、**ChatGPTの画像生成そのものは終わらない**。後継は`gpt-image-1`／`gpt-image-1-mini`で動く**ChatGPT Images**。**画像生成を有効にしたカスタムGPTは影響を受けない**とされている。「ChatGPTで画像が作れなくなる」と書くと完全に誤り
  - 背景：API側のDALL·E-2／DALL·E-3のモデルスナップショットは**2026-05-12までに廃止予定**として先行して告知されていた。今回はChatGPT側の入口が畳まれる番
  - **X投稿ネタとしての判断：採用（→ ideas.md）。**「使う側の何かが変わる」に該当し、しかも**8/30という期限があって、放置すると自分の資産（過去の生成画像）が消える**タイプ。⚠️ただし**このメディアの読者がDALL·E GPTを使っているかは未確認**。自分ごと化できないなら無理に出さない
- **【8/16の記録を訂正】「GPT-5.6が8/13にリリースされた」という二次情報は、日付が誤り**
  - 8/16の回で「releasebot経由の要約にGPT-5.6リリース（8/13）とあるが公式リリースノートに該当エントリなし」と保留したが、**改めて調べると GPT-5.6ファミリー（Sol／Terra／Luna の3モデル）の投入は2026-07-09**で、8月の新発表ではなかった。公式リリースノートに8/13のエントリが無かったのは当然だった
  - ⚠️ **価格は一次確認できていない**：[openai.com/index/gpt-5-6/](https://openai.com/index/gpt-5-6/)はWebFetchが403。二次情報（Wikipedia・devtk.ai・benchlm.ai）が一致して伝えているのは「**発表時はSol $5/$30・Terra $2.50/$15・Luna $1/$6**、その後**2026-07-30にLunaを80%・Terraを20%値下げしてLuna $0.20/$1.20・Terra $2/$12 になった**」という内容。**記事・投稿で数字を使うなら公式Pricingページで取り直す**
  - **このメディアへの意味**：8/13にSonnet 5の値上げ予告が撤回され、8/13にGemini 3.7 Flashが半額の導入価格で出て、7/30にGPT-5.6 Lunaが80%値下げされている。**`research-20260813-01`（料金は予告どおりに動かない）の補強材料が、これで3社そろった**
- **8/15〜8/17の新規リリースノートエントリは確認できず**。最新は8/14付（Web版の無料・GoでThinkが選べる／プロジェクトのメモリ設定変更／対話型クイズ／Linuxデスクトップ公開プレビュー）のままで、8/16の回の記録から変化なし
- 記録のみ：**Atlas（ブラウザ型のエージェント機能）は2026-08-09で稼働終了済み**。機能はChatGPTとCodexに取り込まれた

### Gemini（Google）

- **8/14以降の新規エントリなし**（[ai.google.dev/gemini-api/docs/changelog](https://ai.google.dev/gemini-api/docs/changelog)を確認。ページの`Last updated`も**2026-08-13 UTC**のまま）。最新は8/13の`Gemini 3.7 Flash generally available (GA)`で記録済み

### 国産AIライティングツール

- **8/15〜8/17の新機能・料金変更は確認できず**。検索でヒットするのは日付のない比較記事・ランキング記事のみで、**4日連続で同じ状態**。差分なし

---

#### 【デイリー】2026-08-17

**差分なし。3社とも公式チャネルに8/15以降の新規エントリが無いことを一次情報で確認した。**

- **ChatGPT（OpenAI）：8/15〜8/17の新規エントリなし**。[ChatGPT — Release Notes, help.openai.com](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)を**ブラウザで直接開いて本文を確認**（WebFetchは403が続いている）。**最新エントリは8/14のまま**で、その内容（Web版の無料・GoでThinkが選べる／プロジェクトのメモリ設定変更／対話型クイズ／Linuxデスクトップ公開プレビュー）は8/16の回で記録済み
- **Gemini（Google）：8/14以降の新規エントリなし**（[ai.google.dev/gemini-api/docs/changelog](https://ai.google.dev/gemini-api/docs/changelog)を確認。ページの`Last updated`も**2026-08-13 UTC**のまま）。最新は8/13の`Gemini 3.7 Flash generally available (GA)`で記録済み
- **国産AIライティングツール：8/15〜8/17の新機能・料金変更は確認できず**。検索でヒットするのは日付のない比較記事・ランキング記事のみで、3日連続で同じ状態。**差分なし**
- ⚠️ **記録のみ／投稿候補にしない**：8月の料金まとめ記事（[Business Insider Japan, 2026-08](https://www.businessinsider.jp/article/2608-how-much-did-major-generative-ai-service-fees/)）は「主要8サービスの料金は据え置き」としている。**新情報ではなく既知の状態の確認**にとどまるため、ネタにはしない

---

#### 【デイリー】2026-08-16

**8/15〜8/16の新規差分はなし。ただし8/15の回で拾い漏れていたChatGPTの8/14付リリースノートに、読者の使い方に効く項目があったため補足する。**

- **【8/15の記録漏れ・補足／一次確認済み】ChatGPTのWeb版で、無料プランとGoプランでも「Think」を選べるようになった**（[ChatGPT — Release Notes, help.openai.com](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)・**2026-08-14付**）
  - 原文（verbatim）：`Use Think on Free and Go. Select Think on the web when you want ChatGPT to reason through a harder question.`
  - **一次確認の方法**：`help.openai.com`はWebFetchが403で読めない状態が続いているため、**ブラウザで直接開いて本文を読んだ**（8/15の回で「一次確認は取れていない」と記録した制約を、今回は突破できた）。**このページの最新エントリは8/14で、8/15・8/16のエントリは無い**
  - **⚠️「新機能」と書かないこと**：Think自体は**8/6前後の発表（GPT-5.6 Lunaを無料・Goの既定モデルにする／テキストチャット無制限化）の中で予告済み**で、記事no.59の構成案にも既に記載がある。今回のリリースノートは**「Webで選べるようになった」という提供面の着地**。「新しくThinkが使えるようになった」と書くと誤り
  - 同じ8/14エントリのその他（読者に効く順）：**プロジェクトのメモリ設定を作成後に変更できるようになった**（既定メモリ⇔プロジェクト限定メモリ・**全プラン対象**。ただし共有プロジェクトはプロジェクト限定のまま変更不可）／**対話型クイズ**（全consumerプラン＋Eduプラン・web/mobile）／**Linuxデスクトップアプリが公開プレビュー**（Ubuntu 24.04・26.04 LTS、Debian 13、Fedora 43・44）
  - 8/13エントリ（記録のみ）：Google DriveがLibraryに統合（Plus・Pro・Enterprise・Edu・Healthcare・BusinessのWeb版から順次）／macOS版の`Computer History`（既定オフ・Pro・Business・Enterprise向け・EEA/UK/スイスでは未提供）
- **⚠️GPT-5.6のリリース（8/13）は二次情報のみ**：releasebot経由の要約に「GPT-5.6リリース・エージェント性能とコストの改善」とあるが、上記の公式ChatGPTリリースノートには該当エントリが無い（モデル側の別ページに載っている可能性）。**単独では「新モデルが出た」型でX投稿の採用基準を満たさないため、追いかけない。記録のみ**
- **Gemini（Google）：8/14以降の新規エントリなし**（[ai.google.dev/gemini-api/docs/changelog](https://ai.google.dev/gemini-api/docs/changelog)を直接確認）。最新は8/13の`Gemini 3.7 Flash generally available (GA)`で記録済み
- **国産AIライティングツール：8/15〜8/16の新機能・料金変更は確認できず**。検索でヒットするのは日付のない比較記事・ランキング記事のみ。**差分なし**

---

#### 【デイリー】2026-08-15

**このメディアの読者の使い方に影響する差分はなし。**

- **Gemini（Google）**：Gemini API changelogに**8/14〜8/15の新規エントリなし**（[ai.google.dev/gemini-api/docs/changelog](https://ai.google.dev/gemini-api/docs/changelog)で直接確認）。最新は8/13の`Gemini 3.7 Flash generally available (GA)`で、これは8/14に記録済み
- **ChatGPT（OpenAI）**：**8/14付でChatGPT Enterprise／EDUの「個人ユーザーが個別に認可した同期コネクション」が無効化され、同期済みデータの削除が開始された**。管理者が管理する同期は影響を受けない（新規の個別認可は8/10で停止済み）。**対象がEnterprise／EDUの管理機能であり、このメディアの読者＝個人・中小企業の使い方は変わらない。記録のみ**
  - ⚠️ **一次確認は取れていない**：`help.openai.com`のリリースノートはWebFetchが403で読めず、確認できたのは検索結果の要約と[OpenAIリリースノート一覧](https://openai.com/products/release-notes/)経由の二次情報のみ。**日付・対象範囲を投稿で断定しない**
- **国産AIライティングツール**：8/14〜8/15付の新機能・料金変更は確認できず。検索でヒットするのは日付のない比較記事・まとめ記事のみだった。**差分なし**

---

## [2026-08-14] 調査結果（定期リサーチ・12:00の回）

### Gemini（Google）

- **⚠️【本日8:00のデイリー回の記録は誤り。訂正する】Gemini 3.7 Flashが2026-08-13にGA（一般提供）になっている**
  - デイリー回は「Gemini API changelogに8/13〜8/14の新規エントリなし」と記録したが、**changelogには8/13付で`Gemini 3.7 Flash generally available (GA)`のエントリがある**（[ai.google.dev/gemini-api/docs/changelog](https://ai.google.dev/gemini-api/docs/changelog)）。**この領域を「差分なし」で閉じたのは誤りだった**
  - **価格（公式ブログで確認）**（[Google公式ブログ「Gemini 3.7 Flash: our most intelligent workhorse model」2026-08-13](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/)）：**導入価格が入力$0.75／出力$3.75 per 1M tokens で2026-12-31まで。2027-01-01から通常価格の$1.50／$7.50に移行する**。公式は導入価格を「3.6 Flashの50%」と表現している
  - **条件・除外まで確認した点**：使える場所は**Gemini API（Google AI Studio・Android Studio経由）・Google Antigravity・Gemini Enterprise Agent Platform**、および**Gemini Spark（Google AI Pro／Ultraの加入者向け・160か国以上）**。導入価格はあくまで**期限付きの値下げ**であり、2027年からは3.6 Flashの標準価格と同額に戻る。「Geminiが恒久的に半額になった」と書くと誤りになる
  - 性能面の公式主張：FrontierCode 1.1で43.6%（3.6 Flashは34.4%）、DeepSWEで65.3%（同49.0%）、GDP.pdfベンチマークで34.0%（同22.0%）。**いずれもGoogle自身のベンチマーク値**
  - **3.6 Flashからわずか約3週間での投入**（3.6 Flashは7/21のGA）
  - **X投稿ネタとしての判断**：単独では「新モデルが出た」型のため採用基準を満たさない。ただし**8/11に撤回されたClaude Sonnet 5の値上げ予告（$3/$15）とセットにすると「AIの価格は予告どおりには動かない」という料金の話になる**。既存の`research-20260813-01`（Sonnet 5価格据え置き）の補強材料として使う（→ ideas.md に追記）

### ChatGPT（OpenAI）

- **8/13の「Ultrafast」プレビュー（本日8:00の回で記録済み）以降、新規の発表は確認できず**。API限定プレビューという位置付けも変更なし。読者の使い方が変わる差分はこの領域では引き続きなし

（定期リサーチで随時追記）

---

#### 【デイリー】2026-08-14

**このメディアの読者の使い方に影響する差分はなし。**OpenAIに動きはあったが、対象が違う。

- **ChatGPT／OpenAI：「Ultrafast」モードをプレビュー発表（2026-08-13）**（[OpenAI公式, openai.com](https://openai.com/index/previewing-ultrafast/) ／ [TechCrunch, 2026-08-13](https://techcrunch.com/2026/08/13/openai-introduces-ultrafast-a-new-mode-that-makes-gpt-5-6-sol-work-at-14x-the-speed/)）
  - GPT-5.6 Solを**最大14倍速**で動かす新しいサービスティア。Cerebrasのハードウェアで動き、出力は**最大750トークン/秒**。**知能はStandardと同じ**でスピードだけが変わる
  - **条件・除外まで確認した点**：**まずOpenAI APIから、限定プレビューとして一部の顧客のみ**に提供。ChatGPTのPlus・Proなどの一般プランでは使えない。容量の増加に応じて対象を広げるとしている
  - **採らない理由**：APIの限定プレビューで、ChatGPTやClaude Codeを実務で使っている読者の使い方は今日何も変わらない。「新しいものが出た」型の発表
  - 同日、Dali Rajic氏をChief Revenue Officerに任命（企業動向のため記録のみ）
- **Gemini（Google）：Gemini API changelogに8/13〜8/14の新規エントリなし。**既報の**Imagen 4系・Gemini 3 Image系の停止は8/17**（告知は6/15・変更なし）、`gemini-robotics-er-1.6-preview`の停止は8/31（[ai.google.dev](https://ai.google.dev/gemini-api/docs/changelog)）

---

#### 【デイリー】2026-08-13

**このメディアの読者の使い方に影響する差分はなし。**動きはあったが、いずれも対象が違う。

- **Gemini（Google）：Made by Google 2026を8/12開催**（[techcrunch.com, 2026-08-12](https://techcrunch.com/2026/08/12/google-unveils-pixel-11-lineup-new-airtag-rival-and-gemini-features-at-made-by-google-2026/)）
  - Pixel 11シリーズ・Pixel Watch 5・AirTag対抗のPixel Tagを発表。あわせて**Gemini Automation**（自然言語1回の指示でアプリ・サイトを横断操作させる機能）を発表。Pixel 11でのデビューが見込まれている
  - 上位機能は**Google AI Pro（月$19.99）**に紐づく
  - **採らない理由**：端末購入が前提のハードウェア発表で、PCでClaude Codeを回している読者の使い方は変わらない。「新製品が出た」型の発表そのもの（実測で最も伸びない帯）
  - Gemini APIのchangelogは**8/10〜8/13に新規エントリなし**。最新は7/30のまま（[ai.google.dev](https://ai.google.dev/gemini-api/docs/changelog)）
- **ChatGPT（OpenAI）：新規の機能・料金変更なし。**8/12に企業向けのAI活用事例記事を公開した程度
  - ⚠️ **昨日（8/12）潰した二次情報の誤りが、今日の検索でも同じ形で再浮上した。**「ChatGPT Adsが2026-08-11に日本・英国・メキシコ・ブラジル・韓国でローンチ」という記述。**再確認したが8/12の判断どおり誤り**で、日本での広告表示開始は**2026年6月19日**（[Impress Watch](https://www.watch.impress.co.jp/docs/news/2118443.html)）。8/11という日付は「その時点でのローンチ済み国一覧」を新着と誤読したもの。**明日以降のリサーチでも同じ形で出てくる可能性が高い。この件は決着済みとして扱う**
  - 事実関係（再掲）：広告表示は**Free・Goプランのログイン成人ユーザーのみ**。Plus・Pro・Business・Enterprise・Educationは対象外
  - **【2026-08-15 追記・一次情報で確認】**OpenAI公式ページ「[ChatGPT での広告のテスト](https://openai.com/index/testing-ads-in-chatgpt/)」（初回公開2026-02-09）には、**「2026年8月11日更新：ChatGPT 広告は、英国、メキシコ、ブラジル、日本、韓国で提供を開始しました」**という追記がある。二次情報が「8/11ローンチ」と書いていた出どころはこれ。**ただし日本の実際の表示開始が6/19であることと矛盾はしない**（公式は8/11に「提供中の市場」として追記した形）。上の判断（日本は6/19開始）は維持する。**この件はもう調べ直さない**
  - **課金判断に効く公式の記述（同ページ）**：「広告を表示したくない場合は、Plus または Pro プランにアップグレードするか、**無料プランで広告をオプトアウトして、1日あたりの無料メッセージ数を減らす**ことで対応可能です」。⚠️ この記述は2026-02-09の初回公開時のもので、8/6の「テキストチャット無制限」より前。**無料の無制限が広告受け入れ前提かどうかは公式ページ間で整合が取れていないため、記事で断定しない**

（定期リサーチで随時追記）

---

#### 【デイリー】2026-08-12

**この領域は実質的な差分なし。**8/11以降、OpenAI・Googleとも読者の使い方に影響する新発表は確認できなかった。以下は確認の記録と、二次情報の誤りを1件潰した記録。

- **ChatGPT（OpenAI）**
  - 8/10：レストラン予約検索に対応（OpenTable・Resy・Yelp連携）。全プラン対象だがChatGPT Workは対象外。**このメディアの読者層には無関係のため記録のみ**
  - 8/10：ChatGPT Businessに上位シート（premium seats）を追加。法人向けのため優先度低
  - ⚠️ **二次情報の誤りを1件排除**：検索結果に「ChatGPT Adsが2026-08-11に日本・英国・メキシコ・ブラジル・韓国でローンチ」という記述が複数あったが、**これは誤り**。日本での広告表示開始は**2026年6月19日**（[Impress Watch](https://www.watch.impress.co.jp/docs/news/2118443.html)）、日本の広告主向けAds Manager開放は6/28。8/11という日付は「その時点でのローンチ済み国一覧」を新着と誤読したもの。**約7週間前の出来事であり、デイリーの新情報ではない**
    - 内容自体の事実関係（参考）：広告表示は**Free・Goプランのログイン成人ユーザーのみ**。Plus・Pro・Business・Enterprise・Educationは対象外。回答の下に「Sponsored」表記で表示され、会話内容は広告主に渡らない
- **Gemini（Google）**
  - API changelogに8/10〜8/12の新規エントリなし。最新は7/30（Gemini Robotics ER 2）
  - Imagen 4系3モデル（`imagen-4.0-generate-001`ほか）が**2026-08-17に停止**。ただし告知は6/15で新情報ではなく、画像生成APIのため読者層との接点も薄い（[ai.google.dev](https://ai.google.dev/gemini-api/docs/changelog)）

（定期リサーチで随時追記）

---

## [2026-08-11] 調査結果

### ChatGPT（OpenAI）

- **【旬ネタ】ChatGPT大型アップデート（2026-08-06）**（9to5mac.com, 2026-08-06）
  - **考える量を選ぶスライダーを追加**：回答ごとに「どの程度考えさせるか」をユーザーが選べる。web・モバイル・デスクトップが対象で、Plus・Proユーザーが利用可
    - ⚠️ **「Intelligence Slider」は正式名称ではない**（2026-08-11確認）。9to5macが使っていた呼称で、OpenAI自身は"a slider ... how much thought the model puts into an answer"としか書いていない。TechCrunchは"thinking slider"と表記。**記事・X投稿では機能の説明で書き、ブランド名として扱わない**
  - **無料ユーザーのテキストチャットが無制限に**：GPT-5.6 Lunaでのテキストチャット制限を撤廃。深い推論が必要なときに使う「Think」ボタンも無料ユーザーに開放
    - ⚠️ **無制限はテキストのみ。**ファイル・画像・音声・画像生成には別の制限が残る（OpenAI明言）。また発表当日ではなく「翌週から」の展開
  - **GPT-5.6 Solを改良**：「より直接的な回答・タイトなフォーマット・不要な詳細の回避」を方針に調整。OpenAIは金融・医療・法律プロンプトの内部評価で、**事実誤りを含む回答がGPT-5.5 Instant比で68%減少**（Solの場合）と報告。**Lunaは同じ指標で62%減**（内部評価であり第三者検証はない点に注意）
  - **`Sign in with ChatGPT`ベータを開始**：Airtable・GitLab・HubSpot・Notion・Supabase・Vercel等の一部プラグイン／パートナーサイトが対象
  - **DALL·E GPTを2026-08-30で終了**。Atlasの動作終了（2026-08-09）は前回記録どおり実施
- **Anthropicとの対比**：Claude Code（Opus 5のeffort・**low/medium/high/xhigh/maxの5段階、デフォルトはhigh**）とChatGPTのスライダーが、ほぼ同時期に「推論量をユーザーが選ぶ」UIへ収束した（Claude Code側は公式ドキュメントで確認済み：https://code.claude.com/docs/en/model-config ）。**M-04（Claude Code vs OSSエージェント比較）およびM-01系の比較記事で使える視点**：性能競争から「同じモデルをどう使い分けさせるか」の設計競争に移っている

### Gemini（Google）

- **Gemini 3.6 Flashの詳細スペックを確認**（前回8/3は登場のみ記録）：3.5 Flash比で**出力トークン消費が17%減**、マルチステップのワークフローで推論ステップ・ツール呼び出しの回数も減少。価格は**入力$1.50／出力$7.50 per 1M tokens**（3.5 Flashの出力$9.00から値下げ）。**知識カットオフが2025年1月→2026年3月に前進**。開発者から指摘されていた出力の冗長さへの対応という位置付け（9to5google.com / ai.google.dev, 2026-07-21）
- **Googleが「Gemini 4」を予告**：3.6 Flash発表と同時にティザー。具体的な時期・仕様は未公表（**未確認の予告段階として記録**・9to5google.com, 2026-07-21）

### このメディアへの示唆

- 各社の値下げ・無料枠拡大が同時進行している（ChatGPT無料の無制限化・Gemini 3.6 Flashの値下げ・Opus 5がOpus 4.8と同価格で1Mトークン）。「AIに課金する理由・しない理由」を扱う既存の記事ネタ（2026-05-25リサーチ由来）は、無料枠が広がったことで前提が変わっている。書くなら2026年8月時点の実態に更新が必要

#### 【10:15 補足回】同日2回目の自動実行による差分追記

- **OpenAI・Google（Gemini）とも、8/10〜8/11に新規の発表は確認できず**。朝の回（07:43）で記録したChatGPT 8/6アップデート・Gemini 3.6 Flashが最新のまま。この領域は差分なし

（定期リサーチで随時追記）

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
