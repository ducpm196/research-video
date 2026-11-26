# Lab RBM L02 — Quay vector bằng quaternion đơn vị

Đọc `half_deg x y z` từ stdin (ví dụ `30.0 1.0 2.0 0.0`). Dựng `q = (cos(half), 0, 0, sin(half))`, tính `||q||` và quay `(x, y, z)` bằng `q * v * q^-1`.
In đúng 1 dòng `norm_q=<3 chữ số> rotated=(rx, ry, rz)` (`round(..., 3)`).
