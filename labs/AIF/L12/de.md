# Lab AIF L12 — Lặp giá trị bài toán bất định 3 ô thẳng hàng tới ô đích +1.0

Cho 3 ô `[0, 1, 2]` với ô đích `2` giá trị cố định `+1.0`. Mỗi bước nhận thưởng `r = -0.05`, hệ số chiết khấu `gamma = 0.9`; chọn đi tiến/lùi có xác suất tiến đúng hướng `0.7` và trượt đứng yên `0.3` (lấy `max` theo hai hành động). Chạy `30` vòng lặp giá trị cập nhật `u[0], u[1]`.

Định dạng đầu ra:
`U0=<3 chữ số> U1=<3 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh AIF L12 duong_dan/bai_cua_ban.py
```
