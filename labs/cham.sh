#!/usr/bin/env bash
# Chấm một lab: bash labs/cham.sh <KHOÁ> <Lxx> <tệp>   — chạy tệp rồi so đầu ra với labs/<KHOÁ>/<Lxx>/mong_doi.txt
# Hỗ trợ: .java .py .sql .sh. In "ĐÚNG" hoặc phần khác nhau (diff). Mã thoát 0 = đúng.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K="${1:?thiếu KHOÁ}"; L="${2:?thiếu Lxx}"; F="${3:?thiếu tệp}"
EXP="$HERE/$K/$L/mong_doi.txt"
[ -f "$EXP" ] || { echo "không có $EXP"; exit 2; }
[ -f "$F" ] || { echo "không có tệp $F"; exit 2; }
W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
ABS="$(cd "$(dirname "$F")" && pwd)/$(basename "$F")"

# Chọn trình Python thật: trên Windows, "python3" thường là lối tắt Microsoft Store (in "Python was not found…") nên phải thử chạy --version.
pick_python() {
  local c
  for c in python python3 py; do
    if command -v "$c" >/dev/null 2>&1 && "$c" --version 2>&1 | grep -qE '^Python 3\.'; then echo "$c"; return 0; fi
  done
  return 1
}

case "$F" in
  *.java)
    CLS=$(grep -oE 'public[[:space:]]+(final[[:space:]]+)?class[[:space:]]+[A-Za-z_][A-Za-z0-9_]*' "$ABS" | head -1 | awk '{print $NF}')
    [ -n "$CLS" ] || { echo "không thấy 'public class Tên' trong $F"; exit 2; }
    cp "$ABS" "$W/$CLS.java"
    ( cd "$W" && javac -encoding UTF-8 "$CLS.java" 2>"$W/_err" && java -Dfile.encoding=UTF-8 "$CLS" >"$W/_out" 2>>"$W/_err" ) || { echo "LỖI khi biên dịch/chạy:"; cat "$W/_err"; exit 1; } ;;
  *.py)
    PY=$(pick_python) || { echo "không tìm thấy Python 3 (cài từ python.org, tick Add to PATH)"; exit 2; }
    ( cd "$W" && PYTHONIOENCODING=utf-8 "$PY" "$ABS" >"$W/_out" 2>"$W/_err" ) || { echo "LỖI khi chạy:"; cat "$W/_err"; exit 1; } ;;
  *.sql)
    if command -v sqlite3 >/dev/null 2>&1; then
      ( cd "$W" && sqlite3 :memory: <"$ABS" >"$W/_out" 2>"$W/_err" ) || { echo "LỖI khi chạy:"; cat "$W/_err"; exit 1; }
    else
      PY=$(pick_python) || { echo "không có sqlite3 và không tìm thấy Python 3"; exit 2; }
      ( cd "$W" && PYTHONIOENCODING=utf-8 "$PY" "$HERE/sqlrun.py" "$ABS" >"$W/_out" 2>"$W/_err" ) || { echo "LỖI khi chạy:"; cat "$W/_err"; exit 1; }
    fi ;;
  *.sh)  ( cd "$W" && bash "$ABS" >"$W/_out" 2>"$W/_err" ) || { echo "LỖI khi chạy:"; cat "$W/_err"; exit 1; } ;;
  *) echo "chưa hỗ trợ đuôi tệp này"; exit 2 ;;
esac
norm() { tr -d '\r' <"$1" | sed -e 's/[[:space:]]*$//' | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}'; }
if diff <(norm "$W/_out") <(norm "$EXP") >"$W/_diff"; then echo "ĐÚNG"; exit 0; fi
echo "KHÁC mong đợi (< của bạn, > mong đợi):"; cat "$W/_diff"; exit 1
