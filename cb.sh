#!/bin/bash
# GPTレビュー用の最新の全文（operations/review-packs/ で一番新しいもの）をクリップボードに入れる。
# 使い方：bash cb.sh            … 一番新しいもの
#        bash cb.sh <名前の一部> … 名前に含むもので一番新しいもの
# 【2026-09-25】長いパスはアプリのターミナルで折り返して崩れるため、短いコマンドにした。
# 文字コードの設定（LANG）が空だと、pbcopy は日本語を黙って0字にする。UTF-8を指定し、入った字数を読み戻して確かめる。
export LANG=ja_JP.UTF-8 LC_CTYPE=UTF-8
cd "$(dirname "$0")" || exit 1
f=$(ls -t operations/review-packs/*${1:-}*.txt 2>/dev/null | head -1)
if [ -z "$f" ]; then echo "該当する全文がありません（operations/review-packs/）"; exit 1; fi
pbcopy < "$f"
want=$(wc -c < "$f" | tr -d ' '); got=$(pbpaste | wc -c | tr -d ' ')
if [ "$want" != "$got" ]; then echo "★クリップボードに入っていません（${want}バイト中${got}バイト）"; exit 1; fi
echo "クリップボードに入れました：$(basename "$f")（$(wc -m < "$f" | tr -d ' ')字）。ChatGPTで ⌘+V"
