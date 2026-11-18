#!/usr/bin/env bash
# Cổng một bài PYT: bash audit/pyt/gates.sh L03   (verify → gen → lint → render → lab_gate); in gọn.
cd "$(dirname "$0")/../.." || exit 2
L="$1"; export PYTHONIOENCODING=utf-8; PY=.venv/Scripts/python
echo "== verify_pyt $L"; $PY -B audit/pyt/verify_pyt.py "$L" > /tmp/pyt_verify_$L.txt 2>&1; grep -v "^PASS\|checked_at\|^Python 3.11:" /tmp/pyt_verify_$L.txt | cut -c1-700
echo "== gen"; $PY -B audit/pyt/gen.py "$L" 2>&1 | tail -3
echo "== lint"; $PY -B tools/lv.py lint lessons/pyt/${L}_*.yaml 2>&1 | grep -E "FAIL|WARN|phút" | cut -c1-400
echo "== render"; $PY -B tools/lv.py render lessons/pyt/${L}_*.yaml 2>&1 | grep -E "render:|FAIL|vấn đề|tràn" | cut -c1-200 | head -8
echo "== lab_gate"; $PY -B audit/review/lab_gate.py PYT 2>&1 | tail -3 | cut -c1-400
