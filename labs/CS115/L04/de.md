# Lab CS115 L04 — Gram-Schmidt cho ba vector bằng Python

Cần: Python 3 (không cần thư viện ngoài), `from fractions import Fraction` để số đúng tuyệt đối. Tạo tệp `gs.py`. Vector viết bằng danh sách (số minh hoạ, khác ví dụ trong bài):

```python
x1, x2, x3 = [1, 1, 0], [1, 0, 1], [0, 1, 1]
y = [3, 2, 1]
```

1. Viết hàm `dot(u, v)`. Chạy Gram-Schmidt (chưa chuẩn hoá): `v1 = x1`; `v2 = x2` trừ cái bóng của `x2` trên `v1`; `v3 = x3` trừ cả hai cái bóng (trên `v1` và trên `v2`). Cái bóng của `x` trên `v` là `(dot(x, v) / dot(v, v))` nhân từng thành phần của `v`. In `v1 = ...`, `v2 = ...`, `v3 = ...` (từng số in bằng `str` của `Fraction`, ngăn bằng dấu phẩy và một khoảng trắng, đặt trong `[]`).
2. In `v1.v2 = ...`, `v1.v3 = ...`, `v2.v3 = ...` (cả ba phải bằng 0: phép thử vuông góc).
3. In `binh phuong do dai: [...]` (danh sách `dot(v, v)` của ba vector).
4. Vì `v1, v2, v3` vuông góc nhưng chưa dài 1, toạ độ của `y` theo bộ này là `dot(y, v) / dot(v, v)` cho từng `v`. In `toa do cua y: [...]`.

Chạy: `python gs.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L04 gs.py`.
