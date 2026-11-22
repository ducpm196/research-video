# Lab MLO L05 — Lệch huấn luyện–phục vụ khi không dùng chung công thức chuẩn hoá

Với giá trị đầu vào `x = 80.0` và độ lệch chuẩn `std = 10.0`, tính giá trị chuẩn hoá đúng khi dùng trung bình lúc huấn luyện (`mean_train = 55.0`) so với khi mã phục vụ viết lại nhầm sang trung bình (`mean_serve = 65.0`).

Định dạng đầu ra:
`z_train=<1 chữ số> z_serve_skew=<1 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh MLO L05 duong_dan/bai_cua_ban.py
```
