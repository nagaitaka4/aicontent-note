"""記事MD → WordPress（SWELL）ブロック形式への変換（2026-08-26新設）。

    python3 operations/md-to-wp.py articles/<slug>.md

出力は `operations/wp-output/<slug>.wp.txt`。
WPの記事編集画面 → 右上「⋮」→「コードエディター」に**全文を貼り付ける**。
（ビジュアルエディタに貼るとブロックとして認識されない）

## なぜ作ったか

これまでMDからWPへの変換は手作業だった。【ポイント】などのブロックを1つずつ
WP上で作り直しており、区切り線（wp:separator）がno.59・no.60で抜けたまま
公開直前まで進む事故が2026-08-20に起きている。

変換規則は推測ではなく、**入稿済み記事61本のWP側マークアップをREST APIで実測して**決めた
（2026-08-26・記事ID842の編集画面から `wp.apiFetch` で取得）。実測値は各所のコメントに残す。

## 変換しないもの（入稿後に人が付ける装飾）

- リード1文目のマーカー（`swl-marker mark_yellow`）
- 段落単位の装飾（`is-style-stitch` / `is-style-crease` / `is-style-kakko_box` 等）
- 画像・キャプションボックス

これらはMD側に記法がなく、記事ごとに人が判断して付けている。
"""

import os
import re
import sys
import json
import unicodedata
import urllib.request

SITE = "https://aicontent-note.com"
OUT_DIR = os.path.join(os.path.dirname(__file__), "wp-output")

# MDの【ブロック名】→ SWELLのスタイルクラス。
# 9種は入稿済み記事で実測して確定（2026-08-26）。バッド/ペン/本は記事での使用実績がなく、
# SWELLのCSSに存在するクラス名から対応させた（使う前に1度、WP上で表示を確認する）。
BLOCKS = {
    "ポイント": "is-style-big_icon_point",
    "チェック": "is-style-big_icon_check",
    "バツ印": "is-style-big_icon_batsu",
    "アラート": "is-style-big_icon_caution",
    "はてな": "is-style-big_icon_hatena",
    "メモ": "is-style-big_icon_memo",
    "グッド": "is-style-icon_good",
    "インフォ": "is-style-icon_info",
    "アナウンス": "is-style-icon_announce",
    "バッド": "is-style-icon_bad",       # 未実測
    "ペン": "is-style-icon_pen",         # 未実測
    "本": "is-style-icon_book",          # 未実測
}

# ブロック内を <strong> で囲むか。実測61本では記事ごとにばらついていた
# （point: 素10/太字3、info: 太字8/素1、check: 太字2/素0、memo: 素4/太字0、caution: 素4/太字1）。
# 手作業だったためで、意図的な使い分けではない。**素**に統一する。
BLOCK_STRONG = False

# 地の文の `・` 箇条書きに付ける装飾。実測118件のうち93件（79%）がbg_grid系で、
# 最多は `has-border -border03 is-style-bg_grid`（65件・55%）。これを既定にする。
LIST_CLASS = "has-border -border03 is-style-bg_grid"

SEPARATOR = (
    "<!-- wp:separator -->\n"
    '<hr class="wp-block-separator has-alpha-channel-opacity"/>\n'
    "<!-- /wp:separator -->"
)

CTA_BUTTON = (
    '<!-- wp:loos/button {"hrefUrl":"%s/contact/","isCount":true,'
    '"color":"green","className":"is-style-btn_normal"} -->\n'
    '<div class="swell-block-button green_ is-style-btn_normal" data-id="e8d05f37">'
    '<a href="%s/contact/" class="swell-block-button__link">'
    "<span>お問い合わせフォームはこちら</span></a></div>\n"
    "<!-- /wp:loos/button -->" % (SITE, SITE)
)


def inline(text):
    """MDのインライン記法をHTMLに変換する。"""
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text.strip()


def split_sentences(text):
    """句点で分ける。閉じ括弧・引用符が続く場合はそこまでを1文に含める。"""
    parts = re.split(r"(?<=。)(?![」』）\)])", text)
    return [p for p in (s.strip() for s in parts) if p]


