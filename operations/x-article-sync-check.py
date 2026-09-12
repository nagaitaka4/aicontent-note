#!/usr/bin/env python3
"""X編集部と記事編集部の連携を機械で検査する（2026-09-12新設）。

背景：「記事ネタになりそうな内容は依頼を待たずバックログに追記する」という決まりがあるのに、
X側の下書き（PERM-01・AUTOTAB-01）が記事側に渡っていなかった。人の記憶に頼らず、毎回ここで検査する。

検査すること
  1. knowledge/x/queue.md の在庫サマリー表にあるIDが、記事側（article-backlog.md／tasks/README.md／
     operations/structure-drafts/*-facts.md）のどこかで参照されているか
  2. knowledge/x/ideas.md の「取材待ちリスト」で行頭に 📝（記事級）が付いた行が、記事側で参照されているか
  3. 記事側（tasks/README.md のTOP10・待機列）の各行が「X側の材料」を明記しているか（無ければ「未確認」と出す）
終了コード：未連携が1件以上あれば 1
"""
import io, os, re, sys, glob

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
T = os.path.expanduser("~/Documents/GitHub/tasks/README.md")


def rd(p):
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


queue = rd(R + "knowledge/x/queue.md")
ideas = rd(R + "knowledge/x/ideas.md")
article_side = rd(R + "operations/article-backlog.md") + rd(T) + "".join(rd(p) for p in glob.glob(R + "operations/structure-drafts/*-facts.md"))

# 1. queue の在庫サマリー表（| 順位 | ID | 内容 | ... ）から生きているIDを取る
ids = []
for line in queue.splitlines():
    m = re.match(r"^\|\s*(\d+|—)\s*\|\s*\**([A-Za-z0-9ぁ-ん一-龥ー]+-[A-Za-z0-9ぁ-ん一-龥ー]+)\**\s*\|\s*(.*?)\s*\|", line)
    if m and "~~" not in line:
        ids.append((m.group(2), m.group(3)[:40]))
missing_q = [(i, t) for i, t in ids if i not in article_side]

# 2. 取材待ちリストの 📝 行
sec = ideas.split("## 取材待ちリスト", 1)[1] if "## 取材待ちリスト" in ideas else ""
flagged = [l for l in sec.splitlines() if l.startswith("| 📝")]
missing_i = []
for l in flagged:
    key = re.sub(r"[*📝|]", "", l).strip()[:24]
    if key and key not in article_side:
        missing_i.append(key)

# 3. TOP10・待機列の行に「X側の材料」があるか
tl = rd(T).splitlines()
rows = []
inside = False
for l in tl:
    if l.startswith("## ▼ 全体 TOP10"):
        inside = True
        continue
    if inside and l.startswith("## ") :
        break
    if inside and re.match(r"^\| (\d{1,2}) \| ", l):
        rows.append(l)
no_x = [re.sub(r"\*", "", l.split("|")[2]).strip()[:36] for l in rows if "X側の材料" not in l and "X側" not in l]

print(f"[queue] 在庫サマリーのID {len(ids)}件のうち、記事側に参照が無いもの {len(missing_q)}件")
for i, t in missing_q:
    print(f"   - {i}：{t}")
print(f"[ideas] 取材待ちリストの📝行 {len(flagged)}件のうち、記事側に参照が無いもの {len(missing_i)}件")
for k in missing_i:
    print(f"   - {k}")
print(f"[tasks] TOP10・待機列 {len(rows)}行のうち、「X側の材料」を明記していない行 {len(no_x)}件（未確認＝X側をgrepしてから判定する）")
for k in no_x:
    print(f"   - {k}")
sys.exit(1 if (missing_q or missing_i) else 0)
