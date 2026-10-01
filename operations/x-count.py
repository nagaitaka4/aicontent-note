#!/usr/bin/env python3
"""X投稿の文字数チェック（x-count.py）

Xの上限は「280の重み付き文字数」。数え方は、X公式ライブラリ twitter-text 3.1.0（設定v3）と同じ。
（2026-10-01に公式準拠へ修正。それまでは自前の近似で、公式と食い違っていた。経緯は下）

  重み     日本語・全角は2、半角英数・改行は1。重み1の文字は4つの範囲だけ
           （0–4351・8192–8205・8208–8223・8242–8247）。それ以外は2
           → … ※ ① ★ ♪ ✅ なども2（旧版は1と数えていた）
  URL      長さに関係なく一律23。https:// 付きだけでなく、example.com や README.md、
           main.py のようなスキームなしも URL（公式の全TLD一覧で判定）
  絵文字   1つ（ZWJつなぎ・肌色・国旗・キーキャップ含む）で2
  正規化   数える前にNFC正規化

「140文字」は日本語だけで書いた場合の目安にすぎず、"Claude Code" のような
半角英字を含む投稿では140文字を超えても投稿できる。目視・概算をやめ、必ずこのスクリプトで判定する。

⚠️ 分からないこと（確認できていない）
  - 公式の絵文字表は古い（Emoji 11＝2018年まで）。新しい絵文字（❤️‍🔥 など）は部品ごとに数えられ、2を超える
    （出力に「絵文字注意」と出る）。実際のXが2で数えるかは確認できていない。公式どおり数えるので重めの見積もり
  - README.md・CLAUDE.md・main.py・Node.js のようなファイル名風の文字列も、公式ライブラリは URL（23）と数える
    （.md・.py・.js などがドメインの末尾として登録されているため）。実際のXの現在の挙動は未確認。URLでなければ実際はもっと小さい（＝安全側）
  - 日本語を含むURL（https://example.com/日本語）は、公式ライブラリでは日本語の手前でURLが終わると数える。
    実際のXが全体を23で数えるかは確認できていない（そうなら、ここは実際より大きく出る＝安全側）

経緯
  2026-08-14  CCが「140字」を上限として下書きを削っていたが、ユーザーが投稿した144文字の版は重み266で通った
  2026-09-02  google.com/goto のような裸のドメインを数え落としていた（実際は284で4超過）
  2026-10-01  公式ライブラリと突き合わせたところ、重みの範囲・絵文字・URLの見つけ方・NFC正規化が食い違っていた
              （矢印・三点リーダ・✅を1と数える／絵文字を部品で足す／URL直後の「。」まで吸う／.md・.py・.tokyo など）。
              公式の正規表現（x-count-data.json）を読み込む作りに直した。
              食い違いの全件一覧：tools/post-mae-check/x-count-diff.md
              テスト：tools/post-mae-check/tests/xcount.py（公式ライブラリと乱数・全絵文字・全コードポイントで突き合わせ）

正規表現のデータ x-count-data.json は自動生成（tools/post-mae-check/tests/gen-vendor.js）。手で直さない。
（公式の twitter-text は Apache License 2.0、twemoji-parser は MIT License。全文：tools/post-mae-check/THIRD-PARTY-NOTICES.md）

使い方:
    python3 operations/x-count.py "投稿本文"
    python3 operations/x-count.py < draft.txt
    echo "本文" | python3 operations/x-count.py

他のスクリプトからは weight(text) と MAX_WEIGHT を使う（x-gate.py）。
"""
import bisect
import json
import re
import sys
import unicodedata
from pathlib import Path

MAX_WEIGHT = 280
URL_WEIGHT = 23       # transformedURLLength：Xは全URLをt.coに置換し、長さにかかわらず一律23で数える
EMOJI_WEIGHT = 2      # emojiParsingEnabled: true のときの defaultWeight
# twitter-text v3 の config：この範囲は重み1、それ以外は重み2
LIGHT_RANGES = [(0, 4351), (8192, 8205), (8208, 8223), (8242, 8247)]
MAX_URL_LENGTH = 4096
MAX_TCO_SLUG_LENGTH = 40

_DATA = json.loads(Path(__file__).with_name("x-count-data.json").read_text(encoding="utf-8"))
_EXTRACT_URL = re.compile(_DATA["extractUrl"], re.I)
_ASCII_DOMAIN = re.compile(_DATA["validAsciiDomain"], re.I)
_TCO_URL = re.compile(_DATA["validTcoUrl"], re.I)
_BAD_PREFIX = re.compile(_DATA["invalidUrlWithoutProtocolPrecedingChars"])
_INVALID_CHARS = re.compile(_DATA["invalidChars"])
_EMOJI = re.compile(_DATA["emoji"])
_PICT = [tuple(r) for r in _DATA["pictographic"]]     # Extended_Pictographic（絵柄）の範囲。re には \p{...} が無いので表で持つ
_PICT_STARTS = [a for a, _ in _PICT]
_ZWJ, _VS16, _KEYCAP = 0x200D, 0xFE0F, 0x20E3

