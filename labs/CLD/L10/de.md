# Lab CLD L10 — Dư địa công suất quyết định độ trễ hàng chờ

Đọc `stdin` `mu=<float> l1=<float> l2=<float>`. Tính độ trễ hàng chờ `W = 1000 / (mu - lam)` (ms) tại hai mức tải `l1` và `l2`.

In 2 dòng: `w_at_150=<.1f>ms`, `w_at_190=<.1f>ms`.
Gợi ý Python: `import sys; kv = dict(t.split('=') for t in sys.stdin.read().split())`; ép `float(...)` và in `f"{w:.1f}ms"`.
Chấm tự động: `bash labs/cham.sh CLD L10 duong_dan/bai_cua_ban.py`
