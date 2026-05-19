#!/usr/bin/env bash
for f in "$1"/*.md; do
  echo "=== $(basename "$f") ==="
  awk '/^---$/{c++; next} c==1' "$f"
  echo
done
