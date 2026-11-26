# Lab CSA L05 — Dựng cổng logic phổ quát NAND và bộ cộng bán phần/toàn phần

Đọc từ `stdin` 2 bộ 3 bit đầu vào cho bộ cộng toàn phần (ví dụ `a1=1 b1=1 c1=1 a2=1 b2=0 c2=1`). Chỉ dùng cổng `nand` để dựng NOT/AND/OR/XOR và tính `(sum, cout)` cho hai bộ đầu vào.

In đúng 3 dòng: `not1=<d> and11=<d> or01=<d> xor11=<d>`, `fa_111_sum=<d> fa_111_cout=<d>`, `fa_101_sum=<d> fa_101_cout=<d>`.
Chấm tự động: `bash labs/cham.sh CSA L05 duong_dan/bai_cua_ban.c`
