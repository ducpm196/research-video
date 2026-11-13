#!/usr/bin/env bash
# Chạy đủ cổng cho bài JVA: verify → gen → lint → render (→ lab_gate). Dùng: bash audit/jva/gates.sh L01 [L02 ...]
# Thêm biến SC=1 để chạy cả screen_code (chậm, ~2 phút): SC=1 bash audit/jva/gates.sh L01
cd "$(dirname "$0")/../.." || exit 2
export PYTHONIOENCODING=utf-8
PY=.venv/Scripts/python
for L in "$@"; do
  echo "=== $L"
  $PY -B audit/jva/verify_jva.py "$L" 2>&1 | grep -v "^PASS\|^JDK\|^checked_at" | head -20
  $PY -B audit/jva/gen.py "$L" 2>&1 | tail -3
  $PY tools/lv.py lint lessons/jva/${L}_*.yaml 2>&1 | grep -v "^\[PASS\]\|^checked_at" | head -30
  $PY - "$L" <<'EOF'
import sys, glob, yaml
d = yaml.safe_load(open(glob.glob(f"lessons/jva/{sys.argv[1]}_*.yaml")[0], encoding="utf-8"))
w = sum(len(s["say"].split()) for sc in d["scenes"] for s in sc["steps"])
p = sum(s.get("pause", 0) or 0 for sc in d["scenes"] for s in sc["steps"])
print(f"lời đọc: {w} từ ≈ {w / 176 + p / 60:.1f} phút video (176 từ/phút đo ở bản dựng cũ) (gồm {p}s dừng)")
EOF
  $PY tools/lv.py render lessons/jva/${L}_*.yaml 2>&1 | grep -v "^checked_at" | tail -8
done
$PY -B audit/review/lab_gate.py JVA 2>&1 | tail -3
if [ -n "$SC" ]; then
  $PY -B audit/jva/screen_hand.py 2>&1 | tail -8
  $PY -B audit/review/screen_code.py check --course jva 2>&1 | tail -8
fi
