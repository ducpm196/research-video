# Lab SAR L08 — Tính tồn đọng hàng đợi và thời gian xả

Đọc `stdin` `peak_in=<int> proc=<int> secs=<int> low_in=<int>`. Tính tồn đọng tích lũy `(peak_in - proc) * secs` sau `secs` giây cao điểm, tốc độ xả ròng `proc - low_in` khi nguồn hạ xuống `low_in` và số phút xả sạch.

In 3 dòng (giữ nguyên tên khoá cố định): `backlog_30m=<d>`, `drain_net_per_s=<d>`, `drain_minutes=<.1f>`.
Chấm tự động: `bash labs/cham.sh SAR L08 duong_dan/bai_cua_ban.py`
