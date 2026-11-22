# Lab CS115 L24 — Lagrange cho ước lượng hợp lý cực đại (MLE) phân phối phân loại tổng = 1

Với số đếm `[6, 3, 1]`, thiết lập hàm Lagrange dưới ràng buộc đẳng thức tổng xác suất `sum(p) == 1` để tìm phân phối cực đại hàm hợp lý, rồi kiểm hệ số Lagrange `c_k / p_k = lambda` tại mọi lớp (danh sách `lambda` làm tròn 1 chữ số bằng `round(x, 1)`).

Định dạng đầu ra (3 dòng):
`p=<danh sách 3 số> sum=<1 chữ số>`
`lambda=<danh sách 3 số làm tròn 1 chữ số>`
`lagrange_equal=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L24 duong_dan/bai_cua_ban.py
```
