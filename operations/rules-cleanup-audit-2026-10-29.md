> 2026-10-29 別のエージェント（会話を持たない）がルールファイル6本を全行読んで洗い出した結果。CCが数か所を実物で確認済み（除外台帳342行〜・フォロー運用600行〜・金曜の編集会議1699行・cb.shとmarketing-research-mon-friのSKILL.mdが残っている・task-managementのTOP5表記・x-post-flow 252行「同じ日に複数投稿しない」）。**まだ何も直していない。**

# ルールファイル整理のための洗い出し（読むだけで、編集・コミットはしていません）

対象の6ファイルは全行を読みました。参考ファイル（constraints.py・lessons.md の見出し・MEMORY.md）とスクリプト（x-gate.py・x-hook.py・article-self-check.py・md-to-wp.py）は、照合に必要な所を確認しました。参照先ファイルがあるかどうかは `ls` で確かめています。

**結論**：いちばん効くのは `rules/x-post-flow.md` です。全1,808行のうち約530行は削るか移せます（要確認分まで含めると約700行）。その大半は次の3つです。
- フォロー数の記録
- 除外台帳・対象リストのような日々の状態データ
- 同じ表の重複と、日付つきの経緯

もう一つの問題は、投稿頻度・ランク・取材の条件・朝ブリーフの時刻について、新旧の記述が並んで残っていることです。CCが古い方を読む危険がいちばん高いのはここです。

---

## 1. 重複（43件）

