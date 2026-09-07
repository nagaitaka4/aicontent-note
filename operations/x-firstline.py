#!/usr/bin/env python3
"""X投稿の1行目チェック（x-firstline.py）

**1行目に固有名詞（製品名・サービス名）が入っているか**を機械で判定する。

実測（2026-09-07・公開済み57本）：
    25ビュー以上 23本中20本（87%）が1行目に固有名詞あり
    25ビュー未満 34本中14本（41%）
上位9本のうち8本が1行目に固有名詞を置いている。

⚠️ これは「読者が1行目で何の話か分かるか」の代理指標。
下書きを書いた本人は元ネタを知っているため、「公式ページ」「今回は」で
意味が通ってしまう。目視の自己申告では検出できないので機械で見る。

使い方:
    python3 operations/x-firstline.py "本文"
    python3 operations/x-firstline.py < draft.txt
"""
import sys, re

NOUNS = [
    "ChatGPT","Claude","Google","GPT","Opus","Sonnet","Fable","Haiku",
    "Codex","Gemini","Cursor","DALL","Copilot","Perplexity","Anthropic","OpenAI",
    "WordPress","Search Console","GSC","Cowork","メルカリ","note","X",
    "Plus","Pro","Max","Git","GitHub","llms.txt","cats.txt",
]

def check(text):
    lines = [l for l in text.strip().split("\n") if l.strip()]
    if not lines:
        return None, [], "本文が空です"
    first = lines[0]
    hits = [n for n in NOUNS if n in first]
    return first, hits, None

def main():
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    first, hits, err = check(text)
    if err:
        print(err); sys.exit(1)
    print("1行目 : %s" % first)
    if hits:
        print("固有名詞: %s" % "・".join(hits))
        print("判定  : [OK]")
    else:
        print("固有名詞: なし")
        print("判定  : [NG] 1行目に製品名・サービス名がありません")
        print("      読者は1行目で何の話か分かりません。書き手だけが分かる状態です。")
        sys.exit(1)

if __name__ == "__main__":
    main()
