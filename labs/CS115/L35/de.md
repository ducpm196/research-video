# Lab CS115 L35 — RNN: suy giảm / bùng nổ gradient qua 20 bước và cắt ngưỡng clip = 5.0

Tính `0.8^20` (tắt dần), `1.2^20` (bùng nổ) và độ lớn chuẩn gradient sau khi áp dụng phép cắt trần `clip = 5.0` (nếu vượt ngưỡng `5.0` thì giữ ở `5.0`).

Định dạng đầu ra (2 dòng):
`vanish_20=<5 chữ số> explode_20=<2 chữ số>`
`clipped_norm=<2 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L35 duong_dan/bai_cua_ban.py
```
