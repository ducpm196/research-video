# Lab CS115 L01 — Chiếu vector bằng Python

Cần: Python 3 (không cần thư viện ngoài). Tạo tệp `chieu.py`. Vector viết bằng danh sách, ví dụ `y = [7, 4, 1]` (số minh hoạ, khác ví dụ trong bài).

1. Viết hàm `dot(u, v)` trả về tích vô hướng (nhân từng cặp cùng vị trí rồi cộng). Với `y = [7, 4, 1]`, `u = [2, 0, 1]` in lần lượt 7 dòng dạng:
   `tu so: <số>`, `mau so: <số>`, `c = <số>`, `hinh chieu: [<x>, <y>, <z>]`, `phan con lai z: [<x>, <y>, <z>]`, `z.u = <số>`, `Pytago: <|y|^2> = <|chieu|^2> + <|z|^2>`.
   (tử số = `dot(y, u)`, mẫu số = `dot(u, u)`, `c` = tử số chia mẫu số, **nhưng phải ra số nguyên chính xác**: dùng `from fractions import Fraction` rồi `c = Fraction(tử số, mẫu số)` (hoặc phép chia nguyên `//`), để in `c = 3`, `hinh chieu: [6, 0, 3]`; phép chia `/` thường sẽ in `3.0` và `[6.0, 0.0, 3.0]`, và bị chấm sai, hình chiếu = `c` nhân từng thành phần của `u`, `z` = `y` trừ hình chiếu; dòng cuối: `dot(y, y) = dot(hinh chieu, hinh chieu) + dot(z, z)`.)
2. Với `y = [2, 3]`, `u = [4, 1]` hệ số `c` không còn là số nguyên: dùng `from fractions import Fraction`, in `c = <phân số>` rồi `hinh chieu: [<phân số>, <phân số>]` (in từng phần tử bằng `str`, ghép trong ngoặc vuông, ngăn bằng dấu phẩy và một khoảng trắng).

Chạy: `python chieu.py`. Chấm (từ thư mục gốc của bộ khoá, nơi có thư mục `labs`): `bash labs/cham.sh CS115 L01 chieu.py`.
