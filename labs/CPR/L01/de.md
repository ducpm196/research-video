# Lab CPR L01 — Kiểm tra quay vòng uint8_t và chặn tràn int32_t qua stdin

Viết chương trình C chuẩn C11 đọc 6 số nguyên từ `stdin`: `u_init u_add a1 b1 a2 b2`.
1. Tính tổng `uint8_t` quay vòng `(uint8_t)(u_init + u_add)` → `wrap=<giá trị>`
2. Cộng có kiểm tra `a1 + b1` trên `int32_t` (chặn cả tràn dương và tràn âm, không gây hành vi không xác định) → `add1=<tổng hoặc OVERFLOW>`
3. Cộng có kiểm tra `a2 + b2` trên `int32_t` → `add2=<tổng hoặc OVERFLOW>`

Chấm tự động:
```bash
bash labs/cham.sh CPR L01 duong_dan/bai_cua_ban.c
```

> Gợi ý đọc `stdin`: `unsigned ui = 0, ua = 0; int32_t a1, b1, a2, b2; if (scanf("%u %u %d %d %d %d", &ui, &ua, &a1, &b1, &a2, &b2) != 6) return 1;`.
