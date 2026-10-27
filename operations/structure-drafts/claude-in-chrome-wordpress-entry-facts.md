# 材料シート：Claude CodeにWordPress入稿を任せていいか（TOP10 #1・D-35・新規no.77）

作成：2026-09-11 18:40／**全面更新：2026-10-23 20時台**（題を「no.18の全面改稿」から新規に。数字は4本の時点→10/23時点に数え直し）
> **執筆側はこのシートの事実だけを使う。ここに無い数字・仕様は書かない。**足りない数字は「未計測」と書き、推測で埋めない。
> シートの更新：定期リサーチ（月・金）が公式の変更を見つけたら「3. 公式の一次情報」に追記する。X編集部が同じ題材の下書き・投稿を作ったら「4. X編集部の在庫」に追記する。

## 1. 記事の芯

**⚠️ 2026-10-27訂正：Claude Codeにできるのは公開まで。下書き保存までは筆者が新しい記事で任せている範囲（公開中の記事を直したときの保存はClaude Code）。下の旧い芯の文は、この区別をしていない**

（旧）**「WordPressの入稿は、下書き保存までならClaude Codeに任せられる。いちばん危ないのは、人がWPで直した所を送り直しで消すこと。公開ボタンは人に残し、送る前にWPの今の本文と照合させる」。**
読者＝WordPressのブログをAIで書いていて、入稿まで任せていいか迷っている人。主役は約20本の入稿で起きた失敗と、それぞれ何で止めたか。no.18（4月・自動化前の工程整理・cc-writerシリーズ#04）・no.64（記事1本の流れ全体と判断論）とは問いが違う。

## 2. この環境の実物（2026-10-23 数え直し・根拠はファイルとgit履歴）

### 2-1 入稿した本数（数え方ごとに分ける・足して1つの数字にしない）

| 種類 | 本数 | 中身 | 出どころ |
|---|---|---|---|
| 新規の記事 | **14本**（no.63〜76。うち2本は入稿者の記載なし＝確実なのは12本） | 下書き保存までClaude Code・公開ボタンは人 | `automation-log.md` V-05・各記事の公開コミット |
| 公開済み記事の全面改稿 | **6本**（no.57・27・32・7・23・9） | 下書きを通さず公開中の本文を入れ替え | `rewrite-log.md` |
| 公開済み記事の部分置換 | 延べ12回・のべ26記事 | 旧題のリンク文言・1文・1段落など | `rewrite-log.md`・`lessons.md` |
| 固定ページ | 1本（AIっぽい文章チェッカー） | 下書きまで。SEO SIMPLE PACKの2欄は人が入力（自動モードの安全チェックで止まった） | `tools/post-mae-check/README.md` |
| それより前 | 約61本は人が手作業で入稿。no.62は変換スクリプトの出力を人が貼った | | メモリ`feedback_automation`・`lessons.md` 8/30 |

→ 本文では「新規と書き直しで約20本」と概数で書く（`feedback_no_exact_counts_in_prose`）。「67本」は9/19時点の公開済み記事の総数で、入稿した本数ではない（題に使わない）

### 2-2 今の分担（10/23時点）

| 工程 | 担当・方法 |
|---|---|
| Markdown→WordPressのブロックに変換（SWELLの装飾ブロック・区切り線・CTA・表の列幅・コード欄） | 変換スクリプト（`md-to-wp.py`・2026-08-26〜） |
| ログイン | **人**（いつものChromeでログイン済みの状態を使う） |
| 下書き作成（題・スラッグ・カテゴリー・タグ・コメントを閉じる） | Claude Code：WordPressのREST API（ログイン中のブラウザから） |
| アイキャッチ（画像を作るのはGPTで人）・本文中の画像 | リサイズ・ICCプロファイル除去・アップロード・alt・紐付けはClaude Code（Chrome拡張ごし） |
| 検索結果に出る説明文（SEO SIMPLE PACK） | Claude Code（エディターの欄）。本文を送る前に済ませる |
| 本文 | Claude Code：**WPの今の本文とブロックごとに照合**→送る→送った後にもう一度照合 |
| 確認 | Claude Code：公開ページ・プレビューで見出し・表・マーカー・記法の残り・抜粋・コメント設定を数える |
| 太字・マーカー・表の列幅・言い回しの直し | **人がWPで直す**→Claude CodeがMDへ写す |
| 公開ボタン | **人**（2026-08-27決定・成否に関わらず自動化しない） |
| 公開済み記事を直したときの保存 | Claude Code（10/4〜） |

### 2-3 人がWPで直した所（ログインと公開ボタン以外）

