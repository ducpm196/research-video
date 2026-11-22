# Lab CLC L07 — Giảm ngưỡng mất dữ liệu (RPO) nhờ nhật ký giao dịch WAL

So sánh điểm khôi phục mục tiêu (`RPO`) khi chỉ chụp nhanh (`snapshot`) mỗi `12` giờ (`720` phút) với phương án đẩy thêm nhật ký giao dịch (`WAL`) mỗi `2` phút, và tính hệ số thu hẹp cửa sổ mất dữ liệu.

Định dạng đầu ra (3 dòng):
`snap_rpo_min=<số>`
`wal_rpo_min=<số>`
`rpo_cut=<số>x`

Chấm tự động:
```bash
bash labs/cham.sh CLC L07 duong_dan/bai_cua_ban.py
```
