#!/usr/bin/env bash
# Chạy đủ cổng cho bài JV2: verify → gen → lint → render → lab_gate. Dùng: bash audit/jv2/gates.sh L01 [L02 ...]
cd "$(dirname "$0")/../.." || exit 2
export PYTHONIOENCODING=utf-8
PY=.venv/Scripts/python
for L in "$@"; do
  echo "=== $L"
  $PY -B audit/jv2/verify_jv2.py "$L" 2>&1 | grep -v "^PASS\|^JDK\|^checked_at" | head -20
  $PY -B audit/jv2/gen.py "$L" 2>&1 | tail -3
  $PY tools/lv.py lint lessons/jv2/${L}_*.yaml 2>&1 | grep -v "^\[PASS\]\|^checked_at" | head -30
  $PY tools/lv.py lint lessons/jv2/${L}_*.yaml 2>&1 | grep "ước lượng"
  $PY tools/lv.py render lessons/jv2/${L}_*.yaml 2>&1 | grep -v "^checked_at" | tail -8
done
$PY -B audit/review/lab_gate.py JV2 2>&1 | tail -5
