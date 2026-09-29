#!/usr/bin/env python3
"""X投稿候補のカニバリ（直近の投稿・キューとの重なり）を機械で見る（2026-09-30新設）。

使い方:
  python3 operations/x-cannibal.py 本文.txt [--days 14]

見るもの:
  1. 直近の投稿（sns/posts-stock.md の全文アーカイブ・既定14日以内）
  2. キューの生きている下書き（knowledge/x/queue.md。取り消し線・投稿済み・不採用は除く）

判定（どちらかに当たれば [要確認]）:
  - 文字3グラムの重なり（Jaccard）が 0.18 以上
  - 数字つきの語（「100ドル」「8,300字」など）を1つでも共有している
  - 製品名・機能名など目印の語を2つ以上共有している（Claude・ChatGPTなど、どの投稿にも出る名前は数えない）

[要確認]は禁止ではない。**出力に「◯◯（日付）と◯◯が重なる」と1行書き、続き物として出すか、
題材・数字を替えるかを決める**（2026-09-30：AIMARU-01 が前日の作業の話、OCHITA-01 が
3〜4か月前の話で、どちらもユーザーに「面白くない」と言われた。直近の流れを見ていなかった）。
"""
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STOCK = ROOT / "sns" / "posts-stock.md"
QUEUE = ROOT / "knowledge" / "x" / "queue.md"
JACCARD = 0.18
# どの投稿にも出る製品名は目印にしない（出ても重なりの根拠にならない）
COMMON = {"ai", "x", "claude", "chatgpt", "claudecode", "openai", "gpt", "anthropic", "google", "gemini"}

MARK = re.compile(
    r"[0-9０-９][0-9０-９,，.]*\s*(?:ドル|円|字|本|件|倍|%|％|時間|分|日|か月|ヶ月|人|回)"
    r"|[A-Za-z][A-Za-z0-9.\- ]{1,20}[A-Za-z0-9]"
)


def norm(t):
    return re.sub(r"\s+", "", t)


def grams(t, n=3):
    t = norm(t)
    return {t[i:i + n] for i in range(len(t) - n + 1)}


def marks(t):
    out = set()
    for m in MARK.finditer(t):
        s = re.sub(r"\s+", "", m.group(0))
        if s.lower() in COMMON:
            continue
        if re.match(r"[0-9０-９]", s) and re.match(r"^[1１](件|本|回|人|日|つ)$", s):
            continue            # 「1件」「1本」のような小さい数は目印にしない
        out.add(s)
    return out


def blocks(path, header_re):
    """見出し直後の最初のコードブロックを本文として取る"""
    lines = path.read_text(encoding="utf-8").splitlines()
    res = []
    i = 0
    while i < len(lines):
        m = header_re.match(lines[i])
        if m:
            head = lines[i]
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```") and not lines[j].startswith("#"):
                j += 1
            if j < len(lines) and lines[j].startswith("```"):
                k = j + 1
                body = []
                while k < len(lines) and not lines[k].startswith("```"):
                    body.append(lines[k])
                    k += 1
                res.append((head, "\n".join(body)))
                i = k
        i += 1
    return res


def recent_posts(days):
    since = date.today() - timedelta(days=days)
    out = []
    for head, body in blocks(STOCK, re.compile(r"^### .+｜.+｜(\d{4}-\d{2}-\d{2})\s*$")):
        d = datetime.strptime(re.search(r"(\d{4}-\d{2}-\d{2})\s*$", head).group(1), "%Y-%m-%d").date()
        if d >= since:
            pid = head[4:].split("｜")[0]
            out.append((f"投稿 {pid}（{d.strftime('%m/%d')}）", body))
    return out


def live_queue():
    out = []
    for head, body in blocks(QUEUE, re.compile(r"^### ")):
        if "~~" in head or "投稿済み" in head or "不採用" in head or "閉じた" in head:
            continue
        pid = re.sub(r"[（(].*$", "", head[4:]).strip()
        out.append((f"キュー {pid}", body))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    days = 14
    if "--days" in sys.argv:
        days = int(sys.argv[sys.argv.index("--days") + 1])
        args = [a for a in args if a != str(days)]
    if len(args) != 1:
        sys.exit(__doc__)
    text = Path(args[0]).read_text(encoding="utf-8").strip()
    g, mk = grams(text), marks(text)
    hits = []
    for label, body in recent_posts(days) + live_queue():
        if norm(body) == norm(text):
            continue            # 同じ下書き自身
        gb = grams(body)
        jac = len(g & gb) / max(1, len(g | gb))
        shared = sorted(mk & marks(body))
        nums = [s for s in shared if re.match(r"[0-9０-９]", s)]
        if jac >= JACCARD or nums or len(shared) >= 2:
            hits.append((jac, label, shared))
    hits.sort(reverse=True)
    print(f"比べた範囲: 直近{days}日の投稿＋キューの生きている下書き")
    if not hits:
        print("判定: [OK] 重なりなし")
        return
    for jac, label, shared in hits[:6]:
        print(f"  {label}  重なり{jac:.2f}  共通の目印：{'・'.join(shared) if shared else 'なし'}")
    print("判定: [要確認] 出力に重なりを1行書き、続き物として出すか、題材・数字を替えるかを決める")


if __name__ == "__main__":
    main()
