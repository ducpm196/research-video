# Lab RBM L09 — Tính trị riêng và kiểm định ổn định hệ tuyến tính x' = Ax

Cho ma trận trạng thái `A = [[0, 1], [-6, -5]]`. Tính tổng đường chéo `A[0][0] + A[1][1]`, định thức `det(A)`, giải phương trình đặc trưng tìm hai trị riêng `(l1, l2)` theo thứ tự giảm dần `l1 >= l2` và kiểm tra cả hai đều âm (`stable=0/1`).
In đúng 1 dòng `eigs=(l1, l2) stable=0/1` (mỗi trị riêng lấy 1 chữ số thập phân `:.1f`).

Chấm tự động:
```bash
bash labs/cham.sh RBM L09 duong_dan/bai_cua_ban.py
```
