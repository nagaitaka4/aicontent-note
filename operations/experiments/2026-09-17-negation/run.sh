#!/bin/bash
# 使い方: run.sh <出力ファイル> <プロンプトファイル>
# ⚠️ リポジトリの外で実行する（リポジトリ内で起動するとCLAUDE.mdとルールが読み込まれ、条件がそろわない）
out="$1"; prompt="$2"
cd "/private/tmp/claude-501/-Users-nagaitakashi-Documents-GitHub-aicontent-note/4613b8ff-70ac-4901-9fbf-5e31d533288e/scratchpad/exp" || exit 1
claude -p "$(cat "$prompt")" --model opus --tools "" --no-session-persistence --output-format json < /dev/null 2>/dev/null \
 | python3 -c "import sys,json; d=json.load(sys.stdin); open(sys.argv[1],'w',encoding='utf-8').write(d.get('result','')); print(sys.argv[1].split('/')[-1], len(d.get('result','')), list((d.get('modelUsage') or {}).keys()))" "$out"
