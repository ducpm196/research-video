# Lab CS112 L22 — Đơn hình bằng phân số chính xác, và khối Klee–Minty

Cần: Python 3.11 trở lên. Tạo `donhinh.py` (số liệu minh hoạ, khác ví dụ trong bài). Bài toán: lớn nhất `z = 5*x1 + 4*x2` với

```
6*x1 + 4*x2 <= 24
  x1 + 2*x2 <= 6
 -x1 +   x2 <= 1
         x2 <= 2
x1, x2 >= 0
```

Viết hàm `don_hinh(c, A, b, quy_tac)` (dùng `from fractions import Fraction`): bảng gồm `m` hàng ràng buộc (hệ số của biến chính, biến bù `s1…sm`, vế phải) và hàng `z` (hệ số `-c`); gốc toạ độ hợp lệ (mọi `b >= 0`). Mỗi vòng:

- cột vào: với `quy_tac = "am_nhat"` là cột có hệ số hàng `z` âm nhất (hoà thì chỉ số nhỏ nhất); với `quy_tac = "chi_so_nho"` là cột có chỉ số nhỏ nhất trong các cột có hệ số hàng `z` âm (thứ tự cột: `x1, x2, …, s1, s2, …`); không còn hệ số âm thì dừng;
- hàng ra: chỉ xét hệ số dương trong cột vào, lấy tỉ số `vế phải / hệ số` nhỏ nhất, hoà thì hàng của biến cơ sở có chỉ số cột nhỏ nhất;
- xoay: chia hàng ra cho phần tử xoay, trừ bội của nó khỏi mọi hàng khác (kể cả hàng `z`).

Hàm trả về `z`, giá trị các biến chính và số lần xoay; mỗi lần xoay in `Xoay <k>: cot vao <biến>, hang ra <biến cơ sở bị thay>, z = <z>` (tên biến `x1, x2, s1, s2, …`). Rồi in:

```
Xoay 1: ...
Xoay 2: ...
Toi uu: z = <z>, x1 = <x1>, x2 = <x2>
So lan xoay: <số lần>
Klee-Minty n = 4: am nhat <số lần> lan xoay, chi so nho <số lần> lan xoay
```

Khối Klee–Minty `n = 4` (chỉ số `i, j` từ 1 đến `n`): `c[j] = 2**(n-j)`; `A[i][j] = 2**(i-j+1)` nếu `j < i`, `1` nếu `j == i`, `0` nếu `j > i`; `b[i] = 5**i`. Chạy hàm với cả hai quy tắc trên khối đó (không in từng lần xoay ở đây).

Cú pháp cần dùng (nếu chưa gặp): `Fraction(5, 9)` là phân số 5/9 chính xác; cộng, trừ, nhân, chia, so sánh các `Fraction` như số thường (`Fraction(1, 2) + Fraction(1, 3)` ra `5/6`), nên phép xoay không mất độ chính xác. `min(day, key=lambda j: (T[-1][j], j))` lấy phần tử `j` của `day` có cặp `(T[-1][j], j)` nhỏ nhất (so số trước, hoà thì so `j`).

Chạy: `python donhinh.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L22 donhinh.py`.
