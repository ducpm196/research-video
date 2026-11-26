#!/usr/bin/env bash
set -euo pipefail
exec < <(tr -d '\r')
IFS='|' read -r ADDR COND BIND IV RT
wh=0
[ "$COND" = "service_healthy" ] && wh=1
echo "internal_addr=$ADDR"
echo "wait_healthy=$wh"
echo "max_detect_s=$((IV * RT))"
