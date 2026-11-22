# Lab CLD L09 — Giảm đỉnh tải nhờ chọn tốt hơn trong hai (P2C)

Dùng `random.Random(99)` mô phỏng `15 000` yêu cầu vào `50` máy với giả định các yêu cầu nằm lại tích lũy trên máy theo đếm lượt. So sánh tải cực đại khi chọn ngẫu nhiên 1 máy (`rand1`) so với chọn ngẫu nhiên 2 lượt máy (`r.randrange(50)`, lấy lần lượt `a` rồi `b` có thể trùng) và lấy máy ít tải hơn (`p2c`).

Định dạng đầu ra (3 dòng):
`max_rand1=<số nguyên>`
`max_p2c=<số nguyên>`
`p2c_better=<1 hoặc 0>`

Chấm tự động:
```bash
bash labs/cham.sh CLD L09 duong_dan/bai_cua_ban.py
```
