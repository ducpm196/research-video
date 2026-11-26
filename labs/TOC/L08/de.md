# Lab TOC L08 — Ôtômat đẩy xuống PDA cho 0^n 1^n

Đọc `max_len|w1|w2` từ stdin (ví dụ `10|00001111|01010101`). Kiểm tra PDA trên toàn bộ chuỗi dài `0..max_len` và `w1, w2`.
In đúng 1 dòng `tested=<int> all_match=0/1 ex_00001111=0/1 ex_01010101=0/1`.
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Quy ước: dựng PDA nhận ngôn ngữ `{0^n 1^n}`, đối chiếu kết quả trên mọi chuỗi nhị phân độ dài `0..max_len` để tính `all_match` và giữ nguyên khoá `ex_00001111=` (cho `w1`), `ex_01010101=` (cho `w2`).