def paragraph(text, class_name=None, align_center=False, strong=False):
    """wp:paragraph を組み立てる。2文以上なら句点で <br> を入れる。

    実測：2文以上の段落135件のうち128件（95%）に <br> が入っていた。
    1つの段落のまま行だけ分ける形（空行で分けると余白が空く）。
    """
    sents = split_sentences(text)
    body = "<br>".join(sents) if len(sents) >= 2 else text
    if strong:
        body = "<strong>%s</strong>" % body
    attrs, cls = "", []
    if class_name:
        cls.append(class_name)
    if align_center:
        attrs = ' {"style":{"typography":{"textAlign":"center"}}}'
        cls.append("has-text-align-center")
    elif class_name:
        attrs = ' {"className":"%s"}' % class_name
    cls_attr = ' class="%s"' % " ".join(cls) if cls else ""
    return "<!-- wp:paragraph%s -->\n<p%s>%s</p>\n<!-- /wp:paragraph -->" % (
        attrs,
        cls_attr,
        body,
    )


def heading(text, level=2):
    tag = "h%d" % level
    attrs = "" if level == 2 else ' {"level":%d}' % level
    return '<!-- wp:heading%s -->\n<%s class="wp-block-heading">%s</%s>\n<!-- /wp:heading -->' % (
        attrs,
        tag,
        inline(text),
        tag,
    )


def table(rows):
    """1行目をthead、区切り行(|---|)を捨て、残りをtbodyにする。"""
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [c for c in cells if not all(re.fullmatch(r":?-{2,}:?", x) for x in c)]
    head, body = cells[0], cells[1:]
    th = "".join("<th>%s</th>" % inline(c) for c in head)
    tb = "".join(
        "<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in row) for row in body
    )
    return (
        "<!-- wp:table -->\n"
        '<figure class="wp-block-table"><table class="has-fixed-layout">'
        "<thead><tr>%s</tr></thead><tbody>%s</tbody></table></figure>\n"
        "<!-- /wp:table -->" % (th, tb)
    )


def post_id(slug):
    """公開APIでslugから記事IDを引く（関連記事ブロックに必要）。"""
    url = "%s/wp-json/wp/v2/posts?slug=%s&_fields=id" % (SITE, slug)
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.load(r)
        return data[0]["id"] if data else None
    except Exception:
        return None


def post_link(title, url):
    slug = url.rstrip("/").rsplit("/", 1)[-1]
    pid = post_id(slug)
    if pid is None:
        print("  ⚠️ 記事IDを取得できなかった: %s（WP側で貼り直しが要る）" % slug, file=sys.stderr)
        pid = 0
    link = {"title": title, "id": pid, "url": url, "kind": "post-type", "type": "post"}
    return '<!-- wp:loos/post-link {"linkData":%s,"icon":"link"} /-->' % json.dumps(
        link, ensure_ascii=False, separators=(",", ":")
    )


COPY_MARK = "=" * 26 + " ここから下を全文コピー " + "=" * 26


def frontmatter(md):
    """MDのfrontmatterを辞書で返す（値にコロンが含まれても壊れないよう1回だけ分割する）。"""
    if not md.startswith("---"):
        return {}
    raw = md.split("---", 2)[1]
    fm = {}
    for line in raw.split("\n"):
        if ":" in line and not line.strip().startswith("#"):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def info_header(fm):
    """WPの入力欄に写す情報。**この部分はWPに貼らない**（区切り線から下だけを貼る）。"""
    title = fm.get("title", "")
    desc = fm.get("description", "")
    rows = [
        ("タイトル", "%s（%d字）" % (title, len(title))),
        ("スラッグ", fm.get("slug", "")),
        ("URL", fm.get("url", "")),
        ("説明文（SEO）", "%s（%d字）" % (desc, len(desc))),
        ("カテゴリー", fm.get("category", "")),
        ("タグ", fm.get("tags", "")),
        ("アイキャッチ", fm.get("eyecatch", "")),
        ("アイキャッチalt", fm.get("eyecatch_alt", "")),
        ("記事no.", "%s（%s %s）" % (fm.get("no", ""), fm.get("series", "-"), fm.get("series_no", ""))),
    ]
    # 全角・半角が混ざるので、表示幅（East Asian Width）でそろえる
    def width(t):
        return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in t)

    w = max(width(k) for k, _ in rows)
    lines = ["【WPの入力欄に写す情報】※ここはWPの本文に貼らない", ""]
    lines += ["  %s%s : %s" % (k, " " * (w - width(k)), v) for k, v in rows]
    lines += ["", COPY_MARK, ""]
    return "\n".join(lines)


