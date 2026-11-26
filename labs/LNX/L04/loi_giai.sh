#!/usr/bin/env bash
set -euo pipefail
exec < <(tr -d '\r')
read -r NF SCALE
W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
mkdir -p "$W/dir"
i=1; while [ "$i" -le "$NF" ]; do : > "$W/dir/f_$i"; i=$((i + 1)); done
fc=$(find "$W/dir" -type f | wc -l | tr -d " ")
oc=$(find "$W/dir" | wc -l | tr -d " ")
echo "files=$fc"
echo "objects=$oc"
echo "inodes_scale=$((SCALE + 1))"
