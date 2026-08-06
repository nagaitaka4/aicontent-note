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
CTA_SHIGYO = "企画から執筆・公開まで、まるごとお任せください。お気軽にご相談を。"

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
    # bodyはfrontmatter除去後のため、報告する行番号にファイル基準のオフセットを加える
    offset = text[: text.index(body)].count("\n") if body in text else 0
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

    nested = [
        i + offset
        for i, l in enumerate(lines, 1)
        if re.match(r"^・.*・", re.sub(r"\[.*?\]\(.*?\)", "", l))
        and not l.lstrip().startswith(("|", "#"))
    ]
    if not report("`・`のネストがない", not nested, f"該当行（ファイル基準）: {nested}／項目内の列挙は`A / B`にする"):
        failures += 1

    blank_sep = re.findall(r"^・.*$\n\n^・.*$", body, re.M)
    if not report("`・`箇条書きが空行区切りになっていない（<br>を使う）", not blank_sep, f"{len(blank_sep)}件"):
        failures += 1

    # 2026-08-06：文頭の接続語・主題の「〜は」のあとに読点がないと読みづらいという
    # 指摘を受けて追加。目的語（〜を）や短い副詞の直後は対象外（読点過多を防ぐ）。
    CONJ = "ただし|しかし|また|なお|さらに|一方|逆に|つまり|そのため|例えば"
    comma_miss = []
    for i, l in enumerate(lines, 1):
        if l.lstrip().startswith(("|", "#", "・", "＼", ">")):
            continue
        for m in re.finditer(rf"(?:^|。)({CONJ})(?![、。])", l):
            comma_miss.append((i + offset, m.group(1)))
        for m in re.finditer(r"(当サービス|このメディア|当社)は(?![、。])", l):
            comma_miss.append((i + offset, m.group(0)))
    if not report(
        "接続語・主題の「〜は」の後に読点がある",
        not comma_miss,
        f"該当（ファイル基準）: {comma_miss}／「ただし、」「当サービスは、」の形にする",
    ):
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
        block_body_no_links = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", block_body)
        block_chars = len(re.sub(r"\s|<br>", "", block_body_no_links))
        if block_chars > 80:
            long_blocks.append((block_name, block_chars))
    if not report("ブロック要素が80字以内", not long_blocks, f"{long_blocks}（一言で伝わる長さか確認・箇条書き2つ以上の対比説明は表に戻すことを検討。内容が濃く80字超が妥当な場合のみ目視判断でOK扱いにしてよい）"):
        failures += 1

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

    # --- 段落の長さチェック（リード文だけでなく本文中の全段落が対象。2026-07-31〜）---
    # 従来のリード文チェックは「最初のブロック/箇条書きが出るまで」しか見ておらず、
    # 箇条書き・表・ブロックの後に続く地の文が野放しになっていた。文数だけでなく字数（4行=160字目安）も見る。
    print("\n--- 段落の長さチェック（4行=160字目安。箇条書き・ブロック後の地の文も対象） ---")
    # H1直下の導入リード文はGEO対応ルール（メインKW+直接回答を1文目に含む別基準）の対象のため除外する
    body_after_intro = re.split(r"^## ", body, maxsplit=1, flags=re.M)
    body_for_para_check = "## " + body_after_intro[1] if len(body_after_intro) > 1 else ""
    paragraphs = re.split(r"\n\s*\n", body_for_para_check)
    long_paras = []
    for p in paragraphs:
        p = p.strip()
        if not p or p in BOILERPLATE_EXACT:
            continue
        if re.match(r"^(#|---|\||＼|【|・|-|\[お問い合わせ)", p):
            continue
        plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", p)
        plain = re.sub(r"<br>|\s", "", plain)
        if len(plain) > 160:
            long_paras.append((len(plain), p[:30] + "…"))
    if not report("4行(160字)を超える段落がない", not long_paras, f"{long_paras}"):
        failures += 1

    # --- 一文の長さチェック（2026-08-05〜）---
    # 段落チェック（160字）は通っても、1文が長いままだと読みにくい。
    # 公開53本の実測では平均文長34〜53字・70字超は各記事0〜8件。70字を上限として運用する。
    print("\n--- 一文の長さチェック（70字上限） ---")
    sent_src = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", body_for_para_check)
    long_sents = []
    for line in sent_src.split("\n"):
        line = line.strip()
        if not line or line in BOILERPLATE_EXACT:
            continue
        if re.match(r"^(#|---|\||＼|\[お問い合わせ)", line):
            continue
        for sent in re.split(r"(?<=。)", re.sub(r"<br>", "", line)):
            sent = sent.strip()
            if len(sent) > 70:
                long_sents.append((len(sent), sent[:40] + "…"))
    if not report("70字を超える一文がない", not long_sents, f"{len(long_sents)}件"):
        for n, s in long_sents:
            print(f"   {n}字: {s}")
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
        # 2026-08-06：表のセルは構造化データであり、同じ製品名・項目名が複数の表に出るのは正常。
        # 旧実装はセルを「|」を外して取り出していたため、後段の「表の行同士は除外」条件が一度も
        # 効かず、ヘッダーの製品名同士が完全一致NGとして毎回上がっていた。このチェックの目的は
        # 地の文の言い回しの使い回し検出なので、表の行そのものを対象外にする。
        if line.startswith("|"):
            continue
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
        and difflib.SequenceMatcher(None, a, b).ratio() >= 0.6
        and not (link_href(a) and link_href(a) == link_href(b))  # 同じ内部リンクの本文/関連記事欄への重複掲載は仕様上OK
        and not (link_href(a) and link_href(b))  # 内部リンク導入文同士は「〜は「記事名」で〜」の型が似るため除外
        and not (
            a.lstrip().startswith("・") and b.lstrip().startswith("・")
            and difflib.SequenceMatcher(None, a, b).ratio() < 0.99
        )  # 箇条書き同士は型が揃うのが自然（チェックリスト等）。完全一致のみ検出する
    ]
    # 2026-08-05：閾値0.4は表の並列や導入文の型まで拾い、毎回20件超のNGが出て
    # 「目視で判断」の名のもとに読み流される状態だった。実害のある重複だけを
    # 検出するよう0.6へ引き上げ、表の行同士と内部リンク導入文同士を除外する。
    # 完全一致（1.0）は文言の使い回しなので、閾値に関わらず必ず検出される。
    if similar:
        exact = [x for x in similar if x[0] >= 0.99]
        print(f"[NG] 類似度0.6以上の文ペアが{len(similar)}件（うち完全一致{len(exact)}件）")
        print("     → 完全一致は必ず修正する。0.6〜0.99は片方の表現を変えるか、内容の重複ならセクションごと見直す")
        for ratio, a, b in similar:
            mark = "★完全一致" if ratio >= 0.99 else "        "
            print(f"   {mark} {ratio}: {a[:38]} / {b[:38]}")
        failures += 1
    else:
        print("[OK] 文単位の類似度チェックで重複なし")

    # --- 文字数（2026-08-05〜 INFO表示からNG判定へ変更）---
    # ※かつて4,000字を上限NGにしていたが、それが「NG 0件にするために内容を削る」
    #   という原則2違反を誘発したため2026-08-06に撤廃した。
    # 2026-08-06：文字数をNG判定にしていたため「NG 0件にするために内容を削る」
    # という原則2違反を誘発していた。適正な分量は記事とKWによって異なるので
    # 上限は設けず、参考値の表示のみにする（判断は人が行う）。
    print("\n--- 文字数（参考値・NG判定はしない） ---")
    char_count = len(re.sub(r"\s", "", body))
    print(f"[INFO] 本文 {char_count}字（公開記事の中央値は約3,500字）")
    print("   → 冗長なら削る。ただし数値を理由に内容を削らない（原則2）")

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
