# Lab CS115 L46 — Nghịch đảo: giải M w = b, ma trận gần suy biến, công thức hồi quy

Cần: Python 3 (không cần thư viện ngoài), `from fractions import Fraction`. Tạo tệp `nghichdao.py` (số minh hoạ, khác ví dụ trong bài). Khi in danh sách chứa `Fraction`, đổi từng phần tử sang chuỗi `str(x)` rồi nối bằng `", ".join(...)` (ví dụ `1/100`), tránh `print` thẳng `Fraction` ra chữ `Fraction(...)`.

1. `M = [[5, 2], [7, 3]]`, `b = [9, 13]`. Nghịch đảo hai nhân hai: đổi chỗ `a` và `d`, đổi dấu `b` và `c`, chia cho định thức `ad - bc`. In `dinh thuc M: <số>`, `M nghich dao: [[..], [..]]`, `w: [..]` (nghịch đảo nhân `b`), `M.w: [..]` (M nhân `w` phải ra lại `b`).
2. Ma trận gần suy biến `[[1, 1], [1, 1 + t]]` với `t = 1/100` rồi `t = 1/10000`. Với mỗi `t` in một dòng `t=<t>: dinh thuc <số>, nghich dao lon nhat <số>, w doi <[..]>`. Trong đó "nghịch đảo lớn nhất" là phần tử lớn nhất theo giá trị tuyệt đối của ma trận nghịch đảo, và "`w` đổi" là vector `M⁻¹ nhân [0, 1/1000]` (nghiệm đổi bao nhiêu khi vế phải `b` đổi thêm `1/1000` ở phần tử thứ hai).
3. Công thức hồi quy `w = (X^T X)^{-1} X^T y` với `X = [[1, 1], [1, 2], [1, 3]]`, `y = [2, 2, 4]`. In `hoi quy: w = [..]`.
4. Hai cột giống nhau: `X2 = [[1, 1], [3, 3], [5, 5]]`. In `hai cot giong nhau: dinh thuc X^T X = <số>`.

Chạy: `python nghichdao.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L46 nghichdao.py`.