| # | 場所 | 中身 | 提案 | 減る行数 |
|---|---|---|---|---|
| 1 | CLAUDE.md:17-25／article-flow.md:29／article-flow.md:65-67 | ファイルから読む（title の grep・CTA のコピー・製品名） | CLAUDE.md に残す。article-flow:29 は削除、65-67 は「CLAUDE.md の絶対ルールを実行」の1行にする | 3 |
| 2 | CLAUDE.md:49／article-flow.md:38／constraints.py `title_max` | タイトル35字（理想30〜33字） | constraints を正にし、2か所の数値を削除 | 1 |
| 3 | CLAUDE.md:44／article-flow.md:72 | 前提「見やすく…堅い表現は使わない」が同じ文 | article-flow 5章を正にし、CLAUDE.md は短い参照にする | 0（文を短く） |
| 4 | CLAUDE.md:71／task-management.md:3／session-handoff.md:29 | 「TOP10は tasks/README.md が唯一の正（TOP6は廃止）」 | task-management:3 に1か所。ほかは参照のみ | 1 |
| 5 | CLAUDE.md:87-88／task-management.md:141-156 | 記事の編集会議の進め方（A→B→C・1件ずつ・ファイルにある答え） | task-management に一本化。CLAUDE.md はトリガー語と参照だけ | 2 |
| 6 | CLAUDE.md:90-99／article-flow.md:54-55 | 構成案・本文の提示4手順と「書き換えか削る」。CLAUDE.md→article-flow 2章、article-flow→CLAUDE.md と**参照が堂々巡り** | 手順の本体を article-flow 2章へ移す。CLAUDE.md はトリガーの1〜2行 | CLAUDE −7／article-flow +3 |
| 7 | CLAUDE.md:103-107／x-post-flow.md:1607-1674 | Xのトリガー2つ | CLAUDE.md はトリガー語と参照だけにし、処理内容の説明を削る | 1 |
| 8 | CLAUDE.md:69,73／x-post-flow.md:1637-1639 | git pull・ルールの読み直し | x-post-flow 側は「CLAUDE.md の作業前ルール」の1行 | 1 |
| 9 | article-flow.md:26-31／constraints.py「事実の扱い」8項目 | 作り話厳禁・AIと対等・一般論と分ける・出典・推測を断定しない | constraints を参照し、相場ガイドの一文だけ残す | 4 |
| 10 | article-flow.md:82,85／constraints.py「文の長さ」 | 句点で切る・連用中止・1文に主題1つ・「AはX。逆に、BはY。」 | 85 の「効く／逆に」の具体例だけ残す | 2 |
| 11 | article-flow.md:109／constraints.py「視覚のリズム」 | 表を地の文で言い直さない・但し書きを3文並べない | 削除 | 1 |
| 12 | article-flow.md:108／constraints.py／article-self-check.py:270-282 | 表に強調を入れる | 「例えば」の表記と列幅の話だけ残して短くする | 0（文を短く） |
| 13 | article-flow.md:14／71-78／89／109 | 「同じ趣旨を重ねない・削る」の言い直しが4か所 | 5章冒頭の🔒（71-78）にまとめる。89 は起きやすい4パターンだけ残す | 4 |
| 14 | article-flow.md:177 後半／217-221 | WP側にユーザーの直しが無いか確かめてから差し替える | 217-221 に一本化 | 1 |
| 15 | article-flow.md:286／task-management.md:122,189-198 | 補充はTOP10が10本を切ったときだけ | article-flow は「待機列の上から入れる。補充は task-management の『補充の手順』」に短くする | 0 |
| 16 | article-flow.md:289／task-management.md:220-222 | GSCインデックス確認 | task-management 側を削除（参照先の章も存在しない。表3の#3） | 3 |
| 17 | task-management.md:175-183／x-post-flow.md:903-913 | 記事とXの連携。同じ9/11の経緯（PERM-01・AUTOTAB-01）が両方にある | task-management の表に一本化。x-post-flow 3.6 は4番（🔒）だけ残す | 7 |
| 18 | task-management.md:39-41／x-post-flow.md:161 | Xネタの宛先は ideas.md（posts-stock の断片ストックは旧置き場） | x-post-flow 2章に1行。もう一方は参照 | 2 |
| 19 | task-management.md:94-100／editorial-strategy.md（同ファイル187行で「種類別の実測はここが正」と明言） | 記事の種類別のGSC実測表 | 表を削除して参照に | 9 |
| 20 | x-post-flow.md:166-175／269-276 | 軸②の採用基準表と実測がほぼ同じ文で2回 | 2章に一本化 | 9 |
| 21 | x-post-flow.md:150-155／278-282／890／941-947／1594-1595／917 | リサーチの供給ラインの説明が6か所 | 3.8 に一本化（時刻は表2の#8） | 15 |
| 22 | x-post-flow.md:65-87／234-239／892／1591-1592 | 日常拾い | 1章に一本化 | 5 |
| 23 | x-post-flow.md:41-57／204-206／1636-1642／1692 | 着手前に読むファイル・事実確認 | 0章を正にする。7章は「0章＋Xの実物照合」 | 8 |
| 24 | x-post-flow.md:34,54,505,850,1343,1615,1646,1655,1694 | x-count.py で重みを測る（9回） | 0章で1回だけ書き、あとは x-gate.py の1番に任せる | 3 |
| 25 | x-post-flow.md:598／806（＋1144） | 「投稿の役割は変わる…軸①を4割残す」が同じ文で2回 | 806 を削除 | 2 |
| 26 | x-post-flow.md:831-853／1688-1697 | 運用ループと「次の投稿内容を教えて」 | 7章に一本化 | 8 |
| 27 | x-post-flow.md:210-216／976-988／990-1006／1214 | ランクの定義が4か所（中身も食い違う。表2の#14） | 4章「3条件チェック」の表1つにする | 10 |
| 28 | x-post-flow.md:1049-1093／1257-1272 | キャラ・トーンと「硬く書かない」。硬い言い方と柔らかい言い方の対照表、使ってよい語の一覧がそれぞれ2つずつある | 1257-1272 を正にして統合 | 15 |
| 29 | x-post-flow.md:1117／1484-1486／1800-1808 | 「Xは記事を要約する場所ではない・読む理由を作る」が3回 | リンク型のルールに1回だけ残し、8章を削除 | 10 |
| 30 | x-post-flow.md:299-309／458-485／1652-1654／lessons.md:189 | 相手の投稿を最後まで読む。同じ3件の失敗表が重複している | ルールは458-473に一本化。失敗表（307-309・475-485）は lessons.md:189 に既にあるので削除 | 14 |
| 31 | x-post-flow.md:1342-1343（合格ラインの3・4）／x-gate.py 1〜3 | x-hook の A/B・重みの余裕5 | 「x-gate.py が［出してよい］」の1行にする | 2 |
| 32 | x-post-flow.md:1599-1601（6章「投稿後」）／1752-1765 | 投稿後の記録 | 6章を削除（表3の#23） | 3 |
| 33 | eyecatch-rules.md:14／165-167／article-flow.md:306 | ICCプロファイルを除去する | 165-167 を削除 | 3 |
| 34 | eyecatch-rules.md:51／118 | 黒猫マスコットの廃止 | 118 を削除 | 1 |
| 35 | eyecatch-rules.md:40／117 | 背景に真っ白を使わない | 117 を削除 | 1 |
| 36 | eyecatch-rules.md:41／119 | 指定した文言以外の日本語を入れない | 119 を削除 | 1 |
| 37 | eyecatch-rules.md:32／88 | 品質は参考画像と同じ水準以上 | 88 を削除 | 1 |
| 38 | eyecatch-rules.md:37／100-101 | ジャンプ率・左端を1本の線にそろえる | 凍結した型（37）に寄せる | 1 |
| 39 | eyecatch-rules.md:90／120 | 吹き出し・丸バッジの詰め込み | 120 を削除 | 1 |
| 40 | eyecatch-rules.md:126-131／141-142／32,36 | 他社バナーから取り入れるもの・変えるもの | 126-131 に統合 | 3 |
| 41 | eyecatch-rules.md:148／156 | 「子記事はこのデザインを踏襲」が2回 | 156 を削除 | 1 |
| 42 | article-flow.md:22／132 | NG 0件まで提示しない | 7章1番は「4原則の4」の参照だけ（すでにほぼそうなっている） | 0 |
| 43 | article-flow.md:81,86／constraints.py「リード」「禁止表現」 | リードは1文目で答える・「〜しましょう」を使わない | 理由の一言だけ残して短くする | 0 |

