#!/usr/bin/env bash
# Cổng cả khoá PYT (L00–L13): verify_pyt (mọi bài) → gen → lint từng bài → render từng bài → lab_gate PYT. In gọn.
cd "$(dirname "$0")/../.." || exit 2
export PYTHONIOENCODING=utf-8; PY=.venv/Scripts/python
echo "== verify_pyt (cả khoá)"; $PY -B audit/pyt/verify_pyt.py > /tmp/pyt_verify_all.txt 2>&1; grep -v "^PASS\|^Python 3.11:" /tmp/pyt_verify_all.txt | cut -c1-600
echo "== gen"; $PY -B audit/pyt/gen.py 2>&1 | grep -v "^ghi" | head
for f in lessons/pyt/L*.yaml; do
  b=$(basename "$f"); echo "== $b"
  $PY -B tools/lv.py lint "$f" 2>&1 | grep -E "FAIL|WARN|^lint:" | cut -c1-300
  $PY -B tools/lv.py render "$f" 2>&1 | grep -E "render:|\[FAIL\]" | cut -c1-200 | head -4
done
echo "== lab_gate"; $PY -B audit/review/lab_gate.py PYT 2>&1 | tail -4 | cut -c1-300
echo ALL_DONE
