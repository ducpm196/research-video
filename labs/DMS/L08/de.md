# Lab DMS L08 — Biểu đồ thứ tự và sắp xếp tô pô cho quan hệ "là ước của" trên các ước của 24

Viết `thutu.py` (Python 3.11 trở lên); chạy: `python thutu.py`.

Tập `S = [1, 2, 3, 4, 6, 8, 12, 24]` (các ước của 24); quan hệ `a ≼ b` khi `a` là ước của `b` (`b % a == 0`). Quan hệ "phủ" (cạnh của biểu đồ thứ tự): cặp `(a, b)` với `a` khác `b`, `a ≼ b`, và KHÔNG có phần tử `c` khác `a`, `b` nào mà `a ≼ c` và `c ≼ b`.

In đúng bảy dòng:
1. `so canh Hasse: <số cạnh phủ>`
2. `canh: a-b a-b ...` — các cạnh phủ `a-b` xếp tăng dần theo `a` rồi theo `b`, cách nhau một dấu cách
3. `phan tu toi tieu: <các phần tử không có ai đứng dưới, cách nhau dấu cách>`
4. `phan tu toi dai: <các phần tử không có ai đứng trên>`
5. `cap khong so sanh duoc: <số cặp {a, b} với a < b mà không số nào là ước của số kia>`
6. `sap xep to po (chon so lon nhat): ...` — thuật toán: mỗi lượt, trong các phần tử CHƯA xếp mà mọi phần tử đứng dưới nó đã xếp, chọn phần tử LỚN NHẤT, xếp vào hàng; lặp tới khi hết. In hàng, các số cách nhau một dấu cách.
7. `so cach sap xep to po: <số>` — đếm bằng cách thử mọi hoán vị của S, tức mọi cách xếp thứ tự (`from itertools import permutations` liệt kê chúng): hàng hợp lệ khi mọi cặp `a ≼ b` (a khác b) có `a` đứng trước `b`.

Gợi ý: phần tử "đứng dưới x" là các a khác x mà x % a == 0; dùng `list.index` để biết vị trí trong hàng.

Chấm: `bash labs/cham.sh DMS L08 thutu.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
