# Lab AGT L10 — Quan sát vết truy vết và gỡ lỗi theo Pareto

Đọc `stdin` `errs=<k1:v1,k2:v2,...> top=<k>`. Tính phần trăm của nguyên nhân `top` trên tổng số ca lỗi.

In 1 dòng: `top_cause_pct=<.1f>% total=<d>`.
Chấm tự động: `bash labs/cham.sh AGT L10 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
