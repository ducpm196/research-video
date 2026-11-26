#!/usr/bin/env bash
# Bộ cổng kiểm tra chuẩn AF5 (plan_AF5_20261123T0110Z.md mục 8.1 — 26 cổng).
# Dùng:
#   bash audit/review/audit_final/final_gates_af5.sh nhanh
#   bash audit/review/audit_final/final_gates_af5.sh day_du
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../../.." || exit 1
MODE="${1:-nhanh}"
if [ "$MODE" != "nhanh" ] && [ "$MODE" != "day_du" ]; then
    echo "Dùng: bash audit/review/audit_final/final_gates_af5.sh [nhanh|day_du]" >&2
    exit 2
fi
export PYTHONIOENCODING=utf-8
PY=".venv/Scripts/python"
FAIL_GATES=0

run_gate() {
    local num="$1"
    local name="$2"
    shift 2
    echo "== [$num] $name"
    local out rc
    set +e
    out="$("$@" 2>&1)"
    rc=$?
    set -e
    printf '%s\n' "$out" | tail -n "${TAILN:-5}"
    if [ "$rc" -ne 0 ]; then
        echo "!! GATE_FAIL [$num] $name (rc=$rc)"
        FAIL_GATES=$((FAIL_GATES + 1))
    fi
}

echo "=== final_gates_af5.sh ($MODE) @ $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

run_gate 1 "check_xref"           "$PY" -B audit/review/check_xref.py
run_gate 2 "check_meta"           "$PY" -B audit/review/check_meta.py
run_gate 3 "check_course_refs"    "$PY" -B audit/review/check_course_refs.py
run_gate 4 "check_next_refs"      "$PY" -B audit/review/check_next_refs.py
run_gate 5 "check_legal"          "$PY" -B audit/review/check_legal.py
run_gate 6 "arith_scan"           "$PY" -B audit/review/arith_scan.py
run_gate 7 "check_curricula_graph" "$PY" -B audit/check_curricula_graph.py
run_gate 8 "verify_plan_curricula" "$PY" -B audit/verify_plan_curricula.py

if [ "$MODE" = "day_du" ]; then
    echo "== [9] lv.py curriculum (50 khoá)"
    c_fail=0
    for cp in curriculum/*.yaml; do
        [ "$(basename "$cp")" = "tracks.yaml" ] && continue
        if ! "$PY" -B tools/lv.py curriculum "$cp" >/dev/null 2>&1; then
            echo "FAIL curriculum $cp"
            c_fail=$((c_fail + 1))
        fi
    done
    echo "lv_curriculum_all: $c_fail FAIL"
    [ "$c_fail" -eq 0 ] || FAIL_GATES=$((FAIL_GATES + 1))
fi

run_gate 10 "test_lint + test_e52" bash -c '"$1" -B tests/test_lint.py && "$1" -B tests/test_e52.py' _ "$PY"

echo "== [11] tests mới (check_xref, frozen, cham, content_gates)"
t_fail=0
for tf in tests/test_check_xref.py tests/test_frozen.py tests/test_content_gates.py; do
    [ -f "$tf" ] || continue
    if ! "$PY" -B "$tf"; then t_fail=$((t_fail + 1)); fi
done
if ! bash tests/test_cham.sh; then t_fail=$((t_fail + 1)); fi
[ "$t_fail" -eq 0 ] || FAIL_GATES=$((FAIL_GATES + 1))

run_gate 12 "scan_ctrl"            "$PY" -B audit/review/scan_ctrl.py
run_gate 13 "sync_tpl_from_lesson" "$PY" -B audit/review/sync_tpl_from_lesson.py --all
run_gate 14 "interview_sync_video" "$PY" -B audit/review/interview_sync_video.py --check
run_gate 15 "af2_cover S01..S11"   "$PY" -B audit/review/af2_cover.py --require S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11
run_gate 16 "find_stale_all"       "$PY" -B audit/review/find_stale_all.py

if [ "$MODE" = "day_du" ]; then
    run_gate 17 "pack check --decode" "$PY" -B audit/review/learn_start/pack.py check --decode
else
    run_gate 17 "pack check"          "$PY" -B audit/review/learn_start/pack.py check
fi

run_gate 18 "tts_speed_scan 0.22"  "$PY" -B audit/review/tts_speed_scan.py 0.22

if [ "$MODE" = "day_du" ]; then
    echo "== [19] asr_flags (tất cả khoá)"
    asr_fail=0
    for cp in curriculum/*.yaml; do
        [ "$(basename "$cp")" = "tracks.yaml" ] && continue
        c="$(basename "$cp" .yaml | tr '[:lower:]' '[:upper:]')"
        if ! "$PY" -B audit/review/asr_flags.py "$c" >/dev/null 2>&1; then
            echo "FAIL asr_flags $c"
            asr_fail=$((asr_fail + 1))
        fi
    done
    echo "asr_flags_all: $asr_fail FAIL"
    [ "$asr_fail" -eq 0 ] || FAIL_GATES=$((FAIL_GATES + 1))
fi

if [ -f audit/review/content_gates.py ]; then
    RATCHET_FILE="${AF5_RATCHET:-audit/review/audit_final/logs/af5_exec/content_gates_baseline.tsv}"
    if [ -f "$RATCHET_FILE" ]; then
        run_gate 20 "content_gates --ratchet" "$PY" -B audit/review/content_gates.py --ratchet "$RATCHET_FILE"
    else
        run_gate 20 "content_gates" "$PY" -B audit/review/content_gates.py
    fi
else
    echo "== [20] content_gates: CHUA CO (truoc WP-1)"
fi

if [ "$MODE" = "day_du" ]; then
    run_gate 21 "lab_gate" "$PY" -B audit/review/lab_gate.py
    echo "== [22] bộ kiểm từng khoá (verify_*.py)"
    v_fail=0
    v_cnt=0
    for vp in audit/*/verify_*.py audit/verify_cs115_*.py; do
        [ -f "$vp" ] || continue
        bn="$(basename "$vp")"
        [ "$bn" = "verify_spb.py" ] && continue
        [ "$bn" = "verify_l12_screen.py" ] && continue
        v_cnt=$((v_cnt + 1))
        if ! "$PY" -B "$vp" >/dev/null 2>&1; then
            echo "FAIL $vp"
            v_fail=$((v_fail + 1))
        fi
    done
    echo "verifiers_all: $((v_cnt - v_fail))/$v_cnt PASS, $v_fail FAIL"
    [ "$v_fail" -eq 0 ] || FAIL_GATES=$((FAIL_GATES + 1))

    run_gate 23 "screen_code check" "$PY" -B audit/review/screen_code.py check
    run_gate 24 "pedagogy_scan"     "$PY" -B audit/review/pedagogy_scan.py
    run_gate 25 "audit_all"         "$PY" -B audit/review/audit_all.py

    if [ -f audit/spb/verify_spb.py ]; then
        run_gate 26 "verify_spb" "$PY" -B audit/spb/verify_spb.py
    else
        echo "== [26] verify_spb: CHUA CO SPB"
    fi
fi

echo "=== final_gates_af5 ($MODE): $FAIL_GATES cổng FAIL ==="
[ "$FAIL_GATES" -eq 0 ]
