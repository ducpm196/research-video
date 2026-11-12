#!/usr/bin/env bash
# Cổng giữa đợt LF2 (sau khi dựng lại 45 bài, TRƯỚC khi rà ASR và trước khi 8 bài CV có video). Chạy từ gốc kho:
#   bash audit/review/learn_final/gates_mid.sh > audit/review/learn_final/logs/gates_mid.out 2>&1
cd /d/research-video || exit 1
export PYTHONIOENCODING=utf-8
PY=.venv/Scripts/python
run() { echo "== $1"; shift; "$@" 2>&1 | tail -${TAILN:-3}; }
run checklib_import    bash -c "cd tools && ../.venv/Scripts/python -B -c 'import checklib; print(\"checklib ok\")'"
run verify_bnk         $PY -B audit/bnk/verify_bnk.py
run verify_bnx         $PY -B audit/bnx/verify_bnx.py
run check_xref         $PY -B audit/review/check_xref.py
run check_meta         $PY -B audit/review/check_meta.py
run check_course_refs  $PY -B audit/review/check_course_refs.py
run scan_ctrl          $PY -B audit/review/scan_ctrl.py
run check_curricula_graph $PY -B audit/check_curricula_graph.py
run sync_tpl_all       $PY -B audit/review/sync_tpl_from_lesson.py --all
run test_lint          $PY -B tests/test_lint.py
run interview_sync     $PY -B audit/review/interview_sync_video.py --check
for c in CSA OSY NET TOC PLC SWF SDP DBS DSC DSY WEB DVO CLD SEC BNK BNX; do run "asr_flags_$c" $PY -B audit/review/asr_flags.py $c; done
run pack_check         $PY -B audit/review/learn_start/pack.py check
TAILN=40 run audit_all $PY -B audit/review/audit_all.py
date -u +%Y-%m-%dT%H:%M:%SZ
