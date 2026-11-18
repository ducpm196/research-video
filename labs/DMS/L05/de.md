# Lab DMS L05 — Phép toán tập hợp và bao hàm–loại trừ bằng chương trình

Viết `taphop.py` (Python 3.11 trở lên); chạy: `python taphop.py`.

Cho `A = {2, 3, 5, 7, 11, 13}` và `B = {1, 3, 5, 7, 9, 11}` (kiểu `set` của Python). In đúng sáu dòng, các phần tử của một tập in theo thứ tự tăng dần, cách nhau một dấu cách:
1. `hop: ...` (hợp A và B)
2. `giao: ...`
3. `A bo B: ...` (phần tử thuộc A mà không thuộc B)
4. `B bo A: ...`
5. `so tap con cua A: <số>` (số phần tử của tập lũy thừa của A)
6. `chia het cho 4 hoac 6, tu 1 den 1000: dem=<a> congthuc=<b>` với `a` là số đếm bằng cách duyệt từng số từ 1 đến 1000, `b` là kết quả của công thức bao hàm–loại trừ (số chia hết cho 4, cộng số chia hết cho 6, trừ số chia hết cho bội chung nhỏ nhất của 4 và 6, tức số nhỏ nhất chia hết cho cả hai, là 12).

Gợi ý: `A | B`, `A & B`, `A - B`; `sorted(...)`; `' '.join(str(x) for x in ...)`; `2 ** len(A)`; `n // 4` là phần nguyên của n chia 4.

Chấm: `bash labs/cham.sh DMS L05 taphop.py` — in `ĐÚNG` khi đầu ra trùng `mong_doi.txt`.
