# Lab TOC L01 — DFA chia hết cho m trên số nhị phân

Đọc `m|w1 w2 limit` từ stdin (ví dụ `5|1010 1011 1999`). Dựng DFA `m` trạng thái và kiểm thử `w1`, `w2` cùng mọi số `1..limit`.
In đúng 1 dòng `states=<m> complete=1 s1010=0/1 s1011=0/1 all_2000=0/1`.
Nền tảng Python (`PYT:L04`): đọc dữ liệu qua `sys.stdin.read().strip()`.
Lưu ý giữ đúng tên khoá đầu ra `s1010=... s1011=... all_2000=...` tương ứng cho kết quả trên `w1`, `w2` và mọi số `1..limit`.