## 2. 食い違い・カニバリ（33件）

| # | 場所 | 食い違いの中身（新しい方） | 提案 |
|---|---|---|---|
| 1 | article-flow.md:5 と 38・90・111 | 5行目（8/18）で「数値基準をこのファイルに書かない」と決めたのに、35字・60字/160字・1行40字が書いてある | 数値は削除。40字は constraints に無いので**要確認**（constraints へ移すか） |
| 2 | article-flow.md:80 と 81（＋83 と 75） | 「①体験・失敗から入る」と「リードは体験から入らない」。「体験は3割上限」と「役に立つ体験は入れる（9/30）」 | **要確認**。80 は本文の流れ、81 はリードの話と読めるが、80 には日付が無い |
| 3 | article-flow.md:114 と constraints.py の CTA | シリーズ別・検証系は途中CTAを省いてよい（8/20）が、constraints は「途中1回・末尾1回」のみ | **要確認**。例外を constraints 側に書くか |
| 4 | task-management.md:8-9（7/21）と article-flow.md:286（9/11） | 空いた枠を「ストック全体から最も価値の高いもの」で埋めるか、「待機列の上から」入れるか | 9/11 に合わせて task-management:7-11 を2行にする |
| 5 | task-management.md:55／120／122 | 「0番を通らなければ空欄のまま（9/10）」「TOP10は常に10本（9/10）」「10本を切ったら補充（10/20）」 | **要確認** |
| 6 | task-management.md:139（9/14）と 122（10/20） | 在庫の下限に「待機列の◯が5本以上」が残っている／待機列の本数では補充しない | 10/20 に合わせる。pipeline-status.py の表示も**要確認** |
| 7 | task-management.md:35,147,189 と 191・x-morning-brief の SKILL | 「月・金12:00」「月曜12:00」と、毎朝6:30の朝ブリーフ（月・金は full-research.md）（9/18） | 朝ブリーフに合わせる |
| 8 | x-post-flow.md:154,280,943（7:30）／890,1172（毎日8:00・月金12:00）／155（月・金6:30） | SKILL.md の description は「毎朝6:30」 | 6:30 に統一する |
| 9 | x-post-flow.md:252 と 862,868（8/23）・1148-1152（8/31） | 「同じ日に複数投稿しない」と「旬ネタなら1日2回もあり」 | 252 を削除（**要確認**） |
| 10 | x-post-flow.md:257（8/07）／524-531（8/17）／861（8/23）と 3.8・SKILL | 曜日の割り当ては廃止／月水金／ベースは月水金／毎朝・土日祝も | 現行（毎朝の朝ブリーフ＋鮮度優先）に合わせて1か所にする |
| 11 | x-post-flow.md:529（8/17）／547（8/11）／557（8/14）／1140（8/31） | リプライの頻度が「月水金に1件」「毎日1〜2件」「週5件・平日1件」と割れている | 8/31 の「毎日1〜2件」だけ残す |
| 12 | x-post-flow.md:539-545（8/11）／810 と 1607（8/24）・3.8（9/16） | 週1回のまとめ出し（「Xやることある？」）と、月水金のトリガー・毎朝ブリーフ | 539-545 を削除し、810 を直す |
| 13 | x-post-flow.md:403／407／456／529／556 | 対象リストが「下記8件」「32件・目標10件」「残り3件の補充が必要」「8件」「10アカウント（現在3件）」とばらばら | 407（10/28）以外の件数を削除 |
| 14 | x-post-flow.md:212-216／218／815／986 と 1214（9/8）・1303（9/22） | ★★★★☆・★★★☆☆も出してよい、と書いた所と、「HRのみ」「毎日★★★★★を出す」 | 9/22 に合わせる |
| 15 | x-post-flow.md:1008（8/06・①50/②30/③15/④5を維持）／259-267（8/11）／598,806／1174 と 1213（9/8） | 軸比率の目標と、9/8 の凍結 | 凍結に合わせて古い比率を削除 |
| 16 | x-post-flow.md:91／237／247／248／814／893／1708／1737 と 1307（9/22） | 取材する条件が「HR級<3」「HR≤3」「★★★★★<2」「HR≤2」「キュー<5」「キュー<10」とばらばら／「取材が必要」で終えない | **要確認**。閾値を1つにする |
| 17 | x-post-flow.md:218,226,255／1659／1345-1347 と 1303-1308（9/22） | 素材が無ければ無理に出さない・投稿だけの日があってよい／無ければ作る・毎日1本出す | 投稿については9/22に合わせる。リプライの見送り（518）はそのまま |
| 18 | x-post-flow.md:36-37 と 1282（9/30） | 「強い投稿はCCが考えたネタから生まれない」と、CCがHR級の完成品を書く方針 | 36-37 を直す |
| 19 | x-post-flow.md:1366 と x-gate.py 2・3（9/25） | 「x-hook は［要書き直し］だけでNGにしない」が、x-gate では A/B が［NG］ | 1366 を削除 |
| 20 | x-post-flow.md:1351（9/24）と 1353（9/25） | 盲検の合格基準（①〜④）の旧版が残っている | 1351 の基準部分を削除 |
| 21 | x-post-flow.md:1459／1064,1072／1082 の例文／1114 と 1014-1022（10/13） | 語彙表の「うち→自分」、例文「思ってた自分が一番あぶなかったです」は、x-gate の9番でNGになる | 例文と表を直す（**要確認**：「自分を主語に」は書き手を主語にする意味なので、語だけ置き換える） |
| 22 | x-post-flow.md:1265 と 506（9/23） | 「このアカウントの言い方＝かなりわかります」と「かなりわかりますは定型になっていて使い回さない」 | 1265 の例を差し替える（**要確認**） |
| 23 | x-post-flow.md:1158-1168（9/15）と 1178-1190（9/22） | 「公開から何日後に出すかでは伸び方は決まらない」と「公開の翌日〜3日後・4日以上は弱い」 | 9/22 を正にし、9/15 の実測は lessons へ（**要確認**） |
| 24 | article-flow.md:288・x-post-flow.md:889 と 1597-1598（6章） | 記事公開時のXネタ3本を「下書きにしてキューへ」と「ideas.md の記事由来へ」 | 6章を削除 |
| 25 | x-post-flow.md:1568（1週間以内）・1762（1週間後に補う）と 1682,1767（2週間おき）・biweekly-gsc-x-checkup・MEMORY「投稿3日以内で評価しない」 | 振り返りの時期 | 2週間おきにそろえる（**要確認**） |
| 26 | x-post-flow.md:1790-1796 と 1769（8/06） | ユーザーが手でビューを確認する手順と、「CCがChromeで取得・ユーザーの作業は不要」 | **要確認**：手作業の手順を残すか |
| 27 | task-management.md:214-218 と biweekly-gsc-x-checkup | 月初にユーザーへGSCレポートの共有を頼む／2週間おきにCCが取る | 定期タスクに合わせる（**要確認**） |
| 28 | eyecatch-rules.md:16（7/28）と 28（9/28） | 「Downloads は探さない」と「~/Downloads と images/ の最新を見る」 | 9/28 に合わせて16を直す |
| 29 | eyecatch-rules.md:60,91 と 38・98（9/28） | 「記事固有の文言はプロンプトに書かない・GPTのスレッドで共有済みの前提」と、凍結した型の「一字一句書く」「GPTは毎回新しいチャット」 | 60 と 91 の該当部分を削除 |
| 30 | eyecatch-rules.md:87,89 と 33（9/30）・35（10/27） | 「ミニマル・シンプル・余白4割」と「余白は実測値で渡す」「シンプルにしすぎない」 | **要確認**（新しい方に寄せる） |
| 31 | x-post-flow.md:7-16 と CLAUDE.md:7・コミット 5a09ff3 | Xの目的「Claude Code × 実務」と、読者はClaude専門ではないという定義 | **要確認**（方針は運営者が判断） |
| 32 | x-post-flow.md:1750 と ~/.claude/CLAUDE.md・MEMORY「問いかけのスタイル」 | 「投稿文を作りますか？ストックにしますか？」と聞く手順と、推奨を示してから確認するルール | **要確認** |
| 33 | x-post-flow.md:1497-1548（良い投稿の例4本）と 1097-1103・1071・1080・MEMORY「Xにサイトの実数を出さない」 | 例①は手取り435円＝収益の自虐、例②④は教訓・評論家調の締め、例③は記事本数を出している | **要確認**：例を差し替えるか、model-posts.md へ寄せる（約50行減る） |

