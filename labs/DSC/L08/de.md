# Lab DSC L08 — Ước lượng cỡ mẫu thử nghiệm đối chứng cho hai tỉ lệ

Đọc `stdin` chuỗi `p1=<float> p2=<float>`. Áp dụng công thức cỡ mẫu mỗi nhóm hai thành phần với `pb = (p1 + p2) / 2`, `za = 1.959963984540054`, `zb = 0.8416212335729143`: `n_per_group = ceil(((za*sqrt(2*pb*(1-pb)) + zb*sqrt(p1*(1-p1)+p2*(1-p2))) / (p2 - p1))**2)`.

In 1 dòng: `n_per_group=<d>`.
Chấm tự động: `bash labs/cham.sh DSC L08 duong_dan/bai_cua_ban.py`
Gợi ý đọc đầu vào trong Python: dùng `sys.stdin.read().split()` tách từng cặp `khoá=giá_trị`.
