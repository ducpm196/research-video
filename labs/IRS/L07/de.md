# Lab IRS L07 — Phân rã ma trận bằng SGD kèm chính quy hoá L2

Đọc từ đầu vào chuẩn (`stdin`, dòng chữ dạng `khoá=giá_trị` cách nhau khoảng trắng, ví dụ `p=2.0,1.0 q=1.0,1.0 ...`): `p=<p0,p1> q=<q0,q1> r=<f> eta=<f> lam=<f>` (`<f>` là số thực). Tính sai số `r - dot(p,q)` rồi cập nhật `p` khi `lam = 0` (`p_raw`) và khi có chính quy hoá L2 (`p_reg = p + eta * (err*q - lam*p)`).

In 1 dòng đúng nhãn (`<.1f>` là số thực 1 chữ số thập phân, `<list4>` là danh sách Python làm tròn mỗi phần tử 4 chữ số thập phân như `[1.8, 1.1]`): `err=<.1f> p_raw=<list4> p_reg=<list4>`.
Chấm tự động: `bash labs/cham.sh IRS L07 duong_dan/bai_cua_ban.py`
