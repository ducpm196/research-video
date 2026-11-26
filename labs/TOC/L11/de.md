# Lab TOC L11 — Nghịch lý đường chéo bài toán dừng

Đọc bảng vuông `k×k` (`r0;r1;...`) từ stdin (ví dụ `1,0,1;0,0,1;1,1,0`). Duyệt toàn bộ `2^k` ứng viên kiểm chứng mâu thuẫn đường chéo.
In đúng 1 dòng `table_size=<k> candidates=<2^k> possible_matches=<int>`.
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Định nghĩa `possible_matches`: trong toàn bộ `2^k` dãy nhị phân ứng viên `D`, đếm số hàng `row` thoả đồng thời `D == row` và `D[idx] != row[idx]` (luôn bằng `0` theo lập luận đường chéo).
