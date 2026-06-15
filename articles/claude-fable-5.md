---
no: 36
title: Claude Fable 5とは？Mythos 5・Opus 4.8との違い
date: 2026-06-12
url: https://aicontent-note.com/claude-fable-5/
slug: claude-fable-5
status: published
series: 
series_no: 
description: Claude Fable 5は2026年6月9日に公開されたMythosクラスの一般公開版モデルです。一般向けのFable 5・政府向けのMythos 5・一世代前のOpus 4.8、3つの違いをAnthropicの公式発表をもとに整理します。
eyecatch: eyecatch_0036.png
eyecatch_alt: Claude Fable 5とMythos 5・Opus 4.8の違いを整理した記事のアイキャッチ
category: Claude Code活用
tags: Claude,Fable 5,Anthropic,Mythos 5,Opus 4.8
---

# Claude Fable 5とは？Mythos 5・Opus 4.8との違い

**Claude Fable 5は、2026年6月時点でのClaudeの最上位モデルです。** Anthropicが予告していたMythosクラスのモデルが、一般ユーザー向けに公開された形です。

「Fable 5」「Mythos 5」「Opus 4.8」と名称が増えてきて混乱している方向けに、3つの関係をAnthropicの公式発表をもとに整理します。

---

## Claude Fable 5とは何か

Anthropicの発表では、コーディング・知識・ビジョン・科学研究分野の主要ベンチマークでSOTA（最高水準）の性能を達成したとされています。

> 【インフォ】
> SOTAとは「State of the Art」の略で、その時点でのベンチマーク最高値を指します。

APIの料金は入力$10/100万トークン、出力$50/100万トークン。Pro・MaxプランユーザーはサブスクリプションでFable 5が利用でき、2026年6月22日まで利用プランの上限内に含まれます。ただし、Fable 5はOpusの2倍の使用量を消費します。

---

## FableとMythosというモデルを整理

「Fable 5」と「Mythos 5」。表で整理します。

| 項目 | Claude Fable 5 | Claude Mythos 5 |
|---|---|---|
| 対象 | 一般ユーザー | 米政府・重要インフラ組織 |
| 公開状況 | 公開済み（2026/6/9） | 非公開（限定展開） |
| セーフガード | フルセーフガード付き | 一部セーフガードを緩和 |
| 展開場所 | claude.ai・API・Claude Code | Project Glasswing（15カ国以上・150以上の組織） |
| ベースモデル | 同一 | 同一 |

> 【インフォ】
> セーフガードとは、AIが有害な用途に使われないようにAnthropicが設けた安全制御の仕組みです。特定のリクエストを検知して応答を制限したり、別のモデルに切り替えたりします。Fable 5はこのセーフガードをフルで搭載しており、Mythos 5は政府向けの用途に対応するため一部を緩和しています。

つまり、一般ユーザーが利用するFable 5と、政府向けのMythos 5は兄弟モデルのような関係です。同じモデルを基盤としつつ、用途と安全設計の違いで名称が分かれています。

Mythos 5は政府・重要インフラ組織向けの限定展開であり、一般ユーザーが申し込んだり入手したりする手段はありません。実務上も特に関係しないと考えていいと思います。

> 【ポイント】
> 一般ユーザーが使えるのはFable 5のみ。Mythos 5は政府・重要インフラ向けの限定版です。

---

## Fable 5とOpus 4.8の違い

Fable 5がリリースされる前、Claudeの最上位モデルはOpus 4.8でした。2つの違いを整理します。

| 項目 | Claude Fable 5 | Claude Opus 4.8 |
|---|---|---|
| 位置づけ | 現行最上位 | 一世代前の最上位 |
| 性能 | 最上位 | 上位 |
| セーフガード | 強化（一部リクエストでフォールバック） | 標準（Fable 5のフォールバック先として機能） |
| 特徴 | 最新モデル | フォールバックとしても利用 |
| API料金 | 入力$10・出力$50（/100万トークン） | 据え置き（Opus 4.7と同一） |

Opus 4.8はFable 5の一世代前の最上位モデルで、2026年5月29日にリリースされました。Fable 5の登場後も引き続き利用でき、Fable 5のフォールバック先としても機能します。

