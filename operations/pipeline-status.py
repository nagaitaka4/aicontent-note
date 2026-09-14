#!/usr/bin/env python3
"""記事ネタの供給パイプラインの現在地を1画面で出す（2026-09-14新設・編集会議で設計をユーザー承認）。

在庫3段（テーママップの空欄／待機列の◯／材料シート完成＝すぐ出せる）・種類の比率（issue #2）・
計測カレンダーの期日を、ファイルから読んで並べる。文章のルールを増やさず、機械で数えるための道具。

使い方:
    python3 operations/pipeline-status.py            # 人が読む形
    python3 operations/pipeline-status.py --json     # 定期リサーチが読む形

読むファイル:
    ~/Documents/GitHub/tasks/README.md            TOP10（| 1〜10 |）と待機列（| 11〜20 |）
    operations/theme-map.md                       「読者の段階 × 決めたいこと」の表（アーカイブ欄が「無い」＝空欄）
    operations/structure-drafts/*-facts.md        材料シート（D-番号・T-番号・スラッグで行と対応づける）
    operations/measurement-calendar.md            計測カレンダー（期日）
"""
import datetime
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS = os.path.expanduser("~/Documents/GitHub/tasks/README.md")
THEME = os.path.join(ROOT, "operations", "theme-map.md")
SHEETS = os.path.join(ROOT, "operations", "structure-drafts", "*-facts.md")
CALENDAR = os.path.join(ROOT, "operations", "measurement-calendar.md")

MIN_OPEN_CELLS = 5   # テーママップの空欄（需要あり・アーカイブ無し）
MIN_WAIT_OK = 5      # 待機列の◯
MIN_SHEETS = 5       # 材料シート完成（すぐ出せる）
DUE_WINDOW_DAYS = 7  # 計測カレンダーで「近い期日」とみなす日数

# 材料シートに要る7節（見出しに含まれる語で判定。番号は見ない）
SHEET_SECTIONS = ["芯", "実物", "一次情報", "X編集部", "重なり", "需要", "まだ無い"]

# 種類の比率（GitHub issue #2「記事テーマ設計」。theme-map.md の記載）
RATIO_TARGET = {"実況": 40, "Claude運用": 25, "AI動向": 15, "仕事": 20}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def ids_in(text):
    return set(re.findall(r"\b[DT]-\d+\b", text))


def slugs_in(text):
    return set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+){2,}", text))


def classify(title, cat):
    """種類の推定。行の「（種類：◯◯）」の印 → TOP10の種類欄 → 題名の順。判定できないときは '?'。"""
    t = title + " " + cat
    m = re.search(r"種類：(実況|Claude運用|AI動向|仕事|線引き|リライト)", t)
    if m:  # 行に明示の印があればそれを最優先（例：（種類：実況））
        return m.group(1)
    if "【リライト】" in title:
        return "リライト"
    if "AI動向" in t:
        return "AI動向"
    if "線引き" in t:
        return "線引き"
    if "仕事" in t:
        return "仕事"
    if "実況" in t:
        return "実況"
    if any(k in t for k in ("Claude", "決める", "環境構築", "claude")):
        return "Claude運用"
    return "?"


def parse_tasks():
    lines = read(TASKS).split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("## ▼ 全体 TOP10"))
    rows = {}
    want = 1
    for l in lines[start:]:
        m = re.match(r"^\| (\d+) \| (.*)$", l)
        if not m:
            continue
        n = int(m.group(1))
        if n != want:
            continue
        cells = [c.strip() for c in l.split("|")]
        # cells[0]='' , [1]=番号, [2]=題, [3]=種類 or 判定, [4]=判定 or 根拠
        title = re.sub(r"\*\*", "", cells[2])
        if n <= 10:
            cat, judge = cells[3], cells[4]
        else:
            cat, judge = "", cells[3]
        sym = "◯" if "◯" in judge[:16] else "△" if "△" in judge[:16] else "✗" if "✗" in judge[:16] else "—"
        rows[n] = {
            "n": n, "title": title, "cat": cat, "judge": sym,
            "ids": ids_in(l), "slugs": slugs_in(l), "type": classify(title, cat),
        }
        want += 1
        if want > 20:
            break
    return rows


def parse_sheets():
    sheets = []
    for p in sorted(glob.glob(SHEETS)):
        text = read(p)
        head = "\n".join(text.split("\n")[:4])
        heads = [h for h in text.split("\n") if h.startswith("#")]
        present = [k for k in SHEET_SECTIONS if any(k in h for h in heads)]
        sheets.append({
            "file": os.path.basename(p),
            "slug": os.path.basename(p)[:-len("-facts.md")],
            "ids": ids_in(head),
            "present": present,
            "missing": [k for k in SHEET_SECTIONS if k not in present],
        })
    return sheets


def match_sheet(row, sheets):
    for s in sheets:
        if row["ids"] & s["ids"] or s["slug"] in row["slugs"]:
            return s
    return None


def parse_theme_open():
    open_cells = []
    in_stage = False
    for l in read(THEME).split("\n"):
        if l.startswith("### 段階"):
            in_stage = True
            continue
        if l.startswith("## "):
            in_stage = False
        if not in_stage or not l.startswith("| ") or l.startswith("| 決めたいこと") or l.startswith("|---"):
            continue
        cells = [c.strip() for c in l.split("|")]
        if len(cells) < 7:
            continue
        want, demand, archive, judge = cells[1], cells[2], cells[3], cells[5]
        if "無い" not in archive:
            continue
        if any(k in judge for k in ("TOP10", "待機", "◯", "統合", "出さない", "書かない", "既存で足りる")):
            continue
        open_cells.append({"want": re.sub(r"\*\*", "", want), "demand": demand[:60]})
    return open_cells


