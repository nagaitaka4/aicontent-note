#!/bin/bash
# 2026-09-28 から本体は ~/.local/bin/cb（どのフォルダからでも動く）。この cb.sh は互換のために残す。
exec "$HOME/.local/bin/cb" "$@"
