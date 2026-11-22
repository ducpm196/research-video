# Lab CS115 L34 — CNN: kích thước bản đồ đặc trưng đầu ra và tổng số tham số tích chập

Cho ảnh vuông `28 × 28`, bộ lọc vuông cạnh `K = 5` (thay vì `3` trong bài), đệm `P = 2`, bước nhảy `S = 2`, số kênh vào `C_vao = 3`, số kênh ra `C_ra = 8`, mỗi bộ lọc có cộng 1 hệ số tự do (bias). Tính kích thước phẳng trải của bản đồ đặc trưng đầu ra (`w × w × C_ra`) và tổng số tham số (trọng số và hệ số tự do) của lớp tích chập.

Định dạng đầu ra (2 dòng):
`out_dim=<w>x<w>x8=<tổng số chiều>`
`conv_params=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L34 duong_dan/bai_cua_ban.py
```
