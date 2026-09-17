# -*- coding: utf-8 -*-
"""実験A・Bの集計（2026-09-17）。

A：紹介文30本で「こだわ」が出た本数と回数を数える。
B：記事9本に同じfrontmatterを付けて article-self-check.py を実行し、NGと要確認の項目を条件ごとに並べる。
   CTA・関連記事は3条件とも指示していないので比較から外す。
"""
import glob, os, re, subprocess, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

def exp_a(folder="a", conds=("none", "neg", "pos")):
    rows = {}
    for cond in conds:
        files = sorted(glob.glob(os.path.join(HERE, folder, f"out_{cond}_*.txt")))
        texts = [open(f, encoding="utf-8").read() for f in files]
        hit = [len(re.findall("こだわ", t)) for t in texts]
        fun = [t.count("ふんわり") for t in texts]
        rows[cond] = {"n": len(texts), "本数": sum(1 for h in hit if h), "回数": sum(hit),
                      "ふんわり本数": sum(1 for h in fun if h),
                      "字数中央値": sorted(len(t) for t in texts)[len(texts)//2] if texts else 0}
    return rows

FM = """---
no: 999
title: ブログの更新が止まる理由と、止めないための工夫
slug: experiment
status: draft
description: ブログの更新が止まるのは、ネタ切れより工程の途中で止まることが多いからです。書き始める前と書いた後の2か所で止まる理由と、止めないために工程ごとに決めておくこと、週に1回見るとよい項目を、AIでブログを書いている個人の実体験からまとめました。
category: 継続できる運用設計
tags: ブログ,継続
eyecatch: none.png
---

"""
SKIP = ("CTA", "関連記事", "description", "タイトル35字", "frontmatter")

def exp_b():
    out = {}
    for cond in ["none", "current", "positive"]:
        out[cond] = []
        for f in sorted(g for g in glob.glob(os.path.join(HERE, "b", f"out_{cond}_*.md")) if not g.endswith(".checked.md")):
            body = open(f, encoding="utf-8").read().strip()
            body = re.sub(r"^```(?:markdown|md)?\s*\n|\n```\s*$", "", body)
            tmp = f.replace(".md", ".checked.md")
            open(tmp, "w", encoding="utf-8").write(FM + body + "\n")
            r = subprocess.run(["python3", os.path.join(ROOT, "operations", "article-self-check.py"), tmp],
                               capture_output=True, text=True, cwd=ROOT)
            ng = [l.strip() for l in r.stdout.splitlines() if l.startswith("[NG]") and not any(k in l for k in SKIP)]
            warn = [l.strip() for l in r.stdout.splitlines() if l.startswith("[要確認]")]
            out[cond].append({"file": os.path.basename(f), "chars": len(re.sub(r"\s", "", body)), "NG": ng, "要確認": warn})
    return out

if __name__ == "__main__":
    print(json.dumps({"A": exp_a(), "A2": exp_a("a2", ("neg", "pos")), "B": exp_b()}, ensure_ascii=False, indent=1))
