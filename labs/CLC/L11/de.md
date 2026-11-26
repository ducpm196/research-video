# Lab CLC L11 — Rà phương án chuyển ứng dụng 3 tầng & 6 trụ cột

Đọc `stdin` `db_az=<int> az_av=<float> min_app=<int> max_app=<int>`. Với giả định các vùng sẵn sàng hỏng độc lập, tính độ sẵn sàng tầng dữ liệu đa vùng bằng `100 * (1 - (1 - az_av)^db_az)`, in biên co giãn `min_app,max_app`, đặt `spof_cleared=1` nếu `db_az >= 2` và `min_app >= 2` (ngược lại `0`), và in cố định `pillars=6` (6 trụ cột kiến trúc).

In 4 dòng: `multi_az_avail=<.6f>%`, `app_bounds=<min>,<max>`, `spof_cleared=<0|1>`, `pillars=6`.
Chấm tự động: `bash labs/cham.sh CLC L11 duong_dan/bai_cua_ban.py`
