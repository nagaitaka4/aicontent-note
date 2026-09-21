#!/usr/bin/env python3
"""X投稿のフック・構成チェック（x-hook.py）

**「ニュース解説型」になっていないか**を機械で判定する。
`rules/x-post-flow.md`「硬く書かない」がNGと名指ししている形を、出力前に落とすためのもの。

    NGの形：解説3行 → 最後に自分1行。これはニュース紹介であって、このアカウントの投稿ではない。

2つだけ見る。

  A. 1行目が報告型で終わっていないか
     `〜できました。` `〜になりました。` `〜を書きました。` `〜を調べました。` など。
     これは記事の要約の型で、読む理由にならない（2026-09-18ユーザー指摘）。
     ただし同じ行に「落差・数字・断定」があれば通す（フックが立っているため）。

  B. 自分の話が最後の1ブロックにしか無くないか
     伸びている投稿は「自分の話が真ん中」にある（Plus3-気274／Opus5-気96／メルカリ-リ85）。
     最後のブロックだけに一人称が出るのは、上が全部ニュース解説だという形。

⚠️ どちらも[要書き直し]を返すだけでNGにはしない。`x-firstline.py`と同じ扱い。
   判定するのは人。機械は「見落とし」を防ぐ。

なぜ機械で見るか（2026-09-22・ユーザー指摘で4回目の同種）：
   「解説3行＋最後に自分1行」はルールに書いてあるが、**測る仕組みが無いので
   『通しました』と書けば通ったことになっていた。**重み280は`x-count.py`があるので
   一度も間違えていない。8/28・9/18・9/21・9/22と、フックだけ自己申告で
   すり抜けている。

使い方:
    python3 operations/x-hook.py "本文"
    python3 operations/x-hook.py < draft.txt
"""
import sys, re

# A：1行目の報告型の語尾
REPORT_TAIL = [
    "できました", "できるようになりました", "になりました", "なりました",
    "書きました", "調べました", "並べました", "作りました", "まとめました",
    "出ました", "始まりました", "追加されました", "公開されました",
    "しました", "ました",
]

# A：同じ行にあればフックが立っていると見なす語（落差・逆説・断定）
HOOK_SIGNALS = [
    "でも", "ただ", "じゃなくて", "ではなく", "なのに", "のに", "逆に",
    "だけ", "しか", "ません", "ないです", "より", "はずが", "と思ったら",
]

# B：一人称（`rules/x-post-flow.md`「一人称は『自分』」）
FIRST_PERSON = ["自分", "私", "うち"]


def blocks(text):
    return [b for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]


def sentences(line):
    """1行を文に割る。`〜できました。無料プランも対象です。`のように
    報告型が行の途中で終わる形をすり抜けさせないため（2026-09-22修正）。"""
    return [x for x in re.split(r"(?<=[。！!？?])", line) if x.strip()]


def check_first_line(text):
    lines = [l for l in text.strip().split("\n") if l.strip()]
    first = lines[0] if lines else ""
    tail = None
    for sent in sentences(first):
        t = next((t for t in REPORT_TAIL if re.search(t + r"[。！!]?$", sent.strip())), None)
        if t:
            tail = t
            break
    signals = [s for s in HOOK_SIGNALS if s in first]
    has_num = bool(re.search(r"[0-9０-９]", first))
    return first, tail, signals, has_num


def check_shape(text):
    bs = blocks(text)
    if len(bs) < 2:
        return bs, None
    hit = [i for i, b in enumerate(bs) if any(w in b for w in FIRST_PERSON)]
    if not hit:
        return bs, "none"          # 自分の話がどこにも無い
    if hit == [len(bs) - 1]:
        # 末尾が読者への問いかけなら、その「自分の」は読者を指している可能性が高い
        if re.search(r"[かの][。？?]?$", bs[-1].strip()):
            return bs, "reader"
        return bs, "last"          # 最後のブロックだけ
    return bs, "ok"


def main():
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    if not text.strip():
        print("本文が空です"); sys.exit(1)

    first, tail, signals, has_num = check_first_line(text)
    bs, shape = check_shape(text)
    warn = 0

    print("1行目 : %s" % first)
    if tail and not signals and not has_num:
        warn += 1
        print("A判定 : [要書き直し] 報告型の語尾『%s』で終わり、落差・数字・断定がありません" % tail)
        print("      これは記事の要約の型で、読む理由になりません。")
        print("      先頭に置くのは、告白（やっていなかったこと）・数字・落差。")
    else:
        why = []
        if not tail:  why.append("報告型の語尾でない")
        if signals:   why.append("落差の語＝" + "・".join(signals))
        if has_num:   why.append("数字あり")
        print("A判定 : [OK]（%s）" % "／".join(why))

    print("ブロック数: %d" % len(bs))
    if shape == "last":
        warn += 1
        print("B判定 : [要書き直し] 一人称が最後のブロックにしかありません")
        print("      『解説 → 最後に自分1行』＝ニュース紹介の形です。")
        print("      自分の話を真ん中に置く（実測：Plus3-気274／Opus5-気96／メルカリ-リ85）。")
    elif shape == "reader":
        warn += 1
        print("B判定 : [要書き直し] 一人称が最後の問いかけにしかありません")
        print("      『自分の』が読者を指していて、書き手の話がどこにも入っていない形です。")
        print("      ＝3条件の③（決断・感情）が無い状態。本人の一言を1行足すと強くなります。")
    elif shape == "none":
        print("B判定 : [要目視] 一人称がどこにもありません")
        print("      主語を省くのは可（日本語は成立する）。")
        print("      ただし『自分の話がそもそも入っていない』なら、ニュース紹介です。")
    else:
        print("B判定 : [OK]")

    print("判定  : %s" % ("[要書き直し] %d件" % warn if warn else "[OK]"))

if __name__ == "__main__":
    main()
