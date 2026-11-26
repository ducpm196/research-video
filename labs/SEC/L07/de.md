# Lab SEC L07 — Phát hiện lộ mẫu trên chế độ ECB vs mã khối CTR

Đọc `stdin` `b0=<str8> b1=<str8> n0=<str> n1=<str>`. Giả lập mã hóa khối đơn không nonce (ECB) so với chế độ bộ đếm gắn nonce riêng biệt `n0`, `n1` trên hai khối rõ `b0`, `b1`.

In đúng 3 dòng: `ecb_blocks_identical=<0|1>`, `ctr_blocks_identical=<0|1>`, `ecb_leaks_pattern=<0|1>`.
Chấm tự động: `bash labs/cham.sh SEC L07 duong_dan/bai_cua_ban.py`
