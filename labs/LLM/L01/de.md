# Lab LLM L01 — Độ hỗn loạn (perplexity) và làm trơn cộng 1

Đọc `stdin` `p=<float> steps=<int> ctx=<int> vocab=<int>`. Tính độ hỗn loạn `p^(-1/steps)` và xác suất chưa thấy sau làm trơn cộng 1 `(0 + 1) / (ctx + vocab)`.

In 1 dòng: `perplexity=<.3f> add1_unseen=<.3f>`.
Chấm tự động: `bash labs/cham.sh LLM L01 duong_dan/bai_cua_ban.py`
