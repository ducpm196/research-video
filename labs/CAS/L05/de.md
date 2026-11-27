# Lab CAS L05 — Knight Capital: tốc độ lỗ và xác suất sót triển khai N máy

Đọc `stdin` `loss_m=<float> mins=<float> nodes=<int> p=<float>`. Tính tốc độ lỗ mỗi phút và xác suất ít nhất một máy trong `nodes` máy bị bỏ sót.

In đúng 1 dòng: `loss_per_min_M=<.1f> prob_any_miss=<.4f>`.
Gợi ý Python: `import sys; kv = dict(t.split('=') for t in sys.stdin.read().split())`; dùng `float`/`int`, `1 - (1 - p) ** nodes`, `f"{x:.1f}"` / `f"{y:.4f}"`.
Chấm tự động: `bash labs/cham.sh CAS L05 duong_dan/bai_cua_ban.py`
