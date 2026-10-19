#!/usr/bin/env python3
"""アイキャッチの参考集め：質の高いメディアの記事のアイキャッチ（og:image）を集めて一覧にする。

使い方:
  python3 operations/eyecatch-sampler.py            # MEDIA の全メディアから各8枚
  python3 operations/eyecatch-sampler.py -n 12      # 1メディアあたりの枚数
  python3 operations/eyecatch-sampler.py --only smarthr lig

出力（リポジトリは公開なので、画像はコミットしない＝.gitignore 済み）:
  eyecatch-samples/<日付>/<メディア>/NN.<拡張子>   … GPTに添付する元画像
  eyecatch-samples/<日付>/index.html               … 一覧（ブラウザで開く。画像を押すと元記事）
  eyecatch-samples/<日付>/sheet.jpg                 … 一覧の1枚画像（アプリ内で見る用）

集めた画像は参考に見るためだけに使う（まるっきり同じにしない・knowledge/eyecatch-rules.md）。
"""
import argparse
import datetime
import html
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

# 名前, 表示名, RSS。アイキャッチが写真ではなく、絵と題で作られているメディアを選んでいる（2026-10-19・16メディアから見た目で10に絞った）
# 外したもの（写真が中心で、このメディアの絵＋題のアイキャッチの参考にならない）：PR TIMES MAGAZINE・ラクスルマガジン・KAGOYA・DX Insight・
#   Salesforceブログ・AIsmiley・SEOラボ（サングローブ）・TDI 味噌・ミエルカマガジン（動画のサムネイル型）。バズ部はRSSがSSLで読めない
MEDIA = [
    ("smarthr", "SmartHR Mag.", "https://mag.smarthr.jp/feed.xml"),
    ("lig", "LIGブログ", "https://liginc.co.jp/feed"),
    ("backlog", "Backlogブログ", "https://backlog.com/ja/blog/feed/"),
    ("hubspot", "HubSpotブログ", "https://blog.hubspot.jp/rss.xml"),
    ("notemag", "note公式", "https://note.com/notemag/rss"),
    ("workship", "Workship MAGAZINE", "https://goworkship.com/magazine/feed/"),
    ("liskul", "LISKUL", "https://liskul.com/feed"),
    ("keywordmap", "Keywordmap ACADEMY", "https://keywordmap.jp/academy/feed/"),
    ("seohacks", "SEO HACKS", "https://www.seohacks.net/blog/feed/"),
    ("kaonavi", "カオナビ 人事用語集", "https://www.kaonavi.jp/dictionary/feed/"),
]

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "eyecatch-samples")


def get(url, timeout=15):
    url = urllib.parse.quote(url, safe=":/?&=%#+,;@~")  # 日本語入りのURL
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "")


def feed_items(feed_url, n):
    """RSS/Atom から (題, 記事URL) を新しい順に n 件"""
    data, _ = get(feed_url)
    root = ET.fromstring(data)
    items = []
    for it in root.iter():
        tag = it.tag.split("}")[-1]
        if tag not in ("item", "entry"):
            continue
        title, link = "", ""
        for c in it:
            ct = c.tag.split("}")[-1]
            if ct == "title":
                title = (c.text or "").strip()
            elif ct == "link":
                link = (c.text or "").strip() or c.attrib.get("href", "")
        if link:
            items.append((title, link))
        if len(items) >= n:
            break
    return items


def og_image(page_url):
    data, _ = get(page_url)
    text = data.decode("utf-8", "ignore")
    for pat in (r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']'):
        m = re.search(pat, text, re.I)
        if m:
            return urllib.parse.urljoin(page_url, html.unescape(m.group(1)))  # 相対パスのog:image
    return None


