# 材料シート：Claude Codeはデザイナーの仕事に使えるか（待機列・D-52）

作成：2026-10-19 07時台（定期リサーチ・月曜のフル版②③。リポジトリの実物をCCが数えた）
> **執筆側はこのシートの事実だけを使う。ここに無い数字・仕様は書かない。**足りない数字は「未計測」と書き、推測で埋めない。
> シートの更新：定期リサーチ（月・金）が公式の変更を見つけたら「3. 公式の一次情報」に追記する。X編集部が同じ題材の下書き・投稿を作ったら「4. X編集部の在庫」に追記する。

## 1. 記事の芯

**「デザイナー本人が、ロゴ・アイキャッチ・サイトのファーストビュー（FV）でClaude Codeに何を任せ、何を人に残したか」。**
新シリーズ「Claude Codeは◯◯の仕事に使えるか」（TOP10 #4 事務職が1本目）の2本目。読者が決めたいこと：デザインの仕事にClaude Codeを入れて得をするのはどの工程か。
⚠️ 絵そのものを作るのはChatGPT（画像生成はGPT一択・`editorial-meeting.md` 回答の記録 9/14 C-5）。**Claude Codeが受け持つのは、指示書・ルール・見本の整理・判定・入稿の側**。題の答えはここで分かれる。

## 2. この環境の実物（CCが`git log`・ファイル数で数えた・2026-10-19）

| 仕事 | 実物 | 期間・件数 | 出どころ |
|---|---|---|---|
| サイト制作（OK MADE） | 制作・営業・保守の部署を分けたリポジトリ。FVの指示書・判定基準・見本の語彙（`production/fv-flow.md`・`fv-gates.md`・`fv-judge-rubric.md`・`design-vocabulary.md`ほか） | **450コミット**（2026-08-20〜10-16。8月7・9月233・10月210）。うちFVに触れたコミット101 | `~/Documents/GitHub/ok-made` |
| ロゴ | ロゴ制作の知識をまとめたリポジトリ（ChatGPTのマイGPT用） | `logo-system` 20コミット（5/20〜8/14）・`logo-system02` 17・`gpt-logo-design` 10（7/8〜） | 各リポジトリ |
| アイキャッチ | 記事のアイキャッチ。参考画像を添付→CCがプロンプトを1案→ChatGPTで生成→CCがリサイズ・リネーム | **77枚**（`images/eyecatch_*.png`）。no.23でタッチがずれ、型に「絵のタッチは参考画像と同じ」を足した（10/15） | `images/`・メモリ`feedback_eyecatch_prompt.md` |
| 権利の線引き | ロゴのパクリ・フォントの記事（no.68）を、デザイナー本人の問いから作った | GSC直近3か月＝3クリック・110表示・7.3位 | `articles/logo-plagiarism-how-far-ai-copyright-font.md` |

- ⚠️ OK MADEにはお客さまの名前・制作物が入っている。**記事に出すときは名前を伏せ、工程と件数だけにする**

## 3. 公式の一次情報

- **単体のClaude Design（claude.ai/design）は2026-12-14までに終了**：Claude Code 2.1.302のCHANGELOG verbatim `Added a notice to /design-sync and /design-login that standalone Claude Design (claude.ai/design) closes by December 14, 2026`（`research/trends.md` 2026-10-17）。**本人は未使用**（リポジトリに使用記録なし）
- Claude Docs・Slidesの開始と、Claude Designが会話の中で使えること（9/16公式ブログ）verbatim `Claude Docs and Claude Slides are new today, and Claude Design now works inside your conversations too.` `All three are in beta on paid plans`（`research/trends.md` 2026-09-18）
- 執筆の直前に、Claude Designの終了後の行き先（会話の中で使う形に一本化か）を英語の公式で取り直す

## 4. X編集部の在庫

- `LOGO68-01`「AIで作った作例、タッチやカラーを変えても見本から離れなかった」・`LOGO68-02`「Canvaのテンプレートのロゴは規約では商標に使えない」（`knowledge/x/queue.md`・記事側に参照なし＝`x-article-sync-check.py` 10/19）
- アイキャッチのタッチずれ（10/15）はD-50（バックログ△）にある

## 5. 既存記事との重なり

- no.68 ロゴのパクリはどこまで（権利の線）＝**参考にしてよい範囲**の問い。こちらは**仕事に入れてどの工程が楽になるか**の問い。権利はno.68へリンク
- no.14 Claude Codeと相性のいい仕事（職種一覧・42クリック・827表示）の隣。1つの職種を実物で掘る
- D-48 ホームページを作れるか（△・バックログ）とは別の問い。サイト制作の工程はこの記事ではFVの1節だけにする

## 6. 需要（2026-10-19 Googleサジェスト・2語まで）

- `claude デザイナー`10（使い方／スキル／活用／**claude code web デザイナー**／claude cowork デザイナー）
- `claude デザイン`10（使い方／とは／スキル／システム／プロンプト）・`claude design`10（使い方／料金／何ができる）
- `ai デザイナー`8（**仕事 なくなる**／失業／活用／不要）
- GSC（直近3か月・10/19）：ロゴの束＝`ロゴ パクリ どこまで`12表示1クリック・`ロゴ パクリ`5・`デザイン パクリ どこまで`2・`ロゴデザイン やってはいけない`2／職種の束＝`claude 担当職種`20・`claude code 仕事`11

## 7. まだ無いもの

- **3つの仕事（サイト・ロゴ・アイキャッチ）で、Claude Codeを入れて一番楽になった工程と、楽にならなかった工程はどれか**（本人にしか答えられない）
- **OK MADEのFVを記事に出してよいか**（お客さまの名前を伏せた工程と件数だけでもよいか）。9/12に「OK MADEの部署設計の実況は内輪」とユーザーが判断している＝出すなら工程の話に限る
- 作業時間の差は未計測（`ok-made/prospects/work-time.jsonl`に記録があるが、中身はまだ読んでいない）
- Claude Designは未使用。使うなら実験として行う（終了日12/14より前）
