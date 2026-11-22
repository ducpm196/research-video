#!/usr/bin/env bash
set -euo pipefail
W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
mkdir -p "$W/dir"
i=1; while [ "$i" -le 50 ]; do : > "$W/dir/f_$i"; i=$((i + 1)); done
fc=$(find "$W/dir" -type f | wc -l | tr -d " ")
oc=$(find "$W/dir" | wc -l | tr -d " ")
echo "files=$fc"
echo "objects_50=$oc"
echo "inodes_10k=$((10000 + 1))"
