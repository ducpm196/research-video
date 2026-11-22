# Lab CSA L05 — Dựng cổng logic phổ quát NAND và bộ cộng bán phần/toàn phần

Viết chương trình C chuẩn C11 chỉ dùng hàm `nand(a, b)` để dựng `b_not`, `b_and`, `b_or`, `b_xor`, rồi kiểm tra bộ cộng toàn phần `(a=1, b=1, cin=1)`, in đúng 3 dòng:
1. `not1=0 and11=1 or01=1 xor11=0`
2. `fa_111_sum=1 fa_111_cout=1`
3. `fa_101_sum=0 fa_101_cout=1`

Chấm tự động:
```bash
bash labs/cham.sh CSA L05 duong_dan/bai_cua_ban.c
```
