# Lab DEN L13 — So sánh chi phí mạng của nối phát tán và nối xáo trộn

Đọc `stdin` `big_gb=<float> sm_gb=<float> nodes=<int>`. Tính tổng GB truyền qua mạng khi phát tán bảng nhỏ `(nodes - 1) * sm_gb` vs xáo trộn hai bảng `(big + sm) * (nodes - 1) / nodes`.

In 3 dòng: `broadcast_gb=<d>`, `shuffle_gb=<.2f>`, `network_saved_pct=<.1f>%`.
Chấm tự động: `bash labs/cham.sh DEN L13 duong_dan/bai_cua_ban.py`
