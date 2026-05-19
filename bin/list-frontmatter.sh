#!/usr/bin/env bash
[[ -d "$1" ]] || { echo "usage: list-frontmatter.sh <dir>" >&2; exit 2; }
shopt -s nullglob
for f in "$1"/*.md; do
  echo "=== $(basename "$f") ==="
  awk '/^---$/{c++; next} c==1' "$f"
  echo
done
