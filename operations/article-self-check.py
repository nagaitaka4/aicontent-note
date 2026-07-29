#!/usr/bin/env python3
"""
記事MDファイルの機械チェック統合スクリプト。
rules/article-flow.mdの「機械チェック」項目をすべてここに集約する。
使い方: python3 operations/article-self-check.py articles/[slug].md

このスクリプトが検出できるのはルールのうち「grep・文字数・パターンで機械的に判定できるもの」のみ。
判断が必要な項目（事実性・トーン・体験談の圧縮加減など）はこのスクリプトの対象外。
実行後は必ずスクリプトの出力を読んでから記事を提示する（実行しただけで満足しない）。
"""

import re
import sys
import itertools
import difflib
from collections import Counter

NG_AI_PHRASES = [
    r"ここまで.{0,15}(書いて|説明して|見て|解説して)きました",
    r"について整理すると、大きく",
    r"という点が重要です",
    r"ということが言えます",
]

NG_INSTRUCTION = ["しましょう"]
NG_CTA_OLD = ["コンテンツ更新が止まっていませんか", "▶", "お気軽にご相談ください。", "ぜひ"]
CTA_STANDARD = "企画から執筆・公開まで、まるごとお任せください。お気軽にご相談を。"
CTA_SHIGYO = "企画から執筆・公開まで、まるごとお任せいただけます。気になる方はお気軽にご相談を。"

# 意図的に同じ文言が複数回出てOK（CTA・ブロック名単独行など）
BOILERPLATE_EXACT = {
    CTA_STANDARD,
    CTA_SHIGYO,
    "お気軽にご相談を。",
    "お問い合わせフォームはこちら",
    "＼　ブログ更新が止まっている・記事運用を任せたい方へ　／",
    "＼　ブログ運用代行を行っています　／",
}


