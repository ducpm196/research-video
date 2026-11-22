# Lab RBM L11 — Kiểm định điều kiện bước ổn định Euler trên x' = -8x

Với hệ `x' = -8x`, tính hệ số nhân mỗi bước Euler `g(h) = 1 - 8*h` tại `h = 0.30` (`g_030`, 2 chữ số `:.2f`), cùng giá trị sau `10` bước xuất phát từ `x0 = 1.0` ở cỡ bước phân kỳ `h = 0.30` (`x10_div`, 2 chữ số `:.2f`) và cỡ bước hội tụ `h = 0.05` (`x10_conv`, 5 chữ số `:.5f`).
In đúng 1 dòng `g_030=... x10_div=... x10_conv=...`.

Chấm tự động:
```bash
bash labs/cham.sh RBM L11 duong_dan/bai_cua_ban.py
```
