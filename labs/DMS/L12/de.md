# Lab DMS L12 — Bao hàm–loại trừ: đếm bằng công thức và kiểm bằng cách liệt kê hết

Viết `baohamloaitru.py` (Python 3.11 trở lên); chạy: `python baohamloaitru.py`.

Với mỗi bài, in một dòng `<mô tả>: <bao hàm–loại trừ> <vét cạn>`; `<bao hàm–loại trừ>` tính bằng công thức (cộng, trừ xen kẽ theo số tập trong giao), `<vét cạn>` đếm bằng cách liệt kê hết. Hai số phải bằng nhau.

Năm dòng, đúng chữ (không dấu):
1. `khong chia het cho 3, 5, 7 tu 1 den 1000` — số nguyên từ 1 đến 1000 không chia hết cho số nào trong ba số 3, 5, 7 (bao hàm–loại trừ cho ba tập; số chia hết cho a là `1000 // a`)
2. `D7` — số hoán vị của 7 vật mà không vật nào ở đúng vị trí cũ
3. `D9` — như trên cho 9 vật (vét cạn 362 880 hoán vị)
4. `toan anh 5 phan tu len 3 phan tu` — số hàm từ tập 5 phần tử lên tập 3 phần tử sao cho mọi phần tử của tập đích đều được dùng (bao hàm–loại trừ: lấy tất cả các hàm rồi trừ những hàm bỏ sót ít nhất một giá trị của tập đích, tự lập biểu thức; vét cạn: `product(range(3), repeat=5)` giữ lại dãy dùng đủ 3 giá trị)
5. `so nguyen to cung nhau voi 360 trong 1..360` — đếm các số k từ 1 đến 360 nguyên tố cùng nhau với 360. (Hai số nguyên tố cùng nhau khi ước chung lớn nhất của chúng bằng 1, tức không có số nào lớn hơn 1 chia hết cho cả hai; ví dụ 8 và 15 là nguyên tố cùng nhau, 8 và 12 thì không vì 4 chia hết cho cả hai. `math.gcd(a, b)` cho ước chung lớn nhất của a và b.) Cho 360 = 2³ · 3² · 5, nên chỉ cần các số nguyên tố 2, 3, 5; vét cạn: `math.gcd`.

Ví dụ định dạng: `D3: 2 2`.

Cú pháp cần dùng (chưa học ở đâu trước đó, nên giải thích ngay ở đây):
- `from itertools import permutations, product, combinations` mượn các hàm liệt kê có sẵn: `permutations(range(3))` cho mọi cách xếp 3 số 0, 1, 2 thành hàng (6 hàng); `product(range(3), repeat=2)` cho mọi bộ hai số từ 0 đến 2 (9 bộ); `combinations([2, 3, 5], 2)` cho `(2, 3)`, `(2, 5)`, `(3, 5)`, mọi cách chọn 2 phần tử không kể thứ tự. `from math import comb, factorial, gcd` mượn tổ hợp, giai thừa và ước chung lớn nhất.
- `sum(1 for p in permutations(range(n)) if điều kiện)`: với mỗi `p`, nếu điều kiện đúng thì cộng thêm 1, tức đếm các `p` thoả điều kiện. Dùng vòng lặp thường với `dem = dem + 1` cũng được.
- `all(p[i] != i for i in range(n))`: đúng khi `p[i] != i` đúng với mọi `i` từ 0 đến n − 1. `len(set(f))` đếm số giá trị khác nhau trong `f`.

Chấm: `bash labs/cham.sh DMS L12 baohamloaitru.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
