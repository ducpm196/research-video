# Lab DAN L04 — Phân tích giữ chân theo cohort

Đọc `stdin` `c1=<n0,m1,m2> c2=<n0,m1>`. Tính tỉ lệ giữ chân tháng 1, tháng 2 của nhóm 1, tháng 1 nhóm 2 và kiểm xem nhóm 2 có cải thiện hơn không.

In 2 dòng: `c1_m1=<.1f>% c1_m2=<.1f>%`, `c2_m1=<.1f>% improved=<0|1>`.
Chấm tự động: `bash labs/cham.sh DAN L04 duong_dan/bai_cua_ban.py`

> Gợi ý đọc `stdin`: `kv = dict(t.split("=") for t in sys.stdin.read().split())`, tách danh sách số bằng `.split(",")` và ép `int`.
