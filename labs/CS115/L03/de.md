# Lab CS115 L03 — Khử Gauss: một nghiệm, vô nghiệm hay vô số nghiệm?

Cần: Python 3 (không cần thư viện ngoài; nên dùng `from fractions import Fraction` để khử không bị sai số). Tạo tệp `khu.py`.

Mỗi hệ viết bằng ma trận mở rộng (3 ẩn x, y, z; cột cuối là vế phải; số minh hoạ, khác ví dụ trong bài):

```python
he1 = [[2, 1, -1, 6], [1, 3, 2, 3], [1, 0, -2, 4]]
he2 = [[1, 2, 3, 4], [2, 4, 6, 9], [1, 0, 1, 1]]
he3 = [[1, 2, 3, 4], [2, 4, 6, 8], [1, 0, 1, 1]]
```

Viết hàm khử về dạng bậc thang (đổi chỗ hàng khi số trụ bằng 0), đếm hạng của ma trận hệ số A (3 cột đầu) và hạng của ma trận mở rộng (cả 4 cột), rồi với mỗi hệ in một dòng:

`he <k>: hang A=<r>, hang mo rong=<r'>, <kết luận>`

kết luận là `nghiem duy nhat x=<x>, y=<y>, z=<z>` (hạng bằng số ẩn; thế ngược), hoặc `vo nghiem` (hạng A nhỏ hơn hạng mở rộng), hoặc `vo so nghiem` (hai hạng bằng nhau nhưng nhỏ hơn số ẩn). Nghiệm in đúng dạng số nguyên hoặc phân số `a/b`.

Chạy: `python khu.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L03 khu.py`.
