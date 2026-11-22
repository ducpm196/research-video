# Lab TOC L01 — Dựng DFA 5 trạng thái kiểm tra số nhị phân chia hết cho 5

Cài đặt máy hữu hạn đơn định (DFA) gồm 5 trạng thái phần dư `0..4` theo công thức `du = (2 * du + bit) % 5` bắt đầu từ `0`, nhận khi `du == 0`. Kiểm tra bảng chuyển đủ cả `'0'` và `'1'` tại mọi trạng thái (`complete=1`), kiểm thử toàn bộ số `1..1999`, cùng hai chuỗi `'1010'` (`10`) và `'1011'` (`11`).

Định dạng đầu ra (1 dòng):
`states=<số> complete=<0 hoặc 1> s1010=<0 hoặc 1> s1011=<0 hoặc 1> all_2000=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh TOC L01 duong_dan/bai_cua_ban.py
```
