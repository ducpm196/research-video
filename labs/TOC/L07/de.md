# Lab TOC L07 — Phân tích ưu tiên phép toán so với trái sang phải

Đọc biểu thức `+` và `*` chữ số đơn từ stdin (ví dụ `2+3*4`). Tính cả hai kết quả.
In đúng 1 dòng `precedence=<int> left_to_right=<int>`.
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Quy ước: `precedence` tính phép nhân `*` trước cộng `+`; `left_to_right` tính tuần tự từ trái sang phải bỏ qua ưu tiên phép nhân.
