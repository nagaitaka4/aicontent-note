---
no: 70
series:
series_no:
title: Claudeに会社の情報を渡して大丈夫か。データが学習に使われる条件
date:
url: https://aicontent-note.com/claude-company-data-training/
slug: claude-company-data-training
status: draft
description: Claudeのデータは学習に使われるのか。Free・Pro・Maxでは「AIモデルの改善に協力する」の設定で、通常のチャットやClaude Codeをモデル改善に使うか選べます。私は気づかずオンのまま取引先名や領収書を入れていたので、公式の条件と自分の運用を分けて書きます。
eyecatch_alt: Claudeに会社の情報を渡して大丈夫か、データが学習に使われる条件と自分の設定を確かめた記事のアイキャッチ画像
category: Claude Code活用
tags: Claude,Claude Code,データ学習,プライバシー設定,非エンジニア
eyecatch: eyecatch_0070.png
---

# Claudeに会社の情報を渡して大丈夫か。データが学習に使われる条件

Free・Pro・Maxの通常のチャットは、設定で学習利用が変わります。
Claude Codeも対象で、設定名は「AIモデルの改善に協力する」です。
私は気づかずオンのまま、取引先の会社名や領収書PDFを入れていました。

## 通常のチャットが学習に使われるかは、プランと設定で決まる

通常のチャットの学習利用は、プランと設定で変わります。
Claude Codeも確認の対象です。
設定だけでは説明できない例外もあります。

