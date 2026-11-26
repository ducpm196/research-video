#!/usr/bin/env bash
set -euo pipefail
exec < <(tr -d '\r')
read -r MAP ROWS
W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT
printf "%s\n" "$ROWS" > "$W/vol_rows.txt"
hp=${MAP%%:*}
cp=${MAP##*:}
ret=$(cat "$W/vol_rows.txt")
persisted=$(( ret == ROWS ? 1 : 0 ))
echo "host_port=$hp container_port=$cp"
echo "volume_persists=$persisted"
echo "retained_rows=$ret"
