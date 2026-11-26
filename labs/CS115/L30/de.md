# Lab CS115 L30 — GMM & EM: tính độ thuộc về r_ik (bước E) và cập nhật trung bình (bước M)

Đọc `stdin` `m1=<f> m2=<f> w=<f> x=<f> x2=<f>`. Thực hiện bước E cho hai phân phối chuẩn `N(m1, 1)`, `N(m2, 1)` tại cả `x` lẫn `x2`, rồi chạy bước M cập nhật `mu1_new = (r1(x)*x + r1(x2)*x2) / (r1(x) + r1(x2))` trên cặp `[x, x2]`.

In 2 dòng chuẩn: `r1=<.6f> r2=<.6f>`, `sum=<.1f> mu1_new=<.4f>`.
Chấm tự động: `bash labs/cham.sh CS115 L30 duong_dan/bai_cua_ban.py`
