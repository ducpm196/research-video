# Lab CS115 L23 — MLP: hàm ReLU chuẩn, bão hoà Sigmoid và chuẩn khởi tạo Xavier

Tính đạo hàm `sigmoid(10)*(1-sigmoid(10))`, áp dụng **hàm ReLU chuẩn** `max(0.0, v)` lên dãy `(-3, 0, 4)`, và tính độ lệch chuẩn khởi tạo Xavier `sqrt(2/(n_vao + n_ra))` với `n_vao = 64` (số đầu vào) và `n_ra = 16` (số đầu ra).

Định dạng đầu ra (3 dòng):
`dsigmoid_10=<6 chữ số dạng e>`
`relu=<danh sách 3 số>`
`xavier_std=<4 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L23 duong_dan/bai_cua_ban.py
```
