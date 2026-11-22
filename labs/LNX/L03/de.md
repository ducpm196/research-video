# Lab LNX L03 — Tách luồng 1/2 và lọc lỗi 5xx bằng đường ống

Viết kịch bản Bash tách stdout (luồng 1) và stderr (luồng 2), tạo nhật ký 100 dòng có 12 lỗi 500 và 3 lỗi 503 rồi in đúng 3 dòng:
1. `stdout_ok=1`
2. `stderr_ok=1`
3. `err_5xx=15`

Chấm tự động:
```bash
bash labs/cham.sh LNX L03 duong_dan/bai_cua_ban.sh
```
