# Lab CPR L01 — Kiểm tra quay vòng uint8_t và chặn tràn int32_t

Viết chương trình C chuẩn C11 thực hiện và in đúng 3 dòng:
1. Giá trị `uint8_t` của `(250 + 10)`: `wrap=4`
2. Cộng có kiểm tra `2147483640 + 7`: `add1=2147483647`
3. Cộng có kiểm tra `2147483640 + 8` (bị chặn tràn): `add2=OVERFLOW`

Chấm tự động:
```bash
bash labs/cham.sh CPR L01 duong_dan/bai_cua_ban.c
```
