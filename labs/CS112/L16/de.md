# Lab CS112 L16 — Cái túi phân số, và vì sao tham lam sai với cái túi 0/1

Cần: Python 3.11 trở lên (không cần thư viện ngoài). Tạo `tui.py` (số liệu minh hoạ, khác ví dụ trong bài). Túi chứa tối đa `M = 15` kg; năm món đánh số từ 1:

| món | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| nặng `w` (kg) | 10 | 9 | 5 | 6 | 5 |
| giá trị `p` | 37 | 39 | 26 | 22 | 33 |

Dùng `from fractions import Fraction` để phần lấy và giá trị là số chính xác (không làm tròn). Viết chương trình:

1. sắp các món theo đơn giá `p / w` giảm dần (tính đơn giá bằng `Fraction(p, w)`) rồi in `Thu tu mon: ` và số hiệu món (từ 1) theo thứ tự đó, cách nhau một dấu cách;
2. chạy quy tắc tham lam của cái túi PHÂN SỐ, in `x:` và phần lấy `x` của món 1 đến món 5 (mỗi số in bằng `str(Fraction)`, ví dụ `1`, `0`, `5/9`), rồi in `Tong gia tri: <phân số> = <số thập phân làm tròn 2 chữ số>`;
3. chạy cùng thứ tự đơn giá nhưng cho cái túi 0/1 (lấy nguyên món nếu còn vừa, ngược lại bỏ qua món đó, đi tiếp), và vét cạn mọi tập món (dùng `itertools.combinations`) để tìm giá trị lớn nhất có thể của cái túi 0/1; in `Tham lam 0/1: <giá trị>, toi uu 0/1: <giá trị>`;
4. in `Phan so >= 0/1: CO` nếu giá trị tối ưu của cái túi phân số không nhỏ hơn tối ưu 0/1 (lấy một phần là được thêm quyền, nên không thể tệ hơn).

Cú pháp cần dùng (nếu chưa gặp): `Fraction(5, 9)` là phân số 5/9 chính xác, cộng trừ nhân chia các `Fraction` vẫn ra phân số (`Fraction(1, 2) + Fraction(1, 3)` là `5/6`), `str(Fraction(4, 2))` là `'2'`. `from itertools import combinations` rồi `list(combinations([1, 2, 3], 2))` ra `[(1, 2), (1, 3), (2, 3)]`: mọi cách chọn 2 phần tử, không lặp. `sorted(day, key=lambda i: gia_tri[i])` sắp các phần tử của `day` theo số `gia_tri[i]` tăng dần (thêm dấu trừ trước giá trị để giảm dần).

Chạy: `python tui.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS112 L16 tui.py`.
