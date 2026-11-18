# Lab CS112 L21 — Quy hoạch tuyến tính hai biến: thử mọi giao điểm và chứng chỉ

Cần: Python 3.11 trở lên. Tạo `qhtt.py` (số liệu minh hoạ, khác ví dụ trong bài). Bài toán: lớn nhất `z = 3*x1 + 2*x2` với

```
x1 + x2   <= 9
3*x1 + x2 <= 18
x1        <= 7
x2        <= 6
x1 >= 0, x2 >= 0
```

Dùng `from fractions import Fraction` (nghiệm là phân số chính xác) và `itertools.combinations`. Mỗi ràng buộc và mỗi trục là một đường `a*x1 + b*x2 = c`: bốn đường biên của bốn ràng buộc trên và hai trục `x1 = 0`, `x2 = 0`, cả thảy 6 đường. Viết chương trình:

1. với mọi cặp trong 6 đường, giải hệ hai phương trình bằng trừ vế (cặp song song, định thức `a1*b2 - a2*b1 == 0`, bỏ qua); đếm số cặp giải được;
2. giữ giao điểm thoả cả bốn ràng buộc và `x1 >= 0`, `x2 >= 0` (đó là đỉnh của miền chấp nhận được); tính `z` tại từng đỉnh;
3. dựng chứng chỉ chặn trên: tìm `y1`, `y2` sao cho `y1*(x1 + x2) + y2*(3*x1 + x2)` đúng bằng `3*x1 + 2*x2` (giải hai phương trình theo hệ số của `x1` và `x2`), rồi chặn trên là `y1*9 + y2*18`.

In đúng chín dòng (phân số in bằng `str(Fraction)`, ví dụ `9/2`; đỉnh sắp theo `z` tăng dần):

```
Cap duong giai duoc: <số cặp>
Dinh hop le: <số đỉnh>
(<x1>, <x2>) z = <z>        (một dòng cho mỗi đỉnh, đúng thứ tự trên)
Toi uu: z = <z lớn nhất> tai (<x1>, <x2>)
Chung chi: y1 = <y1>, y2 = <y2>, can tren <chặn trên>
```

Chạy: `python qhtt.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L21 qhtt.py`.
