#!/usr/bin/env python3
"""X投稿の1行目チェック（x-firstline.py）

**1行目に固有名詞（製品名・サービス名）が入っているか**を機械で判定する。

⚠️ 2026-09-18変更：**NGではなく「要目視」を返す。**製品名は「1行目で何の話か分かる」ための
代表例であって、条件ではない。無いときは、1行目だけ読んで分かるかを人が見て決める。

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
    # カタカナ表記（2026-09-08追加：「サーチコンソール」を拾えず誤検知した）
    "サーチコンソール","グーグル","クロード","チャットGPT","ワードプレス","メルカリ",
    # デザインツール（2026-09-17追加：no.68の下書きで「Canva」を拾えず誤検知した）
    "Canva","Adobe","Firefly","Illustrator","Photoshop","Figma",
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
        print("判定  : [要目視] 1行目に製品名・サービス名がありません")
        print("      1行目だけを読んで、読者が何の話か分かりますか。")
        print("      分かるなら、そのまま出してよい（2026-09-18変更）。")
        print("      ⚠️ 製品名は「何の話か分かる」ための代表例であって、条件ではない。")
        print("      題材がツールを特定しない記事（ロゴ・著作権など）で製品名に置き換えると、記事より狭い話に見える。")

if __name__ == "__main__":
    main()
