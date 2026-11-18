# Lab BNX L08 — Chỉ mục ngược và định tuyến mảnh (mô phỏng bằng Python, không cần Elasticsearch)

Có bốn mô tả giao dịch (viết không dấu): `a1` rut tien atm; `a2` chuyen tien the; `a3` chuyen khoan napas; `a4` nap tien the.
Viết `mau.py` (Python 3, chỉ thư viện chuẩn) làm bốn việc, in đúng sáu dòng như `mong_doi.txt`:

1. Dựng chỉ mục ngược (từ → tập mã bản ghi) rồi in danh sách đã sắp của ba từ `tien`, `the`, `chuyen`, dạng `tien: a1 a2 a4` (từ, dấu hai chấm, các mã cách nhau một dấu cách).
2. In `chuyen va the:` và các mã bản ghi chứa cả hai từ (phần chung của hai tập), cùng dạng.
3. In `manh cua 29, 41, 50 voi 5 manh chinh:` và ba mảnh `h % 5`, cách nhau một dấu cách.
4. Đổi từ 4 sang 6 mảnh chính: đếm trong 12 giá trị băm đầu (0 đến 11) bao nhiêu giá trị có `h % 4 == h % 6`. In `doi 4 -> 6 manh chinh: giu manh <số> / 12`.

Gợi ý cú pháp Python: `d = {}` là từ điển rỗng; `d.setdefault(k, set()).add(x)` lấy tập của `k` (tạo tập rỗng nếu chưa có) rồi thêm `x`; `a & b` là phần chung của hai tập; `sorted(t)` xếp một tập; `h % n` là số dư; `print(a, *l)` in `a` rồi từng phần tử của `l` cách nhau dấu cách.

Số liệu là số minh hoạ, khác ví dụ trong bài. Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L08 mau.py`.
