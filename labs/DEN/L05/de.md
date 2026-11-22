# Lab DEN L05 — Chia phân vùng theo ngày để khoanh vùng truy vấn

Một bảng nhật ký lưu `30` ngày liên tiếp, mỗi ngày phát sinh `50 MB` (`MB = mê-ga-byte`). Tính lượng dữ liệu (`MB`) phải quét cho truy vấn chỉ lọc đúng `2` ngày khi có phân vùng theo ngày so với quét toàn bảng.

Định dạng đầu ra (3 dòng):
`full_scan_mb=<số nguyên>`
`pruned_scan_mb=<số nguyên>`
`saved_pct=<1 chữ số>%`

Chấm tự động:
```bash
bash labs/cham.sh DEN L05 duong_dan/bai_cua_ban.py
```