def parse_calendar(today):
    items = []
    if not os.path.exists(CALENDAR):
        return items
    for l in read(CALENDAR).split("\n"):
        if not l.startswith("| ") or l.startswith("| 計測") or l.startswith("|---"):
            continue
        cells = [c.strip() for c in l.split("|")]
        if len(cells) < 7:
            continue
        name, start, due, dest, state = cells[1], cells[2], cells[3], cells[4], cells[5]
        m = re.search(r"(\d{4})-(\d{2})-(\d{2})", due)
        due_date = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None
        days = (due_date - today).days if due_date else None
        items.append({"name": name, "start": start, "due": due, "dest": dest, "state": state, "days": days})
    return items


def main():
    today = datetime.date.today()
    rows = parse_tasks()
    sheets = parse_sheets()
    open_cells = parse_theme_open()
    cal = parse_calendar(today)

    top = [rows[n] for n in range(1, 11) if n in rows]
    wait = [rows[n] for n in range(11, 21) if n in rows]
    wait_ok = [r for r in wait if r["judge"] == "◯"]

    ready, lines_rows = [], []
    for r in top + wait:
        s = match_sheet(r, sheets)
        if s and not s["missing"]:
            ready.append(r)
        lines_rows.append((r, s))

    counts = {}
    for r in top + wait:
        counts[r["type"]] = counts.get(r["type"], 0) + 1
    total = len(top) + len(wait)

    due_soon = [c for c in cal if c["days"] is not None and c["days"] <= DUE_WINDOW_DAYS and "済" not in c["state"]]
    unmatched_sheets = [s for s in sheets if not any(match_sheet(r, [s]) for r in top + wait)]

    result = {
        "date": str(today),
        "top10": len(top), "wait": len(wait), "wait_ok": len(wait_ok),
        "open_cells": len(open_cells), "sheets_ready": len(ready),
        "ratio": counts, "ratio_target": RATIO_TARGET,
        "due_soon": due_soon, "rows": [
            {"n": r["n"], "judge": r["judge"], "type": r["type"], "title": r["title"][:48],
             "sheet": s["file"] if s else None, "missing": s["missing"] if s else SHEET_SECTIONS}
            for r, s in lines_rows],
        "open_cell_list": open_cells,
        "unmatched_sheets": [s["file"] for s in unmatched_sheets],
    }
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return

    def mark(v, m):
        return "✅" if v >= m else "🔴"

    print(f"# パイプラインの現在地（{today}）")
    print()
    print("## 在庫3段（下限）")
    print(f"{mark(len(open_cells), MIN_OPEN_CELLS)} テーママップの空欄（アーカイブ無し・未判定）: {len(open_cells)}本（下限{MIN_OPEN_CELLS}）")
    print(f"{mark(len(wait_ok), MIN_WAIT_OK)} 待機列の◯: {len(wait_ok)}本（下限{MIN_WAIT_OK}）／TOP10 {len(top)}本・待機列 {len(wait)}本")
    print(f"{mark(len(ready), MIN_SHEETS)} 材料シート完成（7節そろい＝すぐ出せる）: {len(ready)}本（下限{MIN_SHEETS}）")
    print()
    print("## TOP10・待機列と材料シート")
    for r, s in lines_rows:
        sheet = s["file"] if s else "シート無し"
        miss = "" if not s else ("　完成" if not s["missing"] else "　欠け: " + "・".join(s["missing"]))
        print(f"{r['n']:>2} {r['judge']} [{r['type']}] {r['title'][:44]} ｜ {sheet}{miss}")
    if unmatched_sheets:
        print("（TOP10・待機列のどの行にも対応しないシート: " + "・".join(s["file"] for s in unmatched_sheets) + "）")
    print()
    print("## 種類の比率（TOP10＋待機列）")
    for k, v in RATIO_TARGET.items():
        c = counts.get(k, 0)
        print(f"{k}: {c}本（{round(100 * c / total) if total else 0}%・目標{v}%）")
    others = {k: v for k, v in counts.items() if k not in RATIO_TARGET}
    if others:
        print("その他: " + "・".join(f"{k} {v}本" for k, v in others.items()) + "（リライト・線引きは目標の外。?は種類が判定できない行）")
    print()
    print("## テーママップの空欄（需要あり・アーカイブ無し・未判定）")
    for c in open_cells:
        print(f"- {c['want']} ｜ {c['demand']}")
    if not open_cells:
        print("- なし（生成機1「当たった記事の次の問い」で空欄を足す）")
    print()
    print(f"## 計測カレンダー（{DUE_WINDOW_DAYS}日以内の期日・超過）")
    for c in due_soon:
        flag = "🔴超過" if c["days"] < 0 else "⏰"
        print(f"{flag} {c['name']} ｜ 期日 {c['due']}（{c['days']:+d}日） → {c['dest']} ｜ {c['state']}")
    if not due_soon:
        print("- なし")
    if not cal:
        print("（operations/measurement-calendar.md が無い）")


if __name__ == "__main__":
    main()
