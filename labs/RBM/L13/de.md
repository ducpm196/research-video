# Lab RBM L13 — Lan truyền hiệp phương sai F*P*F^T trong lọc Kalman 2D

Cho ma trận hiệp phương sai ban đầu `P = [[2.0, 0.5], [0.5, 1.0]]` và ma trận chuyển trạng thái bước `h = 0.5`: `F = [[1.0, 0.5], [0.0, 1.0]]`. Hãy nhân đầy đủ `F * P * F^T` để lấy phương sai vị trí `P_00` và hiệp phương sai vị trí–vận tốc `P_01`.
In đúng 1 dòng `pred_var_pos=... cross_cov_pos_vel=...` (2 chữ số).

Chấm tự động:
```bash
bash labs/cham.sh RBM L13 duong_dan/bai_cua_ban.py
```
