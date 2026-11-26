#!/usr/bin/env bash
# Chấm tự động lab của một bài học (tương thích v1 + v2 theo labs/CONTRACT.yaml).
# Hỗ trợ: .c .java .py .sql .sh .js .md, chế độ tep (có/không ca_an/), du_an (kiem/), giay (bang_kiem.md).
# Dùng:
#   bash labs/cham.sh <thư_mục_lab> [tệp_lời_giải | --du-an <thư_mục_dự_án>]
#   bash labs/cham.sh <KHOÁ> <Lxx> [tệp_lời_giải | --du-an <thư_mục_dự_án>]   (kiểu gọi v1)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARG1="${1:?Thieu thu muc lab hoac ma khoa (vd: labs/PYT/L00 hoac PYT L00)}"
if [ ! -d "$ARG1" ] && [ -n "${2:-}" ] && [ -d "$ROOT/labs/$ARG1/$2" ]; then
    LAB="$ROOT/labs/$ARG1/$2"
    SUB="${3:-}"
    ARG_EXTRA="${4:-}"
else
    LAB="$ARG1"
    SUB="${2:-}"
    ARG_EXTRA="${3:-}"
fi

DU_AN_FLAG=0
if [ "$SUB" = "--du-an" ]; then
    DU_AN_FLAG=1
    SUB="${ARG_EXTRA:?Thieu thu muc du an sau --du-an}"
fi

if [ ! -d "$LAB" ]; then
    echo "Khong thay thu muc lab: $LAB" >&2
    exit 2
fi
LAB="$(cd "$LAB" && pwd)"

if [ -x "$ROOT/.venv/Scripts/python.exe" ]; then
    BASE_PY="$ROOT/.venv/Scripts/python.exe"
elif command -v python3 >/dev/null 2>&1; then
    BASE_PY="python3"
else
    BASE_PY="python"
fi

if [ -z "$SUB" ]; then
    if [ -d "$LAB/loi_giai" ]; then
        SUB="$LAB/loi_giai"
        DU_AN_FLAG=1
    else
        for f in "$LAB"/loi_giai.*; do
            [ -f "$f" ] && { SUB="$f"; break; }
        done
    fi
fi

if [ -z "$SUB" ] || { [ ! -f "$SUB" ] && [ ! -d "$SUB" ]; }; then
    echo "Khong tim thay bai lam / loi giai trong $LAB" >&2
    exit 2
fi

if [ -d "$SUB" ]; then
    DU_AN_FLAG=1
    SUB="$(cd "$SUB" && pwd)"
else
    SUB="$(cd "$(dirname "$SUB")" && pwd)/$(basename "$SUB")"
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Sai số tuỳ chọn cho phép so số thực (mặc định 0 = khớp nguyên văn từng dòng)
SAI_SO="${CHAM_SAI_SO:-0}"
if [ -f "$LAB/sai_so.txt" ]; then
    SAI_SO="$(tr -d ' \r\n' < "$LAB/sai_so.txt")"
fi

if [ "$DU_AN_FLAG" -eq 1 ]; then
    KIEM="$LAB/kiem"
    if [ ! -d "$KIEM" ] && [ ! -f "$SUB/pom.xml" ]; then
        echo "Thieu thu muc kiem trong $LAB" >&2
        exit 2
    fi
    if [ -f "$KIEM/chay_kiem.sh" ]; then
        bash "$KIEM/chay_kiem.sh" "$SUB" "$KIEM"
        echo "ĐÚNG — PASS $LAB (du_an script)"
        exit 0
    elif [ -f "$SUB/pom.xml" ]; then
        cp -R "$SUB"/. "$TMP/proj"
        [ -d "$KIEM" ] && cp -R "$KIEM"/. "$TMP/proj/"
        CHAY_CMD=""
        if [ -f "$LAB/chay.txt" ]; then
            CHAY_CMD="$(tr -d '\r' < "$LAB/chay.txt")"
        fi
        if [ -n "$CHAY_CMD" ]; then
            (cd "$TMP/proj" && eval "$CHAY_CMD")
        elif [ -x "$TMP/proj/mvnw" ] || [ -f "$TMP/proj/mvnw" ]; then
            (cd "$TMP/proj" && chmod +x mvnw && ./mvnw -B verify)
        else
            (cd "$TMP/proj" && mvn -B verify)
        fi
        "$BASE_PY" -X utf8 "$ROOT/labs/kiem_ham.py" --xml "$TMP/proj/target/surefire-reports" --kiem "$KIEM" --mong-doi "$LAB/mong_doi.txt"
        echo "ĐÚNG — PASS $LAB (du_an maven)"
        exit 0
    else
        "$BASE_PY" -X utf8 "$ROOT/labs/kiem_ham.py" --py-du-an "$SUB" "$KIEM"
        echo "ĐÚNG — PASS $LAB (du_an python)"
        exit 0
    fi
