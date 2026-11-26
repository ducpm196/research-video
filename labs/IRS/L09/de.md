# Lab IRS L09 — Khởi động lạnh với phân phối Beta

Đọc từ đầu vào chuẩn (`stdin`, dạng `khoá=giá_trị`) bốn số nguyên `a1=<int> b1=<int> a2=<int> b2=<int>`. Tính trung bình `a/(a+b)` và độ lệch chuẩn phân phối Beta `sqrt(a*b / ((a+b)^2 * (a+b+1)))` cho cặp mới `(a1, b1)` và cặp cũ `(a2, b2)`.

In 2 dòng đúng nhãn (`<.2f>`, `<.3f>`, `<.4f>` tương ứng 2, 3, 4 chữ số sau dấu chấm): `new_mean=<.2f> new_sd=<.3f>`, `old_mean=<.4f> old_sd=<.4f>`.
Chấm tự động: `bash labs/cham.sh IRS L09 duong_dan/bai_cua_ban.py`
