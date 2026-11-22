# Lab SAR L04 — Độ trễ trung bình theo tỉ lệ trúng bộ nhớ đệm (Cache Hit Rate)

Cho thời gian đọc bộ nhớ đệm (`Cache`) là `2 ms` và cơ sở dữ liệu (`DB`) là `80 ms`. Tính độ trễ trung bình `h * 2 + (1 - h) * 80` tại tỉ lệ trúng `85%` và `98%`, cùng hệ số tăng tốc ở `98%` so với khi không có bộ nhớ đệm.

Định dạng đầu ra (3 dòng):
`lat_85pct_ms=<2 chữ số>`
`lat_98pct_ms=<2 chữ số>`
`speedup_98=<1 chữ số>x`

Chấm tự động:
```bash
bash labs/cham.sh SAR L04 duong_dan/bai_cua_ban.py
```
