# Lab DVO L08 — Mô phỏng 4 bước mở rộng–thu gọn (Expand-Contract) đổi tên cột ten -> ho_ten không downtime

Viết chương trình Python mô phỏng trình tự 4 bước mở rộng–thu gọn (Expand-Contract) trên danh sách 2 bản ghi `['An', 'Binh']`: B1 thêm cột mới, B2 ghi kép cả 2 cột + chép ngược dòng cũ, B3 chuyển sang đọc `ho_ten` (đếm số dòng thiếu `ho_ten` khi chuyển = `downtime_s`), B4 xoá cột cũ khi hết tham chiếu, in đúng 3 dòng:
1. `steps_count=4`
2. `dual_write_synced=1`
3. `downtime_s=0`

Chấm tự động:
```bash
bash labs/cham.sh DVO L08 duong_dan/bai_cua_ban.py
```