## 3. 古くなった記述・存在しない参照（33件）

| # | 場所 | 中身 | 提案 | 減る行数 |
|---|---|---|---|---|
| 1 | task-management.md:31 | 「TOP6更新は article-flow『記事公開時の必須作業』」。TOP6は廃止済みで、その章名も無い（実体は8章） | 参照を直す | 0 |
| 2 | task-management.md:27 | 「x-post-flow『タスクリストとの連動』」という章が無い（実体は7章「投稿完了しました」の5番） | 参照を直す | 0 |
| 3 | task-management.md:222 | 「article-flow『記事公開後のGSCインデックス確認』」が無い（8章8番の1行だけ） | 削除（表1の#16） | 0 |
| 4 | x-post-flow.md:814 | 「3.3『キュー在庫の判断基準』」。3.3節は無い（3章241行） | 参照を直す | 0 |
| 5 | task-management.md:7,19,42 | 「TOP5」の表記が残っている | 削除・直す | 1 |
| 6 | CLAUDE.md:71／task-management.md:3／session-handoff.md:29 | 「TOP6は廃止」の注記そのもの | 削除 | 1 |
| 7 | task-management.md:35 | 「marketing-research-mon-fri（月・金12:00）で自動実行」。9/18に統合して削除済み。ただし `~/.claude/scheduled-tasks/marketing-research-mon-fri/SKILL.md` はディスクに残っていて、description に「停止」と書いていない（ai-trends-daily は書いてある） | 文を直す。タスクの実際の状態は**要確認** | 0 |
| 8 | task-management.md:126 | 「marketing-research-mon-fri/SKILL.md『月曜の編集会議準備』」。今は x-morning-brief/full-research.md:61 にある | 参照を直す | 0 |
| 9 | task-management.md:147,189 | 「月曜12:00の定期リサーチ」 | 「月曜の朝ブリーフ（full-research）」に直す | 0 |
| 10 | x-post-flow.md:821,917 | 統合済みの `ai-trends-daily`・`marketing-research-mon-fri` を現役として書いている | 直す | 0 |
| 11 | x-post-flow.md:836,851,1695 | 「GPTレビューは9/25に廃止」の注記が3か所 | 削除 | 2 |
| 12 | x-post-flow.md:810 | 「ユーザーがやるのは『Xやることある？』→…」 | 現行のトリガーに直す | 0 |
| 13 | x-post-flow.md:284-286 | 「4週間後にフォロワー数で判定」。判定は済んでいる（1205で失敗と記録） | 削除 | 3 |
| 14 | x-post-flow.md:870,883 | 「9/8の判定で切り分ける・出す数字」 | 削除 | 2 |
| 15 | x-post-flow.md:1146,1396 | 「9/8の判定で〜を見る」 | 削除 | 2 |
| 16 | x-post-flow.md:1232-1234 | 「4週間後（10/06）に見るもの」。日付が過ぎて、結果の記録が無い | **要確認** | 3 |
| 17 | x-post-flow.md:253 | 「9/30に再評価」。日付が過ぎて、結果が無い | **要確認** | 1 |
| 18 | x-post-flow.md:342-392 | 除外台帳のうち、解除日が10/29以前の39行（@AM09_21〜@yohei_web・@nagataprogram）。残るのは11行。また台帳（50行）と対象リスト（407-452・32行）は毎日書き換える状態データで、7章1683の手順は毎回このルールファイルを書き換えている。published.md:316 にも8/14時点の古い台帳が残っている | 期限切れの行は削除。台帳とリストを knowledge/x/ へ移すかは**要確認** | 39（移す場合はさらに約60） |
| 19 | x-post-flow.md:1024-1047 | 「旧：一人称は自分」の節。10/13に置き換え済み | 1045-1047 の3行だけ新しい節へ移し、残りは削除 | 20 |
| 20 | x-post-flow.md:1459 | 語彙表の「うち→自分」 | 直す | 0 |
| 21 | x-post-flow.md:1552-1562 | 4.5「レビュー方法（ユーザーが投稿案を出したとき）」。盲検と x-gate の流れ、MEMORY「X草案の無断書き換え禁止」と合っていない | **要確認** | 11 |
| 22 | x-post-flow.md:1699-1741 | X編集会議（金曜定例）。朝ブリーフが毎朝在庫と候補を出すようになったあとも開いているか分からない | **要確認** | 43 |
| 23 | x-post-flow.md:1589-1601 | 6章「CCの自動実行」。1章・補充ルール・7章と重なり、中身も古い（表2の#24） | 削除 | 13 |
| 24 | x-post-flow.md:609,613-624 | 9/8の取得ミスの訂正と、ルール4の「当初は1往復」の経緯 | lessons へ | 10 |
| 25 | x-post-flow.md:640 | 「@tk_3118 らは保留・枠が空いたら再検討」。@tk_3118 は9/16に外れている（700） | 削除 | 1 |
| 26 | x-post-flow.md:619-622,747,765 | 9/9〜9/10時点のフォロー数・空き枠 | 削除（表4の#45） | — |
| 27 | CLAUDE.md:96 | 「bash cb.sh は出さない（9/28に廃止）」。リポジトリ直下に cb.sh がまだある | 注記は1行に。cb.sh ファイルを消すかは**要確認** | 0 |
| 28 | CLAUDE.md:132 | 「published.md（全47件）」。published.md 自身が8/06時点で56件と書いている | 件数を削除 | 0 |
| 29 | eyecatch-rules.md:43-47 | 改善候補4件が全部取り消し線（型に採用済み） | 削除 | 5 |
| 30 | eyecatch-rules.md:63-83 | 参考画像なしの試行（9/17に終了） | lessons へ | 21 |
| 31 | eyecatch-rules.md:133-140 | 「以下は9/15時点の記述。上の改訂が優先」の旧文と取り消し線 | 削除 | 8 |
| 32 | eyecatch-rules.md:158-163 | 副業検証シリーズのヘッダー（完結済み・新しく作らない想定） | **要確認** | 6 |
| 33 | session-handoff.md:23 | 「デイリー／フル版」。デイリーは9/17に統合 | 「朝ブリーフ／フル版」に直す | 0 |