# JS の /i と Python の re.I は、大文字小文字の対応表が違う。違いが出る文字だけ、同じ長さの別の文字に置き換えてから正規表現に通す
# （位置は1文字ずつ対応するので、URLの切り出しは元の文字列から行う。tests/xcount.py が全コードポイントで公式と突き合わせている）
#   İ ı ſ   Python の re.I は ASCII の i・s と同じ扱いにする。JS は別の文字として、ラテン拡張（U+0100–024F）の範囲で受ける → 同じ範囲の ƀ に
#   U+A7DC  Unicode 16 で加わった文字。JS は ƛ（U+019B）の大文字として範囲に入れる。Python 3.11 の表（Unicode 14）は知らない → ƀ に
#   K（U+212A）  Python の re.I は k と同じ扱い。JS は別の文字（ドメインには使えるが、ASCIIだけのドメインとは見なさない）→ 私用領域の文字に
_CASEFOLD_TRAP = str.maketrans({"\u0130": "\u0180", "\u0131": "\u0180", "\u017f": "\u0180", "\ua7dc": "\u0180", "\u212a": "\ue000"})


def _utf16_len(s):
    return len(s.encode("utf-16-le", "surrogatepass")) // 2


def _puny_to_ascii(label):
    """punycode.toASCII の移植（長さを測るためだけに使う）。@の前はそのまま、. 。 ． ｡ で区切ってラベルごとに変換"""
    parts = label.split("@")
    prefix = ""
    if len(parts) > 1:
        prefix, label = parts[0] + "@", parts[1]
    label = re.sub("[\x2e。．｡]", ".", label)
    out = []
    for piece in label.split("."):
        if re.search("[^\x20-\x7e]", piece):
            try:
                out.append("xn--" + piece.encode("punycode").decode("ascii"))
            except (UnicodeError, OverflowError):
                return None
        else:
            out.append(piece)
    return prefix + ".".join(out)


def _valid_domain(domain, probe_domain):
    """公式 idna.toAscii の移植。ラベルが63字を超える・不正なpunycodeはURLと見なさない（domain は元の文字列、probe_domain は置き換え後）"""
    if probe_domain[:4] == "xn--" and not _ASCII_DOMAIN.search(probe_domain):
        return False
    for label in domain.split("."):
        enc = _puny_to_ascii(label)
        if enc is None or not 1 <= len(enc) <= 63:
            return False
    return len(domain) > 0


def extract_urls(text):
    """公式 extractUrlsWithIndices（スキームなしも拾う設定）の移植。[(start, end, url)] を返す（位置はコードポイント）"""
    if not text or "." not in text:
        return []
    probe = text.translate(_CASEFOLD_TRAP)
    urls = []
    for m in _EXTRACT_URL.finditer(probe):
        before = m.group(2) or ""
        url = m.group(3) or ""
        protocol = m.group(4) or ""
        domain = m.group(5) or ""
        path = m.group(7) or ""
        end = m.end()
        start = end - len(url)
        orig_domain = text[m.start(5):m.end(5)] if m.group(5) is not None else ""
        orig_url = text[start:end]
        if not _valid_domain(orig_domain, domain) or _utf16_len(protocol or "https://") + _utf16_len(orig_url) > MAX_URL_LENGTH:
            continue
        if not protocol:
            # スキームなし（example.com など）。直前が - _ . / なら URL にしない
            if _BAD_PREFIX.search(before):
                continue
            last = None
            ascii_end = 0
            for am in _ASCII_DOMAIN.finditer(domain):
                a_start = domain.index(am.group(0), ascii_end)
                ascii_end = a_start + len(am.group(0))
                last = [start + a_start, start + ascii_end]
                urls.append(last)
            if last is None:
                continue
            if path:
                last[1] = end
        else:
            # t.co は後ろに余計な文字を続けさせない
            tco = _TCO_URL.match(url)
            if tco:
                if tco.group(1) and len(tco.group(1)) > MAX_TCO_SLUG_LENGTH:
                    continue
                end = start + len(tco.group(0))
            urls.append([start, end])
    return [(s, e, text[s:e]) for s, e in urls]


def extract_emoji(text):
    """公式（twemoji-parser 11.0.2 の表）が「絵文字1つ」と認めるもの。[(start, end, emoji)]"""
    return [(m.start(), m.end(), m.group(0)) for m in _EMOJI.finditer(text)]


def _count(norm):
    """NFC正規化済みの文字列の重みと内訳（公式 parseTweet の本体）"""
    urls = extract_urls(norm)
    emojis = extract_emoji(norm)
    url_at = {s: (e - s) for s, e, _ in urls}
    emoji_at = {s: (e - s) for s, e, _ in emojis}
    total = 0
    light = heavy = 0
    i = 0
    n = len(norm)
    while i < n:
        if i in url_at:
            total += URL_WEIGHT
            i += url_at[i]
            continue
        if i in emoji_at:
            total += EMOJI_WEIGHT
            i += emoji_at[i]
            continue
        o = ord(norm[i])
        # JSは2つ目の半分（低位サロゲート）で重みを決めるので、基本多言語面の外は常に2
        if o <= 0xFFFF and any(a <= o <= b for a, b in LIGHT_RANGES):
            total += 1
            light += 1
        else:
            total += 2
            heavy += 1
        i += 1
    return {"weight": total, "urls": urls, "emojis": emojis, "light": light, "heavy": heavy}


