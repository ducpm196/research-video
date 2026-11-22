# Lab DSC L08 — Ước lượng cỡ mẫu thử nghiệm có đối chứng cho mức tăng 8% lên 9%

Tính cỡ mẫu tối thiểu mỗi nhóm theo công thức phân phối chuẩn với trung bình gộp `pb = (p1 + p2)/2`: `(za*căn(2*pb*(1-pb)) + zb*căn(p1*(1-p1)+p2*(1-p2)))^2 / (p2 - p1)^2` làm tròn lên (với `p1=0.08, p2=0.09, za=1.959964, zb=0.841621`).

Định dạng đầu ra:
`n_per_group=<số nguyên>`

Chấm tự động:
```bash
bash labs/cham.sh DSC L08 duong_dan/bai_cua_ban.py
```
