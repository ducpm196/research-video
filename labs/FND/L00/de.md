# Lab FND L00 — Kiểm máy bằng một tệp lệnh

Cài đủ công cụ theo bài (Git for Windows kèm Git Bash, JDK 21, Python 3.11+, sqlite hoặc dùng `labs/sqlrun.py`), **mở lại** Git Bash.

1. Tạo tệp `kiem.sh` với nội dung dưới đây (chép nguyên; bài L04 sẽ giải thích từng dòng):

```bash
for ten in bash git javac java python; do
  if command -v "$ten" >/dev/null; then echo "✔ $ten"
  else echo "THIEU $ten"; fi
done
if python -c "import sqlite3" 2>/dev/null; then echo "✔ sql"
else echo "THIEU sql"; fi
```

2. Chạy `bash kiem.sh`. Máy đạt khi in **đúng sáu dòng**, mỗi dòng bắt đầu bằng ✔ (xem `mong_doi.txt`).
3. Chấm: `bash labs/cham.sh FND L00 kiem.sh`. Dòng báo THIEU nghĩa là thiếu công cụ đó: cài, mở lại Git Bash, chạy lại.

Muốn xem phiên bản từng công cụ: `bash labs/check_env.sh`.
