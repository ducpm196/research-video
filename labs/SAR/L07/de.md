# Lab SAR L07 — Bộ giới hạn tốc độ thùng token (Token Bucket)

Thùng token bắt đầu đầy với sức chứa `cap = 30`, tốc độ nạp `rate = 15` token/giây. Mô phỏng theo 5 mốc `t = 0..4`: tại `t = 0` lấy ngay lượng token sẵn có trong thùng cho lượt khởi đầu, sau đó ở mỗi giây `t = 1..4` nạp thêm `rate = 15` token rồi tiếp nhận từ đợt `800` yêu cầu/giây trên tổng lưu lượng chuẩn `3 200` yêu cầu, đếm số yêu cầu được nhận (`accepted`) và bị từ chối bảo vệ hệ thống (`rejected`).

Định dạng đầu ra (3 dòng):
`accepted=<số>`
`rejected=<số>`
`accept_pct=<2 chữ số>%`

Chấm tự động:
```bash
bash labs/cham.sh SAR L07 duong_dan/bai_cua_ban.py
```