## 4. 必要以上に長い所・経緯（68件）

「lessons既存」と書いたものは lessons.md に同じ経緯が既にあるので、ルール側を消すだけで済みます。

| # | 場所 | 中身 | 提案 | 減る行数 |
|---|---|---|---|---|
| 1 | article-flow.md:5 | 8/18に6か所で食い違った経緯（constraints.py の docstring と同じ文） | 括弧内を削除 | 0 |
| 2 | article-flow.md:37 | no.59 の重複未遂の経緯 | lessons へ | 0 |
| 3 | article-flow.md:54 | no.74 の経緯 | 削除（lessons既存:791） | 0 |
| 4 | article-flow.md:75,78 | 9/30の訂正の経緯・no.71 | lessons へ | 1 |
| 5 | article-flow.md:90 | no.62 の経緯 | 削除 | 0 |
| 6 | article-flow.md:93,99-104 | 強調の実測と9/01の経緯 | 削除（lessons既存:281） | 6 |
| 7 | article-flow.md:126 | no.23 の経緯 | 短くする | 0 |
| 8 | article-flow.md:134-137 | リードだけを分けた理由・7工程を素通りした話 | lessons へ | 3 |
| 9 | article-flow.md:148-151,165-167 | 7.5 の理由と61本の手作業の経緯 | 削除（lessons既存:251） | 6 |
| 10 | article-flow.md:191-198 | no.56 のFAQの実例 | lessons へ（:430 と近いので**要確認**） | 4 |
| 11 | article-flow.md:212-215 | RESTの更新が上書きされた経緯 | 削除（lessons既存:289） | 4 |
| 12 | article-flow.md:223-225 | ユーザーのマーカー3か所の経緯 | 削除（lessons既存:699） | 3 |
| 13 | article-flow.md:230-234 | 下書きが止まっていた経緯 | 削除（lessons既存:273） | 5 |
| 14 | article-flow.md:252-256 | no.68 の事故の説明 | 手順の2行だけ残す | 2 |
| 15 | article-flow.md:270-271 | ディスカッションの閉じ忘れの経緯 | 削除（lessons既存:391） | 2 |
| 16 | article-flow.md:275 | nonce の経緯 | 短くする | 0 |
| 17 | article-flow.md:293,300-301,304-305,313-316,334-338 | 本文画像の経緯・実例 | 短くする | 5 |
| 18 | article-flow.md:342 | 太字の実測 | 削除 | 1 |
| 19 | task-management.md:7-8 | TOP10に増やした理由 | 削除 | 1 |
| 20 | task-management.md:40-41 | 宛先を誤った経緯 | 1行にまとめる | 1 |
| 21 | task-management.md:59 | 8/21の経緯 | lessons へ | 2 |
| 22 | task-management.md:90-92 | ④を足した理由 | 削除（lessons既存:536） | 3 |
| 23 | task-management.md:110,115-116 | 9/11・9/12の経緯 | 削除（lessons既存:599・629） | 1 |
| 24 | task-management.md:155-156 | 質問から作った経緯 | 削除（lessons既存:561） | 2 |
| 25 | task-management.md:195 | no.18 の経緯（括弧） | lessons へ | 0 |
| 26 | task-management.md:200 | 0番テストの経緯なのに、別の節の末尾に置かれている | 削除（lessons既存:512） | 2 |
| 27 | task-management.md:204 | 8時間の無駄の経緯 | 短くする | 0 |
| 28 | x-post-flow.md:81-87 | 拾い漏れの実例 | lessons へ | 7 |
| 29 | x-post-flow.md:98-107 | 取材の品質ゲートの実例表と経緯 | ルール2行だけ残す | 6 |
| 30 | x-post-flow.md:222,228 | ペースの訂正の経緯 | 削除 | 3 |
| 31 | x-post-flow.md:251 | 敬老の日の経緯 | lessons へ | 1 |
| 32 | x-post-flow.md:265-267 | 比率を変えた理由（もう凍結済み） | lessons へ | 3 |
| 33 | x-post-flow.md:319-334 | ビューの下限・上限撤廃・大型アカウントを避ける理由 | published.md か lessons へ | 8 |
| 34 | x-post-flow.md:405 | 台帳の経緯 | lessons へ | 1 |
| 35 | x-post-flow.md:503 | @shiba_program の経緯 | lessons へ | 1 |
| 36 | x-post-flow.md:520 | @studiomasakaki の経緯 | lessons へ | 1 |
| 37 | x-post-flow.md:560-578 | ローテーションの理由・1回きりにしない理由（表2の#11と#13で大半が不要になる） | lessons へ | 12 |
| 38 | x-post-flow.md:580-598 | 8/12のリプライ初回実測 | 削除（published.md:347 に訂正記録あり） | 19 |
| 39 | x-post-flow.md:600-769 | フォロー運用。ルール8項目・フォロー返しの例外・判断軸以外は、9/9〜10/27の実数表と解除の記録 | ルールの約25行だけ残し、記録は移す（移し先は**要確認**） | 145 |
| 40 | x-post-flow.md:777-785,802-804 | 返信を放置した経緯・割り込みの実例 | lessons へ | 8 |
| 41 | x-post-flow.md:829 | 整合チェックの経緯 | lessons へ | 1 |
| 42 | x-post-flow.md:872-883 | 本数の上限を外した理由 | lessons へ | 12 |
| 43 | x-post-flow.md:912-913 | 3.6 の経緯 | lessons へ | 2 |
| 44 | x-post-flow.md:933-939 | 3.7 の経緯 | lessons へ | 7 |
| 45 | x-post-flow.md:945,947,957 | 3.8 に統合した経緯と理由 | lessons へ | 4 |
| 46 | x-post-flow.md:1055-1064 | 堅さのデータ表 | lessons へ | 9 |
| 47 | x-post-flow.md:1152-1154 | 5本が期限切れになった経緯 | lessons へ | 2 |
| 48 | x-post-flow.md:1158-1168 | 9/15のリンク型の実測（表2の#23） | lessons へ | 10 |
| 49 | x-post-flow.md:1172-1176 | 例外を作った理由・8月の実測 | lessons へ | 4 |
| 50 | x-post-flow.md:1180-1188 | 日数を明文化した経緯の表 | lessons へ | 8 |
| 51 | x-post-flow.md:1201 | CATS-気 の経緯 | lessons へ | 1 |
| 52 | x-post-flow.md:1240-1255 | 1行目ルールの経緯・87%/41%・3件の事例 | lessons へ | 15 |
| 53 | x-post-flow.md:1297,1326 | AIMARU-01・9/22の経緯 | lessons へ | 2 |
| 54 | x-post-flow.md:1347 | 「在庫との関係」の注記 | lessons へ | 1 |
| 55 | x-post-flow.md:1355 | 盲検の経緯 | lessons へ | 1 |
| 56 | x-post-flow.md:1368-1379 | x-hook の検証表・機械で見る理由・経緯 | lessons へ | 11 |
| 57 | x-post-flow.md:1385-1392 | 構成の実測表 | lessons へ | 7 |
| 58 | x-post-flow.md:1406 | RC-02 の経緯 | lessons へ | 1 |
| 59 | x-post-flow.md:1445,1455-1465 | 語彙チェックの理由表 | lessons へ（コマンドは残す） | 10 |
| 60 | x-post-flow.md:1473 | URLの経緯 | 短くする | 0 |
| 61 | x-post-flow.md:1621-1632 | 3点セットを短くした経緯 | 経緯の1行を削除 | 1 |
| 62 | x-post-flow.md:1663 | ユーザー発言の引用 | 削除 | 1 |
| 63 | eyecatch-rules.md:11,13 | GPTでずれた経緯・no.27 の経緯（括弧） | 短くする | 0 |
| 64 | eyecatch-rules.md:21 | 凍結した理由の引用 | 短くする | 0 |
| 65 | eyecatch-rules.md:33-35 | 型の各行に長い経緯が付いている（35は10文） | 経緯は lessons へ。行数は変わらず、字数が大きく減る | 0 |
| 66 | eyecatch-rules.md:113 | 濃色ベタの経緯 | lessons へ | 2 |
| 67 | eyecatch-rules.md:144 | no.68 の経緯 | lessons へ | 2 |
| 68 | CLAUDE.md:35,96,99 | 報告ルール・cb・pbcopy の経緯 | lessons へ | 2 |

