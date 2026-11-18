# Lab DMS L06 — Phân loại hàm trên tập hữu hạn và kiểm chuồng bồ câu bằng máy

Viết `ham.py` (Python 3.11 trở lên); chạy: `python ham.py`.

Phần 1. Năm hàm, mỗi hàm là một từ điển `{phần tử của A: ảnh}` (chép nguyên vào đầu tệp), cùng tập đích B:

```python
HAM = [
    ('f1', {1: 'a', 2: 'b', 3: 'a', 4: 'c'}, {'a', 'b', 'c'}),
    ('f2', {1: 'a', 2: 'c', 3: 'd'}, {'a', 'b', 'c', 'd'}),
    ('f3', {1: 'x', 2: 'z', 3: 'y'}, {'x', 'y', 'z'}),
    ('f4', {1: 'p', 2: 'q', 3: 'p', 4: 'p', 5: 'q'}, {'p', 'q'}),
    ('f5', {1: 'a', 2: 'a', 3: 'b'}, {'a', 'b', 'c'}),
]
```

Với mỗi hàm in một dòng:
- `<tên>: song anh` nếu vừa đơn ánh vừa toàn ánh;
- nếu không: `<tên>: <đơn ánh hay không>, <toàn ánh hay không>` viết đúng `don anh` hoặc `khong don anh`, rồi `toan anh` hoặc `khong toan anh` (theo thứ tự đó: đơn ánh trước, toàn ánh sau). Ví dụ: `f9: khong don anh, toan anh`.

(Đơn ánh: hai phần tử khác nhau luôn có ảnh khác nhau. Toàn ánh: mọi phần tử của B đều là ảnh của ít nhất một phần tử của A.)

Phần 2. Chọn k số khác nhau từ 1 đến 12. Có hai số tổng bằng 13 không? Với k = 7 rồi k = 6, liệt kê MỌI cách chọn và in:
`chon <k> so tu 1 den 12: <tổng số cách chọn> cach, <số cách có hai số tổng 13> cach co cap tong 13`

Cú pháp cần dùng (chưa học ở đâu trước đó, nên giải thích ngay ở đây):
- `from itertools import combinations` ở đầu tệp: mượn một hàm có sẵn của Python. `combinations(range(1, 13), 3)` lần lượt cho mọi cách chọn 3 số khác nhau từ 1 đến 12, không kể thứ tự; mỗi cách là một bộ số như `(1, 2, 3)`, `(1, 2, 4)`, ... Vòng lặp: `for chon in combinations(range(1, 13), k):`.
- `f.values()` là các ảnh của hàm `f` (các giá trị của từ điển); `set(...)` bỏ các giá trị trùng; `len(...)` đếm. Số ảnh khác nhau bằng số phần tử của A nghĩa là hai phần tử khác nhau luôn có ảnh khác nhau.

Chấm: `bash labs/cham.sh DMS L06 ham.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
