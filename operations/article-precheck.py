#!/usr/bin/env python3
"""執筆前チェック（article-precheck.py）

執筆・リライトを始める前に実行し、後から指摘されがちな確認項目を先に潰すためのスクリプト。
2026-08-05のno.40リライトで、執筆後に9回の手戻りが発生した反省から作成。
手戻りの内訳は「執筆前に確認できたはずのもの」が大半だった。

使い方:
    python3 operations/article-precheck.py <slug> ["メインKW"]

例:
    python3 operations/article-precheck.py blog-outsource-pricing-guide "ブログ代行 相場"
"""
import os
import re
import subprocess
import sys
from statistics import median

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def body_len(path):
    """frontmatterを除いた本文の字数（空白除く）"""
    text = open(path, encoding="utf-8").read()
    parts = text.split("---", 2)
    body = parts[2] if len(parts) > 2 else text
    return len(re.sub(r"\s", "", body))


def fm(path, key):
    m = re.search(rf"^{key}:\s*(.*)$", open(path, encoding="utf-8").read(), re.M)
    return m.group(1).strip() if m else ""


def section(title):
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")


def main(slug, kw=""):
    target = os.path.join(ROOT, "articles", f"{slug}.md")
    exists = os.path.exists(target)

    section("① この記事に適した分量（既存記事の実測から）")
    lens = []
    for f in sorted(os.listdir(os.path.join(ROOT, "articles"))):
        if not f.endswith(".md") or "composition" in f:
            continue
        p = os.path.join(ROOT, "articles", f)
        if fm(p, "status") == "published":
            lens.append(body_len(p))
    if lens:
        lens.sort()
        print(f"公開{len(lens)}本：中央値 {int(median(lens))}字／最小 {lens[0]}／最大 {lens[-1]}")
        print(f"直近の水準：{lens[len(lens)//2-2:len(lens)//2+3]}")
    if exists:
        print(f"→ この記事の現在: {body_len(target)}字")
    print("\n【重要】文字数は目標値ではなく冗長検知の指標。")
    print("執筆前にこの記事の適正分量を決め、書いた後に数値で削らない。")
    print("削ってよいのは冗長のみ。正確さ・分かりやすさを損なう削減は禁止。")

    section("② 内部リンク候補（同テーマの公開記事・全件）")
    if kw:
        keys = [k for k in re.split(r"[ 　]", kw) if k]
    else:
        keys = []
    target_cat = fm(target, "category") if exists else ""
    found = []
    for f in sorted(os.listdir(os.path.join(ROOT, "articles"))):
        if not f.endswith(".md") or "composition" in f:
            continue
        p = os.path.join(ROOT, "articles", f)
        if fm(p, "status") != "published" or f == f"{slug}.md":
            continue
        t = fm(p, "title")
        cat = fm(p, "category")
        hit_kw = any(k in t for k in keys) if keys else False
        hit_cat = bool(target_cat) and cat == target_cat
        if hit_kw or hit_cat or not keys:
            mark = "KW" if hit_kw else "同カテゴリ"
            found.append((fm(p, "slug"), t, mark))
    for sl, t, mark in found:
        print(f"  [{mark}] {sl}\n         {t}")
    if not found:
        print("  （キーワード一致なし。キーワードを変えて再実行するか全件を目視で確認）")
    print("\n→ この中にリンクしていない関連記事がないか確認する（2026-08-05にno.40で漏れが発生）")

    section("③ 自社サービス情報の参照先（記憶で書かない）")
    for rel in ["knowledge/service-rules.md", "pages/service.md", "archive/service_model.md"]:
        p = os.path.join(ROOT, rel)
        print(f"  {'✓' if os.path.exists(p) else '×'} {rel}")
    print("\n→ 料金・プラン名・含まれるもの/含まれないものを書くときは3ファイルすべてで照合する")
    print("→ お試しプランは初月限定。『月4本5万円〜』のような下限表記は誤認を招くため使わない")

    section("④ 外部出典の確認（記事に統計・相場を書く場合）")
    if exists:
        urls = re.findall(r"\((https?://[^)]+)\)", open(target, encoding="utf-8").read())
        ext = sorted({u for u in urls if "aicontent-note.com" not in u})
        if ext:
            for u in ext:
                print(f"  {u}")
            print("\n→ WebFetchの要約だけで書かない。ブラウザで原文を開いて確認する")
            print("   （2026-08-05：要約が『専門知識不要』等の条件と『1円を下回ることもある』という")
            print("    但し書きを落とし、相場が実態より高く見える記事になった）")
            print("→ 数値だけでなく【条件・但し書き】も本文に反映する")
            print("→ 『公開日』か『更新日』かを区別して明記する")
            print("→ プラットフォームの『相場ガイド』は発注者向けの目安。成約実績ではない。")
            print("   実勢を書くなら実際の募集案件も確認し、両者を区別して書く（2026-08-05）")
        else:
            print("  外部リンクなし")
    print("→ URLは記憶で書かない。WebSearch/WebFetchで実在を確認してから使う")

    section("⑤ 執筆中に守る制約（機械チェックの対象）")
    print("  一文60字以内 ／ 段落160字以内（2026-08-12に70→60字）")
    print("  リード（H1直下）3文・150字以内、1文目40字以内で検索意図に直接答える")
    print("  H2直下リード 3文・100字以内（表・箇条書きの後の地の文も段落チェックの対象）")
    print("  関連記事3本 ／ CTA2回（間に3セクション以上）")
    print("  `・`項目内の列挙は `A / B`（`・`を重ねない）")
    print("  ※長い文は『削る』のではなく『分ける』で直す（原則2）")
    print("  ※文字数に上限はない。適正な分量は記事とKWによって決まる（原則2）")
    print("  ※表の個数は上限撤廃（INFO表示のみ）。比較・多列情報以外を表にしないことだけ守る")

    section("⑥ 提示前の宣言基準（省略禁止）")
    print("  1. article-self-check.py が【NG 0件】になるまで直す")
    print("     - 記事側の問題 → 記事を直す")
    print("     - 誤検知 → スクリプトを直す（『無視する』で済ませない）")
    print("  2. 出力は grep/head で絞らず最後まで読む（文字数チェックは末尾）")
    print("  3. 全文を読者視点で通し読みする（削った後は特に）")
    print("     - 1箇所直したら影響範囲も直す：同種の誤り／矛盾／二重説明の3点を確認")
    print("     - 入稿済み記事はgit diffで差し替え範囲を特定して伝える")
    print("  4. NG 0件＋通し読み完了後にのみ『入稿できます』と言う")
    print("\n  修正が必要な場合は、問題を全部洗い出してから一度に直す。")
    print("  1件ずつ直して都度提示しない（手戻りが増えるため）。")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")
