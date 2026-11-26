# Lab ROB L02 — Phân giải encoder và sai số trôi ngang

Đọc `D ticks dist_m deg` từ stdin (ví dụ `0.2 2000 15.0 2.0`). Tính `mm/xung` và độ lệch ngang.
In đúng 1 dòng `mm_per_tick=<3 chữ số> lateral_err_15m=<3 chữ số>m`.
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Lưu ý giữ nguyên tên khoá `lateral_err_15m=<3 chữ số>m` tính cho đúng tham số `dist_m` đầu vào bằng `dist_m * sin(radians(deg))`.
