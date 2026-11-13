#!/usr/bin/env bash
# Cổng đợt AF2 = cổng LF2 (final_gates.sh) + cổng mới. Chạy bằng `run_in_background` TRỰC TIẾP (không `nohup … &`), một bản duy nhất:
#   Get-CimInstance Win32_Process | ? CommandLine -match 'final_gates'   # phải rỗng trước khi chạy
#   bash audit/review/audit_final/final_gates_af2.sh > audit/review/audit_final/logs/gates_af2.out 2>&1
# Đọc từng dòng tổng; không tin mã thoát. Cần: docker start bnx-ora bnx-mss. Không chạy song song với dựng (tranh Docker/Redis làm BNX L19 chập chờn).
cd /d/research-video || exit 1
export PYTHONIOENCODING=utf-8
PY=.venv/Scripts/python
run() { echo "== $1"; shift; "$@" 2>&1 | tail -${TAILN:-3}; }
echo "== AF2 cổng mới"
run verify_fnd          $PY -B audit/fnd/verify_fnd.py
[ -f audit/jv2/verify_jv2.py ] && run verify_jv2 $PY -B audit/jv2/verify_jv2.py
run lab_gate            $PY -B audit/review/lab_gate.py
run arith_scan          $PY -B audit/review/arith_scan.py
run check_next_refs     $PY -B audit/review/check_next_refs.py
TAILN=6 run check_legal $PY -B audit/review/check_legal.py
echo "== LF2 cổng cũ (final_gates.sh)"
bash audit/review/learn_full/final_gates.sh
date -u +%Y-%m-%dT%H:%M:%SZ
