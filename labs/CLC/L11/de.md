# Lab CLC L11 — Rà phương án chuyển ứng dụng 3 tầng và kiểm tra 6 trụ cột

Phương án mục tiêu gồm: cơ sở dữ liệu đa vùng sẵn sàng (`db_az = 2`, mỗi AZ `99,9%`), tầng ứng dụng không giữ trạng thái co giãn trong khoảng `[3, 12]` máy, và đầy đủ `6` trụ cột kiến trúc tốt (`Vận hành`, `An toàn`, `Tin cậy`, `Hiệu năng`, `Chi phí`, `Bền vững`). Tính độ sẵn sàng mới của tầng dữ liệu và kiểm tra xem mọi điểm lỗi đơn (`SPOF`) đã được loại bỏ chưa.

Định dạng đầu ra (4 dòng):
`multi_az_avail=<6 chữ số>%`
`app_bounds=<min,max>`
`spof_cleared=<0|1>`
`pillars=<số>`

Chấm tự động:
```bash
bash labs/cham.sh CLC L11 duong_dan/bai_cua_ban.py
```