def collect(media, n, outdir):
    key, label, feed = media
    rows = []
    try:
        items = feed_items(feed, n)
    except Exception as e:
        print(f"[{label}] RSSが読めない: {e}", file=sys.stderr)
        return key, label, rows
    os.makedirs(os.path.join(outdir, key), exist_ok=True)
    for i, (title, link) in enumerate(items, 1):
        try:
            img = og_image(link)
            if not img:
                continue
            data, ctype = get(img)
            ext = "png" if "png" in ctype else "webp" if "webp" in ctype else "jpg"
            path = os.path.join(key, f"{i:02d}.{ext}")
            with open(os.path.join(outdir, path), "wb") as f:
                f.write(data)
            rows.append((title, link, path))
        except Exception as e:
            print(f"[{label}] {link}: {e}", file=sys.stderr)
    print(f"[{label}] {len(rows)}枚")
    return key, label, rows


def write_html(results, outdir, day):
    parts = [f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>アイキャッチ参考 {day}</title>
<style>body{{font-family:sans-serif;margin:16px;background:#f4f2ee;color:#222}}h2{{margin:28px 0 8px;font-size:18px}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}}
a{{color:inherit;text-decoration:none}}figure{{margin:0;background:#fff;border-radius:8px;overflow:hidden}}
img{{width:100%;aspect-ratio:1200/630;object-fit:cover;display:block}}figcaption{{font-size:12px;padding:6px 8px;line-height:1.4}}
code{{font-size:11px;color:#777}}</style>
<h1>アイキャッチ参考（{day}）</h1><p>画像を押すと元の記事。GPTに添付するときは <code>eyecatch-samples/{day}/&lt;メディア&gt;/</code> の画像を使う。</p>"""]
    for key, label, rows in results:
        if not rows:
            continue
        parts.append(f"<h2>{html.escape(label)}</h2><div class=g>")
        for title, link, path in rows:
            parts.append(f'<a href="{html.escape(link)}" target="_blank"><figure><img src="{html.escape(path)}" loading="lazy">'
                         f'<figcaption>{html.escape(title)}<br><code>{html.escape(path)}</code></figcaption></figure></a>')
        parts.append("</div>")
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(parts))


def write_sheet(results, outdir, cols=8, w=260):
    """一覧を1枚の画像に（メディアごとに1段・左端にメディア名）"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None
    h = int(w * 630 / 1200)
    rows = [(label, r) for _, label, r in results if r]
    label_w, pad = 170, 6
    sheet = Image.new("RGB", (label_w + cols * (w + pad) + pad, len(rows) * (h + pad) + pad), (244, 242, 238))
    draw = ImageDraw.Draw(sheet)
    font = None
    for fp in ("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", "/System/Library/Fonts/Hiragino Sans GB.ttc"):
        if os.path.exists(fp):
            font = ImageFont.truetype(fp, 18)
            break
    for y, (label, items) in enumerate(rows):
        top = pad + y * (h + pad)
        draw.text((10, top + h // 2 - 10), label, fill=(30, 30, 30), font=font)
        for x, (_, _, path) in enumerate(items[:cols]):
            try:
                im = Image.open(os.path.join(outdir, path)).convert("RGBA").convert("RGB")
                im = im.resize((w, h))
                sheet.paste(im, (label_w + pad + x * (w + pad), top))
            except Exception:
                pass
    out = os.path.join(outdir, "sheet.jpg")
    sheet.save(out, quality=85)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=8, help="1メディアあたりの枚数")
    ap.add_argument("--only", nargs="*", help="メディアの名前（MEDIAの1列目）で絞る")
    a = ap.parse_args()
    media = [m for m in MEDIA if not a.only or m[0] in a.only]
    day = datetime.date.today().isoformat()
    outdir = os.path.join(ROOT, day)
    os.makedirs(outdir, exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(lambda m: collect(m, a.n, outdir), media))
    write_html(results, outdir, day)
    sheet = write_sheet(results, outdir)
    print(f"一覧: {os.path.join(outdir, 'index.html')}")
    if sheet:
        print(f"1枚画像: {sheet}")


if __name__ == "__main__":
    main()
