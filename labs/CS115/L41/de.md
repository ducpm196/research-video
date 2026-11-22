# Lab CS115 L41 — Attention: softmax(QK^T / sqrt(d)) * V và kiểm tổng trọng số = 1

Tính cơ chế chú ý (`attention`) với số chiều `d = 4`, dãy điểm `QK^T = [2.0, 0.0]`, chia `sqrt(4) = 2`, chuẩn hoá mũ (softmax) theo hàng rồi lấy trung bình có trọng số với vector giá trị `V = [10.0, 2.0]`.

Định dạng đầu ra (2 dòng):
`weights=<danh sách 2 số làm tròn 4 chữ số> sum=<1 chữ số>`
`attn_out=<4 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L41 duong_dan/bai_cua_ban.py
```
