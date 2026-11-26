# Lab TOC L12 — Kiểm tra điều kiện Định lý Rice

Đọc ba biểu thức dạng tổng `x` và số nguyên `e1|e2|e3` từ stdin (ví dụ `2|1+1|x+1`). Kiểm tra tính không tầm thường và đồng nghĩa ngữ nghĩa trên `(0, 1, 2)`.
In đúng 1 dòng `has_yes=0/1 has_no=0/1 syn_diff_same_sem=0/1 rice_applies=0/1`.
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Quy ước tính chất ngữ nghĩa: một biểu thức thoả tính chất nếu `ev(ex, x) % 2 == 0` với mọi `x` trong `(0, 1, 2)` (tức luôn chẵn trên `{0, 1, 2}`); `syn_diff_same_sem` kiểm tra `e1` và `e2` cho cùng dãy giá trị trên `(0, 1, 2)`.
