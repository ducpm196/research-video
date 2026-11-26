# Lab MLO L02 — Phiên bản hoá dữ liệu bằng mã băm SHA-256

Đọc `stdin` `v1=<str>` (dòng 1) và `v2=<str>` (dòng 2, `\n` thành xuống dòng). Lấy 12 ký tự đầu SHA-256 cho mỗi bản và kiểm tra khác nhau.

In 1 dòng: `h1=<hex12> h2=<hex12> changed=<0|1>`.
Chấm tự động: `bash labs/cham.sh MLO L02 duong_dan/bai_cua_ban.py`
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
