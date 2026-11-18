# Lab DMS L13 — Số học mô-đun và thuật toán Euclid mở rộng bằng chương trình

Viết `modun.py` (Python 3.11 trở lên); chạy: `python modun.py`.

In đúng bảy dòng (không dấu):
1. `gcd(462, 1071) = <số>` — ước chung lớn nhất bằng thuật toán Euclid (vòng `while`, thay `(a, b)` bằng `(b, a % b)` tới khi `b` bằng 0)
2. `he so Bezout (x, y) thoa 462x + 1071y = 21: <dung|sai>` — tìm `x`, `y` nguyên bằng Euclid mở rộng (đi ngược các dòng chia), rồi KIỂM `462*x + 1071*y == 21` và in `dung` nếu thoả (không in giá trị x, y vì có nhiều cặp đúng)
3. `-17 mod 5 = <số>` — số dư không âm của −17 khi chia cho 5 (toán học cho kết quả trong 0..4)
4. `(123456789 * 987654321) mod 1000: <a> <b>` — `a` là số dư của TÍCH đầy đủ, `b` là số dư của (tích hai số dư của từng thừa số) — hai số phải bằng nhau
5. `1000 ngay nua tu thu Ba la thu <tên>` — tên ngày đánh số thứ Hai = 0, ..., Chủ nhật = 6 (viết `Hai`, `Ba`, `Tu`, `Nam`, `Sau`, `Bay`, `CN`), tính bằng số dư khi chia cho 7
6. `so buoc Euclid cua (832040, 514229): <số>` — số lần chia lấy dư cho tới khi số dư bằng 0
7. `7x = 3 (mod 30): x = <số>` — số x trong 0..29 thoả `(7*x) % 30 == 3` (duyệt từng x)

Gợi ý cho dòng 2 (Euclid mở rộng bằng vòng lặp, không cần đệ quy). Mỗi lần chia ta giữ hai số `a`, `b` kèm cách viết chúng dưới dạng `A*x + B*y` (A, B là hai số đề cho): `a = A*x0 + B*y0` và `b = A*x1 + B*y1`. Lúc đầu `a = A` nên `(x0, y0) = (1, 0)`, và `b = B` nên `(x1, y1) = (0, 1)`. Mỗi vòng, với thương `q = a // b`, cặp số mới là `(b, a % b)`, và hệ số cập nhật cùng quy tắc với số: số mới thứ hai là `a - q*b`, nên hệ số mới thứ hai là `x0 - q*x1` và `y0 - q*y1`:

```python
def mo_rong(A, B):
    a, b = A, B
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0   # a là ước chung lớn nhất, và A*x0 + B*y0 = a
```

`return a, x0, y0` trả về ba giá trị cùng lúc; nhận bằng `g, x, y = mo_rong(462, 1071)`. Hãy tự chạy tay hai vòng đầu với A = 462, B = 1071 để thấy hệ số đổi.

Chấm: `bash labs/cham.sh DMS L13 modun.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
