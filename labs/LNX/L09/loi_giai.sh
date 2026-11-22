#!/usr/bin/env bash
set -euo pipefail
cfg='cache:6379|service_healthy|0.0.0.0'
addr=${cfg%%|*}
wh=$(echo "$cfg" | grep -q 'service_healthy' && echo 1 || echo 0)
iv=2; rt=5
echo "internal_addr=$addr"
echo "wait_healthy=$wh"
echo "max_detect_s=$((iv * rt))"
