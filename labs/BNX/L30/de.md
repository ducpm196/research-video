# Lab BNX L30 — Cầu dao nhỏ với đồng hồ giả

Viết `mau.py` cài **cầu dao ba trạng thái** `DONG` (đóng, cho gọi) → `MO` (mở, chặn) → `NUA_MO` (thử một cuộc) với **đồng hồ giả** (thời điểm `ms` truyền vào, không ngủ thật):

- ngưỡng: **2** cuộc hỏng liên tiếp thì mở; thời gian chờ ở trạng thái mở: **600 ms** (từ lúc mở tới lúc được thử lại);
- khi `MO` mà chưa đủ 600 ms: chặn (không gọi dịch vụ). Đủ 600 ms thì chuyển `NUA_MO` và cho gọi một cuộc: tốt → `DONG`, hỏng → `MO` (tính lại từ lúc đó);
- gọi mỗi 300 ms từ `ms = 0` tới `3000` (11 lần); dịch vụ hỏng khi `ms < 1500`, tốt từ `1500` trở đi.

In mỗi lần gọi `t=<ms> hong -> <trạng thái>` hoặc `t=<ms> tot -> <trạng thái>`, hoặc `t=<ms> chan` khi bị chặn; dòng cuối `goi that <a>, bi chan <b>`.
Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L30 mau.py`.
