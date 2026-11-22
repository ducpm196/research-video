# Lab RBM L00 — Kiểm chứng ma trận quay 2D R(60°): tính R^T R = I và định thức det R

Lập ma trận quay 2D góc `theta = 60°` (`[[c, -s], [s, c]]`), quay vector `(2, 0)`, tính sai số trực giao lớn nhất của `R^T * R - I` và định thức `det = c^2 + s^2`.
In đúng 1 dòng theo mẫu `rot=(x, y) ortho_err=e det=d` (3 chữ số thập phân cho toạ độ và det, dạng `:.1e` cho `ortho_err`).

Chấm tự động:
```bash
bash labs/cham.sh RBM L00 duong_dan/bai_cua_ban.py
```
