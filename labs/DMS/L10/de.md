# Lab DMS L10 — Tam giác Pascal, tổ hợp và đường đi trên lưới bằng chương trình

Viết `tohop.py` (Python 3.11 trở lên); chạy: `python tohop.py`.

Viết hàm `pascal(n)` trả hàng thứ n của tam giác Pascal (hàng 0 là `[1]`, hàng 1 là `[1, 1]`, ...) bằng QUY TẮC CỘNG (mỗi số bằng tổng hai số phía trên, hai đầu là 1), KHÔNG dùng công thức giai thừa. In đúng năm dòng:

1. `C(12,5): <a> <b>` (`C(n,k)` là tổ hợp chập k của n) — `a` tính bằng công thức giai thừa `12! / (5! 7!)`, `b` lấy từ `pascal(12)[5]`
2. `hang 8 cua tam giac Pascal: ...` — các số của hàng 8, cách nhau một dấu cách
3. `tong hang 6: <số>` — tổng các số của hàng 6
4. `uy ban 3 nguoi, 7 nam 5 nu, it nhat 1 nu: <a> <b>` — `a = C(12,3) − C(7,3)` (lấy từ `pascal`), `b` đếm vét cạn (thử hết mọi trường hợp): liệt kê mọi nhóm 3 người từ 12 người (7 nam, 5 nữ) và đếm nhóm có ít nhất một nữ
5. `duong di luoi 4 phai 3 len: <a> <b>` — `a = C(7,3)` (từ `pascal`), `b` điền số trên lưới: ô (hàng r, cột c) có `d[r][c] = d[r-1][c] + d[r][c-1]`, hàng đầu và cột đầu bằng 1, đáp số là `d[3][4]`

Gợi ý: `from math import factorial`; `from itertools import combinations`; nhóm 3 người: `combinations(nguoi, 3)`.

Cú pháp cần dùng (chưa học ở đâu trước đó, nên giải thích ngay ở đây):
- `from math import factorial` ở đầu tệp: mượn hàm có sẵn `factorial(n)`, cho n giai thừa (`factorial(4)` là 24).
- `from itertools import combinations` mượn hàm có sẵn khác: `combinations(['a', 'b', 'c'], 2)` lần lượt cho `('a', 'b')`, `('a', 'c')`, `('b', 'c')`, mọi cách chọn 2 phần tử, không kể thứ tự. Vòng lặp: `for nhom in combinations(nguoi, 3):`.
- Danh sách lồng nhau: `d = [[1] * 5 for _ in range(4)]` là danh sách 4 hàng, mỗi hàng 5 số 1; `d[r][c]` là ô ở hàng `r`, cột `c` (đếm từ 0).

Chấm: `bash labs/cham.sh DMS L10 tohop.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
