# Lab CAS L02 — Ariane 5 (1996): mô phỏng 3 cách xử lý giá trị vượt ngưỡng 16-bit có dấu

Cho giá trị tốc độ đứng mô phỏng `val = 38_000` vượt trần `[-32768, 32767]` của số nguyên 16 bit có dấu: tính kết quả khi (1) quay vòng hai bù, (2) bão hoà kẹp vào biên gần nhất, (3) gắn cờ dừng báo tràn.

Định dạng đầu ra (1 dòng):
`wrap=<số nguyên> saturate=<số nguyên> overflow=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh CAS L02 duong_dan/bai_cua_ban.py
```
