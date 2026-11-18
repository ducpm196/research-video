# Lab DMS L01 — Kiểm hai biểu thức có tương đương không bằng bảng chân trị

Viết `tuongduong.py` (Python 3.11 trở lên); chạy: `python tuongduong.py`.

Cho sẵn năm cặp biểu thức (chép nguyên đoạn này vào đầu tệp; `lambda` chỉ là cách viết một hàm ngắn trên một dòng, số đầu mỗi cặp là số thứ tự, số thứ hai là số mệnh đề):

```python
def keo(a, b):
    return (not a) or b

CAP = [
    (1, 2, lambda p, q: not (p and (not q)), lambda p, q: (not p) or q),
    (2, 2, lambda p, q: keo(p, q), lambda p, q: keo(q, p)),
    (3, 2, lambda p, q: keo(p, q), lambda p, q: keo(not q, not p)),
    (4, 3, lambda p, q, r: keo(p, keo(q, r)), lambda p, q, r: keo(p and q, r)),
    (5, 3, lambda p, q, r: keo(p, q) and keo(q, r), lambda p, q, r: keo(p, r)),
]
```

Với mỗi cặp, thử MỌI dòng của bảng chân trị (2 mũ n dòng; p đổi chậm nhất, bắt đầu từ đúng đúng...), rồi in một dòng:
- `<số thứ tự>: tuong duong` nếu hai biểu thức cùng chân trị ở mọi dòng;
- `<số thứ tự>: khong tuong duong, dong lech dau tien: <giá trị các mệnh đề, 1 là đúng 0 là sai, cách nhau một dấu cách>` nếu có dòng khác nhau (chỉ in dòng lệch ĐẦU TIÊN theo thứ tự trên).

Cú pháp cần dùng (chưa học ở đâu trước đó, nên giải thích ngay ở đây):
- `from itertools import product` ở đầu tệp: mượn một hàm có sẵn của Python tên `product`. Nó sinh mọi bộ giá trị: `product((True, False), repeat=2)` lần lượt cho `(True, True)`, `(True, False)`, `(False, True)`, `(False, False)` (đúng bốn dòng của bảng chân trị hai mệnh đề); `repeat=3` cho tám dòng.
- `for dong in product((True, False), repeat=n):` chạy vòng lặp qua từng dòng đó; mỗi `dong` là một bộ giá trị.
- `f(*dong)`: dấu `*` trước `dong` mở bộ giá trị thành từng đối số riêng. Nếu `dong` là `(True, False)` thì `f(*dong)` giống hệt `f(True, False)`.

Chấm: `bash labs/cham.sh DMS L01 tuongduong.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