def _is_pict(cp):
    k = bisect.bisect_right(_PICT_STARTS, cp) - 1
    return k >= 0 and cp <= _PICT[k][1]


def _is_skin(cp):
    return 0x1F3FB <= cp <= 0x1F3FF


def _is_ri(cp):
    return 0x1F1E6 <= cp <= 0x1F1FF


def _in_run(cp):
    return _is_pict(cp) or cp in (_ZWJ, _VS16, _KEYCAP) or _is_skin(cp) or _is_ri(cp)


def uncertain_emoji(norm, emojis, urls):
    """公式ライブラリが「1つの絵文字」と認識できず、部品ごとに数えた並びを探す。[(並び, その重み)]
    公式の絵文字表は古い（Emoji 11＝2018年まで）ので、新しい絵文字（ハートの炎など）や、余分な異体字セレクタつきのものが当たる。
    実際のXが2で数えるかは確認できていない。公式どおりに数えると2より多くなる（重めの見積もり）。
    投稿まえチェック（tools/post-mae-check/src/core.js の uncertainEmoji）と同じ判定。tests/xcount.py で一致を確認"""
    n = len(norm)
    covered = bytearray(n)
    for s, e, _ in list(emojis) + list(urls):
        covered[s:e] = b"\x01" * (e - s)
    out = []
    i = 0
    while i < n:
        if not _in_run(ord(norm[i])):
            i += 1
            continue
        j = i
        while j < n and _in_run(ord(norm[j])):
            j += 1
        run = norm[i:j]
        cps = [ord(c) for c in run]
        has_seq = any(c in (_ZWJ, _VS16, _KEYCAP) or _is_skin(c) or _is_ri(c) for c in cps)
        has_pict = any(_is_pict(c) or _is_skin(c) or _is_ri(c) for c in cps)    # 絵柄が無い並び（ZWJだけ・数字の後ろのFE0Fだけ）は絵文字ではない
        if has_seq and has_pict:
            stray = False
            for s, e, text in emojis:
                if s < i or e > j:
                    continue
                o = ord(text) if len(text) == 1 else None
                if text == chr(_VS16):                                           # 単独の異体字セレクタ（公式の表は絵文字1つとして2で数える）
                    stray = True
                elif o is not None and _is_skin(o) and s > 0 and covered[s - 1]:  # 直前の絵文字にくっついた単独の肌色
                    stray = True
                elif o is not None and _is_ri(o) and ((s >= 1 and _is_ri(ord(norm[s - 1]))) or (e < n and _is_ri(ord(norm[e])))):
                    stray = True                                                 # 国旗になれなかった地域指示文字の並び
            if stray or not all(covered[i:j]):
                out.append((run, _count(run)["weight"]))
        i = j
    return out


def analyze(text):
    """重みと内訳を返す。公式 parseTweet と同じ結果になるように作ってある"""
    norm = unicodedata.normalize("NFC", text)
    r = _count(norm)
    r["invalid"] = bool(_INVALID_CHARS.search(norm))
    r["uncertain"] = uncertain_emoji(norm, r["emojis"], r["urls"])
    return r


def weight(text):
    return analyze(text)["weight"]


def _short(s, n=40):
    return s if len(s) <= n else s[:n] + "…"


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    text = text.rstrip("\n")
    r = analyze(text)
    w = r["weight"]
    ok = w <= MAX_WEIGHT
    print(f"素の文字数 : {len(text)}")
    print(f"X重み      : {w} / {MAX_WEIGHT}")
    print(f"残り       : {MAX_WEIGHT - w}")
    print(f"判定       : {'[OK]' if ok else '[NG] 超過'}")
    # 何をURLとして23で数えたかを見せる（2026-09-02の「裸ドメインを数え落とす」ような見落としに気づけるように）
    if r["urls"]:
        shown = "、".join(_short(u) for _, _, u in r["urls"][:5])
        more = f" ほか{len(r['urls']) - 5}件" if len(r["urls"]) > 5 else ""
        print(f"URL換算    : {len(r['urls'])}件×{URL_WEIGHT}（{shown}{more}）")
    if r["uncertain"]:
        shown = "、".join(f"{t} → {w}" for t, w in r["uncertain"][:6])
        print(f"⚠️ 絵文字注意: {shown}（公式の表にない並びを部品ごとに数えている。実際のXが2で数えるかは未確認＝重めの見積もり）")
    if r["invalid"]:
        print("⚠️ 注意    : Xが受け付けない文字（U+FEFF・U+FFFE・U+FFFF）が含まれています")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
