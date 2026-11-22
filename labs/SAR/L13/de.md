# Lab SAR L13 — Quy đổi lưu lượng dòng thời gian 800 triệu bài đăng mỗi ngày

Tính dung lượng thô mỗi ngày khi hệ thống nhận `800 000 000` bài đăng (`tweet`) ngắn, mỗi bài `250 byte` (tính theo `1 GB = 10^9 byte`, `1 TB = 1000 GB`), cùng tốc độ trung bình mỗi giây (`avg_tps`), tốc độ cao điểm hệ số `3x` (tính từ `avg_tps` chưa làm tròn rồi làm tròn bằng `round()` cả `avg` và `peak`) và tổng dung lượng thô sau `1` năm (`365` ngày).

Định dạng đầu ra (3 dòng):
`daily_gb=<số>`
`avg_and_peak_tps=<avg,peak>`
`yearly_tb=<1 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh SAR L13 duong_dan/bai_cua_ban.py
```
