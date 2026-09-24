#!/usr/bin/env python3
"""GPTレビュー用のテキストを1つにまとめ、クリップボードに入れる（2026-09-24新設）。

使い方:
  python3 operations/review-pack.py <構成案または記事のMD> [--stage 構成案|本文]

まとめる順番:
  1. 共通の依頼文（operations/gpt-article-review-prompt.md のコードブロック）
  2. このファイル固有の依頼（ファイル内の「## レビュー依頼（GPT向け）」の節。CCが毎回書く）
  3. 本文（構成案なら先頭の稿だけ。「# 以下、第N稿（参考」以降は送らない）
"""
import re, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

def common_request():
    t = (ROOT / "operations/gpt-article-review-prompt.md").read_text()
    m = re.search(r"```\n(.*?)```", t, re.S)
    return m.group(1).strip() if m else ""

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    path = pathlib.Path(sys.argv[1])
    stage = "本文"
    if "--stage" in sys.argv:
        stage = sys.argv[sys.argv.index("--stage") + 1]
    body = path.read_text()
    body = re.split(r"^# 以下、第\d+稿（参考", body, flags=re.M)[0].rstrip()
    m = re.search(r"^## レビュー依頼（GPT向け）\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    specific = m.group(1).strip() if m else ""
    if m:
        body = (body[:m.start()] + body[m.end():]).strip()
    if not specific:
        print("⚠️ 「## レビュー依頼（GPT向け）」の節がありません。CCが書いてから実行してください。")
        sys.exit(2)
    out = "\n\n".join([
        f"【レビューの対象】{stage}（{path.name}）",
        "【このレビューで見てほしいこと（この記事固有）】\n" + specific,
        "【共通の見方】\n" + common_request(),
        "【ここから対象の全文】\n" + body,
    ])
    subprocess.run("pbcopy", input=out.encode(), check=True)
    print(f"クリップボードに入れました：{len(out)}字（依頼文＋{stage}）。ChatGPTに貼ってください。")

if __name__ == "__main__":
    main()