## 5. スクリプトが判定しているのに文章でも細かく書いている所（11件）

表1の#2・#9〜12・#24・#31もこの種類ですが、そちらに書いたのでここでは除いています。

| # | 場所 | スクリプト | 提案 | 減る行数 |
|---|---|---|---|---|
| 1 | article-flow.md:90（4文以上の段落） | article-self-check.py:540-559 | 「self-check の［要確認］を見る」の1文にする | 0 |
| 2 | article-flow.md:54（前の版より増えたらNG） | article-self-check.py:736-748（`ALLOW_GROWTH`） | 1行にする | 0 |
| 3 | article-flow.md:92-93（リンクは自動で太字） | md-to-wp.py:89-101 | 「`**`を付けない」だけ残す | 1 |
| 4 | article-flow.md:313-317（キャプション必須・警告） | md-to-wp.py:257-267 | 書き方の例だけ残す | 2 |
| 5 | article-flow.md:110-111（読点・ブロック内の改行） | constraints.py「読点」「記法」 | 目視で見る部分だけ残す | 0 |
| 6 | x-post-flow.md:1014-1022（「自分」を使わない） | x-gate.py の9 | 3行にする | 3 |
| 7 | x-post-flow.md:1332（見送りは二度と出さない） | x-gate.py の10 | 経緯の括弧を削除 | 0 |
| 8 | x-post-flow.md:1357-1366（ニュース解説型のA/B） | x-hook.py・x-gate.py の2・3 | 3行にする | 6 |
| 9 | x-post-flow.md:1236-1238（1行目） | x-firstline.py | 2行にする | 1 |
| 10 | x-post-flow.md:1353（盲検の合格条件を列挙） | x-review-judge.py・x-blind-review.md | 条件の列挙を削除して参照に | 0（字数減） |
| 11 | x-post-flow.md:515（リプライの合格条件を列挙） | x-reply-review-judge.py | 同上 | 0（字数減） |

