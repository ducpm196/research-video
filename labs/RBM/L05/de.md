# Lab RBM L05 — Giải động học ngược tay máy 2 khâu

Đọc `L1 L2 x y` từ stdin (ví dụ `1.0 1.0 1.2 0.9`). Kẹp `c2 = (x^2+y^2-L1^2-L2^2)/(2*L1*L2)` vào `[-1, 1]` để tránh sai số số học, giải hai nghiệm `(t1, t2)` tính theo độ và làm tròn 2 chữ số (`down` ứng với `t2 > 0`, `up` ứng với `t2 < 0`), rồi kiểm định lại bằng động học thuận.
In đúng 1 dòng `down=(t1, t2) up=(t1, t2) fk_match=0/1`.
