# Lab PLC L01 — Bộ phân tích từ vựng regex (khớp dài nhất)

Đọc chuỗi biểu thức từ `stdin` (ví dụ `total = 108 - cnt`).
Bỏ qua khoảng trắng rồi tách tuần tự thành danh sách từ tố gồm: tên (`[A-Za-z_][A-Za-z0-9_]*`, có thể chứa chữ cái, chữ số hoặc `_`), số nguyên (`[0-9]+`) và toán tử một ký tự `[=+*/-]` theo nguyên tắc khớp dài nhất.

In đúng 1 dòng `count=<d> toks=<danh sách chuỗi Python chuẩn>` (dùng `str(toks)`).
Chấm tự động: `bash labs/cham.sh PLC L01 duong_dan/bai_cua_ban.py`
