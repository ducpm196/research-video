# Lab DBS L04 — SQLite: kiểm tra tính duy nhất của khoá hợp thành AD

Cơ sở dữ liệu có sẵn bảng `R(A, B, C, D, PRIMARY KEY(A, D))`. Kiểm tra tổng dòng và số cặp `(A, D)` phân biệt, chứng minh `A` riêng lẻ không duy nhất và kiểm tra phụ thuộc hàm `A -> B`.

In đúng 3 dòng: `rows=<d> distinct_ad=<d>`, `a_not_unique=<0|1>`, `fd_a_to_b_holds=<0|1>`.
Chấm tự động: `bash labs/cham.sh DBS L04 duong_dan/bai_cua_ban.sql`
