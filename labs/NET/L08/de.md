# Lab NET L08 (Mô phỏng Bellman-Ford) — Đếm tới vô cùng khi liên kết A-B đứt

Viết chương trình Python mô phỏng hai bộ định tuyến B và C trao đổi khoảng cách tới A sau khi liên kết A-B đứt (bắt đầu `d_B=1, d_C=2`), mỗi vòng lấy `1 + min` từ hàng xóm đến trần RIP `16`, in đúng 3 dòng:
1. `after_round1=B:3,C:2`
2. `rounds_to_reach_16=15`
3. `final_vals=16,16`

Chấm tự động:
```bash
bash labs/cham.sh NET L08 duong_dan/bai_cua_ban.py
```
