# Lab ROB L05 — Tính ma trận Jacobian chuyển động cho lọc Kalman mở rộng (EKF)

Với quãng đi `vh = 2.0 m` và góc hướng hiện tại `theta = 30°`, tính cặp đạo hàm riêng vị trí theo hướng `dx/dtheta = -vh*sin(theta)` và `dy/dtheta = vh*cos(theta)`.
In đúng 1 dòng `jac_theta=(dx_dth, dy_dth)` (3 chữ số).

Chấm tự động:
```bash
bash labs/cham.sh ROB L05 duong_dan/bai_cua_ban.py
```