def convert(md):
    body = md.split("---", 2)[2] if md.startswith("---") else md
    chunks = re.split(r"\n\s*\n", body)
    out, i, has_tail_separator = [], 0, [False]
    while i < len(chunks):
        c = chunks[i].strip()
        i += 1
        if not c or c == "---":
            continue

        # H1はWPのタイトル欄に入るため本文には出さない
        if c.startswith("# "):
            continue

        if c.startswith("## "):
            out.append(SEPARATOR)
            out.append(heading(c[3:], 2))
            continue
        if c.startswith("### "):
            out.append(heading(c[4:], 3))
            continue

        # 表
        if c.startswith("|"):
            out.append(table(c.split("\n")))
            continue

        # 【ブロック名】<br> ＋ 内容
        m = re.match(r"^【([^】]+)】(<br>)?\s*\n?([\s\S]*)$", c)
        if m and m.group(1) in BLOCKS:
            inner = "<br>".join(
                inline(l) for l in m.group(3).split("<br>") if l.strip()
            )
            out.append(
                "<!-- wp:paragraph {\"className\":\"%s\"} -->\n<p class=\"%s\">%s</p>\n<!-- /wp:paragraph -->"
                % (
                    BLOCKS[m.group(1)],
                    BLOCKS[m.group(1)],
                    "<strong>%s</strong>" % inner if BLOCK_STRONG else inner,
                )
            )
            continue

        # CTA（＼〜／ の2行 → 中央寄せ段落 → ボタン）
        if c.startswith("＼"):
            out.append(SEPARATOR)
            lines = [inline(l) for l in c.split("\n") if l.strip()]
            out.append(
                '<!-- wp:paragraph {"style":{"typography":{"textAlign":"center"}}} -->\n'
                '<p class="has-text-align-center"><strong>%s</strong></p>\n'
                "<!-- /wp:paragraph -->" % " <br>".join(lines)
            )
            if i < len(chunks) and "お問い合わせフォームはこちら" in chunks[i]:
                i += 1
            out.append(CTA_BUTTON)
            continue

        # 関連記事（**関連記事** ＋ ・リンク3本 → loos/post-link）
        # no.61の実測では、この直前のseparatorが「記事末尾の1本」に当たる（合計7本）。
        # post-linkの後ろには入れない。
        if c.startswith("**関連記事**"):
            has_tail_separator[0] = True
            out.append(SEPARATOR)
            for l in c.split("\n")[1:]:
                m = re.match(r"^・\[([^\]]+)\]\(([^)]+)\)", l.strip())
                if m:
                    out.append(post_link(m.group(1), m.group(2)))
            continue

        # 地の文の ・箇条書き
        if c.startswith("・"):
            items = "<br>".join(
                inline(l) for l in c.replace("<br>", "\n").split("\n") if l.strip()
            )
            out.append(
                '<!-- wp:paragraph {"className":"%s"} -->\n<p class="%s"><strong>%s</strong></p>\n<!-- /wp:paragraph -->'
                % (LIST_CLASS, LIST_CLASS, items)
            )
            continue

        out.append(paragraph(inline(c.replace("\n", ""))))

    if not has_tail_separator[0]:
        out.append(SEPARATOR)  # 関連記事がない記事だけ、末尾に1本入れる
    return "\n\n".join(out) + "\n"


def main(path):
    with open(path, encoding="utf-8") as f:
        md = f.read()
    slug = os.path.splitext(os.path.basename(path))[0]
    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, slug + ".wp.txt")
    wp = convert(md)
    fm = frontmatter(md)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(info_header(fm) + wp)
    n = {k: wp.count('{"className":"%s"}' % v) for k, v in BLOCKS.items()
         if '{"className":"%s"}' % v in wp}
    print("出力: %s" % dest)
    print(
        "  H2 %d／H3 %d／表 %d／区切り線 %d／ブロック %s"
        % (
            wp.count("<h2 "),
            wp.count("<h3 "),
            wp.count("wp:table -->") // 2,
            wp.count("<!-- wp:separator -->"),
            n or "なし",
        )
    )
    print("\n冒頭に入稿情報（タイトル・説明文・カテゴリー・タグ・アイキャッチ）を付けた。")
    print("『ここから下を全文コピー』の線より下だけを、WPの「コードエディター」に貼り付ける。")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python3 operations/md-to-wp.py articles/<slug>.md")
        sys.exit(1)
    main(sys.argv[1])
