# Lab CS115 L08 — Phân loại điểm dừng bằng định thức con

Cần: Python 3 (không cần thư viện ngoài), `from fractions import Fraction`. Tạo tệp `cuctri.py`. Bốn hàm bậc hai (số minh hoạ, khác ví dụ trong bài), mỗi hàm cho bởi Hessian `H = [[a, b], [b, c]]` (cố định) và vế phải `v` sao cho gradient bằng 0 khi `H nhân p = v` (p là điểm cần tìm):

```python
ham = {
    "f1": ([[2, 1], [1, 2]], [3, 0]),
    "f2": ([[2, -3], [-3, 2]], [0, 0]),
    "f3": ([[-2, 0], [0, -4]], [-4, 0]),
    "f4": ([[2, 2], [2, 2]], [2, 2]),
}
```

Với mỗi hàm theo thứ tự `f1`…`f4`:
1. Định thức con thứ nhất `m1 = a`, thứ hai `m2 = a*c - b*b`.
2. Nếu `m2` khác 0, giải `H nhân p = v` bằng công thức nghịch đảo 2 × 2 (dùng `Fraction`) để được điểm dừng `(x, y)`; nếu `m2` bằng 0 thì không có điểm dừng duy nhất.
3. Kết luận: `m1 > 0` và `m2 > 0` là `day`; `m1 < 0` và `m2 > 0` là `dinh`; `m2 < 0` là `yen ngua`; `m2 = 0` là `chua ket luan`.

In mỗi hàm một dòng, đúng dạng: `f1: diem dung (<x>, <y>), dinh thuc con: <m1> va <m2>, ket luan: <day|dinh|yen ngua|chua ket luan>`. Với hàm không có điểm dừng duy nhất, thay phần điểm dừng bằng `khong co diem dung duy nhat`, cho dòng dạng `f<k>: khong co diem dung duy nhat, dinh thuc con: <m1> va <m2>, ket luan: <...>`.

Chạy: `python cuctri.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L08 cuctri.py`.
