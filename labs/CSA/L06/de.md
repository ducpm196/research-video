# Lab CSA L06 — Bộ cộng 8 bit, trừ bằng bù 2 và cờ tràn

Đọc từ `stdin` `p1=a,b sub=c,d p2=e,f`. Cài hàm cộng 8 bit trả `(sum8, overflow_signed, carry_unsigned)`, thực hiện trừ `c - d` qua cộng bù 2 `((~d) + 1) & 0xFF` và kiểm tra cả hai phép cộng.

In đúng 3 dòng: `add_100_50=<int> ov_signed=<0|1> cf_unsigned=<0|1>`, `sub_40_15=<int>`, `add_200_100=<int> cf_unsigned=<0|1>`.
Chấm tự động: `bash labs/cham.sh CSA L06 duong_dan/bai_cua_ban.py`
