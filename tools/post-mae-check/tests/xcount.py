#!/usr/bin/env python3
"""operations/x-count.py が、公式ライブラリ（twitter-text 3.1.0）と同じ結果になるかを確かめる。

  node tests/gen-xcount-expected.js   公式の答えを tests/out/xcount-cases.json に作る（先に実行）
  python3 tests/xcount.py             x-count.py を突き合わせる

見るもの：fixtures（公式の適合テスト＋手書き例）／乱数60,000本／Unicodeの全絵文字／
          1文字ずつ全コードポイントを6つの型（ドメイン・TLD・パスなど）に置いた約78万本。
          重みとURLの一致を見る。CLI（出力4行・終了コード）も確認する。
"""
import importlib.util
import json
import os
import subprocess
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
OPS = HERE.parent.parent.parent / "operations"

# 環境変数 XCOUNT_PATH で別のコピーを検証できる（わざと壊したコピーでテストが落ちることを確かめるため）
TARGET = Path(os.environ.get("XCOUNT_PATH", OPS / "x-count.py"))
spec = importlib.util.spec_from_file_location("x_count", TARGET)
xc = importlib.util.module_from_spec(spec)
sys.argv = ["x-count.py"]
spec.loader.exec_module(xc)

cases = json.loads((HERE / "out" / "xcount-cases.json").read_text(encoding="utf-8"))
fail = 0


def ng(msg):
    global fail
    fail += 1
    if fail <= 25:
        print("  [NG] " + msg)


# 1. fixtures
n = 0
for c in cases["fixtures"]:
    n += 1
    got = xc.weight(c["t"])
    if got != c["w"]:
        ng(f"[fixtures/{c['source']}] {c['t'][:30]!r}: 公式 {c['w']} / x-count {got}")
print(f"fixtures（公式の適合テスト＋手書き例）: {n - fail} / {n} 本一致")

# 2. 乱数
before = fail
for c in cases["fuzz"]:
    a = xc.analyze(c["t"])
    urls = [u for _, _, u in a["urls"]]
    if a["weight"] != c["w"] or urls != c["u"]:
        ng(f"[乱数] {c['t']!r}: 公式 {c['w']} {c['u']} / x-count {a['weight']} {urls}")
    if [t for t, _ in a["uncertain"]] != c["un"]:
        ng(f"[乱数・絵文字注意] {c['t']!r}: JS版 {c['un']} / x-count {[t for t, _ in a['uncertain']]}")
print(f"乱数: {len(cases['fuzz']) - (fail - before)} / {len(cases['fuzz'])} 本一致（重み・URL・絵文字注意）")

# 3. 全絵文字
before = fail
for c in cases["emoji"]:
    if xc.weight(c["t"]) != c["w"]:
        ng(f"[絵文字] {c['e']!r}: 公式 {c['w']} / x-count {xc.weight(c['t'])}")
    if bool(xc.analyze(c["e"])["uncertain"]) != c["uncertain"]:
        ng(f"[絵文字注意] {c['e']!r}: JS版 {c['uncertain']} / x-count {bool(xc.analyze(c['e'])['uncertain'])}")
print(f"Unicodeの全絵文字: {len(cases['emoji']) - (fail - before)} / {len(cases['emoji'])} 個一致（重みと絵文字注意）")

# 4. 全コードポイント×6型
templates = [
    lambda c: "x" + c + ".com", lambda c: c + "a.com", lambda c: "http://a.com/" + c + "x",
    lambda c: "a.com/" + c, lambda c: "a." + c + "om", lambda c: "a.co" + c,
]
before = fail
total = 0
idx = 0
for a, b in cases["cpRanges"]:
    for cp in range(a, b + 1):
        ch = chr(cp)
        for k, f in enumerate(templates):
            t = f(ch)
            total += 1
            r = xc.analyze(t)
            w, u = cases["cp"]["w"][k][idx], cases["cp"]["u"][k][idx]
            if r["weight"] != w or len(r["urls"]) != u:
                ng(f"[1文字×型{k}] U+{cp:04X} {t!r}: 公式 {w}(URL{u}) / x-count {r['weight']}(URL{len(r['urls'])})")
        idx += 1
print(f"全コードポイント×6型: {total - (fail - before)} / {total} 本一致")

# 5. CLI：出力4行・終了コードが変わっていない
def cli(text):
    p = subprocess.run([sys.executable, str(TARGET), text], capture_output=True, text=True)
    return p.returncode, p.stdout.splitlines()

rc, lines = cli("あ" * 140)
want = ["素の文字数 : 140", "X重み      : 280 / 280", "残り       : 0", "判定       : [OK]"]
if rc != 0 or lines[:4] != want:
    ng(f"[CLI] 280ちょうど: {rc} {lines}")
rc, lines = cli("あ" * 141)
want = ["素の文字数 : 141", "X重み      : 282 / 280", "残り       : -2", "判定       : [NG] 超過"]
if rc != 1 or lines[:4] != want:
    ng(f"[CLI] 282: {rc} {lines}")
rc, lines = cli("詳しくは https://example.com/a と README.md を")
if rc != 0 or not any(l.startswith("URL換算    : 2件×23") for l in lines):
    ng(f"[CLI] URL換算の行: {rc} {lines}")
rc, lines = cli("a\ufeffb")
if rc != 0 or not any("受け付けない文字" in l for l in lines):
    ng(f"[CLI] 無効な文字の注意: {rc} {lines}")
hof = "".join(map(chr, [0x2764, 0xFE0F, 0x200D, 0x1F525]))      # 公式の表に無い絵文字の並び（ハートの炎）
rc, lines = cli("焼けた" + hof)
if rc != 0 or not any(l.startswith("⚠️ 絵文字注意: " + hof + " → 5") for l in lines):
    ng(f"[CLI] 絵文字注意の行: {rc} {lines}")
p = subprocess.run([sys.executable, str(TARGET)], input="標準入力から\n", capture_output=True, text=True)
if p.returncode != 0 or p.stdout.splitlines()[:2] != ["素の文字数 : 6", "X重み      : 12 / 280"]:
    ng(f"[CLI] 標準入力: {p.returncode} {p.stdout.splitlines()}")
print("CLI（出力4行・終了コード・URL換算の行・標準入力）: 確認")

print("\n全部一致" if fail == 0 else f"\n不一致 {fail} 件")
sys.exit(1 if fail else 0)
