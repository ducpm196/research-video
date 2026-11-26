# Lab SAR L10 — Độ trễ ghi đồng bộ liên vùng vs bất đồng bộ tại chỗ

Đọc `stdin` `one_way_ms=<int> local_ms=<int>`. Tính thời gian khứ hồi liên vùng `2 * one_way_ms` so với ghi cục bộ `local_ms` và tỉ số chênh lệch (chia nguyên `(2 * one_way_ms) // local_ms`).

In 3 dòng: `sync_rtt_ms=<d>`, `local_async_ms=<d>`, `latency_ratio=<d>x`.
Chấm tự động: `bash labs/cham.sh SAR L10 duong_dan/bai_cua_ban.py`
