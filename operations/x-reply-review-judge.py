#!/usr/bin/env python3
"""Xリプライの別エージェントレビュー（3人）の返答を集計して、出してよいかを機械で出す（2026-09-25新設）。

使い方:
  python3 operations/x-reply-review-judge.py operations/x-review-runs/<日付>/<run>

合格＝全部満たす（CCが目で判定しない）:
  1. 親投稿の本題に返している（on_core）と3人全員が答えた
  2. 分からない言葉・前提を挙げた読者が1人以下
  3. 教える・訂正・持論に見えると答えた読者が0人
  4. 決まり文句・AIっぽいと答えた読者が1人以下
  5. 親投稿の本人（読者役1）の「うれしいか」が4以上
合格したリプライは reply-pass-<ハッシュ>.txt に保存 → x-gate.py --reply はこれがある本文だけ通す。

経緯（2026-09-25）：朝ブリーフのリプライ案が、相手の投稿の本題（AIの言う通りに500部刷った収支報告）ではなく、
リンク先noteの途中の細部（「PDF不可」の訂正）に寄せていた。手元のネタ（その日の投稿と同じ話）に合わせたため。
ユーザー指摘「リプライ先の内容とコメント内容あってますか？」で発覚。
"""
import json
import re
import sys
from pathlib import Path


def load_result(p):
    m = re.search(r"\{.*\}", p.read_text(encoding="utf-8"), re.S)
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

    print("読者役が書いた親投稿の本題：")
    for n, r in zip(("本人", "フォロワー", "通りすがり"), results):
        print(f"  {n}：{r.get('core', '')}")
    print()

    rows = []
    passed = []
    for it in key["items"]:
        lab = it["label"]
        rs = [r["replies"][lab] for r in results]
        row = dict(it)
        row["on_core"] = sum(1 for x in rs if x.get("on_core"))
        row["unknown_readers"] = sum(1 for x in rs if x.get("unknown"))
        row["unknown_terms"] = sorted({t for x in rs for t in x.get("unknown", [])})
        row["lecture"] = sum(1 for x in rs if x.get("lecture"))
        row["template"] = sum(1 for x in rs if x.get("template"))
        row["glad_author"] = rs[0].get("glad", 0)
        row["glad_avg"] = round(sum(x.get("glad", 0) for x in rs) / len(rs), 2)
        row["profile"] = sum(1 for x in rs if x.get("profile"))
        row["comments"] = [x.get("comment", "") for x in rs]
        why = []
        if row["on_core"] < 3:
            why.append(f"本題に返していると答えたのが{row['on_core']}/3人（全員必要）")
        if row["unknown_readers"] > 1:
            why.append(f"分からない言葉を挙げた読者{row['unknown_readers']}人：" + "・".join(row["unknown_terms"]))
        if row["lecture"] > 0:
            why.append(f"教える・訂正・持論に見える{row['lecture']}人")
        if row["template"] > 1:
            why.append(f"決まり文句・AIっぽい{row['template']}人")
        if row["glad_author"] < 4:
            why.append(f"本人のうれしさ{row['glad_author']}（4以上必要）")
        row["pass"] = not why
        row["why"] = why
        rows.append(row)
        if row["pass"]:
            passed.append(row)
            (d / f"reply-pass-{row['hash']}.txt").write_text(row["text"] + "\n", encoding="utf-8")

    (d / "judge.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    for r in rows:
        print(f"{'✅合格' if r['pass'] else '❌'} {r['id']}  本題{r['on_core']}/3  本人のうれしさ{r['glad_author']}"
              f"（平均{r['glad_avg']}）  プロフ{r['profile']}/3  hash={r['hash']}")
        for w in r["why"]:
            print(f"     - {w}")
        if not r["pass"]:
            for c in r["comments"]:
                if c:
                    print(f"     [{r['id']}] {c}")
    print()
    if passed:
        best = max(passed, key=lambda r: (r["glad_avg"], r["profile"]))
        print(f"判定: [合格] {best['id']}")
        print("次  : python3 operations/x-gate.py 本文ファイル --reply  ※1文字でも変えたら再レビュー")
    else:
        print("判定: [不合格] 合格0本。コメントで書き直して再実行する。")
        print("      本題に返せる自分の実測が無いなら、その相手は見送って次の候補を探す（手元のネタに合わせて相手の話を曲げない）。")


if __name__ == "__main__":
    main()
