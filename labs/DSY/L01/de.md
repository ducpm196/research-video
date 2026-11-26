# Lab DSY L01 — Đồng hồ logic Lamport

Đọc `stdin` `p1=<int> p2=<int>`. Mô phỏng `P1` tăng một bước gửi tới `P2`, `P2` nhận bằng `max(p2, msg) + 1`, làm thêm một việc nội bộ rồi gửi ngược về `P1`.

In đúng 3 dòng: `p2_recv=<d>`, `p2_next=<d>`, `p1_recv_back=<d>`.
Chấm tự động: `bash labs/cham.sh DSY L01 duong_dan/bai_cua_ban.py`
