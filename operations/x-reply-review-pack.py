#!/usr/bin/env python3
"""Xリプライの別エージェントレビューを「3人の読者役」に配る準備をする（2026-09-25新設）。

使い方:
  python3 operations/x-reply-review-pack.py 親投稿.txt リプライ1.txt [リプライ2.txt リプライ3.txt] [--link リンク先の要旨.txt] [--run 名前]

  親投稿.txt       … 相手の投稿の全文（引用・スレッドの続きも含める）。リンクカードの題もここに書く
  リプライN.txt    … リプライ案（1〜3本。書き出しを変えた案を並べると比べられる）
  --link           … 相手の投稿がリンクしている記事の要旨（任意）。**投稿した本人の役にだけ渡す**
                      （本人は自分の記事を知っているが、タイムラインの読者は知らない）

読者役3人:
  1. 親投稿を書いた本人      … 自分の話の本題に返してくれているか・うれしいか
  2. 親投稿のフォロワー      … 親投稿は読んだが、リンク先は読んでいない
  3. 通りすがり              … 親投稿を流し見しただけ。このリプライの主のことは知らない

出力先: operations/x-review-runs/<日付>/<run>/（prompt-1〜3.md・key.json）
返答を result-1〜3.json に保存して x-reply-review-judge.py で判定する。
"""
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "x-review-runs"

spec = importlib.util.spec_from_file_location("x_review_pack", HERE / "x-review-pack.py")
pack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pack)

PERSONAS = [
    ("author", "あなたは下の「親投稿」を書いた本人です。{link}知らないアカウントから、下のリプライ案のどれかが届きました。"),
    ("follower", "あなたは下の「親投稿」を書いた人のフォロワーです。親投稿は読みましたが、リンク先の記事は開いていません。親投稿の下に、知らないアカウントからのリプライが並んでいます。"),
    ("passerby", "あなたはXのタイムラインを流し見している日本の会社員です。下の「親投稿」をさっと読んだだけで、リプライを書いたアカウントのことは何も知りません。"),
]

PROMPT = """{persona}
（ツールやファイルは使わず、読んだ印象だけで答えてください）

【親投稿】
{parent}

下の{labels}は、この親投稿へのリプライ案です。1本ずつ評価してください。

まず最初に、親投稿の本題を1文で書いてください（core）。

各リプライ案について：
- on_core：親投稿の本題に返しているか（true/false）。本題ではない細部や、リプライを書いた人の自分の話に寄せているなら false
- unknown：意味が分からない言葉・前提。親投稿にもリプライにも書かれていない話に触れていて通じないところも含める。無ければ空の配列
- lecture：相手に教える・訂正する・持論を展開している感じがあるか（true/false）
- template：決まり文句・AIが書いたっぽさ・誰にでも使える返しに見えるか（true/false）
- glad：親投稿の本人がこれを受け取ってうれしいか（1〜5）
- profile：このリプライを読んで、書いた人のプロフィールを見に行くか（true/false）
- comment：どこが良い／悪いか、何があれば良くなるか（1〜2文）

**回答はJSONだけを1つ返してください。前後に文章を書かないでください。**形：
{{"core": "", "replies": {{"A": {{"on_core": true, "unknown": [], "lecture": false, "template": false, "glad": 3, "profile": false, "comment": ""}}, ...}}}}

{body}
"""


def main():
    args = sys.argv[1:]
    opts = {}
    for k in ("--link", "--run"):
        if k in args:
            i = args.index(k)
            opts[k] = args[i + 1]
            del args[i:i + 2]
    if not 2 <= len(args) <= 4:
        sys.exit(__doc__)

    parent = pack.norm(Path(args[0]).read_text(encoding="utf-8"))
    link = pack.norm(Path(opts["--link"]).read_text(encoding="utf-8")) if "--link" in opts else ""
    items = []
    for p in args[1:]:
        t = pack.norm(Path(p).read_text(encoding="utf-8"))
        items.append({"id": Path(p).stem, "text": t, "hash": pack.text_hash(t)})
    labels = [chr(ord("A") + i) for i in range(len(items))]
    for lab, it in zip(labels, items):
        it["label"] = lab

    day = RUNS / date.today().isoformat()
    run = opts.get("--run") or f"reply{len(list(day.glob('reply*'))) + 1 if day.exists() else 1}"
    d = day / run
    d.mkdir(parents=True, exist_ok=True)

    body = "\n\n".join(f"【{it['label']}】\n{it['text']}" for it in items)
    for n, (role, persona) in enumerate(PERSONAS, 1):
        link_line = f"親投稿のリンク先はあなたの記事で、要旨は次のとおりです：{link}\n" if (role == "author" and link) else ""
        (d / f"prompt-{n}.md").write_text(
            PROMPT.format(persona=persona.format(link=link_line), parent=parent,
                          labels=f"{labels[0]}〜{labels[-1]}" if len(labels) > 1 else "A", body=body),
            encoding="utf-8")
    (d / "key.json").write_text(json.dumps({"type": "reply", "parent": parent, "items": items},
                                           ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"出力先: {d.relative_to(HERE.parent)}")
    for it in items:
        print(f"  {it['label']} = {it['id']}")
    print("次: prompt-1〜3.md をそれぞれ別のAgent（general-purpose・並列）に渡し、")
    print(f"    返ってきたJSONを result-1〜3.json に保存 → python3 operations/x-reply-review-judge.py {d.relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
