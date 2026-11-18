# Lab DMS L11 — Sao và vạch: đếm nghiệm và kiểm lại bằng cách liệt kê hết

Viết `saovach.py` (Python 3.11 trở lên); chạy: `python saovach.py`.

Với mỗi bài, in một dòng `<mô tả>: <công thức> <vét cạn>`: `<công thức>` là kết quả tính bằng sao và vạch (có thể dùng `from math import comb`; bài 4 dùng công thức "tổng trừ các trường hợp vi phạm"), `<vét cạn>` là kết quả đếm bằng cách liệt kê hết (dùng `itertools.product` hoặc `itertools.combinations_with_replacement`). Hai số phải bằng nhau.

Bốn dòng, đúng chữ (không dấu):
1. `x1+x2+x3+x4 = 7` — số nghiệm nguyên không âm
2. `x1+x2+x3 = 12, moi xi >= 2` — mỗi biến ít nhất 2 (đổi biến yi = xi − 2)
3. `chon 4 vien kem tu 6 vi` — chọn 4 viên kem từ 6 vị, được trùng vị, không kể thứ tự
4. `x1+x2+x3 = 10, moi xi <= 5` — số nghiệm nguyên không âm mà mọi biến không quá 5. Công thức: tổng số nghiệm không giới hạn, trừ đi số nghiệm có một biến từ 6 trở lên (có 3 cách chọn biến đó; không thể có hai biến cùng từ 6 trở lên vì khi đó tổng đã quá 10).

Ví dụ định dạng: `x1+x2 = 3: 4 4`.

Cú pháp cần dùng (chưa học ở đâu trước đó, nên giải thích ngay ở đây):
- `from math import comb` mượn hàm có sẵn: `comb(5, 2)` là tổ hợp chập 2 của 5, bằng 10.
- `from itertools import product, combinations_with_replacement` mượn hai hàm liệt kê. `product(range(3), repeat=2)` lần lượt cho mọi bộ hai số từ 0 đến 2: `(0, 0)`, `(0, 1)`, `(0, 2)`, `(1, 0)`, ... (9 bộ). `combinations_with_replacement('ab', 2)` cho `('a', 'a')`, `('a', 'b')`, `('b', 'b')`: chọn 2 phần tử, được lặp, không kể thứ tự.
- Đếm bộ thoả điều kiện: `sum(1 for x in product(range(8), repeat=4) if sum(x) == 7)` nghĩa là: với mỗi bộ `x`, nếu tổng các số trong `x` bằng 7 thì cộng thêm 1. Cách viết tương đương dài hơn: đặt `dem = 0`, vòng `for x in product(...)`, `if sum(x) == 7:`, `dem = dem + 1`. Dùng vòng lặp thường cũng được.

Chấm: `bash labs/cham.sh DMS L11 saovach.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
