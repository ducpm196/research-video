# Lab SDP L00 — Đo độ phức tạp vòng McCabe bằng cây cú pháp AST thật

Đọc `stdin` chứa mã nguồn một hàm Python kết hợp các lệnh `if`, `for`, `while`, phép `and`/`or`. Dùng `ast` đếm số nút rẽ nhánh và tính độ phức tạp `M = 1 + nhánh`.

In đúng 3 dòng: `decision_points=<d>`, `mccabe_complexity=<d>`, `max_recommended_le10=<0|1>`.
Chấm tự động: `bash labs/cham.sh SDP L00 duong_dan/bai_cua_ban.py`