| プランと設定 | 学習に使われるか | 保持期間 | 根拠 |
| --- | --- | --- | --- |
| Free・Pro・Max＋オン | 通常のチャットやClaude Codeをモデル改善に使う | 最大5年 | [Data usage](https://code.claude.com/docs/en/data-usage) / [保持期間](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data) |
| Free・Pro・Max＋オフ | 新規・保存済みの会話を今後の学習に使わない。例外あり | 30日 | [Data usage](https://code.claude.com/docs/en/data-usage) / [設定変更](https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings) |
| Team・Enterprise・API | 商用規約の範囲では、モデル改善用の提供を選ばない限り使わない | 上記の保持期間とは別の規定 | [Data usage](https://code.claude.com/docs/en/data-usage) |

※Claude.aiのIncognitoチャットは、オンでも学習に使われません。[公式説明](https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training)

Claudeという名前だけで、学習に使われるかは判断できません。
有料のPro・Maxでも、オンなら通常の会話が対象になります。

### 最大5年の対象と、オフでも残る例外

最大5年の保持は、非識別化された形式の学習用データの話です。
対象は、設定をオンにした後に新しく始めた会話や再開した会話です。
オン以前の全履歴に、この期間が一律に適用されるわけではありません。[保持期間の説明](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data)

安全性レビューの対象や、送ったフィードバックには例外があります。
オフでも、安全性の改善やモデル学習に使われる場合があります。[設定変更の説明](https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings) / [消費者向け規約](https://www.anthropic.com/legal/consumer-terms)

ただし、学習を許可しなければ何でも入力してよい、という意味ではありません。
入力の処理に必要な権利や許可を持つ責任は、利用者にあります。[消費者向け規約](https://www.anthropic.com/legal/consumer-terms)

【ポイント】<br>
有料プランでも学習利用の確認は必要です。プラン・設定・例外を分けて見ます。

## オンかオフか、どこで確かめるか

設定の場所は、プライバシー画面です。
確認する項目は、「AIモデルの改善に協力する」です。
現在の状態を画面で確かめられます。

1. 名前のメニューから「設定」を開く。
2. 「プライバシー」を開く。
3. 「AIモデルの改善に協力する」の状態を見る。

[プライバシー設定](https://claude.ai/settings/data-privacy-controls)から直接開くこともできます。
英語UIの項目名は、Help Improve our AI modelsです。[公式手順](https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings)

［設定画面の画像を挿入］

*「AIモデルの改善に協力する」がオフの状態。*

### 既定でオンだったとは言えない

[公式発表](https://www.anthropic.com/news/updates-to-our-consumer-terms)には、既定値がオンかオフかの記載はありません。
新規ユーザーは、登録時に選びます。
既存ユーザーには、選択用のポップアップが表示される案内でした。

選択期限は、2025年10月8日でした。
以後も利用を続けるには、設定の選択が必要という案内です。
これは、2025年8月28日公開の発表に書かれた内容です。[発表原文](https://www.anthropic.com/news/updates-to-our-consumer-terms)

私は選んだ記憶がないのに、確認したときはオンでした。
「後で」を押したのか、読まずに通したのかも分かりません。

【チェック】<br>
契約したプランの記憶だけでなく、現在のアカウントの設定を確認する。

## 私が渡しているもの・渡さないもの

私は、MaxでClaude Codeを毎日使っています。
Claude.aiのチャットも使います。
オンの状態で渡していた情報を、用途と一緒に書き出しました。

| 種類 | 実物の例 | 渡している？ | 決めた理由 |
| --- | --- | --- | --- |
| 取引先の会社名 | 営業リスト・求人情報から抽出した会社名 | 渡している | 分類・優先づけをAIに任せるため |
| 領収書・経費台帳 | 領収書PDF（取引先名・金額）・経費台帳 | 渡している | 仕訳と集計を任せるため |
| 制作中の案件データ | ロゴ案・制作ルール | 渡している | 制作の下書きを任せるため |
| 私のメディアのデータ | 記事本文・検索の数字・X投稿 | 渡している | 私の情報なので迷わない |
| パスワード・ログイン情報 | WordPress等の認証情報 | 渡していない | AIにはログイン・入力をさせないと決めている |
| クレジットカード・口座の情報 | カード番号・口座番号 | 渡していない | 財務情報は入れない |

渡している種類で見ると、半分以上に私以外の情報が含まれます。
それを、モデル改善の対象になり得る設定のまま送っていました。
実際に学習に使われたかまでは、確認できていません。

学習設定とは別に、Claude CodeはPCにも記録を残します。

【メモ】<br>
PCの`~/.claude/projects/`に平文で標準30日残ります。期間は、`cleanupPeriodDays`で変更できます。[公式](https://code.claude.com/docs/en/data-usage)

顧客の情報を預ける判断は、職種ごとの記事でも扱っています。
士業での使い方は、次の2本から読めます。

・[弁護士業務の案件管理と書類作成に、Claude Codeを当てはめた](https://aicontent-note.com/claude-code-lawyer-case-management/)<br>
・[社労士業務の就業規則・36協定に、Claude Codeを当てはめた](https://aicontent-note.com/claude-code-labor-consultant-rules-agreement/)<br>

---

＼　ブログ更新が止まっている・記事運用を任せたい方へ　／
企画から執筆・公開まで、まるごとお任せください。お気軽にご相談を。

[お問い合わせフォームはこちら](https://aicontent-note.com/contact/)

---

## オフにして、何が変わったか

私は、確認した設定をオフに切り替えました。
変更後の扱いは、過去の会話も含めて確認しました。
これからの学習と、すでに始まった学習では扱いが違います。

| 項目 | オフにすると |
| --- | --- |
| これから始めるチャット・コーディングセッション | 今後のモデル学習には使われない |
| 保存済みの過去のチャット・セッション | 今後のモデル学習には使われない |
| 保持期間 | モデル改善を許可する場合の最大5年から30日へ |
| すでに始まっている学習・作られたモデル | そこからは外れない |
| 安全性レビュー・送信したフィードバック | オフでも利用される例外がある |
| 位置情報メタデータ | 別の設定。連動しない |

学習と保持の根拠は、[設定変更](https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings)と[保持期間](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data)の説明です。
フィードバックの例外は、[消費者向け規約](https://www.anthropic.com/legal/consumer-terms)にもあります。
位置情報との関係は、私の画面で確認しました。

【アラート】<br>
オフへの変更で、すでに始まった学習や作られたモデルからは外れません。

その範囲を理解したうえで、私は切り替えました。
取引先の会社名や案件データを、日常的に入れているからです。

私の画面では、切り替え時の確認ダイアログは出ませんでした。
使える機能も変わらず、位置情報メタデータはオンのままでした。

この記事が扱うのは、学習に使われるかどうかです。
情報が漏れるかどうかは、別の話です。
オフにした経験を、そのまま安全性の保証にはできません。

## 会社で使うと、Pro・MaxとTeamは何が違うか

会社で使う場合も、契約と学習条件を分けて見ます。
Pro・MaxとTeamでは、その条件が異なります。
人数や料金も含め、確認できる項目を並べます。

・**Pro・Max**：消費者向けの範囲で、モデル改善はオプトアウト方式です。[Data usage](https://code.claude.com/docs/en/data-usage) / [料金比較](https://claude.com/pricing)<br>
・**Team**：商用規約側の契約で、既定ではコンテンツを学習に使いません。料金比較の原文は、`No model training on your content by default`です。[料金比較](https://claude.com/pricing) / [商用側の対象](https://www.anthropic.com/news/updates-to-our-consumer-terms)<br>
・**Teamの人数と料金**：2〜150名向けです。標準席の月額は、1席あたり年払いで$20、月払いで$25です。日本語ページも米ドル表記です。[日本語料金ページ](https://claude.com/ja/pricing)<br>
・**会社のメールアドレス**：組織のEnterpriseアカウントに紐づく可能性があります。その場合、管理者が入力等の内容にアクセスできることがあります。紐づけ前には通知があります。[Business Domains条項](https://www.anthropic.com/legal/consumer-terms)<br>

### 法人名義でも、規約の範囲は確認が必要

消費者向け規約には、`for individuals or entities`とあります。
個人でも法人でも、Claude.ai／Proは消費者向け規約の範囲です。
会社での利用という理由だけで、商用規約側になるわけではありません。[規約の適用範囲](https://www.anthropic.com/legal/consumer-terms)

【インフォ】<br>
Pro・Maxは消費者向け規約とオプトアウト方式。Teamは商用規約側で、既定では学習に使いません。

## 渡す前に決めておく3つ

次に情報を渡す前に、確認することを3つに絞ります。
設定だけでなく、入力している情報も見ます。
そのうえで、今後の使い方を決めます。

1. **現在の設定を見る。** オンなら、通常の会話をモデル改善に使う設定です。
2. **入れているものを書き出す。** 本人の情報か、それ以外の情報かを分けます。分類や集計など、渡す目的も一緒に書きます。
3. **今後の設定と契約を決める。** 他者の情報を日常的に入れるなら、オフにするかを判断します。Teamも含めて契約を比べる場合は、人数・料金・学習条件を照らし合わせます。

私は、私以外の情報を日常的に入れるため、オフにしました。
切り替えても、使える機能は変わりませんでした。
入力するものと設定を結びつけて考えることが、私には必要でした。

---

＼　ブログ更新が止まっている・記事運用を任せたい方へ　／
企画から執筆・公開まで、まるごとお任せください。お気軽にご相談を。

[お問い合わせフォームはこちら](https://aicontent-note.com/contact/)

---

**関連記事**
・[弁護士業務の案件管理と書類作成に、Claude Codeを当てはめた](https://aicontent-note.com/claude-code-lawyer-case-management/)
・[社労士業務の就業規則・36協定に、Claude Codeを当てはめた](https://aicontent-note.com/claude-code-labor-consultant-rules-agreement/)
・[Claude Codeとは何か？できること・使い方を実際に使って整理した](https://aicontent-note.com/claude-code-introduction/)
