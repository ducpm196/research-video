# Lab DSY L01 [Mô phỏng phân tán] — Đồng hồ logic Lamport

Viết chương trình Python cài đồng hồ Lamport cho 2 nút `P1`, `P2`: `P1` sự kiện nội bộ `(L=1)` gửi sang `P2` đang ở `(L=1)` -> nhận ở `max(1,1)+1 = 2`, tiếp tục `P2` làm việc nội bộ `(3)` gửi trả `P1`, in đúng 3 dòng:
1. `p2_recv=2`
2. `p2_next=3`
3. `p1_recv_back=4`

Chấm tự động:
```bash
bash labs/cham.sh DSY L01 duong_dan/bai_cua_ban.py
```
