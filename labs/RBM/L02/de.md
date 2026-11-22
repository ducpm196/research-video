# Lab RBM L02 — Quay vector bằng quaternion đơn vị và kiểm chuẩn độ dài ||q|| = 1

Dựng quaternion đơn vị `q = (cos 30°, 0, 0, sin 30°)` (quay `60°` quanh trục `z`), kiểm tra độ dài chuẩn `||q||` và quay vector `(1, 2, 0)` bằng `q * (0, x, y, z) * q^-1` (trong đó nghịch đảo `q^-1` giữ phần thực và đổi dấu ba thành phần vector `i, j, k`).
In đúng 1 dòng `norm_q=... rotated=(x, y, z)` (`norm_q` lấy 3 chữ số thập phân `:.3f`, từng toạ độ trong `rotated` dùng `round(..., 3)`).

Chấm tự động:
```bash
bash labs/cham.sh RBM L02 duong_dan/bai_cua_ban.py
```
