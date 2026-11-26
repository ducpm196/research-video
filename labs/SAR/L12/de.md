# Lab SAR L12 — Quy mô QPS đọc/ghi và dung lượng 5 năm cho URL Shortener

Đọc `stdin` `monthly=<int> ratio=<int> rec_b=<int>` (quy ước `1 tháng = 30 ngày = 2 592 000 giây`, `1 TB = 10^12 byte`). Tính tốc độ ghi QPS, tốc độ đọc tương ứng (làm tròn `round(...)`) và tổng TB lưu trữ 5 năm (`60` tháng).

In 3 dòng: `write_qps=<.1f>`, `read_qps=<d>`, `storage_5yr_tb=<.1f>`.
Chấm tự động: `bash labs/cham.sh SAR L12 duong_dan/bai_cua_ban.py`
