#!/usr/bin/env bash
# AF5 nhóm D: lint đủ 777 bài (mỗi khoá một tiến trình) rồi screen_code riêng BNX. Chỉ đọc. Một bản duy nhất, chạy nền trực tiếp.
cd /d/research-video || exit 1
export PYTHONIOENCODING=utf-8
PY=.venv/Scripts/python
L=audit/review/audit_final/logs/af5
echo "START D $(date -u +%Y-%m-%dT%H:%M:%SZ) HEAD=$(git rev-parse --short HEAD)" > $L/summary_D.txt
: > $L/lint_all.out
for c in $(ls lessons); do $PY -B $L/lint_course.py $c >> $L/lint_all.out 2>&1 < /dev/null; echo "rc=$? $c" >> $L/lint_all.out; done
echo "== lint_all $(date -u +%H:%M:%SZ) | khoá: $(grep -c '^LINT ' $L/lint_all.out) | bài: $(grep '^LINT ' $L/lint_all.out | awk '{s+=$3} END{print s}') | FAIL: $(grep '^LINT ' $L/lint_all.out | awk '{s+=$5} END{print s}') | WARN: $(grep '^LINT ' $L/lint_all.out | awk '{s+=$7} END{print s}') | rc≠0: $(grep -c '^rc=[1-9]' $L/lint_all.out)" >> $L/summary_D.txt
for i in 1 2; do
  $PY -B audit/review/screen_code.py check --course BNX -v > $L/screen_code_bnx_run$i.out 2>&1 < /dev/null
  echo "== screen_code_bnx lần $i rc=$? $(date -u +%H:%M:%SZ) | $(grep '^screen_code:' $L/screen_code_bnx_run$i.out | tail -1 | cut -c1-200)" >> $L/summary_D.txt
done
echo "END D $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $L/summary_D.txt
