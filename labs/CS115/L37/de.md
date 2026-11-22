# Lab CS115 L37 — Autoencoder tuyến tính: chiếu lên trục đơn vị (0.6, 0.8) và đo MSE tái tạo

Chiếu 4 điểm `[(3, 4), (5, 0), (-3, -4), (0, 5)]` lên vector đơn vị `u = (0.6, 0.8)` (`z = x*u[0] + y*u[1]`), rồi khôi phục `(z*u[0], z*u[1])` và đo trung bình theo 4 điểm của tổng bình phương sai lệch hai toạ độ `(dx^2 + dy^2)` (`MSE` chuẩn vectơ hai chiều trên 4 mẫu).

Định dạng đầu ra (2 dòng):
`latent=<danh sách 4 số làm tròn 3 chữ số>`
`recon_mse=<4 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L37 duong_dan/bai_cua_ban.py
```
