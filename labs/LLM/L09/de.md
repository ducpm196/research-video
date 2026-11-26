# Lab LLM L09 — Học sở thích Bradley-Terry (sigmoid hiệu điểm thưởng)

Đọc `stdin` `diff=<float>`. Tính xác suất chọn A qua `1 / (1 + exp(-diff))` và hàm mất mát `-ln(p)`.

In 1 dòng: `bt_prob=<.3f> bt_loss=<.3f>`.
Chấm tự động: `bash labs/cham.sh LLM L09 duong_dan/bai_cua_ban.py`
