#!/usr/bin/env python3
"""X投稿の文字数チェック（x-count.py）

Xの上限は「280の重み付き文字数」。日本語・絵文字は1文字=2、半角英数・改行は1文字=1。
「140文字」は日本語だけで書いた場合の目安にすぎず、"Claude Code" のような
半角英字を含む投稿では140文字を超えても投稿できる。

2026-08-14、CCが「140字」を上限として下書きを削っていたが、
ユーザーが投稿した144文字の版は重み266で問題なく通った。
目視・概算をやめ、必ずこのスクリプトで判定する。

使い方:
    python3 operations/x-count.py "投稿本文"
    python3 operations/x-count.py < draft.txt
    echo "本文" | python3 operations/x-count.py
"""
import sys

# twitter-text v3：この範囲は重み1、それ以外は重み2
LIGHT_RANGES = [
    (0, 4351), (8192, 8205), (8208, 8210), (8214, 8231), (8240, 8286),
    (8289, 8292), (8294, 8304), (8308, 8334), (8336, 8348), (8352, 8383),
    (8400, 8432), (8448, 8587), (8592, 9254), (9280, 9290), (9312, 10239),
    (10496, 11007), (11360, 11391), (11776, 11903),
]
MAX_WEIGHT = 280


def weight(text):
    total = 0
    for ch in text:
        o = ord(ch)
        total += 1 if any(a <= o <= b for a, b in LIGHT_RANGES) else 2
    return total


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    text = text.rstrip("\n")
    w = weight(text)
    ok = w <= MAX_WEIGHT
    print(f"素の文字数 : {len(text)}")
    print(f"X重み      : {w} / {MAX_WEIGHT}")
    print(f"残り       : {MAX_WEIGHT - w}")
    print(f"判定       : {'[OK]' if ok else '[NG] 超過'}")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
