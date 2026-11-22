# Lab CS115 L38 — ICA: kiểm tra tính bất biến tỉ lệ và dấu của độ nhọn dư

Cho dãy đối xứng quanh 0 là `xs = [-1.5, -0.5, 0.5, 1.5]` (trung bình `m = 0`, phương sai `sd^2 = sum(x^2)/n`). Tính **độ nhọn dư** (`excess kurtosis = (1/n) * sum((x / sd)^4) - 3`) trên `xs` và trên dãy đổi dấu phóng đại `[-2.0 * x for x in xs]` để chứng minh bất biến theo dấu và tỉ lệ.

Định dạng đầu ra (2 dòng):
`kurt=<4 chữ số> scaled_neg_kurt=<4 chữ số>`
`sign_scale_invariant=<0 hoặc 1>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L38 duong_dan/bai_cua_ban.py
```
