#!/usr/bin/env python3
"""X投稿の盲検レビューを「3人の読者役」に配る準備をする（2026-09-25新設）。

使い方:
  python3 operations/x-review-pack.py 候補1.txt 候補2.txt 候補3.txt [--run 名前]

  引用ポストで出す候補は、本文のあとに「---引用---」の行を置き、その下に引用する投稿を書く
  （読者役には引用つきで見せる。ハッシュ＝ゲートで照合するのは本文だけ・2026-11-05）

やること:
  1. 候補（2〜4本）に、基準の3本（sns/posts-stock.md の実物）を混ぜてシャッフルする
  2. 読者役3人ぶんの依頼文を書き出す（同じ並び・違う読者像）
  3. どれが候補でどれが基準かの対応表（key.json）を保存する

出力先: operations/x-review-runs/<日付>/<run>/
  prompt-1.md〜prompt-3.md … Agentツールにそのまま渡す（ファイル・会話の文脈は渡さない）
  key.json                 … x-review-judge.py が使う（読者役には見せない）

読者役の返答は result-1.json〜result-3.json に保存して、x-review-judge.py で判定する。
"""
import hashlib
import json
import random
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STOCK = ROOT / "sns" / "posts-stock.md"
RUNS = ROOT / "operations" / "x-review-runs"

# 基準の3本（実測で伸びた投稿）。本文は毎回 posts-stock.md から取る
BASELINES = ["Plus3-気", "Opus5-気", "GPTEND-01"]

# 読者役3人。このメディアの読者像（非エンジニア・コンテンツ運用で困っている人）から取る
PERSONAS = [
    "日本の会社員（事務・営業寄り）です。ChatGPTは仕事で少し使っていますが、Claudeはよく知りません。",
    "個人事業主で、自分のブログやSNSを回しています。AIは記事づくりに使い始めたところで、有料プランに入るか迷っています。",
    "中小企業のWeb担当です。会社のブログ更新を外注するか社内でAIを使って回すか迷っています。AIツールの名前はだいたい聞いたことがあります。",
]

PROMPT = """あなたは次の人物です：{persona}
Xのタイムラインを流し見しています。この投稿者のことは何も知りません。前の投稿も読んでいません。
（ツールやファイルは使わず、読んだ印象だけで答えてください）

下の{labels}は、同じアカウントの投稿です。1本ずつ、流し見で読む感覚で評価してください。

各投稿について：
- unknown：意味が分からない言葉・前提（何のことか分からない固有名詞、「昨日の〜」など前を知らないと通じない言い回し、説明のない画面の項目名）。無ければ空の配列
- stop：スクロールが止まるか（1〜5）。1行目だけで判断
- fun：面白いか（1〜5）。書き手の人柄・意外性・失敗や迷いが見えるか。情報だけなら低い
- follow：この人をフォローしたくなるか（1〜5）。次の投稿も読みたいか
- profile：この投稿を読んで、プロフィールを見に行くか（true/false）
- news：ニュースの紹介に見えるか（true/false）。公式発表の要約＋最後に一言、の形なら true
- person：書き手本人の決断・感情・失敗が入っているか（true/false）
- premise：この投稿が受けている話・前提（誰かの意見・話題・「〜と言われる」など）を1文で（topic）。その話が投稿の中（引用している投稿を含む）に書いてあるか（in_post：true/false）。前提なしで成り立つ投稿なら topic は空・in_post は true。**読み手が好意的に補わないと分からない前提は false**
- comment：どこで読む気が落ちたか、何があれば良くなるか（1〜2文）

最後に、全部を「フォローしたくなる順」に並べてください（rank）。

**回答はJSONだけを1つ返してください。前後に文章を書かないでください。**形：
{{"posts": {{"A": {{"unknown": [], "stop": 3, "fun": 3, "follow": 3, "profile": false, "news": false, "person": true, "premise": {{"topic": "", "in_post": true}}, "comment": ""}}, ...}}, "rank": ["A", ...]}}

{body}
"""


def norm(text):
    """判定とゲートで同じ本文かを比べるための正規化（行末の空白と前後の空行だけ落とす）"""
    return "\n".join(l.rstrip() for l in text.strip().split("\n"))


def text_hash(text):
    return hashlib.sha256(norm(text).encode("utf-8")).hexdigest()[:16]


def baseline_text(pid):
    s = STOCK.read_text(encoding="utf-8")
    m = re.search(r"^### " + re.escape(pid) + r"｜.*?\n```\n(.*?)\n```", s, re.S | re.M)
    if not m:
        sys.exit(f"基準 {pid} の本文が posts-stock.md に見つかりません")
    return norm(m.group(1))


QUOTE_SEP = "---引用---"


def split_quote(raw):
    """本文と引用（あれば）に分ける。ハッシュは本文だけで取る"""
    if QUOTE_SEP in raw:
        body, quote = raw.split(QUOTE_SEP, 1)
        return norm(body), norm(quote)
    return norm(raw), ""


def main():
    args = sys.argv[1:]
    run = None
    if "--run" in args:
        i = args.index("--run")
        run = args[i + 1]
        del args[i:i + 2]
    if not 2 <= len(args) <= 4:
        sys.exit("候補は2〜4本（ファイルパス）を渡してください")

    items = []
    for p in args:
        t, q = split_quote(Path(p).read_text(encoding="utf-8"))
        items.append({"kind": "candidate", "id": Path(p).stem, "text": t, "quote": q, "hash": text_hash(t)})
    for b in BASELINES:
        t = baseline_text(b)
        items.append({"kind": "baseline", "id": b, "text": t, "hash": text_hash(t)})

    random.shuffle(items)
    labels = [chr(ord("A") + i) for i in range(len(items))]
    for lab, it in zip(labels, items):
        it["label"] = lab

    day = RUNS / date.today().isoformat()
    if not run:
        run = f"run{len(list(day.glob('run*'))) + 1 if day.exists() else 1}"
    d = day / run
    d.mkdir(parents=True, exist_ok=True)

    def show(it):
        s = f"【{it['label']}】\n{it['text']}"
        if it.get("quote"):
            s += "\n\n（この投稿は次の投稿を引用している）\n> " + it["quote"].replace("\n", "\n> ")
        return s

    body = "\n\n".join(show(it) for it in items)
    for n, persona in enumerate(PERSONAS, 1):
        (d / f"prompt-{n}.md").write_text(
            PROMPT.format(persona=persona, labels=f"{labels[0]}〜{labels[-1]}", body=body),
            encoding="utf-8")
    (d / "key.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"出力先: {d.relative_to(ROOT)}")
    for it in items:
        print(f"  {it['label']} = {it['id']}（{'候補' if it['kind'] == 'candidate' else '基準'}）")
    print("次: prompt-1〜3.md をそれぞれ別のAgent（general-purpose・並列）に渡し、")
    print(f"    返ってきたJSONを {d.relative_to(ROOT)}/result-1.json〜result-3.json に保存 →")
    print(f"    python3 operations/x-review-judge.py {d.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