- **新規14本のうち、公開前に人がWPで直した記録があるのは11本**（no.69は直した人の記載なし・no.63は差分なし・no.76は公開時の直しなし・no.65は記録なし）。中身は太字・マーカー・表の列幅・言い回し・番号付きの手順を枠付きに、など。多い記事で20件ぐらい（no.75）
- ユーザーが毎回入れる直しの傾向（メモリ）：ブロックの中身を太字に／章の要の一文を太字に／「私は、」の後の読点
- → 「人が触るのはログインと公開ボタンだけ」はno.63の時点の話。今は**ほぼ毎回、見た目の仕上げを人がWPの画面でしている**

### 2-4 入稿で起きた失敗（38件から、読者に関係するものを種類で分けた）

| 種類 | 起きたこと | 今の止め方 | 出どころ |
|---|---|---|---|
| **人の直しを消す** | 人がWPで直した6か所を、本文の送り直しで**2回消した**（ユーザーの「元に戻りました」で発覚・リビジョンから復元） | 送る前にWPの今の本文を取り、ブロックごとに照合。WPにしか無いブロックがあれば送らずに確認 | `lessons.md` 2026-09-22（3件目） |
| 同上 | 本文を送った直後にエディターで保存したら、ブラウザに残っていた古い自動保存で**本文が巻き戻った**（ユーザーの「反映されていない」で発覚） | 本文を送ったあとにエディターで保存しない。説明文は先に入れる | `lessons.md` 2026-09-22（2件目）。**本文では原因（自動保存）を断定せず「本文が以前の内容に戻った」と書く**（no.77 GPT本文レビュー：WordPressの自動保存は別のリビジョンで、本文を直接上書きしない仕組み） |
| 同上 | 公開ボタンを押したとき、開いたままのエディターが古い状態で保存し、外したマーカーが戻った | エディターを読み直してから公開 | `lessons.md` 9/2 |
| 同上（止められた例） | 人がWPで編集していたのを照合で見つけ、上書きせず残した／WPで人が手で直した番号付きリストを、全文差し替えで消す前に止めた | 同上 | `lessons.md` 9/9・9/10 |
| **見た目が崩れる** | リンクの中に改行が入り、記事タイトルが「。」で切れて文が終わったように見えた（公開後に実物の画面で発覚・2記事3か所） | 変換スクリプトを直し、公開済み61本を全件確認。公開したら実物の画面を開く | `lessons.md` 2026-08-30 |
| 同上 | コード欄の改行が消えて1行の段落に（no.76）／番号付きの手順が改行なしの1段落に（no.74）／コードの記号がそのまま公開ページに（no.27・no.66） | 変換スクリプトを直す。反映後に記法の残りを数える | `9f6fd86`・`a01e726`・`lessons.md` 9/25 |
| 同上 | 太字の中にマーカーがあると太字が二重になる | **未修正**（その段落だけWPの形を使った） | 引き継ぎ |
| **付け忘れ・残し忘れ** | コメント欄を閉じ忘れた（2回）／切り分けで入れた試しの値「x」が抜粋に残ったまま公開された | 手順に入れる。試しの値を書かない・抜粋が空か確かめる | `lessons.md` 9/3・9/22、`wp-block-guide.md` |
| **送る途中で止まる** | ログインの合言葉（nonce）が取れず403／本文が1回の送信に入らない／分けて送った本文が2文字化けた | 取り方を変える・分けて送る・送る前後で一致を確かめる（SHA） | V-05・`lessons.md` 9/3・9/14 |
| 同上 | 本文の運び方（画像に詰める方法）を、自動モードの安全チェックが「データの持ち出し」として止めた | 一時のファイル入力欄を使う運び方に変えた（10/13〜） | `rewrite-log.md` 10/2・`wp-block-guide.md` |
| 同上 | 固定ページの説明文2欄の入力が安全チェックで止まった | 人が入力 | `tools/post-mae-check/README.md` |

### 2-5 時間

- **入稿1本あたりの所要時間は未計測**（手作業のときも未計測）。本人の目安：1本あたり約3時間（自分が動いた時間・アイキャッチ込み・入稿を自動にした後）、**いちばん効いたのはWP入稿の自動化**（no.32の確認・引き継ぎ）
- 手作業のころの入稿だけの時間 → **確認1**（下の7節）

### 2-6 本人の言葉（X・リプライの実物）

- 「SWELLだから入稿までは無理だと思ってました」（`試さず-気`・9/23・ユーザーが「約半年」を足した版）
- 「送信みたいな戻せない操作ほど手前で止めるのが安心／ブログの公開ボタンだけは今も人が押す」（9/14 リプライ）＝公開ボタンを人に残す理由
- no.64のメモ：「SWELLなので入稿までは無理だと思っていました。初めて試したときの下書きの仕上がりが、思っていたよりずっと良かったです」

## 3. 公式の一次情報（英語の原文・2026-10-23 実Chromeで取得）

