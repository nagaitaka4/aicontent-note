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

# Claudeに会社の情報を渡して大丈夫か。データが学習に使われる条件

Claudeでは、==通常のチャットが学習に使われるかは設定で変わり==ます。
この記事で扱うのは、入力した内容がモデル学習に使われるかだけです。
私はこの設定が気づかずオンのまま、取引先名や領収書を入れていました。

## 通常のチャットが学習に使われるかは、プランと設定で決まる

==答えは、プランと、モデル改善の設定がオンかオフかで決まります==。
情報漏洩やセキュリティ全般は、この記事では扱いません。
公式の条件を先に表にします。

| プラン | 学習に使われるか | 標準の保持期間 | 根拠 |
|---|---|---|---|
| Free・Pro・Max＋設定オン | 使われる | 5年 | [Claude Code公式 Data usage](https://code.claude.com/docs/en/data-usage) |
| Free・Pro・Max＋設定オフ | 使われない | 30日 | 同上 |
| Team・Enterprise・API | 既定で使わない | 30日 | 同上・[料金ページ](https://claude.com/pricing) |

※そのアカウントでClaude Codeを使った分も、同じ扱いです。<br>
※安全性レビュー対象の会話や、自分から送ったフィードバックには、別の保持期間が適用される場合があります。<br>
※Claude.aiのIncognitoチャットは例外で、設定がオンでも学習には使われません（[プライバシーセンター](https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training)）。

公式の原文は「when this setting is on」、つまり設定がオンのときに使う、です。
「Claudeだから危ない」でも「有料だから安全」でもなく、どの設定で使っているかで答えが変わります。

ただし、学習に使われない設定なら何でも入力してよい、という意味ではありません。
Anthropicの[Consumer Terms](https://www.anthropic.com/legal/consumer-terms)は、入力する情報の権利や許可を利用者側に求めています。
原文では「all rights, licenses, and permissions」を持つと利用者が保証します。

【ポイント】<br>
有料のPro・Maxでも、設定がオンなら学習に使われる

## オンかオフか、どこで確かめるか

設定の場所は、設定 → プライバシーです。
見るだけなら、1分かかりません。

1. Claudeの画面で、自分の名前を押す<br>
2. 「設定」→「プライバシー」を開く<br>
3. **AIモデルの改善にご協力ください**のスイッチを見る

URLで直接開くなら、[claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls)です。
英語表示では「Help Improve our AI models」という名前です（[プライバシーセンターの手順](https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings)）。

![Claudeの設定画面。プライバシーの項目にある「AIモデルの改善にご協力ください」のスイッチがオフになっている](https://aicontent-note.com/wp-content/uploads/2026/09/img_0070_01.png "設定 → プライバシーの画面。モデル改善の設定をオフにした状態")

### 既定でオンなのか、と聞かれると

公式には「既定はオン」とも「オフ」とも書かれていません。
新しく登録する人は、登録のときにこの設定を選びます。
以前からの利用者は、2025年10月8日までにポップアップで選ぶ流れでした（[Anthropicの発表](https://www.anthropic.com/news/updates-to-our-consumer-terms)）。

私のアカウントは、オンになっていました。
選んだ記憶はありません。
「後で」を押したのか、読まずに通したのかは、正直に言うと分かりません。

【チェック】<br>
設定を見るのは1分。オンかオフかを、今この場で確かめる

## 私が渡しているもの・渡さないもの

「会社の情報を入れていいか」を書いている本人が、オンのまま何を入れていたか。
Claude Codeに渡した記録から、そのまま並べます。

| 種類 | 実物の例 | 渡している？ | 決めた理由 |
|---|---|---|---|
| 取引先の会社名 | 営業リスト・求人情報から抽出した会社名 | 渡している | 分類と優先づけを任せるため |
| 領収書・経費台帳 | 領収書PDF（取引先名・金額）・経費台帳 | 渡している | 仕訳と集計を任せるため |
| 制作中の案件データ | ロゴ案・制作ルール | 渡している | 制作の下書きを任せるため |
| 自分のメディアのデータ | 記事本文・検索の数字・X投稿 | 渡している | 自分の情報なので迷わない |
| パスワード・ログイン情報 | WordPressなどの認証情報 | 渡していない | AIはログインしない・入力しないと決めている |
| クレジットカード・口座の情報 | カード番号・口座番号 | 渡していない | 財務情報は入れない |

6項目のうち3項目は、自分以外の情報でした。
それを、==モデル改善を許可する設定がオンの状態で送っていた==ことになります。

実際に学習に使われたかどうかは、利用者側からは確かめられません。
確かめられるのは、設定がオンだったところまでです。

【メモ】<br>
ローカルのClaude Codeは、PC側にも記録を残す。<br>
~/.claude/projects/ に平文で標準30日。cleanupPeriodDaysで変更可

顧客の情報を預けるかどうかは、職種ごとに分けて書いています。
弁護士向けは[弁護士業務の案件管理と書類作成に、Claude Codeを当てはめた](https://aicontent-note.com/claude-code-lawyer-case-management/)に。
社労士向けは[社労士業務の就業規則・36協定に、Claude Codeを当てはめた](https://aicontent-note.com/claude-code-labor-consultant-rules-agreement/)にあります。

---

＼　ブログ更新が止まっている・記事運用を任せたい方へ　／
企画から執筆・公開まで、まるごとお任せください。お気軽にご相談を。

[お問い合わせフォームはこちら](https://aicontent-note.com/contact/)

---

## オフにして、何が変わったか

オンだった設定を、オフに切り替えました。
変わることと、変わらないことを分けます。

| 項目 | オフにすると |
|---|---|
| これから始めるチャット・セッション | 今後のモデル学習には使われない |
| 保存済みの過去のチャット・セッション | 今後のモデル学習には使われない |
| 保持期間 | 5年 → 30日 |
| すでに始まっている学習・作られたモデル | 外れない |
| 安全性レビュー対象の会話 | オフでも、安全性の検出・ポリシー適用・安全性研究などに使われる場合がある |
| 自分から送ったフィードバック | オフでもモデル改善に使われる場合がある |
| 「ロケーションメタデータ」 | 別の設定。連動しない |

過去のチャットも「previous or new chats」として、今後の学習には使われなくなります。
すでに始まった学習からは外れません（[プライバシーセンター](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data)）。

【アラート】<br>
オフにしても、すでに始まった学習と、作られたモデルからは外れない

私がオフにした理由は、自分以外の情報を日常的に入れているからです。
切り替えに確認画面は出ず、使える機能も変わりませんでした。

情報が外に漏れるかどうかは、また別の話です。
==オフにしたから安全、とは言えません==。

## 会社で使うと、Pro・MaxとTeamは何が違うか

会社で使う前に見るのは、契約の種類です。
公式で確かめられた事実だけを並べます。

| | Pro・Max | Team |
|---|---|---|
| 規約 | Consumer Terms | Commercial Terms |
| モデル学習 | オプトアウト方式（設定で選ぶ） | 既定で使わない |
| 人数 | 1人 | 2〜150名 |

Claude Code公式は、Free・Pro・Maxを「consumer users」と呼びます。
Team・Enterprise・APIは「commercial users」です。
Pro・Maxはモデル改善を設定で選び、Teamは既定でモデル学習に使いません。

Teamの料金は、標準席が1席あたり月20ドル（年払い）か25ドル（月払い）です（[料金ページ](https://claude.com/ja/pricing)・米ドル表記）。

会社のメールアドレスで登録している人は、規約の「Business Domains」の項も見ておくといいです。
勤め先がAnthropicの企業契約を持つと、アカウントがそこに紐づく場合があります。
その場合、管理者が「monitor and control the Account」できる、と書かれています。

【インフォ】<br>
個人契約のPro・Maxは、学習に使うかを設定で選ぶ方式。<br>
Teamは会社側の契約で、既定ではモデル学習に使わない

## 渡す前に決めておく3つ

「安全か危険か」の二択にはなりません。
自分の設定と、入れているものを見てから決める話です。

1. 自分の設定を見る。オンなら、通常のチャットとセッションをモデル改善に使う設定になっている<br>
2. 入れているものを一度書き出す。自分の情報か、自分以外の情報か<br>
3. 自分以外の情報を日常的に入れるなら、扱いを決める<br>
（モデル改善をオフにする / Teamなどの商用プランを検討する / そもそも渡さない）

私はオフにしました。
使い勝手は変わらなかったので、迷っている人は先に設定だけ見るのがいい気がしています。

---

＼　ブログ更新が止まっている・記事運用を任せたい方へ　／
企画から執筆・公開まで、まるごとお任せください。お気軽にご相談を。

[お問い合わせフォームはこちら](https://aicontent-note.com/contact/)

---

**関連記事**
・[弁護士業務の案件管理と書類作成に、Claude Codeを当てはめた](https://aicontent-note.com/claude-code-lawyer-case-management/)
・[社労士業務の就業規則・36協定に、Claude Codeを当てはめた](https://aicontent-note.com/claude-code-labor-consultant-rules-agreement/)
・[Claude Codeとは何か？できること・使い方を実際に使って整理した](https://aicontent-note.com/claude-code-introduction/)
