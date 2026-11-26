# Lab CPR L05 — Đo bước nhảy con trỏ và hàm mảng chỉ đọc const qua stdin

Viết chương trình C chuẩn C11 đọc `idx` và `n` (`0 <= idx < n <= 256`), tiếp theo đọc `n` số nguyên từ `stdin`.
Tính khoảng cách byte `(const char *)(v + idx) - (const char *)v` và tính tổng qua hàm `sum_ro(const int *a, size_t n)`, in đúng 2 dòng:
1. `offset=<khoảng cách byte>`
2. `sum=<tổng các phần tử>`

Chấm tự động:
```bash
bash labs/cham.sh CPR L05 duong_dan/bai_cua_ban.c
```
