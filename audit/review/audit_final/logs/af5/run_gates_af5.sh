#!/usr/bin/env bash
# AF5 (rà chốt 2026-11-22): chạy lại toàn bộ cổng, mỗi cổng một nhật ký riêng + mã thoát. Chỉ đọc kho (trừ tệp tsv do cổng tự sinh).
# Chạy: bash audit/review/audit_final/logs/af5/run_gates_af5.sh A|B|C   (run_in_background trực tiếp, một bản duy nhất)
cd /d/research-video || exit 1
export PYTHONIOENCODING=utf-8
PY=.venv/Scripts/python
L=audit/review/audit_final/logs/af5
S=$L/summary_$1.txt
run() { n=$1; shift; t0=$(date -u +%H:%M:%SZ); "$@" > $L/$n.out 2>&1 < /dev/null; rc=$?; echo "== $n rc=$rc $t0→$(date -u +%H:%M:%SZ) | $(tail -1 $L/$n.out | cut -c1-220)" >> $S; }
echo "START $1 $(date -u +%Y-%m-%dT%H:%M:%SZ) HEAD=$(git rev-parse --short HEAD)" > $S
if [ "$1" = A ]; then
run check_xref        $PY -B audit/review/check_xref.py
run check_meta        $PY -B audit/review/check_meta.py
run check_course_refs $PY -B audit/review/check_course_refs.py
run check_next_refs   $PY -B audit/review/check_next_refs.py
run check_legal       $PY -B audit/review/check_legal.py
run arith_scan        $PY -B audit/review/arith_scan.py
run curricula_graph   $PY -B audit/check_curricula_graph.py
run plan_curricula    $PY -B audit/verify_plan_curricula.py
run test_lint         $PY -B tests/test_lint.py
run test_e52          $PY -B tests/test_e52.py
run scan_ctrl         $PY -B audit/review/scan_ctrl.py
run sync_tpl_all      $PY -B audit/review/sync_tpl_from_lesson.py --all
run interview_sync    $PY -B audit/review/interview_sync_video.py --check
run af2_cover         $PY -B audit/review/af2_cover.py --require S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11
run find_stale_all    $PY -B scratch/find_stale_all.py
run pack_check        $PY -B audit/review/learn_start/pack.py check
run tts_speed_scan    $PY -B audit/review/tts_speed_scan.py 0.22
run lab_gate          $PY -B audit/review/lab_gate.py
: > $L/asr_flags_all.out
for c in $(ls curriculum/*.yaml | xargs -n1 basename | sed 's/.yaml//' | grep -v tracks); do C=${c^^}; echo "## $C" >> $L/asr_flags_all.out; $PY -B audit/review/asr_flags.py $C >> $L/asr_flags_all.out 2>&1 < /dev/null; echo "rc=$?" >> $L/asr_flags_all.out; done
echo "== asr_flags_all done $(date -u +%H:%M:%SZ)" >> $S
fi
if [ "$1" = B ]; then
for v in audit/*/verify_*.py; do n=$(basename $v .py); run $n $PY -B $v; done
run screen_code_check $PY -B audit/review/screen_code.py check
fi
if [ "$1" = C ]; then
cp audit/review/audit_all.tsv $L/audit_all.before.tsv
cp audit/review/pedagogy_scan.tsv $L/pedagogy_scan.before.tsv
run pedagogy_scan     $PY -B audit/review/pedagogy_scan.py
run audit_all         $PY -B audit/review/audit_all.py
fi
echo "END $1 $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $S
