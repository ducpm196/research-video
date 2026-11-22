# Lab RBM L08 — So sánh trực tiếp RK4 với Euler trên cùng bước h=0.2 giải x' = -x

Từ `x(0) = 1.0`, chạy `5` bước tới `t = 1.0` với `h = 0.2` theo cả Euler và RK4, đối chiếu với `exp(-1)` và tính tỉ lệ giảm sai số `err_euler / err_rk4`.
In đúng 1 dòng `err_euler=... err_rk4=... gain=...x` (`err_euler` lấy 4 chữ số thập phân `:.4f`, `err_rk4` dạng khoa học `:.2e`, `gain` làm tròn nguyên `:.0f`).

Chấm tự động:
```bash
bash labs/cham.sh RBM L08 duong_dan/bai_cua_ban.py
```
