# Lab DVO L08 — Mô phỏng 4 bước Expand-Contract đổi tên cột không downtime

Đọc `stdin` chuỗi `names=<n1,n2,...> backfill=<0|1>`. Chạy 4 pha (`expand_col`, `dual_write_backfill`, `switch_reads`, `drop_old_col`); chỉ chép giá trị sang cột mới `ho_ten` khi `backfill=1`. Khi chuyển đọc, đếm số bản ghi thiếu `ho_ten` (lỗi đọc trên khoá `downtime_s`).

In đúng 3 dòng: `steps_count=<d>`, `dual_write_synced=<0|1>`, `downtime_s=<d>`.
Chấm tự động: `bash labs/cham.sh DVO L08 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
