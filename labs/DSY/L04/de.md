# Lab DSY L04 [Mô phỏng phân tán] — Mô phỏng đánh đổi CP vs AP khi phân vùng mạng

Viết chương trình Python mô phỏng mạng 2 nút chia cắt: nhánh CP từ chối yêu cầu ghi lên phân vùng thiểu số để giữ nhất quán (`diverged=0`); nhánh AP vẫn chấp nhận ghi hai bên nên giá trị lệch nhau (`diverged=1`), in đúng 3 dòng:
1. `cp_rejected_minority=1`
2. `ap_available_minority=1`
3. `ap_diverged=1`

Chấm tự động:
```bash
bash labs/cham.sh DSY L04 duong_dan/bai_cua_ban.py
```
