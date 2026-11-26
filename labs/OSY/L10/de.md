# Lab OSY L10 — Thay trang FIFO (nghịch lý Belady), LRU và OPT

Đọc `stdin` `seq=<int,...> c1=<int> c2=<int>`. Mô phỏng FIFO ở hai cỡ khung `c1, c2`, cùng LRU và OPT ở `c1` khung để đếm số lỗi trang.

In đúng 3 dòng (giữ nguyên tên khoá cố định `fifo_3, fifo_4, lru_3, opt_3` ứng với `c1` và `c2`): `fifo_3=<d> fifo_4=<d> belady=<0|1>`, `lru_3=<d>`, `opt_3=<d>`.
Chấm tự động: `bash labs/cham.sh OSY L10 duong_dan/bai_cua_ban.py`
