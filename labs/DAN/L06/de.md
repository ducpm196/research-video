# Lab DAN L06 — Trung bình trượt 7 ngày khử mùa vụ cuối tuần

Đọc `stdin` `base=<int> slope=<int> bump=<int> days=<int>`. Tạo chuỗi `y[d] = base + slope*d + (bump nếu d%7 in (5,6))`, tính trung bình trượt 7 ngày và kiểm độ dốc có bằng `slope` không.

In 1 dòng: `ma7_diffs=<list3> constant_slope=<0|1>`.
Chấm tự động: `bash labs/cham.sh DAN L06 duong_dan/bai_cua_ban.py`

> Gợi ý đọc `stdin`: `kv = {k: int(v) for k, v in (t.split("=") for t in sys.stdin.read().split())}` rồi tạo chuỗi theo phần dư `d % 7 in (5, 6)`.
