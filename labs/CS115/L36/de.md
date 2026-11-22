# Lab CS115 L36 — AdaBoost trọng số alpha và Gradient Boosting (GBDT) sửa phần dư

Tính trọng số mô hình yếu trong AdaBoost `alpha = 0.5 * ln((1 - eps)/eps)` tại `eps = 0.2`. Sau đó với mô hình cây tăng cường theo gradient (**GBDT** — *Gradient Boosted Decision Trees*), xuất phát từ giá trị đích `y = 10.0`, dự đoán ban đầu `f = 0.0` và tốc độ học `lr = 0.5`: chạy 2 vòng cập nhật `f += lr * (y - f)` để lấy dự đoán và phần dư còn lại `y - f`.

Định dạng đầu ra (2 dòng):
`adaboost_alpha=<4 chữ số>`
`gbdt_f2=<2 chữ số> rem=<2 chữ số>`

Chấm tự động:
```bash
bash labs/cham.sh CS115 L36 duong_dan/bai_cua_ban.py
```
