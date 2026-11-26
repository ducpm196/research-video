# Lab CSA L04 — Epsilon máy, cộng không kết hợp và kiểm FLT_EPSILON

Đọc từ `stdin` 2 số thực `big=1e16 delta=1.0`. So sánh kết quả `(big + delta) - big` với `delta + (big - big)` và kiểm tra `FLT_EPSILON < 1e-6f`.

In đúng 3 dòng: `left_assoc=<.1f>`, `right_assoc=<.1f>`, `eps_f32_lt_1e6=<0|1>`.
Chấm tự động: `bash labs/cham.sh CSA L04 duong_dan/bai_cua_ban.c`
