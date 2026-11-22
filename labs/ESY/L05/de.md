# Lab ESY L05 — Mô phỏng đáp ứng bậc thang của bộ lọc thông thấp số bậc nhất

Với hệ số lọc `alpha = 0.25` và đầu ra ban đầu `y = 0.0`, chạy `8` mẫu có đầu vào cố định `x = 1.0` theo công thức `y <- y + alpha * (x - y)`, rồi đối chiếu với công thức đóng `1 - (1 - alpha)^8`.
In đúng 1 dòng `y8=... closed_form=...` (4 chữ số).

Chấm tự động:
```bash
bash labs/cham.sh ESY L05 duong_dan/bai_cua_ban.py
```
