# Lab CVI L06 — Độ nhạy sai số stereo theo khoảng cách

Đọc `f B Z1 Z2 dh` từ stdin (ví dụ `600.0 0.15 3.0 9.0 1.0`). Tính độ lệch đúng `d = f * B / Z` rồi tính sai số chính xác theo công thức `err = f * B / (d - dh) - Z` (không dùng công thức xấp xỉ).
In đúng 1 dòng `Z3=<Z1> err3=<2 chữ số>m Z9=<Z2> err9=<2 chữ số>m`.
