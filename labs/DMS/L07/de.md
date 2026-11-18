# Lab DMS L07 — Kiểm ba tính chất của quan hệ và tìm lớp tương đương bằng chương trình

Viết `quanhe.py` (Python 3.11 trở lên); chạy: `python quanhe.py`.

Tập `A = {1, 2, 3, 4, 5, 6}`. Bốn quan hệ, mỗi quan hệ là một hàm `R(a, b)` trả đúng khi `a` có quan hệ với `b` (chép nguyên vào đầu tệp):

```python
A = [1, 2, 3, 4, 5, 6]
QH = [
    ('R1', lambda a, b: (a - b) % 4 == 0),
    ('R2', lambda a, b: b % a == 0),
    ('R3', lambda a, b: abs(a - b) <= 1),
    ('R4', lambda a, b: (a + b) % 2 == 0),
]
```

Với mỗi quan hệ, kiểm bốn tính chất trên MỌI phần tử, mọi cặp, mọi bộ ba của A (viết 1 nếu đúng, 0 nếu sai):
- `PX`: phản xạ (mọi a: a R a);
- `DX`: đối xứng (mọi a, b: a R b thì b R a);
- `PDX`: phản đối xứng (mọi a, b: a R b và b R a thì a bằng b);
- `BC`: bắc cầu (mọi a, b, c: a R b và b R c thì a R c).

In một dòng `<tên>: PX=<0|1> DX=<0|1> PDX=<0|1> BC=<0|1>`. Nếu quan hệ là tương đương (PX, DX, BC cùng bằng 1), in thêm vào cuối dòng `, tuong duong, cac lop: ` rồi các lớp tương đương, mỗi lớp là một danh sách tăng dần in bằng `print(sorted(lop))`, các lớp xếp theo phần tử nhỏ nhất, cách nhau một dấu cách.

Ví dụ định dạng: `R9: PX=1 DX=1 PDX=0 BC=1, tuong duong, cac lop: [1, 2] [3]`.

Chấm: `bash labs/cham.sh DMS L07 quanhe.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
