# Lab CS115 L30 — GMM & EM: tính độ thuộc về r_ik (bước E) và cập nhật trung bình (bước M)

Cho hai thành phần chuẩn `N(0, 1)` và `N(4, 1)` có trọng số bằng nhau `0.5`: (1) thực hiện **bước E** tính **độ thuộc về** `r1`, `r2` tại điểm `x = 1.0`; (2) trên bộ 2 điểm `x_list = [1.0, 3.0]` (giả sử tại `3.0` đối xứng có `r1_b = 1 - r1`), thực hiện **bước M** cập nhật trung bình mới `mu1_new = (r1*1.0 + r1_b*3.0) / (r1 + r1_b)`.

Định dạng đầu ra (2 dòng):
`r1=<6 chữ số> r2=<6 chữ số>`
`sum=<1 chữ số> mu1_new=<4 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L30 duong_dan/bai_cua_ban.py
```
