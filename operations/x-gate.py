#!/usr/bin/env python3
"""X投稿を「出してよいか」を1回で判定する最終ゲート（2026-09-25新設）。

使い方:
  python3 operations/x-gate.py 本文.txt --model <型ID> [--overlap "続き物として出す理由"]
  python3 operations/x-gate.py 本文.txt --reply   # リプライ（別エージェントのリプライレビュー合格を求める）

見るもの（全部 [OK] で「出してよい」）:
  1. 重み：280以下かつ残り5以上（x-count.py の数え方）
  2. 1行目の型：x-hook.py のA（報告型の語尾でない）
  3. 構成：x-hook.py のB（一人称が最後のブロックだけ＝ニュース紹介型でない）
  4. 文脈漏れ：x-hook.py のC（「昨日の」など前を知らないと通じない言い回しがない）
  5. 盲検：この本文と一字一句同じものが、今日か昨日の x-review-judge.py で合格している
     → レビューのあとで1文字でも直したら、ここで落ちる（2026-09-25：最後の2語修正が未レビューのまま出た）
  6. 型（2026-09-30新設）：--model の型IDが knowledge/x/model-posts.md の型一覧にある
     → 伸びた実物のどの型を真似たかが言えない候補は出さない
  7. カニバリ（2026-09-30新設）：x-cannibal.py で直近14日の投稿・キューと重なっていない。
     重なる場合は --overlap に「続き物として出す理由」を書けば通す（出力にその1行を載せる）

x-firstline.py（1行目の固有名詞）は[要目視]を返すだけなので、ここでは参考表示にとどめる。
"""
import importlib.util
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "x-review-runs"
MARGIN = 5


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), HERE / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    argv = sys.argv[1:]
    def opt(name):
        if name in argv:
            i = argv.index(name)
            v = argv[i + 1] if i + 1 < len(argv) else ""
            del argv[i:i + 2]
            return v
        return None
    model = opt("--model")
    overlap = opt("--overlap")
    reply = "--reply" in argv
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    count, hook, first, pack = load("x-count"), load("x-hook"), load("x-firstline"), load("x-review-pack")
    text = pack.norm(Path(args[0]).read_text(encoding="utf-8"))
    ng = []

    w = count.weight(text)
    rest = count.MAX_WEIGHT - w
    ok = rest >= MARGIN
    print(f"1 重み   : {w}/{count.MAX_WEIGHT}（残り{rest}） {'[OK]' if ok else '[NG] 残り5未満'}")
    if not ok:
        ng.append("重み")

    if not reply:
        _, tail, signals, has_num = hook.check_first_line(text)
        a_ng = bool(tail and not signals and not has_num)
        print(f"2 1行目  : {'[NG] 報告型の語尾「' + tail + '」' if a_ng else '[OK]'}")
        if a_ng:
            ng.append("1行目")

        _, shape = hook.check_shape(text)
        b_ng = shape in ("last", "reader")
        print(f"3 構成   : {'[NG] 自分の話が最後だけ（ニュース紹介型）' if b_ng else '[OK]'}")
        if b_ng:
            ng.append("構成")

    import re
    leaks = sorted({m.group(0) for p in hook.CONTEXT_LEAK for m in re.finditer(p, text)})
    print(f"4 文脈漏れ: {'[NG] ' + '・'.join(leaks) if leaks else '[OK]'}")
    if leaks:
        ng.append("文脈漏れ")

    h = pack.text_hash(text)
    days = [date.today(), date.today() - timedelta(days=1)]
    prefix = "reply-pass" if reply else "pass"
    hits = [p for d in days for p in (RUNS / d.isoformat()).glob(f"*/{prefix}-{h}.txt")]
    label = "リプライレビュー" if reply else "盲検"
    print(f"5 {label}: {'[OK] ' + str(hits[0].relative_to(HERE.parent)) if hits else '[NG] この本文は' + label + 'に合格していない（hash=' + h + '）'}")
    if not hits:
        ng.append(label)
    if not reply:
        lib = (HERE.parent / "knowledge" / "x" / "model-posts.md").read_text(encoding="utf-8")
        ok_model = bool(model) and f"| {model} |" in lib
        print(f"6 型     : {'[OK] ' + model if ok_model else '[NG] --model の型IDが model-posts.md の型一覧にない（' + str(model) + '）'}")
        if not ok_model:
            ng.append("型")
        import subprocess
        cp = subprocess.run([sys.executable, str(HERE / "x-cannibal.py"), args[0]], capture_output=True, text=True)
        over = "[要確認]" in cp.stdout
        lines = [l.strip() for l in cp.stdout.splitlines() if l.startswith("  ")]
        if over and overlap:
            print(f"7 カニバリ: [OK] 重なりあり・続き物として出す：{overlap}")
            for l in lines:
                print(f"           {l}")
        elif over:
            print("7 カニバリ: [NG] 直近の投稿・キューと重なる（--overlap に理由を書くか、題材・数字を替える）")
            for l in lines:
                print(f"           {l}")
            ng.append("カニバリ")
        else:
            print("7 カニバリ: [OK] 重なりなし")
        _, nouns, _ = first.check(text)
        print(f"  参考   : 1行目の固有名詞 {'・'.join(nouns) if nouns else 'なし（1行目だけで何の話か分かるか目で見る）'}")

    print()
    if ng:
        print(f"判定: [出さない] {'・'.join(ng)}")
        sys.exit(1)
    print("判定: [出してよい]")


if __name__ == "__main__":
    main()
