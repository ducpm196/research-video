# Lab OSY L04 — Duyệt mọi xen kẽ hai luồng tăng x++ gây race condition

Đọc `stdin` `incs=<int> x0=<int>` (mỗi trong 2 luồng chạy `incs` lần chuỗi 3 bước `load, inc, store` trên `x` khởi tạo `x0`). Duyệt DFS theo trạng thái `(p0, p1, r0, r1, x)` mọi chuỗi xen kẽ hợp lệ, in tập giá trị `x` có thể đạt được, biên nhỏ/lớn và cờ `1` nếu có giá trị nhỏ hơn `x0 + 2*incs`.

In đúng 3 dòng: `possible_x=<csv>`, `min_x=<d> max_x=<d>`, `valid_outcomes_lt4=<0|1>`.
Chấm tự động: `bash labs/cham.sh OSY L04 duong_dan/bai_cua_ban.py`