## 参考：メモリとの照合（目立つもの4件）

| # | メモリの項目 | 照合結果 |
|---|---|---|
| 1 | 「X投稿の1行目に固有名詞を入れる…87%vs41%・x-firstline.pyで機械判定」 | x-post-flow:1238-1242 の9/18の訂正（製品名は条件ではない・［要目視］だけ）より古い。メモリ側の更新が必要 |
| 2 | 「アイキャッチPNGのWPアップロードエラー対処」 | eyecatch-rules:14・165-167 と同じ内容 |
| 3 | 「補充はTOP10が10本を切ったときだけ」 | task-management:122 と一致。食い違いはルール側（:139）にある |
| 4 | 「3点セットの提示は短く」「土日祝もXは投稿」 | x-post-flow:1621-1632・250-251 と同じ内容 |

---

## ファイルごとの行数の見込み

| ファイル | 今 | 整理後（確実な分） | 要確認分まで実施した場合 |
|---|---|---|---|
| CLAUDE.md | 139 | 約125 | 約120 |
| rules/article-flow.md | 343 | 約285 | 約280 |
| rules/task-management.md | 228 | 約195 | 約190 |
| rules/session-handoff.md | 33 | 約31 | 約31 |
| rules/x-post-flow.md | 1,808 | 約1,280 | 約1,100（台帳・対象リストの移設、金曜編集会議・4.5・良い例の扱い次第） |
| knowledge/eyecatch-rules.md | 167 | 約115 | 約108 |

