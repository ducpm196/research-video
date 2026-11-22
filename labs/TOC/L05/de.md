# Lab TOC L05 — Cài thuật toán đánh dấu cặp tối thiểu hoá DFA 5 trạng thái

Cho DFA 5 trạng thái `{0,1,2,3,4}` (khởi đầu `0`, nhận `{2,4}`, bảng chuyển: `(0,'0')->1, (0,'1')->2, (1,'0')->1, (1,'1')->2, (2,'0')->2, (2,'1')->1, (3,'0')->4, (3,'1')->4, (4,'0')->4, (4,'1')->3`). Hãy chạy lọc trạng thái tới được từ `0`, rồi chạy thuật toán đánh dấu cặp (lặp tới khi không thêm cặp phân biệt mới) để đếm số cặp bị đánh dấu và số trạng thái tối tiểu còn lại.

Định dạng đầu ra (1 dòng):
`reachable=<số> marked_pairs=<số> min_dfa_states=<số>`

Chấm tự động:
```bash
bash labs/cham.sh TOC L05 duong_dan/bai_cua_ban.py
```
