# Lab OSY L00 — Chế độ nhân, lời gọi hệ thống và chi phí chuyển ngữ cảnh

Viết chương trình C chuẩn C11 tính chi phí CPU khi thực hiện `1 000` lần chuyển ngữ cảnh mỗi giây (mỗi lần `5 us`) và so với mức `50 000` lần/giây, cũng như đọc đúng mã phân biệt chuyển ngữ cảnh vs gọi hàm thường (`mode_switch=1`), in đúng 3 dòng:
1. `cpu_pct_1k=0.50`
2. `cpu_pct_50k=25.00`
3. `syscall_mode_switch=1`

Chấm tự động:
```bash
bash labs/cham.sh OSY L00 duong_dan/bai_cua_ban.c
```
