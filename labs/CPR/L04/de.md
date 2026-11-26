# Lab CPR L04 — Sửa trực tiếp qua con trỏ và hàm divmod kiểm tra chia cho 0

Viết chương trình C chuẩn C11 đọc 4 số nguyên `x y num den` từ `stdin`.
Cài `swap_ptr(int *a, int *b)` kiểm tra `NULL` trước khi hoán đổi và `divmod_i(int x, int d, int *q, int *r)` (nếu `d == 0` in `divmod: ERR_ZERO`), in đúng 2 dòng:
1. `swap: x=<x sau hoán đổi> y=<y sau hoán đổi>`
2. `divmod: q=<q> r=<r>` (hoặc `divmod: ERR_ZERO`)

Chấm tự động:
```bash
bash labs/cham.sh CPR L04 duong_dan/bai_cua_ban.c
```

> Gợi ý đọc `stdin`: dùng toán tử lấy địa chỉ `&` vừa học với `scanf("%d %d %d %d", &x, &y, &num, &den) != 4` để kiểm tra đọc đủ 4 số nguyên.
