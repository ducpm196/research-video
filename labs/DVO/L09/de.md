# Lab DVO L09 — Tính chỉ số DORA: tần suất triển khai và trung vị Lead Time

Đọc `stdin` `deploys=<int> days=<int> leads=<t1,t2,...>`. Tính tần suất triển khai mỗi ngày, trung vị và trung bình cộng thời gian Lead Time.

In đúng 3 dòng: `deploy_per_day=<.2f>`, `lead_median_h=<d>`, `lead_mean_h=<.1f>`.
Chấm tự động: `bash labs/cham.sh DVO L09 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
