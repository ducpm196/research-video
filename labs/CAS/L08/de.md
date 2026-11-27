# Lab CAS L08 — Khoá an toàn hostname & thời gian truyền khôi phục

Đọc `stdin` `host=<str> target=<str> gb=<float> mbps=<float>`. Kiểm tra chặn thao tác xóa sai máy chủ và tính số giờ truyền bản chụp (`1 GB = 8000 Mb`).

In đúng 1 dòng: `aborted=<0|1> restore_hours=<.2f>`.
Gợi ý Python: `import sys; kv = dict(t.split('=') for t in sys.stdin.read().split())`; dùng `float(...)`, `gb * 8000 / mbps / 3600`, `f"{h:.2f}"`.
Chấm tự động: `bash labs/cham.sh CAS L08 duong_dan/bai_cua_ban.py`
