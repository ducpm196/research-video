# Lab DMS L09 — Đếm bằng quy tắc nhân và kiểm lại bằng cách liệt kê hết

Viết `dem.py` (Python 3.11 trở lên); chạy: `python dem.py`.

Với mỗi bài đếm dưới đây, in một dòng `<mô tả>: <công thức> <vét cạn>`, trong đó `<công thức>` là kết quả tính bằng quy tắc nhân / chỉnh hợp / hoán vị (một biểu thức số học, KHÔNG liệt kê), và `<vét cạn>` là kết quả đếm bằng cách liệt kê mọi trường hợp (`itertools.product`, `itertools.permutations`, hoặc vòng lặp). Hai số phải bằng nhau.

Dòng cần in, đúng chữ (không dấu):
1. `ma PIN 4 chu so (duoc lap)` — chuỗi 4 chữ số từ 0 đến 9
2. `ma PIN 4 chu so khac nhau` — 4 chữ số từ 0 đến 9, đôi một khác nhau
3. `xep 5 nguoi thanh hang` — hoán vị của 5 người
4. `chuoi 3 ky tu tu abcd, duoc lap`
5. `chuoi 3 ky tu tu abcd, khong lap`
6. `so chan 3 chu so khac nhau tu 1..5` — số có 3 chữ số đôi một khác nhau lập từ các chữ số 1, 2, 3, 4, 5 và chia hết cho 2

Ví dụ định dạng: `chuoi 2 ky tu tu ab, duoc lap: 4 4`.

Gợi ý: ví dụ ở dòng 6, chọn chữ số hàng đơn vị trước (chẵn), rồi các hàng còn lại là chỉnh hợp.

Cú pháp cần dùng (chưa học ở đâu trước đó, nên giải thích ngay ở đây):
- `from itertools import product, permutations` ở đầu tệp: mượn hai hàm có sẵn của Python. `product('ab', repeat=2)` lần lượt cho `('a', 'a')`, `('a', 'b')`, `('b', 'a')`, `('b', 'b')`: mọi chuỗi có lặp (n mũ k chuỗi). `permutations('abc', 2)` cho `('a', 'b')`, `('a', 'c')`, `('b', 'a')`, ...: mọi chuỗi không lặp (n × (n−1) × ... chuỗi).
- `len(list(...))` đếm số phần tử mà các hàm đó sinh ra. `p[2]` là phần tử thứ ba của bộ `p` (đếm từ 0); `int(p[2]) % 2 == 0` kiểm số đó chẵn.

Chấm: `bash labs/cham.sh DMS L09 dem.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
