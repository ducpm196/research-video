# Lab CS115 L39 — Thực hành 1 bước cập nhật Q-learning với alpha = 0.25, gamma = 0.8

Thực hiện một bước cập nhật công thức `Q(s, a) <- Q + alpha * (r + gamma * maxQ' - Q)` với các tham số mới `Q = 1.0`, tốc độ học `alpha = 0.25`, phần thưởng ngay `r = 2.0`, hệ số chiết khấu `gamma = 0.8`, và giá trị tốt nhất tại trạng thái kế tiếp `maxQ' = 8.0`.

Định dạng đầu ra (2 dòng):
`target=<1 chữ số> td_err=<1 chữ số>`
`q_new=<2 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L39 duong_dan/bai_cua_ban.py
```
