# Lab OSY L04 — Duyệt mọi xen kẽ hai luồng tăng x++ gây tranh chấp dữ liệu

Đọc `stdin` `incs=<int> x0=<int>` (mỗi trong 2 luồng chạy `incs` lần chuỗi 3 bước đọc–cộng–ghi `load, inc, store` trên `x` khởi tạo `x0`). Bắt đầu từ `(0, 0, 0, 0, x0)`, dùng một hàng đợi hoặc danh sách trạng thái chưa duyệt (cùng tập đã thăm) đi hết mọi trạng thái `(p0, p1, r0, r1, x)` đạt tới được, in tập giá trị `x` có thể đạt được khi kết thúc, biên nhỏ/lớn và cờ `1` nếu có giá trị nhỏ hơn `x0 + 2*incs`.

In đúng 3 dòng: `possible_x=<gia_tri_cach_nhau_dau_phay>`, `min_x=<d> max_x=<d>`, `valid_outcomes_lt4=<0|1>`.
Chấm tự động: `bash labs/cham.sh OSY L04 duong_dan/bai_cua_ban.py`
