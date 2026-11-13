# Lab BNK L05 — Thứ tự khoá cho bốn lệnh chuyển

Quy tắc chống bế tắc: **luôn khoá hàng có mã nhỏ hơn trước**, dù lệnh chuyển đi từ đâu tới đâu.

Viết chương trình `ThuTuKhoa` (tệp `ThuTuKhoa.java`). Có bốn lệnh chuyển `(từ, tới)`: `(4, 9) (9, 4) (7, 4) (4, 7)`. Với mỗi lệnh, tính mã khoá trước (nhỏ hơn) và mã khoá sau (lớn hơn) bằng `Math.min` và `Math.max`, rồi in một dòng đúng dạng:

`4 -> 9: khoa 4 roi 9`

Chạy: `javac ThuTuKhoa.java && java ThuTuKhoa`. Chấm: `bash labs/cham.sh BNK L05 ThuTuKhoa.java`.
