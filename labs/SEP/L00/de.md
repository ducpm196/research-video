# Lab SEP L00 — Tác động phần mềm quy mô lớn: lỗi 0.5% trên 500 000 người dùng và thử 150 người

Với một lỗi hiếm xảy ra với xác suất `p = 0.005`: tính số người bị ảnh hưởng khi phát hành cho `500 000` người dùng và xác suất thử nội bộ trên `n = 150` người mà gặp `0` ca lỗi `(1 - p)^n`.

Định dạng đầu ra (1 dòng):
`affected=<số nguyên> prob_zero_150=<3 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh SEP L00 duong_dan/bai_cua_ban.py
```
