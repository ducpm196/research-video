#!/usr/bin/env bash
# Kiểm môi trường thực hành (labs/ENV.md). Chạy: bash labs/check_env.sh
# Chạy THẬT lệnh hỏi phiên bản của từng công cụ (không chỉ dò tên: trên Windows, lối tắt Microsoft Store của Python vẫn "có tên" dù chưa cài)
# rồi so với phiên bản nhỏ nhất mà các lab cần (Java 21, Git 2.28 trở lên, sqlite 3.32 trở lên, Python 3.11 trở lên).
ok=0; bad=0
chk() { # tên, lệnh lấy phiên bản, phiên bản nhỏ nhất (rỗng = chỉ cần chạy được), gợi ý khắc phục
  local out v nho
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
chk "bash"    "bash --version"           "4.0"  "cài Git for Windows (kèm Git Bash) từ git-scm.com"
chk "git"     "git --version"            "2.28" "cài Git for Windows từ git-scm.com (cần 2.28 trở lên)"
chk "javac"   "javac --version"          "21"   "cài Temurin JDK 21 từ adoptium.net rồi mở lại Git Bash (cần bản JDK, 21 trở lên)"
chk "java"    "java --version"           "21"   "cài Temurin JDK 21 từ adoptium.net rồi mở lại Git Bash"
chk "python"  "python --version"         "3.11" "cài Python 3.11+ từ python.org (tick 'Add to PATH'); cần từ bài PYT"
chk "sqlite3" "sqlite3 --version"        "3.32" "BẮT BUỘC (bài FND 8 và 10): tải sqlite-tools-win-x64 từ sqlite.org, giải nén, chép sqlite3.exe vào thư mục bin trong thư mục cá nhân (tự tạo), mở lại Git Bash"
echo "— $ok đạt, $bad thiếu (docker chỉ cần từ chặng 7)"
[ $bad -eq 0 ]
