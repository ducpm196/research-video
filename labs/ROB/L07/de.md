# Lab ROB L07 — Đóng vòng đồ thị tư thế 1D phân bổ đều sai số trên 5 cạnh (4 đo + 1 đóng vòng)

Robot ghi nhận `5` tư thế thô `[0.0, 1.0, 2.0, 3.0, 4.0]` qua `4` cạnh đo quãng đường, và có thêm `1` cạnh đóng vòng nối từ gốc tới điểm cuối đo được `3.5 m` (tổng cộng `5` cạnh đồng trọng số). Chia đều độ lệch đóng vòng cho cả `5` cạnh để tính hiệu chỉnh mỗi cạnh và cập nhật các tư thế.
In đúng 1 dòng `edge_corr=... corrected_poses=[...]` (`edge_corr` lấy 3 chữ số `:.3f`, từng toạ độ làm tròn `round(..., 3)`).

Chấm tự động:
```bash
bash labs/cham.sh ROB L07 duong_dan/bai_cua_ban.py
```
