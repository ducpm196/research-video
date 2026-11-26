# Lab CSA L02 — Phép toán bit, mặt nạ và kiểm lũy thừa của 2

Đọc từ `stdin` dòng `x_hex=5A a=64 b=48 val=5` (`x_hex` dạng hexa, cùng các số nguyên dương `a, b, val`). Kiểm tra bit 3 của `x`, bật bit 0, tắt bit 4, kiểm tra lũy thừa của 2 cho `a` và `b`, và tính `val << 4`.

In đúng 3 dòng: `bit3=<d> set0=0x<XX> clr4=0x<XX>`, `pow2_64=<d> pow2_48=<d>`, `shift_mul=<u>`.
Chấm tự động: `bash labs/cham.sh CSA L02 duong_dan/bai_cua_ban.c`