fi

# Chế độ bài giấy (.md)
if [[ "$SUB" == *.md ]]; then
    CHK="$LAB/bang_kiem.md"
    [ -f "$CHK" ] || CHK="$LAB/mong_doi.txt"
    "$BASE_PY" -X utf8 "$ROOT/labs/kiem_ham.py" --giay "$SUB" "$CHK"
    echo "ĐÚNG — PASS $LAB (giay)"
    exit 0
fi

EXT="${SUB##*.}"
EXT_LC="$(printf '%s' "$EXT" | tr '[:upper:]' '[:lower:]')"
PY_BIN="$BASE_PY"
JAVA_CLS=""
C_BIN=""

# Biên dịch một lần trước khi chạy ca công khai và các ca ẩn
case "$EXT_LC" in
    py)
        if grep -Eq '^\s*(import|from)\s+(sklearn|scipy|torch)\b' "$SUB" 2>/dev/null && [ -x "$ROOT/labs/.venv-ml/Scripts/python.exe" ]; then
            PY_BIN="$ROOT/labs/.venv-ml/Scripts/python.exe"
        elif grep -Eq '^\s*(import|from)\s+(numpy|pandas|matplotlib|pytest)\b' "$SUB" 2>/dev/null && [ -x "$ROOT/labs/.venv-pyt/Scripts/python.exe" ]; then
            PY_BIN="$ROOT/labs/.venv-pyt/Scripts/python.exe"
        fi
        ;;
    c)
        C_BIN="$TMP/prog"
        gcc -O2 -Wall "$SUB" -o "$C_BIN" -lm
        ;;
    java)
        mkdir -p "$TMP/j"
        JAVA_CLS="$(sed -n 's/.*public[[:space:]]\+class[[:space:]]\+\([A-Za-z_][A-Za-z0-9_]*\).*/\1/p' "$SUB" | head -n1)"
        [ -z "$JAVA_CLS" ] && JAVA_CLS="$(basename "$SUB" .java)"
        cp "$SUB" "$TMP/j/$JAVA_CLS.java"
        javac -encoding UTF-8 "$TMP/j/$JAVA_CLS.java"
        ;;
    sql|sh|js)
        ;;
    *)
        echo "Khong ho tro dinh dang: .$EXT" >&2
        exit 2
        ;;
esac

run_one() {
    local in_file="$1"
    local out_file="$2"
    local args_file="${3:-}"
    local extra_args=()
    if [ -n "$args_file" ] && [ -f "$args_file" ]; then
        while IFS= read -r tok; do
            [ -n "$tok" ] && extra_args+=("$tok")
        done < <(tr -d '\r' < "$args_file")
    fi
    rm -rf "$TMP/work" && mkdir -p "$TMP/work"
    case "$EXT_LC" in
        py)   (cd "$TMP/work" && PYTHONIOENCODING=utf-8 "$PY_BIN" -X utf8 "$SUB" "${extra_args[@]}" < "$in_file" > "$out_file") ;;
        c)    (cd "$TMP/work" && "$C_BIN" "${extra_args[@]}" < "$in_file" > "$out_file") ;;
        java) (cd "$TMP/work" && java -Dfile.encoding=UTF-8 -cp "$TMP/j" "$JAVA_CLS" "${extra_args[@]}" < "$in_file" > "$out_file") ;;
        sql)
            local sql_src="$SUB"
            if [ -f "$LAB/khoi_tao.sql" ]; then
                cat "$LAB/khoi_tao.sql" "$SUB" > "$TMP/sql_run.sql"
                sql_src="$TMP/sql_run.sql"
            fi
            if command -v sqlite3 >/dev/null 2>&1; then
                (cd "$TMP/work" && sqlite3 < "$sql_src" > "$out_file")
            else
                (cd "$TMP/work" && PYTHONIOENCODING=utf-8 "$BASE_PY" -X utf8 "$ROOT/labs/sqlrun.py" "$sql_src" < "$in_file" > "$out_file")
            fi
            ;;
        sh)   (cd "$TMP/work" && bash "$SUB" "${extra_args[@]}" < "$in_file" > "$out_file") ;;
        js)   (cd "$TMP/work" && node "$SUB" "${extra_args[@]}" < "$in_file" > "$out_file") ;;
    esac
}

