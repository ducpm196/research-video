# Lab HCI L06 — Công thức phát hiện lỗi khả dụng theo số người thử độc lập N

Với vấn đề có xác suất một người phát hiện được là `lam = 0.25` (tức xác suất một người bỏ sót `p_miss = 1 - lam = 0.75`): tính tỉ lệ lỗi phát hiện được `1 - (1 - lam)^N` (theo %) khi thử `N = 6` và `N = 12` người dùng độc lập.

Định dạng đầu ra (1 dòng):
`n6_pct=<1 chữ số>% n12_pct=<1 chữ số>%`

Chấm tự động:
```bash
bash labs/cham.sh HCI L06 duong_dan/bai_cua_ban.py
```
