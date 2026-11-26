# Lab AGT L01 — Kiểm tra lược đồ tham số gọi công cụ

Đọc `stdin` các lời gọi `val:acc,...` trong đó `val` có thể là `bool`, số âm hoặc nguyên. Chỉ hợp lệ khi `val` là số nguyên thuần `(not True/False)` trong `(0, max_amt]` và `acc` là đúng 10 chữ số.

In 1 dòng: `total_calls=<d> valid_count=<d> idx=<list>`.
Chấm tự động: `bash labs/cham.sh AGT L01 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
