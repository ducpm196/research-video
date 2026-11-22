# Lab CS115 L31 — NMF X ≈ A nhân B: quy tắc nhân giữ mọi phần tử không âm A >= 0, B >= 0

Theo đúng ký hiệu `X ≈ A·B` trong bài: cho vector cột `X_col = [4.0, 3.0]`, ma trận `A = [[2.0, 1.0], [1.0, 2.0]]` và vector hệ số khởi tạo `B = [1.0, 1.0]`. Thực hiện 2 bước cập nhật nhân `B <- B * (A^T X_col) / (A^T A B)` để thấy tổng bình phương sai lệch tái tạo `err = sum((X_col[r] - rec[r])^2)` trên 2 phần tử giảm dần qua từng bước mà mọi hệ số vẫn không âm.

Định dạng đầu ra (2 dòng):
`step1 B=<danh sách 2 số làm tròn 4 chữ số> err=<4 chữ số>`
`step2 B=<danh sách 2 số làm tròn 4 chữ số> err=<4 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L31 duong_dan/bai_cua_ban.py
```