## 整理の優先順（効果が大きい順）

1. **x-post-flow 3.4 の状態データを外に出す**：フォロー数の記録（−145行）と、除外台帳の期限切れ39行の削除。台帳と対象リストを knowledge/x/ へ移せば、ルールファイルを毎日書き換えなくて済みます。
2. **x-post-flow の食い違いをなくす**（表2の#8〜22）：投稿・リプライの頻度、ランク、取材の条件、軸比率、朝ブリーフの時刻、x-hook の扱いの新旧を1つにします。CCが古い記述を読んで動く危険がいちばん大きい所です。
3. **x-post-flow の重複統合と経緯の移動**：軸②の基準、供給ライン、ランク、トーン、3.5章と7章をまとめ、日付つきの経緯を lessons へ移します（合わせて約300行）。
4. **古い参照の修正**：task-management の存在しない章名3件、`marketing-research-mon-fri`・12:00 の表記、TOP5/TOP6、7:30/8:00 の時刻、x-post-flow の「3.3」。
5. **eyecatch-rules と article-flow の片付け**：終了した試行、取り消し線の旧記述、禁止事項の重複を消し、7.5・7.6章の経緯を削ります（多くは lessons に既にあるので、消すだけで済みます）。

## 要確認のまとめ（運営者の判断が必要なもの）

- 除外台帳と対象リストを knowledge/x/ へ移すか。フォローの記録をどこへ移すか。
- 金曜のX編集会議（1699-1741）と、4.5「投稿案のレビュー」が今も使われているか。
- 10/06と9/30の再評価の結果を、どこかに書くか。
- 取材する条件の閾値をどれに統一するか。
- 良い投稿の例4本を差し替えるか、削るか。
- cb.sh ファイルと、`marketing-research-mon-fri` の SKILL.md が残っていること（ルール文の外の問題です）。

関係するパス：
- /Users/nagaitakashi/Documents/GitHub/aicontent-note/CLAUDE.md
- /Users/nagaitakashi/Documents/GitHub/aicontent-note/rules/article-flow.md
- /Users/nagaitakashi/Documents/GitHub/aicontent-note/rules/task-management.md
- /Users/nagaitakashi/Documents/GitHub/aicontent-note/rules/session-handoff.md
- /Users/nagaitakashi/Documents/GitHub/aicontent-note/rules/x-post-flow.md
- /Users/nagaitakashi/Documents/GitHub/aicontent-note/knowledge/eyecatch-rules.md
- /Users/nagaitakashi/Documents/GitHub/aicontent-note/operations/lessons.md
- /Users/nagaitakashi/.claude/scheduled-tasks/x-morning-brief/SKILL.md
- /Users/nagaitakashi/.claude/scheduled-tasks/marketing-research-mon-fri/SKILL.md