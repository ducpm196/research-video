# Lab MLO L08 — Giám sát trôi dữ liệu bằng chỉ số PSI

Đọc `stdin` `exp=<p1,p2,...> cur=<q1,q2,...>`. Tính chỉ số ổn định quần thể `PSI = sum((c - e) * ln(c / e))` và kiểm tra ngưỡng cảnh báo theo dõi `[0.1, 0.25)`.

In 1 dòng: `psi=<.3f> alert_moderate=<0|1>`.
Chấm tự động: `bash labs/cham.sh MLO L08 duong_dan/bai_cua_ban.py`
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
