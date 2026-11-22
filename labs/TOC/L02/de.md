# Lab TOC L02 — Cài phép dựng tập con chuyển NFA {A, B, C} kết thúc bằng '10' sang DFA

Cài đặt thuật toán dựng tập con thật bằng tìm kiếm theo chiều rộng (BFS) từ trạng thái khởi đầu `{A}` của NFA nhận chuỗi kết thúc bằng `'10'` (bảng chuyển NFA: `('A','0')->{'A'}`, `('A','1')->{'A','B'}`, `('B','0')->{'C'}`, trạng thái nhận `'C'`). Chạy DFA vừa dựng trên `'110'` và `'101'`.

Định dạng đầu ra (1 dòng):
`dfa_states=<số> acc_110=<0 hoặc 1> acc_101=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh TOC L02 duong_dan/bai_cua_ban.py
```
