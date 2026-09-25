#!/usr/bin/env python3
"""GPTレビュー用のテキストを1つにまとめ、ファイルに保存してクリップボードに入れる（2026-09-24新設・同日改訂）。

使い方:
  python3 operations/review-pack.py <構成案または記事のMD> [--stage 構成案|本文]

まとめる順番:
  1. このファイル固有の依頼（operations/review-requests/<同じファイル名>。CCがGPT向けに書く）
  2. 共通の見方（operations/gpt-article-review-prompt.md のコードブロック）
  3. 本文（構成案なら先頭の稿だけ。「# 以下、第N稿（参考」以降は送らない）

依頼文を本文と別のファイルに置くのは、CCの見立てを提示前の別エージェントのレビューに混ぜないため。
保存先：operations/review-packs/<ファイル名>.txt（.gitignore）。別セッションにクリップボードを上書きされたら
`bash cb.sh` で入れ直せる。
"""
import os, re, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

def common_request():
    t = (ROOT / "operations/gpt-article-review-prompt.md").read_text()
    m = re.search(r"```\n(.*?)```", t, re.S)
    return m.group(1).strip() if m else ""

def copy_to_clipboard(text):
    """LANGが空だと pbcopy は日本語を黙って0字にする（2026-09-25に発覚）。UTF-8を指定し、読み戻して確かめる。"""
    env = {**os.environ, "LANG": "ja_JP.UTF-8", "LC_CTYPE": "UTF-8"}
    subprocess.run("pbcopy", input=text.encode(), check=True, env=env)
    got = subprocess.run("pbpaste", capture_output=True, env=env).stdout.decode("utf-8", "replace")
    if got != text:
        print(f"★クリップボードに入っていません（{len(text)}字中{len(got)}字）")
        sys.exit(3)


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    path = pathlib.Path(sys.argv[1]).resolve()
    stage = sys.argv[sys.argv.index("--stage") + 1] if "--stage" in sys.argv else "本文"
    req = ROOT / "operations/review-requests" / path.name
    if not req.exists():
        print(f"⚠️ 依頼文がありません：{req.relative_to(ROOT)}。CCが書いてから実行してください。")
        sys.exit(2)
    specific = re.sub(r"^# .*\n", "", req.read_text()).strip()
    body = re.split(r"^# 以下、第\d+稿（参考", path.read_text(), flags=re.M)[0].rstrip()
    out = "\n\n".join([
        f"【レビューの対象】{stage}（{path.name}）",
        "【このレビューで見てほしいこと（この記事固有）】\n" + specific,
        "【共通の見方】\n" + common_request(),
        "【ここから対象の全文】\n" + body,
    ])
    packs = ROOT / "operations/review-packs"
    packs.mkdir(exist_ok=True)
    dest = packs / (path.stem + ".txt")
    dest.write_text(out)
    copy_to_clipboard(out)
    rel = dest.relative_to(ROOT)
    print(f"クリップボードに入れました：{len(out)}字（依頼文＋{stage}）")
    print(f"保存先：{rel}")
    print("入れ直すコマンド：bash cb.sh")

if __name__ == "__main__":
    main()
