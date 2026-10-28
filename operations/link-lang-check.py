#!/usr/bin/env python3
"""記事の外部リンク先が日本語のページかを調べる（link-lang-check.py・2026-10-28新設）

`article-self-check.py` の英語リンク検査はURLの形（`/en/`・`hl=en`）しか見ない。
`anthropic.com/legal/consumer-terms` や `academy.claude.com` のように、URLに言語が入っていない
英語のページは素通りする。読者は英語を読めない（no.77・ユーザー指摘「英語のページで読むことが不可能」）ので、
リンク先を実際に開き、ページの言語（`<html lang>`）を読んで日本語以外を一覧にする。

self-checkはネットに出ない作りなので、別のスクリプトにした。

使い方:
    python3 operations/link-lang-check.py articles/<slug>.md      # 1本
    python3 operations/link-lang-check.py --published              # 公開済みの全記事

判定:
    ja      … 日本語のページ
    非ja    … 日本語以外（en など）。日本語版を探して差し替えるか、無ければ理由を残す
    要確認  … 開けなかった（403・Cloudflareの確認画面・JSでしか言語が出ないなど）。実Chromeで見る
    許可済み … operations/en-link-allow.tsv に理由つきで載っている（日本語版が無く、本文で中身を説明している）
"""
import concurrent.futures
import glob
import html
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
SKIP_HOSTS = ("aicontent-note.com",)


def links(path):
    body = open(path, encoding="utf-8").read().split("---", 2)[-1]
    urls = re.findall(r"\]\((https?://[^)\s]+)\)", body)
    return [u for u in dict.fromkeys(urls) if not any(h in u for h in SKIP_HOSTS)]


# URLに日本語版の印があるページは、開けなくても（403・JSでしか中身が出ない）日本語版として扱う。
# 例：help.openai.com/ja-jp/・openai.com/ja-JP/・helpx.adobe.com/jp/・branddb.wipo.int/ja/（lang属性はenだが画面は日本語）
JA_IN_URL = re.compile(r"/(ja|ja-jp|ja_jp|jp)(/|$)|[?&](hl|lang)=ja\b", re.I)

# 日本語版が無いと確かめ、本文で中身を日本語で説明しているリンク（理由つき）。ここにあるURLは「許可済み」に数える
ALLOW_TSV = os.path.join(ROOT, "operations", "en-link-allow.tsv")
ALLOWED = {l.split("\t")[0]: l.rstrip("\n").split("\t")[-1] for l in open(ALLOW_TSV, encoding="utf-8")
           if l.strip() and not l.startswith("#")} if os.path.exists(ALLOW_TSV) else {}


class _Follow308(urllib.request.HTTPRedirectHandler):
    """urllib は 308 を追わない（claude.com/blog が 308 で返す）"""
    def http_error_308(self, req, fp, code, msg, headers):
        return self.http_error_302(req, fp, 302, msg, headers)


OPENER = urllib.request.build_opener(_Follow308)


def lang_of(url):
    """(判定, 理由, 最終URL) を返す"""
    if url in ALLOWED:
        return "許可済み", "en-link-allow.tsv", url
    if JA_IN_URL.search(url):
        return "ja", "URLにja", url
    # アプリの設定画面（claude.ai/settings など）は、使う人の言語で表示される。読み物のページではないので対象外
    if re.match(r"https?://claude\.ai/settings", url):
        return "ja", "アプリの画面", url
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ja,en;q=0.5"})
    host = re.sub(r"^https?://([^/]+).*", r"\1", url)
    try:
        with OPENER.open(req, timeout=20) as r:
            final = r.geturl()
            ctype = r.headers.get("Content-Type", "")
            head = r.read(200000).decode("utf-8", "ignore")
    except Exception as e:
        # 日本のドメインは、開けなくても日本語のページとみなす（lancers.jpの503など）
        if host.endswith(".jp"):
            return "ja", "日本のドメイン", url
        return "要確認", str(getattr(e, "code", e))[:40], url
    if JA_IN_URL.search(final):
        return "ja", "転送先にja", final
    if "pdf" in ctype or final.lower().endswith(".pdf") or host.endswith(".jp"):
        if host.endswith(".jp"):
            return "ja", "日本のドメイン", final
        return "要確認", "PDF", final
    if re.search(r"Just a moment|cf-browser-verification|challenge-platform", head):
        return "要確認", "確認画面", final
    m = re.search(r"<html[^>]*\blang=[\"']?([A-Za-z-]+)", head, re.I)
    lang = m.group(1) if m else ""
    if not lang:
        return "要確認", "lang無し", final
    return ("ja" if lang.lower().startswith("ja") else "非ja"), lang, final


def main(args):
    if args == ["--published"]:
        paths = sorted(
            p for p in glob.glob(os.path.join(ROOT, "articles", "*.md"))
            if re.search(r"^status:\s*published", open(p, encoding="utf-8").read(), re.M)
        )
    elif args:
        paths = args
    else:
        print(__doc__)
        sys.exit(1)

    per = {p: links(p) for p in paths}
    uniq = sorted({u for us in per.values() for u in us})
    with concurrent.futures.ThreadPoolExecutor(12) as ex:
        res = dict(zip(uniq, ex.map(lang_of, uniq)))

    total = {"ja": 0, "非ja": 0, "要確認": 0, "許可済み": 0}
    for p, us in per.items():
        bad = [(u, res[u]) for u in us if res[u][0] not in ("ja", "許可済み")]
        for u in us:
            total[res[u][0]] += 1
        if bad:
            print("== %s" % os.path.relpath(p, ROOT))
            for u, (kind, lang, final) in bad:
                print("  [%s] %s  (%s)" % (kind, html.unescape(u), lang))
    print("\n外部リンク %d本（重複を除くURL %d種類）：ja %d／非ja %d／要確認 %d／許可済み %d" % (
        sum(len(v) for v in per.values()), len(uniq), total["ja"], total["非ja"], total["要確認"], total["許可済み"]))


if __name__ == "__main__":
    main(sys.argv[1:])
