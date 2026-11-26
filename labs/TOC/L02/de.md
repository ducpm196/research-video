# Lab TOC L02 — Dựng tập con chuyển NFA sang DFA

Đọc `ab|w1 w2` (hậu tố 2 bit) từ stdin (ví dụ `10|110 101`). Dựng NFA nhận chuỗi kết thúc bằng `ab`, chuyển sang DFA bằng BFS và kiểm tra `w1, w2`.
In đúng 1 dòng `dfa_states=<int> acc_110=0/1 acc_101=0/1`.
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Lưu ý giữ đúng tên khoá đầu ra `acc_110=... acc_101=...` tương ứng cho kết quả trên `w1` và `w2`.
