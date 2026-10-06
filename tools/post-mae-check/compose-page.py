#!/usr/bin/env python3
"""投稿まえチェックの固定ページ（説明文＋ツール＋CTA）を、WordPressのコードエディターに貼る1本にまとめる。

  python3 tools/post-mae-check/compose-page.py

やること：
  1. pages/ai-like-text-checker.md を operations/md-to-wp.py で変換する（説明文・表・CTAボタン）
  2. 原稿の「【ツールをここに表示】」の段落を、ツール本体（dist/wp-block.txt）に差し替える
  3. 先頭の「WPの入力欄に写す情報」を、固定ページ用（タイトル・スラッグ・説明文…）に作り直す
  4. 組み立てた結果を検査して（ブロックの対応・CTA文言・ツールが1つだけ・MD記法の残り）、dist/page.wp.txt に書く

先に node build.js で dist/wp-block.txt を作っておく。
貼り方：WPで固定ページを作る →「⋮」→「コードエディター」に dist/page.wp.txt の全文を貼る。
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PAGE_MD = ROOT / "pages" / "ai-like-text-checker.md"
TOOL = ROOT / "tools" / "post-mae-check" / "dist" / "wp-block.txt"
MD_TO_WP = ROOT / "operations" / "md-to-wp.py"
WP_OUT = ROOT / "operations" / "wp-output" / (PAGE_MD.stem + ".wp.txt")
DEST = ROOT / "tools" / "post-mae-check" / "dist" / "page.wp.txt"
DEST_BODY = ROOT / "tools" / "post-mae-check" / "dist" / "page.body.wp.txt"   # 入稿情報を除いた本文だけ（RESTで送る用）
MARKER = "【ツールをここに表示】"
LATEST_ARTICLE = ROOT / "articles" / "chatgpt-claude-division-of-work.md"   # CTAの元（最新の公開記事）。CTAを書き換えるときは最新の公開記事に合わせる


def frontmatter(md):
    fm = {}
    for line in md.split("---", 2)[1].split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def info_block(fm):
    rows = [
        (f"タイトル（{len(fm['title'])}字）", fm["title"]),
        (f"SEOタイトル（{len(fm['seo_title'])}字）", fm["seo_title"]),
        ("スラッグ", fm["slug"]),
        ("URL", fm["url"]),
        (f"説明文・SEO（{len(fm['description'])}字）", fm["description"]),
        ("ページの種類", "固定ページ（記事ではない）"),
        ("アイキャッチ（ファイル）", fm["eyecatch"] + "（1200×630・作成済み。WPのアイキャッチに設定する）"),
        ("アイキャッチのalt", fm["eyecatch_alt"]),
    ]
    lines = ["【WPの入力欄に写す情報】※各欄に写したら、このブロックを削除する", ""]
    for label, value in rows:
        lines += ["■ " + html.escape(label, quote=False), html.escape(value, quote=False), ""]
    return "<!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph -->" % "<br>".join(lines).rstrip("<br>")


def main():
    md = PAGE_MD.read_text(encoding="utf-8")
    fm = frontmatter(md)
    subprocess.run([sys.executable, str(MD_TO_WP), str(PAGE_MD)], check=True, capture_output=True)
    wp = WP_OUT.read_text(encoding="utf-8")
    tool = TOOL.read_text(encoding="utf-8").strip()

    # 先頭の入稿情報（記事用）を固定ページ用に差し替え
    info_re_any = re.compile(r"<!-- wp:paragraph -->\n<p>【WPの入力欄に写す情報】.*?</p>\n<!-- /wp:paragraph -->\n*", re.S)
    info_re = re.compile(r"<!-- wp:paragraph -->\n<p>【WPの入力欄に写す情報】.*?</p>\n<!-- /wp:paragraph -->", re.S)
    assert len(info_re.findall(wp)) == 1, "入稿情報のブロックが1つではない"
    wp = info_re.sub(lambda m: info_block(fm), wp, count=1)

    # ツールの差し込み
    marker_re = re.compile(r"<!-- wp:paragraph -->\n<p>" + re.escape(MARKER) + r"</p>\n<!-- /wp:paragraph -->")
    assert len(marker_re.findall(wp)) == 1, "ツールの差し込み位置が1つではない"
    wp = marker_re.sub(lambda m: tool, wp, count=1)

    # ---- 検査 ----
    assert MARKER not in wp, "差し込みマーカーが残っている"
    assert wp.count("<!-- wp:html -->") == 1 and wp.count("<!-- /wp:html -->") == 1, "ツールのブロックが1つではない"
    assert wp.count("<script>") == 1, "scriptが1つではない"
    opens = re.findall(r"<!-- wp:([a-z/-]+)", wp)
    closes = re.findall(r"<!-- /wp:([a-z/-]+) -->", wp)
    assert sorted(opens) == sorted(closes), "ブロックの開きと閉じが合っていない"
    assert not re.search(r"`|\*\*|==", wp.replace(tool, "")), "MDの記法が変換されずに残っている（ツール本体は除く）"
    # CTAの文言が最新の公開記事と一致していること
    art = LATEST_ARTICLE.read_text(encoding="utf-8")
    m = re.search(r"＼[^\n]*／\n([^\n]*)\n", art)
    cta_line1 = re.search(r"＼[^\n]*／", art).group(0)
    for line in (cta_line1, m.group(1)):
        assert line in md, "CTA文言が最新の公開記事と違う: " + line
        assert html.escape(line, quote=False) in wp, "CTA文言がWPの出力にない: " + line
    assert wp.count("wp:loos/button") == 2, "CTAボタンが1つではない"

    DEST.write_text(wp, encoding="utf-8")

    # 本文だけ（入稿情報の段落を除いたもの）。RESTで送るときに「どこで切るか」を間違えないための出力
    # （2026-09-16 no.68：最初の区切り線で切ってリードが落ちた事故の再発防止）
    body = info_re_any.sub("", wp, count=1).lstrip()
    assert body.startswith("<!-- wp:paragraph -->"), "本文の先頭がリード段落ではない"
    assert body.split("<!-- /wp:paragraph -->", 1)[0].count("swl-marker") == 1, "リードのマーカーが入っていない"
    assert "【WPの入力欄に写す情報】" not in body, "入稿情報が残っている"
    DEST_BODY.write_text(body, encoding="utf-8")
    print(f"書き出し: {DEST.relative_to(ROOT)}（{len(wp) / 1024:.1f} KB）")
    outside = wp.replace(tool, "")      # ツール本体の中の文字列（<h2 など）は数えない
    print(f"  H2 {outside.count('<h2 ')}／表 {outside.count('<!-- /wp:table -->')}／CTAボタン {outside.count('<!-- /wp:loos/button -->')}／ツール 1／区切り線 {outside.count('<!-- wp:separator -->')}")
    print(f"  本文だけ：{DEST_BODY.relative_to(ROOT)}（{len(body) / 1024:.1f} KB）。入稿後に数えて合わせる値：H2 {outside.count('<h2 ')}／表 {outside.count('<!-- /wp:table -->')}／マーカー {body.count('swl-marker')}／CTAボタン {outside.count('<!-- /wp:loos/button -->')}／script 1")
    print("  検査：ブロックの対応・CTA文言（最新の公開記事と一致）・ツールが1つだけ・MD記法の残りなし → OK")


if __name__ == "__main__":
    main()
