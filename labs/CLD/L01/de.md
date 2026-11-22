# Lab CLD L01 — So sánh bộ nhớ (RAM) nền giữa container và máy ảo

Trên một máy chủ chạy `12` ứng dụng, mỗi ứng dụng tự chiếm `40 MB` (`MB = mê-ga-byte`). Container dùng chung nhân hệ điều hành (`0 MB` nhân thêm), còn mỗi máy ảo (`VM`) tốn riêng `450 MB` cho hệ điều hành khách. Tính tổng RAM (tính theo `MB` và phần dư tính bằng `GB`, `1 GB = 1000 MB`).

Định dạng đầu ra (3 dòng):
`container_mb=<số nguyên>`
`vm_mb=<số nguyên>`
`vm_extra_gb=<2 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CLD L01 duong_dan/bai_cua_ban.py
```
