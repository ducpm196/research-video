# Lab SDP L01 — Xử lý lỗi tường minh: thất bại sớm thay vì trả kết quả sai âm thầm

Đọc `stdin` `bad=<str> good=<str>`. Đối chiếu bộ phân tích ngây thơ `parse_prefix(s)` (đọc từng chữ số từ trái sang và dừng ngay tại kí tự không phải chữ số đầu tiên, trả `0` nếu không có chữ số đầu) với bộ phân tích chặt chẽ `int(s)` ném `ValueError` khi chuỗi lẫn ký tự lạ.

In đúng 3 dòng: `naive_12a=<d>`, `strict_42=<d>`, `strict_12a_raised=<0|1>`.
Chấm tự động: `bash labs/cham.sh SDP L01 duong_dan/bai_cua_ban.py`