**[Use Claude Code with Chrome](https://code.claude.com/docs/en/chrome)**
- `Claude opens new tabs for browser tasks and shares your browser's login state, so it can access any site you're already signed into.`
- `When Claude encounters a login page or CAPTCHA, it pauses and asks you to handle it manually.`
- 前提：Chrome・Edge（ほかのChromium系も検出）／拡張機能 v1.0.36以上／`A direct Anthropic plan (Pro, Max, Team, or Enterprise)`／`/login`でのサインインが必要（APIキー・長期トークンでは使えない）
- Capabilities：`Authenticated web apps: interact with Google Docs, Gmail, Notion, or any app you're logged into without API connectors`／`File uploads: attach files from your machine to upload fields on web pages`
- アップロード：`a single upload can include up to 10 MB of files in total`／Readを拒否したファイルは不可
- サイト単位の許可は拡張側の設定（`Site-level permissions are inherited from the Chrome extension.`）

**[Get started with Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome)**
- `Claude in Chrome is available for all paid plans (Pro, Max, Team, and Enterprise).`
- `Claude in Chrome is enhanced with our safety classifiers but is still risky.`
- デスクトップアプリ：Settings → Connectors → Claude in Chrome → Configure（この環境はデスクトップアプリ＋拡張機能。CLIの`--chrome`とは入口が違う）

**[Use Claude in Chrome safely](https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely)**
- 最大のリスクはプロンプトインジェクション（`malicious instructions hidden in web content ... could trick Claude into taking unintended actions`）
- `Claude takes screenshots of the tabs it's working in. Whatever is visible in one of those tabs is captured in the screenshots and becomes part of the conversation.`
- 推奨：`Use a separate browser profile without access to sensitive accounts`／`Start with trusted sites`
- **`You remain responsible for all browser actions taken by Claude performed on your behalf. This includes: Any content published or messages sent`**

## 4. X編集部の在庫（2026-10-23確認）

- 投稿：`自動化64-リ`（9/03・リンク型・11ビュー）「WordPressのブログの入稿、もう自分ではやってません」／`試さず-気`（9/23・14ビュー）「SWELLだから入稿までは無理だと思ってました」
- リプライで同じ実話を使った：9/10 @kiitoshiroko・9/14 @lklkfafa1（公開ボタンだけ人）・9/18 @oikon48・9/23 @moneymog・9/28 @ziko7110_2・10/11 @hisaju01・10/23 @MinatoYuichiro
- 9/3〜の分析：リンク型は「自分の制作の自動化」だと内輪寄りで伸びない（`published.md` ⑥）→ 記事は**読者が自分のブログで決めること**（任せていいか・何を人に残すか）で書く
- ⚠️ `CU-気`（9/7）はComputer Use（画面操作）の話で、Chrome拡張とは別の機能。混ぜない

## 5. 既存記事との重なり

- no.18「入稿・整形・公開はどこまで効率化できるか【Claude Code実践】」（4月・cc-writerシリーズ#04・GSC直近3か月22表示2クリック6.4位）：当時は「ブラウザ操作は任せられない」。**改稿しない**。公開後にno.18の末尾から新記事へ1行リンク
- no.64「ブログ運用はどこまで自動化できたか。人に残った2つの判断」（9/2・7表示14.9位）：入稿の分担表＋記事1本の流れ全体＋判断論。**この記事は入稿だけに絞り、分担表は繰り返さない**。全体の流れはno.64へリンク
- no.70「Claudeに会社の情報を渡して大丈夫か」：画面のスクリーンショットが会話に入る話はここへリンクできる

## 6. 需要（2026-10-23 実測）

- サジェスト：`claude code wordpress`10（連携／開発／mcp／theme／テーマ／skill）・`claude wordpress`10（**自動投稿**／mcp／seo）・`wordpress 入稿`7（自動化／方法／作業）・`claude in chrome`10（使い方／何ができる／料金／セキュリティ）・`claude 自動投稿`10（ほぼSNS）。`claude wordpress 連携`は2件（9/19は10件）。`wordpress 入稿 ai`・`chatgpt wordpress 入稿`は0件
- GSC（直近3か月）：「wordpress」「入稿」を含む検索語は表示0。no.18は22表示・2クリック

## 7. まだ無いもの

- 入稿1本あたりの所要時間（手作業のころも自動化後も未計測）→ **確認1：手作業のころの体感の時間を本人に聞く**
- WP側の設定（SWELL・SEO SIMPLE PACK）が違う読者には手順がそのまま使えない →「WordPressなら同じ形で組める」までにとどめ、手順の細部（nonce・REST・SHA）は書かない
- 太字の二重は未修正（書くなら「まだ直っていない」と書く）