def load(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    parts = text.split("---", 2)
    frontmatter = parts[1] if len(parts) > 2 else ""
    body = parts[2] if len(parts) > 2 else text
    return text, frontmatter, body


def fm_value(frontmatter, key):
    m = re.search(rf"^{key}:\s*(.*)$", frontmatter, re.M)
    return m.group(1).strip() if m else ""


def report(label, ok, detail=""):
    mark = "OK" if ok else "NG"
    line = f"[{mark}] {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    return ok


def main(path):
    text, frontmatter, body = load(path)
    lines = body.split("\n")
    failures = 0

    print("=== 🤖 機械チェック（rules/article-flow.md準拠） ===\n")

    # --- フロントマター ---
    title = fm_value(frontmatter, "title")
    desc = fm_value(frontmatter, "description")
    if not report("タイトル35字以内", len(title) <= 35, f"{len(title)}字: {title}"):
        failures += 1
    if not report("descriptionが120〜140字", 120 <= len(desc) <= 140, f"{len(desc)}字"):
        failures += 1

    # --- 禁止記号・表記 ---
    bad_bullets = [i for i, l in enumerate(lines, 1) if l.startswith("- ")]
    if not report("`-`箇条書きが残っていない", not bad_bullets, f"該当行: {bad_bullets}"):
        failures += 1

    nested = [i for i, l in enumerate(lines, 1) if re.match(r"^・.*・", l)]
    if not report("`・`のネストがない", not nested, f"該当行: {nested}（内部リンクタイトルの・は誤検知の可能性あり・目視で除外可）"):
        failures += 1

    blank_sep = re.findall(r"^・.*$\n\n^・.*$", body, re.M)
    if not report("`・`箇条書きが空行区切りになっていない（<br>を使う）", not blank_sep, f"{len(blank_sep)}件"):
        failures += 1

    half_space = [i for i, l in enumerate(lines, 1) if re.search(r"[。、] ", l)]
    if not report("句読点の後に不要な半角スペースがない", not half_space, f"該当行: {half_space}"):
        failures += 1

    quote_block = re.findall(r"^> ", body, re.M)
    if not report("`>`（Markdown引用）を使っていない", not quote_block, f"{len(quote_block)}件"):
        failures += 1

    old_comment = "<!-- [WP入稿" in body
    if not report("旧HTMLコメント形式のブロック記法がない", not old_comment):
        failures += 1

    shikou = [i for i, l in enumerate(lines, 1) if "しましょう" in l]
    if not report("「〜しましょう」の指示形を使っていない", not shikou, f"該当行: {shikou}"):
        failures += 1

    kiji_ni_kaki = "記事に書き" in body
    if not report("「記事に書きます」ではなく「ノートに残します」", not kiji_ni_kaki):
        failures += 1

    pronoun = [i for i, l in enumerate(lines, 1) if re.search(r"僕|俺", l)]
    if not report("一人称が「私」で統一されている", not pronoun, f"該当行: {pronoun}"):
        failures += 1

    # --- 見出しルール ---
    h2s = re.findall(r"^## (.+)$", body, re.M)
    matome_h2 = [h for h in h2s if "まとめ" in h]
    if not report("H2見出しに「まとめ」がない", not matome_h2, f"{matome_h2}"):
        failures += 1

    ng_heading_words = [h for h in [title] + h2s if re.search(r"導入|結論|まとめ", h)]
    if not report("タイトル・見出しに「導入」「結論」「まとめ」がない", not ng_heading_words, f"{ng_heading_words}"):
        failures += 1

    # --- 表・H3の使いすぎ ---
    table_count = len(re.findall(r"^\|.*\|\s*$\n\|[-:| ]+\|", body, re.M))
    if not report("表は3個まで", table_count <= 3, f"{table_count}個"):
        failures += 1

    h3s = re.findall(r"^### ", body, re.M)
    # 同一H2配下のH3が3つ以上連続していないか
    h2_blocks = re.split(r"^## ", body, flags=re.M)[1:]
    over_h3 = [b.split("\n", 1)[0] for b in h2_blocks if len(re.findall(r"^### ", b, re.M)) >= 3]
    if over_h3:
        print(f"[要確認] 同一H2内にH3が3つ以上: {over_h3}（表化を検討）")

    # --- ブロック要素（【ポイント】等）が長すぎないか ---
    block_matches = re.finditer(r"^【([^】]+)】<br>\n((?:.+\n?)+?)(?=\n\n|\n---|\Z)", body, re.M)
    long_blocks = []
    for m in block_matches:
        block_name, block_body = m.group(1), m.group(2)
        block_chars = len(re.sub(r"\s|<br>", "", block_body))
        if block_chars > 80:
            long_blocks.append((block_name, block_chars))
    if long_blocks:
        print(f"[要確認] ブロック要素が長すぎる可能性: {long_blocks}（80字目安。一言で伝わる長さか確認・箇条書き2つ以上の対比説明は表に戻すことを検討）")

    # --- 箇条書き3行以上連続（表化候補） ---
    bullet_runs = re.findall(r"(?:^・.*\n){3,}", body, re.M)
    if bullet_runs:
        print(f"[要確認] `・`箇条書きが3行以上連続する箇所が{len(bullet_runs)}件（表化を検討）")

    # --- AIっぽい接続表現 ---
    ai_hits = [(i, p) for i, l in enumerate(lines, 1) for p in NG_AI_PHRASES if re.search(p, l)]
    if not report("AIっぽい接続表現が混入していない", not ai_hits, f"{ai_hits}"):
        failures += 1

    # --- CTA ---
    cta_count = body.count("お問い合わせフォームはこちら")
    ng_cta_hits = [p for p in NG_CTA_OLD if p in body]
    is_standard_ok = (CTA_STANDARD in body) or (CTA_SHIGYO in body)
    print(f"[INFO] CTA出現回数: {cta_count}（副業検証シリーズ・Rシリーズは0が正しい。それ以外は通常2）")
    if cta_count > 0:
        if not report("CTA文言が現行フォーマット（通常/士業紹介型）と一致", is_standard_ok):
            failures += 1
        if not report("旧CTA表現（▶・ぜひ・お気軽にご相談ください等）が残っていない", not ng_cta_hits, f"{ng_cta_hits}"):
            failures += 1
    if cta_count == 2:
        cta_positions = [m.start() for m in re.finditer(r"お問い合わせフォームはこちら", body)]
        between = body[cta_positions[0]:cta_positions[1]]
        h2_between = len(re.findall(r"^## ", between, re.M))
        if not report("途中CTAと末尾CTAの間が3セクション以上", h2_between >= 3, f"{h2_between}セクション"):
            failures += 1

    # --- 関連記事 ---
    related_match = re.search(r"\*\*関連記事\*\*\n((?:・.*\n?)+)", body)
    if related_match:
        related_items = [l for l in related_match.group(1).split("\n") if l.strip()]
        report("関連記事が3本", len(related_items) == 3, f"{len(related_items)}本")

    # --- H2直下リード文の文数・段落長 ---
    print("\n--- H2直下リード文チェック ---")
    for s in re.split(r"^## ", body, flags=re.M)[1:]:
        h2title, rest = s.split("\n", 1) if "\n" in s else (s, "")
        # 【ブロック】・箇条書き・H3・CTA(＼)のいずれかが出た時点でリード文とみなす
        lead = re.split(r"\n(【|・|### |＼)", rest)[0].strip()
        # 内部リンクのアンカーテキスト内の「。」は文区切りではないため除外してからカウント
        lead_for_count = re.sub(r"\[[^\]]*\]", lambda m: m.group(0).replace("。", ""), lead)
        sentence_count = lead_for_count.count("。")
        over = sentence_count > 3
        print(f"[{'NG' if over else 'OK'}] {h2title[:30]} リード文{sentence_count}文" + ("（3文超）" if over else ""))
        if over:
            failures += 1

    # --- 重複チェック（feedback_no_repetition.mdより統合） ---
    print("\n--- 重複チェック ---")
    quotes = re.findall(r"「[^」]{2,20}」", body)
    dup_quotes = {k: v for k, v in Counter(quotes).items() if v > 1}
    report("同じ引用フレーズの使い回しがない", not dup_quotes, f"{dup_quotes}")

    chunks = []
    for line in body.split("\n"):
        line = line.strip()
        if not line or line.startswith(("#", "---", "＼", "[", "【")):
            continue
        if line in BOILERPLATE_EXACT:
            continue
        if re.match(r"^\|[-:| ]+\|$", line):  # 表の区切り行
            continue
        if re.match(r"^・?\[.*\]\(https?://[^)]+\)\s*$", line):  # リンクのみの行（関連記事リスト等）は構造上似るため除外
            continue
        if line.startswith("|"):
            chunks.extend(c.strip() for c in line.split("|") if c.strip() and c.strip() not in BOILERPLATE_EXACT)
        else:
            for sent in re.split(r"(?<=。)", line):
                sent = sent.strip()
                if sent and sent not in BOILERPLATE_EXACT:
                    chunks.append(sent)
    def link_href(s):
        m = re.search(r"\((https?://[^)]+)\)", s)
        return m.group(1) if m else None

    similar = [
        (round(difflib.SequenceMatcher(None, a, b).ratio(), 2), a, b)
        for a, b in itertools.combinations(chunks, 2)
        if len(a) >= 12 and len(b) >= 12
        and difflib.SequenceMatcher(None, a, b).ratio() > 0.4
        and not (link_href(a) and link_href(a) == link_href(b))  # 同じ内部リンクの本文/関連記事欄への重複掲載は仕様上OK
    ]
    if similar:
        print(f"[NG] 類似度0.4超の文ペアが{len(similar)}件見つかった（CTA・関連記事リンクは仕様上OKなので除外して目視確認）")
        for ratio, a, b in similar[:10]:
            print(f"   {ratio}: {a[:40]} / {b[:40]}")
        failures += 1
    else:
        print("[OK] 文単位の類似度チェックで重複なし")

    # --- 文字数 ---
    char_count = len(re.sub(r"\s", "", body))
    print(f"\n[INFO] 本文文字数（空白除く概算）: {char_count}字")

    print(f"\n=== 結果: NG {failures}件 ===")
    print("\n--- 👁 判断チェック（このスクリプトでは検出不可・目視で毎回確認） ---")
    for item in [
        "事実以外を書いていないか（実体験のないことを「試みた」と書いていないか）",
        "AIと人が対等な目線か（「AIはこういうもの」という断定がないか）",
        "一般論と自社サービスの説明を混同していないか",
        "断定を避ける表現・本音を出す表現が自然に入っているか",
        "軽い自虐が1〜2箇所程度か（多すぎ・なさすぎでないか）",
        "ネガティブな内容の後に前を向く一文があるか",
        "体験談セクションが記事全体の3割を超えていないか",
        "内部リンクが前回記事の振り返り文の中に自然に埋め込まれているか",
        "文字だけで長く続くセクションに図解画像候補の提案余地がないか",
    ]:
        print(f"  - {item}")

    return failures


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使い方: python3 operations/article-self-check.py articles/[slug].md")
        sys.exit(1)
    n = main(sys.argv[1])
    sys.exit(1 if n else 0)
