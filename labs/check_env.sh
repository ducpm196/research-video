#!/usr/bin/env bash
# Kiểm môi trường thực hành (labs/ENV.md). Chạy: bash labs/check_env.sh
ok=0; bad=0
chk() { # tên, lệnh lấy phiên bản, gợi ý khắc phục
  if command -v "${2%% *}" >/dev/null 2>&1 && out=$(eval "$2" 2>&1 | head -1) && [ -n "$out" ]; then echo "✔ $1: $out"; ok=$((ok+1)); else echo "✘ $1: không tìm thấy — $3"; bad=$((bad+1)); fi
}
chk "bash"    "bash --version"           "cài Git for Windows (kèm Git Bash) từ git-scm.com"
chk "git"     "git --version"            "cài Git for Windows từ git-scm.com"
chk "javac"   "javac -version"           "cài Temurin JDK 21 từ adoptium.net rồi mở lại Git Bash"
chk "java"    "java -version"            "cài Temurin JDK 21 từ adoptium.net rồi mở lại Git Bash"
chk "python"  "python --version"         "cài Python 3.11+ từ python.org (tick 'Add to PATH'); cần từ bài PYT"
chk "sqlite3" "sqlite3 --version"        "tải sqlite-tools từ sqlite.org, đặt sqlite3.exe vào PATH"
echo "— $ok đạt, $bad thiếu (docker chỉ cần từ chặng 7)"
[ $bad -eq 0 ]
