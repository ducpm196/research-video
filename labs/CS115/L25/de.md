# Lab CS115 L25 — SVM lề lớn nhất 2/||w|| và hàm mất mát bản lề (hinge loss)

Với `w = (6, 8), b = -1` và điểm `(1, 1)` mang nhãn `y = -1`, tính độ dài vector trọng số `||w||`, lề hình học `2/||w||`, tích `y*(w·x + b)` và `hinge = max(0, 1 - y*(w·x + b))`.

Định dạng đầu ra (2 dòng):
`norm_w=<1 chữ số> margin=<2 chữ số>`
`y_pred_margin=<1 chữ số> hinge=<1 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L25 duong_dan/bai_cua_ban.py
```
