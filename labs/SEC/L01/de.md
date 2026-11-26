# Lab SEC L01 — PBKDF2-HMAC-SHA256 thật + tính thời gian vét cạn

Đọc `stdin` `pw=<str> salt=<str> iter=<int> alpha=<int> length=<int> fast=<float> slow=<float>`. Dẫn xuất khóa bằng `hashlib.pbkdf2_hmac('sha256', pw.encode(), salt.encode(), iters).hex()` (mặc định `dklen=32` cho 64 ký tự hex) và tính thời gian vét cạn `alpha**length / fast` giây, `alpha**length / slow / 86400` ngày.

In đúng 3 dòng: `fast_crack_s=<.1f>`, `slow_crack_days=<d>`, `pbkdf2_hex_len=<d>`.
Chấm tự động: `bash labs/cham.sh SEC L01 duong_dan/bai_cua_ban.py`
