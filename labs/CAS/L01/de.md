# Lab CAS L01 — Sai số nhị phân 24-bit tích lũy theo giờ

Đọc `stdin` `bits=<int> val=<float> hz=<int> h1=<int> h2=<int>`. Tính sai số chặt cụt ở thanh ghi chấm tĩnh với hệ số nhân `scale = 2 ** bits` (hoặc viết bằng phép dịch bit `1 << bits`) và độ trôi tích lũy sau `h1`, `h2` giờ.

In đúng 1 dòng: `drift_50h=<.4f> drift_100h=<.4f>`.
Gợi ý Python: `import sys; kv = dict(t.split('=') for t in sys.stdin.read().split())`; dùng `int(...)`/`float(...)`, `2 ** bits` (hoặc `1 << bits`), in `f"{x:.4f}"`.
Chấm tự động: `bash labs/cham.sh CAS L01 duong_dan/bai_cua_ban.py`
