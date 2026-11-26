# Lab TOC L05 — Tối thiểu hoá DFA bằng bảng đánh dấu cặp

Đọc `d0_0,d0_1;...|acc0,...` từ stdin (ví dụ `1,2;1,2;2,1;4,4;4,3|2,4`). Lọc trạng thái tới được từ 0, đánh dấu cặp phân biệt và gộp lớp.
In đúng 1 dòng `reachable=<int> marked_pairs=<int> min_dfa_states=<int>`.
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Quy ước DFA đầu vào: trạng thái bắt đầu mặc định là `0`, bảng chữ cái là `{0, 1}` ứng với cặp `d_0, d_1`.
