#!/usr/bin/env python3
"""要注意表現・重なりの判定が、既存の x-hook.py / x-cannibal.py と同じになるかを見る（前半）。

  python3 parity.py   → out/parity-expected.json を作る
  node parity.js      → それを JS 版の判定と突き合わせる（後半）

突き合わせる文章は、リポジトリの実物（sns/posts-stock.md の全投稿・knowledge/x/queue.md の下書き）と、
端の例を集めた手書きの文。実物の文章はこのファイルにも fixtures にも写さない（out/ は git に入れない）。
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OPS = HERE.parent.parent.parent / "operations"


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, OPS / file)
    m = importlib.util.module_from_spec(spec)
    sys.argv = [file]
    spec.loader.exec_module(m)
    return m


hook = load("x_hook", "x-hook.py")
cann = load("x_cannibal", "x-cannibal.py")

# 文章を集める
texts = []
for head, body in cann.blocks(cann.STOCK, re.compile(r"^### .+｜.+｜(\d{4}-\d{2}-\d{2})\s*$")):
    texts.append((head[4:].split("｜")[0], body))
for head, body in cann.blocks(cann.QUEUE, re.compile(r"^### ")):
    texts.append(("Q:" + re.sub(r"[（(].*$", "", head[4:]).strip(), body))

synthetic = [
    "Claude Codeが使えるようになりました。無料プランも対象です。",
    "Claude Codeが使えるようになりました。でも自分は月100ドルのまま。",
    "記事を書きました",
    "記事を書きました。\n\n自分の話です。",
    "3本書きました。",
    "ずっとプランを試してませんでした。",
    "昨日の「無料でリセット」も、まだ押してません。",
    "先日の件と例の設定、前の投稿、9/28に「やった」こと。",
    "これは前回の続きです。それから、これから、それぞれ、あれこれ、それでも。",
    "これが1行目。\nそれは2行目。",
    "\n\n  空行から始まる。\nあれ",
    "一昨日の話。先週の話。さっきの話。この前の話。",
    "何かを調べました！\n\n本文",
    "報告しました？ 次の文です。",
    "AIで5,000字を書きました。",
    "１００本書きました",
    "できるようになりました。",
    "Claude Codeで100ドル分を使いました。8,300字と8,300字も出た。",
    "Claude Code と ChatGPT と Gemini の話。Sonnet 5.5 と Opus 5.5 を比べた。",
    "1件だけ、1本だけ、1回だけ。2件。",
    "",
]
for i, t in enumerate(synthetic):
    texts.append((f"S{i}", t))
texts = [(f"{i:03d}:{label}", t) for i, (label, t) in enumerate(texts)]   # 同じIDが重なっても取り違えないよう通し番号をつける

out = {"texts": [], "overlaps": {}}
for label, t in texts:
    first, tail, signals, has_num = hook.check_first_line(t) if t.strip() else ("", None, [], False)
    leaks = sorted({m.group(0) for p in hook.CONTEXT_LEAK for m in re.finditer(p, t)})
    report = bool(tail and not signals and not has_num)
    out["texts"].append({"label": label, "text": t, "first": first, "report": report, "tail": tail if report else None, "leaks": leaks})

# 重なり：x-cannibal.py main() の判定そのまま（全投稿・全下書きの総当たり）
for label, t in texts:
    if not t.strip():
        continue
    g, mk = cann.grams(t), cann.marks(t)
    hits = []
    for l2, b2 in texts:
        if not b2.strip() or cann.norm(b2) == cann.norm(t):
            continue
        gb = cann.grams(b2)
        jac = len(g & gb) / max(1, len(g | gb))
        shared = sorted(mk & cann.marks(b2))
        nums = [s for s in shared if re.match(r"[0-9０-９]", s)]
        if jac >= cann.JACCARD or nums or len(shared) >= 2:
            hits.append({"other": l2, "jac": jac, "shared": shared})
    out["overlaps"][label] = hits

# AIっぽさ（v2・2026-10-06）：article-self-check.py の NG_AI_PHRASES／constraints.py の VAGUE_NOUN_RE／x-hook.py の check_shape
# 対象は上の文章に加えて、公開記事の本文を段落ごとに（地の文体に誤って当たらないかも同時に見る）
sys.path.insert(0, str(OPS))
selfcheck = load("article_self_check", "article-self-check.py")
NG_AI = [p for p in selfcheck.NG_AI_PHRASES]
ai_texts = [(label, t) for label, t in texts]
ARTICLES = OPS.parent / "articles"
for f in sorted(ARTICLES.glob("*.md")):
    raw = f.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", raw, re.S)
    if not m or not re.search(r"^status:\s*published", m.group(1), re.M):
        continue
    body = re.sub(r"```.*?```", "", raw[m.end():], flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    for j, para in enumerate(b for b in re.split(r"\n\s*\n", body) if b.strip()):
        ai_texts.append((f"A:{f.stem[:24]}:{j}", para))
for t_ in [
    "課金の要否は、使い方で決まります。取れる手が変わる。",
    "ここまで3つの方法を説明してきました。続けるという点が重要です。",
    "明確なラインはありません。\n大きな差もありません。",
    "新機能が出ました。\n\n料金は据え置きです。\n\n自分はまだ試していません。",
    "新機能が出ました。\n\n料金は据え置きです。\n\n自分の場合はどうしますか？",
    "新機能が出ました。\n\n\n\n自分は試しました。",
    "　\n\n自分の話。\n\n説明です。",
]:
    ai_texts.append((f"AS{len(ai_texts)}", t_))
out["ai"] = []
for label, t in ai_texts:
    phrases = sorted(m.group(0) for line in t.split("\n") for pat in NG_AI for m in re.finditer(pat, line))
    first = next((l for l in t.split("\n") if l.strip()), "")
    vague = sorted(m.group(0) for m in re.finditer(selfcheck.VAGUE_NOUN_RE, first))
    shape = hook.check_shape(t)[1] if t.strip() else None
    out["ai"].append({"label": label, "text": t, "phrases": phrases, "vague": vague, "shape": shape})

(HERE / "out").mkdir(exist_ok=True)
(HERE / "out" / "parity-expected.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"文章 {len(texts)} 本（実物 {len(texts) - len(synthetic)}・手書き {len(synthetic)}）／重なりの組 {sum(len(v) for v in out['overlaps'].values())} 件／AIっぽさの突き合わせ {len(out['ai'])} 本（公開記事の段落を含む）")
