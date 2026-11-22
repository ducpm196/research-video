# Lab SEP L11 — Tổ hợp nhận dạng và mức phạt tối đa theo Luật Bảo vệ dữ liệu cá nhân (5% doanh thu)

Tính số tổ hợp phân biệt `2 * 5 * 365 * 100` (2 giới tính, 5 mã vùng, 365 ngày sinh, 100 năm), xác suất một người không trùng ai `(1 - 1/c)^(N - 1)` trong nhóm `N = 50 000` dân, và mức phạt tối đa `5%` doanh thu (Điều 8 Luật 91/2025) cho công ty doanh thu `200 tỉ đồng`.

Định dạng đầu ra (1 dòng):
`combos=<số nguyên> prob_unique=<3 chữ số> max_fine_B=<1 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh SEP L11 duong_dan/bai_cua_ban.py
```
