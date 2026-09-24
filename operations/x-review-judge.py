#!/usr/bin/env python3
"""X投稿の盲検レビュー（読者役3人）の返答を集計して、HR級の合否を機械で出す（2026-09-25新設）。

使い方:
  python3 operations/x-review-judge.py operations/x-review-runs/<日付>/<run>

読むもの: key.json（x-review-pack.py が作る）と result-1.json〜result-3.json（読者役の返答）
書くもの: judge.json（全候補の点数と合否）。合格した候補は pass-<ハッシュ>.txt に本文を保存する
          → x-gate.py はこの pass ファイルがある本文だけを「出してよい」にする

合格（HR級）の条件＝全部満たす。CCが目で判定しない:
  1. 分からない言葉・前提を挙げた読者が1人以下
  2. 止まる・面白い・フォローの平均がすべて4.0以上
  3. ニュースの紹介に見えると答えた読者が1人以下
  4. 書き手本人の決断・感情・失敗が入っていると答えた読者が2人以上（3条件の③）
  5. フォローしたくなる順の平均順位で、基準の3本のうち2本より上
"""
import json
import re
import sys
from pathlib import Path

MIN_SCORE = 4.0
KEYS = ("stop", "fun", "follow")


def load_result(p):
    raw = p.read_text(encoding="utf-8")
    m = re.search(r"\{.*\}", raw, re.S)   # 前後に文章が付いていても中のJSONだけ読む
    if not m:
        sys.exit(f"{p.name}: JSONが見つかりません")
    return json.loads(m.group(0))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    d = Path(sys.argv[1])
    key = json.loads((d / "key.json").read_text(encoding="utf-8"))
    results = [load_result(p) for p in sorted(d.glob("result-*.json"))]
    if len(results) < 3:
        sys.exit(f"読者役の返答が{len(results)}件しかありません（3件必要）")

    n = len(results)
    rows = []
    for it in key:
        lab = it["label"]
        posts = [r["posts"][lab] for r in results]
        ranks = [r["rank"].index(lab) + 1 for r in results]
        row = dict(it)
        row["avg"] = {k: round(sum(p[k] for p in posts) / n, 2) for k in KEYS}
        row["unknown_readers"] = sum(1 for p in posts if p.get("unknown"))
        row["unknown_terms"] = sorted({t for p in posts for t in p.get("unknown", [])})
        row["news_votes"] = sum(1 for p in posts if p.get("news"))
        row["person_votes"] = sum(1 for p in posts if p.get("person"))
        row["profile_votes"] = sum(1 for p in posts if p.get("profile"))
        row["avg_rank"] = round(sum(ranks) / n, 2)
        row["comments"] = [p.get("comment", "") for p in posts]
        rows.append(row)

    base_ranks = sorted(r["avg_rank"] for r in rows if r["kind"] == "baseline")
    second_best_base = base_ranks[1]      # 基準3本のうち2本より上＝2番目の基準より小さい順位

    for r in rows:
        if r["kind"] != "candidate":
            continue
        why = []
        if r["unknown_readers"] > 1:
            why.append(f"分からない言葉を挙げた読者{r['unknown_readers']}人：" + "・".join(r["unknown_terms"]))
        low = [k for k in KEYS if r["avg"][k] < MIN_SCORE]
        if low:
            why.append("平均4.0未満：" + "・".join(f"{k}={r['avg'][k]}" for k in low))
        if r["news_votes"] > 1:
            why.append(f"ニュースの紹介に見える{r['news_votes']}人")
        if r["person_votes"] < 2:
            why.append(f"本人の決断・感情が見える{r['person_votes']}人（③が弱い）")
        if not r["avg_rank"] < second_best_base:
            why.append(f"平均順位{r['avg_rank']}が基準の2本目（{second_best_base}）より上でない")
        r["pass"] = not why
        r["why"] = why

    (d / "judge.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    rows.sort(key=lambda r: r["avg_rank"])
    print(f"読者役 {n}人／{len(rows)}本（平均順位の順）")
    for r in rows:
        tag = "基準" if r["kind"] == "baseline" else ("✅合格" if r["pass"] else "❌")
        a = r["avg"]
        print(f"  {r['avg_rank']:>4} {tag:<4} {r['id']}  止{a['stop']} 面{a['fun']} フォ{a['follow']}"
              f"  プロフ{r['profile_votes']}/{n}  hash={r['hash']}")
        if r["kind"] == "candidate" and not r["pass"]:
            for w in r["why"]:
                print(f"         - {w}")
    passed = [r for r in rows if r["kind"] == "candidate" and r["pass"]]
    for r in passed:
        (d / f"pass-{r['hash']}.txt").write_text(r["text"] + "\n", encoding="utf-8")
    print()
    if passed:
        best = passed[0]
        print(f"判定: [合格] {best['id']}（{len(passed)}本合格）")
        print(f"次  : python3 operations/x-gate.py 本文ファイル  ※1文字でも変えたら再レビュー")
    else:
        print("判定: [不合格] 合格0本。読者役のコメントで3本とも書き直して再実行（上限3回）。")
        print("      3回とも不合格なら、同じ題材を捨てて次の材料へ（SKILL.md 手順5-00の掘る順番）")
        for r in rows:
            if r["kind"] == "candidate":
                for c in r["comments"]:
                    if c:
                        print(f"      [{r['id']}] {c}")


if __name__ == "__main__":
    main()
