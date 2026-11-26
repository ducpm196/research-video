#!/usr/bin/env bash
# Kiểm môi trường thực hành (labs/ENV.md). Chạy: bash labs/check_env.sh
# Chạy THẬT lệnh hỏi phiên bản của từng công cụ rồi so với phiên bản nhỏ nhất mà các lab cần.
ok=0; bad=0; opt_ok=0; opt_bad=0
chk() { # bắt buộc (nhóm nền): tên, lệnh, phiên bản min, gợi ý
  local out v
  out=$(eval "$2" 2>&1 | head -3)
  v=$(printf '%s\n' "$out" | grep -oE '[0-9]+\.[0-9.]*[0-9]' | head -1)
  if [ -n "$v" ]; then
    if [ -z "$3" ] || [ "$(printf '%s\n%s\n' "$3" "$v" | sort -V | head -1)" = "$3" ]; then
      echo "✔ $1: $(printf '%s\n' "$out" | head -1)"; ok=$((ok+1)); return
    fi
    echo "✘ $1: phiên bản $v nhỏ hơn mức tối thiểu $3 — $4"; bad=$((bad+1)); return
  fi
  echo "✘ $1: không chạy được (chưa cài, hoặc chỉ là lối tắt mở cửa hàng ứng dụng) — $4"; bad=$((bad+1))
}
chk_opt() { # tuỳ chọn (nhóm theo chặng sau): tên, lệnh, phiên bản min, gợi ý
  local out v
  out=$(eval "$2" 2>&1 | head -3)
  v=$(printf '%s\n' "$out" | grep -oE '[0-9]+\.[0-9.]*[0-9]' | head -1)
  if [ -n "$v" ]; then
    if [ -z "$3" ] || [ "$(printf '%s\n%s\n' "$3" "$v" | sort -V | head -1)" = "$3" ]; then
      echo "✔ $1: $(printf '%s\n' "$out" | head -1)"; opt_ok=$((opt_ok+1)); return
    fi
    echo "• $1: phiên bản $v nhỏ hơn mức khuyến nghị $3 — $4"; opt_bad=$((opt_bad+1)); return
  fi
  echo "• $1: chưa có (chưa chặn nhóm nền) — $4"; opt_bad=$((opt_bad+1))
}

echo "=== Nhóm 1 · Nền (bắt buộc) ==="
chk "bash"    "bash --version"    "4.0"  "cài Git for Windows (kèm Git Bash) từ git-scm.com"
chk "git"     "git --version"     "2.28" "cài Git for Windows từ git-scm.com (cần 2.28 trở lên)"
chk "javac"   "javac --version"   "21"   "cài Temurin JDK 21 từ adoptium.net rồi mở lại Git Bash (cần bản JDK, 21 trở lên)"
chk "java"    "java --version"    "21"   "cài Temurin JDK 21 từ adoptium.net rồi mở lại Git Bash"
chk "python"  "python --version"  "3.11" "cài Python 3.11+ từ python.org (tick 'Add to PATH'); cần từ bài PYT"
chk "sqlite3" "sqlite3 --version" "3.32" "BẮT BUỘC (bài FND 8 và 10): tải sqlite-tools-win-x64 từ sqlite.org, giải nén, chép sqlite3.exe vào thư mục bin trong thư mục cá nhân (tự tạo), mở lại Git Bash"

echo "=== Nhóm 2 · C (Chặng 6 — CPR) ==="
GCC_CMD="gcc"; command -v gcc >/dev/null 2>&1 || { [ -x /c/tools/w64devkit/bin/gcc.exe ] && GCC_CMD="/c/tools/w64devkit/bin/gcc.exe"; }
chk_opt "gcc" "$GCC_CMD --version" "12.0" "cài w64devkit / gcc để biên dịch lab C"

echo "=== Nhóm 3 · JavaScript (Chặng 7 — WEB) ==="
chk_opt "node" "node --version" "18.0" "cài Node.js LTS để chạy lab JS"

echo "=== Nhóm 4 · Docker và SPB (từ khoá SPB — Chặng 3) ==="
chk_opt "docker" "docker --version" "24.0" "cài Docker Desktop (từ khoá SPB ở Chặng 3; tối thiểu 8 GB RAM)"

echo "=== Nhóm 5 · ML / dữ liệu (labs/.venv-pyt, labs/.venv-ml) ==="
PYT_PY="python"; [ -x "labs/.venv-pyt/Scripts/python.exe" ] && PYT_PY="labs/.venv-pyt/Scripts/python.exe"
ML_PY="python"; [ -x "labs/.venv-ml/Scripts/python.exe" ] && ML_PY="labs/.venv-ml/Scripts/python.exe"
chk_opt "numpy (.venv-pyt)" "$PYT_PY -c 'import numpy; print(numpy.__version__)'" "1.24" "cài labs/.venv-pyt bằng labs/requirements-py.txt"
chk_opt "sklearn (.venv-ml)" "$ML_PY -c 'import sklearn; print(sklearn.__version__)'" "1.4" "cài labs/.venv-ml bằng labs/requirements-ml.txt"

echo "— Nền: $ok đạt, $bad thiếu | Mở rộng: $opt_ok có, $opt_bad chưa có (docker cần từ khoá SPB ở Chặng 3)"
[ $bad -eq 0 ]
