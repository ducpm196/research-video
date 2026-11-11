#!/usr/bin/env bash
# Cổng cuối của đợt LF1 (cùng danh sách với LS1 `logs/verify_final.out`, thêm khoá BNX). Chạy từ gốc kho SAU khi mọi bài đã dựng xong:
#   docker start bnx-ora bnx-mss     # cổng screen_code của BNX chạy Oracle/SQL Server thật; thiếu container thì FAIL "NOT_VERIFIED"
#   bash audit/review/learn_full/final_gates.sh > audit/review/learn_full/logs/verify_final_lf1.out 2>&1
# Mỗi cổng in một dòng tổng; người đọc đối chiếu bằng mắt, không dựa vào mã thoát tổng.
cd /d/research-video || exit 1
export PYTHONIOENCODING=utf-8
PY=.venv/Scripts/python
run() { echo "== $1"; shift; "$@" 2>&1 | tail -${TAILN:-2}; }
run verify_jva         $PY -B audit/jva/verify_jva.py
run verify_bnk         $PY -B audit/bnk/verify_bnk.py
run verify_bnx         $PY -B audit/bnx/verify_bnx.py
run verify_cs112       $PY -B audit/cs112/verify_cs112.py
run verify_cs112_p2    $PY -B audit/cs112/verify_cs112_p2.py
run verify_plan_curricula $PY -B audit/verify_plan_curricula.py
run check_curricula_graph $PY -B audit/check_curricula_graph.py
run lv_curriculum_bnx  $PY -B tools/lv.py curriculum curriculum/bnx.yaml
run test_lint          $PY -B tests/test_lint.py
run check_xref         $PY -B audit/review/check_xref.py
run check_meta         $PY -B audit/review/check_meta.py
run check_course_refs  $PY -B audit/review/check_course_refs.py
run scan_ctrl          $PY -B audit/review/scan_ctrl.py
echo "== sync_tpl (CS112, DMS, CS115)"
for c in cs112 dms cs115; do $PY -B audit/review/sync_tpl_from_lesson.py $c 2>&1 | tail -1; done
run screen_code_all    $PY -B audit/review/screen_code.py check
run interview_sync     $PY -B audit/review/interview_sync_video.py --check
run asr_flags_BNX      $PY -B audit/review/asr_flags.py BNX
# Giải mã trọn 656 video cũ đã chạy sạch ở check_decode_all.out (2026-11-11 02:47→05:45) và KHÔNG tệp nào ngoài BNX đổi sau mốc bắt đầu (kiểm bằng find -newermt),
# nên ở đây giải mã lại BNX; cả kho vẫn kiểm cấu trúc (không --decode). Muốn giải mã lại cả kho: bỏ --course và thêm --decode ở dòng đầu (≈ 1–3 giờ).
echo "== pack.py check --decode --course BNX"
$PY -B audit/review/learn_start/pack.py check --decode --course BNX --tsv audit/review/learn_full/logs/check_decode_final_lf1.tsv 2>&1 | tail -3
echo "== pack.py check (toàn kho, không giải mã)"
$PY -B audit/review/learn_start/pack.py check 2>&1 | tail -3
run audit_all          $PY -B audit/review/audit_all.py
run status_report      $PY -B audit/review/status_report.py
run interview_gen_tables $PY -B audit/review/interview_gen_tables.py
run master_sections    $PY -B audit/review/learn_full/master_sections.py
run pack_page          $PY -B audit/review/learn_start/pack.py page
date -u +%Y-%m-%dT%H:%M:%SZ
