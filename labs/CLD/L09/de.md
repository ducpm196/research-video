# Lab CLD L09 — Giảm đỉnh tải nhờ chọn tốt hơn trong hai (P2C)

Đọc `stdin` `seed=<int> reqs=<int> hosts=<int>`. Mô phỏng chọn ngẫu nhiên 1 máy (`rand1`) so với chọn máy ít tải hơn trong 2 lượt chọn ngẫu nhiên (`p2c`): dùng `random.Random(seed)`, gọi `randrange(hosts)` hai lần độc lập (cho phép trùng) và chỉ đổi sang máy thứ hai nếu tải máy thứ hai nhỏ hơn hẳn (`c[b] < c[a]`).

In 3 dòng: `max_rand1=<d>`, `max_p2c=<d>`, `p2c_better=<0|1>`.
Chấm tự động: `bash labs/cham.sh CLD L09 duong_dan/bai_cua_ban.py`
