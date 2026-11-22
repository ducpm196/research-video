# Lab CS115 L28 — Cây quyết định: Entropy (dùng lôgarit tự nhiên ln), Gini và Độ lợi thông tin

Nút gốc gồm `(5 dương, 5 âm)` được chia 1 nút thành nhánh trái `(4, 1)` và phải `(1, 4)`. Dùng công thức **lôgarit tự nhiên `ln`** (`math.log`, khớp với bài giảng) để tính `H_root`, `H_split`, độ lợi thông tin `info_gain = H_root - H_split` và chỉ số `Gini` tại gốc.

Định dạng đầu ra (2 dòng):
`H_root=<3 chữ số> H_split=<4 chữ số>`
`info_gain=<4 chữ số> gini_root=<2 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L28 duong_dan/bai_cua_ban.py
```
