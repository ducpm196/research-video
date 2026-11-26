# Lab SEC L05 — Kiểm tra chính sách cookie SameSite trước POST chéo trang

Đọc `stdin` `c1=<ss,m,cross> c2=<ss,m,cross> c3=<ss,m,cross>`. Mô phỏng quy tắc trình duyệt gửi cookie theo cờ `SameSite` (`None`, `Lax`, `Strict`), phương thức HTTP và ngữ cảnh chéo trang.

In đúng 3 dòng: `none_cross_post=<0|1>`, `lax_cross_post=<0|1>`, `strict_cross_post=<0|1>`.
Chấm tự động: `bash labs/cham.sh SEC L05 duong_dan/bai_cua_ban.py`