[Claude Opus 4.8について詳しくはこちら](https://aicontent-note.com/claude-opus-4-8-honesty/)

---

## セーフガードとOpus 4.8のフォールバック仕様

Fable 5固有の仕様として、セーフガードによる制限があります。

> 【インフォ】
> フォールバックとは、メインの処理が制限された場合に、自動的に別の手段へ切り替える仕組みのことです。Fable 5では、セーフガードが発動したリクエストをOpus 4.8が代わりに処理します。

Anthropicによると、セーフガードが発動するのは全体の5%未満のセッションです。具体的には、サイバーセキュリティ・生物/化学・蒸留関連のリクエストが該当します。

このフォールバック動作はユーザーが設定でON/OFFを切り替えられます。ONの場合はフラグが立ったリクエストが自動的にOpus 4.8へ切り替わりチャットが続行されます。OFFにした場合はチャットが一時停止されます。フォールバック時はFable 5の料金ではなくOpus 4.8の料金が適用されます。

> 【アラート】
> 通常の業務・コンテンツ制作・一般的なコーディング用途では、ほとんどの場合Fable 5がそのまま応答します。フォールバックが発生しやすいのは、セキュリティや化学系のリクエストです。

Mythos 5が一部セーフガードを緩和しているのは、電力インフラや医療など、高度なセキュリティ分析を必要とする政府機関向けの要件への対応です。

---

＼ ブログ更新が止まっている・記事運用を任せたい方へ ／
企画から執筆・公開まで、まるごとお任せください。お気軽にご相談を。

[お問い合わせフォームはこちら](https://aicontent-note.com/contact/)

---

## Pro/Maxユーザーへの実務的な影響

Pro・MaxプランのユーザーはFable 5を2026年6月22日まで利用プランの上限内で利用できます。6月23日以降はクレジットが別途必要になります。

ただし、6月22日までの期間中も、Fable 5はOpusの2倍の使用量を消費します。上限内には含まれますが、消費ペースは早くなる点に注意が必要です。

> 【チェック】
> 6/22まで：プラン上限内で利用可能（ただしOpusの2倍消費）
> 6/23以降：クレジットが別途必要

6月22日までの期間中に、用途に応じてFable 5とOpus 4.8を使い比べておくのがよさそうです。

なお、Claudeのサブスクリプション構造は6月15日から一部変更があります。自動化・Agent SDK・GitHub Actions利用分が別枠クレジットになる変更で、手動でClaude Codeを使う用途への影響は限定的です。

[課金変更の詳細はこちら](https://aicontent-note.com/claude-subscription-change-june-2026/)

---

## Claude CodeでのFable 5の使い方

Fable 5はclaude.ai・Claude API・Claude Codeのいずれからでも利用できます。claude.aiの場合はモデル選択画面から切り替えられます。

Claude Codeでは、現時点でFast modeのデフォルトモデルがOpus 4.8になっています。精度を重視するコード生成や長時間のエージェント処理を行う場合は、Fable 5が選択肢になります。最新性能を試したい場合はFable 5、Fast modeをそのまま使う場合はOpus 4.8という使い分けになります。

[Claude Codeの基本的な使い方はこちら](https://aicontent-note.com/claude-code-introduction/)

---

## 3つのモデルの関係を整理する

・Fable 5は一般向けの最新最上位モデル（2026年6月9日公開）
・Fable 5は、6/22まではプラン上限内（Opusの2倍消費）、6/23以降はクレジット必要
・Mythos 5は政府・重要インフラ向けの限定版。一般入手は不可
・Opus 4.8は一世代前の最上位モデル。Fable 5のフォールバックとしても機能

名称が増えて分かりにくくなっていますが、一般ユーザーが使う場合は「Fable 5が最新モデル」と覚えておけば十分です。

---

＼ ブログ更新が止まっている・記事運用を任せたい方へ ／
企画から執筆・公開まで、まるごとお任せください。お気軽にご相談を。

[お問い合わせフォームはこちら](https://aicontent-note.com/contact/)

---

**関連記事**
・[Claude Opus 4.8。AIが「ここ怪しい」と言うようになった](https://aicontent-note.com/claude-opus-4-8-honesty/)
・[Claudeの課金が6月から変わる。影響がある使い方・ない使い方](https://aicontent-note.com/claude-subscription-change-june-2026/)
・[Claude Codeとは何か？できること・使い方を実際に使って整理した](https://aicontent-note.com/claude-code-introduction/)
