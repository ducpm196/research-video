# Lab RBM L05 — Giải động học ngược tay máy 2 khâu L1=L2=1.0 bằng định lý cos và atan2

Cho `L1 = 1.0, L2 = 1.0` và điểm đích `(x, y) = (1.2, 0.9)`. Hãy tính hai cặp góc khớp `(t1, t2)` (khuỷu dưới `t2 > 0` và khuỷu trên `t2 < 0`) bằng định lý cos + `math.atan2`, rồi kiểm định lại bằng động học thuận xem cả hai có về đúng `(1.2, 0.9)`.
In đúng 1 dòng `down=(t1, t2) up=(t1, t2) fk_match=0/1` (góc theo độ, 2 chữ số).

Chấm tự động:
```bash
bash labs/cham.sh RBM L05 duong_dan/bai_cua_ban.py
```
