# Lab CLC L07 — Giảm ngưỡng mất dữ liệu (RPO) nhờ WAL

Đọc `stdin` `snap_hours=<int> wal_min=<int>`. Quy đổi RPO của chụp nhanh sang phút, đối chiếu với đẩy nhật ký `wal_min` và tính hệ số thu hẹp.

In 3 dòng: `snap_rpo_min=<d>`, `wal_rpo_min=<d>`, `rpo_cut=<d>x`.
Chấm tự động: `bash labs/cham.sh CLC L07 duong_dan/bai_cua_ban.py`
