# 材料シート：Claude in ChromeでWordPressに入稿（TOP10 #6・D-09）

作成：2026-09-11 18:40（一次情報を直接確認）。**執筆可能：◯（確認事項なし）**
> **執筆側はこのシートの事実だけを使う。ここに無い数字・仕様は書かない。**足りない数字は「未計測」と書き、推測で埋めない。
> シートの更新：定期リサーチ（月・金）が公式の変更を見つけたら「3. 公式の一次情報」に追記する。X編集部が同じ題材の下書き・投稿を作ったら「4. X編集部の在庫」に追記する。

## 1. 記事の芯

**「WordPressの入稿を、Claude CodeにChromeごと任せた。4本で人が触ったのは公開ボタンだけ」。**
主役は実作業の手順（何を任せ、どこで止めたか）。no.64（自動化の限界＝判断論）と分けて、操作の実物に絞る。

## 2. この環境の実物

| 項目 | 値 | 出どころ |
|---|---|---|
| 初回 | 2026-08-28・no.63（V-05） | `operations/automation-log.md` |
| 実施した記事 | no.63（8/28）・no.64（9/2）・no.65（9/4）・no.66（9/10）＝**4本** | `operations/article-md-workflow.md` |
| 工程 | 11工程のうち**10を自動化、「公開」だけ人**（2026-08-27決定・成否に関わらず自動化しない） | `automation-log.md` V-05の表 |
| 使ったもの | Chrome拡張（`claude-in-chrome`）＝いつものChromeなのでログイン済み／WP REST API＋nonce／画像は`file_upload`／SEO SIMPLE PACKの説明文はエディタの`textarea`＋`savePost()` | 同上「詰まった点」6件 |
| 止めた場面 | ①no.57（9/9）：WPに「MDから作れない手作業の復元」（`wp:list`）が残っていて、全文差し替えを部分差し替えに変えた ②no.66（9/10）：WP側で人が15:27に編集していたのをSHA照合で検出し、上書きせず残した | `operations/lessons.md` 2026-09-09・2026-09-10 |
| 変換 | `operations/md-to-wp.py`（MD→Gutenbergブロック・2026-08-26新設。それまで61本を手作業で入稿） | `operations/automation-log.md`・メモリ`feedback_automation` |
| 本文中の画像 | no.65が初（2枚・9/3〜9/4） | 取材待ちリスト |

## 3. 公式の一次情報（[Use Claude Code with Chrome](https://code.claude.com/docs/en/chrome)・2026-09-11取得）

- 必要なもの：Chrome/Edge（Chromium系も可・WSL不可）／拡張機能**v1.0.36以上**／**Pro・Max・Team・Enterprise**（API鍵・長期トークンでは使えない）
- verbatim：`Claude opens new tabs for browser tasks and shares your browser's login state, so it can access any site you're already signed into.` ／ `When Claude encounters a login page or CAPTCHA, it pauses and asks you to handle it manually.`
- CLIは`claude --chrome`、`/chrome`で状態確認・既定で有効化。VS Codeは拡張があれば追加設定なし
- 許可：`Claude in Chrome wants to`のダイアログ。サイト単位の許可は拡張側の設定
- ファイルのアップロード：v2.1.211以降・合計10MBまで・Readを拒否したファイルは不可
- できること（公式の列挙）：ログイン済みのWebアプリ操作・フォーム入力・データ抽出・GIF記録・スクリーンショット保存
- ⚠️ **この環境はデスクトップアプリ＋拡張機能**。CLIの`--chrome`とは入口が違うので、記事では自分の環境を明記する

## 4. X編集部の在庫（2026-09-11確認）

- `自動化64-リ`（9/3・8ビュー）「WordPressのブログの入稿、もう自分ではやってません」（no.64のリンク型）／`CU-気`（9/7・13ビュー）画面操作が裏で動くように
- ⚠️ `CU-気`はComputer Use（画面操作）の話で、Chrome拡張とは別の機能。混ぜない

## 5. 既存記事との重なり

- no.18 入稿・整形・公開はどこまで効率化できるか（4月・手作業時代・26表示3クリック）／no.64 ブログ運用はどこまで自動化できたか（判断論・0表示）。**この記事は「Chrome拡張で実際にやった手順と、止めた2場面」に絞り、判断論はno.64へリンク**

## 6. 需要（2026-09-11実測）

`claude in chrome`9件（拡張機能／インストール／使い方／料金）・`claude code wordpress`10件（連携／mcp／開発／theme）・`claude code ブラウザ`6件（操作／版／テスト）

## 7. まだ無いもの

- **入稿1本あたりの所要時間は未計測**（手作業のときも未計測）。書くなら「工程数10→0」の形で、時間は書かない
- WP側の設定（SWELL・SEO SIMPLE PACK）が違う読者には手順がそのまま使えない → 「WordPressなら同じ形で組める」までにとどめる
