# Lab CSA L04 — Epsilon máy, cộng không kết hợp và kiểm FLT_EPSILON

Viết chương trình C chuẩn C11 minh họa cộng dấu phẩy động không kết hợp: `(1e16 + 1.0) - 1e16 == 0.0` so với `1.0 + (1e16 - 1e16) == 1.0`, và kiểm chứng hằng số `FLT_EPSILON` (ngưỡng epsilon máy 32-bit trong `<float.h>`) nhỏ hơn `1e-6`, in đúng 3 dòng:
1. `left_assoc=0.0`
2. `right_assoc=1.0`
3. `eps_f32_lt_1e6=1`

Chấm tự động:
```bash
bash labs/cham.sh CSA L04 duong_dan/bai_cua_ban.c
```
