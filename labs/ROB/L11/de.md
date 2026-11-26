# Lab ROB L11 — Phép chiếu camera lỗ kim

Đọc `X Z fx cx` từ stdin (ví dụ `0.8 5.0 600.0 320.0`). Tính `u = fx * (X/Z) + cx` làm tròn nguyên.
In đúng 1 dòng `u_px=<int>`.
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Làm tròn `u_px` bằng định dạng `:.0f` của Python.