compare_one() {
    local got_f="$1"
    local want_f="$2"
    local tag="$3"
    if [ "$SAI_SO" = "0" ] || [ "$SAI_SO" = "0.0" ]; then
        tr -d '\r' < "$got_f" | sed 's/[[:space:]]*$//' | awk '{a[NR]=$0} END{while(NR>0 && a[NR]=="") NR--; for(i=1;i<=NR;i++) print a[i]}' > "$TMP/g.norm"
        tr -d '\r' < "$want_f" | sed 's/[[:space:]]*$//' | awk '{a[NR]=$0} END{while(NR>0 && a[NR]=="") NR--; for(i=1;i<=NR;i++) print a[i]}' > "$TMP/w.norm"
        if diff -u "$TMP/w.norm" "$TMP/g.norm" > "$TMP/diff.txt"; then
            return 0
        fi
        echo "FAIL $LAB ($tag):" >&2
        head -n 20 "$TMP/diff.txt" >&2
        return 1
    else
        if ! "$BASE_PY" -X utf8 "$ROOT/labs/kiem_ham.py" --so "$got_f" "$want_f" --sai-so "$SAI_SO"; then
            echo "FAIL $LAB ($tag)" >&2
            return 1
        fi
        return 0
    fi
}

IN_PUB="$LAB/du_lieu.txt"
[ -f "$IN_PUB" ] || IN_PUB="/dev/null"
run_one "$IN_PUB" "$TMP/got_pub.txt"
compare_one "$TMP/got_pub.txt" "$LAB/mong_doi.txt" "cong_khai"

CA_COUNT=0
if [ -f "$LAB/ca_an/ham.json" ] && [ "$EXT_LC" = "py" ]; then
    "$PY_BIN" -X utf8 "$ROOT/labs/kiem_ham.py" --ham-json "$SUB" "$LAB/ca_an/ham.json"
    CA_COUNT=$((CA_COUNT + 1))
fi

shopt -s nullglob
HIDDEN_INS=("$LAB"/ca_an/*.in)
IN_TXTS=("$LAB"/ca_an/in_*.txt)
SEEDS=("$LAB"/ca_an/seed_*.sql)
shopt -u nullglob
for hin in "${HIDDEN_INS[@]}"; do
    hout="${hin%.in}.out"
    if [ ! -f "$hout" ]; then
        echo "FAIL $LAB (thieu tep mong doi an: $hout)" >&2
        exit 1
    fi
    run_one "$hin" "$TMP/got_hid.txt"
    compare_one "$TMP/got_hid.txt" "$hout" "ca_an/$(basename "$hin")"
    CA_COUNT=$((CA_COUNT + 1))
done
for tin in "${IN_TXTS[@]}"; do
    base="$(basename "$tin" .txt)"
    k="${base#in_}"
    tout="$LAB/ca_an/out_${k}.txt"
    if [ ! -f "$tout" ]; then
        echo "FAIL $LAB (thieu tep mong doi an: $tout)" >&2
        exit 1
    fi
    run_one "$tin" "$TMP/got_hid.txt" "$LAB/ca_an/args_${k}.txt"
    compare_one "$TMP/got_hid.txt" "$tout" "ca_an/$(basename "$tin")"
    CA_COUNT=$((CA_COUNT + 1))
done
for sin in "${SEEDS[@]}"; do
    base="$(basename "$sin" .sql)"
    k="${base#seed_}"
    sout="$LAB/ca_an/out_${k}.txt"
    if [ ! -f "$sout" ]; then
        echo "FAIL $LAB (thieu tep mong doi an: $sout)" >&2
        exit 1
    fi
    cat "$sin" "$SUB" > "$TMP/seed_merged.sql"
    if command -v sqlite3 >/dev/null 2>&1; then
        sqlite3 < "$TMP/seed_merged.sql" > "$TMP/got_hid.txt"
    else
        PYTHONIOENCODING=utf-8 "$BASE_PY" -X utf8 "$ROOT/labs/sqlrun.py" "$TMP/seed_merged.sql" > "$TMP/got_hid.txt"
    fi
    compare_one "$TMP/got_hid.txt" "$sout" "ca_an/$(basename "$sin")"
    CA_COUNT=$((CA_COUNT + 1))
done

echo "ĐÚNG — PASS $LAB (${CA_COUNT} ca an)"
