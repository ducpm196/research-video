# Lab DSY L01 — Đồng hồ logic Lamport

Đọc `stdin` `p1=<int> p2=<int>`. Mô phỏng tuần tự: `P1` tăng 1 bước (`msg1 = p1 + 1`) rồi gửi tới `P2`; `P2` nhận bằng `p2_recv = max(p2, msg1) + 1`; ngay sau đó `P2` tăng 1 bước khi gửi phản hồi (`p2_next = p2_recv + 1`) về `P1`; cuối cùng `P1` nhận bằng `p1_recv_back = max(msg1, p2_next) + 1`.

In đúng 3 dòng: `p2_recv=<d>`, `p2_next=<d>`, `p1_recv_back=<d>`.
Chấm tự động: `bash labs/cham.sh DSY L01 duong_dan/bai_cua_ban.py`
