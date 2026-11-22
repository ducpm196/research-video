# Lab RBM L10 — So sánh sai số xác lập điều khiển P thuần và PI hội tụ về 0

Cho hệ bậc nhất `y' = -y + u` xuất phát `y(0) = 0`, tích phân đầu `integ(0) = 0`, mục tiêu `r = 1.0`. Tính sai số xác lập lý thuyết của khâu P thuần `u = K*(1 - y)` (`K = 3.0`). Sau đó mô phỏng `150` bước Euler tiến (`y += dt * (-y + u)`, `dt = 0.05`, tích luỹ `integ += err * dt`) cho bộ điều khiển PI (`Kp = 1.2, Ki = 1.5`).
In đúng 1 dòng `P_steady_err=... PI_final_err=...` (4 chữ số thập phân `:.4f`).

Chấm tự động:
```bash
bash labs/cham.sh RBM L10 duong_dan/bai_cua_ban.py
```
