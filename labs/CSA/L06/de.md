# Lab CSA L06 (Mô phỏng phần cứng ALU) — Bộ cộng 8 bit, trừ bằng bù 2 và cờ tràn

Viết chương trình Python mô phỏng bộ cộng 8 bit phát hiện cả **tràn có dấu (OV)** và **nhớ không dấu (CF)** cho `(100 + 50)` và phép trừ `40 - 15`, in đúng 3 dòng:
1. `add_100_50=150 ov_signed=1 cf_unsigned=0`
2. `sub_40_15=25`
3. `add_200_100=44 cf_unsigned=1`

Chấm tự động:
```bash
bash labs/cham.sh CSA L06 duong_dan/bai_cua_ban.py
```
