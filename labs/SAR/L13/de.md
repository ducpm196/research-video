# Lab SAR L13 — Quy đổi lưu lượng dòng thời gian bài đăng ngày

Đọc `stdin` `daily=<int> bytes=<int> peak_x=<int>` (quy ước hệ thập phân `1 GB = 10^9 byte`, `1 TB = 1000 GB`, lấy phần nguyên `//` cho `daily_gb`). Tính dung lượng GB ngày, tốc độ trung bình (`round(daily / 86400)`) & cao điểm TPS, và dung lượng TB cả năm (`365` ngày).

In 3 dòng: `daily_gb=<d>`, `avg_and_peak_tps=<avg>,<peak>`, `yearly_tb=<.1f>`.
Chấm tự động: `bash labs/cham.sh SAR L13 duong_dan/bai_cua_ban.py`
