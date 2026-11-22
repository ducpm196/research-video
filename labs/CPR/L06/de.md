# Lab CPR L06 — Cấp phát động, mở rộng realloc an toàn và giải phóng

Viết chương trình C chuẩn C11 cấp 3 phần tử `int` bằng `calloc`, gán `{10, 20, 30}`, mở rộng bằng `realloc` an toàn lên 5 phần tử thêm `{40, 50}`, tính tổng và `free`, in đúng 2 dòng:
1. `len=5 sum=150`
2. `freed=1`

Chấm tự động:
```bash
bash labs/cham.sh CPR L06 duong_dan/bai_cua_ban.c
```
