#!/usr/bin/env bash
# Cổng cuối phần cho cả 21 bài DMS (WP5). Không build/tts/asr/git. Chạy: bash audit/dms/af2/final_gates.sh > /tmp/dms_gates.txt
cd "$(dirname "$0")/../../.." || exit 1
export PYTHONIOENCODING=utf-8
PY=.venv/Scripts/python
echo "== lint 21 bài"
for f in lessons/dms/L*.yaml; do
  r=$($PY -B tools/lv.py lint "$f" 2>&1 | grep -E "^lint:")
  echo "$(basename "$f" .yaml | cut -c1-3) $r"
done
echo "== render 21 bài"
for f in lessons/dms/L*.yaml; do
  r=$($PY -B tools/lv.py render "$f" 2>&1 | grep -E "^render:")
  echo "$(basename "$f" .yaml | cut -c1-3) $r"
done
echo "== verify_dms"; $PY -B audit/dms/verify_dms.py 2>&1 | tail -2
echo "== lab_gate"; $PY -B audit/review/lab_gate.py DMS 2>&1 | tail -1
echo "== curriculum"; $PY -B tools/lv.py curriculum curriculum/dms.yaml 2>&1 | tail -2
echo "== graph"; $PY -B audit/check_curricula_graph.py 2>&1 | grep -E "chu trình|VER dẫn|ví dụ có chữ số"
echo "== e52"; $PY -B tests/test_e52.py 2>&1 | tail -1
echo "== screen_code"; $PY -B audit/review/screen_code.py check --course DMS 2>&1 | tail -2
echo "== arith_scan"; $PY -B audit/review/arith_scan.py 2>&1 | tail -1
echo "== xong"
